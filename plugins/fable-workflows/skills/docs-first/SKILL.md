---
name: docs-first
description: Use before implementing, integrating, upgrading, or debugging anything that touches a third-party API, library, framework, CLI, cloud service, or provider SDK - and whenever the user asks for "latest", "current", "official", or "recommended" behavior. Forces reading current authoritative docs before writing code from model memory. Not for declared dead ends - that is getting-unstuck.
---

# Docs First

## Overview

Model memory of external APIs is a cache with no invalidation. Package majors ship, flags get removed, defaults flip, auth scopes change - and code written "from what I remember" compiles confidently against a contract that no longer exists. The failure mode is not ignorance; it is fluent, plausible, outdated code.

**Core principle:** for anything version-sensitive or external, memory is a hypothesis and docs are evidence. Verify the contract before writing against it.

## The Iron Law

```
NO CODE AGAINST AN EXTERNAL CONTRACT FROM MEMORY WHEN CURRENT DOCS ARE REACHABLE
```

If the task depends on a third-party surface and you have not read the docs for the version actually in play, you may not present the implementation as correct.

## When to Use

Trigger a docs pass when any of these hold:

- The user says "latest", "current", "official", "supported", "best practice", "recommended", or "look it up".
- The task adds, upgrades, configures, or imports a package, SDK, framework, plugin, CLI, model, or provider integration.
- The API is fast-moving or version-sensitive: AI SDKs, provider APIs, Next.js, React, Tailwind, Vite, Prisma, Stripe, GitHub, auth libraries, deployment platforms, and similar.
- The implementation depends on auth, OAuth scopes, webhooks, billing, PII, encryption, migrations, retries, rate limits, quotas, caching, or compliance.
- An error mentions deprecation, unknown options, missing exports, invalid config, unsupported fields, changed defaults, or version mismatch.
- The repo has local docs, ADRs, generated schemas, OpenAPI specs, or package READMEs that could define the contract.
- The choice is expensive to reverse: public wire formats, database schema, persistent IDs, event names, customer-visible behavior.
- You catch yourself about to write "usually", "probably", "I think", or "from memory" about an external API.

**Boundary with getting-unstuck:** that skill fires when you are about to declare something impossible; this one fires earlier - before the first line is written against an external contract. Its rationalization "docs from memory are ASSUMED, not VERIFIED" is this skill applied at the dead-end stage. If a docs pass was skipped and you are now stuck, run both: read the docs, then hypothesis-test.

## What Counts as Docs

Use the most authoritative source available, in this order:

1. **Local repo evidence** for project-specific behavior: docs, ADRs, generated types, schemas, package READMEs, tests, existing helper usage.
2. **Official upstream docs** for third-party behavior: API references, migration guides, changelogs, release notes. Find them with web search when the URL is not already known.
3. **Registry metadata** for versions: `npm view <pkg> version` or the ecosystem equivalent, before writing imports or install commands. Then read the docs for that major.
4. **Source code or type definitions** when official docs are incomplete. Treat as evidence, not folklore.

Stack Overflow, old blog posts, and memory are not primary sources when official docs exist. Use community sources only to debug symptoms after the authoritative contract is known.

## Required Workflow

1. **Name the exact surface:** package name, installed version, target version, endpoint, CLI command, config file, or schema.
2. **Reach the current docs:** local docs first for internal code, web search for external surfaces (`<product> <feature> official docs`, `<package> migration guide`).
3. **Read the pages closest to the surface.** For new packages, verify the latest version before writing imports or config.
4. **Extract the facts the task needs:** option names, imports, lifecycle rules, defaults, breaking changes, limits, permissions - for the major actually in play.
5. **Implement using those facts.** If docs conflict with existing code, inspect the local code path and call out the discrepancy.
6. **Verify with the smallest useful check:** typecheck, tests, build, CLI dry run, schema validation.
7. **Name your sources** in the final answer when the evidence affects the recommendation.

## When a Local Read Is Enough

Do not browse the web for every edit. A docs pass can be local and brief when the answer is already in the repo: existing helper usage, nearby tests, typed interfaces, generated clients. For trivial language syntax, typos, formatting, or self-contained code with no external contract, proceed normally. But if the task depends on an external tool, package, or provider's current behavior, web search is usually the right first step.

## If Docs Are Unreachable

If network access, auth, or missing files prevent reading the docs, say so plainly before relying on memory. Narrow the uncertainty (inspect source or types if available) and never present the result as confirmed-current.

## Red Flags - STOP and Read the Docs

- Writing an import, config block, or install command for a package whose current major you have not checked
- Describing provider behavior (pricing, limits, model names, scopes) from memory in a recommendation
- Copying an API call shape "that always worked" into new code
- Explaining an "unknown option" error by guessing instead of opening the changelog
- Choosing a wire format, schema, or event name without reading what the consumer expects

**ALL of these mean: STOP. Run the workflow above.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I know this API well" | You know a past version. Majors ship faster than training cutoffs. |
| "Searching wastes time" | One search costs seconds. Debugging code against a dead contract costs hours. |
| "The example in my memory is canonical" | Examples are the fastest-rotting part of docs. Verify against the current page. |
| "It compiles, so the contract holds" | Runtime behavior, defaults, and quotas do not show up at compile time. |
| "The user is in a hurry" | The user wants working code. Confidently outdated code is the slowest path. |
| "It's a tiny integration" | Auth, billing, and webhook changes hit tiny integrations hardest. |

## Quick Reference

| Situation | Action |
|-----------|--------|
| New/upgraded dependency | Check registry version, read docs for that major |
| Provider API call | Read current API reference, not memory |
| Error mentions deprecation/unknown option | Open changelog and migration guide |
| Internal repo contract | Read local docs, types, tests first |
| Hard-to-reverse choice | Read what every consumer expects before locking it |
| No docs reachable | Say so; present result as unverified |
