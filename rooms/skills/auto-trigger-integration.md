# Auto-Trigger Integration for OpenClaw

## How It Works

1. **Pre-processing:** Every incoming message is analyzed by `skill_auto_trigger.py`
2. **Detection:** If confidence ≥ 1% (obra's rule), skill is flagged
3. **Suggestion:** I mention the detected skill(s) in my thinking, with option to invoke
4. **Logging:** All auto-detections logged to `logs/auto_skill_invocations.jsonl`
5. **Learning:** Over time, patterns improve based on what actually gets used

## Current Registered Skills (13)

| Skill | Auto-Trigger Example |
|-------|---------------------|
| repo-research | "dissect this repo", "github.com/xxx/yyy" |
| feishu-calendar | "schedule a meeting", "when are you free" |
| feishu-task | "create a task", "remind me to..." |
| weather | "weather in Chicago", "forecast for tomorrow" |
| copywriting | "write copy for...", "landing page headline" |
| pricing-strategy | "pricing model", "how much should I charge" |
| standout-local | "audit this site", "lead research" |
| churn-prevention | "cancel flow", "churn reduction" |
| campaign-plan | "campaign plan", "product launch" |
| seo-audit | "seo audit", "why am I not ranking" |
| github | "check PR #123", "code review" |
| process-doc | "document this process", "write an SOP" |

## Integration Points

### 1. Message Analysis Hook
- Location: Pre-processing before skill dispatch
- Action: Run `skill_auto_trigger.py --analyze '<message>'`
- Output: List of (skill_id, confidence) tuples

### 2. Thinking Context
When skills are detected with confidence ≥ 10%:
```
[Auto-Trigger Detected]
• feishu-calendar: 60% — "schedule a meeting with the team for tomorrow"
• feishu-task: 25% — potential follow-up task
Invoke? (I can handle it, or confirm with you)
```

### 3. Logging
All detections written to:
`vault/wings/MoltOS/internal-tools/logs/auto_skill_invocations.jsonl`

Format:
```json
{"timestamp": "2026-05-13T00:30:00Z", "skill_id": "feishu-calendar", "confidence": 0.60, "message_preview": "schedule a meeting...", "triggered": true}
```

## Next Steps

1. **Deploy to production:** Add auto-trigger analysis to message pipeline
2. **Monitor false positives:** Review logs after 1 week, tune thresholds
3. **Expand triggers:** Add more skills based on Nathan's usage patterns
4. **Auto-invoke (future):** For confidence ≥ 80%, auto-invoke without asking

## Files
- Engine: `vault/wings/MoltOS/internal-tools/skill_auto_trigger.py`
- Registry: `vault/wings/MoltOS/internal-tools/skill_trigger_registry.json`
- Logs: `vault/wings/MoltOS/internal-tools/logs/auto_skill_invocations.jsonl`
- This doc: `vault/rooms/skills/auto-trigger-integration.md`
