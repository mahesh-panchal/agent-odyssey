# Claims removed from lesson text: Forest and Gatehouse

Quests: write-the-brief, plan-before-you-edit, the-project-charter, forge-a-skill, close-the-loop, test-the-skill, bundle-a-plugin (forest); plug-in-a-server, guard-the-door, advice-or-enforcement (gatehouse). Shared note: every `ao-badge` line was removed, and the AI for Science notes (research/aiforscience.md, drafts) now appear in the lesson as plain advice; the pointer stays in Lore.

## Write the Brief
- Removed: "Last verified (docs, not run): Claude Code v2.1.323 and OpenCode docs (V2; installed version not checked) on 2026-11-13" | label: Last verified | action: dropped (sources stay in research/forest-and-reef.md)
- Removed: "The one study we read on this found ... (Hu, Rostami and Thomason, 2026 preprint)" | label: attribution | action: stated plainly (persona helps tone/format, can hurt knowledge tasks; 71.6% to 68.0% kept, confirmed in research/lore-extra.md); source stays in Lore
- Removed: "Limits: small open models (7-8B), preprint; flattery not tested" | label: not supported / caveat | action: dropped from body (still in research/lore-extra.md; Lore item says preprint)
- Removed: "(our reading, general practice)" | label: General practice | action: stated plainly as habits
- Removed: "The Claude Code docs note that old conversation can crowd out the files" | label: attribution | action: stated plainly
- Removed: "The docs show no /context equivalent in the TUI" | label: not confirmed | action: turned into learner action (run /help)
- Removed: "see the next quest, Plan Before You Edit" and "See Close the Loop" | label: cross-quest pointer | action: moved to Related

## Plan Before You Edit
- Removed: "Last verified (docs, not run): research/plan-mode.md sources on 2026-11-16 ... last part of permission-modes page not read" | label: Last verified / Not checked | action: dropped
- Removed: "General practice" tags on longer diffs, review checklist, plan-is-advice, agent-can-deviate, when-to-plan bullets, keep PLAN.md | label: General practice | action: stated plainly as habits
- Removed: "the only official when-to-plan line we found; the rest says which parts are docs and which are habits" | label: provenance | action: dropped; line kept as plain advice
- Removed: "Later in the Maze, the Wall of Output makes the same point" and "Ground Truth quest later in the Maze" | label: forward reference | action: moved to Related (Wall of Output, Ground Truth)
- Removed: "The Kennel quest Recruit the Beast introduced the modes" | label: cross-quest pointer | action: dropped (modes defined inline; Related links Grow the Carapace)
- Removed: "The Codon Mill quest Handoff Notes covers what such a file should hold" | label: cross-quest pointer | action: moved to Related
- Removed: "(tell it to go ahead; not always enforced, see the limits below)" | label: caveat | action: dropped; the limits section states it
- Removed: "The docs page does not give its label, and we did not confirm on/off by default" (showClearContextOnPlanAccept) | label: Not checked | action: turned into learner action (look at your approval prompt)
- Removed: OpenCode "shell commands are likely to run without a prompt: confirm in your version" | label: inference | action: turned into learner action (check permission rules)
- Removed: "Not checked: how to switch to the plan agent, whether there is an approval step, rest of default rules" | label: Not checked | action: turned into learner action (read the agents page)
- Removed: "Not checked: how MCP tools behave in plan mode, whether a read-only shell command can have side effects" | label: Not checked | action: turned into learner action (test before trusting)
- Removed: "Not checked: whether /rewind covers the plan file" | label: Not checked | action: dropped; "keep your project under Git" kept
- Removed: "The docs say ... Claude is only instructed to plan" / "From the docs: use plan mode ..." | label: attribution | action: stated plainly
- Removed: callout-warning "The trap" | label: caveat callout | action: kept the tip as a callout-note

## The Project Charter
- Removed: ao-badge "Last verified (docs, not run) ... research/forest-and-reef.md and research/doctor.md" | label: Last verified | action: dropped
- Removed: "Claude Code's docs describe CLAUDE.md as context, and not as enforced configuration" | label: attribution / contrast | action: stated plainly (instructions are advice, loaded as context)
- Removed: "the docs aim for under 200 lines" / "The docs warn that when instructions contradict each other" | label: attribution | action: stated plainly
- Removed: "Not checked: an OpenCode equivalent" of /doctor prompt-audit | label: Not checked | action: turned into learner action (review the file by hand)
- Removed: "the carapace you built in the Crypt" | label: cross-quest pointer | action: replaced by inline definitions of permission rules, hooks, managed settings; Related links Grow the Carapace
- Removed: AI for Science practice 5 paragraph ("European draft with no endorsements yet", "read 2026-11-20 through a fetch summary", llms.txt note) | label: Not checked first-hand / draft | action: habit stated as advice (docstrings with units, versions, assumptions; update on rename; stale docs give plausible wrong results); source stays in Lore
- Removed: "Who Said What is advised" in header | label: n/a | action: kept as link

