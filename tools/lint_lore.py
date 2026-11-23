"""Lint the Lore blocks and build the Lore library page.
Run: pixi run lore [--require]. Without --require, quests with no (or an empty) Lore block are warnings.
A Lore block is `::: {.ao-lore ...}` ... `:::` at the end of a quest .qmd; each item is one bullet:
  - [Title](https://url): Publisher, kind. Why read: one line.   (kind: docs | article | paper | repo)"""
import re, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
KINDS = ("docs", "article", "paper", "repo")
ITEM = re.compile(r"^- \[(?P<title>[^\]]+)\]\((?P<url>\S+?)\): (?P<pub>.+?), (?P<kind>[a-z]+)\. Why read: (?P<why>\S.*)$")
OPEN = re.compile(r"^:::+\s*\{[^}]*\.ao-lore[\s}]")
URL = re.compile(r"https?://[^\s)>\]\"'`<]+")

def norm(u):
    return u.split("#")[0].rstrip("/")

def known_urls():
    out = set()
    for f in (ROOT / "research").glob("*.md"):
        for m in URL.findall(f.read_text()):
            out.add(norm(m.rstrip(".,;:")))
    return out

def quests():
    """[(zone name, quest dict)] in map order then quest order."""
    z = yaml.safe_load((ROOT / "zones.yml").read_text())
    return [(g["name"], q) for g in z["gates"].values() for q in g.get("quests", [])]

def parse(path):
    """Returns (block_found, items, problems). Item = dict(title,url,pub,kind,why,line). Problem = (line, text)."""
    lines = path.read_text().splitlines()
    start = next((i for i, l in enumerate(lines) if OPEN.match(l)), None)
    if start is None: return False, [], []
    items, probs = [], []
    end = next((i for i in range(start + 1, len(lines)) if re.match(r"^:::+\s*$", lines[i])), None)
    if end is None: return True, [], [(start + 1, "Lore block is never closed with :::")]
    body = lines[start + 1:end]
    if not any(l.strip() == "## Lore" for l in body): probs.append((start + 1, "missing heading '## Lore'"))
    if not any(l.strip() == "*Further reading. Optional.*" for l in body):
        probs.append((start + 1, "missing line '*Further reading. Optional.*'"))
    in_comment = False
    for off, l in enumerate(body):
        n = start + 2 + off
        if "<!--" in l: in_comment = True
        if in_comment:
            if "-->" in l: in_comment = False
            continue
        if not l.startswith("- "): continue
        m = ITEM.match(l)
        if not m:
            probs.append((n, "item does not match '- [Title](https://url): Publisher, kind. Why read: ...'"
                             + (" (no 'Why read:' text)" if "Why read:" not in l else ""))); continue
        d = m.groupdict(); d["line"] = n
        if not d["url"].startswith("https://"): probs.append((n, f"link must be https: {d['url']}"))
        if d["kind"] not in KINDS: probs.append((n, f"kind must be one of {'|'.join(KINDS)}, got '{d['kind']}'"))
        items.append(d)
    return True, items, probs

def lint(require):
    known, bad, warn, missing = known_urls(), 0, 0, 0
    for zone, q in quests():
        path = ROOT / q["page"].replace(".html", ".qmd"); rel = path.relative_to(ROOT)
        if not path.exists(): print(f"{rel}:1: quest page listed in zones.yml does not exist"); bad += 1; continue
        found, items, probs = parse(path)
        def err(n, t):
            nonlocal bad; print(f"{rel}:{n}: {t}"); bad += 1
        if not found or not items:
            msg = "no Lore block" if not found else "Lore block has no items yet"
            missing += 1
            if require: err(1, msg)
            else: print(f"warning: {rel}: {msg}"); warn += 1
        for n, t in probs: err(n, t)
        if items and not 2 <= len(items) <= 8: err(items[0]["line"], f"Lore needs 2-8 items, has {len(items)}")
        seen = set()
        for it in items:
            u = norm(it["url"])
            if u in seen: err(it["line"], f"duplicate URL in this quest: {it['url']}")
            seen.add(u)
            if u not in known: err(it["line"], f"URL not found in research/*.md or research/lore-extra.md: {it['url']}")
    same = {}   # (normalised url, why text) -> [quest files]
    for zone, q in quests():
        path = ROOT / q["page"].replace(".html", ".qmd")
        if path.exists():
            for it in parse(path)[1]: same.setdefault((norm(it["url"]), it["why"]), []).append(path.relative_to(ROOT))
    for (u, why), fs in sorted(same.items()):
        if len(fs) >= 3:
            print(f"warning: same Why-read text used verbatim for {u} in {len(fs)} quests ({', '.join(map(str, fs[:3]))}...): "
                  "write quest-specific lines"); warn += 1
    print(f"lore: {bad} problem(s), {warn} warning(s); {missing} quest(s) without Lore yet")
    return bad

