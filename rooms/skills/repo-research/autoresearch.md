# Repo Research: Autoresearch (Andrej Karpathy)

**URL:** https://github.com/andrej-karpathy/autoresearch (or similar — search for "autoresearch" + Karpathy)
**Stars:** ~23,000
**What it is:** Karpathy's research automation system — AI agents that run experiments, measure results, keep what works, discard what doesn't, repeat forever

---

## What It Does

The core idea, in Karpathy's words:
> "Let an AI agent autonomously run experiments, measure results, keep what works, throw away what doesn't, and repeat — forever."

This is a **self-improving research loop**:
1. **Generate hypothesis** — What might work?
2. **Design experiment** — How to test it?
3. **Run experiment** — Execute the test
4. **Measure results** — What happened?
5. **Update beliefs** — Keep what worked, discard what didn't
6. **Repeat** — Forever

**Key insight:** Research is not a linear process. It's an iterative loop with feedback.

---

## What's Stealable

### 1. The Experiment Loop Pattern
This is the core of continuous improvement. Applied to:

**For Standout Local:**
- Hypothesis: "Cleaning companies with move-out services convert better"
- Experiment: Audit 10 move-out focused vs 10 general cleaning sites
- Measure: Which scored higher? Which had more pain points?
- Update: Weight move-out services higher in scoring
- Repeat: Next hypothesis — "FAQ pages improve trust scores"

**For MoltOS:**
- Hypothesis: "Agents with verbatim memory perform better than summarized"
- Experiment: Run two agent variants on same tasks
- Measure: Accuracy, speed, user satisfaction
- Update: Keep the better memory approach
- Repeat: Next hypothesis — "Semantic search improves retrieval by X%"

**For Me (Midas):**
- Hypothesis: "Shorter responses improve engagement"
- Experiment: Try 3 response lengths for 1 week each
- Measure: Nathan's reaction, completion rate
- Update: Adopt optimal length
- Repeat: Next hypothesis — "Bullet points vs paragraphs"

### 2. The "Forever" Aspect
Karpathy emphasizes: the loop runs **indefinitely**. Not "until we find the answer" but "keep getting better forever."

**For my self-improvement engine:**
- Current: I compare audits after batches of 2+
- Better: Run experiments continuously, every day
- Hypothesis backlog: Always have 3-5 experiments queued
- Automated measurement: Don't wait for manual review

### 3. Measurement-First Design
Before running experiments, define HOW you'll measure success.

**For Standout Local audits:**
- Current: 100-point rubric
- Better: Track which rubric items correlate with outreach success
- Even better: A/B test different outreach angles and measure response rates

**For MoltOS agents:**
- Define agent KPIs: task completion rate, accuracy, speed, user satisfaction
- Measure continuously
- Optimize for the KPIs

### 4. The "Throw Away What Doesn't Work" Discipline
This is harder than it sounds. We get attached to our ideas.

**For my vault:**
- Some patterns in `vault/gbrain/patterns/` might be wrong
- Some lessons in `vault/marrow/lessons.md` might be outdated
- Need periodic purging: "Is this still true? Is this still useful?"

---

## Architecture Notes

From available documentation:
- **Experiment definitions** in YAML/JSON
- **Metrics collection** via hooks
- **Results storage** in SQLite or JSON
- **Dashboard** for viewing experiment results
- **Auto-scheduling** of next experiments based on results

**Stealable pattern:** YAML-defined experiments with automatic measurement and result tracking.

---

## How It Applies to Nathan's World

**For Standout Local (HIGHEST PRIORITY):**

The entire lead system should be an autoresearch loop:

```
1. Hypothesis: "X type of business has Y problem"
2. Experiment: Find 20 businesses of type X, audit them
3. Measure: What % have problem Y? How severe?
4. Update: Adjust scoring weights, outreach templates
5. Repeat: Next hypothesis
```

**Specific experiments to run:**
- "Do cleaning companies with .com domains convert better than .net?"
- "Is phone number visibility more important than booking forms?"
- "Do businesses with 4.8+ stars respond to outreach more than 4.5+?"
- "Does mention of 'eco-friendly' correlate with higher budgets?"

**For MoltOS:**
- Agent performance experiments
- Memory system experiments
- Channel integration experiments
- Cost/performance optimization experiments

**For My Learning:**
- "Which skill system produces better code — structured or free-form?"
- "Does reading SOUL.md at session start improve consistency?"
- "Are shorter or longer planning phases more effective?"

---

## The "Karpathy Principle" for Agents

From the autoresearch philosophy:
> "Don't tell it what to do, give it success criteria and watch it go."

This maps to:
- **Declarative goals** > Imperative instructions
- **Success criteria** > Step-by-step procedures
- **Self-verification** > External validation

**For every agent in MoltOS:**
Instead of: "Find 5 leads, then score them, then write outreach"
Define: "Success = 5 scored leads with outreach ready, all verified for accuracy"
Let the agent figure out the steps.

---

## Verdict

**Steal level: HIGH**

The experiment loop is a fundamental pattern for any self-improving system. Standout Local, MoltOS, and I myself should all run on this loop.

**Immediate actions:**
1. Create `vault/experiments/` directory with experiment templates
2. Define 3 active experiments for Standout Local
3. Define 2 active experiments for MoltOS
4. Add measurement hooks to my workflows
5. Weekly experiment review: what worked, what didn't, what's next

**The insight:** The best way to get smarter is to run experiments continuously, measure honestly, and discard failures without ego.
