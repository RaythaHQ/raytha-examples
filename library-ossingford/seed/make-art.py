"""Generated art for Ossingford Public Library (fictional): typographic book covers, branch elevation drawings and news art. No real book, building or person is pictured."""
import os, json, math, html
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,"art"); os.makedirs(OUT,exist_ok=True)
PAPER="#f4eedf"; INK="#1d2433"; RED="#b8432f"; GRN="#2d5a4a"; BRASS="#b08a3e"
def esc(s): return html.escape(s)
def wrap(s,n):
    out,line=[], ""
    for w in s.split():
        if len(line)+len(w)+1>n and line: out.append(line); line=w
        else: line=(line+" "+w).strip()
    if line: out.append(line)
    return out
def light(c):
    c=c.lstrip("#"); r,g,b=int(c[:2],16),int(c[2:4],16),int(c[4:],16); return (r*299+g*587+b*114)/1000>150
for l in open(os.path.join(HERE,"titles.jsonl")):
    p=json.loads(l); c=p["spine"]; fg=INK if light(c) else PAPER; n=p["sort_order"]; k=n%4
    if k==0: deco="".join(f'<circle cx="300" cy="330" r="{40+i*34}" fill="none" stroke="{fg}" stroke-opacity=".35" stroke-width="3"/>' for i in range(6))
    elif k==1: deco="".join(f'<path d="M0 {260+i*26} Q150 {230+i*26} 300 {260+i*26} T600 {260+i*26}" fill="none" stroke="{fg}" stroke-opacity=".4" stroke-width="4"/>' for i in range(9))
    elif k==2: deco="".join(f'<rect x="{60+(i%4)*125}" y="{230+(i//4)*110}" width="105" height="90" fill="{fg}" fill-opacity="{.12+.08*(i%3)}"/>' for i in range(8))
    else: deco="".join(f'<path d="M{i*60} 520 L{i*60+200} 220" stroke="{fg}" stroke-opacity=".3" stroke-width="10"/>' for i in range(-3,10))
    tl=wrap(p["title"],16)[:4]
    tt="".join(f'<text x="44" y="{110+i*52}" font-family="Georgia,serif" font-size="46" font-weight="700" fill="{fg}">{esc(x)}</text>' for i,x in enumerate(tl))
    au=f'<text x="44" y="830" font-family="Helvetica,Arial,sans-serif" font-size="26" letter-spacing="2" fill="{fg}">{esc(p["author"].upper()[:34])}</text>'
    lab=f'<rect x="420" y="760" width="140" height="50" fill="{PAPER}"/><text x="490" y="792" text-anchor="middle" font-family="Courier New,monospace" font-size="17" fill="{INK}">{esc(p["call_number"][:12])}</text>'
    open(f"{OUT}/t-{n:02d}.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 900"><rect width="600" height="900" fill="{c}"/><g transform="translate(0,120)">{deco}</g>{tt}<path d="M44 740H556" stroke="{fg}" stroke-opacity=".6" stroke-width="2"/>{au}{lab}<text x="44" y="880" font-family="Courier New,monospace" font-size="14" fill="{fg}" opacity=".7">GENERATED COVER · FICTIONAL TITLE</text></svg>')
S=f'stroke="{INK}" stroke-width="3" fill="none"'
def ground(): return f'<path d="M0 470H900" stroke="{INK}" stroke-width="4"/>'+"".join(f'<path d="M{x} 470 l-12 14" stroke="{INK}" stroke-width="2"/>' for x in range(20,900,30))
def central():
    cols="".join(f'<rect x="{300+i*60}" y="200" width="22" height="200" {S}/>' for i in range(6))
    return f'<path d="M260 200 L480 110 L700 200Z" {S}/><rect x="260" y="200" width="440" height="20" {S}/>{cols}<rect x="250" y="400" width="460" height="20" {S}/><rect x="240" y="420" width="480" height="20" {S}/><rect x="230" y="440" width="500" height="30" {S}/><rect x="450" y="300" width="60" height="100" fill="{RED}" fill-opacity=".85"/><text x="480" y="165" text-anchor="middle" font-family="Georgia,serif" font-size="18" fill="{INK}">PVBLIC LIBRARY</text><path d="M720 180H860V470H720" {S}/>'+"".join(f'<path d="M{740+i*24} 190V460" stroke="{GRN}" stroke-width="2"/>' for i in range(5))
def millrace():
    win="".join(f'<path d="M{300+i*90} 330 v-50 a25 25 0 0 1 50 0 v50z" {S}/>' for i in range(4))
    return f'<rect x="270" y="230" width="380" height="240" {S}/><path d="M250 230 L460 130 L670 230" {S}/>{win}<rect x="430" y="380" width="60" height="90" fill="{RED}" fill-opacity=".85"/><path d="M90 470 q60 -40 120 0" {S}/><circle cx="150" cy="400" r="60" {S}/>'+"".join(f'<path d="M150 400 L{150+60*math.cos(a)} {400+60*math.sin(a)}" stroke="{INK}" stroke-width="2"/>' for a in [i*math.pi/4 for i in range(8)])+f'<rect x="680" y="330" width="160" height="140" fill="{GRN}" fill-opacity=".25" stroke="{GRN}" stroke-width="3"/>'
def quarry():
    return f'<rect x="200" y="260" width="520" height="210" {S}/><rect x="190" y="240" width="540" height="22" fill="{INK}"/>'+"".join(f'<rect x="{230+i*80}" y="300" width="60" height="80" {S}/>' for i in range(6))+f'<rect x="420" y="390" width="80" height="80" fill="{RED}" fill-opacity=".85"/><path d="M250 240 L330 170 L410 240" stroke="{BRASS}" stroke-width="4" stroke-dasharray="10 8" fill="none"/><text x="460" y="215" text-anchor="middle" font-family="Courier New,monospace" font-size="16" fill="{RED}">ROOF WORK · OPEN FOR HOLDS</text><rect x="760" y="360" width="70" height="110" {S}/>'+"".join(f'<path d="M760 {380+i*20}H830" stroke="{INK}" stroke-width="2"/>' for i in range(4))
def ferrin():
    return f'<path d="M180 470 V250 L520 200 V470" {S}/><path d="M520 200 L760 240 V470" {S}/>'+"".join(f'<path d="M{200+i*40} {245-i*6} l30 -4 v40 l-30 4z" fill="{BRASS}" fill-opacity=".5" stroke="{INK}" stroke-width="1.5"/>' for i in range(8))+f'<rect x="220" y="300" width="270" height="140" fill="{GRN}" fill-opacity=".2" stroke="{INK}" stroke-width="3"/>'+"".join(f'<path d="M{220+i*54} 300V440" stroke="{INK}" stroke-width="2"/>' for i in range(1,5))+f'<rect x="580" y="360" width="70" height="110" fill="{RED}" fill-opacity=".85"/>'
def bus():
    return f'<rect x="170" y="230" width="580" height="200" rx="26" {S}/><rect x="200" y="260" width="110" height="80" {S}/>'+"".join(f'<rect x="{340+i*95}" y="260" width="80" height="80" {S}/>' for i in range(4))+f'<rect x="170" y="360" width="580" height="22" fill="{GRN}"/><text x="460" y="377" text-anchor="middle" font-family="Courier New,monospace" font-size="16" fill="{PAPER}">OSSINGFORD BOOKMOBILE</text><circle cx="280" cy="440" r="34" {S}/><circle cx="640" cy="440" r="34" {S}/>'
FN={"central":central,"millrace":millrace,"quarry":quarry,"ferrin":ferrin,"bookmobile":bus}
for l in open(os.path.join(HERE,"branches.jsonl")):
    p=json.loads(l); c=p["code"]
    open(f"{OUT}/b-{c}.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 520"><rect width="900" height="520" fill="{PAPER}"/>'+"".join(f'<path d="M0 {y}H900" stroke="#d8cdb2" stroke-width="1"/>' for y in range(40,520,32))+f'<path d="M60 0V520" stroke="{RED}" stroke-opacity=".5" stroke-width="2"/>{FN[c]()}{ground()}<text x="80" y="508" font-family="Courier New,monospace" font-size="14" fill="{INK}" opacity=".7">ELEVATION · {esc(p["name"].upper())} · GENERATED DRAWING · FICTIONAL</text></svg>')
for k,glyph in {"roof":"M300 300 L450 180 L600 300","card":"M330 200 h240 v150 h-240z","scope":"M300 330 L560 210 M520 190 l60 40","talk":"M360 200 h180 v110 h-120 l-40 40 v-40 h-20z","bus":"M300 220 h300 v110 h-300z","ledger":"M320 190 h120 v170 h-120z M460 190 h120 v170 h-120z"}.items():
    h=sum(map(ord,k)); stamps="".join(f'<g transform="rotate({(h*i)%30-15} {120+i*170} {90+(h*i)%60})"><rect x="{70+i*170}" y="{60+(h*i)%60}" width="110" height="46" fill="none" stroke="{RED}" stroke-width="3" opacity=".55"/><text x="{125+i*170}" y="{90+(h*i)%60}" text-anchor="middle" font-family="Courier New,monospace" font-size="16" fill="{RED}" opacity=".6">NOV {(h+i*3)%28+1:02d}</text></g>' for i in range(5))
    open(f"{OUT}/n-{k}.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 450"><rect width="900" height="450" fill="{PAPER}"/>'+"".join(f'<path d="M0 {y}H900" stroke="#d8cdb2" stroke-width="1"/>' for y in range(30,450,30))+f'{stamps}<path d="{glyph}" stroke="{GRN}" stroke-width="8" fill="none" stroke-linejoin="round"/><text x="24" y="430" font-family="Courier New,monospace" font-size="14" fill="{INK}" opacity=".7">GENERATED ART · OSSINGFORD PUBLIC LIBRARY (FICTIONAL)</text></svg>')
print("art",len(os.listdir(OUT)))
