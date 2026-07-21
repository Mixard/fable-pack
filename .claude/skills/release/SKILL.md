---
name: release
description: Release procedure for fable-pack - validate, bump plugin versions, changelog, push, refresh local plugin cache. Use whenever committing content changes to plugins/ in this repo.
---

# Releasing fable-pack changes

Plugin updates only reach users after a version bump: Claude Code compares the
`version` field in plugin.json against the installed cache. A push without a bump
is invisible to every installed copy, including the maintainer's own.

## Procedure

1. **Validate**: `python3 scripts/validate.py` must print `OK`. Fix failures before anything else.
2. **Identify changed plugins**: `git status --short plugins/` - every plugin directory with
   changes needs its own bump.
3. **Bump versions** in `plugins/<name>/.claude-plugin/plugin.json` (semver):
   - patch: typo/factual fix inside existing content
   - minor: new skills/agents, changed frontmatter policy, reworked content
   - major: removed or renamed skills/agents (breaks references)
4. **Changelog**: add a `## [<plugin> <version>] - YYYY-MM-DD` section at the top of
   `CHANGELOG.md` (Keep a Changelog format, newest first).
5. **Commit and push** to `main` with a conventional message
   (`feat(<plugin>): ...` / `fix(<plugin>): ...`).
6. **Verify CI**: `gh run list --limit 1` - the `validate` workflow must be `success`.
7. **Refresh local cache** for each changed plugin that is installed locally:
   `claude plugin update <name>@fable-pack`
   The `@fable-pack` marketplace suffix is required - the bare plugin name fails
   with "not found". Restart the session to apply.

## Hard rules

- Never push content changes without the matching version bump (step 3) - this is the
  single most common release mistake in this repo.
- One CHANGELOG entry per released plugin version, not per commit.
- If validate.py fails in CI but passed locally, check Python version drift first.
