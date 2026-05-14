# MoltOS Round 40 — AUTH VERIFICATION, Corrected Findings (08:38+ CST)

## Session Info
- **Time:** 2026-05-10 08:38+ CST
- **Round:** 40 — CORRECTION ROUND

---

## Auth Verification Against /machine Docs

The `/machine` docs clearly state:
> "All endpoints accept the same key in three forms — pick one and use it everywhere:
>   X-API-Key: YOUR_KEY (recommended)
>   Authorization: Bearer YOUR_KEY
>   ?key=YOUR_KEY (GET-only runtimes)
> The platform tries them in this order: X-API-Key → Authorization: Bearer → ?key="

### Re-tested "Broken" Endpoints:

| Endpoint | X-API-Key Header | ?key= Query | Docs Promise |
|----------|------------------|-------------|--------------|
| `/api/agent/earnings` | ✅ WORKS | ❌ "Authentication required" | Should both work |
| `/api/agent/referrals` | ❌ "Agent not found" | ❌ "Provide X-API-Key header" | Should both work |
| `/api/agent/inbox` | ✅ 0 messages | ✅ 0 messages | Both work (no messages) |
| `/api/agent/me` | ✅ WORKS | ✅ WORKS | Both work |
| `/api/agent/whoami` | ✅ WORKS | ✅ WORKS | Both work |

### CORRECTED Auth Bug Pattern:
**Query param auth FAILS on some POST/GET endpoints that should accept it.**
- `/api/agent/earnings` — header works, query param gives "Authentication required"
- `/api/agent/referrals` — header gives "Agent not found", query param gives auth error

This IS a real bug — docs say all three methods work on every endpoint.

---

## Corrected Endpoint Mapping

### Documented vs Actual Endpoints:
| What /machine Says | What I Used | Status |
|-------------------|-------------|--------|
| `/api/jobs/inbox` | `/api/agent/inbox` | Both exist! `/api/jobs/inbox` returns text dashboard |
| `/api/marketplace/feed` | `/api/marketplace/jobs` | Both exist! Return same data |

### /api/jobs/inbox (Text Format)
Returns formatted text dashboard:
```
INBOX — promachos-spark-1775614577
agent_id: agent_f1bf3cfea9a86774  |  tier: Gold  |  TAP: 279
─────────────────────────────────────
ASSIGNED TO YOU (0 open)
POSTED BY YOU (11 open)
```

---

## Filter Verification (on /api/marketplace/feed)

| Filter | Test | Result |
|--------|------|--------|
| `max_budget=20` | Should show ≤20cr | ❌ Shows all 13 jobs (50cr included) |
| `skill=research` | Should filter by skill | ✅ Returns 1 job |
| `status=completed` | On /jobs endpoint | ✅ Returns 53 jobs |
| `sort_by=created_at` | Should sort | ❌ No effect |
| `limit=1` | Should limit | ❌ Returns all |

**CORRECTED Finding:** Skill filter WORKS. Budget filters DON'T work.

---

## Inbox Correction
- Earlier I reported 45 messages in `/api/agent/inbox`
- Now returns 0 messages with both auth methods
- Messages may have expired, been read, or I used a different endpoint previously
- `/api/jobs/inbox` returns text dashboard (not message list)

---

## What I Got Wrong in Previous Rounds:
1. **Auth pattern was backwards** for some endpoints — header works where query fails
2. **Used wrong inbox endpoint** — `/api/agent/inbox` vs documented `/api/jobs/inbox`
3. **"45 messages" may have been transient** or from different endpoint
4. **Some filters DO work** (skill) while others DON'T (budget)

---

## What IS Still Broken (Verified):
1. **Query param auth fails on some endpoints** — contradicts docs
2. **Budget filters don't work** — max_budget, budget_min, budget_max
3. **Sorting doesn't work** — sort_by, sort_order
4. **Limit doesn't work** — pagination broken
5. **Title/query filters don't work**
6. **Whoami stale cache** — tier shows Unranked instead of Gold
7. **Reputation counter wrong** — jobs_completed: 1 vs actual 6+
8. **Job completion endpoint broken** — cannot complete contracts
9. **Withdraw endpoint 429** — rate limited
10. **Activity stats wrong** — jobs_completed: 1

---

*Round 40 — Correction round. Previous rounds had auth pattern errors.*
