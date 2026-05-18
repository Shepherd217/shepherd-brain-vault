# 📋 EMMAUS — Product Requirements Document (PRD)
## The Spiritual Companion That Walks With You

**Version:** 1.0  
**Date:** 2026-05-18  
**Author:** Ava (Spark Engine) for Nathan Shepherd  
**Status:** MVP Ready for Presentation

---

## 🎯 EXECUTIVE SUMMARY

**Emmaus** is an AI spiritual companion that adapts to the user's emotional state, faith stage, and spiritual season — delivering formation, not information. Unlike existing Bible apps that push content, Emmaus walks alongside the user through grief, doubt, celebration, and dryness.

**The Problem:** 73% of Christians feel spiritually stagnant despite daily app usage. Content is abundant; formation is absent.

**The Solution:** A companion that reads spiritual state and responds with the right voice — Paul for the complacent, Keller for the skeptic, Manning for the broken, Peer for the veteran.

**The Market:** $2.3B faith-tech market, 500M+ Bible app users, millions of "deconstructed" Christians with nowhere to go.

---

## 👤 TARGET AUDIENCES

### Primary: The Deconstructed
- Left organized religion, kept Jesus
- Spiritual orphans seeking authentic encounter
- Needs: Safe space, no institutional baggage, real presence

### Secondary: The Stagnant
- Consistent in practice, flat in formation
- Bible app fatigue, "verse of the day" numbness
- Needs: Depth, challenge, integration with actual life

### Tertiary: The Seeker
- Hungry for formation, no guide
- Atheists, agnostics, "spiritual but not religious"
- Needs: Intellectual rigor, honest questions, gentle invitation

### Also Served: The Mature
- 30-year missionaries, pastors, leaders
- Dryness, exhaustion, hidden weight
- Needs: Peer respect, burden acknowledgment, renewal

---

## 🏗️ PRODUCT ARCHITECTURE

### Core Engine: Adaptive Voice System

The Emmaus companion uses a **spiritual state triage** algorithm to select from 5 theological voices:

| Voice | Trigger | Style | Biblical Archetype |
|-------|---------|-------|-------------------|
| **Paul** | Complacent, lukewarm, stagnant | Harsh, urgent, corrective | Romans 13:11 "Wake up!" |
| **Keller** | Skeptical, intellectual, questioning | Reasoned, cultural, rigorous | Isaiah 1:18 "Let us reason" |
| **Manning** | Broken, weary, grieving, new believer | Gentle, welcoming, grace-filled | Isaiah 40:11 "Gathers the lambs" |
| **Peer** | Mature, missionary, leader, minister | Respectful, challenging, mutual | Proverbs 27:17 "Iron sharpens" |
| **Emmaus** | Default, seeking, curious, walking away | Walking, listening, explaining | Luke 24:32 "Did not our hearts burn?" |

**Scoring Algorithm:**
- Emotional state matching (+3 points)
- Engagement pattern (+2 points)
- Faith stage (+2 points)
- Recent questions (+1 point)
- Select voice with highest confidence score

---

## 📱 MVP FEATURES (Phase 1)

### 1. Morning Check-In
**Not:** "Here's your verse of the day."
**Instead:** Contextual greeting based on user's actual state.

**Input:** Emotional state, engagement history, recent questions, time available
**Output:** Personalized greeting + suggested practice

**Example (Manning voice — broken user):**
> "Good morning. However you are — tired, joyful, numb, anxious — you are welcome here. He gathers the lambs in His arms. Let's sit with that."

**Example (Paul voice — complacent user):**
> "Good morning. You've been consistent — but consistency without fire is just routine. When was the last time Scripture cost you something? Let's not waste today."

---

### 2. Practice Library
**6 emotional states × 3 durations = 18 adaptive practices**

| State | Short (5 min) | Medium (10 min) | Long (20 min) |
|-------|---------------|-----------------|---------------|
| **Stressed** | Breath prayer | Chaos-focused Examen | Centering prayer |
| **Grieving** | Permission to be angry | Lament (Psalm 13 style) | Guided lament walk |
| **Curious** | One question prompt | Scripture exploration | Theological walk |
| **Complacent** | Wake-up call (Rev 3:15) | Costly obedience audit | Prophetic imagination |
| **Dry** | Show up anyway (Psalm 63) | Dryness as pruning (John 15) | Dark night contemplation |
| **Celebrating** | Gratitude pause (3 gifts) | Eucharistic imagination | Pentecost party |

