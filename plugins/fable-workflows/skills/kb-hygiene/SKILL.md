---
name: kb-hygiene
description: Use when an agent must open files just to learn what they contain - a notes, research, or docs folder expensive to navigate. Generates a regenerable index, hand-writes preview headers only where the title hides the content, splits a data pipeline into input/output, refreshes drifted headers. Triggers - organize this knowledge base, annotate these docs. Not for source trees.
---

# Knowledge Base Hygiene

## Overview

An agent navigating a document folder pays for every file it must open to discover it is the wrong file. The fix is a cheap preview layer: name plus one line, enough to decide read/skip before loading anything.

The trap is over-applying it. Most well-kept folders already have that layer for free - the filename and the H1. Hand-writing prose on top of a self-describing file buys nothing and creates a second copy of the truth that rots silently.

**Core principle:** generate the preview from what already exists; hand-write only where the title genuinely hides the content.

## The Iron Law

```
NEVER HAND-ANNOTATE WHAT THE TITLE ALREADY REVEALS.
NO ANNOTATION WITHOUT READING THE FILE.
```

## The title-content test - the only gate that matters

For each file ask: **does the title tell what is inside, or only what the file is called?**

| Title reveals content - GENERATE ONLY | Title only names the file - HAND-WRITE |
|---|---|
| `research/03-multiorders.md` -> `# 03. Multiorders` | `club-session-july-01_729900291.txt` -> `# AI Club - Parser Agent - July 01` |
| Single-topic note named after its topic | Meeting transcript, call recording, interview |
| `ADR-001-platform-selection.md` | Dated log, dump, scraped batch |
| Reference page, spec, changelog | Long document covering unrelated topics |
| | File whose conclusion contradicts its title |

Left column: the filename plus H1 is already a working index - stop after the generated index. Right column: the title names an event or a batch, and the content (which tools, which numbers, which conclusion) cannot be derived from it - a hand-written preview adds real information.

A folder is usually mixed. Run the test per file, not per folder.

## Step 0 - Classify the folder

```bash
D=<folder>
find "$D" -name '*.md' | wc -l
find "$D" -regex '.*\.\(py\|js\|ts\|tsx\|php\|sh\|go\|rs\)' | wc -l
find "$D" -type f | wc -l
```

| Signal | Mode | Action |
|---|---|---|
| 10+ documents, little or no code | vault | Steps 1-4 |
| Under 10 files | index-only | Step 1 only |
| Binaries, archives, generated output | index-only | Step 1 only, describe the folder not the files |
| More code than prose | code | Stop. At most a repo map in the README. Never annotate source files |
| Skill or plugin repo (SKILL.md with a `description` field) | skip | The frontmatter is already the preview layer |

Annotating source code is forbidden because imports and signatures already provide the preview, and a prose header above code drifts from it within weeks.

## Step 1 - Generate the index (the default deliverable)

Build it from data that already exists, so it can be regenerated instead of maintained:

```bash
cd <folder>
{ echo "# Index"; echo
  find . -name '*.md' ! -path './.git/*' | sort | while read -r f; do
    printf -- "- \`%s\` - %s\n" "$f" "$(grep -m1 '^# ' "$f" | sed 's/^# //')"
  done
} > INDEX.md
```

Rules:
- Regenerate, never hand-edit. A generated file that someone edited by hand is stale by definition.
- If many H1 lines turn out to be uninformative, that is the finding: fix the titles, then regenerate. A bad title is cheaper to fix than to annotate around.
- For binary or generated folders, describe the folder and its subfolders instead of listing every file.

## Step 2 - Hand-written headers, only for files failing the title-content test

Placed directly after the H1, before any other metadata:

```markdown
# Title that says what this file is

<!-- kb-hygiene: 2026-08-05 -->

**About:** Two to four sentences: what is inside, why open it, the main conclusion. Concrete, not genre: not "project notes" but "unit economics for three funnels, conclusion - CPA $45 against LTV $65".

**Keywords:** term - term - term - term
```

- Read the file first: `head -40` plus `grep '^## '`. Never write an abstract from the filename.
- Rewrite an uninformative H1 while you are there - the title is part of the preview.
- Keywords are what someone would search for: tools, entities, metrics. Not a restatement of the title.
- The date comment is the staleness marker. Keep it.

