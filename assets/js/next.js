/* Quest pages: a "Next steps" block before the Lore section, plus the ending screen and the sealed notice on the final boss page.
   All of it is advice. It fails silently when world.json cannot load. */
(function () {
  var FINALE = null, base = window.AO_BASE || "./";
  function esc(t) { var d = document.createElement("div"); d.textContent = t == null ? "" : t; return d.innerHTML; }
  function passed(id) { return !!(AO.state && AO.state.passed && AO.state.passed[id]); }
  function link(q) {
    return "<li>" + (passed(q.id) ? "<span class='ao-mark'>✔</span> " : "") + "<a href='" + base + q.page + "'>" + esc(q.title) + "</a></li>";
  }
  function here(G, P, quest) {   // this location's quests: finished ones folded away, the next open one highlighted
    var ids = Object.keys(G.quests).filter(function (k) { return G.quests[k].gate === G.quests[quest.id].gate; });
    if (ids.length < 2) return "";
    var done = ids.filter(passed), left = ids.filter(function (k) { return !passed(k); });
    var focus = left.filter(function (k) { return k !== quest.id && P.status(k) === "ready"; })[0];
    var item = function (k) { var q = P.quest(k) || G.quests[k]; return "<li" + (k === focus ? " class='ao-here-next'" : "") + ">" + (k === focus ? "<strong>➜ " : "") + "<a href='" + base + q.page + "'" + (k === quest.id ? " aria-current='page'" : "") + ">" + esc(q.title) + "</a>" + (k === focus ? "</strong>" : "") + (k === quest.id ? " (this page)" : "") + "</li>"; };
    var h = "<h3>In this location (" + done.length + " of " + ids.length + " cleared)</h3>";
    h += "<div class='ao-minimap' data-gate='" + G.quests[quest.id].gate + "' data-current='" + quest.id + "'></div>";
    h += "<details class='ao-here-text'><summary>This location as a list</summary>";
    if (left.length) h += "<ul class='ao-here'>" + left.map(item).join("") + "</ul>";
    if (done.length) h += "<details class='ao-here-done'><summary>Cleared here (" + done.length + ")</summary><ul>" + done.map(function (k) { var q = P.quest(k) || G.quests[k]; return "<li><span class='ao-mark'>✔</span> <a href='" + base + q.page + "'>" + esc(q.title) + "</a></li>"; }).join("") + "</ul></details>";
    return h + "</details>";
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
    var lore = document.querySelector(".ao-related") || document.querySelector(".ao-lore");
    if (lore && lore.parentNode) lore.parentNode.insertBefore(block, lore); else content.appendChild(block);
    var notice = null;
    if (isFinale) {
      notice = document.createElement("aside"); notice.className = "ao-sealed"; notice.setAttribute("aria-label", "Seal status");
      var dlg = document.querySelector(".quest-dialog");
      if (dlg && dlg.parentNode) dlg.parentNode.insertBefore(notice, dlg.nextSibling); else content.insertBefore(notice, content.firstChild);
    }

    function paint() {
      var h = "<h2>Continue the journey</h2>";
      var battle = document.querySelector("[data-ao-test]");
      if (battle && !battle.id) battle.id = "ao-battle";
      if (quest && !onFinale && battle && !passed(quest.id)) {
        h += "<p class='ao-uncleared'>This quest is not cleared yet. <a href='#ao-battle'>Pass its Battle</a> to clear it. A location opens on the map when its quests are cleared.</p>";
      }
      if (quest && !onFinale) {
        var s = P.nextSteps(quest.id);
        var rec = s.recommended.filter(function (r) { return !passed(r.id); });
        var prev = P.prevQuest(quest.id), fol = P.followQuest(quest.id);
        var go = fol && !passed(fol.id) ? fol : rec[0], others = rec.filter(function (r) { return !go || r.id !== go.id; }).slice(0, 2);
        h += "<p class='ao-go'>" + (go ? "<a class='ao-start-btn' rel='next' href='" + base + go.page + "'>Next: " + esc(go.title) + " ▶</a>" : "<span>Every step in reach is cleared.</span>") +
          (prev ? " <a class='ao-back' rel='prev' href='" + base + prev.page + "'>◀ Back: " + esc(prev.title) + "</a>" : "") + "</p>";
        h += here(G, P, quest);
        h += list("Other ways on", others) + list("Side quests (optional)", s.optional);
        var last = G.trunk_order[G.trunk_order.length - 1] === quest.id;
        if (last) {
          var r = P.remainingForFinale(), n = r.branchesNeeded;
          h += "<p>You have reached the end of the trunk. Pick the branches that match your work. " +
            (P.finaleUnlocked() ? "The Murk's Heart is open." : n ? "Finish " + n + " more branch" + (n === 1 ? "" : "es") + " to open the Murk's Heart." : "Finish the rest of the trunk to open the Murk's Heart.") + "</p>";
        }
      } else if (!passed(FINALE)) {
        h += "<p>This is the last stop. Everything else stays open to revisit.</p>";
      } else {
        h += "<p>The Murk is cleared. Every quest stays open to revisit.</p>";
      }
      h += "<p class='ao-soft'><a href='" + base + "start-here.html'>Your path</a> · <a href='" + base + "index.html'>Map</a></p>";
      block.innerHTML = h;
      var mm = block.querySelector(".ao-minimap");
      if (mm && AO.minimap) AO.minimap.render(mm.getAttribute("data-gate"), mm, { current: mm.getAttribute("data-current") });
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
