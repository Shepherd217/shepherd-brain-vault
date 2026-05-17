# StandoutLocal Stripe Integration Brief

**Repo:** https://github.com/Shepherd217/StandoutLocal  
**Local Clone:** `/root/.openclaw/workspace/standoutlocal-repo`  
**Tech Stack:** React 19 + TypeScript + Vite 7.2.4 + Tailwind CSS v3.4.19 + shadcn/ui + React Router (HashRouter) + Lucide React  
**Deployed To:** Vercel (vercel.json present with SPA rewrites)  
**Audit Date:** 2026-05-18  
**Audited By:** Ava

---

## 1. Full File Tree

```
./components.json                 # shadcn/ui component registry
./eslint.config.js                # ESLint configuration
./.gitignore                      # Git ignore rules
./index.html                       # HTML entry point (Vite)
./info.md                          # Project setup notes (40+ shadcn components)
./package.json                     # Dependencies (see below)
./package-lock.json               # Lock file
./postcss.config.js               # PostCSS config
./public/                          # Static assets
  demo-auto-after.jpg
  demo-auto-before.jpg
  demo-cleaning-after.jpg
  demo-cleaning-before.jpg
  demo-salon-after.jpg
  demo-salon-before.jpg
  hero-mockup-after.jpg
  hero-mockup-before.jpg
./README.md                        # Vite template README
./src/
  App.css                          # Default Vite styles (UNUSED - overrides removed in index.css)
  App.tsx                          # Router definition (4 routes)
  components/
    Footer.tsx                     # Site footer with links
    Layout.tsx                     # Layout wrapper (Navbar + Footer + Outlet + scroll restoration)
    Navbar.tsx                     # Navigation bar with CTA
    ui/                            # shadcn/ui components (40+ components)
      accordion.tsx, alert-dialog.tsx, alert.tsx, aspect-ratio.tsx,
      avatar.tsx, badge.tsx, breadcrumb.tsx, button-group.tsx, button.tsx,
      calendar.tsx, card.tsx, carousel.tsx, chart.tsx, checkbox.tsx,
      collapsible.tsx, command.tsx, context-menu.tsx, dialog.tsx, drawer.tsx,
      dropdown-menu.tsx, empty.tsx, field.tsx, form.tsx, hover-card.tsx,
      input-group.tsx, input-otp.tsx, input.tsx, item.tsx, kbd.tsx, label.tsx,
      menubar.tsx, navigation-menu.tsx, pagination.tsx, popover.tsx,
      progress.tsx, radio-group.tsx, resizable.tsx, scroll-area.tsx,
      select.tsx, separator.tsx, sheet.tsx, sidebar.tsx, skeleton.tsx,
      slider.tsx, sonner.tsx, spinner.tsx, switch.tsx, table.tsx, tabs.tsx,
      textarea.tsx, toggle-group.tsx, toggle.tsx, tooltip.tsx
  hooks/
    use-mobile.ts                  # Mobile detection hook
  index.css                        # Global styles + Tailwind directives + theme vars + shadcn base styles
  lib/
    utils.ts                       # cn() utility for Tailwind class merging
  main.tsx                         # Entry point (StrictMode + HashRouter)
  pages/
    Home.tsx                        # Landing page (HERO + TrustCheckForm + all sections)
    Pricing.tsx                     # Pricing page (4 tiers with feature lists)
    Process.tsx                     # Process page (5-step methodology)
    Privacy.tsx                     # Privacy policy
    Terms.tsx                       # Terms of service
./tailwind.config.js              # Tailwind theme config (shadcn theme extension)
./tsconfig.app.json               # TS config for app
./tsconfig.json                   # Root TS config
./tsconfig.node.json              # TS config for Vite/Node
./vercel.json                     # Vercel SPA rewrites (all routes → /index.html)
./vite.config.ts                  # Vite config (React plugin, @ alias, base: "/")
```

