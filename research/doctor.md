# Doctor zone: /doctor, claude doctor, and the "which command shows what" set

Read 2026-11-16. Official docs only. Local `claude --version`: 2.1.325. No model-calling command and no `claude doctor` run (docs say it is local, but not needed).
Method: pages fetched via a summarising fetch tool. Base: C = https://code.claude.com/docs/en/ ; O = https://opencode.ai/docs/
Decision fed: accuracy of the Doctor quest and its command table.

## 1. /doctor (in-session)
- CONFIRMED: syntax `/doctor [prompt-audit [path]]`, alias `/checkup`. It is a bundled SKILL (prompt-based: "give Claude detailed instructions and let it orchestrate the work using its tools"), unlike fixed-logic built-in commands. C commands, C skills
- CONFIRMED: a "setup checkup that diagnoses installation, settings, extension, and CLAUDE.md problems and proposes fixes that Claude applies after you confirm". "Claude reports its findings first and asks for confirmation before changing anything." C commands, C skills#check-your-setup-with-/doctor
- CONFIRMED areas covered (C skills): installation health (duplicate/leftover installs, PATH problems, unparseable settings files, newer version on your release channel); extensions (unused skills, MCP servers, plugins vs context cost; slow hooks); CLAUDE.md files (local copies duplicating checked-in ones, checked-in content Claude could derive from the codebase, always-loaded guidance it offers to migrate into skills / nested CLAUDE.md); permissions (offer to make auto mode default, pre-approve read-only commands you often deny); usage (on Pro/Max/Ultra/Team/Enterprise, changes `/usage` recommends, last 7 days; needs v2.1.305+; omitted while Remote Control is connected).
- CONFIRMED: debug-your-config page adds "duplicate subagent names in the same directory". C debug-your-config
- CONFIRMED: not read-only in the strict sense: it can change things, but only after you confirm. The read-only variant is `claude doctor` (section 2).
- UNCONFIRMED: output format in words. The skills page says nothing about layout. (Since it is a skill, expect a prose report from Claude; this is inference, not documented.)
- UNCONFIRMED: network calls. Not stated for `/doctor`. Inference only: as a skill it runs through the model, so it is not a local-only check. Do not state as fact.
- UNCONFIRMED: checks for keybindings, sandbox availability, MCP config validity, context-usage warnings. NOT listed for `/doctor`. (Context warnings are `/context`; MCP status is `/mcp`.)

