---
name: subagent-driven-development
description: Use when executing an implementation plan with mostly independent tasks in the current session and subagent dispatch is available. A fresh subagent implements each task, a reviewer gates each task, and a whole-branch review closes the work.
---

# Subagent-Driven Development

Execute a plan by dispatching a fresh implementer subagent per task, a task review (spec compliance + code quality) after each, and a broad whole-branch review at the end.

**Why subagents:** You delegate tasks to agents with isolated context. By precisely crafting their instructions and context, you ensure they stay focused and succeed. They never inherit your session's history — you construct exactly what they need. This also preserves your own context for coordination.

**Core principle:** Fresh subagent per task + task review (spec + quality) + broad final review = high quality, fast iteration.

**Narration:** between tool calls, narrate at most one short line — the ledger and tool results carry the record.

**Continuous execution:** Do not pause to check in with the user between tasks. The only reasons to stop: a BLOCKED status you cannot resolve, ambiguity that genuinely prevents progress, or all tasks complete. "Should I continue?" prompts and progress summaries waste the user's time.

## When to Use

Use when: you have a written implementation plan, tasks are mostly independent, and you're executing in this session. If tasks are tightly coupled, execute manually or inline instead. If no plan exists, design and plan first.

**vs. inline plan execution:** fresh subagent per task (no context pollution), review after each task, faster iteration (no human-in-loop between tasks).

## The Process

1. Read the plan once; note context and global constraints; create todos (one per task); check the progress ledger (see Durable Progress).
2. Per task:
   a. Record the current commit as BASE. Extract the task's full text to a brief file. Dispatch an implementer subagent.
   b. If the implementer asks questions, answer them and re-dispatch.
   c. Implementer implements, tests, commits, self-reviews, reports status.
   d. Write the diff to a review package file; dispatch a task reviewer subagent.
   e. Reviewer returns two verdicts: spec compliance and task quality. If issues: dispatch a fix subagent for Critical/Important findings, then re-review. Repeat until approved.
   f. Mark the task complete in todos and the progress ledger.
3. After all tasks: dispatch a final whole-branch code reviewer (most capable model) with a package from the branch's merge base to HEAD.
4. Finish the branch: verify tests, present merge/PR/keep/discard options (see the finishing-a-development-branch skill).

## Pre-Flight Plan Review

Before dispatching Task 1, scan the plan once for conflicts:

- tasks that contradict each other or the plan's Global Constraints
- anything the plan explicitly mandates that the review rubric treats as a defect (a test that asserts nothing, verbatim duplication of a logic block)

Present everything you find to the user as one batched question — each finding beside the plan text that mandates it, asking which governs — before execution begins, not one interrupt per discovery mid-plan. If the scan is clean, proceed without comment.

## Model Selection

Use the least powerful model that can handle each role.

- **Mechanical implementation** (isolated functions, complete spec, 1-2 files): fast, cheap model. When the plan text contains the complete code, implementation is transcription plus testing — cheapest tier.
- **Integration and judgment** (multi-file coordination, pattern matching, debugging): standard model.
- **Architecture and design** — most capable model. The final whole-branch review is one of these.
- **Review tasks**: scale to the diff's size, complexity, and risk. A small mechanical diff doesn't need the top model; a subtle concurrency change does. Use a mid-tier model as the floor for reviewers and for implementers working from prose descriptions.

**Always specify the model explicitly when dispatching.** An omitted model inherits your session's model — often the most capable and expensive — which silently defeats this section.

**Turn count beats token price:** the cheapest models routinely take 2-3x the turns on multi-step work, costing more overall.

## Implementer Dispatch

Write the task's full text from the plan to a brief file (e.g. `task-N-brief.md` in scratch space) — never paste it into the prompt or make the subagent read the whole plan. The dispatch prompt contains:

1. One line on where this task fits in the project
2. The brief path, introduced as "read this first — it is your requirements, with the exact values to use verbatim"
3. Interfaces and decisions from earlier tasks that the brief cannot know
4. Your resolution of any ambiguity you noticed in the brief
5. The report-file path (e.g. `task-N-report.md`) and the report contract

The implementer's contract:
- Ask questions before starting if requirements, approach, or dependencies are unclear; ask mid-work too — never guess
- Implement exactly what the task specifies, write tests (TDD if the task says so), verify, commit, self-review (completeness, quality, YAGNI, tests verify real behavior, pristine test output)
- It is always OK to stop and escalate — bad work is worse than no work
- Write the full report (what was implemented, tests run with results and TDD red/green evidence, files changed, self-review findings, concerns) to the report file
- Return ONLY: **Status** (DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT), commits (short SHA + subject), one-line test summary, concerns, report path — under 15 lines

## Handling Implementer Status

**DONE:** Generate the review package: write `git log --oneline BASE..HEAD`, `git diff --stat BASE..HEAD`, and `git diff -U10 BASE..HEAD` to one uniquely named file (redirect — never let the diff enter your own context). BASE is the commit you recorded before dispatching — never `HEAD~1`, which silently drops all but the last commit of a multi-commit task. Then dispatch the task reviewer with that path.

**DONE_WITH_CONCERNS:** Read the concerns. If about correctness or scope, address before review. If observations ("this file is getting large"), note them and proceed to review.

**NEEDS_CONTEXT:** Provide the missing context and re-dispatch.

