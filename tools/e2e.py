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


    check("map hides unreached gates by default", B.js("document.getElementById('ao-reveal').getAttribute('aria-pressed')") == "false")
    B.js("document.getElementById('ao-reveal').click()")
    check("Show the whole map toggle flips", B.js("document.getElementById('ao-reveal').getAttribute('aria-pressed')") == "true")
    B.js("document.getElementById('ao-reveal').click()")

    # --- a veiled gate refuses Enter ---
    B.js("localStorage.clear()"); B.go(base + "index.html")
    for k, n in (("ArrowUp", 2), ("ArrowRight", 14), ("ArrowUp", 4), ("ArrowRight", 1)):
        for _ in range(n): B.press(k, 0.08)
    B.press("Enter", 1.2)
    check("Enter on a veiled gate stays on the map", B.js("location.pathname").endswith("index.html") or B.js("location.pathname") == "/", B.js("location.pathname"))
    # --- walk to the Crypt from Basecamp: reload resets to start (3,8) ---
    B.go(base + "index.html"); B.js("document.getElementById('ao-reveal').click()")
    for k, n in (("ArrowUp", 2), ("ArrowRight", 14), ("ArrowUp", 4), ("ArrowRight", 1)):
        for _ in range(n): B.press(k, 0.08)
    check("hero reaches the Crypt gate (18,2)", pos() == '{"x":18,"y":2}', pos())
    B.press("Enter", 1.2)
    check("Enter on the open gate opens its quest", B.js("location.pathname").endswith("shield-of-undo.html"), B.js("location.pathname"))
    # --- quest test: first-try scoring, misconception text, pass ---
    wrong = {"Quest": 0}
    B.js("localStorage.clear()"); B.go(base + "zones/crypt/shield-of-undo.html")
    B.click_text("git commit -a")
    check("Next is hidden until the question is solved", B.js("[...document.querySelectorAll('button')].filter(b=>b.textContent.includes('Next')).every(b=>getComputedStyle(b).display==='none')"))
    check("wrong answer shows its misconception", "Committing records the broken state" in B.js("document.querySelector('.ao-fb').textContent"))
    B.click_text("git restore .")
    check("correct answer still explains why the others are wrong", B.js("!!document.querySelector('.ao-why') && document.querySelector('.ao-why').textContent.includes('Committing records the broken state')"))
    B.click_text("Next")
    B.click_text("After the agent"); B.click_text("Before letting"); B.click_text("Next")
    B.click_text("Both files are reverted"); B.click_text("analysis.py is reverted"); B.click_text("Next")
    res = B.js("document.querySelector('[data-ao-test]').textContent")
    check("first-try misses fail the 80% bar", "The Blight holds" in res, res)
    B.click_text("Fight again")
    B.click_text("git restore .")
    check("XP rises while answering, before the quest is cleared", B.js("AO.state.xp") > 0 and not B.js("!!AO.state.passed['crypt-shield-of-undo']"), B.js("AO.state.xp"))
    B.click_text("Next"); B.click_text("Before letting"); B.click_text("Next")
    B.click_text("analysis.py is reverted"); B.click_text("Next")
    check("clean run passes and awards XP", B.js("AO.state.xp") == 50 and B.js("!!AO.state.passed['crypt-shield-of-undo']"), B.js("JSON.stringify(AO.state)"))
    B.go(base + "zones/crypt/shield-of-undo.html"); B.press("m", 1.0)
    check("M key returns to the map from a quest page", B.js("location.pathname").endswith("index.html") or B.js("location.pathname") == "/", B.js("location.pathname"))
    check("Map button is the first HUD item", B.js("document.querySelector('#ao-hud').firstElementChild.textContent.includes('Map')"))
    # --- every quest page in the story data loads a test bank ---
    quests = json.loads(B.js("fetch('/assets/data/world.json').then(r=>r.json()).then(w=>JSON.stringify(Object.values(w.gates).flatMap(g=>g.quests||[])))"))
    for q in quests:
        B.go(base + q["page"], 1.0)
        check("quest page renders a test: " + q["id"], B.js("!!document.querySelector('.ao-round')"))
    # --- path graph: shared helper loads, finale starts locked, next quest follows the trunk ---
    B.go(base + "index.html", 1.0)
    check("path graph loads and the finale gate starts locked", B.js("AO.path.load().then(() => AO.path.finaleUnlocked() === false && AO.path.quest('murk-clear-the-murk').branch === 'finale')") is True)
    check("next quest follows the trunk, not zones.yml order", B.js("AO.path.load().then(() => AO.path.nextQuest().id)") == "basecamp-name-the-fears", B.js("AO.path.load().then(() => AO.path.nextQuest().id)"))
    # Three progress states, injected in the page only (restored afterwards, never saved).
    probe = """AO.path.load().then(G => {
      const old = AO.state.passed, rule = G.finale.requires.branches, f = G.finale.id;
      const build = (nb, withFinale) => { const p = {}; G.trunk_order.forEach(id => p[id] = true);
        rule.of.slice(0, nb).forEach(b => Object.keys(G.quests).forEach(id => { const q = G.quests[id]; if (q.branch === b && !q.optional) p[id] = true; }));
        if (withFinale) p[f] = true; return p; };
      const run = (nb, wf) => { AO.state.passed = build(nb, wf); const n = AO.path.nextQuest();
        return { unlocked: AO.path.finaleUnlocked(), next: n && n.id, nextBranch: n && G.quests[n.id] && G.quests[n.id].branch }; };
      const out = { f: f, short: run(rule.any - 1, false), full: run(rule.any, false), done: run(rule.any, true) };
      AO.state.passed = old; return JSON.stringify(out); })"""
    st = json.loads(B.js(probe))
    check("finale stays locked with the trunk and one branch too few", st["short"]["unlocked"] is False and st["short"]["next"] != st["f"], json.dumps(st["short"]))
    check("trunk plus the needed branches unlocks the finale and points to it", st["full"]["unlocked"] is True and st["full"]["next"] == st["f"], json.dumps(st["full"]))
    check("after the finale the next quest returns to a branch", st["done"]["next"] not in (None, st["f"]) and st["done"]["nextBranch"] not in ("trunk", "finale"), json.dumps(st["done"]))
    B.go(base + "zones/maze/wall-of-output.html", 1.0)
    check("boss fight shows a name and HP bar", B.js("!!document.querySelector('.ao-boss progress')") and "Wall of Output" in B.js("document.querySelector('.ao-boss').textContent"))
    check("exercise files are published", B.js("Promise.all(['tiny.fasta','gc.py'].map(f=>fetch('/exercises/maze/'+f).then(r=>r.ok)))").__class__ is list and all(B.js("Promise.all(['tiny.fasta','gc.py'].map(f=>fetch('/exercises/maze/'+f).then(r=>r.ok)))")))
    # --- Continue block: Next button follows the path, Related links sit apart ---
    B.go(base + "zones/basecamp/name-the-fears.html", 1.5)
    check("Continue block offers Next to the following quest", B.js("(document.querySelector('.ao-nextsteps [rel=next]')||{}).href||''").endswith("three-kinds-of-machine.html"), B.js("(document.querySelector('.ao-nextsteps [rel=next]')||{}).href||''"))
    check("Related lessons list is separate from the Continue block", B.js("!!document.querySelector('.ao-related') && !document.querySelector('.ao-nextsteps').contains(document.querySelector('.ao-related'))"))
    # --- quest log ---
    open0 = B.js("document.getElementById('ao-logbtn').getAttribute('aria-expanded')")
    B.click_text("Quest Log"); open1 = B.js("document.getElementById('ao-logbtn').getAttribute('aria-expanded')")
    check("quest log toggles", open0 != open1, f"{open0}->{open1}")
    B.click_text("Quest Log")
    check("quest log shows cleared quest and story", "✔" in B.js("document.getElementById('ao-log').textContent") and "Save Point" in B.js("document.getElementById('ao-log').textContent"))
    # --- arrow keys ignored inside widgets ---
    B.js("document.querySelector('[data-ao-test]').focus()")
    # --- save/load round trip ---
    code = B.js("AO.exportCode()"); B.js("localStorage.clear()"); B.go(base + "index.html")
    check("fresh state has no XP", B.js("AO.state.xp") == 0)
    B.js("AO.importCode(%s)" % json.dumps(code))
    check("save code round-trips", B.js("AO.state.xp") == 50)
    # --- honour item: bonus XP once, no farming; character sheet renders ---
    B.js("localStorage.clear()"); B.go(base + "zones/forest/the-project-charter.html", 1.0)
    B.js("document.querySelector('.ao-honour input').click()")
    xp1 = B.js("AO.state.xp"); B.js("document.querySelector('.ao-honour input').click()"); B.js("document.querySelector('.ao-honour input').click()")
    check("honour item gives bonus XP exactly once", xp1 == 15 and B.js("AO.state.xp") == 15, f"{xp1}/{B.js('AO.state.xp')}")
    B.go(base + "character.html", 1.0)
    check("character sheet shows skill tree, armour and level", all(B.js("document.getElementById('ao-character').textContent.includes(%s)" % json.dumps(t)) for t in ("Skill tree", "Armour", "Rank")))
    check("skill tree has a leaf per open quest", B.js("document.querySelectorAll('.ao-tree circle').length") >= 15, B.js("document.querySelectorAll('.ao-tree circle').length"))
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
