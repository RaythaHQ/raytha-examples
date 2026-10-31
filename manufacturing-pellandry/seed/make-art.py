"""Generated line drawings for Pellandry Fluid Controls (fictional): blueprint-style product drawings, industry and news art. No real product or place pictured."""
import os, json, math
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,"art"); os.makedirs(OUT,exist_ok=True)
BG="#0f2a44"; LN="#e8f1fa"; AC="#ff6a1a"; GR="#1c3d5e"
def grid(w,h): return f'<rect width="{w}" height="{h}" fill="{BG}"/>'+"".join(f'<path d="M{x} 0V{h}" stroke="{GR}" stroke-width="1"/>' for x in range(0,w,25))+"".join(f'<path d="M0 {y}H{w}" stroke="{GR}" stroke-width="1"/>' for y in range(0,h,25))
def dim(x1,y,x2,label):
    return f'<path d="M{x1} {y}H{x2}" stroke="{AC}" stroke-width="2"/><path d="M{x1} {y-8}V{y+8}M{x2} {y-8}V{y+8}" stroke="{AC}" stroke-width="2"/><text x="{(x1+x2)/2}" y="{y-10}" fill="{AC}" font-family="monospace" font-size="16" text-anchor="middle">{label}</text>'
S=f'stroke="{LN}" stroke-width="3" fill="none"'
def ball():
    return f'<rect x="220" y="200" width="360" height="160" rx="18" {S}/><rect x="120" y="230" width="100" height="100" {S}/><rect x="580" y="230" width="100" height="100" {S}/><circle cx="400" cy="280" r="70" {S}/><rect x="340" y="262" width="120" height="36" {S} stroke-dasharray="8 6"/><rect x="385" y="120" width="30" height="80" {S}/><rect x="300" y="100" width="200" height="22" rx="6" fill="{AC}"/>'
def bfly():
    return f'<circle cx="400" cy="280" r="150" {S}/><circle cx="400" cy="280" r="120" {S}/><ellipse cx="400" cy="280" rx="30" ry="118" {S} stroke-dasharray="8 6"/><path d="M400 90V470" {S}/><rect x="380" y="60" width="40" height="40" {S}/>'+"".join(f'<circle cx="{400+165*math.cos(a)}" cy="{280+165*math.sin(a)}" r="10" {S}/>' for a in [i*math.pi/4+math.pi/8 for i in range(8)])
def check():
    return f'<rect x="230" y="150" width="340" height="260" rx="20" {S}/><path d="M400 160V400" {S}/><path d="M400 280 L300 190 M400 280 L500 190" stroke="{AC}" stroke-width="5"/><path d="M260 280H540" {S} stroke-dasharray="8 6"/>'
def control():
    return f'<path d="M180 360 Q180 300 260 300 H540 Q620 300 620 360 V400 H180Z" {S}/><rect x="330" y="200" width="140" height="100" {S}/><path d="M400 120V300" {S}/><path d="M300 60 H500 L470 120 H330Z" fill="{AC}"/><rect x="370" y="320" width="60" height="50" {S} stroke-dasharray="6 5"/><rect x="120" y="320" width="60" height="80" {S}/><rect x="620" y="320" width="60" height="80" {S}/>'
def act():
    return f'<rect x="170" y="170" width="460" height="200" rx="24" {S}/><circle cx="400" cy="270" r="46" {S}/><path d="M220 270H330M470 270H580" {S} stroke-dasharray="8 6"/><rect x="240" y="235" width="40" height="70" fill="{AC}"/><rect x="520" y="235" width="40" height="70" fill="{AC}"/><rect x="370" y="370" width="60" height="70" {S}/><rect x="360" y="120" width="80" height="50" {S}/>'
def pump():
    return f'<circle cx="330" cy="280" r="130" {S}/><path d="M330 280 m-80 0 a80 80 0 1 0 160 0 a80 80 0 1 0 -160 0" {S} stroke-dasharray="8 6"/>'+"".join(f'<path d="M330 280 L{330+75*math.cos(a)} {280+75*math.sin(a)}" stroke="{AC}" stroke-width="4"/>' for a in [i*math.pi/3 for i in range(6)])+f'<rect x="300" y="100" width="60" height="50" {S}/><rect x="460" y="240" width="220" height="80" {S}/><rect x="680" y="220" width="40" height="120" {S}/>'
FN={"ball":ball,"butterfly":bfly,"check":check,"control":control,"actuator":act,"pump":pump}
for l in open(os.path.join(HERE,"products.jsonl")):
    p=json.loads(l); c=p["code"]
    tb=f'<rect x="560" y="440" width="230" height="50" fill="{BG}" stroke="{LN}" stroke-width="2"/><text x="572" y="462" fill="{LN}" font-family="monospace" font-size="13">DWG {c}-GA · REV {chr(65+p["sort_order"]%5)}</text><text x="572" y="482" fill="{AC}" font-family="monospace" font-size="13">GENERATED · FICTIONAL</text>'
    open(f"{OUT}/p-{c.lower()}.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500">{grid(800,500)}{FN[p["family"]]()}{dim(120,455,520,p["sizes"].split(" (")[0][:22])}{tb}</svg>')
for l in open(os.path.join(HERE,"industries.jsonl")):
    p=json.loads(l); h=sum(map(ord,p["code"]))
    pipes="".join(f'<path d="M-10 {80+i*70} H{200+(h*i)%300} V{120+i*60} H810" stroke="{LN if i%2 else AC}" stroke-width="{14-i*2}" fill="none" opacity=".85"/>' for i in range(5))
    tanks="".join(f'<rect x="{90+i*230}" y="{220+(h*i)%60}" width="120" height="180" rx="60" fill="none" stroke="{LN}" stroke-width="3"/>' for i in range(3))
    open(f"{OUT}/i-{p['code']}.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450">{grid(800,450)}{pipes}{tanks}<text x="24" y="430" font-family="monospace" font-size="14" fill="{LN}" opacity=".7">GENERATED ART · PELLANDRY (FICTIONAL)</text></svg>')
for k in ["bf","prod","loop","safety","quality","price"]:
    h=sum(map(ord,k))
    arcs="".join(f'<circle cx="{(h*(i+2))%800}" cy="{(h*(i+5))%450}" r="{40+(h*i)%120}" fill="none" stroke="{AC if i%3==0 else LN}" stroke-width="3" opacity=".7"/>' for i in range(8))
    open(f"{OUT}/n-{k}.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450">{grid(800,450)}{arcs}<text x="24" y="430" font-family="monospace" font-size="14" fill="{LN}" opacity=".7">GENERATED ART · PELLANDRY (FICTIONAL)</text></svg>')
print("art",len(os.listdir(OUT)))
