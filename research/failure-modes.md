# Failure modes zone: memory, sessions, usage, context poisoning, LLM failure modes

Checked 2026-11-16. Pages fetched via a summarising fetch tool (quotes as returned, short). Paraphrase on the site. Not repeated here: tokens, context window, compaction survival list, CLAUDE.md-as-user-message (see fundamentals.md, terminology.md).
Base: C = https://code.claude.com/docs/en/ ; P = https://platform.claude.com/docs/en/ ; A = https://www.anthropic.com/

## 1. Memory (Claude Code)
- CONFIRMED: two memory systems, both loaded at the start of every session. CLAUDE.md = instructions you write; auto memory = notes Claude writes itself from your corrections and preferences. "Each Claude Code session begins with a fresh context window"; these two carry knowledge across sessions. C memory
- CONFIRMED: CLAUDE.md scopes are project, user, or org. Auto memory is per git repository (all worktrees share it), machine-local, not shared across machines or cloud environments. C memory
- CONFIRMED: auto memory lives in `~/.claude/projects/<project>/memory/`, with a `MEMORY.md` index plus topic files; plain markdown you can read, edit or delete. Only the first 200 lines or 25KB of `MEMORY.md` load at session start; topic files are read on demand. Memory files are exempt from the transcript retention sweep. C memory
- CONFIRMED: `/memory` lists CLAUDE.md files and memory locations, toggles auto memory (`autoMemoryEnabled`), opens the memory folder. "Saved N memories" / "Recalled N memories" in the UI means Claude touched that directory. `/context all` lists Memory files that loaded. C memory, C commands
- CONFIRMED: memory is "context, not enforced configuration"; contradictory instructions: "Claude may pick one arbitrarily". `/doctor prompt-audit` checks instruction files for outdated or conflicting content. C memory
- CONFIRMED difference from the context window: the context window is the live working space of one session and empties with `/clear` or a new session; memory is files on disk re-read into a new window. Memory files also occupy context every session. C how-claude-code-works, C memory
- CONFIRMED (API): memory tool `{"type": "memory_20250818", "name": "memory"}`, client-side: Claude requests file operations (`view`, `create`, `str_replace`, `insert`, `delete`, `rename`) under `/memories`, and your application executes them on storage you control. Purpose: persist info across conversations without keeping it all in the window. Developer must block path traversal. P agents-and-tools/tool-use/memory-tool
- Consequence (inference): memory is not truth, it is text that was once written; wrong entries get loaded forever (see section 4).

## 2. Session / session context
- CONFIRMED: a session is "a saved conversation tied to a project directory", stored locally as JSONL under `~/.claude/projects/<project>/<session-id>.jsonl`; transcripts deleted after 30 days by default (`cleanupPeriodDays`). C sessions
- CONFIRMED: "Sessions are independent": a new session starts with a fresh context window and no history from earlier sessions. C how-claude-code-works
- CONFIRMED commands: `claude --continue` (most recent in this directory), `claude --resume [name|id]` (picker), `/resume` inside a session, `claude --continue --fork-session` or `/branch` (copy into a new session ID), `/rename`, `/clear [name]` (new empty conversation; old one stays resumable; alias `/new`), `/compact [instructions]` (replace history with a summary; stays the same conversation), `/context`, `/export`. C sessions, C commands
- CONFIRMED: resume restores messages, tool calls and results (from the last compaction summary onward if compacted), model and permission mode; it does not restore flags such as `--mcp-config`, `--plugin-dir`, `--add-dir`. C sessions
- CONFIRMED: `/clear` keeps project memory (CLAUDE.md, auto memory) but drops the conversation. C commands ("Between sessions")
- Session vs memory (confirmed pieces combined): session = this conversation's transcript (resumable, temporary, tied to a directory); memory = durable notes/instructions that every new session reads. Compaction shrinks a session; it does not create memory.