def write_lore_page():
    """Generate lore.qmd (gitignored) from all Lore blocks. Never fails on an empty library.
    Each source appears once (dedup by normalised URL) under the first zone that cites it. Every citing quest
    is listed with its own Why-read text unless all citers wrote the same text."""
    srcs, order = {}, []   # normalised url -> dict; first citation wins for title, publisher, kind and zone
    for zone, q in quests():
        path = ROOT / q["page"].replace(".html", ".qmd")
        if not path.exists(): continue
        for it in parse(path)[1]:
            u = norm(it["url"])
            if u not in srcs:
                srcs[u] = dict(it, zone=zone, cited=[], urls=[]); order.append(u)
            srcs[u]["urls"].append(it["url"])
            srcs[u]["cited"].append((q["title"], "./" + q["page"], it["why"]))
    def shown(u):   # first-seen URL, preferring the form without trailing slash or anchor
        return next((x for x in srcs[u]["urls"] if x == u), srcs[u]["urls"][0])
    def link(u): return f"[{srcs[u]['title']}]({shown(u)})"
    out = ['---\ntitle: "Lore library"\n---\n',
           "<!-- Generated by tools/prerender.py from the Lore block at the end of each quest. Do not edit. -->\n",
           "Sources to read more, gathered from the Lore section of each quest. Optional. Each source is listed once, "
           "under the first zone that cites it, with every quest that cites it.\n"]
    if not srcs:
        out.append("**No Lore yet.** No quest has a Lore section so far. As quests gain one, "
                   "their sources will appear here, grouped by zone.\n")
    top = sorted((u for u in order if len(srcs[u]["cited"]) >= 2), key=lambda u: -len(srcs[u]["cited"]))[:8]
    if top:
        out.append("\n## Most cited\n")
        out += [f"- {link(u)}: {len(srcs[u]['cited'])} quests" for u in top]
    zones = list(dict.fromkeys(srcs[u]["zone"] for u in order))
    for zone in [z for z in dict.fromkeys(z for z, _ in quests()) if z in zones]:
        out.append(f"\n## {zone}\n")
        for u in (u for u in order if srcs[u]["zone"] == zone):
            s, c = srcs[u], srcs[u]["cited"]
            head = f"- {link(u)}: {s['pub']}, {s['kind']}."
            if len({w for _, _, w in c}) == 1:
                cites = ", ".join(f"[{t}]({p})" for t, p, _ in c)
                out.append(f"{head} Why read: {c[0][2]} Cited in: {cites}.")
            else:
                out.append(f"{head} Cited by {len(c)} quests; each quest says what to read it for.\n")
                out.append("  Cited in:\n")
                out += [f"  - [{t}]({p}): {w}" for t, p, w in c]
                out.append("")
    # Write only when the content changed: `quarto preview` jumps to whichever page was rewritten last.
    target, text = ROOT / "lore.qmd", "\n".join(out) + "\n"
    if not target.exists() or target.read_text() != text:
        target.write_text(text)

if __name__ == "__main__":
    sys.exit(1 if lint("--require" in sys.argv[1:]) else 0)
