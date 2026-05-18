# Emmaus Task Dependencies

**Board:** emmaus  
**Updated:** 2026-05-18T13:38:00Z

---

## Dependency Graph

```
[001] Theological Review ──┐
                            ├──→ [004] Synthesize Reviews ──→ [005] Apply Improvements ──→ [006] Build Web Interface
[002] Business Review ─────┤                            │
                            │                            └──→ [007] Beta Tester Outreach (parallel)
[003] Writer Review ───────┘
```

## Rules

1. **Task 004** CANNOT start until 001, 002, and 003 are ALL `done`
2. **Task 005** CANNOT start until 004 is `done`
3. **Task 006** CAN start when 005 is `done` (or in parallel if API contract is stable)
4. **Task 007** (Beta Outreach) can start in parallel with 005/006

## Manual Promotion

When all parents of a task are `done`, change child status from `todo` → `ready`.

When a task is `ready` and assigned agent is available, change status to `running` and dispatch.

## Blocked Tasks

| Task | Blocked By | Unblock Condition |
|------|-----------|-------------------|
| 004 | 001, 002, 003 | All 3 reviews `done` |
| 005 | 004 | Synthesis `done` |
| 006 | 005 (soft) | Improvements applied OR API contract stable |

---

## Status Key

- `triage` — Needs clarification before assignment
- `todo` — Defined, waiting for dependencies or assignment
- `ready` — Dependencies met, ready to dispatch
- `running` — Agent actively working
- `blocked` — Stuck, needs intervention
- `done` — Complete, output verified
- `archived` — Done and no longer relevant

---

*Auto-dispatch: Not yet implemented (manual for now)*