## 3. Session usage
- CONFIRMED: `/usage` shows session cost (computed locally from token counts at list price, an estimate), plan usage limits, activity stats; on Pro/Max/Ultra/Team/Enterprise also a breakdown of what counts against limits (skills, subagents, plugins, MCP servers) with recommendations. `/cost` is an alias of `/usage`; `/stats` is an alias opening the Stats tab. Session totals reset on `/clear`. C costs, C commands
- CONFIRMED: for subscribers the dollar figure "isn't relevant for billing"; the plan bars are what matter. Teams/Enterprise: a per-seat allowance with a rolling five-hour window and a weekly window, shared with Claude chat and Cowork. Messages "You've hit your session limit" / "weekly limit" are those windows; `/usage-credits` buys extra. C costs
- CONFIRMED: `/usage` may say "rate limited until ..." meaning only that Claude Code cannot fetch plan limits, "not that your work with Claude is limited". C costs
- CONFIRMED: API usage is billed per token; thinking tokens are billed as output tokens. C costs
- CONFIRMED why usage climbs: Claude Code sends the whole conversation on every request, and each tool-using step is another request; with caching the history is re-read at the cheaper cached rate but a one-line question in an all-day session still draws on the whole conversation. First message after a break longer than the cache lifetime reprocesses everything. `/compact` itself reads the whole conversation (a large request). Also: scheduled `/loop` tasks firing while idle, subagents and agent teams (each its own context; teams about 7x a standard session), extended thinking. C costs
- CONFIRMED large tool outputs: Claude "reading a 10,000-line log" is the docs' own example; a hook can filter to matching lines so context drops from tens of thousands of tokens to hundreds. Subagents keep verbose output in their own window; only a summary returns (but their requests still draw on usage). C costs
- CONFIRMED mitigations: `/clear` between unrelated tasks ("costs nothing"), `/compact <focus>`, `/context` to see what fills the window, `/model` and `/effort` to match model and effort to the job, specific prompts, disable unused MCP servers with `/mcp`, keep CLAUDE.md under 200 lines (move workflows into skills). C costs
- UNCONFIRMED: the exact token size of the plan allowance on Pro/Max; docs point to claude.com/pricing and the Help Center. Do not state numbers.

