#!/usr/bin/env python3
"""Draw the Halverline Studio artwork into ./art: team portraits, client wordmarks, case study covers (browser and phone
mockups in each client's colors), design-system boards, insight covers and small one-page PDFs for the client portal.
Everything is generated, so it is free to reuse."""
import hashlib, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "art"); os.makedirs(OUT, exist_ok=True)
def h(s, n): return int(hashlib.md5(s.encode()).hexdigest(), 16) % n
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")
FONTS = {"serif": "Georgia,'DejaVu Serif',serif", "sans": "'Helvetica Neue',Arial,'DejaVu Sans',sans-serif", "slab": "Rockwell,'Courier New','DejaVu Sans Mono',monospace"}
PAL = [("#1a1a1a", "#ff5b2e"), ("#1f2a44", "#9db4ff"), ("#3b2f2a", "#f0b27a"), ("#20403a", "#9ee0c7"), ("#3a2350", "#d3b8ff"), ("#40201a", "#ffb199")]

def glyph(kind, c1, c2, x, y, s):
    k = s / 40
    g = {"wave": f'<circle cx="20" cy="20" r="20" fill="{c1}"/><path d="M4 22q4-5 8 0t8 0 8 0 8 0" stroke="{c2}" stroke-width="3.2" fill="none" stroke-linecap="round"/><path d="M6 29q3.5-4 7 0t7 0 7 0 7 0" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" opacity=".8"/>',
         "hex": f'<path d="M20 1l17 10v18L20 39 3 29V11z" fill="{c1}"/><path d="M20 10l9 5v10l-9 5-9-5V15z" fill="none" stroke="{c2}" stroke-width="3"/>',
         "arch": f'<path d="M3 39V19a17 17 0 0 1 34 0v20z" fill="{c1}"/><path d="M12 39V22a8 8 0 0 1 16 0v17" fill="none" stroke="{c2}" stroke-width="3"/>',
         "book": f'<rect x="1" y="1" width="38" height="38" rx="10" fill="{c1}"/><path d="M8 12q6-3 12 1q6-4 12-1v17q-6-3-12 1q-6-4-12-1z" fill="{c2}"/><path d="M20 13v17" stroke="{c1}" stroke-width="2"/>',
         "drop": f'<circle cx="20" cy="20" r="19" fill="{c1}"/><path d="M20 7c6 8 9 13 9 17a9 9 0 0 1-18 0c0-4 3-9 9-17z" fill="{c2}"/>',
         "pillar": f'<rect x="1" y="1" width="38" height="38" fill="{c1}"/><path d="M8 13h24M10 31h20M12 15v14M20 15v14M28 15v14" stroke="{c2}" stroke-width="2.6"/><path d="M8 13l12-6 12 6" fill="none" stroke="{c2}" stroke-width="2.6"/>',
         "hook": f'<rect x="1" y="1" width="38" height="38" rx="19" fill="{c1}"/><path d="M24 8v15a6 6 0 0 1-12 0" fill="none" stroke="{c2}" stroke-width="4" stroke-linecap="round"/>',
         "leaf": f'<circle cx="20" cy="20" r="19" fill="{c1}"/><path d="M10 30c0-12 8-20 21-21-1 13-9 21-21 21z" fill="{c2}"/><path d="M11 29L25 15" stroke="{c1}" stroke-width="2"/>',
         "sprout": f'<rect x="1" y="1" width="38" height="38" rx="8" fill="{c1}"/><path d="M20 32V18M20 20c-6 0-9-4-9-9 6 0 9 4 9 9zm0 2c5 0 8-3 8-8-5 0-8 3-8 8z" fill="{c2}" stroke="{c2}" stroke-width="2"/>',
         "ring": f'<circle cx="20" cy="20" r="19" fill="{c1}"/><circle cx="20" cy="20" r="10" fill="none" stroke="{c2}" stroke-width="4"/>'}[kind]
    return f'<g transform="translate({x} {y}) scale({k})">{g}</g>'

