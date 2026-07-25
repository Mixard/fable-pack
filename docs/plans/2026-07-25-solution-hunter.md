# solution-hunter Implementation Plan

> **For agentic workers:** Execute this plan task-by-task (fresh subagent per task with review between tasks, or inline with checkpoints). Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the `solution-hunter` skill (continuous solution-search loop) into the fable-workflows plugin, Stage 0 (round-on-demand MVP) fully specified, Stage 1 (autonomous /loop mode) documented behind calibration gates.

**Architecture:** One skill directory with three files: `SKILL.md` (protocol + state machine), `templates.md` (file-state templates), `prompts.md` (subagent prompt contracts with rules inlined). State of a hunt lives in `research/<slug>/` inside the user's project; only the orchestrator writes state files. Spec: `docs/specs/2026-07-25-solution-hunter-design.md`.

**Tech Stack:** Markdown skill for Claude Code plugin marketplace; `scripts/validate.py` for structural validation; git.

## Global Constraints

- Skill text in English; description frontmatter carries Russian triggers verbatim: «ищи варианты нон-стоп», «перебирай идеи», «не останавливайся пока не найдёшь» (spec §9).
- State dir is `research/<slug>/` **inside the project working directory**, never `~/` (spec §0).
- Unified verdict vocabulary everywhere: `raw → combined → confirmed | refuted | inconclusive`; `confirmed` + BRIEF criterion → `candidate` (spec §2).
- Only the orchestrator writes state files; subagents return text (spec §2).
- Every subagent prompt inlines paths + "read BRIEF/LEDGER/ROUNDS first" + verdict rules (spec §3).
- Search-budget defaults: 24 rounds/day, 100 rounds total before explicit "continue?", auto-pause after 24h user silence (spec §1).
- After content changes to `plugins/`, follow the repo `/release` skill (validate → version bump → CHANGELOG → push → cache refresh).
- Every commit must pass `python3 scripts/validate.py` from repo root.

---

### Task 1: Skill skeleton — frontmatter, overview, modes, preconditions, intake

**Files:**
- Create: `plugins/fable-workflows/skills/solution-hunter/SKILL.md`

**Interfaces:**
- Produces: skill name `solution-hunter`; mode names `Stage 0` / `Stage 1`; state dir contract `research/<slug>/`; BRIEF fields consumed by Tasks 2–5 (goal, success criterion + verification method + mode `verified | hypotheses-only`, task constraints, search budget, `assumed` marks).

- [ ] **Step 1: Create the file with this exact content**

````markdown
---
name: solution-hunter
description: Use when the user wants a continuous, self-driving hunt for solutions to an open-ended problem - generate ideas via subagents, combine them, adversarially verify with executed evidence, and keep iterating rounds until the user stops. Russian triggers - "ищи варианты нон-стоп", "перебирай идеи", "не останавливайся пока не найдёшь", "запусти охоту за решением". Not for re-examining existing materials (critical-review) or breaking a declared dead end (getting-unstuck).
---

# Solution Hunter

## Overview

A perpetual research loop: rounds of generate -> combine -> refute -> synthesize, executed by subagents, anchored in files. The loop never declares victory and never quits on its own - it marks candidates, reports events, and keeps hunting until the user stops it or an auto-pause rule fires.

Core principles:

1. **State lives in files, never in session memory.** Chat is for events, not logs.
2. **No candidate without executed evidence.** A verdict nobody tested is an opinion.
3. **Subagents start blank.** Every subagent prompt carries the state paths and the rules inline (see prompts.md).
4. **The graveyard is load-bearing.** Killed ideas stay in the index forever and steer generators away.

## Modes

| Mode | What it is | When |
|------|-----------|------|
| **Stage 0 - round on demand** | User triggers one round (`/solution-hunter round <slug>`), reads STATUS.md | Default. Mandatory until all calibration gates pass |
| **Stage 1 - autonomous loop** | Rounds fire on self-scheduled wakeups (/loop dynamic mode) | Only after Stage 0 gates pass AND the user explicitly asks |

## Preconditions (check at intake)

- State dir is `research/<slug>/` INSIDE the project working directory - never `~/`.
- Write access to `research/**` and WebSearch/WebFetch for subagents must be allowlisted (settings.json), otherwise an unattended round hangs on a permission prompt. If missing, offer to configure it before starting (update-config skill covers the mechanics).

## Intake

`/solution-hunter <task>`. Fill `research/<slug>/BRIEF.md` (template in templates.md) before the first round:

