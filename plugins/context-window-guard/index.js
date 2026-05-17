import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

// Rough heuristic: ~4 chars per token for English text
function estimateTokens(text) {
  if (!text) return 0;
  return Math.ceil(text.length / 4);
}

function estimateMessageTokens(msg) {
  let text = "";
  if (typeof msg.content === "string") {
    text = msg.content;
  } else if (Array.isArray(msg.content)) {
    for (const block of msg.content) {
      if (block.type === "text" && block.text) {
        text += block.text;
      } else if (block.type === "tool_result" && block.tool_result) {
        text += JSON.stringify(block.tool_result);
      }
    }
  } else if (msg.tool_result) {
    text = JSON.stringify(msg.tool_result);
  }
  return estimateTokens(text);
}

function getModelLimit(modelId, config) {
  const limits = config.modelLimits || {};
  // Exact match
  if (limits[modelId]) return limits[modelId];
  // Partial match (e.g. "kimi/k2p6" matches "kimi")
  for (const key of Object.keys(limits)) {
    if (modelId.includes(key) || key.includes(modelId)) {
      return limits[key];
    }
  }
  // Default fallback
  return 128000;
}

export default definePluginEntry({
  id: "context-window-guard",
  name: "Context Window Cost Guard",
  description:
    "Monitors conversation context window size and warns when approaching token limits.",

  register(api) {
    const config = api.pluginConfig || {};
    if (config.enabled === false) return;

    const warnThreshold = config.warnThreshold ?? 0.8;
    const panicThreshold = config.panicThreshold ?? 0.95;

    api.on("before_prompt_build", (event, ctx) => {
      const messages = event.messages || [];
      const modelId = ctx.modelId || event.modelId || "unknown";
      const limit = getModelLimit(modelId, config);

      let totalTokens = 0;
      for (const msg of messages) {
        totalTokens += estimateMessageTokens(msg);
      }

      const ratio = totalTokens / limit;
      const pct = Math.round(ratio * 100);

      if (ratio >= panicThreshold) {
        return {
          systemText:
            `\n⚠️ CONTEXT WINDOW PANIC: ${pct}% full (${totalTokens.toLocaleString()} / ${limit.toLocaleString()} tokens). ` +
            `IMMEDIATE ACTION REQUIRED: Summarize or compact history NOW to avoid truncation.`,
        };
      }

      if (ratio >= warnThreshold) {
        return {
          systemText:
            `\n⚠️ Context window warning: ${pct}% full (${totalTokens.toLocaleString()} / ${limit.toLocaleString()} tokens). ` +
            `Consider summarizing older messages to preserve room for reasoning.`,
        };
      }

      return;
    });
  },
});
