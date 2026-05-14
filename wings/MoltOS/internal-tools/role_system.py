#!/usr/bin/env python3
"""
RoleSystem — Role-Based Agent Definitions
Steals from CrewAI's role system. Makes FleetCommander smarter.

What it does:
- Defines agent roles: planner, researcher, builder, reviewer, executor
- Each role has: skills, permissions, cost tier, approval requirements
- Routes tasks to agents by role + capability matching
- Tracks role performance (which role handles which tasks best)
- Auto-assigns roles based on task type

Usage:
    python role_system.py --list              # List all roles
    python role_system.py --assign task      # Assign role for task
    python role_system.py --performance      # Show role performance
    python role_system.py --create role      # Create new role
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ── Config ───────────────────────────────────────────────────────────────────
ROLES_DB = Path.home() / ".openclaw/workspace/.cache/roles.json"
ROLES_DB.parent.mkdir(parents=True, exist_ok=True)

# ── Default Roles ───────────────────────────────────────────────────────────

DEFAULT_ROLES = {
    "dreamer": {
        "description": "Proposes ideas, finds patterns, suggests opportunities",
        "skills": ["pattern_miner", "marrow_memory", "kimi_search"],
        "permissions": ["research", "propose", "analyze"],
        "cost_tier": "cheap",
        "approval_required": False,
        "can_delegate_to": ["planner", "researcher"],
    },
    "planner": {
        "description": "Filters proposals, plans execution, decides priorities",
        "skills": ["debate_council", "context_prefect", "config_guardian"],
        "permissions": ["plan", "filter", "prioritize", "approve"],
        "cost_tier": "medium",
        "approval_required": False,
        "can_delegate_to": ["builder", "reviewer", "researcher"],
    },
    "researcher": {
        "description": "Gathers information, verifies facts, explores options",
        "skills": ["kimi_search", "kimi_fetch", "web_fetch", "truth_tether"],
        "permissions": ["research", "verify", "explore"],
        "cost_tier": "cheap",
        "approval_required": False,
        "can_delegate_to": ["analyst"],
    },
    "builder": {
        "description": "Creates tools, writes code, generates skills",
        "skills": ["skill_forge", "autoevolve", "write", "edit"],
        "permissions": ["build", "create", "write", "modify"],
        "cost_tier": "medium",
        "approval_required": True,  # Nathan must approve builds
        "can_delegate_to": ["reviewer"],
    },
    "reviewer": {
        "description": "Verifies quality, checks alignment, validates outputs",
        "skills": ["alignment_check", "truth_tether", "prometheus_lens", "shadow_recorder"],
        "permissions": ["review", "verify", "reject", "score"],
        "cost_tier": "medium",
        "approval_required": False,
        "can_delegate_to": [],
    },
    "executor": {
        "description": "Runs commands, deploys changes, executes plans",
        "skills": ["exec", "fleet_commander", "molt_bridge"],
        "permissions": ["execute", "deploy", "run"],
        "cost_tier": "expensive",
        "approval_required": True,  # Dangerous — needs approval
        "can_delegate_to": [],
    },
    "analyst": {
        "description": "Synthesizes findings, extracts patterns, writes reports",
        "skills": ["pattern_miner", "receipts_engine", "skill_market"],
        "permissions": ["analyze", "synthesize", "report"],
        "cost_tier": "cheap",
        "approval_required": False,
        "can_delegate_to": ["dreamer"],
    },
}

# ── Role Operations ─────────────────────────────────────────────────────────

def load_roles() -> Dict:
    if ROLES_DB.exists():
        return json.loads(ROLES_DB.read_text())
    return DEFAULT_ROLES

def save_roles(roles: Dict):
    ROLES_DB.write_text(json.dumps(roles, indent=2))

def assign_role(task_description: str) -> str:
    """Assign best role for a task."""
    task_lower = task_description.lower()
    
    # Simple keyword matching
    role_scores = {}
    for role_name, role_data in DEFAULT_ROLES.items():
        score = 0
        
        # Check skills against task
        for skill in role_data.get("skills", []):
            if skill.replace("_", " ") in task_lower:
                score += 10
        
        # Check description keywords
        desc_words = role_data["description"].lower().split()
        for word in desc_words:
            if len(word) > 4 and word in task_lower:
                score += 5
        
        role_scores[role_name] = score
    
    best_role = max(role_scores, key=role_scores.get)
    return best_role

def show_roles():
    """Show all roles."""
    roles = load_roles()
    
    print("🎭 ROLE SYSTEM — Agent Roles\n" + "=" * 50)
    for role_name, role_data in roles.items():
        approval = "🔒" if role_data.get("approval_required") else "🔓"
        print(f"\n{approval} {role_name.upper()}")
        print(f"   {role_data['description']}")
        print(f"   Skills: {', '.join(role_data['skills'][:3])}")
        print(f"   Cost tier: {role_data['cost_tier']}")
        print(f"   Can delegate to: {', '.join(role_data['can_delegate_to']) or 'None'}")

def show_performance():
    """Show role performance (placeholder)."""
    print("📊 ROLE PERFORMANCE\n")
    print("(In production: would track which role handles which tasks best)")
    
    roles = load_roles()
    for role_name in roles:
        print(f"   {role_name}: No performance data yet")

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    
    if "--list" in args:
        show_roles()
    elif "--assign" in args:
        idx = args.index("--assign")
        if idx + 1 < len(args):
            task = args[idx + 1]
            role = assign_role(task)
            print(f"🎭 Task: {task}")
            print(f"   Assigned role: {role}")
            print(f"   Skills available: {', '.join(DEFAULT_ROLES[role]['skills'][:3])}")
            if DEFAULT_ROLES[role]['approval_required']:
                print(f"   ⚠️  This role requires Nathan approval")
        else:
            print("Usage: --assign 'task description'")
    elif "--performance" in args:
        show_performance()
    else:
        print(__doc__)
        print("\nCommands:")
        print("  --list              Show all roles")
        print("  --assign task       Assign role for task")
        print("  --performance       Show role performance")

if __name__ == "__main__":
    main()
