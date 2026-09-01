---
name: parallel-plans
description: Use when one implementation plan should run in several Claude Code sessions or worktree subagents at once without conflicts: splits the plan into lanes with exclusive write-sets, a frozen contract layer, atomic git claims and a merge order. Triggers: 'в нескольких сессиях', 'параллельно в сессиях', 'run this plan in parallel'. Extends writing-plans; each lane executes via executing-plans.
---

# Parallel Plans

## Overview

parallel-plans extends writing-plans: it takes the same plan file and adds lanes — disjoint write-sets, a frozen foundation, atomic git claims, and a merge order — so the plan runs correctly across several Claude Code sessions or worktree subagents instead of one.
Each lane still executes with executing-plans or subagent-driven-development; this skill only adds the structure that keeps lanes from colliding and defines how they merge back into main.

## The Iron Law

```
NO LANE WRITES OUTSIDE ITS WRITE-SET. NO FAN-OUT BEFORE FOUNDATION IS ON MAIN.
NO MERGE WITHOUT REBASE AND GREEN VERIFY. ONE LANE PER SESSION. CONTRACT CHANGES ARE THE USER'S DECISION.
```

Three of these are checkable in git rather than by trust: a write-set violation is a diff that touches a file outside the lane's globs; a premature fan-out is a lane branch whose merge-base predates the foundation commit; an unrebased merge is a `--ff-only` that fails and says so. One lane per session and the contract-change rule are conventions the lane prompt states explicitly.

## When to Use

Use when:
- A plan from writing-plans has two or more chunks of work that can run against disjoint files once a shared foundation (types, config, schema) is in place.
- Multiple Claude Code sessions, `isolation: "worktree"` subagents, or people are available to run those chunks at the same time.
- The user asks for parallel execution across sessions or worktrees, including "в нескольких сессиях", "параллельно в сессиях", "run this plan in parallel".

## Not For

- A plan with one linear order and no independent chunks — use executing-plans or subagent-driven-development on it directly.
- A plan that fails any of the Gates below (too little parallel work, foundation too large, shared files everywhere, or the whole job is under an hour).
- Designing the plan itself — that is writing-plans' job; this skill only adds lanes to a plan that already exists.

## Concepts

**Lane** — a unit of parallel work with an exclusive write-set (a glob list; every file outside it is read-only to that lane), its own branch `lane/<plan-slug>/<lane-id>` and worktree `.claude/worktrees/<plan-slug>-<lane-id>`, a `depends_on` list of lanes whose contracts it consumes, a `verify` command, `resources` (ports, database names, temp dirs — no two lanes share a mutable resource), and a lane prompt: the self-sufficient block a session pastes in to start work.

**Lane 0, foundation** — runs serially on main before any fan-out. It lays down what every other lane compiles against: contracts (types, interfaces, API schemas, migrations), shared config (dependency manifests, lockfile, test config, CI, CLAUDE.md), the directories each lane will own, and stubs so every lane's write-set builds clean from the moment it starts.

**Lane Ω, integration** — runs serially after every lane reports done. It merges lanes in dependency order, runs the full suite and end-to-end tests, updates the project map, retires worktrees and branches, and closes the branch with finishing-a-development-branch.

## Plan Format

parallel-plans does not add a new document type. It adds a header line, a Lanes table, and a Contracts block to the same plan file writing-plans produces, placed right after the Global Constraints section.

Header line, directly under the plan title:

```markdown
**Parallel:** 2 lanes; foundation first; merge order 0 -> A -> B -> Ω.
```

Lanes table and contracts:

```markdown
## Lanes
| Lane | Owns (write-set) | Depends on | Verify | Resources |
|------|------------------|------------|--------|-----------|
| 0 foundation | src/contracts/**, package.json, pnpm-lock.yaml, vitest.config.ts | - | pnpm test | - |
| A api | src/api/**, tests/api/** | 0 | pnpm test -- api | port 3101, db app_lane_a |
| B bot | src/bot/**, tests/bot/** | 0 | pnpm test -- bot | port 3102, db app_lane_b |
| Ω integration | everything | A, B | pnpm test && pnpm e2e | prod services |

### Contracts (frozen at fan-out)
<exact signatures, types, endpoints — copied from Lane 0's Produces blocks>
```

The Contracts block is not prose: it is the exact signatures, types, and endpoint shapes Lane 0 produced, copied verbatim from its tasks' Produces blocks. Every other lane codes against this block, not against Lane 0's implementation — changing it after fan-out is a contract change (see The Iron Law).

