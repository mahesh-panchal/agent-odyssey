# Fundamentals zone: tokens, context, prompts, tools, agent vs workflow

Checked 2026-11-16. Official docs only; pages fetched via a summarising fetch tool (quotes as returned, short). Docs pages show no publish date.
Base: P = https://platform.claude.com/docs/en/ ; C = https://code.claude.com/docs/en/ ; A = https://www.anthropic.com/engineering/
Write the site's own wording. Nothing here is to be pasted.

## 1. Tokens
- CONFIRMED: tokens are "the smallest individual units of a language model" and can be words, subwords, characters or bytes. Larger tokens are used when possible (efficiency); smaller tokens let the model handle uncommon or never-seen words. P about-claude/glossary#tokens
- CONFIRMED: characters per token depends on model and language. Older models: about 3.5 English characters per token. Claude 4.7 and later (incl. Sonnet 5.5, Fable/Mythos) use a newer tokenizer giving about 30 percent more tokens for the same text. P glossary; P build-with-claude/token-counting
- CONFIRMED: use the token counting endpoint with the model you plan to use. The count is an "estimate" and may differ slightly from actual use. Counting is free (rate-limited). Do not reuse counts across model generations. P token-counting
- Consequence: token count is not word count; the same prompt costs different amounts on different models.
- UNCONFIRMED (no official page found): letter counting, exact-string copying and "how many Gs in this read" being error-prone, and DNA/protein sequences tokenising badly (arbitrary multi-letter chunks, not one token per base). Neither the glossary nor the prompting best-practices page mentions it (grep for letter/character-count/tokeniz found nothing on the latter). It is a reasonable inference from the glossary (the model sees tokens, not characters). Phrase on the site as "models read tokens, not letters, so..." and label the DNA claim as general knowledge, or show a measured demo with the count_tokens endpoint on a real FASTA line (a demo we run ourselves is a valid source).
- Practical consequence (our advice, inference): for exact counting, reverse-complement, motif position, checksums or sequence-identity tasks, have the agent run code (a script, seqkit, etc.) rather than "read" the string; verify any sequence the model retypes against the source file.

## 2. Context window
- CONFIRMED: the context window is all the text the model can reference when generating, including its own response; a "working memory", distinct from training data. P build-with-claude/context-windows
- CONFIRMED (API): everything in the request counts: system prompt, every message including tool results, images and documents, tool definitions, and the output including extended thinking. P context-windows
- CONFIRMED (Claude Code): context holds "your instructions, the files it reads, its own responses, and content that never appears in your terminal". At start, before you type: CLAUDE.md, auto memory, MCP tool names, skill descriptions (plus any output style or appended system prompt). Each file read, and tool output, then adds more. C context-window; C how-claude-code-works#the-context-window
- CONFIRMED: sizes up to 1M tokens depending on model (Sonnet 5.5, Opus 4.6+, Fable, Haiku 5.5 listed), others 200k. P context-windows
- CONFIRMED: official "context rot" claim, verbatim in P context-windows: "more context isn't automatically better. As token count grows, accuracy and recall degrade, a phenomenon known as context rot." Anthropic links its own article for detail: A effective-context-engineering-for-ai-agents (not fetched; read before citing more than the quote above). Consequence: curating what is in context matters as much as capacity.
- CONFIRMED: Claude Code compacts automatically as the limit nears, replacing history with a summary. "The summary keeps your requests and key code snippets, but detailed instructions from early in the conversation may be lost." Put persistent rules in CLAUDE.md. C how-claude-code-works#when-context-fills-up
- CONFIRMED survives compaction: system prompt, project-root CLAUDE.md, auto memory, skill descriptions re-injected; up to 5 recently read/edited files re-read (a file over 5,000 tokens comes back as a path only); invoked skill bodies capped at 5,000 tokens each, 25,000 total. Path-scoped rules and nested CLAUDE.md are summarised away and reload on demand. C context-window#what-survives-compaction
- CONFIRMED controls: `/compact focus on X`, `/context` (live breakdown), `/clear` between unrelated tasks, `/autocompact <tokens>`, `/rewind` then Summarize, subagents (own context window; only a summary returns). C context-window
- CONFIRMED: if one file or tool output is so large that context refills after every summary, auto-compaction stops after a few tries with an error instead of looping. C how-claude-code-works
- CONFIRMED: Claude Code warns when an MCP tool output exceeds 10,000 tokens; default cap 25,000 (`MAX_MCP_OUTPUT_TOKENS`). C mcp
- Consequence for bioinformatics (inference): do not `cat` a large VCF/BAM-derived table or a full log into the session; ask for head, counts, or a summary script, or delegate to a subagent.
- UNCONFIRMED: any official numeric threshold at which degradation starts. Do not state one.

