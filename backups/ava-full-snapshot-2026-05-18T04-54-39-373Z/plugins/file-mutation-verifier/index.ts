import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { readFileSync, existsSync } from "node:fs";
import { createHash } from "node:crypto";

// ── Session-scoped capture of intended write params ─────────────────────────
const pendingWrites = new Map<string, {
  tool: "write" | "edit";
  path: string;
  content?: string;
  edits?: Array<{ oldText: string; newText: string }>;
}>();

function hashContent(text: string): string {
  return createHash("sha256").update(text).digest("hex").slice(0, 12);
}

function countLines(text: string): number {
  return text.split("\n").length;
}

function countOccurrences(haystack: string, needle: string): number {
  let count = 0;
  let idx = haystack.indexOf(needle);
  while (idx !== -1) {
    count++;
    idx = haystack.indexOf(needle, idx + 1);
  }
  return count;
}

function buildVerifyFooter(
  tool: "write" | "edit",
  path: string,
  intended: any,
  actualContent: string | null
): string {
  const lines: string[] = [];
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
        lines.splice(1, 0); // remove the empty line we already have
      }
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
    // ── 1. Capture intended parameters before execution ─────────────────────
    api.on("before_tool_call", (event, _ctx) => {
      if (event.toolName !== "write" && event.toolName !== "edit") return;
      const params = event.params as any;
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

    // ── 2. Verify & rewrite tool result on persist ──────────────────────────
    api.on("tool_result_persist", (event, _ctx) => {
      const id = event.toolCallId;
      const pending = pendingWrites.get(id);
      if (!pending) return; // not a write/edit we captured
      pendingWrites.delete(id);

      if (event.toolName !== "write" && event.toolName !== "edit") return;

      let actualContent: string | null = null;
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

      // Append footer to the tool result message content
      const msg = event.message as any;
      if (msg && Array.isArray(msg.content)) {
        const textBlocks = msg.content.filter((c: any) => c.type === "text");
        if (textBlocks.length > 0) {
          textBlocks[textBlocks.length - 1].text += footer;
        } else {
          msg.content.push({ type: "text", text: footer });
        }
        return { message: msg };
      }

      // Fallback: if content is a string or some other shape
      if (msg && typeof msg.content === "string") {
        msg.content += footer;
        return { message: msg };
      }

      return;
    });
  },
});
