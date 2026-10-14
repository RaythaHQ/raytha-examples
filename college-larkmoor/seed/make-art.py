#!/usr/bin/env python3
"""Draw the Larkmoor College artwork into ./art: faculty portrait tiles, illustrated covers for campus places, news and teams,
and small one-page PDFs for resources. Everything is generated, so it is free to reuse."""
import hashlib, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "art"); os.makedirs(OUT, exist_ok=True)
PAL = [("#5c1a26", "#c4707b"), ("#24493d", "#9cc7b2"), ("#2f4260", "#a8bfdc"), ("#7a5418", "#e7c27a"),
       ("#4a3157", "#c7afd6"), ("#1d5560", "#93cfd6"), ("#6d1f2b", "#e0a95a"), ("#33402a", "#c9d6a6")]
def h(s, n): return int(hashlib.md5(s.encode()).hexdigest(), 16) % n

def portrait(name, slug):
    a, b = PAL[h(name, len(PAL))]
    ini = "".join(p[0] for p in name.split()[:2]).upper()
    r = h(name + "r", 360); skin = ["#f1c7a5", "#e0ac83", "#c68a62", "#a86b45", "#7a4a2c", "#f6d7bf"][h(name + "s", 6)]
    hair = ["#1f1a17", "#3b2a20", "#6b4226", "#a8742f", "#2d2d2d", "#c9c2b8"][h(name + "h", 6)]
    style = h(name + "st", 3)
    hairpath = ['<path d="M70 118c0-46 26-70 60-70s60 24 60 70c-8-22-28-36-60-36s-52 14-60 36z" fill="%s"/>',
                '<path d="M64 140c-6-60 22-94 66-94s72 34 66 94c-6-30-12-52-20-60-14 8-30 12-46 12s-32-4-46-12c-8 8-14 30-20 60z" fill="%s"/>',
                '<path d="M74 112c4-40 28-60 56-60s52 20 56 60c-16-10-34-16-56-16s-40 6-56 16z" fill="%s"/>'][style] % hair
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 260"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs>
<rect width="260" height="260" fill="url(#g)"/><circle cx="{40 + r % 180}" cy="{30 + r % 60}" r="70" fill="#fff" opacity=".08"/>
<path d="M30 260c6-58 46-86 100-86s94 28 100 86z" fill="#f7f1e6" opacity=".95"/><path d="M104 176l26 34 26-34" fill="none" stroke="{a}" stroke-width="7"/>
<path d="M30 260c6-58 46-86 100-86s94 28 100 86z" fill="{a}" opacity=".35"/>
<rect x="112" y="150" width="36" height="34" rx="12" fill="{skin}"/><ellipse cx="130" cy="118" rx="50" ry="56" fill="{skin}"/>
{hairpath}<circle cx="112" cy="122" r="4.5" fill="#1f1a17"/><circle cx="148" cy="122" r="4.5" fill="#1f1a17"/>
<path d="M116 146q14 10 28 0" stroke="#1f1a17" stroke-width="4" fill="none" stroke-linecap="round" opacity=".7"/>
<text x="236" y="244" text-anchor="end" font-family="Arial,sans-serif" font-weight="700" font-size="22" fill="#fff" opacity=".6">{ini}</text></svg>'''
    open(os.path.join(OUT, f"p-{slug}.svg"), "w").write(svg)

def win(x, y, cols, rows, w=26, hgt=34, gx=18, gy=22, fill="#f6e7c4", op=".85", arch=False):
    s = ""
    for i in range(cols):
        for j in range(rows):
            X, Y = x + i * (w + gx), y + j * (hgt + gy)
            if arch: s += f'<path d="M{X} {Y+hgt}V{Y+w/2}a{w/2} {w/2} 0 0 1 {w} 0V{Y+hgt}z" fill="{fill}" opacity="{op}"/>'
            else: s += f'<rect x="{X}" y="{Y}" width="{w}" height="{hgt}" rx="3" fill="{fill}" opacity="{op}"/>'
    return s

def building(kind, a, b, rnd):
    stone, roof, trim = "#efe4d2", a, "#fbf6ec"
    g = []
    if kind == "hall":  # collegiate hall with clock tower
        g.append(f'<rect x="300" y="300" width="600" height="230" fill="{stone}"/><path d="M280 304 L600 220 L920 304Z" fill="{roof}"/>')
        g.append(f'<rect x="545" y="120" width="110" height="410" fill="{stone}"/><path d="M530 124 L600 40 L670 124Z" fill="{roof}"/>')
        g.append(f'<circle cx="600" cy="190" r="34" fill="{trim}" stroke="{roof}" stroke-width="6"/><path d="M600 190V168M600 190l16 8" stroke="{roof}" stroke-width="5" stroke-linecap="round"/>')
        g.append(win(330, 340, 4, 3, arch=True) + win(700, 340, 4, 3, arch=True) + f'<path d="M570 530V460a30 30 0 0 1 60 0v70z" fill="{roof}" opacity=".85"/>')
    elif kind == "science":
        g.append(f'<rect x="250" y="280" width="700" height="250" rx="6" fill="{stone}"/>' + win(280, 310, 11, 3, w=44, hgt=40, gx=16, gy=26, fill="#cfe6ef", op=".95"))
        g.append(f'<path d="M640 280 L700 200 L900 200 L900 280Z" fill="#dff1e6" stroke="{roof}" stroke-width="4"/><path d="M700 200V280M760 200V280M820 200V280" stroke="{roof}" stroke-width="3"/>')
        g.append(f'<rect x="250" y="270" width="700" height="14" fill="{roof}"/>')
    elif kind == "library":
        g.append(f'<rect x="300" y="250" width="600" height="280" fill="{stone}"/><path d="M270 254 L600 150 L930 254Z" fill="{roof}"/><rect x="290" y="250" width="620" height="18" fill="{trim}"/>')
        g.append("".join(f'<rect x="{340+i*80}" y="285" width="26" height="245" fill="{trim}"/>' for i in range(8)))
        g.append(f'<rect x="280" y="512" width="640" height="18" fill="{trim}"/><path d="M570 530V430h60v100z" fill="{roof}" opacity=".85"/>')
    elif kind == "commons":
        g.append(f'<rect x="240" y="320" width="720" height="210" rx="10" fill="{stone}"/><path d="M220 330 Q600 230 980 330Z" fill="{roof}"/>' + win(270, 360, 9, 2, w=56, hgt=50, gx=22, gy=30, fill="#f6e7c4", op=".95"))
        g.append(f'<rect x="520" y="440" width="160" height="90" rx="6" fill="{roof}" opacity=".85"/>')
    elif kind == "dorm":
        g.append(f'<rect x="330" y="200" width="540" height="330" fill="{stone}"/><rect x="320" y="190" width="560" height="18" fill="{roof}"/>' + win(360, 230, 8, 5, w=36, hgt=34, gx=29, gy=24))
        g.append(f'<path d="M570 530V470h60v60z" fill="{roof}"/>')
    elif kind == "arts":
        g.append(f'<path d="M260 530V300 Q600 160 940 300V530Z" fill="{stone}"/><path d="M260 300 Q600 160 940 300" fill="none" stroke="{roof}" stroke-width="14"/>')
        g.append(win(320, 360, 8, 1, w=50, hgt=120, gx=22, fill="#f6d9a8", op=".95", arch=True) + f'<rect x="540" y="500" width="120" height="30" fill="{roof}"/>')
    elif kind == "fieldhouse":
        g.append(f'<path d="M220 530V330 Q600 200 980 330V530Z" fill="{stone}"/><path d="M220 330 Q600 200 980 330" fill="none" stroke="{roof}" stroke-width="18"/>')
        g.append(win(260, 380, 10, 1, w=50, hgt=60, gx=20, fill="#cfe6ef", op=".95") + f'<rect x="500" y="460" width="200" height="70" fill="{roof}" opacity=".9"/>')
    elif kind == "wellbeing":
        g.append(f'<rect x="300" y="290" width="600" height="240" rx="14" fill="{stone}"/><path d="M290 296 L600 230 L910 296Z" fill="{roof}"/>' + win(340, 330, 7, 2, w=48, hgt=50, gx=30, gy=34, fill="#f6e7c4", op=".95"))
        g.append(f'<circle cx="600" cy="262" r="16" fill="{trim}"/>')
    elif kind == "field":
        g.append(f'<path d="M0 420 L1200 420 L1200 630 L0 630Z" fill="#3f7d4f"/>' + "".join(f'<path d="M{i*150} 630 L{300+i*100} 420" stroke="#fff" stroke-width="2" opacity=".18"/>' for i in range(9)))
        g.append('<path d="M150 600 L420 440 L780 440 L1050 600Z" fill="none" stroke="#fff" stroke-width="5" opacity=".75"/><ellipse cx="600" cy="510" rx="90" ry="34" fill="none" stroke="#fff" stroke-width="5" opacity=".75"/>')
        g.append(f'<path d="M520 440 V400 H680 V440" fill="none" stroke="#fff" stroke-width="6"/><rect x="60" y="300" width="300" height="120" fill="{stone}" opacity=".85"/>' + "".join(f'<rect x="{80+i*44}" y="320" width="30" height="80" fill="{a}" opacity=".5"/>' for i in range(6)))
        g.append('<path d="M980 140v280M1040 140v280" stroke="#e8e2d6" stroke-width="8"/><rect x="960" y="120" width="100" height="36" rx="6" fill="#fff8d8"/>')
    return "".join(g)

def cover(slug, title, kind):
    a, b = PAL[h(slug, len(PAL))]
    rnd = [h(slug + str(i), 1000) / 1000 for i in range(40)]
    shapes = []
    if kind in ("hall", "science", "library", "commons", "dorm", "arts", "fieldhouse", "wellbeing", "field"):
        shapes.append(f'<circle cx="{900 + rnd[0]*200:.0f}" cy="{110 + rnd[1]*40:.0f}" r="56" fill="#fff4d6" opacity=".7"/>')
        shapes.append('<path d="M0 470 Q 300 390 600 440 T 1200 410 V630 H0Z" fill="#fff" opacity=".12"/>')
        shapes.append(building(kind, a, b, rnd))
        if kind != "field":
            shapes.append('<path d="M0 530 H1200 V630 H0Z" fill="#4f7d4a"/><path d="M0 560 Q600 520 1200 560 V630 H0Z" fill="#5e8f56"/>')
            for t in range(5):
                x = 60 + t * 50 + rnd[t] * 20; s = 30 + rnd[t + 9] * 20
                shapes.append(f'<rect x="{x-4:.0f}" y="{530-s*0.4:.0f}" width="8" height="{s*0.5:.0f}" fill="#4a3426"/><circle cx="{x:.0f}" cy="{520-s:.0f}" r="{s:.0f}" fill="#2f6b45" opacity=".9"/>')
                x2 = 1140 - t * 48 - rnd[t + 3] * 20
                shapes.append(f'<rect x="{x2-4:.0f}" y="{530-s*0.4:.0f}" width="8" height="{s*0.5:.0f}" fill="#4a3426"/><circle cx="{x2:.0f}" cy="{520-s:.0f}" r="{s:.0f}" fill="#3b7a50" opacity=".9"/>')
    elif kind == "waves":
        for i in range(7):
            y = 120 + i * 48; amp = 18 + rnd[i] * 30
            shapes.append(f'<path d="M0 {y} C 200 {y-amp}, 400 {y+amp}, 600 {y} S 1000 {y-amp}, 1200 {y} V 630 H 0 Z" fill="#fff" opacity="{0.05 + i*0.025:.3f}"/>')
    elif kind == "grid":
        for i in range(14):
            for j in range(7):
                if rnd[(i*7+j) % 40] > .55:
                    shapes.append(f'<rect x="{60+i*80}" y="{60+j*80}" width="56" height="56" rx="14" fill="#fff" opacity="{.06+rnd[(i+j)%40]*.22:.2f}"/>')
    elif kind == "rings":
        cx, cy = 820 + rnd[0]*200, 300 + rnd[1]*100
        for i in range(9): shapes.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{40+i*46}" fill="none" stroke="#fff" stroke-width="{10-i*0.8:.1f}" opacity="{.28-i*.025:.3f}"/>')
        shapes.append('<path d="M0 500 C 300 460, 500 560, 800 500 S 1100 470, 1200 500 V630 H0Z" fill="#fff" opacity=".18"/>')
    elif kind == "bars":
        for i in range(16):
            ht = 80 + rnd[i] * 380
            shapes.append(f'<rect x="{80+i*68}" y="{560-ht:.0f}" width="40" height="{ht:.0f}" rx="12" fill="#fff" opacity="{.08+rnd[i+16]*.2:.2f}"/>')
    else:  # dots
        for i in range(36):
            shapes.append(f'<circle cx="{rnd[i]*1200:.0f}" cy="{rnd[(i+7)%40]*630:.0f}" r="{12+rnd[(i+3)%40]*70:.0f}" fill="#fff" opacity="{.05+rnd[(i+11)%40]*.15:.2f}"/>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>
<radialGradient id="r" cx=".85" cy=".1" r=".9"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>
<rect width="1200" height="630" fill="url(#g)"/><rect width="1200" height="630" fill="url(#r)"/>{''.join(shapes)}</svg>'''
    open(os.path.join(OUT, f"c-{slug}.svg"), "w").write(svg)