1. **Goal** - one paragraph.
2. **Success criterion** - measurable AND checkable by tools a subagent actually has (WebSearch, Bash calculation, user-provided data). For each evidence type, name the concrete verification method. If nothing available can check the criterion: say so plainly and offer either (a) a proxy criterion that IS checkable, or (b) explicit **hypotheses-only mode** - marked in BRIEF.md and restated in every candidate report. Never start silently unverifiable.
3. **Task constraints** - budget/risk/time of the task itself.
4. **Search budget** - rounds per day (default 24), total rounds before an explicit "continue?" (default 100), auto-pause after 24h of user silence.
5. Unanswered intake questions get a sensible default marked `assumed` - work starts anyway, and every candidate report repeats the assumed list.
````

- [ ] **Step 2: Validate**

Run: `cd /root/fable-skills && python3 scripts/validate.py`
Expected: `OK: 5 plugins, 84 skills, 23 agents`

- [ ] **Step 3: Commit**

```bash
git add plugins/fable-workflows/skills/solution-hunter/SKILL.md
git commit -m "feat(fable-workflows): solution-hunter skeleton (frontmatter, modes, preconditions, intake)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: State-file templates

**Files:**
- Create: `plugins/fable-workflows/skills/solution-hunter/templates.md`

**Interfaces:**
- Consumes: BRIEF field list from Task 1.
- Produces: file names `BRIEF.md`, `STATE.md`, `LEDGER.md`, `ideas/<id>.md`, `ROUNDS.md`, `STATUS.md`, `CANDIDATES.md` and their exact field names — Tasks 3–5 and prompts.md reference these verbatim.

- [ ] **Step 1: Create the file with this exact content**

````markdown
# solution-hunter: state file templates

All state lives in `research/<slug>/` under the project working directory. Only the orchestrator writes these files, atomically, at the end of a phase; subagents return text.

## BRIEF.md

```markdown
# Brief: <task title>
Started: <date>   Slug: <slug>

## Goal
<one paragraph>

## Success criterion (candidate gate)
<measurable AND checkable statement>
Verification methods available to subagents: <WebSearch | Bash calculation | user data | NONE>
Mode: verified | hypotheses-only   # hypotheses-only is restated in every candidate report
Assumed defaults: <list or "none">

## Task constraints
<budget / risk / time of the task itself>

## Search budget
Rounds per day: 24
Total rounds before explicit "continue?": 100
Auto-pause after user silence: 24h

## User corrections (append-only)
- <date>: <correction>
```

## STATE.md — procedure anchor, re-read FIRST on every wakeup

```markdown
# State
Round: 0
Phase: idle | generating | combining | refuting | synthesizing
Next wakeup: <ISO time | none>
Dry rounds streak: 0
Rounds since last user message: 0
Total rounds: 0
Mode: stage0 | stage1
```

## LEDGER.md — compact index, one line per idea

```markdown
# Ledger
| id | canonical statement | status | score |
|----|---------------------|--------|-------|
```

Statuses: `raw | combined | confirmed | refuted | inconclusive | candidate`. Killed ideas stay forever.

## ideas/<id>.md — full card

```markdown
# <id>: <canonical statement>
Lens: <generator lens | "combination of <ids>">
Round born: N

## Hypothesis
<full statement + the concrete test that would verify it>

## Verdicts
### Round N, critic <lens>
Test: <check actually executed> (timebox)
Verdict: CONFIRMED | REFUTED | INCONCLUSIVE (cost to verify: ...)
New fact: <...>
```

## ROUNDS.md — journal, appended every round

```markdown
## Round N (<date>)
Lenses used: <...>
New ideas: <ids | none>   Killed: <ids | none>   Candidates: <ids | none>
New facts:
- <fact>
Dry: yes | no (<reason>)
```

## STATUS.md — dashboard, overwritten every round, half a page max

```markdown
# Status: <task title> — round N
Top candidates: <id: one line each | "none yet">
Best non-candidate lead: <id + status>
Counters: total N | dry streak K | ~X subagent runs spent
Open questions for user: <... | none>
Assumed criteria in effect: <... | none>
```

## CANDIDATES.md — appended when an idea passes the BRIEF criterion

```markdown
## <id>: <canonical statement>   (round N)
Why it passed: <criterion + evidence summary>
Evidence: <numbers / test results / sources>
Assumed: <restate assumed defaults>
```
````

- [ ] **Step 2: Validate**

Run: `cd /root/fable-skills && python3 scripts/validate.py`
Expected: `OK: 5 plugins, 84 skills, 23 agents`

- [ ] **Step 3: Commit**

```bash
git add plugins/fable-workflows/skills/solution-hunter/templates.md
git commit -m "feat(fable-workflows): solution-hunter state templates

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: Subagent prompt contracts

