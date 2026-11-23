# Claims ledger: Codon Mill optional quests

Removed from lesson text in the learner-facing cleanup (2026-11-23). Sources for the kept facts are in research/session-management.md, cache-and-usage.md, fundamentals.md, rag.md, mistral.md and llm-wiki.md.

## When to Start Fresh
- Removed: ao-badge "Last verified (docs, not run): session-management.md sources 2026-11-16 ... cache numbers from a community repo, small samples, not run" | label: Last verified | action: dropped
- Removed: "Topics in this zone were inspired by Matt Pocock's course LLM Fundamentals ... explanations here are our own" | label: provenance | action: dropped from the body (credit needs a home outside the lesson, e.g. a site credits page)
- Removed: "The docs recommend /clear ... say it costs nothing"; "The docs' advice"; "Per the docs"; "docs back the mechanism: Anthropic calls ... context rot" | label: X-says-Y attributions | action: stated plainly; the term "context rot" and "they give no number" dropped
- Removed: "General practice: treat forgetting as a symptom of crowded or degraded context" | label: General practice | action: stated as a signal with the instruction-file move
- Removed: "That is the rule of thumb in this site's research (our inference from the docs)" (carry on when same task) | label: inference | action: stated as a plain signal
- Removed: "Not checked: whether /usage reports a Prompt cache line on every plan" | label: Not checked | action: turned into learner action ("run /usage and read what your plan reports")
- Removed: community multipliers (about 1.5x warm, about 9.8x expired; compact before break about 2.5x, after about as costly as carrying on) and the claude-code-usage-analysis project link/discussion | label: community, small samples (research/cache-and-usage.md findings 1 and 3, labelled small n, not confirmed) | action: dropped; practical habits kept as learner actions. Official lifetimes (about one hour subscription, five minutes API key) and idle compaction kept plainly (CONFIRMED in session-management.md)
- Removed: "one-hour cliff on subscription ... simulator, not a live run" | label: General practice / simulator | action: dropped
- Removed: turning a built-in tool off mid-task cost about 22x; CLAUDE.md edits, MCP additions, effort changes showed no jump | label: community, n=2, preliminary | action: dropped; kept "Decide your tool set at the start of a task" as an action
- Removed: long log in chat adds to later turns (+15%/+64%) | label: community, n=2 | action: dropped number; kept "trim output" as action
- Removed: "Not checked: default auto-compact threshold ... no percentage" | label: Not checked | action: dropped
- Removed: "Not checked: whether the status line can show context fullness" | label: Not checked | action: dropped
- Removed: OpenCode "Not checked: what it keeps when it compacts, /context-style display, local-window effect"; "General practice: same signals apply" | label: Not checked / General practice | action: dropped; kept the plain fact that every model has a finite window; added "run /help" action
- Removed: decision-ladder row notes "(community numbers, small samples)", "Docs: ..." | label: attribution | action: dropped
- Removed: mid-text references to The Context Window, Memory, Sessions and Usage, Handoff Notes | label: cross-references | action: moved to Related (Memory, Sessions and Usage; The Context Window; Handoff Notes; The Stream of Ideas); terms defined in "Words first"

## Too Many Tools, Too Many Agents
- Removed: ao-badge "Last verified (docs, not run) ... figures are Anthropic's own claims, not measured here" | label: Last verified | action: dropped
- Removed: Matt Pocock inspiration line | label: provenance | action: dropped (see above)
- Removed: "These are Anthropic's statements on a docs page, with no method given ... no thresholds were measured" (55k tokens example, 30 to 50 tools) | label: unsupported/unmeasured | action: figures stated plainly with "can"/"roughly"; caveat recorded here only. Note: the figures remain unmeasured by us.
- Removed: "Whether the 30 to 50 tool accuracy claim still applies behind deferral is not stated in the docs we read" | label: Not confirmed | action: dropped
- Removed: community cache test (twenty times cost when a built-in tool is turned off; n=2, preliminary) and link to When to Start Fresh | label: community, preliminary | action: dropped; "choose your tool set before you start" kept as action
- Removed: OpenCode "Not checked: whether OpenCode defers tool definitions" | label: Not checked | action: turned into learner action (check docs, run /help); the safe default (assume cost, keep set small) kept
- Removed: "(general practice, inferred from the above)" on few tools habit | label: inference | action: stated as the habit
- Removed: "Our reading of that, as general practice" on script/call/agent list | label: General practice | action: stated plainly
- Removed: preprint caveats "figures come from the authors' own tasks and models and changed between versions" | label: caveat | action: kept the three findings with figures; caveat recorded here. The figures are not re-checked against the preprint versions.
- Removed: Lore text "no independent measurement"/"figures changed between versions" left untouched (Lore block not edited)
- Removed: inline reference to When to Start Fresh | label: cross-reference | action: moved to Related

