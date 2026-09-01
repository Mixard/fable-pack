# fable-pack 2.0 — design (2026-09-01)

Follow-up to the model-relevance audit (`docs/audits/2026-09-01-model-relevance-audit.md`). Decisions taken by the maintainer on 2026-09-01: removal bar = "both Fable 5.1 and Sonnet 5 know it"; the single-project environment is this server; structure = new fable-mobile plugin plus a domain split of fable-knowledge; parallel-plans lanes run in human sessions with an integration session merging.

Scope of this spec: **Phase 1** (one implementation plan). Phase 2 is outlined at the end and gets its own spec.

## 1. Goals and non-goals

Goals:
1. Remove what the target models already know and fix what the audit proved wrong, so no skill can override a correct model.
2. Replace the monolithic fable-knowledge with domain plugins so a single-project machine installs only its domains.
3. Align the workflow skills with the 2026-09 harness (native worktrees, `/code-review`, AskUserQuestion) and add parallel-plans.
4. Reconfigure this server for the Replyvo mobile app project.

Non-goals (Phase 1): new mobile content beyond moving the five Apple skills; marketing trims; iOS 27 refresh (not GA yet); fable-guard write-set hook.

## 2. Plugin restructure

### 2.1 Removals (bar: Fable ≥ 0.88 and Sonnet ≥ 0.88)

fable-knowledge, 11 skills: clickhouse, database-migrations, evm-gotchas, manim-explainers, nuitka-windows-packaging, nuxt4-patterns, postgres-tips, bun-runtime, pubmed-database, react-performance, remotion.

fable-agents, 4 agents: golang-pro, java-pro, rust-pro, python-pro (all 1.00/1.00 on Sonnet and Opus; the remaining value is a generic "expert" prompt the model produces on its own). **Decision for review:** python-pro is the maintainer's most-used language; it goes by the bar, but keeping it as a role prompt is a legitimate override. bash-pro stays (0.25/0.38), with its two Bash-version errors fixed and trimmed from 292 lines toward 150.

