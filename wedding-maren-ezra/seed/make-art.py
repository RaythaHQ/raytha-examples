#!/usr/bin/env python3
"""Draw the illustrated 'film photos' for the Maren & Ezra wedding site into art/ as SVG.
Every image is generated (layered landscapes with film grain), so it is free to reuse. No people's photos."""
import math, os, random
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "art")
os.makedirs(OUT, exist_ok=True)

def ridge(rnd, w, h, base, amp, n=9, rough=0.35):
    pts, step = [], w / n
    y = base
    for i in range(n + 1):
        y = base - amp * (0.5 + 0.5 * math.sin(i * rnd.uniform(0.6, 1.3) + rnd.random() * 6)) - rnd.uniform(-rough, rough) * amp * 0.4
        pts.append((i * step, y))
    # smooth with quadratic curves
    d = f"M0,{h} L0,{pts[0][1]:.1f} "
    for i in range(1, len(pts)):
        mx, my = (pts[i - 1][0] + pts[i][0]) / 2, (pts[i - 1][1] + pts[i][1]) / 2
        d += f"Q{pts[i-1][0]:.1f},{pts[i-1][1]:.1f} {mx:.1f},{my:.1f} "
    d += f"L{w},{pts[-1][1]:.1f} L{w},{h} Z"
    return d, pts

def peaks(rnd, w, h, base, amp, n=6):
    d = f"M0,{h} L0,{base} "
    x = 0
    while x < w:
        px = x + rnd.uniform(w / n * 0.4, w / n * 0.8); py = base - rnd.uniform(amp * 0.5, amp)
        nx = px + rnd.uniform(w / n * 0.4, w / n * 0.8)
        d += f"L{px:.0f},{py:.0f} L{nx:.0f},{base - rnd.uniform(0, amp*0.25):.0f} "
        x = nx
    return d + f"L{w},{h} Z"

def tree_round(x, y, s, c):
    return (f'<rect x="{x-s*0.06:.1f}" y="{y-s*0.5:.1f}" width="{s*0.12:.1f}" height="{s*0.5:.1f}" fill="{c}"/>'
            f'<circle cx="{x:.1f}" cy="{y-s*0.75:.1f}" r="{s*0.42:.1f}" fill="{c}"/>')

def tree_pine(x, y, s, c):
    return f'<path d="M{x:.1f},{y-s*1.6:.1f} L{x+s*0.38:.1f},{y:.1f} L{x-s*0.38:.1f},{y:.1f} Z" fill="{c}"/>'

