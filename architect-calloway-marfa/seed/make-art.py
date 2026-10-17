"""Blueprint-style drawings for Calloway Marfa: white lines on blueprint blue. Generated, license-free."""
import os, re, json, pathlib
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,"art"); os.makedirs(OUT,exist_ok=True)
def bp(name,sub,seed=0):
 y=480-(seed%3)*30
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 760"><rect width="1200" height="760" fill="#0f2da8"/>'
 svg+='<g stroke="rgba(255,255,255,.25)" stroke-width="1">'+''.join(f'<line x1="{i*40}" y1="0" x2="{i*40}" y2="760"/>' for i in range(31))+''.join(f'<line x1="0" y1="{i*40}" x2="1200" y2="{i*40}"/>' for i in range(20))+'</g>'
 svg+=f'<g fill="none" stroke="#fff" stroke-width="5"><rect x="220" y="{y-220}" width="560" height="220"/><path d="M200 {y-220} L500 {y-300} L800 {y-220}"/><rect x="780" y="{y-150}" width="220" height="150"/><path d="M760 {y-150} L890 {y-210} L1020 {y-150}"/><line x1="120" y1="{y}" x2="1080" y2="{y}"/><rect x="300" y="{y-170}" width="90" height="170"/><rect x="520" y="{y-180}" width="140" height="110"/><circle cx="980" cy="{y-320}" r="42"/></g>'
 name=name.replace("&","&amp;"); sub=str(sub).replace("&","&amp;")
 svg+=f'<g fill="#fff" font-family="monospace"><text x="60" y="80" font-size="34" font-weight="700">{name.upper()}</text><text x="60" y="120" font-size="22" opacity=".85">{sub}</text><text x="60" y="700" font-size="20">JUNE CALLOWAY, AIA (FICTIONAL) - MARFA TX</text></g></svg>'
 return svg
for f in pathlib.Path(HERE).glob("*.jsonl"):
 for line in open(f):
  d=json.loads(line); img=d.get("image","")
  if "@file:./art/" in img:
   fn=img.split("/")[-1]; title=d.get("title","Sheet"); sub=d.get("drawing_no",d.get("date_label","FIELD NOTE"))
   open(os.path.join(OUT,fn),"w").write(bp(title,sub,sum(title.encode())%7))
print("art",len(os.listdir(OUT)))