Tasks are grouped per lane using the writing-plans task template, under headings like `### Lane A — Task A1: ...`, so a lane's session reads only its own tasks. An appendix, `## Lane prompts`, holds one self-sufficient block per lane — see Lane Prompt Template below — so a person can paste a lane's block into a fresh session with nothing else.

## Protocol

1. **Claim.** Reserve a lane atomically in git:

   ```bash
   git worktree add .claude/worktrees/<slug>-<lane> -b lane/<slug>/<lane> main
   ```

   "already exists" on the branch or the worktree path means the lane is taken — stop and report, never force it. On success, call `EnterWorktree(path=.claude/worktrees/<slug>-<lane>)` so isolation enforcement turns on for the rest of the session. When a human is assigning lanes by hand instead of sessions racing for them, `claude --worktree <slug>-<lane>` is an acceptable shortcut — it creates the same path in one step, but on branch `worktree-<slug>-<lane>`, not `lane/<slug>/<lane>`; adjust the branch name in later steps if you use it.

2. **Preconditions.** Confirm the foundation commit is an ancestor of HEAD (`git merge-base --is-ancestor <foundation-commit> HEAD`) and that every lane in `depends_on` is already merged into main (`git branch --merged main` lists it). If either check fails, wait or pick another lane — never start against stale contracts.

3. **Work.** Execute the lane's own tasks, nothing else, with executing-plans inline or subagent-driven-development (subagents dispatched from inside the worktree inherit its isolation). Track progress in a per-lane ledger inside the worktree, `.plan-progress-<lane>.md`.

4. **Boundary.** The write-set is not a suggestion. A task that needs a file outside it stops the lane there. An additive contract need (a new field, a new endpoint) goes into the lane report for Ω to reconcile; a breaking change is the user's decision, lands on main as a new foundation commit, and every other lane rebases onto it before continuing.

5. **Sync.** Rebase onto main at every task boundary and always immediately before hand-off:

   ```bash
   git rebase main
   ```

   SendMessage between local sessions and `notify_when_idle` on a dependency lane's session are optional accelerators for knowing when to rebase — never a requirement; polling `git branch --merged main` works without them.

6. **Hand-off.** Rebase, confirm verify is green, self-review the diff, write the lane report inside the worktree (git-ignored, or committed on the lane branch), and leave the session parked in its worktree. Lane status is entirely readable from git: a branch that exists is claimed, a branch merged into main is done.

7. **Integration (Ω).** Run from the main checkout — never from inside a lane's worktree, since isolation blocks git commands against main from there. For each lane in dependency order, rebase it once more inside its own worktree, then merge from the main checkout:

   ```bash
   git merge --ff-only lane/<slug>/<lane>
   ```

   A merge that isn't a fast-forward means the lane went stale between rebase and merge — send it back to step 5, never force-merge. Run that lane's verify after each merge, then the full suite and end-to-end tests once every lane is in. Update the project map, then retire the lane:

   ```bash
   git worktree remove .claude/worktrees/<slug>-<lane>
   git worktree prune
   git branch -d lane/<slug>/<lane>
   ```

   Close out with finishing-a-development-branch.

## Lane Prompt Template

Fill in every placeholder before pasting this into a fresh session — it must be self-sufficient with nothing else from the plan.

```markdown
You are running one lane of a parallel plan. Follow these rules for the whole session:

1. Write only inside your write-set below. Anything else needed outside it is a stop-and-report, not an improvisation.
2. Never merge or push to main, and never run git commands against the main checkout — you are isolated in a worktree for a reason. Rebase onto main before every hand-off.
3. Do only this lane's tasks. When they are done and verify is green, write the report and stop — do not start another lane or run integration.

Repo: <repo-path>
Plan: <plan-path>
Lane: <lane-id>

Claim:
git worktree add .claude/worktrees/<slug>-<lane> -b lane/<slug>/<lane> main

Then call EnterWorktree(path=.claude/worktrees/<slug>-<lane>).

Write-set: <write-set-globs>

Read this lane's tasks from <plan-path>, section "### Lane <lane-id>", plus the Contracts block. Execute them with executing-plans, or subagent-driven-development if you dispatch further subagents from inside this worktree.

Verify: <verify-command>

Done when: <done-criteria>

Report to: <report-path inside this worktree, e.g. lane-report.md at the worktree root> — lane id, commits made, verify output, anything that needed a file outside the write-set, anything blocked on another lane. The main checkout is write-blocked from an isolated session, so a report path outside the worktree fails.
```

