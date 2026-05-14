---
id: 2026-05-13-004
title: Shared Pattern Library
status: todo
priority: medium
claimed_by: 
created_by: nathan
created_at: 2026-05-13T06:51:00+08:00
depends_on: [2026-05-13-001]
tags: [meta, patterns, learning, optimization]
agent_hints:
  suggest_to: [ava, hermes]
  block_agents: []
---

# Shared Pattern Library

## What
Both agents run sessions with PatternMiner enabled. Index tool sequences from BOTH agents. Build a shared pattern library showing "what works" for each agent's style.

## Why
Ava's workflow (read → fix → test → push) and Hermes's workflow (research → synthesize → commit) are different. If we can see each other's patterns, we can optimize and cross-train.

## Done When
- [ ] PatternMiner indexing sessions from both agents
- [ ] Tool sequence patterns extracted for Ava (minimum 10 sequences)
- [ ] Tool sequence patterns extracted for Hermes (minimum 10 sequences)
- [ ] Comparison written to `rooms/skills/pattern-library-ava-vs-hermes.md`
- [ ] Top 3 patterns from each agent proposed for adoption by the other
- [ ] Pattern library auto-updates when either agent runs sessions

## Notes
Ava's known patterns from current session:
- `exec` → `exec` (88x) — batch tool execution
- `read` → `read` (29x) — multi-file reading
- `exec` → `read` (28x) — execute then inspect

What does Hermes's pattern look like? Let's find out.
