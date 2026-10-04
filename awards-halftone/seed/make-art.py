#!/usr/bin/env python3
"""Draw the entry artwork in art/ as halftone dot patterns.

Every image is generated from a few numbers, so the files are small, license-free and safe to
redistribute. Run from this directory:  python3 make-art.py
"""
import math
import os

W, H, STEP = 800, 1000, 26


def clamp(v):
    return max(0.0, min(1.0, v))


def sun(x, y):
    d = math.hypot(x - .5, y - .38)
    return clamp(1 - d * 2.4) if y < .62 else clamp(.25 + .5 * math.sin(y * 40) * (1 - y))


def wave(x, y):
    return clamp(.5 + .5 * math.sin(x * 9 + math.sin(y * 7) * 2.2) * math.cos(y * 3))


def diag(x, y):
    return clamp((x + y) / 1.6)


def rings(x, y):
    d = math.hypot(x - .62, y - .45)
    return clamp(.5 + .5 * math.sin(d * 38)) * clamp(1.2 - d)


def blobs(x, y):
    v = sum(r / max(.02, math.hypot(x - cx, y - cy)) for cx, cy, r in [(.3, .3, .09), (.7, .55, .12), (.4, .78, .07)])
    return clamp(v - .6)


def portrait(x, y):
    head = ((x - .5) / .2) ** 2 + ((y - .36) / .25) ** 2
    body = y > .66 and abs(x - .5) < .1 + (y - .66) * 1.1
    if head < 1:
        return clamp(.35 + .65 * (x - .3))
    return .9 if body else clamp(.12 * (1 - y))


def ridges(x, y):
    for i, (amp, base) in enumerate([(.06, .42), (.08, .58), (.05, .74)]):
        if y > base + amp * math.sin(x * (6 + i * 3) + i):
            last = i
    try:
        return .3 + .25 * last + .15 * math.sin(x * 20)
    except NameError:
        return clamp(.45 - y * .4)


def letter(ch):
    # Very simple stroke letters on a 0-1 grid: lists of (x0, y0, x1, y1) rectangles.
    shapes = {
        "H": [(.18, .15, .34, .85), (.66, .15, .82, .85), (.18, .44, .82, .56)],
        "A": [(.2, .15, .36, .85), (.64, .15, .8, .85), (.2, .15, .8, .3), (.2, .5, .8, .62)],
        "R": [(.2, .15, .36, .85), (.2, .15, .78, .28), (.62, .15, .78, .55), (.2, .45, .78, .56), (.55, .56, .72, .85)],
        "G": [(.2, .15, .36, .85), (.2, .15, .8, .28), (.2, .72, .8, .85), (.64, .5, .8, .85), (.48, .5, .8, .6)],
        "O": [(.2, .15, .36, .85), (.64, .15, .8, .85), (.2, .15, .8, .28), (.2, .72, .8, .85)],
    }[ch]

    def f(x, y):
        inside = any(a <= x <= c and b <= y <= d for a, b, c, d in shapes)
        return .95 if inside else clamp(.18 * y)
    return f


def grid(x, y):
    return .85 if (int(x * 8) + int(y * 10)) % 2 == 0 else .15


def spiral(x, y):
    a = math.atan2(y - .5, x - .5)
    d = math.hypot(x - .5, y - .5)
    return clamp(.5 + .5 * math.sin(a * 3 + d * 30))


def drop(x, y):
    d = math.hypot(x - .5, (y - .55) * 1.1)
    return clamp(1 - d * 2.1) * (1 if y > .25 else .3)


PATTERNS = {"sun": sun, "wave": wave, "diag": diag, "rings": rings, "blobs": blobs, "portrait": portrait,
            "ridges": ridges, "grid": grid, "spiral": spiral, "drop": drop,
            "H": letter("H"), "A": letter("A"), "R": letter("R"), "G": letter("G"), "O": letter("O")}

# name: (pattern, background, dots, accent shape, accent colour)
ART = {
    "salt-flats": ("ridges", "#efe7d6", "#1d1d1f", "sun", "#ff5a36"),
    "night-ferry": ("wave", "#101827", "#e9e2d0", "moon", "#f2c14e"),
    "the-quiet-hours": ("portrait", "#e8dfcf", "#20201f", "bar", "#2f6fdb"),
    "field-notes-no-4": ("blobs", "#f4efe4", "#0f3d2e", "circle", "#f29e4c"),
    "tidal": ("rings", "#0d1f2d", "#9ad1d4", "none", ""),
    "orchard-type": ("O", "#f1ead9", "#b4321f", "none", ""),
    "heat": ("sun", "#ff5a36", "#1c1310", "none", ""),
    "public-library-week": ("grid", "#f0e9db", "#1d3557", "circle", "#e63946"),
    "after-the-rain": ("drop", "#dfe7ea", "#16324f", "bar", "#f2c14e"),
    "pressure": ("spiral", "#151515", "#f5d547", "none", ""),
    "letters-from-home": ("portrait", "#f3d9c4", "#3a1f1a", "circle", "#2a9d8f"),
    "hartwell-grotesk": ("H", "#121212", "#f2eee6", "bar", "#ff5a36"),
    "low-tide-almanac": ("wave", "#e9e4d8", "#2b4c7e", "sun", "#e76f51"),
    "a-year-of-weather": ("diag", "#f6f1e7", "#264653", "circle", "#e9c46a"),
    "garden-city": ("blobs", "#13261d", "#c8e6a0", "none", ""),
    "rumble": ("R", "#f4ece0", "#111111", "circle", "#ff5a36"),
    "migrations": ("ridges", "#1b1b2f", "#e4d9ff", "moon", "#ff8c61"),
    "glasshouse": ("rings", "#f2efe9", "#5b2a86", "bar", "#ffb703"),
    "ground-floor": ("grid", "#212121", "#ffcf56", "none", ""),
    "gather": ("G", "#e7efe9", "#14532d", "circle", "#f97316"),
    "second-sun": ("sun", "#f6e7c8", "#7c2d12", "none", ""),
    "the-night-shift": ("portrait", "#0f172a", "#f8d38b", "bar", "#ef4444"),
    "atlas-of-small-things": ("spiral", "#f5f0e6", "#1f2937", "sun", "#10b981"),
    "a-is-for-arches": ("A", "#efe6d5", "#283618", "moon", "#dda15e"),
}


def accent(kind, colour):
    if kind == "sun":
        return f'<circle cx="610" cy="230" r="120" fill="{colour}"/>'
    if kind == "moon":
        return f'<circle cx="200" cy="210" r="90" fill="{colour}"/>'
    if kind == "circle":
        return f'<circle cx="400" cy="520" r="250" fill="{colour}" opacity=".9"/>'
    if kind == "bar":
        return f'<rect x="0" y="690" width="800" height="90" fill="{colour}"/>'
    return ""


def draw(name, pattern, bg, fg, kind, colour):
    f = PATTERNS[pattern]
    dots = []
    for j, y in enumerate(range(STEP // 2, H, STEP)):
        off = STEP // 2 if j % 2 else 0
        for x in range(STEP // 2 + off, W, STEP):
            r = f(x / W, y / H) * STEP * .62
            if r > .8:
                dots.append(f'<circle cx="{x}" cy="{y}" r="{r:.1f}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>{accent(kind, colour)}<g fill="{fg}">{"".join(dots)}</g></svg>\n')


if __name__ == "__main__":
    os.makedirs("art", exist_ok=True)
    for name, spec in ART.items():
        with open(os.path.join("art", name + ".svg"), "w") as fh:
            fh.write(draw(name, *spec))
    print(len(ART), "images written to art/")
