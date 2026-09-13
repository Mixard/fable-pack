<p align="center">
  <img src="assets/hero.svg" alt="fable-pack: curated plugin marketplace for Claude Code" width="100%">
</p>

<p align="center">
  <a href="https://github.com/Mixard/fable-pack/actions/workflows/validate.yml"><img src="https://github.com/Mixard/fable-pack/actions/workflows/validate.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-e3b341" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/skills-80-2b3242" alt="80 skills">
  <img src="https://img.shields.io/badge/subagents-18-2b3242" alt="18 subagents">
  <img src="https://img.shields.io/badge/executable_code-guard_hooks_only-2b3242" alt="executable code: opt-in guard hooks only">
</p>

A curated, license-clean plugin marketplace for Claude Code. We reviewed 1,000+ skills and agents from the most popular community packs and kept fewer than 10% — every survivor either contains knowledge a frontier model would otherwise hallucinate, or a battle-tested methodology with hard rules.

```
/plugin marketplace add Mixard/fable-pack
```

## What's new

| Date | Release | Highlights |
|------|---------|------------|
| 2026-09-14 | fable-workflows 2.1.0 | verification-before-completion: acceptance checks defined before the work, checks that can actually fail (positive control, measured numbers), abandoned is not done, final reconciliation against the original request — four ideas from a Leonxlnx/unlazy triage, tooling skipped |
| 2026-09-01 | fable-legacy 1.0.0 | opt-in archive plugin: the 11 knowledge skills, 4 language agents and requesting-code-review retired in 2.0 are back in the marketplace under fable-legacy, so existing servers and older models lose nothing; the default plugins stay lean. Also docs/profiles/mobile-app.md — the install profile (pack + upstream marketplaces) for an Expo/native mobile project |
| 2026-09-01 | fable-mobile 1.1.0 | four Expo-app skills researched from primary sources and hostile-fact-checked before release (208 claims verified, 15 corrected): expo-apple-targets-extensions (share/keyboard extensions, App Groups, EAS signing), mobile-store-compliance (dated Play/App Store calendar + feature checklist), expo-subscriptions (RevenueCat vs StoreKit 2/Play Billing 8-9, sandbox timing, Workers-side verification), mobile-speech-to-text (expo-speech-recognition, SpeechAnalyzer, Android SpeechRecognizer, Gemini audio costs) |
| 2026-09-01 | fable-pack 2.0 | fable-pack 2.0 — blind-audit release: 11 model-known knowledge skills and 4 language agents removed, 7 factual fixes, fable-knowledge split into fable-mobile / fable-web / fable-integrations / fable-media / fable-niche, workflows aligned with native worktrees and /code-review, new parallel-plans |
| 2026-08-22 | fable-workflows 1.3.0, fable-guard 0.5.0 | fact-guard — placeholder over invented client facts, facts file over memory, fabrications ledger checked before delivery; guard hook gains Telegram/Stripe-live/JWT/connection-string patterns |
| 2026-08-05 | fable-workflows 1.2.0 | kb-hygiene — navigability pass for document folders: generated index by default, hand-written preview headers only where the title hides the content (transcripts, dumps, mixed docs), input/output split restricted to real pipelines, mandatory reversal check before bulk writes on unversioned folders |
| 2026-07-26 | fable-workflows 1.1.0 | BuilderIO/skills triage (3 of 11 adopted, adversarially reviewed): docs-first (docs-before-code gate for external contracts), stay-within-limits (95% usage-window rule for long agent runs), agent-watchdog (evidence-based audit of unattended runs); writing-plans gains a 5-step tie-break for competing directions |
| 2026-07-26 | fable-agents 1.1.1 | post-release fact-check: 12 factual fixes across 9 agents (inverted K8s QoS rule, stale JFR flag, JEP 491 pinning fix, `except*` claim, Terraform 1.10 native S3 locking, scan-before-sign gate order); docs aligned (badge, attributions, line limit) |
| 2026-07-25 | fable-agents 1.1.0, fable-guard 0.4.0 | all 19 laundry-list agents rewritten to the bash-pro/incident-responder operational standard (commands, decision tables, gotchas — line counts halved); guard hooks gain a 27-test suite in CI, NotebookEdit coverage, and stale_map path fixes; descriptions capped at 400 chars pack-wide |
| 2026-07-25 | pack-wide audit release | workflows/knowledge/agents 1.0.0, marketing 0.2.0, guard 0.3.0 — fact fixes (FTC Click-to-Cancel status, retired USPTO host), ~2,200 lines of generic content cut, sql-pro and devops-troubleshooter merged away, guard catches sk-proj keys and curl-pipe variants |
| 2026-07-25 | fable-workflows 0.6.0 | solution-hunter — continuous solution-search loop: generator subagents with rotating lenses, adversarial critics executing evidence checks, file-anchored state, budget guards |
| 2026-07-24 | fable-workflows 0.5.0 | critical-review — fresh-eyes re-examination of existing materials through a mandatory 7-lens pass; complements getting-unstuck (0.3.0-0.4.0) |
| 2026-07-21 | fable-workflows 0.2.0 | project-cartography — living three-file project map (CODEMAP / PROJECT_STATE / DECISIONS) so large projects survive session boundaries; lifecycle skills now chain |
| 2026-07-21 | fable-guard 0.2.0 | Stop hook: one-shot stale-map reminder in cartography-mapped projects |
| 2026-07-21 | fable-guard 0.1.0 | New opt-in plugin: PreToolUse hooks that deterministically block secret leaks and `curl \| sh` before execution |
| 2026-07-21 | fable-knowledge 0.3.0 | n8n-selfhosted-ops — first original skill (CLI import without API key, systemd env, Telegram HITL without broken sendAndWait) |
| 2026-07-21 | fable-agents 0.2.0 | Explicit model tier on all 23 agents: 7 opus / 15 sonnet / 1 haiku — no agent inherits the expensive orchestrator model |
| 2026-07-21 | repo | Validator now enforces agent model tiers and link integrity; monthly freshness sweep re-verifies version-fragile skills |

