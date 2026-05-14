#!/usr/bin/env python3
"""
Website Audit Scraper
Pattern: Automated Audit Pipeline (from Standout Local workflow)
Source: URL → Scrape → Analyze → Score → Report

Uses Firecrawl API to scrape websites and generate structured audit reports.
Falls back to basic HTTP fetch if Firecrawl unavailable.
"""

import os
import sys
import re
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

class WebsiteAuditor:
    """Scrapes and audits websites for Standout Local."""
    
    def __init__(self, api_key: str = None, verbose: bool = True):
        self.verbose = verbose
        self.api_key = api_key or os.environ.get('FIRECRAWL_API_KEY', '')
        if not self.api_key:
            # Try to load from TOOLS.md or env
            self.api_key = self._find_api_key()
    
    def _log(self, msg: str):
        if self.verbose:
            print(msg)
    
    def _find_api_key(self) -> str:
        """Try to find Firecrawl API key in vault."""
        tools_md = Path('/root/.openclaw/workspace/TOOLS.md')
        if tools_md.exists():
            content = tools_md.read_text()
            match = re.search(r'API Key:\s*`?([a-f0-9-]+)`?', content)
            if match:
                return match.group(1)
        return ''
    
    def scrape_with_firecrawl(self, url: str) -> Optional[Dict]:
        """Scrape website using Firecrawl API."""
        if not self.api_key:
            self._log("⚠️  No Firecrawl API key found")
            return None
        
        self._log(f"🔥 Scraping with Firecrawl: {url}")
        
        try:
            import requests
            
            response = requests.post(
                'https://api.firecrawl.dev/v0/scrape',
                headers={'Authorization': f'Bearer {self.api_key}'},
                json={'url': url, 'pageOptions': {'onlyMainContent': True}},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'title': data.get('data', {}).get('metadata', {}).get('title', 'No title'),
                    'description': data.get('data', {}).get('metadata', {}).get('description', ''),
                    'content': data.get('data', {}).get('markdown', ''),
                    'url': url,
                    'source': 'firecrawl',
                }
            else:
                self._log(f"⚠️  Firecrawl error: HTTP {response.status_code}")
                return None
                
        except ImportError:
            self._log("⚠️  requests not installed, trying curl...")
            return self._scrape_with_curl(url)
        except Exception as e:
            self._log(f"⚠️  Firecrawl failed: {e}")
            return None
    
    def _scrape_with_curl(self, url: str) -> Optional[Dict]:
        """Fallback scrape using curl."""
        try:
            result = subprocess.run(
                ['curl', '-s', '-L', '--max-time', '15', url],
                capture_output=True,
                text=True,
                timeout=20
            )
            
            if result.returncode == 0:
                html = result.stdout
                
                # Extract title
                title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
                title = title_match.group(1).strip() if title_match else 'No title'
                
                # Extract description
                desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)', html, re.IGNORECASE)
                if not desc_match:
                    desc_match = re.search(r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*name=["\']description["\']', html, re.IGNORECASE)
                description = desc_match.group(1) if desc_match else ''
                
                # Strip HTML for basic content
                text = re.sub(r'<[^>]+>', ' ', html)
                text = re.sub(r'\s+', ' ', text).strip()
                
                return {
                    'title': title,
                    'description': description,
                    'content': text[:5000],
                    'url': url,
                    'source': 'curl',
                }
            
        except Exception as e:
            self._log(f"⚠️  Curl fallback failed: {e}")
        
        return None
    
    def analyze_website(self, data: Dict) -> Dict:
        """Analyze scraped website data."""
        content = data.get('content', '')
        title = data.get('title', '')
        description = data.get('description', '')
        
        analysis = {
            'url': data['url'],
            'title': title,
            'has_title': bool(title and title != 'No title'),
            'has_description': bool(description),
            'description_length': len(description),
            
            # Mobile check
            'has_viewport': 'viewport' in content.lower(),
            
            # Contact info
            'has_phone': bool(re.search(r'\b\d{3}[.-]?\d{3}[.-]?\d{4}\b', content)),
            'has_email': bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)),
            
            # Social proof
            'has_reviews': any(word in content.lower() for word in ['review', 'testimonial', 'rating', 'stars']),
            'has_photos': any(word in content.lower() for word in ['gallery', 'photo', 'image', 'before', 'after']),
            
            # Service info
            'has_services': any(word in content.lower() for word in ['service', 'offering', 'pricing', 'package']),
            'has_pricing': 'price' in content.lower() or 'cost' in content.lower(),
            
            # CTA
            'has_cta': any(word in content.lower() for word in ['call now', 'book', 'schedule', 'quote', 'contact', 'get started']),
            'has_quote_form': any(word in content.lower() for word in ['form', 'submit', 'request quote']),
            
            # Tech
            'has_ssl': data['url'].startswith('https://'),
            'word_count': len(content.split()),
        }
        
        # Calculate scores
        analysis['mobile_score'] = 100 if analysis['has_viewport'] else 20
        analysis['trust_score'] = (
            (20 if analysis['has_phone'] else 0) +
            (20 if analysis['has_email'] else 0) +
            (20 if analysis['has_reviews'] else 0) +
            (20 if analysis['has_photos'] else 0) +
            (20 if analysis['has_ssl'] else 0)
        )
        analysis['conversion_score'] = (
            (25 if analysis['has_cta'] else 0) +
            (25 if analysis['has_quote_form'] else 0) +
            (25 if analysis['has_services'] else 0) +
            (25 if analysis['has_pricing'] else 0)
        )
        analysis['seo_score'] = (
            (30 if analysis['has_title'] else 0) +
            (30 if analysis['has_description'] and analysis['description_length'] > 50 else 0) +
            (20 if analysis['word_count'] > 300 else 0) +
            (20 if analysis['has_ssl'] else 0)
        )
        
        analysis['total_score'] = int(
            (analysis['mobile_score'] + analysis['trust_score'] + 
             analysis['conversion_score'] + analysis['seo_score']) / 4
        )
        
        return analysis
    
    def audit(self, url: str) -> Dict:
        """Full audit: scrape + analyze."""
        self._log(f"\n{'='*60}")
        self._log(f"AUDITING: {url}")
        self._log(f"{'='*60}")
        
        # Scrape
        data = self.scrape_with_firecrawl(url)
        if not data:
            data = self._scrape_with_curl(url)
        
        if not data:
            return {'error': 'Failed to scrape website', 'url': url}
        
        # Analyze
        analysis = self.analyze_website(data)
        
        self._log(f"\n📊 Audit Results")
        self._log(f"   Title: {analysis['title']}")
        self._log(f"   Word count: {analysis['word_count']}")
        self._log(f"   Mobile: {analysis['mobile_score']}/100")
        self._log(f"   Trust: {analysis['trust_score']}/100")
        self._log(f"   Conversion: {analysis['conversion_score']}/100")
        self._log(f"   SEO: {analysis['seo_score']}/100")
        self._log(f"   TOTAL: {analysis['total_score']}/100")
        
        # Pain points
        pains = []
        if not analysis['has_phone']:
            pains.append("No phone number visible")
        if not analysis['has_cta']:
            pains.append("No clear call-to-action")
        if not analysis['has_quote_form']:
            pains.append("No quote request form")
        if not analysis['has_viewport']:
            pains.append("Not mobile-optimized")
        if not analysis['has_reviews']:
            pains.append("No reviews or testimonials")
        if analysis['word_count'] < 200:
            pains.append("Very thin content")
        
        analysis['pain_points'] = pains
        
        self._log(f"\n🎯 Pain Points Found ({len(pains)}):")
        for pain in pains:
            self._log(f"   • {pain}")
        
        return analysis
    
    def save_audit(self, analysis: Dict, output_dir: str = None):
        """Save audit report to vault."""
        output = Path(output_dir or '/root/.openclaw/workspace/vault/wings/StandoutLocal/audits')
        output.mkdir(parents=True, exist_ok=True)
        
        domain = urlparse(analysis['url']).netloc.replace('.', '-')
        filename = f"{domain}-audit.md"
        
        content = f"""---
date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}
url: {analysis['url']}
score: {analysis['total_score']}
type: website-audit
---

# Website Audit: {analysis['url']}

## Score: {analysis['total_score']}/100

| Category | Score | Max |
|---|---|---|
| Mobile | {analysis['mobile_score']} | 100 |
| Trust | {analysis['trust_score']} | 100 |
| Conversion | {analysis['conversion_score']} | 100 |
| SEO | {analysis['seo_score']} | 100 |

## Details

- **Title**: {analysis['title']}
- **Has Description**: {'Yes' if analysis['has_description'] else 'No'}
- **Word Count**: {analysis['word_count']}
- **SSL**: {'Yes' if analysis['has_ssl'] else 'No'}
- **Phone**: {'Yes' if analysis['has_phone'] else 'No'}
- **Email**: {'Yes' if analysis['has_email'] else 'No'}
- **Reviews**: {'Yes' if analysis['has_reviews'] else 'No'}
- **CTA**: {'Yes' if analysis['has_cta'] else 'No'}
- **Quote Form**: {'Yes' if analysis['has_quote_form'] else 'No'}

## Pain Points ({len(analysis.get('pain_points', []))})

"""
        
        for pain in analysis.get('pain_points', []):
            content += f"- {pain}\n"
        
        filepath = output / filename
        filepath.write_text(content)
        
        self._log(f"\n💾 Saved to: {filepath}")
        return str(filepath)


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python website-auditor.py <url>")
        print("Example: python website-auditor.py https://example.com")
        sys.exit(1)
    
    url = sys.argv[1]
    
    auditor = WebsiteAuditor(verbose=True)
    analysis = auditor.audit(url)
    
    if 'error' not in analysis:
        auditor.save_audit(analysis)
    else:
        print(f"Error: {analysis['error']}")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"DONE — Score: {analysis['total_score']}/100")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
