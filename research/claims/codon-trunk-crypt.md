# Claims ledger: codon-mill trunk and memory quests, crypt quests

Removed from lesson text in the learner-facing cleanup (2026-11-23). Sources stay in `research/*.md`.

## Common to the seven codon-mill quests
- Removed: "Topics in this zone were inspired by Matt Pocock's course LLM Fundamentals ... The explanations here are our own." | label: this course's own | action: credit kept as one line ("Inspired by ..."); "explanations are our own" dropped.
- Removed: every `ao-badge` "Last verified (docs, not run) ... on 2026-11-16" line | label: Last verified | action: facts stated plainly; dates and source lists dropped (they remain in research/fundamentals.md, failure-modes.md, session-management.md).
- Removed: "Not checked: <OpenCode ...>" in each OpenCode + Ollama tab | label: Not checked | action: turned into "check OpenCode's documentation for ..."; no OpenCode claim kept beyond the commands the research confirms.

## Tokens, Not Letters
- Removed: "Anthropic's glossary describes tokens as ..." | label: attribution | action: stated plainly.
- Removed: "the docs say newer tokenizers ... about 30 percent more" | label: attribution, Last verified | action: stated plainly.
- Removed: "the docs frame cost in tokens too" | label: attribution | action: stated plainly.
- Removed: "As general practice (we found no official page that says this about DNA), expect these problems" including "A DNA string is not read one base per token... chunks follow no biological rule" | label: General practice / inference | action: dropped as a claim; replaced by "the exercise shows how a tokenizer cuts a DNA line".
- Removed: "Copying exactly ... can drop or swap a character without any sign" | label: general practice | action: dropped; kept as "needs a check against the source".
- Removed: "Small local models tend to be less reliable at exact tasks (general practice)" | label: General practice | action: dropped; turned into "run the exercise with your own model".
- Removed: "The DNA examples are general practice and were not measured here" | label: General practice | action: dropped.

## Where Machines Fail
- Removed: "Verified: ran `echo banana | grep -o n | wc -l` ... printed 2" | label: Verified: ran | action: stated plainly (prints 2, macOS pads with spaces).
- Removed: "Verified: ran `grep -c '>'` on a three-record mock file, printed 3" | label: Verified: ran | action: command kept in table, note dropped.
- Removed: "Models are generally useful where the result is checkable (our inference from the research notes)" | label: inference | action: turned into advice ("use a model where you can check the result").
- Removed: Maynez et al. ACL 2020 finding on unfaithful summaries; "no published faithfulness rate for current Claude"; "the Anthropic docs recommend quote-first extraction" | label: attribution / not found | action: summary spot-check kept as advice; Maynez stays in Lore; faithfulness-rate remark dropped.
- Removed: attributions to arXiv 2505.14172, 2410.19730, 2508.02591 and "state of the science is mixed" | label: attribution | action: condensed to "researchers disagree on why"; papers stay in Lore.
- Removed: "One preprint (arXiv 2410.14166, Xu and Ma; full text) reports that coding models writing Python do these tasks perfectly" | label: unreviewed preprint | action: softened to "does better than answering directly".
- Removed: "General practice: so for exact counts, have the model write the script" | label: General practice | action: stated as advice.
- Removed: "Not checked: how reliable small local models are ... General practice: assume they count about as poorly" | label: Not checked | action: dropped; "try the banana example with your own model".
- Removed: Sharma et al. arXiv 2310.13548 citation (sycophancy); "per Anthropic's docs" and arXiv 2307.03172 (context rot, lost in the middle) | label: attribution | action: facts stated, citations dropped (Lost in the Middle stays in Lore).
- Removed: Non-determinism row "Not checked in the official docs. General practice: run twice and compare" | label: Not checked / General practice | action: turned into learner action (run twice and compare; record command, model, version); the claim that answers can differ stays as "may give different answers".
- Removed: "Items marked general practice or Not checked are not from a source" | label: caveat | action: dropped.
- Removed: "Quest" column of the failure table (Spot the Mirage, The Context Window, Same Every Time, Plug In a Server, "none yet") | label: mid-text quest reference | action: moved to Related lessons; table converted to a list.
- Removed: "Current Claude models list a June 2026 cutoff" was kept as "list a June 2026 training cutoff"; source not re-checked in this pass.

