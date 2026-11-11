"""Generated art for Tarrenhurst School (fictional): division plates, faculty monogram portraits, house banners and story plates. No real person or place is pictured."""
import os, json, html, math
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,"art"); os.makedirs(OUT,exist_ok=True)
IVORY="#f6f1e6"; INK="#1f2a44"; LINE="#d8cdb6"
def esc(s): return html.escape(str(s))
def rows(n): return [json.loads(l) for l in open(os.path.join(HERE,n+".jsonl"))]
def frame(w,h,c): return f'<rect x="14" y="14" width="{w-28}" height="{h-28}" fill="none" stroke="{c}" stroke-width="2"/><rect x="22" y="22" width="{w-44}" height="{h-44}" fill="none" stroke="{c}" stroke-width=".8"/>'
def hatch(w,h,c,step=14): return "".join(f'<path d="M{x} {h} L{x+h} 0" stroke="{c}" stroke-width=".7" opacity=".35"/>' for x in range(-h,w,step))
# division plates: building silhouettes
BUILD={
 "lower":'<rect x="250" y="250" width="300" height="150" fill="C"/><path d="M230 255 L400 150 L570 255Z" fill="C"/><rect x="300" y="300" width="40" height="50" fill="#f6f1e6"/><rect x="460" y="300" width="40" height="50" fill="#f6f1e6"/><rect x="380" y="320" width="40" height="80" fill="#f6f1e6"/><circle cx="150" cy="330" r="55" fill="C" opacity=".55"/><rect x="145" y="330" width="10" height="70" fill="C"/><circle cx="660" cy="320" r="45" fill="C" opacity=".55"/><rect x="655" y="320" width="10" height="80" fill="C"/>',
 "middle":'<rect x="200" y="210" width="400" height="190" fill="C"/><rect x="360" y="140" width="80" height="80" fill="C"/><path d="M350 145 L400 95 L450 145Z" fill="C"/><circle cx="400" cy="175" r="18" fill="#f6f1e6"/>'+"".join(f'<rect x="{230+i*70}" y="250" width="34" height="50" fill="#f6f1e6"/><rect x="{230+i*70}" y="320" width="34" height="50" fill="#f6f1e6"/>' for i in range(6)),
 "upper":'<rect x="170" y="200" width="460" height="200" fill="C"/><path d="M150 205 L400 120 L650 205Z" fill="C"/>'+"".join(f'<rect x="{200+i*56}" y="240" width="22" height="140" fill="#f6f1e6" opacity=".9"/>' for i in range(8))+'<rect x="380" y="60" width="40" height="70" fill="C"/>',
}
for d in rows("divisions"):
    c=d["color"]
    open(f"{OUT}/d-{d['code']}.svg","w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><rect width="800" height="520" fill="{IVORY}"/>{hatch(800,520,LINE)}{frame(800,520,c)}
<g>{BUILD[d['code']].replace('"C"',f'"{c}"')}</g><path d="M60 400 H740" stroke="{c}" stroke-width="3"/>
<text x="400" y="452" text-anchor="middle" font-family="Georgia,serif" font-size="26" font-style="italic" fill="{INK}">{esc(d['name'])} · {esc(d['grades'])}</text>
<text x="400" y="484" text-anchor="middle" font-family="Courier New,monospace" font-size="12" letter-spacing="3" fill="{INK}" opacity=".55">GENERATED PLATE · FICTIONAL SCHOOL</text></svg>''')
# faculty: monogram in an oval frame
for p in rows("faculty"):
    c=p["color"]; ini="".join(w[0] for w in p["name"].replace("-"," ").split()[:2])
    open(f"{OUT}/f-{p['code']}.svg","w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500"><rect width="400" height="500" fill="{IVORY}"/>{hatch(400,500,LINE,10)}{frame(400,500,c)}
<ellipse cx="200" cy="225" rx="128" ry="160" fill="{IVORY}" stroke="{c}" stroke-width="3"/><ellipse cx="200" cy="225" rx="116" ry="148" fill="{c}"/>
<text x="200" y="258" text-anchor="middle" font-family="Georgia,serif" font-size="96" font-style="italic" fill="{IVORY}">{esc(ini)}</text>
<text x="200" y="430" text-anchor="middle" font-family="Georgia,serif" font-size="20" fill="{INK}">{esc(p['name'])}</text>
<text x="200" y="458" text-anchor="middle" font-family="Courier New,monospace" font-size="11" letter-spacing="2" fill="{INK}" opacity=".55">GENERATED PORTRAIT · FICTIONAL</text></svg>''')
# houses: pennant banners
EMB={"ashby":'<circle cx="200" cy="200" r="46" fill="none" stroke="#f6f1e6" stroke-width="6"/>'+"".join(f'<path d="M200 200 L{200+70*math.cos(a*math.pi/6):.1f} {200+70*math.sin(a*math.pi/6):.1f}" stroke="#f6f1e6" stroke-width="4"/>' for a in range(12)),
     "calder":'<path d="M120 260 L180 160 L220 210 L260 140 L300 260Z" fill="#f6f1e6"/>',
     "merrow":"".join(f'<path d="M120 {170+i*30} q20 -16 40 0 t40 0 t40 0 t40 0" fill="none" stroke="#f6f1e6" stroke-width="7"/>' for i in range(4)),
     "thorne":'<path d="M200 130 L216 180 L268 180 L226 210 L242 260 L200 230 L158 260 L174 210 L132 180 L184 180Z" fill="#f6f1e6"/>'}