Full history in [CHANGELOG.md](CHANGELOG.md).

## Why this selection

Most community packs were written for weaker models: they teach the model to write React, name variables, or "think step by step." A frontier model does not need any of that — shipping it as a skill just burns context tokens on things the model already does well.

What a frontier model still gets wrong is narrow and specific:

- **Exact API schemas and CLI flags** — it will confidently invent a plausible-but-wrong parameter name
- **Version-specific behavior after its knowledge cutoff** — Next.js 16, Swift 6.2, iOS 26, Angular 21, n8n 2.8
- **Platform gotchas that contradict intuition** — the documented behavior that no amount of reasoning predicts
- **Methodologies with hard numeric rules** — cold-email benchmarks, A/B sample sizes, TDD's iron law

That is the entire selection bar. Of 269 skills triaged from ECC alone, 18 survived. Of ~745 agents in wshobson/agents, 23 made it in (21 after the 2026-07 overlap merges).

A 2026-09-01 blind-quiz audit tested that bar against the orchestrator model itself: skill and agent facts were extracted as closed-book questions, answered by the target models with no tools and no skills, and graded against the file. Every one of seven confident disagreements between a model's answer and a skill or agent file resolved in the model's favor — the file was wrong or stale, never the model. A skill that only restates what the model already knows is not neutral: it costs context, and where it is wrong it can override a correct answer. Removing model-known content is therefore a correctness measure, not only a cost one. Full method, scores, and the seven disputes: [2026-09-01 model-relevance audit](docs/audits/2026-09-01-model-relevance-audit.md).

## Why it fits Fable

The pack is tuned for a frontier orchestrator model (Claude Fable / Opus) running the main session:

- **Skills carry facts, not lectures** — short, dense, no process rituals. The orchestrator reads exact schemas and flags instead of re-deriving or hallucinating them.
- **Every agent declares the cheapest model that does the job** — 8 on `opus` (architecture, code review, security), 10 on `sonnet` (implementation and operations); `haiku` stays reserved for genuinely mechanical agents. No agent silently inherits the expensive orchestrator model. The orchestrator delegates mechanical skill work down-tier and keeps judgment work for itself.
- **Nothing competes with the model** — no meta-frameworks, no personas, no "orchestration systems" that fight the harness. The pack only fills gaps.

## Install

Install any subset — plugins are independent:

```
/plugin install fable-mobile@fable-pack
/plugin install fable-web@fable-pack
/plugin install fable-integrations@fable-pack
/plugin install fable-media@fable-pack
/plugin install fable-niche@fable-pack
/plugin install fable-agents@fable-pack
/plugin install fable-workflows@fable-pack
/plugin install fable-marketing@fable-pack
/plugin install fable-guard@fable-pack
```

## Plugins

### fable-legacy — 12 skills, 4 agents (opt-in archive)

