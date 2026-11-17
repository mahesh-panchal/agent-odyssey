/* Quest pages: a "Next steps" block before the Lore section, plus the ending screen and the sealed notice on the final boss page.
   All of it is advice. It fails silently when world.json cannot load. */
(function () {
  var FINALE = null, base = window.AO_BASE || "./";
  function esc(t) { var d = document.createElement("div"); d.textContent = t == null ? "" : t; return d.innerHTML; }
  function passed(id) { return !!(AO.state && AO.state.passed && AO.state.passed[id]); }
  function link(q) {
    var st = window.AO.path.status(q.id);
    return "<li><a href='" + base + q.page + "'>" + esc(q.title) + "</a> <span class='ao-soft'>(" + window.AO.path.stateLabel(st) + (q.optional ? ", side quest" : "") + ")</span></li>";
  }
  function list(title, qs) { return qs.length ? "<h3>" + title + "</h3><ul>" + qs.map(link).join("") + "</ul>" : ""; }

  function init(G) {
    var P = AO.path, quest = P.questByPage(location.pathname);
    FINALE = G.finale.id;
    var ending = document.querySelector("[data-ao-ending]");
    var onFinale = !!quest && quest.id === FINALE;
    var isFinale = onFinale || !!ending;
    if (!quest && !isFinale) return;
    var content = document.querySelector("main") || document.getElementById("quarto-document-content") || document.body;
    var block = document.createElement("nav");
    block.className = "ao-nextsteps"; block.setAttribute("aria-label", "Next steps");
    var lore = document.querySelector(".ao-lore");
    if (lore && lore.parentNode) lore.parentNode.insertBefore(block, lore); else content.appendChild(block);
    var notice = null;
    if (isFinale) {
      notice = document.createElement("aside"); notice.className = "ao-sealed"; notice.setAttribute("aria-label", "Seal status");
      var dlg = document.querySelector(".quest-dialog");
      if (dlg && dlg.parentNode) dlg.parentNode.insertBefore(notice, dlg.nextSibling); else content.insertBefore(notice, content.firstChild);
    }

    function paint() {
      var h = "<h2>Next steps</h2>";
      if (quest && !onFinale) {
        var s = P.nextSteps(quest.id);
        var seen = {}; s.unlocks.forEach(function (u) { seen[u.id] = true; });
        var rec = s.recommended.filter(function (r) { return !seen[r.id]; }).slice(0, 3);
        h += list("Unlocks", s.unlocks) + list("Recommended next", rec) + list("Optional side quests", s.optional);
        var last = G.trunk_order[G.trunk_order.length - 1] === quest.id;
        if (last) {
          var r = P.remainingForFinale(), n = r.branchesNeeded;
          h += "<p>You have reached the end of the trunk. The branches hang off it: pick the ones that match your work. " +
            (P.finaleUnlocked() ? "The Murk's Heart is open." : n ? "Finish " + n + " more branch" + (n === 1 ? "" : "es") + " to open the Murk's Heart." : "Finish the rest of the trunk to open the Murk's Heart.") + "</p>";
        }
      } else if (!passed(FINALE)) {
        h += "<p>This is the last stop. Everything else on the site stays open to revisit.</p>";
      } else {
        h += "<p>The Murk is cleared. Every quest stays open to revisit.</p>";
      }
      h += "<p><a href='" + base + "index.html'>Back to the map</a> · <a href='" + base + "start-here.html'>Start Here</a></p>";
      block.innerHTML = h;
      if (isFinale) { paintSeal(); paintEnding(); }
    }

    function paintSeal() {
      if (P.finaleUnlocked() || passed(FINALE)) { notice.hidden = true; notice.innerHTML = ""; return; }
      var r = P.remainingForFinale(), h = "<p><strong>The Murk's Heart is still sealed.</strong> The path suggests finishing these first. You can read on if you like.</p><ul>";
      r.trunk.forEach(function (q) { h += "<li>Trunk: <a href='" + base + q.page + "'>" + esc(q.title) + "</a></li>"; });
      if (r.branchesNeeded) h += "<li>Finish " + r.branchesNeeded + " more branch" + (r.branchesNeeded === 1 ? "" : "es") + ". See <a href='" + base + "start-here.html'>Start Here</a>.</li>";
      notice.innerHTML = h + "</ul>"; notice.hidden = false;
    }

    function paintEnding() {
      if (!ending) return;
      var on = passed(FINALE);
      ending.classList.toggle("ao-ending-on", on);
      ending.hidden = !on;
      var old = ending.querySelector(".ao-ending-extra"); if (old) old.remove();
      if (!on) return;
      var ids = Object.keys(G.quests), cleared = ids.filter(passed).length;
      var done = P.branches().filter(function (b) { return b.complete; }).map(function (b) { return esc(b.name); });
      var extra = document.createElement("div"); extra.className = "ao-ending-extra";
      extra.innerHTML = "<p>You cleared " + cleared + " of " + ids.length + " quests" + (done.length ? " and finished " + (done.length === 1 ? "the branch " : "the branches ") + done.join(", ") : "") + ".</p>" +
        "<p><a href='" + base + "start-here.html'>Back to Start Here</a></p>";
      ending.appendChild(extra);
    }

    paint();
    AO.hooks.push(paint);
  }

  function boot() {
    if (!window.AO || !AO.path) return;
    AO.path.load().then(function (G) { if (G) init(G); }).catch(function () {});
  }
  boot();
})();
