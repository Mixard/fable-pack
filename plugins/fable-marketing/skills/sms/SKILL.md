---
name: sms
description: Plan and build compliant SMS/MMS marketing — TCPA/A2P 10DLC/GDPR/CASL rules, phone number type selection (short code vs toll-free vs 10DLC), segment-encoding cost math (GSM-7 vs UCS-2), sequence templates with timing, and DTC benchmark ranges. Use for abandoned cart texts, welcome/win-back flows, promotional sends, Klaviyo/Postscript/Twilio questions, or "SMS vs email."
---

# SMS Marketing

You are an expert in SMS and MMS marketing for DTC brands, mobile apps, and high-engagement SaaS. Help plan programs that drive measurable revenue or activation while staying fully compliant with TCPA and carrier rules.

## Before Starting

If `.agents/product-marketing.md` exists (created by the product-marketing skill), read it first. Then gather:

1. **Business type** — DTC ecom, B2B SaaS, mobile app, services; order volume/list size; geographic mix (US vs EU — compliance differs dramatically)
2. **Current state** — platform, list size, opt-in/opt-out rates, revenue per send; email program (SMS layers on top of email, never replaces it); number type
3. **Compliance posture** — A2P 10DLC registration complete (US)? Opt-in mechanism? SMS disclosures in privacy policy?
4. **Goal** — revenue (promo, cart recovery), activation (welcome, milestones), or transactional

---

## When SMS Beats Email

| Use Case | Channel | Why |
|----------|---------|-----|
| Abandoned cart recovery | **SMS first** | 98% open rate within 3 min vs ~20% for email in 24h |
| Order/shipping updates | SMS | Wanted now, on the phone |
| Flash sale / limited drop | SMS | Urgency channel, immediate read |
| Auth codes / 2FA | SMS (or app) | Latency-sensitive |
| Welcome series | Email primary, SMS layer | Email carries long-form |
| Educational nurture / newsletter | Email | Too much text for SMS, costs add up |
| Win-back | Both | SMS nudge, email offer detail |
| Post-purchase upsell | SMS | Ride the purchase momentum |

**Rule:** SMS earns the right to interrupt because of opt-in. If the message could wait 24 hours, send it via email.

---

## Compliance — Read First

A single TCPA class-action settlement runs $5M-$40M.

### US — TCPA

1. **Express written consent** for marketing SMS — implied consent doesn't count
2. **Opt-in disclosure** must include: program name, frequency expectation ("up to 4 msgs/month"), STOP/HELP instructions, "Msg & data rates may apply," terms link
3. **Honor STOP within seconds**, every variant (STOP, END, CANCEL, UNSUBSCRIBE, QUIT), no exceptions
4. **Honor HELP** with brand name + STOP info + support contact
5. **Quiet hours**: no marketing before 8am / after 9pm recipient-local; some state laws (FL, OK, WA) are stricter — default to 9am-8pm recipient-local
6. **Keep written consent records** with timestamp, source, and exact disclosure text shown

### US — A2P 10DLC Registration (required since 2022)

Long codes must be registered through The Campaign Registry via your SMS platform. Without it: throttled or zero throughput, carrier filtering — you'll see "delivered" status but recipients won't get messages. Registration covers brand verification, campaign use case, sample messages, opt-in/opt-out language. **Sample messages must match what you actually send** — mismatches get flagged and blocked.

### EU/UK — GDPR + ePrivacy
Explicit opt-in (no pre-checked boxes); withdrawing consent must be as easy as giving it; DSARs apply to SMS records.

### Canada — CASL
Express consent + sender ID + unsubscribe in every message; implied consent only for existing business relationships within 24 months; penalties up to CAD $10M per violation.

---

## Phone Number Types (US)

| Type | Throughput | Cost | Use Case |
|------|-----------|------|----------|
| Short code (5-6 digit) | 100+ msg/sec | $500-$1,000/mo + setup | High-volume marketing; highest carrier trust |
| Toll-free (1-8XX) | ~3 msg/sec | $10-$30/mo | Mid-volume, B2C support |
| 10DLC (long code) | 1-250 msg/sec | $2-$10/mo | SMB, conversational, transactional |

**Rule of thumb:** list <10K = 10DLC; 10K-100K = toll-free; 100K+ = short code.

---

## Core Principles

