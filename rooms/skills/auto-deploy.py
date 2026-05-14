#!/usr/bin/env python3
"""
Auto-Deploy to Vercel
Pattern: CI/CD Integration (from OpenClaw deployment workflow)
Source: Push demo sites to Vercel automatically on spec completion

Automatically deploys Standout Local demo pages to Vercel:
- Takes a project directory (demo site)
- Uses Vercel CLI to deploy
- Updates lead file with deployment URL
- Updates dashboard

Usage: python auto-deploy.py <project-dir> [--lead <lead-file.md>] [--prod]

Requires: Vercel CLI (npm i -g vercel) + token in env
"""

import os
import sys
import re
import json
import yaml
import subprocess
from pathlib import Path
from typing import Dict, Optional, Tuple
from datetime import datetime

class VercelAutoDeploy:
    """Auto-deploy demo sites to Vercel."""
    
    def __init__(self, vault_path: str = None, verbose: bool = True):
        self.vault_path = Path(vault_path or '/root/.openclaw/workspace/vault')
        self.verbose = verbose
        self.results = {
            'deployed': False,
            'url': '',
            'errors': [],
            'logs': []
        }
    
    def _log(self, msg: str):
        if self.verbose:
            print(msg)
        self.results['logs'].append(msg)
    
    def deploy(self, project_dir: str, lead_file: str = None, prod: bool = False) -> Dict:
        """Deploy project to Vercel."""
        project_path = Path(project_dir)
        
        self._log(f"\n{'='*60}")
        self._log(f"VERCEL AUTO-DEPLOY")
        self._log(f"{'='*60}")
        self._log(f"Project: {project_path}")
        
        if not project_path.exists():
            self.results['errors'].append(f"Project directory not found: {project_dir}")
            self._log(f"❌ {self.results['errors'][-1]}")
            return self.results
        
        # Check Vercel CLI
        if not self._check_vercel_cli():
            return self.results
        
        # Check auth
        if not self._check_vercel_auth():
            return self.results
        
        # Deploy
        deploy_result = self._run_vercel_deploy(project_path, prod)
        
        if not deploy_result['success']:
            self.results['errors'].append(f"Deploy failed: {deploy_result.get('error', 'unknown')}")
            return self.results
        
        self.results['deployed'] = True
        self.results['url'] = deploy_result['url']
        
        self._log(f"\n🚀 DEPLOYED: {deploy_result['url']}")
        
        # Update lead file if provided
        if lead_file:
            self._update_lead(lead_file, deploy_result['url'])
        
        # Update dashboard
        self._update_dashboard(deploy_result['url'])
        
        return self.results
    
    def _check_vercel_cli(self) -> bool:
        """Check if Vercel CLI is installed."""
        result = subprocess.run(
            ['which', 'vercel'],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            self.results['errors'].append("Vercel CLI not found. Install: npm i -g vercel")
            self._log("❌ Vercel CLI not installed")
            self._log("   Install: npm i -g vercel")
            return False
        
        self._log("   ✅ Vercel CLI found")
        return True
    
    def _check_vercel_auth(self) -> bool:
        """Check if authenticated with Vercel."""
        result = subprocess.run(
            ['vercel', 'whoami'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            # Try with token from env
            token = os.environ.get('VERCEL_TOKEN', '')
            if not token:
                # Check TOOLS.md for token
                tools_md = self.vault_path.parent / 'TOOLS.md'
                if tools_md.exists():
                    content = tools_md.read_text()
                    match = re.search(r'Token:\s*`?([^`\s]+)`?', content)
                    if match:
                        token = match.group(1)
            
            if token:
                self._log("   ℹ️  Using token from TOOLS.md")
                # Set env for subsequent calls
                os.environ['VERCEL_TOKEN'] = token
                return True
            else:
                self.results['errors'].append("Not authenticated with Vercel. Run: vercel login")
                self._log("❌ Not authenticated with Vercel")
                self._log("   Run: vercel login")
                return False
        
        username = result.stdout.strip()
        self._log(f"   ✅ Authenticated as: {username}")
        return True
    
    def _run_vercel_deploy(self, project_path: Path, prod: bool = False) -> Dict:
        """Run vercel deploy command."""
        cmd = ['vercel', '--yes']
        
        if prod:
            cmd.append('--prod')
        
        # Add token if available
        token = os.environ.get('VERCEL_TOKEN', '')
        if token:
            cmd.extend(['--token', token])
        
        cmd.append(str(project_path))
        
        self._log(f"   🚀 Deploying...")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(project_path)
            )
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Deploy timed out after 120s'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
        
        output = result.stdout + result.stderr
        
        # Extract URL from output
        url_match = re.search(r'https?://[a-zA-Z0-9\-\.]+\.vercel\.app', output)
        
        if url_match and result.returncode == 0:
            return {
                'success': True,
                'url': url_match.group(0),
                'output': output[:500]
            }
        elif url_match:
            # Sometimes vercel returns 0 but warns, still gives URL
            return {
                'success': True,
                'url': url_match.group(0),
                'output': output[:500]
            }
        else:
            return {
                'success': False,
                'error': f'No deployment URL found. Output: {output[:300]}',
                'output': output[:500]
            }
    
    def _update_lead(self, lead_file: str, deploy_url: str):
        """Update lead file with deployment URL."""
        lead_path = Path(lead_file)
        
        if not lead_path.exists():
            self._log(f"   ℹ️  Lead file not found: {lead_file}")
            return False
        
        content = lead_path.read_text()
        
        # Check if already has deploy URL
        if deploy_url in content:
            self._log(f"   ℹ️  Deploy URL already in lead file")
            return True
        
        # Add deploy URL to frontmatter
        pattern = r'^(---\s*\n.*?\n---)\s*\n(.*)$'
        match = re.match(pattern, content, re.DOTALL)
        
        if match:
            frontmatter_text = match.group(1)
            body = match.group(2)
            
            fm = yaml.safe_load(frontmatter_text.replace('---', ''))
            fm['demo_url'] = deploy_url
            fm['deployed_at'] = datetime.now().strftime('%Y-%m-%d')
            
            new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True).strip()
            new_content = f"---\n{new_fm}\n---\n{body}"
            
            lead_path.write_text(new_content)
            self._log(f"   💾 Updated lead file with deploy URL")
            return True
        
        return False
    
    def _update_dashboard(self, deploy_url: str):
        """Update dashboard with new deploy."""
        dashboard_path = self.vault_path / 'wings/StandoutLocal/dashboard.md'
        
        if not dashboard_path.exists():
            self._log(f"   ℹ️  Dashboard not found")
            return False
        
        dashboard = dashboard_path.read_text()
        
        # Check if URL already in dashboard
        if deploy_url in dashboard:
            return True
        
        # Add to recent deploys section
        deploy_entry = f"\n- {deploy_url} — {datetime.now().strftime('%Y-%m-%d')}"
        
        if '## Recent Deploys' in dashboard:
            # Add after the section header
            dashboard = dashboard.replace(
                '## Recent Deploys',
                f'## Recent Deploys{deploy_entry}'
            )
        else:
            # Append new section
            dashboard += f"\n\n## Recent Deploys{deploy_entry}\n"
        
        dashboard_path.write_text(dashboard)
        self._log(f"   💾 Updated dashboard")
        return True


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Auto-deploy to Vercel')
    parser.add_argument('project_dir', help='Directory containing project to deploy')
    parser.add_argument('--lead', '-l', help='Lead file to update with deploy URL')
    parser.add_argument('--prod', action='store_true', help='Deploy to production')
    
    args = parser.parse_args()
    
    deployer = VercelAutoDeploy(verbose=True)
    results = deployer.deploy(args.project_dir, args.lead, args.prod)
    
    if results['deployed']:
        print(f"\n✅ Deployed: {results['url']}")
        sys.exit(0)
    else:
        print(f"\n❌ Deploy failed")
        for err in results['errors']:
            print(f"   {err}")
        sys.exit(1)


if __name__ == '__main__':
    main()
