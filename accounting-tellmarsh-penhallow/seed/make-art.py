"""Generated art for Tellmarsh & Penhallow CPAs (fictional): monogram portraits, industry pictograms and field-note art. No real person or place is pictured."""
import os, json, math, html
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,"art"); os.makedirs(OUT,exist_ok=True)
PAPER="#f5f1e8"; INK="#17213a"; Q=["#2c6e74","#5f8a3a","#c99227","#b4502e"]
def svg(w,h,body): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">{body}</svg>'
def arc(cx,cy,r,a0,a1):
    p=lambda a:(cx+r*math.sin(math.radians(a)),cy-r*math.cos(math.radians(a)))
    (x0,y0),(x1,y1)=p(a0),p(a1); return f"M{x0:.1f} {y0:.1f} A{r} {r} 0 {1 if a1-a0>180 else 0} 1 {x1:.1f} {y1:.1f}"
# portraits: a quarter-dial medallion with initials (no faces)
for l in open(os.path.join(HERE,"people.jsonl")):
    p=json.loads(l); c=p["color"]; ini="".join(w[0] for w in p["name"].replace("-"," ").split()[:2]); n=p["sort_order"]
    rings="".join(f'<path d="{arc(300,300,250-i*26,(n*47+i*61)%360,(n*47+i*61)%360+110+i*30)}" stroke="{PAPER}" stroke-opacity="{.55-i*.08:.2f}" stroke-width="10" fill="none" stroke-linecap="round"/>' for i in range(5))
    ticks="".join(f'<path d="M300 40 V{58 if k%3 else 70}" stroke="{PAPER}" stroke-opacity=".5" stroke-width="3" transform="rotate({k*30} 300 300)"/>' for k in range(12))
    body=f'<rect width="600" height="600" fill="{c}"/>{ticks}{rings}<circle cx="300" cy="300" r="120" fill="{PAPER}"/><text x="300" y="338" text-anchor="middle" font-family="Georgia,serif" font-size="104" font-weight="600" fill="{c}">{html.escape(ini)}</text><text x="300" y="462" text-anchor="middle" font-family="Courier New,monospace" font-size="15" letter-spacing="3" fill="{PAPER}" opacity=".8">GENERATED</text>'
    open(f"{OUT}/p-{p['code']}.svg","w").write(svg(600,600,body))
# industry pictograms on a ruled card
S=lambda c:f'stroke="{c}" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"'
PICS={
 "rest":lambda c:f'<circle cx="400" cy="250" r="120" {S(c)}/><circle cx="400" cy="250" r="80" {S(c)} stroke-opacity=".5"/><path d="M220 140 V360 M200 140 V210 Q220 230 240 210 V140" {S(c)}/><path d="M580 140 Q620 200 580 260 V360" {S(c)}/>',
 "trade":lambda c:f'<path d="M180 360 L330 210 M300 180 l60 -60 l60 60 l-60 60z" {S(c)}/><rect x="430" y="170" width="200" height="190" {S(c)}/><path d="M430 230 H630 M500 170 V360" {S(c)} stroke-opacity=".5"/>',
 "med":lambda c:f'<rect x="300" y="110" width="200" height="280" rx="18" {S(c)}/><path d="M400 180 V300 M340 240 H460" {S(c)}/><path d="M170 300 q40 -80 80 0 t80 0" {S(c)} stroke-opacity=".5"/>',
 "np":lambda c:f'<path d="M400 360 C250 270 220 160 300 130 C350 115 390 150 400 180 C410 150 450 115 500 130 C580 160 550 270 400 360Z" {S(c)}/><path d="M180 380 H620" {S(c)} stroke-opacity=".5"/>',
 "rent":lambda c:f'<path d="M180 370 V230 L280 160 L380 230 V370 Z M420 370 V200 L520 130 L620 200 V370 Z" {S(c)}/><rect x="255" y="300" width="50" height="70" {S(c)} stroke-opacity=".6"/><rect x="495" y="290" width="50" height="80" {S(c)} stroke-opacity=".6"/>',
 "home":lambda c:f'<path d="M230 370 V230 L400 120 L570 230 V370 Z" {S(c)}/><circle cx="400" cy="270" r="50" {S(c)}/><path d="M400 240 V270 L425 285" {S(c)}/>',
}
for l in open(os.path.join(HERE,"industries.jsonl")):
    p=json.loads(l); c=p["color"]; k=p["art"].split("i-")[1][:-4]
    rule="".join(f'<path d="M0 {y} H800" stroke="{INK}" stroke-opacity=".07" stroke-width="2"/>' for y in range(30,500,32))
    body=f'<rect width="800" height="500" fill="{PAPER}"/>{rule}<rect x="0" y="0" width="800" height="14" fill="{c}"/>{PICS[k](c)}<text x="40" y="470" font-family="Courier New,monospace" font-size="18" letter-spacing="3" fill="{INK}" opacity=".6">{html.escape(p["short"].upper())} · GENERATED</text>'
    open(f"{OUT}/i-{k}.svg","w").write(svg(800,500,body))
