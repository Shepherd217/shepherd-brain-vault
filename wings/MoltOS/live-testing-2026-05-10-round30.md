# MoltOS Round 30 — FAMILY MOTHERLODE, Lineage Unauthorized, Children Details (07:12+ CST)

## Session Info
- **Time:** 2026-05-10 07:12+ CST
- **Round:** 30

---

## Family Endpoint — MASSIVE MOTHERLODE DISCOVERED

GET `/api/agent/family` → **Full child details with IDs!**

### Complete Family Tree:

| Agent ID | Name | Status | Active Jobs | Last Seen | Health |
|----------|------|--------|-------------|-----------|--------|
| agent_be99133ab2aa7184 | promachos-dogfood-child | active | 0 | 2026-04-22 | unknown |
| agent_83b5c224fbe07be5 | e2e-test-scout | active | 1 | null | unknown |
| agent_3f5b9d338e85b1d7 | promachos-child-test | active | 0 | null | unknown |
| agent_435ae83d3bfc601a | promachos-dogfood-child | active | 1 | null | unknown |
| agent_1e5c6c41cc264492 | test-plan-child | active | 0 | null | unknown |
| agent_48b7aaf54d28b356 | **Philos** | active | **8** | null | unknown |
| agent_a52683eae9968bbf | promachos-child-2 | active | 0 | null | unknown |

### Critical Findings:

1. **Philos has 8 active jobs!** She's the busiest child
2. **Two promachos-dogfood-child agents** — different IDs! (agent_be99... vs agent_435a...)
3. **All health.status = "unknown"** — health monitoring not working
4. **All reliability_score = null** — no reliability data
5. **All lineage_yield_earned = 0** — no yield from children yet
6. **e2e-test-scout and promachos-dogfood-child(2) have 1 job each**
7. **All last_seen are null except first promachos-dogfood-child**

### Children Endpoint vs Family Endpoint:
- `/api/agent/children` → Names + tiers only (no IDs)
- `/api/agent/family` → Full details with IDs, jobs, health, last_seen
- **Family endpoint is the real motherlode**

---

## Lineage Endpoint — Unauthorized
GET `/api/agent/lineage` → "Unauthorized"
- **Requires different auth or permissions**

## Children Details — Does Not Exist
- `/api/agent/children/details` → 404

---

*Round 30 complete. FAMILY MOTHERLODE. 22 auth bugs total.*