## 3. System prompt vs user prompt vs instruction files
- CONFIRMED: Claude Code's system prompt is "the instructions Claude Code sends ahead of your conversation on every request", covering how Claude uses tools, behaves safely and formats responses. Add with `--append-system-prompt`, replace with `--system-prompt`. C glossary#system-prompt
- CONFIRMED: CLAUDE.md is "loaded at the start of every session as a user message after the system prompt", not part of the system prompt. Output-style instructions likewise. Both reach Claude as "system reminders" in the conversation. C glossary#claude-md, #system-prompt, #system-reminder
- CONFIRMED: system reminders also carry the skills list, hook `additionalContext`, file-changed notes, commit/PR attribution lines. If Claude follows a rule you did not write (e.g. Co-Authored-By), it may come from here. C how-claude-code-works#context-claude-code-adds-on-its-own
- CONFIRMED: CLAUDE.md is "context, not enforced configuration". To block an action regardless, use a PreToolUse hook. "The more specific and concise your instructions, the more consistently Claude follows them." Target under 200 lines per file; longer files "consume more context and reduce adherence". C memory
- CONFIRMED: AGENTS.md is read in place of CLAUDE.md when no CLAUDE.md exists in or above the working dir (v2.1.277+); if both exist, only CLAUDE.md files load unless configured. Import with `@AGENTS.md` from CLAUDE.md to share. C memory#agents-md
- CONFIRMED: editing CLAUDE.md mid-session does not reach the running session until /clear, /compact or restart (from the prompt-caching page, via search summary; C prompt-caching not fetched directly). Re-check before stating as fact.
- CONFIRMED: harness = tools, context management and execution environment around the model; Claude Code is the harness. C glossary#agentic-harness
- Consequence: three layers of authority. Harness system prompt (you rarely edit) > your CLAUDE.md/AGENTS.md (persistent, advisory, spends context every session) > the prompt you type (this task only). Put rules that must never be broken in hooks/permissions, not prose.
- UNCONFIRMED: the user-prompt vs system-prompt precedence/weighting inside the model; no official statement fetched. Do not claim system always wins.

## 4. Tool overload
- CONFIRMED: loading every tool definition up front causes "context bloat" (a typical five-server setup "can consume ~55k tokens in definitions before Claude does any work"; tool search "typically reduces this by over 85 percent", loading 3 to 5 tools) and a selection problem: "Claude's ability to pick the right tool degrades once you exceed 30-50 available tools". P agents-and-tools/tool-use/tool-search-tool
- CONFIRMED guidance: use tool search at 10+ tools, definitions over 10k tokens, or accuracy dropping; below 10 tools or small definitions, plain tool calling is better. Keep the 3 to 5 most-used tools non-deferred. P tool-search-tool#when-to-use-tool-search
- CONFIRMED: tool definitions count toward the context window; `defer_loading: true` keeps a tool out of context until discovered, though the full definitions are still sent in the request. P tool-search-tool; P context-windows
- CONFIRMED (Claude Code): MCP tool search is on by default; "Only tool names and server instructions load at session start, so adding more MCP servers has minimal impact on your context window"; full schema fetched on demand. No fixed per-server cap; "the practical limit is your context window budget". Disable with `ENABLE_TOOL_SEARCH=false`. Falls back to loading everything up front on older models and on Foundry-on-Azure. `/context` shows what is using space. C mcp#scale-with-mcp-tool-search, #configure-tool-search
- CONFIRMED: skills load only descriptions at start; full body on use. `disable-model-invocation: true` keeps a skill's description out of context. C how-claude-code-works#manage-context-with-skills-and-subagents
- Consequence: "install every MCP server" is not free. Deferral softens the context cost in Claude Code, but the 30-50 tool selection claim is about the API; whether it still bites behind deferral is UNCONFIRMED. Prefer few, well-named tools; remove unused servers.
- UNCONFIRMED: the 30-50 and 55k figures are Anthropic's own claims on a docs page, not independent measurements; no methodology cited.

## 5. Agent vs workflow vs single call
Primary source: A building-effective-agents (Anthropic engineering; it says tooling details have changed since Dec 2024, so cite concepts, not tool names).
- CONFIRMED definitions: workflows = "LLMs and tools are orchestrated through predefined code paths"; agents = systems where "LLMs dynamically direct their own processes and tool usage". (Workflow quote as returned by fetch; agent definition was paraphrased by the fetch tool, so re-read the article for exact wording before quoting.)
- CONFIRMED: start with the simplest solution; "building no agentic system at all may be the right choice"; for many applications "optimizing single LLM calls with retrieval and in-context examples is usually enough".
- CONFIRMED: agents trade latency and cost for task performance; autonomy brings higher cost and "compounding errors" risk; test in sandboxes with guardrails; use stopping conditions such as max iterations.
- CONFIRMED: workflows suit well-defined tasks needing predictability; agents suit open-ended problems where the number of steps cannot be predicted.
- CONFIRMED five workflow patterns: prompt chaining, routing, parallelization (sectioning, voting), orchestrator-workers, evaluator-optimizer.
- CONFIRMED (Claude Code): its loop is gather context, take action, verify results, repeat; tools are what make it agentic. C how-claude-code-works#the-agentic-loop. Glossary also: a verification loop (a check the agent can run) is what tells a session it is done. C glossary#verification-loop
- Consequence (inference): a fixed pipeline that always runs fastqc, trim, align is a workflow; Nextflow already is one. A single call suffices for "explain this error" or "convert this samplesheet format" when you paste the input. An agent earns its cost when steps depend on what it finds (debugging a failing run, exploring an unfamiliar repo).
- UNCONFIRMED: any quantified threshold for "when an agent is worth it". None in the article.

## aihero.dev LLM Fundamentals (topic list only)
Fetched 2026-11-16 https://www.aihero.dev/llm-fundamentals. Creator: Matt Pocock (attribute by name and link). Copyright reserved, no licence stated; robots.txt permits AI use. Do not reuse text.
Topics listed: (1) the function of a system prompt; (2) LLMs process numerical representations (tokens), not raw text; (3) problems from filling the context window too much; (4) performance costs of supplying many tools; (5) what an agent is and when one is not needed.
Note: this matches our five topics one to one; link out as "further reading by Matt Pocock", do not mirror its structure beyond the topic names.
- UNCONFIRMED: course depth, price, format (only the topic list was extracted; the fetch tool returned no more).

## Gaps to close before publishing
- Read A effective-context-engineering-for-ai-agents and A advanced-tool-use for the context rot and tool-bloat background.
- Fetch C prompt-caching to confirm the CLAUDE.md mid-session edit behaviour.
- Run our own count_tokens demo on a FASTA line vs an English line of equal length for the DNA claim.
