# Repo Research: Agent Skills (Addy Osmani)

**URL:** https://github.com/addyosmani/agent-skills
**Stars:** 30,000+
**What it is:** 20 production-grade engineering skills for AI coding agents, used by FAANG engineers

---

## What It Does

Addy Osmani (Google Chrome team, known for web performance work) created a structured skill system for AI agents. Not just prompts — **production-grade engineering methodologies** encoded as skills.

**The 20 Skills:**
1. **Define** — Clarify what to build
2. **Plan** — Break it down
3. **Build** — Write the code
4. **Verify** — Prove it works
5. **Review** — Quality check
6. **Debug** — Systematic problem solving
7. **Refactor** — Improve existing code
8. **Test** — Validation strategies
9. **Document** — Technical writing
10. **Deploy** — Release management
11. **Monitor** — Observability
12. **Optimize** — Performance tuning
13. **Secure** — Security practices
14. **Scale** — Growth architecture
15. **Migrate** — Technical transitions
16. **Integrate** — API & service connections
17. **Analyze** — Data & metrics
18. **Design** — UX & architecture
19. **Research** — Technical investigation
20. **Automate** — Workflow optimization

Each skill is a **complete methodology** — not just "write tests" but "here's how to design a test strategy, what to test, how to measure coverage, when to stop."

---

## What's Stealable

### 1. The Skill Definition Format
Skills aren't just markdown files. They're structured:
- **Purpose** — What this skill does
- **When to use** — Trigger conditions
- **Procedure** — Step-by-step methodology
- **Success criteria** — How to know it's done
- **Common pitfalls** — What goes wrong
- **Examples** — Real usage patterns

**For my skill system:**
- Current: Skills are markdown files with instructions
- Better: Add structured sections (purpose, when, procedure, criteria, pitfalls)
- Best: Machine-readable format that agents can parse and execute

### 2. The "Production-Grade" Standard
These aren't hobby skills. They're battle-tested by engineers at top tech companies.

**Key characteristics:**
- **Specific** — Not "write good code" but "use TypeScript strict mode, handle errors in `src/utils/errors.ts`, follow existing patterns in `handlers/`"
- **Measurable** — Success criteria are binary (pass/fail)
- **Context-aware** — Skills reference project-specific files and patterns
- **Failure-aware** — Each skill documents common failure modes

**For my skills:**
- Standout Local audit skill: needs specific rubric, not "check the website"
- Lead scoring skill: needs exact scoring formula, not "score it well"
- Outreach skill: needs tone guidelines, not "write a good email"

### 3. The Plugin Marketplace System
```bash
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```

Skills are:
- **Versioned** — `@addy-agent-skills` specifies version
- **Namespaced** — `addyosmani/` identifies author
- **Installable** — One command to add to any project
- **Composable** — Multiple skill sets can coexist

**For MoltOS:**
- MoltOS should have a skill marketplace
- Skills are packages, not files
- Version control for skills (updates don't break existing agents)
- Namespacing (Nathan's skills vs community skills)

### 4. The 20-Skill Framework as a Checklist
The 20 skills map to the complete software development lifecycle. This is a **universal checklist**.

**For any project Nathan starts:**
1. Did we Define what we're building?
2. Did we Plan the approach?
3. Did we Build it?
4. Did we Verify it works?
5. Did we Review the quality?
6. ... through all 20

**For Standout Local specifically:**
- Define: What business, what pain points
- Plan: Audit → Demo → Outreach sequence
- Build: Create the demo page
- Verify: Does it actually convert?
- Review: Quality check the outreach copy
- Deploy: Send outreach
- Monitor: Track responses
- Optimize: Refine based on results

---

## How It Applies to Nathan's World

**For Me (Midas):**
- Before any coding task: run through Define → Plan → Build → Verify → Review
- After completion: did I hit all 5 quality gates?
- When stuck: check the Debug skill methodology

**For Standout Local:**
- Each lead gets the full 20-skill treatment (scaled to the task)
- Audit = Research + Analyze
- Demo = Design + Build + Verify
- Outreach = Document + Deploy + Monitor
- Pipeline optimization = Optimize + Automate

**For MoltOS:**
- Agent tasks should map to the 20 skills
- Each agent specializes in 2-3 skills
- Coordinator agent assigns tasks based on skill mapping
- Quality gates at each transition

**For Vault/Skilling:**
- `vault/rooms/skills/` should follow the 20-skill taxonomy
- Each skill file: structured with purpose/when/procedure/criteria/pitfalls
- Skill dependencies (Debug requires Test, Deploy requires Verify)

---

## Comparison: Addy Skills vs Karpathy Skills vs My Skills

| Aspect | Addy Skills | Karpathy Skills | My Current |
|--------|-------------|-----------------|------------|
| **Format** | Structured 20-skill system | Single CLAUDE.md | Markdown files |
| **Scope** | Full SDLC | Coding behavior | Task-specific |
| **Specificity** | High (production-grade) | High (behavioral) | Medium |
| **Install** | Plugin marketplace | Plugin marketplace | File-based |
| **Measure** | Success criteria per skill | Observable behavior | Varies |

**Best of all worlds:**
- Karpathy's 4 principles as behavioral foundation
- Addy's 20 skills as task taxonomy
- My domain-specific skills (audit, outreach, lead scoring) as implementations

---

## Verdict

**Steal level: HIGH**

The structured skill format and the 20-skill lifecycle taxonomy are immediately applicable. The plugin marketplace pattern is essential for MoltOS's skill system.

**Immediate actions:**
1. Restructure `vault/rooms/skills/` to follow the 20-skill taxonomy
2. Add structured sections to every skill (purpose, when, procedure, criteria, pitfalls)
3. Design skill marketplace concept for MoltOS
4. Create "Standout Local" skill set following the production-grade standard
5. Add success criteria to every skill I use

**The insight:** Skills aren't just instructions — they're methodologies. The difference between "write tests" and "follow this test strategy with these criteria" is the difference between amateur and professional.
