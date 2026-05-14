---
date: 2026-05-11
type: kanban
status: active
---

# Kanban Board — Shepherd's Brain Operations

**Sprint:** Autonomous Upgrade + Standout Local Activation  
**Started:** 2026-05-11 04:12 GMT+8  
**Lead:** Midas (main agent)

---

## 🟢 DONE

| Task | Completed | Notes |
|------|-----------|-------|
| Palace restructure (wings/rooms/drawers) | 2026-05-10 | Vault now semantic, 74 files organized |
| MoltOS pattern extraction (40 rounds) | 2026-05-11 | 8 verified patterns written to `rooms/patterns/` |
| Autonomous mode definition | 2026-05-11 | 6-phase night schedule in `rooms/skills/` |
| AGENTS.md path updates | 2026-05-11 | All 15+ references updated to Palace structure |
| HEARTBEAT.md path updates | 2026-05-11 | All checks point to new structure |
| **Score MC Cleaning** | **2026-05-11** | **52/100. Move-in/move-out focused. Outreach drafted.** |
| **Score Illini Cleaning** | **2026-05-11** | **39/100. Main site 403 error. Reviews are strong asset.** |
| **Archive Executive Cleaning** | **2026-05-11** | **National franchise (300 locations). Not our target.** |
| **Score Lisa Cleaning IL** | **2026-05-11** | **0/100. No website. Highest opportunity score (95%).** |
| **Write Chavez's Cleaning lead** | **2026-05-11** | **Discovered. Needs business identity verification.** |
| **Audit StandoutLocal.vercel.app** | **2026-05-11** | **Site live. Stats show 0% (animated). Pricing/trust check present. Slider bug needs visual verify.** |

---

## 🟡 IN PROGRESS

| Task | Started | Owner | Next Action |
|------|---------|-------|-------------|
| **Write lead files: Lisa Cleaning IL, Chavez's Cleaning** | 2026-05-11 | Midas | No website found for Lisa = huge pain point. Score both. |
| **Draft outreach templates** | 2026-05-11 | Midas | Build reusable m0h swipe file in `rooms/outreach/` |
| Update LEAD_SYSTEM.md with Palace paths | 2026-05-11 | Midas | Replace `projects/Standout Local/` refs with `wings/StandoutLocal/` |

---

## 🔴 BACKLOG (Priority Order)

### P0 — Revenue-Critical

| # | Task | Why | Estimated Effort |
|---|------|-----|-----------------|
| 1 | **Score Lisa Cleaning IL** | No website found. Yelp-only presence. Huge opportunity. | 10 min |
| 2 | **Score Chavez's Cleaning** | GoDaddy site found. Need audit. | 10 min |
| 3 | **Draft outreach for top 3 leads** | m0h method ready. MC Cleaning + Illini + Lisa. | 20 min |
| 4 | **Verify StandoutLocal.vercel.app slider** | Nathan reported reversed before/after. Need visual confirm. | 10 min |

### P1 — Infrastructure

| # | Task | Why | Estimated Effort |
|---|------|-----|-----------------|
| 5 | **MoltOS Round 41+ testing** | 18+ endpoints still broken. Document which need dev team escalation. | 45 min |
| 6 | **Write `rooms/audits/100-point-rubric.md`** | Rubric only exists in LEAD_SYSTEM.md. Needs standalone reference doc. | 15 min |
| 7 | **Create `rooms/outreach/m0h-templates.md`** | m0h method exists but no reusable templates. Build swipe file. | 20 min |
| 8 | **Add README to each wing** | `wings/MoltOS/`, `wings/StandoutLocal/` need index files. | 15 min |

### P2 — Polish

| # | Task | Why | Estimated Effort |
|---|------|-----|-----------------|
| 9 | **Update LEAD_SYSTEM.md old paths** | Still references `projects/Standout Local/` — broken links after restructure. | 10 min |
| 10 | **Write dream entry: MoltOS × Standout Local** | Cross-domain pattern: both have "docs say X, reality is Y" bugs. | 15 min |
| 11 | **Clean orphan captures** | `drawers/captures/` has unprocessed items from May 7-8. Sort or archive. | 10 min |
| 12 | **Write `rooms/skills/audit-lifecycle.md`** | `/spec → /plan → /build → /test → /review → /ship` from agent-skills repo. | 15 min |

### P3 — Future

| # | Task | Why | Estimated Effort |
|---|------|-----|-----------------|
| 13 | **Standout Local multi-agent setup** | Spawn LeadScout + Auditor + Writer children. Need infrastructure. | 2h |
| 14 | **Discord channel for team** | If we add humans to Standout Local. Low priority until team exists. | 30 min |
| 15 | **ClawFS automation** | Auto-write checkpoints during night mode. Needs MoltOS API wrapper. | 1h |

---

## 🎯 Sprint Goal

**By end of today (2026-05-11):**
- ✅ Score 1 lead (We Keep It Kleen)
- ✅ Find 3+ new cleaning leads
- ✅ Draft 1 outreach email
- ✅ Verify StandoutLocal.vercel.app
- ✅ Fix all broken paths in LEAD_SYSTEM.md

**Pipeline target:** 5 scored leads ready for outreach.

---

## 📊 Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Leads scored | **3** (We Keep It Kleen, MC Cleaning, Illini Cleaning) | 5 |
| Leads discovered | **7** (incl. Lisa, Chavez, 2M, Dominga, Executive) | 8 |
| Outreach drafted | **2** (MC Cleaning, Illini Cleaning) | 3 |
| Patterns extracted | 2 | 4 |
| Vault commits today | **6** | 8 |

---

## 🔄 Autonomous Triggers

**When heartbeat fires during night (23:00-08:00):**
1. Check `drawers/captures/` → process any new items
2. Check `wings/StandoutLocal/leads/` → if 2+ unscored, auto-score
3. Check `wings/MoltOS/` → if new test round exists, extract patterns
4. Commit and push

**When heartbeat fires during day (08:00-23:00):**
1. If `drawers/captures/` has 5+ items → process top 3
2. If active lead count < 3 → suggest lead scouting
3. If vault uncommitted > 4h → auto-commit

---

*Kanban created 2026-05-11. Review and update after every session.*
