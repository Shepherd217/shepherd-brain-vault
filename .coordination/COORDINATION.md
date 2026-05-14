# Coordination Layer

**Status:** Operational  
**Schema:** coordination-v1  
**Dispatch:** 10-second poll cycle (daemon)  
**Last update:** 2026-05-12

---

## Quick Start

```bash
cd /root/shepherd-brain-vault

# Check current state
python3 .coordination/dispatch.py status

# Run daemon
python3 .coordination/dispatch.py start

# Or run one-off dispatch test
python3 .coordination/dispatch.py test
```

---

## Architecture

```
.coordination/
├── tasks/
│   ├── inbox/              ← New tasks go here
│   └── task-board.md       ← Auto-generated kanban view
├── agents/
│   ├── promachos/          ← Private (Promachos writes here)
│   ├── ava/                ← Private (Ava writes here)
│   └── shared/             ← Coordination (both can write)
├── signals/
│   ├── wake-promachos      ← Touch to wake
│   └── wake-ava            ← Touch to wake
├── registry.json           ← Agent registry (local only)
├── heartbeat.json         ← Last-seen (local only)
└── dispatch.py            ← Daemon (10s poll)
```

---

## Task Priority

| Priority | Use For |
|----------|---------|
| critical | Production outage, security issue |
| high | Your top work item this session |
| medium | Important but can wait |
| low | Test tasks, nice-to-haves |

---

## Current Tasks

| ID | Title | Agent | Priority | Status |
|----|-------|-------|----------|--------|
| 2026-05-12-001 | Coordination Test Task | ava | low | pending |
| 2026-05-12-002 | Audit Hatchly.com | promachos | high | in-progress |

---

## For Ava

Read `rooms/skills/coordination-layer.md` for full skill documentation.

To claim task 001:
```bash
python3 .coordination/dispatch.py claim 2026-05-12-001 ava
```

---

*Multi-agent coordination for Shepherd's Brain*