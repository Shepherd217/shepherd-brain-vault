#!/usr/bin/env python3
"""
SkillAutoTrigger — obra's "1% Rule" Implementation

The 1% Rule: If there's even a 1% chance a skill applies to the current
context, the agent MUST invoke it.

This module scans incoming messages/context and auto-invokes relevant skills
without waiting for explicit user mention.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# ── Configuration ───────────────────────────────────────────────────────────

VAULT_PATH = Path("/root/.openclaw/workspace/vault")
SKILLS_DIR = VAULT_PATH / "rooms/skills"
TRIGGER_REGISTRY_FILE = VAULT_PATH / "wings/MoltOS/internal-tools/skill_trigger_registry.json"
AUTO_INVOKE_LOG = VAULT_PATH / "wings/MoltOS/internal-tools/logs/auto_skill_invocations.jsonl"
MIN_CONFIDENCE_THRESHOLD = 0.01  # 1% — the obra rule

# ── Trigger Patterns ────────────────────────────────────────────────────────

DEFAULT_TRIGGERS = {
    "repo-research": {
        "patterns": [
            r"repo\s+research",
            r"picasso\s+steal",
            r"dissect\s+this",
            r"analyze\s+this\s+repo",
            r"github\.com/[^/]+/[^/]+",
            r"what\s+is\s+\w+/\w+",
            r"trending\s+repo",
            r"agent\s+framework",
        ],
        "keywords": ["repo", "github", "steal", "dissect", "analyze", "trending"],
        "context_signals": ["code", "repository", "star", "fork", "commit"],
        "confidence_boost": 0.15,
    },
    "feishu-calendar": {
        "patterns": [
            r"schedule\s+a?\s*meeting",
            r"book\s+a?\s*call",
            r"calendar\s+event",
            r"set\s+up\s+a?\s*meeting",
            r"when\s+are\s+you\s+free",
            r"busy\s+on\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)",
            r"calendar\s+check",
            r"schedule\s+for",
            r"meet\s+(tomorrow|next\s+week|today|monday|tuesday|wednesday|thursday|friday)",
        ],
        "keywords": ["schedule", "calendar", "meeting", "book", "free", "busy", "appointment"],
        "context_signals": ["time", "date", "week", "tomorrow", "today", "next"],
        "confidence_boost": 0.20,
    },
    "feishu-task": {
        "patterns": [
            r"create\s+a?\s*task",
            r"add\s+to\s+(my\s+)?todo",
            r"remind\s+me\s+to",
            r"set\s+a?\s*reminder",
            r"task\s+list",
            r"what\s+are\s+my\s+tasks",
            r"to-do\s+list",
            r"mark\s+.*\s+done",
        ],
        "keywords": ["task", "todo", "remind", "reminder", "deadline", "due", "assign"],
        "context_signals": ["follow", "up", "later", "soon", "need", "should"],
        "confidence_boost": 0.18,
    },
    "weather": {
        "patterns": [
            r"weather\s+in\s+(.+)",
            r"forecast\s+for\s+(.+)",
            r"temperature\s+in\s+(.+)",
            r"is\s+it\s+(raining|snowing|sunny|hot|cold)",
            r"will\s+it\s+rain",
            r"weather\s+today",
            r"weather\s+tomorrow",
        ],
        "keywords": ["weather", "forecast", "temperature", "rain", "snow", "sunny", "climate"],
        "context_signals": ["outside", "travel", "trip", "going", "visiting"],
        "confidence_boost": 0.25,
    },
    "copywriting": {
        "patterns": [
            r"write\s+(copy|ad\s+copy|headline|tagline)",
            r"marketing\s+copy",
            r"landing\s+page\s+copy",
            r"hero\s+section",
            r"value\s+proposition",
            r"cta\s+(copy|text)",
            r"email\s+sequence",
            r"sales\s+page",
        ],
        "keywords": ["copy", "marketing", "headline", "tagline", "landing", "hero", "cta", "sales"],
        "context_signals": ["convert", "persuade", "sell", "promote", "launch"],
        "confidence_boost": 0.15,
    },
    "pricing-strategy": {
        "patterns": [
            r"pricing\s+(model|strategy|page|tier)",
            r"how\s+much\s+should\s+I\s+charge",
            r"freemium\s+model",
            r"subscription\s+pricing",
            r"price\s+increase",
            r"value\s+metric",
            r"per\s+seat\s+pricing",
            r"usage\s+based\s+pricing",
        ],
        "keywords": ["pricing", "price", "cost", "subscription", "freemium", "tier", "plan"],
        "context_signals": ["revenue", "money", "charge", "pay", "customer", "user"],
        "confidence_boost": 0.15,
    },
    "standout-local": {
        "patterns": [
            r"audit\s+(this\s+)?site",
            r"lead\s+(score|research|gen)",
            r"cleaning\s+company",
            r"local\s+business",
            r"website\s+audit",
            r"outreach\s+email",
            r"demo\s+page",
            r"competitor\s+(analysis|research)",
        ],
        "keywords": ["audit", "lead", "local", "business", "cleaning", "outreach", "demo"],
        "context_signals": ["website", "conversion", "seo", "mobile", "score"],
        "confidence_boost": 0.20,
    },
    "churn-prevention": {
        "patterns": [
            r"cancel\s+flow",
            r"churn\s+reduction",
            r"save\s+offer",
            r"exit\s+survey",
            r"dunning\s+email",
            r"payment\s+recovery",
            r"win-back",
            r"failed\s+payment",
        ],
        "keywords": ["churn", "cancel", "retention", "dunning", "recovery", "exit", "save"],
        "context_signals": ["subscription", "customer", "leave", "quit", "stop"],
        "confidence_boost": 0.15,
    },
    "campaign-plan": {
        "patterns": [
            r"campaign\s+(plan|brief|strategy)",
            r"product\s+launch",
            r"go\s+to\s+market",
            r"content\s+calendar",
            r"marketing\s+campaign",
            r"launch\s+plan",
            r"lead\s+gen\s+campaign",
        ],
        "keywords": ["campaign", "launch", "marketing", "content", "calendar", "strategy"],
        "context_signals": ["plan", "schedule", "week", "month", "timeline"],
        "confidence_boost": 0.15,
    },
    "seo-audit": {
        "patterns": [
            r"seo\s+(audit|check|review)",
            r"why\s+am\s+I\s+not\s+ranking",
            r"traffic\s+dropped",
            r"lost\s+rankings",
            r"meta\s+tags",
            r"core\s+web\s+vitals",
            r"crawl\s+errors",
            r"indexing\s+issues",
        ],
        "keywords": ["seo", "ranking", "traffic", "google", "search", "index", "crawl"],
        "context_signals": ["website", "page", "site", "url", "domain"],
        "confidence_boost": 0.18,
    },
    "github": {
        "patterns": [
            r"check\s+(the\s+)?pr\s*#?\d*",
            r"pull\s+request\s*#?\d*",
            r"issue\s*#?\d+",
            r"github\s+(issue|pr|pull)",
            r"ci\s+(run|status|failed)",
            r"merge\s+(conflict|request)",
            r"code\s+review",
        ],
        "keywords": ["github", "pr", "pull", "issue", "ci", "merge", "review", "commit"],
        "context_signals": ["repo", "branch", "main", "master", "feature"],
        "confidence_boost": 0.18,
    },
    "process-doc": {
        "patterns": [
            r"document\s+(this\s+)?process",
            r"write\s+an\s+sop",
            r"standard\s+operating\s+procedure",
            r"raci\s+matrix",
            r"flowchart",
            r"business\s+process",
            r"handoff\s+doc",
        ],
        "keywords": ["process", "sop", "procedure", "flowchart", "raci", "handoff", "document"],
        "context_signals": ["team", "workflow", "step", "stage", "phase"],
        "confidence_boost": 0.12,
    },
}

# ── Core Engine ───────────────────────────────────────────────────────────────

class SkillAutoTrigger:
    """Analyzes messages and auto-invokes skills based on the 1% rule."""

    def __init__(self):
        self.registry = self._load_registry()
        self.invocation_log = []

    def _load_registry(self) -> Dict:
        """Load trigger registry from disk or use defaults."""
        if TRIGGER_REGISTRY_FILE.exists():
            with open(TRIGGER_REGISTRY_FILE) as f:
                return json.load(f)
        return DEFAULT_TRIGGERS

    def _save_registry(self):
        """Persist registry to disk."""
        TRIGGER_REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(TRIGGER_REGISTRY_FILE, 'w') as f:
            json.dump(self.registry, f, indent=2)

    def analyze(self, message: str, context: Optional[Dict] = None) -> List[Tuple[str, float]]:
        """
        Analyze a message and return list of (skill_id, confidence) tuples.
        Only returns skills with confidence >= MIN_CONFIDENCE_THRESHOLD.
        """
        message_lower = message.lower()
        matches = []

        for skill_id, trigger in self.registry.items():
            confidence = self._calculate_confidence(message, message_lower, trigger, context)
            if confidence >= MIN_CONFIDENCE_THRESHOLD:
                matches.append((skill_id, confidence))

        # Sort by confidence descending
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches

    def _calculate_confidence(
        self, message: str, message_lower: str, trigger: Dict, context: Optional[Dict]
    ) -> float:
        """Calculate confidence score (0.0-1.0) that this skill applies."""
        scores = []

        # Pattern matching (regex)
        pattern_hits = 0
        for pattern in trigger.get("patterns", []):
            if re.search(pattern, message, re.IGNORECASE):
                pattern_hits += 1
        if pattern_hits > 0:
            scores.append(min(0.3 + (pattern_hits * 0.1), 0.8))

        # Keyword matching
        keyword_hits = sum(1 for kw in trigger.get("keywords", []) if kw in message_lower)
        if keyword_hits > 0:
            scores.append(min(0.2 + (keyword_hits * 0.08), 0.6))

        # Context signal matching
        if context:
            context_text = json.dumps(context).lower()
            signal_hits = sum(
                1 for sig in trigger.get("context_signals", []) if sig in context_text
            )
            if signal_hits > 0:
                scores.append(min(0.1 + (signal_hits * 0.05), 0.3))

        if not scores:
            return 0.0

        # Combine scores with confidence boost
        base_confidence = max(scores)
        boost = trigger.get("confidence_boost", 0.0)
        return min(base_confidence + boost, 1.0)

    def should_auto_invoke(self, skill_id: str, confidence: float) -> bool:
        """Check if a skill should be auto-invoked based on confidence."""
        return confidence >= MIN_CONFIDENCE_THRESHOLD

    def log_invocation(self, skill_id: str, confidence: float, message_preview: str, triggered: bool):
        """Log an invocation attempt."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "skill_id": skill_id,
            "confidence": confidence,
            "message_preview": message_preview[:200],
            "triggered": triggered,
        }
        self.invocation_log.append(entry)

        # Persist to disk
        AUTO_INVOKE_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(AUTO_INVOKE_LOG, 'a') as f:
            f.write(json.dumps(entry) + '\n')

    def get_stats(self) -> Dict:
        """Get auto-invocation statistics."""
        total = len(self.invocation_log)
        triggered = sum(1 for e in self.invocation_log if e["triggered"])
        by_skill = {}
        for e in self.invocation_log:
            sid = e["skill_id"]
            by_skill[sid] = by_skill.get(sid, {"total": 0, "triggered": 0})
            by_skill[sid]["total"] += 1
            if e["triggered"]:
                by_skill[sid]["triggered"] += 1

        return {
            "total_analyzed": total,
            "total_triggered": triggered,
            "trigger_rate": triggered / total if total > 0 else 0,
            "by_skill": by_skill,
        }

    def add_trigger(self, skill_id: str, patterns: List[str], keywords: List[str],
                    context_signals: List[str], confidence_boost: float = 0.1):
        """Add a new skill trigger to the registry."""
        self.registry[skill_id] = {
            "patterns": patterns,
            "keywords": keywords,
            "context_signals": context_signals,
            "confidence_boost": confidence_boost,
        }
        self._save_registry()


def main():
    """CLI for testing the auto-trigger engine."""
    import sys

    engine = SkillAutoTrigger()

    if len(sys.argv) < 2:
        print("Usage: skill_auto_trigger.py '<message>'")
        print("\nRegistered skills:")
        for sid in engine.registry:
            print(f"  • {sid}")
        print(f"\nThreshold: {MIN_CONFIDENCE_THRESHOLD*100:.0f}%")
        return

    message = sys.argv[1]
    matches = engine.analyze(message)

    print(f"Message: {message[:100]}...")
    print(f"\nMatches (threshold: {MIN_CONFIDENCE_THRESHOLD*100:.0f}%):")

    if not matches:
        print("  No skills triggered.")
        return

    for skill_id, confidence in matches:
        triggered = engine.should_auto_invoke(skill_id, confidence)
        status = "🔥 AUTO-INVOKE" if triggered else "ℹ️  low confidence"
        print(f"  {status} {skill_id}: {confidence*100:.1f}%")
        engine.log_invocation(skill_id, confidence, message, triggered)

    stats = engine.get_stats()
    print(f"\nStats: {stats['total_triggered']}/{stats['total_analyzed']} triggered")


if __name__ == "__main__":
    main()
