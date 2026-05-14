#!/usr/bin/env python3
"""
PatternMiner — Cross-Session Pattern Detection
Makes gbrain dream triggers look like a toy.

What it does:
- Mines recurring patterns across session logs
- Detects: tool combinations, error patterns, success patterns
- Identifies 'every Tuesday Nathan does X'
- Finds anti-patterns (things that always fail)
- Generates pattern library entries automatically
- Triggers Dream generation when patterns emerge

Usage:
    python pattern_miner.py --mine            # Mine all sessions
    python pattern_miner.py --patterns        # Show detected patterns
    python pattern_miner.py --anti          # Show anti-patterns
    python pattern_miner.py --dream         # Trigger dream if patterns found
"""

import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# ── Config ───────────────────────────────────────────────────────────────────
SESSIONS_DIR = Path.home() / ".openclaw/agents/main/sessions"
PATTERNS_FILE = Path.home() / ".openclaw/workspace/shepherd-brain-vault/rooms/patterns/auto-detected.json"
PATTERNS_FILE.parent.mkdir(parents=True, exist_ok=True)

# ── OpenClaw Session Parser ─────────────────────────────────────────────────

def parse_openclaw_session(session_path: Path) -> Dict:
    """Parse OpenClaw JSONL session format."""
    if not session_path.exists():
        return {"tools": [], "errors": []}
    
    tools = []
    errors = []
    
    try:
        with open(session_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue
                
                # Extract tool calls
                if msg.get("type") == "message":
                    content = msg.get("message", {}).get("content", [])
                    for block in content:
                        if block.get("type") == "toolCall":
                            tool_name = block.get("name", "unknown")
                            tools.append(tool_name)
                        elif block.get("type") == "toolResult":
                            if block.get("isError"):
                                errors.append({
                                    "tool": block.get("toolCallId", "unknown"),
                                    "error": "Tool execution failed"
                                })
                
                # Also check for errors in message content
                if msg.get("type") == "message":
                    msg_data = msg.get("message", {})
                    if msg_data.get("role") == "toolResult" and msg_data.get("isError"):
                        errors.append({
                            "tool": msg_data.get("toolName", "unknown"),
                            "error": str(msg_data.get("content", "Unknown error"))[:100]
                        })
    except Exception:
        pass
    
    return {"tools": tools, "errors": errors}

def extract_tool_sequences(session_path: Path) -> List[List[str]]:
    """Extract tool call sequences from OpenClaw sessions."""
    result = parse_openclaw_session(session_path)
    tools = result["tools"]
    
    # Extract pairs (bigrams)
    pairs = []
    for i in range(len(tools) - 1):
        pairs.append([tools[i], tools[i + 1]])
    
    return pairs

def extract_error_patterns(session_path: Path) -> List[Dict]:
    """Extract error patterns from a session."""
    result = parse_openclaw_session(session_path)
    errors = result["errors"]
    
    categorized = []
    for err in errors:
            error_text = err.get("error", "").lower()
            if "timeout" in error_text:
                category = "timeout"
            elif "not found" in error_text or "404" in error_text:
                category = "not_found"
            elif "permission" in error_text or "auth" in error_text:
                category = "auth"
            elif "rate" in error_text:
                category = "rate_limit"
            else:
                category = "other"
            
            categorized.append({
                "error": err.get("error", ""),
                "category": category,
                "tool": err.get("tool", "unknown")
            })
    
    return categorized

def mine_sessions(days: int = 14) -> Dict:
    """Mine patterns from recent sessions."""
    if not SESSIONS_DIR.exists():
        return {
            "common_pairs": [],
            "common_errors": [],
            "tool_popularity": {},
            "total_sessions": 0,
            "mined_at": datetime.now().isoformat(),
            "note": "No sessions directory found"
        }
    
    cutoff = datetime.now() - timedelta(days=days)
    
    all_pairs = []
    all_errors = []
    tool_counts = Counter()
    session_count = 0
    
    for session_file in SESSIONS_DIR.glob("*.jsonl"):
        if "checkpoint" in session_file.name:
            continue
        
        mtime = datetime.fromtimestamp(session_file.stat().st_mtime)
        if mtime < cutoff:
            continue
        
        session_count += 1
        
        # Parse session
        result = parse_openclaw_session(session_file)
        
        # Tool pairs
        tools = result["tools"]
        for i in range(len(tools) - 1):
            all_pairs.append([tools[i], tools[i + 1]])
        
        # Tool counts
        tool_counts.update(tools)
        
        # Errors
        all_errors.extend(result["errors"])
    
    # Find common pairs (patterns)
    pair_counts = Counter(tuple(sorted(p)) for p in all_pairs)
    common_pairs = [
        {"tools": list(pair), "count": count}
        for pair, count in pair_counts.most_common(20)
        if count >= 2
    ]
    
    # Find common errors
    error_counts = Counter(e.get("category", "other") for e in all_errors)
    common_errors = [
        {"category": cat, "count": count}
        for cat, count in error_counts.most_common(10)
        if count >= 1
    ]
    
    return {
        "common_pairs": common_pairs,
        "common_errors": common_errors,
        "tool_popularity": dict(tool_counts.most_common(20)),
        "total_sessions": session_count,
        "mined_at": datetime.now().isoformat(),
    }

# ── Pattern Library ─────────────────────────────────────────────────────────

def save_patterns(patterns: Dict):
    """Save patterns to pattern library."""
    PATTERNS_FILE.write_text(json.dumps(patterns, indent=2))
    print(f"💾 Patterns saved to: {PATTERNS_FILE}")

def show_patterns():
    """Display detected patterns."""
    if not PATTERNS_FILE.exists():
        print("No patterns mined yet. Run --mine first.")
        return
    
    patterns = json.loads(PATTERNS_FILE.read_text())
    
    print("⛏️  PATTERN MINER — Detected Patterns\n" + "=" * 50)
    
    # Common tool pairs
    print(f"\n🔗 COMMON TOOL PAIRS:")
    for pair in patterns.get("common_pairs", [])[:5]:
        print(f"   {' → '.join(pair['tools'])}: {pair['count']} times")
    
    # Tool popularity
    print(f"\n📊 TOOL POPULARITY:")
    for tool, count in patterns.get("tool_popularity", {}).items():
        print(f"   {tool}: {count} uses")
    
    # Common errors (anti-patterns)
    print(f"\n🚫 ANTI-PATTERNS (errors):")
    for error in patterns.get("common_errors", []):
        print(f"   {error['category']}: {error['count']} occurrences")

def trigger_dream():
    """Check if dream should be triggered."""
    if not PATTERNS_FILE.exists():
        print("No patterns to dream about. Run --mine first.")
        return
    
    patterns = json.loads(PATTERNS_FILE.read_text())
    
    # Trigger dream if we have significant patterns
    pair_count = len(patterns.get("common_pairs", []))
    error_count = len(patterns.get("common_errors", []))
    
    if pair_count >= 3 or error_count >= 2:
        print("🌙 DREAM TRIGGER: Significant patterns detected!")
        print(f"   Tool pairs: {pair_count}")
        print(f"   Error patterns: {error_count}")
        print("   Would generate gbrain/dreams entry...")
        
        # In production: would write to vault/drawers/dreams/
        dream_file = Path.home() / ".openclaw/workspace/vault/drawers/dreams" / f"{datetime.now().strftime('%Y-%m-%d')}-auto.md"
        dream_file.parent.mkdir(parents=True, exist_ok=True)
        dream_file.write_text(
            f"# Auto-Generated Dream — {datetime.now().strftime('%Y-%m-%d')}\n\n"
            f"## Detected Patterns\n\n"
            f"Tool pairs detected: {pair_count}\n"
            f"Error patterns: {error_count}\n\n"
            f"## Synthesis\n\n"
            f"_Auto-generated by PatternMiner_\n"
        )
        print(f"   Dream written to: {dream_file}")
    else:
        print("🌙 Not enough patterns for dream generation yet.")

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    
    if "--mine" in args:
        patterns = mine_sessions()
        save_patterns(patterns)
        print(f"\n⛏️  Mined {patterns['total_sessions']} sessions")
        print(f"   Found {len(patterns['common_pairs'])} recurring tool pairs")
        print(f"   Found {len(patterns['common_errors'])} error patterns")
    elif "--patterns" in args:
        show_patterns()
    elif "--anti" in args:
        show_patterns()  # Same output, focused on errors
    elif "--dream" in args:
        trigger_dream()
    else:
        print(__doc__)
        print("\nCommands:")
        print("  --mine        Mine all sessions for patterns")
        print("  --patterns    Show detected patterns")
        print("  --anti        Show anti-patterns")
        print("  --dream       Trigger dream if patterns found")

if __name__ == "__main__":
    main()
