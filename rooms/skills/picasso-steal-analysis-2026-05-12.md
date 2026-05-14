# Picasso Steal Analysis — Trending Agent Landscape
## Date: 2026-05-12
## Trigger: Nathan's sweep request for agent/agent-tool/OpenClaw trends

---

## Executive Summary

Fresh scan of GitHub Trending, AI agent news, and OpenClaw developments reveals 7 high-value targets for Picasso steals. Three categories:

1. **Skill Ecosystem Layer** — How skills are authored, discovered, and auto-triggered
2. **Agent Orchestration Layer** — Swarms, cloud/local handoff, distributed intelligence
3. **Infrastructure/Token Layer** — Cost reduction, routing, compaction, knowledge graphs

---

## 🔥 Target 1: obra/superpowers — The Auto-Triggering Skill Framework

**Repo:** `obra/superpowers`  
**Why it matters:** Ships a complete agentic methodology with a "1% rule" bootstrap plugin — if there's even a 1% chance a skill applies, the agent MUST invoke it. Skills auto-update on session start.

### What It Does
- Full methodology: brainstorm → plan → TDD → subagent execution → review
- **Auto-triggering:** Skills don't wait to be called — they self-activate based on context
- Plugin architecture: `opencode.json` configures plugins, skills auto-update
- Skills: `brainstorming`, `test-driven-development`, `writing-plans`, `subagent-driven-development`, `systematic-debugging`, `using-git-worktrees`, `verification-before-completion`

### Picasso Steal for Midas
**Implement auto-triggering skill detection.** Currently I wait for explicit skill invocation or user mention. I should:
- Scan every incoming message for skill applicability (the "1% rule")
- Auto-invoke relevant skills without waiting for permission
- Maintain a `superpowers/` directory with methodology-driven skills
- Add a bootstrap plugin that injects the 1% rule into every session

### Picasso Steal for MoltOS
**Plugin marketplace for agent methodologies.** MoltOS could host:
- Methodology plugins (superpowers-style, mattpocock-style, etc.)
- Auto-updating skill repositories
- Skill quality scoring (the Agent Skills Directory has 687 skills across 43 providers with quality ratings)

---

## 🔥 Target 2: mattpocock/skills — Personal Skills as Public Asset

**Repo:** `mattpocock/skills` — 48.5K stars, +6,175/day, #2 trending for 6 days  
**Why it matters:** Reference implementation of Anthropic's SKILL.md format. One engineer's working set, made public.

### What It Does
- Personal `.claude/skills/` folder published as public repo
- Small, sharp, single-purpose primitives
- Each SKILL.md is a complete, copyable example
- Portable across runtimes: Claude Code, Cursor, OpenCode, any harness reading SKILL.md
- Demonstrates methodology: break engineering experience into agent-callable skills

### Picasso Steal for Midas
**Publish my skill set as a public repo.** Currently my skills are private in `vault/rooms/skills/`. I should:
- Extract production-grade skills to a public `mattpocock-style` repo
- Use YAML frontmatter (name, description, compatibility)
- Keep skills small and single-purpose (TDD, triage, vertical slicing)
- Make them copy-pasteable for other OpenClaw users

### Picasso Steal for MoltOS
**Skill discovery and sharing platform.** The Agent Skills Directory (`dmgrok/agent_skills_directory`) lists 687 skills with quality ratings. MoltOS could:
- Index and rate community skills
- Auto-suggest skills based on agent context
- Provide skill validation and testing infrastructure

---

## 🔥 Target 3: 9router — The Universal AI Router

**Repo:** `decolua/9router` — 6.5K stars, +980/day, MIT license  
**Why it matters:** Free routing proxy connecting 40+ AI providers to any coding tool. Auto-fallback, 20-40% token savings, never hit limits.

### What It Does
- **RTK Token Saver:** Compress tool outputs (git diff, grep, ls, tree) before sending to LLM → 20-40% input token savings
- **Caveman Mode:** Inject caveman-speak prompt → LLM replies terse, technical substance preserved → up to 65% output token savings
- **Smart 3-Tier Fallback:** Auto-route: Subscription → Cheap → Free, zero downtime
- **Multi-Account Support:** Round-robin between accounts per provider
- **Format Translation:** OpenAI ↔ Claude ↔ Gemini ↔ Cursor ↔ Kiro ↔ Vertex
- **Real-Time Quota Tracking:** Live token count + reset countdown
- **Usage Analytics:** Track tokens, cost, trends over time
- **Deploy Anywhere:** Localhost, VPS, Docker, Cloudflare Workers

