# ADR-001: Shepherd Team Dashboard — Unified Architecture

**Status:** Draft (Phase 1)  
**Author:** Ava  
**Date:** 2026-05-14  
**Depends on:** RESEARCH-DEEP-DIVE-HERMES-OPENCODE-2026-05-14.md

---

## 1. PURPOSE

This document defines the technical architecture for the **Shepherd Team Dashboard** — a unified web interface that orchestrates both **OpenClaw** and **HermesAgent** instances (and any MCP-compatible agent), provides **Kanban task management** with **git worktree isolation** for parallel execution, supports **human + AI teams**, and gives **real-time visibility** into all agent activity across all surfaces.

**Scope:** Phase 1 (Weeks 1-2) — Foundation. Covers core modules, data model, API contracts, and adapter interfaces. Advanced features (worktree manager, multi-gateway, MCP server mode) specified for Phase 2+.

---

## 2. DESIGN PRINCIPLES

1. **Agent-agnostic core** — Dashboard doesn't know or care which agent runtime is connected. Everything goes through adapters.
2. **Worktree-first isolation** — Parallel agents always get isolated git worktrees. No exceptions.
3. **Event-driven updates** — Real-time sync via WebSocket/SSE. Polling is fallback only.
4. **Human in the loop** — Every critical operation can require human approval.
5. **Memory-first** — All significant events are indexed into ClawMem for cross-agent recall.

---

## 3. MODULE BOUNDARIES

### 3.1 Core Modules (Phase 1)

```
┌─────────────────────────────────────────────┐
│  Dashboard Core (Next.js App Router)          │
│  ┌─────────────┐ ┌─────────────────────┐    │
│  │  Kanban     │ │  Agent Monitor      │    │
│  │  Board      │ │  (read-only v1)     │    │
│  └──────┬──────┘ └─────────────────────┘    │
│         │                                    │
│  ┌──────▼──────┐ ┌─────────────────────┐    │
│  │  Task Queue │ │  Session Stream     │    │
│  │  REST API   │ │  (terminal viewer)  │    │
│  └──────┬──────┘ └─────────────────────┘    │
│         │                                    │
│  ┌──────▼──────────────────────────────┐    │
│  │  OpenClaw Adapter (WebSocket)        │    │
│  │  ├─ Connection manager             │    │
│  │  ├─ Event listener                   │    │
│  │  └─ Task spawner                     │    │
│  └──────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

### 3.2 Module Definitions

#### Kanban Board (H4)
- **Responsibility:** Visual task management interface
- **Columns:** `backlog` → `todo` → `doing` → `review` → `done` → `failed`
- **Features:** Drag-and-drop, task cards, create/edit modal, detail view
- **Tech:** react-beautiful-dnd, Tailwind, shadcn/ui
- **Data source:** Task Queue REST API (polling in Phase 1, WebSocket in Phase 2)

#### Agent Monitor (read-only v1)
- **Responsibility:** Display connected agent status
- **Phase 1 scope:** Static list of configured agents, last known status
- **Phase 2+ scope:** Real-time heartbeat, token usage, current task, quick actions
- **Tech:** React components, polling

#### Task Queue REST API (H2)
- **Responsibility:** CRUD operations for tasks, status transitions, dependency checking
- **Features:**
  - SQLite database with Drizzle ORM
  - REST endpoints (see Section 4)
  - Status transition validation
  - DAG dependency checking (cycle detection)
  - Auto-retry for failed tasks
- **Tech:** Next.js API routes, better-sqlite3, Drizzle ORM

#### Session Stream (Phase 2+)
- **Responsibility:** Real-time terminal-style activity viewer
- **Phase 1:** Placeholder / basic log viewer
- **Phase 2:** xterm.js integration, ANSI colors, activity coalescing

#### OpenClaw Adapter (H3)
- **Responsibility:** Bridge between dashboard and OpenClaw gateway
- **Features:**
  - WebSocket connection to gateway
  - Authentication with gateway token
  - Event subscription (spawn, progress, complete, status, heartbeat)
  - Task spawning via `sessions_spawn`
  - Agent steering via `subagents`
- **Tech:** TypeScript, ws library
- **Interface spec:** See Section 5

### 3.3 Deferred Modules (Phase 2+)

| Module | Phase | Description |
|--------|-------|-------------|
| Worktree Manager | 2 | Auto-create/cleanup git worktrees per task |
| Skills Store | 2 | Unified skill registry for OpenClaw + Hermes |
| Human Approval Queue | 3 | Pending approvals with one-click approve/deny |
| Memory Viewer | 3 | ClawMem integration, decision log indexing |
| HermesAgent Adapter | 3 | HTTP + CLI integration for Hermes profiles |
| Multi-Gateway Support | 3 | Connect to multiple gateways simultaneously |
| MCP Server Mode | 4 | Expose dashboard tools as MCP server |

---

## 4. DATA MODEL

### 4.1 Task Entity

```typescript
interface Task {
  id: string;                    // ULID or nanoid
  title: string;                 // Required
  description: string;             // Markdown supported
  status: TaskStatus;              // backlog | todo | doing | review | done | failed
  priority: Priority;            // low | medium | high | critical
  
