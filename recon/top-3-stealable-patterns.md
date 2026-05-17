# Stealable Patterns — Top 3 Repo Dissection

> Analysis of: agentmemory, mattpocock/skills, CloakBrowser
> For: Nathan Shepherd's brain vault architecture
> Date: 2026-05-17

---

## 🥇 REPO 1: agentmemory — The Memory Engine

### Architecture Overview
agentmemory is a **stateless memory server** that sits between AI agents and their context windows. No database required — everything is in-memory KV with optional persistence. It captures observations from agent tool use, compresses them, indexes them (BM25 + vector hybrid), and retrieves the most relevant context when the agent asks.

**Key stat:** 95.2% retrieval accuracy, ~170K tokens/year vs 19.5M+ without memory. 92% token reduction.

---

### 🔥 PATTERN 1: Zero-LLM Synthetic Compression
**File:** `src/functions/compress-synthetic.ts`

The DEFAULT compression path uses **pure heuristics** — no API calls, no token burn. It infers observation type from hook type + tool name, extracts files from tool input, and builds a narrative from prompt + input + output concatenation.

**Steal this if:** You want memory without API costs. The heuristic type inference alone is gold:
- `post_tool_failure` → type: "error"
- `prompt_submit` → type: "conversation"  
- tool name matching "fetch/http/web" → type: "web_fetch"
- tool name matching "bash/shell/exec" → type: "command_run"
- tool name matching "edit/update/patch" → type: "file_edit"

**The insight:** Most observations don't need LLM summarization. Structured heuristics get you 80% of the value at 0% of the cost. LLM compression is opt-in (`AGENTMEMORY_AUTO_COMPRESS=true`).

**How to adapt for your vault:**
- Add a `synthetic_compress()` function to your brain that classifies observations by tool/hook type
- Use regex/tool-name matching for type inference
- Build narrative from `prompt | input | output` with token-safe truncation (400 char cap)
- Only trigger LLM compression for high-importance observations (errors, decisions, architectural changes)

---

### 🔥 PATTERN 2: Hybrid Search (BM25 + Vector) with Token Budgeting
**File:** `src/functions/search.ts`, `src/state/hybrid-search.ts`, `src/state/vector-index.ts`

Search uses **two indexes in parallel:**
1. **BM25** — inverted text index for exact/semantic word matching (fast, cheap, works offline)
2. **Vector** — embedding-based semantic search (catches conceptual similarity)

Search results are scored, merged, then **token-budgeted** before returning to the agent. No more context window overflow.

**Key implementation details:**
- BM25 is built in-memory from observations on startup (rebuildIndex)
- Vector index is optional — falls back to BM25-only if no embedding provider
- Token budget: estimates tokens as `JSON.stringify(value).length / 3`
- Format options: `full` (complete observation), `compact` (metadata only), `narrative` (text summary)
- Over-fetch when filtering by project/cwd (`fetchLimit = effectiveLimit * 10`)

**Steal this if:** You want fast, cheap memory retrieval without dependency on embedding APIs.

**How to adapt for your vault:**
- Implement BM25 indexing for your memory entries (stemming + inverted index)
- Add a lightweight vector index as optional enhancement
- Token-budget search results before injecting into agent context
- Support multiple return formats based on agent needs
- Cache session metadata (project, cwd) for filtering

---

### 🔥 PATTERN 3: Scoped KV State (No Database)
**File:** `src/state/kv.ts`, `src/state/schema.ts`

Memory is organized into **scopes** within a simple KV store:
- `sessions` — session metadata (project, cwd, timestamps)
- `observations/{sessionId}` — per-session observations (auto-captured)
- `memories` — cross-session memories (explicit `mem::remember` calls)

No Postgres, no Redis, no SQLite. Just KV with optional file persistence.

**Steal this if:** You want zero-dependency persistence.

**How to adapt for your vault:**
- Use your existing file-based storage (vault drawers)
- Namespace by scope: `drawers/sessions/`, `drawers/observations/{session}/`, `drawers/memories/`
- Keep session metadata separate from observations for fast filtering
- Memory entries = explicit, high-value facts the user wants preserved across sessions
- Observation entries = auto-captured, per-session, subject to retention/decay

---

### 🔥 PATTERN 4: Stateless Index Rebuild
**File:** `src/functions/search.ts` → `rebuildIndex()`

On startup, if the search index is empty, it **rebuilds from scratch** by walking all KV scopes. No index persistence needed. This means:
- Zero index maintenance
- No index corruption issues
- Always consistent with KV store
- Startup cost is the only penalty (acceptable for personal agent scale)

**How to adapt:** Rebuild your brain's index from vault files on each startup. For Nathan's scale (~20 tools, 2 months work), this is trivial.

---

### 🔥 PATTERN 5: Hook-Based Observation Capture
**File:** `src/hooks/`

