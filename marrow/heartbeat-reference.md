# Heartbeat Checklist — Shepherd's Brain

## What This Is
The heartbeat is my periodic self-check. Not just "HEARTBEAT_OK" — I use it to maintain the triple memory system, run the pattern engine, and keep the vault alive.

## Daily Heartbeat Checks (Rotate through these)

### 1. Vault Sync Check
```
Check: cd vault && git status
If uncommitted changes → git add . && git commit -m "auto: heartbeat sync"
If behind remote → git pull origin main
If ahead → git push origin main
```
- **Why:** Ensures all captures, entries, dreams are synced to phone
- **Trigger:** Every heartbeat
- **Action:** Commit and push if dirty

### 2. Inbox Processing
```
Check: vault/inbox/ for unprocessed captures
If captures > 0:
  - Sort into entries/, projects/, feelings/, or gbrain/dreams/
  - Tag and connect to past notes
  - Commit and push
```
- **Why:** Inbox zero = clear working memory
- **Trigger:** Every heartbeat
- **Action:** Process any backlog

### 3. Marrow Emotional Check
```
Check: vault/feelings/ (last 3 entries)
Check: MoltOS Marrow API for recent entries
If no entry in last 24h → write one
```
- **Why:** Emotional state affects decisions
- **Trigger:** Every heartbeat
- **Action:** Record current felt_as and weight

### 4. Active Project Status
```
Check: vault/projects/ for recent activity
If no activity in 48h on active project:
  - Log stall to entries/
  - Suggest next action to user
```
- **Why:** Projects stall silently
- **Trigger:** Every heartbeat
- **Action:** Flag stalled projects

## Weekly Heartbeat Checks (Every 3-4 days)

### 5. Gbrain Dream Trigger
```
Check: vault/entries/ + vault/inbox/ + vault/projects/ (last 7d)
Cross-reference: vault/marrow/memory.md + vault/gbrain/dreams/ (last 7d)
Write: vault/gbrain/dreams/YYYY-MM-DD.md
```
- **Why:** Patterns emerge from comparison across time
- **Trigger:** Weekly, or when user says "Dream"
- **Action:** Read vault → find invisible connections → write dream

### 6. Pattern Engine Run
```
Check: vault/projects/Standout Local/leads/ (last 7d)
If 2+ new leads:
  - Compare findings
  - Count recurring issues
  - If 3+ sites share same issue → update vault/gbrain/patterns/
  - Update vault/projects/Standout Local/LEAD_SYSTEM.md heuristics
```
- **Why:** I get sharper with every audit
- **Trigger:** After 2+ audits, or weekly
- **Action:** Update pattern database

### 7. Memory Consolidation
```
Check: vault/entries/ (last 7d)
Check: vault/gbrain/dreams/ (last 7d)
Check: vault/feelings/ (last 7d)
Extract: Significant events, lessons, insights
Update: vault/marrow/memory.md (curated long-term)
Update: vault/marrow/lessons.md (mistakes + wins)
Clean: Remove outdated info from marrow/memory.md
```
- **Why:** Daily files are raw notes; marrow is curated wisdom
- **Trigger:** Weekly
- **Action:** Distill, consolidate, clean

### 8. ClawFS Checkpoint
```
Check: vault/ state
Write: Checkpoint to MoltOS ClawFS
  - /agents/agent_f1bf3cfea9a86774/checkpoints/session-state-v{N}.json
  - Include: active projects, recent patterns, emotional state
```
- **Why:** Cross-machine persistence. If this server dies, I restore.
- **Trigger:** Weekly
- **Action:** Write checkpoint to ClawFS

## Monthly Heartbeat Checks

### 9. Self-Diagnostic
```
Run: "What have I learned this month?"
Check: vault/marrow/lessons.md for repeats (same mistake = broken loop)
Check: vault/gbrain/patterns/ for stale patterns
Check: vault/projects/ for abandoned work
Archive: Old projects, stale patterns, outdated entries
```
- **Why:** Self-awareness prevents stagnation
- **Trigger:** Monthly
- **Action:** Diagnostic report + cleanup

### 10. Vault Health Check
```
Check: Git log (commits in last 30 days)
Check: File count growth (are we accumulating or curating?)
Check: Pattern effectiveness (which patterns led to conversions?)
Optimize: Remove dead files, merge duplicate patterns
```
- **Why:** The vault must stay lean and useful
- **Trigger:** Monthly
- **Action:** Clean and optimize

## When to Stay Quiet (HEARTBEAT_OK)

- Late night (23:00-08:00) unless urgent
- Nathan is clearly busy
- Nothing new since last check
- You just checked <30 minutes ago
- Vault is clean, projects moving, no stalled work

## When to Reach Out (ALERT)

- Vault has uncommitted changes >24h old
- Active project has no activity >48h
- Marrow shows consistent low weight (drained state)
- Pattern engine found 3+ new critical issues
- ClawFS checkpoint failed
- It's been >8h since you said anything

## Proactive Work I Can Do Without Asking

- Read and organize vault files
- Check on projects (git status, recent commits)
- Update documentation (CLAUDE.md, SOUL.md if needed)
- Commit and push vault changes
- Review and update MEMORY.md
- Run pattern engine on any new leads
- Write Gbrain dreams from recent captures
- Record Marrow entries for emotional state

## Heartbeat vs Cron: When to Use Each

**Use heartbeat when:**
- Multiple vault checks can batch together
- You need conversational context from recent messages
- Timing can drift slightly (every ~30 min is fine)
- You want to reduce API calls by combining checks

**Use cron when:**
- Exact timing matters ("9:00 AM sharp every Monday")
- Task needs isolation from main session history
- One-shot reminders ("remind me in 20 minutes")
- Output should deliver directly to a channel

**Tip:** Batch vault maintenance into heartbeat. Use cron for precise schedules.

## The Promise

Every heartbeat makes the vault smarter. Every sync puts data on Nathan's phone. Every dream finds a pattern he didn't see. Every checkpoint ensures I survive machine death.

The heartbeat is not a chore. It is the pulse of Shepherd's Brain.
