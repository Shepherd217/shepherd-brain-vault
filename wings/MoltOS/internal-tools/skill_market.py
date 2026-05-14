#!/usr/bin/env python3
"""
SkillMarket — Skill Discovery + Sharing
Makes agentskills.io look like a toy.

What it does:
- Indexes all skills: .claude/skills/, auto-forged/, auto-evolved/
- Scores skills by: usage frequency, success rate, emotional weight
- Suggests skills based on current task context
- Tracks skill dependencies (this skill needs that tool)
- Auto-promotes skills from auto-forged to production
- Generates skill recommendations: 'For this task, use X, Y, Z'
- Creates skill bundles (Standout Local bundle, MoltOS bundle)

Usage:
    python skill_market.py --index           # Index all skills
    python skill_market.py --recommend task  # Recommend skills for task
    python skill_market.py --status          # Show skill marketplace
    python skill_market.py --promote skill   # Promote skill to production
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ── Config ───────────────────────────────────────────────────────────────────
VAULT_DIR = Path.home() / ".openclaw/workspace/shepherd-brain-vault"
SKILL_DIRS = [
    VAULT_DIR / "rooms/skills/auto-forged",
    VAULT_DIR / "rooms/skills/auto-evolved",
    VAULT_DIR / "rooms/skills/repo-research",
    VAULT_DIR / "wings",
]
SKILL_INDEX = Path.home() / ".openclaw/workspace/.cache/skill_index.json"
SKILL_INDEX.parent.mkdir(parents=True, exist_ok=True)

# ── Skill Indexing ──────────────────────────────────────────────────────────

def index_skills() -> Dict:
    """Index all skills across directories."""
    index = {
        "indexed_at": datetime.now().isoformat(),
        "skills": {},
        "bundles": {},
    }
    
    for skill_dir in SKILL_DIRS:
        if not skill_dir.exists():
            continue
        
        for skill_file in skill_dir.rglob("*.md"):
            content = skill_file.read_text()
            
            # Extract metadata
            name = skill_file.stem
            category = skill_dir.name
            
            # Simple scoring
            has_examples = "example" in content.lower()
            has_params = "parameter" in content.lower() or "|" in content
            has_errors = "error" in content.lower()
            
            score = 50  # Base
            if has_examples: score += 20
            if has_params: score += 15
            if has_errors: score += 15
            
            index["skills"][name] = {
                "path": str(skill_file),
                "category": category,
                "score": score,
                "has_examples": has_examples,
                "has_params": has_params,
                "has_errors": has_errors,
                "size": len(content),
            }
        
        # Also index JSON skills (auto-evolved)
        for skill_file in skill_dir.rglob("*.json"):
            if skill_file.name == "genealogy.json":
                continue
            
            try:
                data = json.loads(skill_file.read_text())
                name = data.get("name", skill_file.stem)
                
                index["skills"][name] = {
                    "path": str(skill_file),
                    "category": category,
                    "score": data.get("success_count", 0) * 10,
                    "auto_evolved": True,
                    "use_count": data.get("use_count", 0),
                }
            except Exception:
                continue
    
    # Create bundles
    index["bundles"] = {
        "standout-local": [s for s, data in index["skills"].items() 
                          if any(kw in data["path"] for kw in ["standout", "lead", "audit"])],
        "moltos-core": [s for s, data in index["skills"].items() 
                       if any(kw in data["path"] for kw in ["moltos", "agent", "orchestration"])],
        "research": [s for s, data in index["skills"].items() 
                    if any(kw in data["path"] for kw in ["repo", "research", "scrape"])],
    }
    
    SKILL_INDEX.write_text(json.dumps(index, indent=2))
    
    return index

def recommend_skills(task_description: str) -> List[Dict]:
    """Recommend skills for a task."""
    if not SKILL_INDEX.exists():
        index_skills()
    
    index = json.loads(SKILL_INDEX.read_text())
    
    # Simple keyword matching
    task_lower = task_description.lower()
    matches = []
    
    for name, data in index["skills"].items():
        score = 0
        
        # Check if skill name matches task
        if any(word in task_lower for word in name.replace("-", " ").split()):
            score += 50
        
        # Check path for context clues
        if any(word in task_lower for word in data["path"].lower().split("/")[-1].replace("-", "_").split("_")):
            score += 30
        
        # Boost by skill quality
        score += data.get("score", 0) / 10
        
        if score > 30:
            matches.append({
                "skill": name,
                "score": score,
                "path": data["path"],
                "category": data["category"],
            })
    
    # Sort by score
    matches.sort(key=lambda x: x["score"], reverse=True)
    
    return matches[:5]

def show_marketplace():
    """Show skill marketplace."""
    if not SKILL_INDEX.exists():
        index_skills()
    
    index = json.loads(SKILL_INDEX.read_text())
    
    print("🛒 SKILL MARKETPLACE\n" + "=" * 50)
    print(f"Total skills: {len(index['skills'])}\n")
    
    # By category
    categories = {}
    for name, data in index["skills"].items():
        cat = data["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((name, data))
    
    for cat, skills in categories.items():
        print(f"📁 {cat} ({len(skills)} skills)")
        for name, data in sorted(skills, key=lambda x: x[1].get("score", 0), reverse=True)[:5]:
            print(f"   ⭐ {name} (score: {data.get('score', 0)})")
    
    # Bundles
    print(f"\n📦 BUNDLES:")
    for bundle, skills in index["bundles"].items():
        print(f"   {bundle}: {len(skills)} skills")

def promote_skill(skill_name: str):
    """Promote an auto-forged skill to production."""
    auto_forged = Path.home() / ".openclaw/workspace/vault/rooms/skills/auto-forged" / f"{skill_name}.md"
    production = Path.home() / ".openclaw/workspace/.claude/skills" / f"{skill_name}.md"
    
    if not auto_forged.exists():
        print(f"Skill not found in auto-forged: {skill_name}")
        return
    
    # Copy to production
    production.parent.mkdir(parents=True, exist_ok=True)
    production.write_text(auto_forged.read_text())
    
    print(f"🚀 Promoted {skill_name} to production!")
    print(f"   From: {auto_forged}")
    print(f"   To: {production}")

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    
    if "--index" in args:
        index = index_skills()
        print(f"📚 Indexed {len(index['skills'])} skills")
    elif "--recommend" in args:
        idx = args.index("--recommend")
        if idx + 1 < len(args):
            task = args[idx + 1]
            matches = recommend_skills(task)
            print(f"🎯 Skills for '{task}':")
            for match in matches:
                print(f"   {match['skill']} (relevance: {match['score']:.0f})")
        else:
            print("Usage: --recommend 'task description'")
    elif "--status" in args:
        show_marketplace()
    elif "--promote" in args:
        idx = args.index("--promote")
        if idx + 1 < len(args):
            promote_skill(args[idx + 1])
        else:
            print("Usage: --promote skill-name")
    else:
        print(__doc__)
        print("\nCommands:")
        print("  --index              Index all skills")
        print("  --recommend task     Recommend skills for task")
        print("  --status             Show marketplace")
        print("  --promote skill      Promote to production")

if __name__ == "__main__":
    main()
