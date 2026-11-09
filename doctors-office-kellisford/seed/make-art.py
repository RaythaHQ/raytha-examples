"""Generated art for Kellisford Family Medicine (fictional): provider portraits, visit-type art and notice images. No real person is pictured."""
import os, json, html
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,"art"); os.makedirs(OUT,exist_ok=True)
PAPER="#f6f5ef"; INK="#12303a"; GRID="#d9e3e0"
def esc(s): return html.escape(str(s))
def rows(n): return [json.loads(l) for l in open(os.path.join(HERE,n+".jsonl"))]
def grid(w,h,step=24,col=GRID): return "".join(f'<path d="M{x} 0V{h}" stroke="{col}" stroke-width="1"/>' for x in range(0,w,step))+"".join(f'<path d="M0 {y}H{w}" stroke="{col}" stroke-width="1"/>' for y in range(0,h,step))
# portraits: monogram on chart paper with a pulse line
for p in rows("providers"):
    c=p["color"]; ini="".join(w[0] for w in p["name"].replace("Dr. ","").split()[:2])
    open(f"{OUT}/p-{p['code']}.svg","w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 480"><rect width="400" height="480" fill="{PAPER}"/>{grid(400,480)}
<rect x="0" y="0" width="400" height="14" fill="{c}"/><circle cx="200" cy="190" r="110" fill="{c}"/><text x="200" y="222" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="92" font-weight="700" fill="#fff">{esc(ini)}</text>
<path d="M30 380 H130 L150 340 L180 420 L210 330 L235 380 H370" fill="none" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
<text x="30" y="450" font-family="Courier New,monospace" font-size="14" letter-spacing="2" fill="{INK}" opacity=".55">GENERATED PORTRAIT · FICTIONAL</text></svg>''')
# visit art: a time bar plus icon
ICON={"checkup":"M120 200 h160 M200 120 v160","sick":"M200 130 a70 70 0 1 0 0.1 0z M200 90 v50 M200 270 v50 M120 200 h-50 M280 200 h50","chronic":"M120 270 l50 -80 l50 50 l70 -120","labs":"M200 110 v120 a45 45 0 1 1 -0.1 0z M160 110 h80","vaccine":"M130 270 l140 -140 M250 110 l40 40 M110 290 l-30 30 M170 210 l30 30","virtual":"M110 140 h180 v120 h-180z M230 200 l60 -40 v80z"}
for v in rows("visits"):
    n=v["sort_order"]; c=v["color"]; m=int(v["minutes"]); wbar=min(340,m*8.4)
    open(f"{OUT}/v-{n:02d}.svg","w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><rect width="800" height="520" fill="{PAPER}"/>{grid(800,520,32)}
<rect x="0" y="0" width="800" height="16" fill="{c}"/><g transform="translate(380,40)"><path d="{ICON.get(v['kind'],'M120 200h160')}" fill="none" stroke="{c}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></g>
<text x="48" y="120" font-family="Helvetica,Arial,sans-serif" font-size="46" font-weight="700" fill="{INK}">{esc(m)} min</text>
<text x="48" y="160" font-family="Courier New,monospace" font-size="18" letter-spacing="3" fill="{INK}" opacity=".7">{esc(v['title'].upper()[:28])}</text>
<rect x="48" y="400" width="340" height="18" rx="9" fill="{GRID}"/><rect x="48" y="400" width="{wbar}" height="18" rx="9" fill="{c}"/>
<text x="48" y="470" font-family="Courier New,monospace" font-size="13" fill="{INK}" opacity=".5">GENERATED ART · FICTIONAL PRACTICE · KELLISFORD</text></svg>''')
# notices
for n in rows("updates"):
    img=os.path.basename(n["image"]).replace("n-","").replace(".svg",""); c=["#0f6b66","#d9503a","#c98a12","#2f6f9f","#6a4c93"][n["sort_order"]%5]
    open(f"{OUT}/n-{img}.svg","w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450"><rect width="800" height="450" fill="{PAPER}"/>{grid(800,450,32)}<rect x="0" y="0" width="14" height="450" fill="{c}"/>
<path d="M60 300 H240 L270 240 L320 360 L370 220 L410 300 H740" fill="none" stroke="{c}" stroke-width="6" stroke-linejoin="round"/>
<text x="60" y="120" font-family="Helvetica,Arial,sans-serif" font-size="30" font-weight="700" fill="{INK}">{esc(n["title"][:34])}</text><text x="60" y="160" font-family="Courier New,monospace" font-size="18" letter-spacing="2" fill="{INK}" opacity=".6">{esc(n["date_label"])}</text>
<text x="60" y="420" font-family="Courier New,monospace" font-size="13" fill="{INK}" opacity=".5">GENERATED ART · FICTIONAL</text></svg>''')
print("art ok", len(os.listdir(OUT)))
