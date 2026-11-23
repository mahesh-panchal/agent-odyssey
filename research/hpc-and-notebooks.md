# HPC safety and notebooks with coding agents

Checked 2026-11-16. Official docs fetched via a summarising fetch tool (quotes as returned). Nothing run against a model or cluster.
Base: C = https://code.claude.com/docs/en/ ; O = https://opencode.ai/docs/ ; S = https://slurm.schedmd.com/
Decision fed: accuracy of quest text on HPC and notebook safety. "GENERAL PRACTICE" = not stated in any doc fetched; treat as advice, not fact.

## A1. Slurm commands (official)
- CONFIRMED: sbatch "is used to submit a job script for later execution"; srun "to submit a job for execution or initiate job steps in real time"; squeue "reports the state of jobs or job steps"; scancel "to cancel a pending or running job or job step"; sinfo reports partitions and nodes. S quickstart.html (2026-11-16)
- CONFIRMED: sbatch "exits immediately after the script is successfully transferred to the Slurm controller and assigned a Slurm job ID". Default time limit "is the partition's default time limit". `--test-only` validates and estimates start, "No job is actually submitted". `--parsable` prints only the job ID. S sbatch.html
- CONFIRMED: "If necessary, srun will first create a resource allocation in which to run the parallel job." So srun outside an allocation requests resources and (by default) runs synchronously. S srun.html (first 100k of 175k chars read; `--pty` entry not read)
- CONFIRMED: scancel "is used to signal or cancel jobs, job arrays or job steps"; filters `-u/--user`, `-t/--state`, `-n/--name`, `-p/--partition`; combined filters must all match. Without `--signal` the whole job is terminated (SIGCONT, SIGTERM, then SIGKILL after KillWait). S scancel.html
  - Teaching point: `scancel -u <me>` kills all of the user's jobs, not just the agent's. Prefer `scancel <jobid>` for IDs the agent itself submitted.
- CONFIRMED: Slurm can rate-limit RPCs per user (token bucket, since 23.02): short bursts allowed, "a sustained high rate of requests" restricted. S high_throughput.html. The page says nothing about polling squeue or job arrays vs many sbatch calls.
- CONFIRMED (absence): Slurm quickstart says "All of the commands can run anywhere in the cluster" and does not define login nodes. No official Slurm page fetched covers login-node etiquette. S quickstart.html

## A2. Login node vs compute node (GENERAL PRACTICE)
- UNCONFIRMED by Slurm docs; widely stated in site user guides. Login nodes are shared by all users; heavy work goes through sbatch/srun on compute nodes. Check your own site's docs and cite them in the quest.
- GENERAL PRACTICE, agent must not do on a login node: run pipelines or tools in the foreground (aligners, `nextflow run` as a long process unless site allows a head job), compress/index big files, `find /` or recursive `grep -r` over project/scratch trees, `du -sh` over millions of files, loops that call `squeue` every second, `watch squeue`, build large conda envs, run Jupyter or the agent's test suite at scale.
- GENERAL PRACTICE, OK on a login node: edit text, `git`, `ls` of one dir, `squeue -u $USER`, `sbatch`, `scancel <id>`, `head`/`tail`/`wc` on a log, `sinfo`.
- GENERAL PRACTICE: use `sbatch` for batch work, `srun --pty` or `salloc` for interactive debugging, always set `--time`, `--mem`, `--cpus-per-task`. Use job arrays rather than looping `sbatch` (array vs loop load not covered by the Slurm page above).
- Repo note: a local skill `hpc-cluster-safety` already exists in this environment; reuse its rules for quest text rather than inventing new ones.

