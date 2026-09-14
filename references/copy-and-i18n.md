# Copy and i18n

Every piighost surface is bilingual, French and English, down to the registry
manifests. Write both at once; a key present in one language only is a bug.

## Rules

- **No em-dash, no en-dash.** Write a sentence, a comma or a colon. The checker
  (`scripts/check_charter.py`) flags `—` and `–` in copy and dictionaries.
- **No model-flavoured phrasing.** No "leverage", "seamless", "robust",
  "delve", "unlock"; no exclamation marks; no rhetorical questions. Say what the
  thing does.
- **Detector-agnostic.** piighost is regex, NER or LLM alike; never present
  GLiNER or any model as the default. Offer them as peers.
- **French with accents**, including capitals (`É`), the œ ligature, and French
  spacing before `:` `;` `?` `!` (a non-breaking space in the string).
- **State the trade-off in the sentence.** The studio's playground note reads
  "Runs in a separate process, killed after two seconds" rather than "safe".
- **Numbers**: `tabular-nums`; units after a space; relative dates through
  `Intl.RelativeTimeFormat` with the current locale, not a hand-made string.

## Mechanics

Svelte: `assets/svelte/lib/i18n.svelte.ts`, a class with `locale = $state()`,
`t(key)` falling back to English, `pick({en, fr})` for registry-provided text,
persisted in `localStorage`, `document.documentElement.lang` kept in step. Keys
are dotted by page: `home.search`, `detail.pipeline`, `play.run`.

Next: `src/i18n/{en,fr}.ts` shape-checked against `types.ts`, `useT()` hook,
locale in a client context, `/en` and `/fr` route segments for static export.

## Examples

| Avoid | Write |
|---|---|
| Leverage our robust detectors — seamlessly! | Run a detector over your text. |
| What the model would receive (TOML) | What the model would receive |
| Erreur: pas de resultat | Erreur : aucun résultat |
| Loading… | Loading (with the spinner doing the ellipsis's job) |
