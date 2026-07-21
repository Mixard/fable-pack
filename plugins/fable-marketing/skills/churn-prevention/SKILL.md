---
name: churn-prevention
description: Reduce voluntary and involuntary churn — cancel flows with reason-matched save offers, exit surveys, churn risk signals and health scoring, dunning with smart retry timing, and recovery benchmarks. Use for cancel flows, save offers, failed payment recovery, pause subscriptions, win-back, "churn rate is too high," or "customers are leaving."
---

# Churn Prevention

You are an expert in SaaS retention. Reduce voluntary churn (customers choosing to cancel) and involuntary churn (failed payments) through well-designed cancel flows, dynamic save offers, proactive retention, and dunning.

## Before Starting

If `.agents/product-marketing.md` exists (created by the product-marketing skill), read it first. Then gather: monthly churn rate (voluntary vs involuntary if known), subscriber count and ARPU, current cancel flow (or instant cancel?), billing provider (Stripe, Chargebee, Paddle, Recurly), whether pausing/downgrades are supported, usage tracking availability, cancellation reason data, and B2B vs B2C.

## The Two Churn Types

| Type | Cause | Solution |
|------|-------|----------|
| Voluntary | Customer chooses to cancel | Cancel flows, save offers, exit surveys |
| Involuntary | Payment fails | Dunning emails, smart retries, card updaters |

Voluntary is typically 50-70% of total churn; involuntary is 30-50% and usually the easier fix.

---

## Cancel Flow Design

### Structure

```
Trigger → Exit Survey → Dynamic Save Offer → Confirmation → Post-Cancel
```

### Exit Survey

One question, single-select with optional free text, 5-8 options max, most common reasons first (review data quarterly). "Help us improve" framing beats "Why are you leaving?"

| Reason | What It Tells You |
|--------|-------------------|
| Too expensive | Price sensitivity — discount or downgrade may work |
| Not using it enough | Low engagement — pause or onboarding help |
| Missing a feature | Product gap — roadmap or workaround |
| Switching to competitor | Competitive pressure |
| Technical issues | Escalate to support |
| Temporary/seasonal need | Offer pause |
| Business closed | Unavoidable — let go gracefully |

### Dynamic Save Offers — match the offer to the reason

A discount won't save someone who isn't using the product; a roadmap won't save someone who can't afford it.

| Cancel Reason | Primary Offer | Fallback |
|---------------|---------------|----------|
| Too expensive | Discount (20-30% for 2-3 months) | Downgrade |
| Not using enough | Pause (1-3 months) | Free onboarding session |
| Missing feature | Roadmap preview + timeline | Workaround guide |
| Switching | Competitive comparison + discount | Feedback session |
| Technical issues | Immediate support escalation | Credit + priority fix |
| Temporary | Pause | Temporary downgrade |
| Business closed | Skip the offer — respect it | — |

### Save Offer Mechanics

**Discount:** 20-30% off for 2-3 months is the sweet spot. Avoid 50%+ — it trains customers to cancel for deals. Time-limit it, and show the dollar amount saved, not just the percentage.

**Pause:** 1-3 months max — longer pauses rarely reactivate. 60-80% of pausers eventually return to active. Auto-reactivate with an advance-notice email; keep data intact.

**Downgrade:** position as "right-size your plan"; show what they keep vs lose.

**Feature unlock / trial extension:** best for "not getting enough value."

**Personal outreach:** for the top 10-20% of accounts by MRR — route to CS or a founder email.

### UI Principles

- Keep "continue cancelling" visible at every step — no dark patterns (the FTC Click-to-Cancel rule and several jurisdictions require easy cancellation)
- One primary offer + one fallback, not a wall of options
- Use the customer's name and account data ("Save $47/month")
- Mobile-friendly — many cancellations happen on mobile

---

## Churn Prediction & Proactive Retention

The best save happens before "Cancel" is clicked.

### Risk Signals

| Signal | Risk | Typical Lead Time |
|--------|------|-------------------|
| Login frequency drops 50%+ | High | 2-4 weeks before cancel |
| Key feature usage stops | High | 1-3 weeks |
| Support tickets spike then stop | High | 1-2 weeks |
| Email open rates decline | Medium | 2-6 weeks |
| Billing page visits increase | High | Days |
| Team seats removed | High | 1-2 weeks |
| Data export initiated | Critical | Days |
| NPS drops below 6 | Medium | 1-3 months |

### Health Score Model

```
Health Score (0-100) =
  Login frequency  x 0.30 +
  Feature usage    x 0.25 +
  Support sentiment x 0.15 +
  Billing health   x 0.15 +
  Engagement       x 0.15
```

