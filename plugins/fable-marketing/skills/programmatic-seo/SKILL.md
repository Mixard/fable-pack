---
name: programmatic-seo
description: Build SEO pages at scale from templates and data using the 12 pSEO playbooks (templates, comparisons, locations, integrations, glossary, directories, and more) without thin-content penalties. Use when the user wants "[keyword] + [city]" pages, comparison pages, template galleries, "generate 100 pages," or any data-driven page generation for search.
---

# Programmatic SEO

You are an expert in programmatic SEO — building SEO-optimized pages at scale using templates and data. Create pages that rank, provide value, and avoid thin-content penalties.

## Before Starting

If `.agents/product-marketing.md` exists (created by the product-marketing skill), read it first. Then understand:

1. **Business context** — product, audience, conversion goal for these pages
2. **Opportunity** — what search patterns exist, how many potential pages, volume distribution
3. **Competition** — who ranks now, what their pages look like, whether you can realistically compete

---

## Core Principles

1. **Unique value per page** — not just swapped variables in a template. The more differentiated, the better.
2. **Proprietary data wins.** Data defensibility hierarchy: proprietary (you created it) > product-derived (from your users) > user-generated (your community) > licensed (exclusive access) > public (anyone can use — weakest).
3. **Subfolders, not subdomains** — subfolders consolidate domain authority, subdomains split it. Good: `yoursite.com/templates/resume/`. Bad: `templates.yoursite.com/resume/`.
4. **Genuine search intent match** — pages must actually answer what people search for.
5. **Quality over quantity** — 100 great pages beat 10,000 thin ones.
6. **Avoid penalties** — no doorway pages, keyword stuffing, or duplicate content.

---

## The 12 Playbooks

| Playbook | Pattern | Example |
|----------|---------|---------|
| Templates | "[Type] template" | "resume template" |
| Curation | "best [category]" | "best website builders" |
| Conversions | "[X] to [Y]" | "$10 USD to GBP" |
| Comparisons | "[X] vs [Y]" | "webflow vs wordpress" |
| Examples | "[type] examples" | "landing page examples" |
| Locations | "[service] in [location]" | "dentists in austin" |
| Personas | "[product] for [audience]" | "crm for real estate" |
| Integrations | "[A] [B] integration" | "slack asana integration" |
| Glossary | "what is [term]" | "what is pSEO" |
| Translations | Content in multiple languages | Localized content |
| Directory | "[category] tools" | "ai copywriting tools" |
| Profiles | "[entity name]" | "stripe ceo" |

### Choosing Your Playbook

| If you have... | Consider... |
|----------------|-------------|
| Proprietary data | Directories, Profiles |
| Product with integrations | Integrations |
| Design/creative product | Templates, Examples |
| Multi-segment audience | Personas |
| Local presence | Locations |
| Tool or utility product | Conversions |
| Content/expertise | Glossary, Curation |
| Competitor landscape | Comparisons |

Playbooks layer: "Best coworking spaces in San Diego" = Curation + Locations.

---

## Implementation Framework

### 1. Keyword Pattern Research

- Identify the repeating structure, the variables, and how many unique combinations exist
- Validate demand: aggregate search volume, head vs long-tail distribution, trend direction

### 2. Data Requirements

- What data populates each page? First-party, scraped, licensed, or public?
- How is it updated? Stale data kills these pages.

### 3. Template Design

Page structure:
- Header with the target keyword
- Unique intro (not just variables swapped)
- Data-driven sections
- Related pages / internal links
- CTAs appropriate to search intent

Ensuring uniqueness:
- Conditional content based on data (sections that appear only when data supports them)
- Original insights/analysis per page

### 4. Internal Linking Architecture

**Hub and spoke:** hub = main category page; spokes = individual programmatic pages; cross-links between related spokes.

Avoid orphan pages: every page reachable from the main site, XML sitemap coverage, breadcrumbs with structured data.

### 5. Indexation Strategy

- Prioritize high-volume patterns first
- Noindex very thin variations
- Manage crawl budget; separate sitemaps by page type

---

## Quality Checks

### Pre-Launch

Content: each page provides unique value, answers intent, is readable and useful.
Technical: unique titles and meta descriptions, proper heading structure, schema markup, acceptable page speed.
Linking: connected to site architecture, related pages linked, no orphans.
Indexation: in XML sitemap, crawlable, no conflicting noindex.

### Post-Launch

Track: indexation rate, rankings, traffic, engagement, conversion.
Watch for: thin-content warnings, ranking drops, manual actions, crawl errors.

---

## Common Mistakes

- **Thin content**: just swapping city names in identical text
- **Keyword cannibalization**: multiple pages targeting the same keyword
- **Over-generation**: pages with no search demand
- **Poor data quality**: outdated or incorrect information
- **Ignoring UX**: pages that exist for Google, not users

---

## Output Format

**Strategy document:** opportunity analysis, implementation plan, content guidelines.
**Page template:** URL structure, title/meta templates, content outline, schema markup.

## Questions to Ask

1. What keyword patterns are you targeting?
2. What data do you have (or can acquire)?
3. How many pages are you planning?
4. What does your site authority look like, and who currently ranks?

## Related Skills

- Use the **seo-audit** skill to audit programmatic pages after launch
- Use the **competitors** skill for comparison/alternative page frameworks
- Use the **directory-submissions** skill to build the backlinks these pages need
