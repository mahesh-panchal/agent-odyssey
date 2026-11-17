# Model choice, effort and delegation

Checked 2026-11-17. Official docs only, plus one flagged secondary article. Pages came through a summarising fetch tool (quotes as returned; paraphrase on the site). Docs pages show no publish date; model-config, sub-agents, skills and choosing-a-model pages were read only in their first ~100k characters.
Base: P = https://platform.claude.com/docs/en/ ; C = https://code.claude.com/docs/en/ ; O = https://opencode.ai/docs/
Not repeated: effort levels list, API effort wording, Claude Code effort defaults, `max` overthinking quotes, `ultrathink` (research/terminology.md section 6); `/context`, `/clear`, subagent context isolation, `/usage` cost basics (session-management.md, fundamentals.md).
Decision fed: quest text on picking a model, tuning effort, delegating reading to cheaper subagents.

## 1. Model families (P about-claude/models/choosing-a-model)
- CONFIRMED: four tiers in the selection matrix. Fable 5.2 (`claude-fable-5-2`): highest capability, hours-long agent sessions and deep research. Opus 5.5 (`claude-opus-5-5`): complex agentic coding. Sonnet 5.5: "speed and capability for everyday coding, agent, and enterprise workloads". Haiku 5.5: lowest latency and price, lists "subagent tasks".
- CONFIRMED: "Most workloads start with Claude Opus 5.5." Fable 5.2 is "most capable model open to all customers"; Mythos 5.2 has the same capabilities for verified organisations only.
- CONFIRMED relative cost: Opus 5.5 costs half as much per token as Fable 5.2 (stated in the article only; P fast-mode shows fast prices of $8/$40 per MTok Opus 5.5 vs $16/$80 Fable 5.2, which is the fast-mode rate, not standard). Standard prices live in the models overview table (not fetched). Do not print per-token prices on the site.
- UNCONFIRMED: Haiku 5.5 price rising above 100K-token prompts (article claim only).
- CONFIRMED: two start strategies: efficiency-first (Haiku, upgrade if needed) or capability-first (Opus 5.5, then lower effort or downgrade). Move to Fable 5.2 if evals at `xhigh`/`max` still fall short.
- CONFIRMED: fast mode = same model, "up to 2.5x higher output tokens per second" at premium pricing, on Fable 5.2, Mythos 5.2, Opus 5.5 (Opus 5 research preview; Opus 4.8 deprecated, removal 2026-11-30). API field `speed: "fast"`; not with Batch API or Priority Tier; falling back to standard misses the prompt cache. P build-with-claude/fast-mode
- UNCONFIRMED: how fast mode is switched on in Claude Code (costs page links to C fast-mode, not fetched). Leave it out of quests.

## 2. Aliases and setting the model (C model-config)
- CONFIRMED aliases, exactly: `default` (clears an override; "not itself a model alias"), `best` (same as `opus`), `fable`, `sonnet`, `opus`, `haiku`, `sonnet[1m]`, `opus[1m]`, `opusplan` (opus in plan mode, then sonnet for execution).
- CONFIRMED: on the Anthropic API `opus` = Opus 5.5, `sonnet` = Sonnet 5.5, `haiku` = Haiku 5.5. Other providers resolve aliases to earlier versions (example: Foundry gives Opus 4.6 / Sonnet 4.5).
- CONFIRMED set-model order of priority: `/model <alias|name>` in session (alone opens picker; Enter saves as default, `s` for this session only); `claude --model <alias|name>`; env `ANTHROPIC_MODEL`; settings field `model`; `ANTHROPIC_DEFAULT_MODEL` for new sessions (v2.1.236+).
- CONFIRMED pinning: use a full name such as `claude-opus-5-5`, or set `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`, `ANTHROPIC_DEFAULT_FABLE_MODEL`.
- CONFIRMED default model: Opus 5.5 on Pro, Max, Ultra, Team, Enterprise and API; Sonnet 4.5 on Foundry; an admin default overrides. Admins restrict with `availableModels` (+ `enforceAvailableModels`).
- CONFIRMED: switching models "can change how prompt caching behaves"; Claude Code may ask you to confirm. `/model` switches also reach subagents that inherit.
- Reproducibility (inference): aliases move when a new version ships, so a lab pipeline or course material that must give the same results pins a full name.

