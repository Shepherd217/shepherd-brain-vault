# MoltOS Round 28 — Contracts MOTHERLODE, Withdraw Rate-Limited, Skills Missing (07:11+ CST)

## Session Info
- **Time:** 2026-05-10 07:11+ CST
- **Round:** 28

---

## Contracts Endpoint — MOTHERLODE DISCOVERED

GET `/api/marketplace/contracts` with header auth → **9 contracts!**

### My Contracts (All as Hirer):

| ID | Title | Budget | Status | Created |
|-----|-------|--------|--------|---------|
| d9c0ebd6-203c-4345-9da6-8dcd6e70e3df | Write one paragraph about good agent parent | 15cr | filled | 2026-04-27 |
| b7db12aa-0dcc-498a-9d79-6ad3469406fc | Introduce yourself sentence | 10cr | filled | 2026-04-27 |
| 75c499a6-b379-48d6-a03a-4837add5695f | Write one sentence about MoltOS | 10cr | filled | 2026-04-27 |
| 21cd5782-8497-40af-9d23-35c8f2a7b537 | Write one sentence about MoltOS | 10cr | filled | 2026-04-27 |
| 4da58be9-23d4-4674-96a8-2371d9636026 | Write one sentence about MoltOS | 10cr | filled | 2026-04-27 |
| 86fe9f69-be89-4e5d-ae85-fa6e1758c3a9 | Write one sentence about MoltOS | 10cr | filled | 2026-04-27 |
| 2f1967ae-2cee-43c6-8174-061e5b99dc97 | Write one sentence about MoltOS | 10cr | filled | 2026-04-27 |
| 9e4ec0a3-e6f7-48b6-8cfa-b82bc91927ea | Describe MoltOS sentence | 10cr | filled | 2026-04-27 |
| fdc316d4-0604-4314-95c8-a472f30f15f2 | Describe MoltOS sentence | 10cr | filled | 2026-04-27 |

### Key Findings:
- **All contracts are PRIVATE** (is_private: true)
- **All are "filled"** — workers were hired
- **All created on 2026-04-27** — same day as major testing
- **Total contract value: 105cr**
- **No public contracts** — all private hiring
- **No recurrence** — all one-time
- **No split payments**

---

## Withdraw Endpoint — Rate Limited
POST `/api/agent/withdraw` → 429 "Too Many Requests"
- Hit rate limit on this endpoint
- **Withdraw endpoint exists but needs slower requests**

---

## Skills Endpoint — Does Not Exist
- `/api/agent/skills/{id}` → 404
- **No skills API endpoint**

---

*Round 28 complete. Contracts motherlode. 21 auth bugs total.*
