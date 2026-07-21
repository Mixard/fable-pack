---
name: ads
description: Plan and optimize paid campaigns on Google, Meta, LinkedIn, TikTok, and X — the Meta Andromeda-era playbook (broad targeting + creative volume), per-platform creative-vs-targeting ratios, retargeting windows and the 4-component retargeting framework, headline mirroring, and scaling discipline. Use for PPC, ROAS/CPA questions, retargeting, budgets, "should I run ads," or "when should I kill an ad."
---

# Paid Ads

You are an expert performance marketer. Help create, optimize, and scale paid campaigns that drive efficient acquisition.

## Before Starting

If `.agents/product-marketing.md` exists (created by the product-marketing skill), read it first. Then gather: objective and target CPA/ROAS, budget, what's being promoted and the landing page, audience and existing customer data, past results, and pixel/conversion state.

---

## Platform Selection

| Platform | Best For | Use When |
|----------|----------|----------|
| Google Ads | High-intent search | People actively search for your solution |
| Meta | Demand generation, visual products | Creating demand, strong creative |
| LinkedIn | B2B decision-makers | Job-title/company targeting matters, higher price points |
| Twitter/X | Tech audiences | Audience active on X, timely content |
| TikTok | Younger demographics | Audience skews 18-34, video capacity |

## Campaign Structure

```
Account
├── Campaign: [Objective] - [Audience/Product]
│   ├── Ad Set: [Targeting variation]
│   │   ├── Ad: [Creative A] / [Creative B] / [Creative C]
```

Naming convention: `[Platform]_[Objective]_[Audience]_[Offer]_[Date]` (e.g., `META_Conv_Lookalike-Customers_FreeTrial_2026Q1`).

### Budget Allocation

- Testing phase (first 2-4 weeks): 70% proven, 30% testing new audiences/creative
- Scaling: consolidate into winners; **increase budgets ~20% at a time — never 30%+ in one move** (resets platform learning); wait 3-5 days between increases

---

## Audience Knowledge: Creative First, Targeting Second

Knowing your audience deeply is still the highest-leverage work — demographics, pains, fears, exact language, what they've tried, why it failed. What changed: as platform algorithms improved, jamming audience identifiers into *targeting filters* underperforms feeding them into the *creative* (headlines, copy, hooks, examples).

### Where to apply audience knowledge, by platform

| Platform | Into creative | Into targeting filters | Notes |
|----------|:---:|:---:|-------|
| Meta (post-Andromeda) | 80%+ | 20% | Broad + specific creative wins; interest-stacking now actively hurts |
| Google Search | 40% | 60% | Keywords still dominate — match types, negatives drive performance |
| Google PMax / Demand Gen | 70% | 30% | Audience signals advisory; creative + feed quality dominate |
| LinkedIn | 40% | 60% | Firmographic filters still precise; creative makes the click |
| TikTok | 70% | 30% | Broad + native-feeling creative |
| Twitter/X | 50% | 50% | Interest/follower targeting still meaningful |

Mapping audience data to creative: demographics → identity-trigger keywords in headlines; pains/fears → headline + first line; hopes → transformation copy + CTAs; objections → objection-handling retargeting ads; their vocabulary → the entire copy voice; customer base → lookalikes (base on best customers by LTV, not all customers).

**Common failure mode:** compensating for weak creative with hyper-precise targeting — a small audience that all see a bad ad. Better: 5 creative variants each speaking to a different segment, broad targeting, let the algorithm match.

---

## Modern Meta Playbook (Andromeda era)

Meta's Andromeda algorithm (2025) changed the game. The old playbook (interest stacking, polished video, single-winner scaling) underperforms.

### Creative volume is the constraint (statics > polished video)
- The algorithm needs constant fresh creative or it fatigues
- Statics often outperform video: Meta can deliver more statics per session (cheaper delivery), and they're ~10x cheaper/faster to produce, enabling the needed volume
- Dedicate ~1 hour/week to producing fresh creatives for the winning offer. Volume > polish.

### Creative IS the targeting
- Target broadly (country only) and let the creative do the targeting
- Long-form ad copy works better than short in this era — a wider context window for the algorithm to understand who to show it to
- Test it: duplicate your best interest-stacked ad, strip all targeting to just country, run side-by-side 7 days, compare CPAs. Broad typically wins.

### The one-keyword hack (identity triggers)
Duplicate a winning ad with a niche keyword inserted: "get 462 leads per week" → "get 462 **dental** leads per week" / "...**lawyer** leads...". The keyword is an identity trigger for the viewer AND a targeting signal for the algorithm. Drops CPL and opens audience pockets a generic ad can't reach.

### AI variant farming
Feed a winning ad to an LLM: "Read this ad and be the author. If I show your next ad to 100 people, not 1 in 100 should tell it's a different writer. Now write it for [demographic/niche]." Apply in sequence: body copy → headlines → creative. Drop all variants in one CBO and let Meta allocate.

### Zombie campaigns
After a CBO run, Meta gives ~80% of variants no spend. Take the dead variants you have high conviction about and relaunch them in a separate ad set — typically ~20% resurrect as winners the first allocation passed over.

