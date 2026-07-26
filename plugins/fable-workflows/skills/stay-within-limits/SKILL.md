---
name: stay-within-limits
description: Use when long-running or parallel agent work must respect 5-hour and weekly usage limits - checking usage between waves of subagents, pausing near the cap with self-sufficient wake prompts, and resuming only when the window is clear. Pairs with any /loop-style autonomous run, including solution-hunter Stage 1.
---

# Stay Within Limits

## Overview

Long autonomous runs die in two ways: they burn through the usage window mid-task and stall with work half-done, or they "wait it out" on wall-clock guesses and resume into a window that never actually cleared. Both are avoidable with one discipline: measure usage between waves, pause on a threshold, and resume only on re-measured evidence.

**Core principle:** the usage window is state to be read, not estimated. Elapsed time is not evidence that a window cleared.

## The Iron Law

```
NO NEW WAVE AT OR ABOVE 95% OF AN ACTIVE 5-HOUR OR WEEKLY LIMIT
```

Check usage before launching substantial work and between waves. At or above 95% of either window: stop launching, schedule a resume, and re-check on wake before continuing.

## Core Loop

1. Run a bounded wave of work. Default to at most 3 parallel subagents unless the user or host sets a different throttle.
2. Wait for the wave to finish. Do not interrupt in-flight subagents to save budget - that usually loses paid-for work.
3. Check current 5-hour and weekly usage with the host's usage tool.
4. At or above 95% of either window: stop launching, schedule a self-contained resume for when the window should clear.
5. On wake, re-check the real window before continuing. A new active-block start timestamp is stronger evidence than "enough time passed".

## Usage Signals

Prefer a first-party host usage tool when one exists. In Claude Code a community tool covers the gap:

```sh
npx -y ccusage@latest blocks --active --json
```

Read the active block's start timestamp, current usage, and time remaining from the JSON. `ccusage` is community-maintained and its flags and JSON shape can drift - if the call fails or the shape surprises you, run `npx ccusage@latest --help` and adapt before concluding usage cannot be measured. If the tool reports cost instead of a percentage, convert through the account's known limit; treat any earlier dollar-threshold guardrail as user configuration, not a universal rule. The default stop rule stays 95%.

## Pausing and Resuming

Pause is not stop: nothing is finalized, state stays on disk, and the run continues when the window clears.

When a wake/resume tool is available, schedule the next check for `min(3600, secondsUntilWindowClears)` and chain wakeups for longer waits - each wake re-checks usage, reschedules if still over threshold, and continues only when safely below it.

Every wake prompt must be self-sufficient. Include:

- The remaining plan and next verification steps.
- The check-then-reschedule rule, the 95% threshold, and the wave throttle.
- The exact usage command or host tool to run.
- The previous block/window identifier for comparison.
- The next wave's handoff packets (scope, verification commands, stop conditions) if delegation resumes.

A wake prompt that relies on conversation momentum instead of carrying its own state is a resume that fails after context compaction.

**Boundary with solution-hunter:** solution-hunter Stage 1 already owns its loop mechanics - self-sufficient wakeups, auto-pause rules, file-anchored state. When running it, do not build a second pause convention: add the usage check to the start-of-round state read and treat "window at 95%" as one more auto-pause trigger, using its existing pause/resume vocabulary.

## Choosing the Wait Mechanism

- **Wake/resume tool** when instructions must travel with the future resume.
- **Background sleep or watcher** for fixed timers a process can observe directly.
- **Cron/recurring schedules** only for recurring fresh-session work.

Never short-interval-poll for things the host will notify you about (subagent completion, background tasks). For budget pauses, losing the prompt cache after a long sleep is acceptable - preserving the limit matters more.

## Reporting

On pause, tell the user: which window is over threshold, the observed usage number, when the next check is scheduled, and what work remains. Keep enough state in the wake prompt that the next turn resumes without the conversation.

## Red Flags - STOP and Re-check

- Launching a wave without having measured usage this cycle
- Resuming after a sleep without re-reading the actual window
- "The window must have cleared by now" - wall-clock reasoning in place of a measurement
- Killing in-flight subagents to save budget
- A wake prompt that says "continue where we left off" with no plan, threshold, or command inside
- Polling usage every minute while a wave is still running

**ALL of these mean: STOP. Return to the Core Loop.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "We're probably fine, the last check was recent" | Waves are bursty. One parallel wave can cross 95% alone. Check between waves. |
| "Checking usage wastes a call" | One JSON read costs nothing. Hitting the cap mid-wave strands half-finished work. |
| "Enough hours passed, the window cleared" | Windows are rolling. Compare block timestamps, not elapsed time. |
| "I'll finish this one big wave first" | A wave launched at 94% lands at over-limit. Throttle before, not after. |
| "The wake prompt can be short, context survives" | Context gets compacted. A non-self-sufficient wake prompt is a dead resume. |
| "Cancel the running agents, we're near the cap" | Their tokens are already spent. Cancelling converts spend into zero output. |

## Quick Reference

| Step | Action | Success criteria |
|------|--------|------------------|
| Before work | Measure both windows | Numbers, not guesses |
| Between waves | Re-measure; compare to 95% | Launch only below threshold |
| At threshold | Pause, schedule resume with full state | Wake prompt is self-sufficient |
| On wake | Re-measure before continuing | New block timestamp or clear headroom |
| Inside solution-hunter | Usage check joins the round's state read | One pause convention, not two |