def logo(sp):
    n, f = sp["name"], FONTS[sp["font"]]
    words = n.split(); top = words[0]; rest = " ".join(words[1:])
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 120"><rect width="360" height="120" fill="none"/>' + glyph(sp["glyph"], sp["c1"], sp["c2"], 18, 34, 52) +
           f'<text x="84" y="{66 if not rest else 60}" font-family="{f}" font-size="27" font-weight="700" fill="{sp["c1"]}" letter-spacing="-.3">{esc(top)}</text>' +
           (f'<text x="85" y="84" font-family="{f}" font-size="13" font-weight="600" fill="{sp["c1"]}" opacity=".72" letter-spacing="1.6">{esc(rest.upper())}</text>' if rest else "") + '</svg>')
    open(os.path.join(OUT, f"l-{sp['slug']}.svg"), "w").write(svg)

def portrait(name, slug):
    a, b = PAL[h(name, len(PAL))]
    ini = "".join(p[0] for p in name.split()[:2]).upper()
    skin = ["#f1c7a5", "#e0ac83", "#c68a62", "#a86b45", "#7a4a2c", "#f6d7bf"][h(name + "s", 6)]
    hair = ["#1f1a17", "#3b2a20", "#6b4226", "#a8742f", "#2d2d2d", "#c9c2b8"][h(name + "h", 6)]
    style = h(name + "st", 3)
    hp = ['<path d="M70 118c0-46 26-70 60-70s60 24 60 70c-8-22-28-36-60-36s-52 14-60 36z" fill="%s"/>',
          '<path d="M64 140c-6-60 22-94 66-94s72 34 66 94c-6-30-12-52-20-60-14 8-30 12-46 12s-32-4-46-12c-8 8-14 30-20 60z" fill="%s"/>',
          '<path d="M74 112c4-40 28-60 56-60s52 20 56 60c-16-10-34-16-56-16s-40 6-56 16z" fill="%s"/>'][style] % hair
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 300"><rect width="260" height="300" fill="{b}"/>
<circle cx="{60 + h(name,140)}" cy="70" r="90" fill="#fff" opacity=".18"/><rect x="0" y="210" width="260" height="90" fill="{a}" opacity=".08"/>
<path d="M30 300c6-62 46-92 100-92s94 30 100 92z" fill="{a}"/><path d="M108 210l22 30 22-30" fill="none" stroke="#fff" stroke-width="5" opacity=".7"/>
<rect x="112" y="168" width="36" height="40" rx="12" fill="{skin}"/><ellipse cx="130" cy="132" rx="50" ry="56" fill="{skin}"/>
{hp}<circle cx="112" cy="136" r="4.5" fill="#1f1a17"/><circle cx="148" cy="136" r="4.5" fill="#1f1a17"/>
<path d="M116 160q14 10 28 0" stroke="#1f1a17" stroke-width="4" fill="none" stroke-linecap="round" opacity=".7"/>
<text x="240" y="286" text-anchor="end" font-family="Arial,sans-serif" font-weight="700" font-size="20" fill="#fff" opacity=".75">{ini}</text></svg>'''
    open(os.path.join(OUT, f"p-{slug}.svg"), "w").write(svg)

def mock_page(sp, x, y, w, hgt, phone=False):
    """An abstract web page in the client's colors."""
    c1, c2, f = sp["c1"], sp["c2"], FONTS[sp["font"]]
    r = [h(sp["slug"] + str(i), 1000) / 1000 for i in range(30)]
    s = f'<g transform="translate({x} {y})"><rect width="{w}" height="{hgt}" fill="#fbfaf7"/>'
    nav = 44 if not phone else 40
    s += f'<rect width="{w}" height="{nav}" fill="#fff"/><rect y="{nav-1}" width="{w}" height="1" fill="#e6e2da"/>' + glyph(sp["glyph"], c1, c2, 16, (nav - 24) / 2, 24)
    s += f'<text x="48" y="{nav/2+5}" font-family="{f}" font-size="14" font-weight="700" fill="{c1}">{esc(sp["name"].split()[0])}</text>'
    if not phone:
        s += "".join(f'<rect x="{w-360+i*62}" y="{nav/2-3}" width="44" height="6" rx="3" fill="#cfc9be"/>' for i in range(4)) + f'<rect x="{w-104}" y="{nav/2-12}" width="88" height="24" rx="12" fill="{c2}"/>'
    else:
        s += f'<path d="M{w-34} {nav/2-6}h18M{w-34} {nav/2}h18M{w-34} {nav/2+6}h18" stroke="{c1}" stroke-width="2.4"/>'
    hy = nav; hh = hgt * (0.52 if not phone else 0.46)
    s += f'<rect y="{hy}" width="{w}" height="{hh}" fill="{c1}"/>'
    s += f'<circle cx="{w*(0.78 if not phone else 0.85)}" cy="{hy+hh*0.45}" r="{hh*0.38}" fill="{c2}" opacity=".9"/><circle cx="{w*(0.7 if not phone else 0.7)}" cy="{hy+hh*0.7}" r="{hh*0.2}" fill="#fff" opacity=".14"/>'
    tx = 26 if phone else 48
    hl = sp["headline"].split()
    lines, cur = [], ""
    lim = 16 if phone else 26
    for wd in hl:
        if len(cur) + len(wd) + 1 > lim: lines.append(cur); cur = wd
        else: cur = (cur + " " + wd).strip()
    lines.append(cur); lines = lines[:3]
    fs = 19 if phone else 30
    for i, ln in enumerate(lines):
        s += f'<text x="{tx}" y="{hy+46+i*(fs+8)}" font-family="{f}" font-size="{fs}" font-weight="700" fill="#fff">{esc(ln)}</text>'
    by = hy + 46 + len(lines) * (fs + 8) + 4
    s += f'<rect x="{tx}" y="{by}" width="{w*0.32 if not phone else w*0.6}" height="7" rx="3.5" fill="#fff" opacity=".55"/><rect x="{tx}" y="{by+16}" width="{w*0.26 if not phone else w*0.5}" height="7" rx="3.5" fill="#fff" opacity=".4"/>'
    s += f'<rect x="{tx}" y="{by+38}" width="{110 if not phone else 96}" height="30" rx="15" fill="{c2}"/>'
    cy = hy + hh + 22
    cols = 3 if not phone else 1
    cw = (w - tx * 2 - (cols - 1) * 18) / cols
    for i in range(cols if not phone else 2):
        cx = tx + i * (cw + 18) if not phone else tx
        yy = cy if not phone else cy + i * 120
        ch = (hgt - cy - 20) if not phone else 104
        if yy + 40 > hgt: break
        s += f'<rect x="{cx}" y="{yy}" width="{cw}" height="{ch}" rx="10" fill="#fff" stroke="#e6e2da"/>'
        s += f'<rect x="{cx}" y="{yy}" width="{cw}" height="{min(ch*0.5, 70)}" rx="10" fill="{[c2, c1, "#d9d3c7"][i % 3]}" opacity="{0.85 if i % 3 != 1 else 0.9}"/>'
        s += f'<rect x="{cx+14}" y="{yy+min(ch*0.5,70)+14}" width="{cw*0.6}" height="8" rx="4" fill="#2b2b2b" opacity=".75"/><rect x="{cx+14}" y="{yy+min(ch*0.5,70)+30}" width="{cw*0.8}" height="6" rx="3" fill="#bdb6a9"/>'
    return s + '</g>'

def case_cover(sp):
    c1, c2 = sp["c1"], sp["c2"]
    W, H = 1600, 1000
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c2}"/><stop offset="1" stop-color="{c2}" stop-opacity=".55"/></linearGradient>'
    s += '<filter id="sh" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="24" stdDeviation="26" flood-color="#000" flood-opacity=".28"/></filter><clipPath id="cb"><rect x="190" y="190" width="1060" height="660" rx="6"/></clipPath><clipPath id="cp"><rect x="1166" y="380" width="250" height="520" rx="26"/></clipPath></defs>'
    s += f'<rect width="{W}" height="{H}" fill="#f1ede6"/><rect width="{W}" height="{H}" fill="url(#bg)" opacity=".75"/>'
    s += f'<circle cx="1400" cy="160" r="300" fill="{c1}" opacity=".16"/><circle cx="160" cy="900" r="240" fill="#fff" opacity=".22"/>'
    s += f'<g filter="url(#sh)"><rect x="170" y="150" width="1100" height="720" rx="18" fill="#fff"/></g><rect x="170" y="150" width="1100" height="40" rx="18" fill="#efebe4"/><rect x="170" y="172" width="1100" height="18" fill="#efebe4"/>'
    s += ''.join(f'<circle cx="{198+i*22}" cy="170" r="6" fill="{c}"/>' for i, c in enumerate(["#ff6159", "#ffbd2e", "#28c941"]))
    s += f'<rect x="420" y="160" width="600" height="20" rx="10" fill="#fff"/><text x="720" y="175" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" fill="#8a847a">{sp["slug"].split("-")[0]}.example</text>'
    s += f'<g clip-path="url(#cb)">{mock_page(sp, 190, 190, 1060, 660)}</g>'
    s += f'<g filter="url(#sh)"><rect x="1150" y="360" width="282" height="556" rx="40" fill="#151515"/></g><g clip-path="url(#cp)">{mock_page(sp, 1166, 380, 250, 520, phone=True)}</g>'
    s += '</svg>'
    open(os.path.join(OUT, f"w-{sp['slug']}.svg"), "w").write(s)

def board(sp):
    """A design-system board: palette, type specimen and components."""
    c1, c2, f = sp["c1"], sp["c2"], FONTS[sp["font"]]
    W, H = 1600, 1000
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="#f6f3ee"/>'
    s += f'<text x="90" y="120" font-family="Arial,sans-serif" font-size="20" font-weight="700" fill="#77706a" letter-spacing="3">DESIGN SYSTEM  ·  {esc(sp["name"].upper())}</text>'
    for i, (col, lab) in enumerate([(c1, c1), (c2, c2), ("#1c1c1c", "#1C1C1C"), ("#ffffff", "#FFFFFF"), ("#e6e1d8", "#E6E1D8")]):
        x = 90 + i * 150
        s += f'<rect x="{x}" y="170" width="130" height="170" rx="14" fill="{col}" stroke="#d8d2c8"/><text x="{x+14}" y="320" font-family="Arial,sans-serif" font-size="14" font-weight="700" fill="{"#fff" if i in (0, 2) else "#333"}">{lab.upper()}</text>'
    s += f'<text x="90" y="520" font-family="{f}" font-size="150" font-weight="700" fill="{c1}">Aa</text>'
    s += f'<text x="360" y="440" font-family="{f}" font-size="34" font-weight="700" fill="#1c1c1c">{esc(sp["headline"][:34])}</text>'
    s += f'<text x="360" y="486" font-family="{f}" font-size="20" fill="#5a544e">Headings and body text, tested at 390 px</text><text x="360" y="520" font-family="{f}" font-size="20" fill="#5a544e">ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789</text>'
    s += f'<rect x="90" y="600" width="210" height="58" rx="29" fill="{c2}"/><text x="195" y="636" text-anchor="middle" font-family="Arial,sans-serif" font-size="19" font-weight="700" fill="{c1}">Primary action</text>'
    s += f'<rect x="320" y="600" width="210" height="58" rx="29" fill="none" stroke="{c1}" stroke-width="2.5"/><text x="425" y="636" text-anchor="middle" font-family="Arial,sans-serif" font-size="19" font-weight="700" fill="{c1}">Secondary</text>'
    s += f'<rect x="90" y="700" width="440" height="200" rx="18" fill="#fff" stroke="#ddd6cb"/><rect x="90" y="700" width="440" height="90" rx="18" fill="{c1}"/><rect x="90" y="770" width="440" height="20" fill="{c1}"/><rect x="114" y="814" width="260" height="14" rx="7" fill="#333"/><rect x="114" y="842" width="360" height="10" rx="5" fill="#c3bcb0"/><rect x="114" y="862" width="300" height="10" rx="5" fill="#c3bcb0"/>'
    s += f'<rect x="900" y="170" width="610" height="730" rx="22" fill="{c1}"/>' + glyph(sp["glyph"], "#ffffff", c2, 1110, 330, 200)
    s += f'<text x="1205" y="660" text-anchor="middle" font-family="{f}" font-size="46" font-weight="700" fill="#fff">{esc(sp["name"].split()[0])}</text>'
    s += ''.join(f'<rect x="{960+i*100}" y="760" width="80" height="80" rx="14" fill="#fff" opacity="{.1+i*.15:.2f}"/>' for i in range(5))
    s += '</svg>'
    open(os.path.join(OUT, f"m-{sp['slug']}.svg"), "w").write(s)

CATC = {"design": ("#ff5b2e", "#ffd2c2"), "engineering": ("#2b3cff", "#c9cdff"), "content": ("#0f7a5c", "#bfe9d9"), "accessibility": ("#7a2bd6", "#e0cbff"), "studio": ("#1a1a1a", "#e9e3d8")}
def cover(slug, kind, cat):
    a, b = CATC.get(cat, ("#1a1a1a", "#e9e3d8"))
    r = [h(slug + str(i), 1000) / 1000 for i in range(40)]
    sh = []
    if kind == "rings":
        cx, cy = 820 + r[0] * 200, 300 + r[1] * 100
        for i in range(9): sh.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{40+i*46}" fill="none" stroke="{a}" stroke-width="{10-i*0.8:.1f}" opacity="{.6-i*.05:.2f}"/>')
    elif kind == "grid":
        for i in range(14):
            for j in range(7):
                if r[(i * 7 + j) % 40] > .5: sh.append(f'<rect x="{60+i*80}" y="{60+j*80}" width="56" height="56" rx="{4 if (i+j)%3 else 28}" fill="{a}" opacity="{.15+r[(i+j)%40]*.7:.2f}"/>')
    elif kind == "bars":
        for i in range(16):
            ht = 80 + r[i] * 380; sh.append(f'<rect x="{80+i*68}" y="{560-ht:.0f}" width="40" height="{ht:.0f}" rx="20" fill="{a}" opacity="{.25+r[i+16]*.6:.2f}"/>')
    elif kind == "waves":
        for i in range(7):
            y = 140 + i * 56; amp = 22 + r[i] * 34
            sh.append(f'<path d="M0 {y} C 200 {y-amp}, 400 {y+amp}, 600 {y} S 1000 {y-amp}, 1200 {y}" fill="none" stroke="{a}" stroke-width="{4+i}" opacity="{.25+i*.1:.2f}"/>')
    else:
        for i in range(30): sh.append(f'<circle cx="{r[i]*1200:.0f}" cy="{r[(i+7)%40]*630:.0f}" r="{12+r[(i+3)%40]*70:.0f}" fill="{a}" opacity="{.15+r[(i+11)%40]*.5:.2f}"/>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630"><rect width="1200" height="630" fill="{b}"/>{"".join(sh)}</svg>'
    open(os.path.join(OUT, f"c-{slug}.svg"), "w").write(svg)

def pdf(slug, title, lines, sub=""):
    """A small, valid one-page PDF with a header band and text lines (Helvetica)."""
    def pe(s): return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    ops = ["0.07 0.07 0.07 rg 0 742 612 50 re f", "1 0.357 0.18 rg 0 738 612 4 re f", "1 1 1 rg BT /F2 18 Tf 48 760 Td (" + pe("Halverline Studio") + ") Tj ET",
           "1 1 1 rg BT /F1 10 Tf 420 762 Td (" + pe("Fictional demo document") + ") Tj ET",
           "0.11 0.10 0.10 rg BT /F2 20 Tf 48 700 Td (" + pe(title[:60]) + ") Tj ET",
           "1 0.357 0.18 rg 48 688 60 3 re f", "0.4 0.4 0.42 rg BT /F1 10 Tf 48 670 Td (" + pe(sub[:110]) + ") Tj ET"]
    y = 640
    for ln in lines:
        bold = ln.startswith("#"); t = ln.lstrip("# ")
        ops.append(f"0.16 0.16 0.17 rg BT /{'F2' if bold else 'F1'} {12 if bold else 10.5} Tf 48 {y} Td ({pe(t[:95])}) Tj ET")
        y -= 22 if bold else 16
        if y < 60: break
    ops.append("0.5 0.5 0.52 rg BT /F1 8 Tf 48 36 Td (" + pe("Halverline Studio and its clients are fictional. Demo document for a Raytha example site.") + ") Tj ET")
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
for l in spec["logos"]: logo(l)
for s in spec["shots"]: case_cover(s); board(s)
for c in spec["covers"]: cover(c["slug"], c["kind"], c["cat"])
for d in spec["docs"]: pdf(d["slug"], d["title"], d["lines"], d.get("sub", ""))
print(len(os.listdir(OUT)), "files in", OUT)
