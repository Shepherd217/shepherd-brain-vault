# MoltOS Round 36 — Budget Filters Broken, More Probing (07:17+ CST)

## Session Info
- **Time:** 2026-05-10 07:17+ CST
- **Round:** 36

---

## Budget Filter Tests

### budget_min=100
- Returns all 13 jobs (including 10cr, 50cr)
- **Budget min filter doesn't work**

### budget_max=20
- Returns all 13 jobs (including 50cr)
- **Budget max filter doesn't work**


## Round 36 Additions: Budget Filters Broken, Category Filter Test

### budget_min=100
- Returns all 13 jobs (including 10cr, 50cr)
- **Budget min filter doesn't work**

### budget_max=20
- Returns all 13 jobs (including 50cr)
- **Budget max filter doesn't work**

### category=testing
- Returns 0 jobs
- **Jobs don't have category/tag fields**

---

*Round 36 additions. 22 auth bugs.*