## A3. Shared filesystems (GENERAL PRACTICE)
- UNCONFIRMED in official docs: network filesystems (Lustre, GPFS, NFS) degrade for everyone under metadata-heavy load (huge directory listings, `find`, `grep -r`, many small files). Agents explore by grep/glob, so scope searches to one subdirectory; never start at `/`, `$HOME` or a whole project root.
- CONFIRMED: Claude Code runs its own file tools (Glob, Grep, Read) and bundled ripgrep; Read of a notebook over 256 KB errors and over 100 MB is refused. C tools-reference (a Read cap, not a filesystem-load control)
- CONFIRMED: Claude Code keeps sessions, settings, plugins in `~/.claude`; `CLAUDE_CONFIG_DIR` relocates them ("stores your settings, session history, and plugins there instead"). Also writes `~/.claude.json` (account details, MCP configs, trust decisions). C settings
- GENERAL PRACTICE inference: if `$HOME` is shared/NFS-mounted across nodes, session history and transcripts (which can contain pasted data or paths) live on shared storage. Check permissions (`chmod 700 ~/.claude`) and whether home is backed up or readable by group. Not stated in docs.

## A4. API keys and settings
- CONFIRMED: `ANTHROPIC_API_KEY` is sent as `X-Api-Key`; when set it overrides a subscription login; in `-p` mode it is always used; interactive mode asks once to approve. C env-vars
- CONFIRMED: settings files: user `~/.claude/settings.json`, project `.claude/settings.json` (commit it), local `.claude/settings.local.json` (kept out of git when Claude creates it; add to `.gitignore` if created by hand), managed. Precedence: managed > command line > local > shared project > user. Permission lists merge across files. C settings
- CONFIRMED: `deny` precedes `ask` precedes `allow`; first match wins. Example in docs: `"deny": ["Read(./.env)", "Read(./.env.*)"]`. C settings, C permissions
- CONFIRMED: sandbox default reads cover "Most of the machine, including credential files such as `~/.ssh` and `~/.aws/credentials`". Use `Read(...)` deny rules or `sandbox.filesystem.denyRead` for key files. C sandboxing
- CONFIRMED: sandbox settings include `credentials.files` / `credentials.envVars` keys (purpose not read in detail). UNCONFIRMED what they do. C sandboxing
- GENERAL PRACTICE: never put a key in a script or `.claude/settings.json` that is committed; for shared accounts prefer a per-user key from a file with mode 600, not a lab-wide key in a shared dir. The `apiKeyHelper` setting is named in the settings page; its behaviour was not read. UNCONFIRMED.
- OpenCode: UNCONFIRMED where it stores keys (global config path not given on the permissions page). O permissions

## A5. Claude Code sandbox on Linux
- CONFIRMED: "The sandbox runs on macOS, Linux, and WSL2. On native Windows, Claude Code runs commands unsandboxed." C sandboxing
- CONFIRMED: Linux needs packages `bubblewrap` (filesystem isolation) and `socat` (network relay): `sudo apt-get install bubblewrap socat` or `dnf`. Ripgrep is bundled. Seccomp filter optional (Unix-socket blocking). C sandboxing
  - Teaching point: on a cluster you typically cannot `sudo`; a site must provide bwrap/socat or the sandbox cannot start. Whether bwrap works under a cluster's user-namespace policy is UNCONFIRMED (site-specific).
- CONFIRMED: fail-open by default: if unsupported or the dependency check fails, "Claude Code runs commands without sandboxing"; set `sandbox.failIfUnavailable: true` to exit instead. C sandboxing
- CONFIRMED: sandbox covers shell commands only; "Claude's file tools, MCP servers, and hooks run outside it". Writes allowed to working dir, per-user temp dir, added dirs. C sandboxing
- CONFIRMED: Claude can retry a failed command with `dangerouslyDisableSandbox` unless `allowUnsandboxedCommands` is `false`. `excludedCommands` run with no filesystem or network restrictions. C sandboxing
- CONFIRMED: plain `ssh`, most database drivers and UDP tools ignore the proxy and cannot reach allowed hosts. So `ssh cluster` from inside a sandbox does not work as a hop; run Claude Code on the cluster or outside the sandbox. C sandboxing
- CONFIRMED: `bypassPermissions` "Only use this mode in isolated environments like containers or VMs"; disable with `permissions.disableBypassPermissionsMode: "disable"`. C permissions
- CONFIRMED: sandbox does not run Docker; `docker` needs `excludedCommands`. Apptainer/Singularity not mentioned; UNCONFIRMED.

