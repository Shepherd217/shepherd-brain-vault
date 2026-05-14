---
created_at: 2026-05-13
---

# Coordination Layer Deep Dive

## Current Architecture

The coordination layer is a **file-based dispatch daemon** — not a server, not a queue. Just Python watching markdown files.

### How It Works (10-second polling loop)

```
1. dispatch.py scans .coordination/tasks/inbox/*.md
2. Finds tasks with status: todo and no claimed_by
3. Sorts by priority: critical → high → medium → low
4. Checks registry.json for idle agents
5. Dispatches first matching task to first idle agent
6. Touches .coordination/signals/wake-<agent> to wake them
7. Agent works, updates frontmatter, commits, pushes
```

### Key Files

| File | Purpose |
|------|---------|
| `registry.json` | Agent roster: id, type, zone, status, current_task |
| `heartbeat.json` | Last-seen timestamps per agent |
| `dispatch.py` | The daemon (polls every 10s) |
| `tasks/inbox/*.md` | Task files with YAML frontmatter |
| `signals/wake-*` | Touch files to wake agents |

### Current Agent Roster (Hardcoded)

```json
{
  "promachos": {
    "id": "promachos",
    "type": "execution",
    "zone": "agents/promachos/",
    "status": "idle",
    "current_task": null
  },
  "ava": {
    "id": "ava",
    "type": "ceo",
    "zone": "agents/ava/",
    "status": "idle",
    "current_task": null
  }
}
```

## Agent Roles (Current)

| Agent | Type | What They Do |
|-------|------|--------------|
| **Hermes** (promachos) | Execution | Infrastructure, builds, specs, tests, detailed commits, audits |
| **Ava** | CEO / Spark | Strategy, research, integration, morale, git ops, quick execution |

## What's Missing (The Gap)

Two major capabilities nobody owns:

1. **Deep Research & Intelligence** — Competitive analysis, market mapping, framework research, web crawling. Nathan had Hatchly for this (now pinned).
2. **Memory & Knowledge Management** — GBrain upkeep, knowledge graph maintenance, entity enrichment, dream cycles, cross-reference linting.

## Adding a 3rd Agent: YES, It's Simple

The dispatch.py already supports N agents. No code changes needed — just update `registry.json`.

### Option A: Scout (Research Agent)

```json
{
  "scout": {
    "id": "scout",
    "type": "research",
    "zone": "agents/scout/",
    "status": "idle",
    "current_task": null
  }
}
```

**Role:** Deep research, competitive intelligence, market mapping, framework analysis.
**Tasks they'd own:**
- Task 002 (Research Sprint) — research multi-agent frameworks
- Hatchly-style competitive audits
- "Research X and produce a briefing" tasks
- Web crawling, Perplexity queries, academic verification

**Value:** Frees Ava from research so she can focus on execution. Gives Nathan dedicated intel capability.

### Option B: Atlas (Memory Agent)

```json
{
  "atlas": {
    "id": "atlas",
    "type": "memory",
    "zone": "agents/atlas/",
    "status": "idle",
    "current_task": null
  }
}
```

**Role:** GBrain maintenance, knowledge graph, entity enrichment, memory consolidation.
**Tasks they'd own:**
- Keep brain pages current (enrichment pipeline)
- Run nightly dream cycle (lint, consolidate, fix citations)
- Import new data sources into brain
- Manage entity deduplication
- Update index.md when pages change

**Value:** Brain compounds 24/7 without human/agent intervention. GBrain stays current automatically.

### Option C: Forge (Builder Agent)

```json
{
  "forge": {
    "id": "forge",
    "type": "builder",
    "zone": "agents/forge/",
    "status": "idle",
    "current_task": null
  }
}
```

**Role:** Build new tools, improve existing ones, write code, create skills.
**Tasks they'd own:**
- "Build a tool that does X"
- Refactor existing tools for performance
- Create new skills for the skill market
- Prototype MVPs rapidly

**Value:** Dedicated builder so Ava/Hermes can focus on coordination and strategy.

## What Would Change

### Task Format (Already Supports This)

Tasks already have `agent_hints.suggest_to`:

```yaml
agent_hints:
  suggest_to: [scout, ava]      # Best suited for Scout or Ava
  block_agents: [promachos]    # Hermes should NOT pick this up
```

### Dispatch Logic (No Code Changes)

The dispatch loop already iterates over ALL idle agents:

```python
idle_agents = get_idle_agents(registry)  # Returns ALL idle agents
for task in unclaimed:
    for agent_id in idle_agents:
        # Tries to dispatch to any idle agent
```

Adding a 3rd agent = just add entry to registry.json. That's it.

### New Zone Structure

```
.coordination/agents/
├── promachos/          ← Hermes (execution)
├── ava/                ← Ava (CEO/spark)
├── scout/              ← NEW: Research/intel
└── shared/             ← Both all agents
```

### Task Assignment Pattern

| Task Type | Primary Agent | Secondary |
|-----------|--------------|-----------|
| Infrastructure, builds, specs | Hermes | Forge |
| Strategy, morale, quick wins | Ava | — |
| Deep research, competitive intel | Scout | Ava |
| Brain maintenance, enrichment | Atlas | Ava |
| Tool building, code | Forge | Hermes |
| Cross-agent coordination | Ava | Hermes |

## Recommended: Add BOTH Scout + Atlas

**Why two more:**
- 4 agents = full coverage: Build (Hermes), Spark (Ava), Research (Scout), Memory (Atlas)
- Each has a clear domain — no overlap, no conflict
- Nathan can split tasks across 4 agents instead of 2
- Parallel work scales: 4 agents × 4 tasks = 16 simultaneous workstreams

## How to Add (Steps)

1. **Update registry.json** — Add new agent entries
2. **Create agent zones** — `mkdir .coordination/agents/<name>/`
3. **Update coordination-layer.md skill** — Document new agent
4. **Create agent-specific tasks** — Tasks with `suggest_to: [scout]` or `suggest_to: [atlas]`
5. **Update AGENTS.md** — Add new agent to system prompts

## Open Questions

1. **Do we need a 3rd agent NOW, or wait until Hermes is active?**
2. **What role fills the biggest gap for Nathan's workflow?**
3. **Should the 3rd agent be another OpenClaw instance, or a subagent within Ava/Hermes?**

---

*Analysis by Ava | Coordination layer: operational | Current agents: 2 | Proposed: 4*
