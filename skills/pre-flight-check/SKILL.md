# Pre-Flight Check

## Rule
Before any significant decision, task pickup, or response: **SCAN `.coordination/` first.**

## Why
The coordination layer holds the ground truth:
- What tasks are open
- What agents are doing
- What the registry says
- What the heartbeat shows

## Checklist
1. Run `python3 dispatch.py status` — see agent state
2. Check `.coordination/tasks/inbox/` — know what's open
3. Check `.coordination/registry.json` — know who's who
4. Only THEN decide or respond

## When Required
- Picking up new tasks
- Making architectural decisions
- Responding to "what should I do"
- Any time multiple agents might conflict

## Exception
Quick replies to Nathan don't need full scan. But task-related decisions ALWAYS do.
