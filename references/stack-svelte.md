# Stack: Svelte 5 + Vite (the hub)

Used when the surface ships as a static bundle behind nginx with an API under
`/api`, as `piighost-hub` does on the Litestar + Svelte template.

## Setup

```bash
pnpm add @fontsource-variable/geist @fontsource-variable/geist-mono @lucide/svelte
python scripts/scaffold.py svelte frontend/src   # tokens, lib, ui, entity components
```

`main.ts` imports `./app.css` once. Tailwind v4 through `@tailwindcss/vite`, no
config file; tokens live in `app.css` under `@theme inline`.

## Conventions

- **Runes only.** `$state`, `$derived`, `$props`, `$effect`, snippets with
  `{#snippet}` / `{@render}`. A value that mirrors the URL and accepts edits is
  a writable `$derived`, not `$state` plus `$effect`.
- **Rune modules** end in `.svelte.ts` and must be parsed by the Svelte parser
  with the TypeScript sub-parser; `assets/config/eslint.config.svelte.js` shows
  the `files: ["**/*.svelte", "**/*.svelte.ts"]` override, without which a plain
  `export type` fails to parse.
- **Mutable URL params** inside a component: `SvelteURLSearchParams` from
  `svelte/reactivity`, or the linter objects.
- **Router**: `assets/svelte/lib/router.svelte.ts`, a history router in one
  file; links stay real `<a href>` and a body-level click interceptor handles
  them, so middle-click and new tabs work. nginx falls back to `index.html`.
- **Attributes are expressions.** `placeholder="\bORD-[0-9]{6}\b"` renders a
  bare `6`: Svelte reads `{6}`. Put regex text in a `String.raw` constant.
- **API client**: generated from `openapi.json` (`@hey-api/openapi-ts`), wrapped
  once in `lib/api.ts` with short names and an `ApiError` thrown on non-2xx,
  with `response` optional because a transport failure has none.
- **Class conflicts**: no `tailwind-merge`; a component never passes two
  utilities for the same property. Each `Button` variant owns its border colour.

## CSP

Production headers are `style-src 'self'; script-src 'self'; font-src` implied
by `default-src 'self'`. Consequences: no `style=` attribute anywhere, no CDN
fonts, no highlighter that injects styles. Verify a build by serving `dist/`
with the real header and reading the console; the checker catches the static
cases.

## Verify before you finish

`pnpm exec svelte-check`, `pnpm run lint`, `pnpm build`, then open the pages in
a browser in light and dark, French and English, and confirm no console error.
`grep -c 'style="' dist/index.html` should print 0.
