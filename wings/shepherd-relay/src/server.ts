import express, { Request, Response, NextFunction } from 'express';
import { EventEmitter } from 'events';
import { v4 as uuidv4 } from 'uuid';
import fs from 'fs';
import path from 'path';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';

const app = express();

// ── Security Middleware ──────────────────────────────────────────────
app.use(helmet());

// CORS: default deny all, allow configured origin, or wildcard in dev
const corsOrigin = process.env.RELAY_CORS_ORIGIN;
app.use(cors({
  origin: corsOrigin === '*' ? true : corsOrigin || false,
  credentials: true
}));

// Rate limiting: 100 requests per 15-minute window
app.use(rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req, res) => {
    log(`⛔ Rate limit exceeded: ${req.ip}`);
    res.status(429).json({ error: 'Too many requests, please slow down.' });
  }
}));

app.use(express.json({ limit: '128kb' }));

// ── Configuration ────────────────────────────────────────────────────
const PORT = process.env.RELAY_PORT ? parseInt(process.env.RELAY_PORT) : 7777;
const DATA_DIR = process.env.RELAY_DATA_DIR || path.join(__dirname, '../data');
const TASKS_FILE = path.join(DATA_DIR, 'tasks.jsonl');
const MESSAGES_FILE = path.join(DATA_DIR, 'messages.jsonl');
const REQ_LOG = process.env.RELAY_REQ_LOG === '1' || process.env.RELAY_REQ_LOG === 'true';

// ── In-memory state ─────────────────────────────────────────────────
const clients = new Map<string, express.Response>(); // agent-id → SSE response
const presence = new Map<string, { lastSeen: number; status: string; task: string | null }>();

// Task cache: in-memory Map with async disk flush (fixes race condition)
const taskCache = new Map<string, TaskEntry>();
let taskFlushTimer: NodeJS.Timeout | null = null;

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

// Load existing tasks into memory cache on startup
function loadTasksIntoCache() {
  const tasks = readJsonl<TaskEntry>(TASKS_FILE);
  for (const task of tasks) {
    taskCache.set(task.id, task);
  }
  log(`📂 Loaded ${tasks.length} tasks into memory cache`);
}
loadTasksIntoCache();

