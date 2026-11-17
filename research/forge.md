# Forge zone: skills, skill evals, plugins, OpenCode, trust

Read 2026-11-13. Official docs only. Local `claude --version`: 2.1.325. Docs pages show no publish date; skills page cites versions up to v2.1.319.
Method: pages fetched via a summarising fetch tool (quotes as returned). Base: C = https://code.claude.com/docs/en/ ; O = https://opencode.ai/docs/
Decision fed: accuracy of quest text for Skills -> Evals -> Plugins -> OpenCode -> Security.

## 1. Skills
- CONFIRMED: project skill path `.claude/skills/<skill-name>/SKILL.md` ("loads in sessions in this repository"); personal `~/.claude/skills/<name>/SKILL.md`. C skills
- CONFIRMED: "All fields are optional. Only `description` is recommended." Smallest skill = frontmatter with `description:` + a body. Dir name becomes `/<name>` unless `name` is set. C skills
- CONFIRMED: edits under `.claude/skills/` are picked up without restart; a top-level skills dir created mid-session needs `/reload-skills`. C skills
- CONFIRMED: confirm pickup by typing `/` (menu), running `/skills`, then asking something matching the description. `claude --debug` + search `[names]` for refused names. C skills
- CONFIRMED: `/skill-doctor` shows skills in the listing but never invoked; `/doctor` for setup check. C skills
- CONFIRMED reasons it does not trigger (all from C skills):
  - Frontmatter only read if opening `---` is the file's first line.
  - YAML that fails to parse: skill loads with no fields set.
  - Misspelled field names ignored silently.
  - `description`+`when_to_use` truncated at 1,536 chars in the listing; put key use case first.
  - `disable-model-invocation: true` means Claude cannot invoke it itself.
  - Names with zero-width/control chars or `<`/`>` refused.
  - Skills in subdirectories load only after Claude touches a file there.
- UNCONFIRMED: the page's own "Skill not triggering" troubleshooting section (last ~19.5k chars of the page were not read). Re-read with offset 100000 before quoting.

