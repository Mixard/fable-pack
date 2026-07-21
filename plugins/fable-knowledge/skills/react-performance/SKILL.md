---
name: react-performance
description: Use when writing, reviewing, or refactoring React 18/19 and Next.js code for performance. Organizes 70+ rules across 8 priority categories — eliminating waterfalls, bundle size, server-side, client fetching, re-render, rendering, JS micro-perf, and advanced patterns — with concrete correct/incorrect pairs and version-specific APIs (Next.js 15 after(), React 19 Activity, useEffectEvent, optimizePackageImports).
---

# React Performance

Performance optimization patterns for React 18/19 and Next.js, organized by priority with decision-tree guidance for active code review and refactoring.

## When to Activate

- Writing or reviewing React/Next.js code for performance
- Diagnosing slow page loads, slow interactions, or high CPU on the client
- Auditing bundle size or Lighthouse Core Web Vitals regressions
- Removing waterfalls in Server Components / API routes
- Reducing client-side re-renders
- Optimizing long lists, animations, or hydration

## Priority Index

| Priority | Category | Prefix | When it matters |
|---|---|---|---|
| 1 — CRITICAL | Eliminating Waterfalls | `async-` | Anytime `await` is followed by independent `await` |
| 2 — CRITICAL | Bundle Size Optimization | `bundle-` | First-load JS, route-level imports, third-party libs |
| 3 — HIGH | Server-Side Performance | `server-` | RSC, Server Actions, API routes, SSR |
| 4 — MEDIUM-HIGH | Client-Side Data Fetching | `client-` | SWR / TanStack Query / raw `fetch` in hooks |
| 5 — MEDIUM | Re-render Optimization | `rerender-` | High-frequency state updates, parent-child fan-out |
| 6 — MEDIUM | Rendering Performance | `rendering-` | Long lists, animations, hydration |
| 7 — LOW-MEDIUM | JavaScript Performance | `js-` | Hot loops, frequent allocations |
| 8 — LOW | Advanced Patterns | `advanced-` | Effect-event integration, stable refs |

## 1. Eliminating Waterfalls (CRITICAL)

> Every sequential `await` adds full network latency — waterfalls are the #1 performance killer.

### Cheap conditions before await

Check sync conditions (props, env, hardcoded flags) before awaiting remote data.

```ts
// CORRECT — short-circuit on cheap sync condition first
async function Page({ id }: { id: string }) {
  if (!id) return null;
  const flag = await getFlag("show-page");
  if (!flag) return null;
  const data = await getData(id);
}
```

### Defer awaits until used

```ts
// CORRECT — move await into the branch that uses it
if (mode === "guest") return renderGuest();
const user = await getUser(id);
return renderUser(user);
```

### Promise.all for independent work

```ts
const [user, posts, followers] = await Promise.all([
  getUser(id), getPosts(id), getFollowers(id),
]);
```

### Partial dependencies — start early, await late

```ts
const userP = getUser(id);
const postsP = getPosts(id);
const profile = await getProfile(id);
if (profile.private) return null;
const [user, posts] = await Promise.all([userP, postsP]);
```

### Suspense for streaming

Push `<Suspense>` boundaries close to the data so the page paints what it can while slower sub-trees stream in. Trade-off: layout shift when content arrives — reserve space (skeleton or `min-height`).

### Server Components: parallel through composition

```tsx
// CORRECT — split into children, React runs them in parallel
export default async function Page() {
  return (
    <View>
      <UserSection />
      <CartSection />
    </View>
  );
}
```

Sibling awaits inside one component run sequentially; splitting into child components lets React run them in parallel.

## 2. Bundle Size Optimization (CRITICAL)

### Direct imports, not barrels

Barrel `index.ts` files force the bundler to walk the entire module graph even when tree-shaking removes most of it. Direct imports save 200-800ms of first-load JS in many real-world apps.

```ts
// CORRECT
import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
```

Next.js 13.5+ has Optimize Package Imports (`optimizePackageImports` in `next.config.js`) that automates this for listed packages — use it; manual direct imports still required for non-listed libs.

### Statically analyzable paths

