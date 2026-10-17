#!/usr/bin/env python3
"""Architectural artwork for Marlowe Architecture: house elevations, courtyard plans, portrait, monograms, journal covers, PDFs. Generated, license-free."""
import hashlib, os, json
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,"art"); os.makedirs(OUT,exist_ok=True)
def h(s,n): return int(hashlib.md5(s.encode()).hexdigest(),16)%n
def esc(s): return s.replace("&","&amp;").replace("<","&lt;")
SERIF="Georgia,'DejaVu Serif',serif"; SANS="'Helvetica Neue',Arial,'DejaVu Sans',sans-serif"
def house(x,y,w,seed,wall="#efe6d4",roof="#3a3630",accent="#b4552d"):
    r=[h(seed+str(i),100)/100 for i in range(20)]
    s=f'<g transform="translate({x} {y})">'
    s+=f'<path d="M{-w*.08} {w*.62} L{w*.22} {w*.18} L{w*.55} {w*.58} L{w*.78} {w*.30} L{w*1.05} {w*.62} Z" fill="#d8c9a8" opacity=".55"/>'
    s+=f'<circle cx="{w*.82}" cy="{w*.08}" r="{w*.07}" fill="#e8a34c"/>'
    # main volume
    s+=f'<rect x="{w*.18}" y="{w*.34}" width="{w*.52}" height="{w*.30}" fill="{wall}" stroke="#2b2722" stroke-width="3"/>'
    s+=f'<path d="M{w*.14} {w*.34} L{w*.44} {w*.16} L{w*.74} {w*.34} Z" fill="{roof}"/>'
    s+=f'<rect x="{w*.62}" y="{w*.42}" width="{w*.28}" height="{w*.22}" fill="{wall}" stroke="#2b2722" stroke-width="3"/><path d="M{w*.60} {w*.42} L{w*.76} {w*.30} L{w*.92} {w*.42} Z" fill="{roof}"/>'
    # glass
    s+=f'<rect x="{w*.24}" y="{w*.42}" width="{w*.16}" height="{w*.22}" fill="#7fa3a8" stroke="#2b2722" stroke-width="2.5"/><rect x="{w*.46}" y="{w*.42}" width="{w*.10}" height="{w*.22}" fill="{accent}" stroke="#2b2722" stroke-width="2.5"/><rect x="{w*.68}" y="{w*.48}" width="{w*.16}" height="{w*.16}" fill="#7fa3a8" stroke="#2b2722" stroke-width="2.5"/>'
    # trees
    for tx,ts in [(0.08,1),(0.96,.8)]:
        s+=f'<path d="M{w*tx} {w*.64} L{w*tx} {w*.44}" stroke="#4a3b2c" stroke-width="5"/><circle cx="{w*tx}" cy="{w*.38}" r="{w*.075*ts}" fill="#6b7d4f"/><circle cx="{w*(tx+.05)}" cy="{w*.42}" r="{w*.055*ts}" fill="#7d8f5e"/>'
    s+=f'<line x1="{-w*.05}" y1="{w*.64}" x2="{w*1.05}" y2="{w*.64}" stroke="#2b2722" stroke-width="3"/>'
    s+=f'<path d="M{w*.05} {w*.64} q{w*.1} {-w*.06} {w*.2} 0 q{w*.1} {-w*.05} {w*.2} 0" fill="none" stroke="#6b7d4f" stroke-width="3"/>'
    return s+'</g>'
def cover_file(name,seed,subtitle):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1000"><rect width="1600" height="1000" fill="#f3ead8"/><rect y="620" width="1600" height="380" fill="#e2d3b3"/>{house(180,180,1150,seed)}<text x="80" y="920" font-family="{SERIF}" font-size="44" fill="#2b2722">{esc(name)}</text><text x="80" y="965" font-family="{SANS}" font-size="24" fill="#6b6257">{esc(subtitle)}</text></svg>'
    return svg
def board_file(name,seed):
    # plan-like detail
    s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1000"><rect width="1600" height="1000" fill="#fbf8f1"/><text x="70" y="90" font-family="{SERIF}" font-size="42" fill="#2b2722">{esc(name)} — plan &amp; materials</text>'
    s+='<g stroke="#2b2722" stroke-width="4" fill="none"><rect x="120" y="170" width="760" height="560"/><rect x="120" y="170" width="340" height="260" fill="#efe6d4"/><rect x="460" y="170" width="420" height="340" fill="#dfe8dd"/><rect x="120" y="430" width="340" height="300" fill="#e8dcc4"/><rect x="460" y="510" width="420" height="220" fill="#efe6d4"/><circle cx="670" cy="340" r="110" fill="#cfe0e2"/></g>'
    s+='<g font-family="'+SANS+'" font-size="26" fill="#2b2722"><text x="170" y="310">Living</text><text x="540" y="330">Courtyard</text><text x="170" y="590">Bedrooms</text><text x="540" y="630">Kitchen</text></g>'
    for i,(c,l) in enumerate([("#efe6d4","Limestone"),("#b4552d","Cypress / clay"),("#7fa3a8","Glass in shade"),("#6b7d4f","Live oak court")]):
        y=220+i*105; s+=f'<rect x="1020" y="{y}" width="120" height="70" fill="{c}" stroke="#2b2722" stroke-width="3"/><text x="1170" y="{y+45}" font-family="{SANS}" font-size="28" fill="#2b2722">{l}</text>'
    s+=f'<text x="1020" y="700" font-family="{SERIF}" font-size="30" fill="#2b2722">Drawn by Elena Marlowe, AIA (fictional)</text></svg>'
    return s
