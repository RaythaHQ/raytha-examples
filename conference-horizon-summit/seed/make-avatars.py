#!/usr/bin/env python3
"""Generate the flat, illustrated SVG speaker portraits in ./avatars/ (fictional people, no photos).

Every portrait is drawn from simple shapes, so the files are tiny, license-free and safe to redistribute.
Run from this directory:  python3 make-avatars.py
"""
import json, os, re

SKIN = ["#f5d0b5", "#e8b896", "#c98e68", "#a86f4c", "#7d4f33", "#5c3a26"]
HAIR = ["#1d1a26", "#3b2a20", "#6b4226", "#a8643a", "#d9b26f", "#9aa0ad"]
BG = [("#8b5cf6", "#22d3ee"), ("#ec4899", "#fb923c"), ("#22d3ee", "#a3e635"), ("#f59e0b", "#ec4899"),
      ("#6366f1", "#ec4899"), ("#a3e635", "#22d3ee"), ("#fb923c", "#8b5cf6"), ("#14b8a6", "#6366f1")]
TOP = ["#0f172a", "#1e1b4b", "#f8fafc", "#334155", "#7c2d12", "#064e3b", "#4c1d95", "#e2e8f0"]

# name -> (skin, hair colour, hair style, background, top, glasses)
PEOPLE = {
    "Maya Okafor":      (4, 0, "curly", 0, 0, False),
    "Daniel Reyes":     (2, 1, "short", 1, 3, False),
    "Priya Raman":      (3, 0, "long", 2, 6, True),
    "Lukas Brandt":     (0, 4, "side", 3, 1, True),
    "Sofia Marchetti":  (1, 2, "bob", 4, 2, False),
    "Marcus Bell":      (5, 0, "buzz", 5, 4, False),
    "Hannah Lindqvist": (0, 4, "bun", 6, 7, False),
    "Theo Nakamura":    (1, 0, "side", 7, 0, True),
    "Amara Diallo":     (5, 0, "bun", 1, 5, False),
    "Ethan Cole":       (0, 3, "short", 2, 3, False),
    "Elena Petrova":    (1, 3, "long", 0, 1, False),
    "Javier Ortega":    (2, 5, "buzz", 3, 6, True),
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
<rect width="400" height="500" fill="#0c0b1d"/>
<rect width="400" height="500" fill="url(#bg{gid})" opacity=".9"/>
<rect width="400" height="500" fill="url(#glow{gid})"/>
<circle cx="330" cy="70" r="90" fill="#fff" opacity=".07"/><circle cx="40" cy="430" r="120" fill="#000" opacity=".12"/>
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

def slug(n): return re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")

if __name__ == "__main__":
    os.makedirs("avatars", exist_ok=True)
    for n in PEOPLE:
        open(f"avatars/{slug(n)}.svg", "w").write(svg(n))
    print(f"wrote {len(PEOPLE)} avatars")
