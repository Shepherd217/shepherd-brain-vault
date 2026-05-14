#!/usr/bin/env python3
"""
ReceiptsEngine — Learning Artifacts + Predictive Signals
Hermes has receipts. We make them compounding.

What it does:
- Creates explicit "receipts" for every learning event
- Tracks: what was learned, when, how well it worked, what to try next
- Predictive signals: predicts which receipts will be useful for current task
- Compounding loop: receipts feed into AutoEvolve → AutoEvolve improves receipts
- Receipt quality scoring: not all receipts are equal
- Receipt clustering: find related learnings across time
- Proposal queues: what should be built next based on receipt signals

Usage:
    python receipts_engine.py --create "what I learned"  # Create receipt
    python receipts_engine.py --predict task            # Predict useful receipts
    python receipts_engine.py --queue                   # Show proposal queue
    python receipts_engine.py --status                  # Receipt dashboard
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# ── Config ───────────────────────────────────────────────────────────────────
RECEIPTS_DB = Path.home() / ".openclaw/workspace/.cache/receipts.json"
RECEIPTS_DB.parent.mkdir(parents=True, exist_ok=True)

# ── Receipt Model ─────────────────────────────────────────────────────────────

class Receipt:
    def __init__(self, title: str, learning: str, category: str, 
                 outcome: str = "pending", confidence: float = 0.5):
        self.id = f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.title = title
        self.learning = learning
        self.category = category  # recovery, verification, memory, signal, taste, etc.
        self.outcome = outcome    # pending, success, partial, failure
        self.confidence = confidence
        self.created = datetime.now().isoformat()
        self.applied_count = 0
        self.related_receipts = []
        self.proposal_queue = []  # What this receipt suggests building next
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "learning": self.learning,
            "category": self.category,
            "outcome": self.outcome,
            "confidence": self.confidence,
            "created": self.created,
            "applied_count": self.applied_count,
            "related_receipts": self.related_receipts,
            "proposal_queue": self.proposal_queue,
        }

# ── Receipt Operations ──────────────────────────────────────────────────────

def load_receipts() -> List[Dict]:
    if RECEIPTS_DB.exists():
        return json.loads(RECEIPTS_DB.read_text()).get("receipts", [])
    return []

def save_receipts(receipts: List[Dict]):
    RECEIPTS_DB.write_text(json.dumps({"receipts": receipts}, indent=2))

def create_receipt(title: str, learning: str, category: str, 
                   outcome: str = "pending", confidence: float = 0.5) -> Receipt:
    """Create a new learning receipt."""
    receipt = Receipt(title, learning, category, outcome, confidence)
    receipts = load_receipts()
    receipts.append(receipt.to_dict())
    save_receipts(receipts)
    return receipt

def find_related_receipts(receipt: Dict, all_receipts: List[Dict]) -> List[str]:
    """Find receipts related to this one."""
    related = []
    receipt_words = set(receipt["learning"].lower().split())
    
    for other in all_receipts:
        if other["id"] == receipt["id"]:
            continue
        other_words = set(other["learning"].lower().split())
        common = receipt_words & other_words
        if len(common) >= 3:
            related.append(other["id"])
    
    return related

def predict_useful_receipts(task_description: str) -> List[Dict]:
    """Predict which receipts will be useful for a task."""
    receipts = load_receipts()
    task_words = set(task_description.lower().split())
    
    scored = []
    for receipt in receipts:
        receipt_words = set(receipt["learning"].lower().split())
        common = task_words & receipt_words
        
        # Score by: relevance + confidence + outcome quality
        relevance = len(common) / max(len(task_words), 1)
        confidence = receipt.get("confidence", 0.5)
        outcome_score = {"success": 1.0, "partial": 0.5, "pending": 0.3, "failure": 0.0}.get(
            receipt.get("outcome", "pending"), 0.3
        )
        
        score = relevance * 0.4 + confidence * 0.3 + outcome_score * 0.3
        scored.append((receipt, score))
    
    scored.sort(key=lambda x: x[1], reverse=True)
    return [r for r, s in scored[:5] if s > 0.2]

def generate_proposal_queue() -> List[Dict]:
    """Generate proposal queue from receipts."""
    receipts = load_receipts()
    
    # Find patterns in what needs building
    categories = {}
    for receipt in receipts:
        cat = receipt["category"]
        if cat not in categories:
            categories[cat] = {"count": 0, "confidence": 0, "proposals": []}
        categories[cat]["count"] += 1
        categories[cat]["confidence"] += receipt.get("confidence", 0.5)
        categories[cat]["proposals"].extend(receipt.get("proposal_queue", []))
    
    # Score categories
    scored = []
    for cat, data in categories.items():
        avg_confidence = data["confidence"] / data["count"] if data["count"] else 0
        score = data["count"] * 0.4 + avg_confidence * 0.6
        scored.append({
            "category": cat,
            "score": score,
            "receipt_count": data["count"],
            "avg_confidence": avg_confidence,
            "proposals": list(set(data["proposals"]))[:5],  # Top 5 unique
        })
    
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored

def show_dashboard():
    """Show receipts dashboard."""
    receipts = load_receipts()
    
    print("📜 RECEIPTS ENGINE — Learning Dashboard\n" + "=" * 50)
    print(f"Total receipts: {len(receipts)}\n")
    
    if not receipts:
        print("No receipts yet. Create one with --create")
        return
    
    # By category
    categories = {}
    for receipt in receipts:
        cat = receipt["category"]
        if cat not in categories:
            categories[cat] = {"count": 0, "success": 0}
        categories[cat]["count"] += 1
        if receipt.get("outcome") == "success":
            categories[cat]["success"] += 1
    
    print("By category:")
    for cat, data in sorted(categories.items(), key=lambda x: x[1]["count"], reverse=True):
        rate = (data["success"] / data["count"] * 100) if data["count"] else 0
        print(f"   {cat}: {data['count']} receipts ({rate:.0f}% success)")
    
    # Outcome distribution
    outcomes = {}
    for receipt in receipts:
        o = receipt.get("outcome", "pending")
        outcomes[o] = outcomes.get(o, 0) + 1
    
    print(f"\nOutcome distribution:")
    for outcome, count in outcomes.items():
        print(f"   {outcome}: {count}")
    
    # Recent receipts
    print(f"\nRecent receipts:")
    for receipt in receipts[-5:]:
        status = "✅" if receipt.get("outcome") == "success" else "⏳"
        print(f"   {status} [{receipt['category']}] {receipt['title'][:60]}")

# ── Compounding Loop Integration ─────────────────────────────────────────────

def run_compounding_loop():
    """Run one iteration of the compounding loop."""
    print("🔄 RECEIPTS ENGINE — Compounding Loop\n")
    
    # 1. Check receipts → find patterns
    queue = generate_proposal_queue()
    
    if not queue:
        print("No proposals yet. Create receipts first.")
        return
    
    print("Top proposal categories:")
    for item in queue[:3]:
        print(f"\n📌 {item['category']} (score: {item['score']:.2f})")
        print(f"   Based on {item['receipt_count']} receipts")
        print(f"   Avg confidence: {item['avg_confidence']:.2f}")
        if item["proposals"]:
            print(f"   Proposed builds:")
            for proposal in item["proposals"]:
                print(f"      → {proposal}")
    
    # 2. Update related receipts
    receipts = load_receipts()
    updated = 0
    for receipt in receipts:
        related = find_related_receipts(receipt, receipts)
        if related and not receipt.get("related_receipts"):
            receipt["related_receipts"] = related[:5]
            updated += 1
    
    if updated:
        save_receipts(receipts)
        print(f"\n🔗 Linked {updated} receipts to related learnings")

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    
    if "--create" in args:
        idx = args.index("--create")
        if idx + 3 < len(args):
            title = args[idx + 1]
            learning = args[idx + 2]
            category = args[idx + 3]
            receipt = create_receipt(title, learning, category)
            print(f"📜 Receipt created: {receipt.id}")
            print(f"   Title: {receipt.title}")
            print(f"   Category: {receipt.category}")
        else:
            print("Usage: --create 'title' 'learning' category")
    elif "--predict" in args:
        idx = args.index("--predict")
        if idx + 1 < len(args):
            task = args[idx + 1]
            receipts = predict_useful_receipts(task)
            print(f"🔮 Predicted useful receipts for '{task}':")
            for receipt in receipts:
                print(f"   [{receipt['category']}] {receipt['title'][:60]}")
                print(f"      Learning: {receipt['learning'][:100]}...")
        else:
            print("Usage: --predict 'task description'")
    elif "--queue" in args:
        queue = generate_proposal_queue()
        print("📋 Proposal Queue:\n")
        for item in queue[:5]:
            print(f"{item['category']}: {item['score']:.2f} ({item['receipt_count']} receipts)")
    elif "--loop" in args:
        run_compounding_loop()
    elif "--status" in args:
        show_dashboard()
    else:
        print(__doc__)
        print("\nCommands:")
        print("  --create title learning category   Create receipt")
        print("  --predict task                     Predict useful receipts")
        print("  --queue                            Show proposal queue")
        print("  --loop                             Run compounding loop")
        print("  --status                           Show dashboard")

if __name__ == "__main__":
    main()
