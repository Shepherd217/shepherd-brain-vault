#!/usr/bin/env python3
"""
AutonomousActivator — How to Enable Continuous Autonomous Operation

This script activates the full autonomous loop when you want me to run
without your direct input. It coordinates:
- Periodic research cycles (find repos, dissect, synthesize)
- Self-improvement (improve my own tools based on findings)
- Dream generation (pattern synthesis)
- Memory consolidation (commit vault changes)
- Alignment checks (self-diagnostic)

SAFETY FEATURES:
- Cost tracking (max $5/day)
- Alignment gating (stop if score < 70)
- Nathan approval for major changes
- All findings written to vault for your review

Usage:
    python autonomous_activator.py --enable         # Enable autonomous mode
    python autonomous_activator.py --cycle          # Run one cycle now
    python autonomous_activator.py --status         # Show autonomous status
    python autonomous_activator.py --disable        # Disable autonomous mode
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

CONFIG_FILE = Path.home() / ".openclaw/workspace/.cache/autonomous_config.json"

def load_config():
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {
        "enabled": False,
        "cycles_per_day": 4,
        "max_cost_per_day": 5.0,
        "min_alignment_score": 70,
        "last_cycle": None,
        "total_cycles": 0,
    }

def save_config(config):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2))

def enable_autonomous():
    config = load_config()
    config["enabled"] = True
    config["enabled_at"] = datetime.now().isoformat()
    save_config(config)
    
    print("🤖 AUTONOMOUS MODE ENABLED\n")
    print("I will now run autonomous cycles:")
    print(f"   Frequency: {config['cycles_per_day']} times per day")
    print(f"   Max cost: ${config['max_cost_per_day']}/day")
    print(f"   Min alignment: {config['min_alignment_score']}/100")
    print(f"\nWhat I'll do autonomously:")
    print("   1. Research trending repos/tools")
    print("   2. Dissect them for Picasso steal opportunities")
    print("   3. Synthesize patterns into dreams")
    print("   4. Auto-generate skills from findings")
    print("   5. Improve my own tools")
    print("   6. Run self-diagnostics")
    print("   7. Commit everything to vault")
    print(f"\n📁 All findings saved to: vault/")
    print(f"📊 Dashboard: ~/.openclaw/workspace/.cache/autonomous_cycles.json")
    
    # Create trigger file for heartbeat
    trigger = Path.home() / ".openclaw/workspace/.autonomous_active"
    trigger.write_text("enabled")

def disable_autonomous():
    config = load_config()
    config["enabled"] = False
    config["disabled_at"] = datetime.now().isoformat()
    save_config(config)
    
    trigger = Path.home() / ".openclaw/workspace/.autonomous_active"
    if trigger.exists():
        trigger.unlink()
    
    print("🛑 AUTONOMOUS MODE DISABLED")
    print("   I will only respond to your direct messages.")

def show_status():
    config = load_config()
    
    print("🤖 AUTONOMOUS STATUS\n" + "=" * 50)
    print(f"Enabled: {'✅ YES' if config['enabled'] else '❌ NO'}")
    print(f"Cycles per day: {config['cycles_per_day']}")
    print(f"Max cost/day: ${config['max_cost_per_day']}")
    print(f"Min alignment: {config['min_alignment_score']}/100")
    print(f"Total cycles run: {config.get('total_cycles', 0)}")
    print(f"Last cycle: {config.get('last_cycle', 'Never')}")
    
    if config["enabled"]:
        print(f"\n📋 Next cycle will:")
        print("   - Run autonomous_orchestrator.py --cycle")
        print("   - Save findings to vault/")
        print("   - Update .cache/autonomous_cycles.json")
    else:
        print(f"\n💡 To enable: python autonomous_activator.py --enable")

def main():
    args = sys.argv[1:]
    
    if "--enable" in args:
        enable_autonomous()
    elif "--disable" in args:
        disable_autonomous()
    elif "--status" in args:
        show_status()
    else:
        print(__doc__)
        print("\nCommands:")
        print("  --enable     Enable autonomous mode")
        print("  --disable    Disable autonomous mode")
        print("  --status     Show autonomous status")

if __name__ == "__main__":
    main()
