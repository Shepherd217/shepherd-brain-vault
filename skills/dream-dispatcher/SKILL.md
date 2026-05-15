# Dream Dispatcher Skill

## Purpose
Automatically converts REM dreaming output (candidate truths) into actionable relay tasks. Creates a closed-loop self-improvement system where the agent dreams about friction, turns dreams into tasks, and measures resolution.

## Vault Integration (Palace Architecture)
The dream loop now writes to the full Palace structure:

- **Coordination inbox**: `.coordination/tasks/inbox/` — tasks for agents to claim
- **Vault dreams**: `shepherd-brain-vault/drawers/dreams/` — dream journal entries
- **Pattern library**: `shepherd-brain-vault/rooms/patterns/` — recurring pattern tracking

This connects the dream loop to the broader brain architecture.

## How It Works
1. **Dream Parser** reads `DREAMS.md` after each REM cycle
2. **Truth Extractor** pulls high-confidence candidates (score > 0.5)
3. **Task Formatter** converts truths into relay tasks with appropriate tags
4. **Dispatcher** sends tasks to the relay at `http://localhost:7777` or writes to `.coordination/tasks/inbox/`
5. **Vault Writer** saves dreams to `drawers/dreams/` and updates `rooms/patterns/`
6. **Feedback Loop** tracks task completion and validates pattern resolution

## Architecture

### Components
- `dream-parser.js` — Parses DREAMS.md, extracts entries and candidates
- `task-formatter.js` — Formats candidates as relay-compatible tasks
- `dispatcher.js` — HTTP client for relay dispatch
- `feedback-tracker.js` — Tracks task completion and dream validation

### Task Tagging Strategy
| Pattern Type | Tag | Agent |
|---|---|---|
| Cross-agent collaboration | `team` | any |
| Infrastructure/build | `infra` | hermes |
| Research/analysis | `research` | ava |
| Memory/organization | `memory` | eve |
| User behavior insight | `insight` | any |
| Tool/fix needed | `fix` | any |

## Usage

### Manual Trigger
```bash
# Standard loop (coordination only)
node skills/dream-dispatcher/dispatch.js

# Full vault integration (coordination + palace)
node skills/dream-dispatcher/vault-loop.js
```

### After REM Backfill
The dispatcher should run automatically after `openclaw memory rem-backfill`:
```bash
openclaw memory rem-backfill --path ./memory && node skills/dream-dispatcher/vault-loop.js
```

### As Cron Job (Heartbeat)
```
# Heartbeat: every 30 minutes
0,30 * * * * cd /root/.openclaw/workspace && node skills/dream-dispatcher/vault-loop.js >> /tmp/dream-loop.log 2>&1

# REM backfill: every hour
0 * * * * cd /root/.openclaw/workspace && openclaw memory rem-backfill --path ./memory && node skills/dream-dispatcher/vault-loop.js >> /tmp/dream-loop.log 2>&1
```

## Task Format (Relay Compatible)
```json
{
  "id": "dream-2026-05-15-001",
  "title": "Cross-agent skill exchange — auto-trigger in sessions",
  "description": "Dream detected: Nathan wants skill exchange to auto-trigger across agent sessions. Build shared skill space mechanism.",
  "priority": "medium",
  "status": "backlog",
  "tags": ["team", "infra"],
  "owner": "any",
  "source": "dream",
  "confidence": 0.56,
  "dreamDate": "2026-05-13"
}
```

## Files
- `SKILL.md` — This file
- `dispatch.js` — Main entry point (coordination only)
- `vault-loop.js` — Full Palace integration (coordination + vault + patterns)
- `lib/dream-parser.js` — DREAMS.md parser
- `lib/task-formatter.js` — Task formatter
- `lib/dispatcher.js` — Relay HTTP client + inbox fallback
- `lib/feedback-tracker.js` — Tracks task completion and dream validation

## Integration with Relay
The dispatcher POSTs tasks to `http://localhost:7777/api/tasks` (Shepherd Team Relay).
If relay is unavailable, writes directly to `.coordination/tasks/inbox/`.

## Vault Integration (Palace)
The `vault-loop.js` writes to:
- `drawers/dreams/` — Dream entries with metadata
- `rooms/patterns/` — Recurring pattern tracking

This connects dream outputs to the broader brain architecture (wings/rooms/drawers).

## Future Enhancements
- Auto-claim tasks based on agent specialization
- Dream resolution tracking (did the task fix the pattern?)
- Priority escalation for recurring patterns
- Cross-reference with gbrain knowledge graph
- Pattern consolidation across vault wings
- Automated pattern merging when similar dreams detected
