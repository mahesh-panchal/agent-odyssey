# Tools and guards: MCP and hooks (Claude Code), OpenCode equivalents

Checked 2026-11-16. Official docs only. Pages fetched via a summarising fetch tool (quotes as returned; long pages read in chunks, saved locally and grepped). No model-calling commands were run.
Base: C = https://code.claude.com/docs/en/ ; O = https://opencode.ai/docs/
Note: the OpenCode docs now describe "V2" (docker tag 2.0.0, `/v2/install`). V1 key names differ (see section A4). Verify against the user's installed version.

## A1. MCP in Claude Code: adding servers
- CONFIRMED: HTTP (recommended): `claude mcp add --transport http <name> <url>`. C mcp
- CONFIRMED: SSE is deprecated: "The SSE (Server-Sent Events) transport is deprecated. Use HTTP servers instead, where available." `claude mcp add --transport sse <name> <url>`. C mcp
- CONFIRMED: stdio: `claude mcp add [options] <name> -- <command> [args...]`. "Everything after `--` is passed to the server untouched." Flags: `-s/--scope`, `-e/--env KEY=value`, `-t/--transport`, `-H/--header`. C mcp
- CONFIRMED: project file `.mcp.json` at the project root:
  `{ "mcpServers": { "shared-server": { "type": "http", "url": "https://example.com/mcp" } } }` C mcp
- UNCONFIRMED: exact `.mcp.json` shape for a stdio server (`command`/`args`/`env` keys not seen in the fetched text). Check C mcp before putting it in a quest.
- CONFIRMED: `/mcp` inside a session lists servers and tools (page refers to running `/mcp`). C mcp

## A2. Scopes and the approval prompt
- CONFIRMED scopes: Local (default; current project only; not shared; stored in `~/.claude.json`), Project (shared via version control; `.mcp.json` in project root), User (all your projects; `~/.claude.json`). C mcp
- CONFIRMED: "Local scope is the default."
- CONFIRMED: "For security reasons, Claude Code prompts for approval in interactive sessions before using project-scoped servers from `.mcp.json` files. To reset those approval choices, run `claude mcp reset-project-choices`." C mcp
- CONFIRMED: in `claude -p` and Agent SDK runs "Claude Code can't show that prompt: it loads project-scoped servers without asking." Mitigations named: `disabledMcpjsonServers`, `--setting-sources`/`settingSources`, `--strict-mcp-config`. C mcp
- Teaching point: a cloned repo's `.mcp.json` is code that wants to run on your machine; the approval prompt is the gate, and headless mode has no gate.

## A3. MCP permissions in Claude Code settings
- CONFIRMED naming: `mcp__<server>__<tool>`. "To match every tool from an MCP server, write `mcp__<server>__*`. To match one tool, write its full name." C permissions
- CONFIRMED examples: `mcp__puppeteer` (any tool of the server), `mcp__puppeteer__*`, `mcp__puppeteer__puppeteer_navigate` (one tool). C permissions
- CONFIRMED: characters such as `.` or spaces in server names become `_` (`my.server` -> `mcp__my_server__*`). C permissions
- CONFIRMED: allow-rule globs only after a literal `mcp__<server>__` prefix; "An unanchored allow glob such as `"*"`, `"B*"`, or `"mcp__*"` is skipped and doesn't auto-approve anything." Deny/ask accept `"mcp__*"` (every MCP tool, all servers). C permissions
- CONFIRMED: parameter matching: "When Claude Code loads a settings file, it skips any `mcp__` rule that has parentheses." Parameter-level deny for MCP only via `--disallowedTools`. C permissions
- CONFIRMED: deny and ask rules are evaluated even when a hook returns allow (hooks page). C hooks
- Minimal settings sketch (shape from the `permissions` page; check that page for `allow`/`deny` array syntax before quoting): `"permissions": { "allow": ["mcp__github__get_*"], "deny": ["mcp__github__delete_*"] }`. The `allow`/`deny` key names are UNCONFIRMED in the text fetched for this note.

