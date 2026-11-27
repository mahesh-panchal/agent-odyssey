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

def boss_unbound():
    """The Unbound Astral: a sea-serpent Astral rising from dark water, its binding ring broken, unverified 'facts' floating around it."""
    import math
    im = Image.new("RGBA", (B, B), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ink, body, belly, eye = P["ink"], "#2f6f6a", "#6fb3a6", BP["fog"][4]
    pts = []
    for i in range(40):
        t = i / 39.0
        pts.append((5 + t * 31, 33 + 7 * math.sin(t * 2 * math.pi * 1.2 + .6), 3.2 + 3.2 * t))
    for x, y, r in pts: d.ellipse([x - r - 1, y - r - 1, x + r + 1, y + r + 1], fill=ink)
    for x, y, r in pts: d.ellipse([x - r, y - r, x + r, y + r], fill=body)
    for x, y, r in pts[::2]: d.ellipse([x - r * .5, y + r * .2, x + r * .5, y + r * .8], fill=belly)
    # head, jaw open, teeth
    d.ellipse([30, 14, 46, 30], fill=ink); d.ellipse([31, 15, 45, 29], fill=body)
    d.polygon([(33, 25), (46, 27), (45, 31), (34, 31)], fill=ink)
    for x in (36, 39, 42): d.polygon([(x, 26), (x + 1, 26), (x, 29)], fill="#ffffff")
    d.rectangle([35, 18, 37, 20], fill=eye); d.rectangle([41, 18, 43, 20], fill=eye)
    d.line([34, 15, 31, 11], fill=body, width=2); d.line([44, 15, 46, 11], fill=body, width=2)
    # broken binding ring behind the head
    d.arc([26, 8, 47, 29], 200, 330, fill=P["glow"], width=1); d.arc([26, 8, 47, 29], 350, 60, fill=P["glow"], width=1)
    # dark water
    for y in range(37, B):
        for x in range(B):
            if (y + (x // 3) % 2) % 5 == 0 or y > 43: d.point((x, y), fill=P["water"][2] if y > 43 else P["water"][0])
    d.rectangle([0, 44, B, B], fill=P["water"][2]); d.line([0, 43, B, 43], fill="#8fb8ea")
    speech_bubble(d, 2, 5); speech_bubble(d, 14, 14); speech_bubble(d, 3, 22)
    sparkle(d, 24, 6); sparkle(d, 20, 38)
    return im

def boss_unbound_cleared():
    """The Astral bound again: a small calm wisp inside a chalk ring on still water."""
    im = Image.new("RGBA", (B, B), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 36, B, B], fill=P["water"][0]); d.line([0, 36, B, 36], fill="#8fb8ea")
    for x in range(2, B, 7): d.line([x, 41, x + 3, 41], fill="#8fb8ea")
    d.ellipse([10, 28, 38, 42], outline="#f0ead6", width=1)                           # chalk ring
    d.ellipse([19, 14, 29, 28], fill=P["glow"], outline=P["ink"])                       # small calm Astral
    d.rectangle([22, 19, 23, 20], fill=P["ink"]); d.rectangle([26, 19, 27, 20], fill=P["ink"]); d.line([23, 24, 26, 24], fill=P["ink"])
    d.polygon([(24, 28), (21, 33), (27, 33)], fill=P["glow"])
    for x, y in ((24, 8), (24, 9), (14, 14), (34, 14), (12, 24), (36, 24)): d.point((x, y), fill=BP["glow2"])
    sparkle(d, 9, 12); sparkle(d, 40, 10)
    return im

save(boss_wall(0), OUT / "boss-wall.png")
save(boss_wall(1), OUT / "boss-wall-cracked.png")
save(boss_wall(2), OUT / "boss-wall-broken.png")
save(boss_unbound(), OUT / "boss-unbound.png")
save(boss_unbound_cleared(), OUT / "boss-unbound-cleared.png")

# ---- Party portraits and creature kinds (96x96: twice the boss size, same palette, still pixel art) ----
Q = 96
INK = "#1a1428"

def hx(c, a=255):
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (a,)

def mixc(c1, c2, t):
    a, b = hx(c1), hx(c2)
    return "#%02x%02x%02x" % tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def lite(c, t=.25): return mixc(c, "#ffffff", t)
def dark(c, t=.3): return mixc(c, "#1a1428", t)

SKIN = [("#f4cfa4", "#e0b283", "#b9835a"), ("#d49a62", "#b97a45", "#8f5a30"),
        ("#a8693a", "#8d5524", "#663a14"), ("#e8b87a", "#d09a5c", "#a8743a")]
GOLD, GOLD2 = "#e8b84a", "#fff1b8"
BRASS = ["#f0c870", "#d7a84e", "#b5873a", "#7e5a22"]

def outline_img(im, col=INK):
    src = im.copy(); sp = src.load(); px = im.load(); w, h = im.size
    for y in range(h):
        for x in range(w):
            if sp[x, y][3] == 0 and any(0 <= x + a < w and 0 <= y + b < h and sp[x + a, y + b][3] > 40
                                         for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                px[x, y] = hx(col)
    return im

def sparkle2(d, x, y, big=False):
    d.point((x, y), fill="#ffffff")
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)): d.point((x + dx, y + dy), fill=GOLD)
    if big:
        for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)): d.point((x + dx, y + dy), fill=GOLD2)

