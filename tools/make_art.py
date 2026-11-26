"""Procedural pixel art: tileset, hero sprite sheet and boss portraits from a fixed palette and fixed seeds."""
import random
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw

def save(img, path):
    """Save a PNG only when its bytes changed (keeps `quarto preview` from reloading on every pre-render)."""
    import io
    buf = io.BytesIO(); img.save(buf, "PNG"); data = buf.getvalue()
    if not path.exists() or path.read_bytes() != data:
        path.write_bytes(data)


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
save(sheet, OUT / "tiles.png")

dirs = ["down", "left", "right", "up"]
hs = Image.new("RGBA", (T * 3, T * 4))
for r, dr in enumerate(dirs):
    for c in range(3): hs.paste(hero(dr, c), (c * T, r * T))
save(hs, OUT / "hero.png")

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

save(boss_wall(0), OUT / "boss-wall.png")
save(boss_wall(1), OUT / "boss-wall-cracked.png")
save(boss_wall(2), OUT / "boss-wall-broken.png")
save(boss_murk(), OUT / "boss-murk.png")
save(boss_murk_cleared(), OUT / "boss-murk-cleared.png")

# ---- Party portraits and creature kinds (48x48; same fixed-seed, fixed-palette approach) ----
C = {"ink": "#1a1428", "skin": ["#f0c89a", "#c68642", "#8d5524", "#e0ac69"], "skin_sh": ["#d9aa7a", "#a86c30", "#6e3f18", "#c28d4f"],
     "gold": "#e8b84a", "gold2": "#fff1b8", "brass": ["#b5873a", "#d7a84e", "#7e5a22"], "paper": "#efe3c2", "wax": "#a83232"}