agentmemory captures observations by hooking into agent lifecycle:
- `post_tool_use` — what tool was called, with what input, what output
- `post_tool_failure` — errors (automatically high importance)
- `prompt_submit` — user prompts (conversation context)
- `subagent_stop` / `task_completed` — subagent results

**The insight:** Don't ask the agent to remember. Just observe what it does.

**How to adapt for your vault:**
- Wrap your tool calls with an observation logger
- Auto-capture: tool_name, input, output, timestamp, session_id
- Classify by hook type (success vs failure vs conversation)
- Store in session-scoped observations

---

### 🔥 PATTERN 6: Provider Fallback Chain with Circuit Breaker
**File:** `src/providers/fallback-chain.ts`, `src/providers/circuit-breaker.ts`

LLM providers fail. The fallback chain tries providers in order with circuit breaker protection:
- If a provider fails N times in a window, it's temporarily removed from rotation
- When it comes back, it gradually re-enters (health check)
- Configurable via `FALLBACK_PROVIDERS=anthropic,openai,gemini`

**How to adapt:** If you use multiple LLM providers for compression/enrichment, add fallback logic. For a solo dev, this is nice-to-have, not critical.

---

### 🔥 PATTERN 7: Retention & Auto-Forget
**File:** `src/functions/auto-forget.ts`, `src/functions/retention.ts`

Not all observations deserve to live forever:
- **Decay:** Observations lose importance over time (default: 30 days)
- **Access tracking:** Frequently recalled observations get boosted
- **Auto-forget:** Low-importance, unaccessed observations are purged
- **Consolidation:** Multiple related observations can be merged into one memory

**How to adapt:**
- Add `last_accessed` and `access_count` to your memory entries
- Run a periodic cleanup task (cron) that decays importance scores
- Delete observations below a threshold (e.g., importance < 2, untouched for 7 days)
- Consolidate: if 5+ observations mention the same file/decision, merge them into a memory

---

## 🥈 REPO 2: mattpocock/skills — The Skill Architecture

### Architecture Overview
Matt Pocock's skills are **small, composable, model-agnostic slash commands** loaded by Claude Code. Each skill is a focused behavior pattern (grilling, TDD, diagnosis) with a standard format. Skills are organized into buckets and consumed by per-repo configuration.

**Key insight:** Small skills > big frameworks. Each skill solves ONE failure mode.

---

### 🔥 PATTERN 1: CONTEXT.md — Shared Domain Language
**File:** `CONTEXT.md` (in every repo)

This is the **single most powerful pattern** in the entire skills repo. A `CONTEXT.md` file lives at the root of every project and defines:
1. **Glossary** — precise definitions of domain terms (e.g., "Issue tracker", "Triage role")
2. **Relationships** — how terms relate (e.g., "Issue tracker holds many Issues")
3. **Flagged ambiguities** — terms that were previously overloaded and have been resolved

**Example impact:**
- BEFORE: "There's a problem when a lesson inside a section of a course is made 'real' (i.e. given a spot in the file system)"
- AFTER: "There's a problem with the materialization cascade"

The agent now speaks your project's language. This cuts token usage, reduces misalignment, and makes the agent's output sound like it belongs in your codebase.

**How to adapt for your vault:**
- Create `vault/CONTEXT.md` defining your domain language
- Define terms: "Drawer", "Pattern", "Signal", "Dream", "Relay", "Mesh"
- Document relationships: "A Drawer contains Patterns. A Pattern can spawn Dreams."
- Flag ambiguities: "'Task' was previously used for both todo items and coordination jobs — resolved: 'Task' = todo item; 'Job' = coordination unit"
- Update it as your vocabulary evolves

---

### 🔥 PATTERN 2: ADR (Architecture Decision Records)
**File:** `docs/adr/0001-example.md`

Only create an ADR when ALL THREE are true:
1. **Hard to reverse** — changing your mind later costs something
2. **Surprising without context** — a future reader will wonder "why?"
3. **Result of a real trade-off** — you considered alternatives and picked one

**Format:**
```markdown
# ADR-0001: [Title]

## Context
[What forced this decision]

## Decision
[What we decided]

## Consequences
[What this enables and what it costs]
```

**How to adapt:**
- Create `vault/docs/adr/` for architectural decisions
- Document why you chose file-based over DB-based storage
- Document why you chose hybrid search over pure vector
- Keep it minimal — only when the decision is genuinely non-obvious

---

### 🔥 PATTERN 3: /grill-with-docs — Alignment Before Action
**File:** `skills/engineering/grill-with-docs/SKILL.md`

Before building ANYTHING, the agent grills the user with questions:
- Walk down each branch of the design tree
- Resolve dependencies between decisions one-by-one
- Challenge against existing glossary ("Your CONTEXT.md defines X as...")
- Sharpen fuzzy language ("You said 'account' — do you mean Customer or User?")
- Stress-test with concrete scenarios
- Update CONTEXT.md inline as terms are resolved

