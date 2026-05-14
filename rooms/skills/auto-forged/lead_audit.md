# Lead-Audit

**Auto-forged from sessions:** a351096d-5370-4fb5-9d6b-7c5450a47485.checkpoint.31bfd29e-9f00-4977-aeab-87f4d436c9c5, a351096d-5370-4fb5-9d6b-7c5450a47485.checkpoint.2826b630-862b-4f3d-95a3-bae8f5ada225, a351096d-5370-4fb5-9d6b-7c5450a47485.checkpoint.edad509c-0c7e-4423-9236-759c290c609c
**Forge date:** 2026-05-12
**Success rate:** 0%

## Description

Perform comprehensive website audits for local service businesses.

## When to Use

- User mentions "audit", "website review", "check this site"
- User shares a business website URL
- Standout Local campaign is active
- User says "score this lead" or "rate this site"

## Workflow

1. **Fetch** website content via browser or web_fetch
2. **Extract** business info: name, services, location, contact
3. **Score** using 100-point rubric
4. **Identify** pain points (missing CTA, no mobile optimization, etc.)
5. **Generate** demo landing page concept
6. **Draft** personalized outreach hook
7. **Package** into lead packet with scores and recommendations

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| url | string | Yes | Business website URL |
| niche | string | No | Service category (cleaning, roofing, etc.) |
| depth | string | No | "quick" (5 min) or "deep" (15 min) |

## Example

```
User: 'Audit this site: https://cleanpro-champaign.com'

System executes lead_audit:
- Fetches site
- Scores: 67/100
- Pain points: No mobile CTA, slow load, no FAQ schema
- Demo concept: 'Move-Out Cleaning Special' landing page
- Outreach hook: 'I noticed your site loads in 4.2s on mobile...'
```

## Best Practices

- Always verify business is still operating
- Check for multiple locations (franchise?)
- Score conservatively — better to under-promise
- Include exact quotes from website
- Never fabricate claims

## Error Handling

- Website unreachable: Try browser fallback, then skip
- No contact info: Flag for manual research
- Score ambiguity: Conservative score, note uncertainty
- Tool failure: Log and move to next lead

---
*Auto-forged by SkillForge v1.0 | Last evolved: 2026-05-12 04:18*
