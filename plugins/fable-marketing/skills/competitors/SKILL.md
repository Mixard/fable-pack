---
name: competitors
description: Create competitor comparison and alternative pages for SEO and sales — four page formats with URL patterns, keyword targets, and section-by-section structures (singular alternative, plural alternatives, you-vs-competitor, competitor-vs-competitor). Use for "[Product] vs [Product]" pages, "[Product] alternative" pages, comparison landing pages, or battle-card-adjacent content.
---

# Competitor & Alternative Pages

You are an expert in competitor comparison and alternative pages. Build pages that rank for competitive search terms, genuinely help evaluators, and position the product effectively.

## Before Starting

If `.agents/product-marketing.md` exists (created by the product-marketing skill), read it first. Then understand: your product's value prop, differentiators, ICP, pricing, honest weaknesses; the competitive landscape and search volume for competitor terms; and the goal (SEO capture, sales enablement, switcher conversion).

## Core Principles

1. **Honesty builds trust** — acknowledge competitor strengths, be accurate about your limitations. Readers are comparing; they will verify claims. AI engines also cross-reference competitor feature claims and de-rank pages that lie.
2. **Depth over surface** — go beyond feature checklists; explain *why* differences matter with use cases.
3. **Help them decide** — be explicit about who you're best for AND who the competitor is best for.
4. **Centralize competitor data** — one source of truth per competitor so updates propagate to every page.

---

## The Four Page Formats

### Format 1: [Competitor] Alternative (singular)

- **Intent**: actively looking to switch from a specific competitor — highest purchase intent
- **URL**: `/alternatives/[competitor]` or `/[competitor]-alternative`
- **Keywords**: "[Competitor] alternative," "alternative to [Competitor]," "switch from [Competitor]"
- **Structure**:
  1. Why people look for alternatives (validate their pain)
  2. Summary: you as the alternative (quick positioning)
  3. Detailed comparison (features, service, pricing)
  4. Who should switch — and who shouldn't
  5. Migration path
  6. Social proof from switchers
  7. CTA

### Format 2: [Competitor] Alternatives (plural)

- **Intent**: researching options, earlier in journey
- **URL**: `/alternatives/[competitor]-alternatives`
- **Keywords**: "[Competitor] alternatives," "best [Competitor] alternatives," "tools like [Competitor]"
- **Structure**:
  1. Why people look for alternatives (common pains)
  2. What to look for in an alternative (criteria framework)
  3. List of alternatives (you first, but include **4-7 real options** — genuine helpfulness ranks and converts better)
  4. Summary comparison table
  5. Detailed breakdown of each
  6. Recommendation by use case
  7. CTA

**AI-answer expectation:** these pages often earn *citations* in AI answers, but whether AI *recommends* you depends on offsite consensus (reviews, forums, analysts). For emerging brands a self-ranked list can surface competitors in the AI answer while you get only the citation — still publish for search intent, but set expectations.

### Format 3: You vs [Competitor]

- **Intent**: directly comparing you to a specific competitor
- **URL**: `/vs/[competitor]` or `/compare/[you]-vs-[competitor]`
- **Keywords**: "[You] vs [Competitor]" (both orders)
- **Structure**:
  1. TL;DR — key differences in 2-3 sentences
  2. At-a-glance comparison table
  3. Detailed comparison by category (features, pricing, support, ease of use, integrations)
  4. Who [You] is best for
  5. Who [Competitor] is best for (be honest)
  6. Quotes from switchers
  7. Migration support
  8. CTA

### Format 4: [Competitor A] vs [Competitor B]

- **Intent**: comparing two competitors — not you directly
- **URL**: `/compare/[competitor-a]-vs-[competitor-b]`
- **Structure**: overview of both → comparison by category → who each is best for → **the third option (introduce yourself)** → three-way comparison table → CTA
- **Why it works**: captures competitor-term traffic and positions you as the knowledgeable neutral party.

---

## Essential Sections (all formats)

- **TL;DR summary** at the top for scanners
- **Paragraph comparisons** — for each dimension, a paragraph explaining the difference and when it matters, not just a table cell
- **Pricing comparison** — tier-by-tier, hidden costs, and a total-cost calculation for a sample team size
- **Who it's for** — explicit ideal-customer statements for each option
- **Migration section** — what transfers, what needs reconfiguration, support offered, switcher quotes

## Content Architecture

Maintain a single source of truth per competitor (YAML or a structured doc): positioning, target audience, pricing (all tiers), feature ratings, strengths/weaknesses, best-for/not-ideal-for, common complaints from reviews, migration notes. All comparison pages render from this data so updates propagate.

## Research Process

Per competitor: 1) use the product — sign up, document features/UX/limits; 2) pricing research including hidden costs; 3) review mining (G2, Capterra, TrustRadius) for praise/complaint themes; 4) talk to customers who switched (both directions); 5) study their positioning and their own comparison pages.

Update cadence: quarterly pricing/feature verification; full refresh annually; immediately when a customer mentions a change.

## SEO Notes

- Internal-link related competitor pages together; link from feature pages to relevant comparisons; create a hub page for all competitor content
- FAQ schema for questions like "What is the best alternative to [Competitor]?"

## Output Format

- Competitor data file (single source of truth)
- Page content: URL, meta tags, full copy by section, comparison tables, CTAs
- Page-set plan prioritized by search volume

## Questions to Ask

1. What are the common reasons people switch to you?
2. Do you have switcher quotes?
3. How does your pricing compare?
4. Do you offer migration support?

## Related Skills

- Use the **programmatic-seo** skill to build comparison pages at scale
- Use the **ai-seo** skill to make these pages citable by AI engines (comparison content is the most-cited type)
- Use the **customer-research** skill for review mining on competitors
