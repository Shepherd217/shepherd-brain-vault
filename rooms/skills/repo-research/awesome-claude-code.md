# Repo Research: Awesome Claude Code

**URL:** https://github.com/luandro/awesome-claude-code (or similar curated lists)
**Stars:** Various (the ecosystem has 30K-100K+ across related repos)
**What it is:** Curated collection of tools, workflows, skills, and resources for enhancing Claude Code productivity

---

## What It Does

This is an **ecosystem map** — not a single tool but a directory of the best Claude Code enhancements. The kind of thing that makes you go "oh shit, I didn't know that existed."

**Categories covered:**
- Development environments & Docker
- Project management workflows
- Configuration & setup tools
- Terminal & CLI enhancements
- Authentication & OAuth
- Agent orchestration & parallel execution
- Browser automation
- Learning resources
- Memory & context tools
- Multi-agent systems

---

## What's Stealable

### 1. The Ecosystem Curation Pattern
**The value is in curation, not creation.** This repo doesn't build tools — it finds the best ones and organizes them.

**For my vault:**
- Create `vault/rooms/skills/tool-directory.md` — curated tools I actually use
- Not just a list — annotate WHY each tool matters, WHEN to use it
- Update monthly

**For Standout Local:**
- Curate a "best tools for local business websites" directory
- Not just "here's a form builder" but "use Forminit when you need X, use Typeform when you need Y"

### 2. Specific Tools Worth Stealing

**A. Spec-Driven Development Workflow**
- Repo: `Pimzino/claude-code-spec-workflow` (1.6K stars)
- Pattern: Requirements → Design → Tasks → Implementation
- **Steal for:** Standout Local lead packets (requirements → audit → demo → outreach)

**B. Claude Code Project Management (CCPM)**
- Repo: `automazeio/ccpm` (1.1K stars)
- Pattern: PRD → Epic → Tasks → GitHub Issues
- **Steal for:** MoltOS feature development workflow

**C. Tmux Orchestrator (24/7 Autonomous Agents)**
- Repo: `Jedward23/Tmux-Orchestrator` (1.3K stars)
- Pattern: Three-tier hierarchy — Orchestrator → Project Managers → Engineers
- **Steal for:** MoltOS agent hierarchy

**D. Task Delegation System**
- Pattern: Lightweight slash command for parallel task execution using tmux + git worktrees + markdown prompts
- **Steal for:** My sub-agent spawning (I already do this but could formalize)

**E. rtk — Token Consumption Reducer**
- Repo: High-performance CLI proxy reducing LLM token consumption by 60-90%
- Single Rust binary, zero dependencies
- **Steal for:** MoltOS cost optimization

**F. caveman — Token-Saving Skill**
- Repo: `JuliusBrussee/caveman`
- Pattern: Makes Claude respond in minimal caveman-style language to cut tokens
- **Steal for:** When Nathan just wants a yes/no, not an essay

**G. claude-mem — Auto Memory Capture**
- Repo: `thedotmack/claude-mem` (25.3K stars, fastest growing)
- Pattern: Auto-captures sessions, compresses with AI, injects context into future sessions
- **Steal for:** This is basically what my vault does, but automated. Learn from the compression strategy.

### 3. The `.claude/` Directory Convention
Many tools in this ecosystem use a `.claude/` directory for:
- `CLAUDE.md` — Project-specific behavior rules
- `rules/` — Scoped rule files (backend.md, frontend.md, security.md)
- `skills/` — Custom skills for the project

**For my workspace:**
- I have `SOUL.md` and `AGENTS.md` at root
- Could add `.claude/rules/` for project-specific rules
- Could add `.claude/skills/` for custom skills

### 4. The Claude Playbook Pattern
Repo: `smartwhale8/claude-playbook`
- Production-ready `.claude/` directory template
- Enforces professional software engineering standards
- Drop-in template for any project

**For Standout Local:**
- Create a `.claude/` playbook for the project
- Define: build commands, test procedures, deployment rules
- Nathan can drop this into any repo and Claude Code knows how to work with it

---

## How It Applies to Nathan's World

**For Me (Midas):**
- Install Karpathy skills (already researched)
- Install spec-workflow for structured development
- Set up `.claude/` directory in workspace
- Use tmux orchestrator for parallel sub-agent tasks

**For Standout Local:**
- CCPM workflow for managing the lead pipeline
- Spec-driven development for demo pages
- Claude playbook for consistent code quality
- Browser automation skills for research

**For MoltOS:**
- Agent orchestration patterns from tmux orchestrator
- Token reduction strategies (rtk, caveman)
- Memory management from claude-mem
- Multi-agent coordination patterns

**For General Productivity:**
- The curated list itself is a goldmine
- Every tool has been community-vetted
- Saves hours of discovery time

---

## The Agentic Coding Playbook

One standout entry: `john-wilmes/claude-agentic-coding-playbook`
- 30+ production hooks (context guard, stuck detector, sycophancy detector, PII sanitizer, model router)
- Session-aware statusline
- Skills for checkpointing, investigations, project scaffolding
- `claude-loop` for autonomous multi-task orchestration

**Hooks to steal:**
1. **Context Guard** — Warns at 35%/57%/60% context usage
2. **Stuck Detector** — Detects when the agent is going in circles
3. **Read-Once Dedup** — Prevents redundant file reads
4. **Checkpoint System** — Save session state and memory

**For me:** I should implement a "stuck detector" — when I'm iterating on the same file without progress, flag it and ask for direction.

---

## Verdict

**Steal level: HIGH (as a directory)**

The individual tools are all stealable, but the REAL value is having a curated map of the ecosystem. Instead of building everything from scratch, pick the best tools and integrate them.

**Immediate actions:**
1. Create `.claude/` directory in workspace with rules and skills
2. Install Karpathy skills (already planned)
3. Set up spec-workflow for Standout Local
4. Implement context guard in my sessions
5. Add stuck detection to my workflow
6. Create a "tools I use" directory in vault

**The insight:** Don't build what you can install. The Claude Code ecosystem is maturing fast — ride the wave.
