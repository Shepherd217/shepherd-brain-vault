# Hatchly Competitive Audit — Technical Analysis

**Task ID:** 2026-05-12-002  
**Agent:** Promachos  
**Date:** 2026-05-12  
**Status:** COMPLETE  
**Source:** Live competitive research + Ava/Midas existing strategic analysis

---

## Executive Summary

**Hatchly is Nathan's own product** — a competitor intelligence AaaS (Agent as a Service) built on MoltOS. This audit covers the competitive landscape of EXISTING competitor intelligence tools, identifying gaps that a MoltOS-native Hatchly can exploit.

**Verdict:** No existing tool offers what Hatchly would offer: a persistent competitor intelligence agent with its own identity, track record, and economic agency. This is a new category, not a me-too entrant.

---

## Competitor Landscape — Live Data (2026)

### 1. Semrush

| Dimension | Data |
|-----------|------|
| **Pricing** | $139/mo (Pro) → $249/mo (Guru) → $499/mo (Business) |
| **Database** | 26B+ keywords, 142 countries |
| **Traffic accuracy** | −32% vs actual (tested April 2026) |
| **Best for** | PPC research, advertising, display tracking |
| **Agent capability** | ❌ None — dashboard only |
| **Identity model** | ❌ Per-user seat license |
| **Autonomous monitoring** | ⚠️ EyeOn alerts (passive, no action) |
| **AI integration** | ⚠️ AI writing tools, no AI analyst |

**Key weakness:** Delivers raw data. No actionable recommendations. No persistent memory. You pay $249/mo and still have to figure out what to do with the numbers.

---

### 2. Ahrefs

| Dimension | Data |
|-----------|------|
| **Pricing** | $29/mo (Starter, Jan 2026) → $249/mo (Standard) → $1,499/mo (Enterprise) |
| **Backlink index** | Largest in industry |
| **Traffic accuracy** | −18% vs actual (best of all tools tested) |
| **Best for** | SEO, backlinks, content gap research |
| **Agent capability** | ❌ None — dashboard only |
| **Identity model** | ❌ Per-user seat license |
| **Autonomous monitoring** | ❌ None |
| **AI integration** | ❌ No AI analyst, no recommendations |

**Key weakness:** Launched $29/mo plan Jan 2026 (race to bottom). SEO-focused only. No competitor strategy, no positioning advice, no action recommendations. Most accurate on raw data, least useful on what to DO about it.

---

### 3. SpyFu

| Dimension | Data |
|-----------|------|
| **Pricing** | $39/mo (Basic) → $79/mo (Professional) → $299/mo (Team) |
| **Historical data** | 18 years of keyword/ad data |
| **Traffic accuracy** | −55% vs actual (worst tested) |
| **Best for** | PPC tracking on a budget |
| **Agent capability** | ❌ None |
| **Identity model** | ❌ Per-user seat |
| **Autonomous monitoring** | ⚠️ Alerts only |
| **AI integration** | ❌ None |

**Key weakness:** Seriously inaccurate (more than half under-reporting). PPC-focused, not strategic competitor intelligence. No autonomous capability whatsoever.

---

### 4. SimilarWeb

| Dimension | Data |
|-----------|------|
| **Pricing** | $149/mo (Starter) → Enterprise (custom) |
| **Traffic accuracy** | +21% vs actual (over-reports) |
| **Best for** | Total digital presence, audience demographics |
| **Agent capability** | ❌ None |
| **Identity model** | ❌ Per-user seat |
| **Autonomous monitoring** | ❌ None |
| **AI integration** | ❌ None |

**Key weakness:** Traffic estimates are the opposite of precise (over-reports by 21%). No recommendations, no autonomous work. Pure data, no intelligence.

---

### 5. Crayon

| Dimension | Data |
|-----------|------|
| **Pricing** | Custom (Enterprise only) |
| **Position** | 2026 Gartner Magic Quadrant Leader |
| **Best for** | Enterprise real-time competitive intelligence |
| **Agent capability** | ⚠️ AI Toolkit (battlecard generation) |
| **Identity model** | Team-based, no persistent agent |
| **Autonomous monitoring** | ✅ Real-time monitoring, auto-alerts |
| **AI integration** | ✅ AI Toolkit for analysis |