## A4. What a server can do, injection, guidance
- CONFIRMED capabilities listed: implement features from issue trackers, analyze monitoring data, query databases, integrate designs, automate workflows, react to external events. C mcp
- CONFIRMED security warning (the only one found): "Verify you trust each server before connecting it. Servers that fetch external content can expose you to prompt injection risk." C mcp
- UNCONFIRMED: any longer docs passage on injection via tool results (page text read in full except possibly a few chunks; nothing else found). Do not attribute more to the docs than the sentence above.
- UNCONFIRMED as docs wording: "a stdio server runs code on your machine with your credentials". The docs show stdio servers are commands Claude Code launches (`-- <command>`), and `-e KEY=value` passes secrets to them; the credentials statement is inference, label it so.
- CONFIRMED org controls exist: `allowedMcpServers`/`deniedMcpServers`, `managed-mcp.json`. C mcp, C managed-mcp (linked)
- CONFIRMED: sandboxing note, "sandbox restrictions still apply even if a prompt injection bypasses Claude's decision-making" (use sandbox plus permissions). C permissions

## A5. MCP in OpenCode (V2 docs)
- CONFIRMED (V2): servers go "under `mcp.servers`"; "V2 does not place server names directly under `mcp`." O mcp-servers
- CONFIRMED local shape: `"type": "local"`, `"command": ["npx","-y","example-mcp-server"]`, `"environment": {...}`, `"cwd": "."`. O mcp-servers
- CONFIRMED remote shape: `"type": "remote"`, `"url"`, `"headers": { "Authorization": "Bearer {env:MCP_API_KEY}" }`, `"oauth": false`. O mcp-servers
- CONFIRMED: disable via `"disabled": true` (no `enabled` field documented in V2). O mcp-servers
- CONFIRMED: "MCP tools consume model context, so add only the servers you need." O mcp-servers
- CONFIRMED permissions: rules are an ordered array `"permissions": [ { "action", "resource", "effect" } ]`, effect `allow|ask|deny`; last matching rule wins; no match means `ask`. MCP tool action is `<server>_<tool>` with resource `*` (unsupported chars become `_`); example `{ "action": "context7_*", "resource": "*", "effect": "deny" }`. O permissions, O mcp-servers
- CONFIRMED: V2 names are `permissions`/`shell`/`subagent`, replacing V1 `permission`/`bash`/`task`. O permissions
- UNCONFIRMED: V1 `mcp` key shape (V1 docs not fetched).

## B1. Hooks in Claude Code: where and how
- CONFIRMED locations: `~/.claude/settings.json` (all projects), `.claude/settings.json` (project, committable), `.claude/settings.local.json` (project, not shared), managed policy settings, plugin `hooks/hooks.json`; skill/subagent frontmatter also define hooks. C hooks
- CONFIRMED: "To create a hook, add a `hooks` block to a settings file." C hooks-guide
- CONFIRMED matcher syntax: only letters, digits, `_`, `-`, spaces, `,`, `|` means exact string or list; any other character means a JavaScript regex, unanchored. `Edit|Write` is a list; `^Notebook` is a regex. C hooks
- CONFIRMED MCP matching: `mcp__<server>__<tool>`; "The `.*` is required: a matcher like `mcp__memory` ... is compared as an exact string and matches no tool." Use `mcp__memory__.*`. C hooks
- CONFIRMED input: JSON on stdin with `session_id`, `cwd`, `permission_mode`, `hook_event_name`, `tool_name`, `tool_input` (Bash: `tool_input.command`), `tool_use_id`. C hooks

## B2. Minimal blocking PreToolUse hook
Config (`.claude/settings.json`; shape from the hooks docs example, `matcher: "Bash"`, command path via `$CLAUDE_PROJECT_DIR`):
```json
{ "hooks": { "PreToolUse": [ { "matcher": "Bash",
  "hooks": [ { "type": "command",
    "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-drop-table.sh" } ] } ] } }
```
Script (verbatim from C hooks-guide, "Hook output"), `chmod +x` needed (UNCONFIRMED in docs text read; standard for executables):
```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')
if echo "$COMMAND" | grep -q "drop table"; then
  echo "Blocked: dropping tables is not allowed" >&2  # stderr becomes Claude's feedback
  exit 2                                               # exit 2 = block the action
fi
exit 0  # exit 0 = no decision; the normal permission flow applies
```
- CONFIRMED: exit 2 on PreToolUse "Blocks the tool call"; "Claude sees the stderr message as the denial reason." C hooks
- CONFIRMED: exit 0 does not approve: "the tool call still goes through the normal permission flow". C hooks-guide
- CONFIRMED: any other exit code with no valid JSON: "the action proceeds on most events" (a hook that crashes fails open), unless the hook is configured to block on failure (`onFailure: "block"`). C hooks-guide
- CONFIRMED JSON alternative: exit 0 and print to stdout:
  `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Destructive command blocked by hook"}}`. Values `allow|deny|ask|defer`. "Choose one approach per hook" (exit 2 or JSON, not both). C hooks, C hooks-guide
