# Lore extra sources

URLs the Lore lint (`tools/lint_lore.py`) accepts in addition to those in other `research/*.md` files: supplied by the maintainer or read by the team. One URL per entry; add a note on who supplied it and what it is.

- https://github.blog/ai-and-ml/github-copilot/build-once-run-on-any-agent-a-practical-guide-to-agent-skills/ : "Build once, run on any agent: a practical guide to agent skills", Andrea Griffiths, GitHub Blog, 2026-11-12. Supplied by the maintainer; read 2026-11-17 (see `skills-portability.md`).
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills : "Add an agent skill to GitHub Copilot", GitHub docs. Linked from the article above; not read by us.
- https://github.com/githubevents/build-once-run-on-any-agent : demo repository for the article (demos: proof-agent, dataforge). Linked from the article above; not read by us.

- https://code.claude.com/docs/en/sub-agents : Sub-agents, Anthropic docs. Already cited in research/forest-and-reef.md; spot-checked 2026-11-17 for `model`, `effort`, `tools` frontmatter, model resolution order and the Explore/Plan CLAUDE.md skip (first ~100k characters of ~116k read). Used in Lore for Pick Your Companion.
- https://claude.dev/blog/which-claude-model-should-you-build-with/ : claude.dev blog article, 2026-11-09, byline as shown on the page (not verified); the source of the model-choice ideas in research/model-and-effort.md section 9. Secondary; not in Lore.
- https://www.aihero.dev/what-are-evals : "Your App Is Only As Good As Its Evals", AI Hero, last updated 2024-11-18 (author not verified). Supplied by the maintainer; read 2026-11-20 via a fetch summary, not first-hand. Source of the three grader kinds (deterministic, human, judge model), pass/fail versus score, and dataset points in the "What is an eval?" section of Close the Loop. Secondary; written for app builders.
