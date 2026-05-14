#!/usr/bin/env python3
"""
Lead File Validator
Pattern: Structured Output with Validation (from awesome-llm-apps)
Source: advanced_ai_agents/structured_output/

Validates Standout Local lead files against LEAD_SYSTEM.md schema.
"""

import re
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from urllib.parse import urlparse

class LeadValidator:
    """Validates lead markdown files against the Standout Local schema."""
    
    REQUIRED_FRONTMATTER = [
        'date', 'source', 'status', 'score', 
        'opportunity', 'pain', 'reach', 'fit'
    ]
    
    REQUIRED_SECTIONS = [
        'Business Info',
        'Website Audit',
        'Pain Points Found',
        'Outreach Hook',
        'Demo Page Concept',
        'Outreach Status'
    ]
    
    SCORE_FIELDS = ['score', 'opportunity', 'pain', 'reach', 'fit']
    
    VALID_STATUSES = [
        'discovered', 'scored', 'outreached', 
        'responded', 'converted', 'dead'
    ]
    
    RUBRIC_CATEGORIES = [
        'Mobile-first', 'Speed', 'CTAs', 'Trust signals',
        'Differentiation', 'Content', 'Conversion', 'TOTAL'
    ]
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.fixes_applied: List[str] = []
    
    def _log(self, msg: str):
        if self.verbose:
            print(msg)
    
    def parse_frontmatter(self, content: str) -> Tuple[Optional[Dict], str]:
        """Extract YAML frontmatter and body from markdown."""
        pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
        match = re.match(pattern, content, re.DOTALL)
        
        if not match:
            self.errors.append("Missing YAML frontmatter (--- delimiters)")
            return None, content
        
        try:
            frontmatter = yaml.safe_load(match.group(1))
            body = match.group(2)
            return frontmatter, body
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML frontmatter: {e}")
            return None, content
    
    def validate_frontmatter(self, fm: Dict) -> bool:
        """Validate frontmatter fields."""
        valid = True
        
        # Check required fields
        for field in self.REQUIRED_FRONTMATTER:
            if field not in fm:
                self.errors.append(f"Missing frontmatter field: '{field}'")
                valid = False
        
        # Validate score ranges (allow None for discovered leads)
        for field in self.SCORE_FIELDS:
            if field in fm:
                val = fm[field]
                if val is None:
                    # Allow None for early-stage leads
                    if fm.get('status') not in ['discovered', 'scored']:
                        self.warnings.append(f"'{field}' is empty — lead may need scoring")
                elif not isinstance(val, (int, float)):
                    self.errors.append(f"'{field}' must be numeric or null, got {type(val).__name__}")
                    valid = False
                elif not (0 <= val <= 100):
                    self.errors.append(f"'{field}' must be 0-100, got {val}")
                    valid = False
        
        # Validate status
        if 'status' in fm and fm['status'] not in self.VALID_STATUSES:
            self.warnings.append(
                f"Status '{fm['status']}' not in standard list: {self.VALID_STATUSES}"
            )
        
        # Validate date format
        if 'date' in fm:
            date_str = str(fm['date'])
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                self.warnings.append(f"Date '{date_str}' not in YYYY-MM-DD format")
        
        return valid
    
    def validate_sections(self, body: str) -> bool:
        """Check all required sections exist (flexible matching)."""
        valid = True
        
        for section in self.REQUIRED_SECTIONS:
            # Flexible: allow section name followed by anything on same line
            pattern = rf'^##\s+{re.escape(section)}(?:\s|$)'
            if not re.search(pattern, body, re.MULTILINE):
                self.errors.append(f"Missing required section: '## {section}'")
                valid = False
        
        return valid
    
    def validate_rubric_table(self, body: str) -> bool:
        """Validate the 100-point rubric table."""
        valid = True
        
        # Find the table
        table_pattern = r'\| Category \| Score \| Notes \|.*?\n\|?---.*?\n(.*?)(?:\n##|\Z)'
        match = re.search(table_pattern, body, re.DOTALL)
        
        if not match:
            self.errors.append("Website Audit rubric table not found or malformed")
            return False
        
        table_content = match.group(1)
        
        # Check categories
        found_categories = []
        for line in table_content.strip().split('\n'):
            if '|' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 2 and parts[1] and parts[1] != 'Category':
                    found_categories.append(parts[1])
        
        # Check for TOTAL row
        if 'TOTAL' not in [c for c in found_categories]:
            self.warnings.append("Rubric table missing 'TOTAL' row")
        
        return valid
    
    def validate_business_info(self, body: str) -> bool:
        """Validate Business Info section has key fields."""
        valid = True
        
        info_section_pattern = r'## Business Info\s*\n(.*?)(?=\n## |\Z)'
        match = re.search(info_section_pattern, body, re.DOTALL)
        
        if not match:
            self.errors.append("Business Info section content not found")
            return False
        
        info_content = match.group(1)
        
        # Check for key fields
        key_fields = ['Name:', 'Category:', 'Address:', 'Phone:']
        for field in key_fields:
            if field not in info_content:
                self.warnings.append(f"Business Info missing '{field}'")
        
        # Check phone format
        phone_match = re.search(r'\*\*Phone:\*\*\s*(.+)', info_content)
        if phone_match:
            phone = phone_match.group(1).strip()
            if not re.match(r'[\(\)\d\s\-+.]+', phone):
                self.warnings.append(f"Phone number format unusual: {phone}")
        
        return valid
    
    def validate_outreach_status(self, body: str) -> bool:
        """Check Outreach Status has checkboxes."""
        status_section = re.search(
            r'## Outreach Status\s*\n(.*?)(?=\n## |\Z)',
            body, re.DOTALL
        )
        
        if not status_section:
            return False
        
        content = status_section.group(1)
        
        # Count checkboxes
        checked = len(re.findall(r'- \[x\]', content, re.IGNORECASE))
        unchecked = len(re.findall(r'- \[ \]', content))
        
        if checked + unchecked == 0:
            self.warnings.append("Outreach Status section has no checkboxes")
        
        return True
    
    def auto_fix(self, content: str, fm: Dict, body: str) -> str:
        """Attempt to fix common issues."""
        fixed = content
        
        # Fix missing date format
        if 'date' in fm:
            date_val = fm['date']
            if isinstance(date_val, str) and not re.match(r'^\d{4}-\d{2}-\d{2}$', date_val):
                # Try to parse and reformat
                pass  # Complex, skip for now
        
        return fixed
    
    def validate(self, filepath: str) -> Dict:
        """Full validation of a lead file."""
        path = Path(filepath)
        
        self._log(f"\n{'='*60}")
        self._log(f"VALIDATING: {path.name}")
        self._log(f"{'='*60}")
        
        if not path.exists():
            self.errors.append(f"File not found: {filepath}")
            return self._result(path.name, False)
        
        content = path.read_text()
        
        # Parse
        fm, body = self.parse_frontmatter(content)
        if fm is None:
            return self._result(path.name, False)
        
        # Validate frontmatter
        fm_valid = self.validate_frontmatter(fm)
        
        # Validate sections
        sections_valid = self.validate_sections(body)
        
        # Validate rubric
        rubric_valid = self.validate_rubric_table(body)
        
        # Validate business info
        biz_valid = self.validate_business_info(body)
        
        # Validate outreach status
        status_valid = self.validate_outreach_status(body)
        
        # Summary
        all_valid = fm_valid and sections_valid and rubric_valid and biz_valid and status_valid
        
        return self._result(path.name, all_valid, fm)
    
    def _result(self, filename: str, valid: bool, fm: Dict = None) -> Dict:
        """Generate validation result."""
        result = {
            'filename': filename,
            'valid': valid and len(self.errors) == 0,
            'errors': self.errors.copy(),
            'warnings': self.warnings.copy(),
            'fixes': self.fixes_applied.copy(),
            'score': fm.get('score', 'N/A') if fm else 'N/A',
            'status': fm.get('status', 'N/A') if fm else 'N/A'
        }
        
        self._log(f"\n{'='*60}")
        self._log(f"RESULT: {'✅ PASS' if result['valid'] else '❌ FAIL'}")
        self._log(f"{'='*60}")
        self._log(f"Errors: {len(self.errors)}")
        for e in self.errors:
            self._log(f"  ❌ {e}")
        self._log(f"Warnings: {len(self.warnings)}")
        for w in self.warnings:
            self._log(f"  ⚠️  {w}")
        
        return result
    
    def reset(self):
        """Reset validation state for next file."""
        self.errors = []
        self.warnings = []
        self.fixes_applied = []


