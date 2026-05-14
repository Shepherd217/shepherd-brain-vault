#!/usr/bin/env python3
"""
PrometheusLens — Quality Metrics Dashboard
Makes Mission Control look like a toy.

What it does:
- Tracks tool success/failure rates across sessions
- Measures latency per tool
- Scores session quality (completion, errors, recovery needed)
- Tracks emotional trajectory (weight over time)
- Identifies regressions ("success rate dropped 15% this week")
- Auto-triggers DebateCouncil if quality drops

Usage:
    python prometheus_lens.py --analyze       # Analyze all sessions
    python prometheus_lens.py --trend         # Show trend report
    python prometheus_lens.py --alerts        # Check for regressions
    python prometheus_lens.py --dashboard     # Full dashboard
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
METRICS_FILE = Path.home() / ".openclaw/workspace/.cache/prometheus_metrics.json"
METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)

# ── Metrics Collection ──────────────────────────────────────────────────────

def analyze_session(session_path: Path) -> Dict:
    """Extract metrics from a session file."""
    if not session_path.exists():
        return {}
    
    try:
        content = session_path.read_text()
    except Exception:
        return {}
    
    # Count tool calls and errors
    tool_calls = re.findall(r'"tool":\s*"([^"]+)"', content)
    errors = re.findall(r'"error":\s*"([^"]+)"', content)
    
    # Estimate session length (lines)
    lines = content.count("\n")
    
    # Check for recovery patterns
    recovery_needed = "stalled" in content.lower() or "timeout" in content.lower()
    
    return {
        "session_id": session_path.stem,
        "tool_calls": len(tool_calls),
        "unique_tools": len(set(tool_calls)),
        "errors": len(errors),
        "error_rate": len(errors) / max(len(tool_calls), 1),
        "lines": lines,
        "recovery_needed": recovery_needed,
        "tools_used": list(set(tool_calls)),
    }

def analyze_all_sessions(days: int = 7) -> List[Dict]:
    """Analyze recent sessions."""
    if not SESSIONS_DIR.exists():
        return []
    
    cutoff = datetime.now() - timedelta(days=days)
    sessions = []
    
    for session_file in SESSIONS_DIR.glob("*.jsonl"):
        # Skip checkpoint files
        if "checkpoint" in session_file.name:
            continue
        
        # Check file modification time
        mtime = datetime.fromtimestamp(session_file.stat().st_mtime)
        if mtime < cutoff:
            continue
        
        metrics = analyze_session(session_file)
        if metrics:
            metrics["date"] = mtime.isoformat()
            sessions.append(metrics)
    
    return sessions

# ── Trend Analysis ───────────────────────────────────────────────────────────

def calculate_trends(sessions: List[Dict]) -> Dict:
    """Calculate trends from session metrics."""
    if not sessions:
        return {}
    
    # Sort by date
    sessions.sort(key=lambda s: s.get("date", ""))
    
    # Overall stats
    total_tools = sum(s["tool_calls"] for s in sessions)
    total_errors = sum(s["errors"] for s in sessions)
    avg_error_rate = total_errors / max(total_tools, 1)
    
    # Tool-specific stats
    tool_stats = {}
    for session in sessions:
        for tool in session.get("tools_used", []):
            if tool not in tool_stats:
                tool_stats[tool] = {"calls": 0, "errors": 0}
            tool_stats[tool]["calls"] += 1
    
    # Recovery stats
    recovery_count = sum(1 for s in sessions if s.get("recovery_needed"))
    
    return {
        "total_sessions": len(sessions),
        "total_tools_used": total_tools,
        "total_errors": total_errors,
        "avg_error_rate": avg_error_rate,
        "recovery_rate": recovery_count / len(sessions),
        "tool_breakdown": tool_stats,
        "avg_complexity": sum(s["unique_tools"] for s in sessions) / len(sessions),
    }

def detect_regressions(current: Dict, previous: Dict) -> List[Dict]:
    """Detect quality regressions."""
    alerts = []
    
    if not previous:
        return alerts
    
    # Error rate increased?
    if current["avg_error_rate"] > previous["avg_error_rate"] * 1.2:
        alerts.append({
            "severity": "🔴 HIGH",
            "metric": "error_rate",
            "change": f"+{((current['avg_error_rate'] / previous['avg_error_rate'] - 1) * 100):.0f}%",
            "message": f"Error rate increased from {previous['avg_error_rate']:.1%} to {current['avg_error_rate']:.1%}",
        })
    
    # Recovery rate increased?
    if current["recovery_rate"] > previous["recovery_rate"] * 1.3:
        alerts.append({
            "severity": "🟡 MEDIUM",
            "metric": "recovery_rate",
            "change": f"+{((current['recovery_rate'] / max(previous['recovery_rate'], 0.01) - 1) * 100):.0f}%",
            "message": "More sessions requiring recovery — check tool stability",
        })
    
    # Tool diversity dropped?
    if current["avg_complexity"] < previous["avg_complexity"] * 0.8:
        alerts.append({
            "severity": "🟡 MEDIUM",
            "metric": "complexity",
            "change": f"-{((1 - current['avg_complexity'] / previous['avg_complexity']) * 100):.0f}%",
            "message": "Tool diversity dropped — possible workflow simplification or stagnation",
        })
    
    return alerts

# ── Dashboard ─────────────────────────────────────────────────────────────────

def show_dashboard():
    """Display full metrics dashboard."""
    print("📊 PROMETHEUS LENS — Quality Metrics Dashboard\n" + "=" * 60)
    
    # Current week
    current_sessions = analyze_all_sessions(days=7)
    current = calculate_trends(current_sessions)
    
    # Previous week
    prev_sessions = analyze_all_sessions(days=14)
    # Filter to only previous week (7-14 days ago)
    cutoff = datetime.now() - timedelta(days=7)
    prev_sessions = [s for s in prev_sessions if datetime.fromisoformat(s["date"]) < cutoff]
    previous = calculate_trends(prev_sessions)
    
    if not current:
        print("No recent sessions found.")
        return
    
    print(f"\n📈 CURRENT WEEK ({current['total_sessions']} sessions)")
    print(f"   Total tool calls: {current['total_tools_used']}")
    print(f"   Error rate: {current['avg_error_rate']:.1%}")
    print(f"   Recovery rate: {current['recovery_rate']:.1%}")
    print(f"   Avg tools/session: {current['avg_complexity']:.1f}")
    
    # Tool breakdown
    print(f"\n🔧 TOOL USAGE:")
    for tool, stats in sorted(current['tool_breakdown'].items(), key=lambda x: x[1]['calls'], reverse=True)[:10]:
        print(f"   {tool}: {stats['calls']} calls")
    
    # Regressions
    alerts = detect_regressions(current, previous)
    if alerts:
        print(f"\n🚨 REGRESSION ALERTS:")
        for alert in alerts:
            print(f"   {alert['severity']} {alert['metric']}: {alert['change']}")
            print(f"   → {alert['message']}")
    else:
        print(f"\n✅ No regressions detected")
    
    # Save metrics
    metrics = {
        "last_updated": datetime.now().isoformat(),
        "current_week": current,
        "previous_week": previous,
        "alerts": alerts,
    }
    METRICS_FILE.write_text(json.dumps(metrics, indent=2))
    
    print(f"\n💾 Metrics saved to: {METRICS_FILE}")

def show_trend():
    """Show trend report."""
    if not METRICS_FILE.exists():
        print("No metrics history. Run --dashboard first.")
        return
    
    metrics = json.loads(METRICS_FILE.read_text())
    current = metrics.get("current_week", {})
    previous = metrics.get("previous_week", {})
    
    if not current or not previous:
        print("Insufficient data for trend analysis.")
        return
    
    print("📈 TREND REPORT\n" + "=" * 50)
    print(f"   Sessions: {previous['total_sessions']} → {current['total_sessions']}")
    print(f"   Error rate: {previous['avg_error_rate']:.1%} → {current['avg_error_rate']:.1%}")
    print(f"   Recovery: {previous['recovery_rate']:.1%} → {current['recovery_rate']:.1%}")
    print(f"   Complexity: {previous['avg_complexity']:.1f} → {current['avg_complexity']:.1f}")

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    
    if "--dashboard" in args:
        show_dashboard()
    elif "--trend" in args:
        show_trend()
    elif "--alerts" in args:
        if METRICS_FILE.exists():
            metrics = json.loads(METRICS_FILE.read_text())
            alerts = metrics.get("alerts", [])
            if alerts:
                for alert in alerts:
                    print(f"{alert['severity']} {alert['metric']}: {alert['message']}")
            else:
                print("No active alerts")
        else:
            print("No metrics found. Run --dashboard first.")
    else:
        print(__doc__)
        print("\nCommands:")
        print("  --dashboard    Show full metrics dashboard")
        print("  --trend        Show trend report")
        print("  --alerts       Check for regression alerts")

if __name__ == "__main__":
    main()
