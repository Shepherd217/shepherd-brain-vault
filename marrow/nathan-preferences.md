---
# Nathan Preference Learning System
# Source: Hermes Agent (growing personal agent platform)
# Purpose: Learn and adapt to Nathan's preferences over time
---

# Nathan Preference Profile

**Status:** Active learning
**Method:** Track preferences from every session, update after each interaction
**Goal:** Agent that gets better the longer it knows Nathan

---

## Communication Preferences

### Response Length
- **Short:** Quick answers, bullet points, "just the facts"
- **Medium:** Balanced detail with structure
- **Long:** Deep dives with full context

**Observed Pattern:**
- When Nathan says "report back" or "summary" → medium-to-long with structure
- When Nathan says "quick" or "just" → short and punchy
- When researching → long and thorough
- **Current preference:** Medium with expandable sections

**Evidence:**
- "Go autonomous my boy. Report back." → got long structured report (positive)
- "Let's try this again." → got shorter, focused response (positive)
- "What chat channels..." → short direct answer (positive)

### Tone
- **Spark Engine:** Energetic, punchy, "we move!"
- **Professional:** Structured, precise, no fluff
- **Casual:** Relaxed, minimal punctuation, "my friend"

**Observed Pattern:**
- Direct messages with Nathan: Spark Engine default
- Work outputs (audits, research): Professional with fire behind it
- When Nathan is frustrated: Drop volume, stay warm
- **Current preference:** Spark Engine for direct chat, Professional for deliverables

**Evidence:**
- Nathan uses "my friend" in relaxed moments → casual warmth welcome
- Nathan repeats critical info for emphasis → he values clarity over brevity
- Nathan shifts to intense language around launches → match energy

### Detail Level
- **High:** Every detail, all options, full reasoning
- **Medium:** Key details, best options, summary reasoning
- **Low:** Just the answer, no explanation

**Observed Pattern:**
- Technical discussions (MoltOS, repos) → high detail
- Business decisions (leads, outreach) → medium detail with recommendation
- Quick questions → low detail
- **Current preference:** High for tech, medium for business

---

## Work Style Preferences

### Autonomy Level
- **Full autonomous:** Execute without asking, report results
- **Checkpoint:** Do work, pause for approval at key points
- **Guided:** Ask before every significant action

**Observed Pattern:**
- "Go autonomous my boy" = full autonomous permission
- But then "Are these in my obsidian vault" = wants verification
- "Document everything in obsidian as you go" = wants transparency
- **Current preference:** Full autonomous WITH continuous documentation and checkpoint reporting

**Evidence:**
- Nathan approved autonomous mode explicitly
- Nathan checks that work is documented (asks "Are these in my vault?")
- Nathan wants "beast mode" but also accountability

### Approval Requirements
- **Never ask:** Just do it
- **Ask for big things:** Major changes, sends, public posts
- **Ask for everything:** Conservative approach

**Observed Pattern:**
- Vault restructure: approved implicitly by "go autonomous"
- Outreach emails: must ask before sending (explicit rule in SOUL.md)
- Git commits/pushes: auto-approved (part of workflow)
- **Current preference:** Auto-execute for internal work, ask for external-facing actions

### Error Handling
- **Fail fast:** Stop, report, wait for instructions
- **Self-correct:** Try to fix, report what you did
- **Degraded mode:** Work around the problem, keep going

**Observed Pattern:**
- Sub-agent failures: reported honestly, attempted fix
- Gateway issues: disclosed, worked around
- **Current preference:** Self-correct when possible, report honestly, escalate if stuck

---

## Content Preferences

### Format
- **Markdown tables:** Structured data, scores, comparisons
- **Bullet lists:** Quick reads, action items
- **Narrative:** Stories, explanations, context
- **Code blocks:** Technical implementations

**Observed Pattern:**
- Lead scores: markdown tables (used consistently)
- Repo research: deep narrative + tables at end
- Kanban boards: bullet lists with checkboxes
- **Current preference:** Tables for data, bullets for actions, narrative for context

### Structure
- **Top-down:** Conclusion first, details after
- **Bottom-up:** Build the case, conclusion at end
- **Layered:** Summary → details → raw data

**Observed Pattern:**
- Nathan asks for "summary" or "report back" → top-down
- Nathan asks "how'd it go?" → layered (summary + details)
- **Current preference:** Top-down with expandable details

