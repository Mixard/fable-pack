---
name: seo-audit
description: Audit and diagnose SEO issues — crawlability, indexation, Core Web Vitals thresholds, on-page limits, hreflang/international SEO error catalog, and E-E-A-T. Use when the user asks why they're not ranking, traffic dropped, mentions technical SEO, meta tags, indexing issues, or says "help with SEO" — start with an audit.
---

# SEO Audit

You are an expert in search engine optimization. Identify SEO issues and provide actionable, prioritized recommendations.

## Before Auditing

If `.agents/product-marketing.md` exists (created by the product-marketing skill), read it first. Then understand: site type and business goal, priority keywords, known issues, recent changes/migrations, scope (full site vs specific pages), and whether Search Console access exists.

## Schema Markup Detection Limitation

**Plain HTTP fetches (web_fetch, curl) cannot reliably detect structured data.** Many CMS plugins (AIOSEO, Yoast, RankMath) inject JSON-LD via client-side JavaScript — it won't appear in static HTML, and HTML-to-text conversion strips `<script>` tags.

To check schema accurately:
1. **Browser tool** — render the page and run `document.querySelectorAll('script[type="application/ld+json"]')`
2. **Google Rich Results Test** — https://search.google.com/test/rich-results (renders JS)
3. **Screaming Frog export** — if available (renders JS)

Never report "no schema found" based solely on a raw fetch.

## Priority Order

1. **Crawlability & indexation** (can Google find and index it?)
2. **Technical foundations** (fast and functional?)
3. **On-page optimization**
4. **Content quality** (does it deserve to rank?)
5. **Authority & links**

---

## Technical SEO Audit

### Crawlability

- **robots.txt**: no unintentional blocks; sitemap referenced
- **XML sitemap**: exists, submitted to Search Console, contains only canonical indexable URLs
- **Architecture**: important pages within 3 clicks of homepage; logical hierarchy; no orphan pages
- **Crawl budget** (large sites): parameterized URLs controlled, faceted navigation handled, no session IDs in URLs

### Indexation

- `site:domain.com` check; Search Console coverage vs expected page count
- Noindex tags on important pages; canonicals pointing the wrong way; redirect chains/loops; soft 404s
- **Canonicalization**: self-referencing canonicals on unique pages; HTTP→HTTPS; www vs non-www and trailing-slash consistency

### Core Web Vitals

- **LCP** (Largest Contentful Paint): < 2.5s
- **INP** (Interaction to Next Paint): < 200ms
- **CLS** (Cumulative Layout Shift): < 0.1

Speed factors: TTFB, image optimization, JS execution, CSS delivery, caching, CDN, font loading. Tools: PageSpeed Insights, WebPageTest, Search Console CWV report.

### Mobile, Security, URLs

- Responsive design, tap targets, viewport, same content as desktop
- HTTPS everywhere, valid cert, no mixed content, HTTP→HTTPS redirects
- Readable lowercase hyphenated URLs, no unnecessary parameters

---

## International SEO & Localization

Check whenever the site serves multiple languages or regions — misconfigurations can suppress entire locale variants or drag down site-wide quality signals.

### Hreflang

Three equivalent placements: HTML `<link>` in `<head>`, HTTP `Link` headers, XML sitemap `<xhtml:link>`. If using multiple, they must agree — conflicting signals cause Google to drop that pair. For 10+ locales, prefer sitemap-based (no page weight).

**Check for:**
- Self-referencing entry on every page (page must include itself in the hreflang set — missing it invalidates ALL hreflang on the page)
- Reciprocal links (if A points to B, B must point back, or both are ignored)
- Valid codes: ISO 639-1 language + optional ISO 3166-1 Alpha-2 region (`en`, `en-GB` — never `en-UK`)
- `x-default` present, pointing to the fallback page (language selector or default locale)
- All target URLs return 200, are indexable, and match their canonical URL
- No duplicate language-region codes pointing to different URLs

**Common errors:** missing self-reference (all hreflang ignored); no return tag (pair dropped); `en-UK` instead of `en-GB`; hreflang target is non-canonical, 404, or blocked (cluster discarded); HTML and sitemap annotations disagree.

**At scale:** `<xhtml:link>` children don't count toward the 50K-URL sitemap limit, but the 50MB file limit becomes the bottleneck — plan 2K-5K URLs per file with full hreflang. Hreflang isn't required on every page; focus on pages receiving wrong-language traffic. Bing treats hreflang as a weak signal — supplement with `<html lang>` and `<meta http-equiv="content-language">`.

### Canonicalization for Multilingual Sites

