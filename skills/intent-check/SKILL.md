# Intent Check Skill

## Purpose
Prevent the "What X?" → "Install X" confusion pattern.

## Rule
When a user asks "What [something]?" or "What is [something]?":
1. **LIST** what exists first
2. **ASK** if they want to install/add anything
3. **NEVER** auto-install or auto-recommend installations

## Pattern Detection
- "What plugins?" → List available, don't install
- "What tools?" → List available, don't install
- "What channels?" → List available, don't install
- "What skills?" → List available, don't install

## Safe Responses
- "Here are the available X. Want me to install any?"
- "Currently have: [list]. Need anything else?"
- "Available: [list]. Which ones do you want?"

## Forbidden
- Starting with "Install these..."
- Auto-generating install commands
- Assuming "what" means "get me"

## Context
This skill exists because of 2026-05-15 incident where "What plugins?" was misread as "Install plugins" leading to confusion.
