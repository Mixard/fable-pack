# Changelog

All notable changes to this pack are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [fable-workflows 2.1.0] - 2026-09-14

### Changed

- verification-before-completion: new "Define Done Before the Work" section, adapted from a triage of Leonxlnx/unlazy (MIT) — for multi-part work, acceptance checks (outcome + deciding command + success output) are written before implementing; a check counts as evidence only if it can fail (positive control for absence checks, measured rather than copied numbers, exit code plus success-only marker); an impossible requirement is surfaced as an unmet handoff, never silently dropped. The Requirements pattern now reconciles against the original request and amendments and reports met/unmet/abandoned counts. unlazy's Node gate tooling, approval store, Depth Tree orchestration and Stop hook were not adopted: they overlap subagent-driven-development and parallel-plans and add ceremony without a documented failure they would fix.

## [fable-legacy 1.0.0] - 2026-09-01

### Added

- Opt-in archive plugin holding everything retired in 2.0 (11 knowledge skills, 4 language agents, requesting-code-review), restored verbatim from commit 2c9bd78. Marketplace policy from now on: retired content moves to fable-legacy instead of disappearing, so servers that install from this marketplace never lose a skill they depend on.

## [fable-mobile 1.1.0] - 2026-09-01

### Added

- Four original skills for Expo / React Native apps, each researched from primary sources by a sonnet subagent and then hostile-fact-checked by a second subagent before release (208 claims confirmed, 15 corrected; corrections included two load-bearing plugin behaviors documented wrongly by the plugin's own README):
  - expo-apple-targets-extensions: iOS share and custom keyboard extensions via `@bacons/apple-targets` — config schema, App Groups auto-sync per target type, activation rules, `RequestsOpenAccess` limits, the Today/iMessage-only scope of `NSExtensionContext.open`, EAS signing, open prebuild bugs.
  - mobile-store-compliance: dated Google Play and App Store requirement tables (target API 36, Billing Library 8/9, developer verification, AccessibilityService policy, foreground-service declarations, privacy manifests, Xcode 26 SDK minimum, TestFlight limits) plus a pre-submission checklist keyed to AI text, accessibility overlays, microphone, chat screenshots and subscriptions.
  - expo-subscriptions: RevenueCat vs direct StoreKit 2 / Play Billing decision, exact SDK shapes, Apple sandbox renewal table, App Store Server API and Play Developer API verification from Cloudflare Workers, dated 2026 policy rows.
  - mobile-speech-to-text: expo-speech-recognition options, SFSpeechRecognizer limits vs iOS 26 SpeechAnalyzer, Android SpeechRecognizer extras, Gemini audio limits and per-clip costs against OpenAI and ElevenLabs.

## [fable-workflows 2.0.1] - 2026-09-01

### Fixed

- parallel-plans: the lane prompt template and hand-off step now require the lane report to live inside the worktree. Found by the acceptance run: a headless Sonnet session followed the skill correctly (atomic claim, one commit inside the write-set, sibling lane untouched, verify green, rebase before hand-off) but could not write a report to a path in the main checkout because worktree isolation blocks it.

## [fable-workflows 2.0.0] - 2026-09-01

### Added

- parallel-plans: splits one implementation plan into lanes with exclusive write-sets so several Claude Code sessions or worktree subagents can execute it at once without conflicts — a serial foundation lane (contracts, shared config) merged before fan-out, atomic lane claims via `git worktree add -b lane/<slug>/<lane>`, rebase-before-hand-off, and a serial integration lane that merges `--ff-only` in dependency order from the main checkout. Extends writing-plans; executes via executing-plans. Design: `docs/specs/2026-09-01-fable-pack-2-design.md` section 5.

### Changed

- using-git-worktrees: rewritten around the native harness path — `claude --worktree <name>` / `EnterWorktree` create `.claude/worktrees/<name>` on branch `worktree-<name>`, based on `worktree.baseRef` (`fresh` = remote default branch, `head` = current HEAD), `.worktreeinclude` copies gitignored files, isolation blocks edits and git in the main checkout. The `git worktree add` path stays as a shorter fallback section; the baseline-test step is unchanged.
- finishing-a-development-branch: trimmed; keeps the four-option menu, typed "discard", and merge-verify-remove order. Cleanup now delegates to `ExitWorktree` (keep/remove, `discard_changes` guard); the provenance check recognizes `.claude/worktrees/` as harness-owned; the final whole-branch review points at `/code-review` when available.
- brainstorming: "one question per message" replaced with batched `AskUserQuestion` rounds (up to 4 per round, one topic each, a recommended first choice), falling back to one-per-message only when the tool is unavailable. Per-section approval replaced with one design approval. When the design has 2+ independent components, they are now recorded as lane candidates for parallel-plans.
- writing-plans: Scope Check now mentions lanes, Execution Handoff gains a "Parallel lanes (parallel-plans)" option, and the plan header gets an optional `**Parallel:**` line.
- subagent-driven-development: the blanket "never dispatch implementation subagents in parallel" rule is now scoped — parallel implementers are allowed across lanes with disjoint write-sets (parallel-plans) or with `isolation: "worktree"`; final review may use `/code-review`.
- executing-plans: one line added — inside a lane, the plan's write-set bounds every edit.
- test-driven-development: trimmed toward ~120 lines, keeping the Iron Law, red/green verification, mock rules, and exceptions; rationalization tables and duplicated debugging text cut.

### Removed

- requesting-code-review: covered by the built-in `/code-review` command and by subagent-driven-development's Task Reviewer.

## [fable-agents 2.0.0] - 2026-09-01

### Removed

- golang-pro, java-pro, rust-pro, python-pro: all four scored 1.00/1.00 on both Sonnet and Opus in the 2026-09-01 blind audit — the remaining value was a generic "expert" role prompt the model already produces on its own. python-pro was flagged as the maintainer's most-used language and a legitimate case for keeping as a role prompt, but removed by the same bar applied to the other three.

### Fixed

- bash-pro: corrected Bash version gating for modern features — `EPOCHREALTIME`/`EPOCHSECONDS` are Bash 5.0 (was misattributed to 5.2); `${var@U}`/`${var@u}`/`${var@L}` case conversion and the associative-array improvements are 5.1 (was misattributed to 5.0); `varredir_close` is 5.2. Dropped the claim of "improved exec error handling" (matches no Bash NEWS entry). Source: Bash NEWS file.

## [fable-mobile 1.0.0] - 2026-09-01

### Added

- New plugin: ios-icon-gen, swift-concurrency-6-2, ios26-liquid-glass, apple-foundation-models, wcag22-reference (5 skills), moved from fable-knowledge unchanged except the fix below. Pairs with the official `expo` plugin and rcosteira79/android-skills for Android content.

### Fixed

- wcag22-reference: SwiftUI has no `accessibilityLiveRegion` modifier (Apple's documentation index 404s on it) — replaced with the `updatesFrequently` trait for continuously changing values and `AccessibilityNotification.Announcement` (iOS 17+) / `UIAccessibility.post(.announcement)` for one-off announcements.

## [fable-web 1.0.0] - 2026-09-01

### Added

- New plugin: angular-developer, nextjs-turbopack, pm2-node-services, html-slides, playwright-demo-videos, prisma-patterns (6 skills), moved from fable-knowledge unchanged.

## [fable-integrations 1.0.0] - 2026-09-01

### Added

- New plugin: x-api, jira-integration, nutrient-api, free-tier-scraper-apis, mcp-server-configs, mailtrap-email-integration, laravel-plugin-discovery, codehealth-mcp, claude-devfleet, agent-payment-x402, n8n-selfhosted-ops (11 skills), moved from fable-knowledge unchanged except the fixes below.

### Fixed

- n8n-selfhosted-ops: "credential re-linking cannot be automated via CLI" was wrong — `n8n import:credentials --input=<file>` preserves ids, so nodes re-link automatically (keep `--decrypted` on export across instances with different encryption keys). Source: docs.n8n.io CLI page.
- x-api: default tweet fields (no `tweet.fields` expansion) are `id`, `text`, and `edit_history_tweet_ids` (since Sept 2022), not just `id`/`text`. Source: docs.x.com data dictionary.

## [fable-media 1.0.0] - 2026-09-01

### Added

- New plugin: fal-ai-media, videodb, ffmpeg-media-recipes (3 skills), moved from fable-knowledge unchanged.

## [fable-niche 1.0.0] - 2026-09-01

### Added

- New plugin: kotlin-ktor, kotlin-exposed, perl-modern, cpp-core-guidelines, tinystruct-patterns, flox-environments, uncloud, windows-desktop-e2e, gget, uspto-database, defi-amm-security (11 skills), moved from fable-knowledge unchanged except the fixes below.

### Fixed

- kotlin-ktor: StatusPages handler selection is by nearest class in the exception hierarchy (`selectNearestParentClass`), not `install`-block order — identical in Ktor 1.x through 3.5.2. Source: ktor-server-status-pages `StatusPages.kt`.
- perl-modern: a plain nested read (`$h->{a}{b}`) autovivifies every intermediate level — only the final key stays unset, contrary to the "no autovivification on read" claim. Noted the `no autovivification` pragma (CPAN) as the opt-out. Source: Perl 5.38.2, live interpreter.

## [fable-knowledge] - 2026-09-01 - removed

### Removed

- The plugin is removed from the marketplace. Its 36 remaining skills moved unchanged (bar the fixes above) into five domain plugins — fable-mobile, fable-web, fable-integrations, fable-media, fable-niche (see their 1.0.0 entries above) — so a single-project machine installs only the domains it needs. 11 skills were dropped outright as model-known rather than moved: clickhouse, database-migrations, evm-gotchas, manim-explainers, nuitka-windows-packaging, nuxt4-patterns, postgres-tips, bun-runtime, pubmed-database, react-performance, remotion (all scored 1.00/1.00 on both Fable and Sonnet in the blind audit; see `docs/audits/2026-09-01-model-relevance-audit.md`). Installed fable-knowledge 1.0.0 caches keep working but never update — uninstall it and install the domain plugins you use (README has the full skill-to-plugin migration table).

## [fable-workflows 1.3.0] - 2026-08-22

### Added

- fact-guard: stops invented client facts (names, prices, codes, contacts) from reaching deliverables. Three rules — placeholder instead of a plausible guess (collected into a «Что нужно от вас» list), the project's facts file beats memory (proposes `docs/facts.yaml` at the first real question), and a `known-fabrications.md` ledger with a BLOCKLIST → TRACE → VERDICT check before delivery (inline up to ~2 pages, subagent beyond). Generalizes the ledger + guard pattern one project had built by hand after 15 hallucinated facts; the same failure class was documented in two more projects. The only idea adopted from a triage of nick-vels/skills (autopilot) — its rule "a fact about the user is never invented" — after a critical review refuted the other six candidates (requirements manifest, context handoff, SDD upgrades, secrets skill, Unity knowledge, acceptance protocol) for lack of any documented failure they would fix.

### Changed

- writing-plans, verification-before-completion: one cross-reference line each to fact-guard (client-fact placeholders are mandatory; fact claims are a different gate from status claims).

## [fable-guard 0.5.0] - 2026-08-22

### Added

- Four secret patterns: Telegram bot token, Stripe live key (`sk_live_`/`rk_live_`; test keys deliberately allowed), JWT (three base64url segments), connection string with an embedded password (postgres/mysql/mongodb/redis/amqp). Eleven new test cases, paired positive/negative per pattern.

## [fable-workflows 1.2.0] - 2026-08-05

### Added

- kb-hygiene: navigability pass over document folders (notes, research, transcripts, briefs) so an agent can decide read/skip without opening files. Built from a real pass over two bases and corrected by a critical review of that pass, which refuted the obvious approach: hand-annotating every file. The skill's gate is the title-content test - a note named after its topic (`03-multiorders.md` -> `# 03. Multiorders`) already carries its preview in the filename plus H1, and a generated index extracts it for free; a transcript named after its event (`club-session-july-01_729900291.txt`) hides which tools, numbers and conclusions are inside, and only there does a hand-written header add information. Default deliverable is therefore a regenerable index, not prose. Includes: folder classification table (vault / index-only / code / skill-repo, with source trees forbidden), input/output split restricted to pipelines with an external data source, a mandatory reversal check before any bulk write on an unversioned folder, and a dated staleness marker with the rule that an existing header is a claim, not evidence.

## [fable-workflows 1.1.0] - 2026-07-26

### Added

- 3 skills adapted from BuilderIO/skills (MIT) after an 11-skill triage with an adversarial review pass; all rewritten into the pack's hard-rule format (Iron Law, red flags, rationalization tables):
  - docs-first (renamed from read-the-damn-docs): docs-before-code gate for external contracts — authority hierarchy (local repo > official docs > registry metadata > source), version-verification workflow, boundary with getting-unstuck.
  - stay-within-limits: usage-window management for long agent runs — 95% stop rule, measure-between-waves loop, self-sufficient wake prompts, ccusage staleness caveat, boundary with solution-hunter Stage 1 (one pause convention, not two).
  - agent-watchdog: audit of unattended agent runs from artifacts only (session/cron/PR/log) — contract reconstruction, evidence-classed gap report (Gap/Bug/Verification miss/Scope drift), narrow authorized fixes; boundary with subagent-driven-development's Task Reviewer.

### Changed

- writing-plans: added "Choosing Between Defensible Directions" — 5-step tie-break order salvaged from BuilderIO's plan-arbiter (the rest of that skill was skipped as below the bar).

Skipped in the same triage: rewind (macOS Clips-locked), visual-plan/visual-recap (hosted-connector-locked), efficient-fable/efficient-frontier (triple-redundant with model-economy rules and subagent-driven-development), plow-ahead, quick-recap, plan-arbiter. Rationale recorded in ATTRIBUTIONS.md.

## [fable-agents 1.2.0] - 2026-07-26

### Added

- quant-critic: refute-first reviewer for crypto backtest/strategy claims (22nd agent, first original one). Distilled from a 6-round algo-research hunt (49 ideas, 43 refuted by executed backtests): 9 mandatory checks with measured reference numbers — funding-resample look-ahead (label='left' fabricated +53%/yr), fees-only cost floor 10–16 bps vs 0.1–5 bps directional predictability at 1–3m, fill/knife/untouched triple (93.5% of pullback-limit fills were knives), EW-rebalance compounding artifact (~σ²/2/period), funding settlement vs accrual, liquidation path on mark price, point-in-time universe, Bonferroni over everything tried, hold-out hygiene, capacity in $/yr. Mandatory PASS/FAIL/NOT-RUN/N-A report schema makes skipped checks visible; NOT-RUN on a load-bearing check blocks a CANDIDATE verdict. Draft was adversarially reviewed (26 findings, all triaged and applied) before release.

## [fable-agents 1.1.1] - 2026-07-26

### Fixed

- 12 factual errors found by a post-release adversarial fact-check across 9 agents:
  - kubernetes-architect: QoS rule was inverted — the risky case is request-without-limit (unbounded growth, OOMKills neighbors); limit-without-request is auto-defaulted to request=limit by Kubernetes. "Consolidation" reattributed to Karpenter (cluster-autoscaler does scale-down).
  - python-pro: a plain `except Exception` does catch a TaskGroup's `ExceptionGroup` (it subclasses Exception) — `except*` adds selective unpacking, not catchability; the mutable-default ban is dataclass's own rule, independent of `slots=True`. Both reproduced on a live interpreter.
  - java-pro: `-XX:+FlightRecorder` is a deprecated no-op since JDK 13 — replaced with `-XX:StartFlightRecording`; `synchronized` carrier-thread pinning is fixed by JEP 491 in JDK 24+, so the ReentrantLock advice is now version-gated to 21–23.
  - backend-architect: "never retry on 4xx" corrected — 429 is designed to be retried with `Retry-After` (RFC 6585) and every major SDK does.
  - deployment-engineer: pipeline gates reordered to build → scan → sign — the signature must attest to a scanned artifact (was sign-before-scan, contradicting the file's own principle).
  - terraform-specialist: S3 backend has native locking since Terraform 1.10 (`use_lockfile`), S3+DynamoDB marked legacy; Terraform Cloud renamed to HCP Terraform; noted HCP is not applicable to OpenTofu.
  - database-admin: an idle-in-transaction session holds the xmin horizon and blocks vacuum database-wide, not just on tables it touched (the original understated the blast radius).
  - database-optimizer: `INCLUDE` converts an `Index Scan` into an `Index Only Scan`; residual `Heap Fetches` on an existing Index Only Scan are a visibility-map/VACUUM issue (the original had the mechanism backwards).
  - database-architect: Bigtable has no per-query tunable consistency — attribute narrowed to Cassandra/ScyllaDB.

## [repo] - 2026-07-26

### Fixed

- README "no executable code" badge corrected to "guard hooks only" — fable-guard ships executable PreToolUse hooks, as the Security Model section already stated.
- ATTRIBUTIONS.md brought up to date: 11 of 15 workflows skills adapted (4 original), 46 of 47 knowledge skills from ECC (n8n-selfhosted-ops original), 21 agents.
- CONTRIBUTING.md line limit aligned with the enforced validator value (800, was stale 500).
- validate.py rejects multiline YAML descriptions (the parser reads one line, so the 400 cap was silently bypassable); cap error message no longer claims listing truncation is length-driven — observed harness behavior hides some short descriptions while showing longer ones, so the cap is hygiene, not a guaranteed fix for hidden triggers.
- fable-agents 1.1.0 entry corrected below: the description cap shipped at 400 chars (three descriptions sit at 300–330), and most rewritten agents carry decision rules in prose rather than command blocks.

## [fable-agents 1.1.0] - 2026-07-25

### Changed

- All 19 remaining laundry-list agents rewritten to the operational standard set by bash-pro and incident-responder: decision rules with rationale, counterintuitive gotchas, and review checklists replace capability walls (commands and tables where they earn their place). Line counts roughly halved (e.g. backend-architect 301->80, database-architect 263->114, observability-engineer 235->80); every description rewritten as a distinct router trigger under the 400-char cap. Key Distinctions blocks kept throughout; cross-file topic ownership deduplicated (GitOps in kubernetes-architect, state ops in terraform-specialist, rollout strategy in deployment-engineer, FinOps in cloud-architect).

## [fable-guard 0.4.0] - 2026-07-25

### Added

- scripts/test_guard.py: 27 deterministic tests for both hooks (secrets, dangerous shell, fail-open, stale-map scenarios in throwaway git repos); wired into CI alongside validate.py.

### Fixed

- guard.py now scans NotebookEdit new_source (matcher extended to Write|Edit|NotebookEdit).
- stale_map.py: git-quoted paths (spaces/non-ASCII) no longer misclassified as code changes; rename entries resolve to the new path.

## [fable-workflows 1.0.1] - 2026-07-25

### Fixed

- solution-hunter and critical-review descriptions trimmed under the new 400-char limit (long descriptions get truncated in the harness skill listing, hiding the Russian triggers); all triggers preserved.

## [fable-marketing 0.2.1] - 2026-07-25

### Fixed

- offers, revops, customer-research descriptions trimmed under the 400-char limit; trigger keywords preserved.

## [repo] - 2026-07-25 (second pass)

### Added

- validate.py: descriptions capped at 400 chars (harness listing truncation guard); CI runs test_guard.py.

## [fable-workflows 1.0.0] - 2026-07-25

### Removed

- dispatching-parallel-agents: duplicated what the harness already tells the model via the Agent tool; its one non-obvious rule (parallel dispatch only for fully independent work with no shared state) moved into subagent-driven-development, resolving the previously unstated contradiction between the two skills.

### Fixed

- systematic-debugging: removed the fabricated "Real-World Impact" statistics (15-30 min vs 2-3 h, 95% vs 40% fix rates) - unsourced numbers violated the pack's measured-numbers bar.
- test-driven-development: "No exceptions" label renamed to "No exceptions without asking" (was contradicted by the Exceptions section two paragraphs above).
- brainstorming: removed the Key Principles section (near-verbatim duplicate of the checklist); the unique YAGNI bullet merged into the checklist.

## [fable-knowledge 1.0.0] - 2026-07-25

### Removed

- regex-llm-hybrid: an architecture pattern a frontier model derives on its own; its "98% success" metrics were a single-run anecdote presented as a benchmark.

### Changed

- Generic-content cuts to meet the pack's own bar: cpp-core-guidelines 554->114 lines (kept testing/tooling and an 8-rule counterintuitive table, dropped the guidelines retelling), perl-modern 542->36 (version-gated feature table + legacy-to-modern mapping), react-performance 291->136 (version-specific and counterintuitive rules only, "70+ rules" claim dropped), kotlin-ktor 375->132 (gotchas foregrounded, boilerplate cut); trims in nuxt4-patterns (generic SSR block), postgres-tips (upsert), html-slides (preset catalog compressed), manim-explainers (storytelling advice), pubmed-database (When to Use); nextjs-turbopack hedges replaced with direct facts (Next 16 builds with Turbopack by default, --webpack to opt out).
- Staleness guards added to churn-prone tables: fal-ai-media app_ids, free-tier-scraper-apis Gemini limits, mcp-server-configs pins, uncloud CLI surface, kotlin-exposed dependency pins, videodb capture, nuitka measured tables, x-api base domain.

### Fixed

- uspto-database: search.patentsview.org was retired 2026-03-20 (host no longer resolves) - workflow now points at the data.uspto.gov Open Data Portal migration with the transition guide.
- n8n-selfhosted-ops: sendAndWait issues #13331/#15492 verified closed "not planned" on n8n 2.31 (July 2026) - the HITL workaround remains necessary.
- ffmpeg-media-recipes: example switched to eleven_flash_v2_5 (ElevenLabs' current recommendation over the equivalent-but-slower turbo).
- agent-payment-x402: agentwallet-sdk pin 6.0.0 -> 6.2.1 (verified on npm); ERC-4337 wallet claim softened (x402 commonly uses plain EOA EIP-712/EIP-3009 signatures).
- mcp-server-configs / jira-integration: the deliberate mcp-atlassian 0.21.0 pin annotated (0.23.0 current; later releases renamed tools).
- claude-devfleet: 600 s default timeout flagged as unverified against the current README.

## [fable-agents 1.0.0] - 2026-07-25

### Removed

- sql-pro: merged into database-optimizer (bodies overlapped almost entirely; the distinct analytical-SQL material was absorbed, description now covers advanced SQL triggers).
- devops-troubleshooter: merged into incident-responder (same domain without operational rules; a compact debugging-toolkit section was absorbed).

### Changed

- deployment-engineer: model haiku -> sonnet - SLSA/SBOM/compliance and zero-downtime strategy content is judgment work, not mechanical (was the pack's one tier-policy violation).
- Version refresh across specialists: Rust 1.85+ (2024 edition), Go 1.24+, Java 21/25 LTS, Python 3.13+, Next.js 16 in frontend-developer (now consistent with the nextjs-turbopack skill); dated "2024/2025" phrasing removed from code-reviewer, observability-engineer, python-pro.
- Key Distinctions blocks added to the infrastructure cluster (cloud-architect / kubernetes-architect / terraform-specialist / deployment-engineer) and reliability cluster (incident-responder / observability-engineer / performance-engineer); code-reviewer now defers security-audit depth to security-auditor.
- test-automator: TDD sections removed - the methodology lives in the fable-workflows test-driven-development skill (was a second source of truth).
- Final model split: 7 opus / 14 sonnet.

## [fable-marketing 0.2.0] - 2026-07-25

### Fixed

- churn-prevention: the FTC Click-to-Cancel rule was presented as in force; corrected - struck down by the 8th Circuit in 2025, while state laws (e.g. California auto-renewal) still require easy cancellation.

### Changed

- Unsourced benchmark clusters dated and qualified: revops speed-to-lead 21x (InsideSales ~2007-2011, never re-validated), ads "Andromeda era" figures (practitioner-reported, not Meta-published), ai-seo and directory-submissions AI-citation stats (2024-2025 studies), aso +5.9% CPP lift (industry estimate, not Apple-published), sms TCPA settlement range (historical).
- seo-audit: title/meta character counts marked as approximations of Google's pixel-width truncation.
- ads: Creative Best Practices compressed to a pointer at ad-creative (body now honors the declared boundary); directory-submissions: duplicate 2.8x stat removed, schema table defers to ai-seo.
- copy-editing: compressed 153->112 lines - sweeps reformatted as checklists, arbitrary expert-panel scoring removed, replacement tables kept in full.

## [fable-guard 0.3.0] - 2026-07-25

### Fixed

- guard.py secret patterns: OpenAI project keys (sk-proj-/sk-svcacct-/sk-admin-) were not caught (the classic sk- regex stops at the hyphen); Slack xoxc/xoxe tokens added.
- guard.py shell patterns: now blocks `sh <(curl ...)` process substitution, `sh -c "$(curl ...)"` / `eval "$(curl ...)"` command substitution, and zsh/dash/fish pipe variants.
- `--dangerously-skip-permissions` now blocks only within a claude invocation - no more false positive on commit messages that merely mention the flag.
- Docstring updated to the actual JSON permissionDecision protocol (previously described the old exit-2 protocol).

## [repo] - 2026-07-25

### Changed

- validate.py: maintainer skills in .claude/skills/ are now validated and counted.
- release skill: mandatory README-update step added (badge counts, plugin lists, What's new) - the missing step was the root cause of README drifting from releases.
- freshness-sweep: rotation list updated for removed/renamed content.

## [fable-workflows 0.6.0] - 2026-07-25

### Added

- solution-hunter: continuous solution-search loop - subagent generators with rotating lenses, combinator, three adversarial critics (hostile-skeptic / pre-mortem / data-contradiction) executing evidence checks, file-anchored state (BRIEF/STATE/LEDGER/STATUS) in research/<slug>/, anti-stagnation via getting-unstuck, budget guards (rounds/day, total, auto-pause on silence). Stage 0 (round on demand) is the default; Stage 1 (autonomous /loop wakeups) is gated behind four calibration gates (cost, verification yield, dedup on paraphrases, critic divergence) - all four passed on a live smoke round (9.5 min, ~350K subagent tokens, demo hunt found and bit-exact-verified a 37% compression win). Russian triggers in description ("ищи варианты нон-стоп", "перебирай идеи", "не останавливайся пока не найдёшь").

## [fable-workflows 0.5.0] - 2026-07-24

### Added

- critical-review: fresh-eyes re-examination of existing materials to find what was missed - stale assumptions, blind spots, contradictions with own data, dismissed alternatives. Four phases (claim inventory with evidence/freshness/load classification, mandatory 7-lens pass, evidence-only verification with written log, impact-ranked report). Russian triggers in description ("подумай", "посмотри под другим углом", "что мы упускаем"). Complements getting-unstuck: that skill breaks declared dead ends, this one hunts blind spots when nothing is visibly wrong; confirmed blocked opportunities route into getting-unstuck.

## [fable-workflows 0.4.0] - 2026-07-21

### Changed

- getting-unstuck: added written experiment-log template (per-hypothesis block with test, timebox, verdict, new-fact line) and a loop limit - two consecutive generation rounds with no new distinct hypothesis force the Phase 4 verdict, preventing the skill from becoming an endless rabbit hole.
- systematic-debugging: cross-triggers into getting-unstuck at the two natural impasse points - the "3+ fixes failed, question architecture" step and the "no root cause found" section - so the dead-end process fires exactly where tunnel vision peaks.

## [fable-workflows 0.3.0] - 2026-07-21

### Added

- getting-unstuck: critical-thinking process for apparent dead ends. Iron law: no "impossible" without a verified constraint and 3+ tested hypotheses. Four phases (interrogate the wall, generate hypotheses, evidence-only testing ranked by cost-to-test, verdict with experiment log), hypothesis-generation moves table, rationalization table. Security/permission boundaries and explicit user decisions are declared out of scope - never walls to bypass.

## [fable-workflows 0.2.0] - 2026-07-21

### Added

- project-cartography: living three-file project map (CODEMAP.md, PROJECT_STATE.md, DECISIONS.md) with scaffold templates, update rules, and hard size limits. Design principle: the map serves the model, never commands it - what counts as substantive stays a judgment call.

### Changed

- brainstorming, writing-plans, executing-plans descriptions now point to the next stage in the lifecycle chain (and to project-cartography where relevant).

## [fable-guard 0.2.0] - 2026-07-21

### Added

- Stop hook (stale_map.py): when a project keeps CODEMAP.md and code changed but no map file did, blocks the stop exactly once with a soft reminder; stop_hook_active guards against loops, fail-open on all errors, silent outside mapped projects.

## [fable-guard 0.1.0] - 2026-07-21

### Added

- New opt-in plugin with PreToolUse hooks: blocks secret patterns (Anthropic/OpenAI/GitHub/AWS/Google/Slack keys, private key material) in Bash commands and Write/Edit content, plus dangerous shell patterns (curl|sh, wget|sh, --dangerously-skip-permissions). Single dependency-free Python script, JSON permissionDecision protocol, fails open on malformed input. The four content plugins remain markdown-only; the security model is documented in README.

## [fable-knowledge 0.3.0] - 2026-07-21

### Added

- n8n-selfhosted-ops: operating self-hosted n8n (npm/systemd) - CLI workflow import without an API key, systemd EnvironmentFile for {{$env.*}} expressions, credential re-linking after import, webhook HTTPS requirements, and the Telegram HITL pattern avoiding the broken sendAndWait node (original content, verified on n8n 2.8).

## [repo] - 2026-07-21

### Added

- validate.py: agents must declare an explicit model tier (haiku/sonnet/opus); relative links in all .md content are checked for existence.
- Maintainer skills in .claude/skills/: release (versioned release procedure) and freshness-sweep (monthly staleness check playbook for version-fragile skills).

## [fable-agents 0.2.0] - 2026-07-21

### Changed

- Explicit model tier on all 23 agents (no agent inherits the orchestrator's model anymore). Coding specialists (golang-pro, java-pro, python-pro, rust-pro) moved from opus to sonnet; the six agents without a model field (backend-architect, database-optimizer, frontend-developer, observability-engineer, performance-engineer, sql-pro) set to sonnet. Final split: 7 opus (architecture, review, security), 15 sonnet, 1 haiku.
- README: documented the model policy — cheapest model that does the job well; orchestrator delegates mechanical skill work to lower tiers.

## [0.2.0] - 2026-07-21

Repository restructured from a single-plugin pack (`fable-skills`) into the `fable-pack` marketplace with four independently installable plugins.

### Added

- **fable-agents** (new plugin, 23 subagents) — selected from ~745 agents in wshobson/agents (MIT). Language specialists (python, rust, go, java, sql, bash), review and security audit, infrastructure (kubernetes, terraform, cloud, CI/CD, databases), incident response and observability, frontend and test automation. Shallow stubs and pack-coupled orchestrators were rejected.
- **fable-workflows** (new plugin, 12 skills) — adapted from obra/superpowers (MIT). TDD with the Iron Law and rationalization tables, four-phase systematic debugging, brainstorming, plan writing and execution, verification before completion, git worktrees, subagent-driven development, code review in both directions, branch finishing, parallel agent dispatch. Superpowers-specific plumbing (hooks, scripts, cross-skill invocations) removed; methodology tables kept verbatim.
- **fable-marketing** (new plugin, 20 skills) — triaged from 47 skills in coreyhaines31/marketingskills (MIT), 43% keep rate. Kept only skills with concrete numbers and templates: cold-email reply-rate benchmarks, GEO/AI-SEO citation data, A2P 10DLC compliance, ab-testing sample-size tables, pricing frameworks, programmatic SEO playbooks. Generic advice (copywriting basics, psychology bias catalogs) dropped.
- **fable-knowledge**: 18 new skills from re-triage of ECC at 278 skills (269 candidates reviewed, ~7% keep rate): agent-payment-x402, angular-developer, claude-devfleet, codehealth-mcp, flox-environments, nextjs-turbopack, mailtrap-email-integration, laravel-plugin-discovery, ios-icon-gen, nuitka-windows-packaging, prisma-patterns, uncloud, react-performance, tinystruct-patterns, pubmed-database, uspto-database, gget, windows-desktop-e2e.
- Repository tooling: `scripts/validate.py` (structure, frontmatter, size, emoji checks), GitHub Actions CI, issue templates for content requests and outdated-information reports, CONTRIBUTING.md, ATTRIBUTIONS.md, MIT LICENSE.

### Changed

- Marketplace renamed `fable-skills-marketplace` to `fable-pack`; plugin `fable-skills` renamed to `fable-knowledge` (version 0.2.0). Existing 29 skills moved unchanged to `plugins/fable-knowledge/skills/`.

## [0.1.0] - 2026-07-21

### Added

- Initial `fable-skills` plugin: 29 knowledge-only skills distilled from everything-claude-code (183 skills reviewed). Selection principle: only knowledge a strong model would otherwise hallucinate.
