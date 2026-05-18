import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { join, resolve } from "node:path";
import { homedir } from "node:os";

function sha256(text) {
  return createHash("sha256").update(text).digest("hex");
}

function getCacheDir(config) {
  const dir = config?.cacheDir || "~/.openclaw/prompt-cache";
  return dir.replace(/^~/, homedir());
}

function ensureDir(dir) {
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
}

function hashFile(filepath) {
  try {
    return sha256(readFileSync(filepath, "utf-8"));
  } catch (_) {
    return null;
  }
}

function getContextFiles(workspaceDir) {
  const files = [
    "SOUL.md",
    "USER.md",
    "MEMORY.md",
    "AGENTS.md",
    "IDENTITY.md",
    "HEARTBEAT.md",
    "TOOLS.md",
  ];
  return files.map((f) => join(workspaceDir, f)).filter((p) => existsSync(p));
}

function computeContextFingerprint(workspaceDir) {
  const files = getContextFiles(workspaceDir);
  const hashes = {};
  for (const f of files) {
    hashes[f] = hashFile(f);
  }
  const combined = Object.entries(hashes)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([p, h]) => `${p}:${h}`)
    .join("\n");
  return {
    fingerprint: sha256(combined),
    fileHashes: hashes,
    timestamp: new Date().toISOString(),
  };
}

export async function activate(context) {
  const { config, gateway } = context;
  const cacheDir = getCacheDir(config);
  ensureDir(cacheDir);
  const cacheFile = join(cacheDir, "context-cache.json");

  gateway.tools.register("cache_context_fingerprint", {
    description:
      "Compute and store a fingerprint of all context files (SOUL.md, USER.md, MEMORY.md, etc.). On next session, compare fingerprints to detect what changed.",
    parameters: {
      type: "object",
      properties: {
        workspaceDir: {
          type: "string",
          description: "Path to workspace directory",
          default: "~/.openclaw/workspace",
        },
      },
    },
    handler: async ({ workspaceDir = "~/.openclaw/workspace" }) => {
      const dir = workspaceDir.replace(/^~/, homedir());
      const current = computeContextFingerprint(dir);

      let previous = null;
      try {
        if (existsSync(cacheFile)) {
          previous = JSON.parse(readFileSync(cacheFile, "utf-8"));
        }
      } catch (_) {}

      // Store current
      writeFileSync(cacheFile, JSON.stringify(current, null, 2));

      // Compute delta
      const changed = [];
      const unchanged = [];
      if (previous) {
        for (const [path, hash] of Object.entries(current.fileHashes)) {
          const prevHash = previous.fileHashes?.[path];
          if (prevHash === hash) {
            unchanged.push(path);
          } else {
            changed.push({ path, oldHash: prevHash?.slice(0, 12) || "none", newHash: hash?.slice(0, 12) });
          }
        }
        // Detect removed files
        for (const path of Object.keys(previous.fileHashes || {})) {
          if (!current.fileHashes[path]) {
            changed.push({ path, oldHash: previous.fileHashes[path].slice(0, 12), newHash: "removed" });
          }
        }
      }

      return {
        fingerprint: current.fingerprint.slice(0, 16),
        isNewSession: !previous,
        changed: changed.length > 0 ? changed : undefined,
        unchangedCount: unchanged.length,
        totalFiles: Object.keys(current.fileHashes).length,
        timestamp: current.timestamp,
        cacheHit: previous?.fingerprint === current.fingerprint,
      };
    },
  });

  gateway.tools.register("get_cached_context", {
    description:
      "Retrieve the last stored context fingerprint. Use this at session start to check if context files changed since last run.",
    parameters: {
      type: "object",
      properties: {},
    },
    handler: async () => {
      try {
        if (!existsSync(cacheFile)) {
          return { cached: false, message: "No cached fingerprint found — first run" };
        }
        const cached = JSON.parse(readFileSync(cacheFile, "utf-8"));
        return {
          cached: true,
          fingerprint: cached.fingerprint.slice(0, 16),
          timestamp: cached.timestamp,
          fileCount: Object.keys(cached.fileHashes || {}).length,
        };
      } catch (e) {
        return { cached: false, error: e.message };
      }
    },
  });

  gateway.tools.register("clear_prompt_cache", {
    description: "Clear the context fingerprint cache. Forces full context reload on next session.",
    parameters: { type: "object", properties: {} },
    handler: async () => {
      try {
        if (existsSync(cacheFile)) {
          writeFileSync(cacheFile, JSON.stringify({}, null, 2));
          return { cleared: true };
        }
        return { cleared: false, message: "No cache to clear" };
      } catch (e) {
        return { cleared: false, error: e.message };
      }
    },
  });

  return {
    name: "prompt-cache",
    version: "1.0.0",
  };
}
