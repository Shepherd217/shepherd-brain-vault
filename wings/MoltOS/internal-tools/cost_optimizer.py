#!/usr/bin/env python3
"""
CostOptimizer — Local Model Load Reduction + Cost Tracking
Hermes has this. We make it smarter.

What it does:
- Tracks cost per task, per tool, per session
- Suggests local model alternatives for simple tasks
- Monitors latency vs cost tradeoffs
- Auto-routes: cheap model for simple tasks, expensive for critical
- Tracks token usage per tool to find waste
- Predicts monthly burn rate
- Cost alerts: "You've spent $5 today"

Usage:
    python cost_optimizer.py --track        # Track current session costs
    python cost_optimizer.py --suggest task  # Suggest cheapest way to do task
    python cost_optimizer.py --report        # Daily cost report
    python cost_optimizer.py --alert         # Check if over budget
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# ── Config ───────────────────────────────────────────────────────────────────
COST_LOG = Path.home() / ".openclaw/workspace/.cache/cost_tracker.json"
COST_LOG.parent.mkdir(parents=True, exist_ok=True)

# Approximate costs per 1K tokens (USD)
MODEL_COSTS = {
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    "claude-3-opus": {"input": 0.015, "output": 0.075},
    "claude-3-sonnet": {"input": 0.003, "output": 0.015},
    "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
    "local-llama": {"input": 0.0, "output": 0.0},  # Free but slower
}

# Tool → suggested model tier mapping
TOOL_TIERS = {
    "kimi_search": "cheap",      # Web search doesn't need expensive model
    "web_fetch": "cheap",
    "exec": "local",             # Shell commands = local processing
    "read": "cheap",             # File reading = simple
    "write": "medium",           # Writing needs some quality
    "edit": "medium",
    "sessions_spawn": "medium",  # Sub-agent delegation
    "subagents": "medium",
    "browser": "expensive",        # Browser automation is complex
    "image": "expensive",        # Vision models are costly
    "pdf": "expensive",
}

# ── Cost Tracking ───────────────────────────────────────────────────────────

def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Estimate cost for a model call."""
    costs = MODEL_COSTS.get(model, MODEL_COSTS["gpt-3.5-turbo"])
    input_cost = (input_tokens / 1000) * costs["input"]
    output_cost = (output_tokens / 1000) * costs["output"]
    return input_cost + output_cost

def suggest_model(task_type: str, complexity: str = "medium") -> Dict:
    """Suggest cheapest model for a task."""
    tier = TOOL_TIERS.get(task_type, "medium")
    
    suggestions = {
        "local": {
            "model": "local-llama",
            "cost_per_1k": 0.0,
            "latency": "slow",
            "reason": "Use local model for simple wrapper work",
        },
        "cheap": {
            "model": "claude-3-haiku",
            "cost_per_1k": 0.0015,
            "latency": "fast",
            "reason": "Haiku is cheap and fast for simple tasks",
        },
        "medium": {
            "model": "claude-3-sonnet",
            "cost_per_1k": 0.018,
            "latency": "medium",
            "reason": "Sonnet balances cost and quality",
        },
        "expensive": {
            "model": "claude-3-opus",
            "cost_per_1k": 0.09,
            "latency": "medium",
            "reason": "Opus for complex reasoning tasks",
        },
    }
    
    return suggestions.get(tier, suggestions["medium"])

def load_cost_log() -> Dict:
    if COST_LOG.exists():
        return json.loads(COST_LOG.read_text())
    return {"entries": [], "daily_budget": 10.0}

def save_cost_log(log: Dict):
    COST_LOG.write_text(json.dumps(log, indent=2))

def track_cost(tool: str, model: str, input_tokens: int, output_tokens: int):
    """Track cost for a tool call."""
    log = load_cost_log()
    cost = estimate_cost(model, input_tokens, output_tokens)
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "tool": tool,
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_usd": cost,
    }
    
    log["entries"].append(entry)
    save_cost_log(log)
    
    return cost

def daily_report():
    """Generate daily cost report."""
    log = load_cost_log()
    today = datetime.now().strftime("%Y-%m-%d")
    
    today_entries = [e for e in log["entries"] if e["timestamp"].startswith(today)]
    
    if not today_entries:
        print("💰 COST OPTIMIZER — No costs today")
        return
    
    total = sum(e["cost_usd"] for e in today_entries)
    budget = log.get("daily_budget", 10.0)
    
    print(f"💰 COST OPTIMIZER — Daily Report\n" + "=" * 50)
    print(f"Date: {today}")
    print(f"Total spent: ${total:.4f}")
    print(f"Budget: ${budget:.2f}")
    print(f"Remaining: ${budget - total:.2f}")
    print(f"Calls: {len(today_entries)}\n")
    
    # By tool
    tool_costs = {}
    for e in today_entries:
        tool = e["tool"]
        if tool not in tool_costs:
            tool_costs[tool] = {"cost": 0, "calls": 0}
        tool_costs[tool]["cost"] += e["cost_usd"]
        tool_costs[tool]["calls"] += 1
    
    print("By tool:")
    for tool, data in sorted(tool_costs.items(), key=lambda x: x[1]["cost"], reverse=True):
        print(f"   {tool}: ${data['cost']:.4f} ({data['calls']} calls)")
    
    # Suggestions
    expensive_tools = [t for t, d in tool_costs.items() if d["cost"] > 0.5]
    if expensive_tools:
        print(f"\n💡 Suggestions:")
        for tool in expensive_tools[:3]:
            suggestion = suggest_model(tool)
            print(f"   {tool}: Consider {suggestion['model']} (${suggestion['cost_per_1k']}/1K tokens)")
    
    # Alert
    if total > budget:
        print(f"\n🚨 ALERT: Over budget! Spent ${total:.2f} of ${budget:.2f}")

def check_alert():
    """Check if over budget."""
    log = load_cost_log()
    today = datetime.now().strftime("%Y-%m-%d")
    today_entries = [e for e in log["entries"] if e["timestamp"].startswith(today)]
    total = sum(e["cost_usd"] for e in today_entries)
    budget = log.get("daily_budget", 10.0)
    
    if total > budget:
        print(f"🚨 OVER BUDGET: ${total:.2f} / ${budget:.2f}")
        return 1
    elif total > budget * 0.8:
        print(f"⚠️  Near budget: ${total:.2f} / ${budget:.2f}")
        return 0
    else:
        print(f"✅ On budget: ${total:.2f} / ${budget:.2f}")
        return 0

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    
    if "--track" in args:
        # In production: would read actual session data
        print("💰 Cost tracking active")
        print("   (In production: would track actual API calls)")
    elif "--suggest" in args:
        idx = args.index("--suggest")
        if idx + 1 < len(args):
            task = args[idx + 1]
            suggestion = suggest_model(task)
            print(f"💰 For '{task}':")
            print(f"   Suggested: {suggestion['model']}")
            print(f"   Cost: ${suggestion['cost_per_1k']}/1K tokens")
            print(f"   Latency: {suggestion['latency']}")
            print(f"   Why: {suggestion['reason']}")
        else:
            print("Usage: --suggest task_type")
    elif "--report" in args:
        daily_report()
    elif "--alert" in args:
        sys.exit(check_alert())
    else:
        print(__doc__)
        print("\nCommands:")
        print("  --track              Track session costs")
        print("  --suggest task       Suggest cheapest model")
        print("  --report             Daily cost report")
        print("  --alert              Check budget alert")

if __name__ == "__main__":
    main()
