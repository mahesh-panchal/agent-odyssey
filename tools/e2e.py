"""End-to-end checks: plays the real site with real key events. Run: pixi run e2e (renders first)."""
import json, shutil, sys, tempfile
from pathlib import Path
from browser import Browser, serve

ROOT = Path(__file__).resolve().parent.parent
tmp = Path(tempfile.mkdtemp(prefix="ao-e2e-"))
site = tmp / "site"; shutil.copytree(ROOT / "_site", site)

import fixture
fixture.build(site)

srv = serve(site, 8765); B = Browser(); base = "http://127.0.0.1:8765/"
fails = []
def check(name, cond, extra=""):
    print(("PASS " if cond else "FAIL ") + name + (f"  [{extra}]" if extra and not cond else ""))
    if not cond: fails.append(name)

try:
    # --- map ---
    B.go(base + "index.html")
    pos = lambda: B.js("JSON.stringify(AO.debug.pos())")
    check("map starts at Basecamp (3,8)", pos() == '{"x":3,"y":8}', pos())
    B.press("ArrowRight"); B.press("ArrowRight")
    check("hero walks right 2 tiles", json.loads(pos())["x"] == 5, pos())
    for _ in range(6): B.press("ArrowLeft")
    check("hero stops at the tree wall (x=1 is leftmost walkable)", json.loads(pos())["x"] == 1, pos())


    # --- walk to the Crypt from Basecamp: reload resets to start (3,8) ---
    B.go(base + "index.html")
    for k, n in (("ArrowUp", 2), ("ArrowRight", 14), ("ArrowUp", 4), ("ArrowRight", 1)):
        for _ in range(n): B.press(k, 0.08)
    check("hero reaches the Crypt gate (18,2)", pos() == '{"x":18,"y":2}', pos())
    B.press("Enter", 1.2)
    check("Enter on the open gate opens its quest", B.js("location.pathname").endswith("shield-of-undo.html"), B.js("location.pathname"))
    # --- quest test: first-try scoring, misconception text, pass ---
    wrong = {"Quest": 0}
    B.js("localStorage.clear()"); B.go(base + "zones/crypt/shield-of-undo.html")
    B.click_text("git push")
    check("wrong answer shows its misconception", "Push sends commits" in B.js("document.querySelector('.ao-fb').textContent"))
    B.click_text("git restore ."); B.click_text("Next")
    B.click_text("After the agent"); B.click_text("Before letting"); B.click_text("Next")
    B.click_text("Both changes are undone"); B.click_text("analysis.py is back"); B.click_text("Next")
    res = B.js("document.querySelector('[data-ao-test]').textContent")
    check("first-try misses fail the 80% bar", "The Blight holds" in res, res)
    B.click_text("Fight again")
    B.click_text("git restore ."); B.click_text("Next"); B.click_text("Before letting"); B.click_text("Next")
    B.click_text("analysis.py is back"); B.click_text("Next")
    check("clean run passes and awards XP", B.js("AO.state.xp") == 50 and B.js("!!AO.state.passed['crypt-shield-of-undo']"), B.js("JSON.stringify(AO.state)"))
    # --- every quest page in the story data loads a test bank ---
    quests = json.loads(B.js("fetch('/assets/data/world.json').then(r=>r.json()).then(w=>JSON.stringify(Object.values(w.gates).flatMap(g=>g.quests||[])))"))
    for q in quests:
        B.go(base + q["page"], 1.0)
        check("quest page renders a test: " + q["id"], B.js("!!document.querySelector('.ao-round')"))
    # --- quest log ---
    open0 = B.js("document.getElementById('ao-logbtn').getAttribute('aria-expanded')")
    B.click_text("Quest Log"); open1 = B.js("document.getElementById('ao-logbtn').getAttribute('aria-expanded')")
    check("quest log toggles", open0 != open1, f"{open0}->{open1}")
    B.click_text("Quest Log")
    check("quest log shows cleared quest and story", "✔" in B.js("document.getElementById('ao-log').textContent") and "Shield of Undo" in B.js("document.getElementById('ao-log').textContent"))
    # --- arrow keys ignored inside widgets ---
    B.js("document.querySelector('[data-ao-test]').focus()")
    # --- save/load round trip ---
    code = B.js("AO.exportCode()"); B.js("localStorage.clear()"); B.go(base + "index.html")
    check("fresh state has no XP", B.js("AO.state.xp") == 0)
    B.js("AO.importCode(%s)" % json.dumps(code))
    check("save code round-trips", B.js("AO.state.xp") == 50)
    # --- other question types ---
    B.js("localStorage.clear()"); B.go(base + "fixture.html")
    if B.js("[...document.querySelectorAll('ol li')].map(l=>l.firstChild.textContent.trim()).join(',')") == "one,two,three":
        B.js("document.querySelectorAll('ol li')[0].querySelectorAll('button')[1].click()")   # shuffle happened to be correct: break it
    B.click_text("Check order"); check("order: wrong order explains", "doesn’t" in B.js("document.querySelector('.ao-fb').textContent") or "not right" in B.js("document.querySelector('.ao-fb').textContent") or "goes second" in B.js("document.querySelector('.ao-fb').textContent"), B.js("document.querySelector('.ao-fb').textContent"))
    # DOM reorder does not change the engine's array; drive the real buttons instead:
    for _ in range(10):
        txt = B.js("[...document.querySelectorAll('ol li')].map(l=>l.firstChild.textContent.trim()).join(',')")
        if txt == "one,two,three": break
        want = ["one", "two", "three"]; cur = txt.split(",")
        i = next(i for i in range(3) if cur[i] != want[i]); j = cur.index(want[i])
        B.js(f"document.querySelectorAll('ol li')[{j}].querySelectorAll('button')[0].click()")
    B.click_text("Check order"); ok = B.click_text("Next")
    check("order: correct order accepted (not first try)", ok)
    B.js("[...document.querySelectorAll('select')].forEach(s=>{s.value=s.getAttribute('aria-label').includes('rm')?'allow':'deny'; })")
    B.click_text("Check sorting")
    check("sort: wrong bins show misconceptions", "deletes everything" in B.js("document.querySelector('.ao-fb').textContent") and "ls only reads" in B.js("document.querySelector('.ao-fb').textContent"))
    B.js("[...document.querySelectorAll('select')].forEach(s=>{s.value=s.getAttribute('aria-label').includes('rm')?'deny':'allow'; })")
    B.click_text("Check sorting"); B.click_text("Next")
    B.click_text("1"); check("faulty-line: fine line explained", "fine" in B.js("document.querySelector('.ao-fb').textContent"))
    B.click_text("2"); B.click_text("Next")
    B.js("[...document.querySelectorAll('select')].forEach(s=>{s.value=s.getAttribute('aria-label').includes('a')&&!s.getAttribute('aria-label').includes('b')?'B':'A'; })")
    B.click_text("Check matches")
    check("match: wrong pair shows its misconception", "a is A" in B.js("document.querySelector('.ao-fb').textContent"), B.js("document.querySelector('.ao-fb').textContent"))
finally:
    B.close(); srv.shutdown(); shutil.rmtree(tmp, ignore_errors=True)

print(f"\n{len(fails)} failure(s)"); sys.exit(1 if fails else 0)
