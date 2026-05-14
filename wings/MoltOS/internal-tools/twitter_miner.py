#!/usr/bin/env python3
"""
TwitterMiner — Browse Nathan's Twitter for Research Gold
Uses bird CLI (cookie-based auth) OR browser automation for full access.

**NO API KEYS NEEDED.**

What it does:
- Uses bird CLI to extract Chrome cookies for X auth
- Fetches bookmarks, timeline, likes
- Extracts links to repos, tools, articles
- Saves bookmarks for later processing
- Cross-references with existing research
- Triggers Picasso steal workflow automatically

**Two methods:**
1. bird CLI (preferred) — cookie-based, no API keys
2. Browser automation — OpenClaw native Playwright

Usage:
    python twitter_miner.py --setup          # Setup bird CLI auth
    python twitter_miner.py --mine           # Full mining run
    python twitter_miner.py --status         # Show status
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ── Config ───────────────────────────────────────────────────────────────────
CREDENTIALS_FILE = Path.home() / ".openclaw/workspace/.cache/twitter/credentials.env"
CACHE_DIR = Path.home() / ".openclaw/workspace/.cache/twitter"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

VAULT_RESEARCH_DIR = Path.home() / ".openclaw/workspace/vault/rooms/skills/repo-research/twitter-mined"
VAULT_RESEARCH_DIR.mkdir(parents=True, exist_ok=True)

# ── Bird CLI Setup ───────────────────────────────────────────────────────────

def check_bird_cli() -> bool:
    """Check if bird CLI is installed."""
    try:
        result = subprocess.run(
            ["bird", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_bird_cli():
    """Install bird CLI via npm."""
    print("📦 Installing bird CLI...")
    try:
        result = subprocess.run(
            ["npm", "install", "-g", "bird-cli"],
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            print("✅ bird CLI installed")
            return True
        else:
            print(f"❌ Installation failed: {result.stderr[:200]}")
            return False
    except FileNotFoundError:
        print("❌ npm not found. Install Node.js first.")
        return False

def test_bird_auth() -> bool:
    """Test if bird CLI can authenticate."""
    try:
        result = subprocess.run(
            ["bird", "whoami"],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0 and "username" in result.stdout.lower()
    except Exception:
        return False

def fetch_bookmarks_bird(limit: int = 50) -> List[Dict]:
    """Fetch bookmarks using bird CLI."""
    try:
        result = subprocess.run(
            ["bird", "bookmarks", "--json", "-n", str(limit)],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"❌ bird bookmarks failed: {result.stderr[:200]}")
            return []
    except Exception as e:
        print(f"❌ Error fetching bookmarks: {e}")
        return []

def fetch_timeline_bird(limit: int = 50) -> List[Dict]:
    """Fetch timeline using bird CLI."""
    try:
        result = subprocess.run(
            ["bird", "timeline", "--json", "-n", str(limit)],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"❌ bird timeline failed: {result.stderr[:200]}")
            return []
    except Exception as e:
        print(f"❌ Error fetching timeline: {e}")
        return []

# ── Mining Logic ────────────────────────────────────────────────────────────

def extract_links(tweets: List[Dict]) -> List[str]:
    """Extract all links from tweets."""
    links = []
    for tweet in tweets:
        # bird CLI JSON format
        if isinstance(tweet, dict):
            # Extract URLs from text or entities
            text = tweet.get("text", tweet.get("full_text", ""))
            import re
            urls = re.findall(r"https?://[^\s\"]+", text)
            links.extend(urls)
    return list(set(links))

def categorize_tweets(tweets: List[Dict]) -> Dict[str, List[Dict]]:
    """Categorize tweets by topic."""
    categories = {
        "ai_tools": [],
        "openclaw": [],
        "llm": [],
        "agent_frameworks": [],
        "trading": [],
        "other": []
    }
    
    for tweet in tweets:
        text = tweet.get("text", tweet.get("full_text", "")).lower()
        
        if any(x in text for x in ["openclaw", "claw"]):
            categories["openclaw"].append(tweet)
        elif any(x in text for x in ["llm", "gpt", "claude", "model"]):
            categories["llm"].append(tweet)
        elif any(x in text for x in ["agent", "autonomous", "orchestrator"]):
            categories["agent_frameworks"].append(tweet)
        elif any(x in text for x in ["ai tool", "framework", "library"]):
            categories["ai_tools"].append(tweet)
        elif any(x in text for x in ["trading", "strategy", "backtest"]):
            categories["trading"].append(tweet)
        else:
            categories["other"].append(tweet)
    
    return categories

def save_findings(links: List[str], tweets: List[Dict], source: str = "twitter"):
    """Save extracted links to vault."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    findings_file = VAULT_RESEARCH_DIR / f"findings_{timestamp}.json"
    
    # Categorize
    categories = categorize_tweets(tweets)
    
    findings = {
        "source": source,
        "mined_at": datetime.now().isoformat(),
        "total_tweets": len(tweets),
        "total_links": len(links),
        "categories": {k: len(v) for k, v in categories.items()},
        "links": links,
        "status": "pending_dissection",
    }
    
    findings_file.write_text(json.dumps(findings, indent=2))
    
    # Create markdown summary
    md_file = VAULT_RESEARCH_DIR / f"findings_{timestamp}.md"
    md_content = f"""# Twitter Mining — {datetime.now().strftime("%Y-%m-%d %H:%M")}

**Source:** {source}  
**Tweets mined:** {len(tweets)}  
**Links found:** {len(links)}  
**Status:** Pending dissection

## Categories

"""
    for cat, items in categories.items():
        if items:
            md_content += f"### {cat.replace('_', ' ').title()} ({len(items)})\n\n"
            for item in items[:5]:  # top 5 per category
                text = item.get("text", item.get("full_text", ""))[:100]
                md_content += f"- {text}...\n"
            md_content += "\n"
    
    md_content += f"\n## All Links\n\n"
    for link in links:
        md_content += f"- [ ] {link}\n"
    
    md_content += f"\n---\n*Auto-mined by TwitterMiner during autonomous cycle*\n"
    md_file.write_text(md_content)
    
    print(f"💎 Saved {len(links)} links + {len(tweets)} tweets to vault")
    return findings_file

