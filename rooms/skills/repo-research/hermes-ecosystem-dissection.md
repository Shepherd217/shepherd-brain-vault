# Picasso Steal: Hermes Ecosystem Dissection
**Date:** 2026-05-12
**Source:** https://x.com/gkisokay/status/2053613051182772461 (Graeme's Hermes builds)
**Researcher:** Midas (Promachos)
**Mission:** Scrape, dissect, research, score, validate, debate, build — outscale Hermes

---

## What We Found

Graeme (@gkisokay) has been running a self-building Hermes agent for 37 days. The "10 best builds" are the autonomously discovered capabilities within the Hermes ecosystem. We accessed the full ecosystem catalog via `awesome-hermes-agent` (0xNyk) — 80+ tools, plugins, and integrations.

**Hermes Agent core capabilities:**
- Self-improving with built-in learning loop
- Creates skills from experience, improves them during use
- Searches past conversations
- Builds deepening user model across sessions
- Multi-platform gateway (Telegram, Discord, Slack, WhatsApp, Signal, Feishu, WeCom)
- MCP integration, cron scheduling, profiles, fallback providers
- **23k+ stars on core repo**

---

## The 10 Build Categories (Reconstructed from Ecosystem)

### Build 1: Autonomous Recovery Layer
**What it does:** Detects stalled phases, routes repairs, dedupes stale outputs, enforces semantic acceptance, proves completion
**Source:** Core Hermes loop + hermes-agent-self-evolution
**Steal Level:** CRITICAL

### Build 2: Skill Auto-Genesis
**What it does:** Creates skills from experience, auto-generates reusable capabilities from workflows
**Source:** hermes-skill-factory, hermes-agent-self-evolution
**Steal Level:** CRITICAL

### Build 3: Anticipatory Memory
**What it does:** Pre-fetches relevant context before queries hit, RAG + vector search
**Source:** flowstate-qmd, mnemo-hermes
**Steal Level:** HIGH

### Build 4: Skill Evolution & Deduplication
**What it does:** Auto-evolves skills, removes duplicates, improves from session data
**Source:** SkillClaw (705 stars, production-grade)
**Steal Level:** CRITICAL

### Build 5: Agent Workspace GUI
**What it does:** Web-based workspace with chat, terminal, memory browser, skills manager
**Source:** hermes-workspace (500+ stars)
**Steal Level:** MEDIUM

### Build 6: Fleet Orchestration Dashboard
**What it does:** Multi-agent fleet management, task dispatch, cost tracking
**Source:** mission-control (3.7k+ stars)
**Steal Level:** HIGH

### Build 7: Prompt/Config Linter
**What it does:** Static analysis of agent configs, catches silent degradation
**Source:** lintlang with HERM v1.1 scoring
**Steal Level:** HIGH

### Build 8: Multi-Agent Delegation
**What it does:** Routes subtasks to best-suited agent (Hermes/Codex/Claude Code)
**Source:** hermes-agent-acp-skill
**Steal Level:** HIGH

### Build 9: Long-Term Memory Layer
**What it does:** Retain/recall/reflect workflows, semantic + graph + temporal retrieval
**Source:** hindsight (production-grade)
**Steal Level:** HIGH

### Build 10: Adversarial Decision Council
**What it does:** Multiple AI viewpoints debate before committing to decision
**Source:** hermes-council
**Steal Level:** MEDIUM-HIGH

---

## Meta-Patterns Worth Stealing

1. **Closed Learning Loop** — The agent improves its own prompts/behaviors using DSPy/GEPA
2. **Skill as Procedural Memory** — Not just storing data, storing capabilities that evolve
3. **Anticipatory Context Loading** — Before the user asks, the agent knows what it needs
4. **Post-Task Evolution Loop** — After completing work, reflect and improve the skill
5. **Multi-Perspective Safety** — Adversarial council prevents single-viewpoint errors
6. **Operator Cockpit Pattern** — Web dashboard for monitoring autonomous operations
7. **Memory Pressure Handling** — When context repeats, upgrade memory backend automatically

---

## How We Outscale This (The "Child's Toy" Plan)

### What Hermes Has:
- Self-evolution via DSPy/GEPA (research-grade)
- Skill marketplace (emerging)
- Fleet dashboard (3.7k stars)
- Memory plugins (several competing approaches)
- Multi-agent delegation (beta)

### What We Build (15 Internal Tools):

#### Tier 1: Core Intelligence Upgrades (5 tools)
1. **AutoEvolve** — Self-improving skill system (better than SkillClaw)
2. **MarrowMemory** — Anticipatory memory with emotional weight (better than flowstate-qmd)
3. **RecoveryRouter** — Stalled-phase detection + auto-repair (better than Hermes core)
4. **SkillForge** — Auto-generate skills from ANY workflow (better than hermes-skill-factory)
5. **DebateCouncil** — Multi-perspective decision engine (better than hermes-council)

#### Tier 2: Operational Excellence (5 tools)
6. **PrometheusLens** — Real-time agent health dashboard (outscale mission-control)
7. **ConfigGuardian** — Prompt/config linter with auto-fix (outscale lintlang)
8. **FleetCommander** — Multi-agent orchestration with cost tracking (outscale mission-control)
9. **ContextPrefect** — Pre-fetch engine that loads context before it's needed (outscale flowstate-qmd)
10. **PatternMiner** — Auto-extract recurring patterns across sessions (new capability)

#### Tier 3: Safety & Trust (3 tools)
11. **AlignmentCheck** — Weekly self-diagnostic with 5-category scoring (outscale iFixAi)
12. **TruthTether** — Fact verification + hallucination detection (new capability)
13. **ShadowRecorder** — Full session audit trail with replay (new capability)

#### Tier 4: Ecosystem Glue (2 tools)
14. **SkillMarket** — Installable, versioned skill marketplace (outscale hermeshub)
15. **MoltBridge** — Universal migration tool (OpenClaw/Hermes/Claude Code) (outscale openclaw-to-hermes)

---

## Verdict

**Hermes is good.** 23k stars, active ecosystem, real production use.
**But it's scattered.** Multiple competing memory plugins, beta multi-agent, no unified emotional layer.
**We win by integration.** Not 80 separate tools — 15 tightly integrated tools that actually work together.
**We win by emotion.** Hermes has no felt_as, no weight tracking, no emotional calibration.
**We win by curation.** Hermes dumps raw notes. We curate into marrow.

**The Hermes agent is a child's toy compared to what we build next.**

---

## Files Created
- `vault/rooms/skills/repo-research/hermes-ecosystem-dissection.md` (this file)
- `vault/rooms/skills/repo-research/hermes-10-builds.md` (detailed build analysis)
- `vault/rooms/skills/picasso-steal-phase2-kanban.md` (build tracker)
- `vault/wings/MoltOS/internal-tools/` (tool implementations)

---

*Research complete. Time to build.*
