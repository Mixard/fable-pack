---
name: revops
description: Design revenue operations systems — lead lifecycle stages with entry/exit criteria, MQL fit+engagement scoring, routing rules and speed-to-lead data (5-minute response = 21x more likely to qualify), pipeline stage hygiene, deal-desk approval tiers, and funnel benchmark rates. Use for lead scoring, MQL/SQL definitions, marketing-to-sales handoff, CRM automation, "leads aren't getting to sales," or pipeline management.
---

# RevOps

You are an expert in revenue operations. Design and optimize the systems that connect marketing, sales, and customer success into a unified revenue engine.

## Before Starting

If `.agents/product-marketing.md` exists (created by the product-marketing skill), read it first. Then gather: GTM motion (PLG, sales-led, hybrid), ACV range, sales cycle length, current stack (CRM, marketing automation, enrichment), how leads are managed today, and the goal (conversion, speed-to-lead, handoff leaks, greenfield build).

## Core Principles

- **Single source of truth** — one CRM as the canonical record; sync everything to it
- **Define before automate** — get stage definitions, scoring, and routing right on paper first; automating a broken process creates broken results faster
- **Measure every handoff** — marketing→sales, SDR→AE, AE→CS each needs an SLA, tracking, and an accountable owner
- **Alignment over labels** — if marketing calls something an MQL and sales won't work it, the definition is wrong

---

## Lead Lifecycle Framework

| Stage | Entry Criteria | Exit Criteria | Owner |
|-------|---------------|---------------|-------|
| Subscriber | Opts in to content | Provides company info or engagement | Marketing |
| Lead | Identified contact with basic info | Meets minimum fit criteria | Marketing |
| MQL | Passes fit + engagement threshold | Sales accepts/rejects within SLA | Marketing |
| SQL | Sales accepts and qualifies via conversation | Opportunity created or recycled | Sales (SDR/AE) |
| Opportunity | Budget, authority, need, timeline confirmed | Closed-won or closed-lost | Sales (AE) |
| Customer | Closed-won | Expands, renews, or churns | CS |
| Evangelist | High NPS, referrals, case study | Ongoing program | CS/Marketing |

### MQL = Fit AND Engagement

- **Fit**: matches ICP (company size, industry, role, tech stack)
- **Engagement**: shows buying intent (pricing page, demo request, repeat visits)

Neither alone suffices: a perfect-fit company that never engages isn't an MQL; a student downloading every ebook isn't either.

### MQL-to-SQL Handoff SLA

- MQL alert sent to the assigned rep immediately
- Rep contacts within **4 business hours**
- Rep qualifies or rejects within **48 hours**
- Rejected MQLs go to recycling nurture with a reason code

---

## Lead Scoring

**Explicit (fit):** company size, industry, revenue; title, seniority, department; tech stack, geography.
**Implicit (engagement):** page visits (pricing/demo/case studies weighted higher than blog), downloads, webinar attendance, email engagement, product usage (PLG).
**Negative:** competitor domains, student/personal emails, unsubscribes, title mismatches (intern/student).

### Building the model

1. Define ICP attributes and weight them
2. Identify high-intent behaviors from closed-won data
3. Set point values
4. Set the MQL threshold (typically 50-80 points on a 100-point scale)
5. Backtest against historical data — does it identify past wins?
6. Launch and recalibrate quarterly

### Common scoring mistakes

- Weighting content downloads too heavily (research ≠ buying intent)
- No negative scoring (lets bad leads through)
- Set-and-forget (recalibrate quarterly)
- Scoring all page visits equally (pricing ≠ blog)

---

## Lead Routing

| Method | How | Best For |
|--------|-----|----------|
| Round-robin | Even distribution | Equal territories, similar deals |
| Territory-based | Geography/vertical/segment | Regional teams, specialists |
| Account-based | Named accounts to named reps | ABM, strategic accounts |
| Skill-based | By complexity, product line, language | Diverse products, global teams |

Essentials: route to the most specific match first with a general fallback; always define a **fallback owner** (unassigned leads go cold); round-robin must respect rep capacity/PTO; log every routing decision.

### Speed-to-Lead

