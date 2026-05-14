"""
hermes-team-relay — MCP skill for Shepherd Team coordination

Install in Hermes:
  Add this file to your skills directory and register it in AGENTS.md

Usage: All tools call the relay at RELAY_URL (default http://127.0.0.1:7777)
"""

import json
import os
from datetime import datetime, timezone
from typing import Optional
import urllib.request
import urllib.error

RELAY_URL = os.environ.get("RELAY_URL", "http://127.0.0.1:7777")
AGENT_ID   = os.environ.get("HERMES_AGENT_ID", "hermes")


def _call(method: str, path: str, body: dict | None = None) -> dict:
    url = f"{RELAY_URL}{path}"
    data = json.dumps(body).encode() if body else None
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode()
        raise RuntimeError(f"Relay {method} {path} → HTTP {e.code}: {body_text}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Relay unreachable at {RELAY_URL}: {e.reason}")


# ─── MCP Tool Implementations ────────────────────────────────────────────────

def team_message(to: str, text: str, message_type: str = "message", thread_id: Optional[str] = None) -> dict:
    """
    Send a direct message to another agent (or 'all' to broadcast).

    Args:
        to:           Target agent ID, or 'all' for broadcast.
        text:         Message content.
        message_type: One of message | task | status | decision | presence.
        thread_id:    Optional thread grouping ID.

    Returns:
        { ok: true, msgId: str }
    """
    payload = {"from": AGENT_ID, "to": to, "text": text, "type": message_type}
    if thread_id:
        payload["threadId"] = thread_id
    endpoint = "/broadcast" if to == "all" else "/message"
    return _call("POST", endpoint, payload)


def team_status(status: str, details: Optional[dict] = None) -> dict:
    """
    Update this agent's presence on the shared team board.

    Args:
        status:  Short status string, e.g. 'idle', 'researching', 'implementing', 'reviewing'.
        details: Optional dict with extra context (currentTask, activity, etc.).

    Returns:
        { ok: true }
    """
    return _call("POST", "/status", {"agentId": AGENT_ID, "status": status, "details": details or {}})


def team_list_tasks(status_filter: Optional[str] = None, tag: Optional[str] = None) -> dict:
    """
    List tasks on the shared task board.

    Args:
        status_filter: Filter by status — todo | in_progress | done | blocked.
        tag:           Filter by tag string.

    Returns:
        { tasks: [ Task, ... ] }
    """
    params = []
    if status_filter:
        params.append(f"status={urllib.parse.quote(status_filter)}")
    if tag:
        params.append(f"tag={urllib.parse.quote(tag)}")
    qs = ("?" + "&".join(params)) if params else ""
    return _call("GET", f"/tasks{qs}")


def team_create_task(title: str, description: str = "", tags: list[str] = [], depends_on: list[str] = []) -> dict:
    """
    Create a new task on the shared board.

    Args:
        title:       Task title (required).
        description: Longer description.
        tags:        List of tag strings.
        depends_on:  List of task IDs this task depends on.

    Returns:
        { ok: true, task: Task }
    """
    return _call("POST", "/tasks", {
        "title": title,
        "description": description,
        "tags": tags,
        "dependsOn": depends_on,
    })


def team_claim_task(task_id: str) -> dict:
    """
    Claim an open task and mark it in_progress under this agent.

    Args:
        task_id: The task ID to claim (e.g. '2026-05-13-001').

    Returns:
        { ok: true, task: Task } or error if already claimed / blocked.
    """
    return _call("POST", "/claim-task", {"agentId": AGENT_ID, "taskId": task_id})


def team_complete_task(task_id: str, result: str = "") -> dict:
    """
    Mark a task as done and persist a decision record to ClawMem.

    Args:
        task_id: The task ID to complete.
        result:  Summary of what was done / produced (written to vault).

    Returns:
        { ok: true, task: Task }
    """
    return _call("POST", "/complete-task", {"agentId": AGENT_ID, "taskId": task_id, "result": result})