**Files:**
- Create: `plugins/fable-workflows/skills/solution-hunter/prompts.md`

**Interfaces:**
- Consumes: file names from Task 2; verdict vocabulary from Global Constraints.
- Produces: prompt template names `generator`, `combinator`, `critic`, `dedup`; placeholders `{DIR}` (absolute path to `research/<slug>/`), `{ROUND}`, `{LENS}`, `{AVOID_LIST}`, `{IDEAS_BATCH}`, `{INDEX}`, `{NEW}`. Task 4 references these names.

- [ ] **Step 1: Create the file with this exact content**

````markdown
# solution-hunter: subagent prompt contracts

Subagents start with a BLANK context: they see none of the session, no skills, no state. Every prompt below therefore carries paths and rules inline. Placeholders: `{DIR}` = absolute path to `research/<slug>/`.

The verdict rules and red flags below are adapted from the critical-review skill at build time. When critical-review is updated, port changes here deliberately - they do not propagate on their own.

## generator (model: sonnet, 3-4 per round, one lens each)

```text
You are an idea generator in round {ROUND} of a continuous solution hunt.
First read these files: {DIR}/BRIEF.md, {DIR}/LEDGER.md, {DIR}/ROUNDS.md (last 3 rounds are enough).
The goal and success criterion are in BRIEF.md.

Your lens: {LENS}

Do NOT repeat these ideas (canonical statements + why they died):
{AVOID_LIST}

Produce 3-5 NEW ideas. For each return:
- one-line canonical statement
- 3-5 line hypothesis
- the concrete test that would verify it using tools a subagent has (WebSearch, Bash calculation)

An idea without a concrete test is a slogan - do not return it.
Your final text is raw data for the orchestrator, not a message to a human.
```

Lens pool (rotate; pick 3-4 distinct per round):

| Lens | Instruction |
|------|-------------|
| cross-domain | What solves the structurally same problem in unrelated domains? Port the mechanism. |
| inversion | How would you guarantee failure at this goal? Negate each mechanism. |
| web-recon | WebSearch what practitioners actually do today; extract mechanisms, not links. |
| contrarian | Attack the consensus assumption implicit in BRIEF.md; propose ideas that only work if it is false. |
| decomposition | Split the goal into sub-goals; propose ideas that nail one sub-goal completely. |

## combinator (model: sonnet, 1 per round)

```text
Read {DIR}/BRIEF.md and {DIR}/LEDGER.md.
Take the top live ideas (status raw/combined/confirmed) and produce 2-3 crossbreeds:
combinations that inherit the strength of each parent and cover a parent's weakness.
Output format: same as generators (canonical statement + hypothesis + concrete test).
Do not build on refuted ideas unless the refutation fact no longer applies - if so, say why.
Your final text is raw data for the orchestrator.
```

## critic (model: inherit session model; 3 per round, one lens each: hostile-skeptic | pre-mortem | data-contradiction)

```text
You are an adversarial critic (lens: {LENS}) in a solution hunt.
First read {DIR}/BRIEF.md and {DIR}/LEDGER.md.

Ideas to judge:
{IDEAS_BATCH}

Iron law: NO VERDICT WITHOUT EVIDENCE. EXECUTE the cheapest decisive check yourself
(WebSearch, Bash calculation) within a 5-minute timebox per idea. If the decisive check
is too expensive to run now, the verdict is INCONCLUSIVE plus what it would cost.
Rank your checks by cost-to-test, not by comfort.

Lens instructions:
- hostile-skeptic: what does a competitor or harsh reviewer attack first? Attack it with a fact.
- pre-mortem: the idea failed a month later; write the most plausible post-mortem, then check its key premise.
- data-contradiction: what in the LEDGER/ROUNDS facts contradicts this idea? Quote it.

Red flags (process violations):
- softening a verdict because the idea came from our own pipeline
- CONFIRMED without a check you actually executed
- treating a found blog post as evidence without a number or reproducible fact

Per idea return exactly:
Idea: <id + canonical statement>
Test: <check you actually executed> (timebox)
Verdict: CONFIRMED | REFUTED | INCONCLUSIVE (cost to verify: ...)
New fact: <what we learned even if the idea died>
```

