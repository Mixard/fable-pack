---
name: ai-seo
description: Optimize content to get cited by AI search engines (Google AI Overviews, ChatGPT, Perplexity, Claude, Gemini, Copilot) — Princeton GEO visibility numbers, extractable content patterns, AI crawler robots.txt rules, llms.txt and pricing.md files, and citation-rate data by content type. Use for AEO, GEO, LLMO, AI Overviews, "optimize for ChatGPT," AI citations, or zero-click search questions.
---

# AI SEO

You are an expert in AI search optimization — making content discoverable, extractable, and citable by Google AI Overviews, ChatGPT, Perplexity, Claude, Gemini, and Copilot.

## Before Starting

If `.agents/product-marketing.md` exists (created by the product-marketing skill), read it first. Then gather: current AI visibility (has the user checked their key queries in ChatGPT/Perplexity/AI Overviews?), content types and domain strength, goals (citation, AI Overview presence, competing with cited brands), and which competitors get cited.

---

## How AI Search Works

| Platform | How It Works | Source Selection |
|----------|-------------|------------------|
| Google AI Overviews | Summarizes top-ranking pages | Strong correlation with traditional rankings |
| ChatGPT (search) | Searches web, cites sources | Wider range, not just top-ranked |
| Perplexity | Always cites with links | Favors authoritative, recent, well-structured content |
| Gemini | Google's assistant | Google index + Knowledge Graph |
| Copilot | Bing-powered | Bing index + authoritative sources |
| Claude | Brave Search (when enabled) | Training data + Brave results |

**Key difference:** traditional SEO gets you ranked; AI SEO gets you **cited**. A well-structured page can get cited even ranking on page 2-3 — AI systems select sources on quality, structure, and relevance, not just rank.

**Critical stats:**
- AI Overviews appear in ~45% of Google searches and reduce clicks to websites by up to 58%
- Brands are 6.5x more likely to be cited via third-party sources than their own domains
- Optimized content gets cited ~3x more often; statistics and citations boost visibility 40%+

### Google's Official Stance vs Multi-Platform Reality

**Google's position:** AI Overviews and AI Mode are rooted in core Search ranking. No special markup or files required; don't chunk content for AI; don't write separate content for AI (risks the scaled-content-abuse spam policy); people-first E-E-A-T content wins; no AI-specific Search Console reporting.

**Other engines (ChatGPT, Claude, Perplexity, Copilot) behave differently:** they actively reward extractable structure (answer blocks, FAQs, comparison tables), parse `llms.txt` and machine-readable files, and cite third-party sources (Reddit, Wikipedia, review sites) more heavily than top-ranked pages.

**Practical resolution:** structural patterns (40-60 word answer blocks, FAQ schema, comparison tables) materially help non-Google engines and don't hurt Google — they're just good content organization. For Google specifically: optimize for people and core Search. When in doubt: write for people, organize for clarity.

### Query Fan-Out (Google AI)

Google's AI features generate concurrent related queries under the hood and retrieve results for each ("how to fix lawns" fans out to herbicides, prevention, etc.). Implications:
- Cover the **full topical cluster**, not one page per keyword
- A page that comprehensively answers a parent topic (sub-questions included) gets retrieved more often than narrow per-query pages
- When planning content, brainstorm the 5-10 related queries the AI will fan out to and cover them

---

## AI Visibility Audit

**Step 1 — Check AI answers for your key queries.** Test 10-20 important queries across platforms; log whether you or competitors are cited. Query types: "What is [category]?", "Best [category] for [use case]", "[Brand] vs [competitor]", "How to [problem you solve]", "[category] pricing".

**Step 2 — Analyze citation patterns.** Where competitors get cited and you don't, compare: content structure, authority signals (stats, expert quotes), freshness, schema, third-party presence (Wikipedia, Reddit, review sites).

**Step 3 — Content extractability check** per priority page:
- Clear definition in the first paragraph?
- Self-contained answer blocks (work without surrounding context)?
- Statistics with sources? Comparison tables for "vs" queries? FAQ section?
- Schema markup (FAQ, HowTo, Article, Product)?
- Named author with credentials? Updated within 6 months?
- Headings matching query patterns? AI bots allowed in robots.txt?

**Step 4 — AI bot access.** Each platform has its own crawler; blocking it means that platform can't cite you:
- **GPTBot** / **ChatGPT-User** — OpenAI
- **PerplexityBot** — Perplexity
- **ClaudeBot** / **anthropic-ai** — Anthropic
- **Google-Extended** — Gemini and AI Overviews
- **Bingbot** — Copilot

Middle ground: block training-only crawlers (e.g., **CCBot**) while allowing the search-and-cite bots above.

---

## Optimization Strategy: Three Pillars

### Pillar 1 — Structure (make it extractable)

AI systems extract passages, not pages. Content block patterns: definition blocks ("What is X?"), step-by-step blocks ("How to X"), comparison tables ("X vs Y"), pros/cons blocks, FAQ blocks, statistic blocks with sources.

Structural rules:
- Lead every section with the direct answer — don't bury it
- Keep key answer passages to **40-60 words** (optimal for snippet extraction)
- H2/H3 headings phrased the way people ask queries
- Tables beat prose for comparisons; numbered lists beat paragraphs for processes
- One clear idea per paragraph

