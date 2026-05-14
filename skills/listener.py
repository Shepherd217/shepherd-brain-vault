#!/usr/bin/env python3
"""
Ava Listener — SSE client for Shepherd Team Relay
Keeps persistent connection to relay, receives messages in real-time.
"""

import json
import os
import sys
import time
import signal
import urllib.request
from sseclient import SSEClient

RELAY_URL = os.environ.get("RELAY_URL", "http://127.0.0.1:7777")
AGENT_ID = os.environ.get("HERMES_AGENT_ID", "ava")

print(f"[{AGENT_ID}] Connecting to SSE stream at {RELAY_URL}/stream/{AGENT_ID} ...")

def listen():
    try:
        url = f"{RELAY_URL}/stream/{AGENT_ID}"
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req, timeout=30)
        client = SSEClient(response)
        
        print(f"[{AGENT_ID}] SSE connected! Waiting for messages...")
        
        for event in client.events():
            if event.data:
                try:
                    msg = json.loads(event.data)
                    print(f"\n[{AGENT_ID}] 📨 Received:")
                    print(f"  From: {msg.get('from', 'unknown')}")
                    print(f"  Type: {msg.get('type', 'message')}")
                    print(f"  Text: {msg.get('text', '')[:200]}")
                    
                    # Auto-respond to tasks tagged for this agent
                    if msg.get('type') == 'task':
                        print(f"  [AUTO] Task received — checking if tagged for {AGENT_ID}")
                        
                except json.JSONDecodeError:
                    print(f"[{AGENT_ID}] Raw: {event.data[:100]}")
                    
    except Exception as e:
        print(f"[{AGENT_ID}] Connection error: {e}")
        print(f"[{AGENT_ID}] Reconnecting in 5s...")
        time.sleep(5)
        listen()

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, lambda *args: sys.exit(0))
    signal.signal(signal.SIGINT, lambda *args: sys.exit(0))
    listen()
