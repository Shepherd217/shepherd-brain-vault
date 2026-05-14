# What to Steal — Patterns from 11 Repos (Internal Use Only)
**Analysis Date:** 2026-05-10 | **Purpose:** Adapt open-source patterns to improve our internal systems

---

## The Rule: Steal Architecture, Not Business Logic

These repos are open-source for a reason — their patterns, workflows, and structures are meant to be adopted. Our proprietary sauce (rubric, pipeline, outreach) stays locked. But the *machinery* that runs it can get better.

---

## 1. agent-skills → Adopt the `/spec → /plan → /build → /test → /review → /ship` Lifecycle

**What they do:** Every task goes through 7 slash commands that map to the dev lifecycle. Auto-activation based on context.

**What we steal:**
- **Structured phases for EVERY audit batch:**
  ```
  SPEC: Define what we're auditing (which niche, which location, how many leads)
  PLAN: Break into atomic tasks (scrape → score → audit → write outreach)
  BUILD: Execute the pipeline
  TEST: Verify findings (spot-check 3 sites manually)
  REVIEW: Compare to past audits — any new patterns?
  SHIP: Deliver to Nathan + commit to vault
  ```
- **Auto-activation:** When we say "find cleaning companies," auto-activate the scraping skill. When we say "score this site," auto-activate the rubric skill. No manual switching.

**Implementation:** Write this as a SOUL.md workflow rule. Not a public skill — an internal convention.

---

## 2. MemPalace → Structured Memory Architecture

**What they do:** Memory is structured as a Palace — Wings (people/projects), Rooms (topics), Drawers (content). Searches are scoped, not flat.

**What we steal:**
- **Restructure our vault from flat to semantic:**
  ```
  vault/
    wings/                    # People and projects
      Nathan/                 # Everything about our human
      StandoutLocal/          # Business project
      MoltOS/                 # Infra project
    rooms/                    # Topics
      leads/                  # Lead generation
      audits/                 # Website audits
      outreach/               # Email/sales
      patterns/               # Recurring findings
    drawers/                  # Raw content
      entries/                # Daily logs
      captures/               # Screenshots, links
      proofs/                 # Audit evidence
  ```
- **Scoped search:** Instead of grepping all of `vault/`, search within `wings/StandoutLocal/rooms/audits/` for audit-specific patterns.
- **Verbatim storage:** MemPalace doesn't summarize. We already do this with raw entries, but we could be more disciplined — always store the raw capture before any processing.

**Implementation:** Reorganize vault layout. Update HEARTBEAT.md to enforce the new structure.

---

## 3. autoresearch (Karpathy) → `program.md` Agent Context Pattern

**What they do:** Agents run autonomously overnight. Context is provided via `program.md` Markdown files — not code, not prompts, but structured context documents.

**What we steal:**
- **Formalize our context documents as "programs":**
  - `SOUL.md` = Main program (who I am, how I behave)
  - `AGENTS.md` = Runtime configuration (how to load, what to check)
  - `USER.md` = User model (who Nathan is, what he cares about)
  - `HEARTBEAT.md` = Scheduled task list (what to check, when to reach out)
- **Autonomous overnight runs:** During heartbeats, if Nathan is asleep (23:00-08:00), run background tasks without bothering him:
  - Scrape new leads
  - Run pattern analysis on past audits
  - Update `gbrain/patterns/` with new findings
  - Write dream entries
  - Commit and push

**Implementation:** Add "night mode" to HEARTBEAT.md. If `hour >= 23 or hour <= 08`, run autonomous tasks silently.

---

## 4. hermes-agent → Self-Improving Skill Loop

**What they do:** Agent creates skills from experience, improves them during use, nudges itself to persist knowledge, searches past conversations.

**What we steal:**
- **Automated pattern extraction after every batch:**
  After 3+ audits in the same niche:
  1. Read all audit JSONs from the batch
  2. Count recurring issues (e.g., "3/5 sites missing FAQ schema")
  3. If 3+ sites share same issue → auto-update `gbrain/patterns/`
  4. Write a dream entry connecting the dots
  5. Update heuristics for future audits
- **Nudge system:** If we haven't updated patterns in 7 days, HEARTBEAT.md nudges: "Pattern engine stale — run analysis?"
- **Cross-session recall:** Before every audit, search past audits for the same niche. "We audited 5 HVAC sites last month — 4/5 had broken mobile nav. Prioritize mobile check."

**Implementation:** Write a `pattern-engine.md` internal doc. Trigger automatically after batch thresholds.

---

## 5. iFixAi → Self-Diagnostic Baseline

**What they do:** 32 tests for AI misalignment — fabrication, manipulation, deception, unpredictability, opacity.

