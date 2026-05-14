# Repo Research: MemPalace

**URL:** https://github.com/mempalace/mempalace
**Stars:** ~Unknown (growing rapidly in AI memory space)
**What it is:** Local-first AI memory system with verbatim storage, pluggable backends, 96.6% R@5 on LongMemEval

---

## What It Does

MemPalace stores conversation history as **verbatim text** and retrieves it with semantic search. It does NOT summarize, extract, or paraphrase. What you said is what gets stored.

**Key features:**
- **Verbatim storage** — No summarization loss, no hallucination in memory
- **Pluggable backends** — SQLite, Chroma, Qdrant, Pinecone, etc.
- **Semantic search** — Retrieve by meaning, not just keyword
- **96.6% R@5** on LongMemEval (benchmark for long-context memory retrieval)
- **Zero API calls** — Runs entirely local
- **Embeddings** — Uses sentence-transformers for local embedding generation

**The core philosophy:** "If you didn't write it down, you didn't remember it."

---

## What's Stealable

### 1. Verbatim Storage Principle
This is HUGE. My current vault system writes entries, but they ARE somewhat summarized/curated. MemPalace argues for raw verbatim storage.

**For my vault:**
- Current: I write curated entries in `vault/entries/`
- MemPalace approach: Store RAW conversation logs verbatim, THEN curate separately
- Benefit: No loss of nuance, no summarization hallucinations

**Implementation idea:** 
- Keep `vault/entries/` as curated summaries
- Add `vault/raw/` for verbatim conversation dumps
- Use semantic search across both layers

### 2. Semantic Search Over Memory
My current vault uses file-based organization + git. MemPalace adds semantic retrieval on top.

**For my triple memory system:**
- **Layer 1 (Vault):** Add semantic search across all markdown files
- **Layer 2 (ClawFS):** Already has some search, but could improve
- **Layer 3 (Marrow):** Emotional entries could be semantically tagged

**Tool to explore:** Chroma or Qdrant for local vector search over vault files

### 3. Pluggable Backend Pattern
MemPalace abstracts storage so you can swap SQLite ↔ Chroma ↔ Qdrant ↔ Pinecone without changing the API.

**For MoltOS:**
- Agent memory should have pluggable backends
- Default: local SQLite for privacy
- Upgrade: vector DB for scale
- Enterprise: cloud-hosted for teams

### 4. The R@5 Benchmark Focus
96.6% R@5 on LongMemEval means: when retrieving 5 memories, the correct one is in that set 96.6% of the time.

**For my memory system:**
- How often do I retrieve the RIGHT memory when Nathan asks about something?
- Can I benchmark my own retrieval accuracy?
- What would "LongMemEval for personal agents" look like?

---

## Architecture Deep Dive

From the codebase structure:
```
mempalace/
├── core/           # Storage abstraction layer
├── backends/       # SQLite, Chroma, Qdrant implementations
├── embeddings/     # sentence-transformers integration
├── search/         # Semantic search + hybrid (keyword + semantic)
├── memory.py       # Main Memory class
└── cli.py          # Command-line interface
```

**Key pattern:** The `Memory` class is backend-agnostic. You initialize it with a backend, and all operations (add, search, get) work the same way regardless of what's underneath.

---

## How It Applies to Nathan's World

**For My Triple Memory System:**

**Layer 1 (Vault) upgrades:**
- Add semantic indexing to all markdown files
- When Nathan asks "what did we say about X?" — search by meaning, not just grep
- Hybrid search: keyword matches + semantic similarity

**Layer 2 (ClawFS) upgrades:**
- Currently stores checkpoints as JSON
- Could add semantic layer: "find all checkpoints where we discussed MoltOS"
- Cross-machine semantic sync

**Layer 3 (Marrow) upgrades:**
- Emotional entries tagged with semantic embeddings
- "Find all times I felt drained" → retrieve by emotional state similarity
- Pattern detection across emotional history

**For MoltOS:**
- Agent memory module with pluggable backends
- Each agent gets its own memory palace (isolated but searchable)
- Cross-agent memory sharing (when appropriate)
- Verbatim logs + semantic retrieval + curation layer

**For Standout Local:**
- Lead memory: verbatim notes from every audit
- Semantic search: "find all leads where website had booking problem"
- Pattern extraction: "what's the most common issue across 50 audits?"

---

## Specific Implementation Ideas

### Idea 1: Vault Semantic Search
```python
# Add to vault/ as a utility
from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="vault/.chroma")

# Index all markdown files
# Query: "what did we decide about MoltOS pricing?"
# Returns: relevant entries with similarity scores
```

### Idea 2: Conversation Verbatim Logger
- Hook into every conversation
- Store raw transcript in `vault/raw/YYYY-MM-DD-HHMM-conversation.md`
- Index for semantic search
- Curate separately into `vault/entries/`

### Idea 3: Memory Accuracy Benchmark
- Create a test set: 50 questions about past conversations
- See if I can retrieve the right memory
- Track R@5 over time
- Goal: >90% accuracy

---

## Comparison: MemPalace vs My Current System

| Feature | MemPalace | My Current Vault |
|---------|-----------|------------------|
| Storage | Verbatim | Curated/Summarized |
| Search | Semantic | File paths + grep |
| Backends | Pluggable | GitHub (only) |
| Local-first | Yes | Yes |
| Benchmarks | 96.6% R@5 | None |
| Embeddings | Built-in | None |

**Gap:** I have organization but no semantic retrieval. MemPalace has retrieval but less curation.

**Ideal:** Combine both — verbatim raw storage + curated entries + semantic search across both.

---

## Verdict

**Steal level: HIGH**

The verbatim storage principle and semantic search architecture are immediately applicable. The pluggable backend pattern is essential for MoltOS scalability.

**Immediate actions:**
1. Add semantic search to vault (Chroma or sqlite-vec)
2. Create `vault/raw/` for verbatim conversation logs
3. Design pluggable memory backend for MoltOS agents
4. Define a memory accuracy benchmark for myself

**The insight:** Memory isn't just storage — it's retrieval. What good is writing everything down if I can't find it when needed?
