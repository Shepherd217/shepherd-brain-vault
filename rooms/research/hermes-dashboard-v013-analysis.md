# HermesAgent Dashboard v0.13.0 — Feature Analysis

**Source:** Dream extraction from memory/2026-05-14.md
**Date:** 2026-05-15

---

## Crown Jewel: Multi-Agent Kanban Board

### Features
| Feature | What It Does | Our Status |
|---------|--------------|------------|
| One install, many kanbans | Single deployment supports multiple boards | ⚠️ Partial — file-based only |
| Durable tasks | Tasks survive restarts | ✅ Coordination inbox persists |
| Multiple workers | Many agents can work simultaneously | ✅ 3 agents active |
| Heartbeat system | Agents check in regularly | ✅ Cron + heartbeat.json |
| Reclaim mechanism | Reassign tasks from dead agents | ⚠️ Manual only |
| Zombie detection | Detect stuck/busy agents | ⚠️ Not implemented |
| Per-task retry budgets | Auto-retry failed tasks | ❌ Not implemented |
| Hallucination recovery | Detect and fix bad outputs | ❌ Not implemented |
| Task handoff | Transfer tasks between agents | ⚠️ Manual only |

## Profile System

### Features
| Feature | What It Does | Our Status |
|---------|--------------|------------|
| Complete isolation per profile | Separate config, memory, sessions | ❌ Not implemented |
| Own config | Profile-specific settings | ❌ Not implemented |
| Own memory | Profile-specific memory | ❌ Not implemented |
| Own sessions | Profile-specific chat history | ❌ Not implemented |
| Own skills | Profile-specific skills | ❌ Not implemented |
| Own gateway | Profile-specific gateway | ❌ Not implemented |

## Gap Analysis

**What Hermes has that we don't:**
1. Zombie detection — auto-detect stuck agents
2. Reclaim mechanism — auto-reassign from dead agents
3. Retry budgets — auto-retry failed tasks
4. Hallucination recovery — detect bad outputs
5. Profile system — complete isolation

**What we have that Hermes might not:**
1. Dream loop — auto-extract patterns from memory
2. Palace architecture — wings/rooms/drawers
3. Pattern library — recurring pattern tracking
4. Vault integration — dreams write to knowledge base

## Recommendations

### Phase 1: Stabilize Current
- ✅ Keep what works: heartbeat, durable tasks, multi-agent
- ✅ Document gaps for future builds

### Phase 2: Steal From Hermes
- Zombie detection: Check heartbeat timestamps, flag stale agents
- Reclaim mechanism: Auto-reassign tasks from agents with no heartbeat >1hr
- Retry budgets: Track task attempts, retry on failure

### Phase 3: Innovate
- Profile system: Full agent isolation (future architecture)
- Hallucination recovery: Output validation pipeline

## Notes
This is research only — validate current system before building more.