## Forge a Skill
- Removed: ao-badge "Last verified (docs, not run) ... V2; installed version not checked" | label: Last verified | action: dropped
- Removed: "Idea from the GitHub Blog article ... our own wording; the Agent Skills standard is outside the article's scope" (three places) | label: attribution / supported-by | action: dropped; points stated as advice; article stays in Lore
- Removed: "The Claude Code and OpenCode docs listed in Lore below say both read .claude/skills" | label: attribution | action: stated plainly
- Removed: "The article's advice, which is a sensible habit, is to verify in each client" | label: attribution | action: stated plainly as a checklist
- Removed: "Next you will learn to measure that" | label: forward reference | action: dropped; Related links Close the Loop and Test the Skill
- Removed: callout-warning on allowed-tools | label: caveat callout | action: kept the content as a plain paragraph (read downloaded Skills before installing)

## Close the Loop
- Removed: ao-badge "General practice." | label: General practice | action: dropped
- Removed: AI for Science practice 8 paragraph ("draft with no endorsements yet", "read through a fetch summary", research path) | label: Not checked first-hand / draft | action: four habits and same-family-judge point stated as advice; source stays in Lore
- Removed: two callout-notes | label: callout | action: folded into prose (cases; baseline)
- Table: cells shortened to under 12 words; the example of a deterministic check moved to prose

## Test the Skill
- Removed: ao-badge "Last verified (docs, not run): Claude Code v2.1.325 plugin-evals docs ... claude plugin eval was not run for this page" | label: Last verified / not run | action: dropped
- Removed: "Last verified (docs): the pages read ... no equivalent of claude plugin eval. Treat that as unconfirmed" | label: Not confirmed | action: turned into learner action (check opencode --help and docs); manual comparison kept
- Removed: "Graders come from these six types only" | label: caveat | action: dropped
- Removed: "the next quest covers bundling in more detail" | label: forward reference | action: moved to Related (Bundle a Plugin); plugin directory defined inline
- Removed: "Idea from the GitHub Blog article ... in our own words. The grader and baseline method comes from the Claude Code docs" | label: attribution | action: dropped; three points stated as advice; article stays in Lore
- Removed: callout-warning (costs money) and callout-note (trust decision) | label: caveat callouts | action: kept both as plain paragraphs because they carry safety and cost actions
- Removed: "from the previous quest" in an honour item | label: cross-quest pointer | action: reworded to "a Skill of your own"

## Bundle a Plugin
- Removed: ao-badge "Verified: ran claude plugin validate and --strict ... (2.1.325). Other claims: last verified (docs, not run) 2026-11-13" | label: Verified: ran / Last verified | action: kept the confirmed fact plainly (validate exited 0 on the example with an icon warning); rest dropped
- Removed: "(--strict) ... exited 0" detail about --strict | label: Verified: ran | action: only the plain `validate` result stated; the --strict run is listed in the code comment
- Removed: "Last verified (docs): the config key spelling and whether OpenCode reads a Claude plugin.json are unconfirmed" | label: unconfirmed | action: turned into learner action (check OpenCode docs)
- Removed: "per the docs read" (SKILL.md under .claude/skills found by OpenCode) | label: attribution | action: stated plainly
- Removed: "Per the Claude Code docs, a plugin you install can run arbitrary code" | label: attribution | action: stated plainly; callout-warning turned into plain paragraph (safety rule kept firm)
- Removed: "Idea from the GitHub Blog article ... advice for teams and sits outside the plugin format" | label: attribution | action: dropped; points stated as advice; article stays in Lore
- Removed: "Blocking a merge depends on repository rules and required checks" header wording | label: caveat | action: reworded as "Merge blocking is a repository setting"
- Removed: "the previous quest" / "The evals in the previous quest cover behaviour" | label: cross-quest pointer | action: reworded; Related links Test the Skill

