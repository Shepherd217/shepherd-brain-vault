#!/usr/bin/env python3
"""
Multi-Agent Debate Engine for Lead Scoring
Pattern: Multi-Agent Team (from awesome-llm-apps multi_agent_workflows/)
Source: Agent A (Optimist) + Agent B (Pessimist) + Agent C (Realist) → Consensus

Three agents debate lead quality from different angles:
- Optimist: Sees opportunity, growth potential
- Pessimist: Sees risks, competitive threats
- Realist: Sees practical feasibility, timing

Final score = weighted average of perspectives
"""

import sys
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class AgentOpinion:
    """One agent's scoring perspective."""
    agent: str
    opportunity_score: int
    pain_score: int
    fit_score: int
    reach_score: int
    total: int
    reasoning: str

class DebateEngine:
    """Multi-agent debate for lead scoring."""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.agents = {
            'optimist': self._optimist_score,
            'pessimist': self._pessimist_score,
            'realist': self._realist_score,
        }
    
    def _log(self, msg: str):
        if self.verbose:
            print(msg)
    
    def parse_lead(self, filepath: str) -> Dict:
        """Parse lead file."""
        content = Path(filepath).read_text()
        
        # Parse frontmatter
        pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
        match = re.match(pattern, content, re.DOTALL)
        
        if not match:
            raise ValueError(f"No frontmatter in {filepath}")
        
        fm = yaml.safe_load(match.group(1))
        body = match.group(2)
        
        # Try to get name from frontmatter, fallback to Business Info section
        name = fm.get('name', '')
        if not name or name == 'Unknown':
            # Extract from Business Info
            biz_match = re.search(r'\*\*Name:\*\*\s*(.+)', body)
            if biz_match:
                name = biz_match.group(1).strip()
        
        # Final fallback to filename
        if not name or name == 'Unknown':
            name = Path(filepath).stem.replace('-', ' ').title()
        
        return {
            'name': name,
            'score': fm.get('score', 0),
            'opportunity': fm.get('opportunity', 0),
            'pain': fm.get('pain', 0),
            'reach': fm.get('reach', 0),
            'fit': fm.get('fit', 0),
            'pain_points': self._extract_pain_points(body),
            'demand_score': fm.get('demand_score', 0),
            'conversion_ease': fm.get('conversion_ease', 0),
        }
    
    def _extract_pain_points(self, body: str) -> List[str]:
        """Extract pain points."""
        pattern = r'## Pain Points Found\s*\n(.*?)(?=\n## |\Z)'
        match = re.search(pattern, body, re.DOTALL)
        if not match:
            return []
        
        points = []
        for line in match.group(1).split('\n'):
            m = re.match(r'^\d+\.\s+(.+)', line.strip())
            if m:
                points.append(m.group(1))
        return points
    
    def _optimist_score(self, lead: Dict) -> AgentOpinion:
        """Optimist agent — sees opportunity and growth."""
        opportunity = min(100, lead.get('opportunity', 0) + 15)
        pain = min(100, lead.get('pain', 0) + 10)  # More pain = more opportunity
        fit = min(100, lead.get('fit', 0) + 5)
        reach = min(100, lead.get('reach', 0) + 10)
        
        total = int((opportunity + pain + fit + reach) / 4)
        
        reasoning = (
            f"High growth potential. {lead.get('name', 'This lead')} shows strong "
            f"demand signals. {len(lead.get('pain_points', []))} pain points mean "
            f"clear opportunity for improvement. Move-out season timing is ideal."
        )
        
        return AgentOpinion('optimist', opportunity, pain, fit, reach, total, reasoning)
    
    def _pessimist_score(self, lead: Dict) -> AgentOpinion:
        """Pessimist agent — sees risks and competition."""
        opportunity = max(0, lead.get('opportunity', 0) - 15)
        pain = max(0, lead.get('pain', 0) - 5)
        fit = max(0, lead.get('fit', 0) - 10)
        reach = max(0, lead.get('reach', 0) - 10)
        
        total = int((opportunity + pain + fit + reach) / 4)
        
        pain_count = len(lead.get('pain_points', []))
        reasoning = (
            f"Competitive market. {pain_count} pain points suggest entrenched "
            f"issues. Outreach may be difficult if they don't see the problem. "
            f"Consider timing and resistance to change."
        )
        
        return AgentOpinion('pessimist', opportunity, pain, fit, reach, total, reasoning)
    
    def _realist_score(self, lead: Dict) -> AgentOpinion:
        """Realist agent — sees practical feasibility."""
        opportunity = lead.get('opportunity', 0)
        pain = lead.get('pain', 0)
        fit = lead.get('fit', 0)
        reach = lead.get('reach', 0)
        
        # Adjust based on practical factors
        if 'phone' in str(lead).lower():
            reach = min(100, reach + 5)  # Phone listed = easier to reach
        
        if len(lead.get('pain_points', [])) >= 3:
            pain = min(100, pain + 5)  # Multiple pains = stronger case
        
        total = int((opportunity + pain + fit + reach) / 4)
        
        reasoning = (
            f"Practical assessment. Current score is reasonable. "
            f"{len(lead.get('pain_points', []))} pain points validate need. "
            f"Timing and reachability are key factors."
        )
        
        return AgentOpinion('realist', opportunity, pain, fit, reach, total, reasoning)
    
    def debate(self, lead_file: str) -> Dict:
        """Run multi-agent debate on a lead."""
        lead = self.parse_lead(lead_file)
        
        self._log(f"\n{'='*60}")
        self._log(f"DEBATE: {lead['name']}")
        self._log(f"{'='*60}")
        self._log(f"Original Score: {lead.get('score', 0)}/100")
        self._log(f"Pain Points: {len(lead.get('pain_points', []))}")
        
        # Get all opinions
        opinions = []
        for agent_name, agent_fn in self.agents.items():
            opinion = agent_fn(lead)
            opinions.append(opinion)
            
            self._log(f"\n🎭 {agent_name.upper()}")
            self._log(f"   Opportunity: {opinion.opportunity_score}/100")
            self._log(f"   Pain:        {opinion.pain_score}/100")
            self._log(f"   Fit:         {opinion.fit_score}/100")
            self._log(f"   Reach:       {opinion.reach_score}/100")
            self._log(f"   TOTAL:       {opinion.total}/100")
            self._log(f"   Reasoning:   {opinion.reasoning}")
        
        # Calculate consensus
        # Weighted: optimist 25%, pessimist 25%, realist 50%
        weights = {'optimist': 0.25, 'pessimist': 0.25, 'realist': 0.50}
        
        consensus = {
            'opportunity': 0,
            'pain': 0,
            'fit': 0,
            'reach': 0,
            'total': 0,
        }
        
        for opinion in opinions:
            w = weights[opinion.agent]
            consensus['opportunity'] += opinion.opportunity_score * w
            consensus['pain'] += opinion.pain_score * w
            consensus['fit'] += opinion.fit_score * w
            consensus['reach'] += opinion.reach_score * w
            consensus['total'] += opinion.total * w
        
        # Round
        consensus = {k: round(v) for k, v in consensus.items()}
        
        # Calculate spread (how much agents disagree)
        totals = [o.total for o in opinions]
        spread = max(totals) - min(totals)
        
        self._log(f"\n{'='*60}")
        self._log(f"🤝 CONSENSUS")
        self._log(f"{'='*60}")
        self._log(f"Opportunity: {consensus['opportunity']}/100")
        self._log(f"Pain:        {consensus['pain']}/100")
        self._log(f"Fit:         {consensus['fit']}/100")
        self._log(f"Reach:       {consensus['reach']}/100")
        self._log(f"TOTAL:       {consensus['total']}/100")
        self._log(f"Spread:      {spread} points (max disagreement)")
        
        if spread > 30:
            self._log(f"⚠️  HIGH DISAGREEMENT — Review manually!")
        elif spread > 15:
            self._log(f"⚡ Moderate disagreement — Worth a second look")
        else:
            self._log(f"✅ Strong consensus — Scores are aligned")
        
        return {
            'lead': lead['name'],
            'original_score': lead.get('score', 0),
            'consensus': consensus,
            'spread': spread,
            'opinions': [
                {
                    'agent': o.agent,
                    'scores': {
                        'opportunity': o.opportunity_score,
                        'pain': o.pain_score,
                        'fit': o.fit_score,
                        'reach': o.reach_score,
                        'total': o.total,
                    },
                    'reasoning': o.reasoning,
                }
                for o in opinions
            ]
        }
    
    def save_debate(self, result: Dict, output_dir: str):
        """Save debate results to vault."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        safe_name = re.sub(r'[^\w\-]', '-', result['lead'].lower())
        filename = f"{safe_name}-debate.md"
        
        content = f"""---
