# Plan mode: Claude Code and OpenCode

Checked 2026-11-16. Official docs only. Fetched through a summarising fetch tool (wording is the tool's paraphrase, not verbatim).
Base: C = https://code.claude.com/docs/en/ ; O = https://opencode.ai/docs/
Not repeated: entry basics already in forest-and-reef.md s5, kennel-and-crypt.md (mode table), session-management.md (plan re-injected after compaction, Explore/Plan one-shot). Only additions below.
Caveat: C permission-modes was read to char 100000 of 120324; the last ~20k chars were not read.

## 1. Entering plan mode (C permission-modes)
- CONFIRMED: three entries: `Shift+Tab` mid-session, `/plan` before a prompt, `claude --permission-mode plan`. Default: `defaultMode: plan` in project `.claude/settings.json`.
- CONFIRMED: VS Code ignores project settings for the starting mode; use `claudeCode.initialPermissionMode: plan` in VS Code user settings.
- CONFIRMED: to leave plan mode with no prompt open, press `Shift+Tab` again. At the approval prompt press `Esc` first, because `Shift+Tab` there APPROVES the plan. (Teaching trap.)
- CONFIRMED: status bar shows `⏸ plan mode on`. C common-workflows#plan-before-editing

## 2. Tools in plan mode
- CONFIRMED: reads allowed; Claude may run shell commands to explore. Which shell commands run unprompted depends on the session (first match wins):
  1. Interactive terminal with bypass permissions available: no classifier, no prompt for planning commands.
  2. Auto mode available and `useAutoModeDuringPlan` on (default): the auto-mode classifier reviews shell commands, except critical-path removals.
  3. Otherwise: commands outside the built-in read-only set prompt, even with sandbox auto-allow.
- CONFIRMED: plan files are an exception to the `.claude/` protected-directory rule, so they can be written in plan mode.
- Source: C permission-modes

## 3. Presentation, approval, editing, storage
- CONFIRMED: when ready, Claude presents the plan and asks how to proceed. Options (exact labels):
  - `Yes, and use auto mode` (reads `Yes, auto-accept edits` if auto mode is unavailable; reads `Yes, and switch to BYPASS PERMISSIONS (no further prompts) for this session` if the session started with bypass).
  - `Yes, manually approve edits`.
  - `No, keep planning` (you say what to change).
- CONFIRMED: setting `showClearContextOnPlanAccept` adds a first option that approves and clears the planning context. The page does not give its label. Off by default is NOT stated; treat default as UNCONFIRMED.
- CONFIRMED: approving exits plan mode and switches to the mode of the chosen option. To plan again, `Shift+Tab` or `/plan`.
- CONFIRMED: `Ctrl+G` opens the proposed plan in the default text editor to edit before Claude proceeds.
- CONFIRMED: plan files live in `~/.claude/plans/` by default; `plansDirectory` setting changes it.
- UNCONFIRMED: whether plan context is kept when you pick a non-clear option (page says only that the clear option clears it; keeping is implied, not stated).
- CONFIRMED: accepting a plan gives the session a title based on the plan, unless already named.

## 4. When to plan, when to skip, reviewing the plan
- UNCONFIRMED: any "skip planning if the diff fits in one sentence" wording. grep of C best-practices (fetched 2026-11-16) found no "plan mode", no "ExitPlanMode", no such sentence. Do not cite it.
- CONFIRMED (adjacent): best-practices recommends brainstorming before building: prompt Claude to interview you "until you could write the spec", write `SPEC.md`, then start a FRESH session to build from it (clean context, written definition of done). This is the page's plan-first pattern, not plan mode. C best-practices#brainstorm-with-claude-first
- CONFIRMED: review against the plan: use a subagent to review the diff against `SPEC.md` (requirements implemented, edge cases tested). `/code-review` reviews the diff in a fresh subagent that never saw your conversation. C best-practices
- CONFIRMED: common-workflows says use plan mode "for changes you want to review before they touch disk". That is the only official when-to-plan line found. C common-workflows#plan-before-editing
- CONFIRMED: best-practices says a vague prompt is "completely fine" when exploring, at the cost of more correction.

## 5. Limits (C permission-modes)
- CONFIRMED: in an interactive terminal session with bypass permissions available, Claude is only INSTRUCTED to plan without editing; Claude Code does not enforce it, and edits or shell commands run without a prompt. Explicit `ask` rules and critical-path `rm`/`rmdir` still prompt.
- CONFIRMED: `-p` (non-interactive), Agent SDK and VS Code chat panel keep plan mode's blocks even with bypass available.
- CONFIRMED: deny rules block in every mode. Hooks and mods can approve some calls (details on the permissions page, not read).
- UNCONFIRMED: MCP tools in plan mode. The page does not describe MCP-specific behaviour.
- UNCONFIRMED: side effects of read-only shell commands. Not discussed; teach as an inference only ("read-only set" is not a guarantee against everything).

## 6. Related: Plan subagent, /rewind
- CONFIRMED: built-in `Plan` subagent is a read-only research agent that Claude uses in plan mode to gather codebase context; Write and Edit denied; own context window, so the main thread stays read-only. Inherits parent model; starts WITHOUT CLAUDE.md files and git status snapshot; one-shot, no agent ID, cannot be resumed. Explore is the same but for search. C sub-agents
- CONFIRMED: `/rewind` (aliases `/undo`, `/checkpoint`; or `Esc` `Esc` on empty prompt) tracks Claude's file-edit-tool changes only. Bash-made changes to a file never edited by Claude are not tracked; subagent edits usually not restored; keep Git. Menu actions: Restore code and conversation / Restore conversation / Restore code / Summarize from here / Summarize up to here / Never mind. C checkpointing
- UNCONFIRMED: whether /rewind covers plan files in `~/.claude/plans/`. Not stated.

## 7. OpenCode
- CONFIRMED: built-in primary agents `build` (default, full tools; reading `.env` files asks) and `plan` ("explores and plans without editing normal project files"; can write OpenCode plan files when asked; shell stays under permission control). Subagents `general` (cannot launch subagents) and `explore` (read-only). O agents
- CONFIRMED: `plan` agent: cannot edit files except under the plan directory `~/.opencode/plan`; edit restriction is a `deny`, saved approvals never override a deny. Base policy for every agent is allow-all plus ask on `*.env`/`*.env.*`. O permissions
- CONFIRMED: disable plan with `{"agents": {"plan": {"disabled": true}}}`; `default_agent` picks the primary agent; falls back to `build`. O agents
- UNCONFIRMED: how to switch between build and plan. Neither agents nor tui page mentions a Tab key or `agent_cycle` keybind (tui page does not mention plan at all). Do not state "press Tab".
- UNCONFIRMED: full default denies of `plan` beyond edit, and any plan approval step. permissions page: no plan-specific approval; `ask` rules answer `once`, `always`, `reject`. Plan is not a gate that "hands over" to build.
- CONFIRMED: TUI slash commands (no /plan): /connect /compact(/summarize) /editor /exit /export /help /init /models /new(/clear) /redo /sessions(/resume,/continue) /themes /thinking /undo /update. `/undo` removes last message and its file changes, needs Git. O tui

## 8. Names documented vs not
- Documented (Claude Code): `claude --permission-mode plan`, `/plan [prompt]`, `Shift+Tab`, `Ctrl+G`, `defaultMode: plan`, `useAutoModeDuringPlan`, `showClearContextOnPlanAccept`, `plansDirectory`, `~/.claude/plans/`, `claudeCode.initialPermissionMode`, `Plan` subagent, `/rewind`, `/undo`, `/code-review`.
- Not documented / not found: a `--plan` flag, an "exit plan mode" slash command (only `Shift+Tab`), the tool name `ExitPlanMode` on the pages read, a plan "edit" option in the approval list (editing is `Ctrl+G`), a plan file name pattern, plan-mode MCP rules.
- OpenCode documented: `build`, `plan`, `general`, `explore`, `default_agent`, `agents.plan.disabled`, `~/.opencode/plan`. Not documented: `/plan` command, Tab switching, a plan approval flow.
