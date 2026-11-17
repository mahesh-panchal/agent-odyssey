/* Overworld: canvas tile map, walking hero, gates, Murk over uncleared zones. */
(function () {
  var cv = document.getElementById("ao-world");
  if (!cv) return;
  var T = 16, ctx = cv.getContext("2d"), cap = document.getElementById("ao-caption");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function img(src) { return new Promise(function (r) { var i = new Image(); i.onload = function () { r(i); }; i.src = window.AO_BASE + src; }); }
  Promise.all([fetch(window.AO_BASE + "assets/data/world.json").then(function (r) { return r.json(); }),
               img("assets/img/tiles.png"), img("assets/img/hero.png")]).then(function (a) { start(a[0], a[1], a[2]); });

  function start(world, tiles, hero) {
    var rows = world.map, W = rows[0].length, H = rows.length;
        var TILE = { ".": 0, "=": 1, "~": 2, "#": 3, "o": 5 };
    var gateAt = {}; Object.keys(world.gates).forEach(function (k) { var g = world.gates[k]; gateAt[g.x + "," + g.y] = g; });
    function walkable(x, y) { var c = (rows[y] || "")[x]; return c !== undefined && c !== "#" && c !== "~" && c !== "o"; }
    function cleared(g) { return g.quests && g.quests.length && g.quests.every(function (q) { return AO.state.passed[q.id]; }); }
    var g0 = world.gates[AO.state.prefs.pos && world.gates[AO.state.prefs.pos] ? AO.state.prefs.pos : world.start];
    var p = { x: g0.x, y: g0.y, px: g0.x, py: g0.y, dir: 0, frame: 1, t: 0 };   // px/py = drawn (tweened) position
    var DIR = { down: 0, left: 1, right: 2, up: 3 };

    function firstOpen() { return Object.keys(gateAt).map(function (k) { return gateAt[k]; }).filter(function (g) { return g.status === "open" && !cleared(g); })[0] || {}; }
    function remember(g) { AO.state.prefs.pos = Object.keys(world.gates).find(function (k) { return world.gates[k] === g; }); try { localStorage.setItem("agent-odyssey:v1:state", JSON.stringify(AO.state)); } catch (e) {} }
    function say() {
      var g = gateAt[p.x + "," + p.y];
      var nx = document.getElementById("ao-next"), f = firstOpen();
      if (nx) nx.textContent = f.name ? "▶ Next: walk to the gold gate — " + f.name + " — and press Enter." : "Every open zone is cleared. More zones open in later versions.";
      if (g && g.id === world.gates[world.start].id && g.status !== "open") { cap.textContent = "You are at " + g.name + ", where the journey starts."; return; }
      if (!g) { cap.textContent = "Walk with the arrow keys or WASD. Your first quest is at the gold gate: " + firstOpen().name + "."; return; }
      cap.textContent = g.name + " (" + g.track + ") — " +
        (g.status === "open" ? (cleared(g) ? "cleared. Press Enter to revisit." : "the Murk lingers. Press Enter to enter.")
                             : "thick Murk. Not open yet. Press Enter to look.") +
        (Object.keys(AO.state.passed).length ? "" : " Your first quest is at the gold gate: " + firstOpen().name + ".");
    }
    function move(dx, dy, dir) {
      p.dir = dir;
      if (walkable(p.x + dx, p.y + dy)) { p.x += dx; p.y += dy; p.frame = (p.frame + 1) % 3; p.t = reduce ? 1 : 0; }
      say();
    }
    function enter() {
      var g = gateAt[p.x + "," + p.y]; if (!g) return;
      remember(g);
      if (g.status === "open") {
        var q = g.quests.find(function (q) { return !AO.state.passed[q.id]; }) || g.quests[0];
        location.href = window.AO_BASE + q.page;
      } else {
        cap.textContent = g.name + " lies under thick Murk. It has not opened yet. Come back in a later version.";
      }
    }
    document.addEventListener("keydown", function (e) {
      if (e.altKey || e.ctrlKey || e.metaKey) return;
      if (e.target.closest && e.target.closest("input,textarea,select,button,a")) return;
      var k = e.key.toLowerCase();
      var m = { arrowup: [0, -1, 3], w: [0, -1, 3], arrowdown: [0, 1, 0], s: [0, 1, 0],
                arrowleft: [-1, 0, 1], a: [-1, 0, 1], arrowright: [1, 0, 2], d: [1, 0, 2] }[k];
      if (m) { e.preventDefault(); move(m[0], m[1], m[2]); }
      else if (k === "enter" || k === " ") { e.preventDefault(); enter(); }
    });

    var S = 3;                                   // canvas px per art px; text is drawn crisp at this scale
    cv.width = W * T * S; cv.height = H * T * S;
    function layer() { var c = document.createElement("canvas"); c.width = cv.width; c.height = cv.height;
      var x = c.getContext("2d"); x.imageSmoothingEnabled = false; return [c, x]; }
    var base = layer(), fog = layer(), lab = layer();
    ctx.imageSmoothingEnabled = false;
    var COLORS = { Prologue: "#9ad", Companions: "#e98", Armour: "#e8b84a", Trust: "#8e8", Skills: "#6d9", Level: "#7be", Craft: "#c9f" };

    function buildBase() {
      var b = base[1];
      for (var y = 0; y < H; y++) for (var x = 0; x < W; x++) {
        var c = rows[y][x], idx = gateAt[x + "," + y] ? 4 : (TILE[c] === undefined ? 0 : TILE[c]);
        if (idx === 3 || idx === 5 || idx === 4) b.drawImage(tiles, (idx === 4 ? 1 : 0) * T, 0, T, T, x * T * S, y * T * S, T * S, T * S);
        b.drawImage(tiles, idx * T, 0, T, T, x * T * S, y * T * S, T * S, T * S);
      }
    }
    function buildOverlays() {
      var f = fog[1], l = lab[1]; f.clearRect(0, 0, cv.width, cv.height); l.clearRect(0, 0, cv.width, cv.height);
      l.font = "bold 20px ui-monospace, monospace"; l.textAlign = "center"; l.textBaseline = "middle";
      Object.keys(gateAt).forEach(function (k) {
        var g = gateAt[k], done = cleared(g), cx = (g.x + .5) * T * S, cy = (g.y + .5) * T * S;
        if (!done) {
          var r = 2.6 * T * S, a = g.status === "open" ? .2 : (g.id === "basecamp" ? 0 : .8);
          var gr = f.createRadialGradient(cx, cy, 6, cx, cy, r);
          gr.addColorStop(0, "rgba(70,20,110," + a + ")"); gr.addColorStop(1, "rgba(70,20,110,0)");
          f.fillStyle = gr; f.fillRect(cx - r, cy - r, 2 * r, 2 * r);
        }
        var nxt = firstOpen() === g, txt = (done ? "✔ CLEARED: " : g.id === "basecamp" ? "⌂ START: " : nxt ? "▶ NEXT: " : g.status === "open" ? "OPEN: " : "🔒 ") + g.name, ly = cy - 1.05 * T * S;
        var w = l.measureText(txt).width + 12, lx = Math.min(Math.max(cx, w / 2 + 2), cv.width - w / 2 - 2);
        l.fillStyle = "rgba(20,16,31,.88)"; l.fillRect(lx - w / 2, ly - 14, w, 28);
        l.fillStyle = done ? "#7bd88f" : g.status === "open" ? "#e8b84a" : "#cfc8e0"; l.fillText(txt, lx, ly);
        l.fillStyle = COLORS[g.track] || "#fff"; l.fillRect(lx - w / 2, ly + 14, w, 4);
      });
    }
    buildBase(); buildOverlays();
    AO.hooks.push(function () { buildOverlays(); say(); });

    var open = Object.keys(gateAt).map(function (k) { return gateAt[k]; }).filter(function (g) { return g.status === "open" && !cleared(g); })[0];
    function draw(now) {
      p.px += (p.x - p.px) * (reduce ? 1 : 0.35); p.py += (p.y - p.py) * (reduce ? 1 : 0.35);
      ctx.drawImage(base[0], 0, 0);
      var moving = Math.abs(p.px - p.x) + Math.abs(p.py - p.y) > 0.05, hx = Math.round(p.px * T * S), hy = Math.round(p.py * T * S) - 3 * S;
      ctx.fillStyle = "rgba(255,255,255,.22)"; ctx.beginPath(); ctx.ellipse(hx + T * S / 2, hy + T * S - 2, T * S * .45, T * S * .18, 0, 0, 7); ctx.fill();
      ctx.drawImage(hero, (moving ? p.frame : 1) * T, p.dir * T, T, T, hx - T * S * .125, hy - T * S * .25, T * S * 1.25, T * S * 1.25);
      ctx.globalAlpha = reduce ? 1 : .85 + .15 * Math.sin(now / 800); ctx.drawImage(fog[0], 0, 0); ctx.globalAlpha = 1;
      ctx.drawImage(lab[0], 0, 0);
      if (open) {                                           // gold marker over the open zone: "start here"
        var bob = reduce ? 0 : Math.sin(now / 250) * 3, mx = (open.x + .5) * T * S, my = (open.y + 1.55) * T * S + bob;
        ctx.fillStyle = "#e8b84a"; ctx.beginPath(); ctx.moveTo(mx - 9, my + 12); ctx.lineTo(mx + 9, my + 12); ctx.lineTo(mx, my - 4); ctx.fill();
      }
      requestAnimationFrame(draw);
    }
    AO.debug = { pos: function () { return { x: p.x, y: p.y }; } };
    say(); requestAnimationFrame(draw);
  }
})();
