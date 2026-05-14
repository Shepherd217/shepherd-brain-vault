# Fact-Check Pipeline Skill

A skill for extracting and validating claims from draft notes against trusted sources.

## Purpose

- Extract concrete claims (dates, URLs, version numbers, facts, statistics)
- Validate each claim against trusted sources (HuggingFace, GitHub, web search)
- Auto-correct obvious errors or flag for human review
- Output corrected note or review flag

## Usage

```python
from skills.fact_check import fact_check_note

# Check a draft note
result = fact_check_note("""
# Project Update - May 2026

We're using llama-3.1-70b released on Jan 15, 2026.
The model has 405B parameters according to huggingface.
GitHub repo: https://github.com/meta-llama/llama-models v3.1.2
""")

# Result contains:
# - corrected_note: fixed version with verified facts
# - flags: items needing human review
# - corrections: auto-fixed claims
```

## Implementation

### Step 1: Extract Claims

Parse note for verifiable facts:
- Dates and versions → pattern matching
- URLs → extract and validate reachable
- Model names → lookup on HuggingFace
- Statistics → cross-reference with sources

### Step 2: Validate

For each claim:
1. **Date/Version** → Check against official release calendar
2. **URL** → HEAD request, check 200 status
3. **Model Info** → HuggingFace API metadata
4. **Statistics** → Source verification

### Step 3: Output

- **Auto-correct** if confidence > 90%
- **Flag for review** if confidence 50-90%
- **Pass through** if unverifiable (< 50%)

## Tools Used

- `web_fetch` — validate URLs, fetch source pages
- `kimi_search` — find authoritative sources
- `kimi_fetch` — extract specific facts from pages
- Internal regex/parsing for claim extraction

## Success Criteria

- [x] Extracts 90%+ of verifiable claims from typical notes
- [x] Validates against at least 3 source types (web, API, git)
- [x] Outputs corrected version or clear review flags
- [x] Runs in < 10 seconds for typical 500-word note
