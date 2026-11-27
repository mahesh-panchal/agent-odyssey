# Carry Context Between Sessions: sources and status

Written 2026-11-28 for the new side quest `zones/prompts-and-context/carry-context-between-sessions.qmd`. The page re-splits the old Handoff Notes, When to Start Fresh and Memory, Sessions and Usage pages. Claims were reused from `research/session-management.md` (checked 2026-11-16) and `research/cache-and-usage.md`. The official docs pages were NOT re-fetched on 2026-11-28; only the harness article URL was checked for existence (HTTP 200, title "Effective harnesses for long-running agents").

## Lore URLs
- https://code.claude.com/docs/en/memory : CLAUDE.md versus auto memory, per-repository auto memory, `/memory`, `CLAUDE.local.md` loads after CLAUDE.md, memory is context not enforced configuration (session-management.md section 3).
- https://code.claude.com/docs/en/sessions : `/clear`, `/resume`, `claude --continue`, `/rename`, what a resumed session restores (messages, model, permission mode; `--mcp-config` passed again) (session-management.md sections 1 and 2).
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents : progress file, descriptive commits "so bad changes can be reverted", start-of-session routine (read git log and progress file, run a basic test before new work). Summary-tool read recorded in session-management.md section 3.
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents : structured note-taking outside the context window; context rot.
- https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html : names context poisoning and distraction (community blog).

## Commands on the page (from session-management.md; not re-run)
`/memory`, `/clear` (alias `/new`), `/clear <name>`, `/compact [focus]`, `/resume`, `claude --resume [name]`, `claude --continue`, `/rename`, `/rewind`, `/export` (plain text for a person to read). OpenCode: `/new` (alias `/clear`), `/sessions` (aliases `/resume`, `/continue`), `/compact` (alias `/summarize`), `/export`.

## Our own practice (inference, not official)
Handoff note contents, the mock note, the restatement prompt, "write the note before `/clear`", and the decision table. session-management.md records that no official page prescribes a handoff-file template.

## Unverified on this date
Retention of old transcripts and the 200-line limit of `MEMORY.md` were left out of this page. "Context poisoning" is community vocabulary, not a documented Claude Code term.