**BLOCKED:** Assess: (1) context problem — provide more context, re-dispatch same model; (2) needs more reasoning — re-dispatch with a more capable model; (3) task too large — break it into pieces; (4) plan itself wrong — escalate to the user.

**Never** ignore an escalation or force the same model to retry without changes.

## Task Reviewer Dispatch

The reviewer gets three paths — the brief file, the report file, the review package — plus the global constraints that bind the task (copied verbatim from the plan's Global Constraints or the spec: exact values, formats, relationships). Its instructions:

- This is a task-scoped gate, not a merge review. Read the diff file once; do not crawl the codebase. Inspect code outside the diff only to evaluate a concrete named risk (changed lock ordering, API contract, shared state — checking call sites is legitimate). Read-only: never mutate the working tree, index, HEAD, or branches.
- **Do not trust the report.** Treat it as unverified claims; verify against the diff. Design rationales ("kept it simple per YAGNI") are the implementer grading their own work — a stated rationale never downgrades a finding's severity.
- Do not re-run tests the implementer already ran on this code — the report carries the test evidence. Run only a focused test when reading the code raises a specific doubt. Warnings or noise in reported test output are findings.
- **Part 1, Spec compliance:** Missing (skipped/claimed-but-absent requirements), Extra (unrequested features, over-engineering), Misunderstood (right feature, wrong way). Requirements not verifiable from the diff alone are reported as "cannot verify from diff" items.
- **Part 2, Code quality:** separation of concerns, error handling, DRY without premature abstraction, edge cases, tests verify real behavior (not mocks), file responsibilities match the plan.
- Calibration: Important = the task cannot be trusted until fixed (incorrect/fragile behavior, missed requirement, merge-blocking maintainability damage). "Coverage could be broader" and polish are Minor. If the plan explicitly mandates something the rubric calls a defect, that IS a finding — Important, labeled plan-mandated.
- Output: spec-compliance verdict first, then Strengths, Issues (Critical/Important/Minor, each with file:line, what, why, fix), then **Task quality: Approved | Needs fixes**. Every finding cites file:line. No preamble.

**Constructing reviewer prompts — hard rules:**

- Do not add open-ended directives ("check all uses", "run race tests if useful") without a concrete task-specific reason
- Do not pre-judge findings — never instruct a reviewer to ignore or not flag an issue, or pre-rate severity ("at most Minor"). If your prompt contains "do not flag" or "the plan chose", stop: you are pre-judging, usually to spare yourself a review loop.
- A dispatch prompt describes one task, not the session's history. Do not paste accumulated prior-task summaries — a fresh subagent needs its task, the interfaces it touches, and the global constraints. Nothing else.

## Reviews, Fixes, and "Cannot Verify" Items

- "Cannot verify from diff" items: resolve each one yourself before marking the task complete — you hold the plan and cross-task context. If an item is a real gap, treat it as a failed spec review: send it back and re-review.
- Dispatch fix subagents for Critical and Important findings. Record Minor findings in the progress ledger, and point the final whole-branch review at that list to triage which must be fixed before merge. A roll-up nobody reads is a silent discard.
- A finding labeled plan-mandated — or any finding that conflicts with the plan's text — is the user's decision: present the finding and the plan text, ask which governs.
- Every fix dispatch carries the implementer contract: the fixer re-runs the tests covering its change and appends results to the same report file. Name the covering test files in the dispatch — a one-line fix doesn't need the whole suite. Confirm the fix report contains the covering tests, the command, and output before re-dispatching the reviewer.
- If the final whole-branch review returns findings, dispatch ONE fix subagent with the complete findings list — not one fixer per finding. Per-finding fixers each rebuild context and re-run suites, costing more than all the tasks combined.

## Durable Progress

Conversation memory does not survive compaction. Controllers that lost their place have re-dispatched entire completed task sequences — the single most expensive failure observed. Track progress in a ledger file (e.g. `.plan-progress.md`, git-ignored), not only in todos.

- At skill start, check for the ledger. Tasks listed as complete are DONE — do not re-dispatch; resume at the first task not marked complete.
- When a task's review comes back clean, append one line: `Task N: complete (commits <base7>..<head7>, review clean)`.
- The ledger is your recovery map: the commits it names exist in git even when your context no longer remembers creating them. After compaction, trust the ledger and `git log` over your own recollection.

## Red Flags

**Never:**
- Start implementation on main/master without explicit user consent
- Skip task review, or accept a report missing either verdict (spec compliance AND task quality are both required)
- Proceed with unfixed Critical/Important issues
- Dispatch multiple implementation subagents in parallel (conflicts)
- Make a subagent read the whole plan file (hand it its task brief)
- Skip scene-setting context (the subagent needs to know where its task fits)
- Ignore subagent questions (answer before letting them proceed)
- Accept "close enough" on spec compliance
- Skip the re-review after fixes
- Let implementer self-review replace actual review (both are needed)
- Tell a reviewer what not to flag, or pre-rate a finding's severity in the dispatch
- Dispatch a task reviewer without a diff file — generate it first
- Re-dispatch a task the progress ledger already marks complete — check the ledger (and `git log`) after any compaction or resume

**If the reviewer finds issues:** fix, re-review, repeat until approved.

**If a subagent fails a task:** dispatch a fix subagent with specific instructions — don't fix manually (context pollution).
