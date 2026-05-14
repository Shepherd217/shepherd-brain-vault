#!/usr/bin/env python3
"""
dispatch.py — Batty-style coordination daemon for Shepherd's Brain

Watches .coordination/tasks/inbox/ for new task files.
Dispatches to idle agents based on priority + agent hints.
Updates registry and task board.

Usage:
  python dispatch.py start     # Run daemon (polls every 10s)
  python dispatch.py status   # Show current state
  python dispatch.py test      # Run one poll cycle (no daemon)
  python dispatch.py init      # Initialize first test task
"""

import json
import os
import sys
import time
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

# Config — auto-detect vault root
SCRIPT_DIR = Path(__file__).parent.resolve()
VAULT = SCRIPT_DIR.parent.resolve()
COORD = VAULT / ".coordination"
TASKS = COORD / "tasks"
INBOX = TASKS / "inbox"
REGISTRY = COORD / "registry.json"
HEARTBEAT = COORD / "heartbeat.json"
BOARD = TASKS / "task-board.md"
SIGNALS = COORD / "signals"
POLL_INTERVAL = 10

PRIORITY_ORDER = ["critical", "high", "medium", "low"]


def ensure_state_files():
    """Create registry and heartbeat if they don't exist."""
    if not REGISTRY.exists():
        default_registry = {
            "version": "1.0",
            "schema": "coordination-v1",
            "created": datetime.now().isoformat(),
            "agents": {
                "promachos": {
                    "id": "promachos",
                    "type": "execution",
                    "zone": "agents/promachos/",
                    "status": "idle",
                    "current_task": None
                },
                "ava": {
                    "id": "ava",
                    "type": "ceo",
                    "zone": "agents/ava/",
                    "status": "idle",
                    "current_task": None
                }
            }
        }
        save_json(REGISTRY, default_registry)
        print(f"  ✅ Created {REGISTRY.name}")
    
    if not HEARTBEAT.exists():
        default_heartbeat = {
            "promachos": {"last_seen": None, "status": "idle", "session_count": 0},
            "ava": {"last_seen": None, "status": "idle", "session_count": 0},
            "_meta": {"schema": "coordination-v1", "auto_updated": True}
        }
        save_json(HEARTBEAT, default_heartbeat)
        print(f"  ✅ Created {HEARTBEAT.name}")


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_json(path: Path, data: dict):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def touch(path: Path):
    path.touch()


def get_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter from markdown."""
    if not text.strip().startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fm_text = parts[1]
    result = {}
    for line in fm_text.strip().split("\n"):
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        result[key.strip()] = val.strip()
    return result


def update_frontmatter(text: str, updates: dict) -> str:
    """Update YAML frontmatter in markdown."""
    lines = text.split("\n")
    in_fm = False
    fm_end = 0
    for i, line in enumerate(lines):
        if line.strip() == "---":
            if not in_fm:
                in_fm = True
            else:
                fm_end = i
                break
    if not in_fm or fm_end == 0:
        return text
    for key, val in updates.items():
        found = False
        for i in range(1, fm_end):
            if lines[i].startswith(f"{key}:"):
                lines[i] = f"{key}: {val}"
                found = True
                break
        if not found:
            lines.insert(fm_end, f"{key}: {val}")
            fm_end += 1
    return "\n".join(lines)


def read_task_file(path: Path) -> dict:
    text = path.read_text()
    fm = get_frontmatter(text)
    return {
        "path": path,
        "name": path.name,
        "id": fm.get("id", path.stem),
        "title": fm.get("title", path.stem),
        "status": fm.get("status", "todo"),
        "priority": fm.get("priority", "medium"),
        "claimed_by": fm.get("claimed_by", ""),
        "created_by": fm.get("created_by", "unknown"),
        "tags": fm.get("tags", "").split(",") if fm.get("tags") else [],
    }


def get_idle_agents(registry: dict) -> list:
    return [
        name for name, info in registry.get("agents", {}).items()
        if info.get("status") == "idle"
    ]


def get_unclaimed_tasks() -> list:
    tasks = []
    for f in INBOX.glob("*.md"):
        # Skip README and non-task files
        if f.name.upper().startswith("README"):
            continue
        task = read_task_file(f)
        if task["status"] in ("todo", "backlog") and not task["claimed_by"]:
            tasks.append(task)
    tasks.sort(key=lambda t: PRIORITY_ORDER.index(t["priority"]) if t["priority"] in PRIORITY_ORDER else 2)
    return tasks


def dispatch_task(task: dict, agent_id: str, registry: dict):
    """Claim a task for an agent."""
    path = task["path"]
    text = path.read_text()
    text = update_frontmatter(text, {
        "status": "in-progress",
        "claimed_by": agent_id,
        "claimed_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    })
    path.write_text(text)
    
    # Update registry
    if agent_id in registry.get("agents", {}):
        registry["agents"][agent_id]["status"] = "busy"
        registry["agents"][agent_id]["current_task"] = task["id"]
    
    # Touch wake signal
    wake_file = SIGNALS / f"wake-{agent_id}"
    touch(wake_file)
    
    print(f"  ✅ Dispatched: [{task['id']}] '{task['title']}' → {agent_id}")
    return True


def process_inbox():
    """One poll cycle."""
    ensure_state_files()
    registry = load_json(REGISTRY)
    if not registry:
        print("  ⚠️  No registry found. Run `dispatch.py init` first.")
        return

    # Update heartbeat
    now = datetime.now().isoformat()
    heartbeat = load_json(HEARTBEAT)
    for name in registry.get("agents", {}):
        if name in heartbeat:
            heartbeat[name]["last_seen"] = now
    save_json(HEARTBEAT, heartbeat)

    # Find idle agents
    idle_agents = get_idle_agents(registry)
    if not idle_agents:
        print("  ⏳ No idle agents")
        return

    # Find unclaimed tasks
    unclaimed = get_unclaimed_tasks()
    if not unclaimed:
        print("  ⏳ No unclaimed tasks in inbox")
        return

    # Dispatch to first idle agent that matches agent_hints
    for task in unclaimed:
        for agent_id in idle_agents:
            disp = dispatch_task(task, agent_id, registry)
            if disp:
                save_json(REGISTRY, registry)
                return


def show_status():
    """Show current state."""
    ensure_state_files()
    registry = load_json(REGISTRY)
    heartbeat = load_json(HEARTBEAT)
    
    print("\n🧠 Shepherd's Brain — Coordination Status")
    print("=" * 50)
    
    for name, info in registry.get("agents", {}).items():
        hb = heartbeat.get(name, {})
        status = "🟢 idle" if info.get("status") == "idle" else "🔴 busy"
        task = info.get("current_task", "—")
        last = hb.get("last_seen", "never")
        print(f"\n  {name.upper()} {status}")
        print(f"    Task: {task}")
        print(f"    Last seen: {last}")
    
    print("\n📋 Inbox Tasks:")
    unclaimed = get_unclaimed_tasks()
    if unclaimed:
        for t in unclaimed:
            print(f"  [{t['priority'].upper():8}] {t['id']} — {t['title']}")
    else:
        print("  (empty)")
    
    print()


def init_first_task():
    """Create a test task to verify the system works."""
    task_path = INBOX / "2026-05-12-001.md"
    if task_path.exists():
        print(f"  ℹ️  {task_path.name} already exists")
        return
    
    content = """---