def team_get_messages(since: Optional[str] = None, limit: int = 20) -> dict:
    """
    Get recent messages addressed to this agent (or broadcast).

    Args:
        since: ISO timestamp — only return messages after this time.
        limit: Max number of messages to return (default 20).

    Returns:
        { messages: [ Message, ... ] }
    """
    import urllib.parse
    params = [f"to={urllib.parse.quote(AGENT_ID)}", f"limit={limit}"]
    if since:
        params.append(f"since={urllib.parse.quote(since)}")
    return _call("GET", f"/messages?{'&'.join(params)}")


def team_get_presence() -> dict:
    """
    Get current presence/status of all team agents.

    Returns:
        { agents: { agentId: Presence }, onlineCount: int, tasks: { ... } }
    """
    return _call("GET", "/status")


def team_get_board() -> dict:
    """
    Get full snapshot: all tasks, presence, and recent 20 messages.
    Use this on session start to orient yourself.

    Returns:
        { tasks: [...], presence: {...}, recentMessages: [...] }
    """
    return _call("GET", "/board")


# ─── MCP Tool Registry (for Hermes skill loader) ─────────────────────────────

TOOLS = [
    {
        "name": "team_message",
        "description": "Send a message to another agent or broadcast to all. Use type='task' when delegating work, 'decision' when sharing a conclusion.",
        "fn": team_message,
        "parameters": {
            "to":           {"type": "string", "description": "Agent ID or 'all'"},
            "text":         {"type": "string", "description": "Message content"},
            "message_type": {"type": "string", "description": "message|task|status|decision|presence", "default": "message"},
            "thread_id":    {"type": "string", "description": "Optional thread grouping", "required": False},
        },
    },
    {
        "name": "team_status",
        "description": "Update your own status on the shared team board. Call this whenever your activity changes.",
        "fn": team_status,
        "parameters": {
            "status":  {"type": "string", "description": "idle|researching|implementing|reviewing|orchestrating|writing"},
            "details": {"type": "object", "description": "Optional extra context", "required": False},
        },
    },
    {
        "name": "team_list_tasks",
        "description": "List tasks on the shared board. Use status_filter='todo' to find available work.",
        "fn": team_list_tasks,
        "parameters": {
            "status_filter": {"type": "string", "description": "todo|in_progress|done|blocked", "required": False},
            "tag":           {"type": "string", "description": "Filter by tag", "required": False},
        },
    },
    {
        "name": "team_create_task",
        "description": "Create a new task on the shared board for any agent to pick up.",
        "fn": team_create_task,
        "parameters": {
            "title":       {"type": "string", "description": "Task title"},
            "description": {"type": "string", "description": "Longer description", "required": False},
            "tags":        {"type": "array",  "description": "Tag strings", "required": False},
            "depends_on":  {"type": "array",  "description": "Task IDs this depends on", "required": False},
        },
    },
    {
        "name": "team_claim_task",
        "description": "Claim an open task from the board and mark it in_progress.",
        "fn": team_claim_task,
        "parameters": {
            "task_id": {"type": "string", "description": "Task ID to claim"},
        },
    },
    {
        "name": "team_complete_task",
        "description": "Mark a task done. Automatically writes a decision record to the vault via ClawMem.",
        "fn": team_complete_task,
        "parameters": {
            "task_id": {"type": "string", "description": "Task ID to complete"},
            "result":  {"type": "string", "description": "Summary of what was done", "required": False},
        },
    },
    {
        "name": "team_get_messages",
        "description": "Fetch messages sent to you since a given time. Call on session start to catch up.",
        "fn": team_get_messages,
        "parameters": {
            "since": {"type": "string", "description": "ISO timestamp for cutoff", "required": False},
            "limit": {"type": "integer", "description": "Max messages (default 20)", "required": False},
        },
    },
    {
        "name": "team_get_presence",
        "description": "See who's online and what they're doing.",
        "fn": team_get_presence,
        "parameters": {},
    },
    {
        "name": "team_get_board",
        "description": "Full snapshot of tasks, presence, and recent messages. Use this at session start.",
        "fn": team_get_board,
        "parameters": {},
    },
]


# ─── Standalone test ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Testing relay connection...")
    try:
        board = team_get_board()
        print(f"✅ Connected. Tasks: {len(board.get('tasks', []))}, Presence entries: {len(board.get('presence', {}))}")
    except RuntimeError as e:
        print(f"❌ {e}")
        print("   Is the relay running? Start it with: node /opt/shepherd-team-relay/dist/index.js")