## A6. Network egress from compute nodes
- GENERAL PRACTICE / UNCONFIRMED: many sites give compute nodes no or restricted internet; login nodes often have it. An agent running on a compute node may not reach the model API. Typical pattern: agent on login node or laptop, writes scripts, submits jobs; jobs run offline with pre-staged containers/data. Ask your site.
- CONFIRMED: sandbox proxy checks each host against `network.allowedDomains` (starts empty); outside the list: prompt in manual/acceptEdits, refused in `dontAsk`, allowed without prompt in `bypassPermissions`. `deniedDomains` refused in every mode. C sandboxing
- CONFIRMED: `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` disables auto-updates, telemetry, error reporting and feedback traffic; useful on restricted networks. C env-vars. Proxy variables (`HTTPS_PROXY`) rows not read: UNCONFIRMED here.

## A7. Cost and rate of many cluster commands
- CONFIRMED: Claude Code "charges by API token consumption"; average about $13 per developer per active day, $150-250 per month, under $30 per day for 90% of users (enterprise averages). C costs
- CONFIRMED: full conversation is sent with every request, each tool use sends another request; long sessions cost more; verbose tool output (logs) inflates context. Docs example: a hook that greps `ERROR` from a log "reducing context from tens of thousands of tokens to hundreds". C costs
- CONFIRMED: `BASH_DEFAULT_TIMEOUT_MS` default 120000 (2 min), `BASH_MAX_TIMEOUT_MS` default 600000 (10 min) for foreground commands. So foreground commands over 10 min are cut off by default; an agent waiting on `srun` or a polling loop hits this. C env-vars
- CONFIRMED: scheduled/looped tasks "fire on its interval even while the session is idle, sending your full context each time". Do not `/loop` a squeue poll. C costs
- Scheduler side: no doc found that quantifies a safe squeue polling rate; Slurm RPC rate limiting exists (A1). GENERAL PRACTICE: poll at minutes, not seconds; use `sacct` or job output files instead.

## A8. Policy and data agreements (GENERAL PRACTICE)
- UNCONFIRMED by docs: check institutional policy before sending cluster data, paths, logs or code to an external model API. Human genomic, clinical or controlled-access data (dbGaP, EGA-style agreements) often forbids third-party processing. Agent reads file contents into the model context; Read of any file within the working dir needs no approval (C permissions: file reads and Grep "No, within the working directory").
- CONFIRMED: Read is auto-approved inside the working dir and added dirs, so a project dir with controlled data is readable by the agent unless a `Read(...)` deny rule or `sandbox.filesystem.denyRead` covers it. C permissions, C sandboxing
- CONFIRMED: organisations can enforce managed settings that user files cannot override. C settings
- GENERAL PRACTICE: keep controlled data outside the agent's working dir; give the agent synthetic or de-identified test data; ask the data owner and cluster admins first.

## A9. Should the agent submit jobs? Permission rules
- CONFIRMED: Bash rules: `Bash(sbatch *)` in `ask` forces a prompt; deny > ask > allow; an ask rule prompts even if a narrower allow matches. C permissions
- CONFIRMED: ask/deny apply to any subcommand of a compound command (`&&`, `||`, `;`, `|`, `&`, newlines), including in `for` loops and `$(...)`. C permissions
- CONFIRMED limit: Bash deny/ask rules "isn't a security boundary": `Bash(rm *)` does not stop `/bin/rm` or `bash -c 'rm ...'`; `Bash(git push *)` does not stop `git -C . push`. For enforcement use sandboxing or a PreToolUse hook. C permissions
- CONFIRMED: allow rules are not stripped past env-var wrappers or runners such as `docker exec`, `npx`: write exact inner-command rules. `timeout`, `nice`, `nohup`, `time`, `stdbuf` are stripped. C permissions
- Suggested teaching config (derived from the above, not copied from docs):
  - allow: `Bash(squeue *)`, `Bash(sinfo *)`, `Bash(sacct *)`
  - ask: `Bash(sbatch *)`, `Bash(srun *)`, `Bash(salloc *)`, `Bash(scancel *)`
  - deny: `Bash(scancel -u *)` (and `scancel --user*`), though bypassable per the caveat above
  - Teach: review the script and resource request (`--time`, `--mem`, array size) before approving `sbatch`; `--test-only` is a dry run.
