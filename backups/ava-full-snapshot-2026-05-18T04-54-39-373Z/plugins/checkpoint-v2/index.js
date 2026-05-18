import { existsSync, mkdirSync, writeFileSync, readFileSync, readdirSync, statSync, rmSync, copyFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { homedir } from "node:os";

function ensureDir(dir) {
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
}

function getDirSize(dir) {
  let total = 0;
  try {
    const files = readdirSync(dir);
    for (const f of files) {
      const p = join(dir, f);
      const s = statSync(p);
      if (s.isDirectory()) {
        total += getDirSize(p);
      } else {
        total += s.size;
      }
    }
  } catch (_) {}
  return total;
}

function formatBytes(bytes) {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

export async function activate(context) {
  const { config, gateway } = context;

  const checkpointDir = (config?.checkpointDir || "~/.openclaw/checkpoints").replace(/^~/, homedir());
  const maxCheckpoints = config?.maxCheckpoints || 20;
  const maxTotalSizeMb = config?.maxTotalSizeMb || 500;
  const maxTotalSizeBytes = maxTotalSizeMb * 1024 * 1024;
  const criticalFiles = config?.criticalFiles || [
    "SOUL.md",
    "USER.md",
    "MEMORY.md",
    "AGENTS.md",
    "IDENTITY.md",
    "TOOLS.md",
    "HEARTBEAT.md",
    ".coordination/tasks/task-board.md",
  ];

  ensureDir(checkpointDir);

  function listCheckpoints() {
    try {
      return readdirSync(checkpointDir)
        .filter((d) => d.match(/^\d{4}-\d{2}-\d{2}T/))
        .map((d) => {
          const cpDir = join(checkpointDir, d);
          const metaPath = join(cpDir, "meta.json");
          let meta = {};
          try {
            if (existsSync(metaPath)) meta = JSON.parse(readFileSync(metaPath, "utf-8"));
          } catch (_) {}
          return {
            id: d,
            createdAt: d,
            size: formatBytes(getDirSize(cpDir)),
            sizeBytes: getDirSize(cpDir),
            fileCount: meta.fileCount || 0,
            note: meta.note || "",
          };
        })
        .sort((a, b) => b.createdAt.localeCompare(a.createdAt));
    } catch (_) {
      return [];
    }
  }

  function pruneCheckpoints() {
    const checkpoints = listCheckpoints();
    let totalSize = checkpoints.reduce((sum, cp) => sum + cp.sizeBytes, 0);
    let deleted = [];

    // Prune by count
    while (checkpoints.length > maxCheckpoints) {
      const oldest = checkpoints.pop();
      if (oldest) {
        const cpDir = join(checkpointDir, oldest.id);
        try {
          rmSync(cpDir, { recursive: true });
          totalSize -= oldest.sizeBytes;
          deleted.push(oldest.id);
        } catch (_) {}
      }
    }

    // Prune by size
    while (totalSize > maxTotalSizeBytes && checkpoints.length > 1) {
      const oldest = checkpoints.pop();
      if (oldest) {
        const cpDir = join(checkpointDir, oldest.id);
        try {
          rmSync(cpDir, { recursive: true });
          totalSize -= oldest.sizeBytes;
          deleted.push(oldest.id);
        } catch (_) {}
      }
    }

    return { deleted, totalSize, remainingCount: checkpoints.length };
  }

  gateway.tools.register("create_checkpoint", {
    description:
      "Create a snapshot of critical workspace files. Auto-prunes old checkpoints to stay within disk limits.",
    parameters: {
      type: "object",
      properties: {
        note: {
          type: "string",
          description: "Optional note about what this checkpoint captures",
        },
        includeFiles: {
          type: "array",
          items: { type: "string" },
          description: "Additional files to include beyond the default critical list",
        },
      },
    },
    handler: async ({ note, includeFiles = [] }) => {
      const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
      const cpDir = join(checkpointDir, timestamp);
      ensureDir(cpDir);

      const workspaceDir = process.cwd();
      const filesToBackup = [...criticalFiles, ...includeFiles];
      let copied = 0;
      let failed = 0;

      for (const file of filesToBackup) {
        const src = join(workspaceDir, file);
        const dest = join(cpDir, file.replace(/\//g, "_"));
        try {
          if (existsSync(src)) {
            copyFileSync(src, dest);
            copied++;
          }
        } catch (_) {
          failed++;
        }
      }

      // Write metadata
      const meta = {
        createdAt: timestamp,
        fileCount: copied,
        note: note || "",
        workspaceDir,
        files: filesToBackup,
      };
      writeFileSync(join(cpDir, "meta.json"), JSON.stringify(meta, null, 2));

      // Auto-prune
      const pruneResult = pruneCheckpoints();

      return {
        checkpointId: timestamp,
        filesCopied: copied,
        filesFailed: failed,
        note: note || "",
        pruned: pruneResult.deleted.length > 0 ? pruneResult.deleted : undefined,
        totalCheckpoints: pruneResult.remainingCount,
        totalSize: formatBytes(pruneResult.totalSize),
      };
    },
  });

  gateway.tools.register("list_checkpoints", {
    description: "List all stored checkpoints with size and creation time.",
    parameters: { type: "object", properties: {} },
    handler: async () => {
      const checkpoints = listCheckpoints();
      const totalSize = checkpoints.reduce((sum, cp) => sum + cp.sizeBytes, 0);
      return {
        totalCheckpoints: checkpoints.length,
        totalSize: formatBytes(totalSize),
        maxAllowed: maxCheckpoints,
        maxSizeMb: maxTotalSizeMb,
        checkpoints: checkpoints.slice(0, 10), // Return last 10
      };
    },
  });

  gateway.tools.register("restore_checkpoint", {
    description:
      "Restore files from a checkpoint. OVERWRITES current files — use with caution!",
    parameters: {
      type: "object",
      properties: {
        checkpointId: {
          type: "string",
          description: "Checkpoint ID (timestamp) to restore from",
        },
        dryRun: {
          type: "boolean",
          description: "Show what would be restored without actually doing it",
          default: true,
        },
      },
      required: ["checkpointId"],
    },
    handler: async ({ checkpointId, dryRun = true }) => {
      const cpDir = join(checkpointDir, checkpointId);
      if (!existsSync(cpDir)) {
        return { error: `Checkpoint ${checkpointId} not found` };
      }

      const metaPath = join(cpDir, "meta.json");
      let meta = { files: [] };
      try {
        if (existsSync(metaPath)) meta = JSON.parse(readFileSync(metaPath, "utf-8"));
      } catch (_) {}

      const workspaceDir = process.cwd();
      const restored = [];

      for (const file of meta.files || []) {
        const backupName = file.replace(/\//g, "_");
        const src = join(cpDir, backupName);
        const dest = join(workspaceDir, file);

        if (existsSync(src)) {
          restored.push({ file, dest, size: formatBytes(statSync(src).size) });
          if (!dryRun) {
            try {
              copyFileSync(src, dest);
            } catch (e) {
              restored[restored.length - 1].error = e.message;
            }
          }
        }
      }

      return {
        checkpointId,
        dryRun,
        filesRestored: restored.length,
        files: restored,
        warning: dryRun
          ? "This was a dry run. Set dryRun=false to actually restore."
          : "Files have been overwritten from checkpoint.",
      };
    },
  });

  gateway.tools.register("delete_checkpoint", {
    description: "Delete a specific checkpoint.",
    parameters: {
      type: "object",
      properties: {
        checkpointId: {
          type: "string",
          description: "Checkpoint ID to delete",
        },
      },
      required: ["checkpointId"],
    },
    handler: async ({ checkpointId }) => {
      const cpDir = join(checkpointDir, checkpointId);
      if (!existsSync(cpDir)) {
        return { error: `Checkpoint ${checkpointId} not found` };
      }

      try {
        rmSync(cpDir, { recursive: true });
        return { deleted: true, checkpointId };
      } catch (e) {
        return { deleted: false, error: e.message };
      }
    },
  });

  return {
    name: "checkpoint-v2",
    version: "1.0.0",
  };
}