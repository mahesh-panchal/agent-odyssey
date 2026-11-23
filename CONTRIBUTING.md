# Contributing to Agent Odyssey

## Run it
`pixi install`, then `pixi run preview` (live) or `pixi run render`. `pixi run e2e` drives the built site with real key
presses (needs `quarto install chrome-headless-shell` once). `pixi run shots` writes screenshots for review.

## Add a quest
1. `pixi run new-quest <zone> <slug> "Title"` creates `zones/<zone>/<slug>.qmd` and `.yml`.
2. Add it to `zones.yml` under its gate, with id `<zone>-<slug>`, `page`, `story` and `done` text.
3. Write the test bank (see rules below), then `pixi run render && pixi run e2e`.

## Rules for content
- **Facts:** check tool facts against official docs and record sources in `research/` (the Lore lint needs every link there).
  Lesson text states confirmed facts plainly. It carries no provenance: no 'Verified', 'Last verified', 'General practice', 'Not checked',
  'supported by' or caveat badges. Unconfirmed claims are dropped or turned into an action for the learner ('check your plan's limits').
  What was verified, run or left unconfirmed goes in `research/claims/<group>.md` (per quest) and the topic notes in `research/`.
- **Lesson shape:** a header list (Goal, Before you start, Time), the teaching and hands-on in learning order, `## Battle`,
  bonus items, a `.ao-related` block ('Related lessons': 2-6 links with a line each), then Lore. The body never points at another quest
  ('see X') and never mentions a later quest. Cross-links live in Related lessons. Use lists, not run-in bold paragraphs; keep table cells short.
  `pixi run learner` lints this (`--warn` adds attribution, contrast and run-in checks).
- **Voice:** soft, plain, present tense; say what a thing is rather than what it is not. Keep a negation only when it is a fact to act on, or in a test's `misconception`.
- **No real company or product used as a villain.** The enemy is the Blight: unchecked plausible-but-false output.
- **Sceptic-friendly:** never imply LLM use is mandatory. Mitigations over cheerleading.
- **Exercises** run on a laptop with tiny mock data. No real or sensitive data, ever.
- **Tests:** discriminating, one defensible right answer, every wrong answer carries a `misconception`, every question has
  `explain`. Do not make the correct option the longest or the only hedged one. Types: choice, order, sort, faulty-line, match.
- **Bonus items** (`data-ao-honour`, shown to the learner as "Bonus question" with its XP) give bonus XP only and never gate progress. A test pays XP per question answered right first time and the rest when the quest is cleared, once.
- **Accessibility:** all text is real HTML; colour is never the only signal; everything works with the keyboard.

### Lore
Each quest ends with a `Lore` block after the Battle div (`pixi run new-quest` scaffolds it): optional further reading, a plain always-visible section (not collapsible: Quarto's collapse callout is not keyboard-focusable without custom JS).
- **What belongs:** docs, articles, papers or repos a player can open to read more about this quest's ideas.
- **Only sourced URLs.** Every link must appear in a `research/*.md` file (read by the team) or in `research/lore-extra.md` (supplied by the maintainer). Never invent or guess a URL; the lint checks this.
- **One-line why:** each item is `- [Title](https://url): Publisher, kind. Why read: one line.` with kind one of docs, article, paper, repo. Use https only, no duplicate URL in a quest.
- **2-8 items** per quest. Keep to the best few.
- **Third-party text is not copied.** Link and say in your own words why it is worth reading.
- `pixi run lore` lints the blocks; the Lore library page (`lore.qmd`, generated, gitignored) is built from them on render. It runs with `--require`, so a quest without Lore fails the lint (it runs before `e2e`).

## Review before merging
Run `pixi run shots` right before review, then check `REVIEW.md` for the checklist.

## Licences
Content: CC BY 4.0 (`LICENSE-CONTENT`). Code: MIT (`LICENSE`).
