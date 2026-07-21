---
name: executing-plans
description: Use when you have a written implementation plan to execute inline in the current session, following it task by task with review checkpoints.
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks, report when complete.

If subagent dispatch is available, prefer the subagent-driven-development skill instead — fresh context per task plus per-task review produces higher quality. Use this skill for inline execution.

## The Process

### Step 1: Load and Review Plan
1. Read the plan file
2. Review critically — identify any questions or concerns about the plan
3. If concerns: raise them with the user before starting
4. If no concerns: create todos for the plan items and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (the plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 3: Complete Development

After all tasks complete and verified, finish the branch properly: verify the full test suite, then present the integration options (merge locally, push and create a PR, keep the branch, or discard) and execute the user's choice. The finishing-a-development-branch skill covers this.

## When to Stop and Ask for Help

**STOP executing immediately when:**
- You hit a blocker (missing dependency, test fails, instruction unclear)
- The plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to review (Step 1) when:**
- The user updates the plan based on your feedback
- The fundamental approach needs rethinking

**Don't force through blockers** — stop and ask.

## Remember
- Review the plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Stop when blocked, don't guess
- Never start implementation on main/master without explicit user consent — work on a branch or in an isolated worktree
