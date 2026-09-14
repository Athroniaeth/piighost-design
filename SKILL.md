---
name: piighost-design
description: The design system and front-end conventions of the piighost ecosystem (piighost-hub, piighost-studio, piighost-chat and any new piighost site) with ready-to-copy code. Covers the shadcn neutral tokens with the violet primary, Geist and Geist Mono, light-by-default dark-by-class theming, lucide icons, the three-column numbered workshop grammar, the LangSmith-style catalogue and detail layouts, the shared entity colour palette, bilingual FR/EN copy rules and the no-inline-style CSP constraint, for Svelte 5 + Vite and for Next.js + shadcn base-nova. Use it whenever a task builds, restyles, reviews or extends UI for anything piighost-related, or whenever the user says "match the studio", "like the hub", "piighost look", "PII highlight", "playground", "add a page", "design system", or names a piighost repository in a front-end context, even without asking for a charter explicitly.
license: MIT
metadata:
  author: Athroniaeth
  version: "1.0"
  sources: piighost-hub (Svelte 5), piighost-studio (Next.js)
---

# piighost design

One look for every piighost surface. This skill gives the tokens, the
component vocabulary, the four page layouts and the copy rules, plus the code
that already implements them in two stacks. Start from the assets and adapt;
do not redraw a button.

## 1. Pick the stack, load the right reference

| The project is… | Read | Scaffold |
|---|---|---|
| Svelte 5 + Vite, bundle behind nginx with an `/api` (the hub, the template) | [references/stack-svelte.md](references/stack-svelte.md) | `python scripts/scaffold.py svelte <src-dir>` |
| Next.js static export with shadcn base-nova (the studio) | [references/stack-next.md](references/stack-next.md) | `python scripts/scaffold.py react <src-dir>` |
| Something else on Tailwind v4 | tokens and layouts still apply; port the Svelte components, they are the smallest | copy `assets/tokens/app.css` |

Then, always: [references/tokens.md](references/tokens.md) for values,
[references/components.md](references/components.md) before writing a
component, [references/layouts.md](references/layouts.md) before laying out a
page, [references/entity-colors.md](references/entity-colors.md) when anything
shows a detected value, [references/copy-and-i18n.md](references/copy-and-i18n.md)
when writing a string a visitor reads.

## 2. The charter on one screen

- **Neutral scale, one accent.** shadcn `neutral` variables; the primary is
  violet, `oklch(0.51 0.23 277)` light and `oklch(0.62 0.19 277)` dark. Grey
  carries structure, the primary carries the one active thing, entity colours
  carry meaning. A second accent is a mistake.
- **Geist for text, Geist Mono for anything machine-read**: code, references
  (`piighost/fr-default:240a672d`), hashes, labels, the wordmark. Fonts are
  self-hosted, the CSP forbids a CDN.
- **Light by default, dark on request**, a class on `<html>` the visitor sets,
  remembered, never inferred from the system. Screenshots must match screens.
- **Radius 0.625rem.** Cards `rounded-xl` with `ring-1 ring-foreground/10`,
  controls and rows `rounded-md`, buttons and code `rounded-lg`, chips
  `rounded-full`.
- **Type in rem only.** The root font size grows at 1920 and 2560 px; a
  `text-[13px]` ignores that and looks small on the screens it targets.
- **No inline style, ever.** Production serves `style-src 'self'` without
  `unsafe-inline`; a `style=` attribute or a highlighter that injects styles
  works in development and silently breaks in production. Colours and syntax
  tokens are classes.
- **Icons are lucide**, line style, one import per icon.
- **Copy in French and English at once**, no em-dash, no model-flavoured
  phrasing, detector-agnostic wording.

## 3. Build from the vocabulary