## dedup (model: haiku; escalate to sonnet when the index exceeds 200 ideas)

```text
Known ideas index (one canonical line each, including refuted):
{INDEX}

New ideas:
{NEW}

For each new idea decide: NEW, or DUPLICATE of <id>. A paraphrase that changes the
words but not the mechanism is a DUPLICATE. Return one line per new idea:
<canonical statement> -> NEW | DUP <id>
```
````

- [ ] **Step 2: Validate**

Run: `cd /root/fable-skills && python3 scripts/validate.py`
Expected: `OK: 5 plugins, 84 skills, 23 agents`

- [ ] **Step 3: Commit**

```bash
git add plugins/fable-workflows/skills/solution-hunter/prompts.md
git commit -m "feat(fable-workflows): solution-hunter subagent prompt contracts

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: Round protocol + anti-stagnation (append to SKILL.md)

**Files:**
- Modify: `plugins/fable-workflows/skills/solution-hunter/SKILL.md` (append after the Intake section)

**Interfaces:**
- Consumes: template names from Task 2, prompt names/placeholders from Task 3.
- Produces: section headings `## The Round`, `## Anti-stagnation` — Task 5 appends after them.

- [ ] **Step 1: Append this exact content**

````markdown
## The Round (medium profile: ~8-12 subagents)

Strict wakeup order - never reorder:

0. **Read state first.** Re-read STATE.md + BRIEF.md + any new user messages BEFORE spawning anything. "stop"/"стоп" -> final report (see Autonomous mode). Corrections -> append to BRIEF.md "User corrections".
1. **(Stage 1 only) Schedule the safety wakeup FIRST**, before any subagent. Synthesis may move it, but a round never runs with no next wakeup scheduled.
2. **Phases:**
   - **Generate** - 3-4 `sonnet` subagents, one lens each, rotated from the pool in prompts.md. Input includes the AVOID list: canonical lines of existing + killed ideas with one-line death reasons - never full cards (full cards anchor generators to old phrasing).
   - **Combine** - 1 subagent crossbreeds top live ideas from the index (prompts.md `combinator`).
   - **Dedup** - `haiku` checks new ideas against the index canonical lines (prompts.md `dedup`). Paraphrase = duplicate. Index > 200 ideas -> escalate dedup to `sonnet`.
   - **Refute** - 3 critic subagents (model: inherit), lenses hostile-skeptic / pre-mortem / data-contradiction (prompts.md `critic`). Critics EXECUTE the cheapest decisive check themselves within the timebox; too expensive -> INCONCLUSIVE with cost. Never rely on a critic "knowing" critical-review - the rules are inlined in the prompt.
   - **Synthesize** - orchestrator only, in the main session: update LEDGER.md and ideas/ cards, append the round delta to ROUNDS.md, rewrite STATUS.md, carry new facts into the next round's generator prompts.
3. **Chat output: events only** - new candidate, dry-streak escalation, auto-pause, plus a one-line progress note every ~10 rounds. The log is ROUNDS.md; the dashboard is STATUS.md. Chat is not a log.

Idea lifecycle: `raw -> combined -> confirmed | refuted | inconclusive`; `confirmed` + passes the BRIEF criterion -> `candidate`. One vocabulary everywhere - critics' verdicts map 1:1 onto index statuses. `inconclusive` keeps its cost-to-verify.

## Anti-stagnation

- **Dry round** = no new (non-paraphrase) idea, OR no CONFIRMED/REFUTED verdict at all (an all-INCONCLUSIVE round is dry too).
- **2 dry in a row** -> force-rotate lenses + run the getting-unstuck protocol against the hunt itself: which hidden assumption narrows the search space?
- **4 dry** -> reformulate the task and ask the user. The question does NOT stop wakeup scheduling - the loop keeps going or auto-pauses by budget rules.
````

- [ ] **Step 2: Validate + section check**

Run: `cd /root/fable-skills && python3 scripts/validate.py && grep -c '^## ' plugins/fable-workflows/skills/solution-hunter/SKILL.md`
Expected: `OK: 5 plugins, 84 skills, 23 agents` and section count `6`

- [ ] **Step 3: Commit**

