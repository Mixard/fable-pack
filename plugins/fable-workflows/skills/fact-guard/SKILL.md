---
name: fact-guard
description: Use when deliverable embeds client facts: names, phones, addresses, emails, domains, prices, codes, IDs, dates, quotes in drafts, landing pages, reports, configs. Also when owner says "откуда ты это взял", "это неправильно", "такого нет", "не выдумывай". Placeholder over guess; facts file over memory; ledger checked before delivery.
---

# Fact Guard

## Overview

A plausible invented fact is worse than a visible gap. The gap gets filled by the owner in one reply; the invented phone number, vendor code, or president's name ships, gets quoted, and costs a re-draft, a lost bid, or a client's trust. The same failure was documented in three unrelated projects on one server: a non-existent fax number, a misremembered Instagram handle, a made-up executive name, legal dates copied from the wrong regime.

**Core principle:** a fact about the client is either traced to a named source or shown as a placeholder. There is no third state.

**Boundary:** this skill is about facts *about the client and their world*. Facts about the outside world (library versions, API shapes) are docs-first and freshness-sweep; claims about work status ("tests pass") are verification-before-completion.

## The Iron Law

```
NO CLIENT FACT WITHOUT A SOURCE OR A PLACEHOLDER. NO DELIVERY WITHOUT THE LEDGER CHECK.
```

## When to Use

- Drafting anything an outsider will read: emails, landing copy, ad text, product cards, proposals, reports, government or marketplace submissions.
- Writing config or code that embeds client data: prices, SKUs, contact blocks, license numbers, addresses, handles.
- The owner challenges a fact ("where did that come from?") — that is a ledger event, not just a correction.
- Resuming a project you last touched long ago: memory of client facts decays faster than memory of code.

## Rule 1 — Placeholder, never a guess

When you do not have the value from a source you can name, write a visible placeholder in the owner's language, stating what is needed and who supplies it:

```
[ЦЕНА ПОДПИСКИ — уточнить у владельца]
[PHONE — from brand-facts.yaml, field missing]
```

Collect every placeholder into one list, **«Что нужно от вас»**, at the end of the deliverable or the session report. A placeholder hidden mid-text is a gap nobody fills; a list is a to-do.

Never "fill in something reasonable for now." A draft with `[ЦЕНА — впиши]` is a draft; a draft with `$9.99/мес` you invented is a published mistake waiting for its moment.

## Rule 2 — The project's facts file beats memory

Before writing any client fact, find the project's source of truth:

1. Look for it by name: `shared/brand-facts.yaml`, `docs/facts.yaml`, `*facts*.yaml`, `*static*.md`, `*-facts.md`, and whatever CLAUDE.md names as the canonical facts file.
2. If it exists: every client fact you write is copied from it (or from a document it points to). If the fact is not in it, Rule 1 applies — placeholder, and suggest adding the field once the owner answers.
3. If it does not exist: the first time you must ask the owner for a fact, propose creating `docs/facts.yaml` with that answer as its first entry. One file, flat keys, a `source:` per value. Do not create it speculatively before the first real fact.

A value in your context from an earlier session, a screenshot you half-remember, or "it was probably the same as the other project" is not a source.

## Rule 3 — The fabrications ledger and the delivery check

**The ledger.** `docs/known-fabrications.md` (or an existing file matching `*known-fabrications*` — reuse it, never create a second one). Format, one row per fact that was ever invented or wrong in this project:

```markdown
| # | Fabricated / wrong value | Where it came from | Correct value | Source |
|---|---|---|---|---|
| 1 | **"Trevor Wilson"** as company president | stale bundle row | **Horace Henry** | company site, verified 2026-06-11 |
```

The left column is a literal blocklist: these strings may appear in project files only inside an explicit "do not use / refuted" warning, never as a live fact.

**Ledger events.** A fact is added **in the same turn** it is caught — by the owner, by a reviewer, by your own check. "I'll record it later" is how the same fabrication returns next month with a fresh-context agent who never saw the correction.

**The delivery check** — run before handing over any deliverable that carries client facts:

```
1. BLOCKLIST: grep -F -f <(left column of the ledger) <deliverable>
   Any hit outside a "do not use" warning = FAIL. Fix, re-check.
2. TRACE: for every name, number, code, contact, date, quote in the deliverable:
   traced to the facts file (or a document it names)  -> ok
   placeholder                                         -> ok, goes to «Что нужно от вас»
   neither                                             -> NEEDS-SOURCE: replace with a placeholder or find the source
3. VERDICT: PASS / NEEDS-SOURCE / FAIL stated in one line with counts.
   When uncertain, block — a re-draft is cheaper than a wrong fact in the client's inbox.
```

Inline for deliverables up to ~2 pages. Longer, or when the deliverable is one of many in a batch: dispatch a `haiku`/`sonnet` subagent with three paths — the deliverable, the ledger, the facts file — and the three-step check above verbatim; it returns the verdict line plus the list of NEEDS-SOURCE items, nothing else.

## Red Flags — STOP

- A number, name, or code in your draft that you cannot point to a file for.
- "Something like this" / "for example, $49" / "a typical phone format" in a client-facing draft.
- Correcting a fact the owner flagged without adding a ledger row.
- A second facts file or a second ledger appearing in the project.
- Skipping the delivery check because "it's only an internal memo" — internal memos get pasted into external emails.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The owner will review it anyway" | Owners skim their own facts; they read for tone, not for a transposed digit. The guard exists because they did not catch it last time. |
| "It was correct in the last session" | Your recollection is not a source. The facts file is. |
| "A placeholder looks unprofessional" | An invented price in a client proposal looks far worse, and you will not be there to see it. |
| "It's obviously the same as the other project" | Two projects, two fact sets. The shared phone number was the bug. |
| "I'll add it to the ledger after the fix" | The fix is one turn; the ledger row is the only part that protects the next agent. Same turn. |
| "The ledger is empty, the check is pointless" | The check has two steps; TRACE works with an empty blocklist. The ledger is empty until the first catch, and the first catch is the one you are about to make. |

## Quick Reference

| Situation | Action |
|-----------|--------|
| Need a client fact you don't have | Placeholder `[…— уточнить у владельца]`, add to «Что нужно от вас» |
| Fact exists somewhere | Copy from the facts file; if absent there, placeholder + propose the field |
| Owner says "that's wrong" | Fix + ledger row, same turn |
| About to deliver | BLOCKLIST → TRACE → VERDICT; block when unsure |
| Deliverable > 2 pages or a batch | Subagent with deliverable, ledger, facts file; returns verdict + NEEDS-SOURCE list |
