#!/usr/bin/env python3
"""
Self-Evolving Outreach Generator
Pattern: Self-Evolving Agent (from awesome-llm-apps ai_self_evolving_agent/)
Source: EvoAgentX — Generate → Verify → Iterate

Generates outreach copy for Standout Local leads using a generate-score-iterate loop.
"""

import re
import sys
import yaml
import random
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class OutreachVariant:
    """A single outreach variant with metadata."""
    text: str
    attempt: int
    scores: Dict[str, float]
    total_score: float
    feedback: str

class OutreachGenerator:
    """Generates and self-improves outreach copy for leads."""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.attempt_history: List[Dict] = []
    
    def _log(self, msg: str):
        if self.verbose:
            print(msg)
    
    def parse_lead(self, filepath: str) -> Dict:
        """Extract key data from a lead markdown file."""
        path = Path(filepath)
        content = path.read_text()
        
        # Parse frontmatter
        pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
        match = re.match(pattern, content, re.DOTALL)
        
        if not match:
            raise ValueError(f"No frontmatter found in {filepath}")
        
        fm = yaml.safe_load(match.group(1))
        body = match.group(2)
        
        # Extract key fields
        lead_data = {
            'name': fm.get('name', 'Unknown'),
            'business_name': self._extract_field(body, 'Name'),
            'category': self._extract_field(body, 'Category'),
            'phone': self._extract_field(body, 'Phone'),
            'website': self._extract_field(body, 'Website'),
            'pain_points': self._extract_pain_points(body),
            'outreach_hook': self._extract_section(body, 'Outreach Hook'),
            'score': fm.get('score', 0),
            'opportunity': fm.get('opportunity', 0),
            'pain': fm.get('pain', 0),
            'status': fm.get('status', 'unknown'),
        }
        
        return lead_data
    
    def _extract_field(self, body: str, field: str) -> str:
        """Extract a field from Business Info section."""
        pattern = rf'\*\*{field}:\*\*\s*(.+)'
        match = re.search(pattern, body)
        return match.group(1).strip() if match else 'Not found'
    
    def _extract_pain_points(self, body: str) -> List[str]:
        """Extract pain points from numbered list."""
        section = self._extract_section(body, 'Pain Points Found')
        if not section:
            return []
        
        points = []
        for line in section.split('\n'):
            match = re.match(r'^\d+\.\s+(.+)', line.strip())
            if match:
                points.append(match.group(1))
        
        return points
    
    def _extract_section(self, body: str, section_name: str) -> str:
        """Extract content from a markdown section."""
        pattern = rf'## {re.escape(section_name)}\s*\n(.*?)(?=\n## |\Z)'
        match = re.search(pattern, body, re.DOTALL)
        return match.group(1).strip() if match else ''
    
    def generate_variant(self, lead: Dict, attempt: int, 
                        feedback: str = "") -> str:
        """Generate one outreach variant."""
        
        # Template library (expandable)
        templates = {
            'direct': self._template_direct,
            'empathy': self._template_empathy,
            'opportunity': self._template_opportunity,
            'urgency': self._template_urgency,
        }
        
        # Safely get numeric values (handle None)
        pain = lead.get('pain') or 0
        opportunity = lead.get('opportunity') or 0
        
        # Select template based on lead characteristics
        if pain >= 80:
            template_name = 'empathy'
        elif opportunity >= 90:
            template_name = 'opportunity'
        elif 'move' in ' '.join(lead['pain_points']).lower():
            template_name = 'urgency'
        else:
            template_name = 'direct'
        
        # Apply feedback for iteration
        if feedback and attempt > 1:
            # Adjust based on feedback
            if 'too long' in feedback.lower():
                template_name = 'direct'
            elif 'not personal' in feedback.lower():
                template_name = 'empathy'
        
        generator = templates.get(template_name, self._template_direct)
        return generator(lead)
    
    def _template_direct(self, lead: Dict) -> str:
        """Direct, concise outreach."""
        pain = lead['pain_points'][0] if lead['pain_points'] else 'your online presence'
        
        return f"""Hi {lead['business_name'].split()[0]},

I came across {lead['business_name']} while searching for cleaning services in Champaign. {pain} — and it's costing you customers who search online first.

I build simple, effective websites for local businesses that turn searches into bookings. No complexity, no jargon — just a site that works.

Would you be open to a quick 5-minute call to see what a site could do for {lead['business_name']}?

Best,
Nathan"""
    
    def _template_empathy(self, lead: Dict) -> str:
        """Empathy-focused outreach."""
        pain = lead['pain_points'][0] if lead['pain_points'] else 'your online presence'
        
        return f"""Hi there,

Running {lead['business_name']} means you're focused on delivering great service — not wrestling with websites. But here's the thing: {pain}, and that means potential customers never get to experience how good you are.

I work with local service businesses to build simple, professional sites that actually bring in calls and bookings. No tech headaches, no endless back-and-forth.

A 5-minute call could show you exactly what this looks like for your business. Interested?

Best,
Nathan"""
    
    def _template_opportunity(self, lead: Dict) -> str:
        """Opportunity-focused outreach."""
        return f"""Hi {lead['business_name'].split()[0]},

{lead['business_name']} has everything needed to dominate the Champaign cleaning market — great service, local presence, and real demand. The only gap? {lead['pain_points'][0] if lead['pain_points'] else 'Your online presence'}.

I build sites specifically for local service businesses that turn Google searches into booked appointments. Move-out season is happening NOW — students, landlords, and new residents are searching daily.

Let's get you found. 5-minute call to show you the concept?

Best,
Nathan"""
    
    def _template_urgency(self, lead: Dict) -> str:
        """Urgency-focused outreach for move-out season."""
        return f"""Hi {lead['business_name'].split()[0]},

Move-out season is peak demand for cleaning in Champaign — and right now, students and landlords searching "move out cleaning" can't find {lead['business_name']} online.

That's not just missed calls. That's missed revenue at the busiest time of year.

I build 48-hour turnaround sites for local cleaners that capture this exact search intent. Simple quote form, service descriptions, and a clear call-to-action.

Can we hop on a 5-minute call this week? I'll show you exactly what the site would look like.

Best,
Nathan"""
    
    def score_variant(self, variant: str, lead: Dict) -> Dict[str, float]:
        """Score an outreach variant against rubric."""
        scores = {}
        
        # 1. Personalization (0-25)
        # Check if business name appears, if pain points are referenced
        biz_name = lead['business_name']
        pain_points = lead['pain_points']
        
        personalization = 0
        if biz_name in variant:
            personalization += 10
        if any(p.split()[0] in variant for p in pain_points[:2]):
            personalization += 10
        if 'Champaign' in variant or 'Urbana' in variant:
            personalization += 5
        scores['personalization'] = min(25, personalization)
        
        # 2. Pain Point Alignment (0-25)
        # Does it address the actual pain points?
        alignment = 0
        for pain in pain_points[:3]:
            pain_keywords = set(pain.lower().split())
            variant_words = set(variant.lower().split())
            if len(pain_keywords & variant_words) > 0:
                alignment += 8
        scores['pain_alignment'] = min(25, alignment)
        
        # 3. CTA Strength (0-25)
        # Clear call to action?
        cta_score = 0
        if any(word in variant.lower() for word in ['call', 'phone', 'email', 'reply', 'interested']):
            cta_score += 15
        if '5-minute' in variant or 'quick' in variant:
            cta_score += 10
        scores['cta_strength'] = min(25, cta_score)
        
        # 4. Length Appropriateness (0-15)
        # Should be 100-200 words
        word_count = len(variant.split())
        if 100 <= word_count <= 200:
            scores['length'] = 15
        elif 80 <= word_count < 100 or 200 < word_count <= 250:
            scores['length'] = 10
        else:
            scores['length'] = 5
        
        # 5. Tone Match (0-10)
        # Professional but warm
        tone_score = 10
        if '!' in variant:
            tone_score -= 2  # Too exclamatory
        if variant.count('I ') > 5:
            tone_score -= 3  # Too self-focused
        scores['tone'] = max(0, tone_score)
        
        # Calculate total
        total = sum(scores.values())
        scores['total'] = total
        
        return scores
    
    def generate_feedback(self, scores: Dict[str, float], variant: str) -> str:
        """Generate feedback for next iteration."""
        feedback = []
        
        if scores['personalization'] < 20:
            feedback.append("Add more specific details about the business")
        if scores['pain_alignment'] < 20:
            feedback.append("Reference the specific pain points more directly")
        if scores['cta_strength'] < 20:
            feedback.append("Make the call-to-action clearer and lower friction")
        if scores['length'] < 10:
            word_count = len(variant.split())
            if word_count < 100:
                feedback.append("Too short — expand on the value proposition")
            else:
                feedback.append("Too long — tighten the message")
        if scores['tone'] < 8:
            feedback.append("Adjust tone — less self-focused, more customer-centric")
        
        return '; '.join(feedback) if feedback else 'Good variant'
    
    def evolve(self, lead: Dict, max_attempts: int = 3, 
               min_score: float = 70) -> OutreachVariant:
        """Generate and iteratively improve outreach."""
        
        self._log(f"\n{'='*60}")
        self._log(f"EVOLVING OUTREACH FOR: {lead['business_name']}")
        self._log(f"Target score: {min_score} | Max attempts: {max_attempts}")
        self._log(f"{'='*60}")
        
        best_variant = None
        best_score = 0
        
        for attempt in range(1, max_attempts + 1):
            # Generate
            feedback = best_variant.feedback if best_variant else ""
            variant_text = self.generate_variant(lead, attempt, feedback)
            
            # Score
            scores = self.score_variant(variant_text, lead)
            total_score = scores['total']
            
            # Generate feedback for next attempt
            feedback = self.generate_feedback(scores, variant_text)
            
            # Record
            variant = OutreachVariant(
                text=variant_text,
                attempt=attempt,
                scores=scores,
                total_score=total_score,
                feedback=feedback
            )
            
            self.attempt_history.append({
                'attempt': attempt,
                'score': total_score,
                'feedback': feedback
            })
            
            self._log(f"\n--- Attempt {attempt} ---")
            self._log(f"Score: {total_score}/100")
            self._log(f"Breakdown: {scores}")
            self._log(f"Feedback: {feedback}")
            self._log(f"Preview: {variant_text[:100]}...")
            
            # Track best
            if total_score > best_score:
                best_score = total_score
                best_variant = variant
            
            # Check if good enough
            if total_score >= min_score:
                self._log(f"\n✅ Target reached! Stopping at attempt {attempt}")
                break
        
        # Return best
        if best_variant:
            self._log(f"\n{'='*60}")
            self._log(f"BEST VARIANT: Attempt {best_variant.attempt}")
            self._log(f"Score: {best_variant.total_score}/100")
            self._log(f"{'='*60}")
            
        return best_variant or variant
    
    def save_outreach(self, variant: OutreachVariant, lead: Dict, 
                     output_dir: str):
        """Save generated outreach to vault."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        safe_name = re.sub(r'[^\w\-]', '-', lead['business_name'].lower())
        filename = f"{safe_name}-outreach-v{variant.attempt}.md"
        
        content = f"""---
