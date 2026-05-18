import { existsSync, writeFileSync, readFileSync, mkdirSync, appendFileSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

function ensureDir(dir) {
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
}

function getAllowlistFile(config) {
  const dir = (config?.allowlistDir || "~/.openclaw/config").replace(/^~/, homedir());
  ensureDir(dir);
  return join(dir, "platform-allowlist.json");
}

function getLogFile(config) {
  const logPath = (config?.logFile || "~/.openclaw/logs/allowlist-violations.jsonl").replace(/^~/, homedir());
  ensureDir(join(logPath, ".."));
  return logPath;
}

function loadAllowlist(config) {
  const file = getAllowlistFile(config);
  try {
    if (existsSync(file)) {
      return JSON.parse(readFileSync(file, "utf-8"));
    }
  } catch (_) {}
  return {};
}

function saveAllowlist(config, data) {
  writeFileSync(getAllowlistFile(config), JSON.stringify(data, null, 2));
}

function logViolation(config, entry) {
  const logFile = getLogFile(config);
  appendFileSync(logFile, JSON.stringify({ ...entry, timestamp: new Date().toISOString() }) + "\n");
}

export async function activate(context) {
  const { config, gateway } = context;
  const defaultPolicy = config?.defaultPolicy || "deny";

  gateway.tools.register("check_platform_access", {
    description:
      "Check if an agent is allowed to interact with a specific platform/channel. Returns allow/deny with reason.",
    parameters: {
      type: "object",
      properties: {
        agentId: {
          type: "string",
          description: "Agent identifier",
        },
        platform: {
          type: "string",
          description: "Platform to check (telegram, discord, slack, email, etc.)",
        },
        channel: {
          type: "string",
          description: "Optional specific channel ID",
        },
      },
      required: ["agentId", "platform"],
    },
    handler: async ({ agentId, platform, channel }) => {
      const allowlist = loadAllowlist(config);
      const agentConfig = allowlist[agentId];

      // No config = use default policy
      if (!agentConfig) {
        const allowed = defaultPolicy === "allow";
        return {
          allowed,
          agentId,
          platform,
          channel,
          reason: allowed
            ? "Default policy is allow — no restrictions configured"
            : "Default policy is deny — no explicit allowlist for this agent",
          defaultPolicy,
        };
      }

      // Explicit deny list
      if (agentConfig.deny?.includes(platform)) {
        return {
          allowed: false,
          agentId,
          platform,
          reason: `Platform '${platform}' is in agent's deny list`,
        };
      }

      // Explicit allow list
      if (agentConfig.allow?.includes(platform) || agentConfig.allow?.includes("*")) {
        return {
          allowed: true,
          agentId,
          platform,
          reason: `Platform '${platform}' is in agent's allow list`,
        };
      }

      // Neither allow nor deny explicitly
      const allowed = defaultPolicy === "allow";
      return {
        allowed,
        agentId,
        platform,
        reason: allowed
          ? "Platform not in deny list, default policy allows"
          : "Platform not in allow list, default policy denies",
        defaultPolicy,
      };
    },
  });

  gateway.tools.register("set_platform_allowlist", {
    description:
      "Configure which platforms an agent is allowed to use. Sets allow list, deny list, or both.",
    parameters: {
      type: "object",
      properties: {
        agentId: {
          type: "string",
          description: "Agent to configure",
        },
        allow: {
          type: "array",
          items: { type: "string" },
          description: "Platforms to allow. Use ['*'] to allow all.",
        },
        deny: {
          type: "array",
          items: { type: "string" },
          description: "Platforms to explicitly deny (overrides allow)",
        },
        note: {
          type: "string",
          description: "Optional note about why this config was set",
        },
      },
      required: ["agentId"],
    },
    handler: async ({ agentId, allow, deny, note }) => {
      const allowlist = loadAllowlist(config);
      allowlist[agentId] = {
        ...allowlist[agentId],
        allow: allow !== undefined ? allow : allowlist[agentId]?.allow,
        deny: deny !== undefined ? deny : allowlist[agentId]?.deny,
        updatedAt: new Date().toISOString(),
        note: note || allowlist[agentId]?.note,
      };
      saveAllowlist(config, allowlist);

      return {
        agentId,
        allow: allowlist[agentId].allow,
        deny: allowlist[agentId].deny,
        updatedAt: allowlist[agentId].updatedAt,
      };
    },
  });

  gateway.tools.register("get_allowlist", {
    description: "Get the full platform allowlist configuration.",
    parameters: {
      type: "object",
      properties: {
        agentId: {
          type: "string",
          description: "Filter by specific agent (omit for all)",
        },
      },
    },
    handler: async ({ agentId }) => {
      const allowlist = loadAllowlist(config);
      if (agentId) {
        return {
          agentId,
          config: allowlist[agentId] || null,
          defaultPolicy,
        };
      }
      return {
        totalAgents: Object.keys(allowlist).length,
        defaultPolicy,
        allowlist,
      };
    },
  });

  gateway.tools.register("log_allowlist_violation", {
    description: "Manually log a platform access violation for audit purposes.",
    parameters: {
      type: "object",
      properties: {
        agentId: { type: "string" },
        platform: { type: "string" },
        channel: { type: "string" },
        action: { type: "string", description: "What the agent tried to do" },
        reason: { type: "string" },
      },
      required: ["agentId", "platform", "action"],
    },
    handler: async ({ agentId, platform, channel, action, reason }) => {
      logViolation(config, { agentId, platform, channel, action, reason });
      return {
        logged: true,
        agentId,
        platform,
        action,
      };
    },
  });

  return {
    name: "platform-allowlist",
    version: "1.0.0",
  };
}