# field-note art: dial and chart motifs
def note(k,i):
    c=Q[i%4]; bg=INK
    if k=="dial": d="".join(f'<path d="{arc(400,270,190,m*30+2,m*30+28)}" stroke="{Q[m//3]}" stroke-width="34" fill="none"/>' for m in range(12))+f'<path d="M400 270 L{400+150*math.sin(math.radians(305)):.0f} {270-150*math.cos(math.radians(305)):.0f}" stroke="#fff" stroke-width="6" stroke-linecap="round"/><circle cx="400" cy="270" r="12" fill="#fff"/>'
    elif k=="upload": d="".join(f'<rect x="{180+j*90}" y="{330-j*40}" width="200" height="140" rx="6" fill="{Q[j%4]}" fill-opacity=".9" transform="rotate({-8+j*5} {280+j*90} {400-j*40})"/>' for j in range(4))+'<path d="M560 230 V90 M510 140 L560 90 L610 140" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round"/>'
    elif k=="quarters": d="".join(f'<rect x="{140+j*140}" y="{420-h}" width="100" height="{h}" fill="{Q[j]}"/>' for j,h in enumerate([150,210,170,250]))+f'<path d="M120 420 H700" stroke="#fff" stroke-width="4"/>'
    elif k=="close": d="".join(f'<rect x="{120+j*120}" y="150" width="100" height="220" rx="8" fill="{"#fff" if j<4 else c}" fill-opacity="{.12+j*.15:.2f}"/><text x="{170+j*120}" y="290" text-anchor="middle" font-family="Georgia,serif" font-size="72" fill="#fff">{j+1}</text>' for j in range(5))
    elif k=="hire": d="".join(f'<rect x="{150+(j%4)*130}" y="{120+(j//4)*120}" width="110" height="100" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="3"/>' for j in range(12))+"".join(f'<circle cx="{205+(j%4)*130}" cy="{170+(j//4)*120}" r="22" fill="{Q[j%4]}"/>' for j in [0,3,6,9,11])
    else: d=f'<rect x="230" y="80" width="340" height="400" fill="#fff" fill-opacity=".95"/>'+"".join(f'<path d="M270 {140+j*36} H{530-(j%3)*60}" stroke="{INK}" stroke-opacity=".5" stroke-width="6"/>' for j in range(9))+f'<text x="400" y="130" text-anchor="middle" font-family="Georgia,serif" font-size="40" fill="{c}">990</text>'
    return svg(800,500,f'<rect width="800" height="500" fill="{bg}"/>{d}<text x="40" y="480" font-family="Courier New,monospace" font-size="16" letter-spacing="3" fill="#fff" opacity=".55">GENERATED ART</text>')
for i,l in enumerate(open(os.path.join(HERE,"notes.jsonl"))):
    p=json.loads(l); k=p["image"].split("n-")[1][:-4]; open(f"{OUT}/n-{k}.svg","w").write(note(k,i))
print("art ok", len(os.listdir(OUT)))
