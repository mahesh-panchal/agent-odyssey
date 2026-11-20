# Mistral (hosted, Vibe CLI, open-weight models via Ollama)

Read 2026-11-20 by a research subagent. Method: WebFetch returns a model-extracted view of each page, not raw HTML; items marked (search) are from search-result summaries only and the page itself was not read. Labels: CONFIRMED = read on the page; NOT CONFIRMED = not found or not read. Used by `zones/basecamp/know-your-gear.qmd`, `zones/kennel/adopt-the-pet.qmd`, `zones/kennel/pick-your-companion.qmd`, `zones/crypt/secrets-and-sensitive-ground.qmd`, and the two RAG quests.

## 1. Mistral Vibe CLI
- https://github.com/mistralai/mistral-vibe : "Mistral Vibe is an open-source coding agent for your terminal." Apache 2.0. Install on macOS and Linux: `curl -LsSf https://mistral.ai/vibe/install.sh | bash`, or `uv tool install --python 3.14 mistral-vibe`. Needs Python 3.12 or later. Version and date NOT CONFIRMED on this page.
- https://docs.mistral.ai/mistral-vibe/introduction : commands `vibe` and `vibe-acp`; first run starts a sign-in or API-key wizard (`vibe --setup` repeats it); keys in the OS keyring or `~/.vibe/.env`, or `MISTRAL_API_KEY`; config file `~/.vibe/config.toml`.
- https://docs.mistral.ai/vibe/code/cli/offline-models : "supports any model served behind an OpenAI-compatible API"; lists vLLM (recommended), llama.cpp, LM Studio and Ollama; built-in `llamacpp` preset at `http://127.0.0.1:8080/v1`; custom setup through `[[providers]]` and `[[models]]` tables, `active_model`; `/model` switches. NOT CONFIRMED: an Ollama-specific recipe (the page gives none); the server must stream token usage (`stream_options.include_usage`).
- Instruction file `AGENTS.md`, user-level `~/.vibe/AGENTS.md`, nearest file wins: (search) summary of https://docs.mistral.ai/vibe/code/cli/agents; page not read.
- https://docs.mistral.ai/vibe/code/safety-approvals-permissions : modes `ask`, `accept-edits` (default; auto-approves file edits, still asks for shell commands), `smart-approve`, `auto-approve` ("Trusted, sandboxed environments only"; needs `--auto-approve` or `--yolo`). Programmatic mode denies every call that needs approval. Trusted folders: project config is loaded only from folders you trusted (`~/.vibe/trusted_folders.toml`). Per-tool allow/ask/deny with bash allow and deny lists. The overview (https://docs.mistral.ai/vibe/code/overview) says "By default, it applies file edits without asking."

## 2. Models
- https://docs.mistral.ai/getting-started/models/models_overview/ : active entries include Mistral Small 4 (v26.03, Apache 2.0), Mistral Large 4 (v26.10, "Mistral Ecosystem Open Weight License"), Ministral 3 3B/8B/14B (v25.12, Apache 2.0). Labelled "Premier" with no licence shown: Codestral, Codestral Embed, Mistral Embed, OCR 4.1 and OCR 3. The page never says "API-only", so that reading is our inference. No active Devstral entry: Devstral 2 deprecated 2026-05-22, retires 2026-07-31 (hosted versions; weights remain on Ollama). The list was truncated.
- Licences read on Ollama: devstral-2 (123B) modified MIT with a revenue condition (companies above 20M USD monthly global revenue need a commercial licence); devstral-small-2 Apache 2.0; mistral-medium-3.5 modified MIT.

## 3. Ollama library (tags and sizes as shown 2026-11-20)
- https://ollama.com/library/ministral-3 : `:3b` 3.0 GB, `:8b` 6.0 GB, `:14b` 9.1 GB, `:latest` 6.0 GB; 256K context; vision and tools; Apache 2.0.
- https://ollama.com/library/mistral-small : `:24b` 14 GB; tools; Apache 2.0. https://ollama.com/library/devstral-small-2 : 24b, 15 GB, Apache 2.0, needs Ollama 0.13.3 or later. https://ollama.com/library/mistral : 7b 4.4 GB, tools, Apache (page about a year old).
- No Mistral embedding model on Ollama (https://ollama.com/search?q=embed lists others, such as nomic-embed-text).

## 4. Le Chat, API, data handling
- https://mistral.ai/pricing : Free plan "Limited messages and web searches." and "Limited coding sessions."; Vibe Pro 14.99 USD per month. A free API tier is NOT CONFIRMED.
- https://help.mistral.ai/en/articles/455207-can-i-opt-out-of-my-input-or-output-data-being-used-for-training : Vibe: "users are not opted out by default"; Vibe Enterprise opted out by default; Studio and API opt-out is in the Admin Panel under Privacy; "Opting out of one does not opt you out of the other."
- https://help.mistral.ai/en/articles/347617-do-you-use-my-user-data-to-train-your-models : Vibe Free, Pro, Teams and Student have training on by default with an opt-out; Mistral Studio free mode may use data for training; pay-as-you-go can opt out at any time; for Labs and Public Preview models the opt-out does not apply. (search only, not read: Le Chat Free, Pro and Student default to training allowed; Teams and Enterprise opted out.)
- https://docs.mistral.ai/admin/monitor-comply/zero-data-retention : ZDR means no storing or logging of inputs and outputs for supported API requests longer than needed; pay-as-you-go, stateless calls only, requests reviewed; Agents, Conversations, Files, Chat and Vibe are excluded; "You do not need ZDR to opt out of model training."
- Default retention period in days: NOT CONFIRMED from Mistral pages (a "30 days" figure appeared only on third-party sites and is not used).
- https://docs.mistral.ai/studio/regional-inference : endpoints `api.mistral.ai` (global; "Mistral does not commit to a specific inference location"), `api.eu.mistral.ai`, `api.us.mistral.ai`; EU uses data centers in EU and EFTA countries. Hosting location for Le Chat and Vibe: NOT CONFIRMED.

## 5. Embeddings and OCR
- https://docs.mistral.ai/capabilities/embeddings/overview : embeddings API for text and code (Mistral Embed, Codestral Embed); not on Ollama. API-only is NOT CONFIRMED.
- https://docs.mistral.ai/capabilities/document_ai/basic_ocr : OCR through the API (`client.ocr.process`). Self-hosting not mentioned.

## Our own runs
See the end of this file (added after the runs).

### Runs on 2026-11-20 (macOS, Ollama 0.40.16, `ministral-3:8b` 6.0 GB pulled for this, `nomic-embed-text` embeddings, temperature 0, `think` false, one run each, in a scratch copy of `exercises/codon-mill/mini-rag`)
- `rag.py` question "Does project Heron need to re-analyse ...": k=3 said not enough information; k=5 answered "does not need to re-analyze" and claimed run R7 used release 2.4 (the note says 2.3); `--all` listed the right facts and answered "No" (reasoning: no re-analysis was done); the whole-collection question was not answered.
- `graph.py build`: 80 facts, 1 min 5 s, valid JSON for all 12 notes; odd entries noted on the quest page. `graph.py ask` Heron: 25 facts from 7 notes including the R7 and 2.3 facts, answered "No". Whole-collection question: not answered.
- The `gemma4:12b-mlx` column of the table on the page comes from the earlier runs recorded in `research/rag.md` and the quest page.
- Not run: Mistral Vibe, any Mistral hosted API or Le Chat, `mistral-small`, `devstral-small-2`.