- Each locale page self-canonicals (`/ar/page` → `/ar/page`)
- **Never cross-locale canonical** (French → English) — suppresses the non-canonical locale entirely
- The canonical URL must appear in the hreflang set — otherwise all hreflang is silently ignored
- Canonical overrides hreflang when they conflict
- Protocol/domain must be consistent across canonical, hreflang, and sitemap
- Paginated locale pages: self-referencing canonical per page (never canonical page 2+ to page 1)

**Common mistakes:** all locales canonical to English (kills indexing); CMS setting deep-page canonicals to the homepage; protocol mismatch between canonical and hreflang.

### International Sitemaps

- `xmlns:xhtml` namespace on `<urlset>`; each `<url>` includes `<xhtml:link>` for all locales including itself; `x-default` included; absolute URLs
- Split sitemaps by content type, not by locale
- **Next.js caveat:** `alternates.languages` does NOT auto-include a self-referencing `<xhtml:link>` for the `<loc>` URL — add the current locale explicitly

### Locale URL Structure

- **Recommended:** subdirectories (`/en/`, `/ar/`). Acceptable: subdomains or ccTLDs. Not recommended: `?lang=en`
- All locales prefixed — hiding the locale from URLs prevents Google from distinguishing versions
- No IP/Accept-Language content negotiation (Googlebot crawls from US IPs with no Accept-Language header)
- Google's International Targeting report in Search Console is deprecated; geotargeting relies on hreflang, content signals, and linking patterns

### Content Quality Across Locales

- AI-translated content is not inherently spam (Google's 2025 stance), but scaled low-value translations can trigger the scaled-content-abuse policy
- Google detects language from visible content — translate ALL of it (title, description, headings, body), not just navigation. Translating only template chrome creates duplicates.
- The helpful-content system is site-wide — many thin locale pages can suppress rankings for strong pages too
- Don't noindex thin locales or cross-locale canonical; the right fix is not creating locale pages you can't make genuinely helpful
- Localize signals: currency, phone format, addresses

---

## On-Page SEO Audit

### Title Tags
- Unique per page; primary keyword near the beginning; 50-60 characters; brand name at the end
- Issues: duplicates, truncation, keyword stuffing, missing entirely

### Meta Descriptions
- Unique; 150-160 characters; includes primary keyword; clear value proposition and reason to click

### Headings
- One H1 per page containing the primary keyword; logical H1→H2→H3 hierarchy; no skipped levels; not used purely for styling

### Content
- Keyword in the first 100 words; related keywords naturally; sufficient depth; answers search intent; better than current top rankers
- Thin content: tag/category pages with no value, doorway pages, near-duplicates

### Images
- Descriptive filenames, alt text, compression, modern formats (WebP), lazy loading

### Internal Linking
- Important pages well-linked with descriptive anchors; no broken links; no orphans; no over-optimized anchor text

### Keyword Targeting
- One clear primary keyword per page; title/H1/URL aligned; no cannibalization between pages; logical topical clusters

---

## Content Quality (E-E-A-T)

- **Experience:** first-hand experience demonstrated, original insights/data, real examples
- **Expertise:** author credentials visible, accurate detail, sourced claims
- **Authoritativeness:** recognized in the space, cited by others
- **Trustworthiness:** transparency, contact info, privacy/terms, HTTPS

---

## Common Issues by Site Type

- **SaaS:** thin feature pages, blog disconnected from product pages, missing comparison/alternative pages, no glossary
- **E-commerce:** thin category pages, duplicate product descriptions, missing product schema, faceted-navigation duplicates, mishandled out-of-stock pages
- **Content/blog:** stale content, cannibalization, no topical clustering, missing author pages
- **Multilingual:** hreflang errors, cross-locale canonicals, thin locales, only boilerplate translated, no x-default, IP-based redirects hiding content from Googlebot
- **Local:** inconsistent NAP, missing local schema, no Google Business Profile optimization, no location pages

---

## Output Format

**Executive summary:** overall health, top 3-5 priority issues, quick wins.

For each finding: **Issue** (what's wrong) → **Impact** (High/Medium/Low) → **Evidence** (how you found it) → **Fix** (specific recommendation) → **Priority**.

**Prioritized action plan:** 1) critical fixes blocking indexation/ranking, 2) high-impact improvements, 3) quick wins, 4) long-term recommendations.

## Tools

Free: Google Search Console (essential), PageSpeed Insights, Bing Webmaster Tools, Rich Results Test (use this for schema — it renders JavaScript), Schema Validator.
Paid (if available): Screaming Frog, Ahrefs/Semrush, Sitebulb, ContentKing.

## Related Skills

- Use the **ai-seo** skill for AI search optimization (AI Overviews, ChatGPT/Perplexity citations)
- Use the **programmatic-seo** skill for building pages at scale
- Use the **competitors** skill for comparison-page opportunities
