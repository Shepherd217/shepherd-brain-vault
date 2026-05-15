"use strict";

const fs = require("fs");
const path = require("path");

const FEEDBACK_PATH = process.env.FEEDBACK_PATH || "/root/.openclaw/workspace/skills/dream-dispatcher/feedback.json";
const DREAMS_PATH = process.env.DREAMS_PATH || "/root/.openclaw/workspace/DREAMS.md";

/**
 * Load feedback tracking state
 */
function loadFeedback() {
  if (!fs.existsSync(FEEDBACK_PATH)) {
    return { version: "1.0", tasks: {}, patterns: {} };
  }
  try {
    return JSON.parse(fs.readFileSync(FEEDBACK_PATH, "utf-8"));
  } catch {
    return { version: "1.0", tasks: {}, patterns: {} };
  }
}

/**
 * Save feedback tracking state
 */
function saveFeedback(state) {
  fs.writeFileSync(FEEDBACK_PATH, JSON.stringify(state, null, 2), "utf-8");
}

/**
 * Register a newly dispatched dream task
 */
function trackTask(taskId, dreamDate, pattern, confidence) {
  const state = loadFeedback();
  state.tasks[taskId] = {
    created: new Date().toISOString(),
    dreamDate,
    pattern,
    confidence,
    status: "dispatched",
    resolved: false,
    validatedInDream: null,
  };

  // Track pattern occurrence
  const patternKey = pattern.slice(0, 60);
  if (!state.patterns[patternKey]) {
    state.patterns[patternKey] = {
      firstSeen: dreamDate,
      occurrences: 0,
      tasksCreated: [],
      resolved: false,
    };
  }
  state.patterns[patternKey].occurrences += 1;
  state.patterns[patternKey].tasksCreated.push(taskId);

  saveFeedback(state);
  return state.tasks[taskId];
}

/**
 * Mark a task as resolved
 */
function resolveTask(taskId) {
  const state = loadFeedback();
  if (state.tasks[taskId]) {
    state.tasks[taskId].status = "resolved";
    state.tasks[taskId].resolved = true;
    state.tasks[taskId].resolvedAt = new Date().toISOString();

    // Update pattern
    const patternKey = Object.keys(state.patterns).find((k) =>
      state.patterns[k].tasksCreated.includes(taskId)
    );
    if (patternKey) {
      state.patterns[patternKey].resolved = true;
    }

    saveFeedback(state);
    return true;
  }
  return false;
}

/**
 * Validate if a pattern was resolved in latest dream cycle
 */
function validateInDream(taskId, latestDreamContent) {
  const state = loadFeedback();
  const task = state.tasks[taskId];
  if (!task) return false;

  const patternLower = task.pattern.toLowerCase();
  const dreamLower = latestDreamContent.toLowerCase();

  // Check if pattern still appears in dreams (if not, it's resolved)
  const stillAppears = dreamLower.includes(patternLower.slice(0, 40));

  if (!stillAppears) {
    state.tasks[taskId].validatedInDream = new Date().toISOString();
    state.tasks[taskId].status = "validated-resolved";

    const patternKey = Object.keys(state.patterns).find((k) =>
      state.patterns[k].tasksCreated.includes(taskId)
    );
    if (patternKey) {
      state.patterns[patternKey].resolved = true;
    }

    saveFeedback(state);
    return true;
  }

  return false;
}

/**
 * Check if a pattern is recurring (appeared in multiple dream cycles)
 */
function isRecurring(pattern, threshold = 2) {
  const state = loadFeedback();
  const patternKey = pattern.slice(0, 60);
  return (state.patterns[patternKey]?.occurrences || 0) >= threshold;
}

/**
 * Get unresolved dream tasks
 */
function getUnresolvedTasks() {
  const state = loadFeedback();
  return Object.entries(state.tasks)
    .filter(([, task]) => !task.resolved)
    .map(([id, task]) => ({ id, ...task }));
}

/**
 * Get stats for reporting
 */
function getStats() {
  const state = loadFeedback();
  const tasks = Object.values(state.tasks);
  return {
    totalTasks: tasks.length,
    resolved: tasks.filter((t) => t.resolved).length,
    unresolved: tasks.filter((t) => !t.resolved).length,
    validated: tasks.filter((t) => t.validatedInDream).length,
    patterns: Object.keys(state.patterns).length,
    recurringPatterns: Object.values(state.patterns).filter((p) => p.occurrences >= 2).length,
  };
}

/**
 * Run feedback validation against current DREAMS.md
 */
function runFeedbackLoop() {
  if (!fs.existsSync(DREAMS_PATH)) {
    console.log("  ⚠️  No DREAMS.md found for feedback validation");
    return;
  }

  const dreamContent = fs.readFileSync(DREAMS_PATH, "utf-8");
  const unresolved = getUnresolvedTasks();

  let validated = 0;
  for (const task of unresolved) {
    if (validateInDream(task.id, dreamContent)) {
      validated++;
      console.log(`  ✅ Pattern for ${task.id} validated as resolved`);
    }
  }

  if (validated === 0 && unresolved.length > 0) {
    console.log(`  ⏳ ${unresolved.length} unresolved tasks still active`);
  }

  return { validated, unresolved: unresolved.length };
}

module.exports = {
  trackTask,
  resolveTask,
  validateInDream,
  isRecurring,
  getUnresolvedTasks,
  getStats,
  runFeedbackLoop,
};