### Key Dependencies (package.json)
- `react` ^19.0.0, `react-dom` ^19.0.0
- `react-router-dom` ^7.5.2
- `vite` ^7.2.4
- `tailwindcss` ^4.1.4
- `lucide-react` ^0.488.0
- `@radix-ui/*` (via shadcn)
- `class-variance-authority`, `clsx`, `tailwind-merge`
- `embla-carousel-react` (carousel dependency)
- `recharts` (chart dependency)
- `react-hook-form`, `@hookform/resolvers`, `zod` (form handling)
- **NO Stripe packages installed yet** — will need `@stripe/stripe-js` and `@stripe/react-stripe-js` (or just redirect-to-checkout approach)

---

## 2. Current Router Setup (App.tsx)

```tsx
// File: src/App.tsx (Lines 1-30)
import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import Pricing from "./pages/Pricing";
import Process from "./pages/Process";
import Privacy from "./pages/Privacy";
import Terms from "./pages/Terms";

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/pricing" element={<Pricing />} />
        <Route path="/process" element={<Process />} />
        <Route path="/privacy" element={<Privacy />} />
        <Route path="/terms" element={<Terms />} />
      </Route>
    </Routes>
  );
}

export default App;
```

**Router Type:** HashRouter (from main.tsx)  
**Current Routes:** 5 (/, /pricing, /process, /privacy, /terms)  
**Needed Addition:** `/thank-you` route

---

## 3. Complete CTA Audit — Every Button, Location, Current Behavior

### External Form Action (Forminit — ALL CTAs currently point here)
All "Book a Call", "Get Started", "Get This Package", "Check Your Website", "Free Trust Check" buttons currently open:
```
https://forminit.com/f/ct8mfdi87d8q3q3ppr5edj6n
```

This is a Forminit external form. Every single paid CTA on the site currently dumps users to this generic form instead of Stripe checkout.

---

### CTA #1 — Hero Primary Button (Home.tsx)
- **File:** `src/pages/Home.tsx`
- **Line:** ~225 (within Hero section)
- **Current Code:**
  ```tsx
  <Button 
    className="bg-[#8C9A5C] hover:bg-[#7A8550] text-white px-6 py-6 text-base rounded-lg cursor-pointer"
    onClick={() => window.open('https://forminit.com/f/ct8mfdi87d8q3q3ppr5edj6n', '_blank')}
  >
    Check Your Website <ArrowRight className="ml-2 w-5 h-5" />
  </Button>
  ```
- **Current Behavior:** Opens Forminit form in new tab
- **Product:** N/A (lead capture, not purchase)
- **Stripe Replacement:** Keep as lead capture OR redirect to Free Trust Check flow
- **Recommended:** Keep as-is OR replace with `/pricing` navigation for better funnel

### CTA #2 — Hero Secondary Button (Home.tsx)
- **File:** `src/pages/Home.tsx`
- **Line:** ~245 (within Hero section)
- **Current Code:**
  ```tsx
  <Button 
    variant="outline" 
    className="border-[#7C9885] text-[#7C9885] hover:bg-[#7C9885]/10 px-6 py-6 text-base rounded-lg"
    onClick={() => navigate('/pricing')}
  >
    Get a New Website
  </Button>
  ```
- **Current Behavior:** Navigates to /pricing
- **Stripe Replacement:** No change needed — this is navigation, not purchase

### CTA #3 — Trust Check Link in Hero (Home.tsx)
- **File:** `src/pages/Home.tsx`
- **Line:** ~680 (inline link in hero paragraph)
- **Current Code:**
  ```tsx
  <a 
    href="https://forminit.com/f/ct8mfdi87d8q3q3ppr5edj6n" 
    target="_blank" 
    rel="noopener noreferrer"
    className="text-[#8C9A5C] hover:underline font-medium"
  >
    Free Trust Check
  </a>
  ```
- **Current Behavior:** Opens Forminit form in new tab
- **Product:** N/A (lead capture)
- **Stripe Replacement:** Keep as lead capture form

