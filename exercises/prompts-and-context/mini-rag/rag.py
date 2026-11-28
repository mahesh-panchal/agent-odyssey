"""Simple RAG over the notes/ folder: one note = one chunk.

  python rag.py "your question"            retrieve the top 3 notes, answer from them
  python rag.py "your question" -k 5       retrieve the top 5
  python rag.py "your question" --all      no retrieval: put every note in the prompt
"""
import argparse
from pathlib import Path

from ollama_min import chat, cosine, embed

ap = argparse.ArgumentParser()
ap.add_argument("question")
ap.add_argument("-k", type=int, default=3)
ap.add_argument("--all", action="store_true")
args = ap.parse_args()

notes = {p.name: p.read_text().strip() for p in sorted(Path(__file__).parent.glob("notes/*.txt"))}

if args.all:
    chosen = list(notes)
else:
    names = list(notes)
    vectors = embed([notes[n] for n in names])        # step 1: embed every chunk
    q = embed([args.question])[0]                     # step 2: embed the question
    scored = sorted(zip(names, (cosine(q, v) for v in vectors)), key=lambda s: -s[1])
    chosen = [n for n, _ in scored[: args.k]]         # step 3: keep the k closest
    print("Retrieved:")
    for n, s in scored[: args.k]:
        print(f"  {s:.3f}  {n}")

context = "\n\n".join(f"[{n}]\n{notes[n]}" for n in chosen)
prompt = (
    "Answer the question using only the notes below. If the notes do not contain the answer, say so. "
    "Name the notes you used.\n\n"
    f"{context}\n\nQuestion: {args.question}"
)
print("\nAnswer:\n" + chat(prompt))
