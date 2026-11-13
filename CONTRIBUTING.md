# Contributing to Agent Odyssey

## Run it
`pixi install`, then `pixi run preview` (live) or `pixi run render`. `pixi run e2e` drives the built site with real key
presses (needs `quarto install chrome-headless-shell` once). `pixi run shots` writes screenshots for review.

## Add a quest
1. `pixi run new-quest <zone> <slug> "Title"` creates `zones/<zone>/<slug>.qmd` and `.yml`.
2. Add it to `zones.yml` under its gate, with id `<zone>-<slug>`, `page`, `story` and `done` text.
3. Write the test bank (see rules below), then `pixi run render && pixi run e2e`.

## Rules for content
- **Facts:** check tool facts against official docs. Say "Verified: ran ..." only if you ran it; otherwise
  "Last verified (docs, not run): <tool> <version> on <date>" or "General practice". Record sources in `research/`.
- **No real company or product used as a villain.** The enemy is the Blight: unchecked plausible-but-false output.
- **Sceptic-friendly:** never imply LLM use is mandatory. Mitigations over cheerleading.
- **Exercises** run on a laptop with tiny mock data. No real or sensitive data, ever.
- **Tests:** discriminating, one defensible right answer, every wrong answer carries a `misconception`, every question has
  `explain`. Do not make the correct option the longest or the only hedged one. Types: choice, order, sort, faulty-line, match.
- **Honour items** (`data-ao-honour`) give bonus XP only and never gate progress.
- **Accessibility:** all text is real HTML; colour is never the only signal; everything works with the keyboard.

## Review before merging
Run `pixi run shots` right before review, then check `REVIEW.md` for the checklist.

## Licences
Content: CC BY 4.0 (`LICENSE-CONTENT`). Code: MIT (`LICENSE`).
