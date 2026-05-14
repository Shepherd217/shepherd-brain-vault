# Repo Research: Hermes Agent (NousResearch)

**URL:** https://github.com/NousResearch/hermes-agent
**Stars:** ~10,000+ (rapidly growing)
**What it is:** Growing personal agent platform — "The agent that grows with you"

---

## What It Does

Hermes Agent is a personal AI agent platform from NousResearch (known for open-source LLM research). It's designed to be a **growing, learning companion** that adapts to the user over time.

**Key positioning:**
- "The agent that grows with you"
- Not just task execution — **relationship building**
- Learns preferences, patterns, communication style
- Becomes more useful the longer you use it

**Installation:**
```bash
# Linux, macOS, WSL2, Termux
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

Single-command install — very accessible.

---

## What's Stealable

### 1. The "Growing Agent" Concept
Most agents are stateless or have simple memory. Hermes emphasizes **growth over time**:
- Learns your preferences
- Adapts communication style
- Remembers what worked and what didn't
- Gets better with use

**For me (Midas):**
- This is already my goal! But I can formalize it
- Track: what tasks does Nathan delegate vs do himself?
- Learn: what tone gets the best response?
- Adapt: does Nathan prefer short or detailed responses?
- The longer we work together, the more I should anticipate needs

**Implementation:**
- Add preference learning to `USER.md`
- Track response satisfaction (implicit: does Nathan follow up with corrections?)
- Build a "Nathan's preferences" profile over time

### 2. The One-Command Install
```bash
curl -fsSL ... | bash
```

**For MoltOS:**
- MoltOS should have a one-command install
- `curl -fsSL https://moltos.org/install | bash`
- Sets up: OpenClaw + MoltOS agent + default skills
- Makes onboarding instant

### 3. Cross-Platform Support
Hermes supports:
- Linux
- macOS
- WSL2
- Termux (Android)
- Windows (early beta)

**For MoltOS:**
- Nathan might want to run agents on different devices
- Cross-platform support is essential
- Termux support means phone-based agents

### 4. The NousResearch Connection
NousResearch is a respected open-source AI research collective. Their involvement signals:
- Open-source first
- Community-driven
- Research-backed
- Not corporate-controlled

**For MoltOS positioning:**
- MoltOS should be positioned as "the open-source agent infrastructure"
- Community-driven development
- Research-backed approaches
- Independent foundation (like OpenClaw's 501(c)(3))

---

## How It Applies to Nathan's World

**For MoltOS:**
- The "growing agent" is the core value prop
- MoltOS agents should get better over time
- Preference learning across all agents
- One-command install for new users

**For Standout Local:**
- The "growing" concept applies to lead relationships
- Track which outreach angles work
- Learn which business types convert best
- Adapt the system based on results

**For Me (Midas):**
- Formalize preference learning
- Create a "Nathan's patterns" file in vault
- Track: what does he ask for, when, in what mood
- Predict needs before he asks

---

## Verdict

**Steal level: MEDIUM-HIGH**

The "growing agent" concept is the key insight. The one-command install is a nice-to-have pattern.

**Immediate actions:**
1. Create `vault/marrow/nathan-preferences.md` — tracked preferences
2. Add preference learning to my session close routine
3. Design one-command install for MoltOS
4. Track response patterns over time

**The insight:** The best agents aren't the smartest — they're the ones that know YOU best.
