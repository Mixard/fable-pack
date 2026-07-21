---
name: nextjs-turbopack
description: Use when working on or reviewing Next.js 16+ projects. Covers the proxy.ts middleware rename (do not flag it as misnamed), Turbopack-by-default dev behavior, filesystem caching, and when to fall back to webpack.
---

# Next.js 16 and Turbopack

Version-specific facts about Next.js 16+ that differ from earlier training-data conventions.

## proxy.ts replaces middleware.ts

Next.js 16 renamed the middleware file convention:

- **Next.js 16+**: `proxy.ts` at the project root
- **Pre-16**: `middleware.ts` at the project root

The rename is tied to the Next.js version, not to the bundler in use.

**Do not flag `proxy.ts` as a misnamed or missing middleware file in a Next.js 16 project.** It is correct and intentional. Suggesting a rename back to `middleware.ts` will break middleware execution.

Reference: https://nextjs.org/docs/app/getting-started/proxy

## Turbopack is the default dev bundler

From Next.js 16, `next dev` runs Turbopack (incremental Rust bundler) by default:

- **Filesystem caching**: restarts reuse previous work (typically under `.next`); large projects see roughly 5-14x faster restarts. No extra config needed.
- **Fallback to webpack**: only if you hit a Turbopack bug or depend on a webpack-only dev plugin. Disable with `--webpack` (some releases use `--no-turbopack`; check the docs for the exact version).
- **Production**: whether `next build` uses Turbopack or webpack depends on the exact 16.x release; verify against the docs for the version in use rather than assuming.

## Bundle analysis

Next.js 16.1+ ships an experimental Bundle Analyzer for inspecting output size and finding heavy dependencies; it is enabled via config/experimental flag (version-dependent).

## Practical notes

- Stay on a recent 16.x for stable Turbopack and caching behavior.
- If dev feels slow, confirm Turbopack is active (it is unless explicitly disabled) and that the `.next` cache is not being wiped between runs.
