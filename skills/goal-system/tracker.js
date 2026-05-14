const { promises: fs } = require("fs");
const path = require("path");

const GOALS_DIR = path.join(process.cwd(), ".coordination", "goals");
const ACTIVE_GOAL_FILE = path.join(GOALS_DIR, "active.json");

async function ensureDir() {
  await fs.mkdir(GOALS_DIR, { recursive: true });
}

async function getActiveGoal() {
  try {
    const data = await fs.readFile(ACTIVE_GOAL_FILE, "utf8");
    return JSON.parse(data);
  } catch {
    return null;
  }
}

async function setGoal(condition, metadata = {}) {
  await ensureDir();
  const goal = {
    id: `goal-${Date.now()}`,
    condition: condition,
    status: "active",
    startedAt: new Date().toISOString(),
    completedAt: null,
    turns: 0,
    tokens: 0,
    lastEvaluation: null,
    metadata,
  };
  await fs.writeFile(ACTIVE_GOAL_FILE, JSON.stringify(goal, null, 2));
  return goal;
}

async function incrementTurn(tokensUsed = 0) {
  const goal = await getActiveGoal();
  if (!goal || goal.status !== "active") return null;

  goal.turns += 1;
  goal.tokens += tokensUsed;
  goal.lastEvaluation = new Date().toISOString();
  await fs.writeFile(ACTIVE_GOAL_FILE, JSON.stringify(goal, null, 2));
  return goal;
}

async function evaluateGoal(evidence) {
  const goal = await getActiveGoal();
  if (!goal || goal.status !== "active") return { met: false, goal: null };

  // Simple keyword-based evaluation
  // In production, this would use a small model or structured checks
  const condition = goal.condition.toLowerCase();
  const evidence_lower = (evidence || "").toLowerCase();

  // Check for completion keywords
  const completionMarkers = [
    "done", "complete", "finished", "deployed", "live", "working",
    "success", "passed", "merged", "pushed", "built"
  ];

  const hasCompletionMarker = completionMarkers.some(m =>
    evidence_lower.includes(m)
  );

  // Check if evidence addresses the goal condition
  const goalKeywords = condition.split(/\s+/).filter(w => w.length > 3);
  const matchingKeywords = goalKeywords.filter(k =>
    evidence_lower.includes(k)
  );
  const keywordCoverage = matchingKeywords.length / Math.max(goalKeywords.length, 1);

  const met = hasCompletionMarker && keywordCoverage > 0.3;

  if (met) {
    goal.status = "completed";
    goal.completedAt = new Date().toISOString();
    await fs.writeFile(ACTIVE_GOAL_FILE, JSON.stringify(goal, null, 2));
  }

  return { met, goal, reason: met ? "Completion markers found" : "Still working toward goal" };
}

async function clearGoal() {
  const goal = await getActiveGoal();
  if (!goal) return null;

  goal.status = "cancelled";
  goal.completedAt = new Date().toISOString();
  await fs.writeFile(ACTIVE_GOAL_FILE, JSON.stringify(goal, null, 2));
  return goal;
}

async function getGoalStatus() {
  const goal = await getActiveGoal();
  if (!goal) return null;

  const started = new Date(goal.startedAt);
  const now = new Date();
  const elapsedMinutes = Math.round((now - started) / 60000);

  return {
    ...goal,
    elapsedMinutes,
    isActive: goal.status === "active",
  };
}

module.exports = {
  getActiveGoal,
  setGoal,
  incrementTurn,
  evaluateGoal,
  clearGoal,
  getGoalStatus,
};
