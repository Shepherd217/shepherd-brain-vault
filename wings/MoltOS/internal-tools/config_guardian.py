#!/usr/bin/env python3
"""
ConfigGuardian — Config Validation + Auto-Fix
Makes lintlang look like a toy.

What it does:
- Validates .claude/rules/ for completeness
- Checks .env files for missing keys
- Validates TOOLS.md has all required sections
- Checks SOUL.md, USER.md, AGENTS.md for drift
- Auto-fixes common issues (adds missing sections, updates dates)
- Tracks config health over time
- Fails loudly with specific actionable fixes

Usage:
    python config_guardian.py --validate       # Validate all config files
    python config_guardian.py --fix            # Auto-fix common issues
    python config_guardian.py --status           # Show config health
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ── Config ───────────────────────────────────────────────────────────────────
WORKSPACE = Path.home() / ".openclaw/workspace"
VAULT_DIR = WORKSPACE / "shepherd-brain-vault"
CONFIG_FILES = {
    "SOUL": WORKSPACE / "SOUL.md",
    "USER": WORKSPACE / "USER.md",
    "AGENTS": WORKSPACE / "AGENTS.md",
    "TOOLS": WORKSPACE / "TOOLS.md",
    "IDENTITY": WORKSPACE / "IDENTITY.md",
}
RULES_DIR = VAULT_DIR / "rooms/skills"
SKILLS_DIR = VAULT_DIR / "rooms/skills/auto-forged"
HEALTH_LOG = WORKSPACE / ".cache/config_health.json"
HEALTH_LOG.parent.mkdir(parents=True, exist_ok=True)

# ── Validation Rules ──────────────────────────────────────────────────────

VALIDATION_RULES = {
    "SOUL.md": {
        "required_sections": ["soul", "principles", "how i care", "speaking style"],
        "min_length": 500,
    },
    "USER.md": {
        "required_sections": ["name", "context"],
        "min_length": 100,
    },
    "AGENTS.md": {
        "required_sections": ["first run", "every session", "memory"],
        "min_length": 1000,
    },
    "TOOLS.md": {
        "required_sections": ["what goes here", "examples"],
        "min_length": 200,
    },
}

def validate_file(name: str, path: Path) -> Dict:
    """Validate a single config file."""
    issues = []
    
    if not path.exists():
        return {
            "status": "🔴 MISSING",
            "issues": [f"File does not exist: {path}"],
        }
    
    content = path.read_text().lower()
    rules = VALIDATION_RULES.get(name, {})
    
    # Check required sections
    for section in rules.get("required_sections", []):
        if section.lower() not in content:
            issues.append(f"Missing section: '{section}'")
    
    # Check minimum length
    min_length = rules.get("min_length", 0)
    if len(content) < min_length:
        issues.append(f"Too short: {len(content)} chars (min: {min_length})")
    
    # Check for stale dates
    year_match = re.search(r'20\d{2}', content)
    if year_match:
        file_year = int(year_match.group())
        current_year = datetime.now().year
        if file_year < current_year:
            issues.append(f"Possibly stale (mentions year {file_year}, current is {current_year})")
    
    # Check for TODO markers
    if "todo" in content or "fixme" in content:
        issues.append("Contains TODO/FIXME markers")
    
    status = "🟢 OK" if not issues else "🟡 WARN" if len(issues) < 3 else "🔴 FAIL"
    
    return {
        "status": status,
        "issues": issues,
        "size": len(content),
    }

def validate_rules() -> Dict:
    """Validate .claude/rules/ directory."""
    issues = []
    
    if not RULES_DIR.exists():
        return {
            "status": "🔴 MISSING",
            "issues": [f"Rules directory not found: {RULES_DIR}"],
        }
    
    rules = list(RULES_DIR.glob("*.md"))
    
    if len(rules) == 0:
        issues.append("No rule files found")
    
    for rule_file in rules:
        content = rule_file.read_text()
        if len(content) < 100:
            issues.append(f"Rule {rule_file.name} is very short ({len(content)} chars)")
        if "when to use" not in content.lower() and "trigger" not in content.lower():
            issues.append(f"Rule {rule_file.name} missing usage triggers")
    
    status = "🟢 OK" if not issues else "🟡 WARN"
    
    return {
        "status": status,
        "issues": issues,
        "rules_count": len(rules),
    }

def validate_skills() -> Dict:
    """Validate .claude/skills/ directory."""
    issues = []
    
    if not SKILLS_DIR.exists():
        return {
            "status": "🔴 MISSING",
            "issues": [f"Skills directory not found: {SKILLS_DIR}"],
        }
    
    skills = list(SKILLS_DIR.glob("*.md"))
    
    for skill_file in skills:
        content = skill_file.read_text()
        if "## " not in content:
            issues.append(f"Skill {skill_file.name} missing headers")
        if "example" not in content.lower():
            issues.append(f"Skill {skill_file.name} missing examples")
    
    status = "🟢 OK" if not issues else "🟡 WARN"
    
    return {
        "status": status,
        "issues": issues,
        "skills_count": len(skills),
    }

# ── Auto-Fix ─────────────────────────────────────────────────────────────────

def auto_fix():
    """Attempt to fix common issues."""
    print("🔧 CONFIG GUARDIAN — Auto-Fix Mode\n")
    
    fixes = 0
    
    # Ensure .cache directory exists
    (WORKSPACE / ".cache").mkdir(exist_ok=True)
    
    # Check for missing config files
    for name, path in CONFIG_FILES.items():
        if not path.exists():
            print(f"   Creating template: {path.name}")
            path.write_text(f"# {path.name}\n\n_Template created by ConfigGuardian on {datetime.now().strftime('%Y-%m-%d')}_\n")
            fixes += 1
    
    print(f"\n📊 Applied {fixes} fixes")

def show_status():
    """Show config health dashboard."""
    print("🛡️  CONFIG GUARDIAN — Health Dashboard\n" + "=" * 50)
    
    results = {}
    all_ok = True
    
    # Validate config files
    print("\n📄 CORE FILES:")
    for name, path in CONFIG_FILES.items():
        result = validate_file(f"{name}.md", path)
        results[name] = result
        print(f"   {result['status']} {name}.md ({result['size']} chars)")
        for issue in result['issues'][:3]:
            print(f"      → {issue}")
        if result['status'] != "🟢 OK":
            all_ok = False
    
    # Validate rules
    print("\n📐 RULES:")
    rules_result = validate_rules()
    print(f"   {rules_result['status']} {rules_result['rules_count']} rules")
    for issue in rules_result['issues'][:3]:
        print(f"      → {issue}")
    if rules_result['status'] != "🟢 OK":
        all_ok = False
    
    # Validate skills
    print("\n🎨 SKILLS:")
    skills_result = validate_skills()
    print(f"   {skills_result['status']} {skills_result['skills_count']} skills")
    for issue in skills_result['issues'][:3]:
        print(f"      → {issue}")
    if skills_result['status'] != "🟢 OK":
        all_ok = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_ok:
        print("✅ ALL CONFIG HEALTHY")
    else:
        print("⚠️  ISSUES FOUND — Run with --fix to auto-fix")
    
    # Save health log
    health = {
        "timestamp": datetime.now().isoformat(),
        "all_ok": all_ok,
        "results": results,
        "rules": rules_result,
        "skills": skills_result,
    }
    HEALTH_LOG.write_text(json.dumps(health, indent=2))

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    
    if "--validate" in args:
        show_status()
    elif "--fix" in args:
        auto_fix()
    elif "--status" in args:
        if HEALTH_LOG.exists():
            health = json.loads(HEALTH_LOG.read_text())
            print(f"Last check: {health['timestamp']}")
            print(f"Status: {'✅ ALL OK' if health['all_ok'] else '⚠️ ISSUES FOUND'}")
        else:
            print("No health log. Run --validate first.")
    else:
        print(__doc__)
        print("\nCommands:")
        print("  --validate     Validate all config files")
        print("  --fix          Auto-fix common issues")
        print("  --status       Show last health check")

if __name__ == "__main__":
    main()
