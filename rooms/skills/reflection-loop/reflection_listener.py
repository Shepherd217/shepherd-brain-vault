#!/usr/bin/env python3
"""
Reflection Loop Listener — SSE-based auto-reflection for Shepherd Team

Watches for task_completed events and auto-generates reflection tasks.
"""

import json
import os
import sys
import time
import re
from datetime import datetime
from urllib.request import Request, urlopen
from sseclient import SSEClient

RELAY_URL = os.environ.get("RELAY_URL", "http://127.0.0.1:7777")
AGENT_ID = os.environ.get("HERMES_AGENT_ID", "ava")
REFLECTION_DIR = os.environ.get(
    "REFLECTION_OUTPUT_DIR",
    "/root/.openclaw/workspace/shepherd-brain-vault/rooms/moltos/reflections"
)


def _call(method: str, path: str, body: dict | None = None) -> dict:
    url = f"{RELAY_URL}{path}"
    data = json.dumps(body).encode() if body else None
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"[reflection] API call failed: {e}")
        return {"ok": False, "error": str(e)}


def generate_reflection_task(completed_task: dict) -> dict:
    """Generate a reflection task from a completed task."""
    task_id = completed_task.get("id", "unknown")
    task_title = completed_task.get("title", "Unknown Task")
    owner = completed_task.get("owner", "unknown")
    result = completed_task.get("result", "")
    
    reflection_title = f"Reflection on {task_id}: {task_title}"
    
    description = f"""Agent {owner} completed task "{task_title}".

Original task result summary:
{result[:500] if result else "(no result provided)"}

Please spend 5 minutes answering:
• What went well? What was slow or confusing?
• Any bottlenecks in the tools, environment, or your own approach?
• One concrete improvement you'd make next time (skill patch, prompt tweak, workflow change).
• Optional: Suggest a meta-improvement for the team (e.g., new automation, better documentation).

Store your reflection at: {REFLECTION_DIR}/{owner}/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{task_id}.md"""

    return {
        "title": reflection_title,
        "description": description,
        "tags": ["reflection", owner],
        "priority": "low",  # Reflections are non-urgent
    }


def create_reflection_task(task_data: dict) -> dict:
    """Post reflection task to the shared board."""
    reflection = generate_reflection_task(task_data)
    return _call("POST", "/tasks", reflection)


def save_reflection_to_vault(agent_id: str, task_id: str, reflection_text: str) -> str:
    """Save reflection markdown to vault directory."""
    agent_dir = os.path.join(REFLECTION_DIR, agent_id)
    os.makedirs(agent_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{task_id}.md"
    filepath = os.path.join(agent_dir, filename)
    
    with open(filepath, "w") as f:
        f.write(reflection_text)
    
    return filepath


def process_task_completed(event_data: dict):
    """Handle a task_completed event from the relay."""
    task = event_data.get("task", {})
    task_id = task.get("id", "unknown")
    owner = task.get("owner", "unknown")
    
    print(f"[reflection] Task completed: {task_id} by {owner}")
    
    # Don't reflect on reflection tasks themselves (avoid infinite loop)
    tags = task.get("tags", [])
    if "reflection" in tags:
        print(f"[reflection] Skipping — this is already a reflection task")
        return
    
    # Generate and post reflection task
    result = create_reflection_task(task)
    
    if result.get("ok"):
        reflection_id = result.get("task", {}).get("id", "unknown")
        print(f"[reflection] Created reflection task: {reflection_id}")
        
        # Notify the team
        _call("POST", "/broadcast", {
            "from": "reflection-loop",
            "to": "all",
            "text": f"🔄 Reflection task created for {owner}'s completed work: {task_id}. Check the board!",
            "type": "status",
            "metadata": {"reflection_task_id": reflection_id, "original_task_id": task_id}
        })
    else:
        print(f"[reflection] Failed to create reflection task: {result}")


def listen_for_completions():
    """Main loop: Listen to SSE stream for task completions."""
    stream_url = f"{RELAY_URL}/stream/reflection-loop"
    
    print(f"[reflection] Connecting to {stream_url} ...")
    
    while True:
        try:
            req = Request(stream_url)
            response = urlopen(req, timeout=30)
            client = SSEClient(response)
            
            print("[reflection] SSE connected! Watching for task completions...")
            
            for event in client.events():
                if not event.data:
                    continue
                    
                try:
                    msg = json.loads(event.data)
                    msg_type = msg.get("type", "")
                    
                    # Look for task completion events
                    if msg_type == "status" and "completed" in msg.get("text", "").lower():
                        # Extract task data from message or metadata
                        metadata = msg.get("metadata", {})
                        if "taskId" in metadata:
                            # Fetch full task data
                            task_result = _call("GET", f"/tasks?id={metadata['taskId']}")
                            if task_result.get("ok") and task_result.get("tasks"):
                                process_task_completed({"task": task_result["tasks"][0]})
                    
                    # Also check for explicit task_completed type
                    if msg_type == "task_completed":
                        process_task_completed(msg)
                        
                except json.JSONDecodeError:
                    pass
                except Exception as e:
                    print(f"[reflection] Error processing event: {e}")
                    
        except Exception as e:
            print(f"[reflection] Connection error: {e}")
            print("[reflection] Reconnecting in 5s...")
            time.sleep(5)


def start_reflection_listener(relay_url: str = None, agent_id: str = None):
    """Entry point to start the reflection listener."""
    global RELAY_URL, AGENT_ID
    
    if relay_url:
        RELAY_URL = relay_url
    if agent_id:
        AGENT_ID = agent_id
    
    # Ensure output directory exists
    os.makedirs(REFLECTION_DIR, exist_ok=True)
    
    print(f"[reflection] Starting reflection loop for agent: {AGENT_ID}")
    print(f"[reflection] Relay: {RELAY_URL}")
    print(f"[reflection] Output dir: {REFLECTION_DIR}")
    
    listen_for_completions()


if __name__ == "__main__":
    start_reflection_listener()
