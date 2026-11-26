# Sandbox and permissions (Test the Leash)

Read 2026-11-26 through a summarising fetch subagent; verbatim where marked. Commands were NOT run by us.

- https://code.claude.com/docs/en/sandboxing : `/sandbox`, Seatbelt on macOS, bubblewrap and socat on Linux/WSL2 with apt and dnf commands, native Windows unsandboxed, default write scope, empty allowed-domains proxy, settings keys `sandbox.filesystem.allowWrite` and `sandbox.network.allowedDomains`, probe commands `touch ~/sandbox-probe` and `curl --noproxy '*' https://example.com` with expected errors (verbatim). Sandbox covers Bash, PowerShell and Monitor commands, not Read/Edit/Write, MCP or hooks.
- https://code.claude.com/docs/en/permission-modes : mode table, Shift+Tab, `--permission-mode`.
- https://code.claude.com/docs/en/permissions : rule syntax, deny then ask then allow. The `Read(./.env)` JSON example is composed from verbatim rule forms. A Read deny does not cover shell commands that read files.
- https://code.claude.com/docs/en/devcontainer : `--dangerously-skip-permissions` with a non-root dev container; warning about credentials in `~/.claude` and writes to the bind mount (verbatim).
- https://coderefinery.github.io/coding-with-ai/scenario-agentic/ : full page read. Its sandboxing section is two bullets; the Docker demo and exercise Agent-2 use `docker run -it --network none -v $(pwd):/project python:3.11 bash`. Its sample `.claude/settings.json` keys (`allow_file_read` and so on) could not be verified and are not used.

Not confirmed: the `docker run` line was not run; the prompt wording ("yes once, yes for the session, no") was not seen in a live session; the `/sandbox` mode names are taken from the docs summary.