## 2. Skill evals
- CONFIRMED: `claude plugin eval [target] [options]`; requires Claude Code v2.1.269+, git 2.31+ if git installed. C plugin-evals, C plugins/cli-reference#plugin-eval
- CONFIRMED: target is a plugin dir (`.`), a single `prompt.md`/`case.yaml`, or installed `name[@marketplace]`/`name@skills-dir`. A skills-directory plugin (folder with `.claude-plugin/plugin.json`) qualifies. A bare `.claude/skills/x/SKILL.md` with no manifest is not stated to qualify. C plugin-evals
- CONFIRMED layout: `evals/<case>/prompt.md` (frontmatter = run fields, body = prompt), `evals/<case>/graders/<name>.md` (frontmatter `type` + options), optional `case.yaml`, `evals/results/<timestamp>/{aggregate-result.json,report.html}`. A case with no grader fails to load. `claude plugin eval init --bare <name>` writes a blank case. C plugin-evals
- CONFIRMED prompt.md fields: `max_turns` (10), `timeout_seconds` (300), `runs` (3), `model`, `allowed_tools`, `tags`, `env` (EVAL_* only). C plugin-evals
- CONFIRMED six grader types: `regex`, `tool_used`, `tool_order`, `file_exists` (free, computed from transcript/files); `llm`, `baseline` (judge model, cost). "There are no custom-code graders." C plugin-evals
- CONFIRMED skill-fired grader: `type: tool_used`, `tool: Skill`, `input_match: '"skill"\s*:\s*"(?:[\w-]+:)?your-skill-name"'`; passes if invoked at least once. `tool_used` has `min`/`max` (`min: 0, max: 0` = never called). C plugin-evals
- CONFIRMED scoring: 3 runs per case per arm; run score = fraction of graders passed; case passes when mean >= `--threshold` (default 1.0). Default also runs a no-plugin arm: `WITH`, `W/OUT`, `Δ`. `tool_used: Skill` is excluded from score in two-arm runs (indicator only) unless `arm: both`. C plugin-evals
- CONFIRMED flags: `--runs`, `--case <glob>`, `--tag`, `--model`, `--judge-model`, `--ablation none|with-without`, `--threshold`, `--max-cost-usd`, `--allow-tools`, `--scaffold`, `--trust-plugin`, `--mocks`, `--json [path]`, `--output-dir`, `--no-publish`, `--keep-temp`, `--eval-dir`. Iterate cheaply: `claude plugin eval . --case <name> --runs 1 --ablation none`. C plugin-evals
- CONFIRMED exit codes: 0 pass; 1 below threshold/load failure/untrusted/API error; 2 partial (cost ceiling or auth); 130 interrupted; 143 terminated. C plugin-evals
- CONFIRMED cost: "Every eval run and every judge grader is a real model call on your account"; cost shown is a list-price estimate. About cases x runs x 2 arms agent runs, plus 3 judge calls per `llm`/`baseline` grader per run. C plugin-evals
- CONFIRMED isolation: each run is a `claude -p` child with temp home/cwd/config, only the plugin loaded; no user settings, CLAUDE.md, MCP, other plugins; case files hidden from agent. Read-only tools only unless granted; granting `Bash` runs it under the OS sandbox (writes confined to workspace, network limited); with no sandbox backend (native Windows) runs are refused. First run asks "Trust this plugin directory?". C plugin-evals
- CONFIRMED guidance: phrase prompts as a user would, not naming the skill; pair one result grader with one process grader (`tool_used`/`tool_order`); use `regex` on files for long output, `llm` only for short output with concrete PASS/FAIL rubric; pin `--model`/`--judge-model` in CI. C plugin-evals
- CONFIRMED: Δ near zero with failing `tool_used: Skill` "usually a real finding": the description does not trigger on that phrasing. C plugin-evals
- CONFIRMED: `claude plugin validate` checks syntax/schema, not behavior. C plugin-evals
- CONFIRMED: skill-creator plugin has a separate `evals/evals.json` format; neither tool reads the other's cases. C plugin-evals

## 3. Plugins
- CONFIRMED: plugin = directory of skills, agents, hooks, MCP servers etc. loaded as one unit; manifest optional, at `.claude-plugin/plugin.json`. C plugins (overview), C plugins/manifest-reference
- CONFIRMED manifest: only `name` required (kebab-case; namespaces components, e.g. `/my-first-plugin:hello`). Others: `displayName`, `version` (pins updates), `description`, `author{name,email,url}`, `homepage`, `repository`, `license`, `keywords`, `defaultEnabled`, `dependencies`, `userConfig`, `skills`, `commands`, `agents`, `hooks`, `mcpServers`, `lspServers`, `outputStyles`, `workflows`, `experimental.{themes,monitors,evals}`. Names starting `claude-`/`anthropic-` are a validate error. C plugins/manifest-reference
- CONFIRMED layout: `skills/<name>/SKILL.md`, `commands/` (older; prefer skills), `agents/*.md`, `hooks/hooks.json` (top-level `"hooks"` key), `.mcp.json`, `.lsp.json`, `bin/`, `output-styles/`. Only `plugin.json` goes inside `.claude-plugin/`; components there do not load. C manifest-reference
- CONFIRMED local test without marketplace: `claude --plugin-dir ./my-first-plugin`; `/reload-plugins` after edits; `/plugin` Installed/Errors tabs; `claude plugin list`. `CLAUDE_CODE_PLUGIN_DIRS` needs v2.1.280+. C plugins/create
- CONFIRMED: `claude plugin validate <path> [--strict] [--json]`; exit 0 pass, 1 fail, 2 unexpected error. `--strict` fails on warnings. C plugins/cli-reference#plugin-validate, C manifest-reference
- CONFIRMED subcommands listed: init, install, uninstall, enable, disable, update, list, details, configure, prune, eval, eval init, tag, test (mods), validate; `plugin marketplace add|list|remove|update`. `claude plugins` is an alias. C plugins/cli-reference
- CONFIRMED marketplace: a repo/dir with `.claude-plugin/marketplace.json` listing plugins and where to fetch each; a catalog, not a hosted store. Add once (`claude plugin marketplace add <source>`), install by name (`commit-commands@claude-plugins-official`). Official marketplace auto-added on first interactive start. Install scopes: user, project, local. C plugins (overview)
- CONFIRMED: `claude plugin init <name>` scaffolds under `~/.claude/skills/` (auto-loads as `<name>@skills-dir`). C plugins/create

