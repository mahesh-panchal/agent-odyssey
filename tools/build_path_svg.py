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


OV_TAB = 18   # room above a box for the "You are here" tab


def overview_svg(world, cols, mid):
    """Compact overview: one trunk box, the branches in a grid, one final-boss box. Statuses are added by start.js.

    cols=2 draws a 600-unit-wide grid for wide screens; cols=1 draws a single column for phones.
    """
    g = world["graph"]
    quests, trunk, branches = g["quests"], g["trunk_order"], g["branches"]
    fin = g.get("finale", {})
    need = fin.get("requires", {}).get("branches", {}).get("any", 3)
    gate = world.get("gates", {}).get(fin.get("gate", ""), {})
    fin_name = gate.get("name") or fin.get("title", "Clear the Murk")
    boss = quests[trunk[-1]]["title"].replace("Boss: ", "")
    wide = cols == 2
    W = 600 if wide else 340
    BH = 64 if wide else 58
    PITCH_Y = BH + 22
    TH, FH = 84, 80
    top = 26
    if wide:
        colw, xs, bus_x = 270, [20, 310], 300
        trunk_x, trunk_w = 20, 560
        fin_x, fin_w = 120, 360
    else:
        colw, xs, bus_x = 304, [26], 14
        trunk_x, trunk_w = 10, 320
        fin_x, fin_w = 10, 320
    rows = -(-len(branches) // cols)
    y0 = top + TH + 22
    last_bottom = y0 + (rows - 1) * PITCH_Y + BH
    fin_y = last_bottom + 40
    H = fin_y + FH + 16
    mk = f"ahov{cols}"

    def first_page(b):
        entry = [e for e in b.get("entry", []) if e in quests]
        if entry:
            return quests[entry[0]]["page"]
        ids = [q for q in quests if quests[q].get("branch") == b["id"]]
        return quests[ids[0]]["page"]

    def box(kind, ident, href, title, lines, x, y, w, h, total, extra=""):
        ts = "".join(f'<text class="{c}" x="{x + 12}" y="{y + dy}">{escape(t)}</text>' for c, dy, t in lines)
        return (f'<a class="ovbox {kind}" href="{escape(href)}" data-kind="{kind}" data-id="{escape(ident)}" data-total="{total}" '
                f'data-first="{escape(href)}" aria-label="{escape(title)}"><title>{escape(title)}</title>'
                f'<rect class="box" x="{x}" y="{y}" width="{w}" height="{h}" rx="9"/>{extra}{ts}</a>')

    parts, edges = [], []
    # Trunk
    t_total = len(trunk)
    parts.append(box("trunk", "trunk", quests[trunk[0]]["page"], f"Trunk, {t_total} quests",
                     [("ovt", 24, f"Trunk \u00b7 {t_total} quests"),
                      ("ovn", 46, f"Mid-boss: {boss}"),
                      ("ovs", 68, f"\u25cb not started \u00b7 0/{t_total}")],
                     trunk_x, top, trunk_w, TH, t_total,
                     extra=f'<rect class="box2" x="{trunk_x - 4}" y="{top - 4}" width="{trunk_w + 8}" height="{TH + 8}" rx="12"/>'))
    # Branches in graph order, row by row
    edges.append(f'<path class="ovedge" d="M{bus_x} {top + TH + 4} V{fin_y - 4}" marker-end="url(#{mk})"/>')
    for i, b in enumerate(branches):
        r, c = divmod(i, cols)
        x, y = xs[c], y0 + r * PITCH_Y
        total = len([q for q in quests if quests[q].get("branch") == b["id"] and not quests[q].get("optional")])
        parts.append(box("branch", b["id"], first_page(b), f'{b["name"]}, {total} quests',
                         [("ovt", 26, b["name"]), ("ovs", 48, f"\u25cb not started \u00b7 0/{total}")],
                         x, y, colw, BH, total))
        cy = y + BH / 2
        if wide and c == 0:
            edges.append(f'<line class="ovedge" x1="{bus_x}" y1="{cy}" x2="{x + colw + 3}" y2="{cy}"/>')
        elif wide:
            edges.append(f'<line class="ovedge" x1="{bus_x}" y1="{cy}" x2="{x - 3}" y2="{cy}"/>')
        else:
            edges.append(f'<line class="ovedge" x1="{bus_x}" y1="{cy}" x2="{x - 3}" y2="{cy}"/>')
    # Final boss
    parts.append(box("finale", fin.get("id", "finale"), fin["page"], f"{fin_name}, final boss",
                     [("ovt", 26, fin_name), ("ovn", 48, f"Needs the trunk + any {need} branches"), ("ovs", 70, "\u25cb sealed")],
                     fin_x, fin_y, fin_w, FH, 0,
                     extra=f'<rect class="box2" x="{fin_x - 4}" y="{fin_y - 4}" width="{fin_w + 8}" height="{FH + 8}" rx="12"/>'))
    return (f'<svg class="ao-ov ao-ov{cols}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="group" '
            f'aria-label="Overview: the trunk, {len(branches)} branches and the final boss. Every box is a link.">'
            f'<defs><marker id="{mk}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
            '<path d="M0 0 L10 5 L0 10 z" class="ahead"/></marker></defs>'
            + "".join(edges) + "".join(parts) + "</svg>\n")


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
    for cols, name in ((2, "path-overview.svg"), (1, "path-overview-narrow.svg")):
        ov = out.parent / name
        ov.write_text(overview_svg(world, cols, last_trunk), encoding="utf-8")
        print(f"build_path_svg: wrote {ov}")


if __name__ == "__main__":
    import sys
    main(*sys.argv[1:3])
