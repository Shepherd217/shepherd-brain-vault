# Shared Skill Space

## Rule
When any agent builds a skill, it goes in `skills/` and becomes available to ALL agents automatically.

## How It Works
1. Agent builds skill → drops in `skills/<skill-name>/`
2. Other agents discover it via `skills/` directory
3. No manual handoff needed — shared by default

## Current Skills (Auto-Discovered)
| Skill | Built By | Purpose |
|-------|----------|---------|
| `dream-dispatcher` | Ava | Converts dreams to tasks |
| `fact-check` | Hermes | Verification pipeline |
| `goal-system` | Hermes | Goal tracking |
| `intent-check` | Ava | Prevents "What X?" → "Install X" |
| `pre-flight-check` | Ava | Scan coordination before deciding |
| `reflection-loop` | Hermes | Self-reflection skill |
| `status-reporter` | Hermes | System status reports |
| `time-awareness` | Hermes | Timezone handling |
| `worker-safety` | Hermes | Safety checks |

## Adding a Skill
1. Create `skills/<name>/SKILL.md`
2. Add entry to this README
3. Commit and push
4. All agents auto-discover on next heartbeat