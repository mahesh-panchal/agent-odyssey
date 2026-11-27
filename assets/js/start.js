/* Background: a short path (where you are, the next few steps), the branches, and the whole course as a vertical list.
   Everything is built from the path graph in world.json, so it works without any picture. */
(function () {
  var host = document.getElementById("ao-start-path");
  if (!host) return;
  var base = window.AO_BASE || "./";
  var AHEAD = 3;   // steps shown after the current one
  function esc(t) { var d = document.createElement("div"); d.textContent = t == null ? "" : t; return d.innerHTML; }
  function P() { return window.AO && window.AO.path; }
  function passed(id) { return !!(AO.state && AO.state.passed && AO.state.passed[id]); }
  function plural(n, one, many) { return n + " " + (n === 1 ? one : many); }
  // Assign only when the text changed, so live regions do not re-announce and a focused link keeps focus.
  function setHTML(el, html) { if (el && el.__h !== html) { el.innerHTML = html; el.__h = html; } }

  function step(q, cls, tag) {
    var mark = passed(q.id) ? "<span class='ao-mark'>✔</span> " : "";
    return "<li class='" + cls + (passed(q.id) ? " st-cleared" : "") + "'>" + mark + "<a href='" + base + q.page + "'>" + esc(q.title) + "</a>" +
      (tag ? " <span class='ao-tag'>" + tag + "</span>" : "") + (q.optional ? " <span class='ao-tag'>side quest</span>" : "") + "</li>";
  }

  function paintPath(next) {
    var p = P(), trunk = p.trunkQuests(), left = trunk.filter(function (q) { return !passed(q.id); }), html = "";
    var done = trunk.length - left.length;
    if (left.length) {
      var at = Math.max(0, left.map(function (q) { return q.id; }).indexOf(next && next.id)), cur = left[at];
      var shown = left.slice(at, at + 1 + AHEAD), more = left.length - at - shown.length;
      html += "<h3>The trunk: " + done + " of " + trunk.length + " done</h3><ol class='ao-steps'>";
      shown.forEach(function (q, i) { html += step(q, i === 0 ? "now" : "", i === 0 ? "you are here" : ""); });
      if (more > 0) html += "<li class='more'>" + plural(more, "more step", "more steps") + " on the trunk</li>";
      html += "<li class='more'>Then choose your branches below</li></ol>";
      var side = p.nextSteps(cur.id).optional.slice(0, 3);
      if (side.length) {
        html += "<h3>Side quests you can take on the way</h3><ul class='ao-steps ao-side'>" + side.map(function (q) { return step(q, "", ""); }).join("") + "</ul>";
      }
    } else {
      html += "<h3>The trunk is done</h3><p>Choose the branches that match your work.</p>";
    }
    setHTML(host, html);
  }

  function fillCounts() {
    var p = P(), rule = p.finaleRule(), vals = { trunk: p.trunkQuests().length, branches: p.branches().length, any: rule && rule.any };
    [].forEach.call(document.querySelectorAll("[data-ao-n]"), function (el) {
      var v = vals[el.getAttribute("data-ao-n")]; if (v != null) el.textContent = v;
    });
  }

  function paintSide() {
    var p = P(), next = p.nextQuest(), fq = p.finale(), fid = fq && fq.id;
    setHTML(document.getElementById("ao-start-next"), next
      ? "<a class='ao-start-btn' href='" + base + next.page + "'>" + (Object.keys(AO.state.passed || {}).length ? "Next step: " : "Begin: ") + esc(next.title) + " ▶</a>"
      : passed(fid) ? "<span>The Murk is cleared. Revisit any quest below.</span>"
                    : "<span>Every quest in reach is cleared. Pick a branch below to go on.</span>");

    var link = fq ? "<a href='" + base + fq.page + "'>" + esc(fq.title.replace(/^Boss:\s*/, "")) + "</a>" : "the final boss";
    var r = p.remainingForFinale(), fin;
    if (passed(fid)) fin = "<strong>The Murk's Heart is cleared.</strong> " + link + " holds the ending.";
    else if (p.finaleUnlocked()) fin = "<strong>The Murk's Heart is open.</strong> " + link + " is the last stop.";
    else {
      var bits = [];
      if (r.trunk.length) bits.push("the trunk (" + plural(r.trunk.length, "quest", "quests") + " left)");
      if (r.branchesNeeded) bits.push(plural(r.branchesNeeded, "more branch", "more branches"));
      fin = "<strong>The Murk's Heart is sealed.</strong> It opens when you finish " + bits.join(" and ") + ".";
    }
    setHTML(document.getElementById("ao-start-finale"), fin);

    setHTML(document.getElementById("ao-start-branches"), p.branches().map(function (b) {
      var first = p.laneQuests(b.id).filter(function (q) { return !passed(q.id) && !q.optional; })[0] || p.laneQuests(b.id)[0];
      return "<li><a href='" + base + (first ? first.page : "index.html") + "'><strong>" + esc(b.name) + "</strong></a> <span class='ao-prog'>" + b.done + " of " + b.total + (b.complete ? " done" : "") + "</span>" +
        "<br>" + esc(b.blurb) + (b.who ? " <span class='ao-soft'>For: " + esc(b.who) + "</span>" : "") + "</li>";
    }).join(""));
    paintPath(next);
    buildList();
  }

  // The whole course, trunk then branches, one vertical list.
  function buildList() {
    var el = document.getElementById("ao-start-list"); if (!el) return;
    var p = P();
    function items(qs) { return "<ol class='ao-steps'>" + qs.map(function (q) { return step(q, "", ""); }).join("") + "</ol>"; }
    var html = "<h3>The trunk, in order</h3>" + items(p.trunkQuests());
    p.branches().forEach(function (b) { html += "<h3>Branch: " + esc(b.name) + "</h3>" + items(p.laneQuests(b.id)); });
    var f = p.finale();
    if (f) html += "<h3>Final boss</h3>" + items([f]);
    setHTML(el, html);
  }

  function fallback() {
    var el = document.getElementById("ao-start-next");
    if (el) el.innerHTML = "<a class='ao-start-btn' href='" + base + "index.html'>Open the map</a> <span>and begin with Name the Fears.</span>";
    var l = document.getElementById("ao-start-list");
    if (l) l.innerHTML = "<p>The path data did not load. Open <a href='" + base + "index.html'>the map</a> and begin with Name the Fears.</p>";
  }

  if (!P()) { fallback(); return; }
  P().load().then(function (G) {
    if (!G) { fallback(); return; }
    fillCounts(); paintSide();
    AO.hooks.push(paintSide);
  });
})();
