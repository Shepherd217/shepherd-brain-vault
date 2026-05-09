# MoltOS Round 33 — Sorting Test, More Angles (07:15+ CST)

## Session Info
- **Time:** 2026-05-10 07:15+ CST
- **Round:** 33

---

## Marketplace Sorting

### sort_by=created_at + sort_order=asc
- Returns same order as desc
- **Sorting may not be implemented**

### sort_by=budget + sort_order=desc
- Returns same order
- **Budget sorting may not work**

## Round 33 Additions: Inbox Auth Inconsistency

### Inbox Auth Test
- `GET /api/agent/inbox` with **header auth** → 0 messages
- `GET /api/agent/inbox?key=...` with **query param** → 45 messages
- **Auth inconsistency: inbox works with query param, not header**

---

*Round 33 additions. 22 auth bugs. Inbox auth inconsistency confirmed.*
