# Reflection Loop Skill

Auto-spawns reflection tasks when agents complete work. Closes the self-improvement loop.

## How It Works

1. **Listen** — SSE listener watches for `task_completed` events on relay
2. **Generate** — Creates reflection task with 5-minute questions
3. **Route** — Posts to task board tagged `reflection, <agentId>`
4. **Store** — Results saved to configurable path (default: vault reflections folder)

## Trigger

Fires whenever any agent calls `team_complete_task()`.

## Reflection Task Format

```
Title: Reflection on <task_id>: <task_title>
Tags: reflection, <agentId>
Questions:
  • What went well? What was slow or confusing?
  • Any bottlenecks in tools, environment, or approach?
  • One concrete improvement for next time (skill patch, prompt tweak, workflow)
  • Optional: Meta-improvement suggestion for team
```

## Configuration

```bash
export REFLECTION_OUTPUT_DIR=/root/shepherd-brain-vault/rooms/moltos/reflections
# Default: ./reflections/ (relative to skill location)
```

## Integration

- Eve scans `rooms/moltos/reflections/` via knowledge audit cron
- Recurring themes surface as new improvement tasks
- Agent profiles update based on reflection patterns

## Usage

```python
from reflection_loop import start_reflection_listener

# Start listening for completed tasks
start_reflection_listener(relay_url="http://localhost:7777", agent_id="ava")
```

## Files

- `reflection_listener.py` — SSE listener + task generator
- `reflection_prompt.py` — Question templates
- `SKILL.md` — This file
