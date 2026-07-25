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
Phase: idle | generating | combining | deduping | refuting | synthesizing
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
score = the best executed measurement backing the idea (number + unit), `-` if none yet.

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
