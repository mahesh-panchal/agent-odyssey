# Privacy and unpublished work

Date checked 2026-11-17. Official docs only, via a summarising fetch tool (quotes as returned).
Question: what do the docs say about retention and training use, so the Crypt quest can advise on unpublished ideas and results. Feeds: zones/safe-editing/keep-secrets-out-of-reach.qmd; zones/collaboration/send-small-changes.qmd (disclosure section).

## Claude Code data usage (https://code.claude.com/docs/en/data-usage, read 2026-11-17)
- CONFIRMED training, consumer (Free, Pro, Max, Ultra): "We give you the choice to allow your data to be used to improve future Claude models." Anthropic trains new models on data from these accounts "when this setting is on (including when you use Claude Code from these accounts)".
- CONFIRMED training, commercial (Team, Enterprise, API, 3rd-party platforms, Claude Gov): "Anthropic does not train generative models using code or prompts sent to Claude Code under commercial terms, unless the customer has chosen to provide their data to us for model improvement (for example, the Developer Partner Program)."
- CONFIRMED retention, consumer: 5 years if data use for model improvement is allowed; 30 days if not. Setting at https://claude.ai/settings/data-privacy-controls.
- CONFIRMED retention, commercial (Team, Enterprise, API): standard 30 days; zero data retention available to qualified Enterprise accounts, enabled per organisation.
- CONFIRMED: Claude Code sends all user prompts and model outputs over the network (TLS 1.2+); local transcripts are stored in plaintext under `~/.claude/projects/` for 30 days by default (`cleanupPeriodDays`).
- CONFIRMED: transcripts sent with `/feedback` are retained for 5 years.
- Scope: this page covers Claude Code. Not checked: the claude.ai chat product's privacy help pages, Anthropic's Privacy Center and the Consumer and Commercial Terms text themselves (linked from the page). Not checked: how any other vendor's consumer chat tool handles training or retention.

## Ollama (https://docs.ollama.com/faq, read 2026-11-17)
- CONFIRMED: "Ollama runs locally. We don't see your prompts or data when you run locally."
- CONFIRMED: cloud models are different: Ollama processes prompts and responses to deliver the service; the FAQ says they are not stored or logged and never used for training. Local-only mode: `OLLAMA_NO_CLOUD=1` or `disable_ollama_cloud` in `~/.ollama/server.json`.
- Not checked: Ollama's separate Cloud FAQ, and whether tools or web search used alongside a local model send data elsewhere.

## Unconfirmed (our practice, not doc claims)
- Not checked: any journal or funder policy on disclosing AI assistance. No venue was read, so the quest names none and tells readers to check the venue's own page.
- General practice: preprints, repository tags and lab notebook entries date-stamp work. Not checked against a primary source here.