## RAG and Its Cousins
- Removed: ao-badge "Last verified (docs, not run): papers, docs and posts in Lore, read 2026-11-20 ... numbers are the authors' own" | label: Last verified | action: dropped
- Removed: "[the hands-on follow-up is Grow a Graph with Ollama]" in header and the inline "next quest does this" | label: cross-reference | action: moved to Related
- Removed: "The name comes from a 2020 paper by Lewis and colleagues" authors | label: attribution | action: kept the 2020 paper, dropped the names
- Removed: "A community notebook collection describes a results table losing its structure (we did not run it)" | label: Not checked / community | action: turned into "open a few extracted chunks and read them"; PDF table scrambling stated as "can" (README claim, unchecked)
- Removed: "General practice: the good-for column is our reading ..." | label: General practice | action: dropped
- Removed: "Anthropic reports that adding context, BM25 and a reranker cut top-20 failures from 5.7% to 1.9% on its own tests" | label: X-says-Y | action: stated as "in one reported test"
- Removed: "HyDE's own paper says ... unreal and may contain false details"; "The docs warn it can consume a lot of LLM resources"; "its README calls a 30B model a reasonable minimum" | label: attributions | action: stated plainly (README quote kept for LightRAG); 281 minutes figure from the Graph RAG paper stated plainly
- Removed: "Those results are self-reported: an LLM judge compared answers on questions another LLM generated ... authors of LightRAG note ground truth is hard to define" | label: caveat | action: reduced to "as judged by an LLM; check on your own questions" (bank q needs this); the rest dropped
- Removed: "Han and colleagues", "Xiang and colleagues" names | label: attribution | action: stated as "a 2026 comparison" and plain findings (F1 64.78 vs 63.01, 135 vs 5,560 seconds, 65% entities)
- Removed: "General practice: start with simple RAG, measure ..." | label: General practice | action: stated as advice
- Removed: "Anthropic's post says below 200,000 tokens you can include everything", "Anthropic describes Claude Code navigating just-in-time" | label: attribution | action: stated plainly
- Removed: "General practice (no source opened): a vector index cannot promise a complete filter or exact count" | label: General practice, no source | action: kept as a plain statement because it follows from how top-k retrieval works; flag for maintainer
- Removed: "Two papers found fine-tuning a poor way to add new facts. They did not test LoRA, so that is an inference." | label: inference | action: dropped; kept OpenAI-guide advice (fine-tune for behaviour, supply context for knowledge)
- Removed: "One paper found cache-augmented generation faster than RAG ... 'becomes impractical for significantly larger datasets'" attribution | label: attribution | action: stated plainly
- Removed: "A study from Google researchers ... 2024 models" | label: attribution | action: kept figures ("a long-context model beat RAG on average, same answer on over 60%, Self-Route cut cost 39 to 65%") with "2024 models"; Google named only in Lore
- Removed: "The Ragas paper defines the second one as faithfulness. Splitting the two checks is our suggestion." | label: attribution / our suggestion | action: faithfulness defined plainly; suggestion stated as advice
- Removed: "OWASP says RAG does not fully remove this risk"; links to Guard the Door and The Locked Cabinet in body; "see The Context Window and the Lost in the Middle paper" | label: attribution / cross-reference | action: stated plainly; links moved to Related
- Removed: "General practice" on stale index | label: General practice | action: stated plainly
- Removed: Claude Code tab "docs list a search tool category but do not explain why there is no index, so this page makes no claim about the reason" | label: not confirmed | action: dropped
- Removed: OpenCode "Not checked: how OpenCode itself searches a project" | label: Not checked | action: dropped
- Removed: comparison table "Why" column and cell text over 12 words | label: layout | action: table cut to two short columns; reasons moved to a list below it