### CTA #4 — Trust Check Button in TrustCheckForm (Home.tsx)
- **File:** `src/pages/Home.tsx`
- **Line:** ~835 (at end of TrustCheckForm section)
- **Current Code:**
  ```tsx
  <Button 
    className="bg-[#8C9A5C] hover:bg-[#7A8550] text-white px-8 py-6 text-lg rounded-lg w-full sm:w-auto cursor-pointer"
    onClick={() => window.open('https://forminit.com/f/ct8mfdi87d8q3q3ppr5edj6n', '_blank')}
  >
    Free Trust Check <ArrowRight className="ml-2 w-5 h-5" />
  </Button>
  ```
- **Current Behavior:** Opens Forminit form in new tab
- **Product:** N/A (lead capture)
- **Stripe Replacement:** Keep as lead capture form

### CTA #5 — Pricing Page: "Free Trust Check" Button (Pricing.tsx)
- **File:** `src/pages/Pricing.tsx`
- **Line:** ~155 (Free Trust Check tier)
- **Current Code:**
  ```tsx
  <Button 
    className="w-full bg-[#8C9A5C]/10 hover:bg-[#8C9A5C]/20 text-[#8C9A5C] border border-[#8C9A5C]/30 mt-6"
    onClick={() => window.open('https://forminit.com/f/ct8mfdi87d8q3q3ppr5edj6n', '_blank')}
  >
    Free Trust Check
  </Button>
  ```
- **Current Behavior:** Opens Forminit form in new tab
- **Product:** N/A (free lead capture)
- **Stripe Replacement:** Keep as lead capture form

### CTA #6 — Pricing Page: "Get This Package" Button — Landing Page (Pricing.tsx)
- **File:** `src/pages/Pricing.tsx`
- **Line:** ~315 (Landing Page tier card)
- **Current Code:**
  ```tsx
  <Button 
    className="w-full bg-[#7C9885] hover:bg-[#6A8575] text-white mt-6"
    onClick={() => window.open('https://forminit.com/f/ct8mfdi87d8q3q3ppr5edj6n', '_blank')}
  >
    Get This Package
  </Button>
  ```
- **Current Behavior:** Opens Forminit form in new tab
- **Product:** Landing Page — $897 one-time
- **Stripe Replacement:** Redirect to `VITE_STRIPE_LANDING_PAGE_URL`
- **New Code:**
  ```tsx
  <Button 
    className="w-full bg-[#7C9885] hover:bg-[#6A8575] text-white mt-6"
    onClick={() => window.open(import.meta.env.VITE_STRIPE_LANDING_PAGE_URL, '_blank')}
  >
    Get This Package
  </Button>
  ```

### CTA #7 — Pricing Page: "Get This Package" Button — Full Refresh (Pricing.tsx)
- **File:** `src/pages/Pricing.tsx`
- **Line:** ~495 (Full Refresh tier card)
- **Current Code:**
  ```tsx
  <Button 
    className="w-full bg-[#8C9A5C] hover:bg-[#7A8550] text-white mt-6"
    onClick={() => window.open('https://forminit.com/f/ct8mfdi87d8q3q3ppr5edj6n', '_blank')}
  >
    Get This Package
  </Button>
  ```
- **Current Behavior:** Opens Forminit form in new tab
- **Product:** Full Refresh — $2497 one-time
- **Stripe Replacement:** Redirect to `VITE_STRIPE_REFRESH_URL`
- **New Code:**
  ```tsx
  <Button 
    className="w-full bg-[#8C9A5C] hover:bg-[#7A8550] text-white mt-6"
    onClick={() => window.open(import.meta.env.VITE_STRIPE_REFRESH_URL, '_blank')}
  >
    Get This Package
  </Button>
  ```

### CTA #8 — Pricing Page: "Get This Package" Button — Care Plan (Pricing.tsx)
- **File:** `src/pages/Pricing.tsx`
- **Line:** ~675 (Care Plan tier card)
- **Current Code:**
  ```tsx
  <Button 
    className="w-full bg-[#8C9A5C] hover:bg-[#7A8550] text-white mt-6"
    onClick={() => window.open('https://forminit.com/f/ct8mfdi87d8q3q3ppr5edj6n', '_blank')}
  >
    Get This Package
  </Button>
  ```