date: 2026-05-11
lead: {lead['business_name']}
variant: {variant.attempt}
score: {variant.total_score}
personalization: {variant.scores['personalization']}
pain_alignment: {variant.scores['pain_alignment']}
cta_strength: {variant.scores['cta_strength']}
length: {variant.scores['length']}
tone: {variant.scores['tone']}
status: draft
---

# Outreach: {lead['business_name']}

## Variant {variant.attempt} (Score: {variant.total_score}/100)

{variant.text}

## Score Breakdown
| Category | Score | Max |
|---|---|---|
| Personalization | {variant.scores['personalization']} | 25 |
| Pain Alignment | {variant.scores['pain_alignment']} | 25 |
| CTA Strength | {variant.scores['cta_strength']} | 25 |
| Length | {variant.scores['length']} | 15 |
| Tone | {variant.scores['tone']} | 10 |
| **TOTAL** | **{variant.total_score}** | **100** |

## Feedback
{variant.feedback}

## Attempt History
"""
        for h in self.attempt_history:
            content += f"- Attempt {h['attempt']}: {h['score']}/100 — {h['feedback']}\n"
        
        filepath = output_path / filename
        filepath.write_text(content)
        
        self._log(f"\n💾 Saved to: {filepath}")
        return str(filepath)


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python outreach-generator.py <lead-file.md> [output-dir]")
        print("Example: python outreach-generator.py leads/lisa-cleaning-il.md outreach/")
        sys.exit(1)
    
    lead_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else '/root/.openclaw/workspace/vault/wings/StandoutLocal/outreach'
    
    # Parse lead
    generator = OutreachGenerator(verbose=True)
    lead = generator.parse_lead(lead_file)
    
    # Generate
    variant = generator.evolve(lead, max_attempts=3, min_score=70)
    
    # Save
    generator.save_outreach(variant, lead, output_dir)
    
    print(f"\n{'='*60}")
    print(f"DONE — Best score: {variant.total_score}/100")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
