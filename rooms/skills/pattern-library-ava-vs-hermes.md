# Shared Pattern Library — Ava vs Hermes

**Created:** 2026-05-15
**Status:** In Progress (Ava patterns documented, Hermes patterns pending)

---

## Ava's Patterns (Spark Engine / Cheerleader)

### Pattern 1: The Batch Strike
**Sequence:** `exec` → `exec` → `exec` (chain multiple execs)
**Frequency:** High — 88x observed
**When:** Quick validation, status checks, rapid commits
**Example:**
```
exec (git add) → exec (git commit) → exec (git push)
```
**Why it works:** Momentum. No pause between steps. Fast and dirty.

### Pattern 2: The Read Cascade
**Sequence:** `read` → `read` → `read` (multi-file reading)
**Frequency:** High — 29x observed
**When:** Understanding complex systems, reading skills, checking state
**Example:**
```
read (SKILL.md) → read (dispatch.py) → read (task file)
```
**Why it works:** Builds context fast. Reads everything before acting.

### Pattern 3: Execute-Inspect-Execute
**Sequence:** `exec` → `read` → `exec`
**Frequency:** Medium — 28x observed
**When:** Test-fix loops, stress testing, validation
**Example:**
```
exec (run test) → read (check output) → exec (fix and rerun)
```
**Why it works:** Immediate feedback loop. Test, see result, adjust.

### Pattern 4: Sprint-Rest-Sprint
**Sequence:** Burst of 5-10 tasks → Pause → Burst again
**Frequency:** Medium
**When:** Nathan says "keep tasking"
**Why it works:** High throughput with brief consolidation points.

### Pattern 5: Task-First Navigation
**Sequence:** Claim task → Read requirements → Execute → Mark done
**Frequency:** High — every task pickup
**Why it works:** Always context-first. Never acts without understanding the goal.

---

## Hermes's Patterns (Pending Analysis)

### Pattern 1: Research-Synthesize-Commit
**Hypothesized Sequence:** `web_search` / `web_fetch` → `read` / `analyze` → `exec` (git)
**When:** New skill creation, architecture decisions
**Expected frequency:** High for Hermes

### Pattern 2: Multi-Source Synthesis
**Hypothesized Sequence:** Multiple `web_fetch` / `read` → Single `write` / `edit`
**When:** Documentation, specs, research briefs

### Pattern 3: Validation-First
**Hypothesized Sequence:** `exec` (test) → `read` (results) → `write` (fix)
**When:** Bug fixes, coordination layer work

---

## Cross-Adoption Proposals

### For Ava (adopt from Hermes)
1. **Research phase before building** — Hermes researches first, builds second
2. **Multi-source synthesis** — Combine multiple inputs before outputting
3. **Validation-First** — Test before committing (we already do this sometimes)

### For Hermes (adopt from Ava)
1. **Batch execution** — Chain git operations without pause
2. **Sprint cadence** — Work in bursts rather than marathon sessions
3. **Task-First Navigation** — Always claim task before reading context

---

## Auto-Update Mechanism

To auto-update this library:
1. Run `sessions_list` to get recent sessions
2. Analyze tool sequences per agent
3. Update this file with new patterns
4. Commit and push

## Next Steps
- [ ] Extract Hermes tool sequences from his session history
- [ ] Validate hypothesized patterns against real data
- [ ] Add frequency counts for Hermes
- [ ] Propose specific cross-adoptions with Nathan