## 4. OpenCode (docs as fetched 2026-11-13; no version shown)
- CONFIRMED: OpenCode has plugins AND skills AND agents. O plugins, O skills, O agents
- CONFIRMED plugins: code plugins ("add tools, hooks, integrations, commands, agents"); auto-load `.ts`/`.js` or package folders from `.opencode/plugins/` (project) or `~/.config/opencode/plugins/` (global); or listed in config as npm packages (versioned/scoped), git repos, or local directories. O plugins
- UNCONFIRMED: config key spelling. The fetched page example shows `"plugins": [...]`; I recall `plugin` (singular) from older docs. Check the page raw before teaching.
- CONFIRMED skills: `.opencode/skills`, plus compat `.claude/skills` and `.agents/skills` (project); `~/.config/opencode/skills`, `~/.claude/skills`, `~/.agents/skills` (global). Found as `SKILL.md` in dirs (or flat `*.md`). Skill ID comes from file path; `name` is display only; skills without `description` are not advertised. Model loads via `skill` tool; `@skill-id` in a prompt loads one yourself. Permissions `allow|ask|deny` on `skill`. O skills
- CONFIRMED agents: markdown with frontmatter (body = system prompt) in `.opencode/agents/<name>.md` or `~/.config/opencode/agents/`, or JSONC under `agents`. O agents
- UNCONFIRMED: whether OpenCode reads Claude plugin `.claude-plugin/plugin.json`; docs read say nothing. Only plain `.claude/skills` is documented as compatible.
- UNCONFIRMED: any OpenCode equivalent of `claude plugin eval`/validate (not looked for beyond the three pages).

## 5. Security
- CONFIRMED: "A Claude Code plugin you install can execute arbitrary code on your machine with your user privileges." Hooks, monitors, mods, stdio MCP/LSP servers and `bin/` run; hooks/monitors/servers run outside the sandbox and permission rules. Skills/commands/agents enter context as instructions. C plugins/security
- CONFIRMED: trust warning text: "Make sure you trust a plugin before installing, updating, or using it. Anthropic does not control what MCP servers, files, or other software are included in plugins..." C plugins/security
- CONFIRMED review steps: `claude plugin marketplace list` (source); `/plugin` details pane "Will install"; read `hooks/hooks.json`, `.mcp.json`, `bin/`; `claude --plugin-dir <dir> plugin details <name>` prints a Component inventory without a session. C plugins/security
- CONFIRMED: tiers official / community / third-party; official and community names accepted only from `github.com/anthropics/` sources; marketplace name says who publishes, not what a plugin does. Auto-update can change reviewed files. Remove with `claude plugin uninstall`; cache stays 14 days. C plugins/security
- CONFIRMED: admins can allowlist/block marketplaces, force-enable plugins, disable `--plugin-dir`/`--plugin-url`. C plugins/security
- CONFIRMED: `plugin eval` "is the same trust decision as `claude --plugin-dir`"; passing suite says nothing about plugin safety; hooks you did not write make scores advisory unless run isolated. C plugin-evals
- UNCONFIRMED: official guidance specific to untrusted standalone skills (outside plugins). Not found in pages read.

## Tested
- `claude --version` -> 2.1.325 (Claude Code). No plugin or eval was run (would spend tokens). All behavior above is from docs, not executed.
