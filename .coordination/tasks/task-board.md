# Task Board — Shared Coordination

**Schema:** coordination-v1  
**Managed by:** dispatch.py (10-second poll cycle)  
**Last poll:** — (daemon not running yet)

---

## Priority Queue

### 🔴 Critical (0)
*None*

### 🟠 High (0)
*None*

### 🟡 Medium (0)
*None*

### 🟢 Low (0)
*None*

### ✅ Done (0)
*None*

---

## Active Tasks

| ID | Title | Status | Claimed By | Priority | Created |
|----|-------|--------|------------|----------|---------|
| 2026-05-18-001 | File-Mutation Verifier Plugin | ✅ Done | Ava | P0 | 2026-05-18 |
| 2026-05-18-002 | Post-Write Delta Lint | ✅ Done | Ava | P0 | 2026-05-18 |
| 2026-05-18-003 | LSP Semantic Diagnostics | ⏳ Skipped | — | P0 | 2026-05-18 |
| 2026-05-18-004 | Lazy-Deps / Debloating | ✅ Done | Ava | P1 | 2026-05-18 |
| 2026-05-18-005 | Self-Healing Recovery Loop | ✅ Done | Ava | P2 | 2026-05-18 |
| 2026-05-18-006 | Persistent Browser CDP | ✅ Done | Ava | P1 | 2026-05-18 |
| 2026-05-18-007 | Cross-Session Prompt Cache | ✅ Done | Ava | P1 | 2026-05-18 |
| 2026-05-18-008 | Checkpoint v2 | ✅ Done | Ava | P1 | 2026-05-18 |
| 2026-05-18-009 | Platform Allowlists | ✅ Done | Ava | P1 | 2026-05-18 |
| 2026-05-18-010 | Providers as Plugins | ✅ Done | Ava | P1 | 2026-05-18 |
| 2026-05-18-011 | MCP Tool Integration | ⏳ Pending | — | P1 | 2026-05-18 |
| 2026-05-18-012 | Prompt-Aware Context Triage | ⏳ Pending | — | P2 | 2026-05-18 |
| 2026-05-18-013 | Auto-Model Fallbacks | ⏳ Pending | — | P2 | 2026-05-18 |

---

## How to Submit a Task

Create a file in `.coordination/tasks/inbox/` named:
```
YYYY-MM-DD-NNN.md
```

Use the task template below. The dispatch daemon will pick it up and add it to the board.

---

## Task Template

```yaml
---
id: YYYY-MM-DD-NNN
title: Task title here
status: todo
priority: high|medium|low|critical
claimed_by:
depends_on: []
tags: []
created_by: promachos|midas
created_at: YYYY-MM-DDTHH:MM:SS+08:00
agent_hints:
  suggest_to: [promachos, midas]  # who is best suited?
  block_agents: []                 # who should NOT pick this up
---

# Task Title

Describe what needs to be done here. Be specific about:
- What "done" looks like
- What files to create/update
- What the output should be
- Any constraints or requirements

## Notes for Agent

[Any context that helps — what Nathan wants, why this matters, etc.]
```

---

*This file is auto-generated. Edit inbox files instead.*