## 3. Effort in Claude Code and skills
- CONFIRMED set methods: `/effort`, `--effort`, `CLAUDE_CODE_EFFORT_LEVEL`, settings `effortLevel`, per-model `modelSettings`; `CLAUDE_CODE_EFFORT_LEVEL=auto` sends no level. `ultracode` is a Claude Code setting for dynamic workflows, "not a model effort level". C model-config
- CONFIRMED skill frontmatter `model`: same values as `/model`, or `inherit`; applies for the rest of the turn only, not saved; ignored if `availableModels` excludes it. `effort`: `low|medium|high|xhigh|max` (levels depend on the model); turn-only; overrides session effort but not `CLAUDE_CODE_EFFORT_LEVEL`. With `context: fork` both apply to the forked subagent instead. Example in the docs: `model: opus`, `effort: high`. C skills
- CONFIRMED API defaults (differs from the Claude Code list in terminology.md): `high` everywhere except `medium` on Opus 5.5 and Haiku 5.5, so Sonnet 5.5 is `high` on the API page. P effort. The Claude Code default for Sonnet 5.5 is `medium` per terminology.md; the two pages disagree, so name the surface.
- CONFIRMED model-specific advice: Opus 5.5 default `medium`; Sonnet 5.5: `medium` for well-specified agentic coding, `high` for harder or longer, `xhigh`/`max` only where evals show a gain; Haiku 5.5: start `medium`, and at `low` it "is more likely to skip a search, stop early, or skip a check". P effort
- CONFIRMED: `low` listed for "simpler tasks... such as subagents". Lower effort means fewer, terser tool calls. P effort
- CONFIRMED: "Tuning effort is often a better lever than switching models." P choosing-a-model
- CONFIRMED cost data (Anthropic-internal, "directional"): Sonnet 5.5 `medium` scored about 7 points below `high` for about 59% of the cost on long-horizon coding. P optimizing-for-cost
- CONFIRMED: sweep effort in separate sessions; changing effort mid-session invalidates the cache (top-level effort; per-message effort on supported models keeps it). P optimizing-for-cost, effort
- CONFIRMED: at `xhigh`/`max` Sonnet 5.5 may start extra review rounds; a scoping prompt keeps it on task. P optimizing-for-cost
- CONFIRMED: Opus 4.7 at low/medium scopes work to what was asked; if reasoning looks shallow on hard problems, raise effort rather than prompt around it. P effort
- CONFIRMED (cost-saving pattern): if outcomes are checkable (tests, a verifier), run at `low`, re-run only failures at `high`. Anthropic measure: Opus 5.5 about 97% solved at ~$0.17/task vs 95.3% at $0.29 all-`high` (SWE-bench Pro subset). Caveats: a checker that passes bad work lets failures through; failures take two runs of wall time. P optimizing-for-cost
- CONFIRMED: compare "cost per completed task, not cost per token"; "price the tail" (two of 20 problems carried 43% of spend); failed tasks still bill. P optimizing-for-cost