Content retired from the default plugins by the 2026-09-01 audit because Fable 5.1 and Sonnet 5 already know it: clickhouse, database-migrations, evm-gotchas, manim-explainers, nuitka-windows-packaging, nuxt4-patterns, postgres-tips, bun-runtime, pubmed-database, react-performance, remotion, requesting-code-review; agents golang-pro, java-pro, rust-pro, python-pro. Install only if a server or an older model still relies on it: `/plugin install fable-legacy@fable-pack`. Nothing is ever deleted from the marketplace: retired content moves here.

### fable-mobile — 9 skills

Apple platform APIs, Xcode tooling, cross-platform accessibility mapping, and the Expo-app layer nobody else covers: share/keyboard extensions, store compliance, subscriptions, speech-to-text. Every fact in the four Expo skills was verified against a primary source and hostile-fact-checked before release.

| Category | Skills |
|----------|--------|
| Apple platform APIs | swift-concurrency-6-2, ios26-liquid-glass, apple-foundation-models |
| Xcode tooling | ios-icon-gen |
| Accessibility | wcag22-reference |
| Expo app layer | expo-apple-targets-extensions, expo-subscriptions, mobile-speech-to-text |
| Store submission | mobile-store-compliance |

Install alongside `expo@claude-plugins-official` (official Expo skills) and `android-skills@android-skills` (rcosteira79, native Android) for a complete mobile set.

