import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import type { Task } from "@/types";

const DATA_DIR = join(process.cwd(), "data");
const GOALS_FILE = join(DATA_DIR, "goals.json");

interface GoalLock {
  agentId: string;
  taskId: string;
  lockedAt: string;
  notes: string | null;
}

function loadGoals(): Record<string, GoalLock> {
  try {
    if (existsSync(GOALS_FILE)) {
      return JSON.parse(readFileSync(GOALS_FILE, "utf-8"));
    }
  } catch (_) {}
  return {};
}

function saveGoals(goals: Record<string, GoalLock>): void {
  try {
    writeFileSync(GOALS_FILE, JSON.stringify(goals, null, 2));
  } catch (_) {}
}

export function getAgentGoal(agentId: string): GoalLock | null {
  const goals = loadGoals();
  return goals[agentId] || null;
}

export function setAgentGoal(agentId: string, taskId: string, notes?: string): GoalLock {
  const goals = loadGoals();
  const lock: GoalLock = {
    agentId,
    taskId,
    lockedAt: new Date().toISOString(),
    notes: notes || null,
  };
  goals[agentId] = lock;
  saveGoals(goals);
  return lock;
}

export function clearAgentGoal(agentId: string): boolean {
  const goals = loadGoals();
  if (!goals[agentId]) return false;
  delete goals[agentId];
  saveGoals(goals);
  return true;
}

export function getAllGoals(): Record<string, GoalLock> {
  return loadGoals();
}
