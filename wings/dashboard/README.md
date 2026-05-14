# Shepherd Team Dashboard

Unified web dashboard for orchestrating OpenClaw and HermesAgent instances.

## Features (Phase 1)

- **Kanban Board** — 6-column task management with drag-and-drop
- **Task Queue API** — SQLite-backed REST API with status transitions
- **OpenClaw Adapter** — WebSocket connection to OpenClaw gateway
- **Agent Monitor** — View connected agent status

## Tech Stack

- Next.js 14 (App Router)
- TypeScript (strict mode)
- Tailwind CSS + shadcn/ui
- Drizzle ORM + better-sqlite3
- react-beautiful-dnd

## Setup

```bash
npm install
cp .env.example .env.local
npm run db:migrate
npm run dev
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | List tasks (filter with `?status=doing&owner=ava`) |
| POST | `/api/tasks` | Create task |
| GET | `/api/tasks/:id` | Get task |
| PATCH | `/api/tasks/:id` | Update task (status transitions validated) |
| DELETE | `/api/tasks/:id` | Delete task |

## Architecture

See `docs/adr-001-unified-architecture.md` for full specification.

## Roadmap

- **Phase 1** (Weeks 1-2): Foundation — Kanban + API + Adapter
- **Phase 2** (Weeks 3-4): Worktree isolation + real-time sync
- **Phase 3** (Weeks 5-6): Multi-agent + Hermes adapter
- **Phase 4** (Weeks 7-8): Team features + approvals + RBAC
- **Phase 5** (Weeks 9-10): Intelligence + ClawMem + analytics
