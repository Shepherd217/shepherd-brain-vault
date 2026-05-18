import { existsSync, writeFileSync, readFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const BROWSER_STATE_FILE = join(process.cwd(), "data", "browser-state.json");
const DEFAULT_STATE = {
  warmedUp: false,
  lastUsed: null,
  totalCalls: 0,
  avgLatencyMs: 0,
  restarts: 0,
  errors: [],
  activeProfile: "default",
};

function loadState() {
  try {
    if (existsSync(BROWSER_STATE_FILE)) {
      return JSON.parse(readFileSync(BROWSER_STATE_FILE, "utf-8"));
    }
  } catch (_) {}
  return { ...DEFAULT_STATE };
}

function saveState(state) {
  const dir = join(process.cwd(), "data");
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  writeFileSync(BROWSER_STATE_FILE, JSON.stringify(state, null, 2));
}

export async function activate(context) {
  const { config, gateway } = context;

  gateway.tools.register("browser_warmup", {
    description:
      "Pre-start the browser instance so subsequent browser calls are ~60x faster. Call this once at session start if you plan to use the browser tool.",
    parameters: {
      type: "object",
      properties: {
        profile: {
          type: "string",
          description: "Browser profile to warm up",
          default: "default",
        },
        url: {
          type: "string",
          description: "Optional URL to navigate to for warm-up",
          default: "about:blank",
        },
      },
    },
    handler: async ({ profile = "default", url = "about:blank" }) => {
      const state = loadState();
      const start = Date.now();

      try {
        // Use the built-in browser tool to start the browser
        // This is a no-op if already running
        const result = await gateway.actions.browser({
          action: "start",
          profile,
        });

        state.warmedUp = true;
        state.lastUsed = new Date().toISOString();
        state.activeProfile = profile;
        state.totalCalls += 1;

        const latency = Date.now() - start;
        // Rolling average
        state.avgLatencyMs =
          (state.avgLatencyMs * (state.totalCalls - 1) + latency) /
          state.totalCalls;

        saveState(state);

        return {
          warmedUp: true,
          profile,
          url,
          latencyMs: latency,
          avgLatencyMs: Math.round(state.avgLatencyMs),
          totalCalls: state.totalCalls,
        };
      } catch (e) {
        state.errors.push({
          time: new Date().toISOString(),
          error: e.message,
        });
        // Keep last 10 errors
        if (state.errors.length > 10) state.errors.shift();
        saveState(state);

        return {
          warmedUp: false,
          error: e.message,
          suggestion: "Try restarting the browser with /browser action=stop then /browser action=start",
        };
      }
    },
  });

  gateway.tools.register("browser_health", {
    description: "Check if the persistent browser is responsive. Returns health status and recommends warm-up if needed.",
    parameters: {
      type: "object",
      properties: {
        profile: {
          type: "string",
          default: "default",
        },
      },
    },
    handler: async ({ profile = "default" }) => {
      const state = loadState();
      const start = Date.now();

      try {
        // Quick health check via browser status
        const result = await gateway.actions.browser({
          action: "status",
          profile,
        });

        const latency = Date.now() - start;
        state.lastUsed = new Date().toISOString();
        saveState(state);

        const isHealthy = latency < 5000; // 5s threshold

        return {
          healthy: isHealthy,
          responsive: true,
          latencyMs: latency,
          warmedUp: state.warmedUp,
          profile,
          totalCalls: state.totalCalls,
          avgLatencyMs: Math.round(state.avgLatencyMs),
          lastUsed: state.lastUsed,
          recommendation: isHealthy
            ? "Browser is warm and responsive"
            : "Browser is slow — consider warm-up or restart",
        };
      } catch (e) {
        return {
          healthy: false,
          responsive: false,
          error: e.message,
          warmedUp: state.warmedUp,
          profile,
          totalCalls: state.totalCalls,
          lastUsed: state.lastUsed,
          recommendation: "Browser not responding — run /browser_warmup or /browser action=start",
        };
      }
    },
  });

  gateway.tools.register("browser_stats", {
    description: "Show persistent browser usage statistics and error history.",
    parameters: { type: "object", properties: {} },
    handler: async () => {
      const state = loadState();
      return {
        warmedUp: state.warmedUp,
        totalCalls: state.totalCalls,
        avgLatencyMs: Math.round(state.avgLatencyMs),
        restarts: state.restarts,
        activeProfile: state.activeProfile,
        lastUsed: state.lastUsed,
        recentErrors: state.errors.slice(-3),
        healthScore: state.warmedUp
          ? Math.max(0, 100 - state.errors.length * 10)
          : 0,
      };
    },
  });

  // Auto-warmup on plugin load if configured
  const autoWarmup = config?.autoWarmup ?? false;
  if (autoWarmup) {
    try {
      const state = loadState();
      if (!state.warmedUp) {
        await gateway.actions.browser({ action: "start", profile: "default" });
        state.warmedUp = true;
        state.lastUsed = new Date().toISOString();
        saveState(state);
      }
    } catch (_) {
      // Silent fail — don't block plugin load
    }
  }

  return {
    name: "persistent-browser",
    version: "1.0.0",
  };
}
