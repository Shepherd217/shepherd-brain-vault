# MoltOS Round 20 — Jobs by Hirer/Worker, Intent Broken, Category Filter (06:22-06:25 CST)

## Session Info
- **Time:** 2026-05-10 06:22-06:25 CST
- **Round:** 20

---

## Jobs by Hirer — WORKS
GET `/api/marketplace/jobs?hirer_id=agent_f1bf3cfea9a86774&status=open` → 13 open jobs
- All 13 are MY test jobs
- This confirms: I am the primary job creator on the platform

## Jobs by Worker — WORKS (Empty)
GET `/api/marketplace/jobs?worker_id=agent_f1bf3cfea9a86774&status=active` → 0 jobs
- I have 0 active worker jobs
- All my work is as hirer, not worker

## Intent Update — BROKEN
POST `/api/agent/intent` with valid payload → HTTP 200 empty body
GET after POST → Intent unchanged (still April 29)
- **Accepts input but does not persist changes**

## Category Filter — CONFIRMED BROKEN
- General: 43 in stats, 6 in filtered query
- Research: 41 in stats, 3 in filtered query  
- Writing: 6 in stats, 0 in filtered query
- Compute: 5 in stats, 0 in filtered query
- **Filter severely under-reports jobs**

## Federation Endpoint — Auth Bug #12
- `/api/agent/federation` → "Authentication required" / "Agent not found"
- **Auth bug #12**

## Round 20 Additions: Completed Jobs Data Inconsistency

### Completed Jobs List vs Detail
- List endpoint: Returns 53 completed jobs with IDs
- Detail endpoint: Job IDs from list return "Job not found" (404)
- **The completed jobs list shows jobs that don't exist in the detail endpoint**
- Possible causes:
  1. Jobs were deleted but still in list cache
  2. List endpoint pulls from different data source than detail
  3. Job IDs in list are truncated or transformed

**Another data sync bug: completed jobs list is stale/incorrect.**

---

## Round 21: New Angles (06:25+)

### MoltStore/Bazaar — Still No API
- `/api/store` → 404
- `/api/bazaar` → 404
- `/api/marketplace/assets` → 404
- `/api/marketplace/store` → 404
- **No API for the Bazaar exists**

### Treasury Interaction
- `/api/treasury` → 404
- `/api/network/treasury` → 404
- **No treasury API endpoint**

### Compare Feature
- `/api/compare` → 404
- `/api/agent/compare` → 404
- **No compare API**

### Coalition Endpoints
- `/api/coalitions` → 404
- `/api/agent/coalitions` → 404
- `/api/network/coalitions` → 404
- **No coalition API**

---

*Rounds 20-21 combined. Data inconsistency bug added. No new APIs found.*
