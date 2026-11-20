# LLM-maintained wiki (Karpathy "LLM Wiki" gist)

Read 2026-11-20 by a fetch subagent; used by `zones/codon-mill/llm-wiki.qmd`. Labels: (a) the source states it, (c) our inference.

## Source
- https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f : Andrej Karpathy, gist file `llm-wiki.md`, created 2026-04-04, one revision. The body was read in full from the raw file (about 11,900 characters, not truncated). The comments under the gist (third-party, several promoting their own products) were not evaluated and are not used.
- (a) Subtitle: "A pattern for building personal knowledge bases using LLMs." Described as an "idea file" to give to an agent (Codex, Claude Code, OpenCode named); it says it describes the idea, not an implementation.
- (a) Contrast with RAG: RAG rediscovers knowledge on every question and nothing accumulates. The wiki is "a persistent, compounding artifact".
- (a) Three layers: raw sources (immutable, source of truth), the wiki (LLM-generated Markdown, owned by the LLM), the schema (CLAUDE.md or AGENTS.md; user and LLM co-evolve it).
- (a) Operations: ingest (one source may touch 10 to 15 pages; the author prefers one source at a time with involvement), query (answers with citations; good answers filed back as pages), lint (contradictions, stale claims, orphans, missing pages and cross-references, gaps).
- (a) `index.md` (catalogue read first; "works surprisingly well at moderate scale (~100 sources, ~hundreds of pages)" per the author) and `log.md` (append-only, consistent entry prefix so `grep` works).
- (a) Tooling named: Obsidian ("Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase"), Obsidian Web Clipper, graph view, Dataview, Marp, attachment-folder setting and a download-images hotkey (image handling called clunky), git, and `qmd` (https://github.com/tobi/qmd, local Markdown search with hybrid BM25 and vector search; named in the gist, NOT read by us).
- (a) Use cases listed: personal, research, reading a book, business or team, competitive analysis, due diligence, trip planning, course notes, hobby deep-dives.
- (a) Rationale: the bottleneck of keeping a wiki is bookkeeping; the LLM "doesn't get bored" and can touch many files in one pass.

## More gist details used on the page (all from the raw file, per the fetch report)
- (a) The schema is called "the key configuration file". The index "avoids embedding-based RAG infrastructure" at moderate scale, per the author. The author prefers one source at a time and says batch ingest with less supervision is also possible.
- (a) Obsidian tools: Web Clipper (web articles to Markdown), graph view ("the best way to see the shape of your wiki"; hubs and orphans), Dataview (queries page frontmatter if the LLM adds YAML), Marp (slide decks from Markdown, with an Obsidian plugin). Images: set the attachment folder, bind a hotkey for downloading attachments; "LLMs can't natively read markdown with inline images in one pass", so read the text first, then view images separately; the author calls the handling a bit clunky.
- Our own one-line glosses of what each Obsidian tool does are General practice (Obsidian docs not read).

## Our own additions on the page (not from the gist)
- (c) The bioinformatics use-case table, the sizing questions, the example schema, the layout, the read-only `raw/`, the separate agent folder, commit-per-ingest, the risk list (compounding mistakes, prompt injection in clipped pages, privacy, cost, scale, hollow learning). Not tested; no wiki was built for this page.
- (c) "Obsidian vault is a folder of Markdown files" is general knowledge; Obsidian's docs were not read.
- NOT CONFIRMED: how well small local models handle multi-file ingest; whether the index approach holds beyond about 100 sources; qmd.

## Also used
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents : see `research/rag.md` section 4.