## 4. Context poisoning
- COMMUNITY TERM, not vendor documentation. Coined in "How Long Contexts Fail" by Drew Breunig, 2025-06-22 (author name taken from the O'Reilly reprint listing / my search; the fetched page text did not name him; confirm). https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html
  - Poisoning: a hallucination or other error enters the context and is repeatedly referenced. His example: the Gemini 2.5 technical report's Pokemon-playing agent, whose recorded goals/summary became corrupted with false game state, so it fixated on impossible goals.
  - Same post, also COMMUNITY TERMS: distraction (context so long the model over-focuses on it and neglects what training taught), confusion (superfluous content degrades the answer), clash (new info or tools contradict earlier context).
  - CONFIRMED that the fetched post gives no poisoning-specific fix (promises a follow-up on quarantine and dynamic tool loading). Mitigations below are Anthropic's, or our inference, not his.
- CONFIRMED official adjacent language: Anthropic's context engineering article calls the buildup of stale or unneeded material "context pollution" and notes aggressive compaction can drop details that matter later. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents (fetched; wording from summariser)
- CONFIRMED official guidance that errors persist in the conversation: "If you've corrected the same thing twice and it's still wrong, a third correction mostly adds to a conversation that already contains two failed attempts for Claude to keep re-reading. `/clear` plus one new prompt that folds in what you learned works better almost every time." Also "after two failed corrections run `/clear` and write a better prompt." C best-practices
- CONFIRMED tools: `/rewind` (or Esc twice) rolls conversation and/or code back to an earlier prompt and can summarize stale parts; `/clear`; subagents isolate noisy work. C best-practices, C costs
- Mitigations (inference built on the above): (1) fresh session with a short, corrected brief; (2) rewind to before the bad turn rather than arguing; (3) never let Claude write a claim into CLAUDE.md/MEMORY.md until you checked it against the source (poisoned memory is reloaded every session; open it via `/memory`, delete the line); (4) have the agent re-derive from files or a script, not from earlier chat; (5) use `/doctor prompt-audit` to find stale or contradictory instruction files.
- UNCONFIRMED: any official Anthropic use of the term "context poisoning".

## 4b. Can a session forget on request?
Checked 2026-11-23. Pages read through a summarising fetch tool; the `commands` and `memory` pages were truncated, so lines marked (summary) are not verbatim. Quotes short.
- CONFIRMED the docs are SILENT on whether telling Claude in chat to "forget" or "ignore" something removes it. None of the pages read (context-window, checkpointing, commands, memory, data-usage, claude-directory) say it works, and none say it fails. UNCONFIRMED either way.
- INFERENCE (ours, not a documented claim): text already in the conversation is still sent with every turn, so a chat request to ignore it adds one more message; it does not delete the earlier one. This matches the "third correction adds to a conversation that already holds two failed attempts" guidance in section 4. Do not teach as documented.
- CONFIRMED what does change what the model sees:
  - `/clear`: "Start a new conversation with empty context." C commands
  - `/compact`: "replaces the conversation with a structured summary." C context-window. What a summary drops is not stated; Anthropic's context engineering article says aggressive compaction can lose detail (section 4).
  - `/rewind` Summarize from/up to here: compresses part of the conversation into a summary. "Summarizing doesn't change files on disk, and the original messages stay in the session transcript, so Claude can still reference the details." C checkpointing
- CONFIRMED a cleared conversation can come back: `/resume`, or in the same process the rewind menu entry "`/resume <session-id> (previous session)`", "available until you exit Claude Code or resume a different session". C commands, C checkpointing
- CONFIRMED the transcript is a separate store: "Claude Code clients store session transcripts locally in plaintext under `~/.claude/projects/` for 30 days by default"; `cleanupPeriodDays` changes it. Not encrypted at rest. C data-usage, C claude-directory
- CONFIRMED secrets reach disk: "If a tool reads a `.env` file or a command prints a credential, that value is written to `projects/<project>/<session>.jsonl`." Prevention is a permission rule that denies the read. C claude-directory
- CONFIRMED real deletion on disk: `claude purge` deletes "Transcripts and auto memory under `projects/`" for one project (`--dry-run` to preview, `--all` for every project); or delete the paths by hand. Memory files ("`MEMORY.md` and topic files stay until you or Claude edits or deletes them" (summary)) are removed via `/memory` or by deleting the file. C claude-directory, C memory
- CONFIRMED data sent to Anthropic is retained per plan (30 days; 5 years if data use for model improvement is allowed; commercial standard 30 days). Deleting it for a local session is NOT STATED; only cloud sessions can be deleted by the user. C data-usage. See privacy-and-unpublished-work.md.
- UNCONFIRMED: whether a file read earlier is dropped by `/compact`. The page says "Right after compaction, Claude Code re-reads up to five of the files Claude has read or edited in the session, choosing the ones modified most recently" (C context-window), so a file can return to context. Whether a secret is dropped or returned is NOT STATED. Inference: do not rely on compaction to scrub a secret.
- Three meanings of "forget" to keep apart on the site: (1) out of the live context window (`/clear`, compaction), (2) off disk (transcript: `claude purge`/`cleanupPeriodDays`; memory: `/memory`), (3) off Anthropic's side (retention rules, not user-deletable for local sessions per the pages read). Safest rule for sensitive data: never let it into the session (deny rule, work on the cluster), since removal afterwards covers only the first two.
- Not checked: that the claude-directory and data-usage wording is current beyond 2026-11-23; no command was run (`claude purge` was not executed).

## 5. Token
- Brief: a token is a chunk of text the model reads (word piece, character or byte); not a word. Usage and context limits are counted in tokens. Full detail and sources in fundamentals.md section 1.

## 6. LLM failure modes relevant to scientists
Official hedge to quote in spirit: even advanced models "can sometimes generate text that is factually incorrect or inconsistent with the given context"; techniques "don't eliminate them entirely. Always validate critical information." P test-and-evaluate/strengthen-guardrails/reduce-hallucinations

### Hallucination / fabrication (invented citations, gene IDs, flags, package functions)
- Looks like: plausible DOI or PMID that does not exist; a tool option that was never implemented; confident wrong sequence annotation.
- CONFIRMED mitigations (same page): permit "I don't know"; extract word-for-word quotes first for long documents (page suggests >20k tokens); make every claim cite a quote and retract any claim with none; run the prompt several times and compare (best-of-N); restrict to supplied documents.
- Our advice (inference): look up every citation and ID in PubMed/Ensembl/the tool's `--help`; the agent can run the tool to test a flag.

### Sycophancy
- Looks like: agrees with your wrong hypothesis, softens a correct criticism when you push back, praises a flawed analysis.
- CONFIRMED peer-reviewed: Sharma et al., "Towards Understanding Sycophancy in Language Models", ICLR 2024, arXiv 2310.13548 (Anthropic authors). Five RLHF assistants (incl. claude-1.3, claude-2.0) often match a user's stated view; human and preference-model raters sometimes prefer convincing sycophantic answers to correct ones. https://arxiv.org/abs/2310.13548
- UNCONFIRMED: Anthropic's newer percentages on reduced sycophancy (only secondary summaries seen; https://www.anthropic.com/research/claude-personal-guidance exists, only opening fragment read). Do not quote numbers.
- Mitigation (inference): ask for the strongest case against your idea; do not reveal your preferred answer in the prompt; ask it to check against data, not opinion.

### Arithmetic and counting errors (letters, bases, rows)
- Example: "how many n in banana?" correct answer 2 (b-a-n-a-n-a). Models may mis-state because they see tokens, not letters.
- CONFIRMED (peer-reviewed/preprints, mixed): tokenization is a proposed cause: Cosma et al., "The Strawberry Problem", EMNLP 2025, arXiv 2505.14172 (character-level info is weakly available inside tokens); Zhang et al., "Counting Ability of LLMs and Impact of Tokenization", arXiv 2410.19730 (abstract: chain of thought can help and tokenization changes performance; abstract does not state that failures persist with CoT, but the full text, arxiv.org/html/2410.19730 read 2026-11-17, says significant failures remain even with CoT in models like GPT-4). https://arxiv.org/abs/2505.14172 ; https://arxiv.org/abs/2410.19730
- CONFIRMED counter-view: CharBench, arXiv 2508.02591, finds tokenization properties only weakly correlated with correctness; word length and true count matter more; Fu et al., arXiv 2412.18626, link errors to letter frequency and length. So say "tokenisation is a leading explanation, disputed in detail", not settled. https://arxiv.org/abs/2508.02591
- CONFIRMED fix evidence: arXiv 2410.14166 abstract does not state that Python code makes counting succeed (it says specialised math/coding LLMs still struggle and reasoning before answering is the most robust fix); the full text (arxiv.org/html/2410.14166, read 2026-11-17) says coding LLMs explicitly asked for Python complete the counting tasks, but fail in open-ended prompting. https://arxiv.org/abs/2410.14166 (authors Nan Xu and Xuezhe Ma, seen on the arXiv page 2026-11-17)
- UNCONFIRMED: no Anthropic doc found that discusses letter counting or arithmetic limits. Only mechanism-level support: Anthropic documents a code execution tool and a bash tool that let Claude run code. Models overview lists `server_tools.code_execution` capability. P models/overview
- Mitigation: have the agent run code (`grep -o n | wc -l`, `seqkit stats`, awk) and show the command and output; never trust a count it states in prose. Offer a live demo with `count_tokens` on a FASTA line (our own measurement is a valid source).

### Long-context degradation
- CONFIRMED official: "As token count grows, accuracy and recall degrade, a phenomenon known as context rot." P context-windows (already in fundamentals.md). Anthropic context-engineering article: finite "attention budget". 
- CONFIRMED peer-reviewed: Liu et al., "Lost in the Middle", arXiv 2307.03172 (TACL 2024 per my memory; the search did not confirm the venue): accuracy highest when relevant info is at the start or end of the input, lower in the middle, and falls as input grows. https://arxiv.org/abs/2307.03172
- Mitigation: curate inputs (head, counts, filtered tables), subagents, `/clear`, repeat key instructions in CLAUDE.md, not mid-chat.

### Instruction drift / forgotten instructions
- CONFIRMED official: after auto-compaction "detailed instructions from early in the conversation may be lost"; put persistent rules in CLAUDE.md; long CLAUDE.md "reduce adherence"; CLAUDE.md is advisory, use a PreToolUse hook to block actions. C how-claude-code-works, C memory
- Mitigation: short CLAUDE.md, hooks for must-never rules, `/compact focus on ...`.

### Non-determinism
- UNCONFIRMED (official): the fetched consistency page does not state that outputs vary or discuss temperature. It recommends explicit output formats, examples, retrieval grounding, prompt chaining; for guaranteed JSON use Structured Outputs. P increase-consistency
- Practical (inference, plus doc-backed best-of-N idea above): the same prompt can give different answers; run twice and compare; record the exact command, model, version in your methods; do not treat an agent run as a reproducible analysis, the script it writes is.

### Overconfidence
- CONFIRMED official proxy: "Allow Claude to say I don't know" can drastically reduce false information, implying default answers lack calibrated hedging. P reduce-hallucinations. Claude Code docs: "Claude said it was done and it wasn't quite, usually because it had no way to check its own work"; fix = "give Claude a check to run". C best-practices
- Mitigation: demand a verifying command (tests, row counts, md5, `nextflow -stub`) and read its output.

### Prompt injection
- CONFIRMED official: Anthropic calls it "far from a solved problem", "No browser agent is immune"; mitigations are RL training, classifiers on untrusted content, red teaming; improved safeguards cut internal attack success to about 1-2.4 percent in a Best-of-N test, still "meaningful risk". https://www.anthropic.com/research/prompt-injection-defenses
- CONFIRMED (Claude Code): permission prompts, network commands (`curl`, `wget`) not auto-approved, WebFetch summarised through a separate model call, sandboxed Bash (`/sandbox`), workspace trust dialog. Advice: review commands before approving, avoid piping untrusted content, use VMs for external services. "No system is completely immune." C security
- Relevance: a README, paper PDF, FASTA header, or web page the agent reads can contain instructions. Treat fetched content as data.

### Stale knowledge / training cutoff
- CONFIRMED: Sonnet 5.5 and the other current models list reliable knowledge cutoff and training data cutoff both Jun 2026 (reliable = where knowledge is most extensive; training cutoff = broader range of data). P models/overview
- Consequence: newer tool versions (nf-core modules, Nextflow syntax, database releases) postdate it; check `--version` and the docs. Web search/fetch tools can fetch current info, with the injection caveat above.

## 7. What LLMs do well that is checkable
- Tasks: summarise text, draft prose, explain code or an error, convert formats (samplesheet CSV to JSON), write a script you can run. Shared property: you can inspect the output or run a test. (Inference.)
- CONFIRMED peer-reviewed caveat: Maynez et al., "On Faithfulness and Factuality in Abstractive Summarization", ACL 2020: human raters found substantial hallucinated, unfaithful content in all neural summaries tested; pretrained models did better but not clean. Dated (pre-chat-LLM) evidence; direction still relevant. https://aclanthology.org/2020.acl-main.173
- UNCONFIRMED: an Anthropic-published faithfulness rate for current Claude summarising scientific papers. None found.
- CONFIRMED mitigation (official): quote-first extraction and claim-by-claim citation checking. P reduce-hallucinations
- Spot-check protocol (our advice): check every number, gene/sample name, direction of effect, and negation in the summary against the source; ask for quoted lines with page/section; omissions are harder to see, so skim the source's abstract and limitations yourself.

## Gaps before publishing
- Fetch Breunig's author byline and his follow-up "How to Fix Your Context" (https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html, url unfetched) for named mitigations (quarantine, pruning).
- Confirm TACL venue for Lost in the Middle; verify authors for 2410.14166 and 2410.19730 on arXiv.
- Look for Anthropic text on temperature/non-determinism (API reference, not found here).
- Measure our own banana/FASTA demos (count_tokens) and cite them as first-party.
