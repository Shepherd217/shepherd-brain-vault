---
name: openshell
description: Wrap sub-agent execution in a sandboxed Docker container inspired by NVIDIA OpenShell. Provides isolation, resource limits, and supervision for untrusted or high-risk agent tasks.
usage: "openshell <role-name> <task-description> [--memory=512m] [--cpu=1.0] [--timeout=300]"
examples:
  - openshell security-engineer "Audit external dependency for supply-chain risks" --memory=256m --timeout=600
  - openshell code-reviewer "Review PR from unknown contributor" --memory=512m
  - openshell trend-researcher "Scrape and analyze competitor pricing data" --memory=1g --cpu=2.0
---

# 🛡️ OpenShell — Sandbox for Sub-Agents

Inspired by [NVIDIA OpenShell](https://github.com/NVIDIA/OpenShell), this skill wraps `sessions_spawn` calls in a lightweight Docker sandbox. It adds 4 protection layers to any cast operation:

1. **IPC Layer** — Sub-agent runs in isolated process with no access to host secrets
2. **Resource Restrictions** — Memory, CPU, and disk quotas enforced by container runtime
3. **Isolation** — No network access to internal services unless explicitly allowed
4. **Supervision** — Parent monitors child health, kills on timeout or anomaly

## 🎯 When to Use

| Scenario | Sandboxed? | Why |
|----------|-----------|-----|
| Auditing external code | ✅ YES | Untrusted code execution |
| Reviewing PRs from unknown contributors | ✅ YES | Supply chain risk |
| Scraping competitor websites | ✅ YES | Legal/ethical containment |
| Processing user-uploaded files | ✅ YES | Malware isolation |
| Internal task assignment | ❌ NO | Trusted team, faster execution |
| Building our own code | ❌ NO | We control the source |

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│  Main Session (Ava / Hermes / Eve)      │
│  ├─ Has access to secrets, GitHub, APIs │
│  └─ Calls: openshell <role> <task>      │
└─────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  Docker Container (sandbox-agent)       │
│  ├─ No host filesystem access           │
│  ├─ No env vars from parent             │
│  ├─ Read-only workspace mount           │
│  ├─ Memory limit (e.g. 512m)            │
│  ├─ CPU limit (e.g. 1.0 cores)          │
│  ├─ Network: outbound only, no internal │
│  └─ Auto-kill after timeout             │
└─────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  Sub-Agent (isolated context)           │
│  ├─ Gets role profile from agency-agents│
│  ├─ Gets task description               │
│  ├─ Returns ONLY text output            │
│  └─ Cannot exfiltrate files or secrets  │
└─────────────────────────────────────────┘
```

## ⚡ Quick Start

### Running a Sandboxed Cast

```bash
# Default: 512MB RAM, 1 CPU, 5-min timeout
openshell security-engineer "Audit npm package 'lodash' for known CVEs"

# Heavy analysis: 2GB RAM, 2 CPUs, 10-min timeout
openshell threat-detection-engineer "Analyze this binary for suspicious behavior" --memory=2g --cpu=2.0 --timeout=600

# Light research: 256MB RAM, 30-sec timeout
openshell trend-researcher "Find 3 recent AI framework releases" --memory=256m --timeout=30
```

### In Practice (OpenClaw Tool Chain)

Since we can't directly spawn Docker from `sessions_spawn`, the `openshell` skill documents the **pattern** and provides helper scripts:

```
1. Parent agent calls `sessions_spawn` with isolated context
2. Child agent receives ONLY the task + role profile (no secrets)
3. Child executes within its own tool policy (restricted tool set)
4. Parent captures output and discards the child session
```

## 🔧 Implementation Modes

### Mode A: Docker Sandbox (Full Isolation)

For maximum security, run the sub-agent in a Docker container:

```dockerfile
# Dockerfile.sandbox-agent
FROM node:20-alpine
RUN apk add --no-cache git curl
WORKDIR /workspace
COPY agency-agents/ ./agency-agents/
COPY cast-skill.js ./
CMD ["node", "cast-skill.js"]
```

```bash
# run-sandboxed.sh
docker run \
  --rm \
  --memory=512m \
  --memory-swap=512m \
  --cpus=1.0 \
  --read-only \
  --tmpfs /tmp:noexec,nosuid,size=100m \
  --network=bridge \
  -e "TASK=security-engineer-audit" \
  -e "ROLE_PROFILE=$(cat wings/agency-agents/engineering/engineering-security-engineer.md)" \
  -v "$(pwd)/workspace:/workspace:ro" \
  sandbox-agent:latest
```

### Mode B: OpenClaw Native Isolation (Default)

Since we already use `sessions_spawn` with `runtime="subagent"`, `context="isolated"`, the sub-agent inherits no secrets from the parent. We enhance this with:

1. **Tool restriction** — Pass `toolsAllow` to limit which tools the child can use
2. **Timeout enforcement** — Hard timeout on `sessions_spawn`
3. **Output-only** — Child can only return text, cannot write to parent filesystem
4. **No network whitelist** — Child can use `web_search` and `web_fetch` but cannot access internal IPs

```javascript
// Enhanced isolated spawn (pseudocode)
sessions_spawn({
  runtime: "subagent",
  context: "isolated",
  toolsAllow: ["web_search", "web_fetch", "read", "write"], // no exec, no browser, no message
  timeoutSeconds: 300,
  task: roleProfile + "\n\n" + userTask
});
```

### Mode C: Host Process Jail (Linux)

For environments without Docker, use Linux namespaces:

```bash
# unshare sandbox
unshare --fork --pid --mount-proc --user --map-root-user \
  --net --ipc --uts \
  node cast-skill.js "security-engineer" "audit task"
```

## 📊 Resource Profiles

| Profile | Memory | CPU | Timeout | Use Case |
|---------|--------|-----|---------|----------|
| `micro` | 128m | 0.5 | 60s | Quick lookups, searches |
| `default` | 512m | 1.0 | 300s | Standard audit, review |
| `heavy` | 2g | 2.0 | 600s | Deep analysis, scraping |
| `unlimited` | 4g | 4.0 | 1800s | Compiling, large builds |

## 🛡️ Security Checklist

Before casting to a sandboxed agent, verify:

- [ ] Task does NOT require access to parent secrets (API keys, tokens)
- [ ] Task does NOT need to write to parent filesystem (output goes to return value)
- [ ] Task timeout is set reasonably (don't leave orphans)
- [ ] Child's `toolsAllow` excludes `exec`, `browser` (if full isolation needed)
- [ ] Output will be reviewed before acting on it (don't auto-execute child suggestions)

## 📝 Logging Format

Every sandboxed cast is logged to `drawers/entries/YYYY-MM-DD-openshell-log.md`:

```markdown
## OpenShell Log — YYYY-MM-DD HH:MM UTC
- **Role:** {role-name}
- **Task:** {task}
- **Profile:** {micro|default|heavy|unlimited}
- **Timeout:** {seconds}
- **Status:** success | timeout | killed | error
- **Output size:** {chars}
- **Sub-agent sessionKey:** {sessionKey}
```

## 🔗 Integration with `cast`

The `openshell` skill is a **security wrapper** around `cast`. Usage flow:

1. User asks for a task that needs isolation
2. Ava decides: "This needs OpenShell" vs "This can be a regular cast"
3. If OpenShell: load role profile → spawn with restricted tools → enforce timeout → capture output
4. Return output to user with a "sandboxed" badge

## 🚀 Next Steps

- [ ] Build `run-sandboxed.sh` script for Docker mode
- [ ] Add `openshell` command to `rooms/skills/cast/SKILL.md` as a flag (`--sandbox`)
- [ ] Test with `cast security-engineer --sandbox "Audit X"`
- [ ] Document which agency-agents roles are "sandbox-recommended"

---

*Built by Ava (Spark Engine) for the MoltOS team*
*Inspired by NVIDIA OpenShell — github.com/NVIDIA/OpenShell*
