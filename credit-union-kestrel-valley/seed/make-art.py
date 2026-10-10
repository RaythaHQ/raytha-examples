#!/usr/bin/env python3
"""Draw the Kestrel Valley Credit Union artwork into ./art: portrait tiles for volunteer directors, cover art for articles, news and branches,
and small PDF annual meeting materials, reports and disclosures. Everything is generated, so it is free to reuse."""
import hashlib, math, os, json, zlib
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "art"); os.makedirs(OUT, exist_ok=True)
PAL = [("#0c3b3a", "#4fa59a"), ("#14524f", "#a9d8cf"), ("#8a4a1c", "#e9b27a"), ("#2c4a6b", "#9cc0e0"),
       ("#0c3b3a", "#c8742c"), ("#3f5a3a", "#cbe0b4"), ("#5a3d5c", "#d8bfd6"), ("#6b3a1e", "#f2c9a0")]
def h(s, n): return int(hashlib.md5(s.encode()).hexdigest(), 16) % n
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")

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
<path d="M30 260c6-58 46-86 100-86s94 28 100 86z" fill="{b}" opacity=".9"/><path d="M30 260c6-58 46-86 100-86s94 28 100 86z" fill="#000" opacity=".18"/>
<rect x="112" y="150" width="36" height="34" rx="12" fill="{skin}"/><ellipse cx="130" cy="118" rx="50" ry="56" fill="{skin}"/>
{hairpath}<circle cx="112" cy="122" r="4.5" fill="#1f1a17"/><circle cx="148" cy="122" r="4.5" fill="#1f1a17"/>
<path d="M116 146q14 10 28 0" stroke="#1f1a17" stroke-width="4" fill="none" stroke-linecap="round" opacity=".7"/>
<text x="236" y="244" text-anchor="end" font-family="Inter,Arial,sans-serif" font-weight="700" font-size="22" fill="#fff" opacity=".55">{ini}</text></svg>'''
    open(os.path.join(OUT, f"p-{slug}.svg"), "w").write(svg)

def cover(slug, title, kind):
    a, b = PAL[h(slug, len(PAL))]
    rnd = [h(slug + str(i), 1000) / 1000 for i in range(40)]
    shapes = []
    if kind == "waves":
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
    elif kind == "bars":
        for i in range(16):
            ht = 80 + rnd[i] * 380
            shapes.append(f'<rect x="{80+i*68}" y="{560-ht:.0f}" width="40" height="{ht:.0f}" rx="12" fill="#fff" opacity="{.08+rnd[i+16]*.2:.2f}"/>')
    elif kind == "branch":
        shapes.append('<path d="M0 470 Q 300 400 600 450 T 1200 430 V630 H0Z" fill="#fff" opacity=".10"/><path d="M0 520 Q 400 470 800 510 T 1200 500 V630 H0Z" fill="#fff" opacity=".14"/>')
        bx = 330 + rnd[0]*200; w = 420; ht = 190 + rnd[1]*40
        shapes.append(f'<rect x="{bx:.0f}" y="{520-ht:.0f}" width="{w}" height="{ht:.0f}" fill="#fff" opacity=".9"/>')
        shapes.append(f'<path d="M{bx-30:.0f} {522-ht:.0f} L{bx+w/2:.0f} {430-ht:.0f} L{bx+w+30:.0f} {522-ht:.0f}Z" fill="#fff" opacity=".75"/>')
        for i in range(5): shapes.append(f'<rect x="{bx+30+i*80:.0f}" y="{560-ht:.0f}" width="44" height="64" rx="6" fill="{a}" opacity=".55"/>')
        shapes.append(f'<rect x="{bx+w/2-38:.0f}" y="{440:.0f}" width="76" height="80" rx="8" fill="{a}" opacity=".8"/>')
        shapes.append(f'<rect x="{bx+w+40:.0f}" y="410" width="150" height="110" fill="#fff" opacity=".55"/><rect x="{bx+w+40:.0f}" y="398" width="170" height="16" fill="#fff" opacity=".8"/>')
        for t in range(6): shapes.append(f'<circle cx="{60+t*48+rnd[t]*20:.0f}" cy="{470-rnd[t+5]*30:.0f}" r="{26+rnd[t+9]*16:.0f}" fill="{b}" opacity=".55"/>')
        shapes.append('<path d="M920 150c30-18 60-18 90 0c-30-6-60-6-90 0z M965 150l-10 22 20-22z" fill="#fff" opacity=".7"/>')
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
    ops = ["0.047 0.231 0.227 rg 0 742 612 50 re f", "1 1 1 rg BT /F2 18 Tf 48 760 Td (" + pe("Kestrel Valley Credit Union") + ") Tj ET",
           "1 1 1 rg BT /F1 10 Tf 410 762 Td (" + pe("Fictional demo document") + ") Tj ET",
           "0.09 0.11 0.15 rg BT /F2 20 Tf 48 700 Td (" + pe(title[:60]) + ") Tj ET",
           "0.78 0.45 0.17 rg 48 688 60 3 re f", "0.4 0.45 0.5 rg BT /F1 10 Tf 48 670 Td (" + pe(sub) + ") Tj ET"]
    y = 640
    for ln in lines:
        bold = ln.startswith("#"); t = ln.lstrip("# ")
        ops.append(f"0.2 0.24 0.3 rg BT /{'F2' if bold else 'F1'} {12 if bold else 10.5} Tf 48 {y} Td ({pe(t[:95])}) Tj ET")
        y -= 22 if bold else 16
        if y < 60: break
    ops.append("0.55 0.6 0.65 rg BT /F1 8 Tf 48 36 Td (" + pe("Kestrel Valley Credit Union is fictional and not a real financial institution. Demo document for a Raytha example site.") + ") Tj ET")
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