## 2. Variants and neighbours (exact names)
- CONFIRMED `/doctor prompt-audit [path]` (v2.1.283+): checks CLAUDE.md, CLAUDE.local.md, AGENTS.md plus rules, skills, commands, subagents, output styles under `.claude/` and `~/.claude/` for outdated or conflicting instructions: written for older models, references to missing files/commands, files that contradict each other. Report with proposed edits; "nothing in your files changes until you ask Claude to apply them". Runs through the bundled `/claude-api` skill; unavailable if that skill is off via `skillOverrides` or `disableBundledSkills`. It audits correctness/conflicts, NOT size or cost. C memory#audit-your-instruction-files, C commands
- CONFIRMED `claude doctor` (shell): "read-only installation and settings diagnostics ... without starting a session", incl. install health, settings-file validation errors, Remote Control eligibility, warnings with suggested fixes. Use it when `claude` won't start. C cli-reference, C setup, C troubleshooting
- CONFIRMED lines seen in `claude doctor` output (from docs): `Auto-updates` line (`enabled` / `disabled (set by env: DISABLE_AUTOUPDATER)`), `Last update attempt: failed (install_failed)`, a `Search` line (`OK (bundled)` or system ripgrep path), a warning starting `macOS Keychain is not writable` with a fix, reports a custom launcher the native installer did not create, lists fixes when npm global dir is not writable. C setup, C troubleshoot-install, C troubleshooting
- CONFIRMED caveats: shows Search OK even on slow WSL cross-filesystem; scans shell rc files for an old `claude` alias and hung if one was a directory (fixed v2.1.214). C troubleshooting, C troubleshoot-install
- CONFIRMED `/skill-doctor` (v2.1.252+, needs feature-flag fetching): per-skill context cost and how often used; flags never-invoked skills and says where to turn them off; also lists plugins not used recently. Opens in `/plugin` Stats tab; with `-p` prints text. Excludes bundled and enterprise skills. Not available over Remote Control. C skills#find-unused-skills
- CONFIRMED `/status`: opens Settings on Status tab: version, model, account, connectivity; also which settings sources are active (managed settings in effect?). C commands, C debug-your-config
- CONFIRMED `/context [all]`: colored grid of context use by category (system prompt, tools, MCP tools, subagents, memory files, skills, messages), optimization suggestions, over-limit warnings. `all` expands in fullscreen. C commands, C debug-your-config
- CONFIRMED `/mcp [reconnect|enable|disable ...]`: MCP servers and connection status; manage OAuth. C commands
- CONFIRMED `/permissions` (alias `/allowed-tools`): allow/ask/deny rules by scope, add/remove, working dirs. C commands
- CONFIRMED `/memory`: edit CLAUDE.md files, toggle and view auto memory. C commands
- CONFIRMED `/hooks`: view configured hooks (grouped by event). C commands, C debug-your-config
- CONFIRMED `/skills`: list skills, press `t` to sort by token count. `/reload-skills` rescans disk. C commands
- CONFIRMED `/debug [description]` (bundled skill): turns on debug logging mid-session, then Claude reads the log. `claude --debug='mcp,startup'` (filter only in `=` form), `--debug-file <path>`; logs at `~/.claude/debug/<session-id>.txt`. C commands, C cli-reference, C debug-your-config
- CONFIRMED `claude --safe-mode`: starts with CLAUDE.md, skills, plugins, hooks, MCP, custom commands/agents etc. off; auth, model, built-in tools, permissions normal. C cli-reference, C debug-your-config
- CONFIRMED `/usage` (aliases `/cost`, `/stats`): session cost, plan limits. C commands

## 3. Troubleshooting guidance
- CONFIRMED: "not sure which applies": run `/doctor` for automated check of installation, settings, extensions, context usage; run `claude doctor` from the shell if `claude` won't start; `/mcp` for MCP status. C troubleshooting
- CONFIRMED: footer `Auto-update failed · Run claude doctor` -> doctor only shows date/code, not cause; run `claude update` for the real error. C troubleshoot-install
- CONFIRMED: "Still stuck": if `claude --version` works but something else is wrong, run `claude doctor`; open a GitHub issue with OS, install command, full error output; `/feedback` in session. C troubleshoot-install
- CONFIRMED: settings not applying / hooks / MCP / skills -> debug-your-config page: `/context` first, then `/memory` `/skills` `/hooks` `/mcp` `/permissions` `/doctor` `/status`. `claude doctor` for invalid settings files. C debug-your-config
- UNCONFIRMED: any docs statement on whether doctor output contains paths or keys, or advice to redact it. Not stated. (Only privacy notes found: `/heapdump` `.heapsnapshot` contains conversation and credentials; share only `-diagnostics.json`. C troubleshooting.) Advise readers to review before pasting; label as our advice.

## 4. OpenCode
- CONFIRMED: CLI page lists no doctor/status command. Only diagnostic: `opencode debug paths [selector]` (prints db, home, data, config, cache, state, tmp, bin, log, repos paths; no server, no DB open). O cli/
- UNCONFIRMED: TUI slash commands (e.g. /status): not on the CLI page; the TUI page was not read. Do not claim `opencode doctor` exists.

## 5. Names NOT documented (do not use)
- No `/doctor` options other than `prompt-audit [path]`; no `claude doctor` flags (not checked with `--help`); no `/doctor --fix`; no `/health`.
- Doctor checks for keybindings, sandbox availability, MCP config validity: not documented.
- `claude self-hosted-runner doctor` exists but is for self-hosted runners only. C cli-reference