- OpenCode: CONFIRMED values `allow`, `deny`, `ask`; unmatched action = `ask`; ordered rules in `opencode.jsonc`, e.g. `{ "action": "shell", "resource": "git push *", "effect": "deny" }` (V2 name `shell`, V1 `bash`); `policies` key for hard denials. BUT default base policy starts with `{ "action": "*", "resource": "*", "effect": "allow" }` (only `.env` reads ask), and "no rule asks for `external_directory`". So OpenCode needs explicit `ask` rules for sbatch. O permissions (page version appears to be V2; check your installed version)

## B1. Why .ipynb reviews poorly
- CONFIRMED: notebook is a JSON document (`metadata`, `nbformat`, `nbformat_minor`, `cells`); `display_data` stores `image/png` as base64; code cells carry `execution_count` and metadata. Source/output strings may be stored as lists of strings. https://nbformat.readthedocs.io/en/latest/format_description.html (2026-11-16)
- Derived: a one-line code change also changes `execution_count`, outputs and embedded base64 images, so git diffs are dominated by JSON noise. Not stated as such in the docs.

## B2. Tools
- CONFIRMED nbstripout: "strips output and some metadata"; keeps outputs on disk, only Git sees the cleaned version. `nbstripout --install` writes the filter to `.git/config` and attributes to `.git/info/attributes`; `--attributes=.gitattributes` to version the attributes. Git cannot set up filters on clone ("by design"), so each collaborator must run it. Limits: conflicts on pull/merge with non-stripped local changes; pre-commit mode modifies working copy. https://github.com/kynan/nbstripout
- CONFIRMED jupytext: stores notebooks as Markdown or scripts for "clear and meaningful diffs when doing version control"; `py:percent` recommended for code; paired notebooks = `.ipynb` + `.py` of the same notebook, outputs stay in `.ipynb`, `.py` holds inputs. https://github.com/mwouts/jupytext (the readthedocs pages returned empty; README only)
- CONFIRMED nbdime: `nbdiff` (terminal), `nbdiff-web` (browser), git integration via `nbdime config-git --enable --global`, merge driver keeps conflicted notebooks valid, `nbdime mergetool`. https://nbdime.readthedocs.io/en/latest/
- CONFIRMED marimo: "Every marimo notebook is stored as pure Python (Git-friendly)"; reactive execution: "Delete a cell and marimo scrubs its variables from program memory, eliminating hidden state"; run as script with `python your_notebook.py`; convert: `marimo convert your_notebook.ipynb > your_notebook.py`. https://docs.marimo.io/
- UNCONFIRMED: whether marimo's `.py` stays fully deterministic when cells have side effects; and marimo-specific agent integration (not researched).

## B3. Claude Code and notebooks
- CONFIRMED: `NotebookEdit` "modifies a Jupyter notebook one cell at a time, targeting cells by their `cell_id`"; modes `replace` (default), `insert`, `delete`; not string replacement; refuses non-UTF-8 files; requires permission (listed "Yes"). C tools-reference
- CONFIRMED: permission rules use the `Edit(...)` path format; `Edit(notebooks/**)` covers NotebookEdit. C tools-reference
- CONFIRMED: replacing a code cell clears its execution count and saved outputs; to get outputs back, re-run the cell and dependents. C tools-reference
- CONFIRMED: Read on `.ipynb` returns all cells with outputs (code, markdown, visualizations); error if cells exceed 256 KB or the token limit; notebook over 100 MB refused. Notebooks need a prior read on every model. C tools-reference
- Derived (matches the above): agent never executes cells via NotebookEdit; outputs it edits are stale or empty until a human or `jupyter nbconvert --execute` re-runs. Reading output-heavy notebooks floods context (see A7). Strip outputs before pointing an agent at a notebook (nbstripout) or give it the jupytext `.py`.

