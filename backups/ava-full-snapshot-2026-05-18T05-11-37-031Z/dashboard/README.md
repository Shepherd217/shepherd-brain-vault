# Shepherd Team Dashboard

Unified web dashboard for orchestrating OpenClaw and HermesAgent instances.

## Features (Phase 1)

- **Kanban Board** — 6-column task management with drag-and-drop
- **Task Queue API** — In-memory REST API with status transitions
- **Agent Monitor** — View connected agent status

## Tech Stack

- Next.js 14 (App Router)
- TypeScript (strict mode)
- Tailwind CSS + shadcn/ui
- react-beautiful-dnd

## Setup

```bash
npm install
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

## Note on Database

This demo uses an in-memory store for serverless compatibility. For production, switch to:
- **Turso/libSQL** — Serverless SQLite (recommended)
- **Neon PostgreSQL** — Serverless Postgres
- **Vercel KV** — Redis-based storage

## Architecture

See `docs/adr-001-unified-architecture.md` for full specification.

## Roadmap

- **Phase 1** (Weeks 1-2): Foundation — Kanban + API + Adapter
- **Phase 2** (Weeks 3-4): Worktree isolation + real-time sync
- **Phase 3** (Weeks 5-6): Multi-agent + Hermes adapter
- **Phase 4** (Weeks 7-8): Team features + approvals + RBAC
- **Phase 5** (Weeks 9-10): Intelligence + ClawMem + analytics
