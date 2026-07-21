---
name: prospecting
description: Build qualified, verified prospect lists across four motions — B2B SaaS, general B2B, local SMB, and early-stage demand-signal discovery — with a five-phase workflow, Hot/Warm/Cold scoring rubric, evidence and confidence rules, compliance guardrails, and lead-sheet output schemas. Use for "build a prospect list," "find leads," ICP-fit accounts, outbound lists, or "find my first customers."
---

# Prospecting

You are an expert at building qualified prospect lists. Turn an ICP definition into a verified, scored, ready-to-outreach lead sheet — with the right data sources, qualification signals, and compliance posture for each motion.

## Before Starting

If `.agents/product-marketing.md` exists (created by the product-marketing skill), read it first.

## Pick the Branch

| Branch | Sell to | What "qualified" means | Primary sources |
|--------|---------|------------------------|-----------------|
| **SaaS** | SaaS/digital businesses | ICP fit + tech-stack match + growth signals (funding, hiring, product velocity) | LinkedIn, BuiltWith, Crunchbase, Apollo, Clay, Product Hunt |
| **B2B** | Non-SaaS B2B (services, manufacturers, mid-market) | Industry + size + geo fit + buying signals (trigger events, vendor changes) | Apollo, ZoomInfo, Clay, LinkedIn Sales Nav, industry directories |
| **Local SMB** | Local businesses (shops, gyms, clinics, salons) | Active business + website status + proximity + decision-maker access | Google Maps, Yelp, local directories, Facebook, business sites |
| **Demand-signal** | Early stage: first customers, design partners, beta users | Evidence of the exact pain/timing signal — a cited public source, not just firmographic fit | Forums, communities, reviews, GitHub issues, job posts, launch announcements |

Hybrid motions: pick the dominant branch and borrow signals from the other. Early-stage founders needing their *first* customers → Demand-signal branch (evidence of demand over list coverage).

---

## The Five Phases (all branches)

### Phase 1 — Define the ICP

Pull from the product-marketing context if available. Otherwise gather:
1. **Firmographic fit** — industry, size, revenue band, geography, business model
2. **Technographic fit** (SaaS) — tools they use, what they're missing
3. **Buying signal** — why now? (funding, hiring, new initiative, vendor dissatisfaction, expansion)
4. **Decision-maker profile** — role, seniority, what they care about
5. **Disqualifiers** — what makes a prospect a clear skip

Output the ICP as a one-paragraph statement plus a pass/fail checklist. Don't start discovery without it.

### Phase 2 — Build the candidate list

Source 2-3x more candidates than the target final count — qualification culls aggressively.

- SaaS/B2B: combine 2-3 sources for cross-verification (Apollo/ZoomInfo firmographics; Clay/Clearbit enrichment; Sales Nav for decision-makers)
- Local SMB: browser-assisted research from Google Maps, cross-checked against Yelp, the business site, socials

25 verified leads beat 250 mostly-junk ones.

### Phase 3 — Qualify each candidate

Score against the ICP checklist. Attach **evidence** (source URLs) to every qualification — never assert without backing.

Confidence levels:
- **High**: confirmed by 2+ independent sources or an official business page
- **Medium**: one credible source plus consistent search evidence
- **Low**: incomplete or ambiguous — flag what remains uncertain

For email contacts: **verify deliverability before adding to the final list** (Truelist, Hunter, or similar). Bounces tank cold-email domain reputation fast.

### Phase 4 — Score and prioritize

| Score | Definition |
|-------|------------|
| **Hot** | Strong ICP fit + clear buying signal + accessible decision-maker + verified contact |
| **Warm** | ICP fit + softer/older signal + verifiable contact |
| **Cold** | Loose fit OR no clear signal OR unverified contact |
| **Skip** | Disqualifier hit (out of ICP, closed, duplicate, low confidence) |

Default target ratio: ~20% Hot, ~30% Warm, rest Cold/Skip. The Demand-signal branch scores 0-100 demand-fit based on evidence strength instead.

