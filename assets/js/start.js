/* Start Here: draws status onto the generated quest network and fills the next-step button, branch progress, finale text and the text version of the map. */
(function () {
  var host = document.getElementById("ao-start-net");
  if (!host) return;
  var base = window.AO_BASE || "./";
  function esc(t) { var d = document.createElement("div"); d.textContent = t == null ? "" : t; return d.innerHTML; }
  function P() { return window.AO && window.AO.path; }
  function passed(id) { return !!(AO.state && AO.state.passed && AO.state.passed[id]); }
  function plural(n, one, many) { return n + " " + (n === 1 ? one : many); }
  // Assign only when the text changed, so live regions do not re-announce and a focused link in a list keeps focus.
  function setHTML(el, html) { if (el && el.__h !== html) { el.innerHTML = html; el.__h = html; } }

  var LABEL = { cleared: "✔ cleared", ready: "▶ ready", waiting: "○ later" };   // short, for the node boxes
  var svg = null;

  function paintNodes() {
    if (!svg) return;
    [].forEach.call(svg.querySelectorAll("a.node"), function (a) {
      var st = P().status(a.getAttribute("data-id")), side = a.classList.contains("optional");
      a.setAttribute("class", a.getAttribute("class").replace(/\bst-\w+/g, "").trim() + " st-" + st);
      a.querySelector(".st").textContent = LABEL[st] + (side ? " · side" : "");
      a.setAttribute("aria-label", a.getAttribute("data-title") + ", " + P().stateLabel(st) + (side ? ", side quest" : ""));
    });
    [].forEach.call(svg.querySelectorAll(".bprog"), function (t) {
      var b = P().branches().filter(function (x) { return x.id === t.getAttribute("data-branch"); })[0];
      if (b) t.textContent = "· " + b.done + "/" + b.total + (b.complete ? " complete" : "");
    });
  }

  // "You are here": a gold ring round the next node and a small tab on its top border (clear of the lane labels).
  function paintHere(next) {
    if (!svg) return;
    var old = svg.querySelector(".here"); if (old) old.remove();
    if (!next) return;
    var a = svg.querySelector('a.node[data-id="' + next.id + '"]'); if (!a) return;
    var x = +a.getAttribute("data-x"), top = +a.getAttribute("data-y") - 36;
    var g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    g.setAttribute("class", "here"); g.setAttribute("aria-hidden", "true"); g.setAttribute("data-x", x);
    g.innerHTML = '<rect class="ring" x="' + (x - 75) + '" y="' + (top - 7) + '" width="150" height="86" rx="12"/>' +
      '<rect class="tab" x="' + (x - 46) + '" y="' + (top - 11) + '" width="92" height="17" rx="4"/>' +
      '<text x="' + x + '" y="' + (top + 2) + '" text-anchor="middle">You are here</text>';
    svg.appendChild(g);
  }

  // ---- Overview: one box per stage (trunk, each branch, final boss). Both layouts are inlined; CSS shows one. ----
  var ovSvgs = [];
  function target(qs) {   // first quest in a stage that is not cleared, else its first quest
    return qs.filter(function (q) { return !passed(q.id); })[0] || qs[0];
  }
  function ovState(kind, id) {
    var p = P(), done, total, label, cls, word;
    if (kind === "finale") {
      var f = p.finale(), fid = f && f.id;
      if (passed(fid)) return { cls: "st-complete", text: "✔ cleared", word: "cleared", page: f.page };
      var open = p.finaleUnlocked();
      return { cls: open ? "st-progress" : "st-none", text: open ? "▶ open" : "○ sealed", word: open ? "open" : "sealed", page: f && f.page };
    }
    var qs, name;
    if (kind === "trunk") { qs = p.trunkQuests(); name = "Trunk"; }
    else {
      var b = p.branches().filter(function (x) { return x.id === id; })[0] || {};
      qs = p.laneQuests(id).filter(function (q) { return !q.optional; }); name = b.name;
    }
    done = qs.filter(function (q) { return passed(q.id); }).length; total = qs.length;
    if (total && done === total) { cls = "st-complete"; label = "✔ complete"; word = "complete"; }
    else if (done) { cls = "st-progress"; label = "▶ in progress"; word = "in progress"; }
    else { cls = "st-none"; label = "○ not started"; word = "not started"; }
    var t = target(qs);
    return { cls: cls, text: label + " · " + done + "/" + total, word: word, done: done, total: total, name: name, page: t && t.page };
  }
  function paintOverview(next) {
    ovSvgs.forEach(function (svg) {
      [].forEach.call(svg.querySelectorAll("a.ovbox"), function (a) {
        var kind = a.getAttribute("data-kind"), id = a.getAttribute("data-id"), s = ovState(kind, id);
        a.setAttribute("class", "ovbox " + kind + " " + s.cls);
        var st = a.querySelector(".ovs"); if (st) st.textContent = s.text;
        var title = (a.querySelector("title") || {}).textContent || "";
        var base0 = title.replace(/,.*$/, "");
        a.setAttribute("aria-label", base0 + (s.total != null ? ", " + s.done + " of " + s.total + " quests" : "") + ", " + s.word);
        if (s.page) a.setAttribute("href", base + s.page);
      });
      var old = svg_here(svg); if (old) old.remove();
      if (!next) return;
      var fid = P().finale() && P().finale().id;
      var kind = next.id === fid ? "finale" : next.trunk ? "trunk" : "branch";
      var sel = kind === "branch" ? 'a.ovbox.branch[data-id="' + next.branch + '"]' : "a.ovbox." + kind;
      var a = svg.querySelector(sel); if (!a) return;
      var r = a.querySelector(".box"), x = +r.getAttribute("x"), y = +r.getAttribute("y"), w = +r.getAttribute("width"), h = +r.getAttribute("height");
      var g = document.createElementNS("http://www.w3.org/2000/svg", "g");
      g.setAttribute("class", "ovhere"); g.setAttribute("aria-hidden", "true");
      g.innerHTML = '<rect class="ring" x="' + (x - 6) + '" y="' + (y - 6) + '" width="' + (w + 12) + '" height="' + (h + 12) + '" rx="13"/>' +
        '<rect class="tab" x="' + (x + w / 2 - 50) + '" y="' + (y - 20) + '" width="100" height="18" rx="4"/>' +
        '<text x="' + (x + w / 2) + '" y="' + (y - 7) + '" text-anchor="middle">You are here</text>';
      svg.insertBefore(g, a);   // behind the box so the link stays on top
    });
  }
  function svg_here(svg) { return svg.querySelector(".ovhere"); }

  function fillCounts() {
    var p = P(), rule = p.finaleRule(), vals = { trunk: p.trunkQuests().length, branches: p.branches().length, any: rule && rule.any };
    [].forEach.call(document.querySelectorAll("[data-ao-n]"), function (el) {
      var v = vals[el.getAttribute("data-ao-n")]; if (v != null) el.textContent = v;
    });
  }

  function paintSide() {
    var p = P(), next = p.nextQuest(), fq = p.finale(), fid = fq && fq.id;
    var n = Object.keys(AO.state.passed || {}).length;
    setHTML(document.getElementById("ao-start-next"), next
      ? "<a class='ao-start-btn' href='" + base + next.page + "'>" + (n ? "Next step: " : "Begin: ") + esc(next.title) + " ▶</a>"
      : passed(fid) ? "<span>The Murk is cleared. Revisit any quest from the map below.</span>"
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
      return "<li><strong>" + esc(b.name) + "</strong> <span class='ao-prog'>" + b.done + " of " + b.total + (b.complete ? " done, complete" : " done") + "</span>" +
        "<br>" + esc(b.blurb) + (b.who ? " <em>For: " + esc(b.who) + "</em>" : "") + "</li>";
    }).join(""));
    paintHere(next);
    paintOverview(next);
    buildList();
  }

  // The text version comes straight from the graph, so it works without the picture.
  function buildList() {
    var el = document.getElementById("ao-start-list"); if (!el) return;
    var p = P();
    function items(qs) {
      return qs.map(function (q) {
        return "<li><a href='" + base + q.page + "'>" + esc(q.title) + "</a> <span class='ao-soft'>(" + p.stateLabel(p.status(q.id)) +
          (q.optional ? ", side quest" : "") + ")</span></li>";
      }).join("");
    }
    var html = "<h3>Trunk, in order</h3><ol>" + items(p.trunkQuests()) + "</ol>";
    p.branches().forEach(function (b) { html += "<h3>Branch: " + esc(b.name) + "</h3><ol>" + items(p.laneQuests(b.id)) + "</ol>"; });
    var f = p.finale();
    if (f) html += "<h3>Final boss</h3><ol>" + items([f]) + "</ol>";
    setHTML(el, html);
  }

  function fixLinks() {
    [].forEach.call(svg.querySelectorAll("a.node"), function (a) { a.setAttribute("href", base + a.getAttribute("href")); });
  }

  var first = true;
  function paint() {
    paintNodes(); paintSide();
    if (first) { first = false; scrollToHere(); }
  }
  function scrollToHere() {
    var h = svg && svg.querySelector(".here"); if (!h) return;
    host.scrollLeft = Math.max(0, +h.getAttribute("data-x") - host.clientWidth / 2);
  }

  if (!P()) { fallback(); return; }
  function fallback() {
    var el = document.getElementById("ao-start-next");
    if (el) el.innerHTML = "<a class='ao-start-btn' href='" + base + "index.html'>Open the map</a> <span>and begin with Name the Fears.</span>";
    var l = document.getElementById("ao-start-list");
    if (l) l.innerHTML = "<p>The path data did not load. Open <a href='" + base + "index.html'>the map</a> and begin with Name the Fears.</p>";
  }

  function grab(name) {
    return fetch(base + "assets/data/" + name).then(function (r) { return r.ok ? r.text() : ""; }).catch(function () { return ""; });
  }
  var detail = document.getElementById("ao-start-detail");
  if (detail) {   // closed by default; open on wide screens, and keep the "you are here" node in view when it opens
    if (window.matchMedia && window.matchMedia("(min-width: 900px)").matches) detail.open = true;
    detail.addEventListener("toggle", function () { if (detail.open) scrollToHere(); });
  }

  Promise.all([P().load(), grab("path-network.svg"), grab("path-overview.svg"), grab("path-overview-narrow.svg")]).then(function (res) {
    if (!res[0]) { fallback(); return; }
    if (res[1]) { host.innerHTML = res[1]; svg = host.querySelector("svg"); }
    else host.innerHTML = "<p>The map picture did not load. The text version below lists every quest.</p>";
    if (svg) fixLinks();
    var ov = document.getElementById("ao-start-overview");
    if (ov) {
      if (res[2] || res[3]) {
        ov.innerHTML = (res[2] ? "<div class='ao-ov-wide'>" + res[2] + "</div>" : "") + (res[3] ? "<div class='ao-ov-narrow'>" + res[3] + "</div>" : "");
        ovSvgs = [].slice.call(ov.querySelectorAll("svg"));
      } else ov.innerHTML = "<p>The overview picture did not load. The text version of the map below lists every quest.</p>";
    }
    fillCounts();
    paint();
    AO.hooks.push(function () { paintNodes(); paintSide(); });
  });
})();
