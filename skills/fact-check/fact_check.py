#!/usr/bin/env python3
"""
Fact-Check Pipeline — Extract and validate claims from notes.

Usage:
    from fact_check import fact_check_note
    result = fact_check_note(draft_text)
"""

import re
import json
import requests
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse


@dataclass
class Claim:
    text: str
    claim_type: str  # date, url, version, model, stat, generic
    confidence: float = 0.0
    verified: Optional[bool] = None
    correction: Optional[str] = None
    source: Optional[str] = None
    flag_reason: Optional[str] = None


@dataclass
class FactCheckResult:
    original: str
    corrected_note: str
    claims: List[Claim]
    corrections: List[Dict]
    flags: List[Dict]
    summary: str


# ─── Claim Extractors ──────────────────────────────────────────────

DATE_PATTERNS = [
    # ISO dates, month-year, relative dates
    r'\b(\d{4}-\d{2}-\d{2}|\w+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4})\b',
]

VERSION_PATTERNS = [
    r'\b(v\d+\.\d+(?:\.\d+)?|version \d+\.\d+)\b',
    r'\b(\d+\.\d+\.\d+(?:-[\w.]+)?)\b',  # semver-like
]

URL_PATTERN = r'https?://[^\s<>"\']+'

MODEL_PATTERNS = [
    # Common model name patterns
    r'\b(llama[- ]?\d+(?:\.\d+)?[- ]?\d+b?|gpt-?\d|claude-?\d|gemini-?\w+)\b',
    r'\b([\w-]+-\d+b)(?:-instruct|-chat|-base)?\b',
]

STAT_PATTERNS = [
    # Numbers with units: 405B parameters, 70% accuracy, 1.2M downloads
    r'\b(\d+(?:\.\d+)?\s*[KMGT]?\s*(?:parameters?|params?|tokens?|downloads?|users?|accuracy|score))\b',
    r'\b(\d+(?:\.\d+)?%|\d+\s*percent)\b',
]


def extract_claims(text: str) -> List[Claim]:
    """Extract all verifiable claims from a note."""
    claims = []
    seen = set()
    
    # Extract dates
    for pattern in DATE_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            claim_text = match.group(1)
            if claim_text not in seen:
                seen.add(claim_text)
                claims.append(Claim(text=claim_text, claim_type="date"))
    
    # Extract versions
    for pattern in VERSION_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            claim_text = match.group(1)
            if claim_text not in seen:
                seen.add(claim_text)
                claims.append(Claim(text=claim_text, claim_type="version"))
    
    # Extract URLs
    for match in re.finditer(URL_PATTERN, text):
        claim_text = match.group(0)
        if claim_text not in seen:
            seen.add(claim_text)
            claims.append(Claim(text=claim_text, claim_type="url"))
    
    # Extract model references
    for pattern in MODEL_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            claim_text = match.group(1)
            if claim_text not in seen:
                seen.add(claim_text)
                claims.append(Claim(text=claim_text, claim_type="model"))
    
    # Extract statistics
    for pattern in STAT_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            claim_text = match.group(1)
            if claim_text not in seen:
                seen.add(claim_text)
                claims.append(Claim(text=claim_text, claim_type="stat"))
    
    return claims


# ─── Validators ────────────────────────────────────────────────────

def validate_url(url: str, timeout: int = 5) -> Tuple[bool, Optional[str]]:
    """Check if URL is reachable. Returns (ok, error_or_redirect)."""
    try:
        resp = requests.head(url, timeout=timeout, allow_redirects=True)
        if resp.status_code == 200:
            return True, None
        elif resp.status_code in (301, 302, 307, 308):
            return True, f"Redirects to {resp.headers.get('Location', 'unknown')}"
        elif resp.status_code == 404:
            return False, "Page not found (404)"
        elif resp.status_code >= 500:
            return False, f"Server error ({resp.status_code})"
        else:
            return False, f"HTTP {resp.status_code}"
    except requests.exceptions.Timeout:
        return False, "Request timed out"
    except requests.exceptions.ConnectionError:
        return False, "Connection failed"
    except Exception as e:
        return False, str(e)


