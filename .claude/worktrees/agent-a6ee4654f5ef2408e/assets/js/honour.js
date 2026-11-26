/* Bonus items (data-ao-honour): <div data-ao-honour="id" data-xp="15">Task text</div>. Bonus XP only; never gates anything. */
(function () {
  document.querySelectorAll("[data-ao-honour]").forEach(function (el) {
    var id = "honour-" + el.getAttribute("data-ao-honour"), xp = +el.getAttribute("data-xp") || 10;
    var label = document.createElement("label"), cb = document.createElement("input"), note = document.createElement("span");
    cb.type = "checkbox"; cb.checked = !!AO.state.passed[id];
    note.className = "ao-honour-note"; note.textContent = cb.checked ? " (+" + xp + " XP earned)" : " (+" + xp + " XP)";
    cb.onchange = function () {
      if (cb.checked) { AO.pass(id, xp); note.textContent = " (+" + xp + " XP earned)"; }
      else { cb.checked = true; }          /* claimed once; no XP farming by toggling */
    };
    var body = document.createElement("span"); body.innerHTML = el.innerHTML;
    var tag = document.createElement("strong"); tag.textContent = "Bonus question: "; body.insertBefore(tag, body.firstChild);
    label.appendChild(cb); label.appendChild(document.createTextNode(" ")); label.appendChild(body); label.appendChild(note);
    el.innerHTML = ""; el.appendChild(label); el.classList.add("ao-honour");
  });
})();
