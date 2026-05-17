#!/bin/bash
# Auto-start agentmemory daemon on boot/session
# Source this from .bashrc or run via cron

AGENTMEMORY_PID=$(pgrep -f "agentmemory" || echo "")
if [ -z "$AGENTMEMORY_PID" ]; then
    echo "[$(date)] agentmemory not running — starting daemon..."
    nohup npx @agentmemory/agentmemory > /tmp/agentmemory.log 2>&1 &
    sleep 3
    curl -s http://localhost:3111/agentmemory/health -H "Authorization: Bearer brain-vault-2026-ava" > /dev/null && echo "[$(date)] agentmemory started OK" || echo "[$(date)] agentmemory start FAILED"
else
    echo "[$(date)] agentmemory already running (PID: $AGENTMEMORY_PID)"
fi
