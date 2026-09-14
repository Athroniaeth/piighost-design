# Components

The vocabulary, in the order a page is usually assembled. Svelte 5 versions
live in `assets/svelte/`, React ones in `assets/react/`. Copy the file rather
than re-deriving the classes: the point of a shared vocabulary is that two
pages built a month apart look like one.

## Primitives (`assets/svelte/ui/`, `assets/react/ui/`)

| Component | What it is | Notes |
|---|---|---|
| `Button` | shadcn base-nova button | Variants `default`, `outline`, `ghost`, `secondary`, `link`; sizes `default` h-8, `sm` h-7, `lg` h-9, `xl` h-12, `icon`, `icon-sm`, `icon-lg`. Renders an `<a>` when given `href`, so a link stays a link. Each variant owns its border colour, because `border-transparent` in the base and `border-border` in a variant both set the same property and the stylesheet order, not the class order, decides. React: base-ui composes with `render={<Link/>}`, never `asChild`. |
| `Badge` | 1.25rem pill | `secondary` for tags, `outline` for a kind or a neutral fact, `default` (primary) for a pointer tag such as `prod`. Link-aware. |
| `Card` | `rounded-xl bg-card ring-1 ring-foreground/10 py-4 text-sm` | Optional eyebrow title and an `action` slot on the right. Inner padding `px-4`. |
| `Segmented` | pill toggle | Track `rounded-lg border bg-muted/40 p-1`, active option `bg-background shadow-sm`, inactive `text-muted-foreground`. Two to four options, one value. |
| `Tabs` | link tabs between sibling pages | Same look as `Segmented` but each option is a real `<a>` with `aria-current`. Content tabs inside a page use plain buttons with `bg-primary/10 text-primary` when active (see the detail page). |
| `Region` | one column of a workshop card | `p-4`, header `mb-3` with an optional `StepChip`, an uppercase title, an optional action; body `flex min-h-0 flex-1 flex-col`. Both playground pages and the contribution page import this same piece. |
| `StepChip` | numbered glyph | `size-5 rounded-full bg-primary/10 font-mono text-xs text-primary`; a check once done. |
| `CodeBlock` | code with a copy button | `rounded-lg border bg-muted/30 p-4 pe-12 font-mono text-sm`; the copy button sits top right on an opaque surface so a long line passes under it. Highlighting is class-based. |
| `CopyButton` | ghost icon button | `Copy` then `Check` for 1.5 s. |

## Entity vocabulary (`assets/svelte/components/`, `assets/react/components/`)

| Component | Use |
|---|---|
| `EntityLabel` | A coloured label chip: `rounded px-1.5 py-0.5 font-mono text-xs font-medium` plus a palette class. See `entity-colors.md`. |
| `EntityRow` | One detection in a results list: `rounded-md bg-muted/40 p-2`, label chip, mono surface text, a muted trailing note (score, pattern, "lost to"). `muted` for a dropped detection. |
| `EntityHighlight` | A text with its kept spans tinted in place, `rounded px-1` per span, `title` with label and detector. Only kept spans are drawn; dropped ones are listed beside the text, since two overlapping highlights cannot both be shown. |

## Catalogue and page furniture

| Component | Use |
|---|---|
| `Breadcrumb` + `SiteNav` | The LangSmith-style trail bar, `h-14`, wordmark then `/ segment / segment`; right side: two actions, GitHub, theme, language. |
| `ObjectRow` | One catalogue row: pills, mono reference as title, two-line description, metadata line with icons, a square "Try it" button top right. |
| `FacetSection` | A collapsible facet group: `details/summary`, checkbox rows with a count pill `rounded-full bg-muted px-1.5 text-xs tabular-nums`. |
| `SamplePicker` | A `<select>` that resets to its placeholder after each pick, so the same sample can be loaded twice. |
| `Async` | Promise renderer: spinner row, error with retry, content snippet. Every page loads from an API; one component means no page forgets a state. |
| `ThemeToggle`, `LangToggle`, `GithubIcon`, `KindIcon` | Sun/Moon, a flag plus language name, the GitHub mark, one lucide glyph per object kind. |

## Studio-only pieces (`assets/react/components/`)

`Section` (marketing section: eyebrow in primary uppercase, `text-3xl sm:text-4xl`
title, `max-w-2xl` description, `py-16`, full-height scroll-snap),
`ProjectCard` (linked card with `hover:border-primary` and an arrow that slides
on hover), `FieldLabel` (label with a `?` help tooltip), `RunStatus`,
`LoadingPane` (spinner, title, progress track), `PlaygroundTabs`.

A determinate progress bar is the one place a value has to reach the style
layer. Under the hub's CSP an inline `style` is blocked, so use the native
`<progress value max>` element (styled through `accent-primary` and height
classes) or an indeterminate pulse; the studio's `LoadingPane` sets a width
inline because the studio is not served under that policy.

## States every interactive component shows

- **Idle / empty**: a `text-sm text-muted-foreground` hint saying what to do.
- **Busy**: the primary button shows `Loader2 animate-spin` and its label switches
  to a present participle; the inputs stay enabled where a live value matters
  (a threshold slider, for instance).
- **Done**: the text area becomes a read-only `EntityHighlight` with an
  `outline` `Edit` button beside it; results list in `EntityRow`s.
- **Error**: `text-destructive` line under the action, with a retry where a retry
  makes sense.
- **Focus**: never removed. `focus-visible:border-ring focus-visible:ring-3
  focus-visible:ring-ring/50`.
