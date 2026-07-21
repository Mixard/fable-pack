---
name: aso
description: Audit and optimize App Store and Google Play listings — platform indexation rules (what Apple vs Google indexes), character/byte limits, a weighted 6-dimension scoring rubric, brand-maturity-tiered evaluation, and conversion benchmarks (video lift, screenshot behavior). Use when the user shares an app store URL, asks why downloads are low, or wants keyword/listing optimization.
---

# ASO Audit

Analyze App Store and Google Play listings against ASO best practices: fetch live listing data, score metadata, visuals, and ratings, then produce a prioritized action plan.

## Before Auditing

If `.agents/product-marketing.md` exists (created by the product-marketing skill), read it first.

## Phase 1 — Identify Store & Fetch

URL patterns:
```
Apple:  apps.apple.com/{country}/app/{name}/id{digits}
Google: play.google.com/store/apps/details?id={package}
```

If given an app name instead, search `site:apps.apple.com "{app name}"` or `site:play.google.com "{app name}"`.

Fetch the listing and extract every available field:

**Apple:** app name (30-char limit), subtitle (30), description (not search-indexed — conversion only), promotional text (170 chars, updatable without release), categories, screenshots (count/order/captions), preview video, rating + count, recent reviews, price/IAP, last updated, version notes, localizations, in-app events.

**Google Play:** title (30), short description (80), full description (4,000 chars — IS indexed), category + tags, feature graphic, screenshots, video, rating + count, reviews, price/IAP, last updated, what's new, downloads range, data safety, languages.

Stores render client-side — if the fetch is incomplete, note gaps and ask the user to paste missing fields. Screenshots/captions can't be extracted from HTML: take a browser screenshot of the listing page, or ask the user for one.

## Phase 1.5 — Assess Brand Maturity

Classify the app before scoring — a deliberate brand choice by a household name is not the same as a missed opportunity by an unknown app.

| Tier | Signals | Examples |
|------|---------|----------|
| **Dominant** | Household name, 1M+ ratings, top-10 in category; users search by brand | Instagram, Uber, Spotify |
| **Established** | Category-known, 100K+ ratings, strong organic installs | Strava, Notion, Duolingo |
| **Challenger** | Building awareness, <100K ratings; needs keyword discovery. Most apps. | Most indie/startup apps |

**Dominant apps** get adjusted scoring: brand-only titles are valid (the brand IS the keyword); descriptions scored purely on conversion; lifestyle photography instead of UI demos is legitimate; generic release notes at weekly cadence are fine; missing in-app events isn't a penalty for utility apps; localization scored relative to actual market.

**Established:** brand-first titles fine but should include 1-2 keywords; other dimensions scored normally.

**Challenger:** scored strictly against textbook ASO — every character, screenshot, and keyword matters.

Principle: before docking points, ask "Is this a mistake, or a deliberate choice by a team with data I don't have?"

## Phase 2 — Score Each Dimension

Score 0-10 per dimension, apply tier adjustments, weight:

| # | Dimension | Weight | Covers |
|---|-----------|--------|--------|
| 1 | Title & Subtitle | 20% | Character usage, keyword presence, clarity, brand/keyword balance |
| 2 | Description | 15% | First 3 lines, keyword density (Google), CTA, structure, promo text |
| 3 | Visual Assets | 25% | Screenshot count/quality/messaging, video, icon, feature graphic |
| 4 | Ratings & Reviews | 20% | Average, volume, recency, developer responses |
| 5 | Metadata & Freshness | 10% | Category choice, update recency, localization, data safety |
| 6 | Conversion Signals | 10% | Price positioning, IAP transparency, social proof |

**Final score** = weighted sum out of 100.

| Score | Grade | Meaning |
|-------|-------|---------|
| 85-100 | A | Well-optimized; focus on A/B testing |
| 70-84 | B | Good foundation; clear opportunities |
| 50-69 | C | Significant gaps; prioritized fixes high-impact |
| 30-49 | D | Major optimization needed |
| 0-29 | F | Complete overhaul |

## Phase 3 — Competitor Comparison (optional)

Fetch 2-3 competitors in the category, run the same scoring, build a comparison table, and identify keyword gaps.

## Phase 4 — Generate Report

