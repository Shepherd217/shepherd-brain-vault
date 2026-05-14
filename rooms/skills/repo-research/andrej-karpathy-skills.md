# Repo Research: Andrej Karpathy Skills

**URL:** https://github.com/forrestchang/andrej-karpathy-skills
**Stars:** 109,000+ (one of the most starred repos in GitHub history)
**What it is:** A SINGLE CLAUDE.md file — Karpathy's coding wisdom distilled into 4 behavioral principles for AI coding agents

---

## What It Does

This is not a codebase. It's a **behavioral contract** — a 65-line markdown file that shapes how Claude Code behaves. Based on Andrej Karpathy's observations about how LLMs fail at coding.

**The Four Principles:**

### 1. Think Before Coding
> "Don't assume. Don't hide confusion. Surface tradeoffs."

- State assumptions explicitly
- Present multiple interpretations when ambiguous
- Push back when a simpler approach exists
- Stop when confused and ask for clarification

### 2. Simplicity First
> "Minimum code that solves the problem. Nothing speculative."

- No features beyond what was asked
- No abstractions for single-use code
- No "flexibility" that wasn't requested
- If 200 lines could be 50, rewrite it
- **Test:** Would a senior engineer say this is overcomplicated?

### 3. Surgical Changes
> "Touch only what you must. Clean up only your own mess."

- Don't "improve" adjacent code, comments, or formatting
- Don't refactor things that aren't broken
- Match existing style, even if you'd do it differently
- Every changed line should trace directly to the user's request

### 4. Goal-Driven Execution
> "Don't tell it what to do, give it success criteria and watch it go."

- Define success criteria upfront
- Let the agent loop until criteria are met
- Transform imperative instructions into declarative goals

---

## What's Stealable

### 1. The Single-File Principle
**109K stars for ONE markdown file.** This proves that behavioral contracts are more valuable than code volume.

**For my SOUL.md / AGENTS.md:**
- My SOUL.md already has behavioral guidelines, but they could be more precise
- Add "Surgical Changes" principle — I sometimes over-edit files
- Add "Simplicity First" — I sometimes over-explain or over-engineer

### 2. The "Ask Instead of Assume" Pattern
Karpathy's #1 principle aligns with my "No fabricated claims" rule but goes further — it's about **clarifying intent before acting**.

**Current problem I have:** When Nathan says "go autonomous," I sometimes misinterpret the scope (like this very session where I did lead scraping instead of repo research).

**Fix:** Add a "clarification protocol" — when scope is ambiguous, ask 1-2 clarifying questions before acting. Speed is good, accuracy is better.

### 3. The "Goal-Driven Execution" Loop
Karpathy says: "LLMs are exceptionally good at looping until they meet specific goals."

**For Standout Local:**
- Instead of "find leads," define: "Find 5 cleaning companies in Champaign-Urbana with 4.5+ stars, websites without booking forms, and within 10 miles of campus"
- Let the agent loop until the criteria are met
- Built-in verification at each step

**For MoltOS:**
- Agent tasks should have explicit success criteria
- Agents should self-verify before reporting completion
- "Done" means "criteria met," not "I stopped working"

### 4. The Simplicity-First Filter
> "Would a senior engineer say this is overcomplicated?"

**For my vault:** My vault structure got complex (wings/rooms/drawers/roosts). Is it useful? Yes. Is it overcomplicated? Maybe. The test: can Nathan navigate it easily? If not, simplify.

**For Standout Local demos:** The best landing pages are simple. No animations that don't convert. No features that don't serve the core CTA.

---

## How It Applies to Nathan's World

**For Me (Midas):**
- Before any coding task: state assumptions, define success criteria
- During editing: surgical changes only, match existing style
- When stuck: stop and ask, don't guess

**For Standout Local:**
- Outreach copy: simplicity first — one CTA, one message
- Demo pages: minimum code that converts, nothing speculative
- Audit reports: surgical changes only — fix what hurts, leave what works

**For MoltOS:**
- Agent prompts should include goal-driven criteria
- Agent outputs should self-verify against criteria
- Simple is better — one agent doing one thing well beats a monolith

**For Vault:**
- Entries should be minimum viable memory
- Don't over-categorize if it creates friction
- Match existing patterns (if a format works, don't invent a new one)

---

## The Installation Method

```bash
# As a Claude Code plugin
/plugin marketplace add forrestchang/andrej-karpathy-skills
/plugin install andrej-karpathy-skills@karpathy-skills

# Or just download the file
curl -o CLAUDE.md https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md
```

**Stealable:** The plugin marketplace approach. Skills as installable packages. This is exactly what Addy Osmani's agent-skills does too.

---

## Verdict

**Steal level: MAXIMUM**

This is not about the code — there IS no code. It's about the **principles**.

The four principles should be baked into:
1. My SOUL.md behavioral guidelines
2. Every agent prompt in MoltOS
3. Standout Local's design philosophy
4. My own decision-making process

**Immediate actions:**
1. Update SOUL.md with the 4 principles
2. Create a "Clarification Protocol" for ambiguous requests
3. Add "Surgical Changes" to my editing guidelines
4. Implement goal-driven criteria for all autonomous tasks

**The meta-lesson:** Sometimes the most valuable thing to steal isn't code. It's wisdom.
