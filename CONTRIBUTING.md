# Contributing

Contributions are welcome: new skills, new agents, fixes for outdated information, and requests for coverage you are missing.

## The selection bar

This pack is curated, not exhaustive. Before submitting, check your content against the selection principle:

**fable-knowledge** accepts only knowledge a strong model would otherwise hallucinate:

- exact API schemas, endpoints, request/response shapes
- exact CLI flags and commands for specific tools
- version-specific behavior and recent platform changes
- platform gotchas that contradict intuition
- curated reference data (tables, IDs, limits)
- working non-trivial scripts

It does NOT accept process rituals, generic best practices, personas, or advice a strong model produces reliably on its own.

**fable-agents** accepts deep specialist subagents with concrete, tool-specific knowledge. Breadth without depth is rejected.

**fable-workflows** accepts battle-tested development methodologies with hard rules and anti-pattern tables, not motivational checklists.

**fable-marketing** accepts frameworks with concrete numbers, benchmarks, and templates.

## Format

Skills: `plugins/<plugin>/skills/<name>/SKILL.md` with exactly two frontmatter fields:

```markdown
---
name: my-skill
description: What it covers and when to use it, key use case first.
---
```

Agents: `plugins/fable-agents/agents/<name>.md` with `name` and `description` frontmatter; `description` must state when to delegate to the agent.

Rules for all content:

- English only. No emojis.
- SKILL.md under 500 lines; put heavy reference material in `references/` inside the skill directory.
- No cross-references to files outside the skill's own plugin.
- If you adapted third-party content, it must be under a permissive license (MIT, Apache-2.0, BSD) and you must add the source to `ATTRIBUTIONS.md`.

## Workflow

1. Fork, branch, add or edit content.
2. Run `python3 scripts/validate.py` locally; CI runs the same check.
3. Open a PR. Describe what the content covers and why a strong model needs it.

## Requesting content

Missing a skill or agent? Open an issue with the "Skill or agent request" template. Found outdated information (an API changed, a flag was removed)? Use the "Outdated information" template — these reports are the most valuable maintenance signal for a knowledge pack.
