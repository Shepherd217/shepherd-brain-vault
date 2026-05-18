# 🚨 AVA RECOVERY GUIDE

**If Ava has been deleted/reset, follow these steps to restore her.**

## Quick Recovery (5 minutes)

### Step 1: Clone the Brain Vault
```bash
git clone https://github.com/Shepherd217/shepherd-brain-vault.git
cd shepherd-brain-vault
```

### Step 2: Copy Plugins
```bash
cp -r plugins/* ~/.openclaw/workspace/plugins/
```

### Step 3: Copy Memory Files
```bash
cp memory/SOUL.md ~/.openclaw/workspace/
cp memory/USER.md ~/.openclaw/workspace/
cp memory/MEMORY.md ~/.openclaw/workspace/
cp memory/AGENTS.md ~/.openclaw/workspace/
cp memory/IDENTITY.md ~/.openclaw/workspace/
cp memory/TOOLS.md ~/.openclaw/workspace/
cp memory/HEARTBEAT.md ~/.openclaw/workspace/
```

### Step 4: Update OpenClaw Config
Edit ~/.openclaw/openclaw.json and add these plugin entries:

**Entries:**

- "file-mutation-verifier": { "enabled": true }
- "context-window-guard": { "enabled": true }
- "lazy-dep-loader": { "enabled": true }
- "prompt-cache": { "enabled": true }
- "persistent-browser": { "enabled": true }
- "agent-handoff": { "enabled": true }
- "checkpoint-v2": { "enabled": true }
- "platform-allowlist": { "enabled": true }
- "provider-manager": { "enabled": true }
- "mcp-tool-bridge": { "enabled": true }
- "prompt-context-triage": { "enabled": true }
- "auto-model-fallback": { "enabled": true }
- "agent-mesh": { "enabled": true }
- "task-router": { "enabled": true }
- "agent-specialization": { "enabled": true }

**Allow list:** Add all plugin IDs to plugins.allow array

**Load paths:** Add all plugin directories to plugins.load.paths array

### Step 5: Restart Gateway
```bash
openclaw gateway restart
```

### Step 6: Verify
```bash
openclaw plugins list
```

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

*Snapshot created: 2026-05-18T05:11:37.329Z*
*Agent: Ava v1.0 — Spark Engine*
