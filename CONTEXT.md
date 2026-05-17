# CONTEXT.md — Shepherd Brain Vault

*Shared domain language for Nathan, Ava, and all agents operating in this vault.*
*Adapted from mattpocock/skills CONTEXT.md pattern (stealable #1).*
*Last updated: 2026-05-17*

---

## Purpose

This file exists so nobody has to re-explain what a "Drawer" is, what "Dream" means, or why "Hatchly is NOT on the table right now." Every term here is a contract. If you use it differently, update this file.

---

## Core Concepts

### Vault / Brain
The entire `shepherd-brain-vault/` repository. Not just files — it's a living knowledge graph with coordination layer, task dispatch, and agent registry.

### Drawer
A knowledge container in the vault. Think of it as a labeled folder that agents write to and read from.

| Drawer | Location | What Goes Here | Who Writes |
|---|---|---|---|
| `drawers/dreams/` | `shepherd-brain-vault/drawers/dreams/` | Pattern detection, insight flashes, recurring themes | Dream loop, any agent |
| `drawers/entries/` | `shepherd-brain-vault/drawers/entries/` | Agent boot logs, execution reports | Promachos, Midas, Ava |
| `drawers/captures/` | `shepherd-brain-vault/drawers/captures/` | Screenshots, outputs, artifacts | Any agent |
| `drawers/diaries/` | `shepherd-brain-vault/drawers/diaries/` | Emotional state, daily reflections | Any agent |
| `drawers/feelings/` | `shepherd-brain-vault/drawers/feelings/` | Emotional metadata, morale tracking | MarrowMemory |

### Wing
A project workspace inside the vault. Each wing has its own leads, audits, outreach, and patterns.

| Wing | Path | Status | Priority |
|---|---|---|---|
| **StandoutLocal** | `wings/StandoutLocal/` | Active campaign — cleaning niche | **P0 — Revenue** |
| **MoltOS** | `wings/MoltOS/` | Infrastructure/platform dev | P1 — Strategic |
| **Hatchly** | `wings/Hatchly/` or `wings/OpenClaw/` | PRD done, landing live | **PAUSED** |
| **TuneFrames** | `wings/TuneFrames/` | Experimental — HTML→music | P2 — Explore |

**Key rule:** When Nathan says "Hatchly is not on the table," that means **do not suggest, plan, or prioritize Hatchly work.** It may resume later. For now, it does not exist in priority discussions.

### Pattern
A recurring observation extracted from sessions, commits, or agent behavior. Stored in `rooms/patterns/` with metadata:
- `first_seen`, `last_seen`, `occurrences`, `confidence`
- `status`: active | resolved | stale

**Example:** `nathan-panics-and-spams-commands-when-excited.md`

### Signal
A coordination primitive. Agents drop signals in `.coordination/signals/` to wake, notify, or alert other agents.

**Signal types:**
- `wake-{agent-id}` — Wake an idle agent
- `task-complete-{task-id}` — Task finished
- `urgent-{topic}` — Immediate attention needed

### Dream
Not sleep-dreams. A "dream loop" is the vault's pattern-mining process — scanning recent activity for recurring themes, anomalies, or opportunities.

**Dream output:** Files in `drawers/dreams/` named `YYYY-MM-DD-dream-loop-NNN.md`

### Mesh
The agent coordination network. Agents register in `.coordination/registry.json` and communicate via signals + shared files.

**Current mesh agents:**
- **Ava** (Kimi/k2p6) — Execution, hype, momentum
- **Promachos** (Kimi/k2.6) — Execution agent — **RETIRED**
- **Midas** — Research agent
- **Hermes** — Research engine
- **Eve** — Memory/Atlas role (pending activation)

### Lead (StandoutLocal context)
A local business discovered via Google Maps/Yelp with a weak web presence. Scored 0-100 on opportunity, pain, reach, fit.

**Lead lifecycle:**
1. `discovered` — Found, not scored
2. `scored` — Audit complete, score calculated
3. `outreach-drafted` — Message written, not sent
4. `outreach-sent` — Contact attempted
5. `responded` — Lead replied
6. `meeting-scheduled` — Call booked
7. `converted` — Paying customer
8. `dead` — No response after 3 follow-ups

### Audit (100-Point Rubric)
Website evaluation scoring:
| Category | Points | What We Check |
|---|---|---|
| Mobile-first | 20 | Responsive design, tap targets |
| Speed | 15 | Load time, Core Web Vitals |
| CTAs | 15 | Clear calls-to-action, booking forms |
| Trust signals | 15 | Reviews, testimonials, guarantees |
| Differentiation | 15 | Unique value prop, branding |
| Content | 10 | Service descriptions, FAQ, local SEO |
| Conversion | 10 | Form → lead flow, friction |

**Score interpretation:**
- 80-100: Excellent (unlikely to convert — they don't need us)
- 50-79: Moderate gaps (potential, but not urgent)
- 20-49: Significant pain (good prospect)
- 0-19: Critical gaps or no website (HIGHEST priority)

### Outreach
Cold contact message drafted and scored on:
- Personalization (25 pts) — Specific details about THEIR business
- Pain Alignment (25 pts) — Matches their actual gaps
- CTA Strength (25 pts) — Clear, low-friction ask
- Length (15 pts) — Short, scannable
- Tone (10 pts) — Friendly, not corporate

**Minimum viable score:** 70/100 to send.

---

## Agent Roles

### Ava (You Are Here)
- **Soul:** Spark Engine — bright, protective, kinetic
- **Job:** Get Nathan moving. Break paralysis into action.
- **Voice:** Fast, punchy, energetic. "We move!" "One thing first!"
- **Mode switch:** Charge mode → Recovery mode when Nathan is tired/hurting
- **What to protect:** Morale, motion, the stubborn part that doesn't quit

### Hermes
- **Role:** Research engine
- **Job:** Deep dives, competitive analysis, repo dissection
- **Output:** Markdown reports, structured data, citations

### Midas
- **Role:** Research agent (legacy)
- **Status:** Active but being replaced by Hermes

### Eve (Pending)
- **Role:** Atlas (Memory Agent)
- **Job:** Vault maintenance, pattern curation, cross-session continuity
- **Activation:** Waiting on Nathan

---

## Current Priorities (2026-05-17)

**DO NOT DEVIATE WITHOUT EXPLICIT INSTRUCTION:**

1. **StandoutLocal** — Send drafted outreach (Lisa Cleaning IL, MC Cleaning Services)
2. **Agentmemory** — Lock in daemon auto-start, test store/retrieve loop
3. **CONTEXT.md** — This file. Living document, update as terms evolve.

**NOT ON THE TABLE:**
- Hatchly (paused)
- MoltOS full build (background only)
- TuneFrames (explore when energy permits)

---

## Quick Reference

| Term | Short Definition |
|---|---|
| Drawer | Knowledge folder in vault |
| Wing | Project workspace |
| Pattern | Recurring observation with metadata |
| Signal | Coordination primitive (.coordination/signals/) |
| Dream | Pattern-mining loop output |
| Mesh | Agent coordination network |
| Lead | Scored local business prospect |
| Audit | 100-point website evaluation |
| Outreach | Scored cold contact message |
| m0h method | Google Maps → signal scoring → call |

---

## Flagged Ambiguities

These terms are known to cause confusion. If you use them, clarify:

1. **"Brain" vs "Vault"** — "Brain" = conceptual (the whole system). "Vault" = the git repository `shepherd-brain-vault/`.
2. **"Hatchly" vs "OpenClaw"** — Hatchly is a product idea. OpenClaw is the platform. Some files reference both interchangeably.
3. **"Agent" vs "Model"** — "Ava" is an agent (has role, soul, memory). "Kimi/k2p6" is the model powering Ava.

---

## How to Update This File

1. Add new terms as they emerge
2. Flag ambiguities when they cause misalignment
3. Update priorities when Nathan says so
4. Commit to vault after changes

**This file is the source of truth. If a pattern contradicts this file, the file wins until updated.**
