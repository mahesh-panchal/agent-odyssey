# Agent transcripts as a place secrets leak (blog post, checked against primary sources)

Prompted by a pasted vendor blog post ("Agent transcripts are the new .env", Evgeniy Pats, 2026-11-20; it ends with a pitch for the author's own product, which we do not cite or name). Checked 2026-11-23 by two fetch subagents. Fetch tools return model-extracted views, so quotes are short and some are from summaries (marked). Used by `zones/safe-editing/keep-secrets-out-of-reach.qmd`.

## Claude Code docs (CONFIRMED unless marked)
- https://code.claude.com/docs/en/claude-directory : "If a tool reads a `.env` file or a command prints a credential, that value is written to `projects/<project>/<session>.jsonl`." Also: "Anything that passes through a tool is written to a transcript on disk: file contents, command output, pasted text." `cleanupPeriodDays` default 30, minimum 1. `CLAUDE_CODE_SKIP_PROMPT_HISTORY` skips transcripts and prompt history. `claude purge` deletes the state held for one project.
- https://code.claude.com/docs/en/settings : choosing "Yes, and don't ask again" for a Bash command saves an `allow` rule in `.claude/settings.local.json`. On first write in a git repository, Claude Code adds `**/.claude/settings.local.json` to the global git excludes file; "if you create it by hand, add it to `.gitignore` yourself".
- https://code.claude.com/docs/en/permissions : the saved rule is a pattern (example prompt "Yes, and don't ask again for: npm test *"), not necessarily the literal command. Deny rules for Read "don't apply to arbitrary subprocesses that read or write files indirectly, like a Python or Node script that opens files itself". (Page partly summarised.)
- https://code.claude.com/docs/en/cli-reference : `claude purge` flags `--dry-run`, `--yes`, `--interactive`, `--all`. `CLAUDE_CODE_SKIP_PROMPT_HISTORY` env var: verbatim on claude-directory and cli-reference; env-vars page (summary).
- https://code.claude.com/docs/en/data-usage : transcripts stored locally in plaintext for 30 days by default.
- NOT CONFIRMED: the blog's claim that a password typed into a command ends up in the saved rule. The docs show prefix patterns; the blog cites a user issue from August 2025 that we did not read. Taught as "reported", with the advice to reference secrets as variables.

## Incident (CONFIRMED, read in full)
- https://cursor.com/blog/security-incident-update (2026-11-13): an access key issued to a vendor was exposed; a bucket held "limited coding agent traces, mostly from 2025, from sessions not in Privacy Mode"; "A small number of those traces contained credentials that had not been redacted". Malicious copies of a Claude Code extension were placed on the cache serving the marketplace; "At most 5,000 users ... potentially received the malicious build" in about 11 hours.
- https://cursor.com/blog/claude-code-extension-security-notice (2026-10-29): the malicious build tried to install an SSH backdoor.
- NOT FOUND: the blog's Notion advisory (Notion blog page 1 and security page checked). Not used.

## Other
- https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app-installation : "The installation access token will expire after 1 hour." (verbatim)
- NOT CONFIRMED: Codex session path `~/.codex/sessions` (not on the pages read); `codex exec --ephemeral` and `history.persistence` seen only in summaries of learn.chatgpt.com pages. Not used in the course.
- Not checked: the AWS and Google Cloud short-lived credential claims; the blog's Nx and Shai-Hulud claims.
