#!/usr/bin/env python3
"""Generate the artwork in this folder: illustrated instructor portraits (photos/) and course covers (covers/).

Everything is drawn from simple shapes, so the files are tiny, license-free and safe to redistribute.
The people and courses are fictional. Run from this directory:  python3 make-art.py
"""
import os, re

SKIN = ["#f5d0b5", "#e8b896", "#c98e68", "#a86f4c", "#7d4f33", "#5c3a26"]
HAIR = ["#1d1a26", "#3b2a20", "#6b4226", "#a8643a", "#d9b26f", "#9aa0ad"]
BG = [("#f2a20c", "#e8553d"), ("#1f4d3a", "#4f9a74"), ("#e8553d", "#f2a20c"), ("#3d5af1", "#8fb3ff")]
TOP = ["#16130f", "#f6f1e7", "#1f4d3a", "#7c2d12"]

# name -> (skin, hair colour, hair style, background, top, glasses)
PEOPLE = {
    "Nadia Haddad":   (2, 0, "long", 0, 0, True),
    "Mateo Alvarez":  (1, 1, "short", 3, 1, False),
    "Sam Whitfield":  (0, 4, "side", 1, 3, True),
    "Grace Okonkwo":  (5, 0, "bun", 2, 2, False),
}

def hair(style, c):
    if style == "short":
        return f'<path d="M140 205c0-62 30-96 60-96s62 30 62 92c-12-30-38-44-62-44-26 0-50 16-60 48z" fill="{c}"/>'
    if style == "side":
        return f'<path d="M136 210c-6-70 28-104 66-104 44 0 70 36 62 100-8-28-22-46-40-52-30 10-62 12-88 56z" fill="{c}"/>'
    if style == "buzz":
        return f'<path d="M142 196c4-52 30-80 58-80s56 28 58 80c-14-26-34-38-58-38s-44 12-58 38z" fill="{c}" opacity=".92"/>'
    if style == "long":
        return (f'<path d="M128 330c-18-80-10-150 10-180 16-26 38-40 62-40s48 14 62 40c22 32 28 100 10 180-10-40-14-80-16-120'
                f'-14-30-34-46-56-50-22 6-44 22-56 52-2 40-6 78-16 118z" fill="{c}"/>')
    if style == "bob":
        return (f'<path d="M132 262c-14-64 0-120 24-140 14-12 28-16 44-16s32 4 46 16c24 20 36 76 22 140-6-22-8-46-8-70'
                f'-16-26-36-38-60-40-22 4-46 16-60 42 0 22-2 46-8 68z" fill="{c}"/>')
    if style == "bun":
        return (f'<circle cx="200" cy="96" r="30" fill="{c}"/>'
                f'<path d="M140 206c0-60 28-90 60-90s60 30 60 90c-14-32-36-46-60-46s-46 14-60 46z" fill="{c}"/>')
    if style == "curly":
        dots = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r in [
            (150, 170, 26), (170, 132, 28), (200, 118, 30), (232, 132, 28), (252, 170, 26), (140, 208, 20), (262, 208, 20),
            (186, 140, 24), (216, 140, 24)])
        return dots
    return ""

def svg(name):
    s, h, style, b, t, glasses = PEOPLE[name]
    c1, c2 = BG[b]
    skin, hc, top = SKIN[s], HAIR[h], TOP[t]
    gid = re.sub(r"[^a-z]", "", name.lower())
    g = ""
    if glasses:
        g = ('<g fill="none" stroke="#0b0b14" stroke-width="5" opacity=".85">'
             '<rect x="160" y="196" width="34" height="26" rx="9"/><rect x="206" y="196" width="34" height="26" rx="9"/>'
             '<path d="M194 208h12"/></g>')
    back = hair(style, hc) if style in ("long", "bob", "bun") else ""
    front = "" if style in ("long", "bob", "bun") else hair(style, hc)
    if style == "bun":
        back, front = f'<circle cx="200" cy="96" r="30" fill="{hc}"/>', hair("short", hc)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500" width="400" height="500" role="img" aria-label="Illustrated portrait of {name}">
