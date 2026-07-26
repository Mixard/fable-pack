# Changelog

All notable changes to this pack are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
