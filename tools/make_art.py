"""Procedural pixel art: tileset, hero sprite sheet and boss portraits from a fixed palette and fixed seeds."""
import random
import numpy as np
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

# ---- Boss portraits (48x48 art px; the page scales them up with image-rendering: pixelated) ----
B = 48
BP = {"fog": ["#2a3a36", "#3b4f48", "#52695d", "#6f8574", "#8fa393"], "glowc": "#e8b84a", "glow2": "#fff1b8",
      "term": "#0e0b18", "term2": "#1d1630", "text": "#7bd88f", "text2": "#4f9a63"}

def boss_wall(state):
    """The Wall of Output: staggered terminal-brick wall, scrolling text lines, glowing cursor eyes.
    state: 0 full, 1 cracked, 2 broken."""
    r = random.Random(11)                                   # same bricks in every frame
    im = Image.new("RGBA", (B, B), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    bh, bw = 6, 12
    top = (2, 6, 12)[state]
    for row in range(8):
        y = 2 + row * bh
        if y + bh > B - 2 and row > 7: break
        off = 0 if row % 2 == 0 else bw // 2
        for bx in range(-bw, B + bw, bw):
            x = bx + off
            x0, x1 = max(x, 2), min(x + bw - 1, B - 3)
            if x1 - x0 < 2 or y < top - (3 if (x // bw) % 2 else 0) * (state == 2): continue
            if state == 2 and y < top + 6 and r.random() < 0.5: continue          # missing bricks up top
            if state >= 1 and r.random() < (0.10 if state == 1 else 0.22): continue  # holes
            d.rectangle([x0, y, x1, y + bh - 2], fill=BP["term"], outline=P["stone"][2])
            d.line([x0, y, x1, y], fill=P["stone"][0])                                # lit top edge
            ty = y + 2                                                                # text line
            for tx in range(x0 + 2, x1 - 1, 1):
                if r.random() < 0.72: d.point((tx, ty), fill=BP["text"] if r.random() < .6 else BP["text2"])
            if r.random() < .5: d.point((x0 + 2, ty + 1), fill=BP["text2"])
    # face band: eye sockets and cursor mouth
    ey = 15 if state < 2 else 18
    for ex in (13, 29):
        d.rectangle([ex, ey, ex + 5, ey + 8], fill=P["ink"], outline=P["stone"][1])
        if state == 0:
            d.rectangle([ex + 1, ey + 1, ex + 4, ey + 7], fill=P["glow"])             # block cursor eye
            d.rectangle([ex + 1, ey + 1, ex + 2, ey + 3], fill=BP["glow2"])
        elif state == 1:
            d.rectangle([ex + 1, ey + 2, ex + 4, ey + 7], fill=P["glow"])
            d.rectangle([ex + 1, ey + 2, ex + 4, ey + 3], fill=P["ink"])              # half-lidded
        else:
            d.rectangle([ex + 1, ey + 6, ex + 4, ey + 7], fill=P["glow"])             # dim underscore cursor
    my = ey + 13
    d.rectangle([14, my, 33, my + 3], fill=P["ink"], outline=P["stone"][1])
    for i, x in enumerate(range(16, 32, 3)):
        d.rectangle([x, my + 1, x + 1, my + 2], fill=BP["text"] if state == 0 else BP["text2"])
    if state >= 1:                                          # cracks
        pts = [(24, 2), (22, 7), (25, 11), (21, 16), (24, 21), (20, 26), (22, 31), (19, 36)]
        d.line(pts, fill=P["ink"], width=1)
        d.line([(33, 24), (36, 29), (34, 33), (38, 38)], fill=P["ink"])
        if state == 2: d.line([(8, 20), (11, 25), (9, 30), (12, 38)], fill=P["ink"])
    if state == 2:                                          # rubble
        for _ in range(26):
            x, y = r.randrange(3, 45), r.randrange(40, 46)
            d.rectangle([x, y, x + r.randrange(1, 3), y + 1], fill=r.choice([P["stone"][2], BP["term2"], P["stone"][0]]))
    # base / ground shadow
    d.rectangle([2, 46, 45, 46], fill=P["ink"])
    return im

def fog_field(seed, cx=24, cy=26, rad=19):
    """Noisy blob density map in [0, 1]; heaving fog mass."""
    r = np.random.RandomState(seed)
    yy, xx = np.mgrid[0:B, 0:B].astype(float)
    dens = np.zeros((B, B))
    for _ in range(16):
        bx, by = cx + r.uniform(-15, 15), cy + r.uniform(-11, 11) + 2
        br = r.uniform(8, 14)
        dens += np.clip(1 - ((xx - bx) ** 2 + ((yy - by) * 1.1) ** 2) ** .5 / br, 0, 1)
    coarse = r.rand(12, 12)
    noise = np.kron(coarse, np.ones((4, 4)))
    dens = dens * .8 + noise * .35 * (dens > 0.05)
    return dens

def speech_bubble(d, x, y, mark="!"):
    """A little false 'fact': bright bubble, ink border, tail."""
    d.rectangle([x, y, x + 8, y + 6], fill=BP["glow2"], outline=P["ink"])
    d.point((x + 2, y + 7), fill=P["ink"]); d.point((x + 1, y + 7), fill=BP["glow2"]); d.point((x + 2, y + 8), fill=P["ink"])
    d.line([x + 2, y + 2, x + 6, y + 2], fill=P["glow"]); d.line([x + 2, y + 4, x + 5, y + 4], fill=P["glow"])

def sparkle(d, x, y, c="#ffffff"):
    d.point((x, y), fill=c)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)): d.point((x + dx, y + dy), fill=P["glow"])

def boss_murk():
    im = Image.new("RGBA", (B, B), (0, 0, 0, 0)); px = im.load()
    dens = fog_field(5)
    pal = BP["fog"]
    for y in range(B):
        for x in range(B):
            v = dens[y, x]
            if v < .38: continue
            shade = 0 if v < .55 else 1 if v < .8 else 2 if v < 1.1 else 3
            if y < 22 and shade < 3 and (x + y) % 5 == 0: shade += 1                # lit upper wisps
            px[x, y] = tuple(int(pal[shade][i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    d = ImageDraw.Draw(im)
    # outline: darken any filled pixel next to transparent
    src = im.copy(); sp = src.load()
    for y in range(B):
        for x in range(B):
            if sp[x, y][3] and any(not (0 <= x + a < B and 0 <= y + b < B) or sp[x + a, y + b][3] == 0
                                    for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                px[x, y] = (0x1a, 0x24, 0x22, 255)
    # hollow core with two pale pinprick eyes (a little absurd, not scary)
    d.ellipse([15, 19, 32, 38], fill=P["ink"], outline="#1a2422")
    d.ellipse([17, 21, 30, 36], fill="#0c0a14")
    d.rectangle([20, 26, 21, 28], fill=BP["fog"][4]); d.rectangle([26, 26, 27, 28], fill=BP["fog"][4])
    d.line([22, 32, 25, 32], fill=BP["fog"][2])
    # false glowing facts floating in the fog
    speech_bubble(d, 3, 9); speech_bubble(d, 36, 5); speech_bubble(d, 37, 30)
    sparkle(d, 12, 33); sparkle(d, 33, 15); sparkle(d, 8, 22)
    return im

def boss_murk_cleared():
    im = Image.new("RGBA", (B, B), (0, 0, 0, 0)); d = ImageDraw.Draw(im); px = im.load()
    r = random.Random(3)
    # mossy mound
    for y in range(34, 46):
        half = int(18 * (1 - ((y - 34) / 12.0) ** 2) ** .5) + 1
        for x in range(24 - half, 24 + half):
            px[x, y] = tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,) if (c := r.choice(P["grass"])) else None
    d.line([10, 34, 38, 34], fill=P["leaf"][2])
    # sprout: stem, two leaves, bud
    d.line([24, 34, 24, 22], fill=P["leaf"][1], width=2)
    d.polygon([(23, 30), (15, 27), (12, 29), (16, 32), (23, 32)], fill=P["leaf"][1], outline=P["leaf"][2])
    d.polygon([(25, 27), (33, 23), (36, 25), (32, 28), (25, 29)], fill=P["grass"][1], outline=P["leaf"][2])
    d.ellipse([21, 17, 27, 23], fill=P["glow"], outline=P["ink"])                      # small light
    d.rectangle([23, 19, 24, 20], fill=BP["glow2"])
    for x, y in ((24, 12), (24, 11), (24, 13), (19, 15), (29, 15), (17, 21), (31, 21)): d.point((x, y), fill=BP["glow2"] if (x, y) != (24, 12) else P["glow"])
    # last thin wisps of fog at the edges
    f = fog_field(9)
    for y in range(B):
        for x in range(B):
            if (x < 9 or x > 38) and f[y, x] > 1.15 and y > 30 and px[x, y][3] == 0 and (x + y) % 2 == 0:
                px[x, y] = tuple(int(BP["fog"][3][i:i + 2], 16) for i in (1, 3, 5)) + (110,)
    sparkle(d, 9, 14); sparkle(d, 40, 11)
    return im

boss_wall(0).save(OUT / "boss-wall.png")
boss_wall(1).save(OUT / "boss-wall-cracked.png")
boss_wall(2).save(OUT / "boss-wall-broken.png")
boss_murk().save(OUT / "boss-murk.png")
boss_murk_cleared().save(OUT / "boss-murk-cleared.png")
print("ok art")
