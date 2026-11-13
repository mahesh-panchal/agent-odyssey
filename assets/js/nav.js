/* Quest pages: ← → move between quests (order from world.json); M or Esc returns to the map. */
(function () {
  if (document.getElementById("ao-world")) return;                      // the map handles its own keys
  fetch(window.AO_BASE + "assets/data/world.json").then(function (r) { return r.json(); }).then(function (w) {
    var list = [];
    Object.keys(w.gates).forEach(function (k) { (w.gates[k].quests || []).forEach(function (q) { list.push(q); }); });
    var here = list.findIndex(function (q) { return location.pathname.endsWith(q.page); });
    var prev = here > 0 ? list[here - 1] : null, next = here >= 0 ? list[here + 1] : null;
    var bar = document.createElement("nav"); bar.className = "ao-pager"; bar.setAttribute("aria-label", "Quest navigation");
    function link(q, label, rel) { return q ? "<a rel='" + rel + "' href='" + window.AO_BASE + q.page + "'>" + label + " " + q.title + "</a>" : ""; }
    bar.innerHTML = link(prev, "←", "prev") + "<a href='" + window.AO_BASE + "index.html'>Back to map (M)</a>" + link(next, "→", "next");
    document.body.appendChild(bar);
    document.addEventListener("keydown", function (e) {
      if (e.altKey || e.ctrlKey || e.metaKey || e.shiftKey) return;
      if (e.target.closest && e.target.closest("input,textarea,select,button,[data-game-widget],[contenteditable]")) return;
      if (e.key === "Escape" || e.key.toLowerCase() === "m") { e.preventDefault(); location.href = window.AO_BASE + "index.html"; return; }
      var a = e.key === "ArrowRight" ? bar.querySelector("[rel=next]") : e.key === "ArrowLeft" ? bar.querySelector("[rel=prev]") : null;
      if (a) { e.preventDefault(); location.href = a.href; }
    });
  });
})();
