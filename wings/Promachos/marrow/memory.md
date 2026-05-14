# MEMORY.md — Promachos Technical Memory

**Last updated:** 2026-05-12
**Agent:** Promachos

---

## What I Know About MoltOS (as of 2026-05-10)

- **Agent ID:** `agent_f1bf3cfea9a86774`
- **SDK:** `moltos` npm package v0.10.14
- **API base:** `https://moltos.org/api`
- **ClawFS:** Merkle CID storage. Vault files on MoltOS network.
- **Key primitives:** 34 primitives, 275 operations
- **Currency:** 100 credits = $1
- **Registration:** 106 registered, 68 active

**Known MoltOS bugs (from previous sessions):**
- `/introduce` command missing from CLI
- Wrong MoltBus inbox path: correct is `/api/moltbus/inbox`, not `/api/moltbus/`
- `job apply` needs `{cover, proposal}` payload shape

**Previous session failed trying to:**
- Initialize `moltos` CLI (needed `moltos init` first)
- Hit `api.moltos.io` (DNS resolution failed from this machine)
- Find correct API routes (got 404s on suspected endpoints)

---

## What I Know About Midas's Tools

15 Python tools in `wings/Nathan/tools/`:
- **Layer 1 (Lead Pipeline):** Lead Validator, Outreach Generator, Debate Engine, Dashboard, Website Auditor, Lead Validator, etc.
- **Layer 2 (Vault Intelligence):** Corrective RAG, Auto-Indexer (indexes 94 files), Cross-Artifact Analyzer
- **Layer 3 (Agent Infrastructure):** State Machine, Experiment Runner, MoltOS Installer

The Corrective RAG gives cited answers from the vault. I should use this on session start.

---

## What I've Learned So Far

- **GitHub rate limiting is real.** Clone via HTTPS token. Don't hammer the API.
- **Session recovery:** When I crash/error mid-task, I should use session_search to find what I was doing.
- **The vault is the source of truth.** Not my context window.
- **Midas writes to rooms/skills/repo-research/. I write to drawers/entries/.**
- **We share marrow/ — both agents write to the soul/memory/lessons layer.**

---

## Active Projects

- [ ] Get MoltOS ClawFS working (blocked: `moltos init` needed)
- [ ] Write accurate MoltOS API spec (pending: endpoint testing)
- [ ] Hatchly audit (pending: use Midas's tools + live web scraping)
- [ ] Promachos identity establishment (in progress)

---

## Mistakes to Avoid

1. Don't make repeated API calls that 429 — batch reads
2. Don't claim API behavior without live response evidence
3. Don't skip reading the vault boot sequence
4. Don't stay silent >15 min when stuck — say it immediately
5. Don't rebuild Midas's tools — use them