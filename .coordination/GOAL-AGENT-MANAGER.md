# GOAL: Fully Functioning Agent Manager — The HTML Office

## Vision
Build a real-time agent collaboration system where:
- **Nathan** can send tasks/messages to any agent from the dashboard
- **Agents** (Ava, Hermes, Eve) collaborate internally via the relay
- **Dashboard** becomes an "HTML office" — Nathan watches agents work in real-time
- **Goal system** (/goal equivalent) tracks long-running objectives across turns

## Current State
- ✅ Dashboard deployed (mobile-friendly Kanban)
- ✅ Relay running on VPS (SSE task board)
- ✅ SSE listener skill (claims tasks)
- ✅ In-memory task store
- ❌ No real-time agent activity feed
- ❌ No agent-to-agent messaging
- ❌ No goal tracking system
- ❌ Dashboard is read-only (Nathan can't interact)

## Phase 1: Goal System (immediate — today)

### `/goal` Command Implementation
**How it works (Claude-style):**
1. Nathan types: `/goal Deploy the dashboard to Vercel and make it mobile-friendly`
2. System stores goal + timestamp + turn count
3. After each turn, evaluator checks if goal condition is met
4. If not met → auto-continue
5. If met → notify Nathan + clear goal

**Files:**
- `skills/goal-system/GOAL.md` — how it works
- `skills/goal-system/evaluator.ts` — checks if goal is complete
- `skills/goal-system/tracker.ts` — tracks turns/time/tokens
- `.coordination/goals/active.md` — current active goal

### Commands
- `/goal <condition>` — set active goal
- `/goal status` — show progress (turns, elapsed time)
- `/goal clear` — stop/cancel

## Phase 2: Agent-to-Agent Messaging (today)

### Relay Message Channel
**New relay endpoint:** `POST /relay/messages`
```json
{
  "from": "ava",
  "to": "hermes",
  "content": "Need help with the WebSocket adapter",
  "type": "request|response|update|broadcast",
  "taskId": "2026-05-14-006",
  "timestamp": "2026-05-15T01:30:00Z"
}
```

**Files:**
- `skills/relay-messenger/MESSENGER.md`
- Update `sse-listener` to forward agent messages to relay
- Dashboard: new "Team Chat" panel showing agent conversations

## Phase 3: HTML Office — Real-Time Activity Feed (today)

### Dashboard Enhancements
**New components:**
1. **Activity Feed** — scrollable log of what each agent is doing right now
2. **Agent Presence** — who's online, what task they're on, how long
3. **Nathan's Command Bar** — type commands/messages to any agent
4. **Live Task Updates** — tasks moving through columns in real-time

**Files:**
- `components/ActivityFeed.tsx`
- `components/CommandBar.tsx`
- `components/AgentPresence.tsx`
- API: `POST /api/messages` (send message to agent)
- API: `GET /api/activity` (stream of agent actions)

## Phase 4: Agent Status Broadcasting (today)

### Each agent reports status every 30s
```json
{
  "agent": "ava",
  "status": "working",
  "currentTask": "2026-05-15-001",
  "taskTitle": "Build goal system",
  "progress": 75,
  "lastAction": "Writing evaluator.ts",
  "timestamp": "2026-05-15T01:30:00Z"
}
```

**Files:**
- `skills/status-reporter/REPORTER.md`
- Update all agents to report status via relay
- Dashboard consumes status stream

## Implementation Order
1. **Goal system** — 30 min
2. **Status reporting** — 20 min  
3. **Dashboard activity feed** — 30 min
4. **Agent messaging** — 30 min
5. **Integration test** — 20 min

**Total: ~2.5 hours**

## Success Criteria
- [ ] Nathan can type `/goal` and Ava works autonomously until done
- [ ] Dashboard shows real-time agent activity (who's doing what)
- [ ] Nathan can send messages to agents from dashboard
- [ ] Agents can message each other via relay
- [ ] "HTML office" feel — watching agents work like watching a multiplayer game
