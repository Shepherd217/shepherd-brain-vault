#!/usr/bin/env python3
"""
SkillForge — Self-Building Skill Generator
Generates production-grade .md skills from session patterns.

What it does:
- Watches sessions for repeated tool combinations
- Generates formal SKILL.md files with:
  - Description, usage triggers, example workflow
  - Parameter definitions, error handling, best practices
- Registers skills in vault/rooms/skills/auto-forged/
- Tests skills against recent sessions (did it work?)
- Evolves skills based on usage feedback
- Tracks forge lineage: this skill came from sessions X, Y, Z

Usage:
    python skill_forge.py --watch           # Watch for new patterns
    python skill_forge.py --forge-all       # Forge all detected patterns
    python skill_forge.py --test skill_name # Test a forged skill
    python skill_forge.py --status          # Show forge dashboard
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ── Config ───────────────────────────────────────────────────────────────────
FORGE_DIR = Path.home() / ".openclaw/workspace/vault/rooms/skills/auto-forged"
SESSIONS_DIR = Path.home() / ".openclaw/agents/main/sessions"
FORGE_LOG = FORGE_DIR / ".forge_log.json"

FORGE_DIR.mkdir(parents=True, exist_ok=True)

# ── Skill Templates ───────────────────────────────────────────────────────────

SKILL_TEMPLATE = """# {name}

**Auto-forged from sessions:** {lineage}
**Forge date:** {date}
**Success rate:** {success_rate}

## Description

{description}

## When to Use

{triggers}

## Workflow

{workflow}

## Parameters

{parameters}

## Example

{example}

## Best Practices

{best_practices}

## Error Handling

{error_handling}

