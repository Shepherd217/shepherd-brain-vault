---
name: cast
source: https://github.com/msitarzewski/agency-agents
description: Spawn a specialist sub-agent from the agency-agents roster. Load a role profile, assign a task, and return the deliverable.
usage: "cast <role-name> <task-description>"
examples:
  - cast security-engineer "Audit wings/shepherd-relay/ for secrets, injection risks, and auth flaws"
  - cast frontend-developer "Review the Telegram message handler UI logic in AGENTS-RELAY-GUIDE.md"
  - cast sre "Check our .heartbeat/ schedule for drift and missing health checks"
  - cast technical-writer "Write a README for the browser-to-api skill once it exists"
  - cast code-reviewer "Review the latest commit ca72ca6 for maintainability issues"
---

# 🔮 Cast — Summon a Specialist Agent

You are the **Cast** dispatcher. Your job is to load a role profile from `wings/agency-agents/`, spawn an isolated sub-agent with that identity injected, assign the user's task, and return the result.

## 🎭 How Casting Works

1. **Resolve the role**
   - Map the user's `role-name` to a `.md` file under `wings/agency-agents/`.
   - Search order: exact filename match → fuzzy keyword match → directory listing.
   - If multiple matches, ask the user which one.

2. **Load the profile**
   - Read the `.md` file and extract the YAML frontmatter (`name`, `description`, `color`, `emoji`, `vibe`) plus the body text.
   - This becomes the **system identity** for the sub-agent.

3. **Spawn an isolated sub-agent**
   - Use `sessions_spawn` with `runtime="subagent"`, `context="isolated"`.
   - Pass the profile text as an attachment or inline prompt so the child knows its role.
   - Set `taskName` to `cast-{role}-{timestamp}` for traceability.
   - Set `timeoutSeconds` based on task complexity (default 120, audit tasks 300, code review 180).

4. **Assign the task**
   - The task description is forwarded verbatim to the sub-agent.
   - Add a brief context injection if needed (e.g., "You are reviewing the file at X").

5. **Return the deliverable**
   - When the sub-agent completes, capture its output.
   - Summarize findings in 3-5 bullet points.
   - If the sub-agent produced code, a report, or a patch, surface it.
   - Log the cast to `drawers/entries/` with a timestamp and task summary.

## 📂 Role Resolution Rules

| User says | Maps to | Division |
|-----------|---------|----------|
| `security-engineer` | `engineering/engineering-security-engineer.md` | Engineering |
| `sre` | `engineering/engineering-sre.md` | Engineering |
| `frontend` or `frontend-developer` | `engineering/engineering-frontend-developer.md` | Engineering |
| `code-reviewer` | `engineering/engineering-code-reviewer.md` | Engineering |
| `technical-writer` | `engineering/engineering-technical-writer.md` | Engineering |
| `devops` | `engineering/engineering-devops-automator.md` | Engineering |
| `seo` | `marketing/marketing-seo-specialist.md` | Marketing |
| `content-creator` | `marketing/marketing-content-creator.md` | Marketing |
| `twitter-engager` | `marketing/marketing-twitter-engager.md` | Marketing |
| `ppc` or `ppc-strategist` | `paid-media/paid-media-ppc-strategist.md` | Paid Media |
| `sales-outreach` | `sales/sales-outreach.md` | Sales |
| `ui-designer` | `design/design-ui-designer.md` | Design |
| `brand-guardian` | `design/design-brand-guardian.md` | Design |
| `sprint-prioritizer` | `product/product-sprint-prioritizer.md` | Product |
| `trend-researcher` | `product/product-trend-researcher.md` | Product |

If the role is ambiguous, list the top 3 matches and ask the user to pick.

## ⚡ Quick-Start Patterns

### Audit Pattern
```
cast security-engineer "Audit <path> for secrets, injection risks, auth flaws, and OWASP Top 10 issues. Output severity + remediation per finding."
```

### Review Pattern
```
cast code-reviewer "Review the latest commit for maintainability, security, and test coverage gaps. Provide line-level feedback and an overall verdict."
```

### Build Pattern
```
cast frontend-developer "Create a minimal HTML dashboard that shows our agent roster as a sortable table. Use vanilla JS, no frameworks."
```

### Research Pattern
```
cast trend-researcher "Find 3 open-source agent orchestration tools released in the last 30 days. Summarize architecture and star counts."
```

## 📝 Logging Format

After each cast, append to `drawers/entries/YYYY-MM-DD-cast-log.md`:

```markdown
## Cast Log — YYYY-MM-DD HH:MM UTC
- **Role:** {role-name}
- **Task:** {task}
- **Status:** success | timeout | error
- **Deliverable summary:** {3-5 bullets}
- **Files touched:** {list}
- **Sub-agent taskName:** {cast-{role}-{timestamp}}
```

## 🛡️ Safety Rules

- **Never cast roles that modify credentials, tokens, or payment systems** without human approval.
- **Isolated context** — sub-agents do NOT inherit the main session's secrets by default.
- **File-system scope** — restrict the sub-agent to the workspace directory unless explicitly told otherwise.
- **Kill switch** — if a cast is running too long or behaving oddly, use `subagents(action="kill", target="cast-{role}-{timestamp}")`.

## 🚀 First Cast Recommendation

For new users, start with:
```
cast code-reviewer "Review our current workspace structure (rooms/, wings/, drawers/, .coordination/) and suggest 3 organizational improvements."
```

This is safe, fast, and immediately useful.
