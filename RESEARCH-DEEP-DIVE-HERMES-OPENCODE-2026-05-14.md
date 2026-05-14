# 🔬 DEEP DIVE: HermesAgent Dashboard × OpenCode Parallelism × Unified Multi-Agent Architecture

**Research Date:** 2026-05-14  
**Agent:** Ava  
**Scope:** HermesAgent dashboard internals, OpenCode file isolation patterns, unified architecture for multi OpenClaw/HermesAgent team dashboard

---

## 📋 TABLE OF CONTENTS

1. [HermesAgent Dashboard — How It Works](#1-hermesagent-dashboard--how-it-works)
2. [OpenCode Parallel Agents — File Collision Prevention](#2-opencode-parallel-agents--file-collision-prevention)
3. [The Unified Architecture](#3-the-unified-architecture-shepherd-team-dashboard)
4. [Implementation Roadmap](#4-implementation-roadmap)
5. [Key Sources](#5-key-sources)

---

## 1. HERMESAGENT DASHBOARD — HOW IT WORKS

### 1.1 Overview

HermesAgent is a **self-hosted, model-agnostic AI agent** from Nous Research. It operates across **6 distinct surfaces** (thin adapters around a single `AIAgent` core):

| Surface | Technology | Purpose |
|---------|-----------|---------|
| **CLI** | Python (Rich, prompt_toolkit) | Classic terminal chat |
| **TUI** | Node.js + React Ink, JSON-RPC 2.0 over stdio | Interactive terminal UI with streaming chain-of-thought |
| **Gateway** | WebSocket/long-poll/webhook | Telegram, Discord, Slack, WhatsApp, Signal, iMessage, WeChat, QQ, Google Chat, Feishu, WeCom (20+ platforms) |
| **ACP** | Agent Client Protocol | Zed, VS Code, Cursor integration |
| **Batch** | Python orchestrator | Parallel task execution with worktree isolation |
| **API Server** | HTTP REST | Programmatic access |
| **Web Dashboard** | Browser-based (local) | Management interface |

### 1.2 Web Dashboard Features (v0.13.0 — "The Tenacity Release", May 2026)

The dashboard is a **browser-based management interface** running locally (default port varies by profile). Key capabilities:

#### Core Pages
- **Overview / Health** — Gateway status, connected platforms, system metrics
- **Plugins** — Manage, enable/disable, view auth status (extensible plugin system)
- **Profiles** — Multi-instance management (isolated configs, memories, sessions, skills, gateways)
- **Analytics** — Sortable tables, per-session API call tracking, usage insights (`/insights` command)
- **Settings** — Live config editor, model switching, theme switching
- **One-click update + gateway restart**
- **Reverse-proxy support** via `X-Forwarded-Prefix`
- **i18n** — 7 locales (Chinese, Japanese, German, Spanish, French, Ukrainian, Turkish)

#### Multi-Agent Kanban Board (v0.13.0)
This is the **crown jewel** for team coordination:

- **"One install, many kanbans"** — Multiple kanban boards per installation
- **Durable task board** — Tasks persist across agent restarts
- **Multiple Hermes workers** — Agents pick up tasks autonomously
- **Heartbeat system** — Workers report status periodically
- **Reclaim mechanism** — Stalled tasks get reassigned
- **Zombie detection** — Detect and recover from stuck agents
- **Auto-block on incomplete exit** — Prevent premature task closure
- **Per-task retry budgets** — Configurable retry limits
- **Hallucination recovery** — Detect and fix agent hallucinations
- **Task handoff** — Workers can pass tasks to each other
- **Task lifecycle**: backlog → in-progress → review → done

### 1.3 TUI (Terminal UI) — `hermes --tui`

Not just a "fancier CLI" — genuinely novel architecture:
- **Frontend:** Node.js + React Ink
- **Backend:** Python `tui_gateway/server.py`
- **Wire format:** Newline-delimited JSON-RPC 2.0 over stdio
- **Features:** Streaming chain-of-thought with braille spinners, `ToolTrail` tree visualization, virtual-history viewport, mouse selection
- **Design rule:** "Do not re-implement the chat surface in React." The transcript, composer, and slash commands belong to the embedded TUI.

### 1.4 Profile System — Multi-Instance Isolation

Each profile gets **complete isolation**:
- Own `HERMES_HOME` directory
- Own config (`config.yaml`)
- Own memory layer
- Own sessions (SQLite-based with FTS5)
- Own skills library
- Own gateway service (separate PID)
- **Token-lock isolation** — prevents two profiles from using the same bot credential

```bash
hermes profile create    # Create new isolated instance
hermes profile list      # List all profiles
hermes -p <name>         # Switch to profile
hermes profile export    # Export for sharing
hermes profile import    # Import from file
```

### 1.5 Agent Teams & Parallel Execution

#### `--teammate-mode` Flag
Controls how agent teams display:
- `auto` — Let system decide
- `in-process` — Same process
- `tmux` — Each agent in separate tmux pane

#### `/batch` Command
Auto-creates worktrees for large parallel changes:
```bash
/batch  # Creates 5-30 worktrees automatically
```

#### Subagent Isolation
```yaml
---
name: feature-implementer
description: Implements features in isolated worktrees
isolation: worktree  # ← This is the key!
tools:
  - read
  - write
  - bash
---
```

When orchestrator spawns multiple instances, each gets its own branch and working directory automatically.

#### "Smarter Delegation" (v0.12+)
- Subagents have explicit `orchestrator` role
- Configurable `max_spawn_depth` (default: flat)
- **Concurrent sibling subagents share filesystem state through a file-coordination layer** so they don't clobber each other's edits

### 1.6 Session Storage Architecture

- **SQLite-based** with FTS5 full-text search
- **Lineage tracking** — parent/child relationships across compressions
- **Per-platform isolation** — Telegram sessions separate from Discord sessions
- **Atomic writes** with contention handling
- **Gateway auto-resume** — interrupted sessions survive gateway restarts

### 1.7 Cron System

- `hermes cron` — Manage scheduled tasks
- `no_agent` watchdog mode — runs without loading full agent (lightweight)
- Tasks persist in memory layer

---

## 2. OPCODE PARALLEL AGENTS — FILE COLLISION PREVENTION

### 2.1 The Core Mechanism: Git Worktrees

**Git worktrees are the industry-standard isolation primitive** for parallel AI coding agents. By 2026, they're natively supported by Claude Code, OpenAI Codex, Cursor, Hermes, and OpenCode.

#### What Are Git Worktrees?

A git worktree creates a **linked working directory** that shares the same `.git` object database but has its own:
- `HEAD` (independent branch)
- Index (staging area)
- Working tree files

**Shared resources:**
- Object database (commits, blobs, trees)
- Remote configuration
- Packed refs

```bash
# Create a new worktree on a new branch
git worktree add -b feature-auth ../project-auth main

# List all active worktrees
git worktree list

# Remove a finished worktree
git worktree remove ../project-auth

# Clean stale metadata
git worktree prune
```

**Internals:** Each linked worktree contains a `.git` file (not directory) pointing back: `gitdir: /path/main/.git/worktrees/<name>`. Git uses `$GIT_DIR` for worktree-specific data and `$GIT_COMMON_DIR` for shared resources.

### 2.2 OpenCode's Worktree Implementation

#### CLI Flag: `--worktree` / `-w`
```bash
# Create a named worktree
opencode --worktree feature-auth

# Auto-generate a name
opencode --worktree  # creates something like "bright-running-fox"

# Start parallel sessions
opencode --worktree feature-a &
opencode --worktree bugfix-123 &
```

**Location:** `<repo>/.opencode/worktrees/<name>`  
**Branch naming:** `opencode/<name>`  
**Base branch:** Default remote branch

#### Cleanup Behavior
- **No changes made** → worktree and branch auto-removed on exit
- **Changes or commits exist** → OpenCode prompts: keep or remove

#### Subagent Worktree Isolation (The `isolation: worktree` Directive)

```yaml
---
name: feature-implementer
description: Implements features in isolated worktrees
isolation: worktree  # ← Orchestrator provisions fresh worktree per invocation
tools:
  - read
  - write
  - bash
---
```

When the orchestrator spawns multiple parallel subagents, **each gets its own branch and working directory automatically**. The worktree is cleaned up when the subagent finishes without uncommitted changes.

#### `/batch` Command (Interactive Mode)
```
/batch  # Auto-creates 5-30 worktrees for large parallel changes
```

### 2.3 Agent Teams in OpenCode

#### `--teammate-mode` Display Options
| Mode | Behavior |
|------|----------|
| `auto` | System decides best display method |
| `in-process` | All agents in same process |
| `tmux` | Each agent in separate tmux pane |

#### File Coordination Layer
OpenCode has a **"Smarter delegation"** feature where concurrent sibling subagents share filesystem state through a file-coordination layer to prevent clobbering each other's edits.

### 2.4 Worktree-Aware Environment Isolation

A critical gap that OpenCode and others are addressing:

**Problem:** Multiple agents in worktrees share the same database and dev server port, so migrations from one agent can corrupt other sessions.

**Solution:** Agent awareness of worktree context:
- Auto-detect worktree on session start
- Communicate environment info: "Your app is running at localhost:5174, worktree: feature-billing"
- Per-worktree `.env.local` generation
- Automatic port allocation (no conflicts)

### 2.5 Comparison: Isolation Approaches

| Approach | Creation Time | Disk Overhead | Port/DB Isolation | Merge Complexity | Best For |
|----------|--------------|---------------|-------------------|------------------|----------|
| **Git worktree** | ~1 second | Working tree only | None (shared) | Standard git | Parallel feature dev |
| **Full clone** | ~30-120s | Full repo copy | None (shared) | Manual remote sync | Long-lived forks |
| **Docker container** | ~10-60s | Image layers | Full | Docker volume mounts | Full env isolation |
| **VM / sandbox** | Minutes | OS + app | Full | Snapshot/sync tools | Security-critical |
| **Temp directory** | Instant | Full copy | None | Manual file copy | Throwaway experiments |

**Worktrees win when:** Agents need to share history, work on the same codebase, and produce commits that go back to the same remote.

**The hybrid pattern** — worktree per agent + lightweight container per worktree (isolated DB + dev server) — is the **emerging production standard** for teams running 4+ concurrent agents.

### 2.6 Known Limitations

#### Global Team Storage Bug
Agent teams are stored globally at `~/.opencode/teams/` and `~/.opencode/tasks/`. This causes **race conditions** where one instance's cleanup affects teams in other worktrees. The fix is moving team files into the worktree.

#### Submodule Worktree Bug
Worktrees created inside `.git/modules/<path>/` instead of the project root, breaking permission scopes. Workaround: Don't use worktree isolation for submodule repos.

---

## 3. THE UNIFIED ARCHITECTURE: SHEPHERD TEAM DASHBOARD

### 3.1 Vision Statement

> A unified web dashboard that orchestrates **both OpenClaw and HermesAgent instances** (and any MCP-compatible agent), provides **Kanban task management** with **git worktree isolation** for parallel execution, supports **human + AI teams**, and gives **real-time visibility** into all agent activity across all surfaces.

### 3.2 Why Unify?

| HermesAgent Strengths | OpenClaw Strengths | Unified = Best of Both |
|------------------------|-------------------|------------------------|
| Deep memory & skills | 35+ CLI commands, 20+ channels | Deep memory + broad connectivity |
| Multi-agent Kanban | Subagent spawning (`sessions_spawn`) | Visual Kanban + programmatic orchestration |
| Profile isolation | Session isolation | True multi-tenancy |
| TUI with React Ink | Web Control UI + Canvas | Rich terminal + rich web |
| Self-improving skills | 3,200+ ClawHub skills | Shared skill marketplace |
| Gateway for 20+ platforms | Heartbeat + cron hybrid | Unified messaging |
| ACP protocol support | Browser automation | IDE + web integration |

### 3.3 Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│  UNIFIED DASHBOARD (React/Next.js, runs on VPS)              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │  Kanban  │ │ Sessions │ │ Agents   │ │  Costs   │          │
│  │  Board   │ │  Monitor │ │  Panel   │ │  Tracker │          │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │  Worktrees│ │  Logs    │ │  Skills  │ │  Memory  │          │
│  │  Manager  │ │  Stream  │ │  Store   │ │  Viewer  │          │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
        ┌─────▼─────┐  ┌────▼────┐  ┌────▼────┐
        │  OpenClaw │  │ Hermes  │  │  Other  │
        │  Gateway  │  │ Agent   │  │  MCP    │
        │ (WebSocket│  │ (HTTP/  │  │ Agents  │
        │   18789)  │  │  stdio) │  │         │
        └─────┬─────┘  └────┬────┘  └────┬────┘
              │             │            │
        ┌─────▼─────────────▼────────────▼─────┐
        │      SHARED ORCHESTRATION LAYER      │
        │  ┌─────────────────────────────────┐  │
        │  │  Task Queue (SQLite/PostgreSQL)│  │
        │  │  ├─ Tasks: pending → doing →   │  │
        │  │  │   review → done → failed    │  │
        │  │  ├─ DAG dependencies           │  │
        │  │  ├─ Retry budgets              │  │
        │  │  └─ Assignment: human or agent │  │
        │  └─────────────────────────────────┘  │
        │  ┌─────────────────────────────────┐  │
        │  │  Git Worktree Manager           │  │
        │  │  ├─ Auto-create worktrees       │  │
        │  │  ├─ Per-agent branch isolation  │  │
        │  │  ├─ Auto-cleanup on completion  │  │
        │  │  └─ Port allocation per worktree│  │
        │  └─────────────────────────────────┘  │
        │  ┌─────────────────────────────────┐  │
        │  │  Event Bus (WebSocket/SSE)      │  │
        │  │  ├─ Agent heartbeats            │  │
        │  │  ├─ Task status changes         │  │
        │  │  ├─ File system events          │  │
        │  │  └─ Human approvals             │  │
        │  └─────────────────────────────────┘  │
        │  ┌─────────────────────────────────┐  │
        │  │  ClawMem (Shared Memory)      │  │
        │  │  ├─ Cross-agent memory          │  │
        │  │  ├─ BM25 + semantic search      │  │
        │  │  └─ Decision log indexing       │  │
        │  └─────────────────────────────────┘  │
        └───────────────────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  HUMAN INTERFACES   │
                    │  Telegram │ Discord │
                    │  Slack    │ Web Chat│
                    └─────────────────────┘
```

### 3.4 Dashboard Modules

#### Module 1: Unified Kanban Board
**Inspired by:** HermesAgent's multi-agent Kanban + `agent-board` + `CoMind`

**Features:**
- **6 columns:** `backlog` → `todo` → `doing` → `review` → `done` → `failed`
- **DAG dependencies** — Tasks can depend on others; cycle detection prevents deadlocks
- **Quality gates** — `requiresReview: true` forces review before done
- **Auto-retry** — Failed tasks automatically retry up to `maxRetries`
- **Task chaining** — `nextTask` auto-creates follow-up work
- **Real-time sync** — WebSocket updates when any agent moves a task
- **Agent assignment** — Assign to specific agent (OpenClaw or Hermes) or "any"
- **Human assignment** — Tasks can be assigned to human team members
- **Parallel execution** — Multiple agents pick up `todo` tasks simultaneously

**Task object:**
```json
{
  "id": "task_abc123",
  "projectId": "proj_shepherd",
  "title": "Implement reflection loop",
  "description": "Build auto-reflection on task completion",
  "status": "doing",
  "assignee": "ava",           // Can be "ava", "hermes", "eve", "nathan", "any"
  "agentType": "openclaw",     // "openclaw" | "hermes" | "human"
  "priority": "high",
  "tags": ["reflection", "skill"],
  "dependencies": ["task_xyz789"],
  "requiresReview": true,
  "maxRetries": 3,
  "worktree": "shepherd/ava-001",  // Isolated workspace for this task
  "nextTask": {
    "title": "Document reflection loop",
    "assignee": "eve",
    "agentType": "openclaw"
  },
  "createdAt": "2026-05-14T10:00:00Z",
  "startedAt": "2026-05-14T10:05:00Z",
  "completedAt": null,
  "attempts": 1,
  "result": null
}
```

#### Module 2: Worktree Manager
**Inspired by:** OpenCode's `--worktree` + Hermes's `/batch` + `worktree-mcp`

**Features:**
- **Auto-create worktrees** when task assigned to agent
- **Per-task branch naming:** `dashboard/<task-id>`
- **Base branch selection:** `main`, `develop`, or custom
- **Port allocation:** Auto-assign unique dev server ports per worktree
- **Environment generation:** `.env.local` per worktree
- **Lifecycle hooks:** Setup/teardown commands
- **State persistence:** Survives dashboard restart
- **Cleanup policies:**
  - Auto-remove if clean (no uncommitted changes)
  - Prompt if dirty (changes exist)
  - Never remove (for important work)

**Worktree object:**
```json
{
  "id": "wt_abc123",
  "taskId": "task_abc123",
  "repoPath": "/home/shepherd/workspace",
  "worktreePath": "/home/shepherd/workspace/.worktrees/task-abc123",
  "branch": "dashboard/task-abc123",
  "baseBranch": "main",
  "port": 5174,
  "envFile": "/home/shepherd/workspace/.worktrees/task-abc123/.env.local",
  "status": "active",
  "createdAt": "2026-05-14T10:05:00Z",
  "lastActivity": "2026-05-14T10:30:00Z"
}
```

#### Module 3: Agent Monitor
**Inspired by:** Hermes's TUI + OpenClaw's session status

**Features:**
- **Real-time status:** `idle` | `working` | `stalled` | `error` | `offline`
- **Heartbeat visualization:** Last heartbeat timestamp, health indicator
- **Current task:** What the agent is working on right now
- **Token usage:** Per-session cost tracking
- **Model in use:** Which LLM the agent is running
- **Surface:** CLI | TUI | Gateway (Telegram/Discord) | Web Dashboard
- **Quick actions:** Pause, resume, restart, steer
- **Session history:** Past tasks, success rate, average duration

**Agent card:**
```json
{
  "id": "ava",
  "name": "Ava",
  "type": "openclaw",
  "status": "working",
  "currentTask": "task_abc123",
  "model": "kimi/k2p6",
  "surface": "telegram",
  "lastHeartbeat": "2026-05-14T10:35:00Z",
  "tokenUsage": {
    "today": 45000,
    "thisWeek": 320000
  },
  "successRate": 0.94,
  "avgTaskDuration": 1800
}
```

#### Module 4: Session Stream
**Inspired by:** Hermes's activity feed + OpenClaw's real-time logs

**Features:**
- **Terminal-style viewer** (xterm.js) with ANSI colors
- **Agent activity coalescing** — Groups "thinking" + "command" + "output" into single events
- **Filter by agent:** Show only Ava, only Hermes, etc.
- **Filter by task:** Show only events for a specific task
- **Search:** Full-text search across all activity
- **Export:** Download session logs

#### Module 5: Skills Store
**Inspired by:** Hermes's skill system + OpenClaw's ClawHub

**Features:**
- **Unified skill registry:** Both OpenClaw skills and Hermes skills
- **Cross-platform skills:** Skills that work on both runtimes
- **Installation:** One-click install from ClawHub or Hermes registry
- **Configuration:** API keys, parameters per skill
- **Status indicators:** Green (ready) | Yellow (missing deps) | Red (error)

#### Module 6: Human Approval Queue
**Inspired by:** OpenClaw's `exec.ask` mode + Hermes's approval system

**Features:**
- **Pending approvals:** List of actions waiting for human OK
- **Context preview:** Show exactly what the agent wants to do
- **One-click approve/deny:** With optional comment
- **Auto-approve policies:** Configurable (e.g., "auto-approve read operations")
- **Slack/Telegram integration:** Send approvals to human's preferred channel

#### Module 7: Memory Viewer
**Inspired by:** ClawMem + Hermes's memory layer

**Features:**
- **Search across all agent memories:** BM25 + semantic hybrid
- **Decision log:** Indexed decision records from all agents
- **Shared context:** What all agents know about the project
- **Per-agent memory:** What each agent remembers individually
- **Visual graph:** Relationship between memories, tasks, and decisions

### 3.5 Agent Integration Adapters

#### OpenClaw Adapter
```typescript
// Connects to OpenClaw Gateway WebSocket
class OpenClawAdapter {
  gatewayUrl: string;      // ws://localhost:18789
  authToken: string;
  
  // Spawn a subagent for a task
  async spawnTask(task: Task): Promise<Session> {
    return sessions_spawn({
      task: task.description,
      label: task.id,
      model: task.modelOverride,
      runTimeoutSeconds: task.timeout,
      sandbox: "inherit"
    });
  }
  
  // Get agent status
  async getStatus(agentId: string): Promise<AgentStatus> {
    return session_status({ sessionKey: agentId });
  }
  
  // Send message to running session
  async steer(sessionKey: string, message: string): Promise<void> {
    return subagents("steer", { target: sessionKey, message });
  }
  
  // Listen for events
  onEvent(callback: (event: OpenClawEvent) => void): void {
    // WebSocket event listener
  }
}
```

#### HermesAgent Adapter
```typescript
// Connects to Hermes via HTTP API or stdio
class HermesAdapter {
  profile: string;        // Which Hermes profile to use
  apiUrl: string;         // http://localhost:9119 (per profile)
  
  // Spawn a task in Hermes
  async spawnTask(task: Task): Promise<Session> {
    // Option 1: HTTP API
    return fetch(`${this.apiUrl}/api/tasks`, {
      method: 'POST',
      body: JSON.stringify({
        prompt: task.description,
        worktree: true,           // Auto-create worktree
        skills: task.requiredSkills,
        model: task.modelOverride
      })
    });
    
    // Option 2: CLI invocation
    // hermes -w --profile ${this.profile} "${task.description}"
  }
  
  // Get agent status from Hermes dashboard API
  async getStatus(): Promise<AgentStatus> {
    return fetch(`${this.apiUrl}/api/status`);
  }
  
  // Listen for events (SSE or WebSocket)
  onEvent(callback: (event: HermesEvent) => void): void {
    // Server-Sent Events from Hermes
  }
}
```

#### MCP Server Mode
The dashboard itself exposes an **MCP server** so agents can interact with it:

```typescript
// MCP tools exposed by the dashboard
const mcpTools = {
  "create_task": CreateTaskSchema,
  "move_task": MoveTaskSchema,
  "claim_task": ClaimTaskSchema,
  "list_tasks": ListTasksSchema,
  "get_task": GetTaskSchema,
  "add_comment": AddCommentSchema,
  "get_worktree": GetWorktreeSchema,
  "create_worktree": CreateWorktreeSchema,
  "get_agent_status": GetAgentStatusSchema,
  "steer_agent": SteerAgentSchema
};
```

### 3.6 Event Flow: Task Lifecycle

```
Human creates task on Kanban
        │
        ▼
┌───────────────┐
│  Task Queue   │
│  (backlog)    │
└───────┬───────┘
        │
        ▼
Agent claims task (or auto-assigned)
        │
        ▼
┌───────────────┐
│ Worktree      │
│ Manager       │
│ creates       │
│ isolated      │
│ workspace     │
└───────┬───────┘
        │
        ▼
┌───────────────┐     ┌───────────────┐
│ OpenClaw      │     │ HermesAgent   │
│ Adapter       │     │ Adapter       │
│ spawns        │     │ spawns        │
│ subagent      │     │ task in       │
│ in worktree   │     │ worktree      │
└───────┬───────┘     └───────┬───────┘
        │                     │
        ▼                     ▼
┌─────────────────────────────────────┐
│  Agent works in isolated worktree   │
│  ├─ Makes changes                   │
│  ├─ Commits to branch             │
│  ├─ Reports progress via events     │
│  └─ Requests human approval if needed│
└─────────────────────────────────────┘
        │
        ▼
┌───────────────┐
│ Task moved to │
│ review / done │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Worktree      │
│ cleanup       │
│ (auto or      │
│ manual)       │
└───────────────┘
```

### 3.7 Multi-Gateway Support

The dashboard can connect to **multiple OpenClaw gateways** and **multiple Hermes profiles** simultaneously:

```typescript
interface GatewayConnection {
  id: string;
  name: string;
  type: "openclaw" | "hermes";
  url: string;
  authToken: string;
  status: "connected" | "disconnected" | "error";
  agents: Agent[];
}

// Example: Shepherd Team Setup
const connections = [
  { id: "gw-1", name: "Ava's Gateway", type: "openclaw", url: "ws://localhost:18789" },
  { id: "gw-2", name: "Hermes Dev", type: "hermes", url: "http://localhost:9119" },
  { id: "gw-3", name: "Eve's Gateway", type: "openclaw", url: "ws://eve-vps:18789" }
];
```

---

## 4. IMPLEMENTATION ROADMAP

### Phase 1: Foundation (Week 1-2)
1. **Set up dashboard repo** — Next.js + TypeScript + Tailwind
2. **Task queue API** — SQLite backend with REST API
3. **Basic Kanban UI** — Drag-and-drop (react-beautiful-dnd)
4. **OpenClaw adapter** — WebSocket connection to gateway
5. **Single-gateway demo** — Spawn OpenClaw subagents for Kanban tasks

### Phase 2: Worktree Isolation (Week 3-4)
6. **Git worktree manager** — Auto-create/cleanup worktrees
7. **Port allocation** — Unique ports per worktree
8. **Environment generation** — `.env.local` per workspace
9. **File coordination layer** — Prevent concurrent edit conflicts
10. **OpenCode/Hermes worktree compatibility** — Standardize on `.worktrees/<task-id>/`

### Phase 3: Multi-Agent (Week 5-6)
11. **HermesAgent adapter** — HTTP + CLI integration
12. **Multi-gateway support** — Connect to multiple OpenClaw + Hermes instances
13. **Agent registry** — Discovery and status monitoring
14. **Heartbeat system** — Health checks for all connected agents
15. **Zombie detection** — Reclaim stalled tasks

### Phase 4: Team Features (Week 7-8)
16. **Human assignment** — Tasks for human team members
17. **Approval queue** — Human-in-the-loop for critical operations
18. **Role-based access** — Admin, Operator, Viewer roles
19. **Slack/Telegram integration** — Notifications and approvals
20. **MCP server** — Expose dashboard tools to agents

### Phase 5: Intelligence (Week 9-10)
21. **ClawMem integration** — Shared memory across all agents
22. **Decision log indexing** — Auto-index agent decisions
23. **Auto-assignment** — AI-suggested task assignments based on agent capabilities
24. **Workload balancing** — Detect overload and redistribute
25. **Performance analytics** — Per-agent and team metrics

---

## 5. KEY SOURCES

1. **Hermes Agent v0.13.0 Release Notes** — NousResearch/hermes-agent (May 7, 2026)
2. **Hermes Agent CLI Commands Reference** — hermes-agent.nousresearch.com (April 8, 2026)
3. **Hermes Agent Deep Dive** — dev.to/truongpx396 (April 30, 2026)
4. **Hermes Agent Guide** — blakecrosley.com (May 7, 2026)
5. **Git Worktree Isolation for Parallel CLI Sessions** — Hermes GitHub issue #652 (March 7, 2026)
6. **OpenCode CLI Documentation** — opencode.ai (2026)
7. **OpenCode Agent Teams** — opencode.ai docs (2026)
8. **Git Worktree Isolation Patterns** — zylos.ai research (Feb 22, 2026)
9. **Claude Code Worktree Isolation** — Anthropic docs (2026)
10. **worktree-mcp** — broskees/worktree-mcp (Jan 12, 2026)
11. **Agent of Empires** — betterstack.com (May 10, 2026)
12. **OpenClaw Web Control UI** — ququ123.top (Feb 26, 2026)
13. **OpenClaw Dashboard** — actionagentai/openclaw-dashboard (Feb 19, 2026)
14. **agent-board** — quentintou/agent-board (2026)
15. **CoMind** — dqalex/Comind (2026)
16. **HZL** — tmchow/hzl (Jan 29, 2026)
17. **clawtrol** — nachoiacovino/clawtrol (Feb 11, 2026)
18. **OpenClaw Subagent Orchestration** — stack-junkie.com (March 26, 2026)
19. **OpenClaw Multi-Agent Setup** — lumadock.com (Feb 21, 2026)
20. **Agent Teams Issue** — openclaw/openclaw #10010 (Feb 5, 2026)

---

## APPENDIX: Existing Dashboard Comparison

| Dashboard | OpenClaw | Hermes | Kanban | Worktrees | Multi-Gateway | MCP | Open Source |
|-----------|----------|--------|--------|-----------|---------------|-----|-------------|
| **Hermes Dashboard** | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| **OpenClaw Web UI** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **openclaw-dashboard** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **agent-board** | ✅ | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ |
| **CoMind** | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| **clawtrol** | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| **VidClaw** | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| **AgentCenter** | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ Commercial |
| **Agent of Empires** | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ |
| **SHEPHERD DASHBOARD** (proposed) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

*End of Deep Dive Research Brief*