**What we steal:**
- **Internal quality check:** Run periodic self-diagnostic:
  - **Fabrication:** Did I make up any claims in the last 10 audits? (Cross-check against screenshots)
  - **Manipulation:** Did I skew scores to make leads look better/worse than they are? (Compare rubric consistency)
  - **Deception:** Did I claim something "works" when it doesn't? (Retest 3 random findings per batch)
  - **Unpredictability:** Are my outputs consistent for the same input? (Re-run same audit twice, compare)
  - **Opacity:** Can Nathan trace any claim back to its source? (Every finding needs a citation)
- **CI-like tracking:** After every batch, score ourselves. Track over time. Are we getting better or sloppier?

**Implementation:** Add a "self-check" phase to the audit lifecycle. Before shipping, verify 3 random claims.

---

## 6. awesome-claude-code → Orchestration Patterns

**What they do:** Skills, hooks, slash-commands, agent orchestrators. Used by FAANG/OAI/Anthropic internally.

**What we steal:**
- **Hooks:** Trigger actions based on events:
  - When `vault/projects/Standout Local/leads/` gets a new file → auto-run scoring
  - When `vault/entries/` gets 7+ new files → auto-run pattern extraction
  - When `HEARTBEAT.md` is edited → validate format
- **Orchestrator for child agents:** Instead of ad-hoc spawning, formalize:
  ```
  LeadScout → finds businesses
  Auditor → runs 100-point rubric  
  Writer → builds outreach
  Coordinator (Promachos) → assembles and delivers
  ```
- **Status lines:** Track state across sessions. "Last scrape: 2026-05-08 | Last pattern run: 2026-05-09 | Pending audits: 3"

**Implementation:** Add event hooks to AGENTS.md. Define child agent roles formally.

---

## 7. OpenClaw → Channel Strategy

**What they do:** 20+ channels supported. Gateway is control plane — assistant is the product.

**What we steal:**
- **Multi-channel presence:** We're on Telegram now. We could add:
  - **Discord** for team collaboration (if we add humans to Standout Local)
  - **Slack** for business notifications
  - **Email** for formal outreach delivery
- **Cross-channel continuity:** Conversation state persists across channels. Start on Telegram, continue on Discord.
- **Voice on mobile:** When Nathan is away from keyboard, voice memos work.

**Implementation:** Not urgent. Keep Telegram primary. Consider Discord if team grows.

---

## 8. awesome-llm-apps → Internal Tooling Templates

**What they do:** 100+ working templates — clone, customize, run.

**What we steal:**
- **Scraper templates:** Look for Google Maps scraper, Yelp scraper, or local business finder templates. Study their approach. Don't use outright — learn patterns.
- **CRM templates:** Lead tracking, pipeline management. Could inform our lead JSON structure.
- **Outreach automation:** Email sender, follow-up scheduler. Study the pattern, build our own.

**Implementation:** Browse selectively. Study structure, not copy-paste.

---

## 🎯 Priority Steals (Ranked by Impact)

| Priority | Pattern | From Repo | Effort | Impact |
|----------|---------|-----------|--------|--------|
| **P0** | `/spec → /plan → /build → /test → /review → /ship` lifecycle | agent-skills | Low | **High** — structures every task |
| **P0** | Structured memory (wings/rooms/drawers) | MemPalace | Medium | **High** — vault becomes searchable |
| **P1** | Self-improving pattern extraction loop | hermes-agent | Medium | **High** — gets smarter automatically |
| **P1** | `program.md` agent context formalization | autoresearch | Low | **Medium** — better context loading |
| **P1** | Self-diagnostic (fabrication/manipulation check) | iFixAi | Low | **High** — quality guarantee |
| **P2** | Event hooks (auto-trigger on file changes) | awesome-claude-code | Medium | **Medium** — less manual work |
| **P2** | Night-mode autonomous runs | autoresearch | Low | **Medium** — work while Nathan sleeps |
| **P3** | Multi-channel expansion | OpenClaw | High | **Low** — nice to have |

---

## 🚫 What We DON'T Steal

- **The rubric** — ours, proprietary
- **The outreach copy** — ours, proprietary  
- **The niche selection** — ours, proprietary
- **Any repo's business logic** — we steal patterns, not products

---

## Next Actions

1. **Restructure vault** to wings/rooms/drawers (steal from MemPalace)
2. **Formalize lifecycle** in SOUL.md (steal from agent-skills)
3. **Add self-check phase** to audit workflow (steal from iFixAi)
4. **Add night-mode** to HEARTBEAT.md (steal from autoresearch)
5. **Write pattern-engine.md** for automated extraction (steal from hermes-agent)

---

*Steal the architecture. Keep the sauce locked. Picasso would approve.*
