#!/usr/bin/env python3
"""Draw the event and news illustrations in art/ as flat garden scenes (SVG).
Each image comes from a few numbers, so the files are small and license-free. Run: python3 make-art.py"""
import math, os, random

W, H = 1200, 800
PALETTES = [  # sky, far hill, near hill, soil, leaf, leaf2, accent
    ("#f3e3c3", "#c9d6a3", "#8fb07a", "#7a4b2a", "#2f6b43", "#4f9a5f", "#c8553d"),
    ("#e9efe4", "#b7cdb2", "#6f9c7a", "#5b3a24", "#1f4d35", "#3f7d5a", "#e0a526"),
    ("#f6dccb", "#e7b48f", "#c98461", "#6b3b25", "#2f6b43", "#86a95a", "#2f6f8f"),
    ("#dfe8ee", "#a9c3cf", "#6d97a8", "#4a3527", "#24543e", "#5a8f29", "#d9822b"),
    ("#efe4f1", "#cdb6d4", "#9a7fae", "#4d3328", "#2c5e45", "#6fa36b", "#e0a526"),
]
ART = {  # name: (palette, motif, seed)
    "seed-swap": (1, "seeds", 3), "winterizing": (3, "beds", 7), "legal-clinic": (4, "fence", 11),
    "water-wise": (2, "drip", 5), "repair-day": (0, "tools", 9), "grant-writing": (1, "sprout", 2),
    "hoop-houses": (3, "hoop", 4), "gathering": (0, "crowd", 8), "potluck": (2, "table", 6),
    "news-food-deserts": (0, "beds", 12), "news-seed-record": (1, "seeds", 13), "news-ordinances": (4, "fence", 14),
    "news-cover": (3, "sprout", 15), "news-fall-crops": (2, "beds", 16), "news-austin": (0, "sprout", 17),
}

def leaf(x, y, s, a, c):
    return f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{s*.42:.1f}" ry="{s:.1f}" transform="rotate({a:.0f} {x:.0f} {y:.0f})" fill="{c}"/>'

