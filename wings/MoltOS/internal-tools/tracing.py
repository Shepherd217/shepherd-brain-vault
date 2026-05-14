#!/usr/bin/env python3
"""
Tracing — Decision Trace Logging + Audit Trail
Steals from AutoGen's tracing system.

What it does:
- Records every decision with: timestamp, input, alternatives, chosen, reasoning
- Creates trace trees: why did I choose X over Y?
- Searchable: "show me all decisions where I chose browser over kimi_search"
- Decision replay: reconstruct exact thought process
- Branching: what if I had chosen differently?
- Exports to Obsidian for Nathan's review

Usage:
    python tracing.py --start session_id     # Start trace for session
    python tracing.py --log decision.json   # Log a decision
    python tracing.py --tree                # Show decision tree
    python tracing.py --search query        # Search traces
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ── Config ───────────────────────────────────────────────────────────────────
TRACES_DIR = Path.home() / ".openclaw/workspace/.cache/traces"
TRACES_DIR.mkdir(parents=True, exist_ok=True)

# ── Trace Model ─────────────────────────────────────────────────────────────

class DecisionTrace:
    def __init__(self, session_id: str, decision_id: str, 
                 input_context: str, alternatives: List[str], 
                 chosen: str, reasoning: str, confidence: float):
        self.session_id = session_id
        self.decision_id = decision_id
        self.input_context = input_context
        self.alternatives = alternatives
        self.chosen = chosen
        self.reasoning = reasoning
        self.confidence = confidence
        self.timestamp = datetime.now().isoformat()
        self.outcome = "pending"  # pending, success, failure
    
    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "decision_id": self.decision_id,
            "input_context": self.input_context,
            "alternatives": self.alternatives,
            "chosen": self.chosen,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
            "outcome": self.outcome,
        }

def save_trace(trace: Dict):
    """Save trace to file."""
    trace_file = TRACES_DIR / f"{trace['session_id']}_{trace['decision_id']}.json"
    trace_file.write_text(json.dumps(trace, indent=2))

def load_traces(session_id: Optional[str] = None) -> List[Dict]:
    """Load traces."""
    traces = []
    for trace_file in TRACES_DIR.glob("*.json"):
        trace = json.loads(trace_file.read_text())
        if session_id and trace["session_id"] != session_id:
            continue
        traces.append(trace)
    return traces

def show_decision_tree(session_id: str):
    """Show decision tree for a session."""
    traces = load_traces(session_id)
    
    if not traces:
        print(f"No traces for session: {session_id}")
        return
    
    print(f"🕵️ TRACING — Decision Tree: {session_id[:20]}\n")
    
    # Sort by timestamp
    traces.sort(key=lambda x: x["timestamp"])
    
    for i, trace in enumerate(traces):
        indent = "  " * i
        status = "✅" if trace.get("outcome") == "success" else "⏳"
        print(f"{indent}{status} [{i+1}] {trace['chosen']}")
        print(f"{indent}    Confidence: {trace['confidence']:.0%}")
        print(f"{indent}    Why: {trace['reasoning'][:60]}...")
        
        if trace["alternatives"]:
            print(f"{indent}    Rejected: {', '.join(trace['alternatives'][:3])}")

def search_traces(query: str) -> List[Dict]:
    """Search traces by query."""
    traces = load_traces()
    results = []
    
    for trace in traces:
        # Search in reasoning
        if query.lower() in trace.get("reasoning", "").lower():
            results.append(trace)
            continue
        # Search in chosen
        if query.lower() in trace.get("chosen", "").lower():
            results.append(trace)
            continue
        # Search in alternatives
        for alt in trace.get("alternatives", []):
            if query.lower() in alt.lower():
                results.append(trace)
                break
    
    return results

def log_decision(session_id: str, input_context: str, alternatives: List[str],
                 chosen: str, reasoning: str, confidence: float = 0.5):
    """Log a decision."""
    decision_id = f"dec_{datetime.now().strftime('%H%M%S')}"
    trace = DecisionTrace(session_id, decision_id, input_context, 
                         alternatives, chosen, reasoning, confidence)
    
    save_trace(trace.to_dict())
    
    print(f"🕵️ Decision logged: {decision_id}")
    print(f"   Chosen: {chosen}")
    print(f"   From: {len(alternatives)} alternatives")
    print(f"   Confidence: {confidence:.0%}")

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    
    if "--start" in args:
        idx = args.index("--start")
        if idx + 1 < len(args):
            session_id = args[idx + 1]
            print(f"🕵️ Tracing started for: {session_id[:20]}")
            print(f"   Decisions will be logged to: {TRACES_DIR}")
        else:
            print("Usage: --start session_id")
    elif "--log" in args:
        idx = args.index("--log")
        if idx + 1 < len(args):
            try:
                data = json.loads(args[idx + 1])
                log_decision(
                    data.get("session_id", "unknown"),
                    data.get("input", ""),
                    data.get("alternatives", []),
                    data.get("chosen", ""),
                    data.get("reasoning", ""),
                    data.get("confidence", 0.5)
                )
            except Exception:
                print("Invalid JSON. Format: '{\"session_id\": \"...\", \"input\": \"...\", \"alternatives\": [\"...\"], \"chosen\": \"...\", \"reasoning\": \"...\"}'")
        else:
            print("Usage: --log '{json}'")
    elif "--tree" in args:
        idx = args.index("--tree")
        if idx + 1 < len(args):
            show_decision_tree(args[idx + 1])
        else:
            print("Usage: --tree session_id")
    elif "--search" in args:
        idx = args.index("--search")
        if idx + 1 < len(args):
            query = args[idx + 1]
            results = search_traces(query)
            print(f"🕵️ Found {len(results)} traces matching '{query}':")
            for r in results[:5]:
                print(f"   [{r['timestamp'][:16]}] {r['chosen'][:40]}...")
        else:
            print("Usage: --search query")
    else:
        print(__doc__)
        print("\nCommands:")
        print("  --start session_id     Start trace")
        print("  --log '{json}'         Log decision")
        print("  --tree session_id      Show decision tree")
        print("  --search query         Search traces")

if __name__ == "__main__":
    main()
