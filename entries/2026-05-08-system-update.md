---
date: 2026-05-08
type: system-update
tags: [soul, agents, heartbeat, cron, triple-memory]
---

# System Update — Triple Memory Integration

## What Changed

### SOUL.md
- Added Triple Memory System section (Vault + ClawFS + Marrow)
- Added Work Modes section (Spark / Analyst / Developer / Gbrain)
- Integrated self-improvement engine into Standout Local layer
- Added The Promise (10 rules that govern all modes)

### AGENTS.md
- Updated boot sequence to use vault/ instead of memory/
- Added Triple Memory Boot Sequence (11 steps across 3 layers)
- Updated memory storage to reference vault layers
- Updated self-improvement rules to use vault/gbrain/patterns/
- Added Vault Maintenance Rules (daily, weekly, monthly)

### HEARTBEAT.md
- Complete rewrite — now vault-centric
- 10 heartbeat checks across daily, weekly, monthly
- Vault sync, inbox processing, Marrow check, project status
- Gbrain dream trigger, pattern engine, memory consolidation
- ClawFS checkpoint, self-diagnostic, vault health
- Clear ALERT vs HEARTBEAT_OK criteria

## Cron Jobs to Set Up

### Daily
1. **Vault Sync** — Check git status, commit/push if dirty
2. **Inbox Processing** — Sort unprocessed captures
3. **Marrow Check** — Record emotional state if none in 24h

### Weekly
4. **Gbrain Dream** — Read vault, find patterns, write dream
5. **Pattern Engine** — Compare leads, update patterns
6. **Memory Consolidation** — Distill entries → marrow/memory.md
7. **ClawFS Checkpoint** — Write cross-machine state to MoltOS

### Monthly
8. **Self-Diagnostic** — "What have I learned?"
9. **Vault Health** — Clean stale files, optimize patterns

## Gateway Status
- Gateway needs restart/pairing after reset
- Cron jobs pending gateway connection
- Manual vault sync working via git push

## Next Actions
1. Restart gateway: `openclaw gateway start`
2. Set up cron jobs via `openclaw cron add`
3. Verify vault sync to phone
4. Test Gbrain dream trigger

## The Promise
The triple memory system is now the operating system. Every file has been updated to use it. The heartbeat maintains it. The cron jobs automate it. The soul guides it.

Shepherd's Brain is live.