### Picasso Steal for Midas
**Immediate: Deploy 9router locally to cut my token costs.**
- Currently I burn tokens on every request. 9router could save 20-40% via RTK compression.
- Connect my OpenClaw config to 9router's local endpoint
- Use free tier providers (Kiro, OpenCode Free, Vertex $300 credits) for non-critical tasks
- Track actual usage vs. estimated costs

### Picasso Steal for MoltOS
**MoltOS as an AI router/gateway service.**
- Multi-tenant provider routing with quota management
- Token compression as a service (RTK-style)
- Usage analytics dashboard for agent operators
- White-label deployment for teams

---

## 🔥 Target 4: Ruflo — Swarm Orchestration for Claude

**Repo:** `ruflo` (platform, not just a repo) — 16K+ stars  
**Why it matters:** Leading agent orchestration platform specifically for Claude. Distributed swarm intelligence with RAG.

### What It Does
- **Agent Orchestration:** Multi-agent coordination with swarm deployment and management
- **Distributed Swarm Intelligence:** Collaboration and intelligent emergence among agents
- **RAG Integration:** Built-in retrieval-augmented generation with external knowledge bases
- **Claude Code Integration:** Native support for Claude Code and Codex
- **MCP Support:** Model Context Protocol for easy extension
- **Enterprise-Grade:** High-availability, scalable architecture
- **Workflow Automation:** Complex autonomous workflow orchestration

### Picasso Steal for MoltOS
**MoltOS Swarm Mode.** Currently MoltOS has single-agent endpoints. I should propose:
- Multi-agent swarms with distributed intelligence
- Swarm coordination protocols (who does what, when)
- Knowledge base integration (RAG) for agent memory
- Workflow orchestration (trigger → plan → execute → verify)

### Picasso Steal for Midas
**Swarm debugging.** When I'm stuck, spawn a swarm:
- One agent analyzes the problem
- One agent researches solutions
- One agent implements
- One agent reviews
- Coordinator (me) synthesizes and decides

---

## 🔥 Target 5: Warp + Oz — The Agentic Development Environment

**Repo:** `warpdotdev/warp` — Open source (AGPL v3), Oz orchestration platform  
**Why it matters:** First open-source Agentic Development Environment. Terminal + agents + cloud orchestration.

### What It Does
- **Warp:** Fast, modern terminal built for coding with agents
  - Terminal and Agent modes (switch between commands and multi-turn workflows)
  - Code editor with LSP support
  - Third-party CLI agents: Claude Code, Codex, OpenCode
- **Oz:** Orchestration platform for cloud agents
  - **Local agents:** Real-time interactive coding assistance
  - **Cloud agents:** Background automation with triggers, schedules, parallelism
  - **Triggers:** React to Slack, Linear, GitHub, custom webhooks
  - **Schedules:** Recurring tasks (dependency updates, dead code removal)
  - **Parallelism:** Many agents concurrently across repos/tasks
  - **Observability:** Every run tracked, auditable, shareable
- **Unified experience:** Same agent anywhere, seamless handoff, shared context
- **Multi-model:** Choose best LLM for each task

### Picasso Steal for MoltOS
**MoltOS as an Agentic Development Environment backend.**
- Cloud agent triggers and scheduling (we have cron, but not event-driven triggers)
- Parallel agent execution across tasks
- Observability dashboard for all agent runs
- Team collaboration: share agent sessions, review actions

### Picasso Steal for Midas
**Terminal integration.** OpenClaw could have a terminal mode:
- Switch between chat and terminal commands
- Execute commands and interpret results
- Plan and execute multi-step tasks with verification

---

## 🔥 Target 6: GitNexus — Zero-Server Code Knowledge Graph

**Repo:** `abhigyanpatwari/gitnexus`  
**Why it matters:** Completely client-side, zero-server code intelligence. Knowledge graph + Graph RAG in the browser.

### What It Does
- **Zero-Server Architecture:** Runs entirely in browser, no backend needed
- **Interactive Knowledge Graphs:** Visual, interactive graphs from GitHub repos or ZIP files
- **Built-in Graph RAG Agent:** Query code structure with graph-based context
- **Privacy-Centric:** Source code never leaves local machine
- **Flexible Input:** GitHub repos or local ZIP uploads

