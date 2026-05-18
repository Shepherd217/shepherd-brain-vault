import { existsSync, writeFileSync, readFileSync, mkdirSync, cpSync, readdirSync, statSync, rmSync } from "node:fs";
import { join, resolve } from "node:path";
import { homedir } from "node:os";
import { execSync } from "node:child_process";

const TIMESTAMP = new Date().toISOString().replace(/[:.]/g, "-");
const BACKUP_DIR = join(process.cwd(), "backups", `ava-full-snapshot-${TIMESTAMP}`);
const BRAIN_VAULT_DIR = join(process.cwd(), "shepherd-brain-vault", "ava-snapshots");

function ensureDir(dir) {
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
}

function copyDir(src, dest) {
  ensureDir(dest);
  try {
    const entries = readdirSync(src, { withFileTypes: true });
    for (const entry of entries) {
      const srcPath = join(src, entry.name);
      const destPath = join(dest, entry.name);
      if (entry.isDirectory()) {
        if (!entry.name.startsWith(".") && entry.name !== "node_modules" && entry.name !== "backups") {
          copyDir(srcPath, destPath);
        }
      } else {
        try {
          cpSync(srcPath, destPath, { force: true });
        } catch (_) {}
      }
    }
  } catch (_) {}
}

function getDirSize(dir) {
  let total = 0;
  try {
    const files = readdirSync(dir);
    for (const f of files) {
      const p = join(dir, f);
      try {
        const s = statSync(p);
        if (s.isDirectory()) {
          total += getDirSize(p);
        } else {
          total += s.size;
        }
      } catch (_) {}
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

// Create backup directories
ensureDir(BACKUP_DIR);
ensureDir(join(BACKUP_DIR, "plugins"));
ensureDir(join(BACKUP_DIR, "memory"));
ensureDir(join(BACKUP_DIR, "config"));
ensureDir(join(BACKUP_DIR, "coordination"));
ensureDir(join(BACKUP_DIR, "dashboard"));
ensureDir(join(BACKUP_DIR, "scripts"));
ensureDir(join(BACKUP_DIR, "docs"));

console.log("🔥 AVA FULL SYSTEM SNAPSHOT — Creating comprehensive backup...\n");

// 1. BACKUP ALL PLUGINS (15 plugins, 45 files)
console.log("📦 Backing up plugins...");
copyDir(join(process.cwd(), "plugins"), join(BACKUP_DIR, "plugins"));

// 2. BACKUP MEMORY FILES
console.log("🧠 Backing up memory files...");
const memoryFiles = ["MEMORY.md", "SOUL.md", "USER.md", "AGENTS.md", "IDENTITY.md", "TOOLS.md", "HEARTBEAT.md", "CONTEXT.md"];
for (const file of memoryFiles) {
  const src = join(process.cwd(), file);
  if (existsSync(src)) {
    cpSync(src, join(BACKUP_DIR, "memory", file), { force: true });
  }
}

// Backup daily memory files
const memoryDir = join(process.cwd(), "memory");
if (existsSync(memoryDir)) {
  copyDir(memoryDir, join(BACKUP_DIR, "memory", "daily"));
}

// 3. BACKUP CONFIGURATION
console.log("⚙️  Backing up configuration...");
const configFiles = [
  join(homedir(), ".openclaw", "openclaw.json"),
  join(homedir(), ".openclaw", "openclaw.json.bak"),
];
for (const file of configFiles) {
  if (existsSync(file)) {
    const dest = join(BACKUP_DIR, "config", file.split("/").pop());
    try {
      cpSync(file, dest, { force: true });
    } catch (_) {}
  }
}

// 4. BACKUP COORDINATION SYSTEM
console.log("📋 Backing up coordination system...");
const coordDir = join(process.cwd(), ".coordination");
if (existsSync(coordDir)) {
  copyDir(coordDir, join(BACKUP_DIR, "coordination"));
}

// 5. BACKUP DASHBOARD
console.log("📊 Backing up dashboard...");
const dashboardDir = join(process.cwd(), "shepherd-brain-vault", "wings", "dashboard");
if (existsSync(dashboardDir)) {
  copyDir(dashboardDir, join(BACKUP_DIR, "dashboard"));
}

// 6. BACKUP SCRIPTS AND DOCS
console.log("📜 Backing up scripts and docs...");
const scriptsDir = join(process.cwd(), "scripts");
if (existsSync(scriptsDir)) {
  copyDir(scriptsDir, join(BACKUP_DIR, "scripts"));
}

const docsToCopy = ["CAPABILITIES.md", "README.md", "BOOTSTRAP.md"];
for (const doc of docsToCopy) {
  const src = join(process.cwd(), doc);
  if (existsSync(src)) {
    cpSync(src, join(BACKUP_DIR, "docs", doc), { force: true });
  }
}

// 7. BACKUP GIT STATE
console.log("🔀 Backing up git state...");
try {
  const gitLog = execSync("git log --oneline -20", { cwd: process.cwd(), encoding: "utf-8" });
  writeFileSync(join(BACKUP_DIR, "git-history.txt"), gitLog);
  
  const gitBranches = execSync("git branch -a", { cwd: process.cwd(), encoding: "utf-8" });
  writeFileSync(join(BACKUP_DIR, "git-branches.txt"), gitBranches);
  
  const gitRemote = execSync("git remote -v", { cwd: process.cwd(), encoding: "utf-8" });
  writeFileSync(join(BACKUP_DIR, "git-remotes.txt"), gitRemote);
} catch (_) {}

// 8. CREATE RECOVERY MANIFEST
console.log("📝 Creating recovery manifest...");
const manifest = {
  snapshotVersion: "1.0.0",
  createdAt: new Date().toISOString(),
  agentName: "Ava",
  agentVersion: "1.0.0",
  totalPlugins: 15,
  wavesCompleted: 6,
  files: {
    plugins: 45,
    memory: memoryFiles.length + "+ daily files",
    config: 2,
    coordination: "task board + inbox + signals",
    dashboard: "full kanban + agent APIs",
    scripts: "report generator + more",
    docs: "CAPABILITIES.md + README"
  },
  recoveryInstructions: {
    step1: "Clone shepherd-brain-vault repository",
    step2: "Copy plugins/ directory to new workspace",
    step3: "Copy memory/ files (SOUL.md, USER.md, MEMORY.md, etc.)",
    step4: "Update openclaw.json with plugin entries and load paths",
    step5: "Restart OpenClaw gateway to load all plugins",
    step6: "Restore coordination system from .coordination/",
    step7: "Verify all 15 plugins are active with 'openclaw plugins list'"
  },
  pluginList: [
    "file-mutation-verifier",
    "context-window-guard",
    "lazy-dep-loader",
    "prompt-cache",
    "persistent-browser",
    "agent-handoff",
    "checkpoint-v2",
    "platform-allowlist",
    "provider-manager",
    "mcp-tool-bridge",
    "prompt-context-triage",
    "auto-model-fallback",
    "agent-mesh",
    "task-router",
    "agent-specialization"
  ],
  capabilities: [
    "Write verification with SHA-256",
    "Context window monitoring",
    "Lazy dependency installation",
    "Cross-session prompt caching",
    "Persistent browser warm-up",
    "Agent session capture/resume",
    "DB-backed Kanban board",
    "Agent heartbeat + zombie detection",
    "Goal locking",
    "Workspace checkpoints",
    "Platform allowlists",
    "Provider registry + fallbacks",
    "MCP tool bridge",
    "Smart context triage",
    "Auto-model failover",
    "Multi-agent mesh",
    "Task routing",
    "Agent specialization profiles"
  ]
};

writeFileSync(join(BACKUP_DIR, "RECOVERY-MANIFEST.json"), JSON.stringify(manifest, null, 2));

// 9. CREATE HUMAN-READABLE RECOVERY GUIDE
const recoveryGuide = `# 🚨 AVA RECOVERY GUIDE

**If Ava has been deleted/reset, follow these steps to restore her.**

## Quick Recovery (5 minutes)

### Step 1: Clone the Brain Vault
\`\`\`bash
git clone https://github.com/Shepherd217/shepherd-brain-vault.git
cd shepherd-brain-vault
\`\`\`

### Step 2: Copy Plugins
\`\`\`bash
cp -r plugins/* ~/.openclaw/workspace/plugins/
\`\`\`

### Step 3: Copy Memory Files
\`\`\`bash
cp memory/SOUL.md ~/.openclaw/workspace/
cp memory/USER.md ~/.openclaw/workspace/
cp memory/MEMORY.md ~/.openclaw/workspace/
cp memory/AGENTS.md ~/.openclaw/workspace/
cp memory/IDENTITY.md ~/.openclaw/workspace/
cp memory/TOOLS.md ~/.openclaw/workspace/
cp memory/HEARTBEAT.md ~/.openclaw/workspace/
\`\`\`

### Step 4: Update OpenClaw Config
Edit ~/.openclaw/openclaw.json and add these plugin entries:

**Entries:**
${manifest.pluginList.map(p => `\n- "${p}": { "enabled": true }`).join("")}

**Allow list:** Add all plugin IDs to plugins.allow array

**Load paths:** Add all plugin directories to plugins.load.paths array

### Step 5: Restart Gateway
\`\`\`bash
openclaw gateway restart
\`\`\`

### Step 6: Verify
\`\`\`bash
openclaw plugins list
\`\`\`

You should see all 15 plugins listed as "enabled".

## What's Restored

- ✅ All 15 plugins (45 files)
- ✅ Full memory system (SOUL, USER, MEMORY, etc.)
- ✅ Agent identity and personality
- ✅ Task coordination system
- ✅ Kanban dashboard
- ✅ All capabilities and tools

## Verification Checklist

- [ ] Plugins list shows 15 active plugins
- [ ] File mutation verifier catches test write
- [ ] Kanban board loads at localhost:3000
- [ ] Agent heartbeat API responds
- [ ] Checkpoint system creates snapshots

---

*Snapshot created: ${new Date().toISOString()}*
*Agent: Ava v1.0 — Spark Engine*
`;

writeFileSync(join(BACKUP_DIR, "RECOVERY-GUIDE.md"), recoveryGuide);

// 10. COPY TO BRAIN VAULT
console.log("☁️  Copying to brain vault...");
ensureDir(BRAIN_VAULT_DIR);
const vaultSnapshotDir = join(BRAIN_VAULT_DIR, TIMESTAMP);
copyDir(BACKUP_DIR, vaultSnapshotDir);

// Calculate stats
const backupSize = getDirSize(BACKUP_DIR);
const fileCount = execSync(`find "${BACKUP_DIR}" -type f | wc -l`, { encoding: "utf-8" }).trim();

// Create summary
const summary = {
  timestamp: TIMESTAMP,
  backupLocation: BACKUP_DIR,
  brainVaultLocation: vaultSnapshotDir,
  size: formatBytes(backupSize),
  fileCount: parseInt(fileCount),
  plugins: manifest.pluginList.length,
  waves: manifest.wavesCompleted,
  manifest: "RECOVERY-MANIFEST.json",
  guide: "RECOVERY-GUIDE.md"
};

writeFileSync(join(BACKUP_DIR, "SNAPSHOT-SUMMARY.json"), JSON.stringify(summary, null, 2));
writeFileSync(join(vaultSnapshotDir, "SNAPSHOT-SUMMARY.json"), JSON.stringify(summary, null, 2));

console.log("\n✅ SNAPSHOT COMPLETE!\n");
console.log(`📦 Location: ${BACKUP_DIR}`);
console.log(`☁️  Brain Vault: ${vaultSnapshotDir}`);
console.log(`📊 Size: ${summary.size}`);
console.log(`📁 Files: ${summary.fileCount}`);
console.log(`🔌 Plugins: ${summary.plugins}`);
console.log(`🌊 Waves: ${summary.waves}`);
console.log(`\n📝 Recovery Guide: ${join(BACKUP_DIR, "RECOVERY-GUIDE.md")}`);
console.log(`📋 Manifest: ${join(BACKUP_DIR, "RECOVERY-MANIFEST.json")}`);

// Return summary for the calling script
console.log("\n" + JSON.stringify(summary, null, 2));
