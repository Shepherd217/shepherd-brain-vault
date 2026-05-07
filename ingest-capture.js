#!/usr/bin/env node
/**
 * Shepherd's Brain — Telegram Capture Ingestion Script
 * 
 * This script runs as a background process (or Paperclip routine)
 * that monitors for new Telegram messages from Nathan and writes them
 * to the Obsidian vault inbox folder.
 * 
 * Usage: node ingest-capture.js <message> [source] [tag]
 * Or: Paperclip routine calls this via adapter execution
 */

import { writeFileSync, appendFileSync, existsSync, mkdirSync } from "node:fs";
import { resolve } from "node:path";
import { randomUUID } from "node:crypto";

const VAULT_ROOT = process.env.SHEPHERD_VAULT_ROOT || "/root/.openclaw/workspace/vault";
const INBOX_DIR = resolve(VAULT_ROOT, "inbox");

function ensureDirs() {
  if (!existsSync(INBOX_DIR)) {
    mkdirSync(INBOX_DIR, { recursive: true });
  }
}

function sanitizeFilename(str) {
  return str
    .replace(/[^a-zA-Z0-9\-_\s]/g, "")
    .trim()
    .replace(/\s+/g, "-")
    .slice(0, 60);
}

function formatCapture({ message, source = "telegram", tag = "quick-capture", timestamp = new Date() }) {
  const isoDate = timestamp.toISOString().split("T")[0];
  const isoTime = timestamp.toISOString();
  const id = randomUUID().slice(0, 8);
  
  return {
    filename: `${isoDate}-${id}-${sanitizeFilename(message.slice(0, 30))}.md`,
    content: `---
id: ${id}
source: ${source}
tag: ${tag}
date: ${isoTime}
status: unprocessed
---

# Quick Capture

${message}

## Metadata
- **Captured:** ${isoTime}
- **Source:** ${source}
- **Tag:** ${tag}
- **Status:** unprocessed (awaiting daily brief review)

## Notes
_(Add context, connections, or actions here during processing)_
`,
  };
}

function ingest({ message, source = "telegram", tag = "quick-capture" }) {
  ensureDirs();
  const capture = formatCapture({ message, source, tag });
  const filepath = resolve(INBOX_DIR, capture.filename);
  writeFileSync(filepath, capture.content, "utf8");
  
  // Also append to a daily log for quick scanning
  const today = new Date().toISOString().split("T")[0];
  const dailyLog = resolve(INBOX_DIR, `.log-${today}.md`);
  appendFileSync(dailyLog, `- [${new Date().toISOString()}] [${tag}] ${message.slice(0, 100)}\n`, "utf8");
  
  return { filepath, filename: capture.filename };
}

// CLI usage
if (import.meta.url === `file://${process.argv[1]}`) {
  const message = process.argv[2];
  const source = process.argv[3] || "telegram";
  const tag = process.argv[4] || "quick-capture";
  
  if (!message) {
    console.error("Usage: node ingest-capture.js <message> [source] [tag]");
    process.exit(1);
  }
  
  const result = ingest({ message, source, tag });
  console.log(JSON.stringify({ success: true, ...result }, null, 2));
}

export { ingest, formatCapture };
