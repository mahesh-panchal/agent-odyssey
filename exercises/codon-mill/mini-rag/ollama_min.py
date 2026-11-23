"""Two tiny helpers for a local Ollama server. Standard library only.

Settings come from environment variables so you can swap models without editing code:
  OLLAMA_URL     default http://127.0.0.1:11434
  CHAT_MODEL     default qwen3:4b      (any model you have pulled)
  EMBED_MODEL    default nomic-embed-text
"""
import json
import math
import os
import urllib.request

URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
CHAT_MODEL = os.environ.get("CHAT_MODEL", "qwen3:4b")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "nomic-embed-text")


def _post(path, body):
    req = urllib.request.Request(
        URL + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)


def embed(texts):
    """One vector (a list of numbers) per text. The same model must embed the notes and the question."""
    return _post("/api/embed", {"model": EMBED_MODEL, "input": texts})["embeddings"]


def chat(prompt, schema=None):
    """Ask the chat model one question. With a JSON schema the reply is JSON that follows it."""
    body = {
        "model": CHAT_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "think": False,
        "options": {"temperature": 0, "num_ctx": 8192},
    }
    if schema:
        body["format"] = schema
    return _post("/api/chat", body)["message"]["content"]


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))
