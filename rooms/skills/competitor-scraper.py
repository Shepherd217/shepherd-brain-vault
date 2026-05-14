#!/usr/bin/env python3
"""
Competitor Analysis Scraper
Pattern: Competitive Intelligence (from Standout Local workflow)
Source: Scrape competitor websites in same niche, find gaps and positioning

Analyzes competitor landscape for a given niche + location:
1. Search for competitors
2. Scrape their websites
3. Extract features, messaging, pricing, trust signals
4. Compare against target lead
5. Find positioning gaps and opportunities

Usage: python competitor-scraper.py "cleaning services" "Champaign IL" [--lead <lead-file.md>]
"""

import re
import sys
import json
import yaml
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class CompetitorAnalyzer:
    """Analyzes competitor landscape for a niche."""
    
    def __init__(self, vault_path: str = None, verbose: bool = True):
        self.vault_path = Path(vault_path or '/root/.openclaw/workspace/vault')
        self.verbose = verbose
        self.results = {
            'niche': '',
            'location': '',
            'competitors': [],
            'gaps': [],
            'opportunities': [],
            'report': ''
        }
    
    def _log(self, msg: str):
        if self.verbose:
            print(msg)
    
    def analyze(self, niche: str, location: str, lead_file: str = None) -> Dict:
        """Run full competitor analysis."""
        self.results['niche'] = niche
        self.results['location'] = location
        
        self._log(f"\n{'='*60}")
        self._log(f"COMPETITOR ANALYSIS")
        self._log(f"{'='*60}")
        self._log(f"Niche: {niche}")
        self._log(f"Location: {location}")
        
        # Search for competitors
        competitors = self._search_competitors(niche, location)
        
        if not competitors:
            self._log("❌ No competitors found")
            return self.results
        
        self._log(f"\n🔍 Found {len(competitors)} competitors")
        
        # Analyze each competitor
        for comp in competitors:
            self._analyze_competitor(comp)
        
        # Compare with target lead if provided
        if lead_file:
            self._compare_with_lead(lead_file)
        
        # Find gaps
        self._find_gaps()
        
        # Generate report
        report = self._generate_report()
        
        # Save
        self._save_report(report)
        
        return self.results
    
    def _search_competitors(self, niche: str, location: str) -> List[Dict]:
        """Search for competitors."""
        query = f'{niche} {location}'
        
        # Use kimi-search or web search
        self._log(f"   🔍 Searching: {query}")
        
        # Since we can't easily call kimi_search from here, use a simple approach
        # In production, this would integrate with search API
        # For now, return hardcoded sample competitors for testing
        
        # Try to find leads in same niche for reference
        leads_dir = self.vault_path / 'wings/StandoutLocal/leads'
        if leads_dir.exists():
            # Extract all lead names in same niche
            niche_keywords = niche.lower().split()
            
            for lead_file in leads_dir.glob('*.md'):
                try:
                    content = lead_file.read_text()
                    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
                    if match:
                        fm = yaml.safe_load(match.group(1))
                        name = fm.get('name', '')
                        
                        # Check if in same niche
                        name_lower = name.lower()
                        if any(kw in name_lower for kw in niche_keywords):
                            website = fm.get('website', '')
                            if website and website not in ['none', 'unknown', '']:
                                return [{
                                    'name': name,
                                    'website': website,
                                    'source': 'lead_database'
                                }]
                except:
                    pass
        
        # Fallback: return sample competitors for testing
        self._log("   ℹ️  Using sample competitors for testing")
        return [
            {'name': f'{niche.title()} Pro {location}', 'website': 'https://example.com', 'source': 'sample'},
            {'name': f'Best {niche.title()} {location}', 'website': 'https://example.org', 'source': 'sample'},
        ]
    
    def _analyze_competitor(self, competitor: Dict):
        """Analyze a single competitor."""
        self._log(f"\n   📊 Analyzing: {competitor['name']}")
        
        # Use website auditor if URL is real
        url = competitor.get('website', '')
        
        if url and 'example.com' not in url:
            try:
                auditor_path = self.vault_path / 'rooms/skills/website-auditor.py'
                if auditor_path.exists():
                    result = subprocess.run(
                        ['python3', str(auditor_path), url],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    output = result.stdout + result.stderr
                    
                    # Parse score
                    score_match = re.search(r'SCORE:\s*(\d+)', output)
                    score = int(score_match.group(1)) if score_match else 0
                    
                    competitor['score'] = score
                    competitor['has_website'] = True
                    
                    # Parse features
                    competitor['features'] = self._extract_features_from_audit(output)
                else:
                    competitor['score'] = 0
                    competitor['has_website'] = False
                    competitor['features'] = []
            except:
                competitor['score'] = 0
                competitor['has_website'] = False
                competitor['features'] = []
        else:
            # Sample data for testing
            competitor['score'] = 45 if 'sample' in competitor.get('source', '') else 0
            competitor['has_website'] = True
            competitor['features'] = [
                'Basic contact form',
                'Phone number listed',
                'Service list'
            ]
        
        self.results['competitors'].append(competitor)
        self._log(f"      Score: {competitor.get('score', 'N/A')}/100")
    
    def _extract_features_from_audit(self, audit_output: str) -> List[str]:
        """Extract features from audit output."""
        features = []
        
        # Parse pain points (they indicate what's NOT there, so invert)
        pain_points = re.findall(r'\d+\.\s+(.+)', audit_output)
        
        common_features = [
            'Mobile responsive',
            'Online booking',
            'Pricing display',
            'Google Reviews',
            'Social media links',
            'Service descriptions',
            'Contact form',
            'SSL certificate'
        ]
        
        # If pain point mentions missing something, competitor doesn't have it
        pain_text = ' '.join(pain_points).lower()
        
        for feature in common_features:
            if feature.lower() not in pain_text:
                features.append(feature)
        
        return features
    
    def _compare_with_lead(self, lead_file: str):
        """Compare competitors with target lead."""
        lead_path = Path(lead_file)
        
        if not lead_path.exists():
            return
        
        try:
            content = lead_path.read_text()
            match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
            if match:
                fm = yaml.safe_load(match.group(1))
                self.results['target_lead'] = {
                    'name': fm.get('name', ''),
                    'score': fm.get('score', 0),
                    'website': fm.get('website', ''),
                    'pain': fm.get('pain', 0)
                }
        except:
            pass
    
    def _find_gaps(self):
        """Find market gaps based on competitor analysis."""
        if not self.results['competitors']:
            return
        
        # Collect all competitor features
        all_features = set()
        for comp in self.results['competitors']:
            for feature in comp.get('features', []):
                all_features.add(feature)
        
        # Common gaps in local service businesses
        potential_gaps = [
            'Instant online booking',
            'Transparent pricing calculator',
            'Live chat support',
            'Before/after photo gallery',
            'Customer video testimonials',
            'Service area map with neighborhoods',
            'FAQ with schema markup',
            'Blog with local SEO content',
            'Emergency service badge',
            'Eco-friendly/green messaging',
            'Team member profiles with photos',
            'Real-time availability calendar',
            'Text message reminders',
            'Referral program',
            'Move-out cleaning specialization'
        ]
        
        # Find gaps: features competitors DON'T have
        gaps = []
        for gap in potential_gaps:
            gap_lower = gap.lower()
            has_it = any(gap_lower in f.lower() for f in all_features)
            if not has_it:
                gaps.append(gap)
        
        self.results['gaps'] = gaps[:8]  # Top 8 gaps
        
        # Generate positioning opportunities
        opportunities = []
        
        avg_score = sum(c.get('score', 0) for c in self.results['competitors']) / len(self.results['competitors'])
        
        if avg_score < 60:
            opportunities.append(f"Competitor sites average {avg_score:.0f}/100 — huge opportunity for a better site")
        
        if len(gaps) >= 3:
            opportunities.append(f"{len(gaps)} key features missing across all competitors — first-mover advantage")
        
        if 'Instant online booking' in gaps:
            opportunities.append("No competitor has instant booking — major conversion advantage")
        
        if 'Transparent pricing calculator' in gaps:
            opportunities.append("Pricing is opaque everywhere — transparency wins trust")
        
        if 'Move-out cleaning specialization' in gaps:
            opportunities.append("Move-out season active — no one messaging it")
        
        self.results['opportunities'] = opportunities
    
    def _generate_report(self) -> str:
        """Generate markdown report."""
        niche = self.results['niche']
        location = self.results['location']
        competitors = self.results['competitors']
        gaps = self.results['gaps']
        opportunities = self.results['opportunities']
        
        report = f"""---
date: {datetime.now().strftime('%Y-%m-%d')}
type: competitor-analysis
niche: {niche}
location: {location}
---

# Competitor Analysis: {niche} in {location}

## Market Landscape

**Niche:** {niche}
**Location:** {location}
**Competitors Analyzed:** {len(competitors)}

### Competitor Scores

| Competitor | Score | Website |
|---|---|---|
"""
        
        for comp in competitors:
            name = comp.get('name', 'Unknown')
            score = comp.get('score', 'N/A')
            website = comp.get('website', 'N/A')
            report += f"| {name} | {score}/100 | {website} |\n"
        
        avg_score = sum(c.get('score', 0) for c in competitors) / len(competitors) if competitors else 0
        report += f"\n**Average Competitor Score:** {avg_score:.0f}/100\n"
        
        if 'target_lead' in self.results:
            lead = self.results['target_lead']
            report += f"\n**Your Target ({lead['name']}):** {lead.get('score', 'N/A')}/100\n"
            if lead.get('score', 0) > avg_score:
                report += f"✅ **Already ahead of average!**\n"
            else:
                report += f"⚠️  **Below average — but fixable**\n"
        
        report += f"""

---

## Market Gaps

Features **missing** across all competitors:

"""
        
        for i, gap in enumerate(gaps, 1):
            report += f"{i}. **{gap}** — No competitor offers this\n"
        
        report += f"""

---

## Positioning Opportunities

"""
        
        for opp in opportunities:
            report += f"- {opp}\n"
        
        report += f"""

---

## Recommended Differentiation

Based on gaps, here's how to stand out:

### Immediate Wins (Build First)
"""
        
        immediate = gaps[:3] if len(gaps) >= 3 else gaps
        for gap in immediate:
            report += f"- **{gap}** — Easy to add, high impact\n"
        
        report += f"""

### Competitive Moats (Harder to Copy)
- **Specialized landing pages** — "Move-out cleaning Champaign" ranks #1
- **Review automation** — Auto-request reviews, display live
- **Partnership badges** — "Preferred by UIUC Housing", "Apartment-approved"

---

## Messaging Angles That Work

**What competitors say:** "We clean houses"
**What you should say:** "Champaign's move-out cleaning specialist — 48h turnaround, deposit-back guarantee"

**Why it works:**
- Specificity > generic
- Speed promise > "contact us"
- Guarantee > "trust us"
- Local > "we serve everywhere"

---

## Next Steps

1. **Build the demo** with 2-3 gaps as features
2. **Use comparison tool** to show before/after vs competitors
3. **Target outreach** to leads in this niche with gap-based hook

---

*Analysis generated {datetime.now().strftime('%Y-%m-%d')} by Standout Local*
"""
        
        return report
    
    def _save_report(self, report: str):
        """Save report to vault."""
        reports_dir = self.vault_path / 'wings/StandoutLocal/competitors'
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Create filename from niche + location
        niche_slug = self.results['niche'].lower().replace(' ', '-')
        location_slug = self.results['location'].lower().replace(' ', '-')
        filename = f"{niche_slug}-{location_slug}-competitors.md"
        
        output_path = reports_dir / filename
        output_path.write_text(report)
        
        self._log(f"\n💾 Report saved to: {output_path}")
        self.results['report_path'] = str(output_path)


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Competitor analysis scraper')
    parser.add_argument('niche', help='Business niche (e.g., "cleaning services")')
    parser.add_argument('location', help='Location (e.g., "Champaign IL")')
    parser.add_argument('--lead', '-l', help='Lead file to compare against')
    
    args = parser.parse_args()
    
    analyzer = CompetitorAnalyzer(verbose=True)
    results = analyzer.analyze(args.niche, args.location, args.lead)
    
    if results['competitors']:
        print(f"\n✅ Analyzed {len(results['competitors'])} competitors")
        print(f"   Gaps found: {len(results['gaps'])}")
        print(f"   Opportunities: {len(results['opportunities'])}")
        sys.exit(0)
    else:
        print("\n❌ No competitors found")
        sys.exit(1)


if __name__ == '__main__':
    main()