## The Context Window
- Removed: "Anthropic's docs compare it to working memory, and say it is separate from training" | label: attribution | action: stated plainly.
- Removed: "the docs list: your instructions, files, responses, hidden content" | label: attribution | action: stated plainly.
- Removed: "see Know Your Gear" (CLAUDE.md) | label: mid-text quest reference | action: CLAUDE.md, harness, MCP tools and skill descriptions defined inline.
- Removed: "Anthropic's docs put it directly ... The docs give no number at which it starts, so treat any quoted figure without a source as unverified" | label: attribution / caveat | action: stated plainly; turned into "check the source of any figure you see".
- Removed: "The docs say the summary keeps your requests and key code snippets ..." | label: attribution | action: stated plainly.
- Removed: "Compaction details are Claude Code specific" | label: caveat | action: dropped (tab is labelled Claude Code).
- Removed: "Not checked: OpenCode's compaction behaviour ... General practice: expect any tool to drop or summarise something ... a local model often runs with a smaller window" | label: Not checked / General practice | action: turned into learner action; "often runs with a smaller window" softened to "may".
- Removed: "(general practice)" after habits 1 and 2 | label: General practice | action: stated as advice.
- Removed: "Anthropic's docs target under 200 lines and say longer files use more context and reduce adherence" | label: attribution | action: stated plainly.

## Memory, Sessions and Usage
- Removed: "The docs say each session begins with a fresh context window" | label: attribution | action: stated plainly.
- Removed: "whether allowance already spent on a plan comes back is not documented (our inference: it does not)" and the same in the table | label: inference | action: dropped; turned into "check your plan's documentation".
- Removed: "see your plan docs, as the docs we read confirm the exact windows only for Teams and Enterprise per-seat" | label: caveat | action: replaced by "your plan's documentation gives the exact windows".
- Removed: "The docs do not state allowance sizes for individual plans" | label: Not confirmed | action: replaced by "check the vendor's pricing page".
- Removed: context poisoning provenance: post "How Long Contexts Fail" (2025-06-22), credited to Drew Breunig ("the byline comes from a reprint listing; the page text did not name him"), "no use of this term in Anthropic's docs" | label: attribution / unconfirmed byline | action: dropped; kept "community vocabulary" and the game-agent example. The byline was unconfirmed.
- Removed: "The docs give these reasons" (why usage climbs), "Remedies from the docs" | label: attribution | action: stated plainly.
- Removed: "When to Start Fresh has a section on the cache and the coffee break, with a community measurement (small sample)" | label: mid-text quest reference | action: cache-lifetime fact kept; pointer moved to Related; community measurement dropped.
- Removed: "Anthropic's best-practices guidance is plain: ..." | label: attribution | action: stated plainly.
- Removed: "General practice (our inference, from no official instruction): do not let a claim into CLAUDE.md or auto memory until checked" | label: General practice | action: stated as a firm habit.
- Removed: "Commands the docs confirm" | label: attribution | action: plain command list; commands unchanged.
- Removed: "Not checked: OpenCode's memory files, session commands and usage reporting; whether anything is billed per token" | label: Not checked | action: turned into learner actions.
- Removed: "Claude Code specific unless stated" | label: caveat | action: replaced by "Commands here are Claude Code commands".

## Who Said What
- Removed: "In Claude Code, the docs describe the system prompt as ..." and "The docs say CLAUDE.md is loaded ... as a user message" | label: attribution | action: stated plainly.
- Removed: "We do not know from the docs how the model weighs system prompt against user message, so which one wins is left open" | label: unconfirmed | action: dropped.
- Removed: "the docs point to a PreToolUse hook" | label: attribution | action: stated plainly; hook and deny rule defined inline.
- Removed: "from v2.1.277 per the docs" | label: attribution | action: version kept, source phrase dropped.
- Removed: "Not checked: OpenCode's instruction-file loading rules" | label: Not checked | action: turned into "check OpenCode's documentation".
- Removed: "Other tools arrange this differently; the ideas carry over" | label: caveat | action: dropped.

