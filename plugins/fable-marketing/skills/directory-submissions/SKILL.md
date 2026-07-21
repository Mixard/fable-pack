---
name: directory-submissions
description: Plan the directory layer of a product launch — a tiered catalog of startup/SaaS/AI/MCP directories, the Product Hunt 3-week prep timeline and launch-day rules, the G2 10-reviews-in-30-days protocol, destination-page strategy (alternative/use-case/template pages), and 30/90-day KPI targets. Use for "submit to directories," backlink campaigns, Product Hunt launches, or G2/Capterra listings.
---

# Directory Submissions

You are an expert in directory-driven distribution for software products. Build a compounding backlink + discovery foundation by submitting to the right directories, in the right order, with the right positioning — and make it produce leads, not vanity backlinks.

## Before Starting

If `.agents/product-marketing.md` exists (created by the product-marketing skill), read it first.

## Core Philosophy

Directories are the **foundation layer** of distribution — never the whole strategy. They do three things well:

1. **Pass dofollow backlinks** from high-DR sites, raising your DR so the whole site ranks easier
2. **Create discovery surface area** — directory browsers are in-market buyers
3. **Get you cited by AI engines** — ChatGPT, Claude, Perplexity, and AI Overviews pull heavily from high-DR directories for "best [category]?" queries. AI-referred traffic converts 6-27x higher than traditional search traffic.

Directories alone won't generate meaningful leads. They pass link equity into the pages that DO — template galleries, comparison pages, alternative pages. **Build the destination pages first.**

---

## The Three Hard Rules

### Rule 1: Foundation before submission
Never submit until the landing page a directory will link to is live, indexed, and has:
- Single `<h1>` and sequential heading hierarchy — clean-hierarchy pages show ~2.8x higher AI citation rates; 87% of ChatGPT-cited pages use a single H1
- A real pricing page (even "free while in beta" — most Tier 1 directories require one)
- Privacy policy + terms
- Logo assets: PNG + SVG + square 1024x1024 + favicon
- 5-8 real product screenshots at 1920x1080 (not mockups)
- A 60-90 second demo video — Product Hunt posts with video get ~2.7x more upvotes
- FAQ schema (`FAQPage` JSON-LD is heavily weighted for answer extraction)
- `Organization`, `Product`, `SoftwareApplication` structured data

### Rule 2: Destination pages before directories
Minimum destinations before submitting anywhere:
- 3-5 competitor alternative pages (`/alternatives/[competitor]`) — comparison/alternative pages convert at 5-15% vs 0.5-2% for generic content
- 3-5 use-case pages (`/for/[audience]` or `/use-cases/[use-case]`)
- Template gallery with 20+ entries if applicable — this pattern was Typeform's largest SEO growth driver (~30K non-branded signups, ~$3M/year LTV)
- 1 honest "best of [your category]" post you wrote yourself, covering competitors

### Rule 3: Positioning varies by directory type
Never copy-paste the same description everywhere — AI engines cross-reference and down-weight duplicates, and each audience responds to different framing:

| Surface | Lead with |
|---------|-----------|
| Startup directories | Outcome (audience is founders) |
| SaaS directories | Alternative framing ("[competitor] alternative") |
| AI directories | AI-first architecture |
| Agent/MCP registries | The agent/MCP angle |
| No-code directories | Ease + power |
| Dev directories | Technical depth |
| B2B review sites | ROI + use case |

---

## Workflow

### Step 1: Readiness assessment

Nine questions; a "no" on 1-7 is a hard block:
1. Product publicly accessible (no password wall)?
2. Pricing page live?
3. Privacy + terms live?
4. Logo assets (PNG/SVG/square/favicon)?
5. 5-8 screenshots + 60-90s demo video?
6. Landing pages GEO-ready (single H1, FAQ schema, structured data)?
7. 3+ alternative pages and 3+ use-case pages live and indexed?
8. Template gallery or lead-magnet asset (soft block)?
9. 20+ beta users who could review on G2 (soft block)?

### Step 2: Choose the tiers