def scene(name, seed, w=1200, h=1500, sky=("#f6c58f", "#f19c79", "#7d6b91"), sun=None, moon=False, stars=False,
          layers=(), water=None, trees=None, skyline=None, flowers=None, mountains=None, haze="#ffffff", extra=""):
    rnd = random.Random(seed)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
         '<defs>',
         f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">' + "".join(
             f'<stop offset="{i/(len(sky)-1):.2f}" stop-color="{c}"/>' for i, c in enumerate(reversed(sky))) + '</linearGradient>',
         '<radialGradient id="glow"><stop offset="0" stop-color="#fff6dc" stop-opacity=".95"/><stop offset=".25" stop-color="#ffe7b0" stop-opacity=".5"/><stop offset="1" stop-color="#ffd59a" stop-opacity="0"/></radialGradient>',
         '<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#1b120c" stop-opacity=".45"/></radialGradient>',
         '<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 .5  0 0 0 0 .45  0 0 0 0 .4  0 0 0 .55 0"/></filter>',
         '</defs>', f'<rect width="{w}" height="{h}" fill="url(#sky)"/>']
    if stars:
        for _ in range(140):
            s.append(f'<circle cx="{rnd.uniform(0,w):.0f}" cy="{rnd.uniform(0,h*0.55):.0f}" r="{rnd.uniform(0.8,2.6):.1f}" fill="#fff" opacity="{rnd.uniform(.3,.95):.2f}"/>')
    if sun:
        sx, sy, sr = sun
        s.append(f'<circle cx="{sx}" cy="{sy}" r="{sr*4}" fill="url(#glow)"/>')
        s.append(f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="{"#f4efe0" if moon else "#fff3d6"}"/>')
    if mountains:
        for i, (base, amp, col) in enumerate(mountains):
            s.append(f'<path d="{peaks(rnd, w, h, base, amp)}" fill="{col}"/>')
    if skyline:
        base, col, win = skyline
        x = 0
        while x < w:
            bw = rnd.uniform(60, 150); bh = rnd.uniform(160, 520)
            s.append(f'<rect x="{x:.0f}" y="{base-bh:.0f}" width="{bw:.0f}" height="{bh+400:.0f}" fill="{col}"/>')
            for yy in range(int(base - bh + 20), int(base), 34):
                for xx in range(int(x + 12), int(x + bw - 16), 26):
                    if rnd.random() < 0.33:
                        s.append(f'<rect x="{xx}" y="{yy}" width="12" height="16" fill="{win}" opacity="{rnd.uniform(.5,1):.2f}"/>')
            x += bw + rnd.uniform(4, 18)
    for (base, amp, col) in layers:
        d, pts = ridge(rnd, w, h, base, amp)
        s.append(f'<path d="{d}" fill="{col}"/>')
        s.append(f'<rect width="{w}" height="{h}" fill="{haze}" opacity="0.035"/>')
    if water:
        top, col, shine = water
        s.append(f'<rect x="0" y="{top}" width="{w}" height="{h-top}" fill="{col}"/>')
        for i in range(60):
            y = rnd.uniform(top + 8, h)
            ww = rnd.uniform(40, 260) * (0.4 + (y - top) / (h - top))
            cx = (sun[0] if sun else w / 2) + rnd.gauss(0, 120)
            s.append(f'<rect x="{cx-ww/2:.0f}" y="{y:.0f}" width="{ww:.0f}" height="{rnd.uniform(2,5):.1f}" rx="2" fill="{shine}" opacity="{rnd.uniform(.25,.7):.2f}"/>')
    if trees:
        kind, rows = trees
        for (y0, size, col, count) in rows:
            for i in range(count):
                x = (i + 0.5) * w / count + rnd.uniform(-20, 20)
                yy = y0 + rnd.uniform(-10, 10)
                sz = size * rnd.uniform(0.85, 1.15)
                s.append(tree_pine(x, yy, sz, col) if kind == "pine" else tree_round(x, yy, sz, col))
    if flowers:
        y0, cols = flowers
        for _ in range(420):
            y = rnd.uniform(y0, h); r = 2 + (y - y0) / (h - y0) * 9
            s.append(f'<circle cx="{rnd.uniform(0,w):.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{rnd.choice(cols)}" opacity="{rnd.uniform(.6,1):.2f}"/>')
    s.append(extra)
    s.append(f'<rect width="{w}" height="{h}" fill="url(#vig)"/>')
    s.append(f'<rect width="{w}" height="{h}" filter="url(#grain)" opacity=".5"/>')
    s.append('</svg>')
    open(os.path.join(OUT, name + ".svg"), "w").write("\n".join(s))

# Story chapters
scene("story-library", 2, sky=("#2b3350", "#3d4466", "#6d6b8a"), sun=(880, 260, 44), moon=True, stars=True,
      skyline=(1180, "#1f2436", "#ffd88a"), layers=[(1380, 40, "#171a28")])
scene("story-coast", 3, sky=("#cfe3e6", "#e9d6c4", "#f3c2a3"), sun=(300, 520, 60),
      layers=[(700, 260, "#8a8f86"), (760, 140, "#6c7469")], water=(840, "#5e8a96", "#e9f1ef"))
scene("story-rooftop", 4, sky=("#f7c59f", "#e98a75", "#6a5a86"), sun=(600, 900, 90),
      skyline=(1250, "#3a2f45", "#ffcf7a"), layers=[(1420, 20, "#241c2c")])
scene("story-meadow", 5, sky=("#d8ecf0", "#f6efd8"), sun=(950, 320, 55),
      layers=[(860, 100, "#b8c58f"), (980, 80, "#93a86b"), (1100, 60, "#73904f")], flowers=(1050, ["#f4d35e", "#ffffff", "#e9a3a3", "#f28c6b"]))
scene("story-lake-proposal", 6, sky=("#f9d9b7", "#efb8a4", "#9d9ab8"), sun=(600, 760, 64),
      mountains=[(800, 420, "#8a86a3"), (860, 300, "#6f6b8c")], water=(880, "#7c87a8", "#ffe6c9"),
      trees=("pine", [(890, 90, "#3e4060", 22)]))
scene("story-orchard", 7, sky=("#fde4b9", "#f8c48e", "#e79a72"), sun=(300, 560, 58),
      layers=[(820, 90, "#97875c"), (960, 70, "#6f7446")], trees=("round", [(900, 80, "#55603a", 9), (1120, 140, "#39452a", 5)]))
# Gallery
G = [
 ("gallery-first-snow", 11, dict(sky=("#dfe7ee", "#c7d3df", "#9fb1c4"), mountains=[(820, 460, "#e8eef4"), (900, 300, "#c9d5e0")], trees=("pine", [(1000, 120, "#4a5a63", 14), (1250, 170, "#33424a", 9)]), layers=[(1350, 30, "#f4f7fa")])),
 ("gallery-desert-road", 12, dict(sky=("#f7d4a8", "#f0a986", "#c98b8b"), sun=(900, 680, 70), layers=[(860, 160, "#c7865b"), (980, 70, "#a96a48"), (1180, 30, "#e0b48a")])),
 ("gallery-night-tent", 13, dict(sky=("#0f1530", "#1d2650", "#3a3f6b"), stars=True, sun=(240, 300, 30), moon=True, mountains=[(1000, 380, "#262a48")], trees=("pine", [(1150, 160, "#151832", 12)]), extra='<path d="M520,1260 L700,1000 L880,1260 Z" fill="#f2b45a"/><path d="M700,1000 L740,1260 L660,1260 Z" fill="#c9833a"/>')),
 ("gallery-autumn-hills", 14, dict(sky=("#f3e3c8", "#e7c9a5"), layers=[(760, 140, "#d39a5f"), (880, 110, "#bf6e3f"), (1010, 90, "#9b4f2e"), (1160, 60, "#6e3a24")], trees=("round", [(1040, 70, "#c7643a", 14)]))),
 ("gallery-beach-sunset", 15, dict(sky=("#ffd29e", "#f79c86", "#b77a9b", "#5f5c8d"), sun=(600, 860, 80), water=(880, "#6d6a9a", "#ffd9b0"), layers=[(1330, 20, "#e6c39c")])),
 ("gallery-vineyard", 16, dict(sky=("#e9f0e4", "#f6eccd"), sun=(1000, 260, 50), layers=[(760, 120, "#a9b98a"), (900, 90, "#86a067")], trees=("round", [(980, 40, "#5d7a44", 24), (1080, 55, "#4c6838", 20), (1220, 75, "#3b5530", 16), (1400, 95, "#2d4325", 12)]))),
 ("gallery-river-bridge", 17, dict(sky=("#cfdde6", "#e9e4da"), layers=[(780, 120, "#8fa39a"), (860, 60, "#6e8479")], water=(900, "#5b7d86", "#e3eeee"), extra='<path d="M0,820 Q600,560 1200,820" stroke="#3b3f45" stroke-width="16" fill="none"/>' + "".join(f'<rect x="{x}" y="{820-int(260*(1-((x-600)/600)**2))}" width="6" height="{int(260*(1-((x-600)/600)**2))}" fill="#3b3f45"/>' for x in range(60, 1200, 90)))),
 ("gallery-wildflowers", 18, dict(sky=("#cfe6ef", "#f4f1e3"), sun=(260, 300, 46), layers=[(820, 70, "#a3b97f"), (940, 50, "#87a463")], flowers=(900, ["#ffffff", "#f4c95d", "#c86b8a", "#8a74c9", "#f08a5d"]))),
 ("gallery-city-rain", 19, dict(sky=("#3b4258", "#56607a", "#8a8fa3"), skyline=(1100, "#262b3b", "#ffd17a"), water=(1100, "#2d3245", "#ffd17a"))),
 ("gallery-fog-forest", 20, dict(sky=("#e5e8e3", "#cfd6cf"), trees=("pine", [(760, 200, "#b8c2b9", 9), (980, 260, "#8c9a8f", 8), (1250, 330, "#5f6f63", 6), (1560, 420, "#3a4a3f", 5)]), haze="#ffffff")),
 ("gallery-harbor-morning", 21, dict(sky=("#f9e0c7", "#f3c9b0", "#bfc7d6"), sun=(850, 600, 52), layers=[(720, 80, "#a7a9b8")], water=(760, "#8fa2b6", "#fff1dc"), extra='<path d="M300,1040 h220 l-30,46 h-170 z" fill="#2f3443"/><rect x="400" y="860" width="6" height="180" fill="#2f3443"/><path d="M406,870 L500,1020 L406,1020 z" fill="#f4efe6"/>')),
 ("gallery-blue-hour-lake", 22, dict(sky=("#1f2a4d", "#3a4f80", "#8aa0c8"), sun=(900, 380, 26), moon=True, stars=True, mountains=[(860, 360, "#29355a")], water=(900, "#26335a", "#cbd8f0"), trees=("pine", [(910, 120, "#141c36", 18)]))),
]
for name, seed, kw in G: scene(name, seed, **kw)
print("wrote", len(os.listdir(OUT)), "SVGs to", OUT)
