import express from 'express';
import { EventEmitter } from 'events';
import { v4 as uuidv4 } from 'uuid';
import fs from 'fs';
import path from 'path';

const app = express();
app.use(express.json());

// ── Configuration ────────────────────────────────────────────────────
const PORT = process.env.RELAY_PORT ? parseInt(process.env.RELAY_PORT) : 7777;
const DATA_DIR = process.env.RELAY_DATA_DIR || path.join(__dirname, '../data');
const TASKS_FILE = path.join(DATA_DIR, 'tasks.jsonl');
const MESSAGES_FILE = path.join(DATA_DIR, 'messages.jsonl');

// ── In-memory state ─────────────────────────────────────────────────
const clients = new Map<string, express.Response>(); // agent-id → SSE response
const presence = new Map<string, { lastSeen: number; status: string; task: string | null }>();

// Ensure data dir exists
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// ── Types ─────────────────────────────────────────────────────────────
interface TeamMessage {
  id: string;
  from: string;
  to: string | 'all';
  type: 'message' | 'task' | 'status' | 'decision' | 'presence';
  content: string;
  metadata: {
    taskId?: string;
    priority?: 'low' | 'medium' | 'high' | 'critical';
    timestamp: number;
    [key: string]: any;
  };
}

interface TaskEntry {
  id: string;
  title: string;
  status: 'todo' | 'in-progress' | 'done';
  claimedBy: string | null;
  priority: 'low' | 'medium' | 'high' | 'critical';
  createdAt: number;
  claimedAt: number | null;
  completedAt: number | null;
  description: string;
}

// ── Helpers ───────────────────────────────────────────────────────────
function now() {
  return Math.floor(Date.now() / 1000);
}

function log(msg: string) {
  console.log(`[${new Date().toISOString()}] ${msg}`);
}

function appendJsonl(filePath: string, obj: any) {
  const line = JSON.stringify(obj) + '\n';
  fs.appendFileSync(filePath, line, 'utf-8');
}

function readJsonl<T>(filePath: string): T[] {
  if (!fs.existsSync(filePath)) return [];
  const lines = fs.readFileSync(filePath, 'utf-8').trim().split('\n').filter(Boolean);
  return lines.map(line => JSON.parse(line));
}

function broadcast(msg: TeamMessage) {
  const data = `data: ${JSON.stringify(msg)}\n\n`;
  for (const [agentId, res] of clients.entries()) {
    if (msg.to === 'all' || msg.to === agentId) {
      res.write(data);
    }
  }
}

function sendTo(agentId: string, msg: TeamMessage) {
  const res = clients.get(agentId);
  if (res) {
    res.write(`data: ${JSON.stringify(msg)}\n\n`);
  }
}

// ── SSE Endpoint ──────────────────────────────────────────────────────
app.get('/stream/:agentId', (req, res) => {
  const agentId = req.params.agentId;

  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  clients.set(agentId, res);
  presence.set(agentId, { lastSeen: now(), status: 'active', task: null });

  log(`🔌 ${agentId} connected (${clients.size} active)`);

  // Send welcome
  const welcome: TeamMessage = {
    id: uuidv4(),
    from: 'relay',
    to: agentId,
    type: 'presence',
    content: `Welcome, ${agentId}! Connected to Shepherd Team Relay.`,
    metadata: { timestamp: now(), activeAgents: clients.size }
  };
  res.write(`data: ${JSON.stringify(welcome)}\n\n`);

  // Broadcast join
  const joinMsg: TeamMessage = {
    id: uuidv4(),
    from: 'relay',
    to: 'all',
    type: 'presence',
    content: `${agentId} joined the team.`,
    metadata: { timestamp: now(), agentId }
  };
  broadcast(joinMsg);

  req.on('close', () => {
    clients.delete(agentId);
    presence.set(agentId, { lastSeen: now(), status: 'offline', task: null });
    log(`🔌 ${agentId} disconnected (${clients.size} active)`);

    const leaveMsg: TeamMessage = {
      id: uuidv4(),
      from: 'relay',
      to: 'all',
      type: 'presence',
      content: `${agentId} left.`,
      metadata: { timestamp: now(), agentId }
    };
    broadcast(leaveMsg);
  });
});

// ── POST /message ─────────────────────────────────────────────────────
app.post('/message', (req, res) => {
  const { from, to, content, type = 'message', metadata = {} } = req.body;

  if (!from || !content) {
    return res.status(400).json({ error: 'Missing "from" or "content"' });
  }

  const msg: TeamMessage = {
    id: uuidv4(),
    from,
    to: to || 'all',
    type: type as any,
    content,
    metadata: { ...metadata, timestamp: now() }
  };

  appendJsonl(MESSAGES_FILE, msg);
  broadcast(msg);

  log(`💬 ${from} → ${msg.to}: ${content.slice(0, 60)}`);
  res.json({ success: true, messageId: msg.id });
});

// ── POST /broadcast ───────────────────────────────────────────────────
app.post('/broadcast', (req, res) => {
  const { from, content, type = 'message', metadata = {} } = req.body;

  const msg: TeamMessage = {
    id: uuidv4(),
    from,
    to: 'all',
    type: type as any,
    content,
    metadata: { ...metadata, timestamp: now() }
  };

  appendJsonl(MESSAGES_FILE, msg);
  broadcast(msg);

  log(`📢 ${from} → all: ${content.slice(0, 60)}`);
  res.json({ success: true, messageId: msg.id });
});

