/* Minimap of one location (a gate in zones.yml): its quests as nodes, `after` edges solid, `suggested` edges dashed.
   AO.minimap.render(gateKey, el, { current: questId })  draws into el.
   AO.minimap.progress()                                  adds "n of m cleared" to the home page zone list.
   Advice only: every node is a plain link, nothing is locked. Needs world.json; fails silently without it. */
(function () {
  var AO = window.AO = window.AO || {};
  var W = null, loading = null;
  var COLW = 210, ROWH = 46, PAD = 18, R = 10, RO = 6;

  function esc(t) { var d = document.createElement("div"); d.textContent = t == null ? "" : t; return d.innerHTML; }
  function passed(id) { return !!(AO.state && AO.state.passed && AO.state.passed[id]); }
  function load() {
    if (!loading) loading = fetch(window.AO_BASE + "assets/data/world.json").then(function (r) { return r.json(); })
      .then(function (w) { W = w; return w; }).catch(function () { loading = null; return null; });
    return loading;
  }
  function inGate(G, gate) { return Object.keys(G.quests).filter(function (k) { return G.quests[k].gate === gate; }); }
  function status(id) { return AO.path ? AO.path.status(id) : (passed(id) ? "cleared" : "waiting"); }

  function wrap(t) {                                  // up to two lines of about 24 characters
    if (t.length <= 24) return [t];
    var i = t.lastIndexOf(" ", 24); if (i < 8) i = 24;
    var a = t.slice(0, i).trim(), b = t.slice(i).trim();
    return [a, b.length > 25 ? b.slice(0, 23) + "…" : b];
  }

  function layout(G, ids) {
    var depth = {};
    function d(k) {
      if (depth[k] != null) return depth[k];
      depth[k] = 0;
      var ps = G.quests[k].after.filter(function (p) { return ids.indexOf(p) >= 0; });
      depth[k] = ps.length ? 1 + Math.max.apply(null, ps.map(d)) : 0;
      return depth[k];
    }
    ids.forEach(d);
    var count = {}, pos = {}, cols = 1, rows = 1;
    ids.forEach(function (k) { var c = count[depth[k]] = (count[depth[k]] || 0); count[depth[k]]++; pos[k] = { col: c, row: depth[k] }; cols = Math.max(cols, c + 1); rows = Math.max(rows, depth[k] + 1); });
    ids.forEach(function (k) { pos[k].x = PAD + R + pos[k].col * COLW; pos[k].y = PAD + R + 10 + pos[k].row * ROWH; });
    return { pos: pos, w: PAD * 2 + cols * COLW, h: PAD * 2 + 20 + rows * ROWH };
  }

  function draw(w, gateKey, opts) {
    var G = w.graph, gate = w.gates[gateKey], ids = inGate(G, gateKey);
    if (!G || !gate || !ids.length) return "";
    var L = layout(G, ids), cleared = ids.filter(passed).length;
    var focus = ids.filter(function (k) { return !passed(k) && status(k) === "ready" && !G.quests[k].optional && k !== opts.current; })[0] ||
      ids.filter(function (k) { return !passed(k) && status(k) === "ready" && k !== opts.current; })[0] || null;
    var svg = "", edges = "", nodes = "";
    ids.forEach(function (k) {
      var q = G.quests[k], c = L.pos[k];
      q.after.concat(q.suggested).forEach(function (p) {
        if (ids.indexOf(p) < 0) return;
        var a = L.pos[p], dashed = q.after.indexOf(p) < 0, r = G.quests[p].optional ? RO : R, r2 = q.optional ? RO : R, m = (a.y + c.y) / 2;
        edges += "<path d='M" + a.x + " " + (a.y + r) + " C" + a.x + " " + m + " " + c.x + " " + m + " " + c.x + " " + (c.y - r2) + "' class='ao-mm-edge" + (dashed ? " ao-mm-soft" : "") + "'/>";
      });
    });
    ids.forEach(function (k) {
      var q = G.quests[k], c = L.pos[k], st = status(k), isNext = k === focus, here = k === opts.current, r = q.optional ? RO : R;
      var cls = "ao-mm-node ao-mm-" + (st === "cleared" ? "cleared" : st === "ready" ? "ready" : "waiting") + (isNext ? " ao-mm-next" : "") + (q.optional ? " ao-mm-opt" : "") + (here ? " ao-mm-here" : "");
      var words = (st === "cleared" ? "cleared" : st === "ready" ? "ready" : "not ready yet") + (isNext ? ", next" : "") + (q.trunk ? ", trunk quest" : ", side quest") + (q.optional ? ", optional" : "") + (here ? ", this page" : "");
      var tag = isNext ? "NEXT" : here ? "HERE" : "";
      var t = wrap((q.trunk ? "◆ " : "◇ ") + q.title), ty = c.y + (t.length === 2 ? -2 : 4);
      var label = t.map(function (ln, i) { return "<tspan x='" + (c.x + r + 8) + "' dy='" + (i ? 15 : 0) + "'>" + esc(ln) + "</tspan>"; }).join("");
      nodes += "<a href='" + window.AO_BASE + q.page + "'" + (here ? " aria-current='page'" : "") + " aria-label='" + esc(q.title + ": " + words) + "' class='" + cls + "'>" +
        "<title>" + esc(q.title + " (" + words + ")") + "</title>" +
        (isNext ? "<circle cx='" + c.x + "' cy='" + c.y + "' r='" + (r + 5) + "' class='ao-mm-ring'/>" : "") +
        "<circle cx='" + c.x + "' cy='" + c.y + "' r='" + r + "' class='ao-mm-dot'/>" +
        (st === "cleared" ? "<path d='M" + (c.x - r * .45) + " " + c.y + " l" + (r * .3) + " " + (r * .35) + " l" + (r * .6) + " " + (-r * .75) + "' class='ao-mm-tick'/>" : "") +
        "<text x='" + (c.x + r + 8) + "' y='" + ty + "' class='ao-mm-label'>" + label + "</text>" +
        (tag ? "<text x='" + (c.x - r - 4) + "' y='" + (c.y - r - 4) + "' class='ao-mm-tag'>" + tag + "</text>" : "") + "</a>";
    });
    svg = "<svg viewBox='0 0 " + L.w + " " + L.h + "' width='" + L.w + "' height='" + L.h + "' role='group' aria-labelledby='ao-mm-t-" + gateKey + " ao-mm-d-" + gateKey + "' class='ao-mm-svg'>" +
      "<title id='ao-mm-t-" + gateKey + "'>Map of " + esc(gate.name) + "</title>" +
      "<desc id='ao-mm-d-" + gateKey + "'>" + cleared + " of " + ids.length + " quests cleared. Each quest is a link. Lines join a quest to the quest it follows; dashed lines are suggestions.</desc>" +
      edges + nodes + "</svg>";
    return "<div class='ao-mm-scroll'>" + svg + "</div>" +
      "<p class='ao-mm-key'><span aria-hidden='true'>✔</span> cleared · <span aria-hidden='true'>◎</span> NEXT · ○ not ready yet · ◆ trunk quest · ◇ side quest · small dot = optional · dashed line = suggested order</p>";
  }

  function render(gateKey, el, opts) {
    opts = opts || {};
    if (!el) return Promise.resolve();
    return load().then(function (w) { if (w) el.innerHTML = draw(w, gateKey, opts); });
  }

  // Home page: add "n of m cleared" to each zone link in the text-only zone list.
  function progress() {
    var host = document.getElementById("ao-world") && document.querySelector(".ao-textlist");
    if (!host) return Promise.resolve();
    return load().then(function (w) {
      if (!w || !w.graph) return;
      var G = w.graph;
      host.querySelectorAll("li > a[href*='zones/']").forEach(function (a) {
        if (/\(continued\)/.test(a.textContent)) return;
        var href = (a.getAttribute("href") || "").replace(/\.(qmd|html)$/, "");
        var hit = Object.keys(G.quests).filter(function (k) { var pg = G.quests[k].page.replace(/\.html$/, ""); return href === pg || href.slice(-pg.length) === pg; })[0];
        if (!hit) return;
        var ids = inGate(G, G.quests[hit].gate), n = ids.filter(passed).length;
        var old = a.parentNode.querySelector(".ao-zone-progress"); if (old) old.remove();
        var s = document.createElement("span"); s.className = "ao-zone-progress";
        s.textContent = " — " + n + " of " + ids.length + " cleared" + (n === ids.length ? " ✔" : "");
        a.parentNode.insertBefore(s, a.nextSibling);
      });
    });
  }

  AO.minimap = { render: render, progress: progress };
  if (document.getElementById("ao-world")) { progress(); if (AO.hooks) AO.hooks.push(progress); }
})();
