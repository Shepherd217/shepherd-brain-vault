"use strict";

const { parseDreams, extractCandidates } = require("./dream-parser");

// Tag mapping based on pattern type
const TAG_MAP = {
  "cross-agent": ["team", "infra"],
  "skill": ["infra", "team"],
  "memory": ["memory", "infra"],
  "dreaming": ["research", "infra"],
  "instruction": ["insight", "fix"],
  "standing": ["insight", "memory"],
  "tool": ["fix", "infra"],
  "relay": ["infra", "team"],
  "agent": ["team", "research"],
  "infrastructure": ["infra"],
  "research": ["research"],
  "default": ["insight"],
};

/**
 * Determine tags from candidate text
 */
function inferTags(text) {
  const lower = text.toLowerCase();
  const tags = new Set();

  for (const [keyword, mappedTags] of Object.entries(TAG_MAP)) {
    if (lower.includes(keyword)) {
      mappedTags.forEach((t) => tags.add(t));
    }
  }

  if (tags.size === 0) {
    tags.add("insight");
  }

  return Array.from(tags);
}

/**
 * Determine priority based on confidence and content
 */
function inferPriority(confidence, text) {
  const lower = text.toLowerCase();
  if (lower.includes("critical") || lower.includes("urgent") || lower.includes("block")) {
    return "critical";
  }
  if (confidence >= 0.8 || lower.includes("high priority") || lower.includes("important")) {
    return "high";
  }
  if (confidence >= 0.6) {
    return "medium";
  }
  return "low";
}

/**
 * Suggest owner/agent based on tags
 */
function inferOwner(tags) {
  if (tags.includes("research")) return "ava";
  if (tags.includes("infra")) return "hermes";
  if (tags.includes("memory")) return "eve";
  if (tags.includes("team")) return "any";
  return "any";
}

/**
 * Generate task ID from candidate
 */
function generateTaskId(candidate, index) {
  const date = candidate.day || new Date().toISOString().slice(0, 10);
  return `dream-${date.replace(/-/g, "")}-${String(index + 1).padStart(3, "0")}`;
}

/**
 * Format candidate as relay-compatible task markdown
 */
function formatTask(candidate, index) {
  const tags = inferTags(candidate.text);
  const priority = inferPriority(candidate.confidence, candidate.text);
  const owner = inferOwner(tags);
  const id = generateTaskId(candidate, index);

  return {
    id,
    title: candidate.text.slice(0, 80),
    description: `Dream detected: ${candidate.text}`,
    priority,
    status: "backlog",
    tags,
    owner,
    source: "dream",
    confidence: candidate.confidence,
    dreamDate: candidate.day,
    type: candidate.type || "candidate",
    toMarkdown: () => `---
id: ${id}
title: ${candidate.text.slice(0, 80)}
status: backlog
priority: ${priority}
claimed_by:
created_by: dream-loop
created_at: ${new Date().toISOString()}
depends_on: []
tags: [${tags.join(", ")}]
source: dream
confidence: ${candidate.confidence}
dream_date: ${candidate.day || "unknown"}
agent_hints:
  suggest_to: [${owner === "any" ? "ava, hermes" : owner}]
  block_agents: []
---

# ${candidate.text}

## What
Dream detected this pattern from ${candidate.day || "unknown"} REM cycle.

> "${candidate.text}"

## Why
This emerged as a ${candidate.type === "lasting-update" ? "possible lasting update" : "high-confidence candidate"} with confidence ${candidate.confidence}.

## Done When
- [ ] Pattern is validated or resolved
- [ ] Next dream cycle confirms improvement

## Source
- Dream date: ${candidate.day || "unknown"}
- Source file: ${candidate.source || "DREAMS.md"}
`,
  };
}

/**
 * Format all candidates as tasks
 */
function formatTasks(candidates) {
  return candidates.map((c, i) => formatTask(c, i));
}

module.exports = { formatTasks, formatTask, inferTags, inferPriority, inferOwner };
