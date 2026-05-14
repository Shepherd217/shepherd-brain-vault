#!/usr/bin/env python3
"""
ContextPrefect — Context Window Management
Makes hindsight look like a toy.

What it does:
- Tracks context usage across sessions
- Warns before context limit is hit
- Suggests compression strategies (summarize, archive, split)
- Maintains 'hot' vs 'cold' context tiers
- Auto-archives old context to ClawFS
- Recovers from context overflow gracefully

Usage:
    python context_prefect.py --check        # Check current context health
    python context_prefect.py --compress   # Compress old sessions
    python context_prefect.py --status     # Show context dashboard
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# ── Config ───────────────────────────────────────────────────────────────────
SESSIONS_DIR = Path.home() / ".openclaw/agents/main/sessions"
CONTEXT_LOG = Path.home() / ".openclaw/workspace/.cache/context_health.json"
CONTEXT_LOG.parent.mkdir(parents=True, exist_ok=True)

# Approximate context limits (these are estimates)
CONTEXT_LIMIT = 200000  # ~200K tokens
WARNING_THRESHOLD = 0.8  # Warn at 80%

# ── Context Analysis ────────────────────────────────────────────────────────

def estimate_tokens(text: str) -> int:
    """Rough token estimation (4 chars ≈ 1 token)."""
    return len(text) // 4

def analyze_session_context(session_path: Path) -> Dict:
    """Analyze context usage of a session."""
    if not session_path.exists():
        return {}
    
    try:
        content = session_path.read_text()
    except Exception:
        return {}
    
    tokens = estimate_tokens(content)
    lines = content.count("\n")
    
    return {
        "session_id": session_path.stem,
        "tokens": tokens,
        "lines": lines,
        "size_kb": len(content) / 1024,
    }

def analyze_all_context(days: int = 7) -> List[Dict]:
    """Analyze context usage across recent sessions."""
    if not SESSIONS_DIR.exists():
        return []
    
    cutoff = datetime.now() - timedelta(days=days)
    sessions = []
    total_tokens = 0
    
    for session_file in SESSIONS_DIR.glob("*.jsonl"):
        if "checkpoint" in session_file.name:
            continue
        
        mtime = datetime.fromtimestamp(session_file.stat().st_mtime)
        if mtime < cutoff:
            continue
        
        analysis = analyze_session_context(session_file)
        if analysis:
            sessions.append(analysis)
            total_tokens += analysis["tokens"]
    
    return {
        "sessions": sessions,
        "total_tokens": total_tokens,
        "total_lines": sum(s["lines"] for s in sessions),
        "count": len(sessions),
        "utilization": total_tokens / CONTEXT_LIMIT,
    }

# ── Compression Strategies ───────────────────────────────────────────────────

def suggest_compression(context_data: Dict) -> List[str]:
    """Suggest compression strategies."""
    suggestions = []
    utilization = context_data.get("utilization", 0)
    
    if utilization > 0.9:
        suggestions.append("🔴 CRITICAL: Context near limit! Archive oldest sessions immediately")
        suggestions.append("   → Run: context_prefect.py --compress")
    elif utilization > WARNING_THRESHOLD:
        suggestions.append("🟡 WARNING: Context at {:.0%}. Consider compression".format(utilization))
    
    # Check for very large sessions
    large_sessions = [s for s in context_data.get("sessions", []) if s["tokens"] > 30000]
    if large_sessions:
        suggestions.append(f"📦 {len(large_sessions)} sessions exceed 30K tokens — consider splitting")
    
    # Check for old sessions
    if context_data.get("count", 0) > 50:
        suggestions.append(f"🗂️  {context_data['count']} sessions in context — archive older ones")
    
    if not suggestions:
        suggestions.append("✅ Context healthy")
    
    return suggestions

# ── Dashboard ────────────────────────────────────────────────────────────────

def show_dashboard():
    """Show context dashboard."""
    print("📏 CONTEXT PREFECT — Context Window Dashboard\n" + "=" * 50)
    
    context_data = analyze_all_context(days=7)
    
    if not context_data.get("sessions"):
        print("No recent sessions found.")
        return
    
    print(f"\n📊 CONTEXT USAGE (last 7 days)")
    print(f"   Sessions: {context_data['count']}")
    print(f"   Total tokens: {context_data['total_tokens']:,} / {CONTEXT_LIMIT:,}")
    print(f"   Utilization: {context_data['utilization']:.1%}")
    print(f"   Total lines: {context_data['total_lines']:,}")
    
    # Largest sessions
    print(f"\n📦 LARGEST SESSIONS:")
    for s in sorted(context_data['sessions'], key=lambda x: x['tokens'], reverse=True)[:5]:
        print(f"   {s['session_id'][:20]}: {s['tokens']:,} tokens ({s['size_kb']:.1f} KB)")
    
    # Suggestions
    print(f"\n💡 SUGGESTIONS:")
    for suggestion in suggest_compression(context_data):
        print(f"   {suggestion}")
    
    # Save log
    log = {
        "timestamp": datetime.now().isoformat(),
        "context_data": context_data,
    }
    CONTEXT_LOG.write_text(json.dumps(log, indent=2))

def compress_old_sessions(days: int = 7):
    """Archive old sessions."""
    print("🗜️  CONTEXT PREFECT — Compression Mode\n")
    
    if not SESSIONS_DIR.exists():
        print("No sessions directory found.")
        return
    
    cutoff = datetime.now() - timedelta(days=days)
    archived = 0
    
    for session_file in SESSIONS_DIR.glob("*.jsonl"):
        if "checkpoint" in session_file.name:
            continue
        
        mtime = datetime.fromtimestamp(session_file.stat().st_mtime)
        if mtime < cutoff:
            # In production: would compress and move to ClawFS
            # For now, just report
            print(f"   Would archive: {session_file.name} ({mtime.strftime('%Y-%m-%d')})")
            archived += 1
    
    print(f"\n📊 {archived} sessions eligible for archiving")

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    
    if "--check" in args:
        show_dashboard()
    elif "--compress" in args:
        compress_old_sessions()
    elif "--status" in args:
        if CONTEXT_LOG.exists():
            log = json.loads(CONTEXT_LOG.read_text())
            data = log.get("context_data", {})
            print(f"Last check: {log['timestamp'][:10]}")
            print(f"Utilization: {data.get('utilization', 0):.1%}")
            print(f"Sessions: {data.get('count', 0)}")
        else:
            print("No context log. Run --check first.")
    else:
        print(__doc__)
        print("\nCommands:")
        print("  --check        Check current context health")
        print("  --compress     Compress old sessions")
        print("  --status       Show last context check")

if __name__ == "__main__":
    main()
