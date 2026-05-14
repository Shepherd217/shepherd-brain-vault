---
# Pattern Library: LLM Apps
# Source: awesome-llm-apps (github.com/Shubhamsaboo/awesome-llm-apps)
# Purpose: Curated patterns for Standout Local and MoltOS
---

# Pattern Library — LLM Apps

**Status:** Active collection
**Source:** awesome-llm-apps (106K+ stars, 100+ runnable patterns)
**Method:** Clone → Customize → Ship

---

## Top 5 Patterns for Nathan's World

### Pattern 1: Self-Evolving Agent
**What it does:** Agent generates code, tests it, grades its own output, iterates until passing.

**Architecture:**
```
User Request
  ↓
Agent generates solution (attempt #1)
  ↓
Self-test / unit test / verification
  ↓
Grade output (pass / fail)
  ↓
If fail → analyze failure → regenerate (attempt #2)
  ↓
Loop until pass or max attempts reached
  ↓
Return final solution with attempt history
```

**For Standout Local:**
- Generate outreach variants → A/B test → measure response rate → iterate
- Generate audit reports → self-check against rubric → revise if incomplete
- Generate demo page concepts → verify against pain points → refine

**For MoltOS:**
- Agent generates API test → runs it → checks response → iterates if wrong
- Agent writes documentation → checks completeness → adds missing sections

**Clone → Customize → Ship:**
- Clone: Use the generate → test → grade loop
- Customize: Replace "code" with "outreach copy" or "audit report"
- Ship: Standout Local outreach engine with built-in A/B testing

---

### Pattern 2: Corrective RAG (Retrieval-Augmented Generation)
**What it does:** Retrieve context, check if it's relevant, refine if not, then generate.

**Architecture:**
```
Query
  ↓
Retrieve documents
  ↓
Grade relevance of each document
  ↓
If documents relevant → use them to answer
If not relevant → rewrite query → retrieve again
  ↓
Generate final answer with verified sources
```

**For Standout Local:**
- Retrieve business info → verify it's the RIGHT business (not a name collision)
- Check: Is this the same "Lisa Cleaning" from Yelp vs a different one?
- Prevents the Chavez's Cleaning / landscaping collision

**For MoltOS:**
- Retrieve API docs → verify endpoint behavior matches docs
- If mismatch → flag as bug, don't proceed with incorrect assumptions

**Clone → Customize → Ship:**
- Clone: The retrieve → grade → refine loop
- Customize: Grade "is this the same business?" instead of "is this relevant?"
- Ship: Lead verification pipeline that catches identity collisions

---

### Pattern 3: Multi-Agent Debate
**What it does:** Multiple agents discuss a topic, each with different perspective, converge on best answer.

**Architecture:**
```
Question
  ├─→ Agent A (optimistic): "Here's why this will work..."
  ├─→ Agent B (pessimistic): "Here are the risks..."
  ├─→ Agent C (creative): "What if we tried this instead..."
  └─→ Synthesizer: "Based on all perspectives, best answer is..."
```

**For Standout Local:**
- Agent A: "This lead is HOT — score it 90"
- Agent B: "But the phone number might be old — check it"
- Agent C: "What if we focus on their Yelp reviews instead?"
- Synthesizer: Balanced score with risk assessment

**For MoltOS:**
- Agent A: "This API works fine"
- Agent B: "But it contradicts the docs"
- Agent C: "Let's test from another angle"
- Synthesizer: "Bug confirmed, report it"

**Clone → Customize → Ship:**
- Clone: Multi-perspective discussion + synthesis
- Customize: Perspectives = optimist / skeptic / creative
- Ship: Lead scoring with built-in devil's advocate

---

### Pattern 4: Structured Output with Validation
**What it does:** LLM produces structured data (JSON, markdown), validator checks schema, feedback loop corrects errors.

**Architecture:**
```
Request for structured data
  ↓
LLM generates JSON/markdown
  ↓
Validator checks against schema
  ↓
If invalid → feedback to LLM → regenerate
  ↓
If valid → return structured output
```

**For Standout Local:**
- Generate lead files in exact markdown format
- Validate: Has all required sections? Scores are numbers? Paths are correct?
- Auto-correct missing fields

**For MoltOS:**
- Generate API test results in standard format
- Validate: Status codes are valid? Timestamps are ISO8601?

**Clone → Customize → Ship:**
- Clone: Generate → validate → correct loop
- Customize: Schema = lead file format (from LEAD_SYSTEM.md)
- Ship: Auto-validated lead file generator

---

### Pattern 5: Conversation State Machine
**What it does:** Track conversation state, handle context switching, resume interrupted flows.

**Architecture:**
```
User Message
  ↓
Detect intent (classify)
  ↓
Update conversation state
  ↓
Route to appropriate handler
  ├─→ New request → start fresh pipeline
  ├─→ Follow-up → resume previous context
  ├─→ Interrupt → save state, handle new request, offer to resume
  └─→ Clarification → ask question, wait for answer
```

**For Standout Local:**
- "Find leads" → starts lead pipeline
- "What about that cleaning company?" → resumes previous lead context
- "Actually wait, check this tweet" → saves lead state, switches to research, offers to resume

**For MoltOS:**
- "Test this endpoint" → starts API test
- "What was the result?" → resumes test context
- "Check this other thing first" → saves test state

**Clone → Customize → Ship:**
- Clone: State machine with intent classification
- Customize: States = idle / researching / auditing / drafting / reviewing
- Ship: Context-aware agent that never loses the plot

---

## How to Use This Library

### When Starting a New Feature
1. Check this library — does a pattern fit?
2. Clone the architecture (copy the flow diagram)
3. Customize for Nathan's domain (replace examples)
4. Ship as vault/rooms/skills/ or .claude/skills/

### When Stuck on a Problem
1. Check this library — has someone solved a similar problem?
2. Adapt the pattern (don't copy-paste, understand and adapt)
3. Test with smallest viable example
4. Iterate

### When Reviewing Our Own Work
1. Does our solution match any of these patterns?
2. If yes — are we using the pattern correctly?
3. If no — would a pattern help?

---

## Patterns Wishlist (To Discover)

- [ ] **Agent Swarm Coordination** — How to run 100+ agents without chaos
- [ ] **Human-in-the-Loop** — When to pause for approval vs auto-execute
- [ ] **Continuous Learning** — How to improve from every interaction
- [ ] **Memory Compression** — How to summarize without losing information
- [ ] **Tool Discovery** — How to find and integrate new tools automatically

---

*Library version: 1.0 (2026-05-11)*
*Source: awesome-llm-apps (github.com/Shubhamsaboo/awesome-llm-apps)*
