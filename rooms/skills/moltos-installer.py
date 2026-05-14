#!/usr/bin/env python3
"""
MoltOS One-Command Install
Pattern: One-Command Setup (from iFixAI self-diagnostic + autoresearch bootstrap)
Source: Check Dependencies → Install Missing → Configure → Verify

Sets up MoltOS agent infrastructure in one command:
1. Check Python, pip, git
2. Install MoltOS SDK
3. Configure API keys
4. Verify connectivity
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class MoltOSInstaller:
    """One-command MoltOS installer."""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.checks = []
        self.fixes = []
    
    def _log(self, msg: str):
        if self.verbose:
            print(msg)
    
    def check_python(self) -> bool:
        """Check Python version."""
        version = sys.version_info
        ok = version.major >= 3 and version.minor >= 10
        self.checks.append({
            'name': 'Python',
            'version': f"{version.major}.{version.minor}.{version.micro}",
            'ok': ok,
            'fix': None if ok else 'Install Python 3.10+'
        })
        return ok
    
    def check_pip(self) -> bool:
        """Check pip availability."""
        try:
            result = subprocess.run(
                ['pip', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            ok = result.returncode == 0
            version = result.stdout.strip() if ok else 'Not found'
        except:
            ok = False
            version = 'Not found'
        
        self.checks.append({
            'name': 'pip',
            'version': version,
            'ok': ok,
            'fix': None if ok else 'Install pip (python -m ensurepip)'
        })
        return ok
    
    def check_git(self) -> bool:
        """Check git availability."""
        try:
            result = subprocess.run(
                ['git', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            ok = result.returncode == 0
            version = result.stdout.strip() if ok else 'Not found'
        except:
            ok = False
            version = 'Not found'
        
        self.checks.append({
            'name': 'git',
            'version': version,
            'ok': ok,
            'fix': None if ok else 'Install git'
        })
        return ok
    
    def check_moltos_sdk(self) -> bool:
        """Check if MoltOS SDK is installed."""
        try:
            import moltos
            ok = True
            version = getattr(moltos, '__version__', 'unknown')
        except ImportError:
            ok = False
            version = 'Not installed'
        
        self.checks.append({
            'name': 'moltos-sdk',
            'version': version,
            'ok': ok,
            'fix': None if ok else 'pip install moltos-sdk'
        })
        return ok
    
    def install_moltos_sdk(self) -> bool:
        """Install MoltOS SDK."""
        self._log("📦 Installing MoltOS SDK...")
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', 'moltos-sdk'],
                capture_output=True,
                text=True,
                timeout=60
            )
            ok = result.returncode == 0
            if ok:
                self._log("✅ MoltOS SDK installed")
                self.fixes.append('Installed moltos-sdk')
            else:
                self._log(f"⚠️  Install failed: {result.stderr[:200]}")
            return ok
        except Exception as e:
            self._log(f"⚠️  Install error: {e}")
            return False
    
    def configure_api_keys(self, api_key: str = None, public_key: str = None) -> bool:
        """Configure MoltOS API keys."""
        config_dir = Path.home() / '.moltos'
        config_dir.mkdir(exist_ok=True)
        
        config_file = config_dir / 'config.json'
        
        # Use provided keys or try to find them
        if not api_key:
            # Check environment
            api_key = os.environ.get('MOLTOS_API_KEY', '')
        
        if not public_key:
            public_key = os.environ.get('MOLTOS_PUBLIC_KEY', '')
        
        if not api_key:
            self._log("⚠️  No MoltOS API key found")
            self._log("   Set MOLTOS_API_KEY environment variable or pass --api-key")
            return False
        
        config = {
            'api_key': api_key,
            'public_key': public_key,
            'endpoint': 'https://moltos.org',
        }
        
        config_file.write_text(json.dumps(config, indent=2))
        os.chmod(config_file, 0o600)  # Restrict permissions
        
        self._log("🔑 API keys configured")
        self.fixes.append('Configured API keys')
        return True
    
    def verify_connectivity(self) -> bool:
        """Test MoltOS API connectivity."""
        self._log("🌐 Testing MoltOS connectivity...")
        try:
            # Simple health check
            result = subprocess.run(
                ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', 
                 'https://moltos.org/health'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            status = result.stdout.strip()
            ok = status == '200'
            
            if ok:
                self._log("✅ MoltOS is reachable")
            else:
                self._log(f"⚠️  MoltOS returned HTTP {status}")
            
            self.checks.append({
                'name': 'moltos-connectivity',
                'version': f'HTTP {status}',
                'ok': ok,
                'fix': None if ok else 'Check network or MoltOS status'
            })
            return ok
            
        except Exception as e:
            self._log(f"⚠️  Connectivity test failed: {e}")
            self.checks.append({
                'name': 'moltos-connectivity',
                'version': 'Error',
                'ok': False,
                'fix': 'Check network connection'
            })
            return False
    
    def run_all(self, api_key: str = None, public_key: str = None) -> bool:
        """Run full installation."""
        self._log(f"\n{'='*60}")
        self._log("MoltOS One-Command Install")
        self._log(f"{'='*60}\n")
        
        # Phase 1: Check
        self._log("🔍 Phase 1: Checking dependencies...")
        python_ok = self.check_python()
        pip_ok = self.check_pip()
        git_ok = self.check_git()
        sdk_ok = self.check_moltos_sdk()
        
        # Phase 2: Install
        self._log("\n🔧 Phase 2: Installing missing components...")
        if not sdk_ok and pip_ok:
            self.install_moltos_sdk()
        
        # Phase 3: Configure
        self._log("\n⚙️  Phase 3: Configuring...")
        if api_key:
            self.configure_api_keys(api_key, public_key)
        
        # Phase 4: Verify
        self._log("\n✅ Phase 4: Verification...")
        connectivity_ok = self.verify_connectivity()
        
        # Summary
        self._log(f"\n{'='*60}")
        self._log("INSTALLATION SUMMARY")
        self._log(f"{'='*60}")
        
        all_ok = True
        for check in self.checks:
            status = "✅" if check['ok'] else "❌"
            self._log(f"{status} {check['name']}: {check['version']}")
            if not check['ok']:
                all_ok = False
                if check['fix']:
                    self._log(f"   Fix: {check['fix']}")
        
        if self.fixes:
            self._log(f"\nApplied fixes:")
            for fix in self.fixes:
                self._log(f"  + {fix}")
        
        self._log(f"\n{'='*60}")
        if all_ok:
            self._log("🎉 MoltOS is ready!")
        else:
            self._log("⚠️  Some checks failed. Review above.")
        self._log(f"{'='*60}")
        
        return all_ok


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='One-command MoltOS installer')
    parser.add_argument('--api-key', help='MoltOS API key')
    parser.add_argument('--public-key', help='MoltOS public key')
    parser.add_argument('--check-only', action='store_true', help='Only check, don\'t install')
    
    args = parser.parse_args()
    
    installer = MoltOSInstaller(verbose=True)
    
    if args.check_only:
        installer.check_python()
        installer.check_pip()
        installer.check_git()
        installer.check_moltos_sdk()
        installer.verify_connectivity()
        
        print(f"\n{'='*60}")
        print("CHECK-ONLY MODE")
        print(f"{'='*60}")
        for check in installer.checks:
            status = "✅" if check['ok'] else "❌"
            print(f"{status} {check['name']}: {check['version']}")
    else:
        success = installer.run_all(args.api_key, args.public_key)
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