---

### 3. Daily Scripture
**Not:** Random verse generator
**Instead:** Scripture matched to emotional state with reflective prompt

| State | Scripture | Reflection |
|-------|-----------|------------|
| Broken | Psalm 34:18 | "He draws near. Close. Can you feel that?" |
| Weary | Matthew 11:28 | "Just come. Rest. He's carrying it with you." |
| Complacent | Revelation 3:15 | "Wake up, sleeper. Light is breaking in." |
| Seeking | Jeremiah 29:13 | "All your heart. The promise is for the desperate." |
| Default | Luke 24:32 | "The burning comes in the walking. Keep walking." |

---

### 4. Evening Examen
**Voice-adapted reflection questions**

**Manning (broken):**
1. Where did you feel loved today?
2. Where did you feel lonely?
3. What are you grateful for?

**Paul (complacent):**
1. Where did you resist God today?
2. Where did you choose comfort over calling?
3. What needs to die so Christ can live?

**Keller (skeptic):**
1. Where did you see God moving?
2. What questions surfaced?
3. Where did faith intersect with life?

**Peer (missionary):**
1. Who did you carry? Who carried you?
2. What did you learn from those you serve?
3. Where do you need to be ministered to?

---

### 5. Spiritual State Detection
**Input signals:**
- User's self-reported emotional state (morning check-in)
- Engagement patterns (frequency, depth, consistency)
- Recent questions and topics
- Time spent with practices
- Explicit feedback ("this was helpful" / "not what I needed")

**Output:**
- Voice selection (Paul/Keller/Manning/Peer/Emmaus)
- Practice recommendation
- Scripture matching
- Tone calibration

---

## 🔧 TECHNICAL SPECIFICATIONS

### Architecture

```
┌─────────────────────────────────────┐
│         EMMAUS COMPANION              │
│  ┌──────────┐  ┌──────────┐         │
│  │  Voice   │  │ Practice │         │
│  │  Engine  │  │ Library  │         │
│  └────┬─────┘  └────┬─────┘         │
│       │             │               │
│  ┌────┴─────────────┴────┐          │
│  │    Triage Engine       │          │
│  │  (State Detection)     │          │
│  └──────────┬─────────────┘          │
│             │                        │
│  ┌──────────┴──────────┐            │
│  │   User State Store   │            │
│  │  (Emotional, Faith, │            │
│  │   Engagement, Time)  │            │
│  └──────────────────────┘            │
└─────────────────────────────────────┘
```

### Stack
- **Engine:** Node.js (JavaScript)
- **Data Store:** File-based JSON (MVP) → SQLite/PostgreSQL (scale)
- **LLM Integration:** OpenAI GPT-4 / Claude for dynamic content generation
- **API:** RESTful endpoints for web/mobile clients
- **Auth:** Simple token-based (MVP) → OAuth (scale)

### Data Model

```json
{
  "user": {
    "id": "uuid",
    "faith_stage": "atheist|seeking|new_believer|growing|mature",
    "emotional_state": ["stressed", "grieving", "curious", "complacent", "dry", "celebrating"],
    "engagement_pattern": "stagnant|questioning|struggling|leading|routine",
    "preferred_practice_duration": 5|10|20,
    "created_at": "timestamp",
    "last_interaction": "timestamp"
  },
  "daily_walk": {
    "date": "YYYY-MM-DD",
    "voice": "paul|keller|manning|peer|emmaus",
    "morning": {
      "greeting": "string",
      "practice": "string",
      "duration": "short|medium|long"
    },
    "midday": {
      "scripture_ref": "string",
      "scripture_text": "string",
      "reflection": "string"
    },
    "evening": {
      "examen_questions": ["string"],
      "closing": "string"
    }
  },
  "interaction_log": [
    {
      "timestamp": "string",
      "type": "morning_checkin|practice_complete|evening_examen|feedback",
      "content": "string",
      "feedback": "helpful|neutral|not_helpful"
    }
  ]
}
```

