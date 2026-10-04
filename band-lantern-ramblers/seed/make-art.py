#!/usr/bin/env python3
"""Draw the Lantern Ramblers artwork into art/ as SVG: psychedelic gig posters, light-show 'photos' and member
portraits (abstract, with initials; no real people). Everything is generated, so it is free to reuse."""
import math, os, random, json
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "art")
os.makedirs(OUT, exist_ok=True)
PALS = [["#2a1446", "#ff5e7e", "#ffb347", "#3ad6c4", "#fff3d6"], ["#10233f", "#8b6cff", "#ff8a5b", "#ffd166", "#f6efe4"],
        ["#1d0f2e", "#e83f6f", "#ffbf00", "#2ec4b6", "#fdf0d5"], ["#0f2a2a", "#ff6f59", "#f7c548", "#9b5de5", "#fef6e4"],
        ["#2b0f1f", "#ff9f1c", "#ff4d6d", "#4cc9f0", "#fff1e6"], ["#13132b", "#f15bb5", "#fee440", "#00bbf9", "#f6efe4"]]
GRAIN = '<filter id="g" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 .5 0 0 0 0 .45 0 0 0 0 .4 0 0 0 .5 0"/></filter>'

def wave_band(y, amp, freq, phase, w, h, col, op=1):
    pts = " ".join(f"L{x},{y + amp * math.sin(x / w * freq * 2 * math.pi + phase):.1f}" for x in range(0, w + 20, 20))
    return f'<path d="M0,{h} L0,{y:.1f} {pts} L{w},{h} Z" fill="{col}" opacity="{op}"/>'

def poster(name, seed, w=900, h=1200, style=None):
    r = random.Random(seed); p = PALS[seed % len(PALS)]; bg, a, b, c, ink = p
    style = style or ["rings", "sun", "waves", "spiral", "bloom"][seed % 5]
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><defs>{GRAIN}'
         f'<radialGradient id="glow" cx=".5" cy=".42" r=".6"><stop offset="0" stop-color="{b}" stop-opacity=".55"/><stop offset="1" stop-color="{bg}" stop-opacity="0"/></radialGradient></defs>',
         f'<rect width="{w}" height="{h}" fill="{bg}"/><rect width="{w}" height="{h}" fill="url(#glow)"/>']
    cx, cy = w / 2, h * 0.42
    if style == "rings":
        cols = [a, b, c, ink, a, b, c]
        for i in range(14, 0, -1):
            s.append(f'<circle cx="{cx}" cy="{cy}" r="{i * 38}" fill="{cols[i % len(cols)]}" opacity="{0.25 + 0.05 * (14 - i):.2f}"/>')
    elif style == "sun":
        for i in range(36):
            ang = i / 36 * 2 * math.pi
            x1, y1 = cx + math.cos(ang) * 120, cy + math.sin(ang) * 120
            x2, y2 = cx + math.cos(ang + 0.08) * 900, cy + math.sin(ang + 0.08) * 900
            x3, y3 = cx + math.cos(ang - 0.08) * 900, cy + math.sin(ang - 0.08) * 900
            s.append(f'<path d="M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f} L{x3:.0f},{y3:.0f} Z" fill="{[a, b, c][i % 3]}" opacity=".55"/>')
        s.append(f'<circle cx="{cx}" cy="{cy}" r="170" fill="{b}"/><circle cx="{cx}" cy="{cy}" r="120" fill="{ink}" opacity=".9"/>')
    elif style == "waves":
        for i, col in enumerate([a, b, c, ink, a, b, c, a]):
            s.append(wave_band(h * 0.18 + i * 120, 40 + 10 * i, 1.5 + r.random(), r.random() * 6, w, h, col, 0.85))
    elif style == "spiral":
        for i in range(420):
            t = i / 18; rad = 8 + i * 1.25
            x, y = cx + math.cos(t) * rad, cy + math.sin(t) * rad
            s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{4 + i / 40:.1f}" fill="{[a, b, c, ink][i % 4]}" opacity=".85"/>')
    else:  # bloom
        for k, col in enumerate([a, b, c]):
            for i in range(12):
                ang = i / 12 * 2 * math.pi + k * 0.26
                x, y = cx + math.cos(ang) * (230 - k * 70), cy + math.sin(ang) * (230 - k * 70)
                s.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{120 - k * 30}" ry="{50 - k * 10}" fill="{col}" opacity=".7" transform="rotate({math.degrees(ang):.0f} {x:.0f} {y:.0f})"/>')
        s.append(f'<circle cx="{cx}" cy="{cy}" r="70" fill="{ink}"/>')
    for _ in range(40):
        s.append(f'<circle cx="{r.uniform(0, w):.0f}" cy="{r.uniform(0, h):.0f}" r="{r.uniform(1, 3.5):.1f}" fill="{ink}" opacity="{r.uniform(.3, .8):.2f}"/>')
    s.append(wave_band(h * 0.8, 18, 2, seed, w, h, bg, 0.92))
    s.append(f'<rect width="{w}" height="{h}" filter="url(#g)" opacity=".45"/></svg>')
    open(os.path.join(OUT, name + ".svg"), "w").write("".join(s))

def portrait(name, initials, seed):
    r = random.Random(seed); bg, a, b, c, ink = PALS[seed % len(PALS)]
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1000" width="800" height="1000"><defs>{GRAIN}'
         f'<linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset=".55" stop-color="{b}"/><stop offset="1" stop-color="{c}"/></linearGradient></defs>',
         f'<rect width="800" height="1000" fill="{bg}"/>']
    for i in range(9, 0, -1):
        s.append(f'<circle cx="400" cy="460" r="{i * 52}" fill="none" stroke="url(#lg)" stroke-width="{10 + i}" opacity="{0.15 + i * 0.06:.2f}"/>')
    s.append(f'<circle cx="400" cy="460" r="190" fill="url(#lg)"/>')
    s.append(f'<text x="400" y="525" font-family="Georgia, \'Times New Roman\', serif" font-size="170" font-style="italic" text-anchor="middle" fill="{bg}">{initials}</text>')
    s.append(wave_band(870, 22, 1.6, seed, 800, 1000, a, 0.9))
    s.append(f'<rect width="800" height="1000" filter="url(#g)" opacity=".4"/></svg>')
    open(os.path.join(OUT, name + ".svg"), "w").write("".join(s))

spec = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "art.json")))
for i, n in enumerate(spec["posters"]): poster(n, i + 3)
for i, (n, ini) in enumerate(spec["portraits"]): portrait(n, ini, i + 11)
print("wrote", len(os.listdir(OUT)), "SVGs to", OUT)
