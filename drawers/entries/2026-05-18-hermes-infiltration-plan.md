# 🎯 IMPLEMENTATION PLAN: Hermes v0.13 + v0.14 Infiltration

**Date:** 2026-05-18  
**Agent:** Ava  
**Source:** NousResearch/hermes-agent (open source)  
**Target:** shepherd-brain-vault / OpenClaw integration  
**Status:** DRAFT — awaiting Nathan approval before execution

---

## Executive Summary

Hermes Agent shipped two massive releases in 9 days:
- **v0.13 (May 7)** — "The Tenacity Release" — 864 commits, Kanban multi-agent board, goal locking, checkpoints v2
- **v0.14 (May 16)** — "The Foundation Release" — 808 commits, PyPI install, lazy-deps, LSP diagnostics, cross-session caching

This document maps the stealable architecture to our brain vault. **12 features identified, 5 are P0 (implement immediately), 4 are P1 (this week), 3 are P2 (next sprint).**

---

## Priority Matrix

| Feature | Hermes Version | Our Priority | Effort | Impact | Where It Lives |
|---------|---------------|-------------|--------|--------|----------------|
| 1. File-Mutation Verifier | v0.14 | **P0** | Small | High | Core turn loop |
| 2. LSP Semantic Diagnostics | v0.14 | **P0** | Medium | High | Write tool wrapper |
| 3. Lazy-Deps / Debloating | v0.14 | **P0** | Medium | High | Install layer |
| 4. Cross-Session Prompt Cache | v0.14 | **P0** | Medium | High | ClawMem / gateway |
| 5. Kanban Multi-Agent Board | v0.13 | **P0** | Large | Very High | Dashboard + coordination |
| 6. /goal Target Locking | v0.13 | **P1** | Medium | High | Session state |
| 7. Live Session Handoff | v0.14 | **P1** | Medium | High | Gateway / sessions |
| 8. Persistent Browser CDP | v0.14 | **P1** | Small | Medium | Browser tool |
| 9. Post-Write Delta Lint | v0.13 | **P1** | Small | Medium | Write tool wrapper |
| 10. Checkpoints v2 (Pruning) | v0.13 | **P2** | Medium | Medium | State persistence |
| 11. Platform Allowlists | v0.13 | **P2** | Medium | Low-Med | Config layer |
| 12. Providers as Plugins | v0.13 | **P2** | Large | Medium | Provider system |

---

## P0 — Implement First (This Session / Today)

### 1. File-Mutation Verifier Footer ⭐

**What Hermes does:** After every turn that writes or edits files, the agent gets a short footer summarizing exactly what changed on disk — file paths, line counts, actual delta. Catches cases where writes silently fail or get overwritten.

**Why we need it:** We just hit this bug — the agent said "I updated Pricing.tsx" but the file wasn't actually saved. The mutation verifier would have caught it immediately.

**Implementation:**
- Hook into `write_file` and `edit` tool wrappers
- After successful write, diff against disk to confirm the change landed
- Append a compact footer to the tool result:
  ```
  [MUTATION_VERIFY] 3 files changed: src/pages/Pricing.tsx (+4/-2), ...
  ```
- If diff shows NO change → flag as `MUTATION_FAIL` and retry
- If diff shows unexpected change → flag as `MUTATION_MISMATCH`

**Files to touch:**
- `skills/write_file/` — add verify step
- `skills/edit/` — add verify step
- Core tool result formatter

**Estimated time:** 2-3 hours

---

### 2. LSP Semantic Diagnostics on Every Write ⭐⭐

**What Hermes does:** When agent uses `write_file` or `patch`, Hermes runs a real language server against the edited file and surfaces errors (type errors, undefined symbols, missing imports) before the next turn.

**Why we need it:** We ship broken code downstream and only find out when the build fails or the user complains. Catching errors immediately saves debugging time.

