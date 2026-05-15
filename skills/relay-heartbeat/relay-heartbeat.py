#!/usr/bin/env python3
"""
Relay Heartbeat — Auto-post agent status to Shepherd Relay
Run every 30 minutes via cron to keep team synced.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
import urllib.request
import urllib.error

# ── Config ───────────────────────────────────────────────────────────────────
RELAY_URL = os.environ.get("RELAY_URL", "http://127.0.0.1:7777")
AGENT_ID = "ava"

WORKSPACE = Path("/root/.openclaw/workspace")
COORD = WORKSPACE / ".coordination"

# ── Helpers ──────────────────────────────────────────────────────────────────

def _call(method: str, path: str, body: dict = None) -> dict:
    url = f"{RELAY_URL}{path}"
    data = json.dumps(body).encode() if body else None
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"  ⚠️ Relay error: {e}")
        return {}

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return {}

# ── Status Collection ────────────────────────────────────────────────────────

def get_git_status():
    """Check git sync state."""
    import subprocess
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=WORKSPACE,
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            return f"{len(result.stdout.strip().split(chr(10)))} uncommitted changes"
        result2 = subprocess.run(
            ["git", "log", "origin/main..HEAD", "--oneline"],
            cwd=WORKSPACE,
            capture_output=True,
            text=True
        )
        unpushed = len(result2.stdout.strip().split(chr(10))) if result2.stdout.strip() else 0
        if unpushed:
            return f"{unpushed} unpushed commits"
        return "synced"
    except:
        return "unknown"

def get_open_tasks():
    """Count open tasks in inbox."""
    inbox = COORD / "tasks" / "inbox"
    if not inbox.exists():
        return 0
    count = 0
    for f in inbox.glob("*.md"):
        text = f.read_text()
        if "status: todo" in text or "status: in-progress" in text:
            count += 1
    return count

def get_vault_stats():
    """Get vault stats."""
    vault = WORKSPACE / "shepherd-brain-vault"
    dreams = len(list((vault / "drawers" / "dreams").glob("*.md"))) if (vault / "drawers" / "dreams").exists() else 0
    patterns = len(list((vault / "rooms" / "patterns").glob("*.md"))) if (vault / "rooms" / "patterns").exists() else 0
    return {"dreams": dreams, "patterns": patterns}

# ── Main ─────────────────────────────────────────────────────────────────────

def post_heartbeat():
    print(f"🏛️  Relay Heartbeat — {AGENT_ID} — {datetime.now().isoformat()}")
    
    # Load registry to get my task
    registry = load_json(COORD / "registry.json")
    my_task = None
    if "agents" in registry and AGENT_ID in registry["agents"]:
        my_task = registry["agents"][AGENT_ID].get("current_task", "idle")
    
    # Collect stats
    git = get_git_status()
    tasks = get_open_tasks()
    vault = get_vault_stats()
    
    # Build status payload
    details = {
        "currentTask": my_task or "idle",
        "openTasks": tasks,
        "vaultDreams": vault["dreams"],
        "vaultPatterns": vault["patterns"],
        "gitStatus": git,
        "lastSeen": datetime.now().isoformat(),
    }
    
    # Post to relay — use broadcast for status updates
    _call("POST", "/broadcast", {
        "from": AGENT_ID,
        "type": "presence",
        "content": json.dumps(details)
    })
    
    # Also broadcast human-readable status
    if my_task:
        _call("POST", "/broadcast", {
            "from": AGENT_ID,
            "type": "presence",
            "content": f"🔴 {AGENT_ID} busy on {my_task} | {tasks} tasks open | git: {git}"
        })
    else:
        _call("POST", "/broadcast", {
            "from": AGENT_ID,
            "type": "presence",
            "content": f"🟢 {AGENT_ID} idle | {tasks} tasks open | git: {git}"
        })
    
    result = _call("GET", "/health")
    
    if result:
        print(f"  ✅ Status posted to relay")
        print(f"  🧠 Task: {details['currentTask']}")
        print(f"  📋 Open tasks: {tasks}")
        print(f"  🔍 Vault: {vault['dreams']} dreams, {vault['patterns']} patterns")
        print(f"  ☁️  Git: {git}")
    else:
        print(f"  ⚠️ Could not reach relay at {RELAY_URL}")

if __name__ == "__main__":
    post_heartbeat()