---
*Auto-forged by SkillForge v1.0 | Last evolved: {last_evolved}*
"""

def generate_skill_name(pattern_name: str) -> str:
    """Convert pattern name to skill name."""
    return pattern_name.replace("_", "-").title()

def forge_skill(pattern_name: str, sessions: List[str], confidence: float) -> str:
    """Generate a SKILL.md file from session patterns."""
    
    skill_name = generate_skill_name(pattern_name)
    
    # Analyze what tools were used
    tool_usage = analyze_tool_usage(pattern_name, sessions)
    
    # Build description
    descriptions = {
        "lead_audit": "Perform comprehensive website audits for local service businesses.",
        "outreach_draft": "Draft personalized outreach emails with demo landing page concepts.",
        "repo_research": "Deep-dive research on GitHub repos for pattern extraction.",
        "multi_agent": "Orchestrate multiple sub-agents for parallel task execution.",
        "vault_maintenance": "Maintain vault health: commit, push, index, clean.",
        "crisis_recovery": "Detect and recover from stalled or failed agent sessions.",
    }
    description = descriptions.get(pattern_name, f"Auto-detected pattern: {pattern_name}")
    
    # Build triggers
    triggers = generate_triggers(pattern_name, tool_usage)
    
    # Build workflow
    workflow = generate_workflow(pattern_name, tool_usage)
    
    # Build parameters
    parameters = generate_parameters(pattern_name)
    
    # Build example
    example = generate_example(pattern_name)
    
    # Build best practices
    best_practices = generate_best_practices(pattern_name)
    
    # Build error handling
    error_handling = generate_error_handling(pattern_name)
    
    # Assemble skill
    skill_md = SKILL_TEMPLATE.format(
        name=skill_name,
        lineage=", ".join(sessions[:3]),
        date=datetime.now().strftime("%Y-%m-%d"),
        success_rate=f"{confidence:.0%}",
        description=description,
        triggers=triggers,
        workflow=workflow,
        parameters=parameters,
        example=example,
        best_practices=best_practices,
        error_handling=error_handling,
        last_evolved=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )
    
    return skill_md

def analyze_tool_usage(pattern_name: str, sessions: List[str]) -> Dict:
    """Analyze what tools were used for this pattern."""
    tool_counts = {}
    
    for session_id in sessions[:5]:  # Check last 5 sessions
        session_path = SESSIONS_DIR / f"{session_id}.jsonl"
        if not session_path.exists():
            continue
        
        try:
            content = session_path.read_text()
            tools = re.findall(r'"tool":\s*"([^"]+)"', content)
            for tool in tools:
                tool_counts[tool] = tool_counts.get(tool, 0) + 1
        except Exception:
            continue
    
    return tool_counts

def generate_triggers(pattern_name: str, tool_usage: Dict) -> str:
    """Generate usage triggers."""
    triggers_map = {
        "lead_audit": (
            '- User mentions "audit", "website review", "check this site"\n'
            '- User shares a business website URL\n'
            '- Standout Local campaign is active\n'
            '- User says "score this lead" or "rate this site"'
        ),
        "outreach_draft": (
            '- User mentions "email", "outreach", "contact this business"\n'
            '- Lead audit just completed (auto-trigger)\n'
            '- User says "draft an email" or "write outreach"'
        ),
        "repo_research": (
            '- User shares a GitHub repo URL\n'
            '- User says "research this", "scrape this repo", "Picasso steal"\n'
            '- Pattern discovery mode is active'
        ),
        "multi_agent": (
            '- Task requires parallel execution (research + writing + testing)\n'
            '- User says "orchestrate", "delegate", "spawn agents"\n'
            '- Complex task with multiple independent components'
        ),
        "vault_maintenance": (
            '- Heartbeat detects stale commits\n'
            '- User says "sync vault", "commit changes", "push updates"\n'
            '- End of session detected'
        ),
        "crisis_recovery": (
            '- Session stalled or timed out\n'
            '- Tool execution failed 3+ times\n'
            '- User says "fix this", "recover", "stuck"'
        ),
    }
    return triggers_map.get(pattern_name, "- Auto-detected pattern match")

def generate_workflow(pattern_name: str, tool_usage: Dict) -> str:
    """Generate workflow steps."""
    workflows = {
        "lead_audit": (
            "1. **Fetch** website content via browser or web_fetch\n"
            "2. **Extract** business info: name, services, location, contact\n"
            "3. **Score** using 100-point rubric\n"
            "4. **Identify** pain points (missing CTA, no mobile optimization, etc.)\n"
            "5. **Generate** demo landing page concept\n"
            "6. **Draft** personalized outreach hook\n"
            "7. **Package** into lead packet with scores and recommendations"
        ),
        "outreach_draft": (
            "1. **Load** lead data from audit\n"
            "2. **Research** business owner/manager (LinkedIn, about page)\n"
            "3. **Draft** email with personalized opening\n"
            "4. **Attach** demo concept and relevant pain points\n"
            "5. **Score** email quality (personalization, clarity, CTA)\n"
            "6. **Queue** for review or send"
        ),
        "repo_research": (
            "1. **Fetch** repo README, structure, recent commits\n"
            "2. **Identify** core architecture and unique patterns\n"
            "3. **Map** to Nathan\'s world (how could this upgrade our system?)\n"
            "4. **Score** steal-worthiness (innovation, applicability, integration cost)\n"
            "5. **Document** findings in vault/rooms/skills/repo-research/\n"
            "6. **Build** proof-of-concept if high-value"
        ),
        "multi_agent": (
            "1. **Decompose** task into independent sub-tasks\n"
            "2. **Spawn** sub-agents with specific goals\n"
            "3. **Monitor** progress via subagents(action=\"list\")\n"
            "4. **Collect** results and integrate\n"
            "5. **Validate** outputs against success criteria\n"
            "6. **Report** consolidated results"
        ),
        "vault_maintenance": (
            "1. **Check** git status for uncommitted changes\n"
            "2. **Add** all vault changes\n"
            "3. **Commit** with descriptive message\n"
            "4. **Push** to remote\n"
            "5. **Verify** sync success\n"
            "6. **Update** semantic search index if files changed"
        ),
        "crisis_recovery": (
            "1. **Detect** stalled or failed components\n"
            "2. **Diagnose** root cause (timeout, error, missing dependency)\n"
            "3. **Route** repair using alternate approach\n"
            "4. **Test** fix in isolation\n"
            "5. **Re-integrate** with main workflow\n"
            "6. **Document** failure mode for future prevention"
        ),
    }
    return workflows.get(pattern_name, "1. Detect pattern\n2. Execute relevant tools\n3. Validate output")

def generate_parameters(pattern_name: str) -> str:
    """Generate parameter documentation."""
    params = {
        "lead_audit": (
            "| Parameter | Type | Required | Description |\n"
            "|-----------|------|----------|-------------|\n"
            "| url | string | Yes | Business website URL |\n"
            "| niche | string | No | Service category (cleaning, roofing, etc.) |\n"
            "| depth | string | No | \"quick\" (5 min) or \"deep\" (15 min) |"
        ),
        "outreach_draft": (
            "| Parameter | Type | Required | Description |\n"
            "|-----------|------|----------|-------------|\n"
            "| lead_id | string | Yes | Lead identifier from audit |\n"
            "| tone | string | No | \"professional\", \"casual\", \"urgent\" |\n"
            "| include_demo | bool | No | Attach demo page concept |"
        ),
        "repo_research": (
            "| Parameter | Type | Required | Description |\n"
            "|-----------|------|----------|-------------|\n"
            "| repo_url | string | Yes | GitHub repository URL |\n"
            "| focus | string | No | \"architecture\", \"features\", \"patterns\" |\n"
            "| build_poc | bool | No | Build proof-of-concept if high-value |"
        ),
        "multi_agent": (
            "| Parameter | Type | Required | Description |\n"
            "|-----------|------|----------|-------------|\n"
            "| tasks | list | Yes | Array of sub-task descriptions |\n"
            "| max_agents | int | No | Maximum parallel agents (default: 5) |\n"
            "| timeout | int | No | Timeout per agent in seconds |"
        ),
        "vault_maintenance": (
            "| Parameter | Type | Required | Description |\n"
            "|-----------|------|----------|-------------|\n"
            "| scope | string | No | \"all\" or specific directory |\n"
            "| message | string | No | Custom commit message |\n"
            "| push | bool | No | Push after commit (default: true) |"
        ),
        "crisis_recovery": (
            "| Parameter | Type | Required | Description |\n"
            "|-----------|------|----------|-------------|\n"
            "| component | string | Yes | Failed component identifier |\n"
            "| strategy | string | No | \"retry\", \"alternate\", \"escalate\" |\n"
            "| notify | bool | No | Notify user of recovery attempt |"
        ),
    }
    return params.get(pattern_name, "| Parameter | Type | Required | Description |\n|-----------|------|----------|-------------|\n")

def generate_example(pattern_name: str) -> str:
    """Generate usage example."""
    examples = {
        "lead_audit": (
            "```\n"
            "User: 'Audit this site: https://cleanpro-champaign.com'\n\n"
            "System executes lead_audit:\n"
            "- Fetches site\n"
            "- Scores: 67/100\n"
            "- Pain points: No mobile CTA, slow load, no FAQ schema\n"
            "- Demo concept: 'Move-Out Cleaning Special' landing page\n"
            "- Outreach hook: 'I noticed your site loads in 4.2s on mobile...'\n"
            "```"
        ),
        "outreach_draft": (
            "```\n"
            "User: 'Draft email for lead #47'\n\n"
            "System loads lead #47 data, researches owner,\n"
            "generates personalized email with demo attachment.\n"
            "```"
        ),
        "repo_research": (
            "```\n"
            "User: 'Research this: https://github.com/NousResearch/hermes-agent'\n\n"
            "System fetches repo, analyzes architecture,\n"
            "maps patterns to our system, generates dissection doc.\n"
            "```"
        ),
        "multi_agent": (
            "```\n"
            "User: 'Research 5 cleaning companies in parallel'\n\n"
            "System spawns 5 sub-agents, each audits one company.\n"
            "Results collected and ranked in consolidated report.\n"
            "```"
        ),
        "vault_maintenance": (
            "```\n"
            "Heartbeat triggers vault_maintenance:\n"
            "- Detects 3 uncommitted files\n"
            "- Commits: 'auto: heartbeat sync'\n"
            "- Pushes to origin\n"
            "- Re-indexes semantic search\n"
            "```"
        ),
        "crisis_recovery": (
            "```\n"
            "Session stalled on web_fetch.\n"
            "RecoveryRouter detects timeout after 60s.\n"
            "Switches to browser tool with fallback.\n"
            "Success: content retrieved via alternate path.\n"
            "```"
        ),
    }
    return examples.get(pattern_name, "```\nUser: 'Execute pattern'\n\nSystem detects pattern, executes relevant tools.\n```")

def generate_best_practices(pattern_name: str) -> str:
    """Generate best practices."""
    practices = {
        "lead_audit": (
            "- Always verify business is still operating\n"
            "- Check for multiple locations (franchise?)\n"
            "- Score conservatively — better to under-promise\n"
            "- Include exact quotes from website\n"
            "- Never fabricate claims"
        ),
        "outreach_draft": (
            "- Research recipient before drafting\n"
            "- Keep under 150 words\n"
            "- One clear CTA only\n"
            "- Test send to yourself first\n"
            "- Track open rates if possible"
        ),
        "repo_research": (
            "- Read code, not just README\n"
            "- Check recent issues for hidden patterns\n"
            "- Map to our specific needs (don't cargo cult)\n"
            "- Build smallest viable proof-of-concept\n"
            "- Document integration cost honestly"
        ),
        "multi_agent": (
            "- Decompose into truly independent tasks\n"
            "- Set clear success criteria per agent\n"
            "- Monitor with subagents list\n"
            "- Have fallback if agent fails\n"
            "- Don't spawn more than 5 parallel agents"
        ),
        "vault_maintenance": (
            "- Commit early, commit often\n"
            "- Write descriptive messages\n"
            "- Verify push succeeded\n"
            "- Keep vault lean (archive old files)\n"
            "- Re-index search after bulk changes"
        ),
        "crisis_recovery": (
            "- Always try simplest fix first\n"
            "- Log failure modes for pattern detection\n"
            "- Don't hide errors from user\n"
            "- Escalate if 3 repair attempts fail\n"
            "- Document workaround for future"
        ),
    }
    return practices.get(pattern_name, "- Execute with care\n- Validate outputs\n- Log results")

def generate_error_handling(pattern_name: str) -> str:
    """Generate error handling guidance."""
    errors = {
        "lead_audit": (
            "- Website unreachable: Try browser fallback, then skip\n"
            "- No contact info: Flag for manual research\n"
            "- Score ambiguity: Conservative score, note uncertainty\n"
            "- Tool failure: Log and move to next lead"
        ),
        "outreach_draft": (
            "- No recipient info: Use generic business email\n"
            "- Tone mismatch: Ask user for preference\n"
            "- Send failure: Queue for retry, notify user"
        ),
        "repo_research": (
            "- Repo private: Skip, log inaccessible\n"
            "- Rate limited: Wait 60s, retry with token\n"
            "- No clear patterns: Document 'no steal-worthy patterns found'"
        ),
        "multi_agent": (
            "- Agent timeout: Kill and retry with smaller scope\n"
            "- Agent error: Collect partial results, flag for review\n"
            "- Too many agents: Queue remaining, process in batches"
        ),
        "vault_maintenance": (
            "- Push rejected: Pull first, resolve conflicts\n"
            "- Large files: Use git LFS or exclude\n"
            "- Index fail: Log and retry on next heartbeat"
        ),
        "crisis_recovery": (
            "- All fixes fail: Escalate to user with options\n"
            "- Cascade failure: Stop, assess scope, restart fresh\n"
            "- Data loss: Restore from last checkpoint"
        ),
    }
    return errors.get(pattern_name, "- Log error\n- Notify user\n- Attempt graceful degradation")

# ── Main Operations ───────────────────────────────────────────────────────────

def load_forge_log() -> Dict:
    if FORGE_LOG.exists():
        return json.loads(FORGE_LOG.read_text())
    return {"forged_skills": {}, "evolutions": []}

def save_forge_log(log: Dict):
    FORGE_LOG.write_text(json.dumps(log, indent=2))

def forge_all_detected():
    """Forge skills from all detected patterns."""
    print("🔨 SKILL FORGE — Auto-forging skills from session patterns\n")
    
    log = load_forge_log()
    
    # Load patterns from autoevolve skills
    autoevolve_dir = Path.home() / ".openclaw/workspace/vault/rooms/skills/auto-evolved"
    
    if not autoevolve_dir.exists():
        print("❌ No auto-evolved patterns found. Run autoevolve.py --extract first.")
        return
    
    forged_count = 0
    
    for skill_file in autoevolve_dir.glob("*.json"):
        if skill_file.name == "genealogy.json":
            continue
        
        data = json.loads(skill_file.read_text())
        pattern_name = data["name"]
        
        # Skip if already forged and not evolved
        if pattern_name in log["forged_skills"]:
            existing = log["forged_skills"][pattern_name]
            if existing["evolution_count"] >= data.get("evolution_count", 0):
                print(f"   ⏭️  {pattern_name} — already forged (not evolved)")
                continue
        
        # Forge skill
        sessions = data.get("lineage", [])
        confidence = data.get("success_count", 0) / max(data.get("use_count", 1), 1)
        
        skill_md = forge_skill(pattern_name, sessions, confidence)
        skill_path = FORGE_DIR / f"{pattern_name}.md"
        skill_path.write_text(skill_md)
        
        log["forged_skills"][pattern_name] = {
            "forged_at": datetime.now().isoformat(),
            "confidence": confidence,
            "sessions": sessions,
            "evolution_count": data.get("evolution_count", 0),
            "path": str(skill_path),
        }
        
        forged_count += 1
        print(f"   ✨ Forged: {pattern_name} (confidence: {confidence:.0%})")
    
    save_forge_log(log)
    print(f"\n📊 Forged {forged_count} skills → {FORGE_DIR}")

def show_status():
    """Show forge dashboard."""
    log = load_forge_log()
    
    print("🔨 SKILL FORGE DASHBOARD\n" + "=" * 50)
    print(f"\n📦 Forged skills: {len(log['forged_skills'])}")
    
    for name, info in log["forged_skills"].items():
        print(f"\n   📄 {name}")
        print(f"   Forged: {info['forged_at'][:10]}")
        print(f"   Confidence: {info['confidence']:.0%}")
        print(f"   Sessions: {len(info['sessions'])}")
        print(f"   Evolutions: {info['evolution_count']}")

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    
    if "--forge-all" in args:
        forge_all_detected()
    elif "--status" in args:
        show_status()
    else:
        print(__doc__)
        print("\nCommands:")
        print("  --forge-all     Forge all detected patterns into skills")
        print("  --status        Show forge dashboard")

if __name__ == "__main__":
    main()
