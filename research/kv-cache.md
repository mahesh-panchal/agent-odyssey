# KV cache (the-context-window)

Added 2026-11-26 from a follow-up the user queued on 2026-11-23.

## Sources

- https://huggingface.co/blog/not-lain/kv-caching : Hafedh Hichri, "KV Caching Explained: Optimizing Transformer Inference Efficiency", Hugging Face blog, published 2025-01-30. Read in full by a fetch subagent (about 22,000 characters, no truncation notice). Short quotes only; the rest is paraphrase.

## What the lesson takes from it

- Definition: "storing the intermediate states of attention layers during inference". The lesson says the model stores numbers computed from each earlier token (its keys and values) and reuses them, adding one entry per new token.
- Memory grows with text length (the post's comparison table). The post gives no formula.
- Not in the post, and not claimed from it: how much memory a cache takes, why providers set window limits.

## Known simplifications in the post (why the lesson says less)

- It draws one attention head. Real models store keys and values at every layer and head. Some models share keys and values across heads, which shrinks the cache. The lesson does not give sizes.
- Its table says standard inference "uses less memory" while also saying memory grows with text length. The lesson states only that the cache grows with the window.
- Its benchmark (SmolLM2-1.7B on a T4 GPU, one prompt, about 5.21 times faster with the cache) is a single setup. The lesson cites no speed figure.
- It never mentions prompt caching. The lesson separates the two: the KV cache belongs to the model, the prompt cache is a provider feature that makes a repeated start of a prompt cheaper. The prompt-cache facts are in `research/cache-and-usage.md`.
- 2026-11-26: RAN `claude -p "/context"` (2.1.332): category table (System prompt, System tools, MCP tools, deferred lines, Skills, Messages ~10 tokens, Free space, Autocompact buffer) matches the-context-window hands-on.
