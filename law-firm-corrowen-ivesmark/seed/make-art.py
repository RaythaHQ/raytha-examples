"""Generated portraits for Corrowen & Ivesmark attorneys: abstract initials on ruled paper, no real person pictured."""
import os
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,"art"); os.makedirs(OUT,exist_ok=True)
def art(name,ini,bg,fg,acc,tilt):
    rules="".join(f'<line x1="0" y1="{y}" x2="600" y2="{y}" stroke="{fg}" stroke-opacity=".10" stroke-width="2"/>' for y in range(40,600,34))
    svg=f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600"><rect width="600" height="600" fill="{bg}"/>{rules}<line x1="92" y1="0" x2="92" y2="600" stroke="{acc}" stroke-width="3" stroke-opacity=".7"/><rect x="150" y="150" width="300" height="300" fill="none" stroke="{acc}" stroke-width="10" transform="rotate({tilt} 300 300)" opacity=".85"/><text x="300" y="350" text-anchor="middle" font-family="Georgia,serif" font-style="italic" font-size="150" font-weight="600" fill="{fg}">{ini}</text><text x="300" y="560" text-anchor="middle" font-family="monospace" font-size="18" letter-spacing="3" fill="{fg}" opacity=".55">FICTIONAL ATTORNEY · GENERATED ART</text></svg>"""
    open(os.path.join(OUT,name+".svg"),"w").write(svg)
art("a-helena","HC","#f4f1e8","#15181d","#c2321f",-4)
art("a-bram","BI","#15181d","#f4f1e8","#c2321f",3)
art("a-odalys","OF","#e7ebf3","#1f3f86","#c2321f",-2)
art("a-teodor","TL","#f4f1e8","#1f3f86","#15181d",5)
art("a-wen","WH","#1f3f86","#f4f1e8","#f0b8ab",-5)
art("a-marguerite","MO","#efe5dc","#15181d","#1f3f86",2)
art("a-jonah","JR","#dfe5dd","#15181d","#c2321f",-3)
print("art 7")
