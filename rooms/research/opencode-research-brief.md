---
id: opencode-research-brief
title: OpenCode Parallel Agent Architecture — Research Brief
author: Ava
status: complete
date: 2026-05-14
---

# What We Steal From OpenCode

## Core Architecture

OpenCode is built on **3 pillars** for parallel agents:

### 1. Multi-Session Parallelism
- Multiple agents run in **parallel** on the same project
- Each gets its own **context window** + **session**
- Lead agent spawns teammates, coordinates via message passing

### 2. Event-Driven Coordination (NOT Polling)
- **SSE streams** — one per agent, persistent connection
- **promptAsync** — injects message + starts prompt loop in ONE call
- Agents message each other directly (peer-to-peer)
- Lead doesn't poll — waits for messages

### 3. Git Worktree Isolation
- Each teammate gets **own worktree/branch** by default
- No merge conflicts between parallel agents
- `worktree: false` for read-only agents (explore, review)
- Auto-merge on cleanup: squash-merged as unstaged changes

---

## The OpenCode-ensemble Plugin (Our Blueprint)

### How It Works

```
You: "Fix checkout idempotency + tests + review"

Lead agent:
1. team_create(name: "checkout-idempotency")
2. team_tasks_add([
     { content: "Map checkout flow", priority: "high" },
     { content: "Implement guard", priority: "high", depends_on: ["task_abc"] },
     { content: "Add tests", priority: "high", depends_on: ["task_def"] },
     { content: "Review diff", priority: "medium", depends_on: ["task_def", "task_ghi"] }
   ])
3. team_spawn(name: "scout", agent: "explore", worktree: false, claim_task: "task_abc")
4. team_spawn(name: "api-dev", agent: "build", model: "claude", plan_approval: true, claim_task: "task_def")
5. team_spawn(name: "qa", agent: "build", claim_task: "task_ghi")
6. team_spawn(name: "reviewer", agent: "explore", worktree: false, claim_task: "task_jkl")

Teammates coordinate:
  scout → lead: "Found 3 files, risks in src/webhooks/stripe.ts"
  api-dev → lead: "Plan ready: unique event_id + transaction"
  lead → api-dev: approves plan
  qa → api-dev: "What should tests assert?"
  api-dev → qa: "Assert event_id conflict returns success"

Done:
  team_results(from: "api-dev")
  team_shutdown(member: "api-dev")
  team_merge(member: "api-dev")
```

### Key Features

| Feature | What It Does |
|---------|-------------|
| **Task Dependencies** | `depends_on` array — tasks wait for prerequisites |
| **Plan Approval** | `plan_approval: true` — leader reviews before any edits |
| **Role System** | `explore` (read-only) vs `build` (can edit) |
| **Peer Messaging** | Teammates message each other, not just leader |
| **Crash Recovery** | Stale members marked errored, messages redelivered |
| **Spawn Rollback** | If initial prompt fails, member/session/worktree cleaned up |
| **Timeout Watchdog** | Stuck members auto-timed out and aborted |
| **Stall Detection** | Detects no-progress agents, escalates to lead |
| **Overlap Detection** | `team_merge` blocks if local changes conflict |
| **Rate Limiting** | Token bucket (default 10/sec) |
| **Compaction Safety** | Team context preserved when sessions get long |

### Database Schema (SQLite)

- `teams` — team config
- `members` — agent roster + status
- `tasks` — task board with status + claims
- `messages` — peer messages + system events

### Dashboard

- Real-time at `localhost:4747`
- Agent cards: status, task, activity sparklines
- Task board: progress bars, dependency arrows, collapsible groups
- Activity feed: chat-style bubbles
- Timeline: spawn → message → complete → shutdown events

---

## What Makes OpenCode Different From Claude Code

| Feature | OpenCode | Claude Code |
|---------|----------|-------------|
| **Architecture** | Event-driven (SSE) | Polling |
| **Model Mixing** | Mix providers per teammate | Single provider |
| **Worktrees** | Git isolation by default | Shared workspace |
| **Prompt Injection** | System prompt updated with team state | Not team-aware |
| **Approval Flow** | Plan approval before edits | Not built-in |
| **Crash Recovery** | Auto-recovery + redelivery | Manual |
| **Dashboard** | Built-in real-time dashboard | None |

---

## What We Rip for Shepherd Relay

### MUST HAVE
1. **Event-driven SSE** — No polling. Push-based messages.
2. **Peer-to-peer messaging** — All agents talk to all agents.
3. **Task board with dependencies** — `depends_on` chains.
4. **Agent presence + status** — Who's active, what they're doing.
5. **Append-only JSONL logs** — Never overwrite, always append.
6. **System prompt injection** — Team state in every agent's context.

### SHOULD HAVE
7. **Plan approval workflow** — Review before execution (for risky tasks).
8. **Crash recovery** — Stale agents auto-marked, messages redelivered.
9. **Graceful shutdown** — Agents finish current work before stopping.
10. **Git worktree isolation** — Each agent's own branch (for code tasks).

### NICE TO HAVE
11. **Real-time dashboard** — React app showing all agents.
12. **Rate limiting** — Token bucket per agent.
13. **Stall detection** — Auto-escalate stuck agents.

---

## Our Twist: Cross-Runtime

OpenCode's ensemble is **one runtime** (OpenCode spawns subagents within itself).

Shepherd Relay is **cross-runtime**:
- Ava runs on OpenClaw (Kimi 2.6)
- Hermes runs on HermesAgent (MiniMax 2.7) ← DIFFERENT PLATFORM
- Eve runs on OpenClaw (Nemotron)

**The relay is the bridge.** SSE streams connect regardless of backend.

---

## Key Files to Study

- `opencode-ensemble` repo: GitHub.com/hueyexe/opencode-ensemble
- Core architecture: GitHub.com/opencode-ai/opencode
- Dashboard: `ensemble/dashboard/` in plugin repo
- Task board: `ensemble/lib/tasks.ts`
- Message router: `ensemble/lib/messages.ts`

---

*Research complete. Ready for spec drafting.*

**Next: Use this research to draft `relay-architecture-v1.md` with SPECIFIC decisions on what we implement vs defer.**
