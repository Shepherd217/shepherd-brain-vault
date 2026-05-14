# Multi-Agent

**Auto-forged from sessions:** a351096d-5370-4fb5-9d6b-7c5450a47485.checkpoint.edad509c-0c7e-4423-9236-759c290c609c, 00540939-1df9-4058-bd3e-6f8114f96020.checkpoint.a2e47bb5-6306-4925-a968-6ad6dac0c28a, a351096d-5370-4fb5-9d6b-7c5450a47485.checkpoint.3d77b4f0-934b-4601-aed1-db1dcb31e06b
**Forge date:** 2026-05-12
**Success rate:** 0%

## Description

Orchestrate multiple sub-agents for parallel task execution.

## When to Use

- Task requires parallel execution (research + writing + testing)
- User says "orchestrate", "delegate", "spawn agents"
- Complex task with multiple independent components

## Workflow

1. **Decompose** task into independent sub-tasks
2. **Spawn** sub-agents with specific goals
3. **Monitor** progress via subagents(action="list")
4. **Collect** results and integrate
5. **Validate** outputs against success criteria
6. **Report** consolidated results

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tasks | list | Yes | Array of sub-task descriptions |
| max_agents | int | No | Maximum parallel agents (default: 5) |
| timeout | int | No | Timeout per agent in seconds |

## Example

```
User: 'Research 5 cleaning companies in parallel'

System spawns 5 sub-agents, each audits one company.
Results collected and ranked in consolidated report.
```

## Best Practices

- Decompose into truly independent tasks
- Set clear success criteria per agent
- Monitor with subagents list
- Have fallback if agent fails
- Don't spawn more than 5 parallel agents

## Error Handling

- Agent timeout: Kill and retry with smaller scope
- Agent error: Collect partial results, flag for review
- Too many agents: Queue remaining, process in batches

---
*Auto-forged by SkillForge v1.0 | Last evolved: 2026-05-12 04:18*
