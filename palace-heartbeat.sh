#!/bin/bash
# palace-heartbeat.sh — Active heartbeat that DOES things
# Run this to prove the palace is alive

VAULT="/root/.openclaw/workspace/shepherd-brain-vault"
COORD="/root/.openclaw/workspace/.coordination"

echo "🏛️  Palace Heartbeat — $(date '+%Y-%m-%d %H:%M %Z')"
echo "================================================"

# 1. Check dream freshness
echo ""
echo "🧠 Dream Cycle"
DREAM_COUNT=$(ls $VAULT/drawers/dreams/*.md 2>/dev/null | wc -l)
echo "   Dreams in vault: $DREAM_COUNT"
if [ $DREAM_COUNT -gt 0 ]; then
    LATEST_DREAM=$(ls -t $VAULT/drawers/dreams/*.md | head -1)
    echo "   Latest: $(basename $LATEST_DREAM)"
fi

# 2. Check pattern activity
echo ""
echo "🔍 Patterns Room"
PATTERN_COUNT=$(ls $VAULT/rooms/patterns/*.md 2>/dev/null | wc -l)
echo "   Active patterns: $PATTERN_COUNT"

# 3. Check coordination queue
echo ""
echo "📋 Coordination Inbox"
TODO_COUNT=$(grep -l "status: \(todo\|backlog\)" $COORD/tasks/inbox/*.md 2>/dev/null | wc -l)
DONE_COUNT=$(grep -l "status: done" $COORD/tasks/inbox/*.md 2>/dev/null | wc -l)
echo "   Open tasks: $TODO_COUNT"
echo "   Completed: $DONE_COUNT"

# 4. Check agent status
echo ""
echo "🤖 Agent Status"
python3 $COORD/dispatch.py status 2>/dev/null | grep -E "(PROMACHOS|AVA|EVE)" || echo "   Agents: Check registry.json"

# 5. Check memory freshness
echo ""
echo "📝 Memory"
LATEST_MEMORY=$(ls -t /root/.openclaw/workspace/memory/*.md 2>/dev/null | head -1)
if [ -n "$LATEST_MEMORY" ]; then
    echo "   Latest: $(basename $LATEST_MEMORY)"
    echo "   Size: $(wc -l < $LATEST_MEMORY) lines"
fi

# 6. Git status
echo ""
echo "☁️  Git Sync"
cd /root/.openclaw/workspace
UNPUSHED=$(git log origin/main..HEAD --oneline 2>/dev/null | wc -l)
if [ "$UNPUSHED" -gt 0 ]; then
    echo "   ⚠️  $UNPUSHED commits unpushed"
else
    echo "   ✅ Synced with GitHub"
fi

echo ""
echo "================================================"
echo "💓 Palace is alive. Forward is enough."
