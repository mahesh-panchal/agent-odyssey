# Kennel and crypt: primary-source research

All sources read 2026-11-13. Only official docs, official GitHub repos and release APIs. Doc pages were fetched via a summarising fetch tool; quoted commands/keys come from that output. Anything not confirmed is marked UNCONFIRMED.

## 1. Claude Code: install, login, version

**Latest version.** v2.1.323, published 2026-11-12T22:12Z (`gh api repos/anthropics/claude-code/releases/latest`; https://github.com/anthropics/claude-code/releases/latest, read 2026-11-13).

**Install (native installer is the recommended path).** Source: https://code.claude.com/docs/en/setup (2026-11-13).
- macOS (Apple Silicon), Linux, WSL: `curl -fsSL https://claude.ai/install.sh | bash`
- Windows PowerShell: `irm https://claude.ai/install.ps1 | iex`
- Windows CMD: `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd`
- Homebrew: `brew install --cask claude-code` (stable channel, about a week behind) or `claude-code@latest`. No auto-update; `brew upgrade claude-code`.
- WinGet: `winget install Anthropic.ClaudeCode`
- npm: `npm install -g @anthropic-ai/claude-code` (Node 22+; do not use sudo).
- Linux packages: signed apt/dnf/apk repos at downloads.claude.ai (see setup page).
- WSL: open the WSL distro and run the Linux installer inside it; launch `claude` from the WSL terminal. WSL 2 supports sandboxing; WSL 1 and native Windows do not.
- System requirements: macOS 13+, Ubuntu 20.04+, Debian 10+, Alpine 3.19+, Windows 10 1809+; 4 GB+ RAM; internet required.
- Native installs auto-update in the background; `claude update` forces it. Pin: `curl -fsSL https://claude.ai/install.sh | bash -s 2.1.89` (also `stable`).
- The installer puts a launcher at `~/.local/bin/claude`; if "command not found", PATH is the cause.

**Check version / health.** `claude --version` prints e.g. `2.1.211 (Claude Code)`. `claude doctor` prints read-only diagnostics. `/status` in-session shows login method and loaded settings sources. (setup page)

**Login.** Source: https://code.claude.com/docs/en/authentication (2026-11-13).
- Team plan: run `claude`, browser opens, log in with the claude.ai account your admin invited you to. Free claude.ai plan has no Claude Code access.
- API key (Console): `export ANTHROPIC_API_KEY=...`; in interactive mode Claude Code asks once to approve the key. Or choose the Console account at `/login`.
- Precedence gotcha (quoted behaviour): if a subscription AND `ANTHROPIC_API_KEY` are both present, the key is used once approved; fix with `unset ANTHROPIC_API_KEY`, confirm with `/status`.
- `/logout` to re-authenticate; `claude auth login` / `claude auth logout` exist in the shell; `claude setup-token` makes a one-year token for CI (`CLAUDE_CODE_OAUTH_TOKEN`).
- Credentials: macOS Keychain; Linux `~/.claude/.credentials.json` mode 0600.

## 2. Claude Code: permissions and sandbox

Sources: https://code.claude.com/docs/en/permissions, /permission-modes, /settings, /sandboxing (2026-11-13).

**Modes** (`permissions.defaultMode` value; CLI flag `claude --permission-mode <value>`):
| Value | Meaning |
|---|---|
| `default` (labelled Manual; alias `manual`) | prompts on first use of each tool |
| `acceptEdits` | auto-accepts file edits and common fs commands (`mkdir`, `touch`, `mv`, `cp`) in working dir |
| `plan` | reads files and runs read-only shell commands; does not edit source files |
| `auto` | background classifier approves actions; only appears when available |
| `dontAsk` | auto-denies anything that would prompt; pre-approved tools still run |
| `bypassPermissions` | skips prompts; also `--dangerously-skip-permissions`; docs say use only in containers/VMs |
- Switch in session: `Shift+Tab` cycles `default` -> `acceptEdits` -> `plan` (auto appears if available; `dontAsk` never in cycle; bypass only if started with a bypass flag). Status bar shows e.g. `⏸ plan mode on`.
- Start read-only style: `claude --permission-mode plan`, or `{"permissions": {"defaultMode": "plan"}}`.
- `defaultMode` of `auto` or `bypassPermissions` has no effect from project/local settings files (user or managed only).

**Settings files** (settings page):
- User: `~/.claude/settings.json` (all projects)
- Shared project: `.claude/settings.json` (commit it)
- Project local: `.claude/settings.local.json` (Claude Code adds it to global git excludes when it writes it; if created by hand, gitignore it yourself)
- Managed: `managed-settings.json` / MDM / server-managed (highest precedence)
- Precedence high to low: managed, command line (`--settings`), local, shared project, user. `permissions.allow` lists merge across files. Deny from any scope beats allow from any scope; a matching `ask` beats a more specific `allow`.
- Files are strict JSON (no comments, no trailing commas). Edits reload live.
- Project `permissions.allow` rules only apply after the workspace trust dialog; `deny`/`ask` apply immediately.
- "Yes, and don't ask again" on a Bash command saves an allow rule to `.claude/settings.local.json` (at git repo root).

**Rule syntax.** Format `Tool` or `Tool(specifier)`. Example from the settings page:
```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": ["Bash(npm run lint)", "Bash(npm run test *)"],
    "deny":  ["Read(./.env)", "Read(./.env.*)"]
  }
}
```
Further examples from the permissions page:
- `"allow": ["Bash(npm run *)", "Bash(git commit *)"], "deny": ["Bash(git push *)"]`
- Third list key is `ask` (e.g. `Bash(git clean *)` prompts).
- `Bash` alone or `Bash(*)` = all Bash; as a deny it removes the tool entirely.
- Space before trailing `*` matters: `Bash(ls *)` matches `ls -la` but not `lsof`; `Bash(ls*)` matches both. `Bash(ls:*)` equals `Bash(ls *)`.
- Compound commands are split on `&&`, `||`, `;`, `|`, `|&`, `&`, newline; every part must be allowed. Wrappers `timeout`, `time`, `nice`, `nohup`, `stdbuf` are stripped before matching.
- Read/Edit paths: `Read(./secrets/**)`, `Read(~/Documents/*.pdf)`, `Read(//Users/alice/secrets/**)` (`//` = absolute, `~/` = home, bare or `./` = relative to cwd). `Read(.env)` matches `.env` at any depth. Use `Read`/`Edit` rules, not `Grep`/`Glob`/`Write` rules (those do not match). `.claudeignore` has no effect.
- Deny rules apply when either a symlink or its target matches.
- Caveats (docs): Bash patterns constraining arguments are fragile, e.g. `Bash(curl http://github.com/ *)` misses variants; `Bash(rm *)` does not match `/bin/rm` or `bash -c 'rm ...'`; `Bash(git push *)` does not match `git -C . push`. Read-deny is "best-effort" across built-in tools. Rules are enforced by Claude Code, not the model; CLAUDE.md instructions do not change what is allowed. A PreToolUse hook can add enforcement.
- Built-in read-only commands (`ls`, `cat`, `grep`, `find`, `head`, `wc`, read-only `git`...) run without prompt in every mode; not configurable except via ask/deny rules.
- v2.1.323 release notes: wildcard-attached allow rules like `Bash(ls*)` now prompt in some cases (tightened checks).

**Sandbox** (https://code.claude.com/docs/en/sandboxing):
- OS-enforced boundary for shell commands (Bash, PowerShell, Monitor and child processes) only. File tools (Read/Edit/Write/WebFetch), MCP servers, hooks run OUTSIDE it.
- macOS: Seatbelt (nothing to install). Linux/WSL2: bubblewrap + socat (`sudo apt-get install bubblewrap socat`). Native Windows and WSL1: unsupported.
- Off by default. Enable via `/sandbox`, or `~/.claude/settings.json`: `{"sandbox": {"enabled": true}}`, or `claude --settings '{"sandbox": {"enabled": true, "allowUnsandboxedCommands": false}}'`.
- Keys: `sandbox.enabled`, `failIfUnavailable`, `allowUnsandboxedCommands`, `autoAllowBashIfSandboxed` (default true), `filesystem.allowWrite/denyWrite/denyRead/allowRead`, `network.allowedDomains/deniedDomains`, `excludedCommands`, `credentials.files/envVars`.
- Defaults: writes limited to working dir and temp; reads cover most of the machine INCLUDING `~/.ssh` and `~/.aws/credentials` unless `denyRead` set; network via proxy with empty `allowedDomains`; environment (secrets) inherited.
- Teach: failed commands may retry unsandboxed via `dangerouslyDisableSandbox` unless `allowUnsandboxedCommands: false`. `!` shell-mode commands usually run unsandboxed. `docker` does not work inside. Docs say it is one layer; for stronger isolation use a container or VM.

## 3. OpenCode

**Repo and version.** Repo is now https://github.com/anomalyco/opencode (the sst/opencode URL was not tested; UNCONFIRMED redirect). Latest release by API: `v2.3.0`, 2026-11-13T08:55Z (`gh api repos/anomalyco/opencode/releases`). Note: GitHub's "Latest" flag still points at `v1.19.5` (2026-10-28), so `/releases/latest` is misleading. Docs at https://opencode.ai/docs/ describe "V2".

**Install** (https://opencode.ai/docs/ and repo README, 2026-11-13):
- `curl -fsSL https://opencode.ai/v2/install | bash` (macOS, Linux, WSL; installs to `$HOME/.opencode/bin`)
- `brew install anomalyco/tap/opencode-v2` (README: recommended); `brew install opencode` (official formula, "updated less", version UNCONFIRMED)
- `npm install -g @opencode/cli` (docs page) / `npm i -g @opencode/cli@latest` (README)
- mise: `mise use -g opencode` (needs mise 2026.10.9+, otherwise installs OpenCode 1)
- Windows: docs say "Windows package managers are not supported"; standalone zip or desktop installer. WSL: no special notes on the page; use the Linux curl script inside WSL (inference).
- CONFLICT: Ollama's integration page (https://docs.ollama.com/integrations/opencode) still shows `curl -fsSL https://opencode.ai/install | bash` and `npm install -g opencode-ai` (V1-era). Teach the opencode.ai commands; flag that docs differ.
- Connect a provider in the TUI with `/connect`.

**Config files.** `opencode.json` or `opencode.jsonc`. Global `~/.config/opencode/opencode.json(c)`; project `<project>/opencode.json(c)` or `<project>/.opencode/opencode.json(c)`; managed `/Library/Application Support/opencode` (macOS), `/etc/opencode` (Linux). (https://opencode.ai/docs/config/)

**Local Ollama, V2 form.** (https://opencode.ai/docs/providers/) Ollama at `http://127.0.0.1:11434` is auto-discovered; no config needed. Explicit form:
```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "ollama": {
      "settings": {
        "baseURL": "http://127.0.0.1:11434/v1",
        "apiKey": "{env:OLLAMA_API_KEY}"
      }
    }
  }
}
```
(`apiKey` optional; page says include `/v1`.)

**Local Ollama, V1 form** (https://docs.ollama.com/integrations/opencode):
```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama",
      "options": { "baseURL": "http://localhost:11434/v1" },
      "models": { "qwen3.5": { "name": "qwen3.5" } }
    }
  }
}
```
Ollama also offers `ollama launch opencode` and `ollama launch opencode --config`. Both pages say OpenCode needs 64k+ context ("OpenCode requires a context length of 64k or higher").

**Generic OpenAI-compatible gateway.**
V2 (providers page):
```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "acme": {
      "name": "Acme",
      "env": ["ACME_API_KEY"],
      "package": "@opencode/ai/providers/openai-compatible",
      "settings": { "baseURL": "https://llm.acme.example/v1" },
      "models": { "qwen3-coder": { "name": "Qwen 3 Coder" } }
    }
  }
}
```
Select as `acme/qwen3-coder`.
V2 as shown in the migration guide (https://opencode.ai/docs/migrate-v1/), with explicit env substitution:
```jsonc
"providers": { "acme": {
  "package": "aisdk:@ai-sdk/openai-compatible",
  "settings": { "baseURL": "https://llm.example.com/v1", "apiKey": "{env:ACME_API_KEY}" } } }
```
The `package` string differs between the two official pages (`@opencode/ai/providers/openai-compatible` vs `aisdk:@ai-sdk/openai-compatible`). UNCONFIRMED which is canonical; test before publishing. V1 equivalent: `"provider": {"acme": {"npm": "@ai-sdk/openai-compatible", "api": "https://llm.example.com/v1", "options": {"apiKey": "{env:ACME_API_KEY}"}}}`.
Migration guide: "Existing supported V1 configuration is intended to keep working", but it does not explicitly confirm each V1 key; UNCONFIRMED for `provider`/`permission` in 2.3.0.

**Permissions, V2** (https://opencode.ai/docs/permissions/): top-level `permissions` is an ORDERED ARRAY of `{ "action", "resource", "effect" }`; `effect` is `"allow"`, `"deny"` or `"ask"`. Last matching rule wins. No match means `ask`. Configured `deny` always enforced.
```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "permissions": [
    { "action": "shell", "resource": "*", "effect": "ask" },
    { "action": "shell", "resource": "git status *", "effect": "allow" },
    { "action": "shell", "resource": "git push *", "effect": "deny" }
  ]
}
```
- Actions: `read`, `edit` (covers edit/write/patch), `glob`, `grep`, `shell`, `subagent`, `skill`, `question`, `webfetch`, `websearch`, `external_directory`, MCP `<server>_<tool>`.
- Pattern: `*` matches zero or more characters including `/`; `?` one char; trailing `" *"` also matches the bare command.
- DEFAULT is permissive: base policy `{ "action": "*", "resource": "*", "effect": "allow" }`, with `read` of `*.env` and `*.env.*` set to `ask` (`*.env.example` allow). The built-in `plan` agent denies `edit` except under `~/.opencode/plan`.
- `external_directory` is allowed by default in V2 (V1 asked). To restore: `{ "action": "external_directory", "resource": "*", "effect": "ask" }`.
- Docs: "Shell is not a sandbox. It runs with the host user's authority."
- Org hard-deny block: `"policies": [{ "action": "tool.use", "resource": "shell:sudo *", "effect": "deny" }]`.
- V1 form (from migration guide): `"permission": {"bash": {"git push *": "ask"}, "edit": "allow"}`; V2 names: `bash`->`shell`, `task`->`subagent`, `write`/`patch`->`edit`.
- Teaching implication: a safe-by-default starter needs an explicit `{ "action": "*", "resource": "*", "effect": "ask" }` first, then narrow allows, then denies last (last match wins).

## 4. Ollama

**Latest version.** v0.40.16, 2026-11-09 (stable; `gh api repos/ollama/ollama/releases/latest`). `v0.40.17-rc0` (2026-11-10) is a pre-release.

**Install** (https://github.com/ollama/ollama README; https://docs.ollama.com/linux, 2026-11-13):
- macOS: `curl -fsSL https://ollama.com/install.sh | sh` or the `.dmg` from ollama.com/download/Ollama.dmg
- Linux: `curl -fsSL https://ollama.com/install.sh | sh`. Manual: `curl -fsSL https://ollama.com/download/ollama-linux-amd64.tar.zst | sudo tar x -C /usr`, then `ollama serve`; verify with `ollama -v`. Systemd unit uses `ExecStart=/usr/bin/ollama serve`.
- Windows: `irm https://ollama.com/install.ps1 | iex` or `OllamaSetup.exe`. The Windows page serves the API on `http://localhost:11434` and does not mention WSL.
- WSL: no dedicated primary-source guidance found. UNCONFIRMED. Options are the Linux installer inside WSL, or Windows Ollama reached from WSL (networking not documented).

**CLI** (https://docs.ollama.com/cli): `ollama pull <model>`, `ollama run <model> [prompt]`, `ollama ls`, `ollama ps` (running models), `ollama rm <model>`, `ollama stop <model>`, `ollama serve` (`--help` lists env vars). `ollama show` was not on the CLI page.

**Context length** (https://docs.ollama.com/context-length, 2026-11-13):
- Default depends on VRAM: under 24 GiB VRAM = 4k; 24-48 GiB = 32k; 48 GiB+ = 256k. A 16 GB laptop therefore gets 4k.
- Docs: web search, agents and coding tools should use "at least 64000 tokens".
- Raise: `OLLAMA_CONTEXT_LENGTH=64000 ollama serve`, or the slider in the Ollama app settings. Inside `ollama run`: `/set parameter num_ctx 4096` (shown on https://docs.ollama.com/faq, which also says the default is 4096 and that API requests can pass `"options": {"num_ctx": 4096}`). The FAQ and context pages differ on the default (flat 4096 vs VRAM-tiered); the context-length page is more specific.
- Check: `ollama ps` shows PROCESSOR (e.g. `100% GPU`, or a CPU/GPU split) and, per the context page, CONTEXT. Docs advise avoiding CPU offload. More context needs more memory; a 64k context on 16 GB unified memory may cause CPU spill or slow generation (inference; not measured here).

**Small tool-capable models** (library pages, 2026-11-13). Capability is stated per family; per-tag tool support is not broken out, so confirm with the "tools" badge on each page.
| Tag | Download | Context | Tools | Source |
|---|---|---|---|---|
| `qwen3:8b` | 5.2 GB | 40K | family tagged tools, thinking | ollama.com/library/qwen3 |
| `qwen3:4b` | 2.5 GB | 256K | same | same |
| `llama3.1:8b` | 4.9 GB | 128K | tools | ollama.com/library/llama3.1 |
| `granite4:3b` | 2.1 GB | 128K | tools | ollama.com/library/granite4 |
| `qwen3.5:4b` | 3.3-4.0 GB | 256K | family: vision, tools, thinking | ollama.com/library/qwen3.5 |
| `qwen3.5:9b` (latest) | 6.6-7.6 GB | 256K | same | same |
| `gemma4:e4b` | 6.6-9.5 GB | 128K | tools (family) | ollama.com/library/gemma4 |
- Also in the tools-filtered listing: `bonsai-2` (4b, 9b) and `ornith` (9b). Sizes in GB not read. UNCONFIRMED for fit.
- Do not recommend `qwen3-coder` here: only 30b (19 GB) and 480b tags exist.
- "Fits 16 GB" is my inference from file size only (KV cache and OS need extra headroom); the docs read did not state per-model RAM needs. Download size here is for the default quant listed on the page.
- The Ollama OpenCode page uses `qwen3.5` in its example; the OpenCode providers page uses `ollama pull qwen3:8b`.

## 5. Honest caveats for small local models as agents

From primary sources:
- Default 4k context on a 16 GB machine is far below the 64k that Ollama says agents need and OpenCode "requires". Symptom is an agent that forgets instructions or tool results. Raising context costs memory and can force CPU offload (`ollama ps`).
- Tool calling is a model capability flag; the Ollama tool-calling docs list no model guarantees. Models can return multiple tool calls per reply, and streaming needs chunk assembly. Docs hint that telling the model it is in a loop helps.
- Local-model safety is the tool's, not the model's: OpenCode's default policy is allow-all and "Shell is not a sandbox"; Claude Code's rules are best-effort for reads and fragile for argument patterns. Neither stops a weak model from running a destructive command that your rules fail to match.
- Claude Code sandbox leaves `~/.ssh` readable and secrets in the environment by default.
General (NOT backed by a primary source I read; mark as teaching opinion or test yourself): 3B-8B models are more prone to malformed tool-call JSON, looping, hallucinated flags and file paths, losing the task on long sessions, and weaker multi-file edits than hosted frontier models. Verify before stating as fact.

## Unconfirmed / needs human check

1. Which OpenCode `package` string is canonical for OpenAI-compatible providers (`@opencode/ai/providers/openai-compatible` vs `aisdk:@ai-sdk/openai-compatible`), and whether V1 `provider`/`permission` keys still load in v2.3.0. Test on a clean machine.
2. `brew install opencode` (official formula) version vs V2; and whether sst/opencode redirects to anomalyco/opencode.
3. OpenCode on WSL and Windows: no official WSL notes; Ollama docs show `npm install -g opencode-ai` for Windows (V1-era).
4. Ollama on WSL: no official guidance (install-inside-WSL vs reach Windows host).
5. Default Ollama context: FAQ says 4096, context-length page says VRAM-tiered (4k under 24 GiB). Verify on a 16 GB Mac with `ollama ps`.
6. Per-tag tool support and real RAM fit for the 3B-8B models above; run `ollama show <model>` (capabilities) and `ollama ps` on target hardware. Sizes for `bonsai-2` and `ornith` not read.
7. Claude Code docs show `Bash(ls*)`-style rules tightened in v2.1.323; re-check rule behaviour before publishing exact examples.
8. Model names on the Ollama library (qwen3.5, gemma4, etc.) change quickly; re-check tags the day of publication.
9. Claim that small models are unreliable agents is not sourced to a primary document.
10. Fetched via a summarising tool, so quotes could be paraphrased; spot-check key commands against the live pages.