```ts
// CORRECT — explicit per branch (dynamic template strings defeat trace analysis)
const mod = name === "home" ? await import("./pages/home") : await import("./pages/about");
```

### Dynamic imports for heavy components

```tsx
import dynamic from "next/dynamic";
const HeavyChart = dynamic(() => import("./HeavyChart"), {
  loading: () => <Skeleton />,
  ssr: false, // when client-only
});
```

### Defer third-party scripts

Load analytics, logging, support widgets AFTER hydration. Use `next/script` with `strategy="afterInteractive"` (default) or `"lazyOnload"`.

### Conditional and hover-preload loading

```tsx
if (user.role === "admin") {
  const { AdminPanel } = await import("./admin/AdminPanel");
}
```

Trigger `<link rel="preload">` or `import()` on hover/focus so the bundle is in cache by the time the user clicks.

## 3. Server-Side Performance (HIGH)

### Authenticate Server Actions like API routes

Every `"use server"` function is a public endpoint. Authenticate AND authorize inside the action — never rely on the calling Client Component's gating.

```ts
"use server";
export async function deleteUser(formData: FormData) {
  const session = await getSession();
  if (!session?.user) throw new Error("Unauthorized");
  const targetId = String(formData.get("id"));
  if (session.user.role !== "admin" && session.user.id !== targetId) {
    throw new Error("Forbidden");
  }
  await db.user.delete({ where: { id: targetId } });
}
```

### `React.cache()` for per-request deduplication

```ts
import { cache } from "react";
export const getUser = cache(async (id: string) => db.user.findUnique({ where: { id } }));
```

`React.cache` dedupes within a single request — calling `getUser("1")` from three Server Components in the same render = one DB query.

### LRU cache for cross-request data

For data that does NOT change per request (config, lookup tables), cache outside React with an LRU cache or `unstable_cache`.

### Avoid duplicate serialization in RSC props

When a Server Component renders the same data into multiple Client Components, the data is serialized once per consumer. Lift the Client Component up and pass children.

### Hoist static I/O to module scope

```ts
// CORRECT — runs once at module load
const fontData = readFileSync(fontPath);
export async function Page() { return <Banner font={fontData} />; }
```

### No mutable module-level state in RSC/SSR

Module state on the server is shared across all requests — a race condition between users. Use request-scoped storage (`headers()`, `cookies()`, async context) instead.

### Use `after()` for non-blocking work

Next.js 15 `after()` runs work after the response is sent — logging, cache warming, analytics.

```ts
import { after } from "next/server";
export async function GET() {
  const data = await getData();
  after(() => logAnalytics(data));
  return Response.json(data);
}
```

Also: minimize data passed to Client Components (strip fields, paginate, project columns at the DB layer), and parallelize nested fetches with `Promise.all` per item.

## 4. Client-Side Data Fetching (MEDIUM-HIGH)

- **SWR / TanStack Query for deduplication** — multiple components calling `useUser(id)` should share one network request and one cache entry. Never roll your own `useEffect` + `fetch` for shared data.
- **Deduplicate global event listeners** — a single shared listener via a hook + global subject beats every component adding its own.
- **Passive listeners for scroll** — `window.addEventListener("scroll", handler, { passive: true })` improves scrolling smoothness (the listener cannot `preventDefault()`).
- **localStorage** — always store a `version` field and migrate/discard on schema change; keep payloads small (`localStorage` is synchronous and blocks the main thread).

## 5. Re-render Optimization (MEDIUM)

### Don't subscribe to state used only in callbacks

```tsx
// CORRECT — read once on call, don't subscribe
const handler = () => { const count = useStore.getState().count; doSomething(count); };
```

### Extract expensive work into memoized components

```tsx
const Heavy = memo(function Heavy({ items }: { items: Item[] }) {
  return <Chart data={transform(items)} />;
});
```

### Hoist default non-primitive props

```tsx
const EMPTY: Item[] = [];   // module scope — new array each render breaks memo
<List items={items ?? EMPTY} />
```

### Other re-render rules

