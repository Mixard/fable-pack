# Changelog

All notable changes to this pack are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