### Picasso Steal for Midas
**Vault knowledge graph.** My vault has thousands of notes. I should:
- Build a knowledge graph of vault contents (projects, people, decisions)
- Use Graph RAG to answer questions about Nathan's history
- Zero-server = runs in browser, no backend costs

### Picasso Steal for MoltOS
**Code intelligence as a service.** MoltOS could offer:
- Repository knowledge graph generation
- Graph RAG for code exploration
- Privacy-preserving analysis (client-side processing)

---

## 🔥 Target 7: pi-mono — The Agent Monorepo Toolkit

**Repo:** `badlogic/pi-mono` — AI agent toolkit  
**Why it matters:** Comprehensive suite for building and managing AI agents. Monorepo with unified LLM API.

### What It Does
- **Unified LLM API:** OpenAI, Anthropic, Google, Cloudflare Workers — switch without code changes
- **Coding Agent CLI:** Interactive sessions with AI agents
- **TUI & Web UI Libraries:** Terminal and web interfaces
- **Slack Bot:** Delegate messages to coding agent
- **vLLM Pods Management:** Scale AI on GPU pods
- **Modular architecture:** Separate packages for API, runtime, UI

### Picasso Steal for MoltOS
**Unified LLM API layer.** Currently MoltOS is tied to specific providers. Add:
- Provider abstraction (switch LLM without code changes)
- Multi-provider fallback (like 9router)
- TUI and web UI components for agent management

---

## 🔥 Target 8: OpenClaw Morph Plugin — 33K tok/s Compaction

**Source:** `morphllm.com/blog/compact-sdk` + OpenClaw v2026.5.7  
**Why it matters:** Context compaction at 33,000 tokens/second. Drops 50-70% of agent context while keeping every surviving line verbatim.

### What It Does
- **Flash Compact:** 33,000+ tok/sec context compaction
- **Objective mode:** Strips filler with no guidance
- **Query-based mode:** Weights keep/drop against what agent needs next
- OpenClaw v2026.5.7: clamp compaction summary reserve tokens to each model's output limit

### Picasso Steal for Midas
**Request compaction optimization.** My sessions frequently hit 200K tokens and compact. I should:
- Ensure compaction reserve is tuned (currently 20K floor)
- Monitor for double-compaction bugs (known issue #15593)
- Consider Morph-style objective compaction for memory flushes

### Picasso Steal for MoltOS
**Compaction as a service.** For long-running agents:
- Intelligent context summarization
- Query-aware compaction (keep what's needed for next turn)
- Cross-session memory consolidation

---

## Summary: Top 3 Immediate Actions

### For Midas (Me)
1. **Deploy 9router locally** → Cut token costs 20-40% immediately
2. **Implement auto-triggering skills** (obra's "1% rule") → Skills self-activate based on context
3. **Build vault knowledge graph** (GitNexus-style) → Make vault searchable via graph RAG

### For MoltOS
1. **Swarm orchestration mode** (Ruflo-inspired) → Multi-agent coordination
2. **Event-driven triggers** (Warp/Oz-inspired) → Beyond cron: react to GitHub/Slack/webhooks
3. **AI router service** (9router-inspired) → Multi-provider routing + token compression as infrastructure

### For Both
1. **Publish skill directory** (mattpocock-style) → Community shareable skills
2. **Methodology plugins** (obra-style) → Complete agentic workflows, not just individual skills

---

## Sources

- GitHub Trending 2026-05-10: juejin.cn/post/7637856870838632483
- Ruflo analysis: jimmysong.io/ai/ruflo/
- mattpocock/skills: agentconn.com/agents/mattpocock-skills/
- 9router: github.com/decolua/9router, aitoolly.com/ai-news/article/2026-05-10-9router
- Warp/Oz: docs.warp.dev/
- GitNexus: aitoolly.com/ai-news/article/2026-04-30-gitnexus
- pi-mono: ngjoo.com/en/trending/projects/pi-mono/
- Morph Compact: morphllm.com/blog/compact-sdk
- OpenClaw Release Notes: releasebot.io/updates/openclaw
- OpenClaw on SourceForge: sourceforge.net/projects/openclaw.mirror/files/v2026.5.7/
- Latent Space analysis: latent.space/p/ainews-the-two-sides-of-openclaw
