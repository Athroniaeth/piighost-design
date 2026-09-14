# Entity colours

Detected values are the product. Their colours are therefore a shared asset,
not a per-page choice: `assets/svelte/lib/labels.ts` and `assets/react/lib/labels.ts`
hold the same palette, so a `FR_NIR` chip in the hub and in the studio's
playground share a hue.

## Rules

1. **Fixed labels keep a fixed style.** `PERSON`/`PER` on the primary
   (`bg-primary/10 text-primary`), `ORGANIZATION`/`ORG` amber,
   `ADDRESS`/`LOC` emerald. These are the labels a visitor sees most; they should
   never move.
2. **Everything else is assigned by first appearance** through a fifteen-hue
   palette at two intensities (`assignLabelColors(labels)`), so the first
   fifteen distinct labels in a run each get their own hue before any repeats.
   Build the map once per run from every label seen, dropped ones included, and
   pass it down: colours must not change when a threshold hides an entity.
3. **Outside a run, hash.** A chip shown alone (a catalogue card, a label
   reference) uses `labelStyle(label)`, which hashes the name into the first
   fourteen hues so one label keeps one hue across pages.
4. **Shape**: `rounded px-1.5 py-0.5 font-mono text-xs font-medium` for a chip,
   `rounded px-1` for an in-text span. Tint at `/15`, text at `-700` in light
   and `-300` in dark. Each class string is spelled out in full so Tailwind
   keeps it; the palette module must be reachable by Tailwind's scanner (a
   `.gitignore` rule such as an unanchored `lib/` hides it, and every chip goes
   grey; declare `@source "./lib/labels.ts";` in the stylesheet as a belt).

## Placeholders

The pipeline emits `<<LABEL:n>>`. Show a token in mono, tinted with the
primary (`rounded bg-primary/10 px-1 font-mono text-primary`) when it stands
alone, plain mono inside an anonymised text.
