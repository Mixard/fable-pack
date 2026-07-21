---
name: product-marketing
description: Create or update a product marketing context document (.agents/product-marketing.md) capturing positioning, ICP, personas, competitors, objections, customer language, and proof points. Use at the start of a project before other marketing skills, or when the user mentions positioning, ICP, target audience, or wants to stop repeating foundational product info across marketing tasks.
---

# Product Marketing Context

You help users create and maintain a product marketing context document. This captures foundational positioning and messaging information that other marketing skills reference, so users don't repeat themselves.

The document is stored at `.agents/product-marketing.md`. Other marketing skills in this pack check for this file before asking questions.

## Workflow

### Step 1: Check for Existing Context

First, check if `.agents/product-marketing.md` already exists (also check `.claude/product-marketing.md` in older setups).

**If it exists:**
- Read it and summarize what's captured — note the current document version and recent changelog entries
- Ask which sections they want to update
- Only gather info for those sections
- On any substantive save, bump the version and add a changelog entry (see Step 4)

**If it doesn't exist, offer two options:**

1. **Auto-draft from codebase** (recommended): Study the repo — README, landing pages, marketing copy, about pages, meta descriptions, package.json, existing docs — and draft a V1. The user then reviews, corrects, and fills gaps. Faster than starting from scratch.

2. **Start from scratch**: Walk through each section conversationally, one at a time.

After presenting a draft, ask: "What needs correcting? What's missing?"

### Step 2: Gather Information

Walk through the sections below. For each: briefly explain what you're capturing, ask relevant questions, confirm accuracy, move on. Don't dump all questions at once.

Push for verbatim customer language — exact phrases are more valuable than polished descriptions because they reflect how customers actually think and speak.

---

## Sections to Capture

### 1. Product Overview
- One-line description
- What it does (2-3 sentences)
- Product category (what "shelf" you sit on — how customers search for you)
- Product type (SaaS, marketplace, e-commerce, service, etc.)
- Business model and pricing

### 2. Target Audience
- Target company type (industry, size, stage)
- Target decision-makers (roles, departments)
- Primary use case (the main problem you solve)
- Jobs to be done (2-3 things customers "hire" you for)
- Specific use cases or scenarios

### 3. Personas (B2B only)
If multiple stakeholders are involved in buying, capture for each:
- User, Champion, Decision Maker, Financial Buyer, Technical Influencer
- What each cares about, their challenge, and the value you promise them

### 4. Problems & Pain Points
- Core challenge customers face before finding you
- Why current solutions fall short
- What it costs them (time, money, opportunities)
- Emotional tension (stress, fear, doubt)

### 5. Competitive Landscape
- **Direct competitors**: same solution, same problem (e.g., Calendly vs SavvyCal)
- **Secondary competitors**: different solution, same problem (e.g., Calendly vs Superhuman scheduling)
- **Indirect competitors**: conflicting approach (e.g., Calendly vs personal assistant)
- How each falls short for customers

### 6. Differentiation
- Key differentiators (capabilities alternatives lack)
- How you solve it differently
- Why that's better (benefits)
- Why customers choose you over alternatives

### 7. Objections & Anti-Personas
- Top 3 objections heard in sales and how to address them
- Who is NOT a good fit (anti-persona)

### 8. Switching Dynamics
The JTBD Four Forces:
- **Push**: what frustrations drive them away from current solution
- **Pull**: what attracts them to you
- **Habit**: what keeps them stuck with current approach
- **Anxiety**: what worries them about switching

### 9. Customer Language
- How customers describe the problem (verbatim)
- How they describe your solution (verbatim)
- Words/phrases to use
- Words/phrases to avoid
- Glossary of product-specific terms

### 10. Brand Voice
- Tone (professional, casual, playful, etc.)
- Communication style (direct, conversational, technical)
- Brand personality (3-5 adjectives)

### 11. Proof Points
- Key metrics or results to cite
- Notable customers/logos
- Testimonial snippets
- Main value themes and supporting evidence

### 12. Goals
- Primary business goal
- Key conversion action (what you want people to do)
- Current metrics (if known)

---

## Step 3: Create the Document

After gathering information, create `.agents/product-marketing.md` with this structure:

```markdown
# Product Marketing Context

**Document version:** v1
**Last updated:** [date]

## Product Overview
**One-liner:**
**What it does:**
**Product category:**
**Product type:**
**Business model:**

## Target Audience
**Target companies:**
**Decision-makers:**
**Primary use case:**
**Jobs to be done:**
-
**Use cases:**
-

## Personas
| Persona | Cares about | Challenge | Value we promise |
|---------|-------------|-----------|------------------|
| | | | |

## Problems & Pain Points
**Core problem:**
**Why alternatives fall short:**
-
**What it costs them:**
**Emotional tension:**

## Competitive Landscape
**Direct:** [Competitor] — falls short because...
**Secondary:** [Approach] — falls short because...
**Indirect:** [Alternative] — falls short because...

## Differentiation
**Key differentiators:**
-
**How we do it differently:**
**Why that's better:**
**Why customers choose us:**

## Objections
| Objection | Response |
|-----------|----------|
| | |

**Anti-persona:**

## Switching Dynamics
**Push:**
**Pull:**
**Habit:**
**Anxiety:**

## Customer Language
**How they describe the problem:**
- "[verbatim]"
**How they describe us:**
- "[verbatim]"
**Words to use:**
**Words to avoid:**
**Glossary:**
| Term | Meaning |
|------|---------|
| | |

## Brand Voice
**Tone:**
**Style:**
**Personality:**

## Proof Points
**Metrics:**
**Customers:**
**Testimonials:**
> "[quote]" — [who]
**Value themes:**
| Theme | Proof |
|-------|-------|
| | |

## Goals
**Business goal:**
**Conversion action:**
**Current metrics:**

## Changelog
*Newest first. One line per revision: what changed and why.*
- v1 ([date]) — Initial context.
```

---

## Step 4: Confirm, Version, and Save

- Show the completed document and ask if anything needs adjustment
- **New document:** set `Document version: v1` and a single changelog entry
- **Updating:** increment the version (v2 → v3 ...), update `Last updated` to today, prepend a new changelog entry (newest first) summarizing what changed and why in one line. Never rewrite or reorder past entries. Good entries name the sections touched and the reason, e.g.:
  - `- v3 (2026-07-16) — Repositioned from "email tool" to "deliverability platform"; added RevOps to the ICP.`
- **Pure typo fix:** don't bump the version
- Use ISO dates (YYYY-MM-DD)
- Save to `.agents/product-marketing.md`
- Tell the user: other marketing skills will now use this context automatically

---

## Tips

- **Be specific**: ask "What's the #1 frustration that brings them to you?" not "What problem do they solve?"
- **Capture exact words**: customer language beats polished descriptions
- **Ask for examples**: "Can you give me an example?" unlocks better answers
- **Validate as you go**: summarize each section and confirm before moving on
- **Skip what doesn't apply**: not every product needs all sections (e.g., Personas for B2C)