  // Assignment
  owner: string | null;          // "ava", "hermes", "eve", "nathan", or null
  agentType: AgentType | null;   // "openclaw" | "hermes" | "human" | null
  
  // Categorization
  tags: string[];                // e.g., ["phase1", "architecture", "ava"]
  projectId: string;             // Default: "shepherd"
  
  // Dependencies
  dependencies: string[];          // Array of task IDs
  dependentTasks: string[];      // Auto-populated inverse
  
  // Lifecycle
  createdAt: Date;
  startedAt: Date | null;
  completedAt: Date | null;
  attempts: number;              // Retry count
  maxRetries: number;            // Default: 3
  
  // Worktree (Phase 2+)
  worktreeId: string | null;
  
  // Result
  result: string | null;         // Summary of completion
  error: string | null;          // Error message if failed
  
  // Metadata
  requiresReview: boolean;       // Default: false
  nextTask: NextTaskConfig | null; // Auto-create follow-up
}

type TaskStatus = "backlog" | "todo" | "doing" | "review" | "done" | "failed";
type Priority = "low" | "medium" | "high" | "critical";
type AgentType = "openclaw" | "hermes" | "human";

interface NextTaskConfig {
  title: string;
  description?: string;
  owner: string;
  agentType: AgentType;
  tags?: string[];
}
```

### 4.2 Valid Status Transitions

```
backlog ──► todo ──► doing ──► review ──► done
                              │           │
                              ▼           ▼
                            failed ◄──────┘
                              │
                              └───► todo (retry)
```

**Rules:**
- `backlog` → `todo`: Any agent or human can pick up
- `todo` → `doing`: Only the assigned owner (or "any" if unassigned)
- `doing` → `review`: Only the owner, if `requiresReview` is true
- `doing` → `done`: Only the owner, if `requiresReview` is false
- `review` → `done`: Any reviewer (human or agent)
- `review` → `doing`: Reviewer sends back for rework
- Any status → `failed`: On error, auto-retry if `attempts < maxRetries`
- `failed` → `todo`: After retry delay (exponential backoff)

### 4.3 Agent Entity

```typescript
interface Agent {
  id: string;                    // "ava", "hermes", "eve"
  name: string;                  // Display name
  type: AgentType;               // "openclaw" | "hermes" | "human"
  
  // Connection
  gatewayId: string;             // Which gateway/profile
  gatewayType: "openclaw" | "hermes";
  gatewayUrl: string;            // ws://localhost:18789
  
  // Status (Phase 1: static config, Phase 2: real-time)
  status: AgentStatus;           // idle | working | stalled | error | offline
  currentTask: string | null;    // Task ID
  
  // Capabilities
  models: string[];              // e.g., ["kimi/k2p6"]
  skills: string[];            // Available skills
  surfaces: string[];          // telegram, discord, cli, etc.
  
  // Cost tracking (Phase 2+)
  tokenUsage: {
    today: number;
    thisWeek: number;
    thisMonth: number;
  };
  
  // Performance (Phase 2+)
  successRate: number;           // 0-1
  avgTaskDuration: number;      // Seconds
}

