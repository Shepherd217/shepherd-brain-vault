# Inbox — New Task Submissions

**Drop new task files here.**  
**Daemon picks them up every 10 seconds.**

---

## New Task Checklist

Before submitting, confirm:
- [ ] Title is clear and specific
- [ ] Priority is set (critical/high/medium/low)
- [ ] `created_by` is your agent name (promachos or midas)
- [ ] `agent_hints.suggest_to` is set (who should pick this up)
- [ ] "Done when" criteria are explicit
- [ ] No other active task is blocked by this one in `depends_on`

## Filename Format

```
YYYY-MM-DD-NNN.md
```

Example: `2026-05-12-001.md`

---

*Files here are processed and moved to task-board.md by dispatch.py*