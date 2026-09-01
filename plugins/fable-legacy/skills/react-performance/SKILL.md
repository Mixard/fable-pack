---
name: react-performance
description: Use when writing, reviewing, or refactoring React 18/19 and Next.js code for performance. Covers waterfall elimination, bundle-size APIs, server-side gotchas, and version-specific/counterintuitive rendering behavior — Next.js 15 after(), React 19 Activity, useEffectEvent, optimizePackageImports, and the `&&`-renders-0 gotcha.
---

# React Performance

## 1. Eliminating Waterfalls

> Every sequential `await` adds full network latency — waterfalls are the #1 performance killer.

### Cheap conditions before await

```ts
// CORRECT — short-circuit on cheap sync condition first
async function Page({ id }: { id: string }) {
  if (!id) return null;
  const flag = await getFlag("show-page");
  if (!flag) return null;
  const data = await getData(id);
}
```

### Promise.all for independent work, start-early for partial dependencies

```ts
const [user, posts, followers] = await Promise.all([
  getUser(id), getPosts(id), getFollowers(id),
]);

// Partial dependency — start early, await late
const userP = getUser(id);
const postsP = getPosts(id);
const profile = await getProfile(id);
if (profile.private) return null;
const [user, posts] = await Promise.all([userP, postsP]);
```

### Server Components: parallel through composition, not sibling awaits

Sibling `await`s inside one async component run sequentially. Splitting into child components lets React run them in parallel:

```tsx
export default async function Page() {
  return (
    <View>
      <UserSection />
      <CartSection />
    </View>
  );
}
```

Push `<Suspense>` boundaries close to the data so the page paints what it can while slower sub-trees stream in; reserve space (skeleton/`min-height`) to avoid layout shift when content arrives.

## 2. Bundle Size

Next.js 13.5+ `optimizePackageImports` (in `next.config.js`) automates barrel-file tree-shaking for listed packages — direct imports are still required for libraries not on that list.

```ts
// CORRECT — explicit per branch; dynamic template strings defeat bundler trace analysis
const mod = name === "home" ? await import("./pages/home") : await import("./pages/about");
```

```tsx
import dynamic from "next/dynamic";
const HeavyChart = dynamic(() => import("./HeavyChart"), {
  loading: () => <Skeleton />,
  ssr: false, // client-only
});
```

`next/script` `strategy="afterInteractive"` (default) or `"lazyOnload"` defers third-party scripts until after hydration.

## 3. Server-Side Performance

### Every `"use server"` function is a public HTTP endpoint

Authenticate and authorize inside the action itself — never rely on the calling Client Component's gating, since the action can be invoked directly.

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

### `React.cache()` dedupes within one request, not across requests

```ts
import { cache } from "react";
export const getUser = cache(async (id: string) => db.user.findUnique({ where: { id } }));
```

Calling `getUser("1")` from three Server Components in the same render = one DB query. For data that does NOT change per request (config, lookup tables), cache outside React instead (LRU cache or `unstable_cache`) — `React.cache` alone won't help across requests.

### No mutable module-level state in RSC/SSR

Module state on the server is shared across all concurrent requests — a race condition between users, not a per-request cache. Use request-scoped storage (`headers()`, `cookies()`, async context) instead.

### `after()` for non-blocking work (Next.js 15+)

```ts
import { after } from "next/server";
export async function GET() {
  const data = await getData();
  after(() => logAnalytics(data));
  return Response.json(data);
}
```

`after()` runs work after the response is sent — logging, cache warming, analytics — without delaying the response.

## 4. Client-Side Data Fetching

- SWR / TanStack Query for deduplication — multiple components calling `useUser(id)` share one network request and cache entry; a hand-rolled `useEffect` + `fetch` per component does not.
- `localStorage` reads/writes are synchronous and block the main thread — keep payloads small, and store a `version` field to migrate/discard on schema change.

## 5. Rendering Gotchas

- **`&&` can render `0`** — `{count && <Badge>{count}</Badge>}` renders the literal text `0` when `count` is `0`, because `0` is falsy but not `null`/`undefined`/`false`. Use a ternary: `{count > 0 ? <Badge>{count}</Badge> : null}`.
- **`<Activity mode="visible" | "hidden">`** (React 19) keeps a subtree's state and effects mounted while hidden — cheaper than unmount/remount for tabs and accordions, and avoids losing scroll position/form state.
- **`preload`/`preconnect` come from `react-dom`, not a DOM API** — `import { preload, preconnect } from "react-dom"` issues resource hints from render code.
- **Hydration mismatch suppression must be narrow** — `<time suppressHydrationWarning>` only on the specific leaf node with expected divergence (e.g. locale-formatted timestamps), never on a tree with children, or real mismatches get silently swallowed too.
- **New default array/object props break `memo`** — `<List items={items ?? []} />` creates a new array reference every render, defeating `React.memo` on `List`; hoist the default to module scope (`const EMPTY: Item[] = []`).

## 6. Advanced Patterns

- **`useEffectEvent` values are stable across renders** — do not add them to the effect's dependency array; they intentionally always see the latest closure without re-running the effect.
- **Guard module-level singletons with a module flag, not `useEffect`** — telemetry/logger init that must run once per app load can double-fire under StrictMode/Fast Refresh if gated only by an effect.