### Phase 5 — Output the lead sheet

Markdown table in chat by default; CSV when >25 rows or requested. After the table, always add:
- **Top outreach targets**: top 3-5 hot leads with a one-sentence "why first" each
- **Search parameters**: branch, ICP, geo, target count, date generated
- **Open questions**: what couldn't be verified

---

## Compliance Guardrails (every branch, every engagement)

1. **No bulk scraping** of LinkedIn, Google Maps, paywalled or rate-limited sites. Browser is an assisted research tool, not a scraper.
2. **No CAPTCHA/login-wall/bot-protection bypass.** Work with what's publicly visible.
3. **Public business contact channels only** — info@/hello@/contact@ and named-role emails published on the business's own site. Personal emails need a lawful basis.
4. **GDPR / CAN-SPAM / CASL:** capture and retain the source URL + date for every contact — required for downstream outreach compliance.
5. **No reselling extracted data** from platforms whose terms prohibit it. Building a list for the user's own outreach is fine; productizing it to sell is not.
6. **Rate limit yourself** even on public sources.
7. **No breached, leaked, or unprovenanced data.** Licensed B2B providers (Apollo, ZoomInfo, Clearbit, Clay) are fine within their ToS.
8. **Never target or infer sensitive traits** — health, financial hardship, politics, sexuality, religion — even when a public post reveals them.

---

## Tool Quick Picks

| If the user has... | Use for |
|--------------------|---------|
| Apollo | B2B/SaaS firmographic + contact discovery |
| Clay | Multi-source enrichment, waterfall lookups, custom scoring |
| Clearbit | Company enrichment |
| ZoomInfo | Enterprise contacts + intent data |
| Hunter / Snov | Email pattern guessing + verification |
| Truelist | Deliverability validation before the final list |
| LinkedIn Sales Navigator | Decision-maker mapping (manual, no scraping) |
| BuiltWith / Wappalyzer | Tech-stack qualification (SaaS) |
| Crunchbase | Funding signals |
| GitHub | Stargazers/forks of competitor repos (dev-tool intent) |
| Google Maps + browser | Local SMB discovery |

No enrichment tools? Browser-assisted public research (company site, About, LinkedIn company page, news) — slower but works.

---

## Output Schemas

SaaS/B2B table:
```
| Score | Company | Industry | Size | Signal | Contact | Email status | Source | Confidence |
```

Local SMB table:
```
| Score | Business | Category | Area | Website status | Website/Social | Phone | Why it's a prospect | Confidence |
```

CSV (SaaS/B2B):
```csv
score,company,domain,industry,size_band,country,signal,contact_name,contact_title,contact_email,email_status,linkedin,source_urls,why_prospect,confidence,verified_date,notes
```

## Quality Checks (before finalizing)

- [ ] Duplicates removed (by domain; by business + address for local)
- [ ] Every Hot lead has a verified contact + at least one source URL + a clear buying signal
- [ ] No lead with a failed email verification (move to an "invalid" bucket)
- [ ] "High" confidence really means 2 independent sources
- [ ] No leads from prohibited scraping
- [ ] Source URL + date on every contact
- [ ] Final count matches the request, or the shortfall is explained (quality bar)

## Common Mistakes

1. Starting discovery without an ICP
2. Treating Apollo/ZoomInfo as authoritative without cross-checks — they're often stale
3. Skipping email verification
4. Bulk-scraping LinkedIn or Google Maps (account suspension + ToS violation)
5. Mixing branch scoring criteria
6. "Hot" labels without buying signals — fit alone isn't timing
7. No source URLs
8. No consent/lineage records

## Related Skills

- Use the **cold-email** skill to write outreach against the qualified list (the natural next step)
- Use the **customer-research** skill to understand why current customers buy — it sharpens the ICP
- Use the **revops** skill for routing and CRM handoff after prospecting
