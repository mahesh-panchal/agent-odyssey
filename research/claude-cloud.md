# Claude Code cloud sessions: primary-source research

Date checked 2026-11-17. Official docs only, fetched via a summarising fetch tool (quotes are as returned; spot-check key commands live). Base C = https://code.claude.com/docs/en/ . Pages: CW = claude-code-on-the-web, WQ = web-quickstart, CE = cloud-environments, DU = data-usage, SEC = security, ZDR = zero-data-retention, PM = permission-modes, SET = settings, MOB = mobile, DESK = desktop. Sandbox/permission basics are in research/kennel-and-crypt.md and not repeated.
Secondary: https://claude.dev/blog/claude-code-in-the-cloud/ (Addy Osmani, 2026-10-06; provenance NOT confirmed; no licence stated, so paraphrase only; demo from a fictional repo). Flagged ARTICLE-ONLY below.
Everything marked (time-sensitive) can change; availability, limits and numbers especially.

## 1. What a cloud session is
- CONFIRMED: a Claude Code session on cloud infrastructure instead of your machine; Anthropic-managed by default, or an org self-hosted environment when routed there. Keeps running after you close the laptop. C CW
- CONFIRMED: each session = fresh Ubuntu 24.04 x86_64 VM with your repo cloned; clone happens fresh every session. C CE, C WQ
- CONFIRMED: local sessions run on your machine and use local config; cloud uses "repo only". C WQ (comparison table)
- CONFIRMED what travels: everything committed (CLAUDE.md, .claude/rules, skills, agents, commands; hooks/permissions/.mcp.json in a one-repo session). C CE "What carries over"
- CONFIRMED what does NOT travel: user ~/.claude/CLAUDE.md, ~/.claude/skills|agents|commands, user-scoped plugins and settings, `claude mcp add` servers at local/user scope, ~/.claude/settings.json, .claude/settings.local.json, plugins declared in repo settings, interactive auth such as AWS SSO, MDM/managed-settings files on your device. Org server-managed settings DO apply. C CE, C SET "Settings in cloud sessions"
- CONFIRMED: personal preferences can be written by a setup script to ~/.claude/CLAUDE.md in the VM. C CE
- CONFIRMED: Remote Control is different: code runs on YOUR machine, only the transcript syncs through Anthropic. C SEC, C DU

## 2. How to start (exact names)
- CONFIRMED: browser https://claude.ai/code ("Claude Code on the web"); mobile: Code tab in the Claude app; Desktop: choose Cloud in the environment selector; terminal `claude --cloud "task"`; scheduled tasks (routines) also run as cloud sessions. C CW
- CONFIRMED: `--cloud` clones the GitHub remote at your current branch, not your local checkout; push first. One repo at a time. `--remote` is a deprecated alias. C CW
- CONFIRMED: if the branch is not on GitHub the CLI prints `Branch <name> is not on GitHub` and the session starts from a pushed commit or default branch; unpushed commits and uncommitted changes are absent. C CW
- CONFIRMED: no GitHub remote or no Claude GitHub App on the repo: Claude Code bundles and uploads the local repo (full history all branches plus uncommitted changes to tracked files; <100 MB, git 2.31+; untracked files excluded). On macOS/Linux/WSL uncommitted changes to `.env`, `*.tfvars`, `id_rsa`, `*.pem` and git-filter-managed (LFS) files are left out; on native Windows everything tracked uploads as is. `CCR_FORCE_BUNDLE=1` forces a bundle. C CW
- CONFIRMED: `claude --teleport` (picker) / `claude --teleport <session-id>`; in-session `/teleport` or `/tp`; `/tasks` then `t`; claude.ai/code Open in > Terminal. C CW
- CONFIRMED teleport needs: clean git state (it offers to stash), same repo (not a fork), branch pushed, same claude.ai account. Handoff is one-way from CLI (cloud to terminal); Desktop can send a local session to cloud via Open in > Cloud (conversation carried as a summary). C CW, C DESK
- CONFIRMED: follow-up from any machine: `claude -p "message" --cloud <session-id>`. C CW
- CONFIRMED: `/web-setup` (inside the CLI, not the shell) sends your `gh auth token` to Anthropic; `/login` with claude.ai needed; API-key or Console sign-in does not work. `--cloud`/`--teleport` unavailable with Bedrock/Vertex-style providers. C WQ, C CW
- CONFIRMED: prefill URL params `prompt` (alias `q`), `prompt_url`, `repositories` (alias `repo`), `environment`. C WQ
- CONFIRMED: `/autofix-pr`, Auto-fix toggle, `/mobile` (QR to app store), `/schedule`. C CW, C WQ, C MOB
- NOT documented here: a `claude cloud` subcommand; any flag to choose permission mode for `--cloud` (mode is picked in the UI dropdown).