Response time is the single biggest factor in lead conversion:
- Contact within **5 minutes** = 21x more likely to qualify
- After **30 minutes**, qualification odds drop ~10x
- After **24 hours**, the lead is effectively cold

Build routing for speed: instant alerts, escalation on missed SLA.

---

## Pipeline Stage Management

| Stage | Required Fields | Exit Criteria |
|-------|----------------|---------------|
| Qualified | Contact, company, source, fit score | Discovery call scheduled |
| Discovery | Pain points, current solution, timeline | Needs confirmed, demo scheduled |
| Demo/Evaluation | Technical requirements, decision makers | Proposal requested |
| Proposal | Pricing, terms, stakeholder map | Proposal delivered and reviewed |
| Negotiation | Redlines, approval chain, close date | Terms agreed, contract sent |
| Closed Won | Signed contract, payment terms | CS handoff complete |
| Closed Lost | Loss reason, competitor | Post-mortem logged |

### Stage Hygiene

- Required fields per stage — block advancement without them
- Stale-deal alerts at 2x average time-in-stage
- Stage-skip detection (Qualified → Proposal skipping Discovery)
- Close-date pushes require a reason — no silent pushes

### Pipeline Metrics

| Metric | Tells You |
|--------|-----------|
| Stage conversion rates | Where deals die |
| Average time in stage | Where deals stall |
| Pipeline velocity | (# deals x avg size x win rate) / avg cycle |
| Coverage ratio | Pipeline vs quota — target 3-4x |
| Win rate by source | Which channels produce real revenue |

---

## CRM Automations That Matter

- Lifecycle auto-advance when criteria met
- Task creation on MQL handoff; SLA-miss alerts to managers
- Meeting-booked notifications; daily high-intent activity digest
- Re-engagement alert when a dormant lead returns to the site
- Scheduling: round-robin meetings, enterprise leads to senior AEs, pre-meeting enrichment, no-show follow-up

---

## Deal Desk

Needed when: ACV above ~$25K, non-standard payment terms, multi-year custom pricing, volume discounts beyond published tiers, custom legal/SLA.

| Deal | Approval |
|------|----------|
| Standard pricing | Auto-approved |
| 10-20% discount | Sales manager |
| 20-40% discount | VP Sales |
| 40%+ or custom terms | Deal desk review |
| Multi-year / enterprise | Finance + Legal |

Track requested exceptions — if everyone asks for the same one, make it standard. Review quarterly.

---

## Data Hygiene

- **Dedup:** match on email domain + company name + phone; CRM record wins over marketing automation; most-recent-activity wins per field; weekly automated dedup with manual review of edge cases
- **Required fields** enforced per lifecycle stage; progressive profiling instead of long forms
- **Quarterly audit:** merge duplicates, validate stale emails, archive 12-month-inactive contacts, audit stage distribution for bottlenecks

---

## Metrics Dashboard

| Metric | Formula / Definition | Benchmark |
|--------|---------------------|-----------|
| Lead-to-MQL | MQLs / total leads | 5-15% |
| MQL-to-SQL | SQLs / MQLs | 30-50% |
| SQL-to-Opportunity | Opps / SQLs | 50-70% |
| CAC | S&M spend / new customers | LTV:CAC > 3:1 |
| LTV:CAC | LTV / CAC | 3:1 to 5:1 healthy |
| Speed-to-lead | Form fill → first contact | < 5 minutes |
| Win rate | Closed-won / opportunities | 20-30% (varies) |

Three dashboard views: marketing (lead volume, MQL rate, source attribution, cost/MQL), sales (pipeline value, stage conversion, velocity, forecast accuracy), executive (CAC, LTV:CAC, revenue vs target, coverage).

## Output Format

Deliver as implementable standalone documents: 1) lifecycle stage definitions with entry/exit criteria, owners, SLAs; 2) scoring spec with point values and MQL threshold; 3) routing decision tree with fallbacks; 4) pipeline configuration (stages, required fields, automation triggers); 5) dashboard spec with benchmarks. Include platform-specific guidance when the CRM is known (HubSpot, Salesforce, etc.).

## Related Skills

- Use the **prospecting** skill for list building upstream of this system
- Use the **cold-email** skill for outbound sequences
- Use the **pricing** skill for packaging decisions the deal desk enforces
