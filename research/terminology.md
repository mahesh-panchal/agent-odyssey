# Terminology research for the teaching site

Date checked for every entry: 2026-11-16. Sources are official docs only, fetched via WebFetch. WebFetch returns summaries from a small model, so quotes marked "quote" are as returned and worth a spot-check before publishing. Several long pages were read only up to their first 100,000 characters.

## 1. Model (vs product)
- A model (for example Claude Sonnet 5.5) is the LLM that reasons. Claude Code is a product built around a model. The docs say: "The agentic loop is powered by two components: models that reason and tools that act." "When this guide says 'Claude chooses'... it's the model doing the reasoning."
- Model aliases (`sonnet`, `opus`, `haiku`) "point to the recommended version... and update over time"; pin with a full name such as `claude-opus-5-5`.
- Source: https://code.claude.com/docs/en/how-claude-code-works and https://code.claude.com/docs/en/model-config

## 2. Harness / agent harness
- Claude Code docs: "Claude Code is the layer around the model that provides the tools and manages the context the model sees. This surrounding layer is what the term agentic harness refers to." (Source: https://code.claude.com/docs/en/how-claude-code-works)
- What the harness adds, per the same page:
  - Tools: file operations, search, execution, web, code intelligence.
  - The loop: gather context, take action, verify results, repeat.
  - Permissions: modes (Auto, Manual, Accept edits, Plan) and allow rules in settings.
  - Context management: compaction, CLAUDE.md, auto memory, skills.
  - Checkpoints (undo for file edits).
  - Extensions: skills, MCP, hooks, subagents.
- Same model, different harness: OpenCode is "an open source coding agent" (https://opencode.ai/docs/). Its providers page (https://opencode.ai/docs/providers/) lists Anthropic as a supported provider, set up via `/connect`, which suggests Claude models can run in OpenCode. The page does not document logging in with a Claude Pro/Max subscription.
- Unconfirmed: no official doc states the "same model, different harness gives different results" claim directly. Treat it as an inference from the harness definition.
- Unconfirmed: OpenCode's own tool, permission and loop docs were not fetched (only intro, providers, skills pages).

## 3. Skill (SKILL.md)
- Definition: "Create a `SKILL.md` file with instructions, and Claude adds it to its toolkit. Claude uses skills when relevant, or you can invoke one directly with `/skill-name`." Skills follow the open Agent Skills standard (agentskills.io).
- Format: YAML frontmatter (`name`, `description`, etc.) then Markdown. The `description` says what it does and when to use it, and Claude uses it to decide when to apply the skill. Keep `SKILL.md` under 500 lines.
- Progressive disclosure, three stages:
  1. Startup: only descriptions are loaded. "skill descriptions are loaded into context... but full skill content only loads when invoked." The combined `description` and `when_to_use` text is truncated at 1,536 characters in the skill listing.
  2. On use: the `SKILL.md` body enters the conversation as one message and stays.
  3. Supporting files (reference.md, scripts) load only when `SKILL.md` directs Claude to read them. Scripts can be run without loading their code into context.
- API-doc wording: "At startup, only the metadata (name and description) from all Skills is pre-loaded. Claude reads SKILL.md only when the Skill becomes relevant."
- Authoring limits on platform.claude.com: `name` up to 64 characters (lowercase, digits, hyphens); `description` up to 1,024 characters. The Claude Code page raises the listing cap to 1,536 for description plus `when_to_use`. Reconcile before quoting a number on the site.
- Sources:
  - https://code.claude.com/docs/en/skills
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Unconfirmed: the last ~20k characters of the Claude Code skills page were not read.

### Where skills live (Claude Code)
| Scope | Path |
|---|---|
| Personal (all projects) | `~/.claude/skills/<skill-name>/SKILL.md` |
| Project | `.claude/skills/<skill-name>/SKILL.md` (commit to share) |
| Nested | `<subdir>/.claude/skills/<skill-name>/SKILL.md` |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md`, invoked as `/plugin-name:skill-name` |
- Precedence for same-named skills: enterprise over personal, personal over project. Plugin skills are namespaced.
- The older `.claude/commands/*.md` still works; the docs prefer skills for new work.
- OpenCode also reads `.claude/skills` and `~/.claude/skills` as compatibility paths, plus `.opencode/skills`, `~/.config/opencode/skills` and `.agents/skills`. In OpenCode the model loads a skill by calling a `skill` tool. (https://opencode.ai/docs/skills/)

### How to confirm a skill loaded (Claude Code)
- `/skills` lists available skills.
- `/reload-skills` is needed if the top-level skills directory did not exist when the session started. Edits to existing skill files are picked up live.
- Invoke it directly with `/skill-name`, or ask something matching its description and watch whether Claude uses it.
- `/skill-doctor` shows what each skill costs and how often it is used. `/status` lists skills whose `allowed-tools` were ignored. `claude --debug` logs refused skill names (search for `[names]`).
- Eval route: a `tool_used: Skill` grader checks that the skill fired (see section 7).
- Unconfirmed: exact `/skills` UI layout (not described in the fetched text).

## 4. MCP (Model Context Protocol)
- "MCP (Model Context Protocol) is an open-source standard for connecting AI applications to external systems." AI applications can connect to data sources, tools and workflows. The docs compare it to "a USB-C port for AI applications."
- In Claude Code, MCP servers give Claude external tools. Tool definitions are deferred by default and loaded on demand via tool search, so only tool names and server instructions use context until a tool is used.
- Sources: https://modelcontextprotocol.io/docs/getting-started/intro and https://code.claude.com/docs/en/how-claude-code-works
- Unconfirmed: the MCP spec itself (architecture, transports) and the Claude Code `/mcp` page were not read.

## 5. Hook (Claude Code)
- Definition: "user-defined shell commands, HTTP endpoints, MCP tool calls, LLM prompts, or subagents that execute automatically at specific points in Claude Code's lifecycle." Claude Code passes JSON context about the event to the handler, which can optionally return a decision.
- Events (the page lists 33). Main groups:
  - Session: `SessionStart`, `SessionEnd`.
  - Turn: `UserPromptSubmit`, `Stop`.
  - Tool call: `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PostToolUseFailure`.
  - Subagent and task: `SubagentStart`, `SubagentStop`, `TaskCreated`, `TaskCompleted`.
  - Context: `InstructionsLoaded`, `PreCompact`, `PostCompact`.
  - Other: `Notification`, `WorktreeCreate`, `PreModelSwitch`, `Elicitation`, and more.
- Handler types: `command`, `http`, `mcp_tool`, `prompt`, `agent` (agent hooks are experimental).
- Deterministic vs LLM: the page does not use those words. By its descriptions, `command`, `http` and `mcp_tool` hooks are code-decided, while `prompt` and `agent` hooks have a model decide.
- Blocking: "Exit with code 2 to block the action." For example, a `PreToolUse` hook blocks the tool call and the stderr text becomes the reason. Exit 0 is success. Any other code (including 1) is a non-blocking error and the action proceeds. Exit 2 does not block everywhere: for `PostToolUse` the tool already ran, and for `Notification` the exit code is ignored.
- Hooks vs CLAUDE.md or skill text: the hooks docs fetched do not explicitly say "hooks are deterministic, instructions are advisory." The contrast is an inference from the exit-2 behaviour above. A `PreToolUse` command hook that exits 2 stops the action regardless of what the model wants; CLAUDE.md or skill text can only influence the model. Unconfirmed as an official phrase.
- Source: https://code.claude.com/docs/en/hooks (only the first 100k of ~293k characters were read).
- Unconfirmed: per-event decision JSON schemas, and the hooks-guide page.

## 6. Effort / reasoning effort / extended thinking

### Claude Code effort setting
- "Effort levels control adaptive reasoning": the model decides whether and how much to think on each step. "Lower effort is faster and cheaper for straightforward tasks, while higher effort provides deeper reasoning for complex problems."
- Levels: `low`, `medium`, `high`, `xhigh`, `max`. Opus 4.6 and Sonnet 4.6 lack `xhigh`. Defaults per the docs: `medium` on Opus 5.5, Sonnet 5.5, Haiku 5.5 and Fable 5.2; `xhigh` on Opus 4.7; `high` on others.
- Set with: `/effort` (slider, or `/effort high`), the `/model` picker, `claude --effort <level>`, env `CLAUDE_CODE_EFFORT_LEVEL`, settings `effortLevel`, or `effort` in skill or subagent frontmatter. `max` applies to the current session only unless set via the env var.
- The word `ultrathink` in a prompt asks for deeper reasoning for that turn.
- Thinking cannot be turned off on Opus 5.5, Sonnet 5.5, Haiku 5.5 or Fable. Lower the effort level instead.
- Source: https://code.claude.com/docs/en/model-config

### API effort
- Set `output_config.effort` on a Messages API request. The page says: "control how many tokens Claude spends when responding... trade off between response thoroughness and token efficiency."
- It affects all output tokens: text, tool calls and arguments, and thinking when active. Lower effort means fewer and terser tool calls.
- "Effort is a behavioral signal, not a strict token budget." At low effort Claude still thinks on hard problems, but less.
- The level scale is calibrated per model, so the same level name is not the same amount of thinking across models.
- Source: https://platform.claude.com/docs/en/build-with-claude/effort

### Extended thinking and `budget_tokens` (legacy)
- Manual extended thinking is `thinking: {type: "enabled", budget_tokens: N}`. The minimum is 1,024 and it must be below `max_tokens`. "The budget is a target rather than a strict cap"; `max_tokens` is the hard ceiling. Thinking tokens are billed as output tokens.
- This mode is deprecated. Claude 4.7 and later reject it with a 400 error. The replacement is adaptive thinking (`thinking: {type: "adaptive"}`) with `output_config.effort` setting depth.
- Source: https://platform.claude.com/docs/en/build-with-claude/extended-thinking

### What it trades
- Cost (more thinking and output tokens), latency (slower), and depth or verification. Claude Code docs: higher effort "tested more edge cases and verified more of its work"; lower effort "returned a starting point sooner."
- A model-config page statement says you are "charged for all thinking tokens generated." That is a summarizer paraphrase, so check the page before quoting it verbatim.

### Claims that more effort does NOT help (all from the docs)
- `max`: "may show diminishing returns and is prone to overthinking, so test before adopting it broadly." (Claude Code model-config)
- API, Fable 5.2: most of the capability gain is already present at `high`; above it, "gains are uneven and depend on the task." `max` "runs slower and costs more than at `xhigh`, often for only a small gain."
- API, Opus 4.7: on most workloads `max` adds significant cost for relatively small gains and "can lead to overthinking" on structured-output or less intelligence-sensitive tasks.
- Opus 5: effort controls thinking volume, not visible response length. "Changing effort does not reliably shorten responses", so prompt for length instead.
- Extended thinking: higher budgets give "diminishing returns that depend on the task", at the cost of latency.
- Anthropic's repeated advice: sweep effort on your own evals and step up only where measured gains exist.

## 7. Eval
- Anthropic's general guidance ("Define success criteria and build evaluations"): define success criteria, then design evals that measure against them. Criteria should be specific, measurable, achievable and relevant. Principles: task-specific, automate grading where possible, and prefer volume over hand-graded quality. For LLM-graded evals, use a different model from the one that produced the output. (https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)
- Skills (API docs, "Evaluation-driven development"): create evaluations before extensive documentation. The steps are:
  1. Run Claude on representative tasks without the skill and note failures.
  2. Build three scenarios that test those gaps.
  3. Measure the baseline without the skill.
  4. Write minimal instructions.
  5. Iterate against the baseline.
  - The checklist says "at least three evaluations" and testing with Haiku, Sonnet and Opus. The page notes that "there is not currently a built-in way to run these evaluations" (as of this fetch).
  - (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Claude Code `claude plugin eval`: runs a plugin against cases. Each case is a prompt plus graders, and a grader is a pass/fail check on what Claude produced. Grader types: `regex`, `tool_used`, `tool_order`, `file_exists`, `llm`, `baseline`.
- With vs without comparison: the case is run again with no plugin loaded, giving `WITH` and `W/OUT` scores. "Their difference, Δ, is what the plugin contributed. If a case scores 1.0 both with and without the plugin, the plugin isn't what made it pass." `tool_used: Skill` graders are reported but excluded from the score in both arms. The Δ is reported but never changes the exit code. (https://code.claude.com/docs/en/plugin-evals)
- The same page points to the skill-creator plugin for iterating on a single skill. It uses a different `evals/evals.json` format.
- Unconfirmed: whether Anthropic publishes numeric guidance for the number of runs per case. Only the plugin-evals page was grepped, not read in full.

## 8. Plugin
- Definition: "A Claude Code plugin is a directory of skills, agents, hooks, MCP servers, or other components that Claude Code installs and loads as one unit." Other components include LSP servers, output styles, workflows and themes.
- Manifest: `.claude-plugin/plugin.json`. It is optional; without it Claude Code loads components from the standard layout. When present, `name` is the only required field. Optional fields: `version`, `description`, `author`, and component paths such as `skills`, `hooks`, `mcpServers`.
- Standard layout: `skills/<name>/SKILL.md`, `agents/*.md`, `hooks/hooks.json`, `.mcp.json`, `.lsp.json`, `commands/`. Component files go at the plugin root, not inside `.claude-plugin/`.
- Plugin components are namespaced by plugin name (for example `deploy-tools:reviewer`, `/plugin-name:skill-name`).
- Plugin names starting with `claude-` or `anthropic-` (and similar) are reserved. `claude plugin validate` errors on them.
- Install: `/plugin` (Discover tab), or `claude plugin ...` in the shell. Marketplaces are catalogs defined by `.claude-plugin/marketplace.json`. A local folder can be loaded with `--plugin-dir`. Validate with `claude plugin validate`.
- Context cost: an enabled plugin's skill and agent names and descriptions sit in context every turn; full text loads only on use.
- A plugin is not required. Skills, subagents, hooks and MCP all work standalone; use a plugin to package and distribute several together.
- Sources: https://code.claude.com/docs/en/plugins and https://code.claude.com/docs/en/plugins/manifest-reference
- Unconfirmed: `/plugin` Stats tab behaviour beyond what the skills page said.

## Overall unconfirmed list
- "Same model, different harness gives different results" as an official claim.
- Hooks "deterministic vs advisory" as official wording.
- OpenCode tool, permission and loop internals (and whether Claude subscription logins work there).
- Exact `/skills` UI layout.
- Full contents of the hooks, skills and model-config pages past 100k characters.
