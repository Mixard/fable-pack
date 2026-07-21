# fable-pack

A curated, license-clean plugin marketplace for Claude Code: 79 skills and 23 subagents across four plugins. Install only what you need.

The selection bar is strict: every item either contains knowledge a strong model would otherwise hallucinate (exact API schemas, CLI flags, version-specific behavior, platform gotchas) or a battle-tested methodology with hard rules — not generic best practices. We reviewed 1,000+ skills and agents from the most popular community packs and kept under 10% of the knowledge candidates.

## Install

```
/plugin marketplace add Mixard/fable-pack
```

Then install any subset:

```
/plugin install fable-knowledge@fable-pack
/plugin install fable-agents@fable-pack
/plugin install fable-workflows@fable-pack
/plugin install fable-marketing@fable-pack
```

## Plugins

### fable-knowledge — 47 skills

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
| Packaging / ops | nuitka-windows-packaging, flox-environments, uncloud, windows-desktop-e2e |
| EVM / DeFi | evm-gotchas, defi-amm-security |

### fable-agents — 23 subagents

Deep specialist subagents with concrete, tool-specific knowledge.

| Category | Agents |
|----------|--------|
| Languages | python-pro, rust-pro, golang-pro, java-pro, sql-pro, bash-pro |
| Review / security / perf | code-reviewer, architect-review, security-auditor, performance-engineer |
| Infrastructure | kubernetes-architect, terraform-specialist, cloud-architect, deployment-engineer, database-admin, database-optimizer, database-architect, backend-architect |
| Incident / observability | incident-responder, devops-troubleshooter, observability-engineer |
| Development / QA | frontend-developer, test-automator |

### fable-workflows — 12 skills

Battle-tested development methodologies with hard rules and anti-pattern tables.

test-driven-development, systematic-debugging, brainstorming, writing-plans, executing-plans, verification-before-completion, using-git-worktrees, subagent-driven-development, requesting-code-review, receiving-code-review, finishing-a-development-branch, dispatching-parallel-agents

### fable-marketing — 20 skills

Marketing frameworks with concrete numbers, benchmarks, and templates.

| Category | Skills |
|----------|--------|
| Acquisition | cold-email, ads, ad-creative, prospecting, sms, directory-submissions |
| SEO | seo-audit, ai-seo, programmatic-seo, aso, competitors |
| Conversion / retention | ab-testing, popups, offers, churn-prevention, pricing |
| Foundations | product-marketing, customer-research, copy-editing, revops |

## Selection principle

**Kept** only if a strong model would otherwise get it wrong:

- exact API schemas, endpoints, request/response shapes
- exact CLI flags and commands
- version-specific behavior and recent platform changes (2025+)
- platform gotchas that contradict intuition
- curated reference data and working non-trivial scripts
- methodologies with hard rules and measured numbers

**Dropped**: generic best practices, personas, thin wrappers, pack meta-tooling, and anything a frontier model produces reliably on its own. Of the 269 skills triaged from ECC alone, 18 survived.

## Conventions

- Skills: `plugins/<plugin>/skills/<name>/SKILL.md`, two-field frontmatter (`name`, `description`), optional `references/` and `scripts/`.
- Agents: `plugins/fable-agents/agents/<name>.md` with `name`, `description`, and optional `model` tier.
- English only, no emojis, SKILL.md under 800 lines.
- `python3 scripts/validate.py` checks all of the above; CI runs it on every PR.

## Contributing

Missing a skill? Found stale facts? Open an issue — there are templates for [content requests](.github/ISSUE_TEMPLATE/skill-request.yml) and [outdated information reports](.github/ISSUE_TEMPLATE/outdated-info.yml). Outdated-info reports are the most valuable signal for a knowledge pack. See [CONTRIBUTING.md](CONTRIBUTING.md) for the bar and format.

## Sources and licensing

This pack is MIT licensed. Parts are adapted from permissively licensed community packs — see [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for the full mapping. Full change history in [CHANGELOG.md](CHANGELOG.md).