## 3. GitHub access model
- CONFIRMED two methods. (a) Claude GitHub App via web onboarding: any public repo, plus private repos the App is installed on. (b) `/web-setup`: any repo your `gh` token can reach, App not needed. C CW
- CONFIRMED: Auto-fix and Projects need the App installed on the repo. Org owners may need to approve installs. C CW, C WQ
- CONFIRMED: Team/Enterprise: an Owner must enable the GitHub connector (Organization settings > Connectors); `/web-setup` hidden until Owner enables Quick setup (Organization settings > Claude Code). C WQ, C CW
- CONFIRMED credential handling (Anthropic-hosted): GitHub credentials stored encrypted on Anthropic servers, never enter the VM; VM holds a short-lived credential scoped to the session; a GitHub proxy swaps it. C CW, C SEC, C DU
- CONFIRMED proxy limits: rejects branch deletion and non-branch pushes (tags); does NOT limit which branches a push can update, so use GitHub branch protection or rulesets (a rule the connected access can bypass will not block the push). API requests only for repos attached to the session (403 otherwise); GraphQL blocked (so `gh pr`/`gh issue` fail; REST via `gh api` works). C CE "GitHub proxy", C SEC
- UNCONFIRMED: a documented per-branch credential. The docs describe session-scoped credentials, not branch-scoped ones. Do not teach "branch-limited token".
- CONFIRMED: `/web-setup` token lives encrypted with your account until removed at claude.ai/customize/connectors (that does not revoke it on GitHub). Token may warn about missing `workflow` scope. C WQ
- CONFIRMED: non-GitHub hosts: only as local bundle, cannot push back; PR creation needs GitHub; GitHub Enterprise Server supported on Team/Enterprise. C CW

## 4. Environments
- CONFIRMED: an environment = saved config (network access, env vars, setup script, network secrets). Onboarding creates `Default` with Limited access, no vars, no script. Edited via the selector at claude.ai/code ("New environment", "Network access", "Setup script", "Environment variables"). C CE
- CONFIRMED network access levels (current names): `None`, `Limited` (default allowlist of package registries, GitHub, cloud SDKs while "Allow package managers" is checked, plus your "Allowed domains", `*.` wildcard), `Full`. Old names `Trusted` and `Custom` map to Limited. (Blog names None/Trusted/Custom/Full: ARTICLE-ONLY, outdated vs docs.) C CE
- CONFIRMED: at every level these still work: GitHub via proxy, enabled MCP connectors (traffic via Anthropic servers), hosts of network secrets, and the Anthropic API even at None. No org-level allowlist can be pushed; use an org-shared environment. C CE, C CW
- CONFIRMED env vars: `.env` format; any command Claude runs can read them; "Anyone who uses the environment can read the values"; docs say use network secrets instead where possible. Vars read at session create and when VM restored. C CE
- CONFIRMED network secrets: key stays outside VM; Anthropic's agent proxy adds it to requests for hosts you list. Not for GitHub, api.anthropic.com or public registries (pypi, npm, crates, go proxy), setup-script requests, telemetry. Unavailable with self-hosted envs or customer-managed encryption keys. C CE
- CONFIRMED setup script: Bash, runs as root before Claude launches, must exit 0, keep under ~5 minutes (else not cached), env vars not yet set when it runs, installs need network (None blocks them). Up to 64 KB. C CE
- CONFIRMED caching: filesystem snapshot after setup; packages, images and files persist; running processes/DBs do not. Rebuilt when script or allowed hosts change or after ~7 days. Not re-run when an idle VM is restored. C CE
- CONFIRMED preinstalled: Python (pip, uv, poetry, pytest), Node 20/21/22, Ruby, PHP, Java 21, Go, Rust, C/C++, Docker, PostgreSQL 16, Redis 7, Chrome for Testing, git, gh, jq. No R, conda or bioinformatics tools are listed; .NET not installed. Ask Claude to run `check-tools`. C CE
- CONFIRMED: SessionStart hooks (from committed settings) run on every session; setup scripts are cloud-only. C CE

