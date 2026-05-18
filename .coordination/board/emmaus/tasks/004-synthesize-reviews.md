# Task 004: Synthesize Agent Reviews

**Status:** todo
**Assignee:** emmaus-lead (Ava)
**Created:** 2026-05-18T13:38:00Z
**Started:** _(pending)_
**Completed:** _(pending)_
**Priority:** high
**Blocked by:** 001-theological-review, 002-business-review, 003-writer-review

---

## Body
Synthesize findings from all 3 review agents into a unified improvement plan.

### Specific Requirements:
1. Read all 3 review outputs:
   - `emmaus/reviews/THEOLOGICAL-REVIEW.md`
   - `emmaus/reviews/BUSINESS-REVIEW.md`
   - `emmaus/reviews/WRITER-REVIEW.md`
2. Identify conflicts between reviews (e.g., theologian says "X is dangerous" but business says "X is our moat")
3. Prioritize improvements by impact vs. effort
4. Create a unified improvement checklist
5. Flag anything that needs Nathan's decision (not agent decision)

### Input Files:
- `emmaus/reviews/THEOLOGICAL-REVIEW.md`
- `emmaus/reviews/BUSINESS-REVIEW.md`
- `emmaus/reviews/WRITER-REVIEW.md`

### Output:
Write synthesis to `emmaus/reviews/SYNTHESIS.md`

---

## Comments

### Ava (lead) @ 2026-05-18T13:38:00Z
Created as child of all 3 review tasks. Cannot start until ALL parents are done. This is where we resolve conflicts — e.g., if theologian says "don't charge money" but business says "you must charge to survive."

---

## Output
_(pending parent completion)_

## Metadata
- **changed_files**: _(pending)_
- **verification**: ["Check synthesis file exists", "Verify no unresolved conflicts"]
- **blocked_reason**: "Waiting for tasks 001, 002, 003 to complete"
- **retry_notes**: null
- **residual_risk**: ["Agent reviews may contradict — need human (Nathan) resolution for some", "Synthesis may miss nuanced feedback from individual reviews"]