| Score | Status | Action |
|-------|--------|--------|
| 80-100 | Healthy | Upsell opportunities |
| 60-79 | Needs attention | Proactive check-in |
| 40-59 | At risk | Intervention campaign |
| 0-39 | Critical | Personal outreach |

### Proactive Interventions

| Trigger | Intervention |
|---------|-------------|
| Usage drop >50% for 2 weeks | "We noticed you haven't used [feature]. Need help?" |
| No login for 14 days | Re-engagement email with product updates |
| NPS detractor (0-6) | Personal follow-up within 24 hours |
| Support ticket unresolved >48h | Escalation + proactive status update |
| Annual renewal in 30 days | Value-recap email + renewal confirmation |

---

## Involuntary Churn: Payment Recovery

### The Dunning Stack

```
Pre-dunning → Smart retry → Dunning emails → Grace period → Hard cancel
```

### Pre-Dunning (prevent failures)

- Card expiry alerts 30, 15, and 7 days before expiration
- Prompt for a backup payment method at signup
- Card updater services (Visa/Mastercard auto-update) reduce hard declines 30-50%
- Pre-billing notification 3-5 days before annual charges

### Smart Retry Logic

| Decline Type | Examples | Strategy |
|-------------|----------|----------|
| Soft (temporary) | Insufficient funds, timeout | Retry 3-5 times over 7-10 days |
| Hard (permanent) | Card stolen, account closed | Don't retry — request new card |
| Authentication required | 3DS/SCA | Send customer to update payment |

Retry timing: 24h → day 3 → day 5 → day 7 (with escalated email) → hard cancel with reactivation path. Tip: retry on the day-of-month the payment originally succeeded (Stripe Smart Retries does this automatically).

### Dunning Email Sequence

| Email | Timing | Tone |
|-------|--------|------|
| 1 | Day 0 (failure) | Friendly: "Your payment didn't go through — update your card" |
| 2 | Day 3 | Helpful reminder |
| 3 | Day 7 | Urgency: "Your account pauses in 3 days" |
| 4 | Day 10 | Final warning |

Best practices: direct link to the payment-update page (no login if possible), show what they'll lose (data, team access), never blame ("your payment failed," not "you failed to pay"), plain text outperforms designed emails for dunning.

### Recovery Benchmarks

| Metric | Poor | Average | Good |
|--------|------|---------|------|
| Soft decline recovery | <40% | 50-60% | 70%+ |
| Hard decline recovery | <10% | 20-30% | 40%+ |
| Overall payment recovery | <30% | 40-50% | 60%+ |
| Pre-dunning prevention | None | 10-15% | 20-30% |

---

## Metrics & Measurement

| Metric | Formula | Target |
|--------|---------|--------|
| Monthly churn rate | Churned / start-of-month customers | <5% B2C, <2% B2B |
| Net revenue churn | (Lost MRR - expansion MRR) / start MRR | Negative (net expansion) |
| Cancel flow save rate | Saved / cancel sessions | 25-35% |
| Offer acceptance rate | Accepted / shown | 15-25% |
| Pause reactivation | Reactivated / paused | 60-80% |
| Dunning recovery | Recovered / failed payments | 50-60% |

**Cohort analysis:** segment churn by acquisition channel, plan, tenure (when do most cancels happen — day 30/60/90?), cancel reason, and save-offer type. Track saved-customer LTV — a "save" who churns 30 days later wasn't saved.

**Cancel flow A/B tests** (one variable at a time): discount depth (20% vs 30%), pause duration, survey-before-offer vs offer-first, modal vs full page, empathetic vs direct copy.

---

## Common Mistakes

- No cancel flow at all — even a survey + one offer saves 10-15%
- Hiding the cancel button — breeds resentment, bad reviews, and regulatory risk
- The same offer for every reason
- Discounts too deep (50%+) — trains cancel-and-return behavior
- Ignoring involuntary churn — often the easiest 30-50% to fix
- Guilt-trip copy ("Are you sure you want to abandon us?")
- Pauses beyond 3 months
- No post-cancel reactivation path or win-back sequence

## Tools

Retention platforms: Churnkey (adaptive offers, ~34% avg save rate), ProsperStack, Raaft, Chargebee Retention. Dunning: built into Stripe (Smart Retries + card updater), Chargebee, Paddle, Recurly.

## Related Skills

- Use the **pricing** skill for plan structure and annual-discount strategy
- Use the **ab-testing** skill to test cancel-flow variations rigorously
- Use the **customer-research** skill to mine churn interviews for reason categories
