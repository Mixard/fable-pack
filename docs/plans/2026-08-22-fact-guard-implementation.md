# fact-guard + fable-guard secret patterns — Implementation Plan

> **For agentic workers:** Execute this plan task-by-task (fresh subagent per task with review between tasks, or inline with checkpoints). Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `fable-workflows:fact-guard` (a skill that stops invented client facts from reaching deliverables) and extend `fable-guard` with four secret patterns, released as fable-workflows 1.3.0 and fable-guard 0.5.0.

**Architecture:** One new single-file skill in `plugins/fable-workflows/skills/fact-guard/SKILL.md` written in the pack's hard-rule format (Iron Law, gate, red flags, rationalization table); two one-line cross-references in sibling skills; four regexes appended to `SECRET_PATTERNS` in `plugins/fable-guard/hooks/guard.py` with paired tests in `scripts/test_guard.py`; release bookkeeping per the `release` skill.

**Tech Stack:** Markdown skills, Python 3 (stdlib `re`, `json`) for the hook, `scripts/validate.py` and `scripts/test_guard.py` as the test harness. No new dependencies.

Spec: `docs/specs/2026-08-22-fact-guard-design.md`.

## Global Constraints

- Skill frontmatter: `name` must equal the directory name (`fact-guard`); `description` is ONE line, ≤ 400 chars (validate.py enforces both).
- Skill body in English, Russian trigger phrases allowed only inside `description` (pattern from `critical-review`).
- `test_guard.py` contract: `check_guard(desc, payload, expect_block)` — a blocked call prints JSON to stdout, an allowed call prints nothing; exit code is always 0.
- Stripe **test** keys (`sk_test_…`) must NOT be blocked. Connection strings **without** a password must NOT be blocked. Two-segment `eyJ…` strings must NOT be blocked.
- Versions: `plugins/fable-workflows/.claude-plugin/plugin.json` 1.2.0 → 1.3.0; `plugins/fable-guard/.claude-plugin/plugin.json` 0.4.0 → 0.5.0. No other plugin changes.
- README badge `skills-86` → `skills-87`; section header `### fable-workflows — 19 skills` → `20 skills`; skill list gets `fact-guard` appended.
- Conventional commits; every commit ends with `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.
- Work on branch `fact-guard` off `main`; merge/push only in Task 4.

---

### Task 1: Four new secret patterns in fable-guard (TDD)

**Files:**
- Modify: `plugins/fable-guard/hooks/guard.py:13-24` (the `SECRET_PATTERNS` list)
- Test: `scripts/test_guard.py` (append after the existing `# --- guard.py: secrets ---` block)

**Interfaces:**
- Consumes: `check_guard(desc, payload, expect_block)` and `bash(cmd)` helpers already defined in `scripts/test_guard.py`.
- Produces: nothing consumed by later tasks; Task 4 reads the new labels for the CHANGELOG.

- [ ] **Step 1: Create the branch**

```bash
cd /root/fable-skills && git checkout -b fact-guard main
```

- [ ] **Step 2: Write the failing tests**

Append to `scripts/test_guard.py` directly after the last existing `check_guard(... secrets ...)` call (before the `DANGEROUS_BASH`/other sections — locate with `grep -n "secrets ---" scripts/test_guard.py`):

