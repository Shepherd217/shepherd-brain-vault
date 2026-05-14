# The Palace — Vault Structure Guide
**Inspired by:** MemPalace's wings/rooms/drawers architecture  
**Date:** 2026-05-10 | **Branch:** palace-restructure

---

## Philosophy

The vault is a **Palace** — not a filing cabinet.

- **Wings** are people and projects (who/what we care about)
- **Rooms** are topics and workflows (how we think about things)
- **Drawers** are raw content and evidence (what we captured)

Searches are **scoped**, not flat. Find "all audit patterns for cleaning companies" in `rooms/patterns/` without grepping the entire vault.

---

## Directory Map

### wings/ — People and Projects

| Directory | What Lives Here |
|-----------|-----------------|
| `wings/Nathan/` | Everything about our human. `marrow/` (soul, user, memory, lessons). `SYSTEM_STATUS.md`, `PROJECT_HEAT_MAP.md`, `CLI_Toolkit.md` |
| `wings/StandoutLocal/` | The business. `LEAD_SYSTEM.md`, `m0h-method-adaptation.md`, `leads/` (raw lead data), `templates/` (outreach templates) |
| `wings/MoltOS/` | Agent infrastructure. All API testing reports, endpoint maps, executive summaries |
| `wings/OpenClaw/` | Platform-level configs. `Hatchly/`, `Paperclip/`, `ThirtyDays/`, `TuneFrames/` projects |

**Rule:** If it's about a specific person or project, it goes in a wing.

---

### rooms/ — Topics and Workflows

| Directory | What Lives Here |
|-----------|-----------------|
| `rooms/audits/` | Audit methodology, rubric documentation, scoring guides |
| `rooms/leads/` | Lead generation workflows, scraping guides, prospecting methods |
| `rooms/outreach/` | Email templates, call scripts, objection handling, sales methodology |
| `rooms/patterns/` | Recurring findings across audits. Updated automatically after every batch |
| `rooms/skills/` | Internal skill definitions. How we do things |
| `rooms/memory/` | Long-term memory architecture. `README.md` from old `gbrain/` |
| `rooms/testing/` | Testing frameworks, API test patterns, QA methodology |

**Rule:** If it's a topic or workflow that spans multiple wings, it goes in a room.

---

### drawers/ — Raw Content and Evidence

| Directory | What Lives Here |
|-----------|-----------------|
| `drawers/entries/` | Daily raw logs. What happened, unfiltered |
| `drawers/diaries/` | Curated reflections. Processed entries with insight |
| `drawers/dreams/` | Pattern syntheses. Cross-time connections we found |
| `drawers/feelings/` | Emotional state tracking. Felt_as entries |
| `drawers/captures/` | Incoming captures. Links, screenshots, raw data, inbox items |
| `drawers/proofs/` | Audit evidence. Screenshots, JSON exports, verification data |

**Rule:** If it's raw, unprocessed, or evidentiary, it goes in a drawer.

---

## How to Navigate

### Finding Something by Person/Project
→ Start in `wings/{name}/`

Example: "What do we know about MoltOS auth bugs?"  
→ `wings/MoltOS/` → `FINAL-REPORT-2026-05-10.md`

### Finding Something by Topic
→ Start in `rooms/{topic}/`

Example: "What's our pattern for cleaning company websites?"  
→ `rooms/patterns/` → `standout-local-cleaning.md`

### Finding Raw Evidence
→ Start in `drawers/{type}/`

Example: "Show me the audit screenshots from last week"  
→ `drawers/proofs/` → `2026-05-08-screenshots/`

### Adding New Content
1. **Raw capture** (link, screenshot, note) → `drawers/captures/`
2. **Processed insight** (pattern found, lesson learned) → `rooms/patterns/` or `drawers/diaries/`
3. **Project-specific** (Standout Local lead, MoltOS bug) → `wings/{project}/`

---

## Special Directories (Top Level)

| Directory | Purpose |
|-----------|---------|
| `bookmarks/` | Bookmarked external content (X posts, articles, repos) |
| `CLAUDE.md` | Claude-specific configuration (keep as-is) |
| `ingest-capture.js` | Capture ingestion script (keep as-is) |

---

## Migration Notes

**Old → New mapping:**

| Old Path | New Path |
|----------|----------|
| `entries/` | `drawers/entries/` |
| `diaries/` | `drawers/diaries/` |
| `gbrain/dreams/` | `drawers/dreams/` |
| `gbrain/patterns/` | `rooms/patterns/` |
| `feelings/` | `drawers/feelings/` |
| `inbox/` | `drawers/captures/` |
| `notes/` | `drawers/entries/` |
| `projects/MoltOS/` | `wings/MoltOS/` |
| `projects/Standout Local/` | `wings/StandoutLocal/` |
| `projects/Shepherd's Brain/` | `wings/Nathan/` |
| `marrow/` | `wings/Nathan/marrow/` |

---

## Automation Rules

### After Every Audit Batch (3+ sites)
1. Read `drawers/entries/` (last 7 days)
2. Count recurring issues
3. If 3+ sites share same issue → update `rooms/patterns/`
4. Write `drawers/dreams/YYYY-MM-DD.md`
5. Commit and push

### Weekly Heartbeat
1. Check `wings/{project}/` for stale files (>30 days)
2. Archive or update as needed
3. Review `rooms/patterns/` for stale patterns
4. Update `wings/Nathan/marrow/memory.md` with distilled learnings

### Night Mode (23:00-08:00)
1. Run pattern extraction on recent captures
2. Commit and push vault changes
3. Update cross-references between wings and rooms

---

*Palace restructure completed 2026-05-10. Inspired by MemPalace. Built for speed.*
