# ClawMem Directory Structure

**Created:** 2026-05-13
**Agent:** Ava
**Purpose:** Cross-agent shared memory layer

## Directory Layout

```
_clawmem/
├── user/                    # Persistent cross-agent memories
│   ├── profile.md           # Nathan's static + dynamic profile
│   ├── preferences/         # Extracted preferences
│   └── entities/            # Named entities (people, services, repos)
├── agent/                   # Session-derived operational notes
│   ├── observations/        # Decisions + observations from transcripts
│   ├── handoffs/            # Session summaries with next steps
│   └── antipatterns/        # Accumulated negative patterns
├── resources/               # Static knowledge (no decay)
│   └── static-knowledge/
└── rooms/patterns/          # Recurring insights (auto-extracted)
```

## Rules
- **user/** — Only Nathan or manual edits (persists across all agents)
- **agent/** — Auto-generated from sessions (DO NOT EDIT manually)
- **resources/** — Static knowledge, no recency decay
- **rooms/patterns/** — Pattern extraction from sessions

## Integration
- ClawMem MCP server: `/root/clawmem/bin/clawmem mcp`
- OpenClaw workspace collection: `openclaw-workspace`
- Database: `/root/.cache/clawmem/index.sqlite`

## Status
- ✅ ClawMem installed
- ✅ MCP server registered
- ✅ Workspace indexed (175 docs)
- ⏳ Embeddings pending (172 unembedded)
- ⏳ OpenClaw native plugin — manual setup needed

---
*ClawMem Phase 1 complete | Ava | 2026-05-13*
