#!/usr/bin/env python3
"""
Website Comparison Tool
Pattern: Before/After Comparison (from Standout Local workflow)
Source: Generate side-by-side comparison of current site vs proposed demo

Creates comparison report showing:
- Current state (scraped from live site)
- Proposed state (based on pain points + demo concept)
- Side-by-side markdown for outreach

Usage: python comparison-tool.py <lead-file.md> [--output-dir outreach/]
"""

import re
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class WebsiteComparisonTool:
    """Generates before/after comparison for lead outreach."""
    
    def __init__(self, vault_path: str = None, verbose: bool = True):
        self.vault_path = Path(vault_path or '/root/.openclaw/workspace/vault')
        self.verbose = verbose
        self.results = {}
    
    def _log(self, msg: str):
        if self.verbose:
            print(msg)
    
    def compare(self, lead_file: str, output_dir: str = None) -> Optional[str]:
        """Generate comparison for a lead."""
        lead_path = Path(lead_file)
        
        if not lead_path.exists():
            self._log(f"❌ Lead file not found: {lead_file}")
            return None
        
        self._log(f"\n{'='*60}")
        self._log(f"WEBSITE COMPARISON: {lead_path.stem}")
        self._log(f"{'='*60}")
        
        # Parse lead
        lead_data = self._parse_lead(lead_path)
        if not lead_data:
            return None
        
        # Extract current state from lead file
        current = self._extract_current_state(lead_data)
        
        # Generate proposed state
        proposed = self._generate_proposed_state(lead_data, current)
        
        # Create comparison report
        comparison = self._create_comparison(lead_data, current, proposed)
        
        # Save
        if not output_dir:
            output_dir = self.vault_path / 'wings/StandoutLocal/comparisons'
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{lead_path.stem}-comparison.md"
        output_path = output_dir / filename
        output_path.write_text(comparison)
        
        self._log(f"\n💾 Comparison saved to: {output_path}")
        self._log(f"\n{'='*60}")
        self._log(f"COMPARISON COMPLETE")
        self._log(f"Current Score: {current['score']}/100")
        self._log(f"Proposed Score: {proposed['score']}/100")
        self._log(f"Improvement: +{proposed['score'] - current['score']} points")
        self._log(f"{'='*60}")
        
        return str(output_path)
    
    def _parse_lead(self, lead_path: Path) -> Optional[Dict]:
        """Parse lead file frontmatter and body."""
        content = lead_path.read_text()
        
        pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
        match = re.match(pattern, content, re.DOTALL)
        
        if not match:
            self._log("❌ No frontmatter found")
            return None
        
        try:
            fm = yaml.safe_load(match.group(1))
            body = match.group(2)
        except Exception as e:
            self._log(f"❌ Failed to parse frontmatter: {e}")
            return None
        
        return {
            'name': fm.get('name', lead_path.stem.replace('-', ' ').title()),
            'website': fm.get('website', ''),
            'score': fm.get('score', 0),
            'pain': fm.get('pain', 0),
            'opportunity': fm.get('opportunity', 0),
            'reach': fm.get('reach', 0),
            'fit': fm.get('fit', 0),
            'status': fm.get('status', 'discovered'),
            'frontmatter': fm,
            'body': body
        }
    
    def _extract_current_state(self, lead_data: Dict) -> Dict:
        """Extract current website state from lead file."""
        body = lead_data['body']
        
        # Try to extract audit data from body
        current = {
            'score': lead_data.get('score', 0),
            'has_mobile': self._check_in_body(body, ['mobile', 'responsive']),
            'has_cta': self._check_in_body(body, ['cta', 'call to action', 'book now', 'get quote']),
            'has_trust': self._check_in_body(body, ['trust', 'review', 'testimonial', 'google']),
            'has_social': self._check_in_body(body, ['social', 'facebook', 'instagram']),
            'has_pricing': self._check_in_body(body, ['pricing', 'price', 'cost', 'rate']),
            'has_booking': self._check_in_body(body, ['book', 'schedule', 'appointment']),
            'load_speed': self._extract_speed(body),
            'pain_points': self._extract_pain_points(body)
        }
        
        # If score is 0, estimate from pain points
        if current['score'] == 0 and current['pain_points']:
            current['score'] = max(0, 100 - (len(current['pain_points']) * 12))
        
        return current
    
    def _check_in_body(self, body: str, keywords: List[str]) -> bool:
        """Check if feature exists positively in body (not mentioned as missing)."""
        body_lower = body.lower()
        
        for kw in keywords:
            kw_lower = kw.lower()
            # Find all mentions of this keyword
            for match in re.finditer(r'[^.\n]*?' + re.escape(kw_lower) + r'[^.\n]*', body_lower):
                context = match.group(0)
                # Check if context indicates it's MISSING (not present)
                negative_indicators = ['no ', 'missing ', 'lacks ', 'not ', 'without ', 'none', 'zero']
                if not any(ind in context for ind in negative_indicators):
                    return True
        
        return False
    
    def _extract_speed(self, body: str) -> str:
        """Extract speed mention from body."""
        match = re.search(r'(\d+(?:\.\d+)?)\s*s\b', body, re.IGNORECASE)
        return f"{match.group(1)}s" if match else "Unknown"
    
    def _extract_pain_points(self, body: str) -> List[str]:
        """Extract pain points from body."""
        points = []
        
        # Look for numbered list under Pain Points section
        pain_section = re.search(
            r'## Pain Points Found.*?(?:\n\d+\.\s+(.+?))+(?:\n## |\Z)',
            body, re.DOTALL
        )
        
        if pain_section:
            # Extract all numbered items
            for match in re.finditer(r'\n\d+\.\s+(.+)', body):
                point = match.group(1).strip()
                if point and len(point) > 10:
                    points.append(point)
        
        # Also look for bullet points
        if not points:
            for match in re.finditer(r'\n-\s+(.+)', body):
                point = match.group(1).strip()
                if any(kw in point.lower() for kw in ['missing', 'no ', 'not ', 'slow', 'broken', 'error', 'lacks']):
                    points.append(point)
        
        return points[:7]  # Limit to top 7
    
    def _generate_proposed_state(self, lead_data: Dict, current: Dict) -> Dict:
        """Generate proposed website state based on pain points."""
        pain_points = current['pain_points']
        
        proposed = {
            'score': min(100, current['score'] + 40 + (len(pain_points) * 5)),
            'has_mobile': True,
            'has_cta': True,
            'has_trust': True,
            'has_social': True,
            'has_pricing': True,
            'has_booking': True,
            'load_speed': '< 2s',
            'features_added': self._derive_features(pain_points),
            'demo_concept': self._derive_demo_concept(lead_data)
        }
        
        return proposed
    
    def _derive_features(self, pain_points: List[str]) -> List[str]:
        """Derive features to add based on pain points."""
        features = []
        
        pain_lower = ' '.join(pain_points).lower()
        
        if 'mobile' in pain_lower or 'responsive' in pain_lower:
            features.append("📱 Mobile-first design (80% of visitors)")
        
        if 'cta' in pain_lower or 'call' in pain_lower or 'book' in pain_lower:
            features.append("🎯 Click-to-call + instant quote buttons")
        
        if 'trust' in pain_lower or 'review' in pain_lower:
            features.append("⭐ Live Google Reviews widget")
        
        if 'social' in pain_lower or 'facebook' in pain_lower:
            features.append("📲 Social proof integration")
        
        if 'pricing' in pain_lower or 'price' in pain_lower:
            features.append("💵 Transparent pricing calculator")
        
        if 'speed' in pain_lower or 'slow' in pain_lower:
            features.append("⚡ <2s load speed (Google requirement)")
        
        if 'seo' in pain_lower or 'google' in pain_lower:
            features.append("🔍 Local SEO optimization")
        
        if 'content' in pain_lower or 'thin' in pain_lower:
            features.append("📝 Service-specific landing pages")
        
        # Always add these baseline features
        baseline = [
            "🏠 Professional hero section with local imagery",
            "📞 Click-to-call button (prominent, sticky)",
            "📍 Service area map + neighborhood specificity",
            "🔒 SSL certificate + security badge"
        ]
        
        # Merge without duplicates
        for feature in baseline:
            if not any(f.split()[-1] == feature.split()[-1] for f in features):
                features.append(feature)
        
        return features[:8]  # Limit to top 8
    
    def _derive_demo_concept(self, lead_data: Dict) -> str:
        """Derive demo page concept from lead data."""
        name = lead_data['name']
        
        concepts = [
            f"**{name}** — Clean, Modern, Bookable",
            f"Single-page hero → instant quote for {name}",
            f"Mobile-first landing: 'Book {name} in 30 seconds'",
            f"Trust-first design: reviews → pricing → booking"
        ]
        
        return concepts[0]
    
    def _create_comparison(self, lead_data: Dict, current: Dict, proposed: Dict) -> str:
        """Create comparison markdown."""
        name = lead_data['name']
        
        markdown = f"""---
date: {datetime.now().strftime('%Y-%m-%d')}
lead: {name}
type: before-after-comparison
---

# Website Comparison: {name}

## The Problem

{name} currently scores **{current['score']}/100** on our website effectiveness audit.

**Key Issues:**
"""
        
        # Add pain points
        for i, point in enumerate(current['pain_points'][:5], 1):
            markdown += f"\n{i}. {point}"
        
        markdown += f"""

---

## Before vs After

### 📊 Score Comparison

| Metric | Before | After | Improvement |
|---|---|---|---|
| **Overall Score** | {current['score']}/100 | {proposed['score']}/100 | **+{proposed['score'] - current['score']}** |
| Mobile-Friendly | {'❌ No' if not current['has_mobile'] else '✅ Yes'} | ✅ Yes | Fixed |
| Clear CTAs | {'❌ No' if not current['has_cta'] else '✅ Yes'} | ✅ Yes | Added |
| Trust Signals | {'❌ No' if not current['has_trust'] else '✅ Yes'} | ✅ Yes | Added |
| Social Proof | {'❌ No' if not current['has_social'] else '✅ Yes'} | ✅ Yes | Added |
| Pricing Visible | {'❌ No' if not current['has_pricing'] else '✅ Yes'} | ✅ Yes | Added |
| Online Booking | {'❌ No' if not current['has_booking'] else '✅ Yes'} | ✅ Yes | Added |
| Load Speed | {current['load_speed']} | {proposed['load_speed']} | Optimized |

---

### 🎯 What's Added

"""
        
        for feature in proposed['features_added']:
            markdown += f"- {feature}\n"
        
        markdown += f"""

---

### 📱 Demo Concept

{proposed['demo_concept']}

**What this means:**
- Visitors see exactly what you do in 3 seconds
- They can book or call in 1 click
- Your reviews do the selling
- It works perfectly on phones

---

### 💡 Why This Matters for {name}

**Current State:**
- Visitors bounce because they can't find what they need
- No clear way to contact you
- Missing trust signals (reviews, local presence)
- Not showing up in Google for "cleaning Champaign"

**After State:**
- Every visitor knows exactly what you offer
- 1-click to call or book
- Google Reviews displayed live
- Ranks for "move-out cleaning Champaign IL"
- Mobile visitors convert at 3x the rate

---

### 📈 Expected Impact

| Metric | Current | Projected |
|---|---|---|
| Website conversions | ~0-2% | 8-15% |
| Phone calls from site | Low | 3-5x increase |
| Google ranking | Not visible | Page 1 local |
| Mobile visitors | Bounce 70% | Convert 30%+ |
| Quote requests | Manual only | Automated |

---

## Next Step

**See the full audit:** `{lead_data.get('website', 'N/A')}`
**Ready to upgrade?** We build the new page in 48 hours.

---

*Comparison generated {datetime.now().strftime('%Y-%m-%d')} by Standout Local*
"""
        
        return markdown


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate before/after website comparison')
    parser.add_argument('lead_file', help='Path to lead markdown file')
    parser.add_argument('--output-dir', '-o', help='Output directory (default: vault/wings/StandoutLocal/comparisons)')
    
    args = parser.parse_args()
    
    tool = WebsiteComparisonTool(verbose=True)
    result = tool.compare(args.lead_file, args.output_dir)
    
    if result:
        print(f"\n✅ Comparison generated: {result}")
        sys.exit(0)
    else:
        print("\n❌ Failed to generate comparison")
        sys.exit(1)


if __name__ == '__main__':
    import sys
    main()