- **Primitive dependencies in effects** — `useEffect(() => {}, [id, name])`, not `[{ id, name }]`.
- **Subscribe to derived booleans, not raw values** — `useStore((s) => s.cart.length > 0)` re-renders only when emptiness flips.
- **Derive during render, never via `useEffect`** — `const full = \`${first} ${last}\``.
- **Functional `setState` for stable callbacks** — `useCallback(() => setCount((c) => c + 1), [])`.
- **Lazy state initializer for expensive values** — `useState(() => parseTree(largeInput))`.
- **Avoid memo for simple primitives** — `useMemo(() => x + 1, [x])` is overhead; memo earns its keep on object identity and expensive computation.
- **Split hooks with independent deps** — `const a = useA(source1); const b = useB(source2);`.
- **`startTransition` for non-urgent updates**; **`useDeferredValue` for expensive renders**; **`useRef` for transient frequent values** (timestamps, accumulators).
- **Don't define components inside components** — each render makes a new type, defeating reconciliation and unmounting children.

## 6. Rendering Performance (MEDIUM)

- **Animate the wrapper, not the SVG** — transforming a `<div>` wrapper is GPU-accelerated; transforming the SVG triggers paint.
- **`content-visibility: auto` for long lists** — `.row { content-visibility: auto; contain-intrinsic-size: auto 80px; }` skips offscreen rendering.
- **Hoist static JSX** to module scope.
- **SVG: reduce coordinate precision** — `d="M10.12,20.65"` costs fewer bytes than `M10.123456,20.654321`.
- **Hydration no-flicker via inline script** — for values needed before hydration (theme, locale), inline a `<script>` that sets `document.documentElement.dataset.*` before React mounts.
- **Suppress expected hydration mismatches narrowly** — `<time suppressHydrationWarning>` only on known-divergent leaf nodes, never on a tree with children.
- **`<Activity mode="visible|hidden">`** (React 19) keeps tree state and effects mounted but hides — cheaper than unmount/remount for tabs and accordions.
- **Ternary over `&&`** — `{count > 0 ? <Badge>{count}</Badge> : null}` (a `0` from `&&` renders as a text node).
- **React DOM resource hints** — `import { preload, preconnect } from "react-dom"`.
- **`defer` / `async` on `<script>` tags** — `defer` for ordered execution after DOMContentLoaded; `async` for fire-and-forget.

## 7. JavaScript Performance (LOW-MEDIUM)

- Batch DOM/CSS changes via class swap or `cssText`, not property-by-property
- `Map`/`Set` for repeated lookups and membership — `O(1)` vs `O(n)`
- Cache property access (`const len = arr.length`) and hoist `RegExp` out of loops
- Combine `filter().map()` into one pass (`flatMap` or single `for`)
- Loop for min/max instead of `sort()` — `O(n)` vs `O(n log n)`
- `toSorted()` over mutation when immutability matters
- `requestIdleCallback` for non-critical work

## 8. Advanced Patterns (LOW)

- **`useEffectEvent` deps** — values from `useEffectEvent` are stable; do NOT add them to effect deps.
- **Event handler refs** — for stable callbacks passed to memoized children, keep a `useRef(handler)` updated in an effect and expose a `useCallback` that reads `handlerRef.current`.
- **Init once per app load** — guard module-level singletons (telemetry, logger) with a module-scope flag, not `useEffect`.

## Automated Tools

- **Next.js 13.5+ `optimizePackageImports`** — barrel import optimization
- **React Compiler** — auto-memoization; when the project ships it, demote `rerender-*` manual memoization rules to review-only (manual `useMemo`/`useCallback` becomes noise)
- **Turbopack** — faster builds, better tree-shaking
- **`@next/bundle-analyzer`** — visualize first-load JS

## Lighthouse / Web Vitals Mapping

| Metric | Most relevant categories |
|---|---|
| **LCP** (Largest Contentful Paint) | Waterfalls, Bundle Size, Resource Hints |
| **INP** (Interaction to Next Paint) | Re-render, Rendering, JavaScript |
| **CLS** (Cumulative Layout Shift) | Rendering (Suspense placement, image dimensions) |
| **TBT** (Total Blocking Time) | Bundle Size, JavaScript, Defer Third-Party |
