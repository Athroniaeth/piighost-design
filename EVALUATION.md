# Evaluation

Three tasks, each run twice: once by an agent that loaded this skill, once by
an agent that did not. The baseline was allowed to read the piighost-hub source,
because that is the realistic alternative to a skill: go and look at the
existing repository.

| Task | With the skill | Without |
|---|---|---|
| Build a settings page from scratch for a project where nothing exists yet | 6/6 | 5/6 |
| Review a non-compliant component and rewrite it | 6/6 | 5/6 |
| Add a catalogue page to the existing site | 6/6 | 5/6 |

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

**Reusing the vocabulary instead of re-deriving it.** On the catalogue page,
both runs produced a correct, bilingual, URL-filtered page that passes the
checker. The baseline got there by writing an `AnnotatedText` component that
duplicates `EntityHighlight` and a `SampleRow` that duplicates `ObjectRow`. The
skill's run reused both and added one small helper. Nothing about the duplicate
is wrong on the day it ships; it is wrong six months later, when a change to the
highlight lands in one of the two.

**What the baseline got right.** With the hub source to read, it recovered the
tokens, the fonts, the dark-mode class, the button shape, the URL-filter
convention and, on that task, the bilingual copy. That is the honest result: a
charter is largely legible from the code that follows it. The skill earns its
place where the code cannot speak, on a project that has none yet, on the rules
no file states, and on knowing which component already exists.

## Reproducing

Prompts and assertions are in `evals/evals.json`. Run each with and without the
skill, then grade with the checker plus a read of the outputs.

## Triggering

A skill that never loads is worth nothing, so the description was measured too:
twenty realistic queries, ten that should load the skill and ten near-misses
that should not, each run three times, majority decides. The near-misses share
vocabulary with the skill on purpose: a dark-mode toggle for a personal blog, a
shadcn bug in an unrelated Next.js app, a chart of entity counts, a pre-commit
hook for the em-dash rule, and four pieces of piighost work that are not
interface work.

| Description | Recall | Precision | Accuracy |
|---|---|---|---|
| First draft | 50% | 100% | 75% |
| Naming the symptoms as well as the repositories | 60% | 100% | 80% |
| Leading with when to use it, colloquial names included | 70% | 100% | 85% |

Precision never moved: not one near-miss ever loaded the skill, at any version.
All the headroom was in recall, and it came from two changes. Saying what the
symptom looks like rather than only what the skill contains, so "the dropdown
backgrounds disappear in production but work locally" reaches a charter about
CSP. And accepting the names people actually use, "the hub", "the studio", "our
front-end conventions", rather than requiring a repository name.

Three queries still do not load it, two of them asking to add something to a
page "in the hub" without naming the project. Left there: pushing further would
mean tuning against twenty queries, and the next gain would be fitted to them
rather than to the work.

### How it was measured

`skill-creator`'s own optimisation loop reported a flat zero here, identically
on the queries that should trigger and the ones that should not, which is a
broken measurement rather than a bad description: it stands a slash command in
for a skill and watches for a tool call that never comes. Measuring it properly
took `trigger_test.py` in the workspace, and two false starts worth recording,
since both produced a confident number that was wrong:

- counting a run as untriggered when it timed out. The skill triggers and the
  model then does the whole task, which takes minutes, so every success read as
  a failure. The decision is visible on the first tool call; take it there and
  stop;
- matching the skill's name anywhere in the stream. The session's init event
  enumerates every available skill, so every query scored a trigger before the
  model had decided anything. Only a `Skill` tool call naming this skill counts.
