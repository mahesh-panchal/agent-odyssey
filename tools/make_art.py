"""Procedural pixel art: tileset + hero sprite sheet from a fixed palette and fixed seed."""
import random
from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent.parent / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)
P = {
    "grass": ["#3f7d3a", "#488a42", "#37702f"], "path": ["#b99a62", "#c7aa72", "#a88a54"],
    "water": ["#2b5fa3", "#3470b8", "#244f8a"], "trunk": "#5a3a22", "leaf": ["#215c2b", "#2a6e33", "#1a4a22"],
    "stone": ["#8a8799", "#a29fb3", "#6f6c80"], "glow": "#e8b84a", "ink": "#1a1428",
    "skin": "#f0c89a", "hair": "#5a3a22", "cloak": "#3b6fb6", "cloak2": "#2c5290",
}
T = 16
rng = random.Random(7)

def speckle(d, base, colors, n=22):
    d.rectangle([0, 0, T - 1, T - 1], fill=colors[0])
    for _ in range(n):
        d.point((rng.randrange(T), rng.randrange(T)), fill=rng.choice(colors))

def tile(kind):
    im = Image.new("RGBA", (T, T)); d = ImageDraw.Draw(im)
    if kind == "grass":
        speckle(d, 0, P["grass"])
    elif kind == "path":
        speckle(d, 0, P["path"], 30)
    elif kind == "water":
        speckle(d, 0, P["water"], 18)
        for x in (3, 9): d.line([x, 6, x + 3, 6], fill="#8fb8ea")
    elif kind == "tree":
        speckle(d, 0, P["grass"])
        d.rectangle([7, 10, 8, 15], fill=P["trunk"])
        d.ellipse([2, 1, 13, 11], fill=P["leaf"][1], outline=P["leaf"][2])
        d.ellipse([4, 3, 8, 6], fill=P["leaf"][0])
    elif kind == "gate":
        speckle(d, 0, P["path"], 20)
        d.rectangle([2, 4, 13, 15], fill=P["stone"][0], outline=P["ink"])
        d.rectangle([5, 8, 10, 15], fill=P["ink"])
        d.rectangle([1, 2, 14, 4], fill=P["stone"][1], outline=P["ink"])
        d.point((7, 3), fill=P["glow"]); d.point((8, 3), fill=P["glow"])
    elif kind == "stone":
        speckle(d, 0, P["grass"])
        d.ellipse([4, 7, 12, 13], fill=P["stone"][0], outline=P["ink"])
        d.point((6, 9), fill=P["stone"][1])
    return im

def hero(direction, frame):
    im = Image.new("RGBA", (T, T)); d = ImageDraw.Draw(im)
    step = (0, 1, 0)[frame], (0, 0, 1)[frame]            # alternating leg lift
    d.rectangle([5, 7, 10, 12], fill=P["cloak"], outline=P["ink"])         # body
    d.line([5, 12, 10, 12], fill=P["cloak2"])
    d.rectangle([5, 13 - step[0], 6, 14], fill=P["ink"])                    # legs
    d.rectangle([9, 13 - step[1], 10, 14], fill=P["ink"])
    d.rectangle([5, 2, 10, 7], fill=P["skin"], outline=P["ink"])            # head
    d.rectangle([5, 2, 10, 4], fill=P["hair"])
    if direction == "down":
        d.point((6, 5), fill=P["ink"]); d.point((9, 5), fill=P["ink"])
    elif direction == "left":
        d.point((6, 5), fill=P["ink"]); d.rectangle([9, 3, 10, 6], fill=P["hair"])
    elif direction == "right":
        d.point((9, 5), fill=P["ink"]); d.rectangle([5, 3, 6, 6], fill=P["hair"])
    else:
        d.rectangle([5, 2, 10, 6], fill=P["hair"])
    return im

kinds = ["grass", "path", "water", "tree", "gate", "stone"]
sheet = Image.new("RGBA", (T * len(kinds), T))
for i, k in enumerate(kinds): sheet.paste(tile(k), (i * T, 0))
sheet.save(OUT / "tiles.png")

dirs = ["down", "left", "right", "up"]
hs = Image.new("RGBA", (T * 3, T * 4))
for r, dr in enumerate(dirs):
    for c in range(3): hs.paste(hero(dr, c), (c * T, r * T))
hs.save(OUT / "hero.png")
print("ok art")
