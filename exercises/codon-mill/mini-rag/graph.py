"""A hand-made graph RAG over the notes/ folder, small enough to read in one sitting.

  python graph.py build            ask the model for (subject, relation, object) facts from each note
                                   and save them to graph.json
  python graph.py show             print the saved facts so you can check them
  python graph.py ask "question"   find the entities the question is about, walk the graph outward,
                                   and answer from the facts and the notes they came from
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path

from ollama_min import chat, cosine, embed

HERE = Path(__file__).parent
GRAPH = HERE / "graph.json"
SCHEMA = {
    "type": "object",
    "properties": {
        "facts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "subject": {"type": "string"},
                    "relation": {"type": "string"},
                    "object": {"type": "string"},
                },
                "required": ["subject", "relation", "object"],
            },
        }
    },
    "required": ["facts"],
}


def build():
    facts = []
    for p in sorted(HERE.glob("notes/*.txt")):
        text = p.read_text().strip()
        prompt = (
            "Extract the facts in this note as (subject, relation, object) triples. "
            "Use short, consistent names for things (for example 'Run R7', 'Orion', 'Pipeline 2.3'). "
            "Write out every sample or item in a range such as 'S31 to S36' as its own fact. "
            "Only state what the note says.\n\nNote:\n" + text
        )
        got = json.loads(chat(prompt, SCHEMA))["facts"]
        for f in got:
            f["note"] = p.name
        facts += got
        print(f"{p.name}: {len(got)} facts")
    GRAPH.write_text(json.dumps(facts, indent=1))
    print(f"saved {len(facts)} facts to {GRAPH.name}")


def show():
    for f in json.loads(GRAPH.read_text()):
        print(f"{f['subject']} --{f['relation']}--> {f['object']}    [{f['note']}]")


def ask(question, seeds=3, hops=2):
    facts = json.loads(GRAPH.read_text())
    for f in facts:                                  # models sometimes pad names with spaces
        f["subject"], f["object"] = f["subject"].strip(), f["object"].strip()
    edges = defaultdict(list)                        # entity -> facts that mention it
    for f in facts:
        edges[f["subject"].lower()].append(f)
        edges[f["object"].lower()].append(f)
    names = list(edges)

    # 1. Find the entities the question is about: names written in the question, plus the closest by meaning.
    found = [n for n in names if n in question.lower()]
    q = embed([question])[0]
    close = sorted(zip(names, (cosine(q, v) for v in embed(names))), key=lambda s: -s[1])
    frontier = set(found) | {n for n, _ in close[:seeds]}
    print("Starting entities:", sorted(frontier))

    # 2. Walk outward from them, a few hops.
    seen, used = set(frontier), []
    for _ in range(hops):
        nxt = set()
        for n in frontier:
            for f in edges[n]:
                if f not in used:
                    used.append(f)
                for end in (f["subject"].lower(), f["object"].lower()):
                    if end not in seen:
                        seen.add(end)
                        nxt.add(end)
        frontier = nxt

    # 3. Answer from those facts and the notes they came from.
    note_names = sorted({f["note"] for f in used})
    print(f"Collected {len(used)} facts from {len(note_names)} notes: {', '.join(note_names)}")
    fact_lines = "\n".join(f"- {f['subject']} {f['relation']} {f['object']}" for f in used)
    note_text = "\n".join(f"[{n}] {(HERE / 'notes' / n).read_text().strip()}" for n in note_names)
    prompt = (
        "Answer the question using only the facts and notes below. If they do not contain the answer, say so. "
        "Name the notes you used.\n\nFacts:\n" + fact_lines + "\n\nNotes:\n" + note_text + "\n\nQuestion: " + question
    )
    print("\nAnswer:\n" + chat(prompt))


ap = argparse.ArgumentParser()
ap.add_argument("cmd", choices=["build", "show", "ask"])
ap.add_argument("question", nargs="?")
a = ap.parse_args()
{"build": build, "show": show}.get(a.cmd, lambda: ask(a.question))()
