# Standout Local × m0h Method — Cleaning Company Lead Pipeline
**Adaptation Date:** 2026-05-10 | **Campaign:** Champaign-Urbana Cleaning (Move-Out Season)

---

## The Core Insight

m0h's method finds **businesses with visible gaps** on Google Maps. Our method audits **website conversion gaps**.

**Combined:** We find cleaning companies with weak web presence → score them → build demo pages → close.

---

## Adapted 5-Step Pipeline

### Step 1 — Define Cleaning Company Signals (Our 4 Signals)

| Signal | What to Look For | Why It Matters |
|--------|------------------|----------------|
| **Low review count** | Under 30 Google reviews | Customers pick the 200-review competitor every time |
| **No website OR weak website** | No site, or site missing: booking form, mobile optimization, service pages | Can't convert searchers into bookings |
| **No review responses** | Owner never replies to reviews | Signals "nobody's home" to future customers |
| **Missing move-out/deep cleaning pages** | Only lists "regular cleaning", no specialized services | Missing the highest-urgency search terms |

**Two or more signals = qualified prospect.**

---

### Step 2 — Scrape Champaign-Urbana Cleaning Companies

**Search Queries:**
- "move out cleaning champaign il"
- "apartment cleaning urbana il"
- "deep cleaning savoy il"
- "rental turnover cleaning champaign county"
- "post construction cleaning campustown"

**Tools:**
- Google Maps + Instant Data Scraper (m0h method)
- OR: Manual search + our existing lead collection

**Data to collect:**
- Business name
- Phone number
- Website (if any)
- Review count
- Star rating
- Services listed
- Hours
- Address

---

### Step 3 — Claude Code Audit Pipeline

**Stage 1: Filter Prospects**

```
Read the file champaign-cleaning-leads.csv. Each row is a cleaning company from Google Maps.

For each row, score it 0-4 based on:
1. Review count under 30
2. No website listed OR website missing booking form
3. Star rating below 4.0
4. Missing move-out/deep cleaning service pages

Output prospects.csv with only score >= 2.
Add columns: signal_score, signal_notes, website_url_if_any.
Sort by signal_score descending.
```

**Stage 2: Deep Website Audit (Our 100-Point Rubric)**

For each prospect WITH a website:
- Run our existing 100-point rubric
- Score: Speed, Mobile, SEO, Trust, Conversion, Content
- Flag critical gaps: No booking form, no FAQ, no testimonials, slow load

**Stage 3: Build Demo Concept**

For top 5 prospects:
- Suggest specific demo landing page concept
- Example: "Move-Out Cleaning Champaign — Book in 60 Seconds"
- Reference their actual gaps from signal_notes

**Stage 4: Write Personalized Outreach**

```
Read prospects.csv. For each row with signal_score >= 3, write a cold email:

Rules:
- Lowercase, friendly, no corporate filler
- Lead with ONE specific observation about THEIR listing/website
- Mention ONE thing they're doing well (find it in the data)
- Offer a free 5-minute website audit — never ask for a call
- Maximum 4 short paragraphs
- Sign off: "best, [name]"

Subject line references the specific gap.
Output outreach.csv with: business_name, phone, email, signal_notes, subject, body, demo_concept.
```

---

### Step 4 — The Call (Adapted from m0h)

**Opening 10 seconds (memorize this):**

> *"Hey, is this [name]? I was looking at your Google listing this morning and noticed you don't have a website linked — or your site doesn't have a booking form. Is that something you've been meaning to fix, or is it just not a priority right now?"*

**Why this works for cleaning companies:**
- Move-out season is RIGHT NOW (students leaving, landlords turning units)
- Every day without a booking form = lost $150-400 jobs
- The competitor with "Book Now" button gets the call every time

**The three objections:**

1. **"Not interested"** → "Yeah, totally fair. I just noticed the [missing booking form / low reviews / no move-out page] thing because the cleaning companies ranking above you are getting most of the calls. Takes 30 seconds, then you decide."

2. **"Send me an email"** → "Happy to send it over. Quick question — is the missing booking form something you'd want fixed this month, or are you good with how things are running? Just so I know what to put in the email."

3. **"How much?"** → "Good question, depends on the setup. Honestly the easiest way is I hop on a quick 15-minute call this week, look at your setup, and send you a number that actually fits. Does tomorrow at 10 work?"

**Book the meeting:**
- "I'd love to put together a quick walkthrough of what fixing your web presence would look like — specifically for move-out season. It's free, takes 15 minutes, and you decide at the end. Does tomorrow at 10am work?"

---

### Step 5 — Close and Deliver

**Show the gap:**
- Screen-share their current site (or lack thereof)
- Show competitor sites with "Book Now" buttons
- Show Google search results — they're invisible

**Show the fix (3 options based on gap):**
1. **No website** → One-page conversion-focused landing page with booking form
2. **Has site, no booking** → Add booking form + optimize for mobile
3. **Has booking, weak SEO** → Add FAQ schema, service pages, local SEO

**Ask for the sale:**
- "So this is what I'd build for you. Want me to put it together this week?"
- **Stop talking. Let silence sit.**

**If yes:**
- Invoice within the hour
- Start same day
- Deliver in 48 hours
- Ask for testimonial + 2 referrals

---

## Our Existing Assets to Leverage

| Asset | How We Use It |
|-------|---------------|
| **100-point rubric** | Stage 2 deep audit — score every prospect's website |
| **Demo landing pages** | Pre-built concepts for cleaning companies (move-out, deep clean, apartment turnover) |
| **Audit JSONs** | Structured data we can feed to Claude for automated analysis |
| **GitHub repo** | Portfolio proof — "here's what we built for [similar company]" |
| **Vercel deployment** | Instant demo — "here's your site, live, right now" |

---

## Next Actions

1. **Scrape leads** — Run Google Maps searches for Champaign-Urbana cleaning companies
2. **Build CSV** — Name, phone, website, reviews, services, address
3. **Claude filter** — Run Stage 1 prospect scoring
4. **Deep audit top 10** — Run 100-point rubric on their websites
5. **Build outreach CSV** — Stage 3+4 personalized emails
6. **Start calling** — Use the 10-second opener, book meetings

---

## Move-Out Season Urgency

**Why NOW:**
- Students leaving UIUC (May-August)
- Landlords turning units for fall
- Parents helping kids clean out apartments
- Property managers scheduling bulk cleanings

**The pitch:** *"Every day your site doesn't have a 'Book Move-Out Cleaning' button, your competitor gets that $300 job. Move-out season doesn't wait."*

---

*This combines m0h's Google Maps prospecting with our existing audit infrastructure. The result: a systematic, repeatable pipeline for finding and closing cleaning company clients in Champaign-Urbana.*
