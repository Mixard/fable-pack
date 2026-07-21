---
name: angular-developer
description: Use when writing modern Angular (v19-v21+) code - Signal Forms, linkedSignal, resource/httpResource, effect/afterRenderEffect, native CSS animations (animate.enter/leave), Angular Aria headless components, and the Angular CLI MCP server. Covers version-gated APIs and gotchas that changed after Angular 19.
---

# Modern Angular Patterns

Always check the project's Angular version in `package.json` before choosing APIs - the features below are version-gated and behave differently or do not exist on older versions. When creating a new project, do not pin a version unless asked: use `ng new` if the CLI is installed, otherwise `npx @angular/cli@latest new <name>` (or `npx @angular/cli@<version> new <name>` when the user requests a specific version). After generating code, run `ng build` and fix errors before finishing.

Prefer `ng add <package>` over `npm install` for Angular libraries (it runs init schematics), and `ng generate` for components/services/directives.

## Reactivity: which primitive

- `computed()` - state strictly derived from other state, never manually set.
- `linkedSignal()` - derived default that the user can still override with `.set()`/`.update()`; resets when the source changes. Object form `{ source, computation }` receives `previous` to preserve a still-valid selection. See [linked-signal.md](references/linked-signal.md).
- `resource()` / `httpResource()` - async data as signals (experimental). `params` + async `loader({ params, abortSignal })`; always pass `abortSignal` to fetch. Status signals: `value()`, `hasValue()`, `isLoading()`, `error()`, `status()` (`'idle' | 'loading' | 'resolved' | 'error' | 'reloading' | 'local'`). Prefer `httpResource` when using HttpClient (keeps interceptors). See [resource.md](references/resource.md).
- `effect()` - only for syncing signals to imperative non-signal APIs (analytics, localStorage, canvas). Never propagate signal state inside an effect - use `computed`/`linkedSignal`.
- `afterRenderEffect()` - DOM read/write after render, with ordered phases `earlyRead` -> `write` -> `mixedReadWrite` -> `read`; never read in `write` or write in `read`; client-only (skipped in SSR). See [effects.md](references/effects.md).

## Forms

For new forms on a version that supports Signal Forms (`@angular/forms/signals`), prefer Signal Forms; match the existing strategy in older apps. Full API - `form()`, `FormField`, validators, `schema`, `applyWhen`/`applyEach`, `validateHttp`, `submit` - in [signal-forms.md](references/signal-forms.md).

Critical Signal Forms rules:
- Never use `null`/`undefined` as initial field values - use `''`, `0`, `[]`.
- Field state flags require calling the field first: `form.field().valid()`, not `form.field.valid()`.
- Do not set `min`, `max`, `value`, `disabled`, `readonly` as HTML attributes on `[formField]` inputs - define them as schema rules.
- `when` conditions are only available for `required()`, not other validators.

## Accessibility: Angular Aria

`@angular/aria` (install with `npm install @angular/aria`, must be present before use) provides headless accessible directives for Accordion, Listbox, Combobox, Menu, Tabs, Toolbar, Tree, Grid. They handle keyboard/ARIA/focus; you provide HTML + CSS, styling states via the ARIA attributes the directives set (`[aria-expanded]`, `[aria-selected]`, `[aria-disabled]`, `[aria-current]`). Import paths, directive names, and per-pattern examples in [angular-aria.md](references/angular-aria.md).

## Animations

Angular v20.2+: prefer native CSS with `animate.enter` / `animate.leave` bindings over the deprecated `@angular/animations` package. Angular applies the class during enter/leave and waits for leave animations before DOM removal. When binding `(animate.leave)="onLeave($event)"` for JS-driven animation, you MUST call `event.animationComplete()` or the element is never removed. See [angular-animations.md](references/angular-animations.md).

## Angular CLI MCP Server

The CLI ships an MCP server: `npx @angular/cli mcp`. Default tools: `ai_tutor`, `find_examples`, `get_best_practices`, `list_projects`, `onpush_zoneless_migration`, `search_documentation`. Experimental tools (enable with `-E`): `build`, `devserver.start/stop/wait_for_build`, `e2e`, `modernize`, `test`. Flags: `--read-only`, `--local-only`. Per-IDE config blocks in [mcp.md](references/mcp.md).

## Anti-Patterns

- `null`/`undefined` initial values in signal form models.
- `form.field.valid()` instead of `form.field().valid()`.
- Starting new forms with reactive/template-driven APIs when Signal Forms are supported.
- Calling `inject()` outside an injection context - wrap with `runInInjectionContext` when needed.
- `effect()` for derived state that should be `computed()` or `linkedSignal()`.
- `$parent.$index` in nested `@for` loops - Angular has no `$parent`; alias with `let outerIdx = $index` in the outer loop.