def gear(d, cx, cy, r, teeth, body, hub):
    import math
    for i in range(teeth):
        a = 2 * math.pi * i / teeth
        x, y = cx + math.cos(a) * (r + 2), cy + math.sin(a) * (r + 2)
        d.rectangle([x - 1.5, y - 1.5, x + 1.5, y + 1.5], fill=body)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=body)
    d.ellipse([cx - r + 3, cy - r + 3, cx + r - 3, cy + r - 3], outline=dark(body, .35))
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=hub)
    d.point((cx - r + 3, cy - r + 3), fill=lite(body, .5))

def eye(d, x, y, iris="#3a2a1a"):
    d.rectangle([x, y, x + 6, y + 3], fill="#fff7ee")
    d.rectangle([x + 2, y, x + 4, y + 3], fill=iris)
    d.point((x + 3, y + 1), fill=INK); d.point((x + 2, y), fill="#ffffff")
    d.line([x - 1, y - 1, x + 7, y - 1], fill=INK)

def bust(skin, hair, style, robe, trim, extra=None, glasses=False, hood_col=None):
    im = Image.new("RGBA", (Q, Q), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sl, sb, ss = SKIN[skin]
    robe_d, robe_l = dark(robe, .3), lite(robe, .18)
    if style == "long":
        d.polygon([(24, 40), (28, 14), (48, 8), (68, 14), (72, 40), (74, 84), (22, 84)], fill=hair)
    if style == "hood":
        d.polygon([(14, 70), (12, 36), (22, 14), (48, 2), (74, 14), (84, 36), (82, 70)], fill=hood_col)
        d.polygon([(14, 70), (12, 36), (22, 14), (30, 10), (22, 36), (22, 70)], fill=dark(hood_col, .3))
    d.polygon([(6, 96), (10, 74), (28, 62), (68, 62), (86, 74), (90, 96)], fill=robe)                # shoulders
    d.polygon([(6, 96), (10, 74), (22, 68), (20, 96)], fill=robe_d)
    d.polygon([(90, 96), (86, 74), (74, 68), (76, 96)], fill=robe_d)
    for (x0, y0, x1, y1) in ((34, 70, 30, 96), (62, 70, 66, 96), (48, 86, 48, 96)): d.line([x0, y0, x1, y1], fill=robe_d)
    d.line([40, 68, 36, 96], fill=robe_l); d.line([14, 76, 24, 68], fill=robe_l)
    d.line([12, 74, 28, 63], fill=trim)                                                              # shoulder trim
    d.line([84, 74, 68, 63], fill=dark(trim, .2))
    d.rectangle([41, 48, 55, 64], fill=sb); d.rectangle([41, 56, 55, 63], fill=ss)                    # neck and its shadow
    d.polygon([(33, 62), (48, 84), (63, 62), (57, 62), (48, 74), (39, 62)], fill=trim)               # collar
    d.line([39, 62, 48, 74], fill=dark(trim, .3)); d.line([48, 74, 57, 62], fill=lite(trim, .3))
    d.ellipse([28, 12, 68, 58], fill=sb)                                                             # head
    d.ellipse([28, 12, 64, 54], fill=sl)
    d.ellipse([33, 17, 49, 32], fill=lite(sl, .35))                                                  # forehead light
    d.arc([28, 12, 68, 58], 300, 90, fill=ss, width=3)                                               # jaw shade
    for ex in ((25, 31), (65, 71)):
        d.ellipse([ex[0], 32, ex[1], 45], fill=sb); d.line([ex[0] + 2, 35, ex[0] + 2, 42], fill=ss)
    eye(d, 37, 33); eye(d, 53, 33)
    d.line([37, 29, 44, 28], fill=dark(hair, .1)); d.line([53, 28, 60, 29], fill=dark(hair, .1))
    d.line([48, 36, 47, 44], fill=ss); d.line([46, 45, 50, 45], fill=ss); d.point((45, 44), fill=sb)  # nose
    d.line([43, 50, 53, 50], fill="#8a4a3a"); d.line([44, 51, 52, 51], fill="#c47a68")               # mouth
    d.point((36, 42), fill="#e89a80"); d.point((60, 42), fill="#e89a80")                              # cheeks
    if style in ("short", "long", "hood_cap"):
        d.polygon([(28, 36), (27, 22), (33, 12), (48, 7), (64, 12), (69, 22), (68, 36), (64, 27), (56, 21), (48, 19), (40, 22), (33, 27)], fill=hair)
        for (x0, y0, x1, y1) in ((36, 12, 33, 24), (44, 9, 41, 21), (52, 9, 54, 20), (60, 12, 62, 22)): d.line([x0, y0, x1, y1], fill=lite(hair, .35))
        d.rectangle([28, 30, 30, 40], fill=hair); d.rectangle([66, 30, 68, 40], fill=hair)
    if style == "hood":
        d.polygon([(26, 40), (26, 20), (34, 11), (48, 8), (62, 11), (70, 20), (70, 40), (64, 26), (56, 21), (48, 19), (40, 21), (32, 26)], fill=hood_col)
        d.line([30, 18, 38, 12], fill=lite(hood_col, .25)); d.line([58, 12, 66, 18], fill=lite(hood_col, .25))
    if style == "long":
        d.rectangle([26, 36, 31, 76], fill=hair); d.rectangle([65, 36, 70, 76], fill=hair)
        d.line([28, 40, 28, 74], fill=lite(hair, .3)); d.line([68, 40, 68, 74], fill=dark(hair, .2))
    if glasses:
        d.rectangle([35, 31, 46, 39], outline=INK); d.rectangle([50, 31, 61, 39], outline=INK); d.line([46, 34, 50, 34], fill=INK)
        d.line([36, 32, 39, 32], fill="#cfe9ff"); d.line([51, 32, 54, 32], fill="#cfe9ff")
    if extra: extra(d, im)
    return outline_img(im)

def x_quartermaster(d, im):
    d.rectangle([2, 70, 32, 94], fill="#efe3c2", outline=INK)                                       # ledger
    d.rectangle([2, 70, 6, 94], fill="#2f6b4f"); d.line([6, 70, 6, 94], fill=INK)
    for y in (75, 79, 83, 87): d.line([10, y, 28, y], fill="#9b8a60")
    d.rectangle([22, 90, 28, 94], fill="#a83232")
    for (x0, y0, x1, y1) in ((34, 64, 48, 84), (62, 64, 48, 84)): d.line([x0, y0, x1, y1], fill=GOLD, width=2)   # chain
    for t in range(1, 6):
        x = 34 + (14 * t) / 6; y = 64 + (20 * t) / 6; d.point((x, y - 2), fill=GOLD2)
    d.ellipse([42, 80, 54, 92], fill=GOLD, outline=INK); d.ellipse([45, 83, 51, 89], fill="#2f9a6f"); d.point((46, 84), fill="#ffffff")
    d.ellipse([74, 64, 90, 80], fill="#fff1b8", outline=INK); d.ellipse([78, 68, 86, 76], fill=GOLD)    # milestone beacon
    for (x, y) in ((82, 60), (92, 72), (72, 72), (82, 84)): d.point((x, y), fill=GOLD2)
    sparkle2(d, 90, 56, True)

def x_diviner(d, im):
    d.ellipse([58, 62, 94, 96], fill=BRASS[1], outline=INK)                                         # lens in a brass ring
    d.ellipse([62, 66, 90, 92], fill="#bfe6f5"); d.ellipse([66, 70, 80, 82], fill="#e8f8ff")
    d.arc([62, 66, 90, 92], 200, 340, fill="#ffffff", width=2); d.point((68, 72), fill="#ffffff")
    d.arc([62, 66, 90, 92], 20, 160, fill="#7ab8d8", width=2)
    d.polygon([(60, 92), (52, 96), (62, 96)], fill=BRASS[2])
    d.line([48, 64, 40, 70], fill="#a9b4ff")                                                         # clasp
    for (x, y) in ((8, 24), (88, 18), (10, 56), (84, 48)): sparkle2(d, x, y, True)

def x_artificer(d, im):
    d.rectangle([26, 14, 70, 22], fill=BRASS[2])                                                    # goggle strap on the brow
    for cx in (36, 60):
        d.ellipse([cx - 9, 8, cx + 9, 26], fill=BRASS[1], outline=INK); d.ellipse([cx - 6, 11, cx + 6, 23], fill="#9fd3e6")
        d.arc([cx - 6, 11, cx + 6, 23], 200, 330, fill="#ffffff", width=1)
    d.rectangle([44, 14, 52, 20], fill=BRASS[1])
    d.polygon([(26, 74), (70, 74), (68, 96), (28, 96)], fill="#8a5428")                              # leather apron
    d.polygon([(26, 74), (36, 62), (60, 62), (70, 74)], fill="#7a4a24")
    d.rectangle([36, 82, 60, 94], fill="#6a3f1c", outline=INK); d.line([36, 86, 60, 86], fill="#b9803f")
    for x in range(30, 68, 7): d.point((x, 76), fill="#c99a5a")
    gear(d, 80, 82, 9, 8, BRASS[1], INK)
    for (x, y) in ((6, 30), (88, 34), (10, 62)): sparkle2(d, x, y)

def x_archivist(d, im):
    d.ellipse([4, 72, 22, 90], outline=BRASS[1], width=3)                                           # key ring and keys
    for (x0, y0, x1, y1) in ((18, 82, 34, 92), (14, 86, 28, 96)):
        d.line([x0, y0, x1, y1], fill=BRASS[1], width=2); d.rectangle([x1 - 1, y1 - 1, x1 + 3, y1 + 3], fill=BRASS[2])
    d.rectangle([66, 72, 92, 94], fill="#efe3c2", outline=INK); d.line([66, 78, 92, 78], fill="#cdbd90")
    d.line([69, 82, 88, 82], fill="#9b8a60"); d.line([69, 86, 84, 86], fill="#9b8a60")
    d.ellipse([74, 80, 86, 92], fill="#a83232", outline=INK); d.line([78, 84, 82, 88], fill="#d85a5a"); d.line([82, 84, 78, 88], fill="#d85a5a")
    d.line([74, 94, 70, 96], fill="#a83232"); d.line([86, 94, 90, 96], fill="#a83232")
    sparkle2(d, 10, 28)

def personas():
    return {
        "quartermaster": bust(0, "#5a3a22", "short", "#2f6b4f", GOLD, x_quartermaster),
        "diviner":     bust(1, "#1a1428", "hood", "#3b3f8f", "#a9b4ff", x_diviner, hood_col="#2b2f6e"),
        "artificer":   bust(2, "#2a1a10", "short", "#b8672a", BRASS[1], x_artificer),
        "archivist":   bust(3, "#8a8a9c", "long", "#6b5a8f", "#d8cfa3", x_archivist, glasses=True),
    }

def fur(im, base, dk, lt, seed, density=.18):
    """Scatter short fur strokes over pixels of colour `base`."""
    r = random.Random(seed); px = im.load(); w, h = im.size; bb = hx(base)
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if px[x, y][:3] == bb[:3] and r.random() < density:
                c = hx(dk if r.random() < .6 else lt)
                px[x, y] = c
                if r.random() < .5 and px[x, y + 1][:3] == bb[:3]: px[x, y + 1] = c

def kind_automaton():
    im = Image.new("RGBA", (Q, Q), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    b0, b1, b2, b3 = BRASS
    d.ellipse([14, 88, 84, 95], fill=(26, 20, 40, 90))                                              # ground shadow
    for x in (18, 30, 58, 68):                                                                       # legs with joints and feet
        d.rectangle([x, 62, x + 8, 76], fill=b2); d.line([x + 1, 62, x + 1, 76], fill=b1)
        d.ellipse([x - 1, 72, x + 9, 80], fill=b1, outline=INK); d.point((x + 4, 76), fill=b3)
        d.rectangle([x + 1, 80, x + 7, 88], fill=b2); d.rectangle([x - 2, 88, x + 10, 92], fill=b3); d.line([x - 2, 88, x + 10, 88], fill=b1)
    d.rounded_rectangle([10, 36, 76, 66], radius=6, fill=b1)                                         # body
    d.rounded_rectangle([10, 36, 76, 44], radius=4, fill=b0)
    d.line([10, 56, 76, 56], fill=b2); d.line([26, 36, 26, 66], fill=b2); d.line([60, 36, 60, 66], fill=b2)
    for x in (14, 20, 32, 40, 48, 54, 66, 72):
        for y in (40, 62): d.point((x, y), fill=b3); d.point((x - 1, y - 1), fill=b0)
    d.ellipse([28, 42, 58, 64], fill=INK); d.ellipse([30, 44, 56, 62], fill="#2a2840")               # glass window on the belly
    gear(d, 43, 53, 7, 8, b1, b3); gear(d, 52, 50, 4, 6, b0, b3)
    d.arc([30, 44, 56, 62], 200, 300, fill="#9fd3e6", width=1)
    d.polygon([(70, 38), (84, 24), (90, 32), (78, 52), (72, 62)], fill=b1)                           # neck
    d.rounded_rectangle([74, 14, 94, 38], radius=4, fill=b1)                                         # head
    d.line([76, 16, 92, 16], fill=b0)
    d.polygon([(78, 14), (80, 4), (84, 14)], fill=b2); d.polygon([(86, 14), (90, 4), (92, 14)], fill=b2)   # ear plates
    d.ellipse([80, 20, 90, 30], fill=INK); d.ellipse([81, 21, 89, 29], fill="#7fe0f5"); d.ellipse([83, 22, 86, 25], fill="#ffffff")
    d.rounded_rectangle([88, 28, 96, 36], radius=2, fill=b2); d.point((93, 30), fill=INK); d.point((93, 33), fill=INK)
    d.line([82, 14, 82, 6], fill=b3); d.ellipse([80, 2, 84, 6], fill="#7fe0f5")                      # antenna
    pts = [(10, 44), (4, 40), (8, 36), (2, 32), (6, 28), (0, 24)]                                    # spring tail
    d.line(pts, fill=b2, width=3)
    d.line([30, 36, 24, 26, 18, 22], fill=b3, width=2); d.ellipse([10, 14, 24, 28], outline=b1, width=3); d.line([17, 21, 17, 28], fill=b1, width=2)   # winding key
    for (x, y, r_) in ((66, 28, 3), (62, 20, 4), (58, 11, 3)): d.ellipse([x - r_, y - r_, x + r_, y + r_], fill=(235, 240, 250, 150))  # steam
    return outline_img(im)

def kind_familiar():
    im = Image.new("RGBA", (Q, Q), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fur1, fur2, fur3, cream = "#b06a3a", "#8a4a26", "#c98a52", "#f6e2bd"
    d.ellipse([10, 88, 84, 95], fill=(26, 20, 40, 90))
    d.polygon([(18, 86), (4, 60), (6, 38), (14, 30), (18, 48), (24, 68)], fill=fur2)                 # tail
    d.polygon([(6, 38), (14, 30), (10, 44)], fill=cream)
    d.ellipse([16, 44, 62, 92], fill=fur1)                                                           # body
    d.ellipse([14, 60, 44, 92], fill=fur3)                                                           # haunch
    d.polygon([(52, 44), (66, 52), (68, 80), (56, 92), (50, 70)], fill=fur1)
    d.polygon([(54, 54), (66, 58), (62, 84), (54, 78)], fill=cream)                                  # chest tuft
    d.rectangle([50, 74, 60, 92], fill=fur2); d.rectangle([46, 88, 62, 94], fill=cream)              # front leg and paw
    d.rectangle([22, 84, 40, 94], fill=cream)                                                        # back paw
    d.ellipse([46, 14, 86, 54], fill=fur1)                                                           # head
    d.polygon([(76, 30), (96, 38), (80, 52)], fill=cream); d.polygon([(76, 30), (96, 38), (94, 42), (80, 38)], fill=fur3)   # muzzle
    d.polygon([(48, 22), (46, 2), (62, 16)], fill=fur2); d.polygon([(52, 18), (50, 8), (58, 16)], fill="#e8a0a0")      # ears
    d.polygon([(66, 14), (78, 0), (84, 18)], fill=fur2); d.polygon([(70, 14), (78, 6), (80, 16)], fill="#e8a0a0")
    d.ellipse([58, 26, 70, 36], fill="#fff7ee"); d.ellipse([62, 27, 69, 36], fill="#3a2a1a"); d.point((65, 29), fill="#ffffff")
    d.line([56, 24, 72, 22], fill=fur2, width=2)
    d.ellipse([92, 36, 97, 41], fill=INK); d.line([86, 46, 94, 44], fill=INK)                        # nose and mouth
    d.rectangle([52, 46, 80, 53], fill="#3b6fb6"); d.line([52, 47, 80, 47], fill="#6a9ad8")          # collar
    d.ellipse([62, 52, 72, 62], fill=GOLD, outline=INK); d.line([67, 54, 67, 60], fill=INK); d.line([64, 57, 70, 57], fill=INK)   # rune tag
    fur(im, fur1, fur2, fur3, 5); fur(im, fur3, fur1, "#e0a870", 6, .12)
    for (x, y, x2, y2) in ((28, 66, 32, 74), (32, 66, 36, 74), (36, 66, 40, 74)):                    # glowing rune on the flank
        d.line([x, y, x2, y2], fill="#7fe0f5"); d.point((x, y), fill="#ffffff")
    for (x, y) in ((6, 12), (90, 70), (2, 82), (84, 6)): sparkle2(d, x, y)
    return outline_img(im)

def kind_astral():
    """A starry, winged serpent of light with a dragon's head. Shaded from a path, so the form reads as one creature."""
    import numpy as np
    r = random.Random(21)
    ctrl = np.array([(8, 86), (14, 70), (30, 66), (44, 78), (60, 72), (72, 54), (64, 36), (56, 28)], float)
    def spline(c, n=14):
        out = []
        for i in range(len(c) - 1):
            p0 = c[max(i - 1, 0)]; p1 = c[i]; p2 = c[i + 1]; p3 = c[min(i + 2, len(c) - 1)]
            for t in np.linspace(0, 1, n, endpoint=False):
                out.append(.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
        out.append(c[-1]); return np.array(out)
    path = spline(ctrl); n = len(path); rad = 4 + 9 * (np.linspace(0, 1, n) ** .8)
    im = Image.new("RGBA", (Q, Q), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    bx, by = path[int(n * .30)]                                                                      # wings rise from the back into the empty upper left, clear of the head
    for ox, oy, sc, mem, rib in ((-3, 4, .75, (226, 150, 110, 235), (160, 88, 70, 255)), (3, 2, .95, (255, 214, 140, 245), (200, 120, 70, 255))):
        x0, y0 = bx + ox, by + oy - 4
        P = lambda dx, dy: (x0 + dx * sc, y0 + dy * sc)
        tips = [P(-26, -50), P(-9, -52), P(5, -38)]
        notch = [P(-22, -30), P(-3, -33)]
        edge = [P(0, 0), P(-30, -22), tips[0], notch[0], tips[1], notch[1], tips[2]]
        d.polygon(edge, fill=mem)
        for t in tips + [P(-30, -22)]: d.line([P(0, 0), t], fill=rib, width=2)
    px = im.load(); ramp = ["#141844", "#1d2260", "#2a3290", "#3b46b8", "#5a6fe0", "#8aa0ff", "#c4d4ff"]
    ys, xs = np.mgrid[0:Q, 0:Q]
    dist = np.full((Q, Q), 1e9); idx = np.zeros((Q, Q), int)
    for i, (x, y) in enumerate(path):
        dd = np.hypot(xs - x, ys - y); m = dd < dist; dist[m] = dd[m]; idx[m] = i
    for y in range(Q):
        for x in range(Q):
            i = idx[y, x]
            if dist[y, x] <= rad[i]:
                f = dist[y, x] / rad[i]; up = (path[i][1] - y) / rad[i]
                k = 2 + int(2 * (1 - f) + 2.2 * max(up, 0) - 1.4 * max(-up, 0))
                if i % 8 == 0: k -= 1                                                                # segment rings
                elif r.random() < .05: k += 1                                                        # faint sparkle
                if up < -.55: k = 5 if (x // 3) % 2 else 6                                           # pale belly plates
                px[x, y] = hx(ramp[max(0, min(6, k))])
    d = ImageDraw.Draw(im)
    for i in range(6, n - 6, 5):                                                                     # dorsal fins
        x, y = path[i]; nx, ny = path[i + 1] - path[i - 1]; L = max((nx * nx + ny * ny) ** .5, 1)
        ux, uy = ny / L, -nx / L
        if uy > 0: ux, uy = -ux, -uy
        h = 4 + rad[i] * .6
        d.polygon([(x + ux * rad[i] - nx / L * 2, y + uy * rad[i] - ny / L * 2), (x + ux * (rad[i] + h), y + uy * (rad[i] + h)),
                   (x + ux * rad[i] + nx / L * 2, y + uy * rad[i] + ny / L * 2)], fill="#7fe0f5")
    hx_, hy_ = path[-1]                                                                              # head, drawn back to front, shaded like the body (no inner outlines)
    d.polygon([(hx_ - 12, hy_ - 4), (hx_ - 24, hy_ - 14), (hx_ - 18, hy_ + 6)], fill="#ff9ad8")   # mane
    d.polygon([(hx_ - 12, hy_ + 6), (hx_ - 26, hy_ + 10), (hx_ - 12, hy_ + 14)], fill="#7fe0f5")  # cheek frill
    d.polygon([(hx_ - 4, hy_ - 10), (hx_ - 12, hy_ - 28), (hx_ + 2, hy_ - 12)], fill="#e4ecff")   # horns
    d.polygon([(hx_ + 4, hy_ - 10), (hx_ + 8, hy_ - 26), (hx_ + 12, hy_ - 8)], fill="#e4ecff")
    d.ellipse([hx_ - 16, hy_ - 15, hx_ + 14, hy_ + 15], fill="#b9a8ff")                  # skull
    d.ellipse([hx_ - 13, hy_ - 13, hx_ + 4, hy_ - 4], fill="#d9ceff")                                 # skull highlight
    d.polygon([(hx_ + 4, hy_ + 5), (hx_ + 27, hy_ + 5), (hx_ + 22, hy_ + 14), (hx_ + 6, hy_ + 15)], fill="#8a78e0")   # lower jaw
    d.polygon([(hx_ + 4, hy_ - 9), (hx_ + 27, hy_ - 5), (hx_ + 31, hy_ + 1), (hx_ + 28, hy_ + 5), (hx_ + 4, hy_ + 5)], fill="#d9ceff")  # upper snout
    d.line([hx_ + 5, hy_ + 5, hx_ + 28, hy_ + 5], fill="#5a48b0", width=1)                           # mouth line (dark violet)
    for fx in (hx_ + 12, hx_ + 21): d.polygon([(fx, hy_ + 5), (fx + 4, hy_ + 5), (fx + 1.5, hy_ + 11)], fill="#ffffff")  # two fangs
    d.point((hx_ + 26, hy_ - 2), fill="#5a48b0"); d.point((hx_ + 27, hy_ - 2), fill="#5a48b0")                    # nostril
    d.line([hx_ - 6, hy_ - 9, hx_ + 8, hy_ - 7], fill="#8a78e0", width=2)                                   # brow ridge
    d.ellipse([hx_ - 2, hy_ - 6, hx_ + 8, hy_ + 2], fill=INK); d.ellipse([hx_, hy_ - 5, hx_ + 7, hy_ + 1], fill=GOLD)
    d.line([hx_ + 3, hy_ - 5, hx_ + 3, hy_ + 1], fill=INK); d.point((hx_ + 1, hy_ - 4), fill=GOLD2)   # eye with slit pupil
    for _ in range(70):                                                                              # stars in the body
        x, y = r.randrange(2, Q - 2), r.randrange(2, Q - 2)
        if im.getpixel((x, y))[3] == 255 and dist[y, x] <= rad[idx[y, x]] - 1: d.point((x, y), fill=r.choice(["#ffffff", "#ffffff", GOLD, "#c4d4ff"]))
    for (x, y) in ((6, 52), (88, 82), (20, 20), (90, 20), (40, 90)): sparkle2(d, x, y, True)
    return outline_img(im)

for name, img in personas().items(): save(img, OUT / f"persona-{name}.png")
save(kind_automaton(), OUT / "kind-automaton.png")
save(kind_familiar(), OUT / "kind-familiar.png")
save(kind_astral(), OUT / "kind-astral.png")
print("ok art")
