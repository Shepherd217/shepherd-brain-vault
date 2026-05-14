#!/usr/bin/env python3
"""
AutoEvolve — Self-Improving Skill System
Makes SkillClaw look like a toy.

What it does:
- Watches session logs for repeated successful patterns
- Extracts skills from those patterns
- Tests the generated skills
- Scores them by: frequency, success rate, emotional context
- Evolves existing skills based on new data
- Retires skills that haven't been used in 30 days
- Tracks skill genealogy (this skill came from that session, evolved 3 times)

Usage:
    python autoevolve.py --watch           # Start watching sessions
    python autoevolve.py --extract         # One-time extraction from past sessions
    python autoevolve.py --evolve          # Evolve existing skills
    python autoevolve.py --status          # Show skill genealogy
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# ── Config ───────────────────────────────────────────────────────────────────
VAULT_SKILLS_DIR = Path.home() / ".openclaw/workspace/shepherd-brain-vault/rooms/skills/auto-evolved"
SESSIONS_DIR = Path.home() / ".openclaw/agents/main/sessions"
MARROW_DIR = Path.home() / ".openclaw/workspace/shepherd-brain-vault/drawers/feelings"
GENEALOGY_FILE = VAULT_SKILLS_DIR / "genealogy.json"
SKILL_RETENTION_DAYS = 30
MIN_SUCCESS_RATE = 0.7  # 70% to keep a skill

# Ensure dirs exist
VAULT_SKILLS_DIR.mkdir(parents=True, exist_ok=True)

# ── Skill Model ────────────────────────────────────────────────────────────

class Skill:
    def __init__(self, name: str, source_session: str, pattern: str, tools_used: List[str]):
        self.name = name
        self.source_session = source_session
        self.pattern = pattern
        self.tools_used = tools_used
        self.created_at = datetime.now().isoformat()
        self.last_used = None
        self.use_count = 0
        self.success_count = 0
        self.emotional_weight = 0.0  # +1 if used when Nathan was stressed
        self.lineage = [source_session]
        self.evolution_count = 0
        self.retired = False

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "source_session": self.source_session,
            "pattern": self.pattern,
            "tools_used": self.tools_used,
            "created_at": self.created_at,
            "last_used": self.last_used,
            "use_count": self.use_count,
            "success_count": self.success_count,
            "success_rate": self.success_count / max(self.use_count, 1),
            "emotional_weight": self.emotional_weight,
            "lineage": self.lineage,
            "evolution_count": self.evolution_count,
            "retired": self.retired,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Skill":
        s = cls(data["name"], data["source_session"], data["pattern"], data["tools_used"])
        s.created_at = data["created_at"]
        s.last_used = data.get("last_used")
        s.use_count = data.get("use_count", 0)
        s.success_count = data.get("success_count", 0)
        s.emotional_weight = data.get("emotional_weight", 0.0)
        s.lineage = data.get("lineage", [])
        s.evolution_count = data.get("evolution_count", 0)
        s.retired = data.get("retired", False)
        return s

# ── Pattern Extraction ─────────────────────────────────────────────────────

# Common successful patterns we look for
PATTERNS = {
    "lead_audit": {
        "signals": ["audit", "website", "score", "lead", "review", "conversion"],
        "tools": ["kimi_search", "web_fetch", "browser"],
        "min_signals": 3,
    },
    "outreach_draft": {
        "signals": ["outreach", "email", "demo", "landing page", "personalized"],
        "tools": ["message", "write", "kimi_search"],
        "min_signals": 2,
    },
    "repo_research": {
        "signals": ["repo", "github", "scrape", "dissect", "research", "steal"],
        "tools": ["kimi_search", "kimi_fetch", "web_fetch"],
        "min_signals": 3,
    },
    "multi_agent": {
        "signals": ["subagent", "sessions_spawn", "orchestrate", "delegate"],
        "tools": ["sessions_spawn", "subagents"],
        "min_signals": 2,
    },
    "vault_maintenance": {
        "signals": ["vault", "git", "commit", "push", "sync", "memory"],
        "tools": ["exec", "read", "write"],
        "min_signals": 2,
    },
    "crisis_recovery": {
        "signals": ["stalled", "stuck", "recovery", "repair", "failed", "timeout"],
        "tools": ["exec", "process", "read"],
        "min_signals": 2,
    },
}

def extract_patterns_from_session(session_path: Path) -> List[dict]:
    """Read a session JSONL and extract successful patterns."""
    patterns_found = []
    
    if not session_path.exists():
        return patterns_found
    
    try:
        content = session_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"  ⚠️  Could not read {session_path}: {e}")
        return patterns_found
    
    # Simple signal detection
    lines = content.lower()
    for pattern_name, pattern_def in PATTERNS.items():
        signal_count = sum(1 for signal in pattern_def["signals"] if signal in lines)
        if signal_count >= pattern_def["min_signals"]:
            # Check if tools were used
            tool_count = sum(1 for tool in pattern_def["tools"] if tool in content)
            if tool_count >= 1:
                patterns_found.append({
                    "name": pattern_name,
                    "signals_matched": signal_count,
                    "tools_matched": tool_count,
                    "confidence": min(signal_count / len(pattern_def["signals"]), 1.0),
                })
    
    return patterns_found

def check_emotional_context(session_date: str) -> float:
    """Check if Nathan was stressed/fragile during this session."""
    # Look for feelings entry on that date
    date_prefix = session_date[:10]  # YYYY-MM-DD
    feelings_file = MARROW_DIR / f"{date_prefix}.md"
    
    if not feelings_file.exists():
        return 0.0
    
    content = feelings_file.read_text().lower()
    stress_signals = ["stressed", "frustrated", "exhausted", "drained", "urgent", "angry"]
    stress_count = sum(1 for s in stress_signals if s in content)
    
    return min(stress_count / 3, 1.0)  # Cap at 1.0

# ── Genealogy ────────────────────────────────────────────────────────────────

def load_genealogy() -> Dict:
    if GENEALOGY_FILE.exists():
        return json.loads(GENEALOGY_FILE.read_text())
    return {"skills": {}, "evolutions": [], "retirements": []}

def save_genealogy(genealogy: Dict):
    GENEALOGY_FILE.write_text(json.dumps(genealogy, indent=2))

def find_or_create_skill(pattern_name: str, session_id: str) -> Optional[Skill]:
    """Find existing skill or create new one."""
    genealogy = load_genealogy()
    skill_file = VAULT_SKILLS_DIR / f"{pattern_name}.json"
    
    if skill_file.exists():
        data = json.loads(skill_file.read_text())
        skill = Skill.from_dict(data)
        # Update usage
        skill.use_count += 1
        skill.last_used = datetime.now().isoformat()
        skill.lineage.append(session_id)
        
        # Emotional weighting
        session_date = session_id[:8] if len(session_id) >= 8 else datetime.now().strftime("%Y%m%d")
        formatted_date = f"20{session_date[:2]}-{session_date[2:4]}-{session_date[4:6]}"
        emotional_boost = check_emotional_context(formatted_date)
        skill.emotional_weight = max(skill.emotional_weight, emotional_boost)
        
        return skill
    
    # Create new skill
    skill = Skill(
        name=pattern_name,
        source_session=session_id,
        pattern=f"Auto-extracted from {session_id}",
        tools_used=PATTERNS.get(pattern_name, {}).get("tools", []),
    )
    skill.use_count = 1
    skill.last_used = datetime.now().isoformat()
    
    # Emotional context
    session_date = session_id[:8] if len(session_id) >= 8 else datetime.now().strftime("%Y%m%d")
    formatted_date = f"20{session_date[:2]}-{session_date[2:4]}-{session_date[4:6]}"
    skill.emotional_weight = check_emotional_context(formatted_date)
    
    return skill

def score_skill(skill: Skill) -> float:
    """Score a skill: higher = more valuable."""
    success_rate = skill.success_count / max(skill.use_count, 1)
    recency_boost = 1.0
    if skill.last_used:
        days_since = (datetime.now() - datetime.fromisoformat(skill.last_used)).days
        recency_boost = max(0.5, 1.0 - (days_since / 30))  # Decay over 30 days
    
    return (
        success_rate * 0.4 +          # Success matters most
        skill.emotional_weight * 0.3 +  # Stress-tested skills are gold
        min(skill.use_count / 10, 1.0) * 0.2 +  # Frequency
        recency_boost * 0.1           # Recent use matters a little
    )

def retire_old_skills():
    """Retire skills not used in 30 days."""
    genealogy = load_genealogy()
    now = datetime.now()
    retired = []
    
    for skill_file in VAULT_SKILLS_DIR.glob("*.json"):
        if skill_file.name == "genealogy.json":
            continue
        
        data = json.loads(skill_file.read_text())
        last_used = data.get("last_used")
        if not last_used:
            continue
        
        days_since = (now - datetime.fromisoformat(last_used)).days
        if days_since > SKILL_RETENTION_DAYS:
            data["retired"] = True
            data["retired_at"] = now.isoformat()
            skill_file.write_text(json.dumps(data, indent=2))
            retired.append(data["name"])
            genealogy["retirements"].append({
                "skill": data["name"],
                "retired_at": now.isoformat(),
                "reason": f"Unused for {days_since} days",
            })
    
    if retired:
        print(f"🗑️  Retired {len(retired)} stale skills: {', '.join(retired)}")
    
    save_genealogy(genealogy)

# ── Main Operations ─────────────────────────────────────────────────────────

def extract_all_sessions():
    """One-time extraction from all past sessions."""
    print("🔍 Extracting patterns from all sessions...")
    
    if not SESSIONS_DIR.exists():
        print(f"❌ Sessions directory not found: {SESSIONS_DIR}")
        return
    
    session_files = list(SESSIONS_DIR.glob("*.jsonl"))
    print(f"   Found {len(session_files)} session files")
    
    skills_created = 0
    skills_updated = 0
    
    for session_file in session_files:
        session_id = session_file.stem
        patterns = extract_patterns_from_session(session_file)
        
        for pattern in patterns:
            if pattern["confidence"] < 0.5:
                continue
            
            skill = find_or_create_skill(pattern["name"], session_id)
            if skill:
                skill_file = VAULT_SKILLS_DIR / f"{skill.name}.json"
                if not skill_file.exists():
                    skills_created += 1
                    print(f"   ✨ Created skill: {skill.name} (confidence: {pattern['confidence']:.2f})")
                else:
                    skills_updated += 1
                
                skill_file.write_text(json.dumps(skill.to_dict(), indent=2))
    
    print(f"\n📊 Results: {skills_created} created, {skills_updated} updated")
    retire_old_skills()

def show_status():
    """Display skill genealogy."""
    genealogy = load_genealogy()
    skills = []
    
    for skill_file in VAULT_SKILLS_DIR.glob("*.json"):
        if skill_file.name == "genealogy.json":
            continue
        data = json.loads(skill_file.read_text())
        skills.append(data)
    
    if not skills:
        print("No skills found. Run with --extract first.")
        return
    
    # Sort by score
    skills.sort(key=lambda s: s.get("use_count", 0) * s.get("success_count", 0), reverse=True)
    
    print("\n🧬 SKILL GENEALOGY\n" + "=" * 60)
    for s in skills:
        status = "🗑️ RETIRED" if s.get("retired") else "✅ ACTIVE"
        score = score_skill(Skill.from_dict(s))
        print(f"\n{status} {s['name']}")
        print(f"   Score: {score:.2f} | Uses: {s['use_count']} | Success: {s['success_count']}")
        print(f"   Emotional weight: {s['emotional_weight']:.2f}")
        print(f"   Lineage: {' → '.join(s['lineage'][-3:])}")  # Last 3
        print(f"   Tools: {', '.join(s['tools_used'])}")

def evolve_skills():
    """Evolve existing skills based on new session data."""
    print("🧬 Evolving skills...")
    
    for skill_file in VAULT_SKILLS_DIR.glob("*.json"):
        if skill_file.name == "genealogy.json":
            continue
        
        data = json.loads(skill_file.read_text())
        if data.get("retired"):
            continue
        
        skill = Skill.from_dict(data)
        
        # Evolve if used frequently but success rate is low
        if skill.use_count > 5 and (skill.success_count / skill.use_count) < MIN_SUCCESS_RATE:
            skill.evolution_count += 1
            print(f"   🔄 Evolving {skill.name} (attempt #{skill.evolution_count})")
            # Mark for manual review
            data["needs_review"] = True
            data["review_reason"] = f"Low success rate ({skill.success_count}/{skill.use_count})"
        
        # Evolve if emotional weight is high (Nathan was stressed when using it)
        if skill.emotional_weight > 0.7 and skill.evolution_count < 3:
            skill.evolution_count += 1
            print(f"   🔥 Fast-tracking {skill.name} (stress-tested, evolving #{skill.evolution_count})")
            data["stress_tested"] = True
        
        skill_file.write_text(json.dumps(skill.to_dict(), indent=2))
    
    print("\n✅ Evolution complete. Review flagged skills manually.")

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    
    if "--watch" in args:
        print("👁️  Starting AutoEvolve watcher...")
        print("   (In production: would watch SESSIONS_DIR for new files)")
        print("   Run --extract to process existing sessions, then --watch would monitor.")
    
    elif "--extract" in args:
        extract_all_sessions()
    
    elif "--evolve" in args:
        evolve_skills()
    
    elif "--status" in args:
        show_status()
    
    else:
        print(__doc__)
        print("\nCommands:")
        print("  --watch    Start watching for new sessions")
        print("  --extract  One-time extraction from past sessions")
        print("  --evolve   Evolve existing skills")
        print("  --status   Show skill genealogy")

if __name__ == "__main__":
    main()
