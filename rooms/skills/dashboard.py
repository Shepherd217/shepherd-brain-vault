#!/usr/bin/env python3
"""
Lead Pipeline Dashboard
Pattern: Dashboard/Overview (from awesome-llm-apps ai_dashboards/)
Source: Aggregate all lead data into one unified view

Shows:
- All leads with status, scores, action needed
- Outreach queue (drafted, ready to send, sent)
- Recent activity (last 7 days)
- Pipeline metrics (conversion funnel)
"""

import os
import sys
import yaml
import re
from pathlib import Path
from typing import Dict, List
from datetime import datetime, timedelta

class LeadDashboard:
    """Aggregates all lead pipeline data into dashboard view."""
    
    def __init__(self, vault_path: str = None, verbose: bool = True):
        self.vault_path = Path(vault_path or '/root/.openclaw/workspace/vault')
        self.verbose = verbose
        self.leads_dir = self.vault_path / 'wings/StandoutLocal/leads'
        self.outreach_dir = self.vault_path / 'wings/StandoutLocal/outreach'
        self.debates_dir = self.vault_path / 'wings/StandoutLocal/debates'
    
    def _log(self, msg: str):
        if self.verbose:
            print(msg)
    
    def load_leads(self) -> List[Dict]:
        """Load all lead files."""
        leads = []
        
        if not self.leads_dir.exists():
            return leads
        
        for lead_file in sorted(self.leads_dir.glob('*.md')):
            try:
                content = lead_file.read_text()
                
                # Parse frontmatter
                pattern = r'^---\s*\n(.*?)\n---\s*\n'
                match = re.match(pattern, content, re.DOTALL)
                
                if match:
                    fm = yaml.safe_load(match.group(1))
                    leads.append({
                        'file': lead_file.name,
                        'name': fm.get('name', lead_file.stem),
                        'status': fm.get('status', 'unknown'),
                        'score': fm.get('score', 0) or 0,
                        'opportunity': fm.get('opportunity', 0) or 0,
                        'pain': fm.get('pain', 0) or 0,
                        'reach': fm.get('reach', 0) or 0,
                        'fit': fm.get('fit', 0) or 0,
                        'modified': datetime.fromtimestamp(lead_file.stat().st_mtime),
                    })
            except Exception as e:
                self._log(f"⚠️  Error parsing {lead_file}: {e}")
        
        return leads
    
    def load_outreach(self) -> List[Dict]:
        """Load all outreach files."""
        outreach = []
        
        if not self.outreach_dir.exists():
            return outreach
        
        for out_file in sorted(self.outreach_dir.glob('*.md')):
            try:
                content = out_file.read_text()
                
                # Parse frontmatter
                pattern = r'^---\s*\n(.*?)\n---\s*\n'
                match = re.match(pattern, content, re.DOTALL)
                
                if match:
                    fm = yaml.safe_load(match.group(1))
                    outreach.append({
                        'file': out_file.name,
                        'lead': fm.get('lead', 'Unknown'),
                        'variant': fm.get('variant', 1),
                        'score': fm.get('score', 0) or 0,
                        'status': fm.get('status', 'draft'),
                        'modified': datetime.fromtimestamp(out_file.stat().st_mtime),
                    })
            except Exception as e:
                self._log(f"⚠️  Error parsing {out_file}: {e}")
        
        return outreach
    
    def generate_dashboard(self) -> str:
        """Generate dashboard markdown."""
        leads = self.load_leads()
        outreach = self.load_outreach()
        
        # Calculate metrics
        total_leads = len(leads)
        scored_leads = [l for l in leads if l['status'] in ['scored', 'outreached', 'responded', 'converted']]
        outreached_leads = [l for l in leads if l['status'] == 'outreached']
        drafted_outreach = [o for o in outreach if o['status'] == 'draft']
        avg_score = sum(l['score'] for l in scored_leads) / len(scored_leads) if scored_leads else 0
        
        # Status breakdown
        status_counts = {}
        for l in leads:
            status_counts[l['status']] = status_counts.get(l['status'], 0) + 1
        
        # Top leads
        top_leads = sorted([l for l in leads if l['score']], key=lambda x: x['score'], reverse=True)[:5]
        
        # Recent activity (last 7 days)
        week_ago = datetime.now() - timedelta(days=7)
        recent_leads = [l for l in leads if l['modified'] > week_ago]
        recent_outreach = [o for o in outreach if o['modified'] > week_ago]
        
        # Build dashboard
        dashboard = f"""---
date: {datetime.now().strftime('%Y-%m-%d')}
type: pipeline-dashboard
---

# Standout Local — Pipeline Dashboard
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*

## 📊 Pipeline Metrics

| Metric | Value |
|---|---|
| Total Leads | {total_leads} |
| Scored Leads | {len(scored_leads)} |
| Avg Score | {avg_score:.1f}/100 |
| Outreach Drafted | {len(drafted_outreach)} |
| Outreach Sent | {len(outreached_leads)} |
| Recent Activity (7d) | {len(recent_leads)} leads, {len(recent_outreach)} outreach |

## 📈 Status Breakdown

"""
        
        for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
            bar = '█' * count
            dashboard += f"- **{status}**: {count} {bar}\n"
        
        dashboard += "\n## 🏆 Top 5 Leads\n\n"
        dashboard += "| Rank | Lead | Score | Status |\n"
        dashboard += "|---|---|---|---|\n"
        
        for i, lead in enumerate(top_leads, 1):
            score_emoji = "🔥" if lead['score'] >= 90 else "⚡" if lead['score'] >= 80 else "📌"
            dashboard += f"| {i} | {lead['name']} | {score_emoji} {lead['score']}/100 | {lead['status']} |\n"
        
        dashboard += "\n## 📤 Outreach Queue\n\n"
        if drafted_outreach:
            dashboard += "### Ready to Send\n\n"
            for o in drafted_outreach:
                dashboard += f"- **{o['lead']}** (Variant {o['variant']}, Score: {o['score']}/100)\n"
        else:
            dashboard += "_No drafted outreach. Generate with `outreach-evolver.py`_\n"
        
        dashboard += "\n## 🔔 Recent Activity (Last 7 Days)\n\n"
        
        if recent_leads:
            dashboard += "### New/Updated Leads\n\n"
            for l in recent_leads[:5]:
                days_ago = (datetime.now() - l['modified']).days
                dashboard += f"- {l['name']} — {l['status']} ({days_ago}d ago)\n"
        
        if recent_outreach:
            dashboard += "\n### Generated Outreach\n\n"
            for o in recent_outreach[:5]:
                days_ago = (datetime.now() - o['modified']).days
                dashboard += f"- {o['lead']} — Variant {o['variant']} ({days_ago}d ago)\n"
        
        dashboard += """\n## 🎯 Action Items

"""
        
        # Auto-generate action items
        actions = []
        
        unscored = [l for l in leads if l['status'] in ['discovered', 'unknown']]
        if unscored:
            actions.append(f"Score {len(unscored)} unscored leads (`python lead-validator.py`)")
        
        high_score_no_outreach = [l for l in leads if l['score'] and l['score'] >= 80 and l['status'] not in ['outreached', 'responded', 'converted']]
        if high_score_no_outreach:
            actions.append(f"Generate outreach for {len(high_score_no_outreach)} high-scoring leads (`python outreach-evolver.py`)")
        
        if drafted_outreach:
            actions.append(f"Send {len(drafted_outreach)} drafted outreach messages")
        
        if not actions:
            actions.append("All caught up! Check for new leads.")
        
        for action in actions:
            dashboard += f"- [ ] {action}\n"
        
        dashboard += "\n---\n*Dashboard auto-generated. Run `python dashboard.py` to refresh.*\n"
        
        return dashboard
    
    def save_dashboard(self, output_path: str = None):
        """Save dashboard to vault."""
        output = Path(output_path or self.vault_path / 'wings/StandoutLocal/dashboard.md')
        output.parent.mkdir(parents=True, exist_ok=True)
        
        dashboard = self.generate_dashboard()
        output.write_text(dashboard)
        
        self._log(f"\n💾 Dashboard saved to: {output}")
        return str(output)


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Lead pipeline dashboard')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--print', '-p', action='store_true', help='Print to stdout only')
    
    args = parser.parse_args()
    
    dashboard = LeadDashboard(verbose=not args.print)
    
    if args.print:
        print(dashboard.generate_dashboard())
    else:
        dashboard.save_dashboard(args.output)


if __name__ == '__main__':
    main()
