"use strict";

const { parseDreams, extractCandidates } = require("./lib/dream-parser");
const { formatTasks } = require("./lib/task-formatter");
const { dispatchAll } = require("./lib/dispatcher");
const { trackTask, runFeedbackLoop, getStats } = require("./lib/feedback-tracker");

/**
 * Dream → Task Loop
 * 
 * 1. Parse DREAMS.md
 * 2. Extract high-confidence candidates (>0.5)
 * 3. Format as tasks
 * 4. Dispatch to relay or inbox
 * 5. Track for feedback validation
 */
async function run() {
  console.log("\n🧠 Dream → Task Loop\n");

  // Step 1 + 2: Parse dreams and extract truths
  console.log("[1/5] Parsing DREAMS.md...");
  const entries = parseDreams();
  console.log(`      Found ${entries.length} dream entries`);

  const candidates = extractCandidates(entries, 0.5);
  console.log(`      Extracted ${candidates.length} high-confidence candidates\n`);

  if (candidates.length === 0) {
    console.log("  ⏳ No candidates above threshold. Nothing to dispatch.\n");
    return { dispatched: 0, candidates: 0 };
  }

  // Step 3: Format as tasks
  console.log("[2/5] Formatting tasks...");
  const tasks = formatTasks(candidates);
  console.log(`      Formatted ${tasks.length} tasks\n`);

  // Step 4: Dispatch
  console.log("[3/5] Dispatching...");
  const results = await dispatchAll(tasks);
  const dispatched = results.filter((r) => r.success && !r.skipped).length;
  const skipped = results.filter((r) => r.skipped).length;
  console.log(`      Dispatched: ${dispatched} | Skipped (exists): ${skipped}\n`);

  // Step 5: Track for feedback
  console.log("[4/5] Tracking for feedback...");
  for (let i = 0; i < tasks.length; i++) {
    const result = results[i];
    if (result.success && !result.skipped) {
      trackTask(
        tasks[i].id,
        tasks[i].dreamDate,
        tasks[i].title,
        tasks[i].confidence
      );
    }
  }
  console.log(`      Tracked ${dispatched} new tasks\n`);

  // Run feedback loop
  console.log("[5/5] Running feedback validation...");
  const feedback = runFeedbackLoop();
  console.log();

  // Stats
  const stats = getStats();
  console.log("📊 Dream Loop Stats");
  console.log(`   Total tasks: ${stats.totalTasks}`);
  console.log(`   Resolved:    ${stats.resolved}`);
  console.log(`   Unresolved:  ${stats.unresolved}`);
  console.log(`   Validated:   ${stats.validated}`);
  console.log(`   Patterns:    ${stats.patterns} (${stats.recurringPatterns} recurring)`);
  console.log();

  return {
    entries: entries.length,
    candidates: candidates.length,
    dispatched,
    skipped,
    feedback,
    stats,
  };
}

// Run if called directly
if (require.main === module) {
  run().catch((err) => {
    console.error("  ❌ Dream loop failed:", err.message);
    process.exit(1);
  });
}

module.exports = { run };
