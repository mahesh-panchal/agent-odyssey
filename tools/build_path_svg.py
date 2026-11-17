"""Draw the quest network (trunk spine, branch lanes, finale) as assets/data/path-network.svg.

Reads the `graph` block of assets/data/world.json (written by build_banks.py), so run it after that script.
Statuses (cleared/ready/waiting) and the "you are here" marker are added at runtime by assets/js/start.js.
"""
import json
import textwrap
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "data" / "path-network.svg"

PITCH, NW, NH = 160, 136, 72   # node spacing, node width, node height
SPINE_Y = 110
LANE_Y0, LANE_PITCH = 270, 140
LEFT = 90


def lane_order(ids, quests):
    """Topological order inside one branch (after/suggested edges), required quests first, optional last."""
    placed, rest = [], list(ids)
    while rest:
        ready = [q for q in rest
                 if all(d not in rest for d in quests[q].get("after", []) + quests[q].get("suggested", []))]
        pick = ready[0] if ready else rest[0]
        placed.append(pick)
        rest.remove(pick)
    return [q for q in placed if not quests[q].get("optional")] + [q for q in placed if quests[q].get("optional")]


def node(qid, q, cx, cy, kind):
    """One accessible link node. `kind` is trunk, branch or finale; optional quests are dashed."""
    cls = ["node", kind] + (["optional"] if q.get("optional") else []) + (["boss"] if q.get("boss") else [])
    lines = textwrap.wrap(q["title"], 17)[:3]
    x, y = cx - NW / 2, cy - NH / 2
    tspans = "".join(f'<tspan x="{cx}" dy="{0 if i == 0 else 14}">{escape(t)}</tspan>' for i, t in enumerate(lines))
    shape = (f'<rect class="box" x="{x}" y="{y}" width="{NW}" height="{NH}" rx="8"/>')
    if q.get("boss"):
        shape += f'<rect class="box2" x="{x - 5}" y="{y - 5}" width="{NW + 10}" height="{NH + 10}" rx="11"/>'
    return (f'<a class="{" ".join(cls)}" href="{escape(q["page"])}" data-id="{qid}" data-x="{cx}" data-y="{cy}" '
            f'data-branch="{escape(q.get("branch", ""))}" data-title="{escape(q["title"])}">'
            f'<title>{escape(q["title"])}</title>{shape}'
            f'<text class="t" x="{cx}" y="{y + 18}" text-anchor="middle">{tspans}</text>'
            f'<text class="st" x="{cx}" y="{y + NH - 8}" text-anchor="middle"></text></a>')


