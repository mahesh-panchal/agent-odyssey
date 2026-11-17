"""Convert zones/**/*.yml test banks to assets/data/<zone>-<slug>.json, validating them."""
import json, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "data"
OUT.mkdir(parents=True, exist_ok=True)
TYPES = {"choice", "order", "sort", "faulty-line", "match"}
errors = []

for f in sorted((ROOT / "zones").glob("*/*.yml")):
    bank = yaml.safe_load(f.read_text())
    name = f"{f.parent.name}-{f.stem}"
    for i, q in enumerate(bank.get("questions", [])):
        where = f"{f.relative_to(ROOT)} q{i+1}"
        if q.get("type") not in TYPES:
            errors.append(f"{where}: bad type {q.get('type')!r}")
        t = q["type"]
        if t == "choice":
            opts = q.get("options", [])
            if sum(1 for o in opts if o.get("correct")) != 1:
                errors.append(f"{where}: need exactly one correct option")
            for o in opts:
                if not o.get("correct") and not o.get("misconception"):
                    errors.append(f"{where}: wrong option '{o.get('text')}' lacks misconception")
        elif t == "order":
            if len(q.get("items", [])) < 2:
                errors.append(f"{where}: order needs >= 2 items")
        elif t == "sort":
            bins = q.get("bins", [])
            for it in q.get("items", []):
                if it.get("bin") not in bins:
                    errors.append(f"{where}: item '{it.get('text')}' has unknown bin")
                if not it.get("misconception"):
                    errors.append(f"{where}: item '{it.get('text')}' lacks misconception")
        elif t == "faulty-line":
            lines = q.get("lines", [])
            if sum(1 for l in lines if l.get("faulty")) != 1:
                errors.append(f"{where}: need exactly one faulty line")
            for l in lines:
                if not l.get("faulty") and not l.get("why"):
                    errors.append(f"{where}: fine line '{l.get('text')}' lacks 'why'")
        elif t == "match":
            if len(q.get("pairs", [])) < 2:
                errors.append(f"{where}: match needs >= 2 pairs")
    (OUT / f"{name}.json").write_text(json.dumps(bank, indent=1))
    print(f"ok {name}")

# world.json from zones.yml (gate positions resolved from the ASCII map)
world = yaml.safe_load((ROOT / "zones.yml").read_text())
rows = world["map"]
if len({len(r) for r in rows}) != 1:
    errors.append("zones.yml: map rows must be equal length")
for ch, g in world["gates"].items():
    pos = [(x, y) for y, r in enumerate(rows) for x, c in enumerate(r) if c == ch]
    if len(pos) != 1:
        errors.append(f"gate {ch}: expected 1 position, found {len(pos)}")
        continue
    g["x"], g["y"] = pos[0]
(OUT / "world.json").write_text(json.dumps(world))
print("ok world")

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