def logo(sp):
    ini="".join(w[0] for w in sp["name"].replace("The ","").split()[:2]).upper()
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 120"><path d="M25 82 L60 42 L95 82 M38 82 V62 H82 V82" fill="none" stroke="{sp["c1"]}" stroke-width="5" stroke-linecap="round"/><text x="112" y="66" font-family="{SERIF}" font-size="25" font-weight="700" fill="{sp["c1"]}">{esc(sp["name"])}</text><text x="113" y="90" font-family="{SANS}" font-size="12" letter-spacing="2" fill="{sp["c1"]}" opacity=".7">WITH ELENA MARLOWE</text></svg>'
    open(os.path.join(OUT,f"l-{sp['slug']}.svg"),"w").write(svg)
def portrait(name,slug):
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 300"><rect width="260" height="300" fill="#e8dcc4"/><circle cx="190" cy="55" r="80" fill="#b4552d" opacity=".22"/>{house(-30,150,260,name,wall="#f7f1e3")}
<path d="M30 300c6-62 46-92 100-92s94 30 100 92z" fill="#2b2722"/><rect x="112" y="168" width="36" height="40" rx="12" fill="#c68a62"/><ellipse cx="130" cy="132" rx="50" ry="56" fill="#c68a62"/>
<path d="M64 138c-8-62 24-96 66-96s74 34 66 96c-8-34-14-54-22-62-28 10-60 10-88 0-8 8-14 28-22 62z" fill="#2d2118"/><circle cx="112" cy="136" r="4.5" fill="#1f1a17"/><circle cx="148" cy="136" r="4.5" fill="#1f1a17"/><path d="M116 160q14 10 28 0" stroke="#1f1a17" stroke-width="4" fill="none" stroke-linecap="round"/>
<text x="240" y="286" text-anchor="end" font-family="Arial" font-weight="700" font-size="20" fill="#fff" opacity=".8">EM</text></svg>'''
    open(os.path.join(OUT,f"p-{slug}.svg"),"w").write(svg)
def cover(slug,kind,cat):
    pats={"rings":'<circle cx="600" cy="315" r="180" fill="none" stroke="#b4552d" stroke-width="18"/><circle cx="600" cy="315" r="110" fill="none" stroke="#2b2722" stroke-width="8"/>',"grid":'<path d="M200 120h800M200 260h800M200 400h800M400 80v430M650 80v430M900 80v430" stroke="#2b2722" stroke-width="6" opacity=".5"/>',"bars":'<rect x="220" y="360" width="760" height="42" fill="#b4552d"/><rect x="220" y="260" width="560" height="42" fill="#2b2722"/><rect x="220" y="160" width="660" height="42" fill="#6b7d4f"/>',"dots":'<circle cx="400" cy="220" r="34" fill="#b4552d"/><circle cx="600" cy="320" r="34" fill="#2b2722"/><circle cx="800" cy="220" r="34" fill="#6b7d4f"/>',"waves":'<path d="M180 220q120-70 240 0t240 0 240 0M180 330q120-70 240 0t240 0 240 0" fill="none" stroke="#b4552d" stroke-width="16"/>'}
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630"><rect width="1200" height="630" fill="#f3ead8"/>{pats.get(kind,pats["rings"])}<text x="70" y="560" font-family="{SANS}" font-size="24" letter-spacing="3" fill="#6b6257">{esc(cat.upper())} · MARLOWE ARCHITECTURE</text></svg>'
    open(os.path.join(OUT,f"c-{slug}.svg"),"w").write(svg)
def pdf(doc):
    # minimal PDF with text
    lines=[doc["title"],"",doc["sub"],""]+[(l[2:] if l.startswith("# ") else "- "+l) for l in doc["lines"]]+["","Marlowe Architecture (fictional) — generated example file."]
    txt="BT /F1 13 Tf 50 770 Td "+" ".join(f"({l.replace('(','').replace(')','')}) Tj 0 -22 Td " for l in lines)+"ET"
    objs=[ "1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n","2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n","3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n",f"4 0 obj\n<< /Length {len(txt)} >>\nstream\n{txt}\nendstream\nendobj\n","5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"]
    out="%PDF-1.4\n"; offs=[]
    for o in objs: offs.append(len(out)); out+=o
    xref=len(out); out+=f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n"+"".join(f"{o:010d} 00000 n \n" for o in offs)+f"trailer\n<< /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF"
    open(os.path.join(OUT,f"d-{doc['slug']}.pdf"),"w").write(out)
spec=json.load(open(os.path.join(HERE,"art-spec.json")))
for p in spec["people"]: portrait(p["name"],p["slug"])
for l in spec["logos"]: logo(l)
for s in spec["shots"]:
    open(os.path.join(OUT,f"w-{s['slug']}.svg"),"w").write(cover_file(s["name"],s["slug"],s["headline"][:80]))
    open(os.path.join(OUT,f"m-{s['slug']}.svg"),"w").write(board_file(s["name"],s["slug"]))
for c in spec["covers"]: cover(c["slug"],c["kind"],c["cat"])
for d in spec["docs"]: pdf(d)
print("art",len(os.listdir(OUT)))
