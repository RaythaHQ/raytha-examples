"""Generated line art for Carrow Bend Water: teal reservoir scenes, no real place or person."""
import os
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,"art"); os.makedirs(OUT,exist_ok=True)
def scene(name,title,sub,kind):
    # kind variations: tower, pipes, river, meter, drop, plant
    extra=""
    if kind=="tower": extra='<circle cx="600" cy="240" r="110" fill="none" stroke="#fff" stroke-width="6"/><path d="M520 330 L480 560 M680 330 L720 560 M500 460 H700" stroke="#fff" stroke-width="6" fill="none"/>'
    elif kind=="river": extra='<path d="M80 520 C300 460 420 580 620 520 S980 460 1120 540" stroke="#8fd8ec" stroke-width="22" fill="none"/><path d="M80 580 C320 530 480 630 700 570 S1020 530 1120 590" stroke="#fff" stroke-width="8" fill="none" opacity=".7"/>'
    elif kind=="meter": extra='<circle cx="600" cy="380" r="150" fill="none" stroke="#fff" stroke-width="7"/><path d="M600 380 L680 300" stroke="#ffba08" stroke-width="9"/><circle cx="600" cy="380" r="14" fill="#ffba08"/>'
    elif kind=="plant": extra='<rect x="260" y="360" width="680" height="200" fill="none" stroke="#fff" stroke-width="6"/><path d="M260 360 L600 260 L940 360" stroke="#fff" stroke-width="6" fill="none"/><rect x="520" y="430" width="160" height="130" fill="none" stroke="#8fd8ec" stroke-width="5"/>'
    elif kind=="drop": extra='<path d="M600 180 C600 180 430 420 430 520 a170 170 0 0 0 340 0 C770 420 600 180 600 180Z" fill="none" stroke="#fff" stroke-width="7"/><path d="M520 520 a80 90 0 0 0 80 95" stroke="#8fd8ec" stroke-width="7" fill="none"/>'
    else: extra='<path d="M180 480 H1020 M320 480 V360 M600 480 V320 M880 480 V360" stroke="#fff" stroke-width="7"/><circle cx="320" cy="340" r="22" fill="#ffba08"/><circle cx="600" cy="300" r="22" fill="#ffba08"/><circle cx="880" cy="340" r="22" fill="#ffba08"/>'
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 760"><rect width="1200" height="760" fill="#063a4a"/><g stroke="rgba(143,216,236,.22)">{'' .join(f'<line x1="{i*60}" y1="0" x2="{i*60}" y2="760"/>' for i in range(21))}</g>{extra}<g fill="#fff" font-family="sans-serif"><text x="60" y="92" font-size="36" font-weight="700">{title}</text><text x="60" y="132" font-size="21" opacity=".85">{sub}</text><text x="60" y="700" font-size="17" opacity=".7">CARROW BEND WATER · FICTIONAL EXAMPLE · GENERATED ART</text></g></svg>'''
    open(os.path.join(OUT,name),"w").write(svg)
items=[
 ("a-main-street-boil-notice.svg","MAIN STREET","Boil-water notice · 400-700 blocks","pipes"),
 ("a-elm-ridge-tank-cleaning.svg","ELM RIDGE TANK","Planned outage · tank cleaning","tower"),
 ("a-hydrant-flushing-north.svg","HYDRANT FLUSHING","North side · overnight","pipes"),
 ("a-low-pressure-high-school.svg","LOW PRESSURE","Resolved · PRV replaced","meter"),
 ("a-river-turbidity-storm.svg","OSSEL RIVER","Turbidity after storm · resolved","river"),
 ("q-annual-2025.svg","QUALITY 2025","Annual report · summary","plant"),
 ("q-q3-2026.svg","Q3 2026","Muddy river, clear taps","river"),
 ("q-lead-copper.svg","LEAD & COPPER","Kitchen-tap sampling","drop"),
 ("g-toilet-leak.svg","TOILET LEAK TEST","Ten minutes, food coloring","drop"),
 ("g-read-meter.svg","READ YOUR METER","Catch leaks before the bill","meter"),
 ("g-yard-watering.svg","YARD WATERING","Deep, infrequent, before 9am","river"),
 ("g-winterize.svg","WINTERIZE","Two pipes that freeze","pipes"),
]
for n,t,s,k in items: scene(n,t,s,k)
print("art",len(items))