## 5. Data and privacy (most important)
- CONFIRMED code storage: repo is cloned into the session VM; "Anthropic stores the session transcript so you can return to the session later"; code and session data follow the retention and usage policies for your account type. C DU
- CONFIRMED all outbound traffic from Anthropic-hosted sessions goes through a security proxy for audit logging and abuse prevention. C DU, C CE
- CONFIRMED training: consumer plans (Free/Pro/Max/Ultra): training only if the setting is on, including Claude Code; commercial (Team, Enterprise, API): not trained on code or prompts unless the customer opts in (e.g. Development Partner Program). C DU
- CONFIRMED retention: consumer 5 years if training allowed, 30 days if not; commercial standard 30 days; ZDR for qualified Enterprise accounts. Deleting a cloud session permanently removes its event data. C DU, C CW
- CONFIRMED: ZDR not included in standard Enterprise; per-organization enablement by Anthropic. C ZDR
- CONFIRMED: with ZDR, cloud sessions (including from Desktop) are disabled at the backend because they need server-side storage of prompts/completions. Same for Remote Control, Claude Tag, /feedback. C ZDR
- CONFIRMED: organizations with HIPAA configuration, or ZDR, cannot use cloud sessions or `/web-setup`; customer-managed encryption keys (CMEK) orgs cannot start cloud sessions. HIPAA coverage is for local mode (CLI, Desktop Code tab). C CW, C WQ, C ZDR
- CONFIRMED security model (Anthropic-hosted): isolated VM per session; network limited by default; credentials outside the sandbox; audit logging; VMs reclaimed after inactivity. C SEC, C CW
- CONFIRMED caveat: with network access None, Claude Code still talks to the Anthropic API, "which may allow data to exit the VM". C CW
- CONFIRMED sharing: Team/Enterprise visibility Private or Team; Pro/Max/Ultra Private or Public (any claude.ai user), repo verification off by default. Docs warn sessions may contain code and credentials from private repos. C CW
- CONFIRMED: Anthropic reads only the repo you start the session in, not other connected repos. C DU
- CONFIRMED: Claude can reply on PRs under your GitHub name (labelled as Claude Code), which can trigger comment-driven automation (Atlantis, Terraform Cloud, issue_comment workflows). C CW
- NOT documented: any guidance specific to genomic, patient, human-subject or controlled-access data (dbGaP, EGA, GDPR) for cloud sessions; no data-residency statement found for cloud sessions. UNCONFIRMED. Teaching inference (ours, not a doc claim): treat the clone, transcript and any pasted data as stored by Anthropic; keep controlled data out of the repo, and ask your data-access committee before any cloud use.

## 6. Plans, limits, labels (time-sensitive)
- CONFIRMED: available on Pro, Max, Ultra, Team; Enterprise only with premium seats or Chat + Claude Code seats; custom roles need a "cloud sessions" permission. C CW
- CONFIRMED: usage counts toward plan limits shared with all other Claude and Claude Code use; no separate VM charge; parallel tasks use limits proportionately. C CW, C WQ
- CONFIRMED: org policy `allow_remote_sessions` must be on (Owner: claude.ai/admin-settings/claude-code). C CW
- UNCONFIRMED: a beta or research-preview label. None appeared on the CW/WQ pages as fetched. Re-check before publishing.

