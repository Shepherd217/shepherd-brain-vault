import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import type { Task, Agent, DashboardEvent } from "@/types";

const DATA_DIR = join(process.cwd(), "data");
const TASKS_FILE = join(DATA_DIR, "tasks.json");
const AGENTS_FILE = join(DATA_DIR, "agents.json");
const EVENTS_FILE = join(DATA_DIR, "events.json");

// Ensure data directory exists
try {
  mkdirSync(DATA_DIR, { recursive: true });
} catch (_) {}

function loadJson<T>(path: string, defaultValue: T): T {
  try {
    if (existsSync(path)) {
      const content = readFileSync(path, "utf-8");
      const parsed = JSON.parse(content);
      // Restore Date objects from ISO strings
      return reviveDates(parsed);
    }
  } catch (_) {}
  return defaultValue;
}

function saveJson<T>(path: string, data: T): void {
  try {
    writeFileSync(path, JSON.stringify(data, null, 2));
  } catch (_) {}
}

function reviveDates(obj: unknown): unknown {
  if (obj === null || typeof obj !== "object") return obj;
  if (Array.isArray(obj)) {
    return obj.map(reviveDates);
  }
  const result: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(obj as Record<string, unknown>)) {
    if (typeof value === "string" && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/.test(value)) {
      result[key] = new Date(value);
    } else if (typeof value === "object") {
      result[key] = reviveDates(value);
    } else {
      result[key] = value;
    }
  }
  return result;
}

// ── Tasks ──────────────────────────────────────────────────────────────────
export function getTasks(): Task[] {
  return loadJson<Task[]>(TASKS_FILE, []);
}

export function saveTasks(tasks: Task[]): void {
  saveJson(TASKS_FILE, tasks);
}

export function getTaskById(id: string): Task | undefined {
  return getTasks().find((t) => t.id === id);
}

export function createTask(task: Task): Task {
  const tasks = getTasks();
  tasks.push(task);
  saveTasks(tasks);
  return task;
}

export function updateTask(id: string, updates: Partial<Task>): Task | null {
  const tasks = getTasks();
  const index = tasks.findIndex((t) => t.id === id);
  if (index === -1) return null;
  tasks[index] = { ...tasks[index], ...updates };
  saveTasks(tasks);
  return tasks[index];
}

export function deleteTask(id: string): boolean {
  const tasks = getTasks();
  const index = tasks.findIndex((t) => t.id === id);
  if (index === -1) return false;
  tasks.splice(index, 1);
  saveTasks(tasks);
  return true;
}

// ── Agents ─────────────────────────────────────────────────────────────────
export function getAgents(): Agent[] {
  return loadJson<Agent[]>(AGENTS_FILE, []);
}

export function saveAgents(agents: Agent[]): void {
  saveJson(AGENTS_FILE, agents);
}

export function getAgentById(id: string): Agent | undefined {
  return getAgents().find((a) => a.id === id);
}

export function upsertAgent(agent: Agent): Agent {
  const agents = getAgents();
  const index = agents.findIndex((a) => a.id === agent.id);
  if (index === -1) {
    agents.push(agent);
  } else {
    agents[index] = agent;
  }
  saveAgents(agents);
  return agent;
}

// ── Zombie Detection ────────────────────────────────────────────────────────
const ZOMBIE_THRESHOLD_MS = 5 * 60 * 1000; // 5 minutes

export function detectZombies(): Agent[] {
  const now = Date.now();
  const agents = getAgents();
  const zombies: Agent[] = [];

  for (const agent of agents) {
    const lastSeen = new Date(agent.updatedAt).getTime();
    if (agent.status !== "offline" && now - lastSeen > ZOMBIE_THRESHOLD_MS) {
      agent.status = "offline";
      zombies.push(agent);
    }
  }

  if (zombies.length > 0) {
    saveAgents(agents);
  }

  return zombies;
}

// ── Task Reclaim ────────────────────────────────────────────────────────────
export function reclaimTasksFromZombies(): Task[] {
  const zombies = detectZombies();
  if (zombies.length === 0) return [];

  const reclaimed: Task[] = [];
  const zombieIds = new Set(zombies.map((z) => z.id));

  for (const zombie of zombies) {
    if (!zombie.currentTask) continue;

    const task = getTaskById(zombie.currentTask);
    if (task && task.status === "doing" && zombieIds.has(task.owner || "")) {
      const updated = updateTask(task.id, {
        status: "todo",
        owner: null,
        error: `Reclaimed from zombie agent ${zombie.name} (offline >5min)`,
      });
      if (updated) reclaimed.push(updated);
    }

    // Clear agent's current task
    upsertAgent({ ...zombie, currentTask: null });
  }

  return reclaimed;
}

// ── Events ─────────────────────────────────────────────────────────────────
export function getEvents(): DashboardEvent[] {
  return loadJson<DashboardEvent[]>(EVENTS_FILE, []);
}

export function saveEvents(events: DashboardEvent[]): void {
  saveJson(EVENTS_FILE, events);
}

export function appendEvent(event: DashboardEvent): void {
  const events = getEvents();
  events.push(event);
  // Keep last 1000 events
  if (events.length > 1000) {
    events.splice(0, events.length - 1000);
  }
  saveEvents(events);
}