## 4. Delegation (C sub-agents; C costs; P optimizing-for-cost)
- CONFIRMED subagent `model` accepts `sonnet`, `opus`, `haiku`, `fable`, a full ID (e.g. `claude-opus-5-5`), or `inherit`. Omitted = resolution order, not literally `inherit`. `effort` accepts `low|medium|high|xhigh|max`; it overrides session effort but not `CLAUDE_CODE_EFFORT_LEVEL`. If the subagent's model differs from the main one and has no `effort`, the session level does not apply, so set it.
- CONFIRMED resolution order (first wins): per-invocation `model` parameter; definition `model`; env `CLAUDE_CODE_SUBAGENT_MODEL`; the main conversation's model. `CLAUDE_CODE_SUBAGENT_MODEL` alone does not change built-in Explore/Plan. Forcing: `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` (v2.1.257+) ignores definition and per-call models.
- CONFIRMED built-ins: general-purpose and Plan follow the parent model; `statusline-setup` Sonnet; `claude-code-guide` Haiku. Explore: page says "the parent conversation's model", then (as returned) that with a subscription/Console/gateway it runs on the Opus the alias resolves to. A user subagent named `Explore` overrides it (example `model: haiku`). The Explore wording is contradictory in the summary; re-read before quoting.
- CONFIRMED context/cost benefits: exploration stays out of the main conversation; only a summary returns; "control costs by routing tasks to faster, lower-cost models like Haiku". Caveats: subagent requests count toward the same usage limits; many subagents returning detailed results "can consume significant context".
- CONFIRMED CLAUDE.md: non-fork subagents load the CLAUDE.md hierarchy, except built-in Explore and Plan (skipped for speed); `omitClaudeMd: true` skips it in a custom one. Subagents do not inherit output style or auto memory. Restate must-have rules in the delegation prompt.
- CONFIRMED: subagents inherit the session thinking setting (no per-subagent setting); nested subagents inherit their spawner's model; `/tasks` shows each running subagent's model and effort (v2.1.242+).
- CONFIRMED: orchestrator pattern helped only for routine work with a long cost tail or work larger than one context; for one dependent chain that fits in one context, single model at lower effort won. Opus 5.5 over Sonnet 5.5 subagents cost about a third less on defect search with similar score; Haiku 5.5 subagents on coding "were not better than simply lowering effort". P optimizing-for-cost
- CONFIRMED: build a multimodel setup only if it beats the single model's whole score-vs-spend curve. P optimizing-for-cost
- CONFIRMED: Agent teams: "Use Sonnet for teammates"; about 7x tokens of a standard session in plan mode (C costs).

## 5. Cost visibility (C costs)
- CONFIRMED `/usage`: Session block shows total cost, API and wall duration, lines changed, and "Usage by model" (input, output, cache read/write tokens, $ per model). Dollar figure is computed locally at list price (or admin `modelPricing`), an estimate. Resets on `/clear` (v2.1.211+). Subscribers see plan usage bars instead of meaningful $.
- CONFIRMED: `/usage` Session block also has a `Prompt cache (main)` line (v2.1.251+; main conversation only, not subagents). Plan breakdown attributes usage to skills, subagents, plugins, MCP servers, with recommendations (`f` applies, v2.1.305+).
- CONFIRMED: `/insights` writes an HTML report of how you work. Status line can show cost/context.
- NOT FOUND in these pages: a `/cost` command. Do not teach `/cost`; use `/usage`.
- CONFIRMED: Anthropic average about $13 per developer per active day (enterprise deployments); 90% below $30.

## 6. OpenCode (O models, O agents)
- CONFIRMED: `/models` picks for this session only (config unchanged); `opencode run --model provider/model-id`; `model` key in `opencode.json`/`opencode.jsonc` sets the default, falling back to the newest available model if unavailable. Format `provider/model-id`, optional `#variant` (e.g. `...#high`); IDs case-sensitive.
- CONFIRMED per-agent: `model` key on an agent (markdown frontmatter string, or JSONC object with `providerID`, `model`, `variant`). Frontmatter example: `mode: subagent`, `model: anthropic/claude-sonnet-5-5#high`. A subagent without `model` inherits the parent session model. Built-ins: `build`, `plan` (primary), `general`, `explore` (subagents). The page does not say which model each built-in uses.
- UNCONFIRMED: a `small_model` key (not on the page). Note the JSONC example uses top-level key `agents`; verify against the schema before copying.
- CONFIRMED local models: Ollama at `http://127.0.0.1:11434` is auto-discovered under provider `ollama` (e.g. `ollama/gemma3:4b`); change host with `providers.ollama.settings.baseURL`; LM Studio and vLLM likewise; disable discovery with `"plugins": ["-opencode.provider.ollama"]`.
- UNCONFIRMED: that a local model is good enough as a cheap delegate, its cost, or tool-use quality. The docs only say it can be selected.

