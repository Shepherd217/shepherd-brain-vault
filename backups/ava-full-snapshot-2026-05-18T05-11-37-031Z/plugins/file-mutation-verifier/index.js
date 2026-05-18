import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { readFileSync, existsSync } from "node:fs";
import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";

const pendingWrites = new Map();

function hashContent(text) {
  return createHash("sha256").update(text).digest("hex").slice(0, 12);
}

function countLines(text) {
  return text.split("\n").length;
}

function countOccurrences(haystack, needle) {
  let count = 0;
  let idx = haystack.indexOf(needle);
  while (idx !== -1) {
    count++;
    idx = haystack.indexOf(needle, idx + 1);
  }
  return count;
}

function lintFile(path, content) {
  const lines = [];
  const parts = path.split(".");
  const ext = parts[parts.length - 1].toLowerCase();

  lines.push(`○ lint: checking .${ext} file`);

  if (ext === "json") {
    try {
      JSON.parse(content);
      lines.push("✓ lint: JSON valid");
    } catch (e) {
      lines.push(`✗ lint: JSON syntax error — ${e.message}`);
    }
  }

  if (ext === "py") {
    const result = spawnSync("python3", ["-m", "py_compile", path], { encoding: "utf-8", timeout: 5000 });
    if (result.status === 0) {
      lines.push("✓ lint: Python valid");
    } else {
      const err = (result.stderr || "").trim().split("\n")[0] || "syntax error";
      lines.push(`✗ lint: Python ${err}`);
    }
  }

  if (ext === "yaml" || ext === "yml") {
    try {
      const yaml = require("js-yaml");
      yaml.load(content);
      lines.push("✓ lint: YAML valid");
    } catch (e) {
      if (e.code === "MODULE_NOT_FOUND") {
        lines.push("○ lint: YAML (js-yaml not installed)");
      } else {
        lines.push(`✗ lint: YAML syntax error — ${e.message}`);
      }
    }
  }

  if (ext === "toml") {
    try {
      const toml = require("@iarna/toml");
      toml.parse(content);
      lines.push("✓ lint: TOML valid");
    } catch (e) {
      if (e.code === "MODULE_NOT_FOUND") {
        lines.push("○ lint: TOML (@iarna/toml not installed)");
      } else {
        lines.push(`✗ lint: TOML syntax error — ${e.message}`);
      }
    }
  }

  return lines;
}

function buildVerifyFooter(tool, path, intended, actualContent) {
  const lines = [];
  lines.push("");
  lines.push("─── MUTATION_VERIFY ───");

  if (tool === "write") {
    const intendedContent = intended.content ?? "";
    const intendedHash = hashContent(intendedContent);
    const intendedLines = countLines(intendedContent);

    if (actualContent === null) {
      lines.push(`✗ ${path} — FILE NOT FOUND after write!`);
    } else {
      const actualHash = hashContent(actualContent);
      const actualLines = countLines(actualContent);
      if (actualHash === intendedHash && actualContent === intendedContent) {
        lines.push(`✓ ${path} — ${actualLines} lines, hash ${actualHash}`);
      } else {
        lines.push(`✗ ${path} — MISMATCH!`);
        lines.push(`  expected: ${intendedLines} lines, hash ${intendedHash}`);
        lines.push(`  actual:   ${actualLines} lines, hash ${actualHash}`);
      }
      lines.push(...lintFile(path, actualContent));
    }
  } else if (tool === "edit") {
    if (actualContent === null) {
      lines.push(`✗ ${path} — FILE NOT FOUND after edit!`);
    } else {
      const edits = intended.edits ?? [];
      let allOk = true;
      for (let i = 0; i < edits.length; i++) {
        const { oldText, newText } = edits[i];
        const oldCount = countOccurrences(actualContent, oldText);
        const newCount = countOccurrences(actualContent, newText);
        if (newCount === 0) {
          lines.push(`✗ edit ${i + 1}: newText not found in file`);
          allOk = false;
        } else if (oldCount > 0) {
          lines.push(`✗ edit ${i + 1}: oldText still present (${oldCount}x)`);
          allOk = false;
        } else {
          lines.push(`✓ edit ${i + 1}: replaced (${newCount}x newText)`);
        }
      }
      if (allOk) {
        lines.unshift(`✓ ${path} — ${edits.length} edit(s) verified`);
      }
      lines.push(...lintFile(path, actualContent));
    }
  }

  lines.push("───────────────────────");
  return lines.join("\n");
}

export default definePluginEntry({
  id: "file-mutation-verifier",
  name: "File Mutation Verifier",
  description:
    "Verifies write_file and edit tool calls actually mutated disk. Appends a verification footer to every tool result so the agent catches silent write failures immediately.",

  register(api) {
    api.on("before_tool_call", (event, _ctx) => {
      if (event.toolName !== "write" && event.toolName !== "edit") return;
      const params = event.params;
      const path = params?.path;
      if (!path || typeof path !== "string") return;

      if (event.toolName === "write") {
        pendingWrites.set(event.toolCallId, {
          tool: "write",
          path,
          content: params?.content ?? "",
        });
      } else {
        pendingWrites.set(event.toolCallId, {
          tool: "edit",
          path,
          edits: Array.isArray(params?.edits) ? params.edits : [],
        });
      }
    });

    api.on("tool_result_persist", (event, _ctx) => {
      const id = event.toolCallId;
      const pending = pendingWrites.get(id);
      if (!pending) return;
      pendingWrites.delete(id);

      if (event.toolName !== "write" && event.toolName !== "edit") return;

      let actualContent = null;
      try {
        if (existsSync(pending.path)) {
          actualContent = readFileSync(pending.path, "utf-8");
        }
      } catch (_e) {
        actualContent = null;
      }

      const footer = buildVerifyFooter(
        pending.tool,
        pending.path,
        pending,
        actualContent
      );

      const msg = event.message;
      if (msg && Array.isArray(msg.content)) {
        const textBlocks = msg.content.filter((c) => c.type === "text");
        if (textBlocks.length > 0) {
          textBlocks[textBlocks.length - 1].text += footer;
        } else {
          msg.content.push({ type: "text", text: footer });
        }
        return { message: msg };
      }

      if (msg && typeof msg.content === "string") {
        msg.content += footer;
        return { message: msg };
      }

      return;
    });
  },
});
