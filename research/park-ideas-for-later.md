# Park Ideas for Later: sources

Checked 2026-11-28 against the live pages (fetched as markdown with curl, read by hand). Extends `session-management.md` section 4, which was checked 2026-11-16.

## Confirmed in official docs

- Token costs scale with context size, and Claude Code sends the full conversation with every request. Source: https://code.claude.com/docs/en/costs ("Token costs scale with context size"; "Claude Code sends your full conversation with every request").
- "Clear between tasks": `/clear` for unrelated work, `/rename` before clearing so the session can be found, `/resume` to return. Same costs page, "Reduce token usage".
- `/btw [question]`: side question about the current session without adding to the conversation. `/branch [name]`: copy of the conversation, original reachable with `/resume`. `/subtask <task>`: forked background subagent that inherits the full conversation and returns its result. `/clear [name]`, `/rename`. Source: https://code.claude.com/docs/en/commands
- `/btw` has no tool access and sees the conversation so far (from `session-management.md`, interactive-mode side questions; not re-read on 2026-11-28).
- Auto memory: on by default in local sessions. Asking Claude to "remember that ..." saves to auto memory, and "add this to CLAUDE.md" writes the instructions file. Claude "decides what's worth remembering" and does not save every session. `/memory` lists and opens the files and toggles auto memory. The first 200 lines or 25KB of `MEMORY.md` load at session start. Auto memory is per repository (worktrees of one repository share it). Subagents do not load the main conversation's auto memory. Source: https://code.claude.com/docs/en/memory
- CLAUDE.md is loaded at the start of every session, so its tokens are present in unrelated work. Source: https://code.claude.com/docs/en/costs ("Your CLAUDE.md file is loaded into context at session start") and the memory page.
- `CLAUDE.local.md` holds private per-project preferences and should be gitignored. Source: memory page.
- `/rewind` (aliases `/checkpoint`, `/undo`; `Esc` twice on an empty prompt). A file changed only by Bash commands is not tracked, subagent edits to other files stay, external changes are not tracked, and checkpoints do not replace version control. Source: https://code.claude.com/docs/en/checkpointing
- OpenCode: `/new` (alias `/clear`), `/sessions`, `/undo`, `/redo` on https://opencode.ai/docs/tui/. `AGENTS.md` gives persistent project guidance, loaded from the workspace directory toward the home directory: https://opencode.ai/docs/rules/. The TUI page fetched on 2026-11-28 did not list `/compact`, so the page does not name it.

## Inference (general practice, no official guidance)

- A parking-lot file (`IDEAS.md`), one line per idea with a reason, a trigger and a pointer. Anthropic describes "structured note-taking" (notes persisted outside the context window) in https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents, which the page cites for the practice.
- Keep the file out of the instructions file's imports, and put only a one-line pointer there.
- Where to keep it: in the repository when the team should see it, gitignored when personal, an issue tracker for anything that outlives the week.

## Not verified

- The exact wording Claude uses when it saves a parked follow-up to memory. The page tells the reader to check with `/memory`.
- OpenCode memory features. The page points to its documentation.
- Worktrees and `/rewind` material from the old Capture Ideas Mid-Task page is not reused. It stays covered in `session-management.md`.
