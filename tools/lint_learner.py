"""Lint learner-facing prose in zones/**/*.qmd (and start-here.qmd).

Errors (exit 1): maintainer labels and caveat boxes in lesson text, mid-text references to other quests.
Warnings (with --warn): attribution, X-not-Y contrast phrasing and bold run-in paragraphs.
Allowed places for another quest's title or link: the Prerequisites line in the quest-dialog, and the
`.ao-related` block. Provenance belongs in research/claims/*.md.
"""
import re, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
world = yaml.safe_load((ROOT / "zones.yml").read_text())
quests = {}
for g in world["gates"].values():
    for q in g.get("quests", []):
        quests[q["page"].replace(".html", ".qmd")] = q["title"]
TITLES = {t for t in quests.values()}

ERR = [
    (r"ao-badge", "caveat badge"),
    (r"\bGeneral practice\b|\bgeneral practice\b", "provenance label 'General practice'"),
    (r"Last verified|Verified: ran|\bNot checked\b|Not confirmed here|Not run by this course", "provenance label"),
    (r"\{\.callout-(warning|important)", "caveat callout"),
    (r"supported by|not supported|unsupported by", "'supported by' wording"),
    (r"\(see |\bSee \*|\bsee \*|\bsee the (quest|next|earlier|previous)", "mid-text 'see ...' pointer"),
    (r"research/[\w-]+\.md", "research-note path in lesson text"),
    (r"\bour inference\b|\bthis course's own\b|\blabelled\b", "maintainer note"),
]
WARN = [
    (r"\b(docs|page|paper|guide|article|post|documentation) (say|says|state|states|read|reads)\b|\bAccording to\b|\bper the docs\b", "attribution"),
    (r"\bnot (just|only) [^.]{0,50}\bbut\b|\bis not [^.]{0,40}, it is\b|\bisn't [^.]{0,40}, it's\b|\bnot a [^.]{0,30}, but\b", "X-not-Y contrast"),
    (r"\b(armou?r|the Beast|Blight|companions? are|quartermaster)\b", "odyssey imagery outside the story block"),
    (r"^\*\*[^*]+\*\*[.:]? [^\n]{40,}$", "bold run-in paragraph (consider a list)"),
]

def body_of(text):
    text = re.sub(r"\A---.*?---\n", "", text, flags=re.S)
    text = re.split(r"\n::: ?\{\.ao-lore\}", text)[0]
    text = re.sub(r"\n::: ?\{\.ao-related\}.*?\n:::\n?", "\n", text, flags=re.S)
    text = re.sub(r"::: ?\{\.ao-story\}.*?\n:::\n?", "\n", text, flags=re.S)  # story blocks may use odyssey imagery and foreshadow
    text = re.sub(r"::: ?\{\.quest-dialog\}.*?\n:::", lambda m: "\n".join(l for l in m.group(0).splitlines() if "Prerequisites" not in l and "Before you start" not in l), text, flags=re.S)
    return text

def main():
    errs = warns = 0
    files = sorted((ROOT / "zones").rglob("*.qmd")) + [ROOT / "start-here.qmd"]
    strict = "--warn" in sys.argv
    for f in files:
        rel = str(f.relative_to(ROOT))
        text = body_of(f.read_text())
        for n, line in enumerate(text.splitlines(), 1):
            if re.match(r"\s*(```|    )", line): continue
            for pat, why in ERR:
                if re.search(pat, line):
                    print(f"ERROR {rel}: {why}: {line.strip()[:110]}"); errs += 1
            for t in TITLES:
                if f.name != "start-here.qmd" and quests.get(rel) != t and re.search(r"(\*|\[|“|\")" + re.escape(t) + r"(\*|\]|”|\")", line):
                    print(f"ERROR {rel}: mid-text reference to '{t}': {line.strip()[:90]}"); errs += 1
            if strict:
                for pat, why in WARN:
                    if re.search(pat, line):
                        print(f"warn  {rel}: {why}: {line.strip()[:110]}"); warns += 1
    print(f"{errs} error(s), {warns} warning(s)")
    return 1 if errs else 0

if __name__ == "__main__":
    sys.exit(main())
