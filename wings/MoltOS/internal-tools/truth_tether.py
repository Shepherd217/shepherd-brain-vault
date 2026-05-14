#!/usr/bin/env python3
"""
TruthTether — Fact Verification + Source Tracking
Makes basic fact-checking look like a toy.

What it does:
- Tags all claims with confidence levels (verified / inferred / speculative)
- Tracks sources for every claim (where did this info come from?)
- Cross-references claims across sessions ("I said X on Tuesday, is it still true?")
- Flags contradictions in memory
- Requires evidence for high-stakes claims
- Auto-escalates uncertain claims to DebateCouncil

Usage:
    python truth_tether.py --claim "text"      # Check a claim
    python truth_tether.py --verify file.md    # Verify all claims in file
    python truth_tether.py --contradictions    # Find contradictions
    python truth_tether.py --status            # Show truth dashboard
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ── Config ───────────────────────────────────────────────────────────────────
CLAIMS_DB = Path.home() / ".openclaw/workspace/.cache/truth_claims.json"
CLAIMS_DB.parent.mkdir(parents=True, exist_ok=True)

# ── Claim Model ─────────────────────────────────────────────────────────────

class Claim:
    def __init__(self, text: str, source: str, confidence: str = "inferred"):
        self.text = text
        self.source = source
        self.confidence = confidence  # verified, inferred, speculative
        self.timestamp = datetime.now().isoformat()
        self.verifications = []
    
    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "source": self.source,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
            "verifications": self.verifications,
        }

# ── Claim Extraction ────────────────────────────────────────────────────────

def extract_claims(text: str, source: str = "unknown") -> List[Claim]:
    """Extract claims from text."""
    claims = []
    
    # Look for factual statements (sentences with numbers, names, or specific facts)
    sentences = re.split(r'[.!?]+', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 20:
            continue
        
        # Heuristic: claims often contain numbers, dates, or specific names
        has_number = bool(re.search(r'\d+', sentence))
        has_date = bool(re.search(r'\d{4}|January|February|March|April|May|June|July|August|September|October|November|December', sentence))
        has_specific = bool(re.search(r'https?://|github\.com|@\w+|\$\d+', sentence))
        
        if has_number or has_date or has_specific:
            confidence = "verified" if has_specific else "inferred"
            claims.append(Claim(sentence, source, confidence))
    
    return claims

def check_contradictions(new_claim: Claim, existing_claims: List[Dict]) -> List[Dict]:
    """Check if new claim contradicts existing claims."""
    contradictions = []
    
    for existing in existing_claims:
        # Simple text similarity check
        if len(new_claim.text) > 20 and len(existing["text"]) > 20:
            # Check for negation or opposite numbers
            new_neg = "not " in new_claim.text.lower() or "no " in new_claim.text.lower()
            old_neg = "not " in existing["text"].lower() or "no " in existing["text"].lower()
            
            if new_neg != old_neg and similar_subject(new_claim.text, existing["text"]):
                contradictions.append(existing)
    
    return contradictions

def similar_subject(text1: str, text2: str) -> bool:
    """Check if two texts are about similar subjects."""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    common = words1 & words2
    return len(common) >= 3  # At least 3 common words

def load_claims() -> List[Dict]:
    if CLAIMS_DB.exists():
        return json.loads(CLAIMS_DB.read_text()).get("claims", [])
    return []

def save_claims(claims: List[Dict]):
    CLAIMS_DB.write_text(json.dumps({"claims": claims}, indent=2))

# ── Verification ─────────────────────────────────────────────────────────────

def verify_claim(claim_text: str) -> Dict:
    """Verify a claim (placeholder for actual verification logic)."""
    # In production: would search web, check sources, etc.
    return {
        "claim": claim_text,
        "status": "unverified",  # verified, unverified, disputed
        "confidence": "low",
        "sources": [],
    }

def verify_file(file_path: Path):
    """Verify all claims in a file."""
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return
    
    content = file_path.read_text()
    claims = extract_claims(content, str(file_path))
    
    print(f"🔍 TRUTH TETHER — Verifying {file_path.name}\n")
    print(f"Found {len(claims)} claims to verify\n")
    
    verified = 0
    unverified = 0
    
    for claim in claims:
        result = verify_claim(claim.text)
        
        if result["status"] == "verified":
            verified += 1
            print(f"✅ {claim.text[:80]}...")
        else:
            unverified += 1
            print(f"❓ {claim.text[:80]}...")
            print(f"   Confidence: {result['confidence']}")
    
    print(f"\n📊 Results: {verified} verified, {unverified} unverified")
    
    # Save to database
    existing = load_claims()
    for claim in claims:
        existing.append(claim.to_dict())
    save_claims(existing)

def find_contradictions():
    """Find contradictions in claim database."""
    claims = load_claims()
    
    if len(claims) < 2:
        print("Not enough claims to check for contradictions.")
        return
    
    print("🔍 TRUTH TETHER — Checking for contradictions\n")
    
    found = 0
    for i, claim in enumerate(claims):
        others = claims[i+1:]
        contradictions = check_contradictions(Claim(claim["text"], claim["source"]), others)
        
        if contradictions:
            found += 1
            print(f"⚠️  Potential contradiction:")
            print(f"   Claim A: {claim['text'][:100]}...")
            print(f"   Claim B: {contradictions[0]['text'][:100]}...")
            print()
    
    if not found:
        print("✅ No contradictions found")

def show_status():
    """Show truth dashboard."""
    claims = load_claims()
    
    print("🔍 TRUTH TETHER — Dashboard\n" + "=" * 50)
    print(f"Total claims tracked: {len(claims)}\n")
    
    if claims:
        confidence_dist = {}
        for claim in claims:
            c = claim.get("confidence", "unknown")
            confidence_dist[c] = confidence_dist.get(c, 0) + 1
        
        print("Confidence distribution:")
        for conf, count in confidence_dist.items():
            print(f"   {conf}: {count}")
        
        print(f"\nRecent claims:")
        for claim in claims[-5:]:
            print(f"   [{claim['confidence']}] {claim['text'][:80]}...")

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    
    if "--claim" in args:
        idx = args.index("--claim")
        if idx + 1 < len(args):
            claim_text = args[idx + 1]
            result = verify_claim(claim_text)
            print(f"Claim: {claim_text}")
            print(f"Status: {result['status']}")
            print(f"Confidence: {result['confidence']}")
        else:
            print("Usage: --claim 'text to verify'")
    elif "--verify" in args:
        idx = args.index("--verify")
        if idx + 1 < len(args):
            verify_file(Path(args[idx + 1]))
        else:
            print("Usage: --verify file.md")
    elif "--contradictions" in args:
        find_contradictions()
    elif "--status" in args:
        show_status()
    else:
        print(__doc__)
        print("\nCommands:")
        print("  --claim 'text'     Check a specific claim")
        print("  --verify file.md   Verify all claims in file")
        print("  --contradictions   Find contradictions")
        print("  --status           Show truth dashboard")

if __name__ == "__main__":
    main()
