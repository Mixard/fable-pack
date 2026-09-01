---
name: codehealth-mcp
description: Use when gating refactors, commits, or PRs on structural code health via the CodeScene MCP server (@codescene/codehealth-mcp). Covers the MCP config, the four standalone-mode tools, platform-only tools to avoid, and how to interpret 1-10 Code Health scores.
---

# Code Health MCP (CodeScene)

Structural (design-level) maintainability scoring for files and change sets, complementing lint/style checks. Upstream: codescene-oss/codescene-mcp-server; package `@codescene/codehealth-mcp` (stdio via npx).

## Setup

Claude Code (`~/.claude.json` -> `mcpServers`), or the same block in a repo-root `.mcp.json` for project scope:

```json
"codescene": {
  "command": "npx",
  "args": ["-y", "@codescene/codehealth-mcp"],
  "env": {
    "CS_ACCESS_TOKEN": "YOUR_CS_ACCESS_TOKEN_HERE"
  }
}
```

`CS_ACCESS_TOKEN` is a personal access token (see the upstream repo's `docs/getting-a-personal-access-token.md`). Standalone mode does not require a paid CodeScene platform account for the four tools below. Restart the session and confirm the server is connected before relying on scores.

## Standalone tools (the only ones to call)

| Tool | When to use |
|------|-------------|
| `code_health_review` | Full structural analysis before modifying a file (baseline score + listed code smells) |
| `code_health_score` | Quick numeric score after each change (delta check) |
| `pre_commit_code_health_safeguard` | Block commits that introduce Code Health regressions |
| `analyze_change_set` | Branch-level check before opening a PR |

Do not call platform-only tools (e.g. repository-wide hotspot lists), and do not reference `delta_analysis` - it is not available on standalone.

## Score interpretation (1-10)

| Range | Meaning | Behavior |
|-------|---------|----------|
| 9.0-10.0 | Green - healthy | Safer to extend or refactor |
| 4.0-8.9 | Yellow - debt | Tread carefully; no drive-by refactors |
| 1.0-3.9 | Red - severe debt | Narrow, minimal-diff changes only |

Scoping rule of thumb: below 5 - minimal diff only; 5-7 - no broad refactors; above 7 - refactoring is safer, but still verify the score after each edit.

## Feedback loop

1. Before touching a file: `code_health_review`, record baseline score and smells, plan the smallest change.
2. After each change: `code_health_score` to verify the delta; if the score regressed, fix before continuing - passing tests do not mean healthy design.
3. Before commit: `pre_commit_code_health_safeguard`.
4. Before PR: `analyze_change_set`.

If the MCP is unavailable (offline, bad token, crash): never invent scores. Report the check as skipped and fall back to lint/tests for gating.
