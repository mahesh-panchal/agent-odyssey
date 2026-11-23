# Keep a Paper Trail: sources and status

## Our own teaching practice
The four-step routine (ask, check against ground truth, explain back one sentence per point, keep/edit/revert), the prompt template, the "which document for which moment" table and the habit "agent drafts, you check against ground truth and own the why" are this course's own teaching practice. No source claims them. The worked changelog example (`gc_filter.py` diff and changelog) and the mock ADR (filter as a script) are mock content written for the course; the omitted threshold and the overstated "added tests" are constructed on purpose.

## Pages fetched 2026-11-23 (WebFetch tool, which returns a model-written summary of the page, not the raw text; all three are summaries)
- https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions : Michael Nygard, "Documenting Architecture Decisions". Relied on: ADR sections title, status, context (value-neutral forces), decision ("We will ..."), consequences (all, not just positive); short records, kept in version control next to the code. Our fourth ADR part, "alternatives considered", comes from common ADR templates generally, not from this post.
- https://adr.github.io/ : ADR GitHub organisation home. Relied on: an ADR captures a single architectural decision and its rationale; a project's ADRs form a decision log; the page links to templates. It did not list templates in the summary.
- https://keepachangelog.com/en/1.1.0/ : Keep a Changelog 1.1.0. Relied on: changelogs are for humans; one entry per version, newest first; dumping git logs is poor practice because commit logs are noisy.

## Plain facts used (standard git, not run here)
`git diff` shows changes to tracked files not yet staged; `git diff --stat` summarises files and line counts; `git log -p` shows history with diffs; `git status` lists untracked files.

## Lore URLs
Fetched above (new here): cognitect.com ADR post, adr.github.io, keepachangelog.com. Already in research/*.md and reused: https://code.claude.com/docs/en/best-practices , https://aiforscience.eu/best-practices/07-provenance-and-citation/ , https://aiforscience.eu/best-practices/09-human-in-the-loop/ .