def validate_huggingface_model(model_name: str) -> Tuple[bool, Optional[Dict]]:
    """Check if model exists on HuggingFace."""
    try:
        # Clean up model name
        clean_name = model_name.lower().replace(" ", "-").replace("_", "-")
        
        # Try common prefixes
        prefixes = ["", "meta-llama/", "microsoft/", "google/", "openai/", "anthropic/"]
        
        for prefix in prefixes:
            api_url = f"https://huggingface.co/api/models/{prefix}{clean_name}"
            try:
                resp = requests.get(api_url, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    return True, {
                        "exists": True,
                        "id": data.get("id", prefix + clean_name),
                        "downloads": data.get("downloads", 0),
                        "likes": data.get("likes", 0),
                        "url": f"https://huggingface.co/{prefix}{clean_name}",
                    }
            except:
                continue
        
        # Try search
        search_url = f"https://huggingface.co/api/models?search={clean_name}"
        resp = requests.get(search_url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data and len(data) > 0:
                first = data[0]
                return True, {
                    "exists": True,
                    "id": first.get("id"),
                    "url": f"https://huggingface.co/{first.get('id')}",
                    "note": "Found via search — verify exact match",
                }
        
        return False, {"exists": False, "note": "Model not found on HuggingFace"}
    except Exception as e:
        return False, {"exists": False, "error": str(e)}


def validate_github_repo(repo_url: str) -> Tuple[bool, Optional[Dict]]:
    """Validate GitHub repo URL and get latest info."""
    try:
        parsed = urlparse(repo_url)
        if parsed.netloc != "github.com":
            return False, {"note": "Not a github.com URL"}
        
        parts = parsed.path.strip("/").split("/")
        if len(parts) < 2:
            return False, {"note": "Invalid repo path"}
        
        owner, repo = parts[0], parts[1]
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        
        resp = requests.get(api_url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return True, {
                "exists": True,
                "stars": data.get("stargazers_count", 0),
                "updated": data.get("updated_at"),
                "default_branch": data.get("default_branch"),
                "url": f"https://github.com/{owner}/{repo}",
            }
        elif resp.status_code == 404:
            return False, {"exists": False, "note": "Repository not found"}
        else:
            return False, {"exists": False, "note": f"GitHub API returned {resp.status_code}"}
    except Exception as e:
        return False, {"error": str(e)}


def validate_date(date_str: str) -> Tuple[bool, Optional[str]]:
    """Basic date validation and formatting check."""
    # Try to parse common formats
    import datetime
    
    formats = [
        "%Y-%m-%d",
        "%B %d, %Y",
        "%B %d %Y",
        "%b %d, %Y",
        "%b %d %Y",
        "%m/%d/%Y",
        "%m/%d/%y",
    ]
    
    for fmt in formats:
        try:
            dt = datetime.datetime.strptime(date_str, fmt)
            # Check if date is in the future (suspicious)
            if dt > datetime.datetime.now() + datetime.timedelta(days=30):
                return False, f"Date is in the future ({date_str})"
            # Check if date is too old (before 2020, suspicious for tech)
            if dt.year < 2020:
                return False, f"Date is very old ({date_str}) — verify for tech context"
            return True, None
        except ValueError:
            continue
    
    return False, f"Could not parse date format: {date_str}"


def validate_version(version_str: str, context: str = "") -> Tuple[bool, Optional[str]]:
    """Validate version string against known patterns."""
    # Check if it's a reasonable semver
    semver_pattern = r'^[vV]?(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:-([\w.]+))?$'
    match = re.match(semver_pattern, version_str)
    
    if not match:
        return False, f"Version '{version_str}' doesn't match semver format"
    
    major = int(match.group(1))
    
    # Sanity checks
    if major > 100:
        return False, f"Version major number very high ({major}) — verify"
    
    # If we have context about what this version refers to, we could do more
    # For now, basic format validation
    return True, None


# ─── Main Pipeline ─────────────────────────────────────────────────

def fact_check_note(text: str, auto_correct: bool = True) -> FactCheckResult:
    """
    Main entry point: extract claims, validate, correct/flag.
    
    Args:
        text: Draft note to check
        auto_correct: Whether to auto-fix high-confidence errors
    
    Returns:
        FactCheckResult with corrected note and flags
    """
    claims = extract_claims(text)
    corrections = []
    flags = []
    corrected = text
    
    for claim in claims:
        ok = False
        info = None
        
        if claim.claim_type == "url":
            ok, info = validate_url(claim.text)
            if not ok:
                flags.append({
                    "claim": claim.text,
                    "type": "url",
                    "issue": info or "URL unreachable",
                    "action": "verify_link",
                })
        
        elif claim.claim_type == "model":
            ok, info = validate_huggingface_model(claim.text)
            if ok and info:
                if info.get("note") and "verify exact match" in info.get("note", ""):
                    # Found via search, not exact
                    flags.append({
                        "claim": claim.text,
                        "type": "model",
                        "issue": f"Model found but not exact match: {info.get('id')}",
                        "action": "verify_model_name",
                    })
                else:
                    claim.verified = True
                    claim.source = info.get("url")
            else:
                flags.append({
                    "claim": claim.text,
                    "type": "model",
                    "issue": info.get("note", "Model not found") if isinstance(info, dict) else str(info),
                    "action": "verify_model_name",
                })
        
        elif claim.claim_type == "date":
            ok, info = validate_date(claim.text)
            if not ok:
                flags.append({
                    "claim": claim.text,
                    "type": "date",
                    "issue": info,
                    "action": "verify_date",
                })
            else:
                claim.verified = True
        
        elif claim.claim_type == "version":
            ok, info = validate_version(claim.text)
            if not ok:
                flags.append({
                    "claim": claim.text,
                    "type": "version",
                    "issue": info,
                    "action": "verify_version",
                })
            else:
                claim.verified = True
        
        elif claim.claim_type == "stat":
            # Stats are hard to verify without context — flag for review
            flags.append({
                "claim": claim.text,
                "type": "stat",
                "issue": "Statistic needs source verification",
                "action": "add_citation",
            })
    
    # Build corrected note
    corrected = text
    for flag in flags:
        claim_text = flag["claim"]
        # Add inline flag marker
        marker = f" [⚠️ {flag['action']}: {flag['issue']}]"
        corrected = corrected.replace(claim_text, claim_text + marker)
    
    # Build summary
    total = len(claims)
    verified = sum(1 for c in claims if c.verified)
    flagged = len(flags)
    
    summary = f"Fact-check complete: {verified}/{total} claims verified, {flagged} flagged for review."
    
    return FactCheckResult(
        original=text,
        corrected_note=corrected,
        claims=claims,
        corrections=corrections,
        flags=flags,
        summary=summary,
    )


# ─── JSON Serialization ────────────────────────────────────────────

def result_to_dict(result: FactCheckResult) -> Dict:
    """Convert result to JSON-serializable dict."""
    return {
        "original": result.original,
        "corrected_note": result.corrected_note,
        "claims": [
            {
                "text": c.text,
                "type": c.claim_type,
                "verified": c.verified,
                "source": c.source,
            }
            for c in result.claims
        ],
        "flags": result.flags,
        "summary": result.summary,
    }


# ─── CLI Entry Point ─────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python fact_check.py <note_file>")
        print("   or: echo 'note text' | python fact_check.py -")
        sys.exit(1)
    
    if sys.argv[1] == "-":
        text = sys.stdin.read()
    else:
        with open(sys.argv[1], "r") as f:
            text = f.read()
    
    result = fact_check_note(text)
    print(json.dumps(result_to_dict(result), indent=2))
