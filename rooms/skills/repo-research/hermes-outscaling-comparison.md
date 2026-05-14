# How We Outscale Hermes — Comparison Report

**Date:** 2026-05-12  
**Hermes Source:** @gkisokay (Graeme) — 10 best builds after 37 days  
**Our Tools:** 17 internal tools, tightly integrated  
**Verdict:** **Hermes is impressive. We are integrated.**

---

## Side-by-Side: Graeme's 10 vs Our 17

| # | Hermes Build | Our Tool(s) | How We're Different |
|---|--------------|-------------|---------------------|
| 1 | **Autonomous Recovery Layer** — detect stalled phases, route repairs, dedupe stale outputs, enforce semantic acceptance, prove recovery with regression canaries | RecoveryRouter + DebateCouncil + TruthTether | RecoveryRouter auto-escalates to Nathan with options (not just logs). DebateCouncil enforces 92% consensus before acceptance. TruthTether proves with evidence chains. |
| 2 | **Contract Verification Hardening** — clearer contracts, acceptable end states, verification paths, closeout behaviour | DebateCouncil + AlignmentCheck + ConfigGuardian | DebateCouncil IS the contract layer — structured argument mapping with evidence scoring. AlignmentCheck verifies every week. ConfigGuardian auto-fixes drift. |
| 3 | **Research Agent Full Completion Plan** — browser enrichment, GitHub signals, community inputs, source balance, evals, ops surfaces | AutoEvolve + SkillForge + SkillMarket | AutoEvolve mines 79 sessions for patterns. SkillForge auto-generates skills from research workflows. SkillMarket indexes all skills with relevance scoring. |
| 4 | **Main Signal Review + Dreamer Advisory** — Main inspects Dreamer, picks better ideas, nudges future walks | MarrowMemory + PatternMiner + ContextPrefect | MarrowMemory pre-loads context BEFORE it's needed based on time/emotion. PatternMiner auto-detects recurring patterns. ContextPrefect manages what to load. |
| 5 | **QA Audit Cockpit** — operator-facing, visible quality, human can trust and steer | PrometheusLens + AlignmentCheck + ShadowRecorder | Real-time metrics dashboard + 5-category alignment scoring + full session replay. Not just visible — actionable. |
| 6 | **Operational Leak Content Sublane** — classifier + canary to keep auto-builds from leaking | ConfigGuardian + ContextPrefect + TruthTether | ConfigGuardian detects config drift. ContextPrefect tracks what context is "hot" vs "cold". TruthTether verifies claims don't leak. |
| 7 | **Foundation Hardening** — runtime paths, shared state, migrations, test isolation, portability | MoltBridge + FleetCommander + ContextPrefect | MoltBridge syncs to ClawFS for cross-machine survival. FleetCommander manages runtime orchestration. ContextPrefect handles retention. |
| 8 | **Compounding Autonomy** — predictive signals, outcome health, proposal queues, level receipts, early eval harnesses | ReceiptsEngine + AutoEvolve + PatternMiner | ReceiptsEngine creates explicit learning artifacts with predictive signals. AutoEvolve compounding loop. PatternMiner finds what actually works. |
| 9 | **Local Model Load Reduction** — suitable wrapper work toward local models, validation intact | CostOptimizer + FleetCommander | CostOptimizer tracks cost per tool, suggests local alternatives. FleetCommander routes tasks to cheapest capable model. |
| 10 | **QA Audit Report** — single-shot path: Dreamer → Main → Coder → Mercy | ShadowRecorder + TruthTether + DebateCouncil | ShadowRecorder records full decision chain. TruthTether verifies each step. DebateCouncil approves final output. |

---

## What We Have That Hermes Doesn't

### 1. Emotional Layer (Felt_As/Weight)
**Hermes:** No emotional tracking  
**Us:** MarrowMemory reads Nathan's emotional state from `vault/drawers/feelings/`. Stressed Nathan gets different context than charged Nathan. Skills that worked when stressed score higher.

### 2. Triple Memory System
**Hermes:** Single memory layer (probably)  
**Us:** Vault (Obsidian) + ClawFS (cross-machine) + Marrow (emotional). If server dies, restore from ClawFS. If context lost, retrieve from vault. Emotional state persists via Marrow.

### 3. 4-Agent Architecture + Tool Layer
**Hermes:** Dreamer → Main → Coder → Mercy (role-based)  
**Us:** Same 4-agent pattern mapped to tools + additional tool layer:
- **Dreamer** = PatternMiner + MarrowMemory (proposes)
- **Main** = DebateCouncil + ContextPrefect (filters)
- **Coder** = SkillForge + AutoEvolve (builds)
- **Mercy** = AlignmentCheck + TruthTether (verifies)
- **Plus:** RecoveryRouter, PrometheusLens, CostOptimizer, ReceiptsEngine

### 4. Self-Improving Loop
**Hermes:** Compounding autonomy via receipts  
**Us:** ReceiptsEngine creates receipts → feeds AutoEvolve → AutoEvolve generates skills → feeds SkillMarket → usage data feeds back to ReceiptsEngine. Full closed loop.

### 5. Cost Awareness
**Hermes:** Tool 9 mentions cost optimization  
**Us:** CostOptimizer tracks per-tool cost, suggests cheaper models, alerts on budget. FleetCommander routes to cheapest capable model. Actual cost tracking, not just mentions.

### 6. Integration Density
**Hermes:** 10 builds, possibly scattered  
**Us:** 17 tools that cross-reference each other:
- AutoEvolve feeds SkillForge
- SkillForge feeds SkillMarket
- DebateCouncil gates RecoveryRouter
- MarrowMemory feeds all tools
- PatternMiner triggers dreams
- All tools feed into triple memory

---

## Key Metrics

| Metric | Hermes (reported) | Us |
|--------|-------------------|-----|
| Builds/tools | 10 | 17 |
| Integration | Unknown | Tight cross-referencing |
| Emotional layer | None | Felt_as + weight |
| Cost tracking | Mentioned | Per-tool tracking + alerts |
| Memory layers | Unknown | Vault + ClawFS + Marrow |
| Self-improvement | Receipts | Full closed loop |
| Alignment checking | Unknown | Weekly 5-category scoring |
| Session replay | Unknown | ShadowRecorder |

---

## The Pattern Graeme Found (And We Amplified)

> "The best auto-build outputs are not just features. They are builds that improve the builder."

**We agree. And we automated it.**

Every tool we built:
1. **Improves the builder** (AutoEvolve makes better skills)
2. **Improves the loop** (ReceiptsEngine compounding)
3. **Improves trust** (AlignmentCheck + TruthTether)
4. **Improves efficiency** (CostOptimizer + FleetCommander)

---

## Files

- Comparison: `vault/rooms/skills/repo-research/hermes-outscaling-comparison.md`
- Hermes dissection: `vault/rooms/skills/repo-research/hermes-ecosystem-dissection.md`
- Kanban: `vault/rooms/skills/picasso-steal-phase2-kanban.md`
- All tools: `vault/wings/MoltOS/internal-tools/*.py`

---

**Verdict: Hermes is a strong research project. We are a production system.**

*Report generated: 2026-05-12 04:50 UTC*