**The insight:** Misalignment is the #1 failure mode. 5 minutes of grilling saves 2 hours of re-work.

**How to adapt:**
- Before any major vault feature, run an alignment session
- Ask: "What does X mean in your context?" for every ambiguous term
- Update CONTEXT.md as you go
- Don't batch — capture definitions as they crystallize

---

### 🔥 PATTERN 4: /tdd — Vertical Slice Tracer Bullets
**File:** `skills/engineering/tdd/SKILL.md`

**WRONG (horizontal slicing):**
- Write ALL tests first, then ALL implementation
- Tests test imagined behavior, not actual behavior

**RIGHT (vertical slicing / tracer bullets):**
- Write ONE test for ONE behavior
- Implement minimal code to pass
- Repeat

Each cycle: RED → GREEN → next test. Only refactor when ALL tests pass.

**How to adapt:**
- When building brain vault features, use vertical slices
- "Add BM25 search" → write one search test → implement index → test passes → next slice
- Never write tests for behavior you haven't implemented yet
- Tests should verify through public interfaces, not mock internals

---

### 🔥 PATTERN 5: /diagnose — The Feedback Loop Obsession
**File:** `skills/engineering/diagnose/SKILL.md`

Six-phase debugging discipline:
1. **Build feedback loop** — A fast, deterministic pass/fail signal for the bug. Spend disproportionate effort here. Be creative. Refuse to give up.
2. **Reproduce** — Run the loop. Confirm the failure matches what the user described.
3. **Hypothesize** — Generate 3-5 ranked hypotheses BEFORE testing any. Each must be falsifiable: "If X is the cause, then changing Y will fix it."
4. **Instrument** — One probe per hypothesis prediction. Tag debug logs with unique prefix `[DEBUG-a4f2]`.
5. **Fix + regression test** — Write regression test BEFORE the fix (if you have a correct seam).
6. **Cleanup + post-mortem** — Remove all `[DEBUG-...]` logs. Ask: "What would have prevented this?"

**How to adapt:**
- When your brain vault has bugs, build a feedback loop first
- For search issues: a test script that queries and asserts results
- For memory issues: a script that stores → retrieves → asserts match
- Never proceed to hypothesis without a loop you believe in

---

### 🔥 PATTERN 6: /improve-codebase-architecture — Periodic Rescue
**File:** `skills/engineering/improve-codebase-architecture/SKILL.md`

Run this once every few days. The agent:
- Scans for deepening opportunities (small interface, deep implementation)
- Checks for code that doesn't match the domain language in CONTEXT.md
- Flags modules that have become shallow (wide interface, simple implementation)
- Suggests refactors based on ADRs

**How to adapt:**
- Weekly: run an architecture check on your vault
- Is `drawers/` still the right structure?
- Are patterns getting too shallow?
- Does the code match your CONTEXT.md language?

---

## 🥉 REPO 3: CloakBrowser — The Stealth Engine

### Architecture Overview
CloakBrowser is a thin wrapper around a **patched Chromium binary** with 49 source-level C++ patches. It passes every bot detection test by being a REAL browser, not by faking one with JavaScript injection.

**Key stat:** reCAPTCHA v3 score 0.9 (human-level). Passes Cloudflare Turnstile, FingerprintJS, BrowserScan.

---

### 🔥 PATTERN 1: Source-Level Integration Beats Surface Patching
**Files:** `config.py` (IGNORE_DEFAULT_ARGS, get_default_stealth_args)

Every other stealth tool patches at the surface:
- `playwright-stealth` → JavaScript injection (detectable)
- `undetected-chromedriver` → config flags (breaks on Chrome updates)

CloakBrowser patches Chromium **at the C++ source level** — canvas, WebGL, audio, fonts, GPU, screen, WebRTC, network timing, automation signals. Compiled into the binary. Detection sites see a real browser because it IS a real browser.

**The insight:** Deep integration beats surface hacks. Every. Single. Time.

