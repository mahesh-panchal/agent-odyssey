"""Screenshots for visual review. Usage: pixi run shots [outdir]. Default outdir: ./.shots (gitignored).
Covers: fresh map, narrow map, mid-game (cleared) map, and one page per question type, wide and narrow."""
import json, shutil, sys, tempfile
from pathlib import Path
from browser import Browser, serve

ROOT = Path(__file__).resolve().parent.parent
out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / ".shots"; out.mkdir(exist_ok=True)
tmp = Path(tempfile.mkdtemp(prefix="ao-shots-")); site = tmp / "site"; shutil.copytree(ROOT / "_site", site)
footer = (ROOT / "assets/html/footer.html").read_text()
banks = [json.loads(f.read_text()) for f in sorted((ROOT / "assets/data").glob("*-*.json")) if f.name != "world.json"]
for t in ("order", "sort", "faulty-line", "match", "choice"):          # one real question per type, shown on its own page
    q = next((q for b in banks for q in b.get("questions", []) if q["type"] == t), None)
    if q:
        (site / f"assets/data/shot-{t}.json").write_text(json.dumps({"pass": 0.8, "questions": [q]}))
        (site / f"shot-{t}.html").write_text('<!doctype html><link rel="stylesheet" href="assets/css/rpg.css"><body><div data-ao-test="shot-%s"></div>' % t + footer)
srv = serve(site, 8766); base = "http://127.0.0.1:8766/"
CLEARED = {"v": 1, "xp": 110, "passed": {"basecamp-name-the-fears": True, "basecamp-three-kinds-of-machine": True, "kennel-recruit-the-beast": True, "crypt-shield-of-undo": True},
           "prefs": {"companion": "claude-code", "language": "bash"}}

def fresh(B, url): B.go(base + "index.html"); B.js("localStorage.clear()"); B.go(base + url)
def cleared(B, url):
    B.go(base + "index.html"); B.js("localStorage.setItem('agent-odyssey:v1:state', %s)" % json.dumps(json.dumps(CLEARED))); B.go(base + url)
def view_test(B):                      # bring the quiz into the frame
    B.js("document.querySelector('[data-ao-test]').scrollIntoView({block:'center'})"); import time; time.sleep(0.3)
def wrong_then_view(B, url):          # a genuinely wrong answer, so the feedback state is on screen
    fresh(B, url); B.click_text("git commit -a"); view_test(B)

SHOTS = [
    ("map-fresh-wide", (1400, 900), lambda B: fresh(B, "index.html")),
    ("map-fresh-narrow", (600, 900), lambda B: fresh(B, "index.html")),
    ("map-midgame-wide", (1400, 900), lambda B: cleared(B, "index.html")),
    ("quest-choice-wrong-wide", (1400, 900), lambda B: wrong_then_view(B, "zones/crypt/shield-of-undo.html")),
    ("quest-order-wide", (1400, 900), lambda B: (fresh(B, "zones/kennel/recruit-the-beast.html"), B.click_text("Check order"), view_test(B))),
    ("quest-sort-wide", (1400, 900), lambda B: (fresh(B, "zones/crypt/rules-of-the-carapace.html"), B.click_text("Check sorting"), view_test(B))),
    ("type-faulty-line", (1400, 900), lambda B: (fresh(B, "shot-faulty-line.html"), B.js("document.querySelectorAll('.ao-line')[0].click()"), view_test(B))),
    ("type-match-wrong", (1400, 900), lambda B: (fresh(B, "shot-match.html"), B.click_text("Check matches"), view_test(B))),
    ("quest-boss-wide", (1400, 900), lambda B: (fresh(B, "zones/maze/wall-of-output.html"), B.click_text("Do not accept"), view_test(B))),
    ("quest-exercise-wide", (1400, 900), lambda B: fresh(B, "zones/maze/ground-truth.html")),
    ("character-midgame-wide", (1400, 1700), lambda B: cleared(B, "character.html")),
    ("character-fresh-narrow", (600, 2000), lambda B: fresh(B, "character.html")),
    ("quest-honour-wide", (1400, 900), lambda B: (fresh(B, "zones/crypt/secrets-and-sensitive-ground.html"), B.js("document.querySelector('.ao-honour').scrollIntoView({block:'center'})"), __import__("time").sleep(0.3))),
    ("quest-forest-narrow", (600, 1400), lambda B: fresh(B, "zones/forest/the-project-charter.html")),
    ("quest-forest-skill-wide", (1400, 900), lambda B: fresh(B, "zones/forest/forge-a-skill.html")),
    ("quest-gear-wide", (1400, 1500), lambda B: fresh(B, "zones/basecamp/know-your-gear.html")),
    ("quest-gear-narrow", (600, 1800), lambda B: fresh(B, "zones/basecamp/know-your-gear.html")),
    ("quest-reef-wide", (1400, 900), lambda B: fresh(B, "zones/reef/the-reviewers-code.html")),
    ("map-midgame-narrow", (600, 900), lambda B: cleared(B, "index.html")),
    ("quest-narrow", (600, 900), lambda B: fresh(B, "zones/kennel/pick-your-companion.html")),
]

def lore_view(B):                      # bring the Lore block into the frame
    B.js("document.querySelector('.ao-lore').scrollIntoView({block:'center'})"); __import__("time").sleep(0.3)
