# Meet the Guilds: Skill, MCP server, hook (overview)

Checked 2026-11-28. Official docs fetched directly with curl and searched in the page text. No model-calling commands were run. C = https://code.claude.com/docs/en/ ; O = https://opencode.ai/docs/

## Claude Code
- CONFIRMED: `/skills` "List available skills" (commands page: https://code.claude.com/docs/en/commands).
- CONFIRMED: `/mcp [reconnect|enable|disable ...]` manages MCP server connections; with no argument it opens the interactive list (https://code.claude.com/docs/en/commands).
- CONFIRMED: `/hooks` "View hook configurations" (https://code.claude.com/docs/en/commands).
- CONFIRMED: `claude mcp list` lists servers and shows a health status next to each (https://code.claude.com/docs/en/mcp).
- CONFIRMED: "Hooks are user-defined shell commands, HTTP endpoints, MCP tool calls, LLM prompts, or subagents that execute automatically at specific points in Claude Code's lifecycle." `PreToolUse` runs before a tool call executes (https://code.claude.com/docs/en/hooks).
- CONFIRMED: exit code 2 blocks the tool call; exit 0 with no output is "no decision" and the normal permission flow runs; any other exit code is a non-blocking error and execution continues (https://code.claude.com/docs/en/hooks).
- CONFIRMED from earlier research (research/terminology.md, research/forge.md): a Skill is a folder with `SKILL.md`; only name and description load at session start, the body loads on use (https://code.claude.com/docs/en/skills, https://agentskills.io).
- CONFIRMED from earlier research (research/tools-and-guards.md): a stdio MCP server is a command the harness launches locally, so treat it as installed software; fetched content can carry prompt injection (https://code.claude.com/docs/en/mcp).

## OpenCode
- CONFIRMED: `opencode mcp add <name> --url <url>` and `opencode mcp list` (https://opencode.ai/docs/mcp-servers/). The page also says to use `/mcps` in OpenCode to view, connect, disconnect or authenticate servers.
- CONFIRMED: skills load through a `skill` tool with the skill's exact ID; the tool's list holds only ID, name and description (https://opencode.ai/docs/skills/).
- CONFIRMED from earlier research (research/forge.md): code plugins auto-load from `.opencode/plugins/` (project) or `~/.config/opencode/plugins/` (global) (https://opencode.ai/docs/plugins/).
- UNCONFIRMED: OpenCode has no documented shell-hook config with an exit-code-2 equivalent (research/tools-and-guards.md). The page says only where plugins live and tells the reader to check the docs for what a plugin can block.
- UNCONFIRMED: a command that lists skills in OpenCode. The page asks the agent instead.

## Other
- Model Context Protocol introduction: https://modelcontextprotocol.io/docs/getting-started/intro (already cited in earlier research notes; used here as a Lore link).