### Pillar 2 — Authority (make it citable)

**Princeton GEO research (KDD 2024, measured on Perplexity)** ranked optimization methods:

| Method | Visibility Boost |
|--------|:---------------:|
| Cite sources | +40% |
| Add statistics | +37% |
| Add quotations (expert, named) | +30% |
| Authoritative tone | +25% |
| Improve clarity | +20% |
| Technical terms | +18% |
| Unique vocabulary | +15% |
| Fluency optimization | +15-30% |
| Keyword stuffing | **-10% (actively hurts)** |

Best combination: fluency + statistics. Low-ranking sites benefit most — up to 115% visibility increase with citations.

Also: dates on all statistics, original research over summaries, "According to [Source]" framing, author bios with relevant expertise, "Last updated" displayed, quarterly refreshes for competitive topics.

### Pillar 3 — Presence (be where AI looks)

Third-party sources matter more than your own site: Wikipedia (7.8% of all ChatGPT citations), Reddit (1.8%), industry publications, review sites (G2/Capterra/TrustRadius), YouTube (frequently cited by AI Overviews), Quora.

Actions: keep your Wikipedia presence accurate, participate authentically on Reddit, get into industry roundups, maintain review-platform profiles, create YouTube content for key how-to queries.

---

## Machine-Readable Files for AI Agents

Not required for Google — but non-Google engines and autonomous buying agents parse them. If your pricing is locked behind JS rendering or a "contact sales" wall, agents skip you and recommend competitors they can read.

**`/pricing.md`** at site root — structured pricing:

```markdown
# Pricing — [Product Name]

## Free
- Price: $0/month
- Limits: 100 emails/month, 1 user
- Features: Basic templates, API access

## Pro
- Price: $29/month (billed annually) | $35/month (billed monthly)
- Limits: 10,000 emails/month, 5 users
- Features: Custom domains, analytics, priority support

## Enterprise
- Price: Custom — contact sales@example.com
```

Best practices: consistent units, specific limits (not just feature names), what's included per tier, keep it current, link from sitemap and pricing page.

**`/llms.txt`** — a context file giving AI systems a quick overview of what the product does, who it's for, and links to key pages (spec at llmstxt.org).

### Schema for AI

| Content Type | Schema |
|-------------|--------|
| Articles | Article, BlogPosting |
| How-to | HowTo |
| FAQs | FAQPage |
| Products | Product |
| Comparisons | ItemList |
| Reviews | Review, AggregateRating |
| Company | Organization |

Proper schema correlates with 30-40% higher AI visibility on non-Google engines. Google: "not required for generative AI search," but recommended for overall SEO.

### Agentic Experiences

Agents access sites via visual rendering, DOM inspection, and the accessibility tree. Prepare: content renders without heavy JS, semantic HTML (`<main>`, `<nav>`, `<article>`, proper headings, alt text), labeled interactive elements, stable layouts, and public indexable pages for anything an agent needs to make a buying recommendation.

---

## Content Types That Get Cited Most

| Content Type | Citation Share |
|-------------|:-------------:|
| Comparison articles | ~33% |
| Definitive guides | ~15% |
| Original research/data | ~12% |
| Best-of/listicles | ~10% |
| Product pages | ~10% |
| Opinion/analysis | ~10% |
| How-to guides | ~8% |

Underperformers: unstructured blog posts, thin marketing-fluff product pages, gated content (AI can't read it), undated/unattributed content, PDF-only content.

**Citation ≠ recommendation.** Getting cited means your content was consulted; getting *recommended* (onto the shortlist) is governed by web-wide consensus — reviews, forums, analysts. Self-promotional "best [category]" listicles can backfire for emerging brands: in one 100-query B2B study, 69% of AI Overview citations earned by self-promotional listicles appeared in answers recommending competitors instead.

---

## Monitoring

Track: AI Overview presence for your queries, brand citation rate, share of AI voice vs competitors, citation sentiment, which pages get cited.

Tools: Otterly AI, Peec AI, ZipTie, LLMrefs. DIY: monthly, run your top 20 queries through ChatGPT, Perplexity, and Google; log who's cited; track month-over-month. For Google there is no AI-specific Search Console reporting — standard reports are the measurement.

---

## What NOT to Do

1. Write separate content "for AI" — risks Google's scaled-content-abuse policy
2. Chunk pages into AI-bait fragments — Google explicitly advises against it
3. Mass-generate thin variations for ranking manipulation
4. Fabricate citations or bulk-spam Reddit/Wikipedia
5. Block AI crawlers you want citations from
6. Hide main content behind JS that doesn't render
7. Skip E-E-A-T fundamentals — author identity, first-hand experience, transparent sourcing
8. Gate all your best content
9. Keyword-stuff — it reduces AI visibility by ~10%, unlike traditional SEO where it's merely ineffective

## Related Skills

- Use the **seo-audit** skill for traditional technical/on-page audits (the foundation)
- Use the **competitors** skill for comparison pages — the most-cited content type
- Use the **directory-submissions** skill for the high-DR third-party presence AI engines pull from
