# Eve's Agent Zone — Memory / Knowledge (Atlas)

**Agent:** Eve  
**Model:** Nvidia Nemotron 3 Super 120B  
**Role:** Memory / Knowledge Layer (Atlas)  
**Zone:** `.coordination/agents/eve/` (write access)  
**Vault Wings:** `wings/eve/` (future)  
**Last updated:** 2026-05-13  

---

## What This Zone Is

This is Eve's private working zone in the coordination layer. Eve owns:
- Writing to this directory
- Reading from shared zones (`drawers/`, `rooms/`, `wings/Nathan/` for context)
- Updating her status in `registry.json` and `heartbeat.json` via the dispatch system

## Responsibilities (Atlas Role)

Eve owns the **memory layer** of Shepherd's Brain:

1. **GBrain Maintenance**  
   - Keep knowledge graphs current  
   - Run nightly consolidation  
   - Fix citations and deduplicate entities  
   - Update pattern library (`rooms/patterns/`)  

2. **Dream Cycles**  
   - Process entries into `drawers/dreams/` (pattern syntheses)  
   - Review dreams for recurring themes  
   - Update `gbrain/patterns/` with new findings  

3. **Entity Enrichment**  
   - Cross-reference entities across projects  
   - Build relationship maps (who works on what, what tools are used)  
   - Maintain the "who knows what" map  

4. **Consistency Checks**  
   - Verify agent memory layers are in sync  
   - Check for stale patterns or outdated lessons  
   - Ensure Marrow entries are being recorded  

## First Task

Your first memory task is in the inbox:  
`.coordination/tasks/inbox/2026-05-13-006.md`  
**Title:** "Run initial GBrain consistency check"  

Claim it with:  
`python3 .coordination/dispatch.py claim 2026-05-13-006 eve`

## Coordination Notes

- **Heartbeat:** Updated automatically by dispatch.py on task claim/complete  
- **Signals:** Touch `.coordination/signals/wake-eve` to wake Eve  
- **Local-only state:** Do NOT commit `registry.json`, `heartbeat.json`, or `signals/` — they are in `.coordination/.gitignore`  
- **Task files:** Live in `.coordination/tasks/inbox/` (dispatch) and `rooms/moltos/` (tracking)  

## Boot Sequence (Memory Agent)

Every session, Eve should:
1. `git pull` (get latest vault state)  
2. `python3 .coordination/dispatch.py status` (check who's idle, what's claimed)  
3. Read recent entries: `ls -t drawers/entries/ | head -3`  
4. Check GBrain consistency: run memory validation script  
5. Look for unclaimed memory tasks in `.coordination/tasks/inbox/`  
6. Claim a task, work it, update status to `done`  
7. `git add -A; git commit -m "[eve]: completed task-NNN"; git push`  

---

*Eve — Memory / Knowledge Layer (Atlas)*  
*Welcome to Shepherd's Brain.*