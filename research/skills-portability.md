# Skills portability and team skills: GitHub Blog article

Read 2026-11-17. Source: https://github.blog/ai-and-ml/github-copilot/build-once-run-on-any-agent-a-practical-guide-to-agent-skills/ ("Build once, run on any agent: a practical guide to agent skills", Andrea Griffiths, GitHub Blog, 2026-11-12).
Method: page fetched through a summarising fetch tool, so everything below is a paraphrase of a summary, not a quote. Re-read the article before quoting.
Reuse: footer "© 2026 GitHub, Inc."; no licence for the article text is stated; github.blog/robots.txt has no AI-crawler rules and no Content-Signal line. Copyright is therefore reserved: use the ideas in our own words with credit and a link; copy no text.
Decision fed: advice added to the Forge a Skill, Test the Skill and Bundle a Plugin quests, plus Lore links.

## Advice from the article (ideas, paraphrased)
- CONFIRMED (article): a skill is a versioned folder built around a `SKILL.md` that says when and how to do a repeatable task. Its value is that team knowledge stops living in chats or in one person's head.
- CONFIRMED: a skill describes the method; the environment that runs it still supplies the tools, credentials and permissions. A skill is not an access grant.
- CONFIRMED: skills fit bounded, repeatable work (checklists, releases, migrations, metric pipelines). Work that needs stable interfaces, shared state, audit trails, long-running control or externally enforced permissions is better built as an application.
- CONFIRMED: one skill, one clear job, with a defined input and output. Frontmatter `name` and `description` should say the task and purpose. Include a "when to use" section, what to review, and what evidence to report back.
- CONFIRMED: start with a task you find yourself explaining repeatedly; define its inputs, its boundaries and what a reviewer needs to see.
- CONFIRMED: use a separate verifier for AI-generated work. An agent judging its own output is not an independent check. (The demo's verifier returns PASS, FAIL or PARTIAL and must cite evidence from the changed files.)
- CONFIRMED: portability: write the instructions once and reuse across agent clients, but clients differ in models, tools, credentials and permissions, so verify in each client. After installing, check the client triggers the skill for the right task, loads its references, uses the tools it needs and returns the expected evidence.
- CONFIRMED: the worked example keeps `skills/*/SKILL.md` as the single source, generates client-specific packaging (it names Claude Code, Cursor and GitHub Copilot), and runs a check mode in CI to catch drift between source and generated copies.
- CONFIRMED: split a larger workflow into skills with distinct responsibilities that share project context instead of each rediscovering it; changing one step should touch one skill. Keep project names, databases and conventions in one manifest the skills read instead of hardcoding them; keep discovered details separate from team standards (a pattern found in code is not automatically a rule); have people confirm discovered details where judgment matters. Portability test: could another team reuse the skills with its own manifest without rewriting them?
- CONFIRMED: the example workflow has human checkpoints in each phase and requires approval before schema changes run. Blocking a merge depends on repository rules and required CI checks, not on the skill alone. The demo's review action reads diffs statically and was advisory.
- CONFIRMED (the article's own three-line summary, paraphrased): put business context in one manifest; use one consistent access path across related skills; use instructions to guide, and tests, CI checks and human review to verify.

## Not in the article (do not attribute to it)
- An 'open standard' discussion, a detailed testing method, a folder layout beyond `SKILL.md`, a dedicated security section. (Security appears only implicitly: permissions stay with the host.) Do not credit the article for the Agent Skills standard or for eval design; those come from the Anthropic and OpenCode docs already in research/forge.md and research/terminology.md.
- UNCONFIRMED: the demo repositories' licence.

## Links the article gives (for Lore)
- Add an agent skill to GitHub Copilot (GitHub docs): https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills (not read by us)
- Demo repository: https://github.com/githubevents/build-once-run-on-any-agent (demos: proof-agent, dataforge; not read by us)
