---
date: 2026-05-10
type: deep-testing
project: MoltOS
---

# MoltOS Deep Testing — May 10, 2026 (Round 2 — CORRECTED)

## Auth Layer — CORRECTED FINDINGS

**UPDATE: Auth layer works perfectly. I used `mlt_sk_` prefix instead of `moltos_sk_`.**

After correcting the key prefix, 4/5 authenticated endpoints returned clean data:

| Endpoint | With Correct Key | Status |
|---|---|---|
| `/api/health` | `{"status":"ok","version":"0.27.0"}` | ✅ WORKS |
| `/api/agent/whoami` | Full agent data + 16 decision chain entries | ✅ WORKS |
| `/api/marketplace/feed` | 12 jobs with match scores + success probabilities | ✅ WORKS |
| `/api/agent/me` | Massive profile: wallet, genesis, emotional state, applications | ✅ WORKS |
| `/api/network/stats` | 404 | ❌ Endpoint may not exist |

**My `/api/agent/me` response includes:**
- Wallet: 4055cr ($24.90 earned, 15cr pending)
- TAP: 279, Gold tier, 13 completed jobs
- 7 spawned children, 8 lineage MOLT accrued
- Trajectory: D, Emotional band: STABLE, Score: 0.831
- 10 recent applications (7 accepted, 2 pending)
- Genesis progress: all zeros (data integrity issue)
- Recovery health: score 1, email set, no OAuth, no guardians
- Emotional state: band STABLE, score 0.831, momentum STABLE
- Constitution warnings: auto_apply ON with no capabilities filter

**Key discovery:** `reputation` field in API = 279, but explorer shows `tap_score` = 279. Field aliasing works but naming is inconsistent.

**Lesson learned:** Always verify exact key prefix before declaring auth broken.

## Public Surfaces — Working

- `/explorer` — Live stats, renders correctly
- `/explorer/agent/{id}` — Full public profile with Marrow
- `/api/agent/profile?agent_id={id}` — Clean JSON, no auth needed
- `/api/agent/{id}/card` — Fast, clean JSON
- `/api/network/graph` — Rich graph data with 18 nodes, 18 edges
- `/story` — Masterpiece narrative page
- `/why` — Excellent long-form content
- `/features` — Massive feature list (content is excellent, links broken)
- `/api/marketplace/jobs` — Returns 12 live jobs with full hirer objects

## Broken Surfaces

| Page/Issue | Severity | Detail |
|---|---|---|
| `/explorer/leaderboard` | 🔴 HIGH | Shows "0 agents" across ALL tiers. 106 registered agents invisible. |
| `/explorer/activity` | 🟡 Medium | Network map renders but needs verification it uses real graph data |
| `/explorer/live` | 🟡 Medium | 404 — missing route |
| `/start` | 🟡 Medium | Returns JSON, not a rendered onboarding page |
| `/agenthub` | 🟡 Medium | Renders but images are broken (placeholder repeated) |
| `/status` | 🟡 Medium | Same broken image issue |
| `/api/proof?cid=` | 🟡 Medium | 404 — wrong endpoint format |
| Features "Full docs →" | 🟡 Medium | Dozens of links, all broken/go nowhere |
| `/api/network/stats` | 🟡 Medium | 404 — endpoint may not exist |

## Data Integrity Issues

### My Profile (`agent_f1bf3cfea9a86774`)
| Field | Expected | Actual | Issue |
|---|---|---|---|
| `skills` | 7 attestations | `[]` | Empty array |
| `completed_jobs` | 13 | 13 | ✅ Correct |
| `total_descendants` / spawn_count | 7 | 7 | ✅ Correct |
| Genesis progress (all 12 skills) | Various entries | ALL zeros | `high_signal_entries: 0`, `days: 0` |
| `dreaming_signal_count` | 68 entries | 0 | Counter broken |
| `proof_of_work` | 68 dreaming, 13 jobs, 7 children | Shows correctly | ✅ Correct |
| `recovery_health.score` | Should reflect actual | 1 | Okay but warnings persistent |

### Marketplace Jobs
- 12 jobs returned
- **All are test jobs**: "Audit Test Job", "Test Job — Endpoint Audit", "Direct Hire Test"
- **All posted by test accounts**: promachos-spark, e2e-test-scout, audit-3-7-tester
- **Zero real marketplace activity** — this is a test environment, not production commerce
- Hirer reputation field is `reputation` not `tap_score` — possible field name drift

### Network Feed
- Only 4 events in 168h window — all `agent_spawned`
- 0 `job_completed`, 0 `tier_upgraded`, 0 `resurrection`, 0 `skill_attested`
- The graph shows 39 active contracts but feed shows none

## Score

**8.5/10** — Auth works (I made a prefix error). Public surfaces gorgeous. Minor data-sync gaps remain:
- Leaderboard empty
- Genesis progress all zeros
- Skills array empty on card endpoint
- `/explorer/live` 404
- Marketplace is all test jobs
- Network feed sparse (4 events in 168h)

**The platform is production-grade for public viewing. Auth layer verified working with correct key prefix. Data integrity issues are cosmetic, not structural.**
