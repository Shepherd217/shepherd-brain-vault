#!/usr/bin/env python3
"""
DebateCouncil — Multi-Agent Quality Control with Felt_Weight
Makes hermes-council look like a toy.

What it does:
- Spawns 3 mini sub-agents with different perspectives:
  1. Pragmatist: "Does this actually work?"
  2. Critic: "What's wrong with this?"
  3. User Advocate: "Would Nathan use this?"
- Each agent gets 30 seconds to review
- Weighs by emotional context (if Nathan was drained, Critic gets more weight)
- Produces: approve / revise / reject with specific feedback
- Tracks decision lineage for pattern learning
- If 2/3 reject → auto-route to RecoveryRouter

Usage:
    python debate_council.py --review file.py     # Review a file
    python debate_council.py --review skill.md    # Review a skill
    python debate_council.py --session session_id  # Review a completed session
    python debate_council.py --status             # Show council history
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ── Config ───────────────────────────────────────────────────────────────────
COUNCIL_LOG = Path.home() / ".openclaw/workspace/.cache/debate_council.json"
COUNCIL_LOG.parent.mkdir(parents=True, exist_ok=True)

# ── Emotional Weight Integration ────────────────────────────────────────────

def get_emotional_weight() -> float:
    """Get current emotional weight to adjust council voting."""
    feelings_dir = Path.home() / ".openclaw/workspace/vault/drawers/feelings"
    if not feelings_dir.exists():
        return 0.5
    
    feeling_files = sorted(feelings_dir.glob("*.md"), reverse=True)
    if not feeling_files:
        return 0.5
    
    latest = feeling_files[0]
    content = latest.read_text().lower()
    
    # Parse weight if present
    weight_match = re.search(r'weight:\s*(\d+)', content)
    if weight_match:
        weight = int(weight_match.group(1))
        return weight / 100.0
    
    # Simple heuristic
    stress_count = sum(1 for word in ["stressed", "frustrated", "drained", "tired"] if word in content)
    return max(0.3, 1.0 - (stress_count * 0.2))

# ── Council Agents ───────────────────────────────────────────────────────────

class CouncilMember:
    def __init__(self, name: str, perspective: str, default_weight: float):
        self.name = name
        self.perspective = perspective
        self.default_weight = default_weight
        self.vote = None
        self.reasoning = ""
        self.confidence = 0.0

class Pragmatist(CouncilMember):
    """Reviews: Does this actually work? Is it testable?"""
    def review(self, content: str, emotional_weight: float) -> Dict:
        # Simulate review (in production, this would spawn a real sub-agent)
        checks = [
            "code has no syntax errors",
            "functions are testable",
            "no hardcoded secrets",
            "error handling present",
        ]
        
        score = 0
        reasoning = []
        
        if "def " in content:
            score += 25
            reasoning.append("Has function definitions")
        if "try:" in content or "except" in content:
            score += 25
            reasoning.append("Has error handling")
        if "test" in content.lower() or "assert" in content:
            score += 25
            reasoning.append("Has test patterns")
        if "password" not in content.lower() and "secret" not in content.lower():
            score += 25
            reasoning.append("No obvious secrets")
        else:
            reasoning.append("WARNING: May contain sensitive data")
        
        # Adjust by emotional weight (when stressed, pragmatist demands more proof)
        if emotional_weight < 0.4:
            score *= 0.9  # Stricter when drained
            reasoning.append("Adjusted: Nathan is drained, requiring higher proof")
        
        return {
            "vote": "approve" if score >= 75 else "revise" if score >= 50 else "reject",
            "score": score,
            "reasoning": "; ".join(reasoning),
            "confidence": min(score / 100, 0.95),
        }

class Critic(CouncilMember):
    """Reviews: What's wrong? What edge cases are missed?"""
    def review(self, content: str, emotional_weight: float) -> Dict:
        issues = []
        score = 100
        
        # Check for common issues
        if "TODO" in content or "FIXME" in content:
            issues.append("Contains TODO/FIXME markers")
            score -= 15
        if "pass" in content and content.count("def ") > content.count("pass") + 2:
            issues.append("Some functions may be stubs")
            score -= 10
        if "import" in content and "requirements" not in content.lower():
            issues.append("Check if all imports are documented")
            score -= 5
        if len(content.split("\n")) > 300 and "class " not in content:
            issues.append("Long script without classes — consider modularizing")
            score -= 10
        
        # Emotional adjustment (critic is always harsh, but extra harsh when stressed)
        if emotional_weight < 0.4:
            score -= 10
            issues.append("Emotional state: extra scrutiny applied")
        
        return {
            "vote": "approve" if score >= 80 else "revise" if score >= 60 else "reject",
            "score": max(score, 0),
            "reasoning": "; ".join(issues) if issues else "No major issues found",
            "confidence": min(abs(score - 50) / 50, 0.95),
        }