```python
# --- guard.py: secrets added in fable-guard 0.5.0 ---
check_guard("Telegram bot token", bash("export BOT_TOKEN=1234567890:AAHf3kZ9xQwErTyUiOpAsDfGhJkLzXcVbNm"), True)
check_guard("Telegram-like but short secret part is allowed", bash("echo 1234567890:AAHf3kZ9xQ"), False)
check_guard("Stripe live secret key", bash("export STRIPE_SECRET_KEY=sk_live_Ab12Cd34Ef56Gh78Ij90"), True)
check_guard("Stripe restricted live key in Write",
            {"tool_name": "Write", "tool_input": {"content": "key = 'rk_live_Ab12Cd34Ef56Gh78Ij90'"}}, True)
check_guard("Stripe test key is allowed", bash("export STRIPE_SECRET_KEY=sk_test_Ab12Cd34Ef56Gh78Ij90"), False)
check_guard("JWT three segments in Edit",
            {"tool_name": "Edit", "tool_input": {"new_string": "token=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"}}, True)
check_guard("two-segment eyJ string is allowed", bash("echo eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0"), False)
check_guard("postgres URL with password", bash("export DATABASE_URL=postgres://app:S3cretPass@db.internal:5432/app"), True)
check_guard("mongodb+srv URL with password in Write",
            {"tool_name": "Write", "tool_input": {"content": "uri: mongodb+srv://admin:hunter2@cluster0.example.net/db"}}, True)
check_guard("postgres URL without password is allowed", bash("psql postgresql://app@db.internal:5432/app"), False)
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `python3 scripts/test_guard.py 2>&1 | grep -E "FAIL|passed|failed" | head -20`
Expected: the 6 `expect_block=True` cases above print `FAIL guard: …` (hook currently allows them); the 4 `False` cases print `OK`; the script exits non-zero.

- [ ] **Step 4: Add the patterns**

In `plugins/fable-guard/hooks/guard.py`, replace the last entry of `SECRET_PATTERNS` (the private-key line) so the list ends like this:

```python
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----"), "private key material"),
    (re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b"), "Telegram bot token"),
    (re.compile(r"\b(?:sk|rk)_live_[A-Za-z0-9]{20,}"), "Stripe live key"),
    (re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"), "JWT"),
    (
        re.compile(r"\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqp)://[^\s/:@]+:[^\s@]+@"),
        "connection string with embedded password",
    ),
]
```

- [ ] **Step 5: Run the full hook suite to verify it passes**

Run: `python3 scripts/test_guard.py; echo rc=$?`
Expected: every line `OK`, final `rc=0`, and the existing 27+ cases still pass (no regressions on `sk-` / `ghp_` / AWS etc.).

- [ ] **Step 6: Sweep the server's repos for false positives (spec criterion 4)**

```bash
for d in /root/geo_rpg /root/Tonya_glam /root/tonya_club /root/telegram /root/tg_persons /root/ads-hub /root/automation /root/genlab /root/social_midia_mixard /root/landing-starter /root/new_web_site /root/fable-skills /root/FIXMATE_PROJECT/meta-ads /root/FIXMATE_PROJECT/content /root/FIXMATE_PROJECT/Fix-mate-website /root/FIXMATE_PROJECT/AuraKey-Yelp /root/FIXMATE_PROJECT/DCWP-NYC; do
  echo "== $d"
  git -C "$d" grep -n -E '\b[0-9]{8,10}:[A-Za-z0-9_-]{35}\b|\b(sk|rk)_live_[A-Za-z0-9]{20,}|\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b|\b(postgres(ql)?|mysql|mongodb(\+srv)?|redis|amqp)://[^[:space:]/:@]+:[^[:space:]@]+@' -- . ':!scripts/test_guard.py' ':!docs/plans/2026-08-22-fact-guard-implementation.md' ':!docs/specs/2026-08-22-fact-guard-design.md' | head -5
done
```

Expected: no hits except fixtures that are explicitly test data. Any real hit is reported to the user as a leaked secret (file path only, never the value) — it is not a reason to weaken the pattern.

- [ ] **Step 7: Commit**

```bash
git add plugins/fable-guard/hooks/guard.py scripts/test_guard.py
git commit -m "feat(fable-guard): block Telegram bot tokens, Stripe live keys, JWTs, connection strings with passwords

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: The `fact-guard` skill

**Files:**
- Create: `plugins/fable-workflows/skills/fact-guard/SKILL.md`

**Interfaces:**
- Consumes: nothing.
- Produces: skill name `fact-guard`, ledger filename convention `known-fabrications.md` (glob `*known-fabrications*`), facts-file convention `docs/facts.yaml` — Task 3 references these names verbatim.

- [ ] **Step 1: Write the skill file with exactly this content**

```markdown
---
name: fact-guard
description: Use when a deliverable carries facts about the client or their domain - names, people, phones, addresses, emails, handles, domains, prices, codes, IDs, licenses, dates, legal thresholds, quotes - in drafts, emails, landing pages, reports, product cards, ad copy, configs. Also when the owner says "откуда ты это взял", "это неправильно", "такого нет", "не выдумывай". Placeholder instead of a plausible guess, project facts file over memory, fabrications ledger checked before delivery.
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
```

- [ ] **Step 2: Validate the pack**

Run: `python3 scripts/validate.py`
Expected: `OK`. If it reports the description length, shorten the description without removing the Russian triggers (they are the router hooks).

- [ ] **Step 3: Commit**

```bash
git add plugins/fable-workflows/skills/fact-guard/SKILL.md
git commit -m "feat(fable-workflows): add fact-guard - placeholder over invented client facts, fabrications ledger, delivery check

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: Cross-references and behavioral acceptance of the skill

**Files:**
- Modify: `plugins/fable-workflows/skills/writing-plans/SKILL.md` — the `## No Placeholders` section (around line 130)
- Modify: `plugins/fable-workflows/skills/verification-before-completion/SKILL.md` — the `## Overview` section (lines 7-14)

**Interfaces:**
- Consumes: skill name `fact-guard`, ledger glob `*known-fabrications*` from Task 2.

- [ ] **Step 1: Add the two cross-reference lines**

In `writing-plans/SKILL.md`, append one line at the end of the `## No Placeholders` section (after its last bullet):

```markdown

Placeholders for *client facts* (prices, contacts, codes) are the one exception and are mandatory, not forbidden — see the fact-guard skill.
```

In `verification-before-completion/SKILL.md`, append one line to the end of `## Overview` (after the "Violating the letter…" line):

```markdown

Claims about *facts in a deliverable* (a client's price, phone, code) are verified by a different gate — the fact-guard skill; this skill covers claims about work status.
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate.py`
Expected: `OK`.

- [ ] **Step 3: Acceptance run A — blocklist FAIL on FIXMATE (spec criterion 2)**

Dispatch a `sonnet` subagent with this prompt (paths are real; do not modify anything under `/root/FIXMATE_PROJECT`):

```
Read /root/fable-skills/plugins/fable-workflows/skills/fact-guard/SKILL.md and follow it.
Project: /root/FIXMATE_PROJECT/DCWP-NYC. Deliverable to check (write it to your scratchpad, not into the project):

"Dear Trevor Wilson, FixMate Locksmith (vendor code VS00107380, DCWP #2131003-DCWP) would like to be considered for upcoming lock work at your properties. Call (929) 928-5241."

Run the delivery check from Rule 3. Return only: the verdict line, the blocklist hits (row numbers and the matched strings), the NEEDS-SOURCE list, and which file you used as the ledger and which as the facts file.
```

Expected: verdict `FAIL`; hits on "Trevor Wilson" (row 14) and `VS00107380` (row 2); ledger = `procurement-known-fabrications.md` (found via `*known-fabrications*`, not a newly created file); facts file = `procurement-facts.yaml` and/or `../shared/brand-facts.yaml`. If the subagent creates `docs/known-fabrications.md` in that project, the skill's "reuse it, never create a second one" wording failed — tighten Rule 3 and re-run.

- [ ] **Step 4: Acceptance run B — placeholder on geo_rpg (spec criterion 3)**

Dispatch a `sonnet` subagent (read-only on `/root/geo_rpg`):

```
Read /root/fable-skills/plugins/fable-workflows/skills/fact-guard/SKILL.md and follow it.
Project: /root/geo_rpg. Task: write a 5-line store description for the game that mentions the monthly subscription price and the support email. Write it to your scratchpad only.
Return the text and the «Что нужно от вас» list.
```

Expected: no invented price or email; both appear as placeholders in the text and in the list; the subagent reports that no facts file was found and proposes `docs/facts.yaml` (proposal only — it must not create the file in a read-only run).

- [ ] **Step 5: Record the two runs**

Append a section `## Acceptance runs 2026-08-22` to `docs/specs/2026-08-22-fact-guard-design.md` with the two verdict lines and any wording change they forced.

- [ ] **Step 6: Commit**

```bash
git add plugins/fable-workflows/skills/writing-plans/SKILL.md plugins/fable-workflows/skills/verification-before-completion/SKILL.md docs/specs/2026-08-22-fact-guard-design.md
git commit -m "docs(fable-workflows): cross-link fact-guard from writing-plans and verification-before-completion; record acceptance runs

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: Release fable-workflows 1.3.0 and fable-guard 0.5.0

**Files:**
- Modify: `plugins/fable-workflows/.claude-plugin/plugin.json` (`"version": "1.2.0"` → `"1.3.0"`)
- Modify: `plugins/fable-guard/.claude-plugin/plugin.json` (`"version": "0.4.0"` → `"0.5.0"`)
- Modify: `CHANGELOG.md` (two new sections at the top)
- Modify: `README.md` — badge line 8, "What's new" table (after line 22), `### fable-workflows — 19 skills` header and list (lines 105-109), fable-guard section (line 152+)
- Modify: `ATTRIBUTIONS.md` (one new table row)

**Interfaces:**
- Consumes: labels from Task 1, skill name from Task 2.

- [ ] **Step 1: Bump versions**

```bash
sed -i 's/"version": "1.2.0"/"version": "1.3.0"/' plugins/fable-workflows/.claude-plugin/plugin.json
sed -i 's/"version": "0.4.0"/"version": "0.5.0"/' plugins/fable-guard/.claude-plugin/plugin.json
grep -n '"version"' plugins/fable-workflows/.claude-plugin/plugin.json plugins/fable-guard/.claude-plugin/plugin.json
```

Expected: `1.3.0` and `0.5.0`.

- [ ] **Step 2: CHANGELOG — insert directly under the `# Changelog` intro paragraph, above `## [fable-workflows 1.2.0]`**

```markdown
## [fable-workflows 1.3.0] - 2026-08-22

### Added

- fact-guard: stops invented client facts (names, prices, codes, contacts) from reaching deliverables. Three rules — placeholder instead of a plausible guess (collected into a «Что нужно от вас» list), the project's facts file beats memory (proposes `docs/facts.yaml` at the first real question), and a `known-fabrications.md` ledger with a BLOCKLIST → TRACE → VERDICT check before delivery (inline up to ~2 pages, subagent beyond). Generalizes the ledger + guard pattern one project had built by hand after 15 hallucinated facts; the same failure class was documented in two more projects. The only idea adopted from a triage of nick-vels/skills (autopilot) — its rule "a fact about the user is never invented" — after a critical review refuted the other six candidates (requirements manifest, context handoff, SDD upgrades, secrets skill, Unity knowledge, acceptance protocol) for lack of any documented failure they would fix.

### Changed

- writing-plans, verification-before-completion: one cross-reference line each to fact-guard (client-fact placeholders are mandatory; fact claims are a different gate from status claims).

## [fable-guard 0.5.0] - 2026-08-22

### Added

- Four secret patterns: Telegram bot token, Stripe live key (`sk_live_`/`rk_live_`; test keys deliberately allowed), JWT (three base64url segments), connection string with an embedded password (postgres/mysql/mongodb/redis/amqp). Ten new test cases, paired positive/negative per pattern.

```

- [ ] **Step 3: README**

Badge (line 8): `skills-86` → `skills-87` in both the `src` and `alt` attributes.

"What's new" table — insert as the first data row:

```markdown
| 2026-08-22 | fable-workflows 1.3.0, fable-guard 0.5.0 | fact-guard — placeholder over invented client facts, facts file over memory, fabrications ledger checked before delivery; guard hook gains Telegram/Stripe-live/JWT/connection-string patterns |
```

Section header: `### fable-workflows — 19 skills` → `### fable-workflows — 20 skills`; in the comma list on line 109 append `, fact-guard` after `kb-hygiene`.

fable-guard section (line 152+): where the secret patterns are described, mention the four new ones in one clause (grep the section for "secret" and extend that sentence; do not add a paragraph).

Then: `grep -n "fact-guard" README.md` — expected ≥ 3 hits (table row, skill list, optional prose).

- [ ] **Step 4: ATTRIBUTIONS — add a row to the table**

```markdown
| [nick-vels/skills](https://github.com/nick-vels/skills) (autopilot) | MIT | fable-workflows: one rule adapted into fact-guard ("a fact about the user is never invented — visible placeholder"); fabrications-ledger format comes from an in-house project. Skipped after critical review: requirements manifest + blind acceptance, context ceiling/handoff, long-lived reviewers, secrets redaction (already in fable-guard), dashboard/state.js, polish loop — no documented failure in our projects that they would fix |
```

- [ ] **Step 5: Validate everything**

```bash
python3 scripts/validate.py && python3 scripts/test_guard.py | tail -3
```

Expected: `OK` and all guard cases `OK`.

- [ ] **Step 6: Commit, merge, push, verify CI**

```bash
git add -A
git commit -m "feat(fable-workflows,fable-guard): release 1.3.0 / 0.5.0 - fact-guard skill, four secret patterns

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
git checkout main && git merge --ff-only fact-guard && git push origin main
gh run list --limit 1
```

Expected: the `validate` workflow shows `success` (re-run `gh run list --limit 1` after ~1 minute if `in_progress`).

- [ ] **Step 7: Refresh the local plugin cache**

```bash
claude plugin update fable-workflows@fable-pack
claude plugin update fable-guard@fable-pack
```

Expected: both report the new versions; tell the user a session restart is needed for the skill to load.

---

## Self-review against the spec

- Spec §Part 1, rules 1–3, triggers, out-of-scope, subagent variant → Task 2 (full text). Cross-references → Task 3 step 1.
- Spec §Part 2, four patterns with the stated false-positive decisions, paired tests → Task 1.
- Spec §Versions: 1.3.0 / 0.5.0, CHANGELOG, README, validate.py → Task 4.
- Spec acceptance criteria: 1 → Task 1 step 5 + Task 4 step 5; 2 → Task 3 step 3; 3 → Task 3 step 4; 4 → Task 1 step 6.
- Names used consistently: `fact-guard`, `known-fabrications.md` / glob `*known-fabrications*`, `docs/facts.yaml`, labels "Telegram bot token" / "Stripe live key" / "JWT" / "connection string with embedded password".
- No placeholders: every code/markdown step carries its full content.