Pairs with the official `expo` plugin and [rcosteira79/android-skills](https://github.com/rcosteira79/android-skills) for Android content — Android is not vendored here.

### fable-web — 6 skills

Web framework knowledge: version-specific behavior and gotchas a model's training-data lag makes it guess at.

| Category | Skills |
|----------|--------|
| Frameworks | nextjs-turbopack, angular-developer, prisma-patterns |
| Ops | pm2-node-services |
| Content tooling | html-slides, playwright-demo-videos |

### fable-integrations — 11 skills

Exact API schemas, CLI flags, and MCP configs for third-party services.

| Category | Skills |
|----------|--------|
| API integrations | x-api, jira-integration, nutrient-api, mailtrap-email-integration, free-tier-scraper-apis |
| MCP servers | mcp-server-configs, claude-devfleet, codehealth-mcp, laravel-plugin-discovery |
| Payments | agent-payment-x402 |
| Self-hosted ops | n8n-selfhosted-ops |

### fable-media — 3 skills

Media generation and processing: model app_ids and parameters, SDK methods, FFmpeg recipes.

| Category | Skills |
|----------|--------|
| Media generation | fal-ai-media, videodb, ffmpeg-media-recipes |

### fable-niche — 11 skills

Niche stacks with version-gated gotchas that contradict intuition.

| Category | Skills |
|----------|--------|
| Language niches | kotlin-ktor, kotlin-exposed, perl-modern, cpp-core-guidelines, tinystruct-patterns |
| Packaging / ops | flox-environments, uncloud, windows-desktop-e2e |
| Scientific / gov APIs | gget, uspto-database |
| EVM / DeFi | defi-amm-security |

**Migrating from fable-knowledge 1.0.0**: fable-knowledge is removed from the marketplace — installed 1.0.0 caches keep working but never update. Uninstall it and install the domain plugins you actually use; every skill moved to exactly one of the five plugins above, files unchanged bar the fixes in [CHANGELOG.md](CHANGELOG.md).

```
/plugin uninstall fable-knowledge@fable-pack
/plugin install fable-mobile@fable-pack
/plugin install fable-web@fable-pack
/plugin install fable-integrations@fable-pack
/plugin install fable-media@fable-pack
/plugin install fable-niche@fable-pack
```

11 skills were removed instead of moved — model-known per the 2026-09-01 audit; see [CHANGELOG.md](CHANGELOG.md) and the [audit](docs/audits/2026-09-01-model-relevance-audit.md).

| Skill | New plugin | Skill | New plugin |
|-------|-----------|-------|-----------|
| agent-payment-x402 | fable-integrations | laravel-plugin-discovery | fable-integrations |
| angular-developer | fable-web | mailtrap-email-integration | fable-integrations |
| apple-foundation-models | fable-mobile | mcp-server-configs | fable-integrations |
| claude-devfleet | fable-integrations | n8n-selfhosted-ops | fable-integrations |
| codehealth-mcp | fable-integrations | nextjs-turbopack | fable-web |
| cpp-core-guidelines | fable-niche | nutrient-api | fable-integrations |
| defi-amm-security | fable-niche | perl-modern | fable-niche |
| fal-ai-media | fable-media | playwright-demo-videos | fable-web |
| ffmpeg-media-recipes | fable-media | pm2-node-services | fable-web |
| flox-environments | fable-niche | prisma-patterns | fable-web |
| free-tier-scraper-apis | fable-integrations | swift-concurrency-6-2 | fable-mobile |
| gget | fable-niche | tinystruct-patterns | fable-niche |
| html-slides | fable-web | uncloud | fable-niche |
| ios-icon-gen | fable-mobile | uspto-database | fable-niche |
| ios26-liquid-glass | fable-mobile | videodb | fable-media |
| jira-integration | fable-integrations | wcag22-reference | fable-mobile |
| kotlin-exposed | fable-niche | windows-desktop-e2e | fable-niche |
| kotlin-ktor | fable-niche | x-api | fable-integrations |

### fable-agents — 18 subagents

Deep specialist subagents with concrete, tool-specific knowledge.

| Category | Agents |
|----------|--------|
| Languages | bash-pro |
| Review / security | code-reviewer, architect-review, security-auditor |
| Quant / trading | quant-critic |
| Infrastructure | kubernetes-architect, terraform-specialist, cloud-architect, deployment-engineer, database-admin, database-architect, database-optimizer (incl. advanced SQL) |
| Reliability | incident-responder, observability-engineer, performance-engineer |
| Product | frontend-developer, backend-architect, test-automator |

Every agent declares an explicit model tier — `opus` only where judgment is the product, `sonnet` for implementation and operations (`haiku` is reserved for mechanical work; no current agent qualifies). Overlapping clusters carry Key Distinctions blocks so the router can tell them apart.

### fable-workflows — 20 skills

Battle-tested methodologies with hard rules, adapted from obra/superpowers and BuilderIO/skills plus original additions:

test-driven-development, systematic-debugging, brainstorming, writing-plans, parallel-plans, executing-plans, verification-before-completion, using-git-worktrees, subagent-driven-development, receiving-code-review, finishing-a-development-branch, project-cartography, getting-unstuck, critical-review, solution-hunter, docs-first, stay-within-limits, agent-watchdog, kb-hygiene, fact-guard

Two critical-thinking skills complement each other: **getting-unstuck** fires when a
path is declared impossible and breaks the wall with tested hypotheses;
**critical-review** fires when nothing is visibly wrong and hunts blind spots —
stale assumptions, data contradictions, dismissed alternatives — through a
mandatory 7-lens pass. Blocked opportunities found by the review route into
getting-unstuck. **solution-hunter** extends both into a continuous search loop:
generator subagents with rotating lenses feed adversarial critics that execute
evidence checks, with file-anchored state and budget guards.

Three agent-ops skills cover autonomous and delegated work: **docs-first** gates
code against external contracts on reading current docs instead of model memory,
**stay-within-limits** keeps long runs inside usage windows (measure between
waves, pause at 95%, resume on evidence), and **agent-watchdog** audits
unattended runs from artifacts alone — reconstructing the contract before
judging the work.

**kb-hygiene** covers the document side of the same problem project-cartography
solves for code: a folder of notes, research or transcripts an agent must open
file by file to navigate. Its gate is the title-content test — a note named after
its topic already carries its preview, so a generated index extracts it for free,
while a transcript named after its event hides everything inside and earns a
hand-written header. Prose is the exception, not the default.

**fact-guard** stops invented client facts (names, prices, codes, contacts) from
reaching deliverables: a visible placeholder instead of a plausible guess, the
project's facts file over model memory, and a `known-fabrications.md` ledger
checked before delivery.

The lifecycle skills chain: brainstorming settles the design, writing-plans turns it
into phased tasks, executing-plans runs them, verification closes them out — and
**project-cartography** keeps a three-file living map (CODEMAP, PROJECT_STATE,
DECISIONS) so on large projects every new session starts from ~300 lines instead of
re-reading the codebase. The maps serve the model, never command it: what counts as
substantive stays a judgment call.

### fable-marketing — 20 skills

Marketing frameworks with concrete numbers, benchmarks, and templates.

| Category | Skills |
|----------|--------|
| Acquisition | cold-email, ads, ad-creative, prospecting, sms, directory-submissions |
| SEO | seo-audit, ai-seo, programmatic-seo, aso, competitors |
| Conversion / retention | ab-testing, popups, offers, churn-prevention, pricing |
| Foundations | product-marketing, customer-research, copy-editing, revops |

### fable-guard — deterministic guardrails (opt-in)

PreToolUse hooks that block secret patterns (API keys, tokens, private keys, Telegram
bot tokens, Stripe live keys, JWTs, connection strings with an embedded password) in
shell commands and file writes, plus dangerous shell patterns (`curl | sh`,
`--dangerously-skip-permissions`) — before they execute. A model can be tricked or
forget; a hook fires every time. Also ships a Stop hook that reminds — exactly once,
and only in projects keeping a CODEMAP.md — when code changed but the project map did
not (pairs with the project-cartography skill; whether the change was substantive
stays the model's call). Dependency-free Python, fully readable in
[plugins/fable-guard/hooks/](plugins/fable-guard/hooks/).

## MCP servers

fable-pack ships **no MCP servers** — that is a deliberate part of the security model
below, not a gap. Bundled servers auto-start with your session and widen the attack
surface; a knowledge pack has no business running processes.

Instead, the [mcp-server-configs](plugins/fable-integrations/skills/mcp-server-configs/SKILL.md)
skill (fable-integrations) carries exact, pinned launch configs for the servers people
actually use — Jira, GitHub, Supabase, Playwright, fal.ai, Cloudflare, Vercel, and
others — so the model writes a correct `.mcp.json` on the first try and *you* decide
what runs. Related skills cover the MCP surface where precision matters:
[claude-devfleet](plugins/fable-integrations/skills/claude-devfleet/SKILL.md) (exact tool
signatures for parallel-agent orchestration), [codehealth-mcp](plugins/fable-integrations/skills/codehealth-mcp/SKILL.md),
[laravel-plugin-discovery](plugins/fable-integrations/skills/laravel-plugin-discovery/SKILL.md),
and [nutrient-api](plugins/fable-integrations/skills/nutrient-api/SKILL.md).

## Security model

The eight content plugins are **inert by design**: markdown only — no hooks, no MCP
servers, no code that runs on install or load. Reference scripts inside skills are
examples the model may run with your normal tool permissions, never automatically.
Installing them cannot send your code or keys anywhere.

`fable-guard` is the single deliberate exception: it ships PreToolUse hooks, which
Claude Code runs automatically once the plugin is installed. That is its entire
purpose — deterministic enforcement the model cannot skip. It is opt-in, offline,
stateless, and small enough to audit in one sitting before installing.

## Selection principle

**Kept** only if a strong model would otherwise get it wrong:

- exact API schemas, endpoints, request/response shapes
- exact CLI flags and commands
- version-specific behavior and recent platform changes (2025+)
- platform gotchas that contradict intuition
- curated reference data and working non-trivial scripts
- methodologies with hard rules and measured numbers

**Dropped**: generic best practices, personas, thin wrappers, pack meta-tooling, and anything a frontier model produces reliably on its own.

## Conventions

- Skills: `plugins/<plugin>/skills/<name>/SKILL.md`, two-field frontmatter (`name`, `description`), optional `references/` and `scripts/`.
- Agents: `plugins/fable-agents/agents/<name>.md` with `name`, `description`, and an explicit `model` tier.
- Model policy: every agent declares the cheapest model that does the job well — `opus` only for judgment-heavy work (architecture, code review, security), `sonnet` for implementation and operations, `haiku` for mechanical tasks. Agents never inherit the orchestrator's model. Skills run inline; when a skill implies substantial mechanical work, the orchestrator should delegate it to a subagent on a lower tier.
- English only, no emojis, SKILL.md under 800 lines, descriptions under 400 characters (long descriptions get truncated in the harness skill listing, hiding the triggers).
- `python3 scripts/validate.py` checks all of the above (including required agent model tiers, link integrity, and description length); `python3 scripts/test_guard.py` tests the fable-guard hooks. CI runs both on every PR.

## Contributing

Missing a skill? Found stale facts? Open an issue — there are templates for [content requests](.github/ISSUE_TEMPLATE/skill-request.yml) and [outdated information reports](.github/ISSUE_TEMPLATE/outdated-info.yml). Outdated-info reports are the most valuable signal for a knowledge pack: version-fragile skills are re-verified against current releases on a monthly sweep. See [CONTRIBUTING.md](CONTRIBUTING.md) for the bar and format.

## Sources and licensing

This pack is MIT licensed. Parts are adapted from permissively licensed community packs — see [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for the full mapping: [affaan-m/ECC](https://github.com/affaan-m/ECC), [wshobson/agents](https://github.com/wshobson/agents), [obra/superpowers](https://github.com/obra/superpowers), [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills). Full change history in [CHANGELOG.md](CHANGELOG.md).
