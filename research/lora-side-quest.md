# Should You Fine-Tune? (kennel side quest)

- Moved 2026-11-23 from the trunk lesson Script, Model, or LLM ("Should you fine-tune? A note on LoRA") into the optional Kennel quest `kennel-should-you-fine-tune` (companions branch, after Pick Your Companion). Trunk lesson keeps one sentence pointing to it.
- URLs used (all already in research/lore-extra.md, no new sources):
  - https://unsloth.ai/docs/get-started/fine-tuning-llms-guide
  - https://huggingface.co/docs/peft/main/en/conceptual_guides/lora
  - https://platform.claude.com/docs/en/test-and-evaluate/develop-tests (also in research/terminology.md)
- Supported by the sources (see lore-extra.md): LoRA freezes weights and trains small low-rank adapter matrices; adapters merge into the base model.
- Our own teaching advice (general practice, not from the pages): the four conditions (weights, narrow repeatable task, examples with known answers with some held back, an eval vs the untuned model); try prompt, tools and an eval first; what to track (training data, adapter version, base model). The ID-masking vs methods-summary example uses invented mock tasks and counts.
- No numbers on speed, memory or cost are stated. "Far less memory than retraining everything" is the one relative claim carried over from the old section.