def main(src=None, out=None):
    out = Path(out) if out else OUT
    world = json.loads(Path(src or ROOT / "assets/data/world.json").read_text())
    g = world.get("graph")
    if not g:
        print("build_path_svg: no graph in world.json; skipping")
        return
    quests, trunk, branches = g["quests"], g["trunk_order"], g["branches"]
    tx = {qid: LEFT + i * PITCH for i, qid in enumerate(trunk)}
    last_trunk = trunk[-1]

    # Branch lanes: attach to the trunk quest they follow; rightmost attach on top so rails never cross nodes.
    lanes = []
    for plan_pos, b in enumerate(branches):
        ids = [q for q in quests if quests[q].get("branch") == b["id"]]
        order = lane_order(ids, quests)
        first = quests[order[0]]
        cands = [d for d in first.get("after", []) + first.get("suggested", []) if d in tx]
        attach = max(cands, key=lambda d: tx[d]) if cands else last_trunk
        lanes.append({"b": b, "order": order, "attach": attach, "pos": plan_pos})
    lanes.sort(key=lambda l: (-tx[l["attach"]], l["pos"]))

    extent = tx[last_trunk] + PITCH
    for l in lanes:
        extent = max(extent, tx[l["attach"]] + (len(l["order"]) - 1) * PITCH + NW / 2 + 40)
    bus_x = extent + 30
    fin_cx = bus_x + 150
    height = LANE_Y0 + (len(lanes) - 1) * LANE_PITCH + NH / 2 + 50
    width = fin_cx + 120

    edges, nodes, labels = [], [], []
    # Spine
    labels.append(f'<text class="lane-label" x="{LEFT - NW / 2}" y="{SPINE_Y - NH / 2 - 16}">Trunk: walk it in this order</text>')
    for i, qid in enumerate(trunk):
        q = dict(quests[qid])
        q["boss"] = qid == last_trunk
        nodes.append(node(qid, q, tx[qid], SPINE_Y, "trunk"))
        if i:
            edges.append(f'<line class="edge" x1="{tx[trunk[i - 1]] + NW / 2}" y1="{SPINE_Y}" x2="{tx[qid] - NW / 2 - 2}" y2="{SPINE_Y}" marker-end="url(#ah)"/>')
    # Finale
    fin = g.get("finale", {})
    fq = {"title": fin.get("title", "Clear the Murk"), "page": fin["page"], "branch": "finale", "boss": True}
    need = fin.get("requires", {}).get("branches", {}).get("any", 3)
    edges.append(f'<line class="edge" x1="{tx[last_trunk] + NW / 2 + 5}" y1="{SPINE_Y}" x2="{fin_cx - NW / 2 - 8}" y2="{SPINE_Y}" marker-end="url(#ah)"/>')
    nodes.append(node(fin["id"], fq, fin_cx, SPINE_Y, "finale"))
    labels.append(f'<text class="lane-label" x="{fin_cx - NW / 2}" y="{SPINE_Y - NH / 2 - 16}">Final boss: trunk + any {need} branches</text>')
    # Lanes
    max_bus_y = SPINE_Y
    for k, l in enumerate(lanes):
        cy = LANE_Y0 + k * LANE_PITCH
        max_bus_y = cy
        cx0 = tx[l["attach"]]
        rail = cx0 - 80
        edges.append(f'<path class="edge rail" d="M{cx0} {SPINE_Y + NH / 2} V{SPINE_Y + NH / 2 + 12} H{rail} V{cy} H{cx0 - NW / 2 - 2}" marker-end="url(#ah)"/>')
        labels.append(f'<text class="lane-label" x="{cx0 - NW / 2}" y="{cy - NH / 2 - 10}" data-branch-label="{l["b"]["id"]}">'
                      f'{escape(l["b"]["name"])} <tspan class="bprog" data-branch="{l["b"]["id"]}"></tspan></text>')
        prev = None
        for j, qid in enumerate(l["order"]):
            cx = cx0 + j * PITCH
            nodes.append(node(qid, quests[qid], cx, cy, "branch"))
            if prev is not None:
                dash = " optional" if quests[qid].get("optional") else ""
                edges.append(f'<line class="edge{dash}" x1="{prev + NW / 2}" y1="{cy}" x2="{cx - NW / 2 - 2}" y2="{cy}" marker-end="url(#ah)"/>')
            prev = cx
        edges.append(f'<path class="edge bus" d="M{prev + NW / 2} {cy} H{bus_x}"/>')
    edges.append(f'<path class="edge bus" d="M{bus_x} {max_bus_y} V{SPINE_Y}"/>')

    svg = (f'<svg class="ao-net" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {height:.0f}" '
           f'width="{width:.0f}" height="{height:.0f}" role="group" aria-label="Quest network. A text list of every quest follows the map.">'
           '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
           '<path d="M0 0 L10 5 L0 10 z" class="ahead"/></marker></defs>'
           + "".join(edges) + "".join(labels) + "".join(nodes) + "</svg>\n")
    out.write_text(svg)
    print(f"build_path_svg: wrote {out} ({len(nodes)} nodes)")


if __name__ == "__main__":
    import sys
    main(*sys.argv[1:3])
