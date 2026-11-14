"""Generated art for Hathermouth River Rescue (fictional): side-profile plates of the boats and response vehicle. No real boat, person or place is pictured."""
import os, json, html
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,"art"); os.makedirs(OUT,exist_ok=True)
PAPER="#f3efe4"; NAVY="#10263d"; GRID="#d9d2bf"
def esc(s): return html.escape(str(s))
def rows(n): return [json.loads(l) for l in open(os.path.join(HERE,n+".jsonl"))]
def grid(w,h): return "".join(f'<path d="M{x} 0V{h}" stroke="{GRID}" stroke-width=".6"/>' for x in range(0,w,40))+"".join(f'<path d="M0 {y}H{w}" stroke="{GRID}" stroke-width=".6"/>' for y in range(0,h,40))
def waves(w,y,c):
    return "".join(f'<path d="M0 {y+i*16} '+" ".join(f"q20 -{6-i} 40 0 t40 0" for _ in range(w//80+1))+f'" fill="none" stroke="{c}" stroke-width="{2.4-i*.5}" opacity="{.9-i*.25}"/>' for i in range(3))
def rib(c,big=True):
    s=1.0 if big else .8; ox=150 if big else 210
    return (f'<g transform="translate({ox} 0) scale({s})"><path d="M0 300 L460 300 L520 262 L40 262 Z" fill="{c}"/><path d="M40 262 L520 262 Q545 262 540 280 L520 300" fill="{c}" stroke="{NAVY}" stroke-width="3"/>'
            f'<path d="M10 300 Q0 300 0 288 L0 270 Q0 262 12 262 L40 262" fill="{c}"/><rect x="40" y="248" width="470" height="18" rx="9" fill="{NAVY}"/>'
            f'<path d="M190 248 L200 180 L300 180 L320 248Z" fill="{PAPER}" stroke="{NAVY}" stroke-width="3"/><path d="M210 192 L292 192 L300 220 L206 220Z" fill="#9cc7d2"/>'
            f'<path d="M260 180 L262 120 M246 132 H280" stroke="{NAVY}" stroke-width="4"/><circle cx="262" cy="116" r="6" fill="#d99a1e"/>'
            f'<rect x="-30" y="236" width="30" height="64" rx="4" fill="{NAVY}"/>'+(f'<rect x="-30" y="214" width="30" height="30" rx="4" fill="{NAVY}"/>' if big else '')+
            f'<text x="380" y="290" font-family="Courier New,monospace" font-size="18" font-weight="700" fill="#fff" letter-spacing="2">RESCUE</text></g>')
def flood(c):
    return (f'<g transform="translate(220 0)"><path d="M0 290 Q-20 290 -20 272 Q-20 254 0 254 L330 254 Q370 254 370 272 Q370 290 330 290Z" fill="{c}" stroke="{NAVY}" stroke-width="3"/>'
            f'<path d="M20 254 L320 254" stroke="#fff" stroke-width="3" stroke-dasharray="14 10"/><rect x="-60" y="232" width="40" height="58" rx="4" fill="{NAVY}"/>'
            f'<circle cx="90" cy="236" r="16" fill="#d99a1e"/><circle cx="160" cy="236" r="16" fill="#d99a1e"/><circle cx="230" cy="236" r="16" fill="#d99a1e"/></g>')
def truck(c):
    return (f'<g transform="translate(110 0)"><path d="M0 300 V230 Q0 220 10 220 H170 L200 170 H300 Q312 170 318 180 L350 228 H380 Q392 228 392 240 V300Z" fill="{c}" stroke="{NAVY}" stroke-width="3"/>'
            f'<path d="M210 182 H292 L322 226 H210Z" fill="#9cc7d2"/><rect x="230" y="156" width="70" height="12" rx="3" fill="#1d5f8a"/><rect x="20" y="236" width="140" height="20" fill="#fff" opacity=".9"/>'
            f'<circle cx="80" cy="304" r="30" fill="{NAVY}"/><circle cx="80" cy="304" r="12" fill="#bbb"/><circle cx="320" cy="304" r="30" fill="{NAVY}"/><circle cx="320" cy="304" r="12" fill="#bbb"/>'
            f'<path d="M392 270 H470" stroke="{NAVY}" stroke-width="6"/><path d="M470 250 H560 V290 H470Z" fill="#2f8f8a"/><circle cx="515" cy="300" r="18" fill="{NAVY}"/></g>')
for b in rows("fleet"):
    c=b["color"]; k=b["kind"]
    body={"ilb":rib(c,b["code"]=="ellwood"),"flood":flood(c),"vehicle":truck(c)}[k]
    ground=waves(800,318,"#1d5f8a") if k!="vehicle" else f'<path d="M0 334 H800" stroke="{NAVY}" stroke-width="4"/><path d="M0 346 H800" stroke="{NAVY}" stroke-width="1" stroke-dasharray="20 14"/>'
    open(f"{OUT}/b-{b['code']}.svg","w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 460"><rect width="800" height="460" fill="{PAPER}"/>{grid(800,460)}
<rect x="16" y="16" width="768" height="428" fill="none" stroke="{NAVY}" stroke-width="2"/>
<text x="40" y="58" font-family="Courier New,monospace" font-size="15" letter-spacing="3" fill="{c}" font-weight="700">{esc(b['length'].upper())} · {esc(b['speed'].upper())}</text>
<text x="40" y="96" font-family="Georgia,serif" font-size="34" fill="{NAVY}">{esc(b['name'])}</text>{body}{ground}
<text x="40" y="420" font-family="Courier New,monospace" font-size="12" letter-spacing="2" fill="{NAVY}" opacity=".55">GENERATED PLATE · FICTIONAL CHARITY · IN SERVICE {esc(b['in_service'])}</text></svg>''')
print("art ok", len(os.listdir(OUT)))
