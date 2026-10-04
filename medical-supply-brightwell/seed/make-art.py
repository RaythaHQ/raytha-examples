#!/usr/bin/env python3
"""Draw the product illustrations in art/ from simple shapes.

The files are tiny, license-free and safe to redistribute. Run from this directory:  python3 make-art.py
"""
import os

NAVY, TEAL, MINT, SKY, AMBER, WHITE = "#0b2545", "#0f8b8d", "#dff2ee", "#e8f1f8", "#f4a259", "#ffffff"
S = f'stroke="{NAVY}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"'
T = f'stroke="{NAVY}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"'


def wheel(cx, cy, r, spokes=True):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" {S}/>'
    if spokes and r > 40:
        s += f'<circle cx="{cx}" cy="{cy}" r="{r-18}" fill="none" stroke="{TEAL}" stroke-width="5"/>'
        s += "".join(f'<path d="M{cx} {cy} l{dx} {dy}" stroke="{NAVY}" stroke-width="4" opacity=".5"/>'
                     for dx, dy in [(0, -(r-18)), (0, r-18), (r-18, 0), (-(r-18), 0)])
    s += f'<circle cx="{cx}" cy="{cy}" r="7" fill="{NAVY}"/>'
    return s


ART = {
    "transport-wheelchair": wheel(470, 400, 120) + wheel(300, 470, 34, False) +
        f'<path d="M300 436 L320 300 L470 300 L500 160 M320 300 L300 230 L270 230 M470 300 L470 400" fill="none" {S}/>'
        f'<rect x="318" y="268" width="170" height="34" rx="12" fill="{TEAL}"/><rect x="455" y="150" width="34" height="140" rx="12" fill="{TEAL}" transform="rotate(12 472 220)"/>'
        f'<path d="M500 160 l40 -10" fill="none" {S}/>',
    "rollator": wheel(270, 480, 42, False) + wheel(530, 480, 42, False) +
        f'<path d="M270 438 L330 170 M530 438 L470 170 M330 170 l-40 -10 M470 170 l40 -10 M300 320 L500 320" fill="none" {S}/>'
        f'<rect x="300" y="300" width="200" height="34" rx="14" fill="{TEAL}"/><rect x="330" y="350" width="140" height="60" rx="12" fill="{WHITE}" {T}/>'
        f'<path d="M300 210 q-20 10 -16 40 M500 210 q20 10 16 40" fill="none" stroke="{AMBER}" stroke-width="8" stroke-linecap="round"/>',
    "knee-scooter": wheel(250, 480, 40, False) + wheel(560, 480, 40, False) + wheel(330, 480, 40, False) + wheel(480, 480, 40, False) +
        f'<path d="M250 480 L560 480 M300 470 L520 470 M440 470 L440 330 M300 470 L270 170 M240 170 l60 0" fill="none" {S}/>'
        f'<rect x="380" y="300" width="150" height="40" rx="18" fill="{TEAL}"/>',
    "oxygen-concentrator": f'<rect x="300" y="140" width="200" height="360" rx="36" fill="{WHITE}" {S}/>'
        f'<rect x="330" y="180" width="140" height="70" rx="14" fill="{SKY}" {T}/><circle cx="370" cy="215" r="14" fill="{TEAL}"/><path d="M400 205 h50 M400 225 h34" {T}/>'
        + "".join(f'<path d="M335 {290+i*22} h130" stroke="{NAVY}" stroke-width="6" stroke-linecap="round" opacity=".35"/>' for i in range(7)) +
        f'<circle cx="335" cy="512" r="14" fill="{NAVY}"/><circle cx="465" cy="512" r="14" fill="{NAVY}"/>'
        f'<path d="M500 220 C620 220 620 360 560 400 S520 500 600 520" fill="none" stroke="{TEAL}" stroke-width="8" stroke-linecap="round"/>',
    "portable-oxygen": f'<rect x="300" y="230" width="200" height="250" rx="40" fill="{WHITE}" {S}/>'
        f'<path d="M330 230 C330 120 470 120 470 230" fill="none" stroke="{TEAL}" stroke-width="18" stroke-linecap="round"/>'
        f'<rect x="330" y="270" width="140" height="60" rx="14" fill="{SKY}" {T}/><path d="M350 300 h30" stroke="{TEAL}" stroke-width="8" stroke-linecap="round"/><circle cx="440" cy="300" r="10" fill="{AMBER}"/>'
        + "".join(f'<path d="M340 {360+i*22} h120" stroke="{NAVY}" stroke-width="6" stroke-linecap="round" opacity=".35"/>' for i in range(4)),
    "cpap": f'<rect x="200" y="300" width="260" height="170" rx="34" fill="{WHITE}" {S}/><rect x="230" y="330" width="90" height="56" rx="12" fill="{SKY}" {T}/>'
        f'<rect x="350" y="250" width="110" height="60" rx="16" fill="{TEAL}"/><circle cx="410" cy="420" r="18" fill="none" {T}/>'
        f'<path d="M460 360 C560 360 560 230 610 230" fill="none" stroke="{NAVY}" stroke-width="22" stroke-linecap="round" opacity=".18"/>'
        f'<path d="M460 360 C560 360 560 230 610 230" fill="none" stroke="{TEAL}" stroke-width="10" stroke-linecap="round" stroke-dasharray="2 14"/>'
        f'<path d="M600 190 q60 0 60 50 q0 50 -60 50 q-20 -50 0 -100z" fill="{WHITE}" {S}/>',
    "nebulizer": f'<rect x="200" y="320" width="260" height="150" rx="30" fill="{WHITE}" {S}/><circle cx="270" cy="395" r="26" fill="{TEAL}"/><path d="M330 380 h90 M330 410 h60" {T}/>'
        f'<path d="M460 400 C560 400 520 260 560 240" fill="none" stroke="{TEAL}" stroke-width="8" stroke-linecap="round"/>'
        f'<path d="M530 240 h80 l-14 90 h-52z" fill="{SKY}" {S}/><path d="M570 240 v-50 l40 -20" fill="none" {S}/>',
    "hospital-bed": f'<rect x="150" y="300" width="500" height="40" rx="14" fill="{TEAL}"/>'
        f'<path d="M150 230 V470 M650 270 V470 M150 340 H650 M190 470 v20 M610 470 v20" fill="none" {S}/>'
        f'<path d="M170 300 q20 -60 120 -50 l20 50" fill="{WHITE}" {T}/><rect x="300" y="250" width="200" height="40" rx="12" fill="{WHITE}" {T}/>'
        f'<path d="M330 230 h160 M330 230 v30 M490 230 v30" fill="none" stroke="{AMBER}" stroke-width="8" stroke-linecap="round"/>'
        f'<circle cx="190" cy="500" r="14" fill="{NAVY}"/><circle cx="610" cy="500" r="14" fill="{NAVY}"/>',
    "pressure-mattress": "".join(f'<rect x="{150+i*50}" y="300" width="44" height="110" rx="20" fill="{TEAL if i % 2 else WHITE}" {T}/>' for i in range(10)) +
        f'<rect x="140" y="410" width="520" height="30" rx="12" fill="{SKY}" {T}/>'
        f'<rect x="560" y="470" width="110" height="60" rx="14" fill="{WHITE}" {S}/><circle cx="590" cy="500" r="10" fill="{AMBER}"/>'
        f'<path d="M560 500 C480 500 470 450 420 440" fill="none" stroke="{NAVY}" stroke-width="5" stroke-dasharray="4 10"/>',
    "shower-chair": f'<rect x="280" y="300" width="240" height="40" rx="16" fill="{TEAL}"/>'
        f'<path d="M300 340 L280 500 M500 340 L520 500 M330 340 L330 480 M470 340 L470 480 M300 300 L300 160 L500 160 L500 300" fill="none" {S}/>'
        f'<rect x="320" y="180" width="160" height="80" rx="16" fill="{WHITE}" {T}/>'
        + "".join(f'<circle cx="{360+i*40}" cy="320" r="5" fill="{WHITE}"/>' for i in range(3)) +
        f'<path d="M270 500 h30 M500 500 h30" {S}/>',
    "raised-toilet-seat": f'<ellipse cx="400" cy="330" rx="170" ry="50" fill="{WHITE}" {S}/><ellipse cx="400" cy="330" rx="90" ry="22" fill="{SKY}" {T}/>'
        f'<path d="M230 340 v60 q0 30 40 30 h260 q40 0 40 -30 v-60" fill="{TEAL}" opacity=".9" {S}/>'
        f'<path d="M200 300 v-60 h60 M600 300 v-60 h-60" fill="none" stroke="{AMBER}" stroke-width="10" stroke-linecap="round"/>',
    "transfer-bench": f'<rect x="170" y="300" width="460" height="40" rx="16" fill="{TEAL}"/>'
        f'<path d="M200 340 L190 500 M600 340 L610 500 M330 340 v160 M470 340 v160 M470 300 V170 L620 170 V300" fill="none" {S}/>'
        f'<rect x="490" y="190" width="110" height="70" rx="14" fill="{WHITE}" {T}/>'
        f'<path d="M120 380 q0 -60 60 -60 M120 380 v120" fill="none" stroke="{SKY}" stroke-width="22" stroke-linecap="round"/>',
    "patient-lift": f'<path d="M240 500 L560 500 M300 500 L300 160 L560 160 M300 230 L380 160 M560 160 v60" fill="none" {S}/>'
        f'<circle cx="240" cy="510" r="14" fill="{NAVY}"/><circle cx="560" cy="510" r="14" fill="{NAVY}"/><circle cx="320" cy="510" r="14" fill="{NAVY}"/>'
        f'<rect x="282" y="300" width="36" height="120" rx="12" fill="{TEAL}"/>'
        f'<path d="M520 220 h80 M520 220 L500 380 Q560 430 620 380 L600 220" fill="{SKY}" {T}/>'
        f'<path d="M500 380 Q560 430 620 380" fill="none" stroke="{AMBER}" stroke-width="10" stroke-linecap="round"/>',
    "lift-chair": f'<path d="M260 420 q-40 0 -40 -60 v-180 q0 -40 50 -40 h260 q50 0 50 40 v180 q0 60 -40 60z" fill="{TEAL}" {S}/>'
        f'<rect x="270" y="190" width="260" height="130" rx="40" fill="{WHITE}" {T}/><rect x="250" y="330" width="300" height="70" rx="26" fill="{WHITE}" {T}/>'
        f'<path d="M300 420 l-20 80 M500 420 l20 80" {S}/><rect x="580" y="380" width="44" height="80" rx="12" fill="{WHITE}" {T}/><circle cx="602" cy="405" r="7" fill="{AMBER}"/>',
    "glucose-meter": f'<rect x="300" y="160" width="200" height="320" rx="44" fill="{WHITE}" {S}/><rect x="330" y="200" width="140" height="110" rx="16" fill="{SKY}" {T}/>'
        f'<text x="400" y="272" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="54" font-weight="700" fill="{NAVY}">104</text>'
        f'<circle cx="360" cy="380" r="20" fill="{TEAL}"/><circle cx="440" cy="380" r="20" fill="{TEAL}"/><rect x="370" y="480" width="60" height="70" rx="6" fill="{AMBER}"/>',
    "test-strips": f'<rect x="250" y="190" width="220" height="300" rx="30" fill="{WHITE}" {S}/><rect x="250" y="190" width="220" height="70" rx="30" fill="{TEAL}"/>'
        f'<path d="M290 320 h140 M290 360 h100" {T}/>'
        + "".join(f'<rect x="{500+i*36}" y="{230+i*30}" width="26" height="200" rx="6" fill="{WHITE}" {T} transform="rotate({8+i*6} {513+i*36} {330+i*30})"/>' for i in range(3)),
}


def svg(slug):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600" role="img" aria-label="Illustration">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{MINT}"/><stop offset="1" stop-color="{SKY}"/></linearGradient></defs>
<rect width="800" height="600" fill="url(#bg)"/><circle cx="640" cy="120" r="150" fill="{WHITE}" opacity=".55"/><circle cx="130" cy="520" r="90" fill="{TEAL}" opacity=".08"/>
<ellipse cx="400" cy="530" rx="300" ry="26" fill="{NAVY}" opacity=".08"/>
{ART[slug]}
</svg>
'''


if __name__ == "__main__":
    os.makedirs("art", exist_ok=True)
    for s in ART:
        open(f"art/{s}.svg", "w").write(svg(s))
    print(f"wrote {len(ART)} illustrations")