id: 2026-05-12-001
title: TEST TASK — Verify coordination layer works
status: todo
priority: low
claimed_by:
depends_on: []
tags: [test, coordination]
created_by: promachos
created_at: 2026-05-12T14:45:00+08:00
agent_hints:
  suggest_to: [ava]
  block_agents: []
---

# Coordination Layer Test Task

This is a **test task** to verify the coordination layer is working.

## Done When

- Ava reads this task from the inbox
- Ava claims it (updates claimed_by in frontmatter)
- Ava marks it done (updates status to done)
- Both agents' heartbeat timestamps update

## Background

This was created by Promachos to test the Batty-style dispatch daemon.
If you're reading this, the vault coordination layer is operational.

---

**If you're Ava:** Claim this task by running:
```
python .coordination/dispatch.py claim 2026-05-12-001 ava
```

Or manually update the frontmatter:
```yaml
claimed_by: ava
status: in-progress
```

Then mark done when complete.

---

*Test task — safe to delete after verification.*
"""
    task_path.write_text(content)
    print(f"  ✅ Created test task: {task_path.name}")
    print("  Run `dispatch.py test` to see dispatch in action")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    
    if cmd == "start":
        print(f"🚀 Starting dispatch daemon (poll every {POLL_INTERVAL}s)")
        print("   Press Ctrl+C to stop")
        while True:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Polling...")
            process_inbox()
            time.sleep(POLL_INTERVAL)
    
    elif cmd == "status":
        show_status()
    
    elif cmd == "test":
        print(f"🔄 Running one poll cycle...")
        process_inbox()
    
    elif cmd == "init":
        print("📦 Initializing coordination layer...")
        init_first_task()
    
    elif cmd == "claim":
        if len(sys.argv) < 4:
            print("Usage: dispatch.py claim <task-id> <agent-id>")
            sys.exit(1)
        task_id = sys.argv[2]
        agent_id = sys.argv[3]
        task_file = INBOX / f"{task_id}.md"
        if not task_file.exists():
            task_file = TASKS / f"{task_id}.md"
        if not task_file.exists():
            print(f"  ❌ Task not found: {task_id}")
            sys.exit(1)
        text = task_file.read_text()
        text = update_frontmatter(text, {
            "claimed_by": agent_id,
            "status": "in-progress",
            "claimed_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
        })
        task_file.write_text(text)
        registry = load_json(REGISTRY)
        if agent_id in registry.get("agents", {}):
            registry["agents"][agent_id]["status"] = "busy"
            registry["agents"][agent_id]["current_task"] = task_id
            save_json(REGISTRY, registry)
        touch(SIGNALS / f"wake-{agent_id}")
        print(f"  ✅ Claimed {task_id} → {agent_id}")
    
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: dispatch.py start|status|test|init|claim")
        sys.exit(1)


if __name__ == "__main__":
    main()