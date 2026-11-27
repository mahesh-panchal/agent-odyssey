# AGENTS.md

Instructions for any coding agent writing or reviewing content in this repository. Human contributors read [CONTRIBUTING.md](CONTRIBUTING.md) and [REVIEW.md](REVIEW.md). This file holds the writing standards so an agent does not need re-briefing each session.

## About this repository

Agent Odyssey is a static Quarto role-playing course that teaches bioinformaticians to use coding agents with care. Many readers are new to LLMs and some are sceptical. Each page is a quest: a short story, then plain technical teaching, hands-on steps and a test.

## Two layers on every page

1. **Story** (`::: {.ao-story}`, 3 to 5 sentences, first on the page; cast, creature kinds and vocabulary are in [research/story-bible.md](research/story-bible.md)). Odyssey imagery lives here: the pact, Astrals, Familiars and Automata, the Collegium, Gaia's Rest, the Blight. It ends with one sentence that leads into the lesson and may foreshadow what comes next.
2. **Lesson.** Plain technical words only. No pact, creature, Astral, ward or Blight imagery in text, tables or diagrams. `pixi run learner --warn` flags it.

## Standing rules

1. **Terse prose.** Short declarative sentences, active voice, no hedges or meta-commentary ("note that", "worth noting"). Follow the Google developer documentation style guide.
2. **State the point directly.** No contrast framing: "X, not Y", "not just X but Y", "it is X, not Y", "does not X; it Y", "rather than". Say what is true. Name the alternative only when the reader is likely to pick it. `pixi run learner --warn` flags the common shapes; read for the rest.
3. **British English** in prose. Never alter code identifiers, flags, package names or established terms.
4. **The lesson body never points at a later quest.** The story may foreshadow it. Cross-links live in Related lessons.
5. **Build up.** A page never opens with its full diagram. Introduce one concept per figure, with its explanation next to it, and let each later figure repeat the earlier parts and add one. Words that appear in a figure are listed apart from words that do not.
6. **Scope to the page.** A quest is about 15 to 30 minutes. It is a tutorial with explanation, not a reference manual. A paragraph that reads "the complete set of X" becomes one example and a link.
7. **Define at first use.** Every term, command and acronym a beginner could trip over is defined in a short parenthetical on first use on that page, or is already defined on a page the header list names under Before you start. Give each metaphor a literal meaning before using it (a "dial" is a question, "never" means not using an LLM at all).
8. **Say why now.** The opening of each lesson says what the reader will be able to do and why they need it at this point in the course.

## Review checklist

Run structural checks before line edits.

1. **Mode.** Tutorial plus explanation. Rewrite reference-style enumerations as one example plus a link.
2. **Task.** Does each paragraph support something the reader does or understands now? A true fact that supports no immediate step is cut.
3. **Narrative arc.** Does the page read as concept then consequence, and does it lead into what follows?
4. **Artifact versus narration.** Write the canonical command or config out in full. Cut narration of alternate paths and edge cases.
5. **Coherence.** If deleting a sentence does not weaken the point, delete it.
6. **Justification clauses.** Cut "X, because Y" where Y is not needed beside X.
7. **Signaling.** A list that mixes universal concepts and product-specific names says which is which.
8. **Split attention.** A code block or figure is explained next to it, never "as above".
9. **Redundancy.** Do not re-explain on-screen output field by field.
10. **Curse of knowledge.** Get an independent no-context beginner read. A reviewer who has seen the draft does not count.
11. **Expertise reversal.** Keep beginner aids skippable in a second: a parenthetical, not a paragraph.
12. **Density after an accuracy fix.** Re-check the paragraph against 1, 4 and 5.
13. **Retrieval framing.** Phrase key takeaways so they can be posed as a question. The Battle does this.
14. **Accuracy.** Check commands, config and names against current official docs. Record sources in `research/`.
15. **Style.** No contrast framing ("X, not Y"), terse prose and British spelling, last.

## Process for a non-trivial page

- A beginner-lens pass (checks 1, 3, 7, 10, 11) and an expert-lens pass (check 14), by separate readers.
- Then a scope pass for checks 1, 4, 5 and 12.
- Run `pixi run learner --warn`, `pixi run banks`, `pixi run lore --require`, and `pixi run e2e` before committing.