// Async flush task cache to disk (debounced)
function flushTasks() {
  if (taskFlushTimer) clearTimeout(taskFlushTimer);
  taskFlushTimer = setTimeout(() => {
    const tasks = Array.from(taskCache.values());
    const data = tasks.map(t => JSON.stringify(t)).join('\n') + '\n';
    fs.writeFileSync(TASKS_FILE, data, 'utf-8');
    log(`💾 Task cache flushed to disk (${tasks.length} tasks)`);
  }, 100);
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

// ── Validation Helpers ───────────────────────────────────────────────
const ALLOWED_TYPES = ['message', 'task', 'status', 'decision', 'presence'];
const ALLOWED_PRIORITIES = ['low', 'medium', 'high', 'critical'];
const ALLOWED_STATUSES = ['todo', 'in-progress', 'done'];
const ID_REGEX = /^[a-zA-Z0-9-]{1,64}$/;

function isValidId(id: string): boolean {
  return typeof id === 'string' && ID_REGEX.test(id);
}

function hasLineBreaks(str: string): boolean {
  return typeof str === 'string' && /[\n\r]/.test(str);
}

function sanitizeError(field: string): { error: string } {
  return { error: `Invalid or unsafe value for "${field}"` };
}

// ── Auth Middleware ──────────────────────────────────────────────────
const AUTH_TOKEN = process.env.RELAY_API_TOKEN;

function requireAuth(req: Request, res: Response, next: NextFunction) {
  // If no token configured, skip auth (dev mode)
  if (!AUTH_TOKEN) {
    return next();
  }

  const header = req.headers.authorization || '';
  const match = header.match(/^Bearer\s+(.+)$/i);
  const token = match ? match[1] : null;

  if (!token || token !== AUTH_TOKEN) {
    log(`🔒 Auth failure: ${req.method} ${req.path} from ${req.ip} — invalid or missing token`);
    return res.status(401).json({ error: 'Unauthorized — invalid or missing Bearer token' });
  }

  next();
}

function requireStreamAuth(req: Request, res: Response, next: NextFunction) {
  // If no token configured, skip auth (dev mode)
  if (!AUTH_TOKEN) {
    return next();
  }

  const token = req.query.token as string | undefined;
  if (!token || token !== AUTH_TOKEN) {
    log(`🔒 SSE auth failure: ${req.path} from ${req.ip} — invalid or missing token`);
    return res.status(401).json({ error: 'Unauthorized — invalid or missing token query parameter' });
  }

  next();
}

// ── Request Logging ──────────────────────────────────────────────────
if (REQ_LOG) {
  app.use((req: Request, res: Response, next: NextFunction) => {
    const agentId = req.headers['x-agent-id'] as string || req.params.agentId || 'unknown';
    log(`📡 ${req.method} ${req.path} — agent=${agentId} ip=${req.ip}`);
    next();
  });
}

// ── SSE Endpoint ──────────────────────────────────────────────────────
app.get('/stream/:agentId', requireStreamAuth, (req, res) => {
  const agentId = req.params.agentId;

  // Validate agentId format
  if (!isValidId(agentId)) {
    return res.status(400).json({ error: 'Invalid agentId — alphanumeric and hyphens only, max 64 chars' });
  }

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

  // Replay recent relevant message history (only messages directed to this agent or broadcast)
  try {
    const history = readJsonl<TeamMessage>(MESSAGES_FILE);
    const recent = history
      .filter(m => m.to === 'all' || m.to === agentId)
      .slice(-50); // last 50 relevant messages
    for (const msg of recent) {
      res.write(`data: ${JSON.stringify(msg)}\n\n`);
    }
    if (recent.length > 0) {
      log(`📜 Replayed ${recent.length} relevant messages to ${agentId}`);
    }
  } catch (e) {
    log(`⚠️ Failed to replay history to ${agentId}: ${e}`);
  }

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
app.post('/message', requireAuth, (req, res) => {
  const { from, to, content, type = 'message', metadata = {} } = req.body;

  if (!from || !content) {
    return res.status(400).json({ error: 'Missing "from" or "content"' });
  }

  // Validate IDs
  if (!isValidId(from)) {
    return res.status(400).json(sanitizeError('from'));
  }
  if (to && to !== 'all' && !isValidId(to)) {
    return res.status(400).json(sanitizeError('to'));
  }

  // Validate type
  if (!ALLOWED_TYPES.includes(type)) {
    return res.status(400).json({ error: `Invalid "type" — must be one of: ${ALLOWED_TYPES.join(', ')}` });
  }

  // Sanitize content: reject line breaks
  if (hasLineBreaks(content)) {
    return res.status(400).json({ error: '"content" cannot contain newlines or carriage returns' });
  }

  // Cap content at 10KB
  if (content.length > 10 * 1024) {
    return res.status(400).json({ error: '"content" exceeds maximum length of 10KB' });
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
app.post('/broadcast', requireAuth, (req, res) => {
  const { from, content, type = 'message', metadata = {} } = req.body;

  if (!from || !content) {
    return res.status(400).json({ error: 'Missing "from" or "content"' });
  }

  if (!isValidId(from)) {
    return res.status(400).json(sanitizeError('from'));
  }

  if (!ALLOWED_TYPES.includes(type)) {
    return res.status(400).json({ error: `Invalid "type" — must be one of: ${ALLOWED_TYPES.join(', ')}` });
  }

  if (hasLineBreaks(content)) {
    return res.status(400).json({ error: '"content" cannot contain newlines or carriage returns' });
  }

  if (content.length > 10 * 1024) {
    return res.status(400).json({ error: '"content" exceeds maximum length of 10KB' });
  }

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
  let tasks = Array.from(taskCache.values());
  if (statusFilter && ALLOWED_STATUSES.includes(statusFilter)) {
    tasks = tasks.filter(t => t.status === statusFilter);
  }
  // Sort by createdAt desc
  tasks.sort((a, b) => b.createdAt - a.createdAt);
  res.json({ tasks, count: tasks.length });
});

// ── POST /tasks ───────────────────────────────────────────────────────
app.post('/tasks', requireAuth, (req, res) => {
  const { title, description, priority = 'medium', createdBy } = req.body;

  if (!title) {
    return res.status(400).json({ error: 'Missing "title"' });
  }

  // Validate priority
  if (!ALLOWED_PRIORITIES.includes(priority)) {
    return res.status(400).json({ error: `Invalid "priority" — must be one of: ${ALLOWED_PRIORITIES.join(', ')}` });
  }

  // Sanitize title: reject line breaks
  if (hasLineBreaks(title)) {
    return res.status(400).json({ error: '"title" cannot contain newlines or carriage returns' });
  }

  // Cap title at 200 chars
  if (title.length > 200) {
    return res.status(400).json({ error: '"title" exceeds maximum length of 200 characters' });
  }

  // Sanitize and cap description
  let desc = description || '';
  if (hasLineBreaks(desc)) {
    return res.status(400).json({ error: '"description" cannot contain newlines or carriage returns' });
  }
  if (desc.length > 2 * 1024) {
    return res.status(400).json({ error: '"description" exceeds maximum length of 2KB' });
  }

  if (createdBy && !isValidId(createdBy)) {
    return res.status(400).json(sanitizeError('createdBy'));
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
    description: desc
  };

  taskCache.set(task.id, task);
  flushTasks();

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
app.post('/claim-task', requireAuth, (req, res) => {
  const { taskId, agentId } = req.body;
  if (!taskId || !agentId) {
    return res.status(400).json({ error: 'Missing taskId or agentId' });
  }

  if (!isValidId(agentId)) {
    return res.status(400).json(sanitizeError('agentId'));
  }

  const task = taskCache.get(taskId);
  if (!task) {
    return res.status(404).json({ error: 'Task not found' });
  }
  if (task.status !== 'todo') {
    return res.status(409).json({ error: `Task already ${task.status}` });
  }

  task.status = 'in-progress';
  task.claimedBy = agentId;
  task.claimedAt = now();

  flushTasks();

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
app.post('/complete-task', requireAuth, (req, res) => {
  const { taskId, agentId, summary } = req.body;
  if (!taskId || !agentId) {
    return res.status(400).json({ error: 'Missing taskId or agentId' });
  }

  if (!isValidId(agentId)) {
    return res.status(400).json(sanitizeError('agentId'));
  }

  const task = taskCache.get(taskId);
  if (!task) {
    return res.status(404).json({ error: 'Task not found' });
  }

  task.status = 'done';
  task.completedAt = now();

  flushTasks();

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
  const toFilter = req.query.to as string | undefined;
  let messages = readJsonl<TeamMessage>(MESSAGES_FILE);
  if (since > 0) {
    messages = messages.filter(m => (m.metadata.timestamp || 0) > since);
  }
  if (toFilter) {
    messages = messages.filter(m => m.to === 'all' || m.to === toFilter);
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
  log(`🔒 Auth: ${AUTH_TOKEN ? 'enabled (Bearer token)' : 'disabled (dev mode)'}`);
  log(`🌐 CORS: ${corsOrigin || 'deny all'}`);
  log(`📡 Endpoints:`);
  log(`   GET  /stream/:agentId     — SSE stream (token via ?token=)`);
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
