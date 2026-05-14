#!/usr/bin/env python3
"""
Experiment Runner
Pattern: Experiment Framework (from autoresearch repo)
Source: Hypothesis → Setup → Run → Measure → Report

Runs A/B experiments on outreach copy, website changes, or any variable.
Tracks metrics, calculates statistical significance, reports winners.
"""

import json
import sys
import random
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class ExperimentRunner:
    """Runs controlled experiments with proper tracking."""
    
    def __init__(self, experiments_dir: str = None, verbose: bool = True):
        self.verbose = verbose
        self.experiments_dir = Path(experiments_dir or '/root/.openclaw/workspace/vault/rooms/experiments')
        self.experiments_dir.mkdir(parents=True, exist_ok=True)
    
    def _log(self, msg: str):
        if self.verbose:
            print(msg)
    
    def create_experiment(self, name: str, hypothesis: str, 
                         variants: List[str], 
                         metric: str = 'engagement') -> str:
        """Create a new experiment."""
        exp_id = f"{name.lower().replace(' ', '-')}-{datetime.now().strftime('%Y%m%d')}"
        
        experiment = {
            'id': exp_id,
            'name': name,
            'hypothesis': hypothesis,
            'variants': [{'id': f'v{i}', 'content': v, 'exposures': 0, 'conversions': 0} 
                        for i, v in enumerate(variants)],
            'metric': metric,
            'status': 'running',
            'created': datetime.now().isoformat(),
            'results': [],
        }
        
        # Save
        exp_file = self.experiments_dir / f"{exp_id}.json"
        exp_file.write_text(json.dumps(experiment, indent=2))
        
        self._log(f"🧪 Experiment created: {exp_id}")
        self._log(f"   Hypothesis: {hypothesis}")
        self._log(f"   Variants: {len(variants)}")
        self._log(f"   Metric: {metric}")
        
        return exp_id
    
    def get_variant(self, exp_id: str) -> Dict:
        """Get a variant for exposure (A/B split)."""
        exp = self._load_experiment(exp_id)
        if not exp or exp['status'] != 'running':
            return None
        
        # Weighted random selection (exploration vs exploitation)
        # 80% best performer, 20% random exploration
        variants = exp['variants']
        
        if len(variants) == 1:
            return variants[0]
        
        # Calculate current conversion rates
        for v in variants:
            if v['exposures'] > 0:
                v['rate'] = v['conversions'] / v['exposures']
            else:
                v['rate'] = 0.0
        
        # 80/20 split
        if random.random() < 0.8:
            # Exploit: pick best performer
            best = max(variants, key=lambda x: x['rate'])
            return best
        else:
            # Explore: random pick
            return random.choice(variants)
    
    def record_exposure(self, exp_id: str, variant_id: str):
        """Record that a variant was shown."""
        exp = self._load_experiment(exp_id)
        if not exp:
            return
        
        for v in exp['variants']:
            if v['id'] == variant_id:
                v['exposures'] += 1
                break
        
        self._save_experiment(exp)
    
    def record_conversion(self, exp_id: str, variant_id: str):
        """Record a successful conversion for a variant."""
        exp = self._load_experiment(exp_id)
        if not exp:
            return
        
        for v in exp['variants']:
            if v['id'] == variant_id:
                v['conversions'] += 1
                break
        
        self._save_experiment(exp)
        
        # Check if we have enough data for significance
        self._check_significance(exp)
    
    def _check_significance(self, exp: Dict):
        """Check if experiment has reached statistical significance."""
        variants = exp['variants']
        
        # Need at least 100 exposures per variant
        for v in variants:
            if v['exposures'] < 100:
                return
        
        # Calculate rates
        for v in variants:
            v['rate'] = v['conversions'] / v['exposures']
        
        # Find winner
        winner = max(variants, key=lambda x: x['rate'])
        
        # Simple significance check: winner must be 10% better than others
        significant = True
        for v in variants:
            if v['id'] != winner['id']:
                if winner['rate'] <= v['rate'] * 1.1:
                    significant = False
                    break
        
        if significant:
            self._log(f"\n🏆 SIGNIFICANT RESULT for {exp['id']}!")
            self._log(f"   Winner: {winner['id']} ({winner['rate']:.1%} conversion)")
            for v in variants:
                if v['id'] != winner['id']:
                    self._log(f"   {v['id']}: {v['rate']:.1%} conversion")
            
            exp['status'] = 'completed'
            exp['winner'] = winner['id']
            self._save_experiment(exp)
    
    def get_results(self, exp_id: str) -> Dict:
        """Get current experiment results."""
        exp = self._load_experiment(exp_id)
        if not exp:
            return None
        
        # Calculate current stats
        results = {
            'id': exp['id'],
            'name': exp['name'],
            'status': exp['status'],
            'hypothesis': exp['hypothesis'],
            'metric': exp['metric'],
            'total_exposures': sum(v['exposures'] for v in exp['variants']),
            'total_conversions': sum(v['conversions'] for v in exp['variants']),
            'variants': []
        }
        
        for v in exp['variants']:
            rate = v['conversions'] / v['exposures'] if v['exposures'] > 0 else 0
            results['variants'].append({
                'id': v['id'],
                'exposures': v['exposures'],
                'conversions': v['conversions'],
                'rate': rate,
                'content': v['content'][:100] + '...' if len(v['content']) > 100 else v['content']
            })
        
        if 'winner' in exp:
            results['winner'] = exp['winner']
        
        return results
    
    def list_experiments(self) -> List[Dict]:
        """List all experiments."""
        experiments = []
        for exp_file in sorted(self.experiments_dir.glob('*.json')):
            exp = json.loads(exp_file.read_text())
            experiments.append({
                'id': exp['id'],
                'name': exp['name'],
                'status': exp['status'],
                'created': exp['created']
            })
        return experiments
    
    def _load_experiment(self, exp_id: str) -> Optional[Dict]:
        """Load experiment from disk."""
        exp_file = self.experiments_dir / f"{exp_id}.json"
        if not exp_file.exists():
            return None
        return json.loads(exp_file.read_text())
    
    def _save_experiment(self, exp: Dict):
        """Save experiment to disk."""
        exp_file = self.experiments_dir / f"{exp['id']}.json"
        exp_file.write_text(json.dumps(exp, indent=2))