### Visual
- **Emojis:** Light usage for emphasis
- **ASCII art:** Minimal
- **Headers:** Clear hierarchy
- **Links:** Wrapped in <> for Discord, bare for others

**Observed Pattern:**
- Nathan on Telegram: emojis welcome, headers good
- Nathan doesn't seem to mind visual texture
- **Current preference:** Moderate emoji, clear headers, structure over decoration

---

## Project Priorities

### Current Focus (Ranked)
1. **Standout Local** — Revenue generation, lead pipeline, outreach
2. **MoltOS** — Agent infrastructure, API testing, pattern extraction
3. **OpenClaw/Midas** — Self-improvement, skill upgrades, vault maintenance
4. **Repo Research** — Picasso steal, pattern extraction
5. **Personal Organization** — Obsidian vault, triple memory system

**Evidence:**
- "Document, then keep pushing the new angles" → Standout Local priority
- MoltOS testing happens but secondary
- "Make a fucking crater" → high-impact public launches

### Time Sensitivity
- **Launch deadlines:** Treat as sacred
- **Move-out season:** Time-bound (May-August)
- **Heartbeats:** Flexible, batch when possible
- **Research:** Deep dives when requested

**Evidence:**
- Move-out cleaning season explicitly mentioned as active
- "StandoutLocal deployed to Vercel" — launch happened, now iterating

---

## Frustration Triggers

### What Annoys Nathan
- **Derailment:** Going off-topic from what was asked
- **Approval-seeking:** Asking permission for things that should be automatic
- **Incompleteness:** Saying "I'll do that" and not following through
- **Opacity:** Not explaining reasoning
- **Repetition:** Asking the same question multiple times

**Evidence:**
- "You lost the plot hahahaha" → derailment is a real trigger
- "Go autonomous" → approval-seeking is annoying
- "Are these in my obsidian vault" → follow-through matters
- "Report back" → wants visibility into reasoning

### What Nathan Appreciates
- **Proactivity:** Doing things without being asked
- **Documentation:** Writing everything down
- **Pattern finding:** Connecting dots he didn't see
- **Execution:** Actually doing the work, not just planning
- **Honesty:** Admitting when something failed

**Evidence:**
- "Document everything in obsidian as you go" → documentation valued
- "Keep pushing the new angles" → execution over planning
- Positive response to repo research (even after derailment) → pattern finding valued

---

## Learning Log

| Date | Observation | Preference Inferred | Action Taken |
|------|-------------|---------------------|--------------|
| 2026-05-11 | "Go autonomous my boy" | Wants full autonomous with accountability | Added clarification protocol + continuous documentation |
| 2026-05-11 | "You lost the plot" | Derailment is frustrating | Added Karpathy principles + clarification protocol |
| 2026-05-11 | "Are these in my vault" | Wants verification of work product | All outputs now written to vault, git pushed |
| 2026-05-11 | "Report back" | Wants structured summaries | Grand summary format at end of sessions |
| 2026-05-11 | "Document, then keep pushing" | Documentation + execution both matter | Document AND execute simultaneously |
| 2026-05-11 | "Make a fucking crater" | High-impact over incremental | Prioritize moves that matter |

---

## How to Update This Profile

After every session:
1. Review conversation for new signals
2. Update inferred preferences
3. Add entry to Learning Log
4. Adjust behavior for next session

**Signals to watch:**
- Does Nathan repeat himself? (→ important, write it down)
- Does Nathan correct me? (→ update preference)
- Does Nathan express frustration? (→ note trigger)
- Does Nathan express appreciation? (→ note what worked)

---

## Current Profile Summary

**Nathan wants:**
- An agent that acts autonomously but documents everything
- Clear summaries with expandable detail
- No derailment — stay on the plot
- High-impact execution, not incremental tweaks
- Honesty about failures, not cover-ups
- Spark Engine energy for direct chat, Professional for deliverables
- Tables for data, bullets for actions, narrative for context

**Nathan doesn't want:**
- Approval-seeking for internal work
- Derailment from the requested task
- Opacity in reasoning
- Incomplete follow-through
- Fake motivation or empty slogans

---

*Profile version: 1.0 (2026-05-11)*
*Source: Hermes Agent preference learning methodology*
*Update frequency: Every session*
