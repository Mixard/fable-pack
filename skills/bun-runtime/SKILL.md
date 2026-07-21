---
name: bun-runtime
description: Use when running, testing, or deploying projects with Bun, or migrating from Node. Covers the bun.lock vs bun.lockb version change, Bun.serve/Bun.file/bun:test APIs, key CLI flags, Node compatibility, and Vercel setup.
---

# Bun Runtime

All-in-one JS/TS runtime, package manager, bundler, and test runner. Built on JavaScriptCore (not V8), implemented in Zig. Runs `.ts` natively without a build step.

## Lockfile gotcha

Current Bun writes a text lockfile `bun.lock`; older versions (pre-1.2) wrote binary `bun.lockb`. A repo may contain either — commit whichever the project uses. Newer Bun reads `bun.lockb` and migrates to `bun.lock`; older Bun cannot read `bun.lock`. Don't commit both.

## CLI

```bash
bun install                     # replaces npm install
bun install --frozen-lockfile   # CI/deploys: fail instead of updating lockfile
bun run dev                     # run package.json script
bun src/index.ts                # run a file directly (bun run also works)
bun x cowsay hi                 # npx equivalent (also: bunx)
bun run --env-file=.env dev     # load env file explicitly (.env is auto-loaded by default)
bun test                        # run tests; --watch for watch mode
```

## Runtime APIs

```typescript
// HTTP server
Bun.serve({
  port: 3000,
  fetch(req) {
    return new Response("Hello");
  },
});

// Files (lazy — no I/O until read)
const file = Bun.file("package.json");
const json = await file.json();   // also .text(), .arrayBuffer(), .stream()
await Bun.write("out.txt", "content");
```

Prefer Bun-native APIs over Node equivalents where they exist; they are faster.

## Testing (bun:test)

Jest-like API, no config needed. Picks up `*.test.{ts,js,tsx,jsx}` and `*.spec.*`.

```typescript
import { expect, test, describe, beforeEach, mock } from "bun:test";

test("add", () => {
  expect(1 + 2).toBe(3);
});
```

## Node compatibility

- Node built-ins (`fs`, `path`, `http`, ...) are implemented; most npm packages work unchanged.
- Node-API (N-API) native addons are supported, but packages with prebuilt binaries occasionally target Node ABI specifics — if a native dependency misbehaves under Bun, that is the usual cause; run that project under Node.
- Choose Node over Bun for legacy tooling that assumes Node internals or dependencies with known Bun issues.

## Vercel

Set the runtime to Bun in project settings. Install command: `bun install --frozen-lockfile` for reproducible deploys. Build: `bun run build`, or bundle directly with `bun build ./src/index.ts --outdir=dist`.
