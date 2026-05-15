"use strict";

const fs = require("fs");
const path = require("path");

const DREAMS_PATH = path.resolve(process.env.DREAMS_PATH || "/root/.openclaw/workspace/DREAMS.md");

/**
 * Parse DREAMS.md and extract dream entries with candidates
 */
function parseDreams() {
  if (!fs.existsSync(DREAMS_PATH)) {
    return [];
  }

  const content = fs.readFileSync(DREAMS_PATH, "utf-8");
  const entries = [];

  // Split by backfill entry markers
  const entryRegex = /<!-- openclaw:dreaming:backfill-entry day=([^\s]+) source=([^\s]+) -->/g;
  let match;
  while ((match = entryRegex.exec(content)) !== null) {
    const day = match[1];
    const source = match[2];
    const startIdx = match.index;

    // Find next marker or end of diary
    const nextMatch = entryRegex.exec(content);
    const endIdx = nextMatch ? nextMatch.index : content.indexOf("<!-- openclaw:dreaming:diary:end -->");
    entryRegex.lastIndex = startIdx + match[0].length; // Reset for next iteration

    const entryContent = content.slice(startIdx, endIdx > 0 ? endIdx : undefined);

    // Extract sections
    const whatHappened = extractSection(entryContent, "What Happened");
    const reflections = extractSection(entryContent, "Reflections");
    const candidates = extractSection(entryContent, "Candidates");
    const possibleUpdates = extractSection(entryContent, "Possible Lasting Updates");

    entries.push({
      day,
      source,
      whatHappened,
      reflections,
      candidates,
      possibleUpdates,
    });
  }

  return entries;
}

function extractSection(content, sectionName) {
  const regex = new RegExp(`${sectionName}\\n([\\s\\S]*?)(?=\\n\\n[A-Z]|\\n---|\\n###|$)`);
  const match = content.match(regex);
  if (!match) return [];

  return match[1]
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.length > 0 && line.match(/^\d+\.|^- /))
    .map((line) => line.replace(/^\d+\.\s*/, "").replace(/^- /, "").trim());
}

/**
 * Extract high-confidence candidates for task creation
 */
function extractCandidates(entries, minConfidence = 0.5) {
  const candidates = [];

  for (const entry of entries) {
    for (const candidate of entry.candidates) {
      // Extract confidence if present
      const confidenceMatch = candidate.match(/\[confidence=([\d.]+)\]/);
      const confidence = confidenceMatch ? parseFloat(confidenceMatch[1]) : 0.5;

      if (confidence >= minConfidence) {
        candidates.push({
          text: candidate.replace(/\[confidence=[\d.]+\]/, "").replace(/\[.*?\]/g, "").trim(),
          confidence,
          day: entry.day,
          source: entry.source,
        });
      }
    }

    // Also include "Possible Lasting Updates" as high-confidence candidates
    for (const update of entry.possibleUpdates) {
      candidates.push({
        text: update.replace(/\[.*?\]/g, "").trim(),
        confidence: 0.75, // Updates are pre-filtered as lasting
        day: entry.day,
        source: entry.source,
        type: "lasting-update",
      });
    }
  }

  return candidates;
}

module.exports = { parseDreams, extractCandidates };

// CLI usage
if (require.main === module) {
  const entries = parseDreams();
  const candidates = extractCandidates(entries);
  console.log(JSON.stringify({ entries: entries.length, candidates }, null, 2));
}