<defs>
<linearGradient id="bg{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
<radialGradient id="glow{gid}" cx=".5" cy=".38" r=".6"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
</defs>
<rect width="400" height="500" fill="url(#bg{gid})"/>
<rect width="400" height="500" fill="url(#glow{gid})"/>
<circle cx="330" cy="70" r="90" fill="#fff" opacity=".12"/><path d="M0 380 L400 300 L400 500 L0 500z" fill="#16130f" opacity=".08"/>
{back}
<path d="M70 500c6-96 60-150 130-150s124 54 130 150z" fill="{top}"/>
<path d="M176 300h48v58c-8 12-40 12-48 0z" fill="{skin}"/>
<path d="M176 330c14 8 34 8 48 0v10c-14 8-34 8-48 0z" fill="#000" opacity=".12"/>
<ellipse cx="200" cy="222" rx="60" ry="76" fill="{skin}"/>
<ellipse cx="140" cy="228" rx="10" ry="16" fill="{skin}"/><ellipse cx="260" cy="228" rx="10" ry="16" fill="{skin}"/>
{front}
<g fill="#1a1423"><ellipse cx="177" cy="211" rx="5" ry="6"/><ellipse cx="223" cy="211" rx="5" ry="6"/></g>
<path d="M166 194q11-7 22 0M212 194q11-7 22 0" stroke="#1a1423" stroke-width="4" fill="none" stroke-linecap="round" opacity=".7"/>
<path d="M200 220q-6 18 0 22" stroke="#000" stroke-opacity=".18" stroke-width="4" fill="none" stroke-linecap="round"/>
<path d="M182 260q18 14 36 0" stroke="#5a2a2a" stroke-width="5" fill="none" stroke-linecap="round"/>
{g}
</svg>
'''


# Course covers: one composition per category, in the course accent colour.
COURSES = {
    "sql-for-product-questions":       ("query", "#f2a20c"),
    "dashboards-people-actually-use":  ("data", "#e8553d"),
    "design-systems-from-scratch":     ("design", "#3d5af1"),
    "interface-typography":            ("type", "#c2410c"),
    "product-discovery-in-practice":   ("product", "#1f4d3a"),
    "writing-clear-product-specs":     ("doc", "#0e7490"),
    "leading-your-first-team":         ("leadership", "#7c3aed"),
}

def cover(slug, kind, c):
    ink, paper = "#16130f", "#f6f1e7"
    if kind == "data":
        bars = "".join(f'<rect x="{150+i*120}" y="{600-h}" width="78" height="{h}" rx="10" fill="{paper}" opacity="{.35+i*.1:.2f}"/>'
                       for i, h in enumerate([160, 250, 210, 330, 420, 380, 500]))
        art = (bars + f'<path d="M150 360 C330 300 420 420 600 300 S900 180 1060 120" fill="none" stroke="{ink}" stroke-width="14" stroke-linecap="round"/>'
               f'<circle cx="1060" cy="120" r="26" fill="{ink}"/><circle cx="1060" cy="120" r="10" fill="{paper}"/>')
    elif kind == "design":
        art = (f'<circle cx="420" cy="380" r="230" fill="{paper}" opacity=".9"/><rect x="560" y="170" width="380" height="380" rx="40" fill="{ink}" opacity=".88"/>'
               f'<path d="M700 600 L900 260 L1100 600z" fill="{paper}" opacity=".45"/><circle cx="420" cy="380" r="90" fill="{c}"/>'
               f'<g stroke="{ink}" stroke-width="3" opacity=".35">' + "".join(f'<path d="M{x} 60V690"/>' for x in range(100, 1200, 100)) + '</g>')
    elif kind == "product":
        cards = "".join(f'<rect x="{180+i*90}" y="{150+i*70}" width="520" height="300" rx="28" fill="{paper}" opacity="{.35+i*.2:.2f}"/>' for i in range(3))
        art = (cards + f'<rect x="360" y="290" width="520" height="300" rx="28" fill="{paper}"/>'
               f'<rect x="400" y="330" width="220" height="22" rx="11" fill="{ink}"/><rect x="400" y="372" width="360" height="14" rx="7" fill="{ink}" opacity=".35"/>'
               f'<rect x="400" y="400" width="300" height="14" rx="7" fill="{ink}" opacity=".35"/><circle cx="820" cy="530" r="34" fill="{c}"/>'
               f'<path d="M806 530l10 10 20-22" stroke="{paper}" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
               f'<path d="M950 150 q120 80 60 220" stroke="{ink}" stroke-width="10" fill="none" stroke-dasharray="4 22" stroke-linecap="round"/>')
    elif kind == "query":
        cells = "".join(f'<rect x="{200+c*170}" y="{200+r*80}" width="150" height="60" rx="10" fill="{paper}" opacity="{.95 if r == 0 else (.75 if (r+c) % 3 == 0 else .4)}"/>'
                        for r in range(5) for c in range(5))
        art = (cells + f'<rect x="530" y="270" width="170" height="80" rx="14" fill="none" stroke="{ink}" stroke-width="10"/>'
               f'<path d="M150 150 l-50 225 l50 225 M1100 150 l50 225 l-50 225" stroke="{ink}" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    elif kind == "type":
        art = (f'<text x="140" y="600" font-family="Georgia,serif" font-size="560" font-weight="700" fill="{paper}">A</text>'
               f'<text x="560" y="600" font-family="Helvetica,Arial,sans-serif" font-size="460" font-weight="300" fill="{ink}" opacity=".85">a</text>'
               f'<g stroke="{paper}" stroke-width="3" opacity=".6"><path d="M80 600H1120"/><path d="M80 380H1120" stroke-dasharray="10 12"/><path d="M80 200H1120" stroke-dasharray="10 12"/></g>'
               f'<circle cx="1000" cy="200" r="22" fill="{ink}"/>')
    elif kind == "doc":
        lines = "".join(f'<rect x="440" y="{250+i*46}" width="{[300,260,320,200,280,240,180][i]}" height="16" rx="8" fill="{ink}" opacity=".3"/>' for i in range(7))
        art = (f'<rect x="380" y="100" width="440" height="620" rx="26" fill="{paper}" transform="rotate(-4 600 400)" opacity=".5"/>'
               f'<rect x="380" y="110" width="440" height="620" rx="26" fill="{paper}"/>'
               f'<rect x="440" y="170" width="200" height="30" rx="15" fill="{ink}"/>' + lines +
               f'<rect x="420" y="425" width="360" height="70" rx="12" fill="{c}" opacity=".18"/>'
               f'<path d="M880 560 l120 -120 l40 40 l-120 120 l-60 20z" fill="{ink}"/>')
    else:
        rings = "".join(f'<circle cx="600" cy="700" r="{r}" fill="none" stroke="{paper}" stroke-width="22" opacity="{o}"/>'
                        for r, o in [(520, .18), (420, .3), (320, .45), (220, .65)])
        art = (rings + f'<circle cx="600" cy="700" r="120" fill="{paper}"/>'
               + "".join(f'<circle cx="{x}" cy="{y}" r="30" fill="{ink}"/>' for x, y in [(380, 330), (600, 240), (820, 330)])
               + f'<circle cx="600" cy="240" r="12" fill="{c}"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" width="1200" height="750" role="img" aria-label="Course cover artwork">
<defs><radialGradient id="g" cx=".8" cy=".1" r="1"><stop offset="0" stop-color="#fff" stop-opacity=".28"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>
<rect width="1200" height="750" fill="{c}"/><rect width="1200" height="750" fill="url(#g)"/>
{art}
</svg>
'''

def slug(n): return re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")

if __name__ == "__main__":
    os.makedirs("photos", exist_ok=True); os.makedirs("covers", exist_ok=True)
    for n in PEOPLE:
        open(f"photos/{slug(n)}.svg", "w").write(svg(n))
    for s, (k, c) in COURSES.items():
        open(f"covers/{s}.svg", "w").write(cover(s, k, c))
    print(f"wrote {len(PEOPLE)} portraits and {len(COURSES)} covers")