## Grow a Graph with Ollama
- Removed: ao-badge "Verified: ran rag.py and graph.py on 2026-11-20 (macOS, Ollama 0.40.16) ... One run per question at temperature 0, not repeated ... Not run: LightRAG, GraphRAG, qwen3:4b" | label: Verified: ran / Not checked | action: results kept as plain statements in "What we saw" and the Mistral table (confirmed in research/rag.md section 7 and research/mistral.md "Runs on 2026-11-20"); run conditions recorded here only
- Removed: "This is one question, one model and one run. It illustrates the mechanics and proves nothing about which method is better." | label: caveat | action: replaced by "Try your own questions and compare."
- Removed: "Adopt the Pet suggested qwen3:4b, which this quest did not test" | label: Not checked | action: dropped; "if you try a model under about 7B, read the triples" kept as action
- Removed: "Adopt the Pet explains why the default context is small" | label: cross-reference | action: stated plainly that Ollama's default is small; link in Related
- Removed: "Ollama's docs suggest temperature 0" | label: attribution | action: stated plainly
- Removed: "(we saw two versions)" of answer wording | label: ran once | action: dropped, "wording differs a little" kept
- Removed: "the table in the last quest" / "four steps from the last quest" | label: cross-reference | action: terms defined in "Words first"
- Removed: Mistral section "(Last verified, docs, not run, 2026-11-20; see research/mistral.md)" for 6.0 GB, tools, Apache 2.0 | label: Last verified | action: stated plainly (CONFIRMED in mistral.md)
- Removed: "We did not compare all 80 facts with their notes" | label: Not checked | action: turned into "Read show against the notes yourself"
- Removed: "This is one question, one run and two models, so it does not rank them." and "What we take from it" | label: caveat | action: dropped; kept the plain takeaway that retrieval is one half and the reader model the other
- Removed: "Mistral also offers mistral-small ... we did not run those" | label: not run | action: kept as a plain fact (14 GB, 24B, mistral.md) with an invitation to try
- Removed: "The tools' own documentation is cautious about small models ... Neither gives a benchmark"; "Not checked: how qwen3:4b ... do on this exercise" | label: attribution / Not checked | action: quotes kept, benchmark remark dropped, action to read triples kept
- Removed: "Treat the details below as Last verified (docs, not run)"; LightRAG "release v1.5.8rc1 on 2026-11-15 when read"; GraphRAG "v3.3.0 on 2026-10-08 when read" | label: Last verified | action: replaced by "check their current docs"; versions dropped
- Removed: "Not checked: a documented Ollama setup (none was found in the docs)" | label: Not checked | action: turned into "check the current docs for an Ollama setup"
- Removed: "A closed GitHub issue reports that default embedding vector size 3072 can clash with nomic-embed-text, which is issue evidence, not official guidance" | label: issue-only evidence (rag.md) | action: turned into learner action ("check the embedding vector size matches your embedding model's")
- Removed: "General practice: start with LightRAG on a tiny folder" | label: General practice | action: stated as advice
- Removed: "The Blight likes a confident answer built on a wrong link" | label: story text in steps | action: shortened to a plain sentence
- Removed: link to The Locked Cabinet in Verify section | label: cross-reference | action: moved to Related; plain rule "keep real and controlled data out" kept
- Removed: OpenCode "Not checked: how OpenCode behaves with a model slow at extracting JSON" | label: Not checked | action: dropped
- Removed: Lore-level note about NirDiamant repo caveats | label: n/a | action: Lore not edited

## Keep a Living Wiki
- Removed: ao-badge "Last verified (docs, not run): the LLM Wiki gist ... read in full 2026-11-20. Not run: building a wiki, Obsidian, qmd. Claims about Obsidian beyond the gist are General practice" | label: Last verified / General practice | action: dropped; gist named once as the basis of the lesson
- Removed: "The gist's own words ... Its argument is ..." and many "the gist says/lists/suggests/points out" | label: X-says-Y | action: stated plainly; gist named in the intro and where the lesson quiz needs it
- Removed: "It describes a pattern, and it does not include a program or any measurements. Everything below is that pattern plus our own cautions." | label: provenance | action: reduced to "describes a pattern and includes no program"
- Removed: index at moderate scale "(about 100 sources and a few hundred pages) ... the author's experience; we did not test it"; "Scale ... Not checked by us" | label: Not checked | action: dropped the numbers; turned into action "as the wiki grows, add a search tool"
- Removed: "General practice for your own first version ... It was not run" (example schema) | label: General practice | action: presented as an example to edit
- Removed: qmd mention "Not checked: we have not read or run it" | label: Not checked | action: dropped qmd; kept "add a search tool"
- Removed: "(RAG) General practice: a wiki is a good home for stable understanding" | label: General practice | action: stated plainly
- Removed: "They are our examples, not from the gist, and none was run" (use cases) | label: our inference | action: dropped; use-case table restructured to nested lists (cells were over 12 words)
- Removed: "General practice (Obsidian's own docs were not read)" for vault is a folder of Markdown, and each Obsidian tool gloss | label: General practice | action: stated plainly (general knowledge; flagged in llm-wiki.md as not checked against Obsidian docs)
- Removed: "Habits we suggest, all General practice" | label: General practice | action: stated as habits
- Removed: "The author calls this clunky" (images) | label: attribution | action: dropped
- Removed: "OWASP's warning about retrieved text ..." | label: attribution | action: stated plainly
- Removed: "Not checked: how well small local models do this" | label: Not checked | action: kept the action "try one short, harmless source first"
- Removed: "General practice: watch your usage in the first week" | label: General practice | action: stated as advice
- Removed: "[Name the Fears] has a worry about hollow accomplishment" | label: cross-reference | action: dropped link; "You may not learn it" kept
- Removed: inline links to The Project Charter, The Shield of Undo (current title "Save Point"), Advice or Enforcement, Guard the Door, The Locked Cabinet, Plan Before You Edit, When to Start Fresh, Memory Sessions and Usage | label: cross-references | action: moved to Related (6 items); concepts defined in the body (instruction file, enforcement vs advice)
- Removed: the layers and approach tables | label: layout (cells over 12 words) | action: converted to lists