## Plug In a Server
- Removed: ao-badge "Last verified (docs, not run) ... 2026-11-16 (research/tools-and-guards.md, research/terminology.md)" | label: Last verified | action: dropped
- Removed: "MCP is, in its own words, ..." | label: attribution | action: stated plainly
- Removed: "a reasonable working assumption, offered as general practice (our wording, outside the docs)" | label: General practice / inference | action: stated as "Assume it can do whatever that command can do"
- Removed: "The docs' one security sentence is short: ..." | label: attribution | action: stated plainly
- Removed: "The --env line is an unrun sketch of the syntax" | label: not run | action: turned into learner action (run claude mcp add --help)
- Removed: "For security reasons ... the docs say project-scoped servers load without asking, and name --strict-mcp-config" | label: attribution | action: stated plainly
- Removed: OpenCode "check which version you have installed" | label: caveat | action: kept as learner action
- Removed: "The docs say that MCP tools consume model context" | label: attribution | action: stated plainly
- Removed: "Not checked: project-level approval prompts for OpenCode servers, and how a local Ollama model changes any of this" | label: Not checked | action: turned into learner action (check current docs); Ollama point dropped
- Removed: "The docs give one sentence on this, so the rest is general practice" | label: General practice | action: bullets stated plainly
- Removed: AI for Science practice 3 paragraph (draft, read 2026-11-20 via fetch summary, "asking for such a list is our own suggestion (General practice)") | label: Not checked first-hand / draft / General practice | action: habits stated as advice (registry listing is not a review; source with maintainer and review date; ask for a vetted list; hidden instructions in descriptions and skills); source stays in Lore
- Removed: callout-note on sandbox ("Claude Code's docs also say ...") | label: attribution / callout | action: stated plainly in prose
- Removed: "Grow the Carapace (permission rules). Walk the trunk first." | label: n/a | action: Before you start now links Grow the Carapace and defines permission rule and sandbox

## Guard the Door
- Removed: ao-badge "Last verified (docs, not run) ... (research/tools-and-guards.md)" | label: Last verified | action: dropped
- Removed: "That contrast is our inference from how exit code 2 works, not a phrase from the docs" | label: inference | action: dropped; sentence kept ("a command hook is ordinary code ...")
- Removed: "(short third-party text, quoted with attribution)" | label: attribution | action: now "from the Claude Code hooks guide"
- Removed: "(check the guide for the exact step; chmod +x is the usual way)" | label: not confirmed | action: now "chmod +x is the usual way"
- Removed: "(the guide names onFailure: block; check the current docs for where it goes)" | label: not confirmed | action: kept as learner action (check the hooks reference)
- Removed: "Not checked: an exit-code-2 equivalent or shell-hook configuration" (OpenCode); "whether throwing from a tool hook blocks a call"; "a trust statement for plugins ... an inference"; "how any of this behaves with a local Ollama model" | label: Not checked / inference | action: turned into learner actions (check docs, test throw, test with Ollama); plugin-trust line stated as a firm habit
- Removed: "(our inference; the docs do not discuss evasion)" on string-match evasion | label: inference | action: dropped; point kept as a logical consequence of matching text
- Removed: "Not a sandbox" heading contrast | label: contrast | action: reworded "A string match is easy to dodge"
- Removed: "The docs say command hooks ..." | label: attribution | action: kept the quoted phrase, attribution dropped
- Removed: AI for Science practice 10 paragraph (draft; "testing the checkpoint ... is our own suggestion (General practice)"; fetch-summary note) | label: draft / General practice / Not checked first-hand | action: stated as advice; source stays in Lore
- Removed: "the docs say hooks committed ... run in a folder you have never trusted; the docs name --bare and disableAllHooks" | label: attribution | action: stated plainly

## Advice or Enforcement
- Removed: ao-badge "Last verified (docs, not run) ... (research/tools-and-guards.md)" | label: Last verified | action: dropped
- Removed: table column "Edge, per the docs read or earlier quests" | label: attribution / cross-quest | action: replaced by 3-column table (Control | What it does | Where it can fail) with short cells; no quest references
- Removed: "(see the Carapace quest)" in two table cells | label: cross-quest pointer | action: dropped; Related links Grow the Carapace
- Removed: "The docs say its restrictions still apply if a prompt injection bypasses the model's decision" | label: attribution | action: stated plainly under the Claude Code table
- Removed: "Not checked for OpenCode: exit-code-2 equivalent, throwing in a tool hook, sandboxing, local Ollama effect" | label: Not checked | action: turned into learner action (check current docs)
- Removed: "Git history ... recovery only" long cell | label: n/a | action: shortened
- Removed: AI for Science practice 4 paragraph (draft; "(General practice)"; fetch-summary note; "Their example is ...") | label: draft / General practice / Not checked first-hand | action: habits stated as advice (limits in the system, owners, logs, inventory, scoped account, backup); source stays in Lore
- Removed: "The Gatehouse's rule of thumb" | label: lore-ish framing | action: "The rule of thumb"
- Bank edits (needed because the lesson no longer names the draft or earlier quests): advice-or-enforcement.yml two prompts; close-the-loop.yml, the-project-charter.yml, guard-the-door.yml one prompt each (dropped "AI for Science draft" from the question text).
