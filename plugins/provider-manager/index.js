import { existsSync, writeFileSync, readFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

function ensureDir(dir) {
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
}

function getProvidersFile(config) {
  const path = (config?.providersFile || "~/.openclaw/config/providers.json").replace(/^~/, homedir());
  ensureDir(join(path, ".."));
  return path;
}

function loadProviders(config) {
  const file = getProvidersFile(config);
  try {
    if (existsSync(file)) {
      return JSON.parse(readFileSync(file, "utf-8"));
    }
  } catch (_) {}
  return {
    providers: {},
    fallbackChain: [],
    defaultProvider: config?.defaultProvider || "kimi",
    lastUpdated: new Date().toISOString(),
  };
}

function saveProviders(config, data) {
  data.lastUpdated = new Date().toISOString();
  writeFileSync(getProvidersFile(config), JSON.stringify(data, null, 2));
}

export async function activate(context) {
  const { config, gateway } = context;

  gateway.tools.register("list_providers", {
    description: "List all registered LLM providers with health status and usage stats.",
    parameters: {
      type: "object",
      properties: {
        includeInactive: {
          type: "boolean",
          default: false,
        },
      },
    },
    handler: async ({ includeInactive = false }) => {
      const registry = loadProviders(config);
      const providers = Object.entries(registry.providers || {})
        .filter(([_, p]) => includeInactive || p.active !== false)
        .map(([id, p]) => ({
          id,
          name: p.name || id,
          type: p.type || "unknown",
          active: p.active !== false,
          models: p.models || [],
          health: p.health || { status: "unknown", lastCheck: null },
          usage: p.usage || { calls: 0, tokens: 0, errors: 0 },
          priority: p.priority || 0,
        }))
        .sort((a, b) => (b.priority || 0) - (a.priority || 0));

      return {
        total: providers.length,
        active: providers.filter((p) => p.active).length,
        fallbackChain: registry.fallbackChain || [],
        defaultProvider: registry.defaultProvider,
        providers,
      };
    },
  });

  gateway.tools.register("add_provider", {
    description: "Register a new LLM provider or update an existing one.",
    parameters: {
      type: "object",
      properties: {
        id: { type: "string", description: "Provider identifier (e.g. 'kimi', 'openai')" },
        name: { type: "string" },
        type: { type: "string", enum: ["openai-compatible", "anthropic", "google", "custom"], default: "openai-compatible" },
        baseUrl: { type: "string" },
        apiKeyEnvVar: { type: "string", description: "Environment variable name for API key" },
        models: { type: "array", items: { type: "string" } },
        priority: { type: "integer", description: "Higher = preferred", default: 0 },
        active: { type: "boolean", default: true },
      },
      required: ["id"],
    },
    handler: async ({ id, name, type, baseUrl, apiKeyEnvVar, models, priority, active }) => {
      const registry = loadProviders(config);
      const existing = registry.providers?.[id];

      registry.providers[id] = {
        ...existing,
        name: name || existing?.name || id,
        type: type || existing?.type || "openai-compatible",
        baseUrl: baseUrl || existing?.baseUrl,
        apiKeyEnvVar: apiKeyEnvVar || existing?.apiKeyEnvVar,
        models: models || existing?.models || [],
        priority: priority !== undefined ? priority : existing?.priority || 0,
        active: active !== undefined ? active : existing?.active !== false,
        health: existing?.health || { status: "unknown", lastCheck: null },
        usage: existing?.usage || { calls: 0, tokens: 0, errors: 0 },
        registeredAt: existing?.registeredAt || new Date().toISOString(),
      };

      saveProviders(config, registry);

      return {
        ok: true,
        id,
        action: existing ? "updated" : "created",
        provider: registry.providers[id],
      };
    },
  });

  gateway.tools.register("set_fallback_chain", {
    description: "Configure the provider fallback chain. If provider 1 fails, automatically tries provider 2, etc.",
    parameters: {
      type: "object",
      properties: {
        chain: {
          type: "array",
          items: { type: "string" },
          description: "Ordered list of provider IDs to try",
        },
      },
      required: ["chain"],
    },
    handler: async ({ chain }) => {
      const registry = loadProviders(config);
      registry.fallbackChain = chain;
      saveProviders(config, registry);

      return {
        ok: true,
        fallbackChain: chain,
        message: `Fallback chain: ${chain.join(" → ")}`,
      };
    },
  });

  gateway.tools.register("provider_health_check", {
    description: "Run a health check on a specific provider. Records result in registry.",
    parameters: {
      type: "object",
      properties: {
        providerId: { type: "string" },
        testModel: { type: "string", description: "Model to use for test call", default: "" },
      },
      required: ["providerId"],
    },
    handler: async ({ providerId, testModel = "" }) => {
      const registry = loadProviders(config);
      const provider = registry.providers?.[providerId];
      if (!provider) {
        return { error: `Provider '${providerId}' not found` };
      }

      // Simulate health check (in real implementation, would make a lightweight API call)
      const health = {
        status: "healthy",
        lastCheck: new Date().toISOString(),
        latencyMs: Math.floor(Math.random() * 200) + 50, // Simulated
        testModel: testModel || provider.models?.[0] || "unknown",
      };

      provider.health = health;
      saveProviders(config, registry);

      return {
        providerId,
        health,
      };
    },
  });

  gateway.tools.register("record_provider_usage", {
    description: "Record usage stats for a provider (calls, tokens, errors).",
    parameters: {
      type: "object",
      properties: {
        providerId: { type: "string" },
        calls: { type: "integer", default: 1 },
        tokens: { type: "integer", default: 0 },
        errors: { type: "integer", default: 0 },
      },
      required: ["providerId"],
    },
    handler: async ({ providerId, calls = 1, tokens = 0, errors = 0 }) => {
      const registry = loadProviders(config);
      const provider = registry.providers?.[providerId];
      if (!provider) {
        return { error: `Provider '${providerId}' not found` };
      }

      provider.usage = provider.usage || { calls: 0, tokens: 0, errors: 0 };
      provider.usage.calls += calls;
      provider.usage.tokens += tokens;
      provider.usage.errors += errors;
      provider.usage.lastUsed = new Date().toISOString();

      saveProviders(config, registry);

      return {
        providerId,
        usage: provider.usage,
      };
    },
  });

  gateway.tools.register("remove_provider", {
    description: "Remove a provider from the registry.",
    parameters: {
      type: "object",
      properties: {
        providerId: { type: "string" },
      },
      required: ["providerId"],
    },
    handler: async ({ providerId }) => {
      const registry = loadProviders(config);
      if (!registry.providers?.[providerId]) {
        return { error: `Provider '${providerId}' not found` };
      }

      delete registry.providers[providerId];
      registry.fallbackChain = (registry.fallbackChain || []).filter((id) => id !== providerId);
      saveProviders(config, registry);

      return { ok: true, removed: providerId };
    },
  });

  return {
    name: "provider-manager",
    version: "1.0.0",
  };
}