for h in rows("houses"):
    c=h["color"]
    open(f"{OUT}/h-{h['code']}.svg","w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 560"><rect width="400" height="560" fill="{IVORY}"/>
<rect x="60" y="20" width="280" height="10" rx="5" fill="{INK}"/><path d="M80 30 H320 V470 L200 540 L80 470Z" fill="{c}"/><path d="M96 46 H304 V460 L200 520 L96 460Z" fill="none" stroke="#f6f1e6" stroke-width="2" opacity=".7"/>
{EMB[h['code']]}<text x="200" y="360" text-anchor="middle" font-family="Georgia,serif" font-size="46" fill="#f6f1e6">{esc(h['name'])}</text>
<text x="200" y="400" text-anchor="middle" font-family="Georgia,serif" font-style="italic" font-size="20" fill="#f6f1e6" opacity=".9">{esc(h['motto'])}</text></svg>''')
# stories
import textwrap
for s in rows("stories"):
    k=os.path.basename(s["image"])[2:-4]; c={"classroom":"#3f6177","arts":"#5b3f6e","athletics":"#7a2232","houses":"#5f7a5a","alumni":"#a8812f"}[s["kind"]]
    lines="".join(f'<text x="60" y="{200+i*44}" font-family="Georgia,serif" font-size="34" fill="{INK}">{esc(line)}</text>' for i,line in enumerate(textwrap.wrap(s["title"],24)[:4]))
    open(f"{OUT}/s-{k}.svg","w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500"><rect width="800" height="500" fill="{IVORY}"/>{hatch(800,500,LINE)}{frame(800,500,c)}
<circle cx="630" cy="250" r="110" fill="{c}" opacity=".92"/><circle cx="630" cy="250" r="80" fill="none" stroke="{IVORY}" stroke-width="3"/>
<text x="630" y="268" text-anchor="middle" font-family="Georgia,serif" font-size="56" font-style="italic" fill="{IVORY}">{esc(s['kind'][:1].upper())}</text>
<text x="60" y="140" font-family="Courier New,monospace" font-size="14" letter-spacing="3" fill="{c}">{esc(s['kind'].upper())} · {esc(s['date_label'].upper())}</text>{lines}
<text x="60" y="452" font-family="Courier New,monospace" font-size="12" letter-spacing="2" fill="{INK}" opacity=".5">GENERATED PLATE · FICTIONAL SCHOOL</text></svg>''')
print("art ok", len(os.listdir(OUT)))