## Handoff Notes
- Removed: "Claude Code's docs say each session begins with a fresh context window. Anthropic's article on long-running agents says the same" | label: attribution | action: stated plainly.
- Removed: "(general practice)" on git history durability | label: General practice | action: stated plainly (ordinary git behaviour).
- Removed: "This is general practice. We found no official Claude Code page that prescribes a handoff file or its location, so the structure below is ours." | label: General practice / our own | action: dropped (research/session-management.md confirms no official template).
- Removed: "Anthropic's engineering article 'Effective harnesses for long-running agents' describes ... (our paraphrase)" | label: attribution | action: the three habits kept as advice without the attribution. The article is not among the Lore items.
- Removed: "General practice; there is no official format" before the note contents | label: General practice | action: dropped.
- Removed: "`CLAUDE.local.md` is the only guidance we found on keeping personal per-project notes out of git, and it is meant for preferences" and "Not checked: whether CLAUDE.local.md suits short-lived task notes better" | label: Not checked | action: kept the confirmed facts (loads after CLAUDE.md, add to .gitignore, exists only in the worktree where created); dropped the suitability question.
- Removed: "(general practice)" on writing the note before `/clear` and on the comprehension check | label: General practice | action: stated as advice.
- Removed: "Checking claims against the source is the idea behind Ground Truth (later in the Maze)" | label: forward reference | action: moved to Related.
- Removed: "(see The Stream of Ideas)" and links to Memory, Sessions and Usage in the body | label: mid-text quest reference | action: terms defined inline (context poisoning, parked ideas); links moved to Related.
- Removed: "There is no documented /handoff or /save command. Not checked: whether /export output makes a good handoff; transcripts are long, so a short curated note is probably better (our inference)" | label: Not checked / inference | action: `/export` described as plain text for a person to read; advice to write a short note kept without the claim.
- Removed: "Not checked: OpenCode's memory files ... how a local model with a small window copes" | label: Not checked | action: turned into "check OpenCode's documentation; keep the note short".
- Removed: "Claude Code specific unless stated" | label: caveat | action: replaced by "Commands here are Claude Code commands".

## The Stream of Ideas
- Removed: "Anthropic's writing on context says accuracy and recall degrade ... the docs say the whole conversation is re-sent ... (not checked: how much usage each route below saves ...)" | label: attribution / Not checked | action: facts stated plainly; savings caveat dropped.
- Removed: "in the docs' words" quote ("re-reads on every turn of the fourth") | label: attribution | action: kept as plain sentence.
- Removed: "(general practice, see below)" in triage step 2 | label: General practice | action: dropped.
- Removed: "Per the docs, claude --worktree creates ..." | label: attribution | action: stated plainly.
- Removed: "The docs say checkpoints are 'not a replacement for version control'" and "(our inference from the limits)" for `sed -i` | label: attribution / inference | action: stated plainly; the Bash-change point follows from the confirmed limit that Bash-only changes are not tracked.
- Removed: "General practice (our inference, not a documented feature): no official page describes a parking-lot file" | label: General practice | action: dropped; file advice kept.
- Removed: "the research cautions that a file imported into your instructions costs context each time" | label: attribution | action: stated plainly.
- Removed: "General practice (our inference): plan mode suits a side idea" | label: inference | action: turned into "try it for a side idea".
- Removed: "Not checked: OpenCode's side-question, branch and worktree features; the research could not find its share and fork pages" | label: Not checked | action: turned into "check OpenCode's documentation"; confirmed commands kept.
- Removed: the "Worked example" section | label: duplication | action: the table above it carries the same six cases; three cases kept as a short worked example. Nothing taught was lost.
- Removed: "Claude Code specific unless stated. Parking-lot files are general practice." | label: caveat | action: dropped.

## Save Point
- Removed: "Verified: ran these commands with git 2.54.0 on 2026-11-13" | label: Verified: ran | action: commands stated plainly.
- Removed: `callout-warning` ("Two things git restore does not do for you") | label: caveat callout | action: kept as a plain two-item list of limits (firm, actionable).
- Removed: "The Context Window is advised" from Prerequisites | label: suggested prerequisite | action: moved to Related lessons (not needed by the body).

## Grow the Carapace
- Removed: "Last verified (docs, not run): Claude Code v2.1.323 and OpenCode v2.3.0 on 2026-11-13" | label: Last verified | action: rules stated plainly; versions dropped (kept in research/kennel-and-crypt.md).
- Removed: "A line in your instructions file ... is guidance, and it does not change what is allowed" contrast | label: contrast | action: reworded to a positive statement.
- Removed: "There is no .claudeignore that restricts access" | label: negation | action: kept as a plain actionable fact.

