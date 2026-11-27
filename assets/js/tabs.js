/* Persona tabs: if a saved choice matches no tab (for example after a tab was renamed), select the first tab.
   Quarto's own tab-group persistence leaves every tab unselected and every pane hidden in that case, and it
   does so after the page scripts run, so the repair watches the tabs instead of running once. */
(function () {
  function repair(set) {
    var links = set.querySelectorAll(".nav-link");
    if (links.length && !set.querySelector(".nav-link.active")) links[0].click();
  }
  document.querySelectorAll(".panel-tabset").forEach(function (set) {
    repair(set);
    new MutationObserver(function () { repair(set); }).observe(set, { attributes: true, subtree: true, attributeFilter: ["class"] });
  });
})();
