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
CLEARED = {"v": 1, "xp": 110, "passed": {"kennel-recruit-the-beast": True, "kennel-adopt-the-pet": True, "crypt-shield-of-undo": True},
           "prefs": {"companion": "claude-code", "language": "bash"}}

def fresh(B, url): B.go(base + "index.html"); B.js("localStorage.clear()"); B.go(base + url)
def cleared(B, url):
    B.go(base + "index.html"); B.js("localStorage.setItem('agent-odyssey:v1:state', %s)" % json.dumps(json.dumps(CLEARED))); B.go(base + url)
def view_test(B):                      # bring the quiz into the frame
    B.js("document.querySelector('[data-ao-test]').scrollIntoView({block:'center'})"); import time; time.sleep(0.3)
def wrong_then_view(B, url):          # a genuinely wrong answer, so the feedback state is on screen
    fresh(B, url); B.click_text("git push"); view_test(B)

SHOTS = [
    ("map-fresh-wide", (1400, 900), lambda B: fresh(B, "index.html")),
    ("map-fresh-narrow", (600, 900), lambda B: fresh(B, "index.html")),
    ("map-midgame-wide", (1400, 900), lambda B: cleared(B, "index.html")),
    ("quest-choice-wrong-wide", (1400, 900), lambda B: wrong_then_view(B, "zones/crypt/shield-of-undo.html")),
    ("quest-order-wide", (1400, 900), lambda B: (fresh(B, "zones/kennel/recruit-the-beast.html"), B.click_text("Check order"), view_test(B))),
    ("quest-sort-wide", (1400, 900), lambda B: (fresh(B, "zones/crypt/rules-of-the-carapace.html"), B.click_text("Check sorting"), view_test(B))),
    ("type-faulty-line", (1400, 900), lambda B: (fresh(B, "shot-faulty-line.html"), B.js("document.querySelectorAll('.ao-line')[0].click()"), view_test(B))),
    ("type-match-wrong", (1400, 900), lambda B: (fresh(B, "shot-match.html"), B.click_text("Check matches"), view_test(B))),
    ("quest-narrow", (600, 900), lambda B: fresh(B, "zones/kennel/adopt-the-pet.html")),
]
only = set(sys.argv[2:])
for name, (w, h), steps in SHOTS:
    if only and name not in only: continue
    B = Browser(w, h)
    try:
        steps(B); B.shot(out / f"{name}.png"); print("wrote", out / f"{name}.png")
    finally: B.close()
srv.shutdown(); shutil.rmtree(tmp, ignore_errors=True)
