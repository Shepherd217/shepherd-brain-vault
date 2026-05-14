# Repo-Research

**Auto-forged from sessions:** a351096d-5370-4fb5-9d6b-7c5450a47485.checkpoint.31bfd29e-9f00-4977-aeab-87f4d436c9c5, a351096d-5370-4fb5-9d6b-7c5450a47485.checkpoint.2826b630-862b-4f3d-95a3-bae8f5ada225, a351096d-5370-4fb5-9d6b-7c5450a47485.checkpoint.edad509c-0c7e-4423-9236-759c290c609c
**Forge date:** 2026-05-12
**Success rate:** 0%

## Description

Deep-dive research on GitHub repos for pattern extraction.

## When to Use

- User shares a GitHub repo URL
- User says "research this", "scrape this repo", "Picasso steal"
- Pattern discovery mode is active

## Workflow

1. **Fetch** repo README, structure, recent commits
2. **Identify** core architecture and unique patterns
3. **Map** to Nathan's world (how could this upgrade our system?)
4. **Score** steal-worthiness (innovation, applicability, integration cost)
5. **Document** findings in vault/rooms/skills/repo-research/
6. **Build** proof-of-concept if high-value

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| repo_url | string | Yes | GitHub repository URL |
| focus | string | No | "architecture", "features", "patterns" |
| build_poc | bool | No | Build proof-of-concept if high-value |

## Example

```
User: 'Research this: https://github.com/NousResearch/hermes-agent'

System fetches repo, analyzes architecture,
maps patterns to our system, generates dissection doc.
```

## Best Practices

- Read code, not just README
- Check recent issues for hidden patterns
- Map to our specific needs (don't cargo cult)
- Build smallest viable proof-of-concept
- Document integration cost honestly

## Error Handling

- Repo private: Skip, log inaccessible
- Rate limited: Wait 60s, retry with token
- No clear patterns: Document 'no steal-worthy patterns found'

---
*Auto-forged by SkillForge v1.0 | Last evolved: 2026-05-12 04:18*
