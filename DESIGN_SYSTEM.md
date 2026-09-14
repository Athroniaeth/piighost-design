# The piighost design system

For anyone about to write front-end code in `piighost-hub`, `piighost-studio`,
`piighost-chat` or any new piighost surface.

Every piighost site is meant to read as one product. That only works if we
share one set of parts. This page tells you which parts exist, where they live,
and what to do when none of them fit. **The parts are already written. Copy the
file, do not re-derive the classes.**

If you read nothing else, read [Do not build a button](#do-not-build-a-button)
and [Before you open a pull request](#before-you-open-a-pull-request).

Contents:

1. [The charter in ten lines](#the-charter-in-ten-lines)
2. [Do not build a button](#do-not-build-a-button)
3. [The vocabulary](#the-vocabulary-what-already-exists)
4. [Adding to the vocabulary](#adding-to-the-vocabulary)
5. [Tokens you will actually type](#tokens-you-will-actually-type)
6. [Pick one of four page layouts](#pick-one-of-four-page-layouts)
7. [Entity colours](#entity-colours)
8. [Copy, in French and English](#copy-in-french-and-english)
9. [The five rules that break production](#the-five-rules-that-break-production)
10. [Before you open a pull request](#before-you-open-a-pull-request)

---

## The charter in ten lines

- **Neutral scale, one accent.** shadcn `neutral` variables, with a violet
  primary. Grey carries structure, the primary carries the one active thing,
  entity colours carry meaning. A second accent is a mistake.
- **Geist for text, Geist Mono for anything machine-read**: code, references
  (`piighost/fr-default:240a672d`), hashes, labels, the wordmark.
- **Light by default, dark on a class** the visitor sets and we remember. Never
  inferred from the operating system, so a screenshot matches a screen.
- **Radius `0.625rem`.** Cards `rounded-xl`, controls and rows `rounded-md`,
  buttons and code `rounded-lg`, chips `rounded-full`.
- **Type in rem only.** The root font size grows at 1920 and 2560 px.
- **No inline style, ever.** Production serves `style-src 'self'`.
- **Icons are lucide**, line style, one import per icon.
- **Both languages at once**, French and English, written as you go.
- **Four page layouts**, not five. Pick the one that matches the job.
- **Run the checker before you call it done.**

### Then read your stack's page once

The rules above are shared. The traps are per stack, and they cost an afternoon
each if you meet them by surprise.

- Svelte 5 + Vite (the hub, the template):
  [`references/stack-svelte.md`](references/stack-svelte.md). Runes only, the
  one-file history router, why `.svelte.ts` needs its own ESLint override, and
  why `placeholder="\bORD-[0-9]{6}\b"` renders a bare `6`.
- Next.js static export + shadcn base-nova (the studio):
  [`references/stack-next.md`](references/stack-next.md).

---

## Do not build a button

This is the single most common way a contribution drifts. The sequence that
produces a second button is always the same: you need an action, you do not know
what exists, you write `<button class="px-4 py-2 rounded bg-violet-600 ...">`,
it looks approximately right, it ships. Six months later somebody fixes a focus
ring in `Button.svelte` and your button keeps the bug.

**Before you write any component, list what is already there:**

```bash
ls frontend/src/components/ui frontend/src/components   # hub, Svelte 5 + Vite
ls src/components/ui src/components                     # studio, Next.js
```

Then read [`references/components.md`](references/components.md). An agent or a
human who skips that step reliably rebuilds a highlight or a list row that
already exists.

### The button, concretely

One component, in `ui/Button.svelte` and `ui/button.tsx`. It already covers
every case you are likely to have.

| You want | Use |
|---|---|
| The main action of a screen | `<Button>` (variant `default`, violet) |
| A secondary action beside it | `<Button variant="outline">` |
| A quiet action in a toolbar or a row | `<Button variant="ghost">` |
| A tinted, non-primary action | `<Button variant="secondary">` |
| Something that is really a link | `<Button variant="link">` |
| An icon only | `<Button size="icon">` (`icon-sm`, `icon-lg`) |
| A hero call to action | `<Button size="xl">` |

Sizes are `default` (h-8), `sm` (h-7), `lg` (h-9), `xl` (h-12), `icon` (size-8),
`icon-sm` (size-7), `icon-lg` (size-9). The default is `h-8` on purpose: piighost
screens are dense.

Roughly one `default` button per screen, since it marks the reason the screen
exists. A few `outline`, as many `ghost` as the furniture needs. Two violet
buttons side by side means neither is the primary action.

**Do not restyle a variant at the call site.** If `outline` is not right, the
answer is a different variant, not `class="border-primary text-primary"`. The
`class` prop is for layout only: `w-full`, `mt-auto`, `shrink-0`.

**Icons need no sizing.** The base classes size any `svg` child to `size-4`,
and the `sm` and `xl` sizes override that. Import one lucide icon per file.

Two things the component already handles that a hand-rolled button does not:

- **Give it `href` and it renders an `<a>`.** Middle-click, "open in new tab"
  and crawlers keep working. Never wrap a `Button` in an anchor.
- **Each variant owns its border colour.** `border-transparent` in the base and
  `border-border` in a variant both set the same property, and stylesheet order,
  not class order, decides the winner. This is why we do not use
  `tailwind-merge` and why a component must never pass two utilities for the
  same property.

In React, compose with base-ui's `render` prop, never `asChild`:

```tsx
<Button render={<Link href="/fr/playground" />}>Ouvrir le playground</Button>
```

### The same applies to native inputs

There is no wrapper component per field. There is one class string per control,
in `lib/ui.ts`:

```ts
import { FIELD, FIELD_MONO, TEXTAREA, EYEBROW } from "../lib/ui";
```

There is no `$lib` alias: that is SvelteKit, and the hub is plain Vite. Imports
are relative, and `tsconfig.json` maps `@/*` to `./src/*` if you prefer that.

`FIELD` for a normal input or select, `FIELD_MONO` for ids and patterns,
`TEXTAREA` for the text areas, `EYEBROW` for an uppercase section title. If you
find yourself typing `rounded-md border bg-background px-2.5 py-1.5`, you are
rewriting `FIELD`.

---

## The vocabulary: what already exists

Svelte 5 versions in `assets/svelte/`, React versions in `assets/react/`.

**Primitives.** `Button`, `Badge`, `Card`, `Segmented`, `Tabs`, `Region` +
`StepChip`, `CodeBlock` + `CopyButton`.

**Entities.** `EntityLabel` (a coloured label chip), `EntityRow` (one detection
in a results list), `EntityHighlight` (a text with its kept spans tinted in
place). Colours come from `assignLabelColors()`, built once per run.

**Page furniture.** `Breadcrumb` + `SiteNav` (a slim trail bar, not a marketing
navbar), `ObjectRow` (one catalogue row), `FacetSection` (a collapsible filter
group), `SamplePicker`, `Async` (spinner, error with retry, content; use it rather
than writing an `{#if loading}` ladder, so no page forgets the error case),
`ThemeToggle`, `LangToggle`, `KindIcon`, `GithubIcon`.

**Studio only.** `Section`, `ProjectCard`, `FieldLabel`, `RunStatus`,
`LoadingPane`, `PlaygroundTabs`.

Full table with states and per-stack notes:
[`references/components.md`](references/components.md).

### States every interactive component owes the visitor

| State | What it looks like |
|---|---|
| Idle or empty | A `text-sm text-muted-foreground` hint saying what to do |
| Busy | `Loader2 animate-spin` in the primary button, label switches to a present participle; inputs stay enabled where a live value matters. Do not swap in a different component |
| Done | The text area becomes a read-only `EntityHighlight` with an `outline` Edit button beside it |
| Error | A `text-destructive` line under the action, with a retry where a retry makes sense |
| Focus | `focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50`. Never removed. |

---

## Adding to the vocabulary

Sometimes nothing fits. That is fine. The rule is that it becomes a shared part
rather than a local one.

1. Check again that nothing fits. Most "new" components are an existing one with
   different content.
2. Build it as a component in `ui/` (a primitive) or `components/` (a piighost
   concept), not inline in the page.
3. Use the tokens, not values. If you need a colour that is not in the token
   set, that is a design decision, so raise it before you write it.
4. **Document it in the same change**: add a row to
   [`references/components.md`](references/components.md), and add the file to
   `assets/` if other piighost sites will want it.

A new *page layout* is a bigger decision than a new component. There are four
grammars; a fifth is recorded in [`references/layouts.md`](references/layouts.md)
after a discussion, not improvised in a page.

---

## Tokens you will actually type

Never write a hex colour in a component. Light and dark would drift apart, and
the checker flags it.

| Need | Class |
|---|---|
| Page surface | `bg-background text-foreground` |
| Raised surface | `bg-card` |
| Secondary text, metadata, eyebrows | `text-muted-foreground` |
| A row, a soft chip | `bg-muted/40` |
| Under code | `bg-muted/30` |
| The one active thing | `bg-primary/10 text-primary` |
| A primary surface | `bg-primary text-primary-foreground` |
| Hairline | `border-border`, or `ring-1 ring-foreground/10` |
| Error | `text-destructive` |

The primary is violet, `oklch(0.51 0.23 277)` light and `oklch(0.62 0.19 277)`
dark. Values and the full table: [`references/tokens.md`](references/tokens.md).

**Type scale in practice:**

| Role | Classes |
|---|---|
| Marketing page title | `text-3xl sm:text-4xl font-bold tracking-tight text-balance` |
| Tool page title | `text-xl font-semibold tracking-tight` |
| An object reference used as a title | `font-mono text-lg font-semibold tracking-tight` |
| Eyebrow, region title, card title | `text-xs font-semibold uppercase tracking-wide text-muted-foreground` |
| Body | `text-sm`; long marketing copy `text-base` or `text-lg text-muted-foreground` |
| Metadata and help | `text-xs text-muted-foreground`, plus `tabular-nums` for figures |
| Code, ids, entity surfaces | `font-mono text-sm` or `text-xs` |

**Rhythm:** container `mx-auto max-w-6xl px-4` (tools `max-w-7xl` or
`max-w-[88rem]`), page `py-8`, between cards `gap-5` or `gap-6`, inside a card
`space-y-3`, between controls `gap-2`.

**Card:** `rounded-xl bg-card ring-1 ring-foreground/10 p-4 text-sm`. A ring
rather than a border, because it survives `divide-*` and dark mode alike. A
linked card gets `hover:ring-primary`.

---

## Pick one of four page layouts

| Your page is | Grammar |
|---|---|
| A searchable list | **Catalogue** |
| One object, possibly versioned | **Detail** |
| Something a visitor runs on an input | **Workshop** |
| Explaining or selling | **Marketing** |
| A flat reference list (labels, glossary) | Catalogue without the sidebar: `max-w-4xl`, `grid gap-2 sm:grid-cols-2` of `bg-muted/40` rows |

- **Catalogue**, after the LangSmith Hub: centred mono title, pill search, sort
  chips, a vertical list of `ObjectRow`s, a right sidebar of checkbox facets with
  counts. Filters live in the URL query, so a view is shareable and the back
  button undoes a filter.
- **Detail**: title bar with the mono reference, pills and three actions (copy,
  download, primary "Try it"), a commit-history rail on the left, the selected
  commit with tabs on the right. Content first; the file, the snippets and the
  measurements go under their own tabs.
- **Workshop**, the studio's Two-Up: one `rounded-xl` card split into three
  numbered `Region`s, Configure, Text, Results, full height under the header.
  The primary action and its status line sit at the end of the first column
  (`mt-auto shrink-0`, never `sticky`: the `min-h-0 overflow-auto` context clips
  a sticky footer). Same shell for playground, comparison, chat and contribution.
- **Marketing**: full-height `Section`s with scroll-snap, a centred eyebrow in
  primary uppercase, card grids, a hero with a radial primary glow.

Wireframes and copyable class strings:
[`references/layouts.md`](references/layouts.md).

---

## Entity colours

Detected values are the product, so their colours are a shared asset, not a
per-page choice. `lib/labels.ts` holds the same palette in both stacks, so an
`FR_NIR` chip in the hub and in the studio share a hue.

1. **Fixed labels keep a fixed style.** `PERSON` and `PER` on the primary,
   `ORGANIZATION` and `ORG` amber, `ADDRESS` and `LOC` emerald. These are the
   labels a visitor sees most, and they never move.
2. **Everything else is assigned by first appearance**, through
   `assignLabelColors(labels)`. **Build the map once per run, from every label
   seen including the dropped ones**, and pass it down. If you rebuild it from
   the visible labels, colours shift the moment a threshold hides an entity.
3. **Outside a run, hash**: `labelStyle(label)` gives a lone chip a stable hue
   across pages.
4. **Shape**: `rounded px-1.5 py-0.5 font-mono text-xs font-medium` for a chip,
   `rounded px-1` for an in-text span.

Two gotchas worth knowing before you debug grey chips: every class string is
spelled out in full so Tailwind's scanner keeps it, and the palette module has
to be reachable by that scanner. An unanchored `lib/` line in `.gitignore` hides
it and every chip goes grey. Declare `@source "./lib/labels.ts";` in the
stylesheet as a belt.

Never draw two overlapping highlights. When two patterns claim one span, show
the kept one in the text and list the dropped one beside it as a muted
`EntityRow` reading "lost to X".

More: [`references/entity-colors.md`](references/entity-colors.md).

---

## Copy, in French and English

Every piighost surface is bilingual, down to the registry manifests. Write both
at once; a key present in one language only is a bug, and it is the miss that
surfaces last, when somebody switches the language and reads English back.

- **No em-dash, no en-dash.** Write a sentence, a comma or a colon.
- **No model-flavoured phrasing.** No "leverage", "seamless", "robust", "delve",
  "unlock"; no exclamation marks; no rhetorical questions. Say what the thing
  does.
- **Detector-agnostic.** piighost is regex, NER or LLM alike. Never present
  GLiNER or any model as the default; offer them as peers.
- **French with accents**, including on capitals (`É`), the `œ` ligature, and
  French spacing before `:` `;` `?` `!` (a non-breaking space in the string).
- **State the trade-off in the sentence.** "Runs in a separate process, killed
  after two seconds" beats "safe".
- **Numbers**: `tabular-nums`, units after a space, relative dates through
  `Intl.RelativeTimeFormat` with the current locale rather than a hand-made
  string.

| Avoid | Write |
|---|---|
| Leverage our robust detectors, seamlessly! | Run a detector over your text. |
| Erreur: pas de resultat | Erreur : aucun résultat |
| `Loading...` | `Loading` (the spinner does the ellipsis's job) |

Mechanics per stack: [`references/copy-and-i18n.md`](references/copy-and-i18n.md).

---

## The five rules that break production

These are not style preferences. Each one breaks something a visitor sees.

1. **No `style=` attribute.** Production headers are `style-src 'self'` with no
   `unsafe-inline`. An inline style works perfectly in development and is
   silently dropped in production. This also rules out CDN fonts and any syntax
   highlighter that injects styles. For a determinate progress bar under that
   policy, use the native `<progress value max>` element styled with
   `accent-primary`, or an indeterminate pulse.
2. **No arbitrary pixel font size.** `text-[13px]` ignores the root font size
   bump at 1920 and 2560 px and looks abruptly small on exactly the screens it
   was tuned for. Use the scale, or rem: `text-[0.8125rem]`.
3. **No raw hex colour** outside the token files. Light and dark drift apart.
4. **No `asChild`** in React. The base-ui variant of shadcn composes with
   `render`.
5. **No single-language string, and no em-dash.**

Treat a finding as a defect, not a nit. Stating a rule is not following it.

---

## Before you open a pull request

Run the checker on your source tree and fix every finding:

```bash
python scripts/check_charter.py frontend/src
```

It reports inline styles, pixel font sizes, em-dashes, `asChild`, raw hex
colours, and an interface tree with no French in it, with the reason next to
each. It exits non-zero when anything is found.

Then the stack gate:

```bash
# hub / Svelte 5 + Vite
pnpm exec svelte-check && pnpm run lint && pnpm build
grep -c 'style="' dist/index.html     # must print 0

# studio / Next.js
pnpm lint && pnpm test && pnpm build  # must succeed as a static export
```

Then look at it, in a browser:

- [ ] Light and dark, both readable, no washed-out chip
- [ ] French and English, both complete
- [ ] No console error
- [ ] Focus ring visible on every interactive element, keyboard only
- [ ] Narrow viewport: the layout stacks in a sensible order
- [ ] Nothing in the diff duplicates a component that already exists

### What good looks like

- A results column that truncates a value to make room for a hash is wrong.
  Shorten the metadata instead: `email`, not `piighost/email:9d3fba58`.
- A copy button over a long code line sits on an opaque surface
  (`bg-card shadow-sm ring-1`) so the line passes under it, and the `<pre>`
  keeps `pe-12`.
- A score for one pattern is measured on the labels it emits, not the whole
  corpus, and the page says which. A number without its denominator is a lie.

---

## Where things live

```
SKILL.md                 the charter for coding agents
DESIGN_SYSTEM.md         this page, for people
references/
  tokens.md              colours, type, radius, spacing, theme, icons
  components.md          the vocabulary, states, Svelte and React notes
  layouts.md             catalogue, detail, workshop, marketing, with recipes
  entity-colors.md       the shared palette for detected values
  copy-and-i18n.md       bilingual copy rules
  stack-svelte.md        Svelte 5 + Vite specifics and the CSP
  stack-next.md          Next.js static export and shadcn base-nova specifics
assets/
  tokens/                app.css (Vite) and globals.css (Next)
  svelte/                ui primitives, entity components, lib modules
  react/                 studio components, shadcn primitives, labels.ts
  config/                components.json, ESLint config for .svelte.ts
scripts/
  check_charter.py       the checker described above
  scaffold.py            copies tokens and components into a project
```

Starting a new piighost surface:

```bash
python scripts/scaffold.py svelte frontend/src   # Svelte 5 + Vite
python scripts/scaffold.py react src             # Next.js + shadcn
```

Keep the file names the scaffold gives you. Two pages built a month apart
looking like one page is the entire point.

The reference implementations are
[piighost-hub](https://github.com/Athroniaeth/piighost-hub) for Svelte 5 and
[piighost-studio](https://github.com/Athroniaeth/piighost-studio) for Next.js.
When this page and the code in `assets/` disagree, the code is right and this
page needs a fix.
