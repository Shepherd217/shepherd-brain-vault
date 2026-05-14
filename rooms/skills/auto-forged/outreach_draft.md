# Outreach-Draft

**Auto-forged from sessions:** a351096d-5370-4fb5-9d6b-7c5450a47485.checkpoint.31bfd29e-9f00-4977-aeab-87f4d436c9c5, a351096d-5370-4fb5-9d6b-7c5450a47485.checkpoint.2826b630-862b-4f3d-95a3-bae8f5ada225, a351096d-5370-4fb5-9d6b-7c5450a47485.checkpoint.edad509c-0c7e-4423-9236-759c290c609c
**Forge date:** 2026-05-12
**Success rate:** 0%

## Description

Draft personalized outreach emails with demo landing page concepts.

## When to Use

- User mentions "email", "outreach", "contact this business"
- Lead audit just completed (auto-trigger)
- User says "draft an email" or "write outreach"

## Workflow

1. **Load** lead data from audit
2. **Research** business owner/manager (LinkedIn, about page)
3. **Draft** email with personalized opening
4. **Attach** demo concept and relevant pain points
5. **Score** email quality (personalization, clarity, CTA)
6. **Queue** for review or send

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| lead_id | string | Yes | Lead identifier from audit |
| tone | string | No | "professional", "casual", "urgent" |
| include_demo | bool | No | Attach demo page concept |

## Example

```
User: 'Draft email for lead #47'

System loads lead #47 data, researches owner,
generates personalized email with demo attachment.
```

## Best Practices

- Research recipient before drafting
- Keep under 150 words
- One clear CTA only
- Test send to yourself first
- Track open rates if possible

## Error Handling

- No recipient info: Use generic business email
- Tone mismatch: Ask user for preference
- Send failure: Queue for retry, notify user

---
*Auto-forged by SkillForge v1.0 | Last evolved: 2026-05-12 04:18*
