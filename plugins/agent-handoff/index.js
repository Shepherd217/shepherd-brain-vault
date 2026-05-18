import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { readFileSync, writeFileSync, existsSync, readdirSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";

function readLastLines(path, maxLines) {
  const content = readFileSync(path, "utf-8");
  const lines = content.trim().split("\n").filter((l) => l.trim());
  return lines.slice(-maxLines);
}

function parseSessionMessages(lines) {
  const messages = [];
  for (const line of lines) {
    try {
      const obj = JSON.parse(line);
      if (obj.role && (obj.content || obj.tool_calls || obj.tool_results)) {
        messages.push({
          role: obj.role,
          content: obj.content,
          tool_calls: obj.tool_calls,
          tool_results: obj.tool_results,
          name: obj.name,
          timestamp: obj.timestamp,
        });
      }
    } catch (_) {
      // skip unparseable lines
    }
  }
  return messages;
}

function readMemoryFiles(workspaceDir, files) {
  const result = {};
  for (const file of files) {
    const path = join(workspaceDir, file);
    try {
      if (existsSync(path)) {
        result[file] = readFileSync(path, "utf-8");
      }
    } catch (_) {
      result[file] = null;
    }
  }
  return result;
}

function listWorkingFiles(workspaceDir) {
  try {
    const entries = readdirSync(workspaceDir, { withFileTypes: true, recursive: true });
    return entries
      .filter((e) => e.isFile())
      .map((e) => join(e.path || workspaceDir, e.name))
      .filter((p) => !p.includes("node_modules") && !p.includes(".git") && !p.includes(".openclaw"));
  } catch (_) {
    return [];
  }
}

function getSessionJsonlPath(sessionId) {
  // Try common locations
  const candidates = [
    `/root/.openclaw/agents/main/sessions/${sessionId}.jsonl`,
    `/root/.openclaw/agents/main/sessions/${sessionId}.json`,
  ];
  for (const p of candidates) {
    if (existsSync(p)) return p;
  }
  return null;
}

export default definePluginEntry({
  id: "agent-handoff",
  name: "Agent Handoff",
  description:
    "Capture and resume agent session state for live transfers between models, personas, or agent instances.",

  register(api) {
    const config = api.pluginConfig || {};
    if (config.enabled === false) return;

    const snapshotDir = config.snapshotDir || ".coordination/snapshots";
    const maxMessages = config.maxMessages || 50;
    const memoryFiles = config.memoryFiles || [
      "SOUL.md",
      "USER.md",
      "MEMORY.md",
      "AGENTS.md",
      "CONTEXT.md",
      "TOOLS.md",
    ];

    api.registerTool(
      {
        name: "capture_agent_state",
        description:
          "Capture the current agent session state (recent messages, memory, working files) into a snapshot file for handoff to another agent or model. Returns the snapshot file path.",
        parameters: {
          type: "object",
          properties: {
            snapshot_name: {
              type: "string",
              description: "Name for the snapshot file (without extension). Defaults to timestamp.",
            },
            include_files: {
              type: "array",
              items: { type: "string" },
              description: "Additional file paths to include in snapshot content (not just listing).",
            },
          },
        },
        handler: async (params, ctx) => {
          const workspaceDir = ctx.workspaceDir || "/root/.openclaw/workspace";
          const sessionId = ctx.sessionId || "unknown";
          const name = params.snapshot_name || `handoff-${Date.now()}`;
          const outDir = join(workspaceDir, snapshotDir);

          try {
            mkdirSync(outDir, { recursive: true });
          } catch (_) {}

          // 1. Read recent session messages from JSONL
          let messages = [];
          const sessionPath = getSessionJsonlPath(sessionId);
          if (sessionPath) {
            const lines = readLastLines(sessionPath, maxMessages * 2); // read extra to filter
            messages = parseSessionMessages(lines).slice(-maxMessages);
          }

          // 2. Read memory files
          const memory = readMemoryFiles(workspaceDir, memoryFiles);

          // 3. List working files
          const workingFiles = listWorkingFiles(workspaceDir);

          // 4. Include additional file contents
          const extraFiles = {};
          for (const fp of params.include_files || []) {
            try {
              if (existsSync(fp)) {
                extraFiles[fp] = readFileSync(fp, "utf-8");
              }
            } catch (_) {}
          }

          const snapshot = {
            version: "1.0",
            timestamp: new Date().toISOString(),
            source_agent: ctx.agentId || "unknown",
            source_session: sessionId,
            source_model: ctx.activeModel?.modelId || "unknown",
            messages: messages.map((m) => ({
              role: m.role,
              content:
                typeof m.content === "string"
                  ? m.content.slice(0, 5000)
                  : JSON.stringify(m.content).slice(0, 5000),
              name: m.name,
            })),
            memory: memory,
            working_files: workingFiles.slice(0, 200),
            extra_files: extraFiles,
          };

          const outPath = join(outDir, `${name}.json`);
          writeFileSync(outPath, JSON.stringify(snapshot, null, 2));

          return {
            content: `Snapshot saved to ${outPath}\n\nCaptured:\n- ${messages.length} messages\n- ${Object.keys(memory).length} memory files\n- ${workingFiles.length} working files\n- ${Object.keys(extraFiles).length} extra files`,
          };
        },
      },
      { requireSession: true }
    );

    api.registerTool(
      {
        name: "resume_agent_state",
        description:
          "Resume from a previously captured agent snapshot. Reads the snapshot and returns formatted context for bootstrapping a new agent session.",
        parameters: {
          type: "object",
          properties: {
            snapshot_name: {
              type: "string",
              description: "Name of the snapshot file (without extension).",
            },
            snapshot_path: {
              type: "string",
              description: "Full path to snapshot JSON file. Overrides snapshot_name.",
            },
            message_limit: {
              type: "number",
              description: "Max messages to include in resume context.",
              default: 20,
            },
          },
          required: ["snapshot_name"],
        },
        handler: async (params, ctx) => {
          const workspaceDir = ctx.workspaceDir || "/root/.openclaw/workspace";
          const path =
            params.snapshot_path || join(workspaceDir, snapshotDir, `${params.snapshot_name}.json`);

          if (!existsSync(path)) {
            return { content: `✗ Snapshot not found: ${path}` };
          }

          const snapshot = JSON.parse(readFileSync(path, "utf-8"));
          const limit = params.message_limit || 20;
          const msgs = (snapshot.messages || []).slice(-limit);

          let text = `## AGENT HANDOFF — Resuming from ${snapshot.source_agent || "unknown"}\n\n`;
          text += `**Captured:** ${snapshot.timestamp}\n`;
          text += `**Source model:** ${snapshot.source_model || "unknown"}\n\n`;

          if (snapshot.memory) {
            text += `### Memory Snapshot\n\n`;
            for (const [file, content] of Object.entries(snapshot.memory)) {
              if (content) {
                text += `--- ${file} ---\n${(content).slice(0, 3000)}\n\n`;
              }
            }
          }

          if (msgs.length > 0) {
            text += `### Recent Conversation (${msgs.length} messages)\n\n`;
            for (const m of msgs) {
              text += `**${m.role}${m.name ? ":" + m.name : ""}**\n${m.content}\n\n`;
            }
          }

          if (snapshot.working_files && snapshot.working_files.length > 0) {
            text += `### Working Files (${snapshot.working_files.length})\n\n`;
            text += snapshot.working_files.slice(0, 50).join("\n") + "\n\n";
          }

          if (snapshot.extra_files && Object.keys(snapshot.extra_files).length > 0) {
            text += `### Extra Files\n\n`;
            for (const [fp, content] of Object.entries(snapshot.extra_files)) {
              text += `--- ${fp} ---\n${(content).slice(0, 2000)}\n\n`;
            }
          }

          return { content: text };
        },
      },
      { requireSession: true }
    );
  },
});