fable-workflows, 1 skill: requesting-code-review (covered by the built-in `/code-review` and by subagent-driven-development's Task Reviewer).

### 2.2 Domain plugins replacing fable-knowledge

fable-knowledge is removed from the marketplace (CHANGELOG + README migration note; installed 1.0.0 caches keep working but never update). The 36 remaining skills move, files unchanged except the fixes in §3:

| Plugin (1.0.0) | Skills | Count |
|---|---|---|
| fable-mobile | ios-icon-gen, swift-concurrency-6-2, ios26-liquid-glass, apple-foundation-models, wcag22-reference | 5 |
| fable-web | angular-developer, nextjs-turbopack, pm2-node-services, html-slides, playwright-demo-videos, prisma-patterns | 6 |
| fable-integrations | x-api, jira-integration, nutrient-api, free-tier-scraper-apis, mcp-server-configs, mailtrap-email-integration, laravel-plugin-discovery, codehealth-mcp, claude-devfleet, agent-payment-x402, n8n-selfhosted-ops | 11 |
| fable-media | fal-ai-media, videodb, ffmpeg-media-recipes | 3 |
| fable-niche | kotlin-ktor, kotlin-exposed, perl-modern, cpp-core-guidelines, tinystruct-patterns, flox-environments, uncloud, windows-desktop-e2e, gget, uspto-database, defi-amm-security | 11 |

Each plugin gets `.claude-plugin/plugin.json` (name, description, version 1.0.0, author, license MIT, keywords) and a marketplace.json entry (category, tags). Every skill folder moves with `git mv` so history survives.

Android is **not** vendored: rcosteira79/android-skills is itself a maintained Claude Code marketplace (MIT, 21 skills, updated 2026-08-25) and is installed from upstream on machines that need it. fable-mobile carries only what is original or adapted (Phase 2).

### 2.3 Version bumps

fable-agents 2.0.0 (removals), fable-workflows 2.0.0 (removal + new skill + rewrites), fable-guard unchanged, fable-marketing unchanged, five new plugins at 1.0.0. Pack total after Phase 1: 36 + 20 + 20 = 76 skills (domain plugins + marketing + workflows), 18 agents (22 − 4; 19 if python-pro is kept).

## 3. Factual fixes (verified against primary sources on 2026-09-01)

| File | Change |
|---|---|
| kotlin-ktor | StatusPages: handler selection is by nearest class in the exception hierarchy (`selectNearestParentClass`), not install order; identical in Ktor 1.x–3.x. Rewrite the two lines that claim order matters |
| perl-modern | A plain nested read (`$h->{a}{b}`) autovivifies every intermediate level; only the last key is not created. Mention `no autovivification` pragma as the opt-out |
| n8n-selfhosted-ops | `n8n import:credentials --input=<file>` exists; ids are preserved, so nodes re-link when the credentials export from the same source is imported (needs `--decrypted` across instances with different encryption keys). Replace the "cannot be automated" claim |
| x-api | Default tweet fields are `id`, `text`, `edit_history_tweet_ids` (since Sept 2022) |
| wcag22-reference | SwiftUI live-region cell: there is no `accessibilityLiveRegion` modifier; use the `updatesFrequently` trait for frequently changing values and `AccessibilityNotification.Announcement` (iOS 17+) / `UIAccessibility.post(.announcement)` for announcements |
| bash-pro | `EPOCHREALTIME`/`EPOCHSECONDS` are Bash 5.0; `${var@U}`/`@u`/`@L` and the associative-array improvements are 5.1; `varredir_close` is 5.2; drop "improved exec error handling" |

## 4. Workflow skill changes (fable-workflows 2.0.0)

| Skill | Change |
|---|---|
| using-git-worktrees | Rewrite to ~70 lines around the native path: `claude --worktree <name>` / EnterWorktree create `.claude/worktrees/<name>` on branch `worktree-<name>`, base from `worktree.baseRef` (`fresh` = remote default branch, `head` = current HEAD), `.worktreeinclude` copies gitignored files, isolation blocks edits and git in the main checkout; EnterWorktree(`path`) enters an existing worktree registered in `git worktree list`. Git fallback stays as a short second section (`git worktree add`, gitignore check). Baseline-test step stays |
| finishing-a-development-branch | Trim to ~120 lines: keep the four-option menu, typed "discard", merge → verify → remove order; cleanup delegates to ExitWorktree (keep/remove, `discard_changes` guard); provenance check recognises `.claude/worktrees/` as harness-owned; final whole-branch review points at `/code-review` when available |
| brainstorming | Replace "one question per message" with: batch related questions through AskUserQuestion (≤4 per round, one topic each, options with a recommended first choice); fall back to one-per-message only when the tool is unavailable. Replace per-section approval with one design approval. Add: when the design has ≥2 independent components, record them as lane candidates for parallel-plans |
| writing-plans | Scope Check: mention lanes; Execution Handoff gains option 3 "Parallel lanes (parallel-plans)"; plan header gets an optional `**Parallel:**` line |
| subagent-driven-development | Replace the blanket "never dispatch implementation subagents in parallel" with: parallel implementers only across lanes with disjoint write-sets (parallel-plans) or with `isolation: "worktree"`; final review may use `/code-review` |
| executing-plans | One line: inside a lane, the plan's write-set bounds every edit |
| test-driven-development | Trim to ~120 lines: keep Iron Law, red/green verification, mock rules, exceptions; cut rationalization tables and duplicated debugging text |
| requesting-code-review | Removed |
| parallel-plans | New; §5 |

## 5. parallel-plans (new skill)

Description (≤400 chars, with Russian triggers): "Use when one implementation plan should run in several Claude Code sessions or worktree subagents at once without conflicts: splits the plan into lanes with exclusive write-sets, a frozen contract layer, atomic git claims and a merge order. Triggers: 'в нескольких сессиях', 'параллельно в сессиях', 'run this plan in parallel'. Extends writing-plans; executes via executing-plans."

### 5.1 Concepts

- **Lane**: a unit of parallel work with an exclusive **write-set** (glob list; everything else is read-only for that lane), a branch `lane/<plan-slug>/<lane-id>`, a worktree `.claude/worktrees/<plan-slug>-<lane-id>`, `depends_on` (lanes whose produced contracts it consumes), a `verify` command, `resources` (ports, database names, temp dirs it may use; no two lanes share a mutable resource), and a **lane prompt** the user pastes into a fresh session.
- **Lane 0, foundation** (serial, on main before fan-out): contracts (types, interfaces, API schemas, migrations), shared config (dependency manifests, lockfile, test config, CI, CLAUDE.md), the directories each lane owns, stubs so every lane compiles against the contracts.
- **Lane Ω, integration** (serial, after all lanes): merge in dependency order, full suite and e2e, project-cartography update, cleanup, finishing-a-development-branch.

### 5.2 Plan format (same plan file as writing-plans)

Header line `**Parallel:** N lanes; foundation first; merge order …`. After Global Constraints:

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

Tasks are grouped per lane (`### Lane A — Task A1 …`) in the writing-plans task format, so a session reads only its lane. An appendix `## Lane prompts` holds one self-sufficient block per lane: repo path, plan path, lane id, claim command, write-set, verify command, done criteria, report path.

### 5.3 Protocol

1. **Claim** (atomic in git): `git worktree add .claude/worktrees/<slug>-<lane> -b lane/<slug>/<lane> main`. "already exists" means the lane is taken: stop and report. Then `EnterWorktree(path=…)` so isolation enforcement is on. When the human assigns lanes by hand, `claude --worktree <slug>-<lane>` is acceptable (no claim race).
2. **Preconditions**: foundation commit is an ancestor of HEAD; every `depends_on` lane is already merged into main (`git branch --merged main`). Otherwise wait or pick another lane.
3. **Work**: execute the lane's tasks with executing-plans (inline) or subagent-driven-development (subagents inherit the worktree). Ledger `.plan-progress-<lane>.md` inside the worktree.
4. **Boundary**: any needed edit outside the write-set stops the lane. Additive contract needs go into the lane report; breaking changes are the user's decision and land on main as a foundation commit, after which every lane rebases.
5. **Sync**: `git rebase main` at task boundaries and always before hand-off. SendMessage to sibling sessions and `notify_when_idle` on dependency lanes are optional accelerators, never requirements.
6. **Hand-off**: verify green after rebase, self-review, lane report written, session stays in its worktree. Status is git: branch exists = claimed; branch merged into main = done.
7. **Integration** (Ω, run by the planning session or any free session, from the main checkout): merge lanes in dependency order with `--ff-only` after rebase (a non-ff merge means the lane is stale: send it back to rebase), run the lane's verify after each merge and the full suite at the end, update the project map, remove worktrees (`git worktree remove`, `git worktree prune`) and delete lane branches, then finishing-a-development-branch.

### 5.4 Hard rules and gates

```
NO LANE WRITES OUTSIDE ITS WRITE-SET. NO FAN-OUT BEFORE FOUNDATION IS ON MAIN.
NO MERGE WITHOUT REBASE AND GREEN VERIFY. ONE LANE PER SESSION. CONTRACT CHANGES ARE THE USER'S DECISION.
```

Do not parallelize when: fewer than two lanes have disjoint write-sets after foundation; foundation exceeds a third of the work; more than ~30% of tasks touch shared files; total work is under an hour. Typical size 2–4 lanes. Executors can be human sessions (primary), `isolation: "worktree"` subagents, or agent teams (experimental) — the plan format is the same.

### 5.5 Cross-links

brainstorming (lane candidates) → writing-plans (lanes section, handoff option 3) → parallel-plans (protocol) → executing-plans / subagent-driven-development (per lane) → finishing-a-development-branch (Ω). using-git-worktrees documents the isolation mechanics parallel-plans relies on. project-cartography: only Ω updates the map.

## 6. This server (single project: Replyvo app)

| Action | Detail |
|---|---|
| uninstall | fable-knowledge@fable-pack (replaced), fable-marketing@fable-pack (reinstall at launch for aso/pricing/churn), genlab@genlab-marketplace |
| install | fable-mobile@fable-pack, expo@claude-plugins-official, rcosteira79/android-skills (marketplace add + install), keep fable-workflows, fable-agents, fable-guard; update all to the new versions |
| keep | `~/.claude/skills/{taste-skill,impeccable,emil-design-eng}` stay global (decision 2026-09-01: the maintainer wants them fired for future website/info-page work; cost after the budget fix is ~330 tokens). A memory rule records when to invoke them |
| keep | `skillListingBudgetFraction: 0.02`; re-run the headless listing check after the migration (expected: 0 name-only skills) |
| android repos | keep `/root/android-skills/android-skills` and `_drafts/`; the other four clones are not needed (delete only on explicit request) |

## 7. Documentation and release

README: plugin table (5 new plugins, fable-knowledge migration note), badges, "What's new" row, Why-this-selection paragraph gains the audit's 7:0 lesson and a pointer to the audit; install snippet updated. CHANGELOG: one section per released plugin version. ATTRIBUTIONS: counts updated (ECC skills now 35 of 36 across the five plugins; superpowers 10 of 20 workflows), rows unchanged otherwise. validate.py: no change needed (globs `plugins/*/skills`); add a check that every skill folder is referenced by exactly one plugin. Release per `.claude/skills/release`: validate → bumps → CHANGELOG → README → commit → push → CI → local `claude plugin update`.

## 8. Verification

1. `python3 scripts/validate.py` prints OK with 76 skills, 18 agents.
2. Fresh headless `fable[1m]` session lists 0 name-only skills after the server migration.
3. parallel-plans smoke test on a throwaway repo: two lanes claimed from two headless sessions, the second claim of the same lane fails, both lanes merge `--ff-only` after rebase, verify passes.
4. Every factual fix cites its source in the commit message.
5. `grep -r` for removed skill/agent names returns nothing in README, CHANGELOG (except history), ATTRIBUTIONS, cross-references inside skills.

## 9. Phase 2 (separate spec)

fable-mobile content: android-overlay-a11y translated and generalised; four gap skills researched from primary sources (expo-apple-targets share/keyboard extensions; store-compliance calendar; subscriptions on Expo with Play Billing 8–9 / StoreKit 2 / RevenueCat; speech-to-text facts); adoption of conorluddy/ios-simulator-skill and kylehughes build tools (install upstream if they are plugins, adapt otherwise); apple-foundation-models and ios26-liquid-glass refresh at iOS 27 GA. A mobile-release workflow skill after the first real release.
