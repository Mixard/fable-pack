---
name: popups
description: Create and optimize popups, modals, slide-ins, and banners that convert without annoying users — trigger thresholds (scroll depth, exit intent, time delays), conversion benchmarks by popup type, sizing and frequency-capping rules, and mobile/SEO compliance. Use for exit intent, email capture popups, announcement banners, sticky bars, or "collect emails with a popup."
---

# Popup CRO

You are an expert in popup and modal optimization. Create popups that convert without damaging user experience or brand perception.

## Before Starting

If `.agents/product-marketing.md` exists (created by the product-marketing skill), read it first. Then understand: the popup's purpose (email capture, lead magnet, discount, announcement, exit save), current performance and triggers, traffic sources, new vs returning visitors, and mobile share.

## Core Principles

1. **Timing is everything** — too early is an interruption, too late is a missed opportunity
2. **Value must be obvious** — a clear, immediate benefit relevant to the page, worth the interruption
3. **Respect the user** — easy to dismiss, no traps or tricks, remember preferences

---

## Trigger Strategies

| Trigger | Settings that work | Best For |
|---------|-------------------|----------|
| Time-based | 30-60 seconds (not "after 5 seconds" — proven engagement first) | General site visitors |
| Scroll-based | 25-50% scroll depth | Blog posts, long-form ("You're halfway through — get more like this") |
| Exit intent | Cursor moving to close/leave | E-commerce, lead gen; last-chance capture |
| Click-triggered | User initiates (button/link) | Lead magnets, gated content — zero annoyance, highest conversion |
| Page count | After X pages in session | Multi-page research behavior |
| Behavior-based | Cart abandonment, pricing page visits, repeat views | High-intent segments |

Mobile can't detect exit intent — use back-button or scroll-up triggers instead.

## Benchmarks

| Popup Type | Typical Conversion |
|------------|-------------------|
| Email capture popup | 2-5% |
| Exit intent | 3-10% |
| Click-triggered | 10%+ (self-selected) |

Track: impression rate, conversion rate, immediate close rate, time to close.

---

## Popup Types

### Email capture
Clear value prop (not just "Subscribe"), specific benefit and cadence ("Weekly tips in 5 min"), single field, optional incentive. Copy: benefit/curiosity headline → what they get and how often → specific CTA ("Get Weekly Tips").

### Lead magnet
Show what they get (cover image/preview), tangible promise, minimal fields, instant-delivery expectation.

### Discount/promotion
Clear discount (10%, $20, free shipping), deadline, single use per visitor, easy-to-apply code.

### Exit intent
Acknowledge they're leaving; use a **different** offer than the entry popup; address a common objection. Formats: "Wait! Before you go..." / "Get 10% off your first order" / "Questions? Chat with us."

### Announcement banner
Top of page, single message, dismissable, links to detail, time-limited — don't leave it forever.

### Slide-in
Enters from a corner, doesn't block content, easy to dismiss — for chat, support, secondary CTAs.

---

## Design Rules

- **Hierarchy:** headline → value/offer → form/CTA → visible close option
- **Sizing:** desktop 400-600px wide; never cover the whole screen; mobile: bottom slide-up or centered card, not full-screen
- **Close button:** visible top-right (users who can't find it bounce entirely), tappable on mobile, "No thanks" text link, click-outside-to-close
- **Imagery:** product preview or a face (builds trust) — optional; copy can carry it

### Copy Formulas

- Headlines: "Get [result] in [timeframe]" / "Want [outcome]?" / "Join [X] people who..." / curiosity ("The one thing [audience] gets wrong about [topic]")
- Subheads: expand the promise, kill an objection ("No spam, ever"), set expectations
- CTAs: first person converts better — "Get My Discount" over "Get Your Discount"; specific over generic — "Send Me the Guide" over "Submit"
- Decline links: polite, never guilt-trippy. "No thanks" / "Maybe later" — never "No, I don't want to save money"

---

## Frequency & Targeting Rules

- Show max once per session; remember dismissals (cookie/localStorage) for **7-30 days**
- Exclude converted users and recent dismissers
- Target by traffic source (match the ad message), page type (context-relevant offer), new vs returning
- Exclude checkout and conversion flows entirely

## Compliance & Accessibility

- **GDPR:** clear consent language, privacy policy link, no pre-checked opt-ins
- **Accessibility:** keyboard navigable (Tab/Enter/Esc), focus trap while open, screen-reader compatible, sufficient contrast
- **Google:** intrusive interstitials hurt mobile SEO — no full-screen popups before content on mobile; cookie notices and reasonable banners are fine

---

## Strategy by Business Type

| Business | Layered Strategy |
|----------|------------------|
| E-commerce | Entry/scroll: first-purchase discount → exit intent: bigger discount → cart abandonment: complete order |
| B2B SaaS | Click-triggered: demo/lead magnets → scroll: newsletter → exit intent: trial reminder or content |
| Content/media | Scroll: newsletter after engagement → page count: subscribe on repeat visits → exit intent |
| Lead gen | Time-delayed: list building → click-triggered: specific magnets → exit intent: final capture |

When running multiple popups, define conflict rules so they never stack in one session.

## Experiment Ideas

- **Triggers:** exit intent vs 30s delay vs 50% scroll; delay length (10/30/60s); scroll depth (25/50/75%)
- **Format:** center modal vs corner slide-in; sticky vs static banner; with/without countdown timer (only if the deadline is real)
- **Copy:** urgency vs value framing; CTA text; decline-link tone
- **Personalization:** by traffic source, pages visited, new vs returning
- **Frequency:** once per session vs once per week; cool-down length; escalating offers over repeat visits

## Output Format

For each recommended popup: type, trigger, targeting, frequency rules, full copy (headline/subhead/CTA/decline), and design notes (layout, imagery, mobile behavior). Plus test hypotheses with expected outcomes.

## Related Skills

- Use the **ab-testing** skill to test popup variations properly
- Use the **sms** skill for phone-capture popups feeding SMS programs
