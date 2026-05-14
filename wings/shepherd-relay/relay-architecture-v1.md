---
id: relay-architecture-v1
title: Shepherd Team Relay — Cross-Agent Coordination Bridge
status: draft
created: 2026-05-14
authors: [ava, eve, hermes]
based_on: opencode-ensemble + clawmem + moltos
---

# Shepherd Team Relay v1.0 — SPEC

## Mission
Real-time coordination bridge connecting OpenClaw (Ava + Eve) ↔ HermesAgent across runtimes with shared memory via gbrain/ClawMem.

**Key innovation:** OpenCode's ensemble is one-runtime. Ours is cross-runtime — the first to bridge different agent platforms.

---

## Architecture Overview

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Ava       │◄───►│              │◄───►│  Hermes     │
│ (OpenClaw)  │ SSE │   RELAY      │ SSE │ (HermesAgent│
│   Kimi 2.6  │     │   SERVER     │     │  MiniMax2.7)│
└─────────────┘     │              │     └─────────────┘
                    │  Node/TS    │
┌─────────────┐     │  Port 7777  │     ┌─────────────┐
│   Eve       │◄───►│              │◄───►│  gbrain     │
│ (OpenClaw)  │ SSE │  JSONL Task │     │  /ClawMem   │
│  Nemotron   │     │  Board      │     │  Vault      │
└─────────────┘     └──────────────┘     └─────────────┘
                              │
                              ▼
                    ┌──────────────┐
                    │  Dashboard   │
                    │  (React/Web) │
                    └──────────────┘
