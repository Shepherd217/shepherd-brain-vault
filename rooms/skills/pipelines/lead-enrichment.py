#!/usr/bin/env python3
"""
Lead Enrichment Pipeline
Pattern: Pipeline Orchestration (from awesome-llm-apps ai_orchestration/)
Source: Chain multiple tools together for end-to-end enrichment

One command pipeline:
  Input: Lead file path
  Step 1: Validate structure (lead-validator)
  Step 2: Scrape website (website-auditor) if URL exists
  Step 3: Score website
  Step 4: Update lead file with enriched data
  Step 5: Validate again
  Step 6: Run cross-artifact analysis
  Output: Enriched lead file + audit report

Usage: python lead-enrichment.py <lead-file.md> [--skip-audit]
"""

import sys
import os
import re
import json
import yaml
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class LeadEnrichmentPipeline:
    """End-to-end lead enrichment pipeline."""
    
    def __init__(self, vault_path: str = None, verbose: bool = True):
        self.vault_path = Path(vault_path or '/root/.openclaw/workspace/vault')
        self.verbose = verbose
        self.results = {
            'lead_file': '',
            'steps': [],
            'errors': [],
            'warnings': [],
            'outputs': []
        }
    
    def _log(self, msg: str):
        if self.verbose:
            print(msg)
    
    def _run_step(self, name: str, func, *args, **kwargs) -> any:
        """Execute a pipeline step with error handling."""
        self._log(f"\n{'='*60}")
        self._log(f"STEP: {name}")
        self._log(f"{'='*60}")
        
        try:
            result = func(*args, **kwargs)
            self.results['steps'].append({
                'name': name,
                'status': 'success',
                'output': str(result)[:200] if result else 'done'
            })
            return result
        except Exception as e:
            error_msg = f"{name} failed: {str(e)}"
            self.results['errors'].append(error_msg)
            self.results['steps'].append({
                'name': name,
                'status': 'failed',
                'error': str(e)
            })
            self._log(f"   ❌ {error_msg}")
            return None
    
    def enrich(self, lead_file: str, skip_audit: bool = False) -> Dict:
        """Run full enrichment pipeline on a lead file."""
        lead_path = Path(lead_file)
        self.results['lead_file'] = str(lead_path)
        
        self._log(f"\n{'#'*60}")
        self._log(f"LEAD ENRICHMENT PIPELINE")
        self._log(f"{'#'*60}")
        self._log(f"Target: {lead_path.name}")
        
        if not lead_path.exists():
            self.results['errors'].append(f"Lead file not found: {lead_file}")
            return self.results
        
        # Parse lead file
        lead_data = self._run_step("Parse Lead", self._parse_lead, lead_path)
        if not lead_data:
            return self.results
        
        # Step 1: Validate
        validation = self._run_step("Validate Structure", self._validate_lead, lead_path)
        
        # Step 2: Scrape website (if URL exists and is valid)
        website_url = lead_data.get('website', '')
        invalid_markers = ['none', 'unknown', 'not found', 'n/a', '**none found**', '']
        has_valid_url = website_url and not any(marker in website_url.lower() for marker in invalid_markers)
        
        audit_result = None
        if has_valid_url:
            audit_result = self._run_step("Website Audit", self._audit_website, website_url)
            
            # Step 3: Update lead file with audit data
            if audit_result:
                self._run_step("Update Lead", self._update_lead, lead_path, lead_data, audit_result)
        else:
            self._log("   ℹ️  No valid website URL found — skipping audit")
            self.results['warnings'].append(f"No valid website URL in lead file (got: '{website_url}')")
        
        # Step 4: Re-validate after updates (only if we did an audit)
        if audit_result:
            self._run_step("Re-Validate", self._validate_lead, lead_path)
        
        # Step 5: Cross-artifact check
        if not skip_audit:
            self._run_step("Cross-Artifact Check", self._run_consistency_check)
        
        # Step 6: Update dashboard
        self._run_step("Update Dashboard", self._update_dashboard, lead_data)
        
        # Generate summary
        self._generate_summary()
        
        return self.results
    
    def _parse_lead(self, lead_path: Path) -> Dict:
        """Parse lead file frontmatter and body."""
        content = lead_path.read_text()
        
        # Extract frontmatter
        pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
        match = re.match(pattern, content, re.DOTALL)
        
        if not match:
            raise ValueError("No frontmatter found")
        
        fm = yaml.safe_load(match.group(1))
        body = match.group(2)
        
        # Extract business info
        website = self._extract_field(body, 'Website')
        if not website:
            website = fm.get('website', '')
        
        return {
            'name': fm.get('name', lead_path.stem.replace('-', ' ').title()),
            'status': fm.get('status', 'discovered'),
            'score': fm.get('score', 0),
            'website': website,
            'opportunity': fm.get('opportunity', 0),
            'pain': fm.get('pain', 0),
            'reach': fm.get('reach', 0),
            'fit': fm.get('fit', 0),
            'source': fm.get('source', ''),
            'frontmatter': fm,
            'body': body
        }
    
    def _extract_field(self, body: str, field: str) -> str:
        """Extract a field from Business Info section."""
        pattern = rf'\*\*{field}:\*\*\s*(.+)'
        match = re.search(pattern, body)
        return match.group(1).strip() if match else ''
    
    def _validate_lead(self, lead_path: Path) -> Dict:
        """Run lead validator on file."""
        validator_path = self.vault_path / 'rooms/skills/validators/lead-validator.py'
        
        if not validator_path.exists():
            raise FileNotFoundError("Lead validator not found")
        
        # Run validator
        result = subprocess.run(
            ['python3', str(validator_path), str(lead_path)],
            capture_output=True,
            text=True,
            cwd=str(self.vault_path.parent)
        )
        
        output = result.stdout + result.stderr
        
        # Parse result
        passed = 'PASS' in output and 'FAIL' not in output
        errors = len(re.findall(r'❌', output))
        warnings = len(re.findall(r'⚠️', output))
        
        self._log(f"   {'✅' if passed else '❌'} Validation: {errors} errors, {warnings} warnings")
        
        return {
            'passed': passed,
            'errors': errors,
            'warnings': warnings,
            'output': output[:500]
        }
    
    def _audit_website(self, url: str) -> Optional[Dict]:
        """Run website auditor on URL."""
        auditor_path = self.vault_path / 'rooms/skills/website-auditor.py'
        
        if not auditor_path.exists():
            raise FileNotFoundError("Website auditor not found")
        
        self._log(f"   🔍 Auditing: {url}")
        
        # Run auditor
        result = subprocess.run(
            ['python3', str(auditor_path), url],
            capture_output=True,
            text=True,
            cwd=str(self.vault_path.parent),
            timeout=30
        )
        
        output = result.stdout + result.stderr
        
        # Parse score
        score_match = re.search(r'SCORE:\s*(\d+)', output)
        score = int(score_match.group(1)) if score_match else 0
        
        # Parse pain points
        pain_points = re.findall(r'\d+\.\s+(.+)', output)
        
        self._log(f"   📊 Website Score: {score}/100")
        self._log(f"   📋 Pain Points: {len(pain_points)} found")
        
        return {
            'score': score,
            'url': url,
            'pain_points': pain_points,
            'output': output[:500]
        }
    
    def _update_lead(self, lead_path: Path, lead_data: Dict, audit_result: Dict):
        """Update lead file with audit results."""
        content = lead_path.read_text()
        
        # Parse frontmatter
        pattern = r'^(---\s*\n.*?\n---)\s*\n(.*)$'
        match = re.match(pattern, content, re.DOTALL)
        
        if not match:
            raise ValueError("Cannot parse lead file")
        
        frontmatter_text = match.group(1)
        body = match.group(2)
        
        # Update frontmatter with audit score if website score is present
        fm = yaml.safe_load(frontmatter_text.replace('---', ''))
        
        # Update or add website score
        if audit_result.get('score'):
            fm['website_score'] = audit_result['score']
        
        # Update status if it was discovered and we have a score
        if fm.get('status') == 'discovered' and audit_result.get('score'):
            fm['status'] = 'scored'
        
        # Regenerate frontmatter
        new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True).strip()
        
        # Update body: add/update Website Audit section if it exists
        # or append a note about the audit
        audit_note = f"""

## Automated Audit
- **URL:** {audit_result['url']}
- **Score:** {audit_result['score']}/100
- **Date:** {datetime.now().strftime('%Y-%m-%d')}
- **Pain Points:** {len(audit_result.get('pain_points', []))}
"""
        
        # Check if there's already an audit section
        if '## Automated Audit' not in body:
            # Add before Outreach Status or at the end
            if '## Outreach Status' in body:
                body = body.replace('## Outreach Status', audit_note + '\n## Outreach Status')
            else:
                body += '\n' + audit_note
        else:
            # Replace existing audit section
            body = re.sub(
                r'## Automated Audit.*?\n(?=## |\Z)',
                audit_note.lstrip() + '\n',
                body,
                flags=re.DOTALL
            )
        
        # Reassemble
        new_content = f"---\n{new_fm}\n---\n{body}"
        
        # Write back
        lead_path.write_text(new_content)
        
        self._log(f"   💾 Updated lead file with audit results")
        
        return True
    
    def _run_consistency_check(self) -> Dict:
        """Run cross-artifact analyzer."""
        analyzer_path = self.vault_path / 'rooms/skills/cross-artifact-analyzer.py'
        
        if not analyzer_path.exists():
            raise FileNotFoundError("Cross-artifact analyzer not found")
        
        result = subprocess.run(
            ['python3', str(analyzer_path), '--print'],
            capture_output=True,
            text=True,
            cwd=str(self.vault_path.parent)
        )
        
        output = result.stdout + result.stderr
        passed = result.returncode == 0
        
        self._log(f"   {'✅' if passed else '⚠️'} Consistency check: {'passed' if passed else 'issues found'}")
        
        return {
            'passed': passed,
            'output': output[:300]
        }
    
    def _update_dashboard(self, lead_data: Dict):
        """Update dashboard with enriched lead info."""
        dashboard_path = self.vault_path / 'wings/StandoutLocal/dashboard.md'
        
        if not dashboard_path.exists():
            self._log("   ℹ️  Dashboard not found")
            return False
        
        dashboard = dashboard_path.read_text()
        lead_name = lead_data['name']
        
        # Check if lead is already in dashboard
        if lead_name in dashboard or lead_data.get('frontmatter', {}).get('name', '') in dashboard:
            self._log(f"   ℹ️  {lead_name} already in dashboard")
            return True
        
        # Add to dashboard - append to leads list
        lead_entry = f"\n- **{lead_name}** — {lead_data.get('status', 'discovered')} ({lead_data.get('score', 0)}/100)"
        
        # Find the leads list and append
        if '## Active Leads' in dashboard:
            # Add after the last lead entry
            dashboard += lead_entry
            dashboard_path.write_text(dashboard)
            self._log(f"   💾 Added {lead_name} to dashboard")
            return True
        
        return False
    
    def _generate_summary(self):
        """Generate pipeline summary."""
        self._log(f"\n{'='*60}")
        self._log(f"ENRICHMENT COMPLETE")
        self._log(f"{'='*60}")
        
        success_count = sum(1 for s in self.results['steps'] if s['status'] == 'success')
        total_count = len(self.results['steps'])
        
        self._log(f"Steps completed: {success_count}/{total_count}")
        self._log(f"Errors: {len(self.results['errors'])}")
        self._log(f"Warnings: {len(self.results['warnings'])}")
        
        if self.results['errors']:
            self._log("\nErrors:")
            for e in self.results['errors']:
                self._log(f"  ❌ {e}")
        
        if self.results['warnings']:
            self._log("\nWarnings:")
            for w in self.results['warnings']:
                self._log(f"  ⚠️  {w}")


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Lead enrichment pipeline')
    parser.add_argument('lead_file', help='Path to lead markdown file')
    parser.add_argument('--skip-audit', action='store_true', help='Skip cross-artifact analysis')
    parser.add_argument('--output', '-o', help='Save results to JSON file')
    
    args = parser.parse_args()
    
    pipeline = LeadEnrichmentPipeline(verbose=True)
    results = pipeline.enrich(args.lead_file, skip_audit=args.skip_audit)
    
    if args.output:
        Path(args.output).write_text(json.dumps(results, indent=2))
        print(f"\n💾 Results saved to: {args.output}")
    
    # Exit with error if any critical errors
    if results['errors']:
        sys.exit(1)
    
    sys.exit(0)


if __name__ == '__main__':
    main()