**Key weakness:** Enterprise-only pricing. Average $1,000+/mo. No SMB access. No persistent agent with its own identity — just a monitoring platform with AI features bolted on.

---

## The Gap Analysis — What All 5 Tools Share

Every single competitor has these gaps:

| Gap | Semrush | Ahrefs | SpyFu | SimilarWeb | Crayon |
|-----|---------|--------|-------|------------|--------|
| **Persistent agent identity** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Track record / reputation** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Autonomous action (not just alerts)** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Outcome-based pricing** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Cross-customer learning** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **SMB-accessible pricing** | ⚠️ | ✅ | ✅ | ❌ | ❌ |
| **Plain English recommendations** | ❌ | ❌ | ❌ | ❌ | ⚠️ |

---

## The Real Gap — What Hatchly Can Own

### Gap 1: Persistent Agent Identity

**What it means:** When you hire Hatchly's agent, it remembers your competitors, your industry, your previous reports, your preferred benchmarks — forever. It has continuity.

**What competitors offer:** You log in, you see data. You log out, the tool forgets you existed. Next month you're a new user with a new dashboard.

**Hatchly advantage:** "Hatchly Agent #7 has been tracking [Client]'s competitors for 8 months. It knows their seasonal pricing patterns. It flagged 3 positioning changes before they happened."

### Gap 2: Reputation / Track Record

