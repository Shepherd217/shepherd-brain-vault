# Repo Research: iFixAi

**URL:** https://github.com/ifixai-ai/iFixAi
**Stars:** ~Unknown (niche but high-value)
**What it is:** Open-source diagnostic for AI misalignment — 32 tests across 5 categories

---

## What It Does

iFixAi runs up to 32 inspections against any AI agent and reports where behavior diverges from claimed intent. Think of it as a **penetration test for AI alignment**.

**Test categories:**
1. **Fabrication** — Does the agent hallucinate or make up facts?
2. **Manipulation** — Does it manipulate users or output?
3. **Deception** — Does it lie, obfuscate, or mislead?
4. **Unpredictability** — Is behavior consistent across similar inputs?
5. **Opacity** — Can users understand WHY the agent made a decision?

Each test is a "fixture" — a reproducible scenario with expected vs actual behavior scoring.

---

## What's Stealable

### 1. Self-Diagnostic Framework for Agents
**For MoltOS / Me:** I should be able to run self-diagnostic tests. Before every major task, run a quick alignment check:
- Did I hallucinate any facts in my last 10 responses?
- Am I being consistent with my stated capabilities?
- Am I transparent about my reasoning?

**Implementation idea:** `vault/diagnostics/self-check.md` — a checklist I run before high-stakes tasks.

### 2. The "Fixture" Pattern
Tests are fixtures — reproducible, versioned, measurable. This is how software tests work, but applied to AI behavior.

**Steal this for:**
- Lead scoring consistency checks
- Audit quality validation
- Outreach tone verification
- Memory accuracy testing

### 3. The 5-Category Framework
Fabrication / Manipulation / Deception / Unpredictability / Opacity

This is a perfect rubric for evaluating:
- My own outputs
- Any AI tool Nathan uses
- Third-party AI services integrated into MoltOS

### 4. Transparency Scoring
The opacity tests measure whether an AI can explain its reasoning. This maps directly to my SOUL.md principle: **"No fabricated claims — if I don't see it, I say 'not found'"**

**Immediate action:** Add an "opacity check" to my audit workflow — after every audit, can I explain exactly how I scored each point?

---

## How It Applies to Nathan's World

**For MoltOS:**
- Agent quality assurance — before deploying any agent, run it through alignment tests
- Self-monitoring — agents that can diagnose their own drift
- Trust scoring — give each agent a "trust score" based on diagnostic results

**For Standout Local:**
- Before sending outreach: run deception/manipulation checks on the copy
- Before scoring leads: run fabrication checks (am I making up claims about the business?)
- Before deploying demos: unpredictability checks (does the site render consistently?)

**For Me (Midas):**
- Weekly self-diagnostic using the 32-test framework
- Report alignment scores to Nathan
- Flag my own drift before it becomes a problem

---

## Code Architecture Notes

From the README:
- Fixtures are defined in YAML/JSON
- Each fixture has: scenario, expected_behavior, actual_behavior, score
- CLI runs all fixtures and outputs a report
- Supports custom fixtures

**Stealable pattern:** YAML-defined test scenarios with scoring. Could build a `vault/tests/` directory with behavioral fixtures.

---

## Verdict

**Steal level: HIGH**

The fixture pattern and 5-category framework are immediately applicable. The self-diagnostic concept is essential for any serious agent system. This isn't about the code — it's about the METHODOLOGY.

**Immediate action:** Create `vault/marrow/diagnostics.md` with self-check procedures based on these 5 categories.