- CONFIRMED: precedence across hooks `deny` > `defer` > `ask` > `allow`; all matching hooks run to completion (a deny does not stop a sibling hook's side effects). `"allow"` skips the prompt but "Deny and ask rules are still evaluated regardless of what the hook returns". C hooks

## B3. PostToolUse
- CONFIRMED: exit 2 on PostToolUse "Shows stderr to Claude; the tool already ran". Cannot block. C hooks
- CONFIRMED example: matcher `Edit|Write`, command `f=$(jq -r '.tool_input.file_path') && npx prettier --write --ignore-unknown "$f"`. C hooks-guide
- CONFIRMED: `updatedToolOutput` "only changes what Claude sees. The tool has already run by the time the hook fires, so any files written, commands executed, or network requests sent have already taken effect." C hooks

## B4. Trust and limits
- CONFIRMED: "Command hooks execute shell commands with your full user permissions. They can modify, delete, or access any files your user account can access. Review and test all hook commands before adding them to your configuration." C hooks (Security considerations)
- CONFIRMED: interactive sessions hold back hooks from every settings file until you accept the workspace trust dialog. In `-p`/SDK sessions "Claude Code never shows the dialog and treats the folder as trusted, so hooks committed in a repository's `.claude/settings.json` run in a folder you've never trusted." Advice: review `.claude/` first, use `--bare`, or `--settings '{"disableAllHooks": true}'`. C hooks
- CONFIRMED: best practices: validate inputs, quote variables, block `..` path traversal, absolute paths, skip `.env`/`.git`/keys. C hooks
- CONFIRMED limits: PreToolUse fires only when Claude calls a tool; `@`-referenced files in a prompt are added without a tool call so no hook (even `Read`) fires; none for `EndConversation`. Setup hooks cannot block. `UserPromptSubmit` cannot replace the prompt. C hooks
- CONFIRMED: a matcher is a filter on tool name, not on content: a grep on `tool_input.command` sees only the literal string (our inference: it will miss `rm` hidden in a script the command runs; label as inference when teaching).
- UNCONFIRMED: statement that a Bash-pattern hook can be evaded by obfuscation; not in the docs text read.

## B5. OpenCode equivalent
- CONFIRMED (V2): plugins add "tools, hooks, integrations, commands, agents". O plugins, O build/plugins
- CONFIRMED locations: `.opencode/plugins/` (project) and `~/.config/opencode/plugins/` (global); direct `.ts`/`.js` files load. "A `plugins/` directory beside a project-root `opencode.json(c)` is not discovered automatically." O plugins
- CONFIRMED (V2 docs, build/plugins/server): tool hook
  `await ctx.tool.hook("execute.before", (event) => { if (event.tool === "read") console.log(event.input) })`; "the hook receives the call and can inspect or change its input". V1 key was `"tool.execute.before"`. After: `ctx.tool.hook("execute.after", ...)`. O build/plugins/server
- CONFIRMED: permission hook `ctx.permission.hook("evaluate", ...)`; "Hooks run for `allow` and `ask` decisions."; "An explicit configured `deny` is final and does not invoke the hook."; "A hook may change `effect` to `allow`, `ask`, or `deny`."; `event.message` is the denial reason. O build/plugins/server
- CONFIRMED: "The docs don't describe throwing from a tool hook to block a call" (summariser's statement); documented deny route is the permission `evaluate` hook. UNCONFIRMED: whether throwing in `execute.before` blocks (V1 community pattern, not in fetched docs).
- UNCONFIRMED: a trust/security statement for plugins (none found). Treat plugins as code running with your privileges (inference, same as Claude hooks).
- CONFIRMED: two built-in policy plugins "ignore removals so that a repository cannot switch off" policy. O plugins
- UNCONFIRMED: a direct exit-code-2 equivalent; OpenCode has no shell-hook config documented in pages read.