def validate_directory(directory: str) -> List[Dict]:
    """Validate all lead files in a directory."""
    validator = LeadValidator(verbose=True)
    results = []
    
    path = Path(directory)
    lead_files = list(path.glob('*.md'))
    
    print(f"\n{'#'*60}")
    print(f"LEAD VALIDATION BATCH: {len(lead_files)} files")
    print(f"{'#'*60}")
    
    for lead_file in sorted(lead_files):
        validator.reset()
        result = validator.validate(str(lead_file))
        results.append(result)
    
    # Summary
    passed = sum(1 for r in results if r['valid'])
    failed = len(results) - passed
    
    print(f"\n{'#'*60}")
    print(f"BATCH SUMMARY: {passed}/{len(results)} passed")
    print(f"{'#'*60}")
    
    if failed > 0:
        print("\nFAILED FILES:")
        for r in results:
            if not r['valid']:
                print(f"  ❌ {r['filename']}: {len(r['errors'])} errors")
    
    return results


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Validate single file
        validator = LeadValidator(verbose=True)
        result = validator.validate(sys.argv[1])
        sys.exit(0 if result['valid'] else 1)
    else:
        # Validate all leads in default directory
        leads_dir = '/root/.openclaw/workspace/vault/wings/StandoutLocal/leads'
        results = validate_directory(leads_dir)
        
        # Exit with error if any failed
        failed = sum(1 for r in results if not r['valid'])
        sys.exit(0 if failed == 0 else 1)
