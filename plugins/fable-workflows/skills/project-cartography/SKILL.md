---
name: project-cartography
description: Use when starting a project expected to outgrow one session, when joining a large unfamiliar codebase, or when a session begins in a project that keeps CODEMAP.md/PROJECT_STATE.md. Maintains a living three-file map (what is where, what is happening, why decisions were made) so each session starts from ~300 lines instead of re-reading the codebase.
---

# Project cartography

A frontier model's binding constraint on large projects is context, not intelligence.
Without a map, every session pays a re-reading tax; with a stale map, it pays twice.
This skill maintains three small files that convert "re-read the project" into
"read 300 lines".

**Prime directive: the map serves the model, it does not command it.** These files
transfer context between sessions - they are not process artifacts. If a file stops
earning its tokens, shrink it. Never let map upkeep displace judgment: the model
decides what is substantive, what to record, and what to skip.

## The three files (project root)

**CODEMAP.md** - what is where. One line per directory/module: purpose + the key
entry point. Not a file listing - a reading guide. Target under 100 lines even for
large repos; if a directory needs three lines, it needs a refactor note instead.

```markdown
# CODEMAP
- src/api/ - HTTP layer; routes registered in src/api/router.ts
- src/core/pricing/ - all price math; entry: calculate.ts, pure functions only
- src/jobs/ - cron workers; each file self-registers, see jobs/index.ts
- migrations/ - append-only; never edit applied ones
Danger zones: src/legacy/ (do not touch without reading DECISIONS.md#legacy-freeze)
```

**PROJECT_STATE.md** - what is happening. Done / in progress / next, with dates.
The handoff note a session writes to its successor. Prune ruthlessly: done items
older than a few weeks collapse into one line.

```markdown
# PROJECT STATE (updated 2026-07-21)
## In progress
- payments: Stripe webhook retries - src/jobs/stripe_retry.ts exists, untested
## Next
- rate limiting on /api/quote (decided, see DECISIONS.md#rate-limits)
## Done (recent)
- 2026-07-19: auth moved to sessions, JWT code deleted
```

**DECISIONS.md** - why. Append-only log of choices that future work must not
relitigate: one heading per decision, 3-6 lines each (context, choice, rejected
alternatives, consequences). Record decisions, not discussions.

## When to scaffold

Scaffold at project start only when the project will plausibly outgrow one session -
a script or small tool does not need cartography, and empty ceremony files are worse
than none. In an existing large codebase, generate CODEMAP.md from exploration once,
then maintain.

On scaffold, add one standing rule to the project's CLAUDE.md:

```markdown
## Project map
CODEMAP.md, PROJECT_STATE.md, DECISIONS.md at root are the session handoff. Read them
before exploring. After substantive changes (new module, moved responsibility, finished
or abandoned task, architectural choice), update the affected file - substantive is
your judgment call. Renames, small fixes, and refactors that change no responsibility
do not warrant an update.
```

## Update rules

- Update at natural checkpoints (task finished, direction changed), not per-edit.
- CODEMAP changes only when the answer to "where does X live" changes.
- STATE is rewritten freely; CODEMAP is edited surgically; DECISIONS is append-only.
- Session start in a mapped project: read the three files INSTEAD of broad exploration,
  then verify only the parts you will touch - the map can be stale; trust but verify.
- Planning a large feature (writing-plans skill): the plan's phases land in
  PROJECT_STATE.md "Next" so expansion survives the session.

## Hard rules

- Never block or delay actual work to polish the map - a 2-minute update at a
  checkpoint, not a bookkeeping session.
- Never duplicate what git already records (history, authorship, diffs) or what
  CLAUDE.md already says (conventions, commands).
- Combined size of the three files stays under ~400 lines; beyond that the map has
  become a second codebase - compress it.
