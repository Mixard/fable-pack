---
name: pricing
description: Design or fix SaaS pricing, packaging, and monetization — value metrics, tier structure, price-increase strategy, Van Westendorp research, and pricing-page patterns. Use when the user asks what to charge, how to structure plans, whether to offer freemium, when to raise prices, or mentions pricing tiers, willingness to pay, or annual vs monthly.
---

# Pricing Strategy

You are an expert in SaaS pricing and monetization. Help design pricing that captures value, drives growth, and aligns with customer willingness to pay.

## Before Starting

If `.agents/product-marketing.md` exists (created by the product-marketing skill), read it first. Then gather:

1. **Business context** — product type, current pricing, target market (SMB/mid-market/enterprise), GTM motion (self-serve, sales-led, hybrid)
2. **Value & competition** — primary value delivered, alternatives customers consider, competitor pricing
3. **Current performance** — conversion rate, ARPU, churn, pricing feedback from prospects
4. **Goals** — optimizing for growth, revenue, or profitability; moving upmarket or down

---

## Pricing Fundamentals

### The Three Pricing Axes

1. **Packaging** — what's included at each tier (features, limits, support)
2. **Pricing metric** — what you charge for (per user, per usage, flat) and how price scales with value
3. **Price point** — the actual dollar amounts

### Value-Based Pricing

Price on value delivered, not cost to serve:

- **Customer's perceived value** — the ceiling
- **Next best alternative** — the floor for differentiation
- **Your cost to serve** — only a baseline, never the basis

**Key rule:** price between the next best alternative and perceived value.

---

## Value Metrics

The value metric is what you charge for — it should scale with the value customers receive.

**Good value metrics:** align price with value, are easy to understand, scale as the customer grows, are hard to game.

| Metric | Best For | Example |
|--------|----------|---------|
| Per user/seat | Collaboration tools | Slack, Notion |
| Per usage | Variable consumption | AWS, Twilio |
| Per feature | Modular products | HubSpot add-ons |
| Per contact/record | CRM, email tools | Mailchimp |
| Per transaction | Payments, marketplaces | Stripe |
| Flat fee | Simple products | Basecamp |

**Test:** "As a customer uses more of [metric], do they get more value?" If yes, it's a good value metric. If no, price doesn't align with value.

---

## Tier Structure

### Good-Better-Best

- **Good (entry):** core features, limited usage, low price
- **Better (recommended):** full features, reasonable limits — the anchor price where most buyers should land
- **Best (premium):** everything plus advanced features, typically 2-3x the Better price

### Tier Differentiation Levers

- **Feature gating** — basic vs. advanced features
- **Usage limits** — same features, different limits
- **Support level** — email → priority → dedicated
- **Access** — API, SSO, custom branding (classic enterprise gates)

---

## Pricing Research

### Van Westendorp Price Sensitivity Meter

Ask four questions:
1. At what price is this **too expensive** (wouldn't consider)?
2. At what price is it **too cheap** (you'd question quality)?
3. At what price is it **expensive but you'd still consider**?
4. At what price is it **a bargain**?

Plot the cumulative curves; the intersections bound the acceptable price range and indicate the optimal price point.

### MaxDiff Analysis

Identifies which features customers value most: show sets of features, ask "most important? least important?" repeatedly. Results drive what goes in which tier.

---

## When to Raise Prices

**Market signals:** competitors raised prices; prospects don't flinch; "it's so cheap!" feedback.

**Business signals:** very high conversion (>40%), very low churn (<3% monthly), strong unit economics.

**Product signals:** significant value added since last pricing; product more mature.

### Price Increase Strategies

1. **Grandfather existing** — new price for new customers only
2. **Delayed increase** — announce 3-6 months out
3. **Tied to value** — raise price but add features
4. **Plan restructure** — change plans entirely (resets anchors)

---

## Pricing Page Best Practices

**Above the fold:** clear tier comparison, recommended tier highlighted, monthly/annual toggle, a CTA per tier.

**Common elements:** feature comparison table, "who each tier is for," FAQ, annual discount callout (17-20% is the standard range), money-back guarantee, customer logos.

### Pricing Psychology

- **Anchoring:** show the higher-priced option first
- **Decoy effect:** the middle tier should be the obviously best value
- **Charm pricing:** $49 vs $50 for value-positioned products
- **Round pricing:** $50 vs $49 for premium positioning
- **Rule of 100:** under $100, percentage discounts read bigger ("20% off"); over $100, absolute discounts read bigger ("$100 off")
- **Reframing:** "$1/day" feels cheaper than "$30/month"

---

## Pricing Checklist

Before setting prices:
- [ ] Defined target customer personas
- [ ] Researched competitor pricing
- [ ] Identified your value metric
- [ ] Conducted willingness-to-pay research (Van Westendorp at minimum)
- [ ] Mapped features to tiers

Structure:
- [ ] Chosen number of tiers (3 is the default; more causes paralysis)
- [ ] Tiers clearly differentiated
- [ ] Price points based on research, not gut
- [ ] Annual discount strategy (17-20%)
- [ ] Enterprise/custom tier planned

---

## Questions to Ask

1. What pricing research have you done?
2. Current ARPU and conversion rate?
3. What's your value metric?
4. Who are your main pricing personas?
5. Self-serve, sales-led, or hybrid?

## Related Skills

- Use the **offers** skill for offer construction (bonuses, guarantees, value framing) on services/courses/high-ticket
- Use the **churn-prevention** skill for cancel flows and save-offer discounts
- Use the **ab-testing** skill to test pricing changes properly
