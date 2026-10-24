"""Generated portraits for Pennowick agents: abstract monogram cards, no real person pictured."""
import os
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,"art"); os.makedirs(OUT,exist_ok=True)
def art(name,ini,bg,fg,acc,shape):
    s={"c":f'<circle cx="300" cy="300" r="190" fill="{acc}" opacity=".35"/>',"d":f'<path d="M300 90 L510 300 L300 510 L90 300Z" fill="{acc}" opacity=".35"/>',"a":f'<path d="M110 520 A190 190 0 0 1 490 520Z" fill="{acc}" opacity=".35"/>'}[shape]
    rings="".join(f'<circle cx="300" cy="300" r="{r}" fill="none" stroke="{fg}" stroke-opacity=".12" stroke-width="2"/>' for r in range(60,420,36))
    svg=f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600"><rect width="600" height="600" fill="{bg}"/>{rings}{s}<text x="300" y="350" text-anchor="middle" font-family="Georgia,serif" font-size="150" font-weight="700" fill="{fg}">{ini}</text><text x="300" y="560" text-anchor="middle" font-family="monospace" font-size="18" letter-spacing="3" fill="{fg}" opacity=".6">FICTIONAL AGENT · GENERATED ART</text></svg>"""
    open(os.path.join(OUT,name+".svg"),"w").write(svg)
art("a-ada","AP","#7a2331","#f6ecd6","#c8962e","c")
art("a-tomas","TB","#2f5d62","#f6ecd6","#efe3c4","d")
art("a-priya","PH","#c8962e","#1c2230","#7a2331","a")
art("a-desmond","DA","#1c2230","#efe3c4","#2f5d62","c")
art("a-marisol","MV","#efe3c4","#7a2331","#2f5d62","d")
art("a-kit","KO","#5b6b4a","#f6ecd6","#c8962e","a")
print("art 6")
