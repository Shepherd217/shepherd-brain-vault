# CONTEXT.md — Shepherd Brain Vault

*Shared domain language for Nathan, Ava, and all agents operating in this vault.*
*Adapted from mattpocock/skills CONTEXT.md pattern.*
*Last updated: 2026-05-17*

---

## Purpose

This file exists so nobody has to re-explain what a "Drawer" is, what "Dream" means, or why "Hatchly is NOT on the table right now." Every term here is a contract. If you use it differently, update this file.

---

## Language

### Vault Structure

**Vault**:
The entire `shepherd-brain-vault/` repository — living knowledge graph with coordination layer, task dispatch, and agent registry.
_Avoid_: Brain (ambiguous — "brain" = conceptual whole system), Repo

**Drawer**:
A knowledge container in the vault. Labeled folder that agents write to and read from.
_Avoid_: Folder, Directory

**Wing**:
A project workspace inside the vault. Each wing has its own leads, audits, outreach, and patterns.
_Avoid_: Project, Module

**Room**:
A cross-cutting concern space inside the vault. Patterns live in `rooms/patterns/`. Skills live in `rooms/skills/`.
_Avoid_: Category, Tag

### Coordination

**Signal**:
A coordination primitive. Agents drop signals in `.coordination/signals/` to wake, notify, or alert other agents.
_Avoid_: Message, Notification

**Mesh**:
The agent coordination network. Agents register in `.coordination/registry.json` and communicate via signals + shared files.
_Avoid_: Network, Cluster

**Dream**:
The vault's pattern-mining process — scanning recent activity for recurring themes, anomalies, or opportunities. Not sleep-dreams.
_Avoid_: Insight, Analysis

### Knowledge

**Pattern**:
A recurring observation extracted from sessions, commits, or agent behavior. Stored in `rooms/patterns/` with metadata.
_Avoid_: Trend, Habit

**Lead** (StandoutLocal context):
A local business discovered via Google Maps/Yelp with a weak web presence. Scored 0-100.
_Avoid_: Prospect, Target

**Audit**:
100-point website evaluation using the rubric. Determines if a lead is worth pursuing.
_Avoid_: Review, Check

**Outreach**:
Cold contact message drafted and scored. Minimum 70/100 to send.
_Avoid_: Pitch, Email

### Agents

**Ava**:
Execution agent powered by Spark Engine. Fast, punchy, kinetic. Protects morale and motion.
_Avoid_: Assistant, Bot

**Hermes**:
Research engine. Deep dives, competitive analysis, repo dissection.
_Avoid_: Researcher, Analyst

**Promachos**:
Former execution agent. RETIRED. Replaced by Ava.
_Avoid_: Old agent

**Eve**:
Pending activation — Atlas/Memory role. Vault maintenance, pattern curation.
_Avoid_: Memory agent

---

## Relationships

- A **Vault** contains multiple **Wings** and **Rooms**
- A **Wing** contains **Leads**, **Audits**, and **Outreach** drafts
- A **Room** contains **Patterns** or **Skills**
- A **Drawer** contains **Dreams**, **Entries**, **Captures**, **Diaries**, or **Feelings**
- An **Agent** registers in the **Mesh** and communicates via **Signals**
- A **Dream** loop scans recent activity and outputs **Patterns**
- A **Lead** progresses through a lifecycle: `discovered` → `scored` → `outreach-drafted` → `outreach-sent` → `responded` → `meeting-scheduled` → `converted` or `dead`

---

## Example Dialogue

> **Nathan:** "When a **Lead** is `scored`, do we immediately draft **Outreach**?"
> **Ava:** "No — we only draft **Outreach** if the **Audit** score is below 50. High scores mean they don't need us."

---

## Flagged Ambiguities

- **"Brain" vs "Vault"** — "Brain" = conceptual (the whole system). "Vault" = the git repository `shepherd-brain-vault/`. Use "Vault" when referring to files.
- **"Hatchly" vs "OpenClaw"** — Hatchly is a product idea. OpenClaw is the platform. Hatchly is PAUSED; do not suggest or prioritize it.
- **"Agent" vs "Model"** — "Ava" is an agent (has role, soul, memory). "Kimi/k2p6" is the model powering Ava.
- **"Lead" vs "Customer"** — A **Lead** is a prospect (not yet contacted). A **Customer** is a converted lead (paying).
- **"Dream" vs "Diary"** — A **Dream** is pattern-mining output. A **Diary** is emotional state / daily reflection.

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
| Room | Cross-cutting concern space |
| Pattern | Recurring observation with metadata |
| Signal | Coordination primitive (.coordination/signals/) |
| Dream | Pattern-mining loop output |
| Mesh | Agent coordination network |
| Lead | Scored local business prospect |
| Audit | 100-point website evaluation |
| Outreach | Scored cold contact message |
| m0h method | Google Maps → signal scoring → call |

---

## How to Update This File

1. Add new terms as they emerge
2. Flag ambiguities when they cause misalignment
3. Update priorities when Nathan says so
4. Commit to vault after changes

**This file is the source of truth. If a pattern contradicts this file, the file wins until updated.**
