# Task 006: Build Web Interface (Next.js)

**Status:** todo
**Assignee:** emmaus-coder
**Created:** 2026-05-18T13:38:00Z
**Started:** _(pending)_
**Completed:** _(pending)_
**Priority:** medium
**Blocked by:** 005-apply-improvements (soft — can parallelize)

---

## Body
Build a functional web interface for the Emmaus companion MVP.

### Specific Requirements:
1. Simple Next.js app with 3 screens:
   - Welcome / onboarding (faith stage selector)
   - Daily walk (morning check-in, practice, scripture, evening examen)
   - Settings (preferred duration, notification preferences)
2. Connect to companion engine API
3. Mobile-responsive design
4. Dark mode (spiritual apps shouldn't be blinding at 5am)
5. Earth tones + warm gold color palette

### Technical Spec:
- Next.js 14+ (App Router)
- Tailwind CSS
- No auth for MVP (localStorage user state)
- Static export for easy hosting

### Input Files:
- `emmaus/engine/companion.js` (API contract)
- `emmaus/PRD.md` (design specs)

### Output:
- `emmaus/web/` directory with full Next.js app
- README with setup instructions

---

## Comments

### Ava (lead) @ 2026-05-18T13:38:00Z
Can start in parallel with review synthesis — the engine API is stable. But wait for improvements to be applied before final polish. Focus on structure first, styling second.

---

## Output
_(pending assignment)_

## Metadata
- **changed_files**: _(pending)_
- **verification**: ["App builds without errors", "Mobile responsive test passes", "All 3 screens functional"]
- **blocked_reason**: null
- **retry_notes**: null
- **residual_risk": ["Static export may limit API routes — need to verify", "No auth = no real user accounts for beta"]