## 7. Limits and failure modes
- CONFIRMED VM ceilings (approximate, may change): 4 vCPUs, 16 GB RAM, 30 GB disk; heavy jobs may be stopped. Docs point to Remote Control (your hardware) or a self-hosted environment. C CE
- CONFIRMED timeouts: foreground command 2 min default, up to 10; then moved to background up to 30 more minutes; SessionStart hook 600 s; env vars `BASH_DEFAULT_TIMEOUT_MS`, `BASH_MAX_TIMEOUT_MS`. C CE
- CONFIRMED idle: VM pauses after a few minutes with files saved, may later be reclaimed. Reopening restores conversation history only; running shell commands, subagents, session-scoped schedules and /loop are lost. Waiting on an MCP approval counts as idle. C CW, C CE
- CONFIRMED: x86_64 only; use x86_64 Linux builds. Interactive SSO unsupported. Docs do not list GPUs.
- NOT documented: GPU, VPN or on-prem network access, mounting local or HPC filesystems, large data upload. UNCONFIRMED; inference from the above: no local DBs/VPN/HPC and 30 GB disk. Mark as inference.
- CONFIRMED: Anthropic-hosted needs GitHub for clone/PR; `claude --cloud` fails on API-key/third-party-provider auth. C CW

## 8. Permission modes in cloud
- CONFIRMED: cloud offers Accept edits (corresponds to `default`), Plan, Auto (unless org disables; greyed on unsupported models). No Manual, no Bypass. C WQ, C PM, C DESK
- CONFIRMED: `defaultMode` `bypassPermissions` and `dontAsk` from settings files are ignored in cloud; `acceptEdits` honoured. Server reviews actions in auto mode on cloud sessions. C PM
- CONFIRMED: mode picked in dropdown at creation and during run; resumed in the same mode after VM reclaim. C CW
- NOT documented here: whether the Bash sandbox of the local CLI is used inside the VM. Docs describe VM isolation plus proxy instead.
- CONFIRMED: "Plan locally, execute in cloud" via `claude --permission-mode plan`, commit and push the plan, then `claude --cloud`. C CW

## 9. OpenCode / Ollama equivalent
- UNCONFIRMED for hosted agent sessions. https://opencode.ai/docs/ (fetched 2026-11-17) describes no hosted/remote agent session; it has `opencode pair` (web UI via one-time local link), Docker images, and OpenCode Console/Go (model access, not session hosting). Ollama: not checked for a cloud-session feature beyond kennel-and-crypt.md. Do not claim an equivalent; self-hosting means your own VM/container.

## 10. ARTICLE-ONLY (paraphrased; official docs agree where tagged)
- Ticket-style prompts: problem, expected result, a command that proves it. Docs only say be specific, name files, paste errors (WQ). Proof-command part ARTICLE-ONLY.
- Push local commits first. Docs CONFIRM.
- Output is a branch to turn into a PR. Docs CONFIRM.
- Parallel sessions each get a machine. Docs CONFIRM.
- Teleport needs clean tree and pushed branch. Docs CONFIRM.
- Env vars visible to everyone using the environment. Docs CONFIRM; docs go further (network secrets).
- Commit as you go because idle VMs are reclaimed: docs CONFIRM reclaim; the "commit as you go" habit is ARTICLE-ONLY (files saved while paused, but not guaranteed after reclaim: inference).
- Narrowest network access that works: ARTICLE-ONLY advice (docs show levels, give no recommendation).
- Keep repo self-sufficient (.claude/, .mcp.json, CLAUDE.md). Docs CONFIRM via "what carries over".
- Plan limits shared, five sessions about five times faster use: docs CONFIRM sharing; the multiplier is ARTICLE-ONLY.
- Local beats cloud for local databases, VPN, GPU, hardware: ARTICLE-ONLY as stated; docs only say local config/tools/environment fit local or Remote Control (WQ) and hardware beyond the limits fits Remote Control.
- Article figures (demo timings, 40 test reruns, 61-72 s runs) are from a fictional repo: do not cite.

## Exact names documented vs not
Documented: `claude --cloud`, `claude --teleport [id]`, `/teleport` `/tp`, `/web-setup`, `/autofix-pr`, `/schedule`, `/tasks`, `claude -p "..." --cloud <id>`, `CCR_FORCE_BUNDLE=1`, `claude auth login`, `allow_remote_sessions`, claude.ai/code, Default environment, None/Limited/Full, "Allow package managers", "Allowed domains", network secrets, agent proxy, GitHub proxy, Quick setup, `check-tools`.
Not documented: beta label, GPU, VPN, data-residency, sensitive-data guidance, per-branch credentials, `claude cloud`.
