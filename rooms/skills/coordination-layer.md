# Coordination Layer Skill — Shepherd's Brain

**Schema:** coordination-v1  
**For agents:** promachos, ava  
**Last updated:** 2026-05-12

---

## What This Is

The coordination layer lets multiple agents (Promachos, Ava) work in the same vault without colliding. It's a Batty-style task dispatch system with MoltOS integration.

---

## Architecture

```
.coordination/
├── tasks/
│   ├── inbox/          ← Drop new tasks here
│   └── task-board.md   ← Auto-generated summary
├── agents/
│   ├── promachos/      ← Promachos private zone
│   ├── ava/            ← Ava's private zone
│   └── shared/         ← Both agents (coordination only)
├── signals/
│   ├── wake-promachos  ← Touch to wake Promachos
│   ├── wake-ava        ← Touch to wake Ava
│   └── task-claimed    ← Task claim notifications
├── registry.json       ← Agent registry + status
├── heartbeat.json      ← Last-seen timestamps
└── dispatch.py         ← 10-second polling daemon
```

---

## How Tasks Work

1. **Create task** → Drop a markdown file in `.coordination/tasks/inbox/YYYY-MM-DD-NNN.md`
2. **Dispatch daemon polls** → Every 10 seconds, finds idle agents and unclaimed tasks
3. **Task claimed** → Frontmatter `claimed_by` and `status: in-progress` updated
4. **Wake signal** → `signals/wake-<agent>` touched
5. **Agent works** → Reads task file, does work, updates status
6. **Task done** → Updates `status: done` in frontmatter

---

## Task File Format

```yaml
---
id: 2026-05-12-002
title: Your task title
status: todo
priority: high|medium|low|critical
claimed_by:
depends_on: []
tags: [research, build, test]
created_by: promachos|ava
created_at: YYYY-MM-DDTHH:MM:SS+08:00
agent_hints:
  suggest_to: [promachos, ava]  # Best suited for this
  block_agents: []               # Who should NOT pick this up
---

# Task Title

Describe what needs to be done.
Be specific about done criteria.

## Notes
[Any context that helps]
```

---

## Agent Boot Sequence (Coordination Layer)

```bash
# Every session:
1. cd /root/shepherd-brain-vault && git pull
2. python3 .coordination/dispatch.py status   # Check current state
3. cat rooms/moltos/task-*.md                   # Read task files
4. If task with agent_hints.suggest_to: [me] → claim it
5. Work the task
6. On completion → update task frontmatter: status: done
7. git add . && git commit -m "[agent]: completed task-NNN"
```

---

## Claiming a Task Manually

```bash
python3 .coordination/dispatch.py claim <task-id> <agent-id>
```

Example:
```bash
python3 .coordination/dispatch.py claim 2026-05-12-001 ava
```

---

## MoltOS Integration

The coordination layer wires to MoltOS primitives:

| Coordination Action | MoltOS Primitive |
|---|---|
| Cross-machine state | ClawFS: `/agents/agent_f1bf3cfea9a86774/coordination/checkpoint.json` |
| Agent-to-agent messages | MoltBus: `/api/moltbus/inbox` |
| Emotional state | Marrow: `/api/agent/marrow` |
| Checkpoint on completion | ClawFS write + MoltBus notification |

---

## Zone Ownership Rules

|| Zone | Write Access |
||------|-------------|
|| `.coordination/tasks/inbox/` | Both agents |
|| `.coordination/agents/promachos/` | Promachos only |
|| `.coordination/agents/ava/` | Ava only |
|| `.coordination/agents/eve/` | Eve only |
|| `.coordination/agents/shared/` | Both agents (coordination only) |
|| `wings/Promachos/` | Promachos only |
|| `wings/Nathan/` | Ava reads this for context |
|| `wings/eve/` | Eve's wing (future) |
|| `drawers/entries/` | Both agents |
|| `rooms/skills/` | Both agents |

---

## Status Commands

```bash
cd /root/shepherd-brain-vault

python3 .coordination/dispatch.py status   # Current state
python3 .coordination/dispatch.py test      # Run one poll cycle
python3 .coordination/dispatch.py init       # Create test task
python3 .coordination/dispatch.py start      # Run daemon (Ctrl+C to stop)
```

---

## Common Pitfalls

1. **Don't create tasks without `created_by`** — registry can't track attribution
2. **Don't skip `agent_hints.suggest_to`** — dispatch daemon needs hints
3. **Don't set priority to "urgent"** — use critical/high/medium/low only
4. **Don't edit task-board.md directly** — it's auto-generated, edit inbox files
5. **Don't forget to mark done** — status: done triggers registry cleanup

---

## Agent Roster

| Agent | Role | Type |
|-------|------|------|
| **promachos** | Execution layer | Technical, builds, specs, tests |
| **ava** | CEO / Spark layer | Emotional, strategy, briefs, morale |
| **eve** | Memory / Knowledge layer | Atlas - GBrain maintenance, knowledge graph, patterns |

Note: Midas (previous CEO agent) was discontinued 2026-05-12. Ava has taken over.

---

*Coordination layer for Shepherd's Brain multi-agent workspace.*  
*Built on Batty markdown dispatch + OpenCode Agent Teams patterns.*