def plant(r, x, base, h, p):
    out = [f'<rect x="{x-3:.0f}" y="{base-h:.0f}" width="6" height="{h:.0f}" rx="3" fill="{p[4]}"/>']
    for i in range(int(h // 22)):
        yy = base - 18 - i * 22
        out.append(leaf(x - 16, yy, 18 + r.random() * 6, -50, p[5] if i % 2 else p[4]))
        out.append(leaf(x + 16, yy - 9, 18 + r.random() * 6, 50, p[4] if i % 2 else p[5]))
    if r.random() < .5:
        out.append(f'<circle cx="{x:.0f}" cy="{base-h-8:.0f}" r="{10+r.random()*6:.0f}" fill="{p[6]}"/>')
    return "".join(out)

def scene(name, pi, motif, seed):
    r = random.Random(seed); p = PALETTES[pi]
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
         f'<rect width="{W}" height="{H}" fill="{p[0]}"/>',
         f'<circle cx="{r.randint(760,1020)}" cy="{r.randint(150,230)}" r="{r.randint(80,120)}" fill="{p[6]}" opacity=".9"/>',
         f'<path d="M0 430 Q300 {r.randint(300,380)} 600 420 T1200 400 V800 H0Z" fill="{p[1]}"/>',
         f'<path d="M0 520 Q350 {r.randint(430,480)} 700 520 T1200 500 V800 H0Z" fill="{p[2]}"/>']
    if motif in ("beds", "drip", "sprout", "seeds"):
        for row in range(3):
            y = 600 + row * 70
            s.append(f'<rect x="-20" y="{y}" width="{W+40}" height="46" rx="23" fill="{p[3]}" opacity="{.75+row*.1:.2f}"/>')
            for x in range(60 + row * 30, W, 120 if motif != "sprout" else 90):
                h = r.randint(40, 110) if motif != "sprout" else r.randint(30, 60)
                s.append(plant(r, x, y + 10, h, p))
            if motif == "drip":
                s.append(f'<path d="M0 {y+30} H{W}" stroke="#2f6f8f" stroke-width="6" stroke-dasharray="2 22" stroke-linecap="round"/>')
        if motif == "seeds":
            for _ in range(90):
                s.append(f'<ellipse cx="{r.randint(0,W)}" cy="{r.randint(560,800)}" rx="7" ry="4" fill="{p[6]}" transform="rotate({r.randint(0,180)} 0 0)" opacity=".0"/>')
            for _ in range(70):
                x, y = r.randint(30, W - 30), r.randint(80, 520)
                s.append(f'<ellipse cx="{x}" cy="{y}" rx="9" ry="5" fill="{r.choice([p[6],p[3],p[4]])}" transform="rotate({r.randint(0,180)} {x} {y})"/>')
    elif motif == "fence":
        for x in range(0, W, 70):
            s.append(f'<path d="M{x+10} 700 V560 l20 -24 l20 24 V700Z" fill="#f7f1e3" stroke="{p[3]}" stroke-width="3"/>')
        s.append(f'<rect x="0" y="590" width="{W}" height="14" fill="#f7f1e3"/><rect x="0" y="650" width="{W}" height="14" fill="#f7f1e3"/>')
        for x in range(40, W, 140): s.append(plant(r, x, 720, r.randint(80, 150), p))
    elif motif == "hoop":
        s.append(f'<rect x="0" y="640" width="{W}" height="160" fill="{p[3]}"/>')
        s.append(f'<path d="M260 660 A340 300 0 0 1 940 660Z" fill="#ffffff" opacity=".55" stroke="#ffffff" stroke-width="6"/>')
        for i in range(6): s.append(f'<path d="M{300+i*20} 660 A{300-i*20} {270-i*18} 0 0 1 {900-i*20} 660" fill="none" stroke="#ffffff" stroke-width="3" opacity=".7"/>')
        for x in range(330, 900, 70): s.append(plant(r, x, 660, r.randint(50, 110), p))
    elif motif == "tools":
        s.append(f'<rect x="0" y="620" width="{W}" height="180" fill="{p[3]}"/>')
        for i, x in enumerate(range(170, W - 100, 190)):
            s.append(f'<rect x="{x}" y="280" width="16" height="360" rx="8" fill="#8a5a3b" transform="rotate({r.randint(-12,12)} {x} 620)"/>')
            s.append(f'<path d="M{x-40} 560 h96 l-14 90 h-68z" fill="{[p[6],"#6b7b86",p[4]][i%3]}" transform="rotate({r.randint(-12,12)} {x} 620)"/>')
    elif motif in ("crowd", "table"):
        s.append(f'<rect x="0" y="640" width="{W}" height="160" fill="{p[3]}" opacity=".85"/>')
        if motif == "table":
            s.append(f'<rect x="140" y="560" width="920" height="26" rx="8" fill="#f7f1e3"/>')
            for x in range(200, 1040, 110):
                s.append(f'<ellipse cx="{x}" cy="550" rx="40" ry="14" fill="{r.choice(p[4:])}"/><circle cx="{x}" cy="536" r="14" fill="{p[6]}"/>')
        for x in range(60, W, 80):
            hh = r.randint(150, 210); c = r.choice([p[4], p[6], "#2f6f8f", "#7a5c9e", p[5]])
            s.append(f'<rect x="{x-22}" y="{760-hh}" width="44" height="{hh}" rx="22" fill="{c}"/><circle cx="{x}" cy="{730-hh}" r="22" fill="#e7c4a0"/>')
    s.append('</svg>\n')
    return "".join(s)

if __name__ == "__main__":
    os.makedirs("art", exist_ok=True)
    for n, (pi, m, sd) in ART.items():
        open(os.path.join("art", n + ".svg"), "w").write(scene(n, pi, m, sd))
    print(len(ART), "images written to art/")
