/* Character sheet: skill tree (a phylogeny of quests), armour plates, level. Renders into #ao-character if present. */
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
        "</p><p class='ao-soft'>Rank rises with quests cleared. Collaboration and teaching quests (Biodiversity Reef) are where the sceptics' hardest worries are answered.</p>";

      /* Armour */
      var arm = byTrack("Armour"), plates = [];
      if (arm && arm.quests) arm.quests.forEach(function (q) { plates.push([q.title, !!done[q.id], q.done]); });
      html += "<h2>Armour</h2><div class='ao-armour'>" + (plates.length ? plates.map(function (p) {
        return "<div class='" + (p[1] ? "on" : "") + "'><strong>" + (p[1] ? "✔ " : "○ ") + esc(p[0]) + "</strong><br>" + (p[1] ? esc(p[2]) : "not yet forged") + "</div>";
      }).join("") : "<p>No armour quests yet.</p>") + "</div>";

      /* Skill tree: one clade per zone, one leaf per quest. Text-first: list below the picture. */
      var tracks = gates.filter(function (g) { return g.quests && g.quests.length; });
      var W = 640, rowH = 34, H = tracks.reduce(function (n, g) { return n + g.quests.length; }, 0) * rowH + 30, y = 20, svg = "";
      var rootX = 24, rootY = H / 2;
      tracks.forEach(function (g) {
        var ys = g.quests.map(function (_, i) { return y + i * rowH; }), midY = (ys[0] + ys[ys.length - 1]) / 2, cx = 200;
        var lit = g.quests.some(function (q) { return done[q.id]; });
        svg += "<path d='M" + rootX + " " + rootY + " C 110 " + rootY + " 110 " + midY + " " + cx + " " + midY + "' stroke='" + (lit ? "#e8b84a" : "#6b5f86") + "' fill='none' stroke-width='2'/>";
        svg += "<text x='" + (cx - 6) + "' y='" + (midY - 10) + "' text-anchor='end'>" + esc(g.name) + "</text>";
        g.quests.forEach(function (q, i) {
          var on = !!done[q.id];
          svg += "<path d='M" + cx + " " + midY + " H 230 V " + ys[i] + " H 260' stroke='" + (on ? "#e8b84a" : "#6b5f86") + "' fill='none' stroke-width='2'/>" +
            "<g class='" + (on ? "on" : "") + "'><circle cx='268' cy='" + ys[i] + "' r='7'/><text x='284' y='" + (ys[i] + 4) + "'>" + (on ? "✔ " : "") + esc(q.title) + "</text></g>";
        });
        y += g.quests.length * rowH;
      });
      svg = "<circle cx='" + rootX + "' cy='" + rootY + "' r='8' fill='#e8b84a'/>" + svg;
      html += "<h2>Skill tree</h2><svg class='ao-tree' viewBox='0 0 " + W + " " + H + "' role='img' aria-label='Skill tree: " + cleared + " quests cleared'>" + svg + "</svg>";
      html += "<details class='ao-textlist'><summary>Skill tree as text</summary><ul>" + tracks.map(function (g) {
        return "<li><strong>" + esc(g.name) + "</strong> (" + esc(g.track) + "): " + g.quests.map(function (q) { return (done[q.id] ? "✔ " : "○ ") + esc(q.title); }).join(", ") + "</li>";
      }).join("") + "</ul></details>";
      host.innerHTML = html;
    }
    AO.hooks.push(paint); paint();
  });
})();
