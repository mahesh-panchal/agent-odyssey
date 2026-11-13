/* Test engine: choice, order, sort, faulty-line, match. Keyboard operable; wrong answers explain the misconception.
   A question counts only if right on the FIRST check; you may keep trying to see the explanation and move on. */
(function () {
  function h(tag, attrs, kids) {
    var e = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { if (k === "text") e.textContent = attrs[k]; else e.setAttribute(k, attrs[k]); });
    (kids || []).forEach(function (c) { e.appendChild(c); });
    return e;
  }
  function shuffle(a) { return a.map(function (x) { return [Math.random(), x]; }).sort(function (p, q) { return p[0] - q[0]; }).map(function (p) { return p[1]; }); }

  /* After a correct answer: say why the other choices are wrong (or why each item sits where it does). */
  function why(q) {
    var rows = [];
    if (q.type === "choice") q.options.forEach(function (o) { if (!o.correct) rows.push(["✖ " + o.text, o.misconception]); });
    else if (q.type === "sort") q.items.forEach(function (it) { rows.push([it.text + "  →  " + it.bin, it.misconception]); });
    else if (q.type === "match") q.pairs.forEach(function (p) { rows.push([p.left + "  →  " + p.right, p.misconception]); });
    else if (q.type === "faulty-line") q.lines.forEach(function (l) { if (!l.faulty) rows.push([l.text.trim(), l.why]); });
    else if (q.type === "order" && q.why) Object.keys(q.why).forEach(function (k) { rows.push([k, q.why[k]]); });
    rows = rows.filter(function (r) { return r[1]; });
    if (!rows.length) return null;
    var d = h("details", { class: "ao-why", open: "" }, [h("summary", { text: q.type === "choice" ? "Why the other answers are wrong" : "Why each one belongs where it does" })]);
    rows.forEach(function (r) { d.appendChild(h("p", {}, [h("strong", { text: r[0] + ": " }), h("span", { text: r[1] })])); });
    return d;
  }

  /* Each renderer: (q, box, report) where report(ok, message) is called on every check. */
  var R = {};
  R.choice = function (q, box, report) {
    shuffle(q.options).forEach(function (o, i) {
      var b = h("button", { text: String.fromCharCode(65 + i) + ")  " + o.text }); b.onclick = function () { report(!!o.correct, o.correct ? "" : o.misconception); }; box.appendChild(b);
    });
  };
  R.order = function (q, box, report) {
    var items = shuffle(q.items.slice()), list = h("ol", {});
    function paint() {
      list.innerHTML = "";
      items.forEach(function (t, i) {
        var li = h("li", {}, [h("span", { text: t + " " }),
          h("button", { text: "↑", "aria-label": "Move up: " + t }), h("button", { text: "↓", "aria-label": "Move down: " + t })]);
        var bs = li.querySelectorAll("button");
        bs[0].onclick = function () { if (i > 0) { items.splice(i - 1, 0, items.splice(i, 1)[0]); paint(); list.children[i - 1].querySelectorAll("button")[0].focus(); } };
        bs[1].onclick = function () { if (i < items.length - 1) { items.splice(i + 1, 0, items.splice(i, 1)[0]); paint(); list.children[i + 1].querySelectorAll("button")[1].focus(); } };
        list.appendChild(li);
      });
    }
    paint(); box.appendChild(list);
    var go = h("button", { text: "Check order" });
    go.onclick = function () {
      var bad = items.findIndex(function (t, i) { return t !== q.items[i]; });
      report(bad < 0, bad < 0 ? "" : ((q.why && q.why[items[bad]]) || ("Position " + (bad + 1) + " is not right: “" + items[bad] + "” does not belong there.")));
    };
    box.appendChild(go);
  };
  R.sort = function (q, box, report) {
    var rows = q.items.map(function (it) {
      var sel = h("select", { "aria-label": "Bin for: " + it.text }, [h("option", { value: "", text: "— choose —" })]
        .concat(q.bins.map(function (b) { return h("option", { value: b, text: b }); })));
      box.appendChild(h("p", {}, [h("span", { text: it.text + "  " }), sel])); return { it: it, sel: sel };
    });
    var go = h("button", { text: "Check sorting" });
    go.onclick = function () {
      var wrong = rows.filter(function (r) { return r.sel.value !== r.it.bin; });
      rows.forEach(function (r) { r.sel.style.outline = r.sel.value === r.it.bin ? "2px solid #7bd88f" : "2px solid #ff7a7a"; });
      report(!wrong.length, wrong.map(function (r) { return "✖ " + r.it.text + ": " + r.it.misconception; }).join("\n"));
    };
    box.appendChild(go);
  };
  R["faulty-line"] = function (q, box, report) {
    var pre = h("div", { class: "ao-code", role: "group", "aria-label": "Lines of output" });
    q.lines.forEach(function (l, i) {
      var b = h("button", { text: (i + 1) + "  " + l.text, class: "ao-line" });
      b.onclick = function () { report(!!l.faulty, l.faulty ? "" : (l.why || "That line is fine.")); }; pre.appendChild(b);
    });
    box.appendChild(pre);
  };
  R.match = function (q, box, report) {
    var rights = shuffle(q.pairs.map(function (p) { return p.right; }));
    var rows = q.pairs.map(function (p) {
      var sel = h("select", { "aria-label": "Match for: " + p.left }, [h("option", { value: "", text: "— choose —" })]
        .concat(rights.map(function (r) { return h("option", { value: r, text: r }); })));
      box.appendChild(h("p", {}, [h("span", { text: p.left + "  →  " }), sel])); return { p: p, sel: sel };
    });
    var go = h("button", { text: "Check matches" });
    go.onclick = function () {
      var wrong = rows.filter(function (r) { return r.sel.value !== r.p.right; });
      rows.forEach(function (r) { r.sel.style.outline = r.sel.value === r.p.right ? "2px solid #7bd88f" : "2px solid #ff7a7a"; });
      report(!wrong.length, wrong.map(function (r) { return "✖ " + r.p.left + ": " + (r.p.misconception || "that is not the match."); }).join("\n"));
    };
    box.appendChild(go);
  };

  document.querySelectorAll("[data-ao-test]").forEach(function (el) {
    var id = el.getAttribute("data-ao-test"), xp = +el.getAttribute("data-xp") || 50;
    el.setAttribute("data-game-widget", "");
    fetch(window.AO_BASE + "assets/data/" + id + ".json").then(function (r) { return r.json(); }).then(function (bank) {
      var qs = bank.questions, pass = bank.pass || 0.8;
      function run() {
        var score = 0, i = 0;
        function finish() {
          var ok = score / qs.length >= pass;
          el.innerHTML = "";
          el.appendChild(h("p", { role: "status", text: (ok ? "✔ Victory! The Blight recedes. " : "✖ The Blight holds. ") + score + "/" + qs.length + " right first time." + (ok ? "" : " Need " + Math.ceil(pass * qs.length) + ".") }));
          if (ok) AO.pass(id, xp); else { var b = h("button", { text: "Fight again" }); b.onclick = run; el.appendChild(b); }
        }
        function show() {
          if (i >= qs.length) return finish();
          var q = qs[i], tries = 0, solved = false;
          el.innerHTML = "";
          if (bank.boss) {
            var hp = Math.max(0, qs.length - score), bar = h("progress", { max: qs.length, value: hp, "aria-label": "Boss HP" });
            el.appendChild(h("p", { class: "ao-boss" }, [h("strong", { text: "⚔ " + bank.boss.name + "  " }), bar, h("span", { text: "  HP " + hp + "/" + qs.length })]));
          }
          el.appendChild(h("p", { text: "Round " + (i + 1) + " of " + qs.length, class: "ao-round" }));
          el.appendChild(h("p", {}, [h("strong", { text: q.prompt })]));
          var box = h("div", {}), fb = h("p", { "aria-live": "polite", class: "ao-fb" }), next = h("button", { text: "Next ▶", class: "ao-next-btn" });
          next.hidden = true; next.onclick = function () { i++; show(); };
          R[q.type](q, box, function (ok, msg) {
            if (solved) return;
            tries++;
            if (ok) { solved = true; if (tries === 1) score++; var pr = el.querySelector(".ao-boss progress"); if (pr) { pr.value = qs.length - score; pr.nextSibling.textContent = "  HP " + (qs.length - score) + "/" + qs.length; } fb.className = "ao-fb ok"; fb.textContent = (tries === 1 ? "✔ Correct." : "✔ Correct (not first try).") + (q.explain ? " " + q.explain : ""); var w = why(q); if (w) fb.parentNode.insertBefore(w, next); next.hidden = false; next.focus(); }
            else { fb.className = "ao-fb bad"; fb.textContent = "✖ Not quite. " + msg; }
          });
          el.appendChild(box); el.appendChild(fb); el.appendChild(next);
        }
        show();
      }
      run();
    });
  });
})();
