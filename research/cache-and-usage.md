# Prompt cache, breaks and usage: community measurements

Checked 2026-11-20. Third-party material: ideas only, paraphrased on the site, credited. Read through a summarising fetch tool, so numbers are as reported to us and not re-read by hand. Not run here.
Sources:
- R = https://github.com/inevolin/claude-code-usage-analysis (README and FINDINGS.md; MIT licence; author's own "empirical analysis")
- Reddit thread summarising R: a bot-generated TL;DR of about 50 comments, not a primary source. Used only to see which points readers took away. Not linked.
- Official docs on the cache lifetime (about 1 hour on a subscription, 5 minutes on an API key) are already recorded in session-management.md section 1.
Decision fed: the "cache and the break" section of When to Start Fresh, a note in Memory, Sessions and Usage, and a note in Too Many Tools.

## What R is
- LABEL: secondary source, single author, authorship and method not independently checked.
- Not a large corpus study. Live Claude Code runs (one model, medium effort, one CLI version, API key with the 5-minute cache), mostly 1 to 3 runs per condition, plus a simulator for other scenarios.
- Units are "cache-weighted units" (list-price cost relative to the input price). R says these are not a subscription bill, because subscription-limit weights are not published.
- R's FINDINGS.md lists its own limits: the "10x" headline holds only for the 5-minute cache; ratios against a small baseline inflate; most conditions ran once on small tasks; simulator constants are shaky.

## Findings worth teaching (R's numbers, small n)
1. Cache expiry after a pause (5-minute cache, about 97k tokens of history, small next fix): pauses of 2 to 4 minutes cost about 1.5x a brand-new session; pauses of 6 to 13 minutes cost about 9.8x. Scales with history size (only one size measured). Best-supported finding in R.
2. 1-hour cache: R says no cliff until a break passes one hour; its multiplier for that case came from the simulator, not a live run.
3. `/compact` timing: compacting before the break (cache warm) about 2.5x a new session; compacting after the break about 9.7x, no better than just continuing (about 9.9x). n=2 to 3.
4. Mid-session changes: editing CLAUDE.md, adding an MCP server or changing effort left cost near 1x (cache not broken); turning a built-in tool off mid-task cost about 22x a normal turn with 0% read from cache (n=2, R calls it preliminary). Switching models is from Anthropic docs in R, not tested.
5. Long tool output left in chat: about +15% over the next six turns for a 750-token log, about +64% for a 5,000-token log (n=2 each, preliminary).
6. Three quick related fixes in one warm session used about 28% less than three `/clear` sessions (n=1; holds while history stays small, about 20k tokens).
7. Client comparison (n=1): same bugfix, CLI 1.00x, Desktop Code tab 1.80x; Desktop started with more tools loaded (35 vs 14). Treat as a hint.
8. Compaction trigger tuning (`--autocompact`, percentage overrides): live results were mixed and noise-prone; R says its simulator savings are estimates. Not taught on the site.

## Reddit thread (bot summary)
- Takeaways readers drew: cache is 5 min on API key and 1 hour on subscription; after a break prefer `/clear` plus a short hand-written summary; do not toggle tools mid-task; keep build and test logs short (tail them); the Desktop app loads more tools than the CLI.
- Differences from R: the thread says "don't toggle tools" broadly, while R found MCP additions and effort changes harmless and only a built-in tool being turned off costly. The site follows R's narrower version, labelled preliminary.
- Not checked: the UI cache timer (some report seeing it in VS Code), third-party cache-timer tools.

## Site wording rules for this material
- Say "reported" and give the size (a handful of runs) wherever a multiplier appears; round to "about".
- Lead with the official cache lifetimes (docs), then R's measurements as a community example.
- Do not name or recommend third-party mods or apps.
- The hand-written note after a break is the Handoff Notes quest's job; link to it, do not duplicate it.