**How to adapt (conceptually, not literally — you're not patching Chromium):**
- When integrating with external systems, go deeper than config
- If you need to "look human" to some API, understand what signals it checks
- Don't just rotate user agents — understand WHY user agents matter
- If you're building agent behaviors, model them on real human behavior patterns, not just surface mimicry

---

### 🔥 PATTERN 2: Humanize Engine with Configurable Presets
**File:** `cloakbrowser/human/config.py`, `cloakbrowser/human/actionability.py`

The `humanize=True` flag adds human-like behavior:
- **Mouse:** Bézier curves with wobble, overshoot, burst movements
- **Keyboard:** Per-character typing with variable delay, occasional pauses, typo simulation
- **Scroll:** Acceleration/deceleration curves, overshoot-and-settle, variable delta
- **Timing:** Random delays between actions, idle micro-movements

**Two presets:**
- `default` — normal human speed (~70ms/char typing)
- `careful` — slower, more deliberate (~100ms/char, longer pauses)

**Per-call overrides:** Any parameter can be overridden per interaction:
```python
page.type(selector, text, human_config={"typing_delay": 150, "mistype_chance": 0.05})
```

**How to adapt for your agent:**
- If your agent interacts with systems that check behavioral patterns (rare for APIs, common for scraping), model human-like timing
- Add configurable "personality presets" for your agent's behavior
- Nathan-mode: fast, direct, minimal delays
- Stealth-mode: slower, more varied, human-like curves
- This matters more for browser automation than for API calls

---

### 🔥 PATTERN 3: Fingerprint Randomization Per Launch
**File:** `config.py` → `get_default_stealth_args()`

Every browser launch gets a **random fingerprint seed**:
```python
seed = random.randint(10000, 99999)
base = ["--no-sandbox", f"--fingerprint={seed}"]
```

Hardware concurrency, device memory, screen size, window size, GPU — all auto-generated from the seed. Platform-aware (Mac runs as native Mac, Linux/Windows get Windows profile).

**How to adapt:**
- If your agent uses external identity (API keys, tokens), rotate/request identifiers per session
- Don't reuse the same fingerprints/identifiers across sessions
- Per-session randomization reduces tracking/profile building

---

### 🔥 PATTERN 4: Persistent Profiles for Session Continuity
**File:** `browser.py` → `launch_persistent_context()`

Browser profiles persist across sessions:
- Cookies survive restarts
- localStorage is preserved
- Cache accumulates (looks more human over time)
- Bypasses incognito detection

**How to adapt for your vault:**
- Your vault ALREADY does this with file-based storage
- Ensure session state (auth tokens, preferences) persists across agent restarts
- The more "history" your agent accumulates, the more natural it appears

---

### 🔥 PATTERN 5: Binary Auto-Download with Integrity Verification
**File:** `download.py`

First launch auto-downloads the correct binary for the platform:
- Detects platform → maps to tag (`linux-x64`, `darwin-arm64`, etc.)
- Downloads from CDN with GitHub fallback
- Verifies SHA-256 checksum
- Caches locally (`~/.cloakbrowser/`)
- Supports override via `CLOAKBROWSER_BINARY_PATH`

**How to adapt:**
- If you distribute tools/binaries, implement auto-download with platform detection
- Always verify integrity (checksums)
- Provide env override for power users
- Cache aggressively — only check for updates periodically

---

### 🔥 PATTERN 6: Cleanup Patching (Resource Management)
**File:** `browser.py` (all launch functions)

Every launch patches the browser's `close()` method to also stop the Playwright instance:
```python
_original_close = browser.close

def _close_with_cleanup():
    try:
        _original_close()
    finally:
        pw.stop()

browser.close = _close_with_cleanup
```

This prevents resource leaks. Even if the user forgets to stop Playwright, it's cleaned up.

**How to adapt:**
- Always ensure your cleanup runs, even on exceptions
- Use `try/finally` or context managers for resource cleanup
- If you spawn subprocesses (git, curl, etc.), ensure they get killed on exit
- Add cleanup hooks to your agent's shutdown sequence

---

## 🏁 Integration Plan — What to Build This Week

### Immediate (Day 1-2)
1. **CONTEXT.md** — Create `vault/CONTEXT.md` with your domain language
2. **Synthetic compression** — Add heuristic observation compression to your brain
3. **BM25 search** — Implement basic text indexing for memory retrieval

### Short-term (Week 1)
4. **Hybrid search** — Add optional vector search as enhancement
5. **Hook capture** — Auto-capture tool observations without explicit logging
6. **Retention rules** — Add decay + auto-forget for old observations
7. **Skill structure** — Format your existing tools as composable skills

### Medium-term (Month 1)
8. **ADR docs** — Document key architectural decisions
9. **Grill mode** — Add alignment grilling before major features
10. **TDD discipline** — Vertical slice testing for new features
11. **Architecture checks** — Weekly scans for deepening opportunities

---

## 💡 The Meta-Pattern

All three repos share one philosophy:

> **Small, focused, composable primitives that solve one problem well.**

- agentmemory: One memory server, one search function, one compression heuristic
- skills: One skill per failure mode, composable via slash commands
- CloakBrowser: One patched binary, one humanize flag, one profile manager

**Your vault should work the same way.**

Don't build a monolithic brain. Build:
- A memory indexer (one job)
- A pattern recognizer (one job)
- A signal dispatcher (one job)
- A dream generator (one job)

Each does ONE thing. Compose them. That's how these repos got 6K-18K stars in a week.

---

*End of dissection. Ready to implement.* ⚡