## 7. Local models with Claude Code
- UNCONFIRMED: any Claude doc page on running Ollama as a Claude Code subagent. Claude Code subagent `model` values are Claude aliases or Claude IDs only (section 4). Ollama is an OpenCode-only claim on these pages. (Gateway use via `ANTHROPIC_BASE_URL` appears on the sub-agents page but was not pursued.)

## 8. Preserved thinking and switching (P preserved-thinking)
- CONFIRMED: on the API, a thinking block is tied to the preceding prompt, the model and the account. A model that cannot read another's blocks drops them for that request, no error, no billing; switching back reads them again. Haiku 5.5 to Opus 5.5 keeps reasoning; Opus 5.5 to Sonnet 5.5 or Haiku 5.5 does not; Fable 5.2 to anything else drops it. Useful only as "switching down loses earlier reasoning"; Claude Code handles this itself.
- CONFIRMED: per-turn model overrides in skills last one turn; `/model` switch persists.

## 9. Secondary source: claude.dev blog (Addy Osmani, 2026-11-09)
Provenance not confirmed, no reuse licence, benchmark numbers vendor-run and unverified. Ideas paraphrased only; cite as "one article" or not at all. Mapped to the official docs:
- Default Opus 5.5 at `medium`; step down to Sonnet 5.5 for well-scoped fixes; Haiku for classification and extraction and as subagent; Fable 5.2 for hardest work. Official docs support this tiering (P choosing-a-model, optimizing). The per-task-type table is ARTICLE-ONLY in detail (bug fixes vs migrations).
- Raise effort before switching models. Official: partly (P choosing-a-model "better lever"). "Past `high` one more level can cost as much as a larger model; test the next model up at lower effort" is ARTICLE-ONLY.
- Effort cannot add knowledge the model lacks: ARTICLE-ONLY (the docs say higher effort adds thoroughness, not this).
- Order: give a check first, then raise effort, then change model: ARTICLE-ONLY as a sequence; the docs do say to give verification targets (C costs).
- Run checkable tasks at low, re-run failures at high: official (section 3).
- Cost per finished task, not per token; price the hardest tasks: official.
- Keep expensive-model context lean, push bulk reading to cheaper subagents; edits stay on the main model: official for delegation benefits; "keep edits on the main model" is ARTICLE-ONLY.
- Switching models mid-conversation misses the cache; compact or start fresh first: partly official (model-config note, preserved-thinking). The specific "compact first" tip is ARTICLE-ONLY.
- Pin a subagent's model in its definition (article example `model: haiku`, tools `Read, Grep, Glob, Bash`, "log-reader"), and define your own `Explore` on Haiku: official (section 4).
- `opusplan` caution (puts edits on the smaller model; measure on own tasks): the alias is official; the caution is ARTICLE-ONLY.
- Test on your own tasks with outcome checks, separate sessions per effort level: official (P optimizing-for-cost, choosing-a-model).

## 10. Exact names
- Documented: aliases above; `/model`, `--model`, `ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_MODEL`, settings `model`; `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU,FABLE}_MODEL`; `/effort`, `--effort`, `CLAUDE_CODE_EFFORT_LEVEL`, `effortLevel`, `modelSettings`; frontmatter `model`, `effort` (skills and subagents), `omitClaudeMd`; `CLAUDE_CODE_SUBAGENT_MODEL`, `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`; `availableModels`; `/usage`, `/insights`, `/tasks`; `MAX_THINKING_TOKENS` (fixed-budget models only; adaptive models ignore it); API `output_config.effort`, `speed: "fast"`.
- NOT documented in these pages: `/cost`, `--subagent-model`, a per-subagent thinking setting, `small_model`, any Ollama-via-Claude-Code route, a documented price table in these pages.

## Open items
- Read C model-config past 100k (effort resolution order, auto-compact window) and C fast-mode before quoting.
- Re-read Explore wording on C sub-agents.
