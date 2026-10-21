"""Generated art for Abacene customer stories: abstract usage charts, no real company, product or person."""
import os, math
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,"art"); os.makedirs(OUT,exist_ok=True)
def art(name,word,meter,seed,acc):
    pts=[]; v=0.45
    for i in range(25):
        v+=0.035*math.sin(i*0.7+seed)+0.012*((i*seed)%3-1)+0.01
        pts.append((60+i*45, 560-min(max(v,0.1),0.95)*380))
    line=" ".join(f"{x:.0f},{y:.0f}" for x,y in pts); area=f"60,600 {line} {pts[-1][0]:.0f},600"
    bars="".join(f'<rect x="{80+i*44}" y="{640-(18+((i*seed*7)%40))}" width="26" height="{18+((i*seed*7)%40)}" fill="#29443a"/>' for i in range(25))
    svg=f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 760"><rect width="1200" height="760" fill="#0c1613"/><g stroke="#1b2e27">{''.join(f'<line x1="60" y1="{y}" x2="1140" y2="{y}"/>' for y in range(180,620,60))}</g><polygon points="{area}" fill="{acc}" opacity=".14"/><polyline points="{line}" fill="none" stroke="{acc}" stroke-width="5"/>{bars}<circle cx="{pts[-1][0]:.0f}" cy="{pts[-1][1]:.0f}" r="10" fill="#ff6a2b"/><g font-family="monospace" fill="#dfe9e4"><text x="60" y="92" font-size="40" font-weight="700">{word}</text><text x="60" y="134" font-size="22" fill="#9fb5ab">{meter}</text><text x="60" y="712" font-size="16" fill="#6f8a80">FICTIONAL CUSTOMER · ABACENE EXAMPLE · GENERATED ART</text></g></svg>"""
    open(os.path.join(OUT,name),"w").write(svg)
art("s-quillon.svg","quillon geocode","geocode.lookups · count() by region",1.3,"#7fe0b0")
art("s-larchmere.svg","larchmere speech","speech.minutes · sum() by model",2.1,"#9cc4ff")
art("s-brackwater.svg","brackwater telematics","fleet.devices · unique(device_id)",3.7,"#cdeedd")
art("s-hobwick.svg","hobwick payroll","payroll.runs · credits burndown",4.4,"#ffb08a")
print("art 4")
