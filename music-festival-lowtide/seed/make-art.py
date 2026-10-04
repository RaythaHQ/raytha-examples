#!/usr/bin/env python3
"""Draw a square poster-style image for every artist in artists.jsonl into art/ (SVG).
Shapes and colours come from the artist's name and genre, so the files are small, repeatable and license-free.
Run: python3 make-art.py"""
import hashlib, json, math, os, random

PAL = {  # background, deep, accent 1, accent 2, light
    "indie": ("#ffb347", "#3b1f5c", "#ff6b4a", "#1fb5a8", "#fff3dc"),
    "rock": ("#1b2440", "#0b1020", "#ff6b4a", "#ffb347", "#f4ead8"),
    "pop": ("#ff8fb1", "#3a1d6e", "#ffd166", "#5ee6d0", "#fff4f8"),
    "electronic": ("#0f2b3d", "#06121c", "#1fb5a8", "#b69cff", "#d9fff8"),
    "hip_hop": ("#ffd166", "#1d1d1d", "#ff6b4a", "#3a86ff", "#fffaf0"),
    "soul": ("#7a2e3a", "#2a0f16", "#ffb347", "#ff8fb1", "#ffeedd"),
    "folk": ("#cfe3d2", "#22433a", "#e08a4f", "#5d8f7a", "#fbf7ee"),
}
S = 1200

def art(slug, genre):
    r = random.Random(int(hashlib.md5(slug.encode()).hexdigest()[:8], 16))
    bg, deep, a1, a2, lt = PAL[genre]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">',
           f'<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{bg}"/><stop offset="1" stop-color="{deep}"/></linearGradient>'
           f'<filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .35 0"/></filter></defs>',
           f'<rect width="{S}" height="{S}" fill="url(#g)"/>']
    style = r.choice(["sun", "rings", "bars", "grid"])
    cx, cy = r.randint(380, 820), r.randint(330, 560)
    if style == "sun":
        rad = r.randint(230, 330)
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="{a1}"/>')
        for i in range(6):
            y = cy + rad * (0.15 + i * 0.16)
            out.append(f'<rect x="0" y="{y:.0f}" width="{S}" height="{10 + i * 5}" fill="{bg}" opacity=".9"/>')
    elif style == "rings":
        for i in range(7, 0, -1):
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{i * 55}" fill="{a1 if i % 2 else a2}" opacity="{0.35 + i * 0.08:.2f}"/>')
    elif style == "bars":
        n = r.randint(9, 15)
        for i in range(n):
            h = r.randint(160, 620); w = S / n
            out.append(f'<rect x="{i * w + 8:.0f}" y="{760 - h}" width="{w - 16:.0f}" height="{h}" rx="{w / 2 - 8:.0f}" fill="{a1 if i % 3 else a2}"/>')
    else:
        for i in range(6):
            for j in range(6):
                if r.random() < .55:
                    out.append(f'<circle cx="{150 + i * 180}" cy="{120 + j * 130}" r="{r.randint(18, 62)}" fill="{a1 if (i + j) % 2 else a2}" opacity=".9"/>')
    # waves at the bottom
    for k in range(4):
        base = 780 + k * 105; amp = 26 + k * 6; ph = r.random() * 6.3; col = [a2, lt, a1, deep][k]
        pts = " ".join(f"{x},{base + amp * math.sin(x / 95 + ph + k):.0f}" for x in range(0, S + 40, 40))
        out.append(f'<polygon points="0,{S} {pts} {S},{S}" fill="{col}" opacity="{0.9 if k != 1 else 0.55}"/>')
    out.append(f'<rect width="{S}" height="{S}" filter="url(#n)"/>')
    out.append('</svg>')
    return "\n".join(out)

here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "art"), exist_ok=True)
n = 0
for line in open(os.path.join(here, "artists.jsonl")):
    a = json.loads(line); slug = a["image"].split("/")[-1][:-4]
    open(os.path.join(here, "art", slug + ".svg"), "w").write(art(slug, a["genre"])); n += 1
print(f"wrote {n} images to art/")