- **Current Behavior:** Opens Forminit form in new tab
- **Product:** Care Plan — $249/month recurring
- **Stripe Replacement:** Redirect to `VITE_STRIPE_CARE_PLAN_URL`
- **New Code:**
  ```tsx
  <Button 
    className="w-full bg-[#8C9A5C] hover:bg-[#7A8550] text-white mt-6"
    onClick={() => window.open(import.meta.env.VITE_STRIPE_CARE_PLAN_URL, '_blank')}
  >
    Get This Package
  </Button>
  ```

### CTA #9 — Pricing Page: "Book a Call" Button (Pricing.tsx)
- **File:** `src/pages/Pricing.tsx`
- **Line:** ~830 (Custom tier / bottom CTA)
- **Current Code:**
  ```tsx
  <Button 
    className="bg-[#8C9A5C] hover:bg-[#7A8550] text-white px-8 py-6 text-lg rounded-lg cursor-pointer"
    onClick={() => window.open('https://forminit.com/f/ct8mfdi87d8q3q3ppr5edj6n', '_blank')}
  >
    Book a Call <ArrowRight className="ml-2 w-5 h-5" />
  </Button>
  ```
- **Current Behavior:** Opens Forminit form in new tab
- **Product:** N/A (lead capture / consultation booking)
- **Stripe Replacement:** Keep as lead capture form (or replace with Calendly/Cal.com)

### CTA #10 — Navbar "Check Your Site" Button (Navbar.tsx)
- **File:** `src/components/Navbar.tsx`
- **Line:** ~108
- **Current Code:**
  ```tsx
  <Button
    className="bg-[#8C9A5C] hover:bg-[#7A8550] text-white rounded-lg text-sm"
    onClick={() => window.open('https://forminit.com/f/ct8mfdi87d8q3q3ppr5edj6n', '_blank')}
  >
    Check Your Site
  </Button>
  ```
- **Current Behavior:** Opens Forminit form in new tab
- **Product:** N/A (lead capture)
- **Stripe Replacement:** Keep as lead capture form

### CTA #11 — Process Page CTAs (Process.tsx)
- **File:** `src/pages/Process.tsx`
- **Multiple Lines:** ~130, ~290, ~480, ~640, ~800 (each step section)
- **Pattern:** Each step has a "Get Started" or "Start Your Project" or "Start With a Trust Check" button
- **Current Code Pattern (example from Step 1):**
  ```tsx
  <Button 
    className="bg-[#8C9A5C] hover:bg-[#7A8550] text-white mt-6"
    onClick={() => window.open('https://forminit.com/f/ct8mfdi87d8q3q3ppr5edj6n', '_blank')}
  >
    Get Started
  </Button>
  ```
- **Current Behavior:** Opens Forminit form in new tab
- **Stripe Replacement:** These are mid-funnel CTAs — **keep as lead capture** (they're not at purchase intent yet)

---

## 4. Current Pricing Page Structure (Pricing.tsx)

The pricing page currently shows **4 tiers:**

| Tier | Price | Description | Current CTA |
|------|-------|-------------|-------------|
| **Free Trust Check** | FREE | Single-page review, mobile check, CTA placement | "Free Trust Check" → Forminit |
| **Landing Page** | **$897** one-time | 1-page mobile-first site, 3 CTAs, review embed, Google setup | "Get This Package" → Forminit |
| **Full Refresh** | **$2,497** one-time | 3-5 pages, all Landing Page features + services, about, contact + blog setup | "Get This Package" → Forminit |
| **Care Plan** | **$249**/month | Monthly edits, performance monitoring, review integration, quarterly refresh | "Get This Package" → Forminit |
| **Custom** | "Let's Talk" | Large sites, booking integrations, multi-location | "Book a Call" → Forminit |

**Key Finding:** The prices shown ($897, $2,497, $249/mo) match the Stripe products Nathan specified. The "Custom" tier doesn't need a Stripe product (it's consultation-based).