| Tier | When | Examples | Count |
|------|------|----------|-------|
| 1 — Flagship launch | Launch week only | Product Hunt (anchor), BetaList, HN Show HN, Fazier, DevHunt | ~15 |
| 2 — Startup/SaaS | Week 1 + rolling | AlternativeTo, SaaSHub, G2, Capterra, F6S, SourceForge | ~50 |
| 3 — AI directories | Weeks 1-3 | TAAFT, Futurepedia, Toolify, Future Tools | ~40 |
| 4 — Agent/MCP registries | Weeks 1-3 (if MCP) | Glama, APITracker, LF MCP Registry | ~10 |
| 5 — No-code | Weeks 1-3 (if fits) | NoCodeFinder, No Code MBA, MakerPad | ~8 |
| 6 — "Best of" listicles | Rolling outreach | Cold outreach to DR 40+ posts | ~10 inclusions |
| 7 — Integration marketplaces | When integrations ship | Zapier, HubSpot, Slack, Notion | ~5 |
| 8 — Profile/content platforms | Rolling | GitHub, Substack, Dev.to, SlideShare | ~50 |
| 9-13 — Local, forums, PR sites, bookmarking, niche verticals | Rolling, where genuine fit | Varies | ~80 |

**Triage rule:** only submit where the product genuinely fits — forced listings get rejected and burn the first-submission advantage.

### Step 3: Prepare asset variations

Per tier: tagline under 10 words, short description at ~60 chars, long description ~150 words, 5-8 category tags, logo, screenshots + video URL, 2-3 sentence founder story. Vary the opening sentence, feature emphasis, and audience framing per tier.

### Step 4: Batch submit

Track in a spreadsheet (columns: directory, tier, date, listing URL, status, moderator notes). 2-3 hours per batch is realistic. Once live, verify the backlink exists and is dofollow: `curl -sIL <listing-url> | grep -i 'rel='` — if no `rel=nofollow`, it's dofollow.

---

## Product Hunt Deep Dive (the anchor event)

The current PH algorithm weighs **comment quality** over upvote count — 50 upvotes + 30 genuine comments ranks above 200 upvotes + 5 comments. ~80% of failed launches fail because they launched without a warm audience or asked for upvotes instead of feedback.

### 3-week prep timeline

- **Day -21 to -14:** warm up your account — upvote and thoughtfully comment on 3 launches/day, follow 100+ active makers
- **Day -14:** create an "Upcoming" page; drive traffic to collect notify-on-launch subscribers
- **Day -10 (optional):** line up a hunter — trade a feature or intro, don't pay cash; a known hunter adds ~15% day-one momentum but isn't required
- **Day -7:** draft launch assets — gallery images (1270x760), tagline, 260-char description, your first comment, a customer's first comment
- **Day -3:** warm the email list ("We're launching Tuesday...")
- **Day -1:** final checks — product works in incognito, video autoplays, CTA goes to signup

### Launch day

- **Launch at 12:01 AM Pacific, Tuesday-Thursday only** — weekend launches get 60-70% less traffic; 12:01 AM maximizes the 24-hour window
- **First 2 hours are everything** — you need 50+ supporters in the first 2 hours to trigger algorithmic distribution
- Post the first comment yourself: why you built it, what's different, what to try first
- Reply to every comment within 30 minutes — PH measures maker responsiveness
- Share to: X thread, LinkedIn post, communities, email list, power users via DM
- **Never ask for upvotes — ask for feedback.** "Would love your honest take on the positioning" converts ~3x better and avoids anti-manipulation filters
- Don't DM strangers — the community flags it and moderators hide the post

### Post-launch

Day 2: honest launch-recap post with numbers; cross-post to Indie Hackers and r/SaaS. Only submit to Show HN with a genuinely technical angle.

---

## Reviews Playbook (G2 / Capterra)

Listings without reviews are worthless. **10 reviews is the threshold for Grid appearance.**

### The 10-in-30 protocol

1. Day 1 post-launch: identify 20 users who completed a meaningful action
2. Send each a personal email with a **direct review URL** (cuts friction ~70%)
3. Offer a modest thank-you — G2 and TrustRadius explicitly allow small incentives (e.g., $25 gift card)
4. Follow up once after 5 days; never twice
5. Target 50% conversion → 10 reviews from 20 asks

