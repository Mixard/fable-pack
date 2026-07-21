<p align="center">
  <img src="assets/hero.svg" alt="fable-pack: curated plugin marketplace for Claude Code" width="100%">
</p>

<p align="center">
  <a href="https://github.com/Mixard/fable-pack/actions/workflows/validate.yml"><img src="https://github.com/Mixard/fable-pack/actions/workflows/validate.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-e3b341" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/skills-81-2b3242" alt="81 skills">
  <img src="https://img.shields.io/badge/subagents-23-2b3242" alt="23 subagents">
  <img src="https://img.shields.io/badge/executable_code-none-2b3242" alt="no executable code">
</p>

A curated, license-clean plugin marketplace for Claude Code. We reviewed 1,000+ skills and agents from the most popular community packs and kept fewer than 10% — every survivor either contains knowledge a frontier model would otherwise hallucinate, or a battle-tested methodology with hard rules.

```
/plugin marketplace add Mixard/fable-pack
```

## What's new

| Date | Release | Highlights |
|------|---------|------------|
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

That is the entire selection bar. Of 269 skills triaged from ECC alone, 18 survived. Of ~745 agents in wshobson/agents, 23 made it in.

## Why it fits Fable

The pack is tuned for a frontier orchestrator model (Claude Fable / Opus) running the main session:

- **Skills carry facts, not lectures** — short, dense, no process rituals. The orchestrator reads exact schemas and flags instead of re-deriving or hallucinating them.
- **Every agent declares the cheapest model that does the job** — 7 on `opus` (architecture, code review, security), 15 on `sonnet` (implementation and operations), 1 on `haiku`. No agent silently inherits the expensive orchestrator model. The orchestrator delegates mechanical skill work down-tier and keeps judgment work for itself.
- **Nothing competes with the model** — no meta-frameworks, no personas, no "orchestration systems" that fight the harness. The pack only fills gaps.

## Install

Install any subset — plugins are independent:

```
/plugin install fable-knowledge@fable-pack
/plugin install fable-agents@fable-pack
/plugin install fable-workflows@fable-pack
/plugin install fable-marketing@fable-pack
/plugin install fable-guard@fable-pack
```

## Plugins

### fable-knowledge — 48 skills

Knowledge-only: exact API schemas, CLI flags, version-specific behavior, platform gotchas. No process rituals.

| Category | Skills |
|----------|--------|
| Media / video | fal-ai-media, videodb, remotion, ffmpeg-media-recipes, manim-explainers, playwright-demo-videos, html-slides, ios-icon-gen |
| API integrations | x-api, jira-integration, nutrient-api, free-tier-scraper-apis, mcp-server-configs, mailtrap-email-integration, laravel-plugin-discovery, codehealth-mcp, claude-devfleet, agent-payment-x402 |
| Web / frameworks | bun-runtime, nuxt4-patterns, nextjs-turbopack, react-performance, angular-developer, wcag22-reference, pm2-node-services |
| Data | clickhouse, database-migrations, postgres-tips, prisma-patterns, regex-llm-hybrid |
| Scientific APIs | pubmed-database, uspto-database, gget |
| Apple (2025+ APIs) | swift-concurrency-6-2, ios26-liquid-glass, apple-foundation-models |
| Language niches | kotlin-exposed, kotlin-ktor, perl-modern, cpp-core-guidelines, tinystruct-patterns |
| Packaging / ops | nuitka-windows-packaging, flox-environments, uncloud, windows-desktop-e2e, n8n-selfhosted-ops |
| EVM / DeFi | evm-gotchas, defi-amm-security |

### fable-agents — 23 subagents

Deep specialist subagents with concrete, tool-specific knowledge.

| Category | Agents |
|----------|--------|
| Languages | python-pro, rust-pro, golang-pro, java-pro, sql-pro, bash-pro |
| Review / security | code-reviewer, architect-review, security-auditor |
| Infrastructure | kubernetes-architect, terraform-specialist, cloud-architect, deployment-engineer, database-admin, database-architect, database-optimizer |
| Reliability | devops-troubleshooter, incident-responder, observability-engineer, performance-engineer |
| Product | frontend-developer, backend-architect, test-automator |

Every agent declares an explicit model tier — `opus` only where judgment is the product, `sonnet` for implementation, `haiku` for mechanical work.

### fable-workflows — 13 skills

Battle-tested methodologies with hard rules, adapted from obra/superpowers:

test-driven-development, systematic-debugging, brainstorming, writing-plans, executing-plans, verification-before-completion, using-git-worktrees, subagent-driven-development, requesting-code-review, receiving-code-review, finishing-a-development-branch, dispatching-parallel-agents, project-cartography

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

PreToolUse hooks that block secret patterns (API keys, tokens, private keys) in shell
commands and file writes, plus dangerous shell patterns (`curl | sh`,
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

Instead, the [mcp-server-configs](plugins/fable-knowledge/skills/mcp-server-configs/SKILL.md)
skill (fable-knowledge) carries exact, pinned launch configs for the servers people
actually use — Jira, GitHub, Supabase, Playwright, fal.ai, Cloudflare, Vercel, and
others — so the model writes a correct `.mcp.json` on the first try and *you* decide
what runs. Related skills cover the MCP surface where precision matters:
[claude-devfleet](plugins/fable-knowledge/skills/claude-devfleet/SKILL.md) (exact tool
signatures for parallel-agent orchestration), [codehealth-mcp](plugins/fable-knowledge/skills/codehealth-mcp/SKILL.md),
[laravel-plugin-discovery](plugins/fable-knowledge/skills/laravel-plugin-discovery/SKILL.md),
and [nutrient-api](plugins/fable-knowledge/skills/nutrient-api/SKILL.md).

## Security model

The four content plugins are **inert by design**: markdown only — no hooks, no MCP
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
- English only, no emojis, SKILL.md under 800 lines.
- `python3 scripts/validate.py` checks all of the above (including required agent model tiers and link integrity); CI runs it on every PR.

## Contributing

Missing a skill? Found stale facts? Open an issue — there are templates for [content requests](.github/ISSUE_TEMPLATE/skill-request.yml) and [outdated information reports](.github/ISSUE_TEMPLATE/outdated-info.yml). Outdated-info reports are the most valuable signal for a knowledge pack: version-fragile skills are re-verified against current releases on a monthly sweep. See [CONTRIBUTING.md](CONTRIBUTING.md) for the bar and format.

## Sources and licensing

This pack is MIT licensed. Parts are adapted from permissively licensed community packs — see [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for the full mapping: [affaan-m/ECC](https://github.com/affaan-m/ECC), [wshobson/agents](https://github.com/wshobson/agents), [obra/superpowers](https://github.com/obra/superpowers), [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills). Full change history in [CHANGELOG.md](CHANGELOG.md).
