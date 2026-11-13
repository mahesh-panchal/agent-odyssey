# Review tactics

Living document. Update the tactics and the changelog whenever the build gains something new to review.

## Tiers (run in this order; cheap first)
1. **Build + validate**: `pixi run render` (bank validation fails the build on missing misconception text, bad bins, etc.).
2. **Behaviour**: `pixi run e2e` drives the built site with real key events (map walking, gates, quest scoring, every
   question type, quest log, save/load). Add a check here whenever a feature is added or a bug is fixed.
3. **Visual review**: `pixi run shots` writes screenshots to `.shots/`. A fresh reviewer agent sees only the images and
   the checklist below (not the author's conclusions), so it is not anchored on what the author meant.
4. **Fact review** (content quests): every command/flag/config key is traced to `research/*.md` with a source URL and read
   date, or marked UNCONFIRMED. The quest's "last verified" badge must match the research file.
5. **Human review**: the team lead reads quests for tone and for what the team's own policies actually say.

## Visual checklist (for the reviewer)
- Is it obvious where to go and what to do within 5 seconds? Is the next step visible?
- Is any text clipped, overlapped by another element, or too small/low-contrast to read?
- Does the layout hold at 1400px and 600px wide? No horizontal scroll, no panel covering content.
- Do open, locked and cleared states look different without relying on colour alone?
- Does the art read as one consistent style? Anything confusing or ugly?

## Behaviour checklist (author)
- Keyboard-only path works for every interaction; arrows never fire while focus is in a widget.
- Wrong answers explain the misconception; scoring counts first-try only; retries reshuffle.
- State survives reload, export/import round-trips, and a missing/blocked localStorage does not break the page.

## Lessons that changed the tactics
- The first reviewer saw screenshots taken *before* new content landed. Always run `pixi run shots` immediately before a
  review (it re-renders first), and tell the reviewer which build it is looking at.
- A reviewer only sees states you photograph. `shots.py` now covers a fresh map, a mid-game (cleared) map, every
  question type, and narrow widths. Add a shot whenever a new visual state or question type appears.
- Reviewers judge what is visible, not behaviour. Behaviour (keys, scoring, save/load, every quest page loading) belongs in
  `pixi run e2e`. The first reviewer's most useful findings were about clarity (where do I go next?), so keep the
  "5 seconds" question in the checklist.
- Facts: where a claim can be run locally (e.g. `git restore .`), run it and say so in the badge ("Verified: ran...").
  Where it can only be read from docs, the badge says "docs, not run".

- Check that screenshots show the state their filename claims. Round 2's "wrong answer" shot clicked a random option and
  captured a correct one; the reviewer caught it. `shots.py` now clicks a known-wrong option and scrolls the quiz into view.
- Form controls need their own styling pass: unstyled `<select>`s rendered black-on-dark and were only spotted by looking
  at a screenshot of a sorting question.

- Bare fixture pages lack the site theme, so some defects (like a visible hidden button) only exist in the fixture. When a
  shot looks wrong, check it against the real page before fixing the site.
- Exercise data must be run, not assumed: the Maze's planted bug and the awk cross-check were executed and their real
  output is what the page shows.

## Changelog
- v1 (slice): tiers 1-3 added; e2e covers map, gates, quest scoring, 5 question types, quest log, save/load.
- v2: shots cover states and widths; e2e smoke-checks every quest page; Kennel and Crypt quests carry fact badges;
  cleared/open/locked map states reviewed.
- v3: second reviewer round fixed START/NEXT/CLEARED map labels, removed the key-hint toast, made the quest-log 'Now' follow
  the page, and styled feedback and form controls. Not yet done: per-answer `explain` text in the banks, a closer-to-content
  header at wide widths, shots for faulty-line and match questions.
- v4: review items closed (explain text, HUD alignment, per-type shots). Sequence Maze added with a boss; e2e checks boss HUD
  and that exercise files are published. Next review round should look at the Maze pages and the boss in shots.
- v5: Basecamp, Forest, Reef, Crypt secrets quest, honour items, character sheet. Two independent reviewers (visual from
  screenshots; content from files). Fixed: stale-looking midgame shot state, honour label, secrets-page overclaims (env vars,
  local models), Claude Code-only claims scoped, distractor strawmen reduced in several banks, SVG label legibility.
  Still open: correct options tend to be longest/hedged across older banks; OpenCode docs describe V2 and the installed version
  was not checked; HUD companion/language selectors rely on Quarto tab sync only; Pipeline Factory and MCP/hooks are v2.
