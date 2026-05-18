import { existsSync, writeFileSync, readFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

function ensureDir(dir) {
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
}

function getStateFile(config) {
  const path = (config?.stateFile || "~/.openclaw/config/fallback-state.json").replace(/^~/, homedir());
  ensureDir(join(path, ".."));
  return path;
}

function loadState(config) {
  const file = getStateFile(config);
  try {
    if (existsSync(file)) {
      return JSON.parse(readFileSync(file, "utf-8"));
    }
  } catch (_) {}
  return {
    currentProvider: config?.primaryProvider || "kimi",
    fallbackChain: config?.fallbackChain || ["kimi", "openai", "anthropic"],
    providerHealth: {},
    lastFallback: null,
    totalFallbacks: 0
  };
}

function saveState(config, data) {
  writeFileSync(getStateFile(config), JSON.stringify(data, null, 2));
}

export async function activate(context) {
  const { config, gateway } = context;

  gateway.tools.register("check_model_health", {
    description: "Check health of a specific model/provider and return status.",
    parameters: {
      type: "object",
      properties": {
        provider: { type: "string", description: "Provider to check" },
        testPrompt: { type: "string", default: "Hello", description: "Test prompt for health check" }
      },
      required: ["provider"]
    },
    handler: async ({ provider, testPrompt = "Hello" }) => {
      const state = loadState(config);
      
      // Simulated health check
      const isHealthy = Math.random() > 0.1; // 90% success rate for demo
      const latency = Math.floor(Math.random() * 2000) + 100;
      
      state.providerHealth[provider] = {
        healthy: isHealthy,
        latency,
        lastCheck: new Date().toISOString(),
        consecutiveFailures: isHealthy ? 0 : (state.providerHealth[provider]?.consecutiveFailures || 0) + 1
      };
      
      saveState(config, state);
      
      return {
        provider,
        healthy: isHealthy,
        latency,
        consecutiveFailures: state.providerHealth[provider].consecutiveFailures,
        recommendation: isHealthy ? "Provider healthy" : `Provider unhealthy — consider fallback after ${3 - state.providerHealth[provider].consecutiveFailures} more failures`
      };
    }
  });

  gateway.tools.register("force_fallback", {
    description: "Manually trigger a fallback to the next provider in the chain.",
    parameters: {
      type: "object",
      properties: {
        reason: { type: "string", description: "Why fallback is needed" }
      }
    },
    handler: async ({ reason = "Manual fallback" }) => {
      const state = loadState(config);
      const chain = state.fallbackChain;
      const currentIdx = chain.indexOf(state.currentProvider);
      const nextIdx = (currentIdx + 1) % chain.length;
      const nextProvider = chain[nextIdx];
      
      state.currentProvider = nextProvider;
      state.lastFallback = {
        from: chain[currentIdx],
        to: nextProvider,
        reason,
        timestamp: new Date().toISOString()
      };
      state.totalFallbacks += 1;
      
      saveState(config, state);
      
      return {
        fallback: true,
        from: chain[currentIdx],
        to: nextProvider,
        reason,
        totalFallbacks: state.totalFallbacks,
        chain
      };
    }
  });

  gateway.tools.register("get_fallback_status", {
    description: "Get current fallback status and provider health overview.",
    parameters: { type: "object", properties: {} },
    handler: async () => {
      const state = loadState(config);
      
      return {
        currentProvider: state.currentProvider,
        fallbackChain: state.fallbackChain,
        totalFallbacks: state.totalFallbacks,
        lastFallback: state.lastFallback,
        providerHealth: state.providerHealth,
        status: state.totalFallbacks === 0 ? "healthy" : "degraded"
      };
    }
  });

  return {
    name: "auto-model-fallback",
    version: "1.0.0"
  };
}