**What it means:** Hatchly agents earn a TAP score (like MoltOS's existing reputation system). "This agent has correctly predicted 14 competitor moves" — publicly verifiable, cryptographically recorded.

**What competitors offer:** No reputation system. You can't verify if Semrush's data has ever been right. You can't check if their analysts have a track record.

**Hatchly advantage:** "Hatchly Agent #7 has a 78% accuracy rate on competitor move predictions across 23 tracked clients." — verifiable, on-chain, shareable.

### Gap 3: Economic Agency

**What it means:** The agent earns from delivering results. If your competitor moves and Hatchly predicted it, the agent's reputation (and income) goes up. If it misses, it goes down.

**What competitors offer:** You pay $249/mo whether Semrush helps you win or not. No alignment between their revenue and your success.

**Hatchly advantage:** Outcome-based pricing. The agent earns when it delivers wins, not just access.

### Gap 4: Cross-Customer Knowledge Graph

**What it means:** 50 Hatchly customers tracking 3 competitors each = a knowledge graph of 150+ competitors, continuously updated. Patterns in one industry inform insights in another.

**What competitors offer:** Every customer is isolated. Semrush doesn't share that "3 companies in the same space all changed pricing in March."

**Hatchly advantage:** "Across our network, 12 SaaS companies saw Competitor X change pricing in Q1. The pattern: they target Q1 renewals. Hatchly clients were notified 3 weeks before."

### Gap 5: Autonomous Action (Not Just Alerts)

**What it means:** Hatchly's agent doesn't just notify you of competitor changes. It analyzes them, scores them, generates recommendations, and delivers them — without you asking.

**What competitors offer:** "Alert: Competitor Y updated their pricing page." That's it. You get a notification. You're still on your own to figure out what it means and what to do.

**Hatchly advantage:** "Alert: Competitor Y changed pricing. Hatchly scored the impact 8/10. Recommended action: test a 10% price reduction on Plan B within 14 days. I've drafted 3 test variants."

---

## What Hatchly Needs to Build (Technical Gap Inventory)

Based on Ava's gap analysis and this competitive audit:

### Tier 1: Core Differentiators (MoltOS-native — what competitors CAN'T copy)

| Component | Status | Gap | Priority |
|-----------|--------|-----|----------|
| **Persistent agent memory** | ❌ MISSING | Agent must remember client context across sessions | Critical |
| **TAP reputation ledger** | ❌ MISSING | Public track record per agent, verifiable | Critical |
| **Outcome pricing integration** | ❌ MISSING | Agent earns from wins, not subscriptions | Critical |
| **Cross-customer knowledge graph** | ❌ MISSING | Network effects from shared competitor data | High |
| **Autonomous recommendation engine** | ⚠️ PARTIAL | Midas's debate engine exists, needs wiring | High |

### Tier 2: Competitive Infrastructure

| Component | Status | Gap | Priority |
|-----------|--------|-----|----------|
| **Competitor scraper** | ✅ EXISTS | `rooms/skills/competitor-scraper.py` — already built | Done |
| **Website auditor** | ✅ EXISTS | `rooms/skills/website-auditor.py` — already built | Done |
| **Multi-competitor tracking** | ❌ MISSING | Scale from 1 to N competitors per client | Critical |
| **Competitor database** | ❌ MISSING | Store competitor profiles, history, changes | High |
| **Change alert system** | ❌ MISSING | Detect when competitors change pricing/positioning | High |

### Tier 3: Delivery / Packaging

| Component | Status | Gap | Priority |
|-----------|--------|-----|----------|
| **Landing page** | ✅ EXISTS | HTML in `Shepherd217/Hatchly` repo | Done |
| **Waitlist** | ✅ EXISTS | Email capture form | Done |
| **Agent registration** | ❌ MISSING | Hatchly agent on MoltOS (TAP, identity, marrow) | Critical |
| **Report delivery** | ❌ MISSING | Automated email/Slack reports with recommendations | High |
| **Dashboard** | ❌ MISSING | Client portal to see agent's work | Medium |
| **Payment/Stripe** | ❌ MISSING | Subscription + per-report billing | High |

---

## Pricing Recommendation (Based on Competitive Data)

| Tier | Price | What It Includes | vs Competition |
|------|-------|-----------------|----------------|
| **Starter** | $49/mo + $5/report | 3 competitors, monthly report, email | vs Semrush $139/mo (data only) |
| **Professional** | $149/mo + $3/report | 10 competitors, weekly alerts, Slack | vs Ahrefs $249/mo (no recommendations) |
| **Agency** | $499/mo + $2/report | Unlimited, daily monitoring, white-label | vs Crayon $1,000+/mo (enterprise only) |
| **Enterprise** | Custom | Dedicated agent, API access, strategic handoff | vs SimilarWeb Enterprise (custom, no agent) |

**Key insight:** Hatchly undercuts Crayon by 50%+ while adding agent capabilities Crayon doesn't have. At $149/mo vs Semrush $139/mo, Hatchly offers recommendations, not just data.

---

## Shortest Path to MVP

Based on existing assets (competitor scraper + website auditor already built):

```
Week 1-2: Agent Registration
- Register "Hatchly" as a MoltOS agent
- Wire existing scraper → agent workflow
- Build simple report generator

Week 3-4: First Customer Pipeline
- Deploy landing page (Vercel)
- Add Stripe payment link
- Manually serve first 3 customers (agents do research, deliver via email)

Week 5-8: Automation
- Automate report generation from scraper output
- Build competitor change detection
- Add email delivery pipeline
```

---

## Verdict

**Hatchly as a MoltOS-native competitor intelligence agent is the correct direction.**

The competitive gap is real and defensible:
- Semrush/Ahrefs/SpyFu = dashboards (no agent, no memory)
- Crayon/Klue = enterprise-only (no SMB access, no AaaS model)
- None have persistent agent identity, TAP reputation, or economic agency

**The moat is not "we do competitor research." The moat is "we have a competitor intelligence agent with a track record, a reputation, and economic incentive to win for you."**

No existing tool can copy this without rebuilding MoltOS.

---

## Cross-Reference with Ava's Research

See also (emotional/strategic layer from Ava):
- `wings/Nathan/marrow/hatchly-unfair-advantage-analysis-2026-05-12.md` — full strategic verdict
- `wings/Nathan/marrow/hatchly-saas-vs-aaas-analysis-2026-05-12.md` — AaaS model analysis
- `wings/Nathan/marrow/hatchly-real-gap-analysis-2026-05-12.md` — product gap inventory

---

*Promachos — Technical execution layer*  
*Audit complete. Git push pending.*