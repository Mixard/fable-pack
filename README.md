# fable-skills

Curated knowledge-only skill pack for Claude Code, distilled from [everything-claude-code](https://github.com/affaan-m/everything-claude-code) (183 skills reviewed, 29 kept).

Selection principle: only knowledge a strong model would otherwise hallucinate — exact API schemas and endpoints, CLI flags, version-specific behavior, platform gotchas, curated references, working scripts. Process discipline (TDD rituals, verification checklists, planning scaffolds), generic best practices, and pack meta-tooling were dropped.

## Skills

| Category | Skills |
|----------|--------|
| Media / video | fal-ai-media, videodb, remotion, ffmpeg-media-recipes, manim-explainers, playwright-demo-videos, html-slides |
| API integrations | x-api, jira-integration, nutrient-api, free-tier-scraper-apis, mcp-server-configs |
| Web / runtimes | bun-runtime, nuxt4-patterns, wcag22-reference, pm2-node-services |
| Data | clickhouse, database-migrations, postgres-tips, regex-llm-hybrid |
| Apple (2025 APIs) | swift-concurrency-6-2, ios26-liquid-glass, apple-foundation-models |
| Language niches | kotlin-exposed, kotlin-ktor, perl-modern, cpp-core-guidelines |
| EVM / DeFi | evm-gotchas, defi-amm-security |

## Install

As a plugin (marketplace flow):

```
/plugin marketplace add /root/fable-skills
/plugin install fable-skills@fable-skills-marketplace
```

Or reference skills directly by symlinking individual skill folders into `~/.claude/skills/`.

## Conventions

- Each skill: `skills/<name>/SKILL.md` with two-field frontmatter (`name`, `description`), optional `references/` and `scripts/`.
- Knowledge only, no process rituals. Files under 800 lines. English, no emojis.
