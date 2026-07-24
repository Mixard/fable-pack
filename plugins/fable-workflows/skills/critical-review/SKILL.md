---
name: critical-review
description: Use when asked to re-examine existing materials, plans, strategies, or results with fresh eyes and find what was missed - stale assumptions, blind spots, contradictions with own data, overlooked opportunities. Russian triggers - "подумай", "посмотри под другим углом", "что мы упускаем", "критическое мышление", "что не так". Not for dead ends - if something is claimed impossible or blocked, use getting-unstuck instead.
---

# Critical Review

## Overview

Projects fail quietly long before they fail loudly. The materials already contain the warning signs - assumptions nobody re-checked, decisions made under conditions that no longer hold, data that contradicts the plan, opportunities dismissed in one line months ago. A generic "looks good, maybe improve X" pass finds none of this.

**Core principle:** a finding without evidence is an opinion. Every "we missed this" must arrive with the fact that proves it - a number, a test run, a quote from the materials themselves.

**Boundary with getting-unstuck:** that skill fires when a path is claimed *closed* ("impossible", "unsupported", "blocked") and breaks the wall. This skill fires when nothing is visibly wrong - and hunts for what the current angle of view hides. If this review surfaces a "we can't do X" claim, hand it to getting-unstuck for demolition.

## The Iron Law

```
NO FINDING WITHOUT EVIDENCE. NO REVIEW WITHOUT ALL LENSES.
```

A review that skips lenses finds only what it was already looking for - which is exactly the failure mode this skill exists to break.

## When to Use

- The user asks to "подумай", "посмотри под другим углом", "что мы упускаем", or requests a critical pass over materials
- Before committing to the next phase of a project (scaling spend, going live, building on top of a decision)
- After new data arrived that nobody has reconciled with the original plan
- The project feels fine but hasn't been challenged since it started

**Not for:** debugging a concrete failure (systematic-debugging), breaking a declared dead end (getting-unstuck), reviewing a code diff (requesting-code-review).

## The Four Phases

### Phase 1: Inventory the Claims

Read the materials and extract every load-bearing claim - assumptions, decisions, conclusions, targets. For each one record:

1. **Evidence class:** VERIFIED (tested/measured, source in hand) or ASSUMED (memory, extrapolation, "seemed reasonable at the time")
2. **Freshness:** when was it last checked, and has anything relevant changed since
3. **Load:** what breaks downstream if this claim is false

Output: a numbered claim list. ASSUMED + high-load + stale is the priority queue for Phase 3.

### Phase 2: The Lens Pass

Run **every** lens over the materials. Each lens answers one question and produces candidate findings - do not evaluate them yet, evaluation during generation kills the uncomfortable ones first.

| Lens | Question |
|------|----------|
| Assumption audit | "Which claims from Phase 1 have never been tested - and what one command/query would test them today?" |
| Pre-mortem (inversion) | "It's N weeks later and this plan failed. What is the most plausible written post-mortem?" |
| Hostile skeptic | "A competitor or a harsh reviewer reads these materials. What do they attack first?" |
| Data contradiction | "What in our own numbers/logs/results contradicts our stated conclusions?" |
| Dismissed alternatives | "What options were rejected in one line? Do the rejection reasons still hold?" |
| Zoom out | "Restate the goal one level up. Does the current work still serve it, or are we optimizing a step?" |
| Fresh eyes | "Spawn a subagent with a *neutral* statement - goal and raw facts only, none of the accumulated framing - and compare its read against ours." |

Write candidates as a numbered list, each with a one-line verification test: not "the audience might be wrong" but "F3: targeting assumes movers are reachable via interest X - test: pull delivery_estimate for the exact ad-set spec."

### Phase 3: Verify the Findings

Same discipline as getting-unstuck Phase 3:

1. **Rank by cost-to-test, not by comfort.** The finding you least want to be true gets no discount.
2. **Verdict only by evidence.** CONFIRMED (fact in hand) / REFUTED (fact in hand) / INCONCLUSIVE (test too costly now - report it, don't bury it).
3. **Minimal experiments, timeboxed.** One variable, minutes not hours.
4. **Record a written log** - one block per finding:

   ```
   F3: targeting assumes movers reachable via interest X
   Test: delivery_estimate for exact ad-set spec    (timebox: 3 min)
   Verdict: REFUTED - audience is 217k, not narrow; assumption was stale
   New fact: interest cage conflicts with broad-on-sub-$10 guardrail
   ```

5. **Let results breed.** A confirmed finding often reclassifies other claims from Phase 1 - loop once with the new facts. Two rounds with no new distinct finding means stop and report.

### Phase 4: Report

Rank confirmed findings by impact, not by discovery order. For each:

1. **What we missed** - one sentence
2. **The evidence** - the fact/log block that proves it
3. **What changes** - the concrete decision or action it triggers

Then route: blocked opportunities → getting-unstuck; concrete defects → systematic-debugging; plan revisions → writing-plans. Close with the INCONCLUSIVE list and what testing each would cost.

A report of confirmed findings without evidence blocks, or a "nothing found" verdict without a full lens pass, is a process violation - return to Phase 2.

## Red Flags - STOP and Follow Process

- Producing generic advice that would fit any project ("consider adding tests", "monitor metrics")
- Skipping a lens because "it obviously doesn't apply here"
- Reporting a finding you haven't verified because it "feels right"
- Softening a confirmed finding because it contradicts earlier work done in this same session
- Declaring "everything looks fine" in less time than reading the materials takes

**ALL of these mean: STOP. Return to the phase you shortcut.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "We already reviewed this last month" | Claims decay. VERIFIED has a date; after it, it's ASSUMED again. |
| "The author knew what they were doing" | Competence doesn't stop conditions from changing under a decision. |
| "Criticizing our own plan wastes momentum" | A blind spot found today costs an edit. Found in production, it costs the project. |
| "The data roughly matches" | "Roughly" is where contradictions hide. Reconcile the exact numbers. |
| "That alternative was rejected for a reason" | Was the reason VERIFIED, and does it still hold at today's versions/prices/scale? |
| "No findings means I did it wrong" | A full lens pass with zero confirmed findings is a valid, valuable verdict - if the log proves the pass happened. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Inventory** | Extract claims, classify evidence + freshness + load | Numbered claim list with priority queue |
| **2. Lens pass** | All 7 lenses, candidates with one-line tests | Numbered findings, none pre-filtered |
| **3. Verify** | Cheapest first, evidence-only verdicts, written log | Every finding CONFIRMED/REFUTED/INCONCLUSIVE |
| **4. Report** | Rank by impact, evidence attached, route follow-ups | Actionable findings or a proven clean pass |
