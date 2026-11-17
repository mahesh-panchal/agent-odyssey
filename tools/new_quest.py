"""Scaffold a quest: pixi run new-quest <zone> <slug> "<Title>". Creates zones/<zone>/<slug>.{qmd,yml}.
You still add the quest to zones.yml (id must be <zone>-<slug>)."""
import sys
from pathlib import Path
if len(sys.argv) != 4:
    sys.exit('usage: new-quest <zone> <slug> "<Title>"')
zone, slug, title = sys.argv[1:]
d = Path(__file__).resolve().parent.parent / "zones" / zone; d.mkdir(parents=True, exist_ok=True)
q, y = d / f"{slug}.qmd", d / f"{slug}.yml"
if q.exists() or y.exists():
    sys.exit("refusing to overwrite an existing quest")
q.write_text(f'''---
title: "{title}"
---

::: {{.quest-dialog}}
**Prerequisites:** TODO. **Objective:** TODO. **Time:** about 15 minutes.
<span class="ao-badge">TODO: "Verified: ran ..." only if you ran it; otherwise "Last verified (docs, not run): <tool> <version> on <date>" or "General practice".</span>
:::

TODO: teach the idea. Use `::: {{.panel-tabset group="companion"}}` for Claude Code | OpenCode + Ollama.

## Battle

<div data-ao-test="{zone}-{slug}" data-xp="60"></div>

::: {{.ao-lore}}
## Lore

*Further reading. Optional.*

<!-- TODO: 2-8 items, one per line, only URLs from research/*.md or research/lore-extra.md:
- [Title](https://url): Publisher, docs. Why read: one line.
-->
:::
''')
y.write_text('''pass: 0.8
questions:
  - type: choice
    prompt: "TODO"
    explain: "TODO: why the right answer is right."
    options:
      - { text: "Right answer", correct: true }
      - { text: "Wrong answer", misconception: "Say which misconception this reveals." }
''')
print(f"created {q} and {y}\nNext: add id '{zone}-{slug}' to zones.yml, then `pixi run render`.")