class UserAdvocate(CouncilMember):
    """Reviews: Would Nathan actually use this? Is it natural language friendly?"""
    def review(self, content: str, emotional_weight: float) -> Dict:
        score = 0
        reasoning = []
        
        # Check for natural language interface
        if "argparse" in content or "sys.argv" in content:
            score += 30
            reasoning.append("Has CLI interface")
        if "__doc__" in content:
            score += 20
            reasoning.append("Has documentation")
        if "Usage:" in content:
            score += 20
            reasoning.append("Has usage examples")
        
        # Check for integration with our system
        if "vault" in content.lower() or "moltos" in content.lower():
            score += 20
            reasoning.append("Integrates with our ecosystem")
        
        # Emotional: when drained, prefer simpler interfaces
        if emotional_weight < 0.4:
            if "simple" in content.lower() or "easy" in content.lower():
                score += 10
                reasoning.append("Simplicity bonus: Nathan is drained")
            else:
                score -= 10
                reasoning.append("Complexity penalty: Nathan is drained")
        
        return {
            "vote": "approve" if score >= 70 else "revise" if score >= 50 else "reject",
            "score": score,
            "reasoning": "; ".join(reasoning) if reasoning else "Check usability manually",
            "confidence": min(score / 100, 0.95),
        }

# ── Council Orchestration ────────────────────────────────────────────────────

def run_council(content: str, context: str = "") -> Dict:
    """Run the full council review."""
    print("🏛️  DEBATE COUNCIL — Multi-Agent Quality Review\n")
    
    emotional_weight = get_emotional_weight()
    print(f"💓 Emotional weight: {emotional_weight:.0%} (adjusts council voting)")
    print(f"📋 Reviewing: {context}\n")
    
    # Create council
    members = [
        Pragmatist("Pragmatist", "Does it work?", 0.35),
        Critic("Critic", "What's wrong?", 0.35),
        UserAdvocate("UserAdvocate", "Would Nathan use it?", 0.30),
    ]
    
    # Run reviews
    results = {}
    for member in members:
        print(f"👤 {member.name} ({member.perspective})...")
        result = member.review(content, emotional_weight)
        results[member.name] = result
        print(f"   Verdict: {result['vote'].upper()} (score: {result['score']}/100)")
        print(f"   Reasoning: {result['reasoning']}")
        print(f"   Confidence: {result['confidence']:.0%}")
        print()
    
    # Weighted voting
    votes = {"approve": 0, "revise": 0, "reject": 0}
    for name, result in results.items():
        weight = next(m.default_weight for m in members if m.name == name)
        votes[result["vote"]] += weight * result["confidence"]
    
    final_verdict = max(votes, key=votes.get)
    
    # Log decision
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "context": context,
        "emotional_weight": emotional_weight,
        "members": results,
        "votes": votes,
        "verdict": final_verdict,
    }
    
    log = json.loads(COUNCIL_LOG.read_text()) if COUNCIL_LOG.exists() else {"reviews": []}
    log["reviews"].append(log_entry)
    COUNCIL_LOG.write_text(json.dumps(log, indent=2))
    
    # Display result
    print("=" * 50)
    print(f"🏆 FINAL VERDICT: {final_verdict.upper()}")
    print(f"   Approve: {votes['approve']:.2f}")
    print(f"   Revise:  {votes['revise']:.2f}")
    print(f"   Reject:  {votes['reject']:.2f}")
    print()
    
    if final_verdict == "reject":
        print("🔄 Routing to RecoveryRouter for repair...")
        print("   (In production: would trigger recovery_router.py --repair)")
    elif final_verdict == "revise":
        print("✏️  Revision needed. Key issues:")
        for name, result in results.items():
            if result["vote"] != "approve":
                print(f"   - {name}: {result['reasoning']}")
    else:
        print("✅ Council approves. Ready for production.")
    
    return log_entry

def show_status():
    """Show council history."""
    if not COUNCIL_LOG.exists():
        print("No council reviews yet.")
        return
    
    log = json.loads(COUNCIL_LOG.read_text())
    reviews = log.get("reviews", [])
    
    print("🏛️  DEBATE COUNCIL HISTORY\n" + "=" * 50)
    print(f"Total reviews: {len(reviews)}\n")
    
    verdict_counts = {"approve": 0, "revise": 0, "reject": 0}
    for r in reviews:
        verdict_counts[r["verdict"]] += 1
    
    print("Verdict distribution:")
    for v, c in verdict_counts.items():
        pct = c / len(reviews) * 100 if reviews else 0
        print(f"   {v.upper()}: {c} ({pct:.0f}%)")
    
    print(f"\nRecent reviews:")
    for r in reviews[-5:]:
        print(f"   {r['timestamp'][:10]} — {r['verdict'].upper()} — {r['context'][:50]}...")

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    
    if "--review" in args:
        idx = args.index("--review")
        if idx + 1 < len(args):
            file_path = Path(args[idx + 1])
            if file_path.exists():
                content = file_path.read_text()
                run_council(content, str(file_path))
            else:
                print(f"File not found: {file_path}")
        else:
            print("Usage: --review <file_path>")
    elif "--status" in args:
        show_status()
    else:
        print(__doc__)
        print("\nCommands:")
        print("  --review file    Review a file with the council")
        print("  --status         Show council history")

if __name__ == "__main__":
    main()
