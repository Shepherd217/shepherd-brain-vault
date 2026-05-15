"use strict";

const fs = require("fs");
const path = require("path");
const http = require("http");

const RELAY_URL = process.env.RELAY_URL || "http://localhost:7777/api/tasks";
const INBOX_PATH = process.env.INBOX_PATH || "/root/.openclaw/workspace/.coordination/tasks/inbox";

/**
 * Check if relay is available
 */
function isRelayAvailable() {
  return new Promise((resolve) => {
    const url = new URL(RELAY_URL);
    const req = http.request(
      {
        hostname: url.hostname,
        port: url.port || 80,
        path: "/health",
        method: "GET",
        timeout: 2000,
      },
      (res) => {
        resolve(res.statusCode === 200);
      }
    );
    req.on("error", () => resolve(false));
    req.on("timeout", () => {
      req.destroy();
      resolve(false);
    });
    req.end();
  });
}

/**
 * POST task to relay
 */
async function dispatchToRelay(task) {
  return new Promise((resolve, reject) => {
    const url = new URL(RELAY_URL);
    const data = JSON.stringify(task);

    const req = http.request(
      {
        hostname: url.hostname,
        port: url.port || 80,
        path: url.pathname,
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Content-Length": Buffer.byteLength(data),
        },
        timeout: 5000,
      },
      (res) => {
        let body = "";
        res.on("data", (chunk) => (body += chunk));
        res.on("end", () => {
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve({ success: true, relay: true, response: body });
          } else {
            reject(new Error(`Relay returned ${res.statusCode}: ${body}`));
          }
        });
      }
    );

    req.on("error", reject);
    req.on("timeout", () => {
      req.destroy();
      reject(new Error("Relay request timed out"));
    });

    req.write(data);
    req.end();
  });
}

/**
 * Write task to inbox as markdown file
 */
function dispatchToInbox(task) {
  const filename = `${task.id}.md`;
  const filepath = path.join(INBOX_PATH, filename);

  // Skip if already exists
  if (fs.existsSync(filepath)) {
    return { success: true, skipped: true, path: filepath };
  }

  const markdown = task.toMarkdown ? task.toMarkdown() : generateMarkdown(task);
  fs.writeFileSync(filepath, markdown, "utf-8");

  return { success: true, relay: false, path: filepath };
}

/**
 * Generate markdown for plain task objects (fallback)
 */
function generateMarkdown(task) {
  return `---
id: ${task.id}
title: ${task.title}
status: ${task.status || "backlog"}
priority: ${task.priority || "medium"}
claimed_by:
created_by: dream-loop
created_at: ${new Date().toISOString()}
depends_on: []
tags: [${(task.tags || []).join(", ")}]
source: dream
confidence: ${task.confidence || 0.5}
dream_date: ${task.dreamDate || "unknown"}
agent_hints:
  suggest_to: [${task.owner === "any" ? "ava, hermes" : task.owner || "ava"}]
  block_agents: []
---

# ${task.title}

## What
${task.description || "Dream-detected pattern"}

## Done When
- [ ] Pattern is validated or resolved
- [ ] Next dream cycle confirms improvement
`;
}

/**
 * Dispatch task — tries relay first, falls back to inbox
 */
async function dispatch(task) {
  const relayAvailable = await isRelayAvailable();

  if (relayAvailable) {
    try {
      const result = await dispatchToRelay(task);
      return { ...result, method: "relay" };
    } catch (err) {
      console.error(`  ⚠️  Relay failed: ${err.message}. Falling back to inbox.`);
    }
  }

  return { ...dispatchToInbox(task), method: "inbox" };
}

/**
 * Dispatch multiple tasks
 */
async function dispatchAll(tasks) {
  const results = [];
  for (const task of tasks) {
    try {
      const result = await dispatch(task);
      results.push({ task: task.id, ...result });
      if (result.skipped) {
        console.log(`  ⏭️  Skipped ${task.id} (already exists)`);
      } else if (result.method === "relay") {
        console.log(`  ✅ Dispatched ${task.id} → relay`);
      } else {
        console.log(`  ✅ Dispatched ${task.id} → inbox (${result.path})`);
      }
    } catch (err) {
      console.error(`  ❌ Failed to dispatch ${task.id}: ${err.message}`);
      results.push({ task: task.id, success: false, error: err.message });
    }
  }
  return results;
}

module.exports = { dispatch, dispatchAll, isRelayAvailable, dispatchToInbox };
