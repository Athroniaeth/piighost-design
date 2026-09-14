# Evaluation

Three tasks, each run twice: once by an agent that loaded this skill, once by
an agent that did not. The baseline was allowed to read the piighost-hub source,
because that is the realistic alternative to a skill: go and look at the
existing repository.

Two of the three pairs completed; the third (a new catalogue page) was cut short
by a rate limit and is still worth running.

| Task | With the skill | Without |
|---|---|---|
| Build a settings page from scratch for a project where nothing exists yet | 6/6 | 5/6 |
| Review a non-compliant component and rewrite it | 6/6 | 5/6 |

## What the skill changed

**Bilingual copy.** The baseline wrote a good-looking settings page in English
only, with no dictionary at all and its strings inline in the markup. Every
piighost surface is bilingual; that is the kind of omission nobody notices until
someone switches the language. The skill's run shipped an `EN`/`FR` pair, a
language toggle and French spacing.

**Obeying the rule it just stated.** Both runs of the review task found the
inline styles, the pixel font sizes, the hex colours and the em-dash. The
baseline then left an em-dash in its own review. The skill's run did not, and
that is what `scripts/check_charter.py` is for: a rule an agent restates is not
a rule an agent follows.

**What the baseline got right.** With the hub source to read, it recovered the
tokens, the fonts, the dark-mode class and the button shape. That is the honest
result: the charter is legible from the code. The skill's value is the part that
is not in any one file, the copy rules, the layout grammars, and a checker that
runs.

## Reproducing

Prompts and assertions are in `evals/evals.json`. Run each with and without the
skill, then grade with the checker plus a read of the outputs.
