/* Character sheet: skill tree (a spine of trunk quests with branches), armour plates, level. Renders into #ao-character if present. */
(function () {
  var host = document.getElementById("ao-character"); if (!host) return;
  var RANKS = ["Spore", "Plankton", "Grazer", "Forager", "Hunter", "Keystone"];
  function esc(t) { var d = document.createElement("div"); d.textContent = t; return d.innerHTML; }
  fetch(window.AO_BASE + "assets/data/world.json").then(function (r) { return r.json(); }).then(function (w) {
    var gates = Object.keys(w.gates).map(function (k) { return w.gates[k]; });
    function paint() {
      var done = AO.state.passed, byTrack = function (t) { return gates.filter(function (g) { return g.track === t; })[0]; };
      var cleared = Object.keys(done).filter(function (k) { return k.indexOf("honour-") !== 0; }).length;
      var rank = Math.min(RANKS.length - 1, Math.floor(cleared / 3));

      /* Level */
      var html = "<h2>Level</h2><p><strong>Rank: " + RANKS[rank] + "</strong> · XP " + AO.state.xp + " · quests cleared " + cleared +
        "</p><p class='ao-soft'>Rank rises as you clear quests. Optional honour items add XP but never rank.</p>";

      /* Armour */
      var arm = byTrack("Armour"), plates = [];
      if (arm && arm.quests) arm.quests.forEach(function (q) { plates.push([q.title, !!done[q.id], q.done, arm.name]); });
      html += "<h2>Armour</h2><div class='ao-armour'>" + (plates.length ? plates.map(function (p) {
        return "<div class='" + (p[1] ? "on" : "") + "'><strong>" + (p[1] ? "✔ " : "○ ") + esc(p[0]) + "</strong><br>" + (p[1] ? esc(p[2]) : "not yet forged. Clear this quest in the " + esc(p[3]) + ".") + "</div>";
      }).join("") : "<p>No armour quests yet.</p>") + "</div>";

      /* Skill tree: a vertical spine of trunk quests (first at the bottom, final boss at the top). Each branch grows sideways from the
         spine quest it depends on, on a grid: one column per step, one row per spine quest. Lines are straight or right-angled and follow
         each quest's first dependency; readiness uses all of them. Nodes are links; names show on hover and focus. */
      var tracks = gates.filter(function (g) { return g.quests && g.quests.length; });
      var G = w.graph, GQ = G.quests, trunk = G.trunk_order, fin = G.finale.id, base = window.AO_BASE || "./";
      var total = Object.keys(GQ).length, N = trunk.length, ROW = 46, COL = 44, TOP = 70;
      var pos = {}, cell = { L: {}, R: {} }, minC = 0, minR = 0, maxR = N, edgeList = [], heads = [];
      trunk.forEach(function (id, i) { pos[id] = { c: 0, r: i, kind: "trunk" }; });
      pos[fin] = { c: 0, r: N, kind: "boss" };
      var tIdx = function (id) { return trunk.indexOf(id); };
      var free = function (sd, c, r) { return r >= -3 && r <= N && !cell[sd][c + ":" + r]; };
      var primary = function (id) { var same = GQ[id].after.filter(function (d) { return GQ[d] && GQ[d].branch === GQ[id].branch && tIdx(d) < 0; }); return same[0] || null; };
      var kids = function (id) { return Object.keys(GQ).filter(function (k) { return tIdx(k) < 0 && primary(k) === id; }); };
      var place = function (id, sd, c, r, parent) {
        var q = GQ[id];
        for (var k = 0; k < 40; k++) {
          var rr = r + (k % 2 ? -1 : 1) * Math.ceil(k / 2);
          if (free(sd, c, rr)) {
            cell[sd][c + ":" + rr] = id; pos[id] = { c: c, r: rr, sd: sd, kind: q.optional ? "opt" : "req" }; edgeList.push([parent, id]);
            minC = Math.max(minC, c); minR = Math.min(minR, rr); maxR = Math.max(maxR, rr);
            kids(id).forEach(function (kid) { place(kid, sd, c + 1, rr, id); });
            return rr;
          }
        }
      };
      var roots = Object.keys(GQ).filter(function (id) { return tIdx(id) < 0 && id !== fin && !primary(id); }), flip = 0;
      var anchorOf = function (id) { var t = GQ[id].after.map(tIdx).filter(function (i) { return i >= 0; }); return t.length ? Math.max.apply(null, t) : 0; };
      roots.sort(function (p, q) { return anchorOf(p) - anchorOf(q); }).forEach(function (id) {
        var a = anchorOf(id), order = flip++ % 2 ? ["L", "R"] : ["R", "L"], done1 = false;
        for (var k = 0; k < 14 && !done1; k++) {
          var rr = a + (k % 2 ? -1 : 1) * Math.ceil(k / 2);
          order.forEach(function (sd) { if (!done1 && free(sd, 1, rr)) { place(id, sd, 1, rr, trunk[a]); done1 = true; } });
        }
        var bname = G.branches.filter(function (b) { return b.id === GQ[id].branch; })[0];
        if (bname && !heads.some(function (h) { return h.id === bname.id; }) && pos[id]) heads.push({ id: bname.id, name: bname.name, at: id });
      });
      var padL = 30, SIDE = (minC + 1) * COL + padL, W = SIDE * 2, H = TOP + (maxR - minR + 1) * ROW + 40;
      var X = function (p) { return SIDE + (p.sd === "L" ? -1 : 1) * p.c * COL; }, Y = function (p) { return TOP + (maxR - p.r) * ROW; };
      var stOf = function (id) {
        if (done[id]) return "cleared";
        if (id === fin) return AO.path && AO.path.finaleUnlocked && AO.path.finaleUnlocked() ? "ready" : "locked";
        return GQ[id].after.every(function (d) { return done[d]; }) ? "ready" : "locked";
      };
      var edges = "", nodes = "", edgeOf = function (a, b) {
        var pa = pos[a], pb = pos[b], x1 = X(pa), y1 = Y(pa), x2 = X(pb), y2 = Y(pb), d;
        if (x1 === x2 || y1 === y2) d = "M" + x1 + " " + y1 + " L" + x2 + " " + y2;
        else { var xm = Math.round((x1 + x2) / 2); d = "M" + x1 + " " + y1 + " H" + xm + " V" + y2 + " H" + x2; }
        edges += "<path class='ao-edge " + (done[a] ? "lit" : "dim") + "' d='" + d + "'/>";
      };
      trunk.forEach(function (id, i) { edgeOf(id, i + 1 < N ? trunk[i + 1] : fin); });
      edgeList.forEach(function (e) { edgeOf(e[0], e[1]); });
      Object.keys(pos).forEach(function (id) {
        var q = GQ[id], p = pos[id], st = stOf(id), x = X(p), y = Y(p), r = p.kind === "boss" ? 22 : p.kind === "trunk" ? 13 : p.kind === "opt" ? 8 : 11;
        var left = p.sd === "L", words = st === "cleared" ? "cleared" : st === "ready" ? "ready" : "locked";
        var shape = p.kind === "opt"
          ? "<polygon class='shape' points='" + x + "," + (y - r - 2) + " " + (x + r + 2) + "," + y + " " + x + "," + (y + r + 2) + " " + (x - r - 2) + "," + y + "'/>"
          : "<circle class='shape' cx='" + x + "' cy='" + y + "' r='" + r + "'/>";
        var mark = st === "cleared" ? "<path class='ao-tick' d='M" + (x - r / 2) + " " + y + " l" + (r / 3) + " " + (r / 3) + " l" + (r * 0.7) + " " + (-r * 0.7) + "' fill='none'/>"
          : st === "locked" ? "<text class='ao-lock' x='" + x + "' y='" + (y + 5) + "' text-anchor='middle'>" + (p.kind === "boss" ? "🔒" : "") + "</text>" : "";
        var ring = st === "ready" ? "<circle class='ao-pulse' cx='" + x + "' cy='" + y + "' r='" + (r + 5) + "'/>" : "";
        nodes += "<a class='ao-node st-" + st + " k-" + p.kind + "' href='" + base + q.page + "' aria-label='" + esc(q.title) + (q.optional ? " (side quest)" : "") + ", " + words + "'><g class='" + (st === "cleared" ? "on" : "") + "'>" +
          "<title>" + esc(q.title) + (q.optional ? " (side quest)" : "") + ", " + words + "</title>" + ring + shape + mark +
          "<text class='lbl' x='" + (left || p.kind === "trunk" && false ? x - r - 8 : x + r + 8) + "' y='" + (y + 4) + "' text-anchor='" + (left ? "end" : "start") + "'>" + esc(q.title) + "</text></g></a>";
      });
      var labels = "<text class='ao-branchname' x='" + SIDE + "' y='" + (TOP - 44) + "' text-anchor='middle'>Final boss</text>" +
        "<text class='ao-branchname' x='" + SIDE + "' y='" + (H - 8) + "' text-anchor='middle'>Start</text>";
      heads.forEach(function (h) {
        var p = pos[h.at], left = p.sd === "L";
        labels += "<text class='ao-branchname' x='" + (X(p) + (left ? 12 : -12)) + "' y='" + (Y(p) - 18) + "' text-anchor='" + (left ? "end" : "start") + "'>" + esc(h.name) + "</text>";
      });
      var legend = "<p class='ao-treekey'><span>● cleared (tick)</span> <span>◎ ready (ringed)</span> <span>◌ locked (dashed)</span> <span>◆ side quest</span> Hover or focus a node for its name.</p>";
      html += "<h2>Skill tree</h2>" + legend + "<div class='ao-treewrap'><svg class='ao-tree' viewBox='0 0 " + W + " " + H + "' role='group' aria-label='Skill tree: " + cleared + " of " + total + " quests cleared'>" +
        labels + edges + nodes + "</svg></div>";
      html += "<details class='ao-textlist'><summary>Skill tree as text</summary><ul>" + tracks.map(function (g) {
        return "<li><strong>" + esc(g.name) + "</strong> (" + esc(g.track) + "): " + g.quests.map(function (q) { return (done[q.id] ? "✔ " : "○ ") + esc(q.title); }).join(", ") + "</li>";
      }).join("") + "</ul></details>";
      host.innerHTML = html;
    }
    AO.hooks.push(paint); paint();
  });
})();
