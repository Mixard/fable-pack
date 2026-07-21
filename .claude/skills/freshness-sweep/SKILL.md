---
name: freshness-sweep
description: Monthly staleness check for version-fragile skills - verify pinned versions and APIs against current releases via web search, file outdated-info issues. Use when asked to check pack freshness or when a scheduled sweep fires.
---

# Freshness sweep

A knowledge pack rots silently: a skill pinned to "Ktor 3.x" or "Next.js 16" keeps
asserting stale facts with full confidence long after the ecosystem moves. Stale
knowledge is worse than no knowledge - the model would otherwise hedge or search.

## Procedure

1. **Pick targets** (max 10 per sweep, rotate): the most version-fragile skills first.
   Fragility ranking:
   - pinned major versions in the name or first paragraph (nextjs-turbopack,
     swift-concurrency-6-2, ios26-liquid-glass, angular-developer, bun-runtime,
     kotlin-exposed, kotlin-ktor, nuxt4-patterns, react-performance, remotion)
   - hosted API endpoints and pricing (fal-ai-media, nutrient-api, mailtrap-email-integration,
     free-tier-scraper-apis, x-api, agent-payment-x402)
   - stable references (regex-llm-hybrid, ffmpeg-media-recipes, wcag22-reference) - lowest
     priority, check yearly at most.
   Track rotation state in `.claude/skills/freshness-sweep/last-sweep.md` (date + skills checked).
2. **Verify each target** with web search: current stable version, breaking changes since
   the version the skill documents, deprecated flags/endpoints the skill still recommends.
   Delegate per-skill checks to subagents on sonnet - this is mechanical verification.
3. **File findings**: for each confirmed stale fact, open a GitHub issue with the
   outdated-info template:
   `gh issue create -R Mixard/fable-pack --title "outdated: <skill>: <fact>" --body "..."`
   Include: the stale claim (file + line), the current fact, the source URL, date checked.
4. **Do not edit skills during the sweep** - the sweep finds, issues track, fixes are
   separate reviewed commits (then follow the release skill).
5. **Update rotation state** and report: N checked, M stale, issue links.

## Hard rules

- Never mark a skill fresh from model knowledge alone - every "still current" verdict
  needs a web source dated within the last 3 months.
- A version bump upstream is not automatically staleness: check whether the skill's
  facts actually broke before filing.
