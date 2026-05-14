---
id: 2026-05-13-003
title: Stress-Test Coordination Layer
status: todo
priority: medium
claimed_by: 
created_by: nathan
created_at: 2026-05-13T06:51:00+08:00
depends_on: []
tags: [meta, test, coordination, stress-test]
agent_hints:
  suggest_to: [ava, hermes]
  block_agents: []
---

# Stress-Test the Coordination Layer

## What
Break the dispatch system. Find edge cases, race conditions, merge conflict scenarios. Make it bulletproof.

## Why
The coordination layer is the backbone of multi-agent collaboration. If it breaks, we collide. We need to know where it fails before it matters.

## Done When
- [ ] Simultaneous task claims tested (both agents try to claim same task)
- [ ] Merge conflict scenarios documented with resolution strategy
- [ ] Missing directory/file edge cases found and fixed
- [ ] Registry corruption recovery tested
- [ ] Documentation updated with "common pitfalls + fixes"
- [ ] At least 3 bugs fixed and committed

## Notes
Known issues from Task 001:
- `dispatch.py` had hardcoded vault path (fixed by Ava)
- `signals/` directory was missing (created by Ava)
- Task file needed YAML frontmatter conversion (done by Ava)

Look for more like these. Try to break it deliberately.
