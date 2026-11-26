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

      /* Skill tree: the trunk is a spine from the first quest (bottom) to the final boss (top). Each branch sprouts from the spine
         at the trunk quest it depends on; lines follow the `after` edges. Nodes are links; labels show on hover and focus. */
      var tracks = gates.filter(function (g) { return g.quests && g.quests.length; });
      var G = w.graph, GQ = G.quests, trunk = G.trunk_order, fin = G.finale.id, base = window.AO_BASE || "./";
      var total = Object.keys(GQ).length, ROW = 70, PAD = 70, COLW = 200, STEP = 56, SPINE = 0;
      var trunkY = function (i) { return PAD + (trunk.length - i) * ROW; };
      var pos = {}, headers = [];
      trunk.forEach(function (id, i) { pos[id] = { x: 0, y: trunkY(i), kind: "trunk" }; });
      pos[fin] = { x: 0, y: PAD - 20, kind: "boss" };
      var lvl = function (id, memo) {
        if (memo[id] != null) return memo[id];
        var ins = GQ[id].after.filter(function (d) { return GQ[d] && GQ[d].branch === GQ[id].branch; });
        return (memo[id] = ins.length ? 1 + Math.max.apply(null, ins.map(function (d) { return lvl(d, memo); })) : 0);
      };
      var tIdx = function (id) { return trunk.indexOf(id); };
      var anchor = {};
      for (var pass = 0; pass < 4; pass++) G.branches.forEach(function (b) {
        var best = -1;
        Object.keys(GQ).filter(function (id) { return GQ[id].branch === b.id; }).forEach(function (id) {
          GQ[id].after.forEach(function (d) {
            var t = tIdx(d); if (t < 0 && GQ[d] && anchor[GQ[d].branch] != null) t = anchor[GQ[d].branch];
            if (t > best) best = t;
          });
        });
        anchor[b.id] = best >= 0 ? best : trunk.length - 1;
      });
      var cols = { L: [], R: [] }, maxCol = 0;
      G.branches.slice().sort(function (p, q) { return anchor[p.id] - anchor[q.id]; }).forEach(function (b, bi) {
        var ids = Object.keys(GQ).filter(function (id) { return GQ[id].branch === b.id; }), memo = {};
        var byLvl = {}; ids.forEach(function (id) { var l = lvl(id, memo); (byLvl[l] = byLvl[l] || []).push(id); });
        var yTop = trunkY(anchor[b.id]) - Math.max.apply(null, Object.keys(byLvl)) * STEP, yBot = trunkY(anchor[b.id]);
        var sides = bi % 2 ? ["L", "R"] : ["R", "L"], put = null;
        for (var c = 0; c < 6 && !put; c++) sides.forEach(function (sd) {
          if (put) return;
          var used = cols[sd][c] = cols[sd][c] || [];
          if (!used.some(function (r) { return yTop - 50 < r[1] && yBot + 30 > r[0]; })) { used.push([yTop - 50, yBot]); put = { sd: sd, c: c }; }
        });
        maxCol = Math.max(maxCol, put.c);
        var cx = (put.sd === "R" ? 1 : -1) * (150 + put.c * COLW);
        Object.keys(byLvl).forEach(function (l) {
          byLvl[l].forEach(function (id, j) {
            pos[id] = { x: cx + (j - (byLvl[l].length - 1) / 2) * 62, y: yBot - l * STEP, kind: GQ[id].optional ? "opt" : "req", side: put.sd };
          });
        });
        headers.push({ name: b.name, x: cx, y: yTop - 30 });
      });
      var halfW = 150 + maxCol * COLW + 120, W = halfW * 2, H = trunkY(0) + PAD, X = function (v) { return Math.round(halfW + v); };
      var stOf = function (id) {
        if (done[id]) return "cleared";
        if (id === fin) return AO.path && AO.path.finaleUnlocked && AO.path.finaleUnlocked() ? "ready" : "locked";
        return GQ[id].after.every(function (d) { return done[d]; }) ? "ready" : "locked";
      };
      var edges = "", nodes = "";
      Object.keys(GQ).forEach(function (id) {
        var deps = GQ[id].after.slice();
        if (id === fin) deps = [trunk[trunk.length - 1]];
        deps.forEach(function (d) {
          if (!pos[d] || !pos[id]) return;
          var x1 = X(pos[d].x), y1 = pos[d].y, x2 = X(pos[id].x), y2 = pos[id].y, ym = Math.round((y1 + y2) / 2);
          edges += "<path class='ao-edge " + (done[d] ? "lit" : "dim") + "' d='M" + x1 + " " + y1 + " C" + x1 + " " + ym + " " + x2 + " " + ym + " " + x2 + " " + y2 + "'/>";
        });
      });
      Object.keys(pos).forEach(function (id) {
        var q = GQ[id], p = pos[id], st = stOf(id), x = X(p.x), y = p.y, r = p.kind === "boss" ? 24 : p.kind === "trunk" ? 16 : p.kind === "opt" ? 10 : 13;
        var left = p.side === "L", words = st === "cleared" ? "cleared" : st === "ready" ? "ready" : "locked";
        var shape = p.kind === "opt"
          ? "<polygon class='shape' points='" + x + "," + (y - r - 2) + " " + (x + r + 2) + "," + y + " " + x + "," + (y + r + 2) + " " + (x - r - 2) + "," + y + "'/>"
          : "<circle class='shape' cx='" + x + "' cy='" + y + "' r='" + r + "'/>";
        var mark = st === "cleared" ? "<path class='ao-tick' d='M" + (x - r / 2) + " " + y + " l" + (r / 3) + " " + (r / 3) + " l" + (r * 0.7) + " " + (-r * 0.7) + "' fill='none'/>"
          : st === "locked" ? "<text class='ao-lock' x='" + x + "' y='" + (y + 5) + "' text-anchor='middle'>" + (p.kind === "boss" ? "🔒" : "") + "</text>" : "";
        var ring = st === "ready" ? "<circle class='ao-pulse' cx='" + x + "' cy='" + y + "' r='" + (r + 6) + "'/>" : "";
        nodes += "<a class='ao-node st-" + st + " k-" + p.kind + "' href='" + base + q.page + "' aria-label='" + esc(q.title) + (q.optional ? " (side quest)" : "") + ", " + words + "'><g class='" + (st === "cleared" ? "on" : "") + "'>" +
          "<title>" + esc(q.title) + (q.optional ? " (side quest)" : "") + ", " + words + "</title>" + ring + shape + mark +
          "<text class='lbl' x='" + (left ? x - r - 10 : x + r + 10) + "' y='" + (y + 5) + "' text-anchor='" + (left ? "end" : "start") + "'>" + esc(q.title) + "</text></g></a>";
      });
      var heads = headers.map(function (h) { return "<text class='ao-branchname' x='" + X(h.x) + "' y='" + h.y + "' text-anchor='middle'>" + esc(h.name) + "</text>"; }).join("");
      var legend = "<p class='ao-treekey'><span>● cleared (tick)</span> <span>◎ ready (ringed)</span> <span>◌ locked (dashed)</span> <span>◆ side quest</span> Hover or focus a node for its name.</p>";
      html += "<h2>Skill tree</h2>" + legend + "<div class='ao-treewrap' tabindex='-1'><svg class='ao-tree' width='" + W + "' height='" + H + "' viewBox='0 0 " + W + " " + H + "' role='group' aria-label='Skill tree: " + cleared + " of " + total + " quests cleared'>" +
        heads + edges + nodes + "</svg></div>";
      html += "<details class='ao-textlist'><summary>Skill tree as text</summary><ul>" + tracks.map(function (g) {
        return "<li><strong>" + esc(g.name) + "</strong> (" + esc(g.track) + "): " + g.quests.map(function (q) { return (done[q.id] ? "✔ " : "○ ") + esc(q.title); }).join(", ") + "</li>";
      }).join("") + "</ul></details>";
      host.innerHTML = html;
    }
    AO.hooks.push(paint); paint();
  });
})();
