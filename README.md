# piighost-design

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

## What is inside

```
SKILL.md                 the charter on one screen, the workflow, the pointers
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
