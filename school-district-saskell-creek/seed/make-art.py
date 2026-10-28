"""Generated art for Saskell Creek Public Schools: geometric school buildings in each feeder line's color, and abstract news images. No real place or person pictured."""
import os, json
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,"art"); os.makedirs(OUT,exist_ok=True)
LC={"ridge":"#0f7c74","creek":"#c8402a","mill":"#6a4bc4","shared":"#5b6475"}
def bld(code,line,level,seed):
    c=LC[line]; r=(seed*37)%11
    sky=f'<rect width="800" height="500" fill="#f6f1e4"/><circle cx="{620-r*12}" cy="{110+r*4}" r="54" fill="#f6b800"/>'
    hills=f'<path d="M0 380 Q200 {320+r*3} 400 360 T800 {340-r*2} V500 H0Z" fill="{c}" opacity=".18"/>'
    if level in("high","cte"): body=f'<rect x="120" y="210" width="560" height="190" fill="#fffdf7" stroke="#1d2433" stroke-width="6"/><rect x="330" y="150" width="140" height="250" fill="{c}"/><rect x="360" y="300" width="80" height="100" fill="#1d2433"/>'+"".join(f'<rect x="{150+i*58}" y="240" width="34" height="44" fill="{c}" opacity=".55"/>' for i in range(3))+"".join(f'<rect x="{500+i*58}" y="240" width="34" height="44" fill="{c}" opacity=".55"/>' for i in range(3))+'<rect x="350" y="170" width="100" height="40" fill="#fffdf7"/>'
    elif level=="middle": body=f'<rect x="170" y="230" width="460" height="170" fill="#fffdf7" stroke="#1d2433" stroke-width="6"/><path d="M150 236 L400 140 L650 236Z" fill="{c}"/><rect x="365" y="310" width="70" height="90" fill="#1d2433"/>'+"".join(f'<rect x="{200+i*62}" y="260" width="38" height="40" fill="{c}" opacity=".5"/>' for i in range(3))+"".join(f'<rect x="{470+i*62}" y="260" width="38" height="40" fill="{c}" opacity=".5"/>' for i in range(3))
    else: body=f'<rect x="220" y="250" width="360" height="150" fill="#fffdf7" stroke="#1d2433" stroke-width="6"/><path d="M200 256 L400 170 L600 256Z" fill="{c}"/><rect x="385" y="120" width="30" height="70" fill="#1d2433"/><path d="M415 125 h50 l-12 14 12 14 h-50Z" fill="#f6b800"/><rect x="370" y="320" width="60" height="80" rx="30" fill="#1d2433"/>'+"".join(f'<circle cx="{270+i*70}" cy="300" r="18" fill="{c}" opacity=".5"/>' for i in (0,1,3.75,4.75))
    ground='<rect x="0" y="400" width="800" height="100" fill="#1d2433"/>'+f'<rect x="0" y="440" width="800" height="14" fill="{c}"/>'+"".join(f'<circle cx="{80+i*160}" cy="447" r="12" fill="#fffdf7" stroke="#1d2433" stroke-width="5"/>' for i in range(5))
    open(f"{OUT}/s-{code}.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500">{sky}{hills}{body}{ground}<text x="24" y="40" font-family="monospace" font-size="16" letter-spacing="2" fill="#1d2433" opacity=".6">GENERATED ART · FICTIONAL SCHOOL</text></svg>')
for i,l in enumerate(open(os.path.join(HERE,"schools.jsonl"))):
    s=json.loads(l); bld(s["code"],s["line"],s["level"],i+3)
NEWS={"status":("#f6b800","#1d2433"),"board":("#1d2433","#f6b800"),"lang":("#0f7c74","#f6f1e4"),"cafe":("#5b6475","#f6b800"),"band":("#c8402a","#f6f1e4"),"bus":("#f6b800","#0f7c74"),"green":("#6a4bc4","#f6f1e4")}
for k,(bg,fg) in NEWS.items():
    h=sum(map(ord,k))
    shapes="".join(f'<circle cx="{(h*(i+3))%800}" cy="{(h*(i+7))%450}" r="{30+(h*i)%90}" fill="{fg}" opacity="{.10+.08*(i%3)}"/>' for i in range(7))
    lines="".join(f'<path d="M-20 {120+i*90} C 200 {60+i*90+(h%40)}, 500 {180+i*90}, 820 {100+i*90}" stroke="{fg}" stroke-width="{10-i*2}" fill="none" opacity=".7"/>' for i in range(4))
    open(f"{OUT}/n-{k}.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450"><rect width="800" height="450" fill="{bg}"/>{shapes}{lines}<text x="24" y="430" font-family="monospace" font-size="15" letter-spacing="2" fill="{fg}" opacity=".7">GENERATED ART · SASKELL CREEK (FICTIONAL)</text></svg>')
print("art", len(os.listdir(OUT)))