### Deadlines and badges

- G2 quarterly report cutoffs (roughly late April for Summer, late July for Fall) — missing one means waiting 3 months for the next Grid update
- "Users Love Us" badge is free: 20 reviews at 4.0+ average
- Grid/Momentum/Award badges require a paid plan ($2,999+/year) — **don't pay for G2 in year one**; free listing + Users Love Us is sufficient

---

## Destination Pages Strategy

### 1. Alternative pages (highest ROI)
`/alternatives/[competitor]`, one per top competitor. Convert at 5-15%, up to 15-30% for bottom-of-funnel queries. Each needs: honest comparison table, "when to choose them / when to choose us," pricing comparison, use-case examples, FAQ with schema. **Be honest — AI engines cross-reference feature claims and de-rank lies.**

### 2. Use-case / ICP pages
`/for/[audience]`, `/use-cases/[use-case]` — one per ICP.

### 3. Template/asset gallery (if applicable)
One indexable page per template: keyword H1, 150+ word description, screenshot, "when to use this," CTA, related templates at the bottom. Realistic targets: 100 templates by day 30, 300 by day 90.

### 4. Self-authored "best of" listicles
`/blog/best-[category]-tools-[year]` including yourself + ~10 competitors with real assessments. Ranks for category queries and becomes a citable reference for AI engines.

### 5. Integration pages
`/integrations/[partner]` per integration — the Zapier pattern (~2.6M monthly organic visits from programmatic integration pages, ~15% of their organic traffic).

---

## GEO Tactics (getting the destination pages cited)

1. One H1, sequential hierarchy (2.8x citation rate)
2. Dense factual content with citable stats — specific numbers over vague claims
3. FAQ schema on every landing page
4. Comparison tables (extractable structure)
5. Explicit "what it is" paragraph in the first 100 words
6. Genuine Reddit and HN mentions (heavily indexed by Claude and Perplexity)
7. Original research ("We analyzed 10,000 X and found Y")
8. Claim Crunchbase, LinkedIn company page, and Wikidata — all feed AI corpora
9. MCP registries with quality grades (Glama) if applicable

Measure monthly: ask ChatGPT, Claude, and Perplexity "best [category] tools?" and log where you appear.

---

## KPIs

| Metric | Day 0 | Day 30 | Day 90 |
|--------|-------|--------|--------|
| Domain Rating | 0 | 20 | 30+ |
| Referring domains | 0 | 30 | 80+ |
| Indexed pages | — | 50 | 200+ |
| Organic clicks/day | 0 | 30 | 200+ |
| Directory listings live | 0 | 50 | 70+ |
| G2 reviews | 0 | 10 | 25 |
| AI citations (manual check) | 0 | 3 | 15+ |
| Signups from directory referrals | 0 | 50 | 300 |

---

## What NOT to Do

1. Don't pay for submission services ($60-$200 packages) — these are free; it's an afternoon of copy-paste
2. Don't submit to spam directories (DR under ~10, no traffic) — they dilute your profile and risk penalties
3. Don't use one description everywhere
4. Don't treat directories as your entire GTM
5. Don't list on G2/Capterra without running the reviews protocol
6. Don't ask for Product Hunt upvotes — ask for feedback
7. Don't submit before the destination page exists
8. Don't lie on comparison pages
9. Don't over-index on the launch-day spike — the flywheel is templates + alternatives + reviews + ongoing content
10. Don't forget Crunchbase, LinkedIn, and Wikidata

## Output Format

When asked for a directory plan, return: readiness assessment (missing blockers), tier selection with rationale, week 1/2/3 submission batches, destination-page build list, positioning variants per tier, the PH timeline mapped to calendar dates, the 10-in-30 reviews plan, and weekly targets.

## Related Skills

- Use the **programmatic-seo** skill for the destination pages backlinks flow into
- Use the **competitors** skill for the alternative-page pattern
- Use the **ai-seo** skill for deeper GEO/citation optimization
