---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs. Requires running verification commands and confirming output before making any success claims; evidence before assertions always.
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

Claims about *facts in a deliverable* (a client's price, phone, code) are verified by a different gate — the fact-guard skill; this skill covers claims about work status.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Define Done Before the Work

For multi-part or long autonomous work (not a one-line edit), write the acceptance checks **before** implementing: one observable outcome per independently required part of the request, each with the command that decides it and the output that means success. Checks written after the work tend to measure what was built, not what was asked.

A check is only evidence if it can fail:
- **Absence checks need a positive control.** "grep finds no X" proves nothing until the same grep finds X where X exists (wrong path, wrong pattern, and empty input all return nothing).
- **Measure numbers, don't copy them.** A figure supplied by the plan, the user, or an agent is not its own proof; re-derive it.
- **Require exit code AND a success-only marker** - a script that prints "passed" before crashing, or exits 0 on a skipped suite, fools either one alone.

**An impossible requirement is never silently dropped.** Mark it unmet with the reason and surface it as a handoff to the user. Abandoned is not done: the report is not "complete" while any required outcome is unmet, abandoned, or waiting on an owner decision.

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist against the original request | Tests passing, plan ticked off |
| Nothing left / no matches | Same check finds a known positive | Empty output |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence != evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter != compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion != excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

## Key Patterns

**Tests:**
```
GOOD: [Run test command] [See: 34/34 pass] "All tests pass"
BAD:  "Should pass now" / "Looks correct"
```

**Regression tests (TDD red-green):**
```
GOOD: Write -> Run (pass) -> Revert fix -> Run (MUST FAIL) -> Restore -> Run (pass)
BAD:  "I've written a regression test" (without red-green verification)
```

**Build:**
```
GOOD: [Run build] [See: exit 0] "Build passes"
BAD:  "Linter passed" (linter doesn't check compilation)
```

**Requirements:**
```
GOOD: Re-read the original request + later amendments (not only the plan) -> Checklist
      -> Verify each -> Report met / unmet / abandoned counts, naming every unmet item
BAD:  "Tests pass, phase complete" / quietly omitting the part that didn't work
```

**Agent delegation:**
```
GOOD: Agent reports success -> Check VCS diff -> Verify changes -> Report actual state
BAD:  Trust agent report
```

## Why This Matters

Unverified claims break trust, ship undefined functions that crash, ship incomplete features, and waste time on false completion followed by redirects and rework. One "Done!" that wasn't costs more credibility than ten honest "still failing" reports.

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.