Must include: score card (6 dimensions + grade), top 3 quick wins (<1 hour, highest impact), per-dimension findings with specific fixes, keyword suggestions with rationale, visual asset recommendations, and a priority action plan ordered by impact vs effort.

Report rules: every recommendation specific ("Change subtitle from X to Y," with character counts), flag Apple-vs-Google differences, note what can't be assessed without paid tools (search volume, exact rankings).

---

## Platform-Specific Rules

### Apple App Store — Key Facts

- Indexed text = Title (30 chars) + Subtitle (30 chars) + hidden Keyword field (100 **bytes** — Arabic/CJK chars use 2-3 bytes each)
- Long description is NOT indexed — optimize it for conversion only
- Promotional text (170 chars) does NOT affect search (Apple confirmed)
- Never repeat words across title/subtitle/keyword field — Apple indexes each word once
- Keyword field format: commas, no spaces ("photo,editor,filter")
- Screenshots: up to 10 per device; first 3 visible in search — ~90% of users never scroll past the 3rd
- Screenshot captions are indexed (AI extraction, since June 2025)
- In-app events: max 10 published, max 31 days each; indexed and appear in search
- Custom Product Pages (up to 70) appear in organic search; average +5.9% conversion lift
- App preview video: up to 3, 15-30s, autoplays muted — +20-40% conversion lift
- SKStoreReviewController: max 3 rating prompts per 365 days
- Apple has human editorial curation — design quality matters more

### Google Play — Key Facts

- Indexed text = Title (30) + Short description (80) + Full description (4,000 — target 2-3% keyword density, naturally)
- No hidden keyword field — all keywords must be in visible text; NLP detects and penalizes stuffing
- Prohibited in title: emojis, ALL CAPS, "best"/"#1"/"free", CTAs (enforced since 2021)
- Screenshots: min 2, **max 8** per device (not 10 like Apple)
- Feature graphic (1024x500 exact) required for featured placements
- Video does NOT autoplay — only ~6% tap play (low ROI vs iOS)
- **Android Vitals directly affect ranking**: crash rate >1.09% or ANR >0.47% = reduced visibility
- Promotional Content: submit 14 days early for featuring; participating apps see ~2x explore acquisitions
- Custom Store Listings: up to 50 (target churned users, countries, ad campaigns)
- Store Listing Experiments: up to 3 variants, run 7+ days, 1 experiment at a time

### What Apple Indexes vs What Google Indexes

| Field | Apple | Google |
|-------|-------|--------|
| Title | Yes | Yes (strongest signal) |
| Subtitle / short desc | Yes | Yes |
| Keyword field | Yes (hidden) | Does not exist |
| Long description | No | Yes (heavily) |
| Screenshot captions | Yes (since 2025) | No |
| In-app events | Yes | N/A (LiveOps instead) |
| Developer name | No | Partial |
| IAP names | Yes | Yes |

---

## Common Issues Checklist

**Always flag (all tiers):**
- [ ] Rating below 4.0
- [ ] Last update > 3 months ago
- [ ] Google Play description with no keyword strategy (under ~1% density)
- [ ] Google Play missing feature graphic
- [ ] Apple keyword field likely repeating title/subtitle words
- [ ] Category mismatch — less competition available in another category
- [ ] Fewer than 5 screenshots

**Flag for Challenger/Established only** (may be deliberate for Dominant):
- [ ] Title wastes characters on brand-only (no keywords)
- [ ] Subtitle/short description duplicating title keywords
- [ ] Generic first 3 description lines
- [ ] No preview video
- [ ] Screenshots are UI dumps with no captions/messaging
- [ ] Only 1-2 localizations (score relative to actual market)
- [ ] No in-app events / promotional content

**Flag with context:** no developer responses to negative reviews (note review volume); generic "What's New" (acceptable at weekly+ cadence for big apps).

## Questions to Ask

1. App Store or Google Play URL?
2. Your app or a competitor's?
3. Competitor URLs to compare against?
4. Focus: search visibility, conversion, or both?
5. Access to App Store Connect / Play Console data?

## Related Skills

- Use the **ad-creative** skill for app-install ad creatives
- Use the **customer-research** skill to mine reviews for listing copy language