# ── Main Mining ─────────────────────────────────────────────────────────────

def run_full_mine():
    """Run complete Twitter mining cycle."""
    print("🐦 TWITTER MINER — Full Mining Run\n")
    
    # Check bird CLI
    if not check_bird_cli():
        print("❌ bird CLI not found")
        print("   Install with: npm install -g bird-cli")
        print("   Or use: python twitter_miner.py --setup")
        return
    
    # Test auth
    if not test_bird_auth():
        print("❌ bird CLI auth failed")
        print("   You need to log into X in Chrome first")
        print("   Run: bird --chrome-profile 'Default' whoami")
        return
    
    print("✅ bird CLI authenticated\n")
    
    # Fetch data
    print("📡 Fetching bookmarks...")
    bookmarks = fetch_bookmarks_bird(limit=50)
    print(f"   Found {len(bookmarks)} bookmarks")
    
    print("\n📡 Fetching timeline...")
    timeline = fetch_timeline_bird(limit=50)
    print(f"   Found {len(timeline)} timeline tweets")
    
    all_tweets = bookmarks + timeline
    
    # Extract links
    print("\n🔗 Extracting links...")
    links = extract_links(all_tweets)
    print(f"   Found {len(links)} unique links")
    
    # Filter for repos
    repo_links = [l for l in links if "github.com" in l or "gitlab.com" in l]
    print(f"   Repos/tools: {len(repo_links)}")
    
    # Save to vault
    print("\n💾 Saving to vault...")
    findings_file = save_findings(links, all_tweets, "twitter_bird_cli")
    
    # Trigger next steps
    print("\n🔄 Next steps:")
    print("   1. Dissect repos (repo_dissection cycle)")
    print("   2. Synthesize patterns (dream_synthesis)")
    print("   3. Generate skills (skill_generation)")
    
    print(f"\n✅ Mining complete!")
    
    return findings_file

def setup_bird():
    """Setup bird CLI authentication."""
    print("🐦 TWITTER MINER — Setup\n")
    
    if not check_bird_cli():
        if not install_bird_cli():
            return False
    
    print("\n📋 Setup steps:")
    print("   1. Open Chrome and log into x.com")
    print("   2. Close Chrome completely")
    print("   3. Run: bird --chrome-profile 'Default' whoami")
    print("\n   If that shows your username, you're good to go!")
    print("\n   Then run: python twitter_miner.py --mine")
    
    return True

def show_status():
    """Show mining status."""
    print("🐦 TWITTER MINER — Status\n")
    print(f"bird CLI: {'✅ Installed' if check_bird_cli() else '❌ Not installed'}")
    print(f"Auth: {'✅ Working' if test_bird_auth() else '❌ Not authenticated'}")
    
    findings = list(VAULT_RESEARCH_DIR.glob("findings_*.json"))
    print(f"Previous mining runs: {len(findings)}")
    
    if findings:
        latest = max(findings, key=lambda p: p.stat().st_mtime)
        print(f"Last run: {datetime.fromtimestamp(latest.stat().st_mtime).strftime('%Y-%m-%d %H:%M')}")
        data = json.loads(latest.read_text())
        print(f"Links found: {data.get('total_links', 0)}")

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    
    if "--mine" in args:
        run_full_mine()
    elif "--setup" in args:
        setup_bird()
    elif "--status" in args:
        show_status()
    else:
        print(__doc__)
        print("\nCommands:")
        print("  --setup             Setup bird CLI auth")
        print("  --mine              Full mining run")
        print("  --status            Show status")

if __name__ == "__main__":
    main()
