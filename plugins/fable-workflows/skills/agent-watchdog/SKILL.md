---
name: agent-watchdog
description: Use when asked to watch, audit, compare, or fix another agent's work given only artifacts - a session ID or transcript, a scheduled/cron run, a PR, branch, CI run, log, or pasted summary. Reconstruct what was asked, verify what happened against evidence, report gaps, fix narrowly only when authorized. Not for a task you just dispatched - that is subagent-driven-development.
---

# Agent Watchdog

## Overview

An unattended agent run - a scheduled job, a background session, a teammate's agent - ends with a summary written by the agent itself. Summaries describe intent, not outcome: "done" may mean done, half-done, or done to the wrong spec. Auditing such a run means reconstructing the original contract from artifacts and judging the work against evidence, not against the agent's own account.

**Core principle:** the user's request is the source of truth. The watched agent's summary is a claim to be verified.

## The Iron Law

```
NO VERDICT ON ANOTHER AGENT'S WORK WITHOUT THE RECONSTRUCTED REQUEST AND INSPECTED EVIDENCE
```

If you have not established what was actually asked AND looked at what actually changed (diffs, logs, test output - not prose), you may not report the work as complete or broken.

## Choose the Mode

Infer the mode from the user's wording; when authority is unclear, default to audit-only and say what you would fix.

- **Watch only:** monitor a session, PR, branch, or CI run until it reaches a terminal state. No edits.
- **Audit:** read the prompt, transcript, diff, tests, CI, and final claims; return a gap report. No edits.
- **Audit and fix:** audit first, then make narrow fixes for clear gaps. No broad rewrites, branch movement, or speculative changes.
- **Compare:** given multiple sessions or agents, judge each against the same original request and reconcile the differences that matter.

## Resolve the Target

1. List every artifact supplied: session ID, transcript path, thread URL, PR, branch, commit, CI run, log, or pasted summary.
2. Resolve it through the most direct source available - host history tools, local transcript files, repo logs, `gh` - preferring raw artifacts over anyone's summary.
3. If the run is still in flight and the ask is to watch, poll at a reasonable interval until it is done, blocked, stale, or waiting on a human.
4. If the artifact cannot be resolved, ask for the missing identifier. Do not audit a paraphrase when the primary source was offered.

## Reconstruct the Contract

Before judging anything, write down the contract the watched agent was working under:

- The original request and any later scope changes.
- Explicit constraints: branch rules, no-edit zones, deadlines, version pins, validation expectations, security/privacy limits.
- Implied acceptance criteria: user-visible behavior, tests, CI, docs, status updates.
- The watched agent's final claims and its stated "could not do" caveats.

## Audit the Evidence

Inspect evidence, not vibes:

- Read the changed files and the relevant unchanged files around them.
- Check `git status`/`git diff` without disturbing unrelated local work.
- Compare commands the agent claimed to run against actual output where available.
- Inspect failed or skipped tests, CI logs, review comments, and error traces.
- For PR work, verify unresolved threads and CI state from the source system.
- For UI work, prefer screenshots or a browser check over prose claims.

Classify each issue found:

| Class | Meaning |
|-------|---------|
| **Gap** | Requested behavior is missing or incomplete |
| **Bug** | The implementation likely fails or regresses behavior |
| **Verification miss** | The work may be right but the evidence is weak or absent |
| **Scope drift** | Unrelated changes were made or a constraint was skipped |
| **No issue** | The concern is handled - cite the evidence |

## Fix Narrowly

Only when the user authorized repair:

1. Fix only gaps backed by clear evidence.
2. Preserve unrelated local changes; never move branches unless that exact operation was requested.
3. Follow existing repo patterns; verify with targeted tests.
4. Re-run the smallest useful validation after each meaningful fix.
5. If a fix needs a product decision, credential, destructive action, or broad rewrite - stop and report the decision instead of guessing.

## Report

Lead with the outcome; keep it scannable. Name exact files, commands, PRs, and thread IDs where they matter.

```md
Status
- Done, blocked, stale, or still running.

Requested
- What the user asked the watched agent to do.

Observed
- What the agent changed, claimed, and actually verified.

Gaps
- Missing behavior, bugs, weak verification, scope drift.

Fixes made
- Files changed and validation run. Omit for audit-only.

Remaining risk
- Anything unverified or waiting on CI/review/human input.
```

**Boundary with subagent-driven-development:** its Task Reviewer gates work you just dispatched - the brief, the report, and a fresh diff are already in hand. This skill covers the other case: a run you did not watch, where the contract itself must be reconstructed from artifacts before any judgment is possible.

## Red Flags - STOP and Return to Evidence

- Writing "the agent completed the task" with the agent's summary as the only source
- Judging the work against your guess of the request instead of the reconstructed contract
- Marking a gap "fixed" without re-running the validation that exposed it
- Fixing beyond the evidence - refactors, style passes, branch moves nobody asked for
- Reporting "tests pass" from the transcript's claim rather than a fresh run
- Auditing a pasted summary when the session, diff, or PR was available

**ALL of these mean: STOP. Reconstruct the contract, inspect the artifact.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The agent's summary is detailed, so it's accurate" | Detail measures effort, not truth. Summaries describe intent; diffs describe outcome. |
| "Re-running the tests is redundant" | A claim in a transcript is not a test run. Fresh output or it did not happen. |
| "The request is obvious from the diff" | Diffs show what was done, not what was asked. Scope drift hides exactly there. |
| "While I'm here, I'll clean this up too" | Unauthorized fixes are scope drift - the same defect you were sent to find. |
| "It's still running, I'll report from partial output" | Partial state misclassifies in-progress work as gaps. Wait for a terminal state or say it is in flight. |
| "The user trusts the other agent, keep it light" | The user asked for a watchdog. Light audits return the summary they already had. |

## Quick Reference

| Phase | Key activity | Success criteria |
|-------|--------------|------------------|
| **Mode** | Infer watch/audit/fix/compare from wording | Authority is explicit; default audit-only |
| **Resolve** | Reach the primary artifact | Raw source, not a paraphrase |
| **Contract** | Reconstruct request, constraints, acceptance | Judging against the ask, not the summary |
| **Audit** | Inspect diffs, logs, tests, CI | Every issue classified with evidence |
| **Fix** | Narrow, authorized, validated | No branch moves, no speculative rewrites |
| **Report** | Status, gaps, fixes, remaining risk | Exact files, commands, IDs named |
