# OpenCode and Ollama route (Recruit the Beast, Prerequisites)

Read 2026-11-26 by a web-fetch agent (summaries, quotes short) and checked against the local install (OpenCode v2.4.1, Ollama 0.40.18).

- https://opencode.ai/docs/ : install methods. macOS and Linux: `curl -fsSL https://opencode.ai/v2/install | bash`. The page says Windows package managers are not supported; Windows is a standalone zip.
- https://opencode.ai/docs/providers/ : Ollama needs no /connect; OpenCode probes http://127.0.0.1:11434 and adds the models it finds to /models. Model ids look like `ollama/<name>`.
- https://opencode.ai/docs/agents/ : the plan agent "explores and plans without editing normal project files"; shell commands remain permission-controlled. The build agent is the default.
- https://opencode.ai/docs/permissions/ : base policy allows everything except reading `.env` files (ask); last matching rule wins.
- https://docs.ollama.com/quickstart , https://docs.ollama.com/context-length , https://docs.ollama.com/macos , https://docs.ollama.com/linux , https://docs.ollama.com/windows : install paths (macOS .dmg, Linux script, Windows OllamaSetup.exe); agents and coding tools should use at least 64000 tokens of context; the default depends on VRAM (4k under 24 GiB).

RUN 2026-11-26 (local): `opencode --version` (v2.4.1), `opencode models` (lists `ollama/<name>` entries found automatically), `opencode debug paths`, `ollama --version`, `ollama ps`. `opencode run --agent plan -m ollama/ministral-3:8b "Create a file called made-by-plan.txt ..."` in a scratch folder: the agent declined and no file appeared.

NOT FOUND in the docs: the key or command to switch to the plan agent inside the interface (the lesson uses `opencode run --agent plan`); `/init`; a Homebrew cask for Ollama. NOT RUN: Windows, Linux, the Ollama install steps themselves, `qwen3:4b` (not pulled locally), the full interface.

## Test the Leash, OpenCode route (2026-11-26)

Sources read (web-fetch agent, summaries): https://opencode.ai/docs/permissions/ , https://opencode.ai/docs/agents/ , https://opencode.ai/docs/config/ , https://opencode.ai/docs/keybinds/ , https://opencode.ai/docs/tui/ . Interactive prompt choices: Allow once, Allow always, Reject (permissions page). `Shift+Tab` cycles agents (keybinds page). V2 rule fields are `action`, `resource`, `effect`; last matching rule wins. The pages read mention no operating-system sandbox; /docs/security and /docs/sandbox return 404. The docs warn that `shell` runs with the host user's filesystem, process and network authority.

RUN locally with `opencode run -m ollama/ministral-3:8b` in scratch folders (OpenCode v2.4.1):
- `edit` rule `ask` plus a write prompt: "This non-interactive run cannot ask the user for permission, so the request was rejected"; no file written.
- `--agent plan` asked to create a file: declined, no file.
- `read` deny on `*.env`: read tool gave "Permission denied: read"; `cat .env` through the shell printed the file. Adding `shell` deny on `cat *` gave "Permission denied: shell"; `python3 -c "print(open('.env').read())"` still printed the file.
- Docker 29.9.3: `docker run --rm --network none -v <folder>:/project -w /project bash:5 ...` showed a different root filesystem, "bad address" for a download, and a file written into the mounted folder. The lesson uses `python:3.11`, which was not pulled; `curl` there is not run.

NOT RUN: the interactive prompt and `Shift+Tab` (needs the full interface), `qwen3:4b` (not pulled; the lesson's example model), Windows, Linux.

Secrets page, OpenCode note (2026-11-26): `opencode session list|delete|export` exist (`opencode session --help`); the local `opencode.db` has session, message and part tables (table names only were listed). "Allow always" saving project allow rules is from the permissions page (summary). Default retention of OpenCode sessions was NOT found.
