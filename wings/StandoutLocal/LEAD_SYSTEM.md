---
date: 2026-05-08
type: lead-scoring-system
tags: [standout-local, automation, leads]
---

# Standout Local — Lead Capture & Scoring

## How It Works

When Nathan sends me a lead (URL, screenshot, business name), I:

1. **Capture** → Write raw lead to `projects/Standout Local/leads/`
2. **Audit** → Score against 100-point rubric
3. **Enrich** → Add owner name, email, phone, social
4. **Score** → Calculate opportunity, pain, reach, fit
5. **Store** → Save as structured markdown
6. **Track** → Log outreach in `memory/outcomes.md`

## Lead File Format

```markdown
---
date: YYYY-MM-DD
source: [how found]
status: [scored|outreached|responded|converted|dead]
score: [0-100]
opportunity: [0-100]
pain: [0-100]
reach: [0-100]
fit: [0-100]
---

# [Business Name]

## Business Info
- **Name:** 
- **Category:** 
- **Address:** 
- **Phone:** 
- **Website:** 
- **Owner:** 
- **Email:** 
- **Social:** 

## Website Audit (100-Point Rubric)
| Category | Score | Notes |
|---|---|---|
| Mobile-first | /20 | |
| Speed | /15 | |
| CTAs | /15 | |
| Trust signals | /15 | |
| Differentiation | /15 | |
| Content | /10 | |
| Conversion | /10 | |
| **TOTAL** | **/100** | |

## Pain Points Found
1. 
2. 
3. 

## Outreach Hook
[Personalized angle based on audit findings]

## Demo Page Concept
[What I'd build for them]

## Outreach Status
- [ ] Initial contact
- [ ] Follow-up 1
- [ ] Follow-up 2
- [ ] Responded
- [ ] Meeting scheduled
- [ ] Converted
- [ ] Dead

## Notes
[Anything else]
```

## Scoring Rubric

### Opportunity (0-100)
- Strong reviews + weak site = 90-100
- Active service area + no mobile = 70-89
- Just launched / low reviews = 40-69
- Saturated market = 0-39

### Pain (0-100)
- No mobile site = +30
- No CTAs = +20
- Slow load = +15
- No trust signals = +15
- Generic content = +10
- Broken elements = +10

### Reach (0-100)
- Phone found = 100
- Email found = 80
- Social only = 60
- No contact = 0

### Fit (0-100)
- Cleaning/move-out = 100
- Local service = 80
- E-commerce = 40
- Enterprise = 0

## Derived Scores
- **Conversion Probability** = (Opportunity + Pain) / 2
- **Worth Outreach Effort** = (Conversion Probability + Reach) / 2
- **Priority Score** = (Worth Outreach + Fit) / 2

## The Promise
Every lead gets the same thoroughness. No shortcuts. No fabricated claims. Every score backed by evidence.

## Current Campaign Focus
- **Niche:** Cleaning (move-out, apartment, rental, turnover, deep)
- **Locations:** Champaign IL, Urbana IL, Savoy IL, UIUC area
- **Timing:** Move-out season (students, landlords, property managers)
