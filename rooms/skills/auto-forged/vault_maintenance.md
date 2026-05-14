# Vault-Maintenance

**Auto-forged from sessions:** a351096d-5370-4fb5-9d6b-7c5450a47485.checkpoint.31bfd29e-9f00-4977-aeab-87f4d436c9c5, a351096d-5370-4fb5-9d6b-7c5450a47485.checkpoint.2826b630-862b-4f3d-95a3-bae8f5ada225, a351096d-5370-4fb5-9d6b-7c5450a47485.checkpoint.edad509c-0c7e-4423-9236-759c290c609c
**Forge date:** 2026-05-12
**Success rate:** 0%

## Description

Maintain vault health: commit, push, index, clean.

## When to Use

- Heartbeat detects stale commits
- User says "sync vault", "commit changes", "push updates"
- End of session detected

## Workflow

1. **Check** git status for uncommitted changes
2. **Add** all vault changes
3. **Commit** with descriptive message
4. **Push** to remote
5. **Verify** sync success
6. **Update** semantic search index if files changed

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| scope | string | No | "all" or specific directory |
| message | string | No | Custom commit message |
| push | bool | No | Push after commit (default: true) |

## Example

```
Heartbeat triggers vault_maintenance:
- Detects 3 uncommitted files
- Commits: 'auto: heartbeat sync'
- Pushes to origin
- Re-indexes semantic search
```

## Best Practices

- Commit early, commit often
- Write descriptive messages
- Verify push succeeded
- Keep vault lean (archive old files)
- Re-index search after bulk changes

## Error Handling

- Push rejected: Pull first, resolve conflicts
- Large files: Use git LFS or exclude
- Index fail: Log and retry on next heartbeat

---
*Auto-forged by SkillForge v1.0 | Last evolved: 2026-05-12 04:18*
