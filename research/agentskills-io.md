# agentskills.io (forge-a-skill)

Added 2026-11-26 from a follow-up the user queued on 2026-11-23.

## Sources

Read by a fetch subagent, returned as markdown (not as summaries), no truncation notice on any page except the client showcase.

- https://agentskills.io/home : overview. Open format, "originally developed by Anthropic, released as an open standard".
- https://agentskills.io/specification : SKILL.md layout, frontmatter fields and limits, progressive disclosure.
- https://agentskills.io/skill-creation/best-practices : what to put in a skill.
- https://agentskills.io/skill-creation/evaluating-skills : with/without evals in `evals/evals.json`.
- https://agentskills.io/skill-creation/using-scripts : scripts in skills.
- https://agentskills.io/client-implementation/adding-skills-support : how a client discovers and loads skills.
- https://agentskills.io/llms.txt : page index.
- https://agentskills.io/clients.md : adopter list. The list is rendered by script and did NOT come through, so no adopter is named in the lesson.
- Not read: the quickstart and "optimizing skill descriptions" pages.

## What the lesson takes from it

- Three-step loading: name and description at start (about 100 tokens per skill), body on activation (specification recommends under 5,000 tokens), bundled files on demand. The client guide gives the catalogue cost as "about 50 to 100 tokens per skill", so the lesson says "about 100" as the specification does.
- Required fields in the open format: `name` (1 to 64 characters, lowercase letters, digits and hyphens, matches the folder name) and `description` (1 to 1,024 characters). Claude Code treats both as optional (see `research/forest-and-reef.md`). The lesson tells the learner to write both and meet the stricter limits.
- Writing test: "Would the agent get this wrong without this instruction?" (best practices). The "gotchas" example in the lesson (FASTA header with spaces) is our own.

## Not used (and why)

- `evals/evals.json` layout: it differs from Claude Code's `claude plugin eval` layout that the Test the Skill quest teaches. Mixing them would confuse.
- Script guidance (non-interactive, `--help`, dry-run, exit codes): sound, but outside this quest's scope. Candidate for a later note.
- Discovery paths (`.agents/skills/` as a cross-client convention): the pages say some clients scan `.claude/skills/`; whether Claude Code reads `.agents/skills/` was not checked, so the lesson makes no claim.
- `allowed-tools`: marked "Experimental" in the specification.

## Differences found against earlier course material

- `exercises/forge/fasta-tools/skills/check-fasta/SKILL.md` had no `name`. Added `name: check-fasta` (commit d455f66) so the file is valid in the open format.