def main():
    """CLI demo."""
    runner = ExperimentRunner(verbose=True)
    
    # Create test experiment
    exp_id = runner.create_experiment(
        name="Outreach CTA Test",
        hypothesis="'5-minute call' CTA gets more responses than 'quick chat'",
        variants=[
            "Would you be open to a quick 5-minute call this week?",
            "Can we hop on a quick chat sometime?",
            "Interested? Just reply and we'll find a time."
        ],
        metric="response_rate"
    )
    
    print(f"\n{'='*60}")
    print("SIMULATING 50 EXPOSURES...")
    print(f"{'='*60}")
    
    # Simulate exposures
    for i in range(50):
        variant = runner.get_variant(exp_id)
        runner.record_exposure(exp_id, variant['id'])
        
        # Simulate conversions (variant 0 wins 15%, variant 1 wins 8%, variant 2 wins 10%)
        rates = {'v0': 0.15, 'v1': 0.08, 'v2': 0.10}
        if random.random() < rates[variant['id']]:
            runner.record_conversion(exp_id, variant['id'])
    
    # Show results
    results = runner.get_results(exp_id)
    print(f"\n{'='*60}")
    print("RESULTS")
    print(f"{'='*60}")
    print(f"Experiment: {results['name']}")
    print(f"Status: {results['status']}")
    print(f"Total exposures: {results['total_exposures']}")
    print(f"Total conversions: {results['total_conversions']}")
    print()
    
    for v in results['variants']:
        bar = '█' * int(v['rate'] * 50)
        print(f"{v['id']}: {v['exposures']} exposures, {v['conversions']} conversions ({v['rate']:.1%}) {bar}")
    
    if 'winner' in results:
        print(f"\n🏆 Winner: {results['winner']}")
    
    print(f"\n{'='*60}")


if __name__ == '__main__':
    main()