date: 2026-05-11
lead: {result['lead']}
original_score: {result['original_score']}
consensus_score: {result['consensus']['total']}
spread: {result['spread']}
type: multi-agent-debate
---

# Debate Results: {result['lead']}

## Original Score
**{result['original_score']}/100**

## Consensus Score
**{result['consensus']['total']}/100**

| Dimension | Score |
|---|---|
| Opportunity | {result['consensus']['opportunity']}/100 |
| Pain | {result['consensus']['pain']}/100 |
| Fit | {result['consensus']['fit']}/100 |
| Reach | {result['consensus']['reach']}/100 |

## Agent Opinions

"""
        
        for opinion in result['opinions']:
            content += f"""### {opinion['agent'].title()}
**Total: {opinion['scores']['total']}/100**

| Dimension | Score |
|---|---|
| Opportunity | {opinion['scores']['opportunity']}/100 |
| Pain | {opinion['scores']['pain']}/100 |
| Fit | {opinion['scores']['fit']}/100 |
| Reach | {opinion['scores']['reach']}/100 |

{opinion['reasoning']}

---

"""
        
        content += f"""## Spread Analysis
**Disagreement: {result['spread']} points**

"""
        
        if result['spread'] > 30:
            content += "⚠️ **HIGH DISAGREEMENT** — Agents strongly disagree. Review manually!\n"
        elif result['spread'] > 15:
            content += "⚡ **Moderate disagreement** — Worth a second look.\n"
        else:
            content += "✅ **Strong consensus** — All agents aligned on this lead.\n"
        
        filepath = output_path / filename
        filepath.write_text(content)
        
        self._log(f"\n💾 Saved to: {filepath}")
        return str(filepath)


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python debate-engine.py <lead-file.md> [output-dir]")
        print("Example: python debate-engine.py leads/lisa-cleaning-il.md debates/")
        sys.exit(1)
    
    lead_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else '/root/.openclaw/workspace/vault/wings/StandoutLocal/debates'
    
    engine = DebateEngine(verbose=True)
    result = engine.debate(lead_file)
    engine.save_debate(result, output_dir)
    
    print(f"\n{'='*60}")
    print(f"DONE — Consensus: {result['consensus']['total']}/100 (spread: {result['spread']})")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
