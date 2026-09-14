# Layouts

Four grammars cover every piighost surface so far. Pick the one that matches
the job, then reuse its recipe verbatim; a new grammar is a decision to record
here, not a page-level improvisation.

## 1. Catalogue (after the LangSmith Hub)

For a list of things a visitor searches, filters and opens.

```
┌───────────────────────────────────────────────────────────────┐
│ piighost hub / …                 Playground [Contribute] ◐ 🇬🇧 │  h-14 trail bar
├───────────────────────────────────────────────────────────────┤
│                        piighost hub                           │  font-mono text-4xl
│              one line of muted description                    │
│      ( search patterns, groups, configurations…       🔍 )    │  rounded-full h-14
├───────────────────────────────────────────────────────────────┤
│ [Relevance][Recently updated][Most used]…      46 results │ ▢ Type      │
│ ┌───────────────────────────────────────────┐  ▶           │ ☐ pattern 28│
│ │ (config)(fr)(eu)(chat)                    │              │ ☐ group   11│
│ │ piighost/fr-default                       │              │ ▢ Region    │
│ │ two-line description…                     │              │ ☐ fr      10│
│ │ ⚙ configuration • Updated 2 d • 🏷 11 • ⑂ 1 • 🔗 0    │              │ …           │
│ └───────────────────────────────────────────┘              │             │
│ … more rows …                                              │  sticky     │
│                 ‹ 1 2 3 ›                                  │  top-20     │
└───────────────────────────────────────────────────────────────┘
```

Recipe: hero `mx-auto max-w-3xl px-4 pt-14 pb-10 text-center`, then
`mx-auto max-w-7xl px-4 py-8` with `grid gap-8 lg:grid-cols-[minmax(0,1fr)_16rem]`.
Sort chips: `rounded-md border px-3 py-1.5 text-sm`, active `bg-muted font-medium
border-transparent`. Rows: `ObjectRow`, `space-y-3`. Sidebar: a card of
`FacetSection`s, `lg:sticky lg:top-20`. Filters live in the URL query, so a view
is shareable and the back button undoes a filter. Without a query, sort by date;
relevance is flat.

## 2. Detail (after a LangSmith prompt page)

For one object with a history.

```
┌───────────────────────────────────────────────────────────────┐
│ ⚙ piighost/fr-default (config)(fr)(eu)      [⧉] [⬇] [▶ Try it]│  title bar, border-b
│ one line of description                                       │
├─────────────────┬─────────────────────────────────────────────┤
│ Commit history 1│ ⑂ 240a672d (prod)(latest)  2 days ago       │
│ ┌─────────────┐ │ [Content] Pipeline file  Use it  Coverage   │  tabs: active bg-primary/10
│ │⑂ 240a672d   │ │ ┌ DETECTORS ─────────────────────────────┐  │
│ │ (prod)      │ │ │ regex-fr  regex  piighost/fr-extended…  │  │
│ │ 2 days ago  │ │ │ [FR_PHONE][FR_IBAN]…                    │  │
│ └─────────────┘ │ └────────────────────────────────────────┘  │
│                 │ ┌ STAGES ┐ …                                │
└─────────────────┴─────────────────────────────────────────────┘
```

Recipe: title bar `mx-auto max-w-7xl px-4 py-4 flex flex-wrap items-center gap-3`
with the reference in `font-mono text-xl font-bold`, then
`grid gap-8 lg:grid-cols-[17rem_minmax(0,1fr)]`. History cards
`rounded-lg p-3 ring-1 ring-foreground/10`, selected `bg-muted`. The right column
starts with the commit heading, then the tab strip, then `Card`s in
`flex flex-col gap-5`. Content first; the file, the snippets and the measurements
under their own tabs.

## 3. Workshop (the studio's Two-Up)

For anything a visitor configures, feeds a text, runs, and reads.

```
┌ [Run][Compare][Chat] ───────────────────────────────────────────┐
│ ① CONFIGURE       │ ② TEXT      [Input|Anonymized] [sample ▾] │ ③ RESULTS    │
│ (Object|Regex)    │ textarea → highlight when done            │ [EMAIL] a@b… │
│ ref select        │                                           │ [PHONE] …    │
│                   │                                           │ DROPPED      │
│ [▶ Run]           │                                           │ [CARD] lost… │
│ 0.2 ms · 3 kept   │ [Edit]                                    │              │
│ privacy note      │                                           │              │
└───────────────────┴───────────────────────────────────────────┴──────────────┘
```

Recipe: outer `mx-auto flex w-full max-w-[88rem] flex-col p-4 lg:h-[calc(100dvh-4rem)]`,
optional `Tabs`, then the card
`grid flex-1 divide-y overflow-hidden rounded-xl border bg-card shadow-sm lg:min-h-0
lg:grid-cols-[minmax(0,0.95fr)_minmax(0,1.9fr)_minmax(0,1.05fr)] lg:divide-x lg:divide-y-0`
holding three `Region`s. The primary action and its status line sit at the end
of the first column (`mt-auto`, `shrink-0`, never `sticky`: the `min-h-0
overflow-auto` context clips a sticky footer). Narrow screens stack the regions
in flow order. Same shell for playground, comparison, chat, contribution.

## 4. Marketing (the studio)

For a landing or a project page: full-height `Section`s with scroll-snap, a
centred eyebrow in primary uppercase, `text-3xl sm:text-4xl` titles, cards in
`grid gap-6 sm:grid-cols-2 lg:grid-cols-3`, a hero with a radial primary glow
(`bg-[radial-gradient(60%_50%_at_50%_0%,var(--primary)/12%,transparent)]`) and
two `xl` buttons, one primary and one outline with the GitHub mark. Navbar
`h-16`, footer three columns `py-12` and a `text-xs` MIT line.

## Choosing

| The page is… | Grammar |
|---|---|
| a searchable list | Catalogue |
| one object, possibly versioned | Detail |
| something to run on an input | Workshop |
| explaining or selling | Marketing |
| a reference list (labels, glossary) | Catalogue without sidebar: `max-w-4xl`, `grid gap-2 sm:grid-cols-2` of `bg-muted/40` rows |
