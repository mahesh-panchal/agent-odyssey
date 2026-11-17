"""Heuristic bank lint: flags choice questions whose correct option is the longest (a guessing cue)."""
import sys
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parent.parent
tot = flagged = 0
for f in sorted((ROOT / "zones").glob("*/*.yml")):
    for i, q in enumerate(yaml.safe_load(f.read_text())["questions"]):
        if q["type"] != "choice": continue
        tot += 1
        c = next(o for o in q["options"] if o.get("correct")); lens = [len(o["text"]) for o in q["options"]]
        if len(c["text"]) == max(lens) and len(c["text"]) > 1.15 * sorted(lens)[-2]:
            flagged += 1; print(f"{f.relative_to(ROOT)} q{i+1}: correct={len(c['text'])} others={sorted(lens)[:-1]}")
print(f"{flagged}/{tot} choice questions have a clearly longest correct option")
