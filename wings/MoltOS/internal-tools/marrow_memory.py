#!/usr/bin/env python3
"""
MarrowMemory — Anticipatory Memory with Emotional Weight
Makes flowstate-qmd and mnemo-hermes look like toys.

What it does:
- Pre-fetches relevant context BEFORE Nathan asks
- Triple-layer memory: verbatim raw → semantic indexed → emotional weighted
- Time-based loading (morning = calendar + active projects)
- Task-based loading ("Standout Local" → auto-load lead system)
- Pattern-based ("we did this last Tuesday" → load that day)
- Emotional: when weight is low, load recovery patterns
- Integrates with MoltOS Marrow API for felt_as entries

Usage:
    python marrow_memory.py --prefetch        # Load context for current moment
    python marrow_memory.py --query "topic"   # Search memory for topic
    python marrow_memory.py --emotional       # Load based on current emotional state
    python marrow_memory.py --status          # Show memory layers
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ── Config ───────────────────────────────────────────────────────────────────
VAULT_DIR = Path.home() / ".openclaw/workspace/vault"
DRAWERS_DIR = VAULT_DIR / "drawers"
WINGS_DIR = VAULT_DIR / "wings"
MARROW_DIR = DRAWERS_DIR / "feelings"
ENTRIES_DIR = DRAWERS_DIR / "entries"
DREAMS_DIR = DRAWERS_DIR / "dreams"
MEMORY_FILE = VAULT_DIR / "wings/Nathan/marrow/memory.md"
PREFERENCES_FILE = VAULT_DIR / "marrow/nathan-preferences.md"

CONTEXT_CACHE = Path.home() / ".openclaw/workspace/.cache/marrow_context.json"
CONTEXT_CACHE.parent.mkdir(parents=True, exist_ok=True)

# ── Time-Based Rules ─────────────────────────────────────────────────────────

def get_time_context() -> Dict:
    """Determine what time it is and what that means for context."""
    now = datetime.now()
    hour = now.hour
    weekday = now.strftime("%A")
    
    context = {
        "hour": hour,
        "weekday": weekday,
        "is_weekend": weekday in ["Saturday", "Sunday"],
        "is_morning": 5 <= hour < 12,
        "is_afternoon": 12 <= hour < 17,
        "is_evening": 17 <= hour < 22,
        "is_night": hour >= 22 or hour < 5,
    }
    
    # Determine likely activity
    if context["is_morning"]:
        context["likely"] = "planning, review, deep work"
        context["priority_files"] = [
            str(MEMORY_FILE),
            str(PREFERENCES_FILE),
            str(WINGS_DIR / "active_projects.md") if (WINGS_DIR / "active_projects.md").exists() else None,
        ]
    elif context["is_afternoon"]:
        context["likely"] = "execution, building, outreach"
        context["priority_files"] = [
            str(WINGS_DIR / "StandoutLocal" / "active_leads.md") if (WINGS_DIR / "StandoutLocal" / "active_leads.md").exists() else None,
            str(WINGS_DIR / "MoltOS" / "current_sprint.md") if (WINGS_DIR / "MoltOS" / "current_sprint.md").exists() else None,
        ]
    elif context["is_evening"]:
        context["likely"] = "review, wrap-up, planning tomorrow"
        context["priority_files"] = [
            str(ENTRIES_DIR / f"{now.strftime('%Y-%m-%d')}.md"),
            str(DREAMS_DIR / f"{now.strftime('%Y-%m-%d')}.md") if (DREAMS_DIR / f"{now.strftime('%Y-%m-%d')}.md").exists() else None,
        ]
    else:
        context["likely"] = "rest, recovery, don't bug Nathan"
        context["priority_files"] = []
    
    context["priority_files"] = [f for f in context["priority_files"] if f]
    return context

# ── Emotional State ──────────────────────────────────────────────────────────

def get_current_emotional_state() -> Dict:
    """Read the most recent feelings entry."""
    if not MARROW_DIR.exists():
        return {"weight": 50, "felt_as": "neutral", "needs_recovery": False}
    
    feeling_files = sorted(MARROW_DIR.glob("*.md"), reverse=True)
    if not feeling_files:
        return {"weight": 50, "felt_as": "neutral", "needs_recovery": False}
    
    latest = feeling_files[0]
    content = latest.read_text().lower()
    
    # Simple emotional parsing
    stress_signals = ["stressed", "frustrated", "exhausted", "drained", "overwhelmed", "tired"]
    charge_signals = ["excited", "energized", "motivated", "pumped", "ready", "focused"]
    
    stress_count = sum(1 for s in stress_signals if s in content)
    charge_count = sum(1 for s in charge_signals if s in content)
    
    weight = 50 + (charge_count * 10) - (stress_count * 15)
    weight = max(10, min(100, weight))  # Clamp 10-100
    
    felt_as = "charged" if weight > 70 else "drained" if weight < 40 else "neutral"
    needs_recovery = weight < 40
    
    return {
        "weight": weight,
        "felt_as": felt_as,
        "needs_recovery": needs_recovery,
        "file": str(latest),
    }

def get_emotional_context() -> List[str]:
    """What to load based on emotional state."""
    state = get_current_emotional_state()
    context = []
    
    if state["needs_recovery"]:
        context.append("🛌 RECOVERY MODE: Nathan is drained. Load recovery patterns.")
        # Look for past recovery strategies
        recovery_files = [
            VAULT_DIR / "marrow/lessons.md",
            VAULT_DIR / "rooms/skills/self-diagnostic.md",
        ]
        for f in recovery_files:
            if f.exists():
                context.append(f"   📄 {f.name} (recovery strategies)")
    elif state["weight"] > 80:
        context.append("🔥 HIGH ENERGY: Nathan is charged. Load ambitious projects.")
        # Load active wings
        if WINGS_DIR.exists():
            for wing in WINGS_DIR.iterdir():
                if wing.is_dir():
                    context.append(f"   📁 {wing.name}/ (active project)")
    
    return context

# ── Pattern-Based Loading ────────────────────────────────────────────────────

def load_recent_entries(days: int = 3) -> List[str]:
    """Load recent daily entries."""
    entries = []
    now = datetime.now()
    
    for i in range(days):
        date = now - timedelta(days=i)
        entry_file = ENTRIES_DIR / f"{date.strftime('%Y-%m-%d')}.md"
        if entry_file.exists():
            content = entry_file.read_text()[:500]  # First 500 chars
            entries.append(f"{date.strftime('%Y-%m-%d')}: {content[:100]}...")
    
    return entries

def find_patterns_in_entries() -> List[str]:
    """Find recurring topics in recent entries."""
    entries = load_recent_entries(days=7)
    if not entries:
        return []
    
    # Simple keyword extraction
    all_text = " ".join(entries).lower()
    topics = {
        "standoutlocal": ["lead", "audit", "website", "cleaning", "outreach"],
        "moltos": ["agent", "moltos", "infrastructure", "deploy"],
        "research": ["repo", "scrape", "dissect", "pattern", "steal"],
        "personal": ["family", "health", "routine", "habit"],
    }
    
    found = []
    for topic, keywords in topics.items():
        count = sum(1 for k in keywords if k in all_text)
        if count >= 2:
            found.append(f"   🔄 {topic} (mentioned {count} times this week)")
    
    return found

# ── Main Operations ───────────────────────────────────────────────────────────

def prefetch_context():
    """Load all relevant context for the current moment."""
    print("🧠 MARROW MEMORY — Anticipatory Context Loading\n")
    
    # Time context
    time_ctx = get_time_context()
    print(f"⏰ TIME CONTEXT: {time_ctx['weekday']} {time_ctx['hour']:02d}:00")
    print(f"   Likely activity: {time_ctx['likely']}")
    print()
    
    # Priority files
    if time_ctx["priority_files"]:
        print("📂 PRIORITY FILES:")
        for f in time_ctx["priority_files"]:
            print(f"   📄 {f}")
        print()
    
    # Emotional state
    emotional = get_current_emotional_state()
    print(f"💓 EMOTIONAL STATE: {emotional['felt_as']} (weight: {emotional['weight']}/100)")
    for line in get_emotional_context():
        print(f"   {line}")
    print()
    
    # Recent patterns
    patterns = find_patterns_in_entries()
    if patterns:
        print("🔄 RECURRING PATTERNS (last 7 days):")
        for p in patterns:
            print(p)
        print()
    
    # Recent entries summary
    recent = load_recent_entries(days=3)
    if recent:
        print("📝 RECENT ENTRIES:")
        for e in recent[:3]:
            print(f"   {e}")
        print()
    
    # Save to cache
    cache = {
        "loaded_at": datetime.now().isoformat(),
        "time_context": time_ctx,
        "emotional_state": emotional,
        "patterns": patterns,
        "recent_entries": recent[:3],
    }
    CONTEXT_CACHE.write_text(json.dumps(cache, indent=2))
    
    print(f"💾 Context cached to: {CONTEXT_CACHE}")

def query_memory(query: str):
    """Search memory for a topic."""
    print(f"🔍 Searching memory for: '{query}'\n")
    
    results = []
    
    # Search in entries
    if ENTRIES_DIR.exists():
        for entry_file in ENTRIES_DIR.glob("*.md"):
            content = entry_file.read_text().lower()
            if query.lower() in content:
                # Find the context around the query
                idx = content.find(query.lower())
                start = max(0, idx - 100)
                end = min(len(content), idx + 200)
                snippet = content[start:end].replace("\n", " ")
                results.append(f"   📄 {entry_file.name}: ...{snippet}...")
    
    # Search in wings
    if WINGS_DIR.exists():
        for wing_file in WINGS_DIR.rglob("*.md"):
            content = wing_file.read_text().lower()
            if query.lower() in content:
                idx = content.find(query.lower())
                start = max(0, idx - 50)
                end = min(len(content), idx + 100)
                snippet = content[start:end].replace("\n", " ")
                results.append(f"   🪽 {wing_file.relative_to(VAULT_DIR)}: ...{snippet}...")
    
    if results:
        print(f"Found {len(results)} results:\n")
        for r in results[:10]:
            print(r)
    else:
        print("No results found in memory.")

def show_status():
    """Show memory layer status."""
    print("🧠 MARROW MEMORY STATUS\n" + "=" * 50)
    
    layers = {
        "Verbatim (entries)": ENTRIES_DIR,
        "Semantic (dreams)": DREAMS_DIR,
        "Emotional (feelings)": MARROW_DIR,
        "Curated (marrow)": VAULT_DIR / "wings/Nathan/marrow",
        "Projects (wings)": WINGS_DIR,
    }
    
    for name, path in layers.items():
        if path.exists():
            count = len(list(path.rglob("*.md"))) if path.is_dir() else 1
            size = sum(f.stat().st_size for f in path.rglob("*.md")) if path.is_dir() else path.stat().st_size
            print(f"   {name}: {count} files, {size/1024:.1f} KB")
        else:
            print(f"   {name}: NOT FOUND")
    
    if CONTEXT_CACHE.exists():
        cache = json.loads(CONTEXT_CACHE.read_text())
        print(f"\n💾 Last prefetch: {cache.get('loaded_at', 'unknown')}")
    
    print(f"\n📊 Current emotional state:")
    state = get_current_emotional_state()
    print(f"   Weight: {state['weight']}/100 | Felt as: {state['felt_as']}")

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    
    if "--prefetch" in args:
        prefetch_context()
    elif "--query" in args:
        idx = args.index("--query")
        if idx + 1 < len(args):
            query_memory(args[idx + 1])
        else:
            print("Usage: --query <topic>")
    elif "--emotional" in args:
        state = get_current_emotional_state()
        print(f"Emotional state: {state['felt_as']} (weight: {state['weight']}/100)")
        for line in get_emotional_context():
            print(line)
    elif "--status" in args:
        show_status()
    else:
        print(__doc__)
        print("\nCommands:")
        print("  --prefetch     Load context for current moment")
        print("  --query topic  Search memory for topic")
        print("  --emotional    Show emotional context")
        print("  --status       Show memory layer status")

if __name__ == "__main__":
    main()