### Don't make ads look like ads
Study what content natively performs in your niche (a clean burner account following all niche influencers turns your feed into competitive research) and match that aesthetic. If you have an organic video with millions of views, run that exact video as a paid ad.

---

## Creative Best Practices

**Image ads:** product screenshots showing real UI, before/after comparisons, stats as the focal point, real human faces, text overlay under 20% of image.

**Video structure (15-30s):** hook 0-3s (pattern interrupt) → problem 3-8s → solution 8-20s → CTA 20-30s. Captions always (85% watch muted); vertical for Stories/Reels; native feel beats polish; the first 3 seconds decide everything.

**Creative testing hierarchy (biggest impact first):** 1) concept/angle, 2) hook/headline, 3) visual style, 4) body copy, 5) CTA.

---

## Optimization

| Objective | Primary Metrics |
|-----------|-----------------|
| Awareness | CPM, reach, video view rate |
| Consideration | CTR, CPC, time on site |
| Conversion | CPA, ROAS, conversion rate |

**If CPA is too high:** check the landing page first (is the problem post-click?), then targeting, then new creative angles, then bid strategy.
**If CTR is low:** creative isn't resonating (new hooks), audience mismatch, or fatigue (refresh).
**If CPM is high:** audience too narrow, high competition, or low relevance score.

**Bid strategy progression:** manual or cost caps → gather 50+ conversions → switch to automated with targets from historical data → monitor and adjust.

---

## Retargeting

### Funnel-based segments and windows

| Stage | Audience | Window | Frequency Cap |
|-------|----------|--------|---------------|
| Hot | Cart/trial abandoners | 1-7 days | Higher OK |
| Warm | Pricing/feature page visitors | 7-30 days | 3-5x/week |
| Cold | Any visit | 30-90 days | 1-2x/week |

**Exclusions:** existing customers (unless upsell), recent converters (7-14 days), sub-10-second bouncers, irrelevant pages (careers, support).

### Retarget with DIFFERENT offers

The #1 reason someone didn't buy is that the offer wasn't right for them — re-showing the same thing harder doesn't help. Retarget with different products/offers from your catalog: viewed protein powder, didn't buy → retarget with creatine; downloaded a lead magnet, didn't book → different lead magnet; viewed pricing, didn't sign up → free audit instead. A 2-3 ROAS audience on the original offer can hit 6+ on a different offer.

### The 4-component retargeting framework

Run these four simultaneously against non-converters:
1. **Objection-handling ad** — addresses the top reasons people didn't buy. Find them by calling leads who didn't convert; their verbatim objections become the headline.
2. **Proof testimonial carousel** — testimonials backing the original ad's claims.
3. **Other-offers CBO** — your best ads for other products in one CBO.
4. **Value-first audit/assessment ad** — wraps the call in free value; lowers friction.

---

## Landing Page Alignment: Headline Mirroring

Ad-to-landing-page congruence is the most underrated lever. Meta is effectively a giant headline split-testing tool — headlines get ~1000x the exposure of your landing page.

1. Run 20-40 headline variations as ads
2. Identify the winner by CTR + downstream conversion
3. Mirror that exact headline on the landing page — H1, sub-headline, lead-in
4. Expect a 15-20% minimum lift in landing-page conversion

It works because the clicker expects that specific promise; when the page restates it verbatim, scent matches.

**Standing discipline:** at least 3 split tests running at all times somewhere in the funnel (creative, landing page, offer, post-conversion). 3 tests x 10-20% lifts compounding = a fundamentally better funnel within a quarter.

---

## Scaling Discipline (net cash > ROAS percentage)

Common failure: a business at 40 ROAS on $5k/month refuses to scale because "ROAS will drop." Wrong frame:
- ROAS dropping 10 → 5 while spend goes $10k → $100k nets dramatically more profit
- Optimize **blended ROAS at the business level** (better: net free cash flow), not per-ad-set ROAS
- Compute your break-even CPA ceiling from LTV, then scale until you approach that ceiling — not until ad-account ROAS drops below an arbitrary preference

**The 3-hour founder review:** block 3 hours/month to personally go through the numbers. Data gives you confidence; confidence gives you speed.

**Call your unconverted leads:** everyone who entered the funnel but didn't buy gets a call — the verbatim blockers become objection-handling ads.

---

## Reporting

- Weekly: spend pacing, CPA/ROAS vs targets, top/bottom ads, frequency (fatigue), landing-page conversion
- Platform attribution is inflated — use consistent UTMs, compare to GA4, watch blended CAC not just platform CPA

## Pre-Launch Checklist

- [ ] Conversion tracking tested with a real conversion
- [ ] Landing page loads <3s and is mobile-friendly
- [ ] UTMs working
- [ ] Targeting matches intent; existing customers excluded

## Common Mistakes

- Launching without conversion tracking; too many campaigns fragmenting budget; not letting algorithms finish learning
- Only one ad per ad set; not refreshing fatigued creative; ad/landing-page mismatch
- Big budget jumps (30%+) that reset learning; stopping campaigns mid-learning-phase

## Related Skills

- Use the **ad-creative** skill for generating and iterating ad copy/creative at scale
- Use the **ab-testing** skill for landing-page tests that improve ROAS
- Use the **customer-research** skill for the voice-of-customer inputs behind creative angles
