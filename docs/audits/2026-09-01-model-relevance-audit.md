# Model-relevance audit of fable-pack (2026-09-01)

Question asked by the maintainer: the orchestrator model got smarter (Claude Fable 5.1, knowledge cutoff June 2026). Which skills still earn their place, which have become ballast, what must change, and what is missing for the next project (Replyvo mobile app: Expo + native Kotlin/Swift modules).

Method, findings, verdicts and open decisions are below. Raw material (questions, blind answers, grades, dispute resolutions) lives in the session scratchpad `quiz/` directory; this document keeps only the results.

## 1. Method

Reading a skill and asking "do I know this?" is contaminated: once read, everything feels familiar. So the audit ran a blind quiz:

1. Sonnet subagents extracted 3–5 load-bearing questions per file (exact flags, versions, thresholds, gotchas; nothing that already appears in the frontmatter description): 193 questions for 47 knowledge skills, 60 for 20 marketing skills, 68 for 22 agents.
2. The questions were answered closed-book by headless sessions with no tools and no skills (`claude -p --disable-slash-commands --tools ""`): knowledge and marketing on `claude-fable-5-1`, knowledge again on `claude-sonnet-5` (the tier this pack's subagents run on), agents on `claude-sonnet-5` and `claude-opus-5` (the tiers agents run on). UNKNOWN was allowed and rewarded over guessing.
3. Sonnet graders scored each answer CORRECT / PARTIAL / WRONG / UNKNOWN against the file; score = (correct + 0.5·partial)/n. Confident contradictions (WRONG at confidence ≥70) were flagged as disputes.
4. Every dispute was resolved against primary sources (official docs, NEWS files, shipped source, a live Perl interpreter).

Limits: n = 3–5 questions per file, so a 1.00 means "the model knows the facts the extractor judged load-bearing", not "knows everything in the file". Workflow skills are methodology, not facts, and were judged by reading, not quizzed.

## 2. Findings that change decisions

**F1. Disputes went 7:0 against the files.** Every confident disagreement between the blind model and a skill/agent file was resolved in the model's favour:

| Dispute | Verdict | Evidence |
|---|---|---|
| kotlin-ktor: StatusPages handlers match in install order | SKILL-WRONG | `findHandlerByValue` filters all matching keys and calls `selectNearestParentClass`; identical in Ktor 1.x, 2.x, 3.x (3.5.2) |
| x-api: default tweet fields are only `id`, `text` | SKILL-OUTDATED | Data dictionary: defaults are `id`, `text`, `edit_history_tweet_ids` (since Sept 2022) |
| bash-pro: `EPOCHREALTIME` is a Bash 5.2 feature | BOTH-PARTIAL | NEWS: `EPOCHREALTIME`/`EPOCHSECONDS` are 5.0; `varredir_close` is 5.2; "improved exec error handling" matches no NEWS entry |
| bash-pro: `${var@U}`/`@L` and assoc-array improvements are Bash 5.0 | AGENT-WRONG | NEWS: all under bash-5.1 |
| n8n-selfhosted-ops: credential re-linking cannot be automated via CLI | SKILL-WRONG | `n8n import:credentials --input=<file>` is documented; ids are preserved, so nodes re-link |
| perl-modern: a plain read of `$h->{a}{b}` never autovivifies | SKILL-WRONG | Perl 5.38.2: the read creates `$h->{a} = {}`; `autovivification` pragma docs confirm |
| wcag22-reference: SwiftUI live region is `.accessibilityLiveRegion(.polite)` | SKILL-WRONG | No such API: Apple docs index returns 404 for `View/accessibilityLiveRegion(_:)`; the real primitives are the `updatesFrequently` trait (iOS 13+) and accessibility announcements |

Consequence: a skill whose facts the model already knows is not neutral. It costs context, and where it is wrong it overrides a correct model. Removal of model-known skills is a correctness measure, not only a cost one.

**F2. The skill listing was silently truncated.** Claude Code injects skill descriptions into the system prompt under a budget of 1% of the model's context window and drops descriptions of the least-invoked skills first (skills docs, "listing budget"). With 87 pack skills plus built-ins, a fresh `fable[1m]` session listed 25 skills by name only, 17 of them from fable-workflows (the router could not see triggers like «подумай»). Fix applied and verified on 2026-09-01: `"skillListingBudgetFraction": 0.02` in `~/.claude/settings.json`; a fresh session now shows all 106 descriptions (0 name-only). `skillOverrides` cannot help here: it does not apply to plugin skills. The earlier memory note that "descriptions are hidden regardless of length" was a misreading of the same mechanism (cumulative budget, usage-ordered).

**F3. Sonnet 5 still needs skills Fable does not.** Knowledge quiz, question-weighted over all 193 questions: Fable 0.86, Sonnet 0.64. Extreme case: angular-developer, Fable 1.00 vs Sonnet 0.00. The pack's subagents run on Sonnet and load plugin skills, so "Fable knows it" alone is not sufficient grounds for removal.

**F4. Marketing numbers are genuinely absent from the model.** 27 of 60 marketing answers were honest UNKNOWN; mean score 0.47; only aso (1.00), ad-creative and sms (0.83) are largely known. The pack's benchmark tables are doing real work.

**F5. Agents: facts known, roles still useful.** Sonnet 0.77 / Opus 0.84 question-weighted; 12 of 22 agents scored 1.00 on both tiers. The value that remains in those files is the review rubric and decision tables, not the facts. Weak spots that do carry unknown facts: quant-critic (0.00/0.33), incident-responder (0.25/0.25), bash-pro (0.25/0.38, two factual errors), architect-review (0.33/0.33).

## 3. Per-skill scores

Knowledge (Fable / Sonnet). HIGH = number of quiz facts tied to versions or endpoints likely to drift.

| Skill | Lines | Fable | Sonnet | HIGH | Verdict |
|---|---|---|---|---|---|
| angular-developer | 49 | 1.00 | 0.00 | 0 | keep (Sonnet) |
| apple-foundation-models | 177 | 1.00 | 1.00 | 0 | keep, refresh at iOS 27 GA (8,192-token context, Vision) |
| clickhouse | 112 | 1.00 | 1.00 | 0 | remove |
| database-migrations | 161 | 1.00 | 1.00 | 0 | remove |
| defi-amm-security | 142 | 1.00 | 0.75 | 0 | keep (Sonnet) |
| evm-gotchas | 184 | 1.00 | 1.00 | 0 | remove |
| ios26-liquid-glass | 218 | 1.00 | 0.75 | 3 | keep (Sonnet), refresh at iOS 27 GA |
| kotlin-exposed | 292 | 1.00 | 0.60 | 2 | keep (Sonnet) |
| manim-explainers | 29 | 1.00 | 1.00 | 0 | remove |
| nextjs-turbopack | 39 | 1.00 | 0.75 | 1 | keep (Sonnet) |
| nuitka-windows-packaging | 191 | 1.00 | 1.00 | 1 | remove |
| nutrient-api | 129 | 1.00 | 0.50 | 0 | keep (Sonnet) |
| nuxt4-patterns | 67 | 1.00 | 1.00 | 0 | remove |
| postgres-tips | 75 | 1.00 | 1.00 | 0 | remove |
| pubmed-database | 118 | 1.00 | 1.00 | 1 | remove |
| react-performance | 136 | 1.00 | 1.00 | 0 | remove |
| remotion | 90 | 1.00 | 1.00 | 0 | remove |
| uspto-database | 101 | 1.00 | 0.75 | 2 | keep (Sonnet) |
| prisma-patterns | 328 | 0.90 | 0.80 | 1 | keep, trim |
| bun-runtime | 65 | 0.88 | 1.00 | 0 | remove (borderline) |
| cpp-core-guidelines | 114 | 0.88 | 0.88 | 0 | keep |
| ffmpeg-media-recipes | 111 | 0.88 | 0.75 | 1 | keep |
| playwright-demo-videos | 172 | 0.88 | 0.75 | 0 | keep |
| videodb | 105 | 0.88 | 0.00 | 1 | keep |
| uncloud | 270 | 0.80 | 0.00 | 2 | keep |
| windows-desktop-e2e | 367 | 0.80 | 0.90 | 0 | keep, trim |
| fal-ai-media | 139 | 0.75 | 0.50 | 0 | keep |
| gget | 88 | 0.75 | 0.75 | 0 | keep |
| ios-icon-gen | 110 | 0.75 | 0.75 | 0 | keep |
| jira-integration | 154 | 0.75 | 0.75 | 2 | keep |
| kotlin-ktor | 132 | 0.75 | 0.50 | 0 | keep, fix StatusPages claim |
| mailtrap-email-integration | 55 | 0.75 | 0.88 | 1 | keep |
| perl-modern | 36 | 0.75 | 0.75 | 0 | keep, fix autovivification claim |
| pm2-node-services | 74 | 0.75 | 0.75 | 0 | keep |
| swift-concurrency-6-2 | 134 | 0.75 | 0.50 | 0 | keep; add Swift 6.3 note |
| tinystruct-patterns | 203 | 0.75 | 0.25 | 1 | keep |
| wcag22-reference | 73 | 0.75 | 0.75 | 0 | keep, fix SwiftUI live-region cell |
| x-api | 162 | 0.75 | 1.00 | 1 | keep, fix default fields |
| free-tier-scraper-apis | 75 | 0.63 | 0.38 | 2 | keep, refresh Gemini table |
| n8n-selfhosted-ops | 65 | 0.63 | 0.75 | 1 | keep, fix import:credentials claim |
| codehealth-mcp | 54 | 0.62 | 0.00 | 0 | keep |
| flox-environments | 283 | 0.60 | 0.60 | 0 | keep |
| html-slides | 185 | 0.50 | 0.25 | 0 | keep |
| mcp-server-configs | 124 | 0.50 | 0.75 | 1 | keep |
| agent-payment-x402 | 128 | 0.38 | 0.12 | 0 | keep |
| laravel-plugin-discovery | 66 | 0.38 | 0.00 | 2 | keep |
| claude-devfleet | 49 | 0.25 | 0.00 | 0 | keep |

Removal rule used: both Fable and Sonnet ≥ 0.88 and no post-cutoff refresh planned. Eleven knowledge skills meet it (clickhouse, database-migrations, evm-gotchas, manim-explainers, nuitka-windows-packaging, nuxt4-patterns, postgres-tips, bun-runtime, pubmed-database, react-performance, remotion).

Agents (Sonnet / Opus):

| Agent | Sonnet | Opus | Verdict |
|---|---|---|---|
| backend-architect, database-admin, database-architect, database-optimizer, frontend-developer, golang-pro, performance-engineer, python-pro, rust-pro, security-auditor, terraform-specialist, test-automator | 1.00 | 1.00 | facts known; value left is the rubric. Propose removing the three language agents nobody here uses (golang-pro, java-pro, rust-pro); keep the rest as role prompts and cut their fact sections |
| deployment-engineer, kubernetes-architect | 0.83 | 1.00 | keep |
| observability-engineer | 0.83 | 0.83 | keep |
| cloud-architect, java-pro | 0.67 | 1.00 | keep / remove java-pro (see above) |
| code-reviewer | 0.67 | 0.67 | keep |
| architect-review | 0.33 | 0.33 | keep |
| bash-pro | 0.25 | 0.38 | keep, fix two Bash version claims, trim 292 lines |
| incident-responder | 0.25 | 0.25 | keep |
| quant-critic | 0.00 | 0.33 | keep (original methodology) |

Marketing (Fable): aso 1.00; ad-creative, sms 0.83; ai-seo, competitors, pricing, product-marketing, programmatic-seo, seo-audit 0.67; copy-editing, popups 0.50; customer-research, directory-submissions, offers, prospecting, revops 0.33; ads 0.17; ab-testing, churn-prevention, cold-email 0.00. Verdict: keep all; trim aso/ad-creative/sms to their tables.

## 4. Workflow skills (judged by reading against today's harness)

| Skill | Verdict | Reason |
|---|---|---|
| using-git-worktrees (181) | rewrite to ~70 lines | Harness owns this now: `claude --worktree`, EnterWorktree/ExitWorktree, `.claude/worktrees/`, `worktree-<name>` branches, `worktree.baseRef`, `.worktreeinclude`, isolation enforcement. The skill still defaults to `.worktrees/` and treats native tools as hypothetical |
| finishing-a-development-branch (221) | trim to ~120 lines | Keep the four-option menu and merge → verify → remove order; cleanup is ExitWorktree now; provenance check must recognise `.claude/worktrees/` |
| requesting-code-review (149) | remove | Built-in `/code-review` (levels, `--fix`, `--comment`, ultra) and subagent-driven-development's Task Reviewer cover it. receiving-code-review stays (no built-in equivalent) |
| brainstorming (97) | update rituals | "One question per message" and "approve each section" fight AskUserQuestion (up to 4 questions with options) and autonomous runs; batch questions, one approval; add the decomposition → parallel lanes hook |
| writing-plans (170) | extend | Scope Check suggests lanes for ≥2 independent components; Execution Handoff gets option 3 "parallel lanes" |
| subagent-driven-development (141) | extend | "Never dispatch implementation subagents in parallel" predates Agent `isolation: worktree`; parallel is safe with disjoint write-sets |
| executing-plans (57) | keep + one line | The per-lane executor; write-set bounds every edit |
| test-driven-development (244) | trim to ~120 | Iron law still needed; rationalization tables and mock lore are ballast |
| verification-before-completion (136) | keep, optional trim | Fresh-evidence gate and revert-to-prove-red still catch "should work now" |
| solution-hunter | keep; note future port to the Workflow tool | Heaviest ritual; the Workflow tool is its natural deterministic home |
| agent-watchdog, critical-review, docs-first, fact-guard, getting-unstuck, kb-hygiene, project-cartography, receiving-code-review, stay-within-limits, systematic-debugging | keep | Each fixes a documented failure mode with no built-in equivalent |
| parallel-plans (new) | add | See §6 |

## 5. Mobile: what exists, what to adopt

Local `/root/android-skills/` (cloned 2026-08-28) and a web sweep of ~40 candidates, evaluated against the pack bar (details in the session research report):

| Candidate | License | Verdict |
|---|---|---|
| rcosteira79/android-skills (21 skills, updated 2026-08-25) | MIT | adopt a subset (gradle/AGP 9, coroutines, flows, testing, debugging, source-search); it already absorbed chrisbanes, Meet-Miyani, aldefy, skydoves, android/skills |
| Drjacky/claude-android-ninja (36k lines) | Apache-2.0 | adapt narrowly: Android 17/API 37 migration, Play Integrity, AGP 9/R8 gotchas |
| dpconde/claude-android-skill | MIT | skip (stale pins: Kotlin 1.9, BOM 2024) |
| aldefy/compose-skill | MIT | skip (absorbed; only TV/motion is unique) |
| chrisbanes/skills | Apache-2.0 | skip (absorbed) |
| expo@claude-plugins-official (25+ skills: expo-module, eas-app-stores, eas-workflows, eas-simulator, expo-upgrade) | MIT | install; primary set for the Replyvo stack |
| conorluddy/ios-simulator-skill | MIT | adopt |
| kylehughes/apple-platform-build-tools plugin | MIT | adopt |
| twostraws/SwiftUI-Agent-Skill, AvdLee/SwiftUI-Agent-Skill | MIT | diff, adopt one |
| dpearson2699/swift-ios-skills | PolyForm Perimeter | skip (license) |
| rshankras/claude-code-apple-skills | MIT | skip bulk (self-declared unverified AI content) |
| `_drafts/android-overlay-a11y` (own, RU, 194 lines, sourced 2026-08-28) | — | strongest document found for its niche; keep as a project skill, translate/generalise later |

Post-cutoff platform facts verified 2026-09-01: Android 17 (API 37) GA 2026-06-16; Play requires targetSdk 36 for new apps/updates since 2026-08-31 (extension to 2026-11-01); Play Billing Library 8+ required since 2026-08-31, latest v9; AGP 9.4.0, Gradle 9.7.1, Kotlin 2.4.10, Compose BOM 2026.08.00; Material 3 Expressive components still experimental; iOS 27 / Xcode 27 still in beta (GA expected mid-September); Swift 6.3 stable since 2026-03-24 with Xcode 26.4; App Store requires Xcode 26 SDK since 2026-04-28; Foundation Models on iOS 27: 8,192-token on-device context, Vision input, Private Cloud Compute option.

Gaps no candidate fills (write ourselves): iOS share/keyboard extension via expo-apple-targets (App Groups, memory limit, activation rules); store-compliance calendar (Data safety, Accessibility declaration, PrivacyInfo.xcprivacy, AI-content reporting); subscriptions on Expo (StoreKit 2 / Play Billing 8–9 / RevenueCat); speech-to-text facts (expo-speech-recognition, SpeechAnalyzer, Gemini audio).

## 6. parallel-plans (new workflow skill, design)

Problem: one plan, several Claude Code sessions (or worktree subagents) on the same repo, no interference. Design (pre-approval):

- Lane = exclusive write-set (globs) + branch `lane/<slug>/<id>` + worktree `.claude/worktrees/<slug>-<id>` + depends_on + verify command + resources (ports, db names) + a self-sufficient lane prompt.
- Lane 0 (foundation, serial, merged before fan-out): contracts, shared config, lockfile, scaffolding, stubs. Lane Ω (integration, serial): merge in dependency order, full suite, cartography update, cleanup.
- Claim is atomic via git: `git worktree add ... -b lane/<slug>/<id> main` fails if the branch exists. Then EnterWorktree(path=...) so isolation enforcement is on.
- Sync by `git rebase main` at task boundaries; SendMessage / `notify_when_idle` optional.
- Hard rules: no lane writes outside its write-set; no fan-out before foundation is on main; no merge without rebase and green verify; contract changes are the user's decision.
- Gates: fewer than 2 disjoint lanes, foundation over a third of the work, or under an hour of work → use subagent-driven-development in one session instead.
- Executors: human sessions (primary), Agent `isolation: worktree` subagents, or agent teams (experimental) — same plan format.
- Edits elsewhere: brainstorming and writing-plans gain the lanes hook; subagent-driven-development drops the blanket ban on parallel implementers.

## 7. Single-project profile (Replyvo app)

Keep: expo plugin; android-skills subset; own overlay-a11y skill; fable-knowledge: ios-icon-gen, swift-concurrency-6-2, ios26-liquid-glass, wcag22-reference (apple-foundation-models only if an on-device mode appears); fable-workflows (all but kb-hygiene, solution-hunter, agent-watchdog, stay-within-limits, fact-guard); fable-guard; agents: code-reviewer, security-auditor, test-automator, frontend-developer, backend-architect, performance-engineer; ios-simulator + build-tools skills.

Not needed for that project: 41 of 47 knowledge skills, 16 of 22 agents, all of fable-marketing until launch (then aso, pricing, churn-prevention), genlab, taste-skill, impeccable, and four of the five cloned Android repos.

Mechanism: plugins install whole, and `skillOverrides` ignores plugin skills, so a lean install needs either domain-split plugins (fable-knowledge → mobile / web / data / media / integrations / niche) or a new fable-mobile plugin plus a project-local `.claude/agents/` with the six agents.

## 8. Open decisions

1. Reference model for the bar: remove only what both Fable and Sonnet know (proposed), or Fable-only.
2. Language agents (golang-pro, java-pro, rust-pro; python-pro?) — remove or keep as role prompts.
3. Pack structure for the single-project environment: domain-split fable-knowledge vs new fable-mobile plugin.
4. parallel-plans: executors and merge authority (integration session proposed), enable agent teams or not.
5. Whether the single-project environment is this server or a new one, and whether the app's landing/marketing lives there too.

## 9. Applied in this session

- `~/.claude/settings.json`: `skillListingBudgetFraction: 0.02` (verified: 0 name-only skills in a fresh session; backup in the session scratchpad).
- No pack files were changed; all verdicts above await the maintainer's decision.