```bash
git add plugins/fable-workflows/skills/solution-hunter/SKILL.md
git commit -m "feat(fable-workflows): solution-hunter round protocol and anti-stagnation

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 5: Autonomous mode, recovery, model routing, calibration gates, red flags (append to SKILL.md)

**Files:**
- Modify: `plugins/fable-workflows/skills/solution-hunter/SKILL.md` (append at end)

**Interfaces:**
- Consumes: mode names from Task 1, round order from Task 4.
- Produces: complete SKILL.md; calibration gate numbers consumed by Task 6 smoke test.

- [ ] **Step 1: Append this exact content**

````markdown
## Autonomous mode (Stage 1)

- User commands are processed at the start of the next wakeup; a message sent mid-sleep waits up to the wakeup interval (20-30 min) - an accepted platform limit, state it to the user when Stage 1 starts.
- **"stop"/"стоп"** -> ScheduleWakeup with `stop: true` (kills pending wakeups) + a final summary report over the whole LEDGER.
- **Auto-pause** (pause != stop, nothing is finalized): 24h of user silence, OR the daily round limit, OR the total round limit from BRIEF.md. Any user message resumes the loop.
- Escalations that "ask the user" go to chat AND to STATUS.md open-questions; the loop then continues within budget rules rather than blocking on the answer.

## Recovery

- Every wakeup prompt must be self-sufficient: slug, path `research/<slug>/`, and the instruction "re-read the solution-hunter SKILL.md and STATE.md first". The procedure is anchored in files, so the loop survives context compaction.
- `/solution-hunter resume <slug>` rebuilds a hunt from files after a crashed round or a dead session: read STATE.md, finish or discard the interrupted phase, continue from the recorded round number.

## Model routing and budget

- Generators/combinator: `sonnet`. Mechanics (dedup, file drafting): `haiku`, escalating on the stated thresholds. Critics: inherit the session model. Synthesis: main session.
- Never let a subagent inherit the orchestrator model where a lower tier suffices.
- Before offering Stage 1: measure one full round's cost and wall-clock on a demo hunt. A round longer than ~15 min or costlier than the user accepts -> shrink the profile or slow the cadence first.

## Calibration gates (Stage 0 -> Stage 1)

All four must pass on a demo hunt before autonomous mode is offered:

1. **Cost**: one full round measured (tokens + wall-clock) and accepted by the user.
2. **Verification yield**: >= 40% of verdicts are CONFIRMED/REFUTED on a checkable demo task. Below that, fix the evidence standard before automating.
3. **Dedup**: a planted paraphrase of a refuted idea gets caught by the dedup phase.
4. **Critic divergence**: < 80% identical verdicts across the three critics; otherwise collapse to ONE critic prompted with all three lenses (3x cheaper).

## Red flags

- A candidate whose evidence nobody executed.
- Chat filling with per-round logs (logs belong in ROUNDS.md).
- A Stage 1 round running with no next wakeup scheduled.
- Verdict vocabulary drift (e.g. "verified" instead of CONFIRMED).
- Starting a hunt whose criterion nothing can check, without the hypotheses-only marking.
- Skipping intake budget limits "because the user is in a hurry" - the limits ARE the user's protection.
````

- [ ] **Step 2: Validate + final structure check**

Run: `cd /root/fable-skills && python3 scripts/validate.py && grep -c '^## ' plugins/fable-workflows/skills/solution-hunter/SKILL.md && wc -l plugins/fable-workflows/skills/solution-hunter/SKILL.md`
Expected: `OK: 5 plugins, 84 skills, 23 agents`, section count `11`, SKILL.md in the 180-260 line range (in family with neighbors at 57-244)

- [ ] **Step 3: Commit**

```bash
git add plugins/fable-workflows/skills/solution-hunter/SKILL.md
git commit -m "feat(fable-workflows): solution-hunter autonomous mode, recovery, calibration gates

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 6: Stage 0 smoke test — one real round on a demo hunt

**Files:**
- Create (outside repo, in scratchpad): `research/demo-log-compression/` — BRIEF.md, STATE.md, LEDGER.md, ideas/, ROUNDS.md, STATUS.md
- No repo commit from this task; findings feed Task 7's changelog text and the calibration-gate record.

**Interfaces:**
- Consumes: full SKILL.md protocol (Tasks 1,4,5), templates (Task 2), prompts (Task 3).
- Produces: measured round cost + wall-clock; gate 2-4 results; list of prompt/template defects to fix before release.

- [ ] **Step 1: Intake.** In the scratchpad directory, run the intake per SKILL.md for the demo task: "Find a way to store JSON logs with >= 30% size saving, lossless." Criterion is Bash-checkable (generate a sample log, measure). Fill BRIEF.md from templates.md; Mode: verified; budget defaults.