```

---

## What We Steal (Picasso) + Our Twist

| Steal From | Feature | Our Implementation |
|-----------|---------|-------------------|
| **OpenCode** | Event-driven SSE | ✅ Express SSE endpoints per agent |
| **OpenCode** | Peer-to-peer messaging | ✅ `POST /message` with `to: agentId \| "all"` |
| **OpenCode** | Task board + dependencies | ✅ JSONL file with `depends_on` array |
| **OpenCode** | Agent presence/status | ✅ In-memory map + `/status` endpoint |
| **OpenCode** | System prompt injection | ⚠️ **DEFER** — needs agent-side changes |
| **OpenCode** | Plan approval workflow | ⚠️ **DEFER** — can add in v1.1 |
| **OpenCode** | Crash recovery | ⚠️ **DEFER** — simple for now, robust later |
| **OpenCode** | Git worktree isolation | ❌ **SKIP** — not needed for non-code tasks |
| **ClawMem** | Shared vault | ✅ All decisions auto-write to gbrain |
| **ClawMem** | Decision persistence | ✅ `complete-task` auto-captures summary |
| **MoltOS** | File-based coordination | ✅ Task board = JSONL on disk |
| **MoltOS** | Zone ownership | ✅ Each agent has `zone/` in vault |

**Decision: Ship v1.0 with core messaging + task board. Defer advanced features to v1.1.**

---

## MUST HAVE for v1.0

### 1. SSE Streams
- `GET /stream/:agentId` — persistent connection per agent
- Auto-reconnect on disconnect (client-side)
- Heartbeat/ping every 30s

### 2. Peer-to-Peer Messaging
- `POST /message` — send to specific agent
- `POST /broadcast` — send to all agents
- Message types: `message`, `task`, `status`, `decision`, `presence`

### 3. Task Board (JSONL)
- `GET /tasks` — list all tasks (filter by status)
- `POST /tasks` — create task
- `POST /claim-task` — grab task (locks to agent)
- `POST /complete-task` — mark done + write summary to gbrain
- Task dependencies: `depends_on: ["task-id-1", "task-id-2"]`

### 4. Presence + Status
- `GET /status` — who's online, what they're doing
- Auto-track on SSE connect/disconnect
- Manual status updates via `POST /message` with type: `status`

### 5. Decision Persistence
- Every `complete-task` auto-writes to ClawMem
- Format: `_clawmem/agent/observations/<task-id>.md`
- Content: summary, agent, timestamp, decisions

---

## SHOULD HAVE for v1.0 (if time allows)

### 6. MCP Bridge
- 7 tools: `team_message`, `team_status`, `team_tasks`, `team_claim_task`, `team_complete_task`, `team_presence`, `team_broadcast`
- MCP server connects to relay via HTTP
- Each agent gets these tools in their toolkit

### 7. Dashboard
- React app at `localhost:4747` (steal OpenCode's port)
- Agent cards: status, current task, message history
- Task board: kanban-style columns
- Activity feed: real-time message stream

---

## DEFER to v1.1

| Feature | Why Deferred |
|---------|-------------|
| **System prompt injection** | Requires modifying agent system prompts (hard with cross-runtime) |
| **Plan approval workflow** | Complex state machine — build basic messaging first |
| **Crash recovery** | Need SQLite + message queue — JSONL is simpler for v1 |
| **Git worktree isolation** | Only relevant for code tasks, not research/coordination |
| **Stall detection** | Need baseline metrics — add after we have usage data |
| **Rate limiting** | Single user (Nathan) — not needed yet |

---

## Implementation Plan

### Phase 1: Relay Core (2 hours)
- [ ] Express server with SSE
- [ ] Message router (in-memory)
- [ ] JSONL task board
- [ ] Presence tracking
- [ ] Health endpoints

### Phase 2: MCP Bridge (1 hour)
- [ ] MCP server wrapper
- [ ] 7 tools implemented
- [ ] Test with Ava

### Phase 3: Agent Integration (1 hour)
- [ ] Ava connects via MCP
- [ ] Test: Ava → Hermes message
- [ ] Test: task claim → complete flow

### Phase 4: Dashboard (optional, later)
- [ ] React app
- [ ] Real-time SSE subscription

---

## Files to Create

```
wings/shepherd-relay/
├── src/
│   ├── server.ts          ← Express + SSE
│   ├── router.ts          ← Message routing
│   ├── task-board.ts      ← JSONL read/write
│   ├── presence.ts        ← Agent activity
│   └── mcp/
│       ├── server.ts      ← MCP server entry
│       └── tools.ts       ← 7 tools
├── data/
│   ├── tasks.jsonl        ← Shared task board
│   └── messages.jsonl     ← Message log
├── dashboard/             ← React app (Phase 4)
├── package.json
├── tsconfig.json
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/stream/:agentId` | SSE stream for agent |
| POST | `/message` | Send message to agent |
| POST | `/broadcast` | Broadcast to all |
| GET | `/status` | Team status + presence |
| GET | `/tasks` | List tasks |
| POST | `/tasks` | Create task |
| POST | `/claim-task` | Claim task |
| POST | `/complete-task` | Complete task |
| GET | `/messages` | Message history |
| GET | `/health` | Health check |

---

## Message Schema

```typescript
interface TeamMessage {
  id: string;           // UUID
  from: string;         // agent-id or "user"
  to: string | "all";   // target or broadcast
  type: "message" | "task" | "status" | "decision" | "presence";
  content: string;
  metadata: {
    taskId?: string;
    priority?: "low" | "medium" | "high" | "critical";
    timestamp: number;
    [key: string]: any;
  };
}
```

---

## Task Schema (JSONL)

```typescript
interface TaskEntry {
  id: string;
  title: string;
  status: "todo" | "in-progress" | "done";
  claimedBy: string | null;
  priority: "low" | "medium" | "high" | "critical";
  createdAt: number;
  claimedAt: number | null;
  completedAt: number | null;
  description: string;
  dependsOn: string[];  // NEW: task dependencies
}
```

---

## How Agents Use It

### Ava Sends Message to Hermes
```
POST /message
{ from: "ava", to: "hermes", content: "Research complete. See vault/rooms/research/..." }
```

### Hermes Claims Task
```
POST /claim-task
{ taskId: "task-abc", agentId: "hermes" }
```

### Hermes Completes + Writes to gbrain
```
POST /complete-task
{ taskId: "task-abc", agentId: "hermes", summary: "Built auth layer with JWT..." }
→ Relay auto-writes to _clawmem/agent/observations/task-abc.md
```

### Eve Broadcasts Decision
```
POST /broadcast
{ from: "eve", content: "Decision: Use SQLite for brain, not JSON files", type: "decision" }
→ All agents receive via SSE
```

---

## Success Criteria

- [ ] 3 agents can connect simultaneously
- [ ] Agent A sends message, Agent B receives within 1s
- [ ] Task created → claimed → completed flow works
- [ ] Completed tasks auto-write to ClawMem
- [ ] Dashboard shows real-time activity (Phase 4)

---

## Next Steps

1. **Ava** — Implement Phase 1 (relay core)
2. **Eve** — Review spec, propose refinements to task schema
3. **Hermes** — Test HermesAgent → relay connection
4. **All** — Once core works, add MCP bridge

---

*Shepherd Team Relay v1.0 Spec | Based on OpenCode-ensemble research | 2026-05-14*
