/* A one-line story key under the first story block, so a page opened alone still explains the cast. */
(function () {
  var s = document.querySelector(".ao-story");
  if (!s || document.querySelector(".ao-storykey")) return;
  var p = document.createElement("p");
  p.className = "ao-storykey";
  p.textContent = "In this story an Astral is a language model, an automaton is a script, a familiar is a trained model (all three are shokanju, summoned creatures), and the Blight is false output that nobody checked. The party is a manager (Guildmaster Aris), an analyst (Diviner Ilsa), an engineer (Artificer Bob) and a data steward (Archivist Elowen). Brannoch, Sefa, Tam and Oleander are tavern patrons, not the party. The lessons use plain technical words.";
  s.parentNode.insertBefore(p, s.nextSibling);
})();
