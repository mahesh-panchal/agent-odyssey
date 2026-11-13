# Forest and Reef: Claude Code and OpenCode facts

Question: what do official docs say about instruction files, skills, context management, plan mode and subagents in Claude Code and OpenCode?
Decision it feeds: accuracy of the "Forest" and "Reef" zone content in Agent Odyssey.

Read on 2026-11-13. Local `claude --version`: 2.1.323. The doc pages show no "last updated" date; the version read is "live site as of 2026-11-13". OpenCode version was not recorded and its GitHub repo was NOT read (docs site only). OpenCode docs describe some V2 behaviour ("accepted in V2"), so verify against the installed version.
Note: the fetch tool summarises pages with a small model; quotes marked "..." are as returned, long pages (skills, sub-agents, permission-modes) had their last ~15% unread.

## 1. Claude Code: CLAUDE.md  (source: https://code.claude.com/docs/en/memory)

- CONFIRMED User file: `~/.claude/CLAUDE.md` (personal, all projects).
- CONFIRMED Project file: `./CLAUDE.md` or `./.claude/CLAUDE.md` (team-shared via source control).
- CONFIRMED Local file: `./CLAUDE.local.md`, personal per-project, add to `.gitignore`.
- CONFIRMED Org-wide managed CLAUDE.md also exists (same page, "Deploy organization-wide").
- CONFIRMED Loading: CLAUDE.md and CLAUDE.local.md in the working directory and every directory above it load at launch; all are concatenated (not overriding), ordered root-down so the closest is read last.
- CONFIRMED Subdirectory CLAUDE.md files load on demand, once Claude reads/writes/edits a file in that subdirectory.
- CONFIRMED Imports: `@path/to/import` syntax; imported files are expanded into context with the importing file. Import parsing skips code spans/fenced blocks (wrap `@README` in backticks to keep literal). Imports "don't reduce its context cost". Imports outside the working directory prompt for approval.
- CONFIRMED `/init`: "Run `/init` to generate a starting CLAUDE.md automatically"; it analyses the codebase (build commands, test instructions, conventions); if one exists it suggests improvements instead of overwriting. `CLAUDE_CODE_NEW_INIT=1` gives an interactive multi-phase flow.
- CONFIRMED `/memory`: lists CLAUDE.md, CLAUDE.local.md and memory file locations, toggles auto memory, opens files in editor.
- CONFIRMED Size guidance: "target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence." Use `.claude/rules/` (with `paths:` frontmatter) for part-of-codebase rules. A file over 4 MiB is skipped.
- CONFIRMED Advisory, not enforced: "Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead." Best-practices page (https://code.claude.com/docs/en/best-practices) agrees: "`CLAUDE.md` is for guidelines, and Claude is allowed to decide a guideline doesn't apply"; things that must always happen belong in hooks, deny rules or managed settings.
- CONFIRMED Best-practices test for what to write: "Could it find this by reading the code? Would it actually go and look? If both are yes, leave it out." Also `/context all` confirms the file loaded; `/doctor prompt-audit` audits instruction files.
- CONFIRMED AGENTS.md: Claude Code reads `AGENTS.md` only when no CLAUDE.md/CLAUDE.local.md exists in the working directory or above (default `claude-md-or-agents-md`); otherwise CLAUDE.md only.
- CONFIRMED Auto memory (separate from CLAUDE.md): Claude-written notes at `~/.claude/projects/<project>/memory/`; first 200 lines or 25KB of MEMORY.md load each session.

## 2. Claude Code: Skills  (source: https://code.claude.com/docs/en/skills)

- CONFIRMED Layout: a directory with required `SKILL.md` plus optional files. Locations: personal `~/.claude/skills/<name>/SKILL.md`; project `.claude/skills/<name>/SKILL.md`; nested `<subdir>/.claude/skills/...`; plugin `<plugin>/skills/<name>/SKILL.md`; enterprise via managed settings; `--add-dir` directories.
- CONFIRMED Frontmatter: "All fields are optional. Only `description` is recommended so Claude knows when to use the skill." `name` defaults to the directory name. Other fields: `when_to_use`, `allowed-tools`, `disallowed-tools`, `disable-model-invocation`, `user-invocable`, `arguments`, `argument-hint`, `context`/`agent` (fork to subagent), `model`, `effort`, `hooks`, `paths`, `shell`. description+when_to_use truncated at 1,536 chars in the listing.
- CONFIRMED Invocation: default = both user (`/name`) and Claude (automatic, by matching `description`). `disable-model-invocation: true` = user only; `user-invocable: false` = Claude only.
- CONFIRMED Progressive loading: "in a regular session, skill descriptions are loaded into context so Claude knows what's available, but full skill content only loads when invoked"; body then stays in context. Recommended `SKILL.md` under 500 lines.
- CONFIRMED Bundling: supporting files (reference.md, examples.md, `scripts/helper.py`) allowed; scripts are "executed, not loaded"; reference with `${CLAUDE_SKILL_DIR}`.
- CONFIRMED `allowed-tools`: tools Claude may use without asking permission during the turn that invokes the skill; it "does not restrict which tools are available".
- CONFIRMED Custom commands merged into skills: `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` both create `/deploy`; commands are "the older format and still works"; "Prefer a skill for new work."
- CONFIRMED Open standard note: the page links the Agent Skills spec (https://agentskills.io) which accepts `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`.
- CONFIRMED Skill bodies survive compaction, capped 5,000 tokens/skill, 25,000 total (https://code.claude.com/docs/en/context-window).

## 3. OpenCode  (sources: https://opencode.ai/docs/rules/, /skills/, /agents/, /config/, /tui/, /commands/)

- CONFIRMED AGENTS.md: project root `AGENTS.md` (applies to that directory and subdirectories); global `~/.config/opencode/AGENTS.md`.
- CONFIRMED `/init`: "Guided setup for creating or updating `AGENTS.md`" (tui page); scans repo, may ask questions; improves an existing file in place (rules page).
- CONFIRMED Extra instructions: `instructions` array in `opencode.json` (project) or `~/.config/opencode/opencode.json`; globs and remote URLs (5 s timeout) supported; loaded alongside AGENTS.md.
- CONFIRMED Claude Code compatibility: falls back to project `CLAUDE.md` if no `AGENTS.md`, and to `~/.claude/CLAUDE.md` if no global AGENTS.md; first match wins per category (AGENTS.md beats CLAUDE.md). Env variables can disable the fallbacks (names not captured; see rules page).
- CONFIRMED Skills locations: global `~/.config/opencode/skills`, plus `~/.claude/skills` and `~/.agents/skills`; project `.opencode/skills`, plus `.claude/skills` and `.agents/skills`; extra dirs/HTTP catalogs via `skills` array in config. Directory name is plural `skills` (not `.opencode/skill`).
- CONFIRMED Skill format: file named `SKILL.md`; the file path determines the skill ID, frontmatter `name` is only a display label; skills without `description` are not advertised; `disable-model-invocation: true` or `metadata.opencode/autoinvoke: false` hides from model.
- CONFIRMED Skill loading: model sees ID/name/description list, then calls the `skill` tool to load the body (plus base dir and up to ten supporting file paths); supporting files read only when the skill directs. Permissions via `skill` rules allow/ask/deny; user can mention `@skill-id`.
- CONFIRMED Custom agents: Markdown files in `~/.config/opencode/agents/<name>.md` or `.opencode/agents/<name>.md` (frontmatter `description`, `mode`, `permissions`; body = system prompt), or `agents` key in `opencode.jsonc`. Built-in primary agents `build` and `plan`; subagents `general` and `explore`.
- CONFIRMED Custom commands exist: `.opencode/commands/*.md` (commands page).

## 4. Context windows

Claude Code (https://code.claude.com/docs/en/context-window, best-practices):
- CONFIRMED Context window holds "your instructions, the files it reads, its own responses, and content that never appears in your terminal". Before you type: CLAUDE.md, auto memory, MCP tool names and skill descriptions load.
- CONFIRMED `/compact` "replaces the conversation with a structured summary"; accepts focus text (`/compact focus on the auth bug fix`). Project-root CLAUDE.md, auto memory, plan-mode plan re-injected from disk; nested CLAUDE.md and `paths:` rules reload on demand; up to five recently touched files re-read.
- CONFIRMED Auto-compaction: "Claude Code compacts automatically as you approach the limit, so a full context window doesn't end your session." Threshold configurable (`/autocompact 500k`); per-model defaults on model-config page (not read).
- CONFIRMED `/clear`: use between unrelated tasks; "Old conversation crowds out the files you need next and costs tokens on every message." `/clear <name>` names the session left; `--resume` returns to it.
- CONFIRMED `/context`: "live breakdown by category with optimization suggestions, including which CLAUDE.md and auto memory files loaded".
- CONFIRMED `/rewind` (or Esc Esc): roll back code/conversation, or "Summarize from here".
- CONFIRMED Degradation, as stated by docs: a longer CLAUDE.md "reduce[s] adherence"; after two failed corrections, "a third correction mostly adds to a conversation that already contains two failed attempts for Claude to keep re-reading", so `/clear` and re-prompt; "a focused context gets you better answers and costs less". The docs do NOT give a mechanism (e.g. attention dilution) beyond this.
- CONFIRMED Window size: best-practices says "Most current models have a 1M-token window and compaction happens on its own, so running out is rare" and lists "manage context aggressively" as an outdated tip, while `/clear` between tasks is still worth doing.

OpenCode (https://opencode.ai/docs/tui/, /config/):
- CONFIRMED `/compact` (alias `/summarize`): "Compact the current session." `/new` (alias `/clear`): "Start a new session." `/undo` and `/redo` need Git. `/sessions` (aliases `/resume`, `/continue`) switches sessions.
- CONFIRMED Config `compaction`: `auto` on/off, `keep.tokens` (recent context kept), `buffer` (share of context window kept free before auto-compaction starts). "Automatic compaction uses the selected model's usable input budget."
- UNCONFIRMED OpenCode has no `/context` equivalent in the TUI doc fetched (not listed); `prune`/`reserved` options (from older versions) not on config page.
- UNCONFIRMED OpenCode docs' stated reason why long sessions degrade; none found.

## 5. Plan mode and workflow  (https://code.claude.com/docs/en/permission-modes, best-practices)

- CONFIRMED Plan mode: "tells Claude to research and propose changes without making them. Claude reads files, runs shell commands to explore, and writes a plan, but does not edit your source." Enter with Shift+Tab, `/plan <prompt>`, or `claude --permission-mode plan`; default via `defaultMode: plan`. Ctrl+G opens plan in editor. On approval choose auto mode or manual edit approval, or keep planning.
- CONFIRMED Page's use-case summary: "Explore before changing anything | `claude --permission-mode plan` | Claude Code blocks edits until you approve a plan."
- UNCONFIRMED A named four-phase "explore, plan, implement, commit" recipe in the current best-practices page. The 2026-11-13 page text does not contain it (grep for "plan mode" found none); the workflow is implied by plan mode only. The previous version of that recipe is from memory and must not be cited.
- CONFIRMED Verification: best-practices lists a check Claude can run: in the prompt ("run the auth tests after, and keep going until they pass"), `/goal <condition>`, `/code-review` (fresh subagent). "ask Claude for *evidence*: the command it ran and its output... 'All tests pass' on its own tells you very little." "the single most useful line in your CLAUDE.md is the command that runs [the test suite]."
- CONFIRMED Specific prompts: "If you name the file, describe the symptom, and say what 'fixed' looks like up front, you usually save yourself a round of corrections later." Example: replace "fix the login bug" with "users report login fails after the session times out. look at token refresh in src/auth/, write a failing test that reproduces it, then fix it". Vague prompts are fine for open exploration.
- CONFIRMED Course correction: Esc to interrupt; after two failed corrections `/clear` and rewrite the prompt.
- OpenCode: CONFIRMED `plan` primary agent "explores and plans without editing normal project files" (agents page). No OpenCode best-practices page was read.

## 6. Subagents

Claude Code (https://code.claude.com/docs/en/sub-agents): "Subagents are specialized AI assistants that handle specific types of tasks." Each "runs in its own context window with a custom system prompt, specific tool access, and independent permissions." Use one when a side task "would flood your main conversation with search results, logs, or file contents you won't reference again: the subagent does that work in its own context and returns only the summary." A non-fork subagent does not see the conversation history, invoked skills or files already read. Defined as Markdown with YAML frontmatter (`name`, `description` required) in `.claude/agents/` or `~/.claude/agents/`. Cost caveat (best-practices): each subagent spends its own tokens and can be slower than doing it inline; a fresh reviewer helps because it has not seen your reasoning, but delegating does not itself improve the answer. CONFIRMED.

OpenCode (https://opencode.ai/docs/agents/): subagents "run with fresh context in their own child sessions", launched via the `subagent` tool; they run in the background and the parent receives a report when the child goes idle. Built-ins: `general` (broad tools, cannot launch more subagents) and `explore` (read-only search). CONFIRMED.

## Tested

- `claude --version` -> 2.1.323 (Claude Code). No commands run against OpenCode.

## Unconfirmed / not checked

- OpenCode GitHub repo and installed version not read; the docs mention V2, so some behaviour may differ per version.
- Names of the OpenCode env vars that disable Claude compatibility.
- Per-model default auto-compact thresholds (model-config page not read).
- Final ~15% of the skills, sub-agents and permission-modes pages was not read by the fetch tool.
- Explicit explore-plan-code recipe in current Claude Code best-practices (see section 5).
- Official mechanism for why long sessions degrade (only the statements above exist).