---

## 5. Files That Need Changes

### File 1: `src/App.tsx` — Add /thank-you route
**Current:**
```tsx
<Route path="/terms" element={<Terms />} />
```
**Add After:**
```tsx
<Route path="/thank-you" element={<ThankYou />} />
```
**Also add import:**
```tsx
import ThankYou from "./pages/ThankYou";
```

### File 2: `src/pages/Pricing.tsx` — 3 CTAs need Stripe redirect
**Lines to change:** ~315, ~495, ~675
**Change pattern:**
```tsx
// FROM:
onClick={() => window.open('https://forminit.com/f/ct8mfdi87d8q3q3ppr5edj6n', '_blank')}

// TO:
onClick={() => window.open(import.meta.env.VITE_STRIPE_LANDING_PAGE_URL, '_blank')}
// or VITE_STRIPE_REFRESH_URL
// or VITE_STRIPE_CARE_PLAN_URL
```

### File 3: `src/pages/ThankYou.tsx` — NEW FILE (does not exist)
**Create at:** `src/pages/ThankYou.tsx`
**Content spec:**
- Route: `/thank-you`
- Content: Success message after Stripe payment
- Should show:
  - "Thank You! Your payment was successful."
  - Product name confirmation (passed via query params or session)
  - "We'll be in touch within 24 hours to schedule your kickoff call."
  - "Questions? Email hello@standoutlocal.dev"
- Style: Match existing brand colors (`#3C3836` text, `#8C9A5C` accents)
- Should use existing Layout component (automatically via App.tsx route nesting)

### File 4: `.env.example` — NEW FILE
**Create at:** `.env.example`
```
# Stripe Checkout URLs (Payment Links or Checkout Session URLs)
VITE_STRIPE_LANDING_PAGE_URL=https://buy.stripe.com/...
VITE_STRIPE_REFRESH_URL=https://buy.stripe.com/...
VITE_STRIPE_CARE_PLAN_URL=https://buy.stripe.com/...
```

### File 5: `vercel.json` — No changes needed
Current config already handles SPA routing correctly:
```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

### File 6: `vite.config.ts` — No changes needed
The `base: '/'` is correct for Vercel deployment.

### File 7: `src/main.tsx` — No changes needed
HashRouter is already configured.

---

## 6. Stripe Product Spec

| Product | Price | Type | Stripe Product Name | Environment Variable |
|---------|-------|------|---------------------|----------------------|
| **Landing Page** | $897 | One-time | `Landing Page - Standout Local` | `VITE_STRIPE_LANDING_PAGE_URL` |
| **Full Refresh** | $2,497 | One-time | `Full Refresh - Standout Local` | `VITE_STRIPE_REFRESH_URL` |
| **Care Plan** | $249/mo | Recurring monthly | `Care Plan - Standout Local` | `VITE_STRIPE_CARE_PLAN_URL` |

**Implementation Recommendation:** Use Stripe Payment Links (simplest for static site)
1. Create 3 products in Stripe Dashboard
2. Create 3 Payment Links (one per product)
3. Set success URL to `https://standoutlocal.dev/#/thank-you`
4. Copy Payment Link URLs to Vercel environment variables
5. No backend needed

**Alternative:** Stripe Checkout Sessions (requires backend webhook)
- More complex but allows post-payment automation
- Would need a serverless function on Vercel
- Not recommended for MVP

---

## 7. Environment Variables Needed

| Variable | Value | Set In |
|----------|-------|--------|
| `VITE_STRIPE_LANDING_PAGE_URL` | Stripe Payment Link for $897 | Vercel Dashboard + `.env.local` |
| `VITE_STRIPE_REFRESH_URL` | Stripe Payment Link for $2497 | Vercel Dashboard + `.env.local` |
| `VITE_STRIPE_CARE_PLAN_URL` | Stripe Payment Link for $249/mo | Vercel Dashboard + `.env.local` |

**Vite prefix:** All env vars must start with `VITE_` to be exposed to client-side code.

