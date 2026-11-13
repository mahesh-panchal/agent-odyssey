/* Player state: localStorage, namespaced + versioned; export/import as a save code. */
(function () {
  var KEY = "agent-odyssey:v1:state", VERSION = 1;
  var defaults = { v: VERSION, passed: {}, xp: 0, prefs: { companion: "claude-code", language: "bash" } };
  function safe(fn, fb) { try { return fn(); } catch (e) { return fb; } }
  function load() {
    var s = safe(function () { return JSON.parse(localStorage.getItem(KEY)); }, null);
    return Object.assign({}, defaults, s || {});
  }
  var AO = window.AO = {
    hooks: [],
    state: load(),
    save: function () { safe(function () { localStorage.setItem(KEY, JSON.stringify(AO.state)); }); AO.render(); },
    pass: function (id, xp) {
      if (!AO.state.passed[id]) { AO.state.passed[id] = true; AO.state.xp += xp || 0; }
      AO.save();
    },
    exportCode: function () { return btoa(JSON.stringify(AO.state)); },
    importCode: function (code) {
      var s = JSON.parse(atob(code.trim()));
      if (!s || typeof s.v !== "number" || s.v > VERSION) throw new Error("Unsupported save");
      AO.state = Object.assign({}, defaults, s); AO.save();
    },
    render: function () {
      var h = document.getElementById("ao-hud");
      if (!h) { h = document.createElement("header"); h.id = "ao-hud"; (document.getElementById("quarto-document-content") || document.body).prepend(h); }
      var n = Object.keys(AO.state.passed).length;
      h.innerHTML = "<button id='ao-logbtn' aria-expanded='false' aria-controls='ao-log'>Quest Log ▾</button> <a href='" + (window.AO_BASE || "./") + "index.html'>Map</a> <a href='" + (window.AO_BASE || "./") + "character.html'>Character</a> <span style='white-space:nowrap'>XP " + AO.state.xp + " · Quests cleared " + n + "</span> " +
        "<button id='ao-exp'>Save code</button> <button id='ao-imp'>Load code</button>";
      (AO.hooks || []).forEach(function (f) { f(); });
      document.getElementById("ao-exp").onclick = function () { prompt("Copy your save code:", AO.exportCode()); };
      document.getElementById("ao-imp").onclick = function () {
        var c = prompt("Paste a save code:"); if (!c) return;
        try { AO.importCode(c); } catch (e) { alert("That code did not work: " + e.message); }
      };
    }
  };
  AO.render();
})();
