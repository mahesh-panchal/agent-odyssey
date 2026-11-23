/* Path graph: trunk, branches and the final boss rule, read from world.json (graph). No DOM use.
   Progress is AO.state.passed (quest id -> true). Everything except the finale is advice, never a lock. */
(function () {
  var AO = window.AO = window.AO || {};
  var G = null, loading = null;

  function passed(id) { return !!(AO.state && AO.state.passed && AO.state.passed[id]); }
  function ids() { return G ? Object.keys(G.quests) : []; }
  function full(id) { var q = G && G.quests[id]; return q ? Object.assign({ id: id }, q) : null; }
  function isFinale(id) { return !!G && G.finale.id === id; }
  function trunk() { return G ? G.trunk_order : []; }
  function ready(id) { return G.quests[id].after.every(passed); }
  function branchQuests(b) { return ids().filter(function (id) { return G.quests[id].branch === b; }); }
  function required(b) { return branchQuests(b).filter(function (id) { return !G.quests[id].optional; }); }
  function rule() { return G.finale.requires.branches; }

  function trunkDone() { return !!G && trunk().every(passed); }

  function branches() {
    if (!G) return [];
    return G.branches.map(function (b) {
      var req = required(b.id), done = req.filter(passed).length;
      return { id: b.id, name: b.name, blurb: b.blurb, who: b.who, done: done, total: req.length, complete: req.length > 0 && done === req.length };
    });
  }
  function branchesComplete() {
    if (!G) return 0;
    var of = rule().of;
    return branches().filter(function (b) { return b.complete && of.indexOf(b.id) >= 0; }).length;
  }
  function finaleUnlocked() { return !!G && trunkDone() && branchesComplete() >= rule().any; }
  function remainingForFinale() {
    if (!G) return { trunk: [], branchesNeeded: 0 };
    return { trunk: trunk().filter(function (id) { return !passed(id); }).map(full),
             branchesNeeded: Math.max(0, rule().any - branchesComplete()) };
  }

  function status(id) {
    if (!G || !G.quests[id]) return "waiting";
    if (passed(id)) return "cleared";
    if (isFinale(id)) return finaleUnlocked() ? "ready" : "waiting";
    return ready(id) ? "ready" : "waiting";
  }

  function questByPage(pathname) {
    if (!G || !pathname) return null;
    var p = String(pathname).split(/[?#]/)[0].replace(/\.html$/, "").replace(/\/$/, "");
    var hit = ids().filter(function (id) {
      var pg = G.quests[id].page.replace(/\.html$/, "");
      return p === pg || p.slice(-(pg.length + 1)) === "/" + pg;
    })[0];
    return hit ? full(hit) : null;
  }

  function nextQuest() {
    if (!G) return null;
    var t = trunk().filter(function (id) { return !passed(id); });
    if (t.length) return full(t.filter(ready)[0] || t[0]);
    if (finaleUnlocked() && !passed(G.finale.id)) return full(G.finale.id);
    var cands = branches().filter(function (b) { return !b.complete; }).map(function (b, i) {
      var nq = required(b.id).filter(function (id) { return !passed(id) && ready(id); })[0];
      return { b: b, i: i, nq: nq };
    }).filter(function (c) { return c.nq; });
    cands.sort(function (a, c) { return (c.b.done - a.b.done) || (c.b.done / c.b.total - a.b.done / a.b.total) || (a.i - c.i); });
    return cands.length ? full(cands[0].nq) : null;
  }

  function nextSteps(id) {
    var out = { unlocks: [], recommended: [], optional: [] };
    if (!G || !G.quests[id]) return out;
    var me = G.quests[id], all = ids().filter(function (k) { return k !== id && !isFinale(k); });
    var unlocks = all.filter(function (k) { return G.quests[k].after.indexOf(id) >= 0; });
    var softer = all.filter(function (k) { return G.quests[k].suggested.indexOf(id) >= 0; });
    var open = function (k) { return !passed(k) && ready(k); };
    var rec = [];
    function add(k) { if (k && rec.indexOf(k) < 0 && rec.length < 3) rec.push(k); }
    unlocks.filter(open).filter(function (k) { return !G.quests[k].optional; }).forEach(add);
    softer.filter(open).filter(function (k) { return !G.quests[k].optional; }).forEach(add);
    if (rec.length < 3) {
      var nq = nextQuest();
      if (nq && nq.id !== id) add(nq.id);
    }
    var opt = unlocks.concat(softer, all.filter(function (k) { return G.quests[k].branch === me.branch && me.branch !== "trunk"; }))
      .filter(function (k, i, a) { return a.indexOf(k) === i && G.quests[k].optional && !passed(k) && ready(k); });
    out.unlocks = unlocks.map(full);
    out.recommended = rec.map(full);
    out.optional = opt.map(full);
    return out;
  }

  function load() {
    if (!loading) loading = fetch(window.AO_BASE + "assets/data/world.json")
      .then(function (r) { return r.json(); })
      .then(function (w) { G = w.graph || null; if (!G) loading = null; return G; })
      .catch(function () { loading = null; return null; });
    return loading;
  }

  // Ordered lists for the text version of the map: trunk in order, each branch with required quests first, optional last.
  function trunkQuests() { return trunk().map(full); }
  function laneQuests(b) {
    if (!G) return [];
    var rest = branchQuests(b), placed = [];
    while (rest.length) {
      var okIds = rest.filter(function (id) { return G.quests[id].after.concat(G.quests[id].suggested).every(function (d) { return rest.indexOf(d) < 0; }); });
      var pick = okIds[0] || rest[0];
      placed.push(pick); rest.splice(rest.indexOf(pick), 1);
    }
    var req = placed.filter(function (id) { return !G.quests[id].optional; });
    return req.concat(placed.filter(function (id) { return G.quests[id].optional; })).map(full);
  }
  // The step before this one on its own path: the previous trunk quest, or the previous quest in its branch.
  function prevQuest(id) {
    if (!G || !G.quests[id]) return null;
    var q = G.quests[id], list = q.branch === "trunk" ? trunk().slice() : laneQuests(q.branch).map(function (x) { return x.id; });
    if (isFinale(id)) return full(trunk()[trunk().length - 1]);
    var i = list.indexOf(id);
    return i > 0 ? full(list[i - 1]) : null;
  }
  // The step after this one on its own path (advice only): the next trunk quest, or the next required quest in its branch.
  function followQuest(id) {
    if (!G || !G.quests[id] || isFinale(id)) return null;
    var q = G.quests[id];
    var list = q.branch === "trunk" ? trunk().slice() : laneQuests(q.branch).filter(function (x) { return !x.optional; }).map(function (x) { return x.id; });
    var i = list.indexOf(id);
    return i >= 0 && i < list.length - 1 ? full(list[i + 1]) : null;
  }
  function finale() { return G ? full(G.finale.id) : null; }
  function finaleRule() { return G ? { any: rule().any, of: rule().of.length } : null; }
  var WORDS = { cleared: "cleared", ready: "ready", waiting: "" };
  function stateLabel(st) { return WORDS[st] || st; }

  AO.path = { load: load, quest: function (id) { return full(id); }, questByPage: questByPage, status: status,
              trunkDone: trunkDone, branches: branches, branchesComplete: branchesComplete,
              finaleUnlocked: finaleUnlocked, remainingForFinale: remainingForFinale, nextSteps: nextSteps, nextQuest: nextQuest,
              finale: finale, finaleRule: finaleRule, trunkQuests: trunkQuests, laneQuests: laneQuests, stateLabel: stateLabel, prevQuest: prevQuest, followQuest: followQuest };
})();
