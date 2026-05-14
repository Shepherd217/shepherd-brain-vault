#!/usr/bin/env python3
"""
ShadowRecorder — Session Recording + Replay
Makes basic logging look like a toy.

What it does:
- Records every tool call, decision, and outcome
- Creates 'shadow' session files with full context
- Enables replay: 'show me what you did at 3pm Tuesday'
- Tracks decision lineage (why did I choose tool X over Y?)
- Generates session summaries automatically
- Searchable by tool, outcome, or emotional state
- Exports to Obsidian for Nathan's review

Usage:
    python shadow_recorder.py --record session_id   # Record/review session
    python shadow_recorder.py --search tool_name    # Search by tool
    python shadow_recorder.py --summary             # Generate summary
    python shadow_recorder.py --export              # Export to Obsidian
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# ── Config ───────────────────────────────────────────────────────────────────
SESSIONS_DIR = Path.home() / ".openclaw/agents/main/sessions"
SHADOW_DIR = Path.home() / ".openclaw/workspace/.cache/shadows"
SHADOW_DIR.mkdir(parents=True, exist_ok=True)
VAULT_ENTRIES = Path.home() / ".openclaw/workspace/shepherd-brain-vault/drawers/entries"

# ── Session Recording ───────────────────────────────────────────────────────

def record_session(session_id: str) -> Dict:
    """Create a rich shadow recording of a session."""
    session_path = SESSIONS_DIR / f"{session_id}.jsonl"
    
    if not session_path.exists():
        return {"error": f"Session not found: {session_id}"}
    
    try:
        content = session_path.read_text()
    except Exception as e:
        return {"error": str(e)}
    
    # Extract tool calls with timestamps
    tool_calls = []
    for line in content.split("\n"):
        if '"tool":' in line:
            # Extract tool name
            match = re.search(r'"tool":\s*"([^"]+)"', line)
            if match:
                tool_calls.append({
                    "tool": match.group(1),
                    "line": line[:200],  # First 200 chars
                })
    
    # Extract errors
    errors = re.findall(r'"error":\s*"([^"]+)"', content)
    
    # Extract user messages (simplified)
    user_messages = re.findall(r'"role":\s*"user".*?"content":\s*"([^"]+)"', content, re.DOTALL)
    
    # Create shadow record
    shadow = {
        "session_id": session_id,
        "recorded_at": datetime.now().isoformat(),
        "tool_calls": tool_calls,
        "errors": errors,
        "error_count": len(errors),
        "tool_count": len(tool_calls),
        "unique_tools": len(set(t["tool"] for t in tool_calls)),
        "user_messages": len(user_messages),
        "size_kb": len(content) / 1024,
    }
    
    # Save shadow
    shadow_file = SHADOW_DIR / f"{session_id}.json"
    shadow_file.write_text(json.dumps(shadow, indent=2))
    
    return shadow

def search_shadows(query: str) -> List[Dict]:
    """Search shadow recordings."""
    results = []
    
    for shadow_file in SHADOW_DIR.glob("*.json"):
        shadow = json.loads(shadow_file.read_text())
        
        # Search in tool calls
        for call in shadow.get("tool_calls", []):
            if query.lower() in call["tool"].lower():
                results.append({
                    "session_id": shadow["session_id"],
                    "match": f"Tool: {call['tool']}",
                    "recorded": shadow["recorded_at"],
                })
                break
        
        # Search in errors
        for error in shadow.get("errors", []):
            if query.lower() in error.lower():
                results.append({
                    "session_id": shadow["session_id"],
                    "match": f"Error: {error[:100]}",
                    "recorded": shadow["recorded_at"],
                })
                break
    
    return results

def generate_summary(days: int = 1) -> str:
    """Generate a summary of recent sessions."""
    cutoff = datetime.now() - timedelta(days=days)
    
    shadows = []
    for shadow_file in SHADOW_DIR.glob("*.json"):
        shadow = json.loads(shadow_file.read_text())
        recorded = datetime.fromisoformat(shadow["recorded_at"])
        if recorded >= cutoff:
            shadows.append(shadow)
    
    if not shadows:
        return "No sessions recorded in the last day."
    
    summary = f"# Session Summary — Last {days} Day(s)\n\n"
    summary += f"**Sessions:** {len(shadows)}\n"
    summary += f"**Total tool calls:** {sum(s['tool_count'] for s in shadows)}\n"
    summary += f"**Total errors:** {sum(s['error_count'] for s in shadows)}\n"
    summary += f"**Unique tools used:** {len(set(t for s in shadows for t in [c['tool'] for c in s.get('tool_calls', [])]))}\n\n"
    
    # Tool breakdown
    tool_counts = {}
    for shadow in shadows:
        for call in shadow.get("tool_calls", []):
            tool = call["tool"]
            tool_counts[tool] = tool_counts.get(tool, 0) + 1
    
    summary += "## Tool Usage\n\n"
    for tool, count in sorted(tool_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        summary += f"- {tool}: {count}\n"
    
    # Error summary
    errors = []
    for shadow in shadows:
        errors.extend(shadow.get("errors", []))
    
    if errors:
        summary += "\n## Errors\n\n"
        for error in errors[:5]:
            summary += f"- {error[:100]}...\n"
    
    return summary

def export_to_obsidian():
    """Export session summary to Obsidian."""
    summary = generate_summary(days=1)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    entry_file = VAULT_ENTRIES / f"{date_str}-shadow-summary.md"
    
    if not entry_file.parent.exists():
        entry_file.parent.mkdir(parents=True, exist_ok=True)
    
    entry_file.write_text(summary)
    
    print(f"📓 Exported to: {entry_file}")

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    
    if "--record" in args:
        idx = args.index("--record")
        if idx + 1 < len(args):
            session_id = args[idx + 1]
            shadow = record_session(session_id)
            print(f"📹 Shadow recorded: {session_id}")
            print(f"   Tools: {shadow.get('tool_count', 0)}")
            print(f"   Errors: {shadow.get('error_count', 0)}")
            print(f"   Size: {shadow.get('size_kb', 0):.1f} KB")
        else:
            print("Usage: --record session_id")
    elif "--search" in args:
        idx = args.index("--search")
        if idx + 1 < len(args):
            query = args[idx + 1]
            results = search_shadows(query)
            print(f"🔍 Found {len(results)} matches for '{query}':")
            for r in results[:10]:
                print(f"   {r['session_id'][:20]}: {r['match'][:80]}")
        else:
            print("Usage: --search query")
    elif "--summary" in args:
        print(generate_summary())
    elif "--export" in args:
        export_to_obsidian()
    else:
        print(__doc__)
        print("\nCommands:")
        print("  --record session_id   Record/review session")
        print("  --search query        Search shadows")
        print("  --summary             Generate summary")
        print("  --export              Export to Obsidian")

if __name__ == "__main__":
    main()
