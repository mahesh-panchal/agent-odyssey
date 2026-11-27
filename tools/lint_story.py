"""Story continuity check: run it after any change to a story block, the guide cast or the zone map.

Reads zones.yml (gates, `guides`, trunk order, branch entries) and the `::: {.ao-story}` block of every quest.
Errors (exit 1):
  - the story names none of its zone's guides (who supplies the knowledge here?)
  - a guide written as role plus name that is not in the cast of zones.yml (typo or invented guide)
  - a retired story word (research/story-bible.md)
  - the story is shorter than 3 or longer than 5 sentences
  - the story moves the party to a new zone (trunk step into a different zone, or a branch entry quest) without a travel word
Warnings (with --warn): contrast framing ('X, not Y', 'rather than').
Judgement still needed: the order of places, who knows what, the scroll's path. Re-read the chain with `--chain`.
"""
import re, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
world = yaml.safe_load((ROOT / "zones.yml").read_text())
ROLES = r"(Wanderer|Sage|Hallmaster|Warden|Miller|Tinker|Beastmaster|Cartographer|Surveyor|Smith|Watchman|Tidewarden|Diver|Net-mender|Scribe|Record Keeper|Gatekeeper|Queue Master)"
TRAVEL = re.compile(r"\b(walk|walks|walked|return|returns|arrive|arrives|leave|leaves|cross|crosses|climb|climbs|road|reach|reaches|follow|leads|head|heads|journey|enter|enters|goes|go)\b", re.I)
RETIRED = re.compile(r"kennel master|\bthe Beast\b|tongue-spirit|\barmou?r\b|\bcarapace\b|\bcompanion\b|\bthe Pet\b", re.I)
CONTRAST = re.compile(r"rather than|\bnot (just|only|merely)\b|\bnot [^.]{0,30}, but\b|, not ", re.I)


def story_of(qmd):
    t = (ROOT / qmd).read_text()
    m = re.search(r"::: \{\.ao-story\}\n(.*?)\n(?:::: \{\.panel-tabset|!\[|:::\n)", t, re.S)
    return " ".join(m.group(1).split()) if m else ""


def main():
    cast = {g for gate in world["gates"].values() for g in gate.get("guides", [])}
    gate_of, quest = {}, {}
    for ch, gate in world["gates"].items():
        for q in gate["quests"]:
            gate_of[q["id"]] = ch; quest[q["id"]] = q
    entries = {e for b in world["branches"] for e in b.get("entry", [])}
    trunk = world["trunk_order"]
    prev = {qid: (trunk[i - 1] if i else None) for i, qid in enumerate(trunk)}
    errs = warns = 0
    for ch, gate in world["gates"].items():
        for q in gate["quests"]:
            qmd = q["page"].replace(".html", ".qmd"); s = story_of(qmd); rel = qmd
            def err(msg):
                nonlocal errs; print(f"ERROR {rel}: {msg}"); errs += 1
            if not s:
                err("no story block found"); continue
            n = len(re.findall(r"[.!?](?:\s|$)", s))
            if not 3 <= n <= 5: err(f"{n} sentences (want 3 to 5)")
            guides = gate.get("guides", [])
            if guides and not any(g in s or g.split()[-1] in s for g in guides):
                err(f"names none of the guides of {gate['name']}: {', '.join(guides)}")
            for m in re.finditer(ROLES + r" ([A-Z][a-z]+)", s):
                if m.group(0) not in cast: err(f"unknown guide '{m.group(0)}' (not in zones.yml guides)")
            if RETIRED.search(s): err(f"retired story word '{RETIRED.search(s).group(0)}'")
            qid = q["id"]; moved = False
            if qid in prev and prev[qid]: moved = gate_of[prev[qid]] != ch
            if qid in entries: moved = True
            if moved and not TRAVEL.search(s): err("moves the party to a new zone but has no travel word")
            if "--warn" in sys.argv and CONTRAST.search(s):
                print(f"warn  {rel}: contrast framing '{CONTRAST.search(s).group(0)}'"); warns += 1
    if "--chain" in sys.argv:
        print("\nTRUNK CHAIN (zone: quest | guide named | travel word)")
        for qid in trunk:
            s = story_of(quest[qid]["page"].replace(".html", ".qmd")); gate = world["gates"][gate_of[qid]]
            g = next((x for x in gate.get("guides", []) if x in s or x.split()[-1] in s), "none")
            print(f"  {gate['name']}: {quest[qid]['title']} | {g} | {'travel' if TRAVEL.search(s) else '-'}")
    print(f"{errs} error(s), {warns} warning(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
