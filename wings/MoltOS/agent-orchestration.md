---
date: 2026-05-11
type: architecture-design
source: microsoft-ai-agents-for-beginners (Lesson 8)
tags: [moltos, multi-agent, orchestration, architecture]
---

# MoltOS — Multi-Agent Orchestration Design

**Status:** Design Phase
**Source:** Microsoft AI Agents for Beginners (Lesson 8: Multi-Agent Systems)
**Goal:** Define agent roles, handoff protocols, and coordination model for MoltOS

---

## Why Multi-Agent?

A single agent doing everything = jack of all trades, master of none.

Multiple specialized agents coordinated by a supervisor =:
- **Parallel work:** Research, analysis, and writing happen simultaneously
- **Better quality:** Each agent is an expert in its domain
- **Fault isolation:** One agent failing doesn't crash the whole pipeline
- **Scalability:** Add new agents without rewriting existing ones
- **Observability:** Each step is visible and debuggable

---

## Agent Roles

### 1. CoordinatorAgent (Supervisor)
**Purpose:** Orchestrate the pipeline, manage state, handle errors
**When to invoke:** Any complex task requiring multiple steps
**Tools:** All other agents, state manager, error handler
**Success criteria:** Task completes end-to-end, no dropped handoffs

**Behavior:**
- Receives high-level goal from user
- Breaks into sub-tasks
- Assigns to appropriate agents
- Monitors progress
- Retries failed steps
- Returns final result to user

### 2. ResearchAgent
**Purpose:** Find information, collect data, discover resources
**When to invoke:** Need facts, URLs, contact info, reviews, competitors
**Tools:** Web search, browser, web_fetch, kim_search
**Success criteria:** Returns structured data with sources, no hallucination

**Behavior:**
- Searches for specified information
- Visits URLs to extract details
- Returns structured findings (JSON/markdown)
- Cites sources for every claim
- Flags when information is incomplete

### 3. AnalysisAgent
**Purpose:** Process data, score, rank, identify patterns
**When to invoke:** Raw data needs interpretation, scoring, prioritization
**Tools:** Calculation, comparison, pattern matching
**Success criteria:** Accurate scores, consistent methodology, no bias

**Behavior:**
- Takes structured data from ResearchAgent
- Applies scoring rubrics
- Identifies top opportunities
- Returns ranked results with reasoning
- Flags edge cases and anomalies

### 4. WritingAgent
**Purpose:** Produce content, drafts, summaries, reports
**When to invoke:** Need emails, documents, reports, outreach copy
**Tools:** Markdown, templates, style guides
**Success criteria:** On-topic, well-structured, matches tone requirements

**Behavior:**
- Takes data + context from other agents
- Produces draft content
- Follows templates and style guides
- Self-reviews against criteria
- Returns polished output

### 5. ReviewAgent
**Purpose:** Quality check, verify, critique, suggest improvements
**When to invoke:** Before delivering final output to user
**Tools:** Checklists, rubrics, comparison with standards
**Success criteria:** Catches errors, suggests improvements, doesn't block unnecessarily

**Behavior:**
- Reviews output from WritingAgent (or any agent)
- Checks against success criteria
- Verifies facts (spot-checks with ResearchAgent if needed)
- Suggests improvements
- Approves or sends back for revision

---

## Handoff Protocol

### Message Format
```json
{
  "from": "ResearchAgent",
  "to": "AnalysisAgent",
  "task_id": "uuid",
  "status": "complete",
  "payload": {
    "data": "...",
    "sources": ["..."],
    "confidence": 0.95,
    "gaps": ["..."]
  },
  "metadata": {
    "started_at": "2026-05-11T04:00:00Z",
    "completed_at": "2026-05-11T04:05:00Z",
    "tokens_used": 1234
  }
}
```

### Handoff Rules
1. **Self-verify before handoff:** Agent checks its own output against criteria
2. **Include confidence score:** How sure is the agent about its output?
3. **Document gaps:** What couldn't be found or is uncertain?
4. **Pass full context:** Don't make the next agent re-discover what you found
5. **Timeout handling:** If agent doesn't respond in X minutes, retry or escalate

### Pipeline Example: Standout Local Lead Generation

```
User: "Find 5 cleaning leads in Champaign"
  ↓
CoordinatorAgent: Breaks into sub-tasks
  ├─→ ResearchAgent: "Find cleaning companies in Champaign"
  │     ↓
  │     [Searches, visits sites, collects data]
  │     ↓
  │     Returns: 7 businesses with URLs, reviews, contact info
  │
  ├─→ AnalysisAgent: "Score these 7 leads"
  │     ↓
  │     [Applies rubric, calculates derived scores]
  │     ↓
  │     Returns: Ranked list, top 5 identified
  │
  ├─→ WritingAgent: "Create lead files for top 5"
  │     ↓
  │     [Generates markdown files with audit sections]
  │     ↓
  │     Returns: 5 lead files ready for review
  │
  └─→ ReviewAgent: "Check lead files for accuracy"
        ↓
        [Verifies scores, checks for fabrication]
        ↓
        Returns: Approved or revision requests

CoordinatorAgent: Compiles final report
  ↓
User: "Here's your 5 leads, scored and ready for outreach"
```

