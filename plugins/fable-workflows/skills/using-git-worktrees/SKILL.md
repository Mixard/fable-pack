---
name: using-git-worktrees
description: Use when starting feature work that needs isolation from the current workspace, or before executing implementation plans. Ensures an isolated workspace exists via native tools (--worktree/EnterWorktree) or a git worktree fallback.
---

# Using Git Worktrees

## Overview

Ensure work happens in an isolated workspace. Prefer native tools (`--worktree`/EnterWorktree). Fall back to manual git worktrees only when no native tool is available.

**Core principle:** Detect existing isolation first. Then use native tools. Then fall back to git. Never fight the harness.

## Step 0: Detect Existing Isolation

Check before creating anything — including whether the session itself started with `--worktree`/EnterWorktree, which already puts you in one:

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
git rev-parse --show-superproject-working-tree 2>/dev/null  # non-empty = submodule, not a worktree
```

**`GIT_DIR != GIT_COMMON` (and not a submodule), or session started with `--worktree`/EnterWorktree:** already isolated — skip to Step 2, do not create another worktree.

**`GIT_DIR == GIT_COMMON` (or a submodule):** normal checkout. Ask consent unless the user already stated a preference: "Would you like me to set up an isolated worktree? It protects your current branch from changes." Declined -> work in place, skip to Step 2.

## Step 1a: Native Tools (preferred)

`claude --worktree <name>` (alias `-w`) or `EnterWorktree(name: <name>)` creates `.claude/worktrees/<name>/` on branch `worktree-<name>`; reusing a name reopens that worktree. Base ref follows `worktree.baseRef`: `"fresh"` = remote default branch (local HEAD if no remote), `"head"` = current HEAD. `.worktreeinclude` (gitignore syntax, repo root) copies gitignored files like `.env` into new worktrees. `EnterWorktree(path: <path>)` enters a worktree already listed by `git worktree list` under `.claude/worktrees/`. While isolated, Edit/Write/NotebookEdit into the main checkout and Bash whose cwd or git target is the main checkout are blocked — enforced, not a convention.

Have a native tool? Use it, skip to Step 2. Only fall through to 1b with none available.

## Step 1b: Git Worktree Fallback

Default to `.claude/worktrees/` (harness-recognised) and verify it's ignored first:

```bash
git check-ignore -q .claude/worktrees || { echo ".claude/worktrees" >> .gitignore; git add .gitignore; git commit -m "chore: ignore worktree directory"; }
git worktree add .claude/worktrees/<branch> -b <branch>
cd .claude/worktrees/<branch>
```

**Sandbox fallback:** `git worktree add` denied by sandbox -> tell the user, work in the current directory instead.

## Step 2: Project Setup

```bash
if [ -f package.json ]; then npm install; fi
if [ -f Cargo.toml ]; then cargo build; fi
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi
if [ -f go.mod ]; then go mod download; fi
```

## Step 3: Verify Clean Baseline

```bash
npm test / cargo test / pytest / go test ./...
```

Fail -> report failures, ask whether to proceed or investigate. Pass -> report ready: path, test count, feature name.

## Quick Reference

| Situation | Action |
|-----------|--------|
| Already isolated, or in a submodule | Step 0 handles it — skip creation, or treat as normal repo |
| Native tool available | Use it (Step 1a) |
| No native tool | Git fallback (Step 1b) |
| Permission error on `git worktree add` | Sandbox fallback, work in place |

## Red Flags

**Never:**
- Use `git worktree add` when `--worktree`/EnterWorktree is available — the #1 mistake
- Remove a worktree from inside it (see finishing-a-development-branch)
- Proceed with failing tests without asking

**Always:** run Step 0 detection first, prefer native tools over the git fallback, verify the fallback directory is ignored, verify a clean test baseline.
