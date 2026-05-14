#!/usr/bin/env python3
"""
Cross-Artifact Analyzer
Pattern: Cross-Artifact Analysis (from GitHub Spec-Kit /speckit.analyze)
Source: Check consistency across specs, plans, data models, and implementations

Analyzes the vault for inconsistencies between:
- LEAD_SYSTEM.md schema vs lead-validator.py enforcement
- Outreach files referencing valid leads
- Dashboard including all leads
- Pattern library matching actual implementations
- Generated artifacts vs source files
"""

import os
import sys
import re
import yaml
import importlib.util
from pathlib import Path
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass

@dataclass
class Inconsistency:
    """One found inconsistency."""
    severity: str  # critical, warning, info
    category: str
    message: str
    file_a: str
    file_b: str
    detail: str

class CrossArtifactAnalyzer:
    """Analyzes vault for cross-file inconsistencies."""
    
    def __init__(self, vault_path: str = None, verbose: bool = True):
        self.vault_path = Path(vault_path or '/root/.openclaw/workspace/vault')
        self.verbose = verbose
        self.issues: List[Inconsistency] = []
    
    def _log(self, msg: str):
        if self.verbose:
            print(msg)
    
    def analyze_all(self) -> List[Inconsistency]:
        """Run all cross-artifact checks."""
        self._log(f"\n{'='*60}")
        self._log("CROSS-ARTIFACT ANALYSIS")
        self._log(f"{'='*60}")
        self._log(f"Vault: {self.vault_path}")
        
        self.check_lead_system_vs_validator()
        self.check_outreach_vs_leads()
        self.check_dashboard_vs_leads()
        self.check_patterns_vs_implementations()
        self.check_debates_vs_leads()
        self.check_audits_vs_sources()
        
        return self.issues
    
    def check_lead_system_vs_validator(self):
        """Check LEAD_SYSTEM.md schema matches validator enforcement."""
        self._log("\n🔍 Checking LEAD_SYSTEM.md vs lead-validator.py...")
        
        lead_system = self.vault_path / 'wings/StandoutLocal/LEAD_SYSTEM.md'
        validator = self.vault_path / 'rooms/skills/validators/lead-validator.py'
        
        if not lead_system.exists():
            self.issues.append(Inconsistency(
                severity='critical',
                category='schema',
                message='LEAD_SYSTEM.md not found',
                file_a=str(lead_system),
                file_b='',
                detail='Validator has nothing to validate against'
            ))
            return
        
        if not validator.exists():
            self.issues.append(Inconsistency(
                severity='critical',
                category='schema',
                message='lead-validator.py not found',
                file_a=str(validator),
                file_b='',
                detail='Schema exists but no validator to enforce it'
            ))
            return
        
        # Extract required sections from LEAD_SYSTEM.md
        system_content = lead_system.read_text()
        required_sections = self._extract_required_sections(system_content)
        
        # Check validator enforces these sections
        validator_content = validator.read_text()
        
        missing_in_validator = []
        for section in required_sections:
            # Check if section name appears in validator code
            section_normalized = section.lower().replace(' ', '_').replace('-', '_')
            if section_normalized not in validator_content.lower() and section not in validator_content:
                missing_in_validator.append(section)
        
        # Check if validator enforces sections that are part of "Lead File Format"
        # The validator checks frontmatter + required sections = file format
        if 'Lead File Format' in missing_in_validator:
            has_frontmatter_check = any('frontmatter' in validator_content.lower() for _ in range(1))
            has_section_check = any('required_sections' in validator_content.lower() for _ in range(1))
            if has_frontmatter_check and has_section_check:
                missing_in_validator.remove('Lead File Format')
        
        if missing_in_validator:
            self.issues.append(Inconsistency(
                severity='warning',
                category='schema',
                message=f'{len(missing_in_validator)} sections in LEAD_SYSTEM.md not checked by validator',
                file_a=str(lead_system),
                file_b=str(validator),
                detail=f'Missing: {", ".join(missing_in_validator[:5])}'
            ))
        else:
            self._log("   ✅ All LEAD_SYSTEM sections covered by validator")
        
        # Check numeric ranges
        if '0-100' not in system_content:
            self.issues.append(Inconsistency(
                severity='warning',
                category='schema',
                message='LEAD_SYSTEM.md does not specify 0-100 score range',
                file_a=str(lead_system),
                file_b='',
                detail='Validator may enforce ranges not documented'
            ))
    
    def check_outreach_vs_leads(self):
        """Check outreach files reference valid leads."""
        self._log("\n🔍 Checking outreach files vs leads...")
        
        leads_dir = self.vault_path / 'wings/StandoutLocal/leads'
        outreach_dir = self.vault_path / 'wings/StandoutLocal/outreach'
        
        if not leads_dir.exists():
            self.issues.append(Inconsistency(
                severity='warning',
                category='references',
                message='Leads directory not found',
                file_a=str(leads_dir),
                file_b='',
                detail='Cannot validate outreach references'
            ))
            return
        
        # Get valid lead names from files
        valid_leads = set()
        for lead_file in leads_dir.glob('*.md'):
            try:
                content = lead_file.read_text()
                match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
                if match:
                    fm = yaml.safe_load(match.group(1))
                    name = fm.get('name', lead_file.stem)
                    valid_leads.add(name)
                    valid_leads.add(lead_file.stem)
                    # Also add normalized versions for fuzzy matching
                    valid_leads.add(name.lower().replace(' ', '-'))
                    valid_leads.add(lead_file.stem.lower().replace('-', ' '))
            except:
                valid_leads.add(lead_file.stem)
                valid_leads.add(lead_file.stem.lower().replace('-', ' '))
        
        # Check outreach files
        if not outreach_dir.exists():
            self._log("   ℹ️  No outreach directory yet")
            return
        
        orphaned_outreach = []
        for out_file in outreach_dir.glob('*.md'):
            try:
                content = out_file.read_text()
                match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
                if match:
                    fm = yaml.safe_load(match.group(1))
                    lead_name = fm.get('lead', '')
                    
                    # Check if lead exists (fuzzy matching)
                    lead_name_norm = lead_name.lower().replace(' ', '-')
                    lead_exists = any(
                        lead_name_norm == vl.lower() or 
                        lead_name.lower() == vl.lower() or
                        lead_name_norm in vl.lower() or
                        vl.lower() in lead_name_norm
                        for vl in valid_leads
                    )
                    
                    if not lead_exists and lead_name:
                        orphaned_outreach.append((out_file.name, lead_name))
            except:
                pass
        
        if orphaned_outreach:
            self.issues.append(Inconsistency(
                severity='warning',
                category='references',
                message=f'{len(orphaned_outreach)} outreach files reference missing leads',
                file_a=str(outreach_dir),
                file_b=str(leads_dir),
                detail=f'Orphaned: {", ".join(f"{o[0]} → {o[1]}" for o in orphaned_outreach[:3])}'
            ))
        else:
            self._log("   ✅ All outreach files reference valid leads")
    
    def check_dashboard_vs_leads(self):
        """Check dashboard includes all leads."""
        self._log("\n🔍 Checking dashboard vs leads...")
        
        dashboard = self.vault_path / 'wings/StandoutLocal/dashboard.md'
        leads_dir = self.vault_path / 'wings/StandoutLocal/leads'
        
        if not dashboard.exists():
            self.issues.append(Inconsistency(
                severity='warning',
                category='coverage',
                message='Dashboard not found',
                file_a=str(dashboard),
                file_b='',
                detail='Pipeline view not available'
            ))
            return
        
        if not leads_dir.exists():
            return
        
        dashboard_content = dashboard.read_text()
        lead_files = list(leads_dir.glob('*.md'))
        
        # Count leads mentioned in dashboard
        leads_in_dashboard = 0
        for lead_file in lead_files:
            lead_name = lead_file.stem
            if lead_name in dashboard_content or lead_file.name in dashboard_content:
                leads_in_dashboard += 1
        
        missing = len(lead_files) - leads_in_dashboard
        
        if missing > 0:
            self.issues.append(Inconsistency(
                severity='warning',
                category='coverage',
                message=f'Dashboard missing {missing}/{len(lead_files)} leads',
                file_a=str(dashboard),
                file_b=str(leads_dir),
                detail=f'{leads_in_dashboard} leads shown, {missing} not referenced'
            ))
        else:
            self._log(f"   ✅ Dashboard covers all {len(lead_files)} leads")
    
    def check_patterns_vs_implementations(self):
        """Check pattern library matches actual tools."""
        self._log("\n🔍 Checking pattern library vs implementations...")
        
        pattern_lib = self.vault_path / 'rooms/skills/pattern-library.md'
        tools_dir = self.vault_path / 'rooms/skills'
        
        if not pattern_lib.exists():
            self.issues.append(Inconsistency(
                severity='info',
                category='documentation',
                message='Pattern library not found',
                file_a=str(pattern_lib),
                file_b='',
                detail='Cannot check if patterns are implemented'
            ))
            return
        
        # Extract pattern names from library
        lib_content = pattern_lib.read_text()
        pattern_names = re.findall(r'### Pattern \d+: (.+)', lib_content)
        
        # Check which have .py implementations
        implemented = []
        not_implemented = []
        
        for pattern in pattern_names:
            # Look for any .py file that might implement this
            pattern_slug = pattern.lower().replace(' ', '-')
            # Strip parenthetical content for matching
            pattern_clean = re.sub(r'\s*\([^)]+\)', '', pattern).lower().strip()
            found = False
            for py_file in tools_dir.rglob('*.py'):
                # Check filename
                if pattern_slug in py_file.name.lower() or pattern_clean in py_file.name.lower():
                    found = True
                    break
                # Check file content
                try:
                    content = py_file.read_text()
                    if pattern.lower() in content.lower() or pattern_clean in content.lower():
                        found = True
                        break
                except:
                    pass
            
            if found:
                implemented.append(pattern)
            else:
                not_implemented.append(pattern)
        
        if not_implemented:
            self.issues.append(Inconsistency(
                severity='info',
                category='documentation',
                message=f'{len(not_implemented)} patterns in library without clear implementation',
                file_a=str(pattern_lib),
                file_b=str(tools_dir),
                detail=f'Not found: {", ".join(not_implemented[:3])}'
            ))
        else:
            self._log(f"   ✅ All {len(implemented)} patterns have implementations")
    
    def check_debates_vs_leads(self):
        """Check debate files reference valid leads."""
        self._log("\n🔍 Checking debates vs leads...")
        
        leads_dir = self.vault_path / 'wings/StandoutLocal/leads'
        debates_dir = self.vault_path / 'wings/StandoutLocal/debates'
        
        if not debates_dir.exists() or not debates_dir.glob('*.md'):
            self._log("   ℹ️  No debates directory yet")
            return
        
        valid_leads = set()
        if leads_dir.exists():
            for lead_file in leads_dir.glob('*.md'):
                valid_leads.add(lead_file.stem)
        
        orphaned = []
        for debate_file in debates_dir.glob('*.md'):
            try:
                content = debate_file.read_text()
                match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
                if match:
                    fm = yaml.safe_load(match.group(1))
                    lead = fm.get('lead', '')
                    lead_slug = lead.lower().replace(' ', '-')
                    
                    if lead_slug and not any(lead_slug in vl for vl in valid_leads):
                        orphaned.append((debate_file.name, lead))
            except:
                pass
        
        if orphaned:
            self.issues.append(Inconsistency(
                severity='warning',
                category='references',
                message=f'{len(orphaned)} debate files reference missing leads',
                file_a=str(debates_dir),
                file_b=str(leads_dir),
                detail=f'Orphaned: {", ".join(f"{o[0]} → {o[1]}" for o in orphaned)}'
            ))
        else:
            self._log("   ✅ All debates reference valid leads")
    
    def check_audits_vs_sources(self):
        """Check audit files have source URLs."""
        self._log("\n🔍 Checking audits for source URLs...")
        
        audits_dir = self.vault_path / 'wings/StandoutLocal/audits'
        
        if not audits_dir.exists():
            self._log("   ℹ️  No audits directory yet")
            return
        
        missing_url = []
        for audit_file in audits_dir.glob('*.md'):
            try:
                content = audit_file.read_text()
                match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
                if match:
                    fm = yaml.safe_load(match.group(1))
                    if not fm.get('url'):
                        missing_url.append(audit_file.name)
            except:
                missing_url.append(audit_file.name)
        
        if missing_url:
            self.issues.append(Inconsistency(
                severity='info',
                category='metadata',
                message=f'{len(missing_url)} audit files missing source URL',
                file_a=str(audits_dir),
                file_b='',
                detail=f'Missing URL: {", ".join(missing_url[:3])}'
            ))
        else:
            self._log("   ✅ All audits have source URLs")
    
    def _extract_required_sections(self, content: str) -> List[str]:
        """Extract required section names from LEAD_SYSTEM.md.
        
        Only extracts sections that describe lead file structure,
        skipping documentation/instructional sections."""
        sections = []
        # Only extract sections that are part of lead file format
        # Skip: How It Works, The Promise, etc.
        skip_keywords = [
            'how it works', 'the promise', 'when nathan',
            'every lead gets', 'scoring rubric', 'derived scores'
        ]
        
        for match in re.finditer(r'## ([A-Z][A-Za-z\s]+)', content):
            section = match.group(1).strip()
            # Skip if it contains instructional keywords
            if any(skip in section.lower() for skip in skip_keywords):
                continue
            # Only include sections that describe file parts
            if any(keyword in section.lower() for keyword in 
                   ['lead file', 'format', 'section', 'required', 'schema']):
                sections.append(section)
        
        return sections
    
    def generate_report(self) -> str:
        """Generate markdown report."""
        report = f"""---
date: 2026-05-11
type: cross-artifact-analysis
---

# Cross-Artifact Analysis Report

## Summary

| Metric | Value |
|---|---|
| Total Issues | {len(self.issues)} |
| Critical | {len([i for i in self.issues if i.severity == 'critical'])} |
| Warnings | {len([i for i in self.issues if i.severity == 'warning'])} |
| Info | {len([i for i in self.issues if i.severity == 'info'])} |

## Issues Found

"""
        
        if not self.issues:
            report += "✅ **No inconsistencies found. All artifacts are consistent.**\n"
        else:
            for issue in sorted(self.issues, key=lambda x: {'critical': 0, 'warning': 1, 'info': 2}[x.severity]):
                icon = "🔴" if issue.severity == 'critical' else "⚠️" if issue.severity == 'warning' else "ℹ️"
                report += f"### {icon} {issue.category.title()}: {issue.message}\n\n"
                report += f"- **File A:** `{issue.file_a}`\n"
                if issue.file_b:
                    report += f"- **File B:** `{issue.file_b}`\n"
                report += f"- **Detail:** {issue.detail}\n\n"
        
        report += "---\n*Run `python cross-artifact-analyzer.py` to refresh.*\n"
        
        return report
    
    def save_report(self, output_path: str = None):
        """Save report to vault."""
        output = Path(output_path or self.vault_path / 'wings/StandoutLocal/consistency-report.md')
        output.parent.mkdir(parents=True, exist_ok=True)
        
        report = self.generate_report()
        output.write_text(report)
        
        self._log(f"\n💾 Report saved to: {output}")
        return str(output)


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Cross-artifact consistency analyzer')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--print', '-p', action='store_true', help='Print to stdout only')
    
    args = parser.parse_args()
    
    analyzer = CrossArtifactAnalyzer(verbose=True)
    issues = analyzer.analyze_all()
    
    if args.print:
        print(analyzer.generate_report())
    else:
        analyzer.save_report(args.output)
    
    # Exit with error code if critical issues found
    critical_count = len([i for i in issues if i.severity == 'critical'])
    if critical_count > 0:
        print(f"\n❌ {critical_count} critical issues found")
        sys.exit(1)
    
    warning_count = len([i for i in issues if i.severity == 'warning'])
    if warning_count > 0:
        print(f"\n⚠️  {warning_count} warnings found")
        sys.exit(2)  # Different exit code for warnings
    
    print("\n✅ All checks passed")
    sys.exit(0)


if __name__ == '__main__':
    main()