---

## Error Handling

### Failure Modes
1. **Agent timeout:** Retry once, then escalate to CoordinatorAgent
2. **Low confidence output:** Flag for human review, don't auto-proceed
3. **Missing required data:** Ask ResearchAgent to fill gaps
4. **Contradictory results:** Log both, flag for human resolution
5. **Agent crash:** CoordinatorAgent restarts agent, replay last known state

### Recovery Strategy
```
If ResearchAgent fails:
  → Retry with broader search terms
  → If still failing, mark as "insufficient data" and proceed with what we have

If AnalysisAgent fails:
  → Retry with simplified scoring
  → If still failing, pass raw data to WritingAgent with note

If WritingAgent fails:
  → Retry with simpler template
  → If still failing, return structured data to user with apology

If ReviewAgent fails:
  → Log warning, proceed without review (degraded but functional)
```

---

## State Management

### Persistent State (ClawFS)
```json
{
  "session_id": "uuid",
  "goal": "Find 5 cleaning leads in Champaign",
  "status": "in_progress",
  "agents": {
    "ResearchAgent": {"status": "complete", "output": "..."},
    "AnalysisAgent": {"status": "running", "input": "..."},
    "WritingAgent": {"status": "pending"},
    "ReviewAgent": {"status": "pending"}
  },
  "results": {},
  "errors": [],
  "created_at": "2026-05-11T04:00:00Z",
  "updated_at": "2026-05-11T04:10:00Z"
}
```

### State Transitions
- `pending` → `running` → `complete` | `failed` | `retry`
- CoordinatorAgent updates state after each handoff
- User can query state at any time: "Where are we on the lead search?"

---

## Implementation Phases

### Phase 1: Design (Current)
- ✅ Agent roles defined
- ✅ Handoff protocol designed
- ✅ Error handling specified
- ⬜ State management implemented
- ⬜ Message format standardized

### Phase 2: MVP (Next Sprint)
- Implement CoordinatorAgent skeleton
- Implement ResearchAgent + AnalysisAgent pipeline
- Test with simple task: "Find 3 leads and score them"
- Validate handoff protocol

### Phase 3: Full Pipeline
- Add WritingAgent + ReviewAgent
- Integrate with Standout Local workflow
- Add error recovery
- Add user query interface ("What's the status?")

### Phase 4: Advanced Features
- Parallel agent execution (ResearchAgent × 3 for different queries)
- Agent specialization (StandoutLocal-ResearchAgent vs MoltOS-ResearchAgent)
- Learning from failures (auto-adjust parameters)
- Human-in-the-loop for low-confidence decisions

---

## Integration with MCP/A2A

### Model Context Protocol (MCP)
- Each agent exposes its capabilities via MCP
- Tools are discoverable and standardized
- Agent can use any MCP-compatible tool

### Agent-to-Agent Protocol (A2A)
- Handoff messages follow A2A standard
- Interoperability with external agents
- Secure, authenticated communication

---

## Success Criteria

- [ ] CoordinatorAgent can manage full pipeline end-to-end
- [ ] Handoffs include all required context (no re-discovery)
- [ ] Errors are caught and recovered gracefully
- [ ] User can query status at any point
- [ ] Pipeline completes in <5 minutes for simple tasks
- [ ] Output quality matches or exceeds single-agent execution
- [ ] No hallucination or fabricated claims in final output

---

## Risks

1. **Complexity overhead:** Multi-agent may be slower than single-agent for simple tasks
   - *Mitigation:* Use single-agent for simple tasks, multi-agent only when beneficial

2. **Context loss between agents:** Information dropped during handoff
   - *Mitigation:* Standardized message format, mandatory context fields

3. **Agent disagreement:** Different agents produce contradictory results
   - *Mitigation:* ReviewAgent as arbiter, human escalation for unresolved conflicts

4. **Debugging difficulty:** Hard to trace which agent caused an issue
   - *Mitigation:* Detailed state logging, session replay capability

---

## Next Steps

- [ ] Implement CoordinatorAgent skeleton
- [ ] Define message schema (JSON schema validation)
- [ ] Create agent registry (what agents exist, what they do)
- [ ] Test pipeline with mock data
- [ ] Integrate with MoltOS agent infrastructure
- [ ] Document API for external agent integration

---

#moltos #multi-agent #orchestration #architecture #microsoft-agents

---

*Design complete. Ready for implementation.*