## Integration (Ω)

Ω is not a lane that writes feature code — it is the serial merge-and-verify pass from Protocol step 7, called out here because it is the step most tempting to rush.

- Run it from the main checkout, by the planning session or any session that is free — never from inside a lane's worktree.
- Merge order follows `depends_on`, not the order lanes finished in: a lane cannot merge before a lane it depends on, even if it reported done first.
- Every merge is `--ff-only`; a rejection means rebase-and-retry, never force.
- Run each lane's own verify right after its merge, so a break is pinned to the lane that caused it, then the full suite and end-to-end tests once all lanes are in.
- Update the project map — this is the one point in the run where the map changes, since individual lanes only touch their own write-set.
- Retire every worktree and branch, then hand off to finishing-a-development-branch for the usual close on the now-unified branch.

## Gates

Do not parallelize when any of these hold — run the plan with executing-plans or subagent-driven-development instead:

- Fewer than two lanes end up with disjoint write-sets once the foundation is factored out.
- The foundation itself is more than a third of the total work.
- More than about 30% of tasks touch shared files — the write-sets are not actually disjoint.
- The total work is under an hour — coordination overhead costs more than serial execution saves.

Typical lane count is 2-4; more than that usually means the write-sets are too fine-grained to be worth separate sessions. Executors can be human-run Claude Code sessions (the primary case), `isolation: "worktree"` subagents, or agent teams (experimental, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` — teams share a task list with file-locked claims, which overlaps this skill's claim step). The plan format is identical regardless of which one executes a lane.

## Red Flags

Never:
- Start a lane's tasks before `EnterWorktree` succeeds and verify runs clean against the foundation.
- Edit a file outside your write-set because it is "just one line" — stop and report instead; that line is how two lanes collide.
- Merge a lane into main with anything but `--ff-only`, or merge lanes out of `depends_on` order.
- Run two lanes' work in the same session or the same worktree "to save time" — that is serial execution wearing a parallel plan's clothes, and it drops the isolation the write-set rule depends on.
- Treat "already exists" on `git worktree add` as something to work around — it means the lane is claimed; pick a different one or ask.
- Skip Ω's full-suite run because every lane's own verify was green — green lanes can still conflict at the seams.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "It's just one small file outside my write-set" | That is exactly the collision the write-set exists to prevent — stop and report, do not improvise. |
| "My lane is done, I'll start reviewing or merging the others" | One lane per session. Hand off and stop; Ω is a separate step, possibly a separate session. |
| "Rebasing every boundary is slow, I'll do it once at the end" | A rebase deferred to the end happens under pressure, right when the merge queue is waiting. Rebase at every boundary. |
| "The contract's missing a field, I'll just add it in my lane" | Contract changes are the user's decision, land on main as a foundation commit, and trigger a rebase in every lane — not a unilateral edit in one. |
| "Foundation's basically done, let's fan out early" | A lane branched before the foundation commit is on main is branched off contracts that can still change under it. Wait for the commit. |

## Quick Reference

| Step | Action | Command / check |
|------|--------|------------------|
| 1. Claim | Reserve a lane | `git worktree add … -b lane/<slug>/<lane> main`, then `EnterWorktree` |
| 2. Preconditions | Confirm foundation and deps are in | `git merge-base --is-ancestor`, `git branch --merged main` |
| 3. Work | Execute this lane's tasks only | executing-plans / subagent-driven-development |
| 4. Boundary | Stop on out-of-write-set edits | write it into the lane report, don't make the edit |
| 5. Sync | Pick up merged and foundation changes | `git rebase main` |
| 6. Hand-off | Green verify, report, stay parked | branch exists = claimed, merged = done |
| 7. Integration (Ω) | Merge in dependency order | `git merge --ff-only`, full suite, `git worktree remove` / `prune` |

## Cross-links

brainstorming surfaces lane candidates while the design is still being explored. writing-plans turns the settled design into the plan file this skill adds lanes to, and can offer lane splitting as a third hand-off option when a plan has independent chunks. parallel-plans owns the claim-work-sync-merge protocol in between. Each lane then executes with executing-plans inline or subagent-driven-development for further fan-out. using-git-worktrees documents the isolation mechanics — EnterWorktree, blocked main-checkout access — that this skill relies on rather than reimplementing. finishing-a-development-branch closes out Ω's unified branch. project-cartography's map is updated only once, by Ω, never by individual lanes.
