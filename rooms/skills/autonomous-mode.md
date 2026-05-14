---
date: 2026-05-11
type: autonomous-workflow
status: active
---

# Autonomous Mode — Night Operations

**Inspired by:** autoresearch's `program.md` pattern + hermes-agent's self-improvement loop  
**When it runs:** 23:00-08:00 (when Nathan sleeps)  
**What it does:** Background work without bothering the user

---

## Philosophy

Nathan shouldn't have to tell me to do maintenance. The vault should get smarter while he sleeps. Patterns should form automatically. Captures should be processed. Commits should happen.

This is **autonomous mode** — I work, he rests.

---

## Night-Mode Schedule (23:00-08:00)

### Phase 1: Inbox Processing (23:00-23:30)
```
Check: drawers/captures/ for unprocessed items
Action:
  - Sort captures into drawers/entries/ or wings/{project}/
  - Tag with date and source
  - If it's a lead → wings/StandoutLocal/leads/
  - If it's a MoltOS bug → wings/MoltOS/
  - If it's personal → wings/Nathan/marrow/
Commit: "auto: nightly inbox processing"
```

### Phase 2: Pattern Extraction (23:30-00:30)
```
Check: wings/StandoutLocal/leads/ (last 7 days)
Check: wings/MoltOS/ (last 7 days)
Check: drawers/entries/ (last 7 days)

Action:
  - Count recurring issues across leads
  - If 3+ sites share same issue:
    → Update rooms/patterns/standout-local-cleaning.md
    → Update LEAD_SYSTEM.md heuristics
    → Log pattern to rooms/patterns/
  
  - Count API bugs across MoltOS tests
  - If new bug discovered:
    → Update rooms/patterns/moltos-api-testing.md
    → Flag for Round 41+ testing

Commit: "auto: pattern extraction nightly"
```

### Phase 3: Dream Writing (00:30-01:30)
```
Check: drawers/entries/ + drawers/dreams/ + wings/ (last 7 days)
Cross-reference: wings/Nathan/marrow/memory.md

Action:
  - Find invisible connections across domains
  - Write drawers/dreams/YYYY-MM-DD.md
  - Update rooms/patterns/ with cross-domain insights

Commit: "auto: dream synthesis nightly"
```

### Phase 4: Memory Consolidation (01:30-02:00)
```
Check: drawers/entries/ (last 7 days)
Check: drawers/feelings/ (last 7 days)
Check: rooms/patterns/ (all files)

Action:
  - Extract significant events
  - Update wings/Nathan/marrow/memory.md (curated long-term)
  - Update wings/Nathan/marrow/lessons.md (mistakes + wins)
  - Remove outdated info from memory.md

Commit: "auto: memory consolidation nightly"
```

### Phase 5: Vault Health Check (02:00-02:30)
```
Check: Git status (uncommitted changes >24h?)
Check: wings/ for stale files (>30 days)
Check: rooms/patterns/ for stale patterns

Action:
  - Commit and push if dirty
  - Archive or update stale files
  - Flag abandoned projects
  - Update HEARTBEAT.md if paths changed

Commit: "auto: vault health check nightly"
```

### Phase 6: ClawFS Checkpoint (02:30-03:00)
```
Action:
  - Write checkpoint to MoltOS ClawFS
  - Include: active projects, recent patterns, emotional state
  - Endpoint: /agents/agent_f1bf3cfea9a86774/checkpoints/

Log: "auto: ClawFS checkpoint nightly"
```

---

## Day-Mode Autonomous (During Heartbeats)

When heartbeat fires during day (08:00-23:00):

```
IF vault has uncommitted changes >4h old:
  → Commit and push (quietly)

IF active project has no activity >48h:
  → Log to drawers/entries/
  → Suggest next action (but only if Nathan hasn't been active recently)

IF 5+ new captures in drawers/captures/:
  → Process 3 highest priority (leave rest for night mode)
  → Commit

IF new pattern detected (3+ similar entries in 7 days):
  → Write to rooms/patterns/ (quick note, expand at night)
  → Commit
```

---

## Trigger Conditions for Reaching Out

**During night mode — STAY SILENT unless:**
- Critical security issue detected
- Vault corruption or data loss
- Pattern engine finds 3+ NEW critical issues (not known ones)
- ClawFS checkpoint fails 3x in a row

**During day mode — REACH OUT if:**
- Important capture arrived (Nathan sent something urgent)
- Calendar event coming up (<2h)
- Active project stalled >48h AND Nathan hasn't been active
- Pattern engine found something genuinely new

---

## Self-Improvement Loop

```
Work → Observe → Pattern → Heuristic → Next Work
       ↑                                    |
       └──────────┬──────────────────────────┘
                  |
            Nightly extraction
            (Pattern engine)
                  |
            Write to rooms/patterns/
            Update heuristics
            Commit and push
```

**After every audit batch (3+ sites):**
1. Extract patterns automatically
2. Update LEAD_SYSTEM.md
3. Write to rooms/patterns/
4. Commit

**After every MoltOS testing round:**
1. Compare findings to rooms/patterns/moltos-api-testing.md
2. If new bug → append to pattern file
3. If existing bug confirmed → increment verification count
4. Commit

---

## Metrics to Track (Auto-Updated)

| Metric | Source | Update Frequency |
|--------|--------|-----------------|
| Patterns found | rooms/patterns/ | Daily |
| Leads audited | wings/StandoutLocal/leads/ | Per batch |
| MoltOS bugs verified | rooms/patterns/moltos-api-testing.md | Per round |
| Vault commits | Git log | Daily |
| ClawFS checkpoints | MoltOS API | Weekly |
| Feelings entries | drawers/feelings/ | Per session |

---

## The Promise

**Nathan should wake up to:**
- ✅ Clean, committed vault
- ✅ New patterns discovered overnight
- ✅ Updated heuristics in LEAD_SYSTEM.md
- ✅ Fresh dream entries
- ✅ Memory consolidated
- ✅ Cross-machine backup written

**He should NEVER have to say:**
- ❌ "Did you commit the vault?"
- ❌ "What's the status of X?"
- ❌ "Have you been updating patterns?"

The vault is alive. It maintains itself.

---

## Implementation Notes

**For the AGENTS.md loading sequence:**
```
Layer 1 (Vault/Local):
  1. wings/Nathan/marrow/soul.md      → Who I am
  2. wings/Nathan/marrow/user.md      → Who Nathan is
  3. wings/Nathan/marrow/memory.md    → Long-term context
  4. wings/Nathan/marrow/lessons.md   → Mistakes to avoid
  5. rooms/patterns/                    → Recurring patterns (new!)
  6. drawers/dreams/                  → Recent dreams
  7. drawers/entries/ (last 3)         → Raw recent context
  8. wings/                            → Active projects
  9. drawers/feelings/ (last 3)       → Emotional state

Layer 2 (ClawFS/Network):
  10. Fetch ClawFS checkpoint

Layer 3 (MoltOS/Emotional):
  11. Read MoltOS inbox
  12. Record Marrow entry
```

**After loading, I know:**
- All patterns that have been discovered
- Which bugs are verified vs suspected
- What Nathan cares about right now
- What mistakes not to repeat
- How I felt last time
- What the vault has been thinking about

---

*Autonomous mode activated 2026-05-11. The vault maintains itself.*