Primitives: `Button` (default, outline, ghost, secondary, link; h-8 default),
`Badge` (secondary for tags, outline for facts, default for a pointer such as
`prod`), `Card`, `Segmented`, `Tabs`, `Region` + `StepChip`, `CodeBlock` +
`CopyButton`. Entities: `EntityLabel`, `EntityRow`, `EntityHighlight`, coloured
through `assignLabelColors()` built once per run. Furniture: `Breadcrumb` +
`SiteNav` (a slim trail bar, not a marketing navbar), `ObjectRow`,
`FacetSection`, `SamplePicker`, `Async`, `ThemeToggle`, `LangToggle`.

Native controls share one class string (`lib/ui.ts`: `FIELD`, `FIELD_MONO`,
`TEXTAREA`) instead of a wrapper per field. Eyebrow titles are
`text-xs font-semibold uppercase tracking-wide text-muted-foreground`.

Details, states and React equivalents: [references/components.md](references/components.md).

## 4. Lay the page out with one of four grammars

1. **Catalogue** (after the LangSmith Hub): centred mono title, pill search,
   sort chips, a vertical list of `ObjectRow`s, a right sidebar of checkbox
   facets with counts, filters in the URL.
2. **Detail**: title bar with the mono reference, pills and three actions
   (copy, download, primary "Try it"); a commit-history rail on the left; the
   selected commit with tabs on the right, content first.
3. **Workshop** (the studio's Two-Up): one `rounded-xl` card split into three
   numbered `Region`s, Configure, Text, Results, full height under the header,
   the primary action at the end of the first column with its status line.
4. **Marketing**: full-height `Section`s, eyebrow in primary uppercase, card
   grids, a hero with a radial primary glow.

Recipes and wireframes: [references/layouts.md](references/layouts.md).

## 5. Workflow

1. Read the stack reference, scaffold or copy the assets, keep file names.
2. Compose the page from the grammar. Before writing any component, list the
   project's `components/` and `components/ui/` and read
   [references/components.md](references/components.md): an agent that skips
   this reliably rebuilds a highlight or a list row that already exists, and the
   duplicate only hurts months later when a fix lands in one of the two. Add to
   the vocabulary only when nothing fits, and document the addition in the same
   change.
3. Write the copy in both languages as you go.
4. Run the checker on the source tree and fix every finding:
   ```bash
   python scripts/check_charter.py frontend/src
   ```
   It reports inline styles, px font sizes, em-dashes, `asChild`, raw hex
   colours, and an interface tree with no French in it, with the reason next to
   each. That last one exists because an agent building a page from scratch
   reliably ships it in English only: the copy rule is the easiest to read and
   the easiest to forget.
5. Verify in a real browser: light and dark, French and English, no console
   error, and the built bundle carries no `style=` attribute.

## 6. What good looks like

- A results column that truncates a value to make room for a hash is wrong;
  shorten the metadata (`email`, not `piighost/email:9d3fba58`).
- Two patterns claiming one span: show the kept one in the text and list the
  dropped one beside it as a muted `EntityRow` with "lost to X". Never draw
  two overlapping highlights.
- A copy button over a long code line sits on an opaque surface
  (`bg-card shadow-sm ring-1`) so the line passes under it, and the `<pre>`
  keeps `pe-12`.
- A score for one pattern is measured on the labels it emits, not the whole
  corpus, and the page says which; a number without its denominator is a lie.
- A single-language string, a hex colour, a `style=`, an em-dash or a
  `text-[13px]` is a defect, not a nit: each one breaks something a visitor
  sees, in production or on a large screen. Stating a rule is not following it;
  run the checker on your own output before you call the work done.

## Assets

- `assets/tokens/app.css` (Vite) and `assets/tokens/globals.css` (Next): the
  same tokens in the two stylesheet shapes.
- `assets/svelte/`: the hub's `ui/`, `components/` and `lib/`, Svelte 5 runes.
- `assets/react/`: the studio's playground components, `Section`, navbar,
  footer, shadcn base-nova primitives, and `lib/labels.ts`.
- `assets/config/`: `components.json` for shadcn, an ESLint config that parses
  `.svelte.ts` modules.
- `scripts/check_charter.py`, `scripts/scaffold.py`: standard-library Python.