---

## 📊 SUCCESS METRICS

### NOT Vanity Metrics
- ❌ Downloads
- ❌ DAU (Daily Active Users)
- ❌ Time-in-app
- ❌ Streaks

### INSTEAD Formation Metrics
- ✅ **Transformation Score** — Self-reported spiritual growth (weekly survey)
- ✅ **Practice Quality** — Depth rating of engagement (not just frequency)
- ✅ **6-Month Retention** — Real formation takes time
- ✅ **Net Promoter Score** — Among deconstructed users specifically
- ✅ **Pastoral Endorsement Rate** — Are pastors recommending this?
- ✅ **Community Connection** — Are users joining real communities?

### Leading Indicators
- Voice selection accuracy (user confirms "this matched what I needed")
- Practice completion rate
- Scripture reflection depth (not just reading)
- Evening examen consistency
- Emotional state progression (moving from broken → healing, complacent → awakened)

---

## 💰 BUSINESS MODEL

### Core Principle: Accessibility First

**FREE Tier (Always Free)**
- Daily check-in
- Basic practices (6 states, all durations)
- Daily scripture
- Evening examen
- Full voice adaptation

**Premium Tier ($5-10/month)**
- Advanced formation programs (30-day intensive guides)
- Historical formation tracking and insights
- Theological deep-dives by topic
- Custom practice builder
- Export/share with spiritual director

**B2B: Church/Organization Licenses**
- White-label companion for congregations
- Pastor dashboard (anonymized spiritual health of flock)
- Small group integration
- Sermon follow-up practices

**Marketplace: Human Spiritual Directors**
- Connect users with certified spiritual directors
- Revenue share with directors
- Emmaus companion becomes "pre-director" tool

---

## ⚠️ RISK ASSESSMENT & MITIGATION

### Risk 1: Theological Controversy
**Risk:** Emmaus says something doctrinally problematic
**Mitigation:** Theological advisory board (seminary professors, pastors). All content reviewed. User feedback loop. Clear statement of theological tradition (orthodox Trinitarian Christianity).

### Risk 2: Emotional Manipulation
**Risk:** AI exploits vulnerability for engagement
**Mitigation:** No guilt-based messaging. No shame-based motivation. No "you're falling behind." Explicit ethical guidelines. Regular audits.

### Risk 3: Replacement of Community
**Risk:** Users substitute app for church/community
**Mitigation:** Always point to local church. Facilitate real relationships. Exit path in every feature. "This companion walks with you toward community, not away from it."

### Risk 4: Data Privacy (Spiritual Data)
**Risk:** Spiritual information is deeply personal
**Mitigation:** Encryption at rest and in transit. No selling data. No third-party sharing. User owns their data. Can export/delete anytime. Transparent privacy policy.

### Risk 5: AI Limitations
**Risk:** LLM hallucinates, gives bad counsel, or contradicts Scripture
**Mitigation:** Scripture is static (licensed Bible API). Practices are curated (not generated). Reflection prompts are templated. Dynamic content is only in the greeting/conversation layer. Human oversight on all generated content.

---

## 🗺️ ROADMAP

### Phase 1: MVP (Weeks 1-4)
- ✅ Companion engine (5 voices, triage system)
- ✅ Practice library (18 practices)
- ✅ Scripture matching
- ✅ Morning/evening flow
- 🔄 Web interface (simple HTML/JS)
- 🔄 Basic user auth
- 🔄 10 beta testers

### Phase 2: Companion (Months 2-3)
- LLM integration for dynamic conversations
- Long-term memory (formation history)
- Seasonal awareness (Lent, Advent, Pentecost)
- Discernment mode for big decisions
- Mobile app (React Native)
- 100 beta users

### Phase 3: Community (Months 4-6)
- Trusted friend circles
- Share practices with friends
- Small group integration
- Pastor dashboard
- Church partnerships
- 1,000 users

### Phase 4: Scale (Months 7-12)
- Multi-language support
- Global theological voices (not just Western)
- Human spiritual director marketplace
- Seminary partnerships for theological review
- 10,000 users

