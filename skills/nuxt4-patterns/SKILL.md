---
name: nuxt4-patterns
description: Use when building or debugging Nuxt 4 apps with SSR, hybrid rendering, or data fetching. Covers routeRules (swr/isr/prerender), hydration-safe useFetch/useAsyncData, Lazy components, hydrate-on-visible, defineLazyHydrationComponent, and SSR gotchas.
---

# Nuxt 4 Patterns

## Route rules

Rendering and caching strategy per route group in `nuxt.config.ts`:

```ts
export default defineNuxtConfig({
  routeRules: {
    '/': { prerender: true },              // static HTML at build time
    '/products/**': { swr: 3600 },         // serve cached, revalidate in background
    '/blog/**': { isr: true },             // incremental static regeneration (platform-dependent)
    '/admin/**': { ssr: false },           // client-rendered route
    '/api/**': { cache: { maxAge: 3600 } } // Nitro response cache; `redirect` also available
  },
})
```

Pick rules per route group (marketing vs catalog vs dashboard vs API), not one global strategy. `swr` takes seconds; `isr` accepts `true` or a seconds value on platforms that support it (e.g. Vercel).

## Data fetching

- `await useFetch('/api/...')` for SSR-safe page/component reads: server-fetched data goes into the Nuxt payload, so hydration does not refetch.
- `useAsyncData(key, handler)` when the fetcher is not a plain `$fetch` call, needs a custom key, or composes multiple sources. Give it a stable key; handlers run during SSR and hydration, so keep them side-effect free.
- `$fetch()` directly only for user-triggered writes or client-only actions — top-level `$fetch` in setup runs twice (server and client) with no payload transfer.
- `lazy: true` / `useLazyFetch` / `useLazyAsyncData` for non-critical data that should not block navigation; render on `status === 'pending'`.
- `server: false` only for data irrelevant to SEO/first paint.
- Trim payloads with `pick`; prefer shallow reactivity when deep is unneeded.

```ts
const route = useRoute() // Nuxt's useRoute, not vue-router's

const { data: article, status, error, refresh } = await useAsyncData(
  () => `article:${route.params.slug}`,
  () => $fetch(`/api/articles/${route.params.slug}`),
)

const { data: comments } = await useFetch(
  `/api/articles/${route.params.slug}/comments`,
  { lazy: true, server: false },
)
```

## Hydration safety

First render must be deterministic — server HTML and first client render have to match.

- No `Date.now()`, `Math.random()`, browser APIs, or localStorage reads in SSR-rendered template state. Move them to `onMounted()`, guard with `import.meta.client`, or isolate in `<ClientOnly>` / a `.client.vue` component.
- Import `useRoute()` from Nuxt, not `vue-router` — they differ during SSR.
- Do not drive SSR markup from `route.fullPath`: URL fragments (`#hash`) exist only on the client, so full-path-dependent markup mismatches.
- `ssr: false` route rules are an escape hatch for genuinely browser-only areas, not a fix for mismatches.

## Lazy loading and lazy hydration

Nuxt code-splits per page already; get route boundaries right before micro-splitting components.

```vue
<template>
  <!-- Lazy prefix = dynamic import; v-if defers loading the chunk -->
  <LazyRecommendations v-if="showRecommendations" />

  <!-- loaded with the page, hydrated when scrolled into view -->
  <LazyProductGallery hydrate-on-visible />
</template>
```

- `Lazy` prefix on any auto-imported component makes it a dynamic import.
- Hydration-strategy props on Lazy components: `hydrate-on-visible`, `hydrate-on-idle`, `hydrate-on-interaction`, `hydrate-on-media-query`, `hydrate-after` (ms), `hydrate-when` (boolean), `hydrate-never`.
- Custom strategies: `defineLazyHydrationComponent('visible' | 'idle' | ..., () => import('...'))`.
- Lazy hydration works on single-file components only, and passing new props to a lazily hydrated component triggers immediate hydration.
- Use `<NuxtLink>` for internal navigation so Nuxt prefetches route chunks and payloads.
