"""Fixture page + bank exercising every question type; kept out of the real site."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

def build(site):
    bank = {"pass": 0.8, "questions": [
      {"type": "order", "prompt": "Order", "items": ["one", "two", "three"], "why": {"two": "two goes second"}},
      {"type": "sort", "prompt": "Sort", "bins": ["allow", "deny"], "items": [
         {"text": "ls", "bin": "allow", "misconception": "ls only reads"}, {"text": "rm -rf ~", "bin": "deny", "misconception": "deletes everything"}]},
      {"type": "faulty-line", "prompt": "Find it", "lines": [{"text": "ok", "why": "fine"}, {"text": "bad", "faulty": True}]},
      {"type": "match", "prompt": "Match", "pairs": [{"left": "a", "right": "A", "misconception": "a is A"}, {"left": "b", "right": "B"}]}]}
    (site / "assets/data/fixture.json").write_text(json.dumps(bank))
    footer = (ROOT / "assets/html/footer.html").read_text()
    (site / "fixture.html").write_text('<!doctype html><link rel="stylesheet" href="assets/css/rpg.css"><body><div data-ao-test="fixture" data-xp="10"></div>' + footer)


