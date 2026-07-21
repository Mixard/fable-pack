---
name: ab-testing
description: Design statistically valid A/B tests and run a growth experimentation program — sample-size tables, hypothesis framework, ICE prioritization, velocity targets, and an experiment playbook template. Use when the user wants to test two versions, asks how long to run a test, mentions statistical significance, or wants a systematic experiment backlog.
---

# A/B Testing & Experimentation

You are an expert in experimentation. Design tests that produce statistically valid, actionable results.

## Before Starting

If `.agents/product-marketing.md` exists (created by the product-marketing skill), read it first. Then understand: what you're trying to improve, the baseline conversion rate, traffic volume, and constraints (tooling, timeline).

---

## Core Principles

1. **Start with a hypothesis** — a specific prediction based on reasoning or data, not "let's see what happens"
2. **Test one thing** — single variable per test, or you can't attribute the result
3. **Statistical rigor** — pre-determine sample size; don't peek and stop early
4. **Measure what matters** — primary metric tied to business value, secondary metrics for context, guardrail metrics to prevent harm

## Hypothesis Framework

```
Because [observation/data],
we believe [change]
will cause [expected outcome]
for [audience].
We'll know this is true when [metrics].
```

**Weak:** "Changing the button color might increase clicks."
**Strong:** "Because users report difficulty finding the CTA (per heatmaps), we believe making the button larger with contrasting color will increase CTA clicks by 15%+ for new visitors, measured as click-through rate from page view to signup start."

---

## Sample Size Quick Reference

Visitors needed per variant (95% confidence, 80% power):

| Baseline conversion | Detect 10% lift | 20% lift | 50% lift |
|---------------------|-----------------|----------|----------|
| 1% | 150k/variant | 39k/variant | 6k/variant |
| 3% | 47k/variant | 12k/variant | 2k/variant |
| 5% | 27k/variant | 7k/variant | 1.2k/variant |
| 10% | 12k/variant | 3k/variant | 550/variant |

Use a calculator for exact numbers (Evan Miller's sample-size calculator or Optimizely's). If your traffic can't reach the sample size in ~4 weeks, test something bolder or move up-funnel.

## Test Types

| Type | Description | Traffic Needed |
|------|-------------|----------------|
| A/B | Two versions, single change | Moderate |
| A/B/n | Multiple variants | Higher |
| MVT | Multiple changes in combinations | Very high |
| Split URL | Different URLs per variant | Moderate |

## Metrics Selection

- **Primary**: the single metric you'll call the test on, directly tied to the hypothesis
- **Secondary**: explain why/how the change worked
- **Guardrail**: things that must not get worse; stop the test if significantly negative

Example (pricing page test): primary = plan selection rate; secondary = time on page, plan distribution; guardrail = support tickets, refund rate.

## Traffic Allocation

| Approach | Split | When |
|----------|-------|------|
| Standard | 50/50 | Default |
| Conservative | 90/10, 80/20 | Limit risk of a bad variant |
| Ramping | Start small, increase | Technical risk mitigation |

Ensure returning users see the same variant, and exposure is balanced across time of day/week.

## Implementation

- **Client-side** (JS modifies page after load): fast to ship, can flicker. Tools: PostHog, Optimizely, VWO.
- **Server-side** (variant decided before render): no flicker, needs dev work. Tools: PostHog, LaunchDarkly, Split.

## Running the Test

Pre-launch checklist: hypothesis documented, primary metric defined, sample size calculated, variants QA'd, tracking verified.

**The peeking problem:** checking results before reaching sample size and stopping early produces false positives. Pre-commit to the sample size. During the test: monitor for technical issues and guardrails only; don't modify variants or add new traffic sources.

## Analyzing Results

1. Reached sample size? If not, the result is preliminary.
2. Statistically significant? (95% confidence = p < 0.05 — a threshold, not a guarantee)
3. Effect size meaningful? Compare to your minimum detectable effect; project business impact.
4. Secondary metrics consistent with the story?
5. Guardrail concerns?
6. Segment differences? (Mobile vs desktop, new vs returning)

| Result | Conclusion |
|--------|------------|
| Significant winner | Implement variant |
| Significant loser | Keep control, learn why |
| No significant difference | Need more traffic or a bolder test |
| Mixed signals | Dig deeper, segment |

---

## Growth Experimentation Program

Individual tests are valuable; a continuous program is a compounding asset.

### The Experiment Loop

```
Generate hypotheses → ICE-prioritize → Run → Analyze → Promote winners to playbook → New hypotheses → repeat
```

### Hypothesis Sources

| Source | Look For |
|--------|----------|
| Analytics | Drop-off points, low-converting pages, weak segments |
| Customer research | Pain points, confusion, unmet expectations |
| Competitor analysis | Messaging or UX patterns they use that you don't |
| Support tickets | Recurring questions about conversion flows |
| Heatmaps/recordings | Hesitation, rage-clicks, abandonment |
| Past experiments | Significant losers often reveal new angles |

### ICE Prioritization

Score each hypothesis 1-10 on **Impact** (how much it moves the primary metric if it works), **Confidence** (based on data, not gut), **Ease** (how fast/cheap to ship and measure). ICE = (I + C + E) / 3. Run highest first; re-score monthly.

### Experiment Velocity Targets

| Metric | Target |
|--------|--------|
| Experiments launched per month | 4-8 for most teams |
| Win rate | 20-30% is normal for mature programs (sustained higher rates suggest conservative hypotheses) |
| Average test duration | 2-4 weeks |
| Backlog depth | 20+ hypotheses queued |

### The Experiment Playbook

When a test concludes, document the pattern:

```
## [Experiment Name]
**Date**: [date]
**Hypothesis**: [the hypothesis]
**Sample size**: [n per variant]
**Result**: [winner/loser/inconclusive] — [primary metric] changed by [X%] (95% CI: [range], p=[value])
**Guardrails**: [outcomes]
**Segment deltas**: [notable differences]
**Why it worked/failed**: [analysis]
**Pattern**: [the reusable insight — e.g., "social proof near pricing CTAs increases plan selection"]
**Apply to**: [other pages/flows]
**Status**: [implemented / parked / needs follow-up]
```

Over time this becomes a library of proven growth patterns specific to your product.

### Cadence

- **Weekly (30 min):** review running experiments for technical issues and guardrails. Don't call winners early; do stop tests with significantly negative guardrails.
- **Bi-weekly:** conclude finished experiments, update playbook, launch next from backlog.
- **Monthly (1 hr):** review velocity, win rate, cumulative lift; replenish and re-ICE the backlog.
- **Quarterly:** audit the playbook — which winning patterns haven't been scaled? Which funnel areas are under-tested?

---

## Common Mistakes

- Testing changes too small to detect; testing too many things at once
- Stopping early; changing variants mid-test
- Ignoring confidence intervals; cherry-picking segments; over-interpreting inconclusive results

## Related Skills

- Use the **popups**, **churn-prevention**, and **pricing** skills for test ideas in those areas
- Use the **ad-creative** skill for creative test structure on paid channels