def outline_px(im, col=C["ink"]):
    """Add a 1px ink outline around every opaque pixel."""
    src = im.copy(); sp = src.load(); px = im.load()
    for y in range(B):
        for x in range(B):
            if sp[x, y][3] == 0 and any(0 <= x + a < B and 0 <= y + b < B and sp[x + a, y + b][3] > 0
                                         for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                px[x, y] = tuple(int(col[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    return im

def bust(skin, hair, style, robe, robe2, trim, extra=None, glasses=False):
    im = Image.new("RGBA", (B, B), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sk, ssh = C["skin"][skin], C["skin_sh"][skin]
    if style == "long": d.rectangle([13, 12, 34, 34], fill=hair)
    d.polygon([(6, 47), (9, 35), (17, 30), (30, 30), (38, 35), (41, 47)], fill=robe)       # shoulders
    d.polygon([(6, 47), (9, 35), (13, 33), (12, 47)], fill=robe2)
    d.polygon([(41, 47), (38, 35), (34, 33), (35, 47)], fill=robe2)
    d.rectangle([21, 25, 26, 31], fill=ssh)                                                  # neck
    d.polygon([(17, 30), (24, 38), (31, 30), (28, 30), (24, 34), (20, 30)], fill=trim)       # collar trim
    d.ellipse([15, 8, 32, 27], fill=sk)                                                      # head
    d.rectangle([15, 17, 16, 20], fill=sk); d.rectangle([31, 17, 32, 20], fill=sk)           # ears
    if style in ("short", "long", "cap"):
        d.pieslice([14, 5, 33, 22], 180, 360, fill=hair); d.rectangle([15, 11, 32, 13], fill=hair)
    if style == "bald":
        d.arc([14, 5, 33, 22], 200, 340, fill=hair)
    if style == "hood":
        d.pieslice([12, 3, 35, 24], 180, 360, fill=robe2); d.rectangle([12, 13, 15, 26], fill=robe2); d.rectangle([32, 13, 35, 26], fill=robe2)
        d.ellipse([16, 10, 31, 26], fill=sk)
    d.point((20, 18), fill=C["ink"]); d.point((27, 18), fill=C["ink"])
    d.line([22, 23, 25, 23], fill=ssh)
    if glasses:
        d.rectangle([18, 16, 22, 20], outline=C["ink"]); d.rectangle([25, 16, 29, 20], outline=C["ink"]); d.line([22, 18, 25, 18], fill=C["ink"])
    if extra: extra(d, im)
    return outline_px(im)

def x_guildmaster(d, im):
    d.rectangle([2, 38, 14, 47], fill=C["paper"], outline=C["ink"])                         # ledger
    for y in (40, 42, 44): d.line([4, y, 12, y], fill="#9b8a60")
    d.line([30, 34, 24, 40], fill=C["gold"]); d.line([18, 34, 24, 40], fill=C["gold"])       # chain of office
    d.ellipse([22, 39, 26, 43], fill=C["gold"], outline=C["ink"])
    d.ellipse([39, 36, 45, 42], fill=C["gold2"], outline=C["ink"]); d.point((42, 39), fill=C["gold"])   # milestone beacon

def x_diviner(d, im):
    d.ellipse([33, 33, 45, 45], fill="#bfe6f5", outline=C["ink"]); d.ellipse([35, 35, 40, 40], fill="#ffffff")   # ground-truth lens
    d.line([33, 44, 28, 47], fill=C["brass"][0], width=2)
    for (x, y) in ((5, 12), (42, 10), (7, 34)): sparkle(d, x, y)

def x_artificer(d, im):
    d.rectangle([15, 6, 32, 10], fill=C["brass"][1], outline=C["ink"])                      # goggles on the brow
    d.ellipse([16, 5, 22, 11], fill="#9fd3e6", outline=C["ink"]); d.ellipse([25, 5, 31, 11], fill="#9fd3e6", outline=C["ink"])
    d.rectangle([12, 34, 36, 47], fill="#7a4a24")                                            # leather apron
    d.rectangle([20, 38, 28, 44], fill="#5a3a22", outline=C["ink"])
    d.ellipse([36, 36, 45, 45], fill=C["brass"][1], outline=C["ink"]); d.ellipse([39, 39, 42, 42], fill=C["ink"])  # gear
    for (x, y) in ((40, 34), (46, 40), (40, 47), (35, 40)): d.point((x, y), fill=C["brass"][1])
    sparkle(d, 5, 20); sparkle(d, 44, 20)

def x_archivist(d, im):
    d.ellipse([3, 36, 11, 44], outline=C["brass"][1], width=2)                               # key ring
    d.line([11, 40, 18, 44], fill=C["brass"][1], width=2); d.rectangle([17, 43, 20, 46], fill=C["brass"][1])
    d.rectangle([34, 37, 45, 46], fill=C["paper"], outline=C["ink"]); d.ellipse([37, 39, 42, 44], fill=C["wax"], outline=C["ink"])   # sealed scroll
    d.rectangle([5, 12, 6, 12], fill=C["gold"])

def personas():
    return {
        "guildmaster": bust(0, "#5a3a22", "short", "#2f6b4f", "#245640", C["gold"], x_guildmaster),
        "diviner":     bust(1, "#1a1428", "hood", "#3b3f8f", "#2b2f6e", "#a9b4ff", x_diviner),
        "artificer":   bust(2, "#2a1a10", "short", "#b8672a", "#8f4f1f", C["brass"][1], x_artificer),
        "archivist":   bust(3, "#7a7a8c", "long", "#6b5a8f", "#51436f", "#d8cfa3", x_archivist, glasses=True),
    }

def kind_automaton():
    im = Image.new("RGBA", (B, B), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    b0, b1, b2 = C["brass"][0], C["brass"][1], C["brass"][2]
    for x in (11, 18, 29, 36):                                                               # jointed legs
        d.rectangle([x, 30, x + 3, 36], fill=b0); d.rectangle([x - 1, 36, x + 4, 42], fill=b2)
    d.rectangle([9, 18, 38, 31], fill=b1)                                                    # body plates
    d.line([9, 24, 38, 24], fill=b2)
    for x in range(11, 37, 6): d.point((x, 20), fill=b2); d.point((x, 28), fill=b2)          # rivets
    d.ellipse([18, 19, 29, 30], fill=b0, outline=C["ink"]); d.ellipse([21, 22, 26, 27], fill=C["ink"])   # gear with a hub
    for (x, y) in ((23, 18), (23, 31), (17, 24), (30, 24)): d.rectangle([x, y, x + 1, y + 1], fill=b0)
    d.rectangle([34, 11, 45, 22], fill=b1)                                                   # head
    d.polygon([(40, 11), (42, 6), (44, 11)], fill=b0)                                        # ear plate
    d.ellipse([38, 14, 43, 19], fill="#bfe6f5", outline=C["ink"]); d.point((40, 16), fill="#ffffff")      # lens eye
    d.rectangle([43, 18, 46, 21], fill=b2)                                                   # muzzle
    d.line([9, 22, 3, 18], fill=b2, width=2); d.line([3, 18, 3, 14], fill=b2, width=2)        # wind-up key
    d.ellipse([1, 10, 6, 15], outline=b1, width=2)
    d.rectangle([4, 43, 44, 44], fill=C["ink"])
    return outline_px(im)

def kind_familiar():
    im = Image.new("RGBA", (B, B), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fur, fur2, belly = "#a8683a", "#7a4a26", "#f0d9b5"
    d.polygon([(8, 38), (3, 24), (7, 20), (11, 30)], fill=fur2)                              # tail
    d.polygon([(7, 20), (4, 16), (9, 18)], fill=belly)
    d.ellipse([8, 22, 32, 44], fill=fur)                                                     # haunch and body
    d.ellipse([20, 20, 34, 40], fill=fur)
    d.rectangle([13, 36, 19, 45], fill=fur2); d.rectangle([24, 36, 30, 45], fill=fur2)       # legs
    d.rectangle([12, 44, 20, 46], fill=belly); d.rectangle([23, 44, 31, 46], fill=belly)
    d.polygon([(30, 8), (28, 0), (35, 6)], fill=fur2); d.polygon([(38, 6), (42, 0), (43, 9)], fill=fur2)   # ears
    d.ellipse([28, 6, 44, 24], fill=fur)                                                     # head
    d.polygon([(40, 14), (47, 18), (40, 23)], fill=belly)                                    # muzzle
    d.point((46, 18), fill=C["ink"]); d.point((37, 12), fill=C["ink"]); d.point((38, 12), fill=C["ink"])
    d.rectangle([29, 22, 41, 25], fill="#3b6fb6")                                            # collar
    d.ellipse([33, 25, 38, 30], fill=C["gold"], outline=C["ink"]); d.line([35, 26, 35, 29], fill=C["ink"])       # rune tag
    for (x, y) in ((5, 8), (44, 38), (3, 40)): sparkle(d, x, y)
    return outline_px(im)

def kind_astral():
    """A starry serpent of light with a dragon's head: dark body, lighter head so the silhouette reads."""
    im = Image.new("RGBA", (B, B), (0, 0, 0, 0)); d = ImageDraw.Draw(im); r = random.Random(21)
    ctrl = [(5, 43), (9, 35), (17, 36), (26, 40), (34, 34), (37, 25), (31, 19)]             # S-curve from tail to neck
    path = []
    for i in range(len(ctrl) - 1):
        (x0, y0), (x1, y1) = ctrl[i], ctrl[i + 1]
        for t in range(12): path.append((x0 + (x1 - x0) * t / 12, y0 + (y1 - y0) * t / 12))
    n = len(path); body = ["#1d2150", "#2a2f7a", "#3b3f9a", "#4d52b8"]
    for i, (x, y) in enumerate(path):
        rad = 1.5 + 4.5 * i / n
        d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=body[min(3, 4 * i // n)])
    for i in range(0, n, 3):                                                                 # dorsal fins in cyan
        x, y = path[i]; d.polygon([(x - 1, y - 4 - i // 12), (x + 1, y - 4 - i // 12), (x, y - 7 - i // 10)], fill="#7fe0f5")
    hx, hy = 29, 12                                                                          # head
    d.polygon([(hx - 7, hy - 4), (hx - 13, hy - 12), (hx - 3, hy - 8)], fill="#7fe0f5")      # horns
    d.polygon([(hx + 1, hy - 8), (hx + 6, hy - 14), (hx + 8, hy - 6)], fill="#7fe0f5")
    d.ellipse([hx - 8, hy - 7, hx + 8, hy + 8], fill="#b9a8ff")
    d.polygon([(hx + 4, hy - 2), (hx + 16, hy + 2), (hx + 5, hy + 8)], fill="#d9ceff")       # snout
    d.line([hx + 5, hy + 4, hx + 14, hy + 4], fill=C["ink"])                                 # mouth line
    d.point((hx + 13, hy), fill=C["ink"])                                                    # nostril
    d.rectangle([hx - 2, hy - 3, hx + 2, hy + 1], fill=C["ink"]); d.rectangle([hx - 1, hy - 2, hx + 1, hy], fill=C["gold"]); d.point((hx, hy - 2), fill=C["gold2"])
    d.polygon([(hx - 8, hy + 2), (hx - 14, hy + 8), (hx - 6, hy + 6)], fill="#7fe0f5")       # whisker-mane
    for _ in range(46):                                                                      # stars inside the body
        x, y = r.randrange(2, 46), r.randrange(4, 46)
        px = im.getpixel((x, y))
        if px[3] > 0 and px[:3] != (0xb9, 0xa8, 0xff): d.point((x, y), fill=r.choice(["#ffffff", "#ffffff", C["gold"], "#c4d4ff"]))
    for (x, y) in ((44, 36), (3, 22), (42, 44), (14, 12), (20, 26)): sparkle(d, x, y)
    return outline_px(im)

for name, img in personas().items(): save(img, OUT / f"persona-{name}.png")
save(kind_automaton(), OUT / "kind-automaton.png")
save(kind_familiar(), OUT / "kind-familiar.png")
save(kind_astral(), OUT / "kind-astral.png")
print("ok art")