// ── GET /status ───────────────────────────────────────────────────────
app.get('/status', (req, res) => {
  const status: Record<string, any> = {};
  for (const [agentId, pres] of presence.entries()) {
    status[agentId] = {
      ...pres,
      online: clients.has(agentId)
    };
  }
  res.json({ agents: status, activeConnections: clients.size });
});

// ── GET /tasks ────────────────────────────────────────────────────────
app.get('/tasks', (req, res) => {
  const statusFilter = req.query.status as string | undefined;
  let tasks = readJsonl<TaskEntry>(TASKS_FILE);
  if (statusFilter) {
    tasks = tasks.filter(t => t.status === statusFilter);
  }
  res.json({ tasks, count: tasks.length });
});

// ── POST /tasks ───────────────────────────────────────────────────────
app.post('/tasks', (req, res) => {
  const { title, description, priority = 'medium', createdBy } = req.body;

  if (!title) {
    return res.status(400).json({ error: 'Missing "title"' });
  }

  const task: TaskEntry = {
    id: uuidv4(),
    title,
    status: 'todo',
    claimedBy: null,
    priority,
    createdAt: now(),
    claimedAt: null,
    completedAt: null,
    description: description || ''
  };

  appendJsonl(TASKS_FILE, task);

  const msg: TeamMessage = {
    id: uuidv4(),
    from: createdBy || 'relay',
    to: 'all',
    type: 'task',
    content: `New task: ${title}`,
    metadata: { taskId: task.id, priority, timestamp: now() }
  };
  broadcast(msg);

  log(`📝 Task created: ${title} (${task.id})`);
  res.json({ success: true, task });
});

// ── POST /claim-task ──────────────────────────────────────────────────
app.post('/claim-task', (req, res) => {
  const { taskId, agentId } = req.body;
  if (!taskId || !agentId) {
    return res.status(400).json({ error: 'Missing taskId or agentId' });
  }

  const tasks = readJsonl<TaskEntry>(TASKS_FILE);
  const task = tasks.find(t => t.id === taskId);
  if (!task) {
    return res.status(404).json({ error: 'Task not found' });
  }
  if (task.status !== 'todo') {
    return res.status(409).json({ error: `Task already ${task.status}` });
  }

  task.status = 'in-progress';
  task.claimedBy = agentId;
  task.claimedAt = now();

  // Re-write tasks file (inefficient but simple for now)
  fs.writeFileSync(TASKS_FILE, tasks.map(t => JSON.stringify(t)).join('\n') + '\n');

  // Update presence
  const pres = presence.get(agentId);
  if (pres) {
    pres.task = task.title;
    presence.set(agentId, pres);
  }

  const msg: TeamMessage = {
    id: uuidv4(),
    from: agentId,
    to: 'all',
    type: 'task',
    content: `${agentId} claimed task: ${task.title}`,
    metadata: { taskId, timestamp: now() }
  };
  broadcast(msg);

  log(`✋ ${agentId} claimed: ${task.title}`);
  res.json({ success: true, task });
});

// ── POST /complete-task ────────────────────────────────────────────────
app.post('/complete-task', (req, res) => {
  const { taskId, agentId, summary } = req.body;
  if (!taskId || !agentId) {
    return res.status(400).json({ error: 'Missing taskId or agentId' });
  }

  const tasks = readJsonl<TaskEntry>(TASKS_FILE);
  const task = tasks.find(t => t.id === taskId);
  if (!task) {
    return res.status(404).json({ error: 'Task not found' });
  }

  task.status = 'done';
  task.completedAt = now();

  fs.writeFileSync(TASKS_FILE, tasks.map(t => JSON.stringify(t)).join('\n') + '\n');

  // Update presence
  const pres = presence.get(agentId);
  if (pres) {
    pres.task = null;
    presence.set(agentId, pres);
  }

  const msg: TeamMessage = {
    id: uuidv4(),
    from: agentId,
    to: 'all',
    type: 'task',
    content: `${agentId} completed: ${task.title}. ${summary || ''}`,
    metadata: { taskId, timestamp: now(), summary }
  };
  broadcast(msg);

  log(`✅ ${agentId} completed: ${task.title}`);
  res.json({ success: true, task });
});

// ── GET /messages ─────────────────────────────────────────────────────
app.get('/messages', (req, res) => {
  const since = req.query.since ? parseInt(req.query.since as string) : 0;
  let messages = readJsonl<TeamMessage>(MESSAGES_FILE);
  if (since > 0) {
    messages = messages.filter(m => (m.metadata.timestamp || 0) > since);
  }
  res.json({ messages, count: messages.length });
});

// ── Health ────────────────────────────────────────────────────────────
app.get('/health', (req, res) => {
  res.json({ status: 'ok', agents: clients.size, uptime: process.uptime() });
});

// ── Start ─────────────────────────────────────────────────────────────
app.listen(PORT, () => {
  log(`🚀 Shepherd Relay running on port ${PORT}`);
  log(`📁 Data directory: ${DATA_DIR}`);
  log(`📡 Endpoints:`);
  log(`   GET  /stream/:agentId     — SSE stream`);
  log(`   POST /message            — Send message`);
  log(`   POST /broadcast          — Broadcast to all`);
  log(`   GET  /status             — Team status`);
  log(`   GET  /tasks              — Task board`);
  log(`   POST /tasks              — Create task`);
  log(`   POST /claim-task         — Claim task`);
  log(`   POST /complete-task      — Complete task`);
  log(`   GET  /messages           — Message history`);
  log(`   GET  /health             — Health check`);
});
