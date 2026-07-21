# Changelog

All notable changes to this pack are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
