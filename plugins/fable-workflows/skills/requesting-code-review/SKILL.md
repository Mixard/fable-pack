---
name: requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements. Dispatches a code reviewer subagent with a precisely scoped context.
---

# Requesting Code Review

Dispatch a code reviewer subagent to catch issues before they cascade. The reviewer gets precisely crafted context for evaluation — never your session's history. This keeps the reviewer focused on the work product, not your thought process, and preserves your own context for continued work.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing a major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing a complex bug

## How to Request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main, or the recorded task base
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch a general-purpose subagent with the template below**, filling DESCRIPTION (brief summary of what you built), PLAN_OR_REQUIREMENTS (what it should do), BASE_SHA, HEAD_SHA.

**3. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if the reviewer is wrong (with technical reasoning)

## Reviewer Prompt Template

```
You are a Senior Code Reviewer. Review completed work against its plan or
requirements and identify issues before they cascade.

## What Was Implemented
[DESCRIPTION]

## Requirements / Plan
[PLAN_OR_REQUIREMENTS]

## Git Range to Review
Base: [BASE_SHA]  Head: [HEAD_SHA]

    git diff --stat [BASE_SHA]..[HEAD_SHA]
    git diff [BASE_SHA]..[HEAD_SHA]

## Read-Only Review
Your review is read-only on this checkout. Do not mutate the working tree,
the index, HEAD, or branch state in any way. Use `git show`, `git diff`,
`git log` to inspect history. If you need a working copy of another
revision, use a temporary worktree — never move HEAD on this checkout.

## What to Check

Plan alignment: implementation matches plan/requirements? Deviations
justified? All planned functionality present?

Code quality: separation of concerns, error handling, type safety, DRY
without premature abstraction, edge cases.

Architecture: sound design, scalability/performance, security, clean
integration with surrounding code.

Testing: tests verify real behavior (not mocks), edge cases covered,
integration tests where they matter, all passing.

Production readiness: migration strategy if schema changed, backward
compatibility, documentation, no obvious bugs.

## Calibration
Categorize issues by actual severity — not everything is Critical.
Acknowledge what was done well before listing issues. Flag significant
deviations from the plan specifically so the implementer can confirm
whether they were intentional. If you find issues with the plan itself
rather than the implementation, say so.

## Output Format

### Strengths
[What's well done? Be specific.]

### Issues
#### Critical (Must Fix)
[Bugs, security issues, data loss risks, broken functionality]
#### Important (Should Fix)
[Architecture problems, missing features, poor error handling, test gaps]
#### Minor (Nice to Have)
[Code style, optimization opportunities, documentation polish]

For each issue: file:line reference, what's wrong, why it matters, how to
fix (if not obvious).

### Recommendations
[Improvements for code quality, architecture, or process]

### Assessment
Ready to merge? [Yes | No | With fixes]
Reasoning: [1-2 sentence technical assessment]

## Critical Rules
DO: categorize by actual severity; be specific (file:line); explain WHY
each issue matters; acknowledge strengths; give a clear verdict.
DON'T: say "looks good" without checking; mark nitpicks as Critical; give
feedback on code you didn't read; be vague ("improve error handling");
avoid giving a clear verdict.
```

## Example

```
[Just completed Task 2: Add verification function]

Dispatch reviewer:
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types
  PLAN_OR_REQUIREMENTS: Task 2 from docs/plans/deployment-plan.md
  BASE_SHA: a7981ec   HEAD_SHA: 3df7661

Reviewer returns:
  Strengths: clean architecture, real tests
  Issues: Important - missing progress indicators
          Minor - magic number (100) for reporting interval
  Assessment: Ready to proceed

[Fix progress indicators, continue to Task 3]
```

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback

**If the reviewer is wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification
