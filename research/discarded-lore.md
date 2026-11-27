# Discarded lore

Lore items from quests removed in the chapter restructure (branch `restructure-chapters`), kept here so they can be reused if the content returns. Lore on course pages keeps only what the course teaches. Format as in `tools/lint_lore.py`.


## Should You Fine-Tune? (removed: off-scope, about training models)

Original page: `zones/kennel/should-you-fine-tune.qmd` at commit e1ce760.

- [Fine-tuning LLMs Guide](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide): Unsloth, docs. Why read: a beginner-friendly walk through LoRA, QLoRA, dataset shape and training settings; it is a vendor guide for its own tool, so treat its speed and hardware claims as the vendor's.
- [LoRA](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora): Hugging Face, docs. Why read: the PEFT library's explanation of how LoRA works, what rank and alpha control, and how to merge an adapter back into the base model.
- [Define success criteria and build evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests): Anthropic, docs. Why read: it shows how to turn "it seems fine" into a measurable check, which is how you compare a tuned model with an untuned one.


## Why Notebooks Diff Badly (removed: general notebook practice)

Original page: `zones/scriptorium/why-notebooks-diff-badly.qmd` at commit e1ce760.

- [The Notebook file format](https://nbformat.readthedocs.io/en/latest/format_description.html): nbformat, docs. Why read: it is the spec showing that a notebook is JSON holding outputs, execution counts and base64 images, which explains the noisy diffs.
- [nbstripout](https://github.com/kynan/nbstripout): nbstripout project (GitHub), repo. Why read: it strips outputs from a notebook with a Git filter set up by `nbstripout --install`, so Git never sees them.
- [Jupytext](https://github.com/jupytext/jupytext): jupytext project (GitHub), repo. Why read: it pairs an .ipynb with a plain .py so reviewers diff the code only.
- [nbdime](https://nbdime.readthedocs.io/en/latest/): nbdime project, docs. Why read: it gives notebook-aware diff and merge tools if you must keep .ipynb in Git.
- [marimo documentation](https://docs.marimo.io/): marimo, docs. Why read: it describes a notebook stored as plain Python, so Git diffs show code only.


## Run It Top to Bottom (removed: general notebook practice)

Original page: `zones/scriptorium/run-it-top-to-bottom.qmd` at commit e1ce760.

- [marimo documentation](https://docs.marimo.io/): marimo, docs. Why read: it describes reactive cells that re-run in dependency order, a notebook design where hidden run-order state is harder to create.
- [The Notebook file format](https://nbformat.readthedocs.io/en/latest/format_description.html): nbformat, docs. Why read: it is the spec showing that a notebook stores outputs and execution counts in its JSON, which is where a stale stored result lives.
