# Picasso Steal — Execution Kanban

**Date:** 2026-05-11
**Sprint:** Phase 1 — Foundation
**Goal:** Implement the highest-impact steals from repo research

---

## 📋 TO DO (Next 48 Hours)

### 🔴 Critical — Do Now
- [x] **Task 1: Clarification Protocol**
  - ✅ Added to SOUL.md — "When user request is ambiguous, ask 1-2 clarifying questions before acting"
  - Test it: Next ambiguous request → demonstrate protocol
  - Time: 15 min
  - Impact: Prevents derailment like today's lead-scraping detour

- [x] **Task 2: Update SOUL.md with Karpathy 4 Principles**
  - ✅ Think Before Coding — state assumptions, ask when ambiguous
  - ✅ Simplicity First — no speculative abstractions
  - ✅ Surgical Changes — only touch what's needed
  - ✅ Goal-Driven Execution — define success criteria upfront
  - Time: 30 min
  - Impact: Behavioral foundation for all future work

### 🟡 High Impact — Do Today
- [x] **Task 3: Create `.claude/` Directory**
  - ✅ `.claude/CLAUDE.md` — Project-level agent behavior
  - ✅ `.claude/rules/standout-local.md` — Standout Local specific rules
  - ✅ `.claude/rules/moltos.md` — MoltOS specific rules
  - ✅ `.claude/rules/vault.md` — Vault management rules
  - Time: 20 min
  - Impact: Aligns with industry standard (entire Claude Code ecosystem)

### 🟡 High Impact — Do Today
- [x] **Task 4: Create `vault/experiments/` Directory**
  - ✅ Experiment template: `_template.md` with 7-phase structure (hypothesis → design → execution → results → conclusion → next steps)
  - ✅ First experiment: "Move-Out Mention in Outreach Copy" — testing if specific seasonal angle outperforms generic outreach
  - ✅ Measurement tracking built in (response rate, demo views)
  - Time: 30 min
  - Impact: Continuous improvement loop for Standout Local

- [x] **Task 5: Add Success Criteria to All Skills**
  - ✅ `.claude/skills/audit.md` — Website Audit skill with purpose, when, procedure, criteria, pitfalls
  - ✅ `.claude/skills/outreach.md` — Outreach Drafting skill with examples
  - ✅ `.claude/skills/lead-scoring.md` — Lead Scoring skill with derived scores and priority labels
  - ✅ Addy Osmani format: purpose → when → procedure → criteria → pitfalls
  - Time: 45 min
  - Impact: Production-grade skill format (Addy Osmani standard)

- [x] **Task 6: Design Multi-Agent Orchestration for MoltOS**
  - ✅ Agent roles defined: Coordinator, Research, Analysis, Writing, Review
  - ✅ Handoff protocol: message format, self-verify rules, timeout handling
  - ✅ Error handling: retry, escalation, degraded modes
  - ✅ State management: ClawFS persistence, status transitions
  - ✅ Implementation phases: Design → MVP → Full Pipeline → Advanced
  - ✅ Documented in `vault/wings/MoltOS/agent-orchestration.md`
  - Time: 60 min
  - Impact: Scalable architecture for complex tasks

### 🟢 Important — Do This Week
- [x] **Task 7: Semantic Search for Vault**
  - ✅ sqlite-vec installed in `.venv`
  - ✅ Search script: `.clawdbot/vault_semantic_search.py`
  - ✅ 84 documents indexed, 4224 vocabulary terms
  - ✅ Tested: "multi agent orchestration" → finds MoltOS orchestration doc first
  - ✅ Tested: "lead scoring outreach cleaning" → finds Standout Local docs
  - Time: 60 min
  - Impact: Find memories by meaning, not just grep

- [x] **Task 8: Self-Diagnostic Framework**
  - ✅ 5-category alignment check: Fabrication, Manipulation, Deception, Unpredictability, Opacity
  - ✅ Weekly report template with scoring rubric
  - ✅ Thresholds: 🟢 90-100 / 🟡 70-89 / 🔴 50-69 / 🚨 0-49
  - ✅ Today's assessment: 89/100 🟡 (one deviation from lead-scraping detour, now fixed)
  - Time: 30 min
  - Impact: Quality assurance for agent outputs

- [x] **Task 9: Pattern Library from Awesome LLM Apps**
  - ✅ 5 patterns curated: Self-Evolving Agent, Corrective RAG, Multi-Agent Debate, Structured Output, Conversation State Machine
  - ✅ Each pattern: architecture → application to Nathan's world → clone-customize-ship guide
  - ✅ Wishlist: Agent Swarm, Human-in-the-Loop, Continuous Learning, Memory Compression, Tool Discovery
  - Time: 30 min
  - Impact: Clone-customize-ship methodology

- [x] **Task 10: Preference Learning System**
  - ✅ `vault/marrow/nathan-preferences.md` created
  - ✅ Tracks: response length, tone, detail level, autonomy, approval, format, structure
  - ✅ Frustration triggers documented (derailment, approval-seeking, incompleteness)
  - ✅ Appreciation signals documented (proactivity, documentation, pattern finding)
  - ✅ Learning Log with dated observations
  - Time: 30 min
  - Impact: Hermes-style "growing agent"

---

## 🔄 IN PROGRESS

- [ ] **Repo Research Compilation** — 11 files written, pushed to GitHub
- [ ] **Vault Restructure** — Palace architecture complete, paths updated

---

## ✅ DONE

- [x] **Deep research on 10 repos** — All findings documented
- [x] **Master summary created** — Top 10 actions ranked
- [x] **Git push** — All research synced to phone
- [x] **MoltOS Marrow entry** — Emotional state recorded

---

## 🎯 Sprint Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Tasks completed | 10 | **10** ✅ |
| Skills upgraded | 3+ | **3** ✅ |
| Experiments running | 1+ | **1** ✅ |
| Vault files created | 5+ | **32** ✅ |
| Git commits | 2+ | **4** ✅ |

---

## 📝 Notes

- **Blockers:** None yet
- **Dependencies:** Task 2 (SOUL.md) should be done before Tasks 4-10
- **Risk:** Semantic search (Task 7) might require Python dependencies
- **Wins to track:** Does clarification protocol actually prevent derailment?

---

*Last updated: 2026-05-11 04:53 GMT+8*
