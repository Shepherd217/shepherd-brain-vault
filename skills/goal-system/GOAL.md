# Goal System — Autonomous Task Completion

## How It Works

Inspired by Claude Code's `/goal` command:

1. **Set Goal**: User types `/goal <completion condition>`
2. **Work Loop**: Agent works autonomously across turns
3. **Evaluate**: After each turn, check if goal is met
4. **Continue**: If not met → keep working
5. **Complete**: If met → notify user, clear goal

## Commands

| Command | Description |
|---------|-------------|
| `/goal <condition>` | Set active goal |
| `/goal status` | Show progress (turns, time, tokens) |
| `/goal clear` | Cancel active goal |

## File Structure

```
skills/goal-system/
├── GOAL.md           # This file
├── evaluator.ts      # Checks if goal is complete
├── tracker.ts        # Tracks turns/time/tokens
└── active.md         # Current active goal (auto-generated)
```

## Evaluation Logic

The evaluator is a lightweight check that runs after each turn:

```typescript
// evaluator.ts
export function evaluateGoal(goal: string, context: TurnContext): boolean {
  // Parse goal condition
  // Check if evidence exists in conversation
  // Return true/false with reason
}
```

## Tracking

Stored in `.coordination/goals/active.md`:
```yaml
goal: "Deploy dashboard to Vercel"
startedAt: "2026-05-15T01:00:00Z"
elapsedMinutes: 45
turns: 12
tokens: 89000
status: active  # active | completed | cancelled
lastEvaluation: "Turn 12: dashboard deployed, mobile-friendly, tests passing"
```

## Usage

```
User: /goal Build a mobile-friendly dashboard and deploy to Vercel

[Agent works across multiple turns]
[After each turn, evaluator checks progress]

Turn 1: Researching mobile best practices... (3,200 tokens)
Turn 5: Building components... (8,100 tokens)  
Turn 12: Deployed! (2,100 tokens)

✅ Goal met! Elapsed: 45min | Turns: 12 | Tokens: 89,000
```
