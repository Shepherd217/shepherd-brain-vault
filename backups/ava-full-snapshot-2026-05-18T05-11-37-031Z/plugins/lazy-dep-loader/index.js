import { execSync } from "node:child_process";
import { createRequire } from "node:module";
import { existsSync, mkdirSync, writeFileSync, readFileSync } from "node:fs";
import { join } from "node:path";

const require = createRequire(import.meta.url);
const LAZY_CACHE_DIR = join(process.cwd(), ".lazy-deps");
const LAZY_LOG_FILE = join(LAZY_CACHE_DIR, "install-log.json");

function ensureCacheDir() {
  if (!existsSync(LAZY_CACHE_DIR)) {
    mkdirSync(LAZY_CACHE_DIR, { recursive: true });
  }
}

function logInstall(moduleName, success, error = null) {
  ensureCacheDir();
  let log = {};
  try {
    if (existsSync(LAZY_LOG_FILE)) {
      log = JSON.parse(readFileSync(LAZY_LOG_FILE, "utf-8"));
    }
  } catch (_) {}
  log[moduleName] = {
    installedAt: new Date().toISOString(),
    success,
    error,
  };
  writeFileSync(LAZY_LOG_FILE, JSON.stringify(log, null, 2));
}

function tryRequire(moduleName) {
  try {
    return require(moduleName);
  } catch (_) {
    return null;
  }
}

function installNpm(moduleName, timeoutMs = 60000) {
  try {
    execSync(`npm install ${moduleName} --prefix ${LAZY_CACHE_DIR} --no-save --no-package-lock`, {
      timeout: timeoutMs,
      stdio: "pipe",
    });
    return true;
  } catch (e) {
    return false;
  }
}

function installPip(moduleName, timeoutMs = 60000) {
  try {
    execSync(`pip install ${moduleName} --target ${LAZY_CACHE_DIR}`, {
      timeout: timeoutMs,
      stdio: "pipe",
    });
    return true;
  } catch (e) {
    return false;
  }
}

export async function activate(context) {
  const { config, gateway } = context;

  gateway.tools.register("lazy_require", {
    description:
      "Lazily load a heavy dependency. Tries to require it first; if missing, auto-installs via npm or pip, then returns the module.",
    parameters: {
      type: "object",
      properties: {
        module: {
          type: "string",
          description: "NPM or PyPI package name to load",
        },
        packageManager: {
          type: "string",
          enum: ["npm", "pip", "auto"],
          description: "Which package manager to use if install needed",
          default: "auto",
        },
        timeoutMs: {
          type: "integer",
          description: "Max ms to wait for install",
          default: 60000,
        },
        importPath: {
          type: "string",
          description: "Sub-path to import from the package (e.g. '@anthropic-ai/sdk' -> 'sdk')",
        },
      },
      required: ["module"],
    },
    handler: async ({ module: moduleName, packageManager = "auto", timeoutMs = 60000, importPath }) => {
      // 1. Try to require directly
      let loaded = tryRequire(moduleName);
      if (loaded) {
        return {
          loaded: true,
          fromCache: true,
          installNeeded: false,
          module: moduleName,
        };
      }

      // 2. Determine package manager
      let pm = packageManager;
      if (pm === "auto") {
        pm = moduleName.startsWith("python-") || moduleName.includes("py-") ? "pip" : "npm";
      }

      // 3. Install
      const installed = pm === "pip" ? installPip(moduleName, timeoutMs) : installNpm(moduleName, timeoutMs);
      if (!installed) {
        logInstall(moduleName, false, `Failed to install via ${pm}`);
        return {
          loaded: false,
          error: `Failed to install ${moduleName} via ${pm}`,
          module: moduleName,
        };
      }

      // 4. Try require again
      loaded = tryRequire(moduleName);
      if (!loaded) {
        logInstall(moduleName, false, "Install succeeded but require still failed");
        return {
          loaded: false,
          error: `Installed ${moduleName} but could not require it`,
          module: moduleName,
        };
      }

      logInstall(moduleName, true);

      // 5. If importPath specified, drill into it
      if (importPath && typeof loaded === "object") {
        loaded = loaded[importPath] || loaded;
      }

      return {
        loaded: true,
        fromCache: false,
        installNeeded: true,
        installMethod: pm,
        module: moduleName,
      };
    },
  });

  gateway.tools.register("lazy_install_status", {
    description: "Check which lazy dependencies have been installed and when.",
    parameters: {
      type: "object",
      properties: {
        module: {
          type: "string",
          description: "Specific module to check (omit for all)",
        },
      },
    },
    handler: async ({ module: moduleName }) => {
      ensureCacheDir();
      let log = {};
      try {
        if (existsSync(LAZY_LOG_FILE)) {
          log = JSON.parse(readFileSync(LAZY_LOG_FILE, "utf-8"));
        }
      } catch (_) {}

      if (moduleName) {
        const entry = log[moduleName];
        return {
          module: moduleName,
          installed: !!entry,
          details: entry || null,
        };
      }

      return {
        totalInstalled: Object.keys(log).length,
        modules: log,
      };
    },
  });

  return {
    name: "lazy-dep-loader",
    version: "1.0.0",
  };
}