def pdf(slug, title, lines, sub=""):
    """A small, valid one-page PDF with a header band and text lines (Helvetica)."""
    def pe(s): return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    ops = ["0.427 0.122 0.169 rg 0 742 612 50 re f", "1 1 1 rg BT /F2 18 Tf 48 760 Td (" + pe("Larkmoor College") + ") Tj ET",
           "1 1 1 rg BT /F1 10 Tf 430 762 Td (" + pe("Fictional demo document") + ") Tj ET",
           "0.11 0.10 0.13 rg BT /F2 20 Tf 48 700 Td (" + pe(title[:60]) + ") Tj ET",
           "0.79 0.60 0.23 rg 48 688 60 3 re f", "0.4 0.4 0.45 rg BT /F1 10 Tf 48 670 Td (" + pe(sub[:110]) + ") Tj ET"]
    y = 640
    for ln in lines:
        bold = ln.startswith("#"); t = ln.lstrip("# ")
        ops.append(f"0.18 0.16 0.2 rg BT /{'F2' if bold else 'F1'} {12 if bold else 10.5} Tf 48 {y} Td ({pe(t[:95])}) Tj ET")
        y -= 22 if bold else 16
        if y < 60: break
    ops.append("0.5 0.5 0.55 rg BT /F1 8 Tf 48 36 Td (" + pe("Larkmoor College is fictional and not a real college. Demo document for a Raytha example site.") + ") Tj ET")
    stream = "\n".join(ops).encode("latin-1", "replace")
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>", b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>",
            b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream"]
    out = b"%PDF-1.4\n"; offs = []
    for i, o in enumerate(objs):
        offs.append(len(out)); out += b"%d 0 obj\n" % (i + 1) + o + b"\nendobj\n"
    x = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1) + b"".join(b"%010d 00000 n \n" % o for o in offs)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, x)
    open(os.path.join(OUT, f"d-{slug}.pdf"), "wb").write(out)

spec = json.load(open(os.path.join(HERE, "art-spec.json")))
for p in spec["people"]: portrait(p["name"], p["slug"])
for c in spec["covers"]: cover(c["slug"], c.get("title", ""), c["kind"])
for d in spec["docs"]: pdf(d["slug"], d["title"], d["lines"], d.get("sub", ""))
print(len(os.listdir(OUT)), "files in", OUT)