## Step 3 - input/output split, only for pipelines

Apply only when data visibly moves: something arrives from outside, gets processed, and a final artifact comes out.

```
input/    arrived from outside; never edited by hand, the source overwrites it
output/   final artifacts only; this is what search targets
```

Do not apply to code repos (they already have `src/tests/docs`), to topic-based folders (the topics are the structure), or to folders with no external source.

After moving files, repair what pointed at them: links in README and index files, `OUT`-style constants in loader scripts, cron entries. Then run the broken-link check in Step 4.

## Step 4 - Verify

```bash
# every document is reachable from the generated index
diff <(find <folder> -name '*.md' ! -name INDEX.md | sort) \
     <(grep -o '`[^`]*\.md`' <folder>/INDEX.md | tr -d '`' | sort)

# files that were supposed to get a header but did not
for f in <folder>/*.md; do head -8 "$f" | grep -q '\*\*About:\*\*' || echo "NO HEADER: $f"; done

# relative links that broke during the move
grep -o '](\./\?[^)#][^)]*)' <file>.md | tr -d '](' | sed 's/)$//' \
  | while read -r p; do [ -e "$p" ] || echo "BROKEN: $p"; done
```

Done when: the index covers every document, headers exist exactly where the test demanded them, no broken links, and any loader script still writes to the new layout (run it once on a single item to prove it).

## Reversal - required before any bulk write

Bulk annotation is a write across dozens of files. Establish the undo path first:

```bash
git -C <folder> rev-parse --is-inside-work-tree   # if this fails, there is no undo via VCS
```

If the folder is not under version control, either commit it first or verify the headers are machine-removable before writing:

```python
import pathlib
for p in pathlib.Path('.').rglob('*.md'):
    L = open(p).read().split('\n')
    ok = len(L) > 6 and L[0].startswith('# ') and L[2].startswith('<!-- kb-hygiene:') \
         and L[4].startswith('**About:**') and L[6].startswith('**Keywords:**')
    if not ok:
        print("not cleanly removable:", p)
```

Same shape, reversed, strips them. Never start a bulk pass on an unversioned folder without this check.

## Staleness

A hand-written header is a copy of the truth and decays independently of the file. This is the failure mode that makes the whole layer worse than nothing: an agent trusts a header that describes a rewritten file and confidently reads the wrong thing.

- Working on an already-annotated base: compare the header against the content **before** trusting it. An existing header is a claim, not evidence.
- Files changed after their `kb-hygiene` date are suspects. Rewrite the header in the same commit as the content, or delete it.
- Never carry a header across a rewrite unchanged.

## Cost check before a bulk pass

Writing N abstracts costs N reads plus N writes now, to save reads later. It pays back only if the folder gets searched repeatedly and its titles are opaque. A one-off research dump nobody will query again does not need it - generate the index and stop.

## Red flags - stop and return to the gate

- Annotating a file whose H1 already answers "what is inside"
- Writing an abstract without opening the file
- Running a bulk pass on an unversioned folder without the reversal check
- Applying input/output to a folder with no external data source
- Adding preview headers to source code
- Hand-editing a generated index instead of regenerating it

## Common rationalizations

| Excuse | Reality |
|---|---|
| "Consistency - annotate every file" | Consistency is not the goal; read/skip decisions are. Uniform noise still costs tokens to read. |
| "The header will be kept up to date" | It will not. Assume every header drifts and design for detection, not discipline. |
| "input/output is just cleaner" | It is a pipeline layout. Without an external source it adds two hops to every path for nothing. |
| "The index can be maintained by hand" | Then it is stale by the second commit. If it cannot be regenerated, it is not an index. |
| "More context in the header is better" | The header is a routing decision, not a summary. Four sentences that end without a conclusion are worse than one that states it. |

## What this skill does not do

- Does not rewrite file content - it adds a header and moves files.
- Does not delete anything. Duplicates and junk get reported to the user.
- Does not touch `.git`, `venv`, `node_modules`, `__pycache__`, or build output.
- Does not organize source code. For a code repository use project-cartography instead.
