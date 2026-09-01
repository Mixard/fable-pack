---
name: finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work. Guides completion by presenting structured options for merge, PR, keep, or discard, and handles worktree cleanup.
---

# Finishing a Development Branch

## Overview

Guide completion of development work by presenting clear options and handling the chosen workflow. **Core principle:** Verify tests -> Detect environment -> Present options -> Execute choice -> Clean up.

## The Process

### Step 1: Verify Tests

```bash
npm test / cargo test / pytest / go test ./...
```

Fail -> report `Tests failing (<N> failures). Must fix before completing:` with the failures shown, then stop — don't proceed to Step 2. Pass -> continue to Step 2.

### Step 2: Detect Environment

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
```
Determines which menu to show and how cleanup works:

| State | Menu | Cleanup |
|-------|------|---------|
| `GIT_DIR == GIT_COMMON` (normal repo) | Standard 4 options | No worktree to clean up |
| `GIT_DIR != GIT_COMMON`, named branch | Standard 4 options | Provenance-based (see Step 6) |
| `GIT_DIR != GIT_COMMON`, detached HEAD | Reduced 3 options (no merge) | No cleanup (externally managed) |

### Step 3: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```
Or ask: "This branch split from main - is that correct?"

### Step 4: Present Options

**Normal repo and named-branch worktree — present exactly these 4 options:**
```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```
**Detached HEAD — present exactly these 3 options:**
```
Implementation complete. You're on a detached HEAD (externally managed workspace).

1. Push as new branch and create a Pull Request
2. Keep as-is (I'll handle it later)
3. Discard this work

Which option?
```
Keep options concise — no added explanation.

### Step 5: Execute Choice

**Option 1 — Merge Locally:** the merge runs in the main checkout, which an isolated session cannot touch — leave isolation first.
- Harness-created worktree (`.claude/worktrees/`): `ExitWorktree(action: "keep")` first; the session returns to the main checkout with isolation off.
- Self-created worktree: `cd "$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)"`.
```bash
git checkout <base-branch> && git pull && git merge <feature-branch>
<test command>   # verify tests on the merged result
```
Cleanup worktree (Step 6), then `git branch -d <feature-branch>`.

**Option 2 — Push and Create PR:**
```bash
git push -u origin <feature-branch>
```
**Do NOT clean up the worktree** — the user needs it alive to iterate on PR feedback.

**Option 3 — Keep As-Is:** Report "Keeping branch <name>. Worktree preserved at <path>." **Don't clean up the worktree.**

**Option 4 — Discard:** confirm first —
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```
Wait for exact confirmation. Harness-created worktree: `ExitWorktree(action: "remove", discard_changes: true)` deletes the worktree and its branch in one step. Self-created: `cd "$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)"`, cleanup worktree (Step 6), then force-delete: `git branch -D <feature-branch>`.

### Step 6: Cleanup Workspace

**Only runs for Options 1 and 4.** Options 2 and 3 always preserve the worktree.

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```
**`GIT_DIR == GIT_COMMON`:** normal repo, no worktree to clean up. Done.

**Worktree path under `.claude/worktrees/`:** harness-created. After Option 1 (session already left with `ExitWorktree(action: "keep")` and merged): `git worktree remove .claude/worktrees/<name>` then `git worktree prune`. Option 4: `ExitWorktree(action: "remove", discard_changes: true)` from inside the worktree, after the typed confirmation — it refuses to remove unmerged work otherwise.

**Self-created (e.g. under `.worktrees/`, `worktrees/`):**
```bash
cd "$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)"
git worktree remove "$WORKTREE_PATH"
git worktree prune
```
**Otherwise:** the host environment owns this workspace — do not remove it manually.

For the final whole-branch review prefer the built-in `/code-review` when available.

## Red Flags

**Never:**
- Proceed with failing tests, or merge without verifying tests on the result
- Delete work without typed "discard" confirmation
- Run `git worktree remove` from inside the worktree being removed, or `git merge` from inside an isolated worktree session (leave with ExitWorktree first)
- Pass `discard_changes: true` to ExitWorktree before the typed confirmation

**Always:** verify tests before offering options, detect environment before presenting the menu, present exactly 4 options (3 for detached HEAD), get typed confirmation for Option 4, clean up only for Options 1 and 4 — via ExitWorktree for harness-created worktrees, `git worktree remove` + `prune` for self-created ones.
