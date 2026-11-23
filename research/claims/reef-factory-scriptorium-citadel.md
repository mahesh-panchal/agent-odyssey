# Claims removed from lesson text: Reef, Factory, Scriptorium, Citadel

Format: removed claim | label | action. Written 2026-11-23.

## Send Small, Say So
- Removed: "General practice, not a vendor claim" badge | General practice | dropped (the habits are stated as advice)
- Removed: "Not checked: any venue's disclosure policy" | Not checked | turned into learner action ("Read its own page before you submit")
- Removed: "Team norms you agree locally override these defaults" | General practice | kept in body as "Follow your team's norm"
- Removed: "The Wall of Output is advised" prerequisite | n/a | moved to Related

## The Reviewer's Code
- Removed: "General practice, not a vendor claim. Team norms ... override" badge | General practice | dropped
- Removed: "the Wall of Output taught why" | cross-quest reference | moved to Related

## Teach and Share the Load
- Removed: badge "General practice, not a vendor claim" and three inline "General practice. Nothing here depends on a tool or a version." badges | General practice | dropped
- Removed: "Many people report it, and it points to something useful" | unsourced framing | trimmed to "Many people report it"; the habits are unchanged

## Dry Run First
- Removed: "Last verified (docs, not run): Snakemake and Nextflow docs on 2026-11-13 (research/factory.md)" | Last verified | dropped; Nextflow/Snakemake facts stated plainly
- Removed: "Not confirmed in the docs: exactly which wiring errors a Snakemake dry run reports, treat as typical behaviour" | Not checked | dropped (body only says a dry run shows the plan and that a passing run means a plan could be built)
- Removed: "as in the Wall of Output", "as in Ground Truth" | cross-quest reference | replaced by self-contained wording; Ground Truth moved to Related and prerequisites

## Read the Rails
- Removed: "General practice. The snippets were reasoned through, not run." | General practice | dropped
- Removed: italic "where does each input come from..." question reworded to plain sentence | style | n/a

## Same Every Time
- Removed: "General practice, not a vendor claim" badge | General practice | dropped
- Removed: "a different sense from the prompt cache used in Claude Code sessions" | cross-quest contrast | dropped
- Removed: "See The Locked Cabinet" | cross-quest reference | moved to Related
- Removed: "This is a necessary start" wording | style | kept the fact that a pinned model may still vary

## Why Notebooks Diff Badly
- Removed: "Verified: ran diff and git diff --no-index --stat on the mock notebooks on 2026-11-16 (macOS, Python 3.9.6)" | Verified: ran | stated plainly (the diff output shown is real)
- Removed: "Last verified (docs, not run): nbformat, nbstripout, jupytext, nbdime and marimo docs on 2026-11-16" | Last verified | dropped; tool facts stated plainly
- Removed: "mock files omit cell ids, so not strictly valid nbformat 4.5" | maintainer note | dropped
- Removed: "General practice, not measured here: in a real notebook an image is often tens of kilobytes" | General practice, not measured | turned into learner action (`git diff --stat` shows the size of a notebook diff); the "tens of kilobytes" figure dropped
- Removed: "that this makes diffs noisy is our reading of it" | inference | dropped (the shown diff is the evidence)
- Removed: "the costs above are our judgement, except the nbstripout clone limit, which is from its docs" | General practice | dropped; costs listed plainly; the closing "smallest change / largest change" judgement dropped (unconfirmed)
- Removed: "nbstripout's pre-commit mode modifies the working copy, per its docs" | attribution | stated plainly
- Removed: "That is general practice; check the docs for your version" | General practice | turned into "Check the docs for your version"
- Removed: "This quest has no tool-specific claims for OpenCode" | caveat | turned into "Check OpenCode's docs"
- Removed: table of four options (long cells) | structure | restructured into a list

## Run It Top to Bottom
- Removed: "Verified: ran run_cells.py on 2026-11-16 (macOS, Python 3.9.6). Output below is the real output" | Verified: ran | stated plainly (output is shown)
- Removed: "Last verified (docs, not run): marimo and Claude Code docs on 2026-11-16" | Last verified | dropped
- Removed: "py:percent-like style; headers carry our own numbers, so this is not standard py:percent" | maintainer note | dropped
- Removed: "General practice: on a cluster, run notebooks as a batch job ... Your cluster's policy decides (see the Citadel quests)" | General practice + cross-quest | stated as advice; Citadel moved to Related
- Removed: "Its docs describe a reactive model ... which the docs say eliminates hidden state" | attribution | stated plainly
- Removed: "Check the docs for how side effects behave, because this quest did not test that" | Not checked | turned into learner action
- Removed: "General practice: pin the environment ... keep an agent from running pip install" | General practice | stated as advice
- Removed: "This quest makes no claims about how OpenCode edits notebooks" | caveat | turned into "Check OpenCode's docs"
- Removed: "as in the Ground Truth quest in the Maze" | cross-quest reference | moved to Related