def page(name, url, w=1400, h=1400): return (name, (w, h), lambda B: fresh(B, url))
SHOTS += [
    page("quest-companion-wide", "zones/kennel/pick-your-companion.html"),
    page("quest-companion-narrow", "zones/kennel/pick-your-companion.html", 600, 1800),
    page("quest-cloud-wide", "zones/kennel/claude-in-the-cloud.html"),
    page("quest-cloud-narrow", "zones/kennel/claude-in-the-cloud.html", 600, 1800),
    ("quest-lore-wide", (1400, 900), lambda B: (fresh(B, "zones/kennel/claude-in-the-cloud.html"), lore_view(B))),
    ("quest-lore-narrow", (600, 900), lambda B: (fresh(B, "zones/kennel/claude-in-the-cloud.html"), lore_view(B))),
    page("lore-library-wide", "lore.html", 1400, 1800),
    page("lore-library-narrow", "lore.html", 600, 2400),
]
# Guided path: Start Here, the sealed and unlocked finale, the ending and the Wall boss.
_G = json.loads((ROOT / "assets/data/world.json").read_text())["graph"]
_QS = _G["quests"]; _FIN = _G["finale"]["id"]
def _ids(trunk=True, branches=()):
    return [i for i, q in _QS.items() if (trunk and q["trunk"]) or q.get("branch") in branches]
def with_state(B, url, ids):
    st = {"v": 1, "xp": 500, "passed": {i: True for i in ids}, "prefs": {}}
    B.go(base + "index.html"); B.js("localStorage.setItem('agent-odyssey:v1:state', %s)" % json.dumps(json.dumps(st))); B.go(base + url)
_B3 = [b["id"] for b in _G["branches"]][:3]
SHOTS += [
    page("path-start-here-wide", "start-here.html", 1400, 1800),
    page("path-start-here-narrow", "start-here.html", 600, 2400),
    ("path-start-here-midgame-wide", (1400, 1800), lambda B: with_state(B, "start-here.html", _ids(True, _B3[:1]))),
    ("path-start-here-unlocked-wide", (1400, 1800), lambda B: with_state(B, "start-here.html", _ids(True, _B3))),
    ("path-map-unlocked-wide", (1400, 900), lambda B: with_state(B, "index.html", _ids(True, _B3))),
    ("path-start-path-wide", (1400, 1200), lambda B: with_state(B, "start-here.html", _ids(True, _B3[:1]))),
    ("path-start-path-narrow", (500, 1600), lambda B: fresh(B, "start-here.html")),
    page("path-finale-sealed-wide", "zones/murk/clear-the-murk.html", 1400, 1800),
    page("path-finale-sealed-narrow", "zones/murk/clear-the-murk.html", 600, 2400),
    ("path-finale-unlocked-wide", (1400, 1800), lambda B: with_state(B, "zones/murk/clear-the-murk.html", _ids(True, _B3))),
    ("path-finale-cleared-wide", (1400, 1800), lambda B: with_state(B, "zones/murk/clear-the-murk.html", _ids(True, _B3) + [_FIN])),
    page("path-boss-wall-wide", "zones/maze/wall-of-output.html"),
    page("home-party-wide", "index.html", 1400, 2400),
    page("home-party-narrow", "index.html", 500, 3200),
    ("path-quest-nextsteps-wide", (1400, 900), lambda B: (with_state(B, "zones/basecamp/name-the-fears.html", ["basecamp-name-the-fears"]),
        B.js("(document.querySelector('.ao-nextsteps')||document.body).scrollIntoView({block:'center'})"))),
]
for z, slugs in {"citadel": ["jobs-not-jam", "keys-on-shared-ground", "login-node-manners"],
                 "gatehouse": ["plug-in-a-server", "guard-the-door", "advice-or-enforcement"],
                 "codon-mill": ["the-context-window", "tokens-not-letters", "memory-sessions-and-usage", "the-stream-of-ideas", "too-many-tools-too-many-agents", "when-to-start-fresh", "where-machines-fail", "who-said-what", "handoff-notes", "rag-and-its-cousins", "grow-a-graph-with-ollama", "llm-wiki"],
                 "factory": ["dry-run-first", "read-the-rails", "same-every-time"],
                 "scriptorium": ["run-it-top-to-bottom", "why-notebooks-diff-badly"],
                 "maze": ["spot-the-mirage"], "reef": ["send-small-say-so", "teach-and-share-the-load"],
                 "forest": ["bundle-a-plugin", "close-the-loop", "plan-before-you-edit", "test-the-skill", "write-the-brief"],
                 "basecamp": ["name-the-fears", "three-kinds-of-machine"], "crypt": []}.items():
    for sl in slugs:
        SHOTS.append(page(f"zone-{z}-{sl}-wide", f"zones/{z}/{sl}.html"))
        if z in ("citadel", "gatehouse"): SHOTS.append(page(f"zone-{z}-{sl}-narrow", f"zones/{z}/{sl}.html", 600, 1800))
only = set(sys.argv[2:])
for name, (w, h), steps in SHOTS:
    if only and name not in only: continue
    B = Browser(w, h)
    try:
        steps(B); B.shot(out / f"{name}.png"); print("wrote", out / f"{name}.png")
    finally: B.close()
srv.shutdown(); shutil.rmtree(tmp, ignore_errors=True)