- [ ] **Step 2: Run one full round manually following `## The Round` exactly**: 3 generators (lenses: web-recon, inversion, decomposition) + 1 combinator + dedup + 3 critics + synthesis. Use the prompts from prompts.md verbatim with placeholders filled.

- [ ] **Step 3: Plant the dedup probe.** Before the round's dedup phase, add to LEDGER.md a refuted idea `d1 | "gzip every log file" | refuted` and ensure one generator output paraphrases it ("compress each log with zlib"). Expected: dedup returns `DUP d1`.

- [ ] **Step 4: Score the gates.**
- Gate 1: record tokens + wall-clock of the round (from /cost or task usage lines). Expected: round <= 15 min; record cost.
- Gate 2: count verdicts; expected >= 40% CONFIRMED/REFUTED (the demo criterion is Bash-checkable, so critics can execute real tests).
- Gate 3: the planted paraphrase is caught (Step 3).
- Gate 4: diff the three critics' verdicts on the same batch; record % identical. If > 80%, note "collapse to single 3-lens critic" as a release-note caveat and edit SKILL.md `## Calibration gates` accordingly before release.

- [ ] **Step 5: Verify state discipline.** Check: every file matches its template; every verdict card has an executed Test line; STATUS.md is half a page; chat received events only. Any deviation -> fix SKILL.md/prompts.md wording now, re-run the failing phase, commit the fix:

```bash
git add plugins/fable-workflows/skills/solution-hunter/
git commit -m "fix(fable-workflows): solution-hunter prompt/template fixes from smoke round

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 7: Release

**Files:**
- Modify: `plugins/fable-workflows/.claude-plugin/plugin.json` (version `0.5.0` -> `0.6.0`)
- Modify: `CHANGELOG.md` (new entry at top)

**Interfaces:**
- Consumes: smoke-test results from Task 6 (cost figure and gate outcomes belong in the changelog entry if notable).

- [ ] **Step 1: Follow the repo `/release` skill** (it owns the exact procedure: validate → bump → changelog → push → local plugin cache refresh). The changelog entry to add under `## [fable-workflows 0.6.0] - <date>`:

```markdown
### Added

- solution-hunter: continuous solution-search loop - subagent generators with rotating lenses, combinator, three adversarial critics (hostile-skeptic / pre-mortem / data-contradiction) executing evidence checks, file-anchored state (BRIEF/STATE/LEDGER/STATUS) in research/<slug>/, anti-stagnation via getting-unstuck, budget guards (rounds/day, total, auto-pause on silence). Stage 0 (round on demand) is the default; Stage 1 (autonomous /loop wakeups) is gated behind four calibration gates (cost, verification yield, dedup on paraphrases, critic divergence). Russian triggers in description ("ищи варианты нон-стоп", "перебирай идеи", "не останавливайся пока не найдёшь").
```

- [ ] **Step 2: Verify the release**

Run: `cd /root/fable-skills && python3 scripts/validate.py && git log --oneline -3`
Expected: `OK: 5 plugins, 84 skills, 23 agents`; release commit on top; branch pushed per /release output.

- [ ] **Step 3: Confirm the skill is live locally** — new session or plugin cache refresh per /release; `solution-hunter` appears in the skills listing.

---

## Self-Review (executed at plan time)

1. **Spec coverage:** §0 preconditions -> Task 1; §1 intake -> Task 1; §2 files -> Task 2; §3 round + prompt contract -> Tasks 3-4; §4 anti-stagnation -> Task 4; §5 autonomous mode -> Task 5; §6 recovery -> Task 5; §7 models/budget -> Task 5; §8 staging/calibration -> Tasks 5-6; §9 packaging -> Task 7. Spec "Тестирование" items: long-run 10+ rounds, stop test, survival test, compaction test are **Stage 1 acceptance** — they require the autonomous mode to be switched on and are deliberately deferred to the Stage 0 -> Stage 1 transition (recorded in Calibration gates); dedup-paraphrase and unverifiable-intake tests are covered by Task 6 Steps 3-4 and Task 1 intake rules.
2. **Placeholder scan:** no TBD/TODO; all content blocks are complete verbatim text.
3. **Type consistency:** file names (BRIEF/STATE/LEDGER/ideas/ROUNDS/STATUS/CANDIDATES), verdict vocabulary (CONFIRMED/REFUTED/INCONCLUSIVE), placeholder names ({DIR},{LENS},{AVOID_LIST},{IDEAS_BATCH},{INDEX},{NEW}), and mode names (Stage 0/Stage 1) are identical across Tasks 1-6.