## The Locked Cabinet
- Removed: badge: "General practice (the habits). Mistral facts: Last verified (docs, not run), read 2026-11-20 through a summarising tool. Transcript facts: Last verified, read 2026-11-23. Your own data agreement and cluster policy override anything here." | label: General practice / Last verified | action: dropped; the data-agreement sentence kept as a firm statement in the intro.
- Removed: callout-note "Not confirmed here: exactly how each tool treats shell reads of denied files" | label: Not confirmed | action: kept the tip; confirmed fact added (deny rules do not apply to a Python or Node script that opens the file itself, from research/transcripts-and-secrets.md); the unknown became "for another tool, check its documentation".
- Removed: section "What the European draft best practices add" with "a draft with no endorsements yet", "Not checked first-hand: read 2026-11-20 through a fetch summary", and the specific claim that keys "sit in the provider's logs under your account's retention terms" | label: Not checked first-hand | action: kept as three habits (reading discloses; rotate keys after the agent opens `.env`; ask data steward about lawful basis, processor contract, transfer basis; sandbox or network limit). The provider-logs claim and the AI for Science attribution were dropped; the practice 11 link stays in Lore.
- Removed: "Read 2026-11-23 on the docs pages listed in research/...; no command was run" | label: Verified/Last verified | action: dropped; facts stated plainly.
- Removed: incident wording "a bucket of agent traces, shared with a vendor for training, was copied" and "We read the vendor's own post; the numbers are theirs" | label: overstated / attribution | action: rewritten to what research/transcripts-and-secrets.md confirms (an access key issued to a vendor was exposed; a bucket held limited coding agent traces; a small number held credentials not redacted). "Shared for training" and "copied" are not in the notes and were dropped. The vendor name was never in the lesson.
- Removed: "Reported by users, not confirmed in the docs: a password typed into an approved command can end up in that file" | label: NOT CONFIRMED (research/transcripts-and-secrets.md) | action: dropped as a claim; turned into the action "open the file now and then and delete any saved rule that contains a secret".
- Removed: "(General practice)" on the make-a-leak-worth-little habit and on "Ask your data steward" | label: General practice | action: stated as advice. The GitHub one-hour token fact is confirmed and stays.
- Removed: "The docs also say deny rules on files do not stop a script the agent runs from reading them" | label: attribution | action: merged into the callout, stated plainly.
- Removed: "This page does not claim either has happened" (unpublished-ideas worry) and "Another version is a company showing a proof of something you spent years on" | label: caveat | action: dropped.
- Removed: "What the docs say (Claude Code data usage page, read 2026-11-17)" | label: attribution / read on date | action: facts stated plainly.
- Removed: "Anthropic says it does not train on code or prompts ... under commercial terms" | label: attribution | action: stated plainly.
- Removed: "Not checked: the claude.ai chat privacy pages and the full terms" | label: Not checked | action: turned into "read the terms of the exact tool and plan you use, including the privacy page of any chat app".
- Removed: Mistral "read 2026-11-20 through a summarising tool, so re-check the wording" | label: read on date / summarising tool | action: kept only the points marked CONFIRMED in research/mistral.md.
- Removed: "we did not find a default retention period on Mistral's own pages" | label: NOT CONFIRMED | action: replaced by "for retention periods, check Mistral's current terms".
- Removed: "we could not tell whether 'Chat' means Le Chat or chat requests" | label: unconfirmed | action: list kept verbatim ("Agents, Conversations, Files, Chat and Vibe are excluded"), the doubt dropped.
- Removed: "We did not confirm where Le Chat or Vibe run" | label: NOT CONFIRMED | action: replaced by "ask the vendor if location matters".
- Removed: "Not checked: Le Chat's own privacy page (only a search summary was seen), Mistral's privacy policy, and any other vendor's tools" | label: Not checked | action: dropped (the habit "read each vendor's terms" covers it).
- Removed: "Ollama's page" attribution for Apache 2.0 and "Ollama says it does not see your prompts" | label: attribution | action: stated plainly.
- Removed: links in body to Adopt the Pet and Free Is Not Free, and the mention of the Carapace quest in the callout | label: mid-text quest reference | action: moved to Related; "deny rule" and "local model" defined inline.
- Removed: "Nobody checks this and nothing depends on it. It is here because the real rules are in a document your group holds, and this site cannot see it." | label: caveat | action: shortened to two plain sentences.
