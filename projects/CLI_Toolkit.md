---
date: 2026-05-08
type: cli-toolkit
tags: [printing-press, cli, integration]
---

# Printing Press CLI Toolkit

## Installed CLIs

### espn-pp-cli — Sports Data
- **What:** Live scores, standings, news, game history across 17 sports
- **Usage:** `espn-pp-cli [command] --agent` (JSON output for automation)
- **Path:** `/root/go/bin/espn-pp-cli`

### flight-goat-pp-cli — Flight Data
- **What:** Flight search, SQLite watchlist, connectivity checks
- **Usage:** `flight-goat-pp-cli [command] --agent`
- **Special:** `flight-goat-pp-cli doctor` — verifies auth/connectivity
- **Path:** `/root/go/bin/flight-goat-pp-cli`

### movie-goat-pp-cli — Movie Ratings
- **What:** TMDb + OMDb ratings, tonight picks, watchlist
- **Usage:** `movie-goat-pp-cli [command] --agent`
- **Special:** `movie-goat-pp-cli tonight` — trending titles streaming now
- **Path:** `/root/go/bin/movie-goat-pp-cli`

## Integration with Triple Memory

When Nathan asks me to check sports scores, flight prices, or movie ratings:
1. Run the CLI with `--agent` flag (JSON output)
2. Parse the JSON
3. Write structured result to vault
4. Push to GitHub
5. Nathan has it on his phone in Obsidian

## Vault Storage Pattern

```
vault/
├── captures/
│   ├── espn-YYYY-MM-DD.md        # Sports results
│   ├── flights-YYYY-MM-DD.md     # Flight searches
│   └── movies-YYYY-MM-DD.md    # Movie picks/ratings
```

## Usage Examples

### Check Tonight's Movies
```bash
movie-goat-pp-cli tonight --agent > /tmp/movies.json
```
→ I parse JSON → write to `captures/movies-2026-05-08.md`

### Check Live Scores
```bash
espn-pp-cli scores --sport nba --agent > /tmp/espn.json
```
→ I parse JSON → write to `captures/espn-2026-05-08.md`

### Check Flights
```bash
flight-goat-pp-cli search --origin ORD --destination LAX --agent > /tmp/flights.json
```
→ I parse JSON → write to `captures/flights-2026-05-08.md`

## Recipe Goat
- **Status:** Blocked — OOM during compile (Surf-Chrome transport is heavy)
- **Retry:** Manual Go install if needed
- **Command:** `go install github.com/mvanhorn/printing-press-library/library/lifestyle/recipe-goat/cmd/recipe-goat-pp-cli@latest`

## The Promise
These CLIs feed the vault. The vault feeds the Gbrain. The Gbrain finds patterns. Every sports check, every flight search, every movie night — all captured, all connected, all part of the triple memory.