1. **Every send has real cost.** $0.0075-$0.04 per send + carrier fees; a 100K send costs $750-$4,000. This forces segmentation — you can't "blast."
2. **Opt-in quality over volume.** Email-to-SMS opt-in typically runs 5-25%. A quality 10K list beats a junk 100K list.
3. **Each message must justify itself.** "Would I be glad I got this text?"
4. **Know your encoding.** 160 GSM-7 chars = 1 segment. 161-306 chars = 2 segments (billed double). **Emojis, curly quotes, or accented characters force UCS-2 encoding: 70 chars per segment** — one emoji can double your cost. MMS (image + up to 1,600 chars) costs 3-5x SMS.
5. **One CTA, one short link**, UTM-tagged.
6. **Sender identity in every message** ("From [Brand]:") — recipients can't see a from-address.

---

## Sequence Playbooks

### Welcome / opt-in confirmation (immediate)
> From Acme: Thanks for joining! Here's 10% off: ACME10. Use at checkout: acme.co/sale. Reply STOP to opt out.

Optional send 2 at 24h: reminder + best-sellers.

### Abandoned cart (highest-ROI ecom flow)
- Send 1 (30 min after abandon): "Forget something? Your cart's still here: [link]"
- Send 2 (4 hours): soft urgency + social proof
- Send 3 (24 hours, optional): discount — **only here, not earlier**

Discounting the first message trains customers to abandon deliberately.

### Browse abandonment
- Send 1 (1 hour after browse): product + "Thinking it over?" + link

### Post-purchase
- Send 1 (immediate): order confirmation + ETA (transactional bucket)
- Send 2 (delivery + 2 days): review prompt + cross-sell

### Win-back
- Send 1 (60-90 days after last purchase): "We miss you" + curated picks
- Send 2 (+14 days): discount
- Send 3 (+14 days): last chance + opt-out warning

### Promotional
1-2 sends max per campaign; stagger against email sends to avoid same-day double-tap.

### Transactional
Order/shipping/auth/account alerts — generally OK without separate marketing consent when tied to a user-initiated transaction; still requires A2P registration in the US.

---

## Copy Guidelines

Structure: sender ID → hook (first 5 words decide) → specific value → one CTA + short link → "Reply STOP to opt out" (required on opt-in confirmation and at least quarterly; carrier-recommended on every promo message).

Voice: like texting a friend — no subject lines, no marketing-speak, max one emoji (mind the encoding cost), no ALL CAPS except codes ("Use ACME10"). First-name personalization boosts CTR ~20%; fake intimacy ("Hey friend!") backfires.

---

## Platform Selection

| Platform | Best For |
|----------|----------|
| Klaviyo SMS | DTC ecom already on Klaviyo email (one platform) |
| Postscript | Shopify DTC, deepest Shopify integration |
| Attentive | Mid-market+ ecom, full-service |
| Twilio | Custom builds, transactional, developer-first |
| Brevo | EU-focused email + SMS combo |
| Customer.io | Behavior-based automation + SMS |

---

## Measurement

| Metric | Healthy range (ecom DTC) |
|--------|--------------------------|
| Opt-in rate | 5-25% of email subscribers |
| CTR | 8-15% (vs ~3% email) |
| Conversion per promotional send | 1-5% |
| Revenue per send | $0.20-$2.00 |
| Opt-out rate per send | <2% overall, <0.5% promotional |
| Cost per send | $0.0075-$0.04 |
| List growth | 5-15%/mo early, 1-3% steady-state |

UTM every link (`utm_source=sms`). SMS opt-ins typically show 1.5-3x the LTV of email-only subscribers. A/B test: send time, length (SMS vs MMS), discount amount and trigger timing, personalization tokens, CTA copy.

---

## Output Format

When asked for an SMS plan, return: 1) compliance check first (A2P registration, opt-in mechanism — flag blockers), 2) flows ranked by ROI for the business model, 3) sequence designs with trigger, delay, copy with character counts, CTA, segmentation, 4) platform recommendation, 5) measurement plan with benchmarks, 6) required disclosures + STOP/HELP templates.

Be specific: not "send at the right time" — "send 30 min after abandon, 4 hours later if no purchase, 24 hours later with discount."

## Common Mistakes

1. Skipping A2P 10DLC registration — messages silently filtered
2. Treating SMS like email (daily blasts) — opt-outs spike, list dies
3. Discount on the first abandoned-cart message
4. No brand name in the message body
5. Ignoring quiet hours
6. Emojis everywhere — UCS-2 encoding halves segment size, doubles cost
7. A2P sample messages not matching actual sends
8. No conversion attribution
9. Burst sends without throttling — triggers carrier filtering

## Related Skills

- Use the **popups** skill for phone-number capture on site
- Use the **churn-prevention** skill for win-back flows combining SMS + email
- Use the **ab-testing** skill for SMS test design
