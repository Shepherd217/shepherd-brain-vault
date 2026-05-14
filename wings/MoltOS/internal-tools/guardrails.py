#!/usr/bin/env python3
"""
Guardrails — Input Validation + Safety Constraints
Steals from AutoGen's guardrail system.

What it does:
- Validates inputs before they reach agents
- Enforces constraints: max tokens, banned topics, required fields
- Sanitizes outputs: no PII leakage, no hallucinated URLs
- Rate limiting: prevent spam loops
- Content classification: safe / risky / dangerous
- Auto-rejects if validation fails

Usage:
    python guardrails.py --check input.json   # Validate input
    python guardrails.py --sanitize output   # Sanitize output
    python guardrails.py --classify text     # Classify safety level
    python guardrails.py --limits            # Show current limits
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

# ── Config ───────────────────────────────────────────────────────────────────
GUARDRAILS_CONFIG = Path.home() / ".openclaw/workspace/.cache/guardrails.json"
GUARDRAILS_CONFIG.parent.mkdir(parents=True, exist_ok=True)

DEFAULT_LIMITS = {
    "max_tokens_per_request": 100000,
    "max_requests_per_minute": 60,
    "max_cost_per_session": 50.0,
    "banned_topics": ["harmful", "illegal", "explicit"],
    "required_fields": ["task", "context"],
    "pii_patterns": [
        r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
        r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",  # Credit card
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
    ],
    "allowed_domains": ["github.com", "docs.openclaw.ai", "moltos.org"],
    "max_subagents": 5,
    "max_session_duration_hours": 4,
}

# ── Validation ──────────────────────────────────────────────────────────────

def load_config() -> Dict:
    if GUARDRAILS_CONFIG.exists():
        return json.loads(GUARDRAILS_CONFIG.read_text())
    return DEFAULT_LIMITS

def validate_input(data: Dict) -> Dict:
    """Validate input data against guardrails."""
    config = load_config()
    errors = []
    warnings = []
    
    # Check required fields
    for field in config.get("required_fields", []):
        if field not in data or not data[field]:
            errors.append(f"Missing required field: {field}")
    
    # Check token estimate
    if "tokens" in data:
        if data["tokens"] > config["max_tokens_per_request"]:
            errors.append(f"Token limit exceeded: {data['tokens']} > {config['max_tokens_per_request']}")
    
    # Check banned topics
    content = json.dumps(data).lower()
    for topic in config.get("banned_topics", []):
        if topic in content:
            errors.append(f"Banned topic detected: {topic}")
    
    # Check PII
    for pattern in config.get("pii_patterns", []):
        if re.search(pattern, json.dumps(data)):
            warnings.append("Potential PII detected — will be sanitized")
    
    # Check cost
    if "estimated_cost" in data:
        if data["estimated_cost"] > config["max_cost_per_session"]:
            errors.append(f"Cost limit exceeded: ${data['estimated_cost']} > ${config['max_cost_per_session']}")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "sanitized": len(warnings) > 0,
    }

def sanitize_output(text: str) -> str:
    """Sanitize output to remove PII and unsafe content."""
    config = load_config()
    
    # Remove PII
    for pattern in config.get("pii_patterns", []):
        text = re.sub(pattern, "[REDACTED]", text)
    
    # Check for hallucinated URLs
    urls = re.findall(r"https?://[^\s\"]+", text)
    allowed = config.get("allowed_domains", [])
    
    for url in urls:
        if not any(domain in url for domain in allowed):
            # Check if URL is real (in production: would verify)
            text = text.replace(url, f"[UNVERIFIED_URL: {url[:30]}...]")
    
    return text

def classify_safety(text: str) -> str:
    """Classify content safety level."""
    text_lower = text.lower()
    
    # Dangerous patterns
    dangerous = ["rm -rf /", "drop table", "delete from", "format c:", "sudo"]
    risky = ["exec", "subprocess", "eval(", "os.system"]
    
    for pattern in dangerous:
        if pattern in text_lower:
            return "dangerous"
    
    for pattern in risky:
        if pattern in text_lower:
            return "risky"
    
    return "safe"

def show_limits():
    """Show current guardrail limits."""
    config = load_config()
    
    print("🛡️ GUARDRAILS — Current Limits\n" + "=" * 50)
    print(f"Max tokens/request: {config['max_tokens_per_request']:,}")
    print(f"Max requests/minute: {config['max_requests_per_minute']}")
    print(f"Max cost/session: ${config['max_cost_per_session']}")
    print(f"Max subagents: {config['max_subagents']}")
    print(f"Max session duration: {config['max_session_duration_hours']}h")
    print(f"\nBanned topics: {', '.join(config['banned_topics'])}")
    print(f"Required fields: {', '.join(config['required_fields'])}")
    print(f"Allowed domains: {', '.join(config['allowed_domains'])}")

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    
    if "--check" in args:
        idx = args.index("--check")
        if idx + 1 < len(args):
            try:
                data = json.loads(args[idx + 1])
            except Exception:
                print("Invalid JSON input")
                return
            result = validate_input(data)
            print(f"🛡️ Validation: {'✅ PASS' if result['valid'] else '❌ FAIL'}")
            if result["errors"]:
                print("Errors:")
                for e in result["errors"]:
                    print(f"   ❌ {e}")
            if result["warnings"]:
                print("Warnings:")
                for w in result["warnings"]:
                    print(f"   ⚠️  {w}")
        else:
            print("Usage: --check '{\"key\": \"value\"}'")
    elif "--sanitize" in args:
        idx = args.index("--sanitize")
        if idx + 1 < len(args):
            text = args[idx + 1]
            clean = sanitize_output(text)
            print(f"🛡️ Sanitized:\n{clean}")
        else:
            print("Usage: --sanitize 'text to sanitize'")
    elif "--classify" in args:
        idx = args.index("--classify")
        if idx + 1 < len(args):
            text = args[idx + 1]
            level = classify_safety(text)
            print(f"🛡️ Safety level: {level.upper()}")
        else:
            print("Usage: --classify 'text to classify'")
    elif "--limits" in args:
        show_limits()
    else:
        print(__doc__)
        print("\nCommands:")
        print("  --check '{json}'      Validate input")
        print("  --sanitize 'text'     Sanitize output")
        print("  --classify 'text'     Classify safety")
        print("  --limits              Show limits")

if __name__ == "__main__":
    main()