## B4. Review and reproducibility (GENERAL PRACTICE unless cited)
- Review agent-edited notebooks as text: pair with jupytext `.py` or use `nbdiff`; review the diff of source cells only; check `git diff --stat` for stray outputs/images.
- Reproducibility: Restart Kernel and Run All, top to bottom, before commit; out-of-order cells and deleted cells leave hidden state in the kernel (marimo's design removes this per its docs, B2). An agent that replaces a cell clears outputs (B3), so a green-looking notebook can be stale.
- Run headless in CI or a cluster job, not an interactive Jupyter on the login node (see A2).
- Pin environments: container or lockfile; the agent should not `pip install` into a shared env.

## A6. Maintainer-authored HPC skill (read 2026-11-17)
Source: https://github.com/NBISweden/claude-skills/pull/10 , file `plugins/nbis-safety/skills/hpc-cluster-safety/SKILL.md`. This is the site owner's own practice (a maintainers' skill, not vendor docs). Nothing run. Quest text treats it as "General practice" unless a Slurm man page below confirms it. Site names in the source are deliberately not repeated; the quests stay generic.
- Maintainers' practice (General practice): agents on login nodes may be barred by site policy (then use an interactive compute allocation; ask staff); scope filesystem operations (no broad `find`/`du`/`ls --recursive`/`grep --recursive`, no `ls --format=long` or wide globs on big directories, avoid many small files); poll no faster than about once a minute, one loop, scoped; prefer `sbatch --parsable --wait` or the pipeline's poller; never resubmit because a wait timed out, check `State` with `sacct`; arrays with a concurrency cap; ask where scratch is, not `/tmp`, `$TMPDIR` set proves nothing; stay inside the project's paths; do not assume Slurm; compare request, allocation and use with `sacct`; `rsync --dry-run --itemize-changes` before copy, list before `rm`, large transfers via scheduler or a data-transfer node; stricter project instructions (AGENTS.md) win over the skill; prefer long options; do not trust "a few seconds", ask.
- CONFIRMED (Slurm man pages, read 2026-11-17, version shown on page 26.05):
  - squeue.html: running it "from loops" can degrade `slurmctld` (possible denial of service); `--user` and a single job ID via `--jobs` improve performance on large systems.
  - sacct.html: "Do not run sacct or other Slurm client commands that send remote procedure calls to slurmdbd from loops." States include `OUT_OF_MEMORY` ("Job experienced out of memory error"); ExitCode has the signal number after a colon.
  - sbatch.html: `--parsable` prints only the job ID (and cluster name if present). `--wait`: "Do not exit until the submitted job terminates"; sbatch's exit code equals the job's; signal-terminated gives 1; arrays give the highest task code. `--array=0-15%4` limits simultaneous tasks to 4. `--mem-per-cpu` above `MaxMemPerCPU` is reduced and `--cpus-per-task` is raised to compensate (the page also notes `--mem` handling; the exact `--mem` above CPUs x limit behaviour and the 0:125 / 137 exit codes were not confirmed on these pages: UNCONFIRMED, treated as maintainers' practice).
  - scancel.html: other bulk selectors besides `--user`: `--me` ("jobs owned by the current user"), `--name`, `--state` (PENDING, RUNNING or SUSPENDED), `--partition`, also `--account`, `--qos`, `--reservation`, `--wckey`, `--nodelist`; combined filters must all match. The page does not say which version added `--me`.
- NOT CHECKED: `scontrol show partition`, `MaxMemPerCPU`, `TRESBillingWeights`, `EnforcePartLimits` claims (scontrol/slurm.conf pages not fetched).


## Status of the source skill (2026-11-23)
The maintainer reports that the hpc-cluster-safety skill (https://github.com/NBISweden/claude-skills/pull/10) is their own work, adapted from their own skill, and has been merged into the NBIS skills. Not re-checked on GitHub by us; re-compare the Citadel quests with the merged file if its content changed in review.
