"""Convert zones/**/*.yml test banks to assets/data/<zone>-<slug>.json, validating them."""
import json, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
def put(path, text):
    """Write only when the content changed, so `quarto preview` is not told every file changed on each pre-render."""
    if not path.exists() or path.read_text() != text:
        path.write_text(text)


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
    put(OUT / f"{name}.json", json.dumps(bank, indent=1))
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

def build_graph(world):
    """Path graph from the per-quest fields in zones.yml. Appends to `errors`; returns the graph dict."""
    quests, gate_of = {}, {}
    for ch, g in world["gates"].items():
        for q in g.get("quests", []):
            if q["id"] in quests:
                errors.append(f"graph: duplicate quest id {q['id']}")
            quests[q["id"]] = q; gate_of[q["id"]] = ch
    branches, trunk_order, finale = world.pop("branches", []), world.pop("trunk_order", []), world.pop("finale", {})
    bids = [b["id"] for b in branches]
    if len(set(bids)) != len(bids):
        errors.append("graph: duplicate branch ids")
    fid = finale.get("id")
    if fid not in quests:
        errors.append(f"graph: finale quest {fid!r} is not in any gate")
    elif gate_of[fid] != finale.get("gate"):
        errors.append(f"graph: finale quest sits in gate {gate_of[fid]}, finale says {finale.get('gate')}")
    out = {}
    for qid, q in quests.items():
        for f in ("after", "branch", "trunk", "optional"):
            if f not in q:
                errors.append(f"graph: {qid} lacks '{f}'")
        a, sg = q.get("after", []), q.get("suggested", [])
        for ref in a + sg:
            if ref not in quests:
                errors.append(f"graph: {qid} refers to unknown quest {ref!r}")
        if qid in a or qid in sg:
            errors.append(f"graph: {qid} refers to itself")
        br = q.get("branch")
        if br not in bids + ["trunk", "finale"]:
            errors.append(f"graph: {qid} has unknown branch {br!r}")
        if bool(q.get("trunk")) != (br == "trunk"):
            errors.append(f"graph: {qid} trunk flag and branch {br!r} disagree")
        if q.get("trunk") and q.get("optional"):
            errors.append(f"graph: trunk quest {qid} cannot be optional")
        if (br == "finale") != (qid == fid):
            errors.append(f"graph: only the finale quest may use branch 'finale' ({qid})")
        out[qid] = {"title": q["title"], "page": q["page"], "gate": gate_of[qid], "after": a, "suggested": sg,
                    "branch": br, "trunk": bool(q.get("trunk")), "optional": bool(q.get("optional"))}
    # Cycles (Kahn over after + suggested edges).
    deps = {k: set(v["after"]) | set(v["suggested"]) for k, v in out.items()}
    deps = {k: {d for d in v if d in out} for k, v in deps.items()}
    while True:
        free = [k for k, v in deps.items() if not v]
        if not free:
            break
        for k in free:
            del deps[k]
        for v in deps.values():
            v.difference_update(free)
    if deps:
        errors.append("graph: cycle among " + ", ".join(sorted(deps)))
    trunk_set = {k for k, v in out.items() if v["trunk"]}
    if len(set(trunk_order)) != len(trunk_order) or set(trunk_order) != trunk_set:
        errors.append("graph: trunk_order must list each trunk quest exactly once; differs by "
                      + str(sorted(set(trunk_order) ^ trunk_set)))
    pos = {k: i for i, k in enumerate(trunk_order)}
    for k in trunk_order:
        for d in out.get(k, {}).get("after", []):
            if d not in pos or pos[d] > pos[k]:
                errors.append(f"graph: trunk quest {k} comes before its prerequisite {d}")
    for b in branches:
        mine = [k for k, v in out.items() if v["branch"] == b["id"]]
        if not [k for k in mine if not out[k]["optional"]]:
            errors.append(f"graph: branch {b['id']} has no required quest")
        for e in b.get("entry", []):
            if e not in mine:
                errors.append(f"graph: branch {b['id']} entry {e!r} is not one of its quests")
        for f in ("name", "blurb", "who"):
            if not b.get(f):
                errors.append(f"graph: branch {b['id']} lacks '{f}'")
    req = finale.get("requires", {})
    br_req = req.get("branches", {})
    if req.get("trunk") != "all":
        errors.append("graph: finale requires.trunk must be 'all'")
    unknown = [b for b in br_req.get("of", []) if b not in bids]
    if unknown or not isinstance(br_req.get("any"), int) or not 1 <= br_req["any"] <= len(br_req.get("of", [])):
        errors.append(f"graph: finale branch rule is inconsistent (unknown {unknown}, any={br_req.get('any')})")
    if fid in quests:
        finale = dict(finale, page=quests[fid]["page"], title=quests[fid]["title"])
    return {"quests": out, "branches": branches, "trunk_order": trunk_order, "finale": finale}

world["graph"] = build_graph(world)
put(OUT / "world.json", json.dumps(world))
print("ok world")

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