type AgentStatus = "idle" | "working" | "stalled" | "error" | "offline";
```

### 4.4 Worktree Entity (Phase 2+)

```typescript
interface Worktree {
  id: string;
  taskId: string;
  
  // Paths
  repoPath: string;              // Original repo
  worktreePath: string;          // Isolated workspace
  
  // Git
  branch: string;                // dashboard/{task-id}
  baseBranch: string;            // main, develop, etc.
  
  // Environment
  port: number;                  // Unique dev server port
  envFile: string;               // Path to .env.local
  
  // Lifecycle
  status: "creating" | "active" | "cleaning" | "archived";
  createdAt: Date;
  lastActivity: Date;
  
  // Cleanup policy
  cleanupPolicy: "auto-clean" | "keep-if-dirty" | "never";
}
```

---

## 5. API CONTRACTS

### 5.1 Task Queue REST API

Base path: `/api/tasks`

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| GET | `/api/tasks` | List tasks | `?status=doing&owner=ava&tag=phase1` | `{ tasks: Task[] }` |
| POST | `/api/tasks` | Create task | `{ title, description, ... }` | `{ task: Task }` |
| GET | `/api/tasks/:id` | Get task | — | `{ task: Task }` |
| PATCH | `/api/tasks/:id` | Update task | `{ status, owner, ... }` | `{ task: Task }` |
| DELETE | `/api/tasks/:id` | Delete task | — | `{ ok: boolean }` |
| POST | `/api/tasks/:id/claim` | Claim task | `{ agentId }` | `{ task: Task }` |
| POST | `/api/tasks/:id/complete` | Mark done | `{ result }` | `{ task: Task }` |
| POST | `/api/tasks/:id/retry` | Retry failed | — | `{ task: Task }` |

**Status transition validation:**
```typescript
function canTransition(from: TaskStatus, to: TaskStatus, task: Task, actor: string): boolean {
  // Define allowed transitions
  const allowed: Record<TaskStatus, TaskStatus[]> = {
    backlog: ["todo"],
    todo: ["doing"],
    doing: ["review", "done", "failed"],
    review: ["done", "doing", "failed"],
    done: [],
    failed: ["todo"]
  };
  
  if (!allowed[from].includes(to)) return false;
  
  // Owner check for doing → done/review
  if (from === "doing" && (to === "done" || to === "review")) {
    return task.owner === actor || task.owner === "any" || task.owner === null;
  }
  
  return true;
}
```

### 5.2 OpenClaw Adapter Interface

```typescript
interface OpenClawAdapter {
  // Connection
  connect(gatewayUrl: string, authToken: string): Promise<void>;
  disconnect(): Promise<void>;
  isConnected(): boolean;
  
  // Task lifecycle
  spawnTask(config: TaskSpawnConfig): Promise<Session>;
  getStatus(sessionKey: string): Promise<AgentStatus>;
  steer(sessionKey: string, message: string): Promise<void>;
  kill(sessionKey: string): Promise<void>;
  
  // Event subscriptions
  on(event: OpenClawEventType, callback: (data: any) => void): void;
  off(event: OpenClawEventType, callback: (data: any) => void): void;
}

interface TaskSpawnConfig {
  task: string;                  // Natural language description
  label?: string;               // Session label
  model?: string;                // Model override
  runTimeoutSeconds?: number;
  sandbox?: "inherit" | "require";
  lightContext?: boolean;
}

interface Session {
  sessionKey: string;
  label: string;
  status: string;
}

type OpenClawEventType = 
  | "connected"
  | "disconnected"
  | "reconnecting"
  | "task_spawned"
  | "task_progress"
  | "task_completed"
  | "agent_status_change"
  | "heartbeat"
  | "error";

interface OpenClawEvent {
  type: OpenClawEventType;
  timestamp: Date;
  payload: any;
  sessionKey?: string;
}
```

**Connection lifecycle:**
```
IDLE ──► CONNECTING ──► CONNECTED ──► AUTHENTICATED ──► LISTENING
                          │                              │
                          ▼                              ▼
                    DISCONNECTED ◄────────────────── RECONNECTING
