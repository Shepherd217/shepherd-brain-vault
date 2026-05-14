---
date: 2026-05-11
source: https://github.com/rohitg00/agentmemory
stars: trending
author: rohitg00
---

# AgentMemory — Research Notes

## What It Is
Persistent memory engine for AI coding agents. Captures every tool use, compresses into structured memory, and injects relevant context at session start.

**Built on:** iii-engine (infrastructure)
**License:** Apache-2.0
**Install:** `npx @agentmemory/agentmemory`

---

## Core Architecture

### Memory Pipeline
```
PostToolUse hook fires
  ↓
SHA-256 dedup (5min window)
  ↓
Privacy filter (strip secrets, API keys)
  ↓
Store raw observation
  ↓
LLM compress → structured facts + concepts + narrative
  ↓
Vector embedding (local or API)
  ↓
Index in BM25 + vector
```

### 4-Tier Memory Model
| Tier | What | Analogy |
|------|------|---------|
| Working | Raw observations from tool use | Short-term memory |
| Episodic | Compressed session summaries | "What happened" |
| Semantic | Extracted facts and patterns | "What I know" |
| Procedural | Workflows and decision patterns | "How to do it" |

### Hybrid Search (Triple-Stream)
1. **BM25** — Stemmed keyword matching with synonym expansion
2. **Vector** — Cosine similarity over dense embeddings
3. **Graph** — Knowledge graph traversal via entity matching
4. **Fusion** — Reciprocal Rank Fusion (RRF, k=60)

---

## Key Patterns to Steal

### 1. Automatic Capture via Hooks
**What:** 12 hooks capture everything without manual effort
**Hooks:** SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, PostToolUseFailure, PreCompact, SubagentStart/Stop, Stop, SessionEnd

**Steal for Midas:**
- Add automatic session capture to HEARTBEAT.md
- After every tool use, compress observation into vault
- Currently we write manually — this automates it

### 2. Privacy Filter
**What:** Strips secrets, API keys, `<private>` tags before storage
**Steal for Midas:** Already in SOUL.md (no tokens in files), but could formalize a regex stripper

### 3. Memory Lifecycle (Decay + Auto-Forget)
**What:** Memories decay over time (Ebbinghaus curve). Frequently accessed = strengthen. Stale = auto-evict. Contradictions detected and resolved.
**Steal for Midas:** Weekly vault cleanup already exists, but could add:
- Auto-archive files not accessed in 90 days
- Detect contradictions in MEMORY.md (old vs new preferences)
- Importance scoring for entries

### 4. Knowledge Graph
**What:** Entity extraction + BFS traversal
**Steal for Midas:** Could extract entities from vault entries and build a graph of connections
- Nathan → Standout Local → leads → audits → outreach
- Patterns → tools → builds → commits

### 5. Cross-Agent Memory Sharing
**What:** MCP + REST API lets any agent access the same memory
**Steal for Midas:** ClawFS already does this, but agentmemory has:
- Real-time sync
- Team memory with namespaces
- Lease-based exclusive access (multi-agent coordination)

### 6. Token Budget Injection
**What:** Only injects top-K memories within token budget (default 2000)
**Steal for Midas:** Our context windows are large but could benefit from selective loading
- Load only relevant wings/ files based on current task
- Skip drawers/ unless explicitly requested

### 7. Real-Time Viewer
**What:** Port 3113 shows live observation stream, session explorer, memory browser
**Steal for Midas:** Dashboard is static. Could add:
- Live git status viewer
- Real-time vault change stream
- Active build progress

---

## Integration with OpenClaw

agentmemory HAS an OpenClaw integration:
- **MCP server:** 51 tools available
- **Plugin:** `plugins.slots.memory = "agentmemory"`
- **Path:** `integrations/openclaw` in repo

**MCP Config:**
```json
{
  "mcpServers": {
    "agentmemory": {
      "command": "npx",
      "args": ["-y", "@agentmemory/mcp"]
    }
  }
}
```

**OpenClaw plugin path:** `~/.openclaw/extensions/agentmemory`

---

## Benchmarks

| Metric | agentmemory | BM25-only | Built-in (CLAUDE.md) |
|--------|-------------|-----------|----------------------|
| R@5 (retrieval) | 95.2% | 86.2% | N/A |
| Tokens/year | ~170K | ~650K | 19.5M+ |
| Cost/year | ~$10 | ~$500 | Impossible |
| Scale | Unlimited | Unlimited | 200-line cap |
| Cross-agent | Yes | No | No |

---

## Verdict: MAXIMUM

**Why MAXIMUM:**
1. Direct OpenClaw integration exists (not theoretical)
2. Solves our #1 friction: manual memory writing
3. Hybrid search (BM25 + vector + graph) is strictly better than our TF-IDF
4. Cross-agent sharing aligns with MoltOS multi-agent vision
5. Apache-2.0 license = free to use, modify, redistribute
6. 95.2% retrieval accuracy vs our current ~70%

**What We'd Get:**
- Automatic session capture (no more manual writing to MEMORY.md)
- Better semantic search (BM25 + vector + graph vs our TF-IDF)
- Knowledge graph of vault connections
- Real-time memory viewer
- Token-efficient context injection (2000 tokens vs loading entire vault)
- Cross-agent memory sharing (if we expand to multiple agents)

**What We'd Keep:**
- Vault as source of truth (agentmemory would mirror, not replace)
- Git sync to phone (Obsidian)
- ClawFS for cross-machine persistence
- MoltOS Marrow for emotional state

---

## Implementation Plan

### Phase 1: MCP Integration (Minimal)
1. Add agentmemory MCP server to OpenClaw config
2. Test `memory_recall` and `memory_save` tools
3. Let it capture sessions automatically
4. Keep writing to vault manually as backup

### Phase 2: Hybrid Search Upgrade
1. Replace our TF-IDF search with agentmemory's hybrid search
2. Index all vault files via agentmemory API
3. Use `memory_smart_search` for queries

### Phase 3: Knowledge Graph
1. Enable graph extraction
2. Build entity graph of Nathan's projects, leads, patterns
3. Use graph traversal for "related to" queries

### Phase 4: Auto-Write to Vault
1. Configure agentmemory to export to Obsidian format
2. Auto-write captures to `vault/drawers/captures/`
3. Maintain manual curation for curated entries

---

## Risk Assessment

| Risk | Level | Mitigation |
|------|-------|------------|
| Requires Node.js + iii-engine | Medium | Use Docker fallback |
| New dependency to maintain | Low | Apache-2.0, active development |
| Privacy of Nathan's data | Low | Self-hosted, privacy filter built-in |
| Overlap with existing systems | Medium | agentmemory mirrors, vault stays source |
| Token cost for compression | Low | Local embeddings free, LLM optional |

---

## Recommendation

**INSTALL IT.** The OpenClaw integration is ready. The MCP server gives us 51 tools. It automates the #1 friction point (manual memory writing) and upgrades our search quality from ~70% to 95%.

**Next step:** Test MCP integration in OpenClaw. If stable, enable automatic capture for one session and compare recall quality.

---

*Research completed 2026-05-11*
