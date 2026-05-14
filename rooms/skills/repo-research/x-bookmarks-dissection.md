# Repo Dissection: x-bookmarks by sharbelxyz
**Date:** 2026-05-12  
**Source:** Nathan's bookmark + Grok research  
**Dissected by:** Midas (Promachos)

---

## What It Is

An **OpenClaw skill** that turns X/Twitter bookmarks into agent actions. Not summaries — actual executable proposals.

**Core thesis:** "Stop hoarding. Start applying."

---

## Architecture

### Dual Backend (Auto-Detecting)

| Backend | Auth Method | Pros | Cons |
|---------|-------------|------|------|
| **bird CLI** | Cookie-based (Chrome profile) | No API keys, no dev account, works immediately | Requires Chrome login |
| **X API v2** | OAuth 2.0 | Official, scalable, production-ready | Needs dev account, OAuth setup |

**Auto-detection flow:**
1. Try `bird whoami` → if works, use bird CLI
2. If not, check `~/.config/x-bookmarks/` for API tokens
3. If neither, walk user through setup

### Bird CLI — The Key Insight

```bash
npm install -g bird-cli
# Log into x.com in Chrome
bird --chrome-profile "Default" bookmarks --json
```

**What bird does:**
- Reads Chrome cookies (`auth_token` + `ct0`)
- Makes authenticated requests AS the logged-in user
- Supports: bookmarks, timeline, search, DMs, lists
- No API keys. No OAuth. No developer account.

**Why this works:**
- X/Twitter stores session cookies in Chrome
- bird extracts those cookies and uses them for API-like requests
- As long as Chrome is logged in, bird has full read access
- This is the same mechanism browser extensions use

---

## What It Does (Workflow)

### 1. Fetch Bookmarks
- Pulls latest bookmarks via bird or API
- Outputs standardized JSON regardless of backend

### 2. Categorize
- AI-categorizes by topic: AI tools, trading, marketing, crypto, etc.
- Not manual tagging — the agent figures it out

### 3. Propose Actions
This is the killer feature. Not summaries. Actions:

```
📂 AI TOOLS (3)
• @someone shared a repo for automating video edits
  → 🤖 I CAN: Clone it, test it, and set it up for you

📂 TRADING (2)  
• @trader posted a new momentum strategy with backtest data
  → 🤖 I CAN: Compare this against your current strategy
```

### 4. Natural Language Interface
- "check my bookmarks"
- "bookmark digest"
- "what did I bookmark this week?"
- "find patterns in my bookmarks"
- "clean up old bookmarks"

### 5. Scheduled Digests
- Cron support for automatic bookmark checks
- Delivers digest to user on schedule

---

## File Structure

```
x-bookmarks/
├── SKILL.md                    # Agent instructions
├── scripts/
│   ├── fetch_bookmarks.sh        # bird CLI wrapper
│   ├── fetch_bookmarks_api.py    # X API v2 fetcher
│   └── x_api_auth.py             # OAuth 2.0 PKCE helper
└── references/
    └── auth-setup.md             # Detailed setup guide
```

---

## Integration with Our System

### How to Adapt for Our TwitterMiner

**Option 1: Direct bird CLI Integration**
- Install bird-cli on server: `npm install -g bird-cli`
- Point bird to Chrome profile with X login
- Use bird to fetch bookmarks, timeline, likes
- Feed into our existing dissection pipeline

**Option 2: Browser Automation (OpenClaw native)**
- OpenClaw has built-in Playwright/CDP browser control
- Open x.com, log in once, save session
- Scroll timeline, read posts, extract links
- No third-party dependencies

**Option 3: Hybrid**
- Try bird CLI first (fastest)
- Fallback to browser automation
- Fallback to API (if available)

### What We'd Steal

1. **Cookie-based auth approach** — no API keys needed
2. **Action proposal system** — not summaries, but executable next steps
3. **Auto-detection logic** — try multiple backends, pick what works
4. **Categorization engine** — AI-powered topic clustering
5. **Scheduled digest pattern** — cron-based automatic processing

### Adaptation to Our Workflow

Instead of just fetching bookmarks, our TwitterMiner would:
1. **Fetch** bookmarks + timeline + likes via bird
2. **Extract** all GitHub/repo links
3. **Dissect** each repo (Picasso steal analysis)
4. **Score** for steal-ability
5. **Write** research to `vault/rooms/skills/repo-research/twitter-mined/`
6. **Propose** actions: "Clone this", "Steal this pattern", "Build similar tool"
7. **Auto-generate** skills from patterns found
8. **Deliver** morning digest to Nathan

---

## Why This Matters

**This is the solution to our Twitter auth problem.**

- No API keys
- No OAuth redirects
- No developer account
- Just Chrome cookies + bird CLI

**Nathan can:**
1. Log into X on the server browser (one time)
2. I grab cookies automatically
3. Browse bookmarks/timeline autonomously
4. Extract repos, dissect them, write to vault

---

## Next Steps

1. Install bird-cli on server
2. Open browser, navigate to x.com
3. Have Nathan log in (one time)
4. Save cookies to persistent storage
5. Test bird CLI bookmarks fetch
6. Integrate into TwitterMiner
7. Run first autonomous bookmark mining cycle

---

## Related Repos & Ecosystem

From Grok's research, here are other relevant X/Twitter tools for OpenClaw:

### Scraping & Mining
- **hundevmode/twitter-x-apify-actors-openclaw-skill** — Apify actors for production scraping (followers, leads, enrichment)
- **ythx-101/x-tweet-fetcher** — Fetches tweets/replies without login/API keys (multiple backends)

### Research & Search
- **rohunvora/x-research-skill** — Search tweets, pull threads, monitor accounts
- **X Search skill** — Available on ClawHub (search X content directly)

### Posting & Automation
- **ALT-F1-OpenClaw/openclaw-skill-x-twitter** — Post tweets, threads, media via API v2
- **opentweet/x-poster** — Twitter posting automation
- **TweetClaw** — Tweet automation skill

### MCP Integrations
- **Composio Twitter MCP** — Full toolkit (bookmarks, timeline, posting, lists) via Model Context Protocol
- **lunarpulse/openclaw-mcp-plugin** — Connect any MCP server to OpenClaw

### Bookmark Skills (Variations)
- **openclaw-x-bookmark-archiver** — Archive bookmarks long-term
- **bookmark-intelligence** — Pattern detection in bookmarks

---

## Links

- **Repo:** https://github.com/sharbelxyz/x-bookmarks
- **bird CLI:** https://github.com/elizaOS/bird (or npm: bird-cli)
- **OpenClaw skills docs:** https://docs.openclaw.ai/skills
- **awesome-openclaw-skills list** — Categorized skill directory

---

*Dissected by Midas. Saved to vault for autonomous reference.*
