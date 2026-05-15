"use strict";

const fs = require("fs");
const path = require("path");
const { parseDreams, extractCandidates } = require("./lib/dream-parser");
const { formatTasks } = require("./lib/task-formatter");
const { dispatchAll } = require("./lib/dispatcher");
const { trackTask, runFeedbackLoop, getStats } = require("./lib/feedback-tracker");

const VAULT_PATH = process.env.VAULT_PATH || "/root/.openclaw/workspace/shepherd-brain-vault";
const DREAMS_PATH = process.env.DREAMS_PATH || "/root/.openclaw/workspace/DREAMS.md";

/**
 * Write dream summary to vault drawers/dreams/
 */
function writeDreamToVault(candidate, index) {
  const date = candidate.day || new Date().toISOString().slice(0, 10);
  const dreamDir = path.join(VAULT_PATH, "drawers", "dreams");
  
  if (!fs.existsSync(dreamDir)) {
    fs.mkdirSync(dreamDir, { recursive: true });
  }

  const filename = `${date}-dream-loop-${String(index + 1).padStart(3, "0")}.md`;
  const filepath = path.join(dreamDir, filename);

  // Skip if exists
  if (fs.existsSync(filepath)) {
    return { skipped: true, path: filepath };
  }

  const content = `---
date: ${date}
source: dream-loop
confidence: ${candidate.confidence}
type: ${candidate.type || "candidate"}
status: active
---

# Dream: ${candidate.text.slice(0, 60)}

## Pattern Detected
${candidate.text}

## Source
- Day: ${date}
- Source: ${candidate.source || "DREAMS.md"}
- Confidence: ${candidate.confidence}

## Action Taken
- [x] Dispatched to coordination inbox
- [ ] Pattern validated in next dream cycle

## Related
- See coordination tasks for resolution tracking
`;

  fs.writeFileSync(filepath, content, "utf-8");
  return { written: true, path: filepath };
}

/**
 * Update rooms/patterns/ if recurring pattern detected
 */
function updatePatternLibrary(candidate) {
  const patternsDir = path.join(VAULT_PATH, "rooms", "patterns");
  
  if (!fs.existsSync(patternsDir)) {
    fs.mkdirSync(patternsDir, { recursive: true });
  }

  // Extract key phrase (first 40 chars normalized)
  const patternKey = candidate.text.toLowerCase().replace(/[^a-z0-9]/g, "-").slice(0, 40);
  const filepath = path.join(patternsDir, `${patternKey}.md`);

  if (fs.existsSync(filepath)) {
    // Update existing pattern occurrence count
    const existing = fs.readFileSync(filepath, "utf-8");
    const countMatch = existing.match(/occurrences: (\d+)/);
    const count = countMatch ? parseInt(countMatch[1]) + 1 : 2;
    
    const updated = existing.replace(/occurrences: \d+/, `occurrences: ${count}`)
                           .replace(/last_seen: .*/, `last_seen: ${new Date().toISOString()}`);
    
    fs.writeFileSync(filepath, updated, "utf-8");
    return { updated: true, path: filepath, occurrences: count };
  }

  // Create new pattern
  const content = `---
pattern: ${candidate.text.slice(0, 80)}
first_seen: ${candidate.day || new Date().toISOString()}
last_seen: ${new Date().toISOString()}
occurrences: 1
confidence: ${candidate.confidence}
status: active
---

# Pattern: ${candidate.text.slice(0, 60)}

## Description
${candidate.text}

## Occurrences
- First seen: ${candidate.day || "unknown"}
- Source: ${candidate.source || "DREAMS.md"}

## Related Tasks
- See coordination inbox for dispatched tasks

## Notes
Pattern detected by dream loop. Monitor for recurrence.
`;

  fs.writeFileSync(filepath, content, "utf-8");
  return { created: true, path: filepath, occurrences: 1 };
}

/**
 * Full vault-integrated dream loop
 */
async function runVaultLoop() {
  console.log("\n🏛️  Palace Dream Loop\n");

  // Parse dreams
  const entries = parseDreams();
  console.log(`[1/6] Parsed ${entries.length} dream entries`);

  const candidates = extractCandidates(entries, 0.5);
  console.log(`[2/6] Extracted ${candidates.length} candidates\n`);

  if (candidates.length === 0) {
    console.log("  ⏳ No candidates. Vault loop complete.\n");
    return { dispatched: 0, vaultWritten: 0 };
  }

  // Format and dispatch to coordination
  const tasks = formatTasks(candidates);
  console.log(`[3/6] Formatted ${tasks.length} tasks`);
  
  const dispatchResults = await dispatchAll(tasks);
  const dispatched = dispatchResults.filter(r => r.success && !r.skipped).length;
  console.log(`      Dispatched: ${dispatched}\n`);

  // Track feedback
  console.log(`[4/6] Tracking feedback...`);
  for (let i = 0; i < tasks.length; i++) {
    if (dispatchResults[i].success && !dispatchResults[i].skipped) {
      trackTask(tasks[i].id, tasks[i].dreamDate, tasks[i].title, tasks[i].confidence);
    }
  }

  // Write to vault dreams drawer
  console.log(`[5/6] Writing to vault drawers/dreams/...`);
  let vaultWritten = 0;
  let patternsUpdated = 0;
  
  for (let i = 0; i < candidates.length; i++) {
    const result = writeDreamToVault(candidates[i], i);
    if (result.written) vaultWritten++;
    
    // Update pattern library
    const patternResult = updatePatternLibrary(candidates[i]);
    if (patternResult.created || patternResult.updated) patternsUpdated++;
  }
  
  console.log(`      Vault dreams: ${vaultWritten} new`);
  console.log(`      Patterns: ${patternsUpdated} updated\n`);

  // Run feedback validation
  console.log(`[6/6] Feedback validation...`);
  const feedback = runFeedbackLoop();

  // Stats
  const stats = getStats();
  console.log(`\n📊 Stats`);
  console.log(`   Coordination tasks: ${stats.totalTasks}`);
  console.log(`   Vault dreams: ${vaultWritten}`);
  console.log(`   Patterns: ${patternsUpdated}`);
  console.log(`   Unresolved: ${stats.unresolved}\n`);

  return {
    entries: entries.length,
    candidates: candidates.length,
    dispatched,
    vaultWritten,
    patternsUpdated,
    feedback,
    stats,
  };
}

// Run if called directly
if (require.main === module) {
  runVaultLoop().catch((err) => {
    console.error("  ❌ Vault dream loop failed:", err.message);
    process.exit(1);
  });
}

module.exports = { runVaultLoop, writeDreamToVault, updatePatternLibrary };