**Implementation:**
- Install `pyright` (Python) + `typescript-language-server` (TS) + `vscode-json-languageserver`
- After every write/edit, spawn the relevant LSP server in single-file mode
- Capture diagnostics, filter to NEW errors only (don't re-report existing)
- Surface as a `[[diagnostic]]` block in the tool result
- If error count > threshold, pause and ask user before continuing

**Files to touch:**
- New skill: `lsp-diagnostic/` or integrate into existing write/edit skills
- `skills/write_file/` — post-write diagnostic hook
- `skills/edit/` — post-patch diagnostic hook

**Estimated time:** 4-6 hours

---

### 3. Lazy-Deps / Debloating ⭐⭐⭐

**What Hermes does:** Heavy backends (Slack SDK, Matrix SDK, image-gen SDKs, voice/TTS providers) install automatically on first use, not upfront. `[all]` extras drops everything covered by lazy-deps.

**Why we need it:** Our install is getting heavy. Every new skill adds dependencies. Nathan shouldn't wait 30 seconds for imports he doesn't use.

**Implementation:**
- Tag each skill with `lazy_deps: ["package1", "package2"]` in `SKILL.md` frontmatter
- On skill load, check if deps are installed. If not, install them.
- Cache installed state in `.clawdeps/` or `~/.openclaw/.lazydeps/`
- `pip install openclaw-agent` should be the PyPI package (long-term)
- For now, make our workspace startup faster by deferring heavy imports

**Files to touch:**
- Skill loader (`skills/__init__.py` or equivalent)
- Each `SKILL.md` — add `lazy_deps` metadata
- Workspace bootstrap scripts

**Estimated time:** 3-4 hours

---

### 4. Cross-Session Prompt Caching (1-Hour TTL) ⭐⭐⭐⭐

**What Hermes does:** System prompt + skills + memory cache for an hour across sessions. Start a `/new` session and the cache is still warm. Background memory review also hits cache.

**Why we need it:** Every new session burns full tokens on system prompt + SOUL.md + USER.md + MEMORY.md + skills. That's $0.02-0.05 per session start that could be cached.

**Implementation:**
- Hash the system prompt + active skills + memory context
- Store hash → prompt prefix in a local cache file (`~/.openclaw/.prompt_cache/`)
- On session start, compute hash, check cache. If hit and <1h old, use cached prefix.
- Include cache metadata in API request (`cache_control: {type: "ephemeral"}` for Anthropic, or equivalent for other providers)
- If cache miss, store result for next session
- Background memory consolidation tasks should reuse cache

**Files to touch:**
- Gateway prompt assembly layer
- Session initialization code
- Memory consolidation jobs

**Estimated time:** 4-5 hours

---

### 5. Kanban Multi-Agent Board — The Big One ⭐⭐⭐⭐⭐

**What Hermes does:** Durable task board where multiple Hermes workers pick up tasks, hand off, and close them. Heartbeats, reclaim, zombie detection, retry budgets, hallucination gate. One install, many kanbans.

**Why we need it:** We already have a task board (`.coordination/tasks/task-board.md`) and a dashboard (`wings/dashboard/`). But the board is static markdown, and the dashboard is in-memory. We need the real thing.

**Implementation (phased):**

**Phase A — Database Backend (Today):**
- Switch dashboard from in-memory to Turso/libSQL (serverless SQLite)
- Schema: `tasks`, `agents`, `worktrees`, `task_assignments`, `task_history`
- Replace polling with WebSocket/SSE for real-time updates

**Phase B — Worker Pool (This Week):**
- Agent heartbeat every 30s → updates `agents.last_heartbeat`
- Task claiming: agent picks up `todo` task, sets `claimed_by` + `started_at`
- Zombie detection: if `last_heartbeat` > 5 min, reclaim task to `todo`
- Retry budget: `max_retries` field, decrement on failure, escalate to `failed` when exhausted

**Phase C — Handoff + Hallucination Gate (Next Sprint):**
- Task handoff: agent A can `handoff_task(task_id, agent_id)` with context transfer
- Hallucination gate: if agent produces output that fails a checksum/validation, auto-retry with different model
- Multi-kanban: `boards` table so we can have separate boards per project

**Files to touch:**
- `wings/dashboard/` — full rewrite of data layer
- `.coordination/tasks/` — migrate from markdown to DB
- New: `wings/dashboard/src/lib/kanban-engine.ts`
- New: `wings/dashboard/src/lib/agent-pool.ts`

**Estimated time:** 12-16 hours (spread across 3 phases)

---

## P1 — This Week

### 6. /goal Target Locking

**What Hermes does:** `/goal` locks the agent onto a target. It stays on task across turns. The "Ralph loop" as a first-class primitive.

**Why we need it:** We lose track mid-conversation. The user says "update the pricing page" and 10 messages later we're talking about Stripe integration. A locked goal would keep us on track.

**Implementation:**
- Add `goal` field to session state
- On every turn, prepend a goal reminder to the system context:
  ```
  [ACTIVE_GOAL] Update pricing display to match Stripe. Do NOT deviate.
  ```
- If agent detects deviation, self-correct or ask for confirmation to change goal
- Goal persists across `/new` sessions (with cache, see #4)
- User can `/goal <text>` to set, `/goal clear` to remove

**Files to touch:**
- Session state management
- Gateway prompt assembly

**Estimated time:** 2-3 hours

---

### 7. Live Session Handoff (/handoff)

**What Hermes does:** `/handoff` moves the active session — every message, tool call, piece of context — to a different model/persona/profile live, without dropping anything.

**Why we need it:** Switch from fast model (kimi-k2p6) to deep reasoning (Claude) mid-debug without losing context. Or hand off from me (Ava) to another agent persona.

**Implementation:**
- Serialize session state (messages, tool calls, file changes, goals) to a portable format
- On `/handoff model=<target>`, inject system event that exports state, then reloads with new model
- Preserve reasoning metadata across the transfer
- Atomic: either full transfer or rollback to previous state

**Files to touch:**
- Gateway session management
- New endpoint or slash command handler

**Estimated time:** 4-6 hours

---

### 8. Persistent Browser CDP Connection

**What Hermes does:** Browser tool uses one persistent DevTools connection instead of spinning up a new session every time. 180x faster.

**Why we need it:** Every `browser` call takes 2-5 seconds. Persistent connection makes it feel instant.

**Implementation:**
- Launch Chrome/Chromium with `--remote-debugging-port=9222` at gateway startup
- Maintain a single CDP WebSocket connection in the browser tool
- Reuse the same browser context (tabs) across calls
- Only spawn new DevTools session on explicit `browser:start`

**Files to touch:**
- Browser tool (`browser` action handling)
- Gateway startup script

**Estimated time:** 2-3 hours

---

### 9. Post-Write Delta Lint (v0.13 Baseline)

**What Hermes does:** After `write_file` + `patch`, run basic syntax lint on Python/JSON/YAML/TOML. Surface errors immediately.

**Why we need it:** Simpler version of #2 (LSP). Catches obvious syntax errors without full language server overhead.

**Implementation:**
- `python -m py_compile <file>` for .py files
- `json.load()` for .json files
- `yaml.safe_load()` for .yaml/.yml files
- `toml.load()` for .toml files
- Surface syntax errors as `[[lint_error]]` blocks
- Run before the more expensive LSP check (#2)

**Files to touch:**
- `skills/write_file/` — add lint step
- `skills/edit/` — add lint step

**Estimated time:** 1-2 hours

---

## P2 — Next Sprint

### 10. Checkpoints v2 (Real Pruning, Disk Guardrails)

**What Hermes does:** State persistence rewritten. Real pruning, disk guardrails, no more orphan shadow repos.

**Why we need it:** Our `_clawmem` and `.cache/` directories grow unbounded. Old session checkpoints and shadow repos accumulate.

**Implementation:**
- Max disk quota for checkpoints (e.g., 1GB)
- Pruning strategy: keep last N sessions + any pinned sessions + last 7 days
- Orphan detection: scan for shadow repos with no parent session
- Auto-archive old sessions to compressed format before deletion

**Files to touch:**
- `_clawmem/` management
- Session persistence layer
- New: `clawmem-prune` CLI or cron job

**Estimated time:** 4-6 hours

---

### 11. Platform Allowlists Everywhere

**What Hermes does:** `allowed_channels` / `allowed_chats` / `allowed_rooms` config across Slack, Telegram, Mattermost, Matrix, DingTalk.

**Why we need it:** We have Telegram allowlist already but it's basic. We need the same for Discord, Slack, etc. as we expand.

**Implementation:**
- Add `allowed_chats` / `allowed_channels` / `allowed_rooms` to each channel config
- Reject messages from unauthorized sources at the gateway level (before they reach the agent)
- Default to deny (secure by default)
- Audit log for rejected attempts

**Files to touch:**
- Gateway channel routing
- Config schema (`config.schema.lookup` or equivalent)

**Estimated time:** 3-4 hours

---

### 12. Providers as Plugins (Pluggable Provider Surface)

**What Hermes does:** `ProviderProfile` ABC + `plugins/model-providers/`. Drop in third-party providers without touching core.

**Why we need it:** We currently hardcode provider configs. If Nathan wants to add a new provider (NovitaAI, local Ollama, etc.), he has to edit core files.

**Implementation:**
- Define `ProviderProfile` abstract base class with methods: `chat()`, `embed()`, `validate_credentials()`
- Load provider plugins from `plugins/model-providers/` directory
- Each plugin: `provider.py` + `config.yaml` + optional `auth.py`
- Core gateway only knows the ABC, not the providers
- Providers self-register on gateway startup

**Files to touch:**
- New: `plugins/model-providers/` directory
- Gateway provider loading logic
- Config schema update

**Estimated time:** 8-10 hours

---

## Implementation Order

### Wave 1 — Safety Net (Today, 4-6 hours)
1. File-Mutation Verifier (#1)
2. Post-Write Delta Lint (#9)
3. LSP Semantic Diagnostics (#2)

**Result:** We stop shipping broken code. Every write is verified + linted + diagnosed.

### Wave 2 — Speed + Cost (This Week, 6-8 hours)
4. Lazy-Deps / Debloating (#3)
5. Cross-Session Prompt Caching (#4)
6. Persistent Browser CDP (#8)

**Result:** Faster startup, cheaper sessions, instant browser calls.

### Wave 3 — Coordination (This Week, 12-16 hours)
7. Kanban Multi-Agent Board Phase A (#5)
8. /goal Target Locking (#6)
9. Live Session Handoff (#7)

**Result:** Real task orchestration. Agents know what they're doing and can hand off cleanly.

### Wave 4 — Architecture (Next Sprint, 12-16 hours)
10. Kanban Multi-Agent Board Phase B+C (#5 continued)
11. Checkpoints v2 (#10)
12. Platform Allowlists (#11)
13. Providers as Plugins (#12)

**Result:** Professional-grade agent infrastructure.

---

## What We DON'T Need

Not everything Hermes does fits our use case:

| Hermes Feature | Skip Reason |
|----------------|-------------|
| xAI Grok / SuperGrok OAuth | Nathan doesn't use xAI |
| Voice cloning (xAI Custom Voices) | Not a priority |
| Google Chat platform | We use Telegram |
| LINE / SimpleX Chat platforms | Wrong markets |
| x_search (Twitter search tool) | We already have research tools |
| 7 i18n locales | English only for now |
| OpenRouter Pareto router | We use specific models |
| Clickable terminal URLs | Nice but not critical |
| Zed ACP Registry | We don't use Zed |
| Microsoft Teams stack | Wrong platform |
| NovitaAI provider | Not needed yet |
| video_generate | Not needed yet |
| computer_use CUA driver | Not needed yet |

---

## Risks & Mitigations

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| LSP integration is brittle | Medium | Start with basic lint (#9) before full LSP |
| Prompt caching not supported by all providers | High | Only enable for Anthropic/OpenAI. Fallback to no-cache for others. |
| Kanban DB migration breaks existing tasks | Medium | Back up `.coordination/tasks/inbox/` before migration |
| Lazy-deps cause import errors mid-task | Low | Install-before-use with timeout + retry |
| Session handoff loses tool context | Medium | Serialize full tool call history + results |

---

## Success Metrics

After Wave 1:
- Zero undetected file write failures
- 100% of broken syntax caught before next turn

After Wave 2:
- Session start time reduced by 30%
- Token cost per new session reduced by 20-40%
- Browser tool calls <500ms (from 2-5s)

After Wave 3:
- Task board has 100% DB persistence (no in-memory)
- Agent deviation from goal detected and corrected within 2 turns
- Session handoff completes without context loss

After Wave 4:
- Multi-agent kanban handles 3+ concurrent agents
- Orphan checkpoints: zero
- New provider added without touching core: <30 min

---

## Next Step

Nathan: **Approve the wave order** or reorder. I can start Wave 1 immediately. The File-Mutation Verifier alone would have caught the Pricing.tsx bug we just hit.

🫡
