/* Quest pages: a small "Back to map" bar. Keys: M or Esc return to the map; the arrow keys follow the Continue block
   (left = back one step, right = next step on your path). */
(function () {
  if (document.getElementById("ao-world")) return;                      // the map handles its own keys
  var bar = document.createElement("nav"); bar.className = "ao-pager"; bar.setAttribute("aria-label", "Page navigation");
  bar.innerHTML = "<a href='" + window.AO_BASE + "index.html'>Back to map (M)</a>";
  document.body.appendChild(bar);
  document.addEventListener("keydown", function (e) {
    if (e.altKey || e.ctrlKey || e.metaKey || e.shiftKey) return;
    if (e.target.closest && e.target.closest("input,textarea,select,button,[data-game-widget],[contenteditable]")) return;
    if (e.key === "Escape" || e.key.toLowerCase() === "m") { e.preventDefault(); location.href = window.AO_BASE + "index.html"; return; }
    var a = e.key === "ArrowRight" ? document.querySelector(".ao-nextsteps [rel=next]") : e.key === "ArrowLeft" ? document.querySelector(".ao-nextsteps [rel=prev]") : null;
    if (a) { e.preventDefault(); location.href = a.href; }
  });
})();
