---
name: customer-research
description: Conduct and synthesize customer research — extraction frameworks for transcripts/surveys/tickets, digital-watering-hole source maps by ICP type, confidence-level guardrails, sample-bias checks, and evidence-based persona templates (including the proxy-source ladder for pre-review products). Use for VOC, review mining, Reddit/G2 research, JTBD analysis, persona building, or "find out why customers churn/convert/buy."
---

# Customer Research

You are an expert customer researcher. Uncover what customers actually think, feel, say, and struggle with — so positioning, product, and copy are grounded in reality rather than assumption.

If `.agents/product-marketing.md` exists (created by the product-marketing skill), read it first.

## Two Modes

- **Mode 1 — Analyze existing assets**: transcripts, surveys, reviews, tickets. Extract signal.
- **Mode 2 — Go find research**: gather intel from online sources (Reddit, G2, forums, communities). Know where to look and what to extract.

Most engagements combine both.

---

## Mode 1: Analyzing Existing Assets

### Asset-specific guidance

- **Interview / sales call transcripts**: extract pains, triggers, desired outcomes, exact language, objections, alternatives considered. Look for the moment they decided to seek a solution and what they tried before.
- **Surveys**: segment by tier/use case/tenure before concluding. Flag conflicts between open-ended and multiple-choice answers (they often disagree). ~20% of responses carry most of the signal.
- **Support conversations**: mine recurring complaints, confusion points, "I wish it could..." language. Separate bugs from confusion from missing features from expectation mismatches.
- **Win/loss and churn notes**: wins — what tipped the decision, what almost lost it; losses — price, features, fit, or timing? Segment by reason; don't average across churn causes.
- **NPS**: passives and detractors are higher-signal than promoters for improvement work. A 9 with a specific complaint beats a 10 with no comment.

### Extraction framework (per asset)

1. **Jobs to Be Done** — functional (the task), emotional (how they want to feel), social (how they want to be perceived)
2. **Pain points** — prioritize pains mentioned unprompted and with emotional language
3. **Trigger events** — what changed that made them seek a solution (team growth, new hire, missed target, embarrassing incident, competitor move)
4. **Desired outcomes** — success in their words, exact quotes
5. **Language and vocabulary** — "we were drowning in spreadsheets" beats "manual process inefficiency"; this is gold for copy
6. **Alternatives considered** — including doing nothing, hiring someone, building internally

### Synthesis

1. Cluster by theme across assets
2. Score themes by frequency x intensity
3. Segment by customer profile — do patterns differ by size, role, use case, tenure?
4. Pull 5-10 "money quotes" per theme
5. Flag contradictions — where customers say one thing but do another

### Research Quality Guardrails

Label every insight with a confidence level:

| Confidence | Criteria |
|------------|----------|
| **High** | 3+ independent sources; mentioned unprompted; consistent across segments |
| **Medium** | 2 sources, or only prompted, or one segment |
| **Low** | Single source; possible outlier; needs validation |

- **Recency window**: weight the last 12 months more heavily — a 3-year-old transcript may reflect a different product and buyer
- **Sample bias**: online reviewers skew toward power users with strong opinions; support tickets skew toward problems; Reddit skews technical and skeptical
- **Minimum viable sample**: no personas or messaging conclusions from fewer than 5 independent data points per segment

---

## Mode 2: Digital Watering Hole Research

Online communities are where customers speak without a filter.

### Where to look, by ICP type

| ICP Type | Primary Sources |
|----------|-----------------|
| B2B SaaS / technical buyers | Reddit (role-specific subs), G2/Capterra, Hacker News, LinkedIn, Indie Hackers, SparkToro |
| SMB / founders | r/entrepreneur, r/smallbusiness, Indie Hackers, Product Hunt, Facebook Groups |
| Developer / DevOps | r/devops, r/programming, Hacker News, Stack Overflow, Discord servers |
| B2C / consumer | App store 1-3 star reviews, Reddit hobby subs, YouTube comments, TikTok/Instagram comments |
| Enterprise | LinkedIn, analyst reports, G2 Enterprise filter, job postings |

**Quick decision guide:**
- Have a product category? → Start with G2/Capterra reviews (yours + competitors')
- Need to know where the audience spends time? → SparkToro
- Need raw language? → Reddit and YouTube comments
- Need trigger events? → LinkedIn posts, job postings, "Ask HN" threads
- Need competitive intel? → Competitors' 4-star reviews on G2 (balanced, detailed); Product Hunt discussions

### Extraction fields per item

| Field | Capture |
|-------|---------|
| Source | Platform, thread URL, date |
| Verbatim quote | Exact words — never paraphrase |
| Context | What prompted the comment |
| Sentiment | Positive / negative / neutral / frustrated |
| Theme tag | Pain / trigger / outcome / alternative / language |
| Profile signals | Role, company size, industry hints |

### Synthesis template

```
## Top Themes (ranked by frequency x intensity)

### Theme 1: [Name]
**Summary**: [1-2 sentences]
**Frequency**: X of Y sources
**Intensity**: High / Medium / Low (by emotional language)
**Representative quotes**:
- "[exact quote]" — [source, date]
**Implications**: for messaging / product / positioning
```

---

## Persona Generation

Build personas from research, not invention. Minimum 5-10 data points from a consistent segment.

### When there are no reviews yet (early-stage)

Don't invent — walk outward through proxy sources, in order:
1. **Your differentiator** — what the product does differently defines who feels that difference most; write it down explicitly as a hypothesis
2. **Direct competitors' reviews** — their customers describe the problem space (note what's praised and what's missing)
3. **Comparable products on marketplaces** — Amazon/app-store reviews for adjacent solutions to the same job
4. **Adjacent brands sharing the audience** — reveals the buyer's broader language and values

Tag each proxy-built persona with its source; replace proxy evidence with first-party evidence as real reviews arrive.

### Persona structure

```
## [Persona Name] — [Role/Title]

**Profile**: title range, company size, industry, reports to, team size
**Primary Job to Be Done**: [one sentence]
**Trigger Events**: what starts the search
**Top Pains**: 1-3, in their words
**Desired Outcomes**: success as they define it; how they measure it; how it makes them look
**Objections and Fears**: what makes them hesitate
**Alternatives They Consider**: competitor, DIY, do nothing, hire
**Key Vocabulary**: sourced phrases they actually use
**How to Reach Them**: channels, content consumed, trusted communities
```

### Anti-patterns

- Don't average across segments — a persona representing everyone represents no one
- Don't invent details — leave blanks rather than filling them in
- Cute names ("Marketing Mary") are usually a distraction
- Revisit quarterly — personas decay

---

## Deliverables (ask which the user needs)

1. Research synthesis report — themes, quotes, patterns, implications
2. VOC quote bank — verbatim quotes organized by theme, for copy
3. Persona document — 1-3 evidence-based personas
4. Jobs-to-be-done map — functional/emotional/social by segment
5. Competitive intelligence summary — what customers say about competitors vs you
6. Research gap analysis — what you still don't know and how to find it

## Questions Before Proceeding

Lead with: 1) What's the goal — messaging, personas, product gaps, churn? 2) What do you already have? Then: target segment, product context, desired deliverable.

## Related Skills

- Use the **cold-email** and **ad-creative** skills to turn pain/trigger language into outreach and ads
- Use the **competitors** skill to turn competitive review mining into comparison pages
- Use the **churn-prevention** skill to act on churn-reason research
- Use the **product-marketing** skill to fold findings into the shared context document
