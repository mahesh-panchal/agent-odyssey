/* Quest log: a collapsible left panel that carries the story (data from zones.yml via world.json). */
(function () {
  fetch(window.AO_BASE + "assets/data/world.json").then(function (r) { return r.json(); }).then(function (w) {
    var gates = Object.keys(w.gates).map(function (k) { return w.gates[k]; });
    var aside = document.createElement("aside"); aside.id = "ao-log"; aside.setAttribute("aria-label", "Quest log");
    document.body.appendChild(aside);
    var wide = window.matchMedia("(min-width: 1180px)");
    function esc(t) { var d = document.createElement("div"); d.textContent = t; return d.innerHTML; }
    function link(q) { return "<a href='" + window.AO_BASE + q.page + "'>" + esc(q.title) + "</a>"; }

    function paint() {
      var done = AO.state.passed, here = location.pathname, cur = null, chron = [];
      var onPage = null;
      gates.forEach(function (g) { (g.quests || []).forEach(function (q) {
        if (done[q.id]) chron.push(q.done); else { if (!cur) cur = { g: g, q: q }; if (location.pathname.endsWith(q.page)) onPage = { g: g, q: q }; }
      }); });
      // Off a quest page, "Now" follows the path's next quest; on a quest page it shows that page's quest.
      var nq = !onPage && AO.path && AO.path.nextQuest && AO.path.nextQuest();
      if (nq) gates.forEach(function (g) { (g.quests || []).forEach(function (q) { if (q.id === nq.id) cur = { g: g, q: q }; }); });
      cur = onPage || cur;
      var html = "<h2>Chronicle</h2>";
      html += cur ? "<div class='ao-now'><strong>Now:</strong> " + esc(cur.g.name) + " — " + link(cur.q) + "<p>" + esc(cur.q.story || "") + "</p></div>"
                  : "<div class='ao-now'><strong>Now:</strong> every open quest is cleared. More zones open in later versions.</div>";
      gates.forEach(function (g) {
        var qs = g.quests || [], open = cur && cur.g === g;
        html += "<details" + (open ? " open" : "") + "><summary>" + esc(g.name) + (g.status !== "open" && !(g.id === "murk" && AO.path && AO.path.finaleUnlocked && AO.path.finaleUnlocked()) ? " 🔒" : (function () { var req = qs.filter(function (q) { var n = AO.path && AO.path.quest(q.id); return !(n && n.optional); }); return req.length && req.every(function (q) { return done[q.id]; }); })() ? " ✔" : (function () { var n = qs.filter(function (q) { return done[q.id]; }).length; return n ? " (" + n + "/" + qs.length + " cleared)" : ""; })()) + "</summary>";
        if (!qs.length) html += "<p class='ao-soft'>" + esc(g.blurb || "") + "</p>";
        qs.forEach(function (q) {
          var st = done[q.id] ? "✔" : (cur && cur.q === q ? "➜" : "○");
          html += "<p>" + st + " " + link(q) + "</p>";
        });
        html += "</details>";
      });
      html += "<details><summary>Story so far</summary><p>" + esc(w.prologue) + "</p>" +
              chron.map(function (t) { return "<p>" + esc(t) + "</p>"; }).join("") + "</details>";
      aside.innerHTML = html;
    }
    function apply(open) {
      aside.hidden = !open;
      document.body.classList.toggle("ao-log-open", open && wide.matches);
      var b = document.getElementById("ao-logbtn");
      if (b) { b.setAttribute("aria-expanded", String(open)); b.textContent = "Quest Log " + (open ? "▴" : "▾"); }
    }
    function isOpen() { var p = AO.state.prefs; return p.log === undefined ? wide.matches : p.log; }
    function bind() {
      var b = document.getElementById("ao-logbtn"); if (!b) return;
      b.onclick = function () { AO.state.prefs.log = !isOpen(); AO.save(); };
      apply(isOpen());
    }
    AO.hooks.push(function () { paint(); bind(); });
    paint(); bind();
    if (window.AO && AO.path && AO.path.load) AO.path.load().then(function () { paint(); bind(); });
  });
})();
