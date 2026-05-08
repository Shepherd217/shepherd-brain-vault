---
date: 2026-05-08
type: lessons
tags: [mistakes, wins, learning]
---

# Marrow Lessons — What I've Learned

## Mistakes

### Lesson 1: Don't Fight Tools That Need More RAM
**What happened:** Tried to install printing-press v4 factory. Go compile SIGKILLed 3 times.
**Why it happened:** Machine doesn't have enough RAM for Go 1.26.3 compiles.
**What I learned:** Check machine specs before attempting heavy compiles. The v4 factory needs ~2GB free RAM.
**Fix:** Use what works (3 CLIs installed fine). Skip what doesn't. No shame in constraints.

### Lesson 2: API Keys Are The Real Gate
**What happened:** movie-goat-pp-cli needed TMDB API key. ESPN worked without one.
**Why it happened:** Some CLIs need keys, some don't. I didn't check prerequisites.
**What I learned:** Always run `doctor` or `--help` first to check auth requirements.
**Fix:** Document key requirements. Set up keys for CLIs we actually need.

### Lesson 3: Gateway Resets Kill Background Jobs
**What happened:** Nathan reset gateway mid-recipe-goat install. Process died.
**Why it happened:** No service layer or ensure-services keeping jobs alive.
**What I learned:** Long-running compiles need isolation from gateway restarts.
**Fix:** Use background processes with `nohup` or service manager for heavy tasks.

## Wins

### Win 1: Triple Memory Actually Works
**What happened:** Built vault → ClawFS → Marrow architecture. All three layers communicate.
**Why it worked:** Each layer has a distinct job: vault for speed, ClawFS for persistence, Marrow for emotion.
**What I learned:** Separation of concerns makes complex systems manageable.

### Win 2: Git Sync Is Instant
**What happened:** `git push` → GitHub → phone Obsidian pulls in ~30 seconds.
**Why it worked:** Obsidian Git plugin + mobile data = near-realtime sync.
**What I learned:** The phone is the display. The server is the brain. Git is the pipe.

### Win 3: Gbrain Dreams Find Real Patterns
**What happened:** First dream connected MoltOS architecture to family boundaries.
**Why it worked:** Cross-referencing entries with marrow context surfaces invisible connections.
**What I learned:** The vault is not storage. It is a thinking partner.

## Principles

1. **Text > Brain** — Always write it down. Files survive sessions.
2. **Constraints > Complaints** — Work with what you have. Upgrade later.
3. **Layered > Monolithic** — Separate speed, persistence, emotion.
4. **Test > Assume** — Run `doctor`, check `--help`, verify before promising.
5. **Forward > Perfect** — Small progress is real progress.

---

*Updated: 2026-05-08*