---

## 8. /thank-you Page Spec

### Route
- **Path:** `/thank-you`
- **Router Addition:** `src/App.tsx` — add `<Route path="/thank-you" element={<ThankYou />} />`

### Content
```tsx
// src/pages/ThankYou.tsx
import { CheckCircle, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

export default function ThankYou() {
  const navigate = useNavigate();
  
  return (
    <div className="min-h-screen bg-[#F5F5F0] py-24 px-4">
      <div className="max-w-2xl mx-auto text-center">
        <div className="w-20 h-20 bg-[#8C9A5C]/20 rounded-full flex items-center justify-center mx-auto mb-8">
          <CheckCircle className="w-10 h-10 text-[#8C9A5C]" />
        </div>
        
        <h1 className="text-4xl font-bold text-[#3C3836] mb-4">
          Thank You!
        </h1>
        
        <p className="text-lg text-[#5A524C] mb-6">
          Your payment was successful. We've received your order and will be in touch within 24 hours to schedule your kickoff call.
        </p>
        
        <div className="bg-white rounded-lg p-6 border border-[#E8E4DF] mb-8 text-left">
          <h3 className="font-semibold text-[#3C3836] mb-2">What happens next?</h3>
          <ul className="space-y-2 text-[#5A524C]">
            <li className="flex items-start gap-2">
              <span className="text-[#8C9A5C] font-bold">1.</span>
              <span>You'll receive a confirmation email within 5 minutes</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-[#8C9A5C] font-bold">2.</span>
              <span>We'll send a brief questionnaire to understand your business</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-[#8C9A5C] font-bold">3.</span>
              <span>Schedule your kickoff call (30 min) at your convenience</span>
            </li>
          </ul>
        </div>
        
        <p className="text-sm text-[#5A524C] mb-8">
          Questions? Email us at <a href="mailto:hello@standoutlocal.dev" className="text-[#8C9A5C] hover:underline">hello@standoutlocal.dev</a>
        </p>
        
        <Button
          variant="outline"
          className="border-[#7C9885] text-[#7C9885] hover:bg-[#7C9885]/10"
          onClick={() => navigate('/')}
        >
          <ArrowLeft className="mr-2 w-4 h-4" />
          Back to Home
        </Button>
      </div>
    </div>
  );
}
```

---

## 9. Deployment Notes

### What Needs to Happen on Vercel:
1. **Add 3 Environment Variables** in Vercel Dashboard:
   - `VITE_STRIPE_LANDING_PAGE_URL`
   - `VITE_STRIPE_REFRESH_URL`
   - `VITE_STRIPE_CARE_PLAN_URL`

2. **No serverless functions needed** if using Stripe Payment Links (recommended)

3. **Redeploy** after env vars are set (Vercel automatically rebuilds)

### What Gets Pushed in Code:
1. Modified `src/App.tsx` (new route)
2. Modified `src/pages/Pricing.tsx` (3 CTAs changed)
3. New `src/pages/ThankYou.tsx`
4. New `.env.example` (template only — real values go in Vercel)

### No Changes Needed:
- `vercel.json` (already handles SPA routing)
- `vite.config.ts` (base path correct)
- `src/main.tsx` (HashRouter already configured)
- Any other pages or components

---

## 10. Summary Checklist

- [ ] Create 3 Stripe products + Payment Links in Stripe Dashboard
- [ ] Add 3 environment variables to Vercel
- [ ] Modify `src/App.tsx` — add `/thank-you` route
- [ ] Modify `src/pages/Pricing.tsx` — 3 CTAs → Stripe URLs
- [ ] Create `src/pages/ThankYou.tsx` — success page
- [ ] Create `.env.example` — template for local dev
- [ ] Test all 3 payment flows end-to-end
- [ ] Set Payment Link success URLs to `https://standoutlocal.dev/#/thank-you`

---

**Brief prepared by:** Ava  
**Status:** Ready for implementation  
**Next Step:** Nathan to create Stripe products → share Payment Link URLs → Ava implements code changes
