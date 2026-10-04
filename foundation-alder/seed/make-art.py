#!/usr/bin/env python3
"""Draw the impact story illustrations into art/ (SVG): layered hills, the river and a motif for each story.
Repeatable and license-free. Run: python3 make-art.py"""
import math, os, random
W, H = 1600, 1000
PAL = {"flood": ("#e9dfcc", "#2f6f8f", "#1d4a5e", "#b5453a"), "marsh": ("#e8e4cf", "#5d7d4a", "#2f4d36", "#2f6f8f"),
       "books": ("#efe3d3", "#7a5aa6", "#3d2b5a", "#c8662b"), "trades": ("#ece2cf", "#3f7d4e", "#22402b", "#c8662b"),
       "salmon": ("#e6e3d6", "#2f6f8f", "#1b3b4a", "#d0573f"), "homes": ("#f0e2cf", "#c8662b", "#5a2d17", "#2f6f8f")}

def hills(r, sky, mid, deep):
    out = []
    for k, (base, amp, col, op) in enumerate([(560, 70, mid, .45), (640, 60, mid, .75), (730, 50, deep, .9)]):
        ph = r.random() * 6
        pts = " ".join(f"{x},{base + amp * math.sin(x / (260 - k * 40) + ph) + 18 * math.sin(x / 70 + ph * 2):.0f}" for x in range(0, W + 40, 40))
        out.append(f'<polygon points="0,{H} {pts} {W},{H}" fill="{col}" opacity="{op}"/>')
    return out

def motif(name, r, mid, deep, acc):
    o = []
    if name == "flood":
        for i in range(70):
            x = r.randint(0, W); y = r.randint(0, 520)
            o.append(f'<line x1="{x}" y1="{y}" x2="{x - 18}" y2="{y + 60}" stroke="{deep}" stroke-width="4" opacity=".35" stroke-linecap="round"/>')
        o.append(f'<path d="M0 820 C300 780 500 860 800 820 S1300 780 1600 820 V1000 H0Z" fill="{mid}" opacity=".9"/>')
        for i in range(5):
            x = 260 + i * 260; o.append(f'<g transform="translate({x} 760)"><rect x="-50" y="-70" width="100" height="90" fill="#f6f1e7"/><path d="M-62 -66 L0 -118 L62 -66Z" fill="{acc}"/><rect x="-14" y="-30" width="28" height="50" fill="{deep}"/></g>')
    elif name == "marsh":
        for i in range(160):
            x = r.randint(0, W); h = r.randint(60, 190); y = r.randint(760, 980)
            o.append(f'<path d="M{x} {y} q {r.randint(-20, 20)} {-h / 2} {r.randint(-30, 30)} {-h}" stroke="{deep}" stroke-width="5" fill="none" opacity=".75" stroke-linecap="round"/>')
        for i in range(6):
            x, y = r.randint(200, 1400), r.randint(140, 400)
            o.append(f'<path d="M{x} {y} q 22 -18 44 0 q 22 -18 44 0" stroke="{deep}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    elif name == "books":
        x = 340
        for i in range(11):
            w = r.randint(60, 110); h = r.randint(260, 400); col = [mid, acc, deep, "#e0b04a"][i % 4]
            o.append(f'<rect x="{x}" y="{900 - h}" width="{w}" height="{h}" rx="8" fill="{col}"/><rect x="{x + 12}" y="{930 - h}" width="{w - 24}" height="10" fill="#f6f1e7" opacity=".7"/>')
            x += w + 10
    elif name == "trades":
        for i in range(7):
            x = 220 + i * 180; o.append(f'<rect x="{x}" y="380" width="26" height="600" fill="{deep}"/>')
        for j in range(4):
            y = 420 + j * 140; o.append(f'<rect x="200" y="{y}" width="1230" height="22" fill="{acc}"/>')
        o.append(f'<path d="M1300 120 L1300 380 M1300 140 L900 140 L900 260" stroke="{deep}" stroke-width="14" fill="none"/>')
    elif name == "salmon":
        o.append(f'<path d="M-20 760 C300 700 520 860 820 780 S1300 690 1620 760 V1000 H-20Z" fill="{mid}"/>')
        for i in range(9):
            x, y, s = r.randint(150, 1450), r.randint(800, 950), r.uniform(.7, 1.3)
            o.append(f'<g transform="translate({x} {y}) scale({s:.2f}) rotate({r.randint(-15, 15)})"><path d="M-60 0 C-30 -28 30 -28 52 0 C30 28 -30 28 -60 0Z" fill="{acc}"/><path d="M52 0 L84 -22 L80 22Z" fill="{acc}"/><circle cx="-38" cy="-4" r="4" fill="#fff"/></g>')
    elif name == "homes":
        x = 120
        for i in range(8):
            w = r.randint(140, 190); h = r.randint(220, 380); col = [mid, deep, acc, "#e0b04a"][i % 4]
            o.append(f'<rect x="{x}" y="{900 - h}" width="{w}" height="{h}" fill="{col}"/><path d="M{x - 10} {900 - h} L{x + w / 2} {840 - h} L{x + w + 10} {900 - h}Z" fill="{deep}"/>')
            for yy in range(900 - h + 30, 840, 70):
                for xx in (x + 25, x + w - 55):
                    o.append(f'<rect x="{xx}" y="{yy}" width="30" height="36" fill="#f6e7b0" opacity=".9"/>')
            x += w + 14
    return o

here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "art"), exist_ok=True)
for name, (sky, mid, deep, acc) in PAL.items():
    r = random.Random(name)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">', f'<rect width="{W}" height="{H}" fill="{sky}"/>',
           f'<circle cx="{r.randint(1000, 1350)}" cy="{r.randint(220, 320)}" r="{r.randint(110, 150)}" fill="{acc}" opacity=".85"/>']
    out += hills(r, sky, mid, deep)
    out.append(f'<path d="M{r.randint(500, 900)} 600 C 700 720 1100 760 900 1000" stroke="#f6f1e7" stroke-width="34" fill="none" opacity=".55"/>')
    out += motif(name, r, mid, deep, acc)
    out.append('</svg>')
    open(os.path.join(here, "art", name + ".svg"), "w").write("\n".join(out))
print(f"wrote {len(PAL)} images to art/")