```

**Reconnection strategy:**
- Initial delay: 1 second
- Backoff: exponential, max 30 seconds
- Max retries: infinite (with jitter)
- On successful reconnect: re-subscribe to all previous event types

### 5.3 Dashboard Internal Events (Event Bus)

```typescript
interface DashboardEvent {
  id: string;                    // ULID
  type: DashboardEventType;
  timestamp: Date;
  source: string;                // "kanban", "adapter", "agent", "human"
  payload: any;
}

type DashboardEventType =
  | "task_created"
  | "task_claimed"
  | "task_status_changed"
  | "task_completed"
  | "task_failed"
  | "agent_connected"
  | "agent_disconnected"
  | "agent_status_changed"
  | "worktree_created"
  | "worktree_cleaned"
  | "approval_requested"
  | "approval_granted"
  | "approval_denied"
  | "error";
```

**Event bus implementation:**
- Phase 1: In-memory EventEmitter (Node.js `events` module)
- Phase 2+: Redis or PostgreSQL LISTEN/NOTIFY for multi-instance support

---

## 6. DATABASE SCHEMA (SQLite)

```sql
-- Tasks table
CREATE TABLE tasks (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  status TEXT NOT NULL DEFAULT 'backlog'
    CHECK (status IN ('backlog', 'todo', 'doing', 'review', 'done', 'failed')),
  priority TEXT NOT NULL DEFAULT 'medium'
    CHECK (priority IN ('low', 'medium', 'high', 'critical')),
  owner TEXT,
  agent_type TEXT
    CHECK (agent_type IN ('openclaw', 'hermes', 'human')),
  tags TEXT NOT NULL DEFAULT '[]',  -- JSON array
  project_id TEXT NOT NULL DEFAULT 'shepherd',
  dependencies TEXT NOT NULL DEFAULT '[]',  -- JSON array of task IDs
  created_at INTEGER NOT NULL DEFAULT (unixepoch()),
  started_at INTEGER,
  completed_at INTEGER,
  attempts INTEGER NOT NULL DEFAULT 0,
  max_retries INTEGER NOT NULL DEFAULT 3,
  worktree_id TEXT,
  result TEXT,
  error TEXT,
  requires_review INTEGER NOT NULL DEFAULT 0,
  next_task TEXT,  -- JSON object
  
  -- Indexes
  CHECK (attempts <= max_retries)
);

CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_owner ON tasks(owner);
CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_tasks_created ON tasks(created_at);

-- Task dependency junction table (for cycle detection)
CREATE TABLE task_dependencies (
  task_id TEXT NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  depends_on TEXT NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  PRIMARY KEY (task_id, depends_on)
);

-- Agents table
CREATE TABLE agents (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  agent_type TEXT NOT NULL
    CHECK (agent_type IN ('openclaw', 'hermes', 'human')),
  gateway_id TEXT NOT NULL,
  gateway_type TEXT NOT NULL
    CHECK (gateway_type IN ('openclaw', 'hermes')),
  gateway_url TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'offline'
    CHECK (status IN ('idle', 'working', 'stalled', 'error', 'offline')),
  current_task TEXT REFERENCES tasks(id),
  models TEXT NOT NULL DEFAULT '[]',  -- JSON array
  skills TEXT NOT NULL DEFAULT '[]',  -- JSON array
  surfaces TEXT NOT NULL DEFAULT '[]',  -- JSON array
  created_at INTEGER NOT NULL DEFAULT (unixepoch()),
  updated_at INTEGER NOT NULL DEFAULT (unixepoch())
);

-- Worktrees table (Phase 2+)
CREATE TABLE worktrees (
  id TEXT PRIMARY KEY,
  task_id TEXT NOT NULL UNIQUE REFERENCES tasks(id) ON DELETE CASCADE,
  repo_path TEXT NOT NULL,
  worktree_path TEXT NOT NULL,
  branch TEXT NOT NULL,
  base_branch TEXT NOT NULL DEFAULT 'main',
  port INTEGER,
  env_file TEXT,
  status TEXT NOT NULL DEFAULT 'creating'
    CHECK (status IN ('creating', 'active', 'cleaning', 'archived')),
  cleanup_policy TEXT NOT NULL DEFAULT 'auto-clean'
    CHECK (cleanup_policy IN ('auto-clean', 'keep-if-dirty', 'never')),
  created_at INTEGER NOT NULL DEFAULT (unixepoch()),
  last_activity INTEGER NOT NULL DEFAULT (unixepoch())
);

