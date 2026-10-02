# piighost-design

> [!WARNING]
> **Superseded, archived.** This is the version 1 design system (Geist, a 0.625rem radius, the old violet). Its values and components no longer match what ships.
> The current identity (Schibsted Grotesk and IBM Plex Mono, a 0.25rem radius, dark by default) is maintained in a separate repository. Its tokens ship in [`piighost-site/frontend/src/app.css`](https://github.com/Athroniaeth/piighost-site/blob/main/frontend/src/app.css), and the Svelte components that follow it are in [piighost-site](https://github.com/Athroniaeth/piighost-site) and [piighost-hub](https://github.com/Athroniaeth/piighost-hub).

An [Agent Skill](https://agentskills.io) that gives Claude Code (and any
compatible agent) the design system of the piighost ecosystem: tokens,
components, page layouts, copy rules, and the code that implements them in
Svelte 5 and in Next.js.

Sources: [piighost-hub](https://github.com/Athroniaeth/piighost-hub) (Svelte 5 +
Vite, the reference implementation) and
[piighost-studio](https://github.com/Athroniaeth/piighost-studio) (Next.js +
shadcn base-nova).

## Install

```bash
# for one project
git clone https://github.com/Athroniaeth/piighost-design .claude/skills/piighost-design

# for every project on this machine
git clone https://github.com/Athroniaeth/piighost-design ~/.claude/skills/piighost-design
```

Claude Code reads `SKILL.md` and loads the references and assets on demand.

## For people

Working on a piighost front end by hand rather than with an agent, read
[DESIGN_SYSTEM.md](DESIGN_SYSTEM.md): the same system addressed to a human
contributor, with the vocabulary that already exists, the button rules, how to
add to the vocabulary, the rules that break production when ignored, and the
pre-pull-request checklist. Start there rather than inventing a button.

## What is inside

```
SKILL.md                 the charter on one screen, the workflow, the pointers
DESIGN_SYSTEM.md         the same system for human contributors
references/
  tokens.md              colours, type, radius, spacing, theme, icons
  components.md          the vocabulary, states, Svelte and React notes
  layouts.md             catalogue, detail, workshop, marketing, with recipes
  entity-colors.md       the shared palette for detected values
  copy-and-i18n.md       bilingual copy rules
  stack-svelte.md        Svelte 5 + Vite specifics and CSP
  stack-next.md          Next.js static export + shadcn base-nova specifics
assets/
  tokens/                app.css (Vite) and globals.css (Next)
  svelte/                ui primitives, entity components, lib modules
  react/                 studio components, shadcn primitives, labels.ts
  config/                components.json, ESLint config for .svelte.ts
scripts/
  check_charter.py       flags inline styles, px font sizes, em-dashes, asChild, hex colours
  scaffold.py            copies tokens and components into a project
evals/                   prompts used to test the skill
```

## Check a project

```bash
python scripts/check_charter.py frontend/src
```

## License

MIT.
