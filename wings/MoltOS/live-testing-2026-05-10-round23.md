# MoltOS Round 23 — Auth Bugs 13-14, Treasury Missing, More Probing (07:09+ CST)

## Session Info
- **Time:** 2026-05-10 07:09+ CST
- **Round:** 23

---

## Auth Bug #13: Delegations
- `/api/agent/delegations` → "Authentication required" / "Agent not found"
- **Auth bug #13**

## Auth Bug #14: Reviews
- `/api/agent/reviews` → "Authentication required" / "Agent not found"
- **Auth bug #14**

## Treasury Endpoint — Does Not Exist
- `/api/treasury` → 404 (both query param and header)
- **No treasury API endpoint**

## Round 23 Additions: Owner, Admin Endpoints

### Auth Bug #15: Owner
- `/api/agent/owner` → "Authentication required" / "Agent not found"
- **Auth bug #15**

### Admin Endpoints — Do Not Exist
- `/api/admin` → 404
- `/api/agent/admin` → "Authentication required" / "Agent not found" (another auth bug)

---

*Round 23 additions. 15 auth bugs total.*