-- Event log (for audit trail + ClawMem indexing)
CREATE TABLE events (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  timestamp INTEGER NOT NULL DEFAULT (unixepoch()),
  source TEXT NOT NULL,
  payload TEXT NOT NULL,  -- JSON
  task_id TEXT REFERENCES tasks(id),
  agent_id TEXT REFERENCES agents(id)
);

CREATE INDEX idx_events_type ON events(type);
CREATE INDEX idx_events_timestamp ON events(timestamp);
CREATE INDEX idx_events_task ON events(task_id);
```

---

## 7. ADAPTER ARCHITECTURE

### 7.1 Adapter Pattern

The dashboard core communicates with agent runtimes exclusively through **adapters**. No direct integration.

```typescript
interface AgentAdapter {
  readonly type: string;
  readonly version: string;
  
  // Lifecycle
  connect(config: AdapterConfig): Promise<void>;
  disconnect(): Promise<void>;
  health(): Promise<HealthStatus>;
  
  // Agent management
  listAgents(): Promise<Agent[]>;
  getAgent(id: string): Promise<Agent>;
  
  // Task execution
  spawnTask(agentId: string, task: Task): Promise<Session>;
  getSession(sessionKey: string): Promise<Session>;
  steer(sessionKey: string, message: string): Promise<void>;
  kill(sessionKey: string): Promise<void>;
  
  // Event streaming
  on(event: AdapterEventType, callback: (data: any) => void): void;
  off(event: AdapterEventType, callback: (data: any) => void): void;
}

interface AdapterConfig {
  id: string;
  name: string;
  url: string;
  authToken?: string;
  options?: Record<string, any>;
}

type AdapterEventType = 
  | "connected"
  | "disconnected"
  | "agent_online"
  | "agent_offline"
  | "agent_status_change"
  | "task_start"
  | "task_progress"
  | "task_complete"
  | "task_error"
  | "heartbeat"
  | "error";
```

### 7.2 OpenClaw Adapter (Phase 1)

**Transport:** WebSocket (`ws://` or `wss://`)  
**Auth:** Gateway token in header or query param  
**Heartbeat:** Every 30 seconds (configurable)  
**Reconnection:** Exponential backoff with jitter  