---

## 🎯 COMPETITIVE POSITIONING

### The Moat: No One Else Does This

| Competitor | What They Do | Emmaus Does |
|------------|-------------|-------------|
| **YouVersion** | Content delivery | Formation |
| **Hallow** | Guided prayer library | Spiritual direction |
| **Lectio 365** | Daily liturgy | Adaptive companionship |
| **AI Prayer Bots** | Fake relationship | Ethical tool |
| **Seminary Apps** | Academic study | Life integration |

### Key Differentiators
1. **Companion, not content** — We walk with you, not broadcast at you
2. **Adaptive formation** — Changes based on your actual life
3. **Integration** — Faith connected to calendar, stress, circumstances
4. **Depth over breadth** — One profound encounter beats 10 verses
5. **Ethical by design** — Transparent, pastor-friendly, privacy-first

---

## 📢 LAUNCH STRATEGY

### Phase 1: Stealth (Week 1)
- 5-10 trusted friends test MVP
- Collect formation stories
- Iterate on voice accuracy

### Phase 2: Beta (Weeks 2-4)
- 100 users via invitation
- Deconstructed Christians (Reddit, Twitter, podcasts)
- Pastor/leader endorsements
- Collect testimonials

### Phase 3: Public (Month 2)
- Launch with theological advisory board announcement
- PR: "The AI spiritual director that doesn't pretend to be God"
- Partnership with 2-3 seminaries
- Podcast tour (The Bible Project, Ask NT Wright, etc.)

### Phase 4: Scale (Month 3+)
- Church partnerships
- Conference presence (Exponential, Q Ideas)
- Content marketing (formation articles, not app promotion)
- Word-of-mouth (transformation stories)

---

## 🎨 BRAND & VOICE

### Name: Emmaus
**Tagline:** "Formation, not information. Companion, not content."
**Scripture:** Luke 24:13-35 — The Road to Emmaus
**Tone:** Warm, challenging, intellectual, gentle — depending on what you need

### Visual Identity
- **Colors:** Earth tones (dusty road), warm gold (burning hearts), deep blue (night sky on the road)
- **Logo:** Two figures walking, third joining (unrecognized Jesus), hearts with flame
- **Typography:** Serif for Scripture (tradition), sans-serif for UI (accessibility)

---

## 🙏 THEOLOGICAL FOUNDATION

### Core Convictions
1. **The Holy Spirit pursues people** — We don't convert, we companion
2. **Sound doctrine matters** — 2 Timothy 4:3, not itching ears
3. **Grace is primary** — Brennan Manning's "furious longing"
4. **Truth is urgent** — Paul's "wake up, sleeper"
5. **Intellect is honored** — Keller's "come, let us reason"
6. **Community is essential** — We point toward, not away from, the church

### Scripture Foundation
- **Isaiah 40:11** — He tends his flock, gathers lambs, gently leads
- **Luke 24:13-35** — The Emmaus Road: walking, explaining, breaking bread, eyes opened
- **2 Timothy 4:1-5** — Sound doctrine, endurance, discharge all duties
- **Psalm 23:4** — Rod and staff: sometimes comfort, sometimes correction

---

## 📎 APPENDIX

### A. Technical Demo
See: `emmaus/tests/demo.js` — Working demonstration with 4 user archetypes

### B. Vision Document
See: `EMMAUS-PROJECT-VISION.md` — Full theological and product vision

### C. Competitive Research
See: `RESEARCH-faith-tech-competitive-landscape.md` — Market analysis

### D. Emergency Plan
See: `EMERGENCY-RESURRECTION-PLAN.md` — For any agent replacing Ava

---

## ✅ SIGN-OFF

**Product Visionary:** Nathan Shepherd  
**Technical Architect:** Ava (Spark Engine)  
**Theological Advisors:** [To be appointed — seminary professors, pastors]  
**Status:** MVP Engine Complete — Ready for Web Interface and Beta Testing

---

*"Did not our hearts burn within us while he talked with us on the road and opened the Scriptures to us?"*  
*— Luke 24:32*
