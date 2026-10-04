"""Draw the ten fictional company logos as square SVG marks (no fonts, no third-party assets).

    python3 make-logos.py     # writes logos/<slug>.svg
"""
import math, os

def frame(color, body, bg="#ffffff"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">'
            f'<rect width="128" height="128" rx="30" fill="{color}"/>{body}</svg>\n')

W = "#ffffff"
def rays(n, r1, r2, cx=64, cy=64, w=7, a0=0.0, a1=2 * math.pi):
    out = ""
    for i in range(n):
        a = a0 + (a1 - a0) * i / (n - 1 if a1 - a0 < 2 * math.pi else n)
        x1, y1 = cx + r1 * math.cos(a), cy + r1 * math.sin(a)
        x2, y2 = cx + r2 * math.cos(a), cy + r2 * math.sin(a)
        out += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{W}" stroke-width="{w}" stroke-linecap="round"/>'
    return out

LOGOS = {
    # Solar: a rising sun over a horizon line
    "helio-forge": ("#e8890c", '<path d="M30 80a34 34 0 0 1 68 0z" fill="#fff"/>' + rays(5, 42, 52, 64, 80, 6, math.pi * 1.1, math.pi * 1.9).replace('stroke="#ffffff"', 'stroke="#fff" opacity=".9"') + '<rect x="22" y="86" width="84" height="8" rx="4" fill="#fff"/>'),
    # Storage: stacked battery cells
    "voltcrest": ("#1f9d55", '<rect x="40" y="26" width="48" height="80" rx="10" fill="none" stroke="#fff" stroke-width="7"/><rect x="54" y="16" width="20" height="10" rx="3" fill="#fff"/><rect x="50" y="72" width="28" height="9" rx="3" fill="#fff"/><rect x="50" y="58" width="28" height="9" rx="3" fill="#fff"/><rect x="50" y="44" width="28" height="9" rx="3" fill="#fff" opacity=".45"/>'),
    # Grid software: connected nodes
    "gridwise": ("#2456d6", '<path d="M34 40L94 40M34 40L64 88M94 40L64 88M34 40L34 88M94 40L94 88M34 88L94 88" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".7"/>' + ''.join(f'<circle cx="{x}" cy="{y}" r="9" fill="#fff"/>' for x, y in [(34,40),(94,40),(64,88),(34,88),(94,88)])),
    # Carbon removal: a well drawing down into the ground
    "deepwell-carbon": ("#0f6b62", '<circle cx="64" cy="46" r="22" fill="none" stroke="#fff" stroke-width="7"/><path d="M64 68v36M52 92l12 12 12-12" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/><circle cx="64" cy="46" r="7" fill="#fff"/>'),
    # Mobility / charging: a loop wave
    "tidal-loop": ("#0b8bc4", '<path d="M22 70c14-26 28-26 42 0s28 26 42 0" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round"/><path d="M22 48c14-26 28-26 42 0s28 26 42 0" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" opacity=".45"/>'),
    # Regenerative agriculture: furrows and a sprout
    "furrow": ("#5a8f12", '<path d="M24 96h80M32 82h64M42 68h44" stroke="#fff" stroke-width="7" stroke-linecap="round"/><path d="M64 68V34" stroke="#fff" stroke-width="7" stroke-linecap="round"/><path d="M64 46c0-12 10-18 22-18 0 12-10 18-22 18zM64 54c0-10-8-16-18-16 0 10 8 16 18 16z" fill="#fff"/>'),
    # Buildings / heat pumps: a house with a flame
    "thermal-union": ("#d9572b", '<path d="M26 62L64 30l38 32v40H26z" fill="none" stroke="#fff" stroke-width="7" stroke-linejoin="round"/><path d="M64 96c-10 0-16-7-16-15 0-10 10-14 10-24 8 5 9 11 8 15 3-2 5-5 5-8 6 5 9 10 9 17 0 8-6 15-16 15z" fill="#fff"/>'),
    # Climate data: a leaf seen as a satellite grid
    "canopy-analytics": ("#137a3a", '<path d="M30 98C30 54 54 30 98 30c0 44-24 68-68 68z" fill="#fff"/><path d="M30 98L78 50M50 78h18M62 66h18M50 58v18M62 46v18" stroke="#137a3a" stroke-width="5" stroke-linecap="round"/>'),
    # Ocean carbon: kelp fronds
    "saltmarsh-labs": ("#0a7f99", '<path d="M44 104c0-24 12-30 12-52s-8-26-8-26M64 104c0-30 14-36 14-58M84 104c0-20-10-28-10-46" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round"/><circle cx="56" cy="40" r="5" fill="#fff"/><circle cx="78" cy="36" r="5" fill="#fff"/>'),
    # Community energy: a bolt in a ring
    "ampere-commons": ("#6b3fd4", '<circle cx="64" cy="64" r="38" fill="none" stroke="#fff" stroke-width="7" opacity=".5"/><path d="M70 22L40 70h22l-6 36 32-50H66z" fill="#fff"/>'),
}

os.makedirs("logos", exist_ok=True)
for slug, (color, body) in LOGOS.items():
    with open(f"logos/{slug}.svg", "w") as fh:
        fh.write(frame(color, body))
    print("logos/" + slug + ".svg")
