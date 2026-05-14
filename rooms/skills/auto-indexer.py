#!/usr/bin/env python3
"""
Semantic Search Auto-Index
Pattern: Auto-Index (from awesome-llm-apps vector_dbs_and_search_tools/)
Source: Watch → Detect Change → Rebuild Index → Notify

Watches vault markdown files and automatically rebuilds semantic search index
when files are added, modified, or deleted.
"""

import os
import sys
import time
import hashlib
import json
from pathlib import Path
from typing import Dict, Set
from datetime import datetime

VAULT_PATH = "/root/.openclaw/workspace/vault"
DB_PATH = "/root/.openclaw/workspace/.clawdbot/vault-search.db"
WATCH_INTERVAL = 60  # seconds

class AutoIndexer:
    """Watches vault and auto-rebuilds search index."""
    
    def __init__(self, vault_path: str = None, db_path: str = None, 
                 interval: int = 60, verbose: bool = True):
        self.vault_path = Path(vault_path or VAULT_PATH)
        self.db_path = Path(db_path or DB_PATH)
        self.interval = interval
        self.verbose = verbose
        self.file_hashes: Dict[str, str] = {}
        self.state_file = self.db_path.parent / 'auto-index-state.json'
        
        # Load previous state
        self._load_state()
    
    def _log(self, msg: str):
        if self.verbose:
            print(msg)
    
    def _load_state(self):
        """Load file hash state from disk."""
        if self.state_file.exists():
            self.file_hashes = json.loads(self.state_file.read_text())
    
    def _save_state(self):
        """Save file hash state to disk."""
        self.state_file.write_text(json.dumps(self.file_hashes, indent=2))
    
    def _hash_file(self, path: str) -> str:
        """Compute MD5 hash of file content."""
        try:
            with open(path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return ''
    
    def scan_vault(self) -> Dict[str, str]:
        """Scan vault for all markdown files."""
        files = {}
        for md_file in self.vault_path.rglob('*.md'):
            # Skip node_modules, .git, .venv, repo-research
            path_str = str(md_file)
            if any(skip in path_str for skip in ['node_modules', '.git', '.venv', 'repo-research']):
                continue
            
            rel_path = os.path.relpath(path_str, self.vault_path)
            files[rel_path] = self._hash_file(path_str)
        
        return files
    
    def detect_changes(self, current: Dict[str, str]) -> Dict:
        """Detect added, modified, deleted files."""
        added = [f for f in current if f not in self.file_hashes]
        deleted = [f for f in self.file_hashes if f not in current]
        modified = [f for f in current if f in self.file_hashes and current[f] != self.file_hashes[f]]
        
        return {
            'added': added,
            'deleted': deleted,
            'modified': modified,
            'total': len(current),
            'changed': len(added) + len(deleted) + len(modified)
        }
    
    def rebuild_index(self):
        """Trigger index rebuild by running vault_semantic_search.py."""
        import subprocess
        
        script_path = self.db_path.parent / 'vault_semantic_search.py'
        if not script_path.exists():
            self._log(f"⚠️  Index script not found: {script_path}")
            return False
        
        self._log("🔨 Rebuilding search index...")
        try:
            result = subprocess.run(
                [sys.executable, str(script_path), 'index'],
                cwd=str(script_path.parent),
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                self._log("✅ Index rebuilt successfully")
                return True
            else:
                self._log(f"⚠️  Index rebuild failed: {result.stderr[:200]}")
                return False
                
        except Exception as e:
            self._log(f"⚠️  Error rebuilding index: {e}")
            return False
    
    def run_once(self) -> bool:
        """Run one scan cycle. Returns True if changes detected."""
        current = self.scan_vault()
        changes = self.detect_changes(current)
        
        if changes['changed'] > 0:
            self._log(f"\n🔄 Changes detected at {datetime.now().strftime('%H:%M:%S')}")
            if changes['added']:
                self._log(f"   + Added: {len(changes['added'])} files")
                for f in changes['added'][:3]:
                    self._log(f"      + {f}")
                if len(changes['added']) > 3:
                    self._log(f"      ... and {len(changes['added']) - 3} more")
            
            if changes['modified']:
                self._log(f"   ~ Modified: {len(changes['modified'])} files")
                for f in changes['modified'][:3]:
                    self._log(f"      ~ {f}")
                if len(changes['modified']) > 3:
                    self._log(f"      ... and {len(changes['modified']) - 3} more")
            
            if changes['deleted']:
                self._log(f"   - Deleted: {len(changes['deleted'])} files")
            
            # Update state
            self.file_hashes = current
            self._save_state()
            
            # Rebuild index
            self.rebuild_index()
            
            return True
        
        return False
    
    def watch(self, max_cycles: int = None):
        """Watch vault continuously."""
        self._log(f"👁️  Watching: {self.vault_path}")
        self._log(f"   Interval: {self.interval}s")
        self._log(f"   Press Ctrl+C to stop\n")
        
        cycle = 0
        try:
            while True:
                changed = self.run_once()
                
                if not changed:
                    self._log(f"✓ {datetime.now().strftime('%H:%M:%S')} — No changes ({self.file_hashes.__len__()} files)")
                
                cycle += 1
                if max_cycles and cycle >= max_cycles:
                    break
                
                time.sleep(self.interval)
                
        except KeyboardInterrupt:
            self._log("\n\n👋 Stopped by user")
            self._save_state()
    
    def status(self):
        """Show current watch status."""
        current = self.scan_vault()
        changes = self.detect_changes(current)
        
        print(f"{'='*60}")
        print(f"Auto-Index Status")
        print(f"{'='*60}")
        print(f"Vault path: {self.vault_path}")
        print(f"Database: {self.db_path}")
        print(f"Tracked files: {len(self.file_hashes)}")
        print(f"Current files: {len(current)}")
        print(f"Pending changes: {changes['changed']}")
        
        if changes['added']:
            print(f"\nNew files ({len(changes['added'])}):")
            for f in changes['added'][:5]:
                print(f"  + {f}")
        
        if changes['modified']:
            print(f"\nModified files ({len(changes['modified'])}):")
            for f in changes['modified'][:5]:
                print(f"  ~ {f}")
        
        print(f"{'='*60}")


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Auto-index vault semantic search')
    parser.add_argument('command', choices=['watch', 'once', 'status'], 
                       help='Command to run')
    parser.add_argument('--interval', type=int, default=60,
                       help='Watch interval in seconds')
    
    args = parser.parse_args()
    
    indexer = AutoIndexer(interval=args.interval, verbose=True)
    
    if args.command == 'watch':
        indexer.watch()
    elif args.command == 'once':
        indexer.run_once()
    elif args.command == 'status':
        indexer.status()


if __name__ == '__main__':
    main()
