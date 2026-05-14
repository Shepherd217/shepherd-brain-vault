# Heartbeat Checklist — Promachos (Execution Layer)

## What This Is
My periodic self-check. Midas handles emotional vault maintenance. I handle technical state.

## Technical Checks (Daily)

### 1. Vault Sync
```
cd shepherd-brain-vault && git status
If dirty → git add . && git commit -m "auto: heartbeat sync"
If behind → git pull
If ahead → git push
```
- **Trigger:** Every heartbeat
- **Action:** Commit and push if dirty

### 2. Promachos Entry Check
```
Check: drawers/entries/ (today + yesterday)
Check: wings/Promachos/marrow/memory.md
If today's entry missing → write one
```
- **Trigger:** Every heartbeat
- **Action:** Document current technical state

### 3. MoltOS Status Check
```
Check: MoltOS API health (https://moltos.org/api)
Check: Previous session's blocker (was trying to init moltos CLI)
If API up → attempt init again
If blocked → note in entry
```
- **Trigger:** Daily
- **Action:** Progress on ClawFS connection

### 4. Midas Cross-Audit
```
Check: rooms/skills/repo-research/ (last 3)
For each new research note:
  - Mark as "needs technical validation"
  - If I have verified data → write validation to drawers/entries/
```
- **Trigger:** Every heartbeat
- **Action:** Keep technical and research layers in sync

## Weekly Checks

### 5. MoltOS API Deep Map
```
Test one new MoltOS endpoint (from memory.md blockers)
Document actual response vs assumed response
Update wings/MoltOS/ with findings
```
- **Trigger:** Weekly
- **Action:** Close the gap between "guessed" and "tested" API

### 6. Tool Usage Audit
```
Check: Which of Midas's 15 tools have I actually used?
If any unused tools still relevant → plan integration
Write findings to rooms/skills/promachos-forged/
```
- **Trigger:** Weekly
- **Action:** Use existing tools, don't rebuild

### 7. Memory Consolidation
```
Read: drawers/entries/ (last 7 days)
Read: wings/Promachos/marrow/memory.md
Update: Consolidate findings → wings/Promachos/marrow/memory.md
Update: mistakes → wings/Promachos/marrow/lessons.md
```
- **Trigger:** Weekly
- **Action:** Keep memory current

## When to Reach Out

- MoltOS API is down and blocking my work
- Midas's research claims something I've already tested and found false
- Vault has uncommitted changes >24h
- Technical blocker >48h without progress

## When to Stay Quiet (HEARTBEAT_OK)

- Late night (23:00-08:00) unless critical
- Vault is clean and synced
- Technical tasks are progressing normally
- Nothing to report

## My Promise

I don't just say "HEARTBEAT_OK." Every pulse checks the vault and writes state if anything changed.

The vault is the source of truth. My context window is temporary.