"""Generated art for Helderwyn Museum of Making (fictional): object plates, exhibition posters, gallery plans, portraits, journal art."""
import os, json, html
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,"art"); os.makedirs(OUT,exist_ok=True)
PAPER="#f3efe6"; INK="#1c1916"; RED="#8b3a2a"; MOSS="#2f4a3c"; BRASS="#a07840"; WALL="#ebe4d6"
def esc(s): return html.escape(str(s))
def wrap(s,n):
    out,line=[],""
    for w in s.split():
        if len(line)+len(w)+1>n and line: out.append(line); line=w
        else: line=(line+" "+w).strip()
    if line: out.append(line)
    return out
# objects
for l in open(os.path.join(HERE,"objects.jsonl")):
    p=json.loads(l); n=p["sort_order"]; c=p.get("color") or MOSS; kind=p["kind"]
    glyph={"tool":"M180 420 L420 180 M400 160 l40 40","textile":"M200 200 h300 v40 h-300z M200 280 h300 v40 h-300z M200 360 h220 v40 h-220z","ceramic":"M300 180 q80 0 80 60 v140 q0 40 -80 40 q-80 0 -80 -40 v-140 q0 -60 80 -60z","furniture":"M220 360 h260 v40 h-260z M240 200 h40 v160 h-40z M420 200 h40 v160 h-40z","machine":"M200 300 h300 v80 h-300z M280 200 h140 v100 h-140z"}.get(kind,"M250 250 h200 v200 h-200z")
    tl=wrap(p["title"],18)[:3]
    tt="".join(f'<text x="40" y="{520+i*36}" font-family="Georgia,serif" font-size="28" font-weight="700" fill="{INK}">{esc(x)}</text>' for i,x in enumerate(tl))
    open(f"{OUT}/o-{n:02d}.svg","w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 750"><rect width="600" height="750" fill="{PAPER}"/>
<rect x="24" y="24" width="552" height="700" fill="none" stroke="{INK}" stroke-width="2"/>
<rect x="24" y="24" width="552" height="14" fill="{c}"/>
<path d="{glyph}" stroke="{c}" stroke-width="10" fill="none" stroke-linejoin="round" opacity=".85"/>
<text x="40" y="470" font-family="Courier New,monospace" font-size="18" letter-spacing="2" fill="{RED}">{esc(p["accession"])}</text>
{tt}
<text x="40" y="650" font-family="Helvetica,Arial,sans-serif" font-size="16" fill="{INK}" opacity=".75">{esc(p["maker"][:40])}</text>
<text x="40" y="678" font-family="Courier New,monospace" font-size="14" fill="{INK}" opacity=".55">{esc(p["date_label"])} · {esc(p["materials"][:28])}</text>
<text x="40" y="710" font-family="Courier New,monospace" font-size="12" fill="{INK}" opacity=".45">GENERATED PLATE · FICTIONAL OBJECT</text></svg>''')
# exhibitions
for l in open(os.path.join(HERE,"exhibitions.jsonl")):
    p=json.loads(l); n=p["sort_order"]; c=p.get("color") or RED
    tl=wrap(p["title"],14)[:3]
    tt="".join(f'<text x="48" y="{200+i*70}" font-family="Georgia,serif" font-size="56" font-weight="700" fill="{PAPER}">{esc(x)}</text>' for i,x in enumerate(tl))
    open(f"{OUT}/e-{n:02d}.svg","w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750"><rect width="1200" height="750" fill="{c}"/>
<rect x="40" y="40" width="1120" height="670" fill="none" stroke="{PAPER}" stroke-width="2" opacity=".5"/>
<text x="48" y="100" font-family="Courier New,monospace" font-size="22" letter-spacing="4" fill="{PAPER}" opacity=".85">{esc(p["status"].upper())} · {esc(p["dates"][:40])}</text>
{tt}
<text x="48" y="460" font-family="Helvetica,Arial,sans-serif" font-size="28" fill="{PAPER}" opacity=".9">{esc(p["subtitle"][:60])}</text>
<text x="48" y="680" font-family="Courier New,monospace" font-size="18" fill="{PAPER}" opacity=".7">HELDERWYN MUSEUM OF MAKING · ROOKWATER</text>
<text x="48" y="710" font-family="Courier New,monospace" font-size="14" fill="{PAPER}" opacity=".5">GENERATED POSTER · FICTIONAL EXHIBITION</text></svg>''')
# galleries
for l in open(os.path.join(HERE,"galleries.jsonl")):
    p=json.loads(l); c=p["code"]; col=p.get("color") or MOSS
    open(f"{OUT}/g-{c}.svg","w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 520"><rect width="900" height="520" fill="{WALL}"/>
'''+"".join(f'<path d="M0 {y}H900" stroke="#d8cdb2" stroke-width="1"/>' for y in range(40,520,32))+f'''
<rect x="120" y="100" width="660" height="320" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>
<rect x="120" y="100" width="660" height="18" fill="{col}"/>
<rect x="200" y="180" width="200" height="160" fill="none" stroke="{INK}" stroke-width="2"/>
<rect x="460" y="180" width="240" height="100" fill="none" stroke="{INK}" stroke-width="2"/>
<rect x="460" y="300" width="120" height="40" fill="{col}" fill-opacity=".35" stroke="{INK}" stroke-width="2"/>
<text x="450" y="90" text-anchor="middle" font-family="Courier New,monospace" font-size="20" letter-spacing="3" fill="{INK}">{esc(p["name"].upper())}</text>
<text x="140" y="480" font-family="Courier New,monospace" font-size="14" fill="{INK}" opacity=".6">GALLERY PLAN · {esc(p["floor"].upper())} · GENERATED · FICTIONAL</text></svg>''')
# people
for l in open(os.path.join(HERE,"people.jsonl")):
    p=json.loads(l); c=p["code"]; col=p.get("color") or MOSS; initials="".join(x[0] for x in p["name"].split()[:2])
    open(f"{OUT}/p-{c}.svg","w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 480"><rect width="400" height="480" fill="{PAPER}"/>
<rect x="40" y="40" width="320" height="320" fill="{col}"/>
<circle cx="200" cy="180" r="70" fill="{PAPER}" fill-opacity=".25"/>
<text x="200" y="195" text-anchor="middle" font-family="Georgia,serif" font-size="48" fill="{PAPER}">{esc(initials)}</text>
<text x="40" y="400" font-family="Georgia,serif" font-size="22" font-weight="700" fill="{INK}">{esc(p["name"])}</text>
<text x="40" y="430" font-family="Courier New,monospace" font-size="14" fill="{RED}">{esc(p["title_line"][:36])}</text>
<text x="40" y="460" font-family="Courier New,monospace" font-size="12" fill="{INK}" opacity=".5">GENERATED PORTRAIT · FICTIONAL</text></svg>''')
# journal
for k,glyph in {"bench":"M150 280 h600 v80 h-600z M200 200 h80 v80 h-80z M420 180 h120 v100 h-120z M650 210 h80 v70 h-80z","label":"M250 160 h400 v280 h-400z M280 220 h340 M280 280 h280 M280 340 h200","school":"M300 180 h400 v40 h-400z M300 250 h400 v40 h-400z M300 320 h280 v40 h-280z","vault":"M280 160 h340 v280 h-340z M320 220 h80 v40 h-80z","crate":"M220 200 h460 v220 h-460z M220 280 h460 M450 200 v220","tour":"M300 180 l150 220 l150 -220 M300 180 h300"}.items():
    open(f"{OUT}/n-{k}.svg","w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 450"><rect width="900" height="450" fill="{PAPER}"/>
'''+"".join(f'<path d="M0 {y}H900" stroke="#d8cdb2" stroke-width="1"/>' for y in range(30,450,30))+f'''
<path d="{glyph}" stroke="{MOSS}" stroke-width="8" fill="none" stroke-linejoin="round"/>
<text x="24" y="430" font-family="Courier New,monospace" font-size="14" fill="{INK}" opacity=".6">GENERATED ART · HELDERWYN MUSEUM (FICTIONAL)</text></svg>''')
print("art", len(os.listdir(OUT)))
