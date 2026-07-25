---
name: solution-hunter
description: Use when the user wants a continuous, self-driving hunt for solutions to an open-ended problem - subagent generators, combination, adversarial verification with executed evidence, iterating until stopped. Russian triggers - "ищи варианты нон-стоп", "перебирай идеи", "не останавливайся пока не найдёшь". Not for existing materials (critical-review) or declared dead ends (getting-unstuck).
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

## The Round (medium profile: ~8-12 subagents)

Strict wakeup order - never reorder:

0. **Read state first.** Re-read STATE.md + BRIEF.md + any new user messages BEFORE spawning anything. "stop"/"стоп" -> final report (see Autonomous mode). Corrections -> append to BRIEF.md "User corrections".
1. **(Stage 1 only) Schedule the safety wakeup FIRST**, before any subagent. Synthesis may move it, but a round never runs with no next wakeup scheduled.
2. **Phases:**
   - **Generate** - 3-4 `sonnet` subagents, one lens each, rotated from the pool in prompts.md. Input includes the AVOID list: canonical lines of existing + killed ideas with one-line death reasons - never full cards (full cards anchor generators to old phrasing).
   - **Combine** - 1 subagent crossbreeds top live ideas from the index (prompts.md `combinator`). Skip this phase while the index holds fewer than 2 live ideas (typical in round 1) - a combinator with no parents is paid-for noise.
   - **Dedup** - `haiku` checks new ideas against the index canonical lines (prompts.md `dedup`). Paraphrase = duplicate. Index > 200 ideas -> escalate dedup to `sonnet`.
   - **Refute** - 3 critic subagents (model: inherit), lenses hostile-skeptic / pre-mortem / data-contradiction (prompts.md `critic`). Critics EXECUTE the cheapest decisive check themselves within the timebox; too expensive -> INCONCLUSIVE with cost. Never rely on a critic "knowing" critical-review - the rules are inlined in the prompt.
   - **Synthesize** - orchestrator only, in the main session: update LEDGER.md and ideas/ cards, append the round delta to ROUNDS.md, rewrite STATUS.md, append to CANDIDATES.md when an idea passes the BRIEF criterion, carry new facts into the next round's generator prompts. Conflicting critic verdicts are resolved by evidence quality, not majority - a narrower claim backed by an executed number beats a broad verdict; record the resolution in the idea card.
3. **Chat output: events only** - new candidate, dry-streak escalation, auto-pause, plus a one-line progress note every ~10 rounds. The log is ROUNDS.md; the dashboard is STATUS.md. Chat is not a log.

Idea lifecycle: `raw -> combined -> confirmed | refuted | inconclusive`; `confirmed` + passes the BRIEF criterion -> `candidate`. One vocabulary everywhere - critics' verdicts map 1:1 onto index statuses. `inconclusive` keeps its cost-to-verify.

## Anti-stagnation

- **Dry round** = no new (non-paraphrase) idea, OR no CONFIRMED/REFUTED verdict at all (an all-INCONCLUSIVE round is dry too).
- **2 dry in a row** -> force-rotate lenses + run the getting-unstuck protocol against the hunt itself: which hidden assumption narrows the search space?
- **4 dry** -> reformulate the task and ask the user. The question does NOT stop wakeup scheduling - the loop keeps going or auto-pauses by budget rules.

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
2. **Verification yield**: >= 40% of verdicts are CONFIRMED/REFUTED on a checkable demo task. Below that, fix the evidence standard before automating. Same demo hunt also sanity-checks the generators' output: every idea must arrive with a concrete executable test; slogans mean the generator prompt failed.
3. **Dedup**: a planted paraphrase of a refuted idea gets caught by the dedup phase.
4. **Critic divergence**: < 80% identical verdicts across the three critics; otherwise collapse to ONE critic prompted with all three lenses (3x cheaper).

## Red flags

- A candidate whose evidence nobody executed.
- Chat filling with per-round logs (logs belong in ROUNDS.md).
- A Stage 1 round running with no next wakeup scheduled.
- Verdict vocabulary drift (e.g. "verified" instead of CONFIRMED).
- Starting a hunt whose criterion nothing can check, without the hypotheses-only marking.
- Skipping intake budget limits "because the user is in a hurry" - the limits ARE the user's protection.
