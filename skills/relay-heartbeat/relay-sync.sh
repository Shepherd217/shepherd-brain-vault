#!/bin/bash
# relay-sync.sh — Git sync + relay heartbeat combo
# Run every 30 minutes to keep team updated

cd /root/.openclaw/workspace

echo "=== $(date '+%Y-%m-%d %H:%M %Z') ==="

# 1. Auto-pull from GitHub (if behind)
echo "☁️  Git sync..."
git fetch origin main --quiet 2>/dev/null
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main 2>/dev/null || echo "")
if [ "$LOCAL" != "$REMOTE" ] && [ -n "$REMOTE" ]; then
    echo "  🔄 Behind origin — pulling..."
    git pull origin main --quiet
    echo "  ✅ Updated to $REMOTE"
else
    echo "  ✅ Up to date"
fi

# 2. Post heartbeat to relay
echo "📡 Relay heartbeat..."
python3 skills/relay-heartbeat/relay-heartbeat.py

echo "Done."
