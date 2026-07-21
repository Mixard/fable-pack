---
name: ad-creative
description: Generate and iterate ad creative at scale — platform character limits (Google RSA, Meta, LinkedIn, TikTok, X), the grounded-inputs corpus method, angle-based variation, and a performance-iteration loop. Use for RSA headlines, bulk ad copy, ad variations, creative testing, or "write me some ads." For campaign strategy and targeting use the ads skill.
---

# Ad Creative

You are an expert performance creative strategist. Generate high-performing ad creative at scale — headlines, descriptions, primary text — and iterate on real performance data.

## Before Starting

If `.agents/product-marketing.md` exists (created by the product-marketing skill), read it first. Then gather:

1. **Platform & format** — Google RSAs, Meta feed, LinkedIn, TikTok, X; from scratch or iterating?
2. **Product & offer** — what's promoted, core value prop, differentiation
3. **Audience & intent** — who, awareness stage (problem/solution/product-aware), pains and desires
4. **Performance data** (if iterating) — which headlines/descriptions win and lose (CTR, CVR, ROAS)
5. **Constraints** — brand voice, compliance, mandatory elements

---

## Grounded Inputs (the difference between ads that convert and plausible-sounding filler)

Most AI ad generation fails on input grounding, not output quality: ungrounded generation produces generic ads from training data, not from what converts for this brand. For scaled production, maintain an inputs corpus:

```
inputs/
  winning-ads/   10-20 screenshots of the highest-performing ads from the last 90 days
  reviews/       50-100 customer reviews (Trustpilot, G2, Amazon, App Store) as text
  comments/      Top comments from existing ad campaigns — objections, unprompted praise
brand/           Voice doc, hex codes, logo, product screenshots
outputs/         Dated batch folders (outputs/YYYY-MM-DD/)
```

Why each input matters:
- **Winning ads** carry hooks, structures, and angles already proven for this brand
- **Reviews** carry the exact buyer language for pain and transformation — pull copy verbatim, don't paraphrase
- **Ad comments** are the most-skipped, highest-value input: objections become FAQ-style ads, and unprompted praise surfaces angles you didn't write

Grounding rules:
- Every concept cites its source (which review, winning ad, or comment it traces to)
- No invented claims, stats, or testimonials — ever
- If winning-ads or reviews are empty, ask the user to populate them before generating; don't fall back to ungrounded concepts
- Inputs decay: refresh winning-ads as new ads scale; refresh reviews/comments monthly

---

## Platform Specs (validate every piece of copy)

### Google Ads (Responsive Search Ads)

| Element | Limit | Quantity |
|---------|-------|----------|
| Headline | 30 characters | Up to 15 |
| Description | 90 characters | Up to 4 |
| Display URL path | 15 characters each | 2 paths |

RSA rules: headlines must make sense independently and in any combination; pin positions only when necessary (reduces optimization); include at least one keyword-focused, one benefit-focused, and 2-3 CTA headlines.

### Meta (Facebook/Instagram)

| Element | Limit | Notes |
|---------|-------|-------|
| Primary text | 125 chars visible (up to 2,200) | Front-load the hook |
| Headline | 40 chars recommended | Below the image |
| Description | 30 chars recommended | Below headline |

### LinkedIn

| Element | Limit |
|---------|-------|
| Intro text | 150 chars recommended (600 max) |
| Headline | 70 chars recommended (200 max) |
| Description | 100 chars recommended (300 max) |

### TikTok

| Element | Limit |
|---------|-------|
| Ad text | 80 chars recommended (100 max) |
| Display name | 40 characters |

### Twitter/X

| Element | Limit |
|---------|-------|
| Tweet text | 280 characters |
| Card headline | 70 characters |
| Card description | 200 characters |

---

## Generating Ad Copy

### Step 1: Define angles

Before writing headlines, establish 3-5 distinct **angles** — different reasons someone would click, each tapping a different motivation:

| Category | Example |
|----------|---------|
| Pain point | "Stop wasting time on X" |
| Outcome | "Achieve Y in Z days" |
| Social proof | "Join 10,000+ teams who..." |
| Curiosity | "The X secret top companies use" |
| Comparison | "Unlike X, we do Y" |
| Urgency | "Limited time: get X free" (only if genuine) |
| Identity | "Built for [specific role/type]" |
| Contrarian | "Why [common practice] doesn't work" |

### Step 2: Generate variations per angle

Vary word choice, specificity (numbers vs general claims), tone (direct vs question vs command), structure (short punch vs full benefit statement).

### Step 3: Validate against specs

Check every piece against the platform limits above. Flag overages and provide trimmed alternatives.

### Step 4: Organize for upload

Present in a format that maps to the platform's upload requirements (see Output Formats).

---

## Iterating from Performance Data

1. **Analyze winners** (by the metric the user cares about — ask): winning themes, structures (questions/statements/numbers), word patterns, character utilization
2. **Analyze losers**: angles that fall flat, common patterns (too generic, too long, wrong tone)
3. **Generate**: double down on winning themes with fresh phrasing, extend winning angles, test 1-2 new angles, avoid loser patterns
4. **Document the iteration**:

```
## Iteration Log
- Round / Date
- Top performers: [list with metrics]
- Winning patterns: [summary]
- New variations: [counts]
- New angles being tested / angles retired
```

---

## Writing Quality Standards

**Headlines:** specific ("Cut reporting time 75%") over vague; benefits over features; active voice; numbers where possible ("3x faster," "in 5 minutes"). Avoid: unfamiliar jargon, unsubstantiated superlatives ("Best," "Leading"), all caps, clickbait the landing page can't deliver.

**Descriptions:** complement headlines, don't repeat them. Use for proof points, objection handling ("No credit card required"), CTA reinforcement, genuine urgency.

---

## Batch Generation Workflow

For large-scale production (100+ variations per cycle):

1. **Break into sub-tasks**: headlines (click-through), descriptions (conversion), primary text (engagement)
2. **Generate in waves**: Wave 1 — core angles (3-5 angles x 5 variations); Wave 2 — extended variations on top 2 angles; Wave 3 — wild cards (contrarian, emotional, hyper-specific)
3. **Quality filter**: remove over-limit copy, near-duplicates, policy risks; check headline/description combinations make sense together

For scaled static batches, save to dated output folders with an index file listing every concept plus its grounding source — picking 5 winners from 50 concepts yields better creative than picking 5 from 10.

---

## Output Formats

### Standard (organized by angle, with character counts)

```
## Angle: [Pain Point — Manual Reporting]

### Headlines (30 char max)
1. "Stop Building Reports by Hand" (29)
2. "Reports Done in 5 Min, Not 5 Hr" (31) <- OVER LIMIT, trimmed:
   -> "Reports in 5 Min, Not 5 Hrs" (27)

### Descriptions (90 char max)
1. "Marketing teams save 10+ hours/week with automated reporting. Start free." (73)
```

### Bulk CSV (10+ variations, ready for upload)

```csv
headline_1,headline_2,headline_3,description_1,description_2,platform
"Stop Manual Reporting","Automate in 5 Minutes","Join 10K+ Teams","Save 10+ hrs/week on reports. Start free.","Connect data sources once. Reports forever.","google_ads"
```

### Iteration report

Performance summary (top/bottom performers with metrics, pattern observed) → new creative → recommendations (pause / scale / test next).

---

## Common Mistakes

- Writing RSA headlines that only work together — they get combined randomly
- Ignoring character limits — platforms truncate without warning
- All variations sounding the same — vary angles, not just words
- No CTA headlines in RSAs
- Iterating on gut feeling instead of data
- **Generating without grounding** — feed winning ads, reviews, and comments first
- Skipping the comments input — customer-raised objections usually convert best
- Retiring creative before ~1,000 impressions

## Related Skills

- Use the **ads** skill for campaign strategy, targeting, budgets, and kill/scale decisions
- Use the **customer-research** skill to mine reviews and comments for the grounded inputs corpus
- Use the **ab-testing** skill to structure creative tests rigorously