## Login Node Manners
- Removed: "Last verified (docs, not run): Slurm, Claude Code and OpenCode (V2) docs on 2026-11-16" | Last verified | dropped
- Removed: "Everything ... etiquette is general practice: the Slurm documentation does not define login nodes" | General practice | dropped; advice stated plainly, one firm sentence kept ("Ask your cluster staff before running an agent on the login node")
- Removed: "This page makes no claim that using an LLM agent on a cluster is allowed or expected" | caveat | dropped
- Removed: "Follow your own cluster's policy over this page" (repeated) | caveat | reduced to a short clause in the firm sentence
- Removed: "Some sites forbid agents on login nodes altogether, or allow them only inside an interactive compute allocation (where internet access may be restricted)" | General practice, unconfirmed | shortened to "Some sites allow agents only inside an interactive compute allocation" and covered by the firm staff sentence
- Removed: "its documentation does not describe them [Glob, Grep] as a control on filesystem load" | Not checked (absence) | turned into "do not limit filesystem load. Scope the search yourself" (action)
- Removed: "From the Slurm documentation:" before the command table | attribution | stated plainly
- Removed: "No job is actually submitted" quote and "same spirit as the Factory's Dry Run First" | attribution / cross-quest | stated plainly; Dry Run First moved to Related
- Removed: "Per the sbatch page, --mem-per-cpu above MaxMemPerCPU is reduced and --cpus-per-task raised" | partly confirmed | softened to "a memory request can also change the CPU count; ask your site for the limit"
- Removed: "Slurm may raise the CPU count with no error; it can also reject the job" | Not checked | dropped
- Removed: "Read the limits with scontrol show partition <name>" | Not checked (scontrol page not fetched) | turned into "Ask your site's guide or staff for that limit"
- Removed: "OUT_OF_MEMORY, often with exit code 0:125 (tools report 137)" | Not checked | dropped the exit codes; kept `OUT_OF_MEMORY` in State
- Removed: "Not checked: the 0:125 code and the --mem widening rule" | Not checked | dropped with the claims
- Removed: "you usually cannot install packages system-wide on a cluster, so a site may have to provide them. Whether it works there is site-specific" | General practice | turned into "ask staff whether they are installed"
- Removed: "(see Jobs, Not Jam)", "The Factory's Dry Run First is the same habit" | cross-quest references | moved to Related (Jobs, Not Jam and Keys on Shared Ground are later quests; they appear only in Related)
- Removed: "OpenCode ... (V2 docs; check your installed version) ... likely to run unprompted; confirm in your version" | Last verified + hedge | stated that the base policy starts with allow-all (from the V2 docs read), with a learner action to check the installed version
- Removed: "the default alone is a weak guard" | inference | dropped
- Removed: "From the Claude Code docs: foreground commands time out ..." | attribution | stated plainly

## Jobs, Not Jam
- Removed: "Last verified (docs, not run): Slurm, Claude Code and OpenCode (V2) docs on 2026-11-16" | Last verified | dropped
- Removed: "Follow your own cluster's policy and data agreement over this page. This page makes no claim that agent use is allowed or expected on any cluster" | caveat | reduced to one firm sentence ("Ask your cluster staff before letting an agent near your cluster account")
- Removed: "General practice: limit sacct with --jobs or --starttime" | General practice | stated as advice
- Removed: "Rules are enforced by the harness" | wording | "The tool enforces permission rules"
- Removed: "adapted from the permission rules in the docs" | attribution | dropped
- Removed: "The caveat: the docs say Bash rules are not a security boundary" | attribution | stated plainly (safety-relevant fact kept)
- Removed: "by the same logic a scancel rule is not watertight" | inference | kept as "can be bypassed the same way"
- Removed: "per the docs ... likely to run unprompted; confirm in your version" | hedge | see Login Node Manners
- Removed: "General practice (the site owner's own skill, research/hpc-and-notebooks.md)" | General practice | dropped label; habits stated as advice
- Removed: "From the Claude Code docs:" | attribution | stated plainly
- Removed: "The squeue and sacct pages warn against ..." | attribution | kept as "manual pages warn" (the lesson is about the scheduler's own warning); reword to a plain fact if a later pass prefers

## Keys on Shared Ground
- Removed: "Last verified (docs, not run): Slurm and Claude Code docs on 2026-11-16" | Last verified | dropped
- Removed: "A claim marked general practice is advice and is not a documented fact" | provenance explainer | dropped
- Removed: "Follow your own cluster's policy ... no claim that using an LLM agent on a cluster is allowed ... Many sites have rules, and some forbid it" | caveat | reduced to one firm sentence ("Ask your cluster staff before sending any cluster data to an external model API")
- Removed: "The docs do not say this; it is an inference" (session history on shared storage) | inference | stated as a check the learner does (`chmod 700 ~/.claude`, who can read home)
- Removed: "Settings files, from the docs" | attribution | stated plainly
- Removed: "General practice:" on key handling, controlled data and egress | General practice | stated as advice
- Removed: "Not confirmed here: how OpenCode stores keys, and what apiKeyHelper does" | Not checked | turned into learner action (look it up in your version's docs)
- Removed: "General practice, not checked in the docs, so ask your site: compute nodes restrict internet" | unconfirmed | kept as "Some sites restrict ... Ask staff what outbound access your jobs have"
- Removed: "Some sites forbid agents on login nodes and allow them only in an interactive compute allocation" (repeated from Login Node Manners) | unconfirmed | dropped here (covered in Login Node Manners and the staff question)
- Removed: "stricter than a generic skill" | maintainer note | "stricter than these notes"
- Removed: "Not checked here: whether a local model through Ollama changes what your data agreement requires" | Not checked | turned into a question for staff
- Removed: "Where OpenCode keeps its keys is not confirmed here" | Not checked | turned into learner action