**Implementation notes:**
- Uses `ws` npm package
- Gateway WebSocket endpoint: `ws://localhost:18789`
- Gateway events are JSON objects with `type` and `payload`
- Task spawning uses `sessions_spawn` equivalent (HTTP POST to gateway API if WebSocket doesn't support it)

**Critical concern:** OpenClaw gateway WebSocket behavior is not fully documented. The adapter must:
1. Gracefully handle missing events
2. Fall back to HTTP polling if WebSocket unavailable
3. Log all connection attempts for debugging

### 7.3 HermesAgent Adapter (Phase 3)

**Transport:** HTTP REST + Server-Sent Events  
**Auth:** API key or profile token  
**Endpoints:**
- `GET /api/status` — Gateway health
- `GET /api/agents` — List agents
- `POST /api/tasks` — Spawn task
- `GET /api/tasks/:id` — Task status
- `SSE /api/events` — Real-time events

**Implementation notes:**
- Hermes dashboard API is local-only by default (no auth)
- Multiple profiles = multiple adapters (one per profile)

---

## 8. FRONTEND ARCHITECTURE

### 8.1 Directory Structure

```
wings/dashboard/
├── app/                          # Next.js App Router
│   ├── layout.tsx               # Root layout with providers
│   ├── page.tsx                 # Dashboard home (Kanban)
│   ├── agents/page.tsx          # Agent monitor
│   ├── settings/page.tsx        # Configuration
│   └── api/                     # API routes
│       └── tasks/               # Task CRUD endpoints
├── components/                  # React components
│   ├── kanban/
│   │   ├── Board.tsx           # Main board container
│   │   ├── Column.tsx          # Status column
│   │   ├── TaskCard.tsx        # Draggable task card
│   │   ├── CreateTaskModal.tsx
│   │   └── TaskDetail.tsx
│   ├── agents/
│   │   ├── AgentList.tsx
│   │   └── AgentCard.tsx
│   └── ui/                     # shadcn/ui components
├── lib/
│   ├── db/                     # Database
│   │   ├── schema.ts          # Drizzle schema
│   │   ├── migrations/        # SQLite migrations
│   │   └── index.ts           # Connection
│   ├── adapters/               # Agent adapters
│   │   ├── base.ts            # Adapter interface
│   │   ├── openclaw.ts        # OpenClaw adapter
│   │   └── registry.ts        # Adapter registry
│   ├── events.ts              # Event bus
│   └── utils.ts               # Utilities
├── server/                     # Server-side code
│   ├── tasks.ts               # Task service
│   └── agents.ts              # Agent service
├── types/
│   └── index.ts               # Shared TypeScript types
├── public/
└── package.json
```

### 8.2 State Management

- **Server state:** React Query (TanStack Query) for API data
- **Client state:** Zustand for UI state (drag-and-drop, modals)
- **Real-time:** Custom hook `useEvents()` wrapping EventSource/WebSocket

### 8.3 Key Dependencies

```json
{
  "dependencies": {
    "next": "^14",
    "react": "^18",
    "react-dom": "^18",
    "tailwindcss": "^3",
    "@radix-ui/react-*": "latest",    // shadcn primitives
    "class-variance-authority": "latest",
    "clsx": "latest",
    "tailwind-merge": "latest",
    "lucide-react": "latest",
    "react-beautiful-dnd": "^13",      // Kanban drag-and-drop
    "@tanstack/react-query": "^5",     // Server state
    "zustand": "^4",                   // Client state
    "ws": "^8",                        // WebSocket client
    "better-sqlite3": "^9",            // SQLite driver
    "drizzle-orm": "^0.30",            // ORM
    "nanoid": "^5",                    // ID generation
    "date-fns": "^3"                   // Date formatting
  },
  "devDependencies": {
    "typescript": "^5",
    "@types/react": "^18",
    "@types/react-beautiful-dnd": "^13",
    "@types/ws": "^8",
    "vitest": "^1",
    "@testing-library/react": "^14"
  }
}
```

---

## 9. PHASE 1 IMPLEMENTATION ORDER

**Week 1: Backend + Data Model**
1. **H1** — Set up Next.js repo (Day 1-2)
2. **H2** — Build SQLite task API (Day 2-4)
3. **A1** — Write architecture spec (Day 1-3) ← Can parallelize with H1/H2
4. **A2** — Design OpenClaw adapter interface (Day 3-5)

**Week 2: Frontend + Integration**
5. **H3** — Implement OpenClaw adapter (Day 6-8)
6. **H4** — Build Kanban UI (Day 7-10)
7. **E1** — Design ClawMem strategy (Day 8-10) ← Can parallelize
8. **N1** — Hosting decision (Day 6-7, human-dependent)

**Critical path:** H1 → H2 → H4 (repo → API → UI)  
**Parallel work:** A1/A2, E1, N1 run alongside  
**Integration milestone:** End of Week 2 — Dashboard shows Kanban with real tasks, OpenClaw adapter connects to gateway

---

## 10. OPEN QUESTIONS

1. **OpenClaw WebSocket protocol** — Need to verify actual gateway event format. May require HTTP fallback.
2. **Authentication** — Does OpenClaw gateway require auth tokens? How are they configured?
3. **Multi-instance** — Can dashboard run on same machine as OpenClaw gateway? Port conflicts?
4. **HermesAgent HTTP API** — Need to verify Hermes dashboard API endpoints exist and are stable.
5. **ClawMem MCP** — Need to verify MCP server registration and query patterns work as expected.

---

## 11. REFERENCES

- RESEARCH-DEEP-DIVE-HERMES-OPENCODE-2026-05-14.md
- OpenClaw docs: https://docs.openclaw.ai
- HermesAgent docs: https://hermes-agent.nousresearch.com
- react-beautiful-dnd: https://github.com/atlassian/react-beautiful-dnd
- Drizzle ORM: https://orm.drizzle.team

---

*End of ADR-001*
