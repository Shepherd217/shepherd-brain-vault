#!/usr/bin/env python3
"""
OpenClaw Skill Auto-Trigger Integration Module

This module integrates the auto-trigger engine into the agent's
message processing pipeline. Call analyze_message() on every
incoming message to get skill recommendations.
"""

import json
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional

VAULT_PATH = Path("/root/.openclaw/workspace/vault")
TRIGGER_SCRIPT = VAULT_PATH / "wings/MoltOS/internal-tools/skill_auto_trigger.py"

def analyze_message(message: str) -> List[Tuple[str, float]]:
    """
    Analyze an incoming message and return recommended skills.
    
    Returns list of (skill_id, confidence) tuples, sorted by confidence.
    Only returns skills with confidence >= 0.01 (1% rule).
    """
    if not TRIGGER_SCRIPT.exists():
        return []
    
    try:
        result = subprocess.run(
            ["python3", str(TRIGGER_SCRIPT), message],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # Parse output for matches
        matches = []
        for line in result.stdout.split('\n'):
            line = line.strip()
            if 'AUTO-INVOKE' in line or 'low confidence' in line:
                if 'AUTO-INVOKE' in line:
                    prefix = 'AUTO-INVOKE'
                else:
                    prefix = 'low confidence'
                idx = line.find(prefix)
                if idx >= 0:
                    rest = line[idx + len(prefix):].strip()
                    parts = rest.split(':')
                    if len(parts) >= 2:
                        skill_id = parts[0].strip()
                        conf_str = parts[1].replace('%', '').strip()
                        try:
                            confidence = float(conf_str) / 100
                            if skill_id and skill_id != 'AUTO-INVOKE' and skill_id != 'low':
                                matches.append((skill_id, confidence))
                        except ValueError:
                            pass
        
        return matches
        
    except Exception:
        return []

def format_suggestion(skill_id: str, confidence: float, message: str) -> str:
    """Format a skill suggestion for display."""
    conf_pct = confidence * 100
    if conf_pct >= 50:
        return f"🔥 **{skill_id}** ({conf_pct:.0f}%) — Strong match for this request"
    elif conf_pct >= 20:
        return f"⚡ **{skill_id}** ({conf_pct:.0f}%) — Likely relevant"
    else:
        return f"ℹ️  **{skill_id}** ({conf_pct:.0f}%) — Possible match"

def get_suggestions_text(message: str, top_n: int = 3) -> Optional[str]:
    """
    Get formatted suggestion text for the thinking block.
    Returns None if no relevant skills detected.
    """
    matches = analyze_message(message)
    
    if not matches:
        return None
    
    # Filter to meaningful matches
    meaningful = [(s, c) for s, c in matches if c >= 0.10]  # 10% threshold for suggestions
    
    if not meaningful:
        return None
    
    lines = ["[Auto-Trigger Analysis]"]
    for skill_id, conf in meaningful[:top_n]:
        lines.append(format_suggestion(skill_id, conf, message))
    
    if len(meaningful) > top_n:
        lines.append(f"... and {len(meaningful) - top_n} more")
    
    lines.append("\nWant me to invoke any of these?")
    return "\n".join(lines)


# ── Simple Test ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        # Run test cases
        test_messages = [
            "schedule a meeting with the team for tomorrow afternoon",
            "write copy for a landing page about AI agents",
            "what's the weather like in Chicago?",
            "audit this cleaning company website",
            "just saying hi",
        ]
        
        for msg in test_messages:
            print(f"\nMessage: '{msg}'")
            print("-" * 50)
            suggestion = get_suggestions_text(msg)
            if suggestion:
                print(suggestion)
            else:
                print("(no skills triggered)")
        
    else:
        msg = sys.argv[1]
        suggestion = get_suggestions_text(msg)
        if suggestion:
            print(suggestion)
        else:
            print("(no skills triggered)")
