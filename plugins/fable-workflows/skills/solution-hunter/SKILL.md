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
