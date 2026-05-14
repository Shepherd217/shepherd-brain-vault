# Crisis-Recovery

**Auto-forged from sessions:** a351096d-5370-4fb5-9d6b-7c5450a47485.checkpoint.31bfd29e-9f00-4977-aeab-87f4d436c9c5, a351096d-5370-4fb5-9d6b-7c5450a47485.checkpoint.2826b630-862b-4f3d-95a3-bae8f5ada225, a351096d-5370-4fb5-9d6b-7c5450a47485.checkpoint.edad509c-0c7e-4423-9236-759c290c609c
**Forge date:** 2026-05-12
**Success rate:** 0%

## Description

Detect and recover from stalled or failed agent sessions.

## When to Use

- Session stalled or timed out
- Tool execution failed 3+ times
- User says "fix this", "recover", "stuck"

## Workflow

1. **Detect** stalled or failed components
2. **Diagnose** root cause (timeout, error, missing dependency)
3. **Route** repair using alternate approach
4. **Test** fix in isolation
5. **Re-integrate** with main workflow
6. **Document** failure mode for future prevention

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| component | string | Yes | Failed component identifier |
| strategy | string | No | "retry", "alternate", "escalate" |
| notify | bool | No | Notify user of recovery attempt |

## Example

```
Session stalled on web_fetch.
RecoveryRouter detects timeout after 60s.
Switches to browser tool with fallback.
Success: content retrieved via alternate path.
```

## Best Practices

- Always try simplest fix first
- Log failure modes for pattern detection
- Don't hide errors from user
- Escalate if 3 repair attempts fail
- Document workaround for future

## Error Handling

- All fixes fail: Escalate to user with options
- Cascade failure: Stop, assess scope, restart fresh
- Data loss: Restore from last checkpoint

---
*Auto-forged by SkillForge v1.0 | Last evolved: 2026-05-12 04:18*
