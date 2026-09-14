# Tokens

One set of tokens, two stylesheets: `assets/tokens/app.css` for a Vite or
SvelteKit project, `assets/tokens/globals.css` for a Next.js project generated
by shadcn. Both declare the same variables with the same values, so a screen
from the hub and a screen from the studio read as one product.

## Colours

The scale is shadcn's `neutral` base with one violet primary. Everything else
is grey, which is what lets the entity colours and the primary carry meaning.

| Token | Light | Dark | Use |
|---|---|---|---|
| `--background` | `oklch(1 0 0)` | `oklch(0.145 0 0)` | page |
| `--foreground` | `oklch(0.145 0 0)` | `oklch(0.985 0 0)` | text |
| `--card` | `oklch(1 0 0)` | `oklch(0.205 0 0)` | raised surfaces |
| `--primary` | `oklch(0.51 0.23 277)` | `oklch(0.62 0.19 277)` | the one accent: primary buttons, active tab, links, step chips |
| `--primary-foreground` | `oklch(0.98 0 0)` | `oklch(0.13 0 0)` | text on primary |
| `--secondary` / `--muted` / `--accent` | `oklch(0.97 0 0)` | `oklch(0.269 0 0)` | tints for rows, pills, code backgrounds |
| `--muted-foreground` | `oklch(0.556 0 0)` | `oklch(0.708 0 0)` | secondary text, metadata, eyebrows |
| `--border` / `--input` | `oklch(0.922 0 0)` | `oklch(1 0 0 / 10%)` | hairlines |
| `--ring` | same as primary | same as primary | focus |
| `--destructive` | `oklch(0.577 0.245 27.325)` | `oklch(0.704 0.191 22.216)` | errors, deletion |

Tailwind classes map one to one: `bg-background`, `text-muted-foreground`,
`border-border`, `ring-ring/50`, `bg-primary/10`. Never write a hex colour in a
component: light and dark would drift apart, and the checker flags it.

Two tints do most of the work: `bg-muted/40` for a row or a soft chip,
`bg-primary/10 text-primary` for an active state, a step chip, or a `PERSON`
entity. `bg-muted/30` under code.

## Type

- **Text**: Geist. **Code, references, hashes, labels, the wordmark**: Geist Mono.
- Vite: `@import "@fontsource-variable/geist"; @import "@fontsource-variable/geist-mono";`
  then `--font-sans: "Geist Variable", …; --font-mono: "Geist Mono Variable", …`.
  Self-hosted on purpose: a CSP of `default-src 'self'` allows no font CDN.
- Next: `Geist` and `Geist_Mono` from `next/font/google` with the
  `--font-geist-sans` / `--font-geist-mono` variables, as `globals.css` expects.
- The root font size grows on large displays: `18px` at 1920, `21px` at 2560.
  Everything is in rem so this acts like a browser zoom. **Never `text-[13px]`**;
  use the scale (`text-xs`, `text-sm`) or rem (`text-[0.8125rem]`).

Scale in practice:

| Role | Classes |
|---|---|
| Page title (marketing) | `text-3xl sm:text-4xl font-bold tracking-tight text-balance` |
| Page title (tool) | `text-xl font-semibold tracking-tight` |
| Object reference as title | `font-mono text-lg font-semibold tracking-tight` |
| Eyebrow / region / card title | `text-xs font-semibold uppercase tracking-wide text-muted-foreground` |
| Body | `text-sm`; long marketing copy `text-base` or `text-lg text-muted-foreground` |
| Metadata, help, notes | `text-xs text-muted-foreground`, `tabular-nums` for figures |
| Code, entity surfaces, ids | `font-mono text-sm` or `text-xs` |

## Radius, spacing, surfaces

- `--radius: 0.625rem`. Cards and workshop shells `rounded-xl`, controls and
  rows `rounded-md` (`rounded-lg` for buttons and code blocks), pills and step
  chips `rounded-full`.
- Card: `rounded-xl bg-card ring-1 ring-foreground/10 p-4 text-sm` (a ring, not
  a border: it survives `divide-*` and dark mode alike). Hover on a linked card:
  `hover:ring-primary`.
- Rhythm: container `mx-auto max-w-6xl px-4` (tools `max-w-7xl` or
  `max-w-[88rem]`); page `py-8`; between cards `gap-5` or `gap-6`; inside a
  card `space-y-3`; between controls `gap-2`; workshop region `p-4` with a
  `mb-3` header.
- Native controls share one class string rather than a wrapper each:
  `w-full rounded-md border bg-background px-2.5 py-1.5 text-xs` (`font-mono`
  variant for ids and patterns). See `assets/svelte/lib/ui.ts`.

## Theme

Light by default, dark as a class on `<html>`, toggled by the visitor and
remembered, never inferred from the system. The studio does this so a
screenshot and the visitor's screen match. Vite: `assets/svelte/lib/theme.svelte.ts`
and `@custom-variant dark (&:is(.dark *));`. Next: `next-themes` with
`attribute="class" defaultTheme="light" enableSystem={false}`.

## Icons

lucide, line style, one import per icon (`@lucide/svelte/icons/copy`,
`lucide-react`). Default `size-4` inside buttons, `size-5` in the nav bar,
`size-3` inside chips. A GitHub mark is the one custom SVG (`GithubIcon`).

## Syntax highlighting

Classes, never inline styles. The hub tokenises TOML and regex itself
(`assets/svelte/lib/highlight.ts`) and colours with `.tok-*` classes declared
in `app.css`. The studio uses Shiki with CSS-variable themes and forces the
colour through classes (`.shiki span { color: var(--shiki-light) }`).
