"""Inline SVG-diagrammen voor de AI-Cursus (kernversie okt. 2026).
Coördinatenstelsel: 520 eenheden breed = 132 mm tekstkolom (1 eenheid ~ 0,25 mm).
Lettergroottes daardoor: 13 ~ 9,4 pt, 11,5 ~ 8,3 pt (ondergrens).
Generieke bouwers: ladder, methode, flow, cards, hub, bars, stack, two, knoppen, kaart, anchor."""
from html import escape as _e

INK="#20262b"; SOFT="#5c6368"; ACCENT="#20262b"; ACCENT2="#20262b"; GEEL="#ffd400"

def _badge(cx,cy,r,n,on=False):
    """Het blokje: vierkant, geel met inkt als het de actieve stap is, anders inkt met wit."""
    f=GEEL if on else INK; c=INK if on else "#ffffff"
    return (f'<rect x="{cx-r:.1f}" y="{cy-r:.1f}" width="{2*r:.1f}" height="{2*r:.1f}" fill="{f}"/>'
            + _t(cx,cy+4.5,n,12,700,c,"middle"))
RULE="#cfd3cc"; LIGHT="#e8eae4"; WARM="#e8eae4"
TONES={"g":("#e8eae4","#20262b"),"o":("#e8eae4","#20262b"),"r":("#f2f3ef","#5c6368"),
       "b":(LIGHT,ACCENT),"w":(WARM,ACCENT2),"n":("#e8eae4","#5c6368")}
W=520
FT=13.2    # titels in vakken
FS=11.6    # subtekst
FK=10.6    # kickers (kapitalen)

def wrap(text, n):
    words=str(text).split(); lines=[]; cur=""
    for w in words:
        if len(cur)+len(w)+(1 if cur else 0) <= n: cur=(cur+" "+w).strip()
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines or [""]

def _chars(width, size, bold=False):
    return max(5, int(width/(size*(0.53 if bold else 0.49))))

def _svg(h, body):
    return (f'<svg viewBox="0 0 {W} {h:.0f}" xmlns="http://www.w3.org/2000/svg" font-family="Atkinson, Atkinson Hyperlegible Next, Arial, sans-serif">'
            f'<defs><marker id="ar" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">'
            f'<path d="M0 0 L7 3.5 L0 7 Z" fill="{SOFT}"/></marker>'
            f'<marker id="ar2" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">'
            f'<path d="M0 0 L7 3.5 L0 7 Z" fill="{ACCENT2}"/></marker></defs>{body}</svg>')

def _t(x,y,s,size=FS,weight=400,fill=INK,anchor="start",family="Atkinson, Atkinson Hyperlegible Next, Arial, sans-serif",style=""):
    st=f' font-style="{style}"' if style else ""
    ls=' letter-spacing="0.6"' if size==FK else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{st}{ls}>{_e(str(s))}</text>')

# ------------------------------------------------------------------ ladder
LADDER=[("Deel 1","Aan de slag"),("Deel 2","Je persoonlijke assistent"),
        ("Deel 3","AI als hefboom"),("Deel 4","Geïntegreerde systemen")]
def ladder(hl=None, note="meer draait vanzelf →"):
    gap=7; x0=4; sw=(W-2*x0-3*gap)/4; sh=50; base=40+4*sh; p=[]
    for i,(t,sub) in enumerate(LADDER):
        x=x0+i*(sw+gap); h=(i+1)*sh; y=base-h; on=(hl==i+1)
        fill="#20262b" if i%2==0 else "#353c41"
        p.append(f'<rect x="{x:.1f}" y="{y}" width="{sw:.1f}" height="{h}" rx="0" fill="{fill}"'
                 + (f' stroke="{GEEL}" stroke-width="0"' if on else "")+'/>')
        p.append(_t(x+10,y+21,t,15,700,"#fff",family="Literata, Georgia, serif"))
        for j,ln in enumerate(wrap(sub,_chars(sw-18,FS))): p.append(_t(x+10,y+37+j*13,ln,FS,400,"#e6e8e3"))
        if on:
            p.append(f'<rect x="{x:.1f}" y="{y-25}" width="100" height="19" fill="{GEEL}"/>')
            p.append(_t(x+50,y-12,"JE STAAT HIER",FK,700,INK,"middle"))
    p.append(f'<line x1="{x0}" y1="{base+5}" x2="{W-x0}" y2="{base+5}" stroke="{RULE}" stroke-width="2"/>')
    if note: p.append(_t(W-6,22,note,FS,400,SOFT,"end"))
    return _svg(base+10,"".join(p))

# ------------------------------------------------------------------ methode
def methode(scope=1):
    steps=["Braindump","Bronnen","Prompt-|engineer","Eerste|versie","Bijschaven","Bewaren"]
    gap=10; x0=3; bw=(W-2*x0-5*gap)/6; y=6; bh=72; p=[]
    for i,s in enumerate(steps):
        x=x0+i*(bw+gap); six=(i==5); on=(scope==2 and six)
        fill=WARM if six else LIGHT; br=ACCENT2 if six else ACCENT
        p.append(f'<rect x="{x:.1f}" y="{y}" width="{bw:.1f}" height="{bh}" rx="0" fill="{fill}" stroke="{br}" stroke-width="{2.8 if on else 1.4}"/>')
        p.append(_badge(x+14,y+15,9.5,i+1,six))
        ls=s.split("|"); ty=y+52 if len(ls)==1 else y+45
        for j,ln in enumerate(ls): p.append(_t(x+bw/2,ty+j*15,ln,12.6,700,INK,"middle"))
        if i<5:
            ax=x+bw; ay=y+bh/2
            p.append(f'<path d="M{ax+1:.1f} {ay} L{ax+gap-2:.1f} {ay}" stroke="{SOFT}" stroke-width="1.6" marker-end="url(#ar)"/>')
    by=y+bh+10
    a0=x0; a1=x0+5*(bw+gap)-gap
    p.append(f'<path d="M{a0} {by} L{a0} {by+6} L{a1:.1f} {by+6} L{a1:.1f} {by}" fill="none" stroke="{ACCENT}" stroke-width="1.3"/>')
    p.append(_t((a0+a1)/2,by+22,"Deel 1 · stap 1 tot 5",12.4,700,ACCENT,"middle"))
    b0=x0+5*(bw+gap); b1=b0+bw
    p.append(f'<path d="M{b0:.1f} {by} L{b0:.1f} {by+6} L{b1:.1f} {by+6} L{b1:.1f} {by}" fill="none" stroke="{ACCENT2}" stroke-width="1.3"/>')
    p.append(_t((b0+b1)/2,by+22,"Deel 2",12.4,700,SOFT,"middle"))
    return _svg(by+30,"".join(p))

# ------------------------------------------------------------------ flow
def flow(items, hl=None, foot=None, loop=None, num=False, tone=None, lf=None):
    """items: [(titel, sub)]. hl: 1-based (int of lijst). loop: label van terugpijl. foot: accolade-tekst."""
    n=len(items); gap=16 if n>3 else 22; x0=3; bw=(W-2*x0-gap*(n-1))/n
    tsz=FT if bw>95 else 12.2; ssz=FS if bw>95 else 11
    tl=[wrap(t,_chars(bw-12,tsz,True)) for t,_ in items]
    sl=[wrap(s,_chars(bw-12,ssz)) if s else [] for _,s in items]
    head=36 if num else 14
    bh=head+max(len(a)*15.5+len(b)*13.5 for a,b in zip(tl,sl))+14
    y=4; p=[]
    hls=[hl] if isinstance(hl,int) else (hl or [])
    for i in range(n):
        x=x0+i*(bw+gap); on=(i+1) in hls
        key=tone[i] if tone and i<len(tone) else ("w" if on else "b")
        f,b=TONES[key]
        p.append(f'<rect x="{x:.1f}" y="{y}" width="{bw:.1f}" height="{bh:.1f}" rx="0" fill="{f}" stroke="{b}" stroke-width="{2.4 if on else 1.3}"/>')
        yy=y+head+12
        if num:
            p.append(_badge(x+bw/2,y+18,10,i+1,on))
        for j,ln in enumerate(tl[i]): p.append(_t(x+bw/2,yy+j*15.5,ln,tsz,700,INK,"middle"))
        yy+=len(tl[i])*15.5+1
        for j,ln in enumerate(sl[i]): p.append(_t(x+bw/2,yy+j*13.5,ln,ssz,400,SOFT,"middle"))
        if i<n-1:
            ax=x+bw; ay=y+bh/2
            p.append(f'<path d="M{ax+2:.1f} {ay:.1f} L{ax+gap-2:.1f} {ay:.1f}" stroke="{SOFT}" stroke-width="1.6" marker-end="url(#ar)"/>')
    H=y+bh+6
    if loop:
        last=(lf or n)-1; lx0=x0+bw/2; lx1=x0+last*(bw+gap)+bw/2; ly=y+bh+20
        p.append(f'<path d="M{lx1:.1f} {y+bh:.1f} L{lx1:.1f} {ly:.1f} L{lx0:.1f} {ly:.1f} L{lx0:.1f} {y+bh+4:.1f}" fill="none" stroke="{ACCENT2}" stroke-width="1.6" stroke-dasharray="4 3" marker-end="url(#ar2)"/>')
        p.append(_t((lx0+lx1)/2,ly+17,loop,12,700,SOFT,"middle")); H=ly+24
    if foot:
        fy=H+2
        p.append(f'<path d="M{x0} {fy:.1f} L{x0} {fy+6:.1f} L{W-x0} {fy+6:.1f} L{W-x0} {fy:.1f}" fill="none" stroke="{ACCENT}" stroke-width="1.2"/>')
        p.append(_t(W/2,fy+22,foot,12,700,ACCENT,"middle")); H=fy+28
    return _svg(H,"".join(p))

# ------------------------------------------------------------------ cards
def cards(items, tone=None, num=False):
    """items: [(kicker, titel, [regels], voet)]"""
    n=len(items); gap=10; x0=3; bw=(W-2*x0-gap*(n-1))/n; pad=10
    tz=14 if n<=3 else 13; bz=FS if n<=3 else 11
    cs=_chars(bw-2*pad,bz)
    body=[[l for r in it[2] for l in (wrap(r,cs) if r else [])] for it in items]
    tls=[wrap(it[1],_chars(bw-2*pad,tz,True)) for it in items]
    foot=[wrap(it[3],_chars(bw-2*pad,bz,True)) if len(it)>3 and it[3] else [] for it in items]
    kick=any(it[0] for it in items) or num
    top=(28 if kick else 6)
    tmax=max(len(t) for t in tls); bmax=max(len(b) for b in body); fmax=max(len(f) for f in foot)
    bh=top+tmax*17+12+bmax*14+(fmax*13.5+14 if fmax else 0)+14
    y=4; p=[]
    for i,it in enumerate(items):
        x=x0+i*(bw+gap)
        key=tone[i] if tone and i<len(tone) else "b"
        f,b=TONES[key]
        p.append(f'<rect x="{x:.1f}" y="{y}" width="{bw:.1f}" height="{bh:.1f}" rx="0" fill="{f}" stroke="{b}" stroke-width="1.4"/>')
        if num:
            p.append(_badge(x+pad+9,y+17,9.5,i+1))
            if it[0]: p.append(_t(x+pad+24,y+21,it[0],FK,700,b))
        elif it[0]: p.append(_t(x+pad,y+20,it[0],FK,700,b))
        yy=y+top+16
        for j,ln in enumerate(tls[i]): p.append(_t(x+pad,yy+j*17,ln,tz,700,INK,family="Literata, Georgia, serif"))
        ly=y+top+16+tmax*17-8
        p.append(f'<line x1="{x+pad:.1f}" y1="{ly:.1f}" x2="{x+bw-pad:.1f}" y2="{ly:.1f}" stroke="{RULE}"/>')
        yy=ly+17
        for j,ln in enumerate(body[i]): p.append(_t(x+pad,yy+j*14,ln,bz,400,SOFT))
        if foot[i]:
            fy=y+bh-12-(len(foot[i])-1)*13.5
            for j,ln in enumerate(foot[i]): p.append(_t(x+pad,fy+j*13.5,ln,bz,700,b))
    return _svg(bh+10,"".join(p))

# ------------------------------------------------------------------ hub
def hub(center, nodes, sub=""):
    cx=W/2; cy=104; p=[]; nw=150; nh=40
    if len(nodes)<=4: pos=[(nw/2+3,34),(W-nw/2-3,34),(nw/2+3,174),(W-nw/2-3,174)]
    else: pos=[(nw/2+3,34),(W-nw/2-3,34),(nw/2+3,104),(W-nw/2-3,104),(nw/2+3,174),(W-nw/2-3,174)]
    for (x,y) in pos[:len(nodes)]:
        p.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="{RULE}" stroke-width="2" stroke-dasharray="5 4"/>')
    for (x,y),nd in zip(pos,nodes):
        p.append(f'<rect x="{x-nw/2}" y="{y-nh/2}" width="{nw}" height="{nh}" rx="0" fill="{LIGHT}" stroke="{ACCENT}" stroke-width="1.3"/>')
        p.append(_t(x,y+5,nd,FT,700,INK,"middle"))
    cw=180 if len(nodes)>4 else 150
    sl=wrap(sub,_chars(cw-16,FS)) if sub else []
    ch=46+len(sl)*14
    p.append(f'<rect x="{cx-cw/2}" y="{cy-ch/2}" width="{cw}" height="{ch}" rx="0" fill="{ACCENT}"/>')
    ty=cy-ch/2+26
    p.append(_t(cx,ty,center,16,700,"#fff","middle",family="Literata, Georgia, serif"))
    for j,ln in enumerate(sl): p.append(_t(cx,ty+19+j*14,ln,FS,400,"#e6e8e3","middle"))
    return _svg(200,"".join(p))

# ------------------------------------------------------------------ bars
def bars(rows, hl=None, note=None):
    mx=max(float(r[1]) for r in rows); lw=150; bw=W-lw-110; p=[]; y=4
    for i,(l,v,txt) in enumerate(rows):
        on=(hl==i+1); L=bw*float(v)/mx
        p.append(_t(0,y+15,l,12.4,700,INK))
        p.append(f'<rect x="{lw}" y="{y+2}" width="{bw}" height="19" rx="0" fill="#e8eae4"/>')
        p.append(f'<rect x="{lw}" y="{y+2}" width="{L:.1f}" height="19" rx="0" fill="{GEEL if on else ACCENT}"/>')
        p.append(_t(lw+L+8,y+16,txt,12,700 if on else 400,INK))
        y+=32
    if note: p.append(_t(0,y+10,note,11,400,SOFT,style="italic")); y+=16
    return _svg(y+4,"".join(p))

# ------------------------------------------------------------------ stack (oplopende trap)
def stack(rows, note=None, hl=None):
    n=len(rows); gap=6; sw=(W-6-gap*(n-1))/n; step=26; p=[]
    lines=[(wrap(t,_chars(sw-18,FT,True)), wrap(s,_chars(sw-18,FS))) for t,s in rows]
    need=max(len(a)*15+len(b)*13.5 for a,b in lines)+52
    base=need+(n-1)*step+4
    for i,(t,s) in enumerate(rows):
        x=3+i*(sw+gap); h=need+i*step; y=base-h; on=(hl==i+1)
        f,b=(WARM,ACCENT2) if on else (LIGHT,ACCENT)
        p.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{sw:.1f}" height="{h:.1f}" rx="0" fill="{f}" stroke="{b}" stroke-width="{2.2 if on else 1.3}"/>')
        p.append(_badge(x+18,y+18,10,i+1,on))
        a,bb=lines[i]; yy=y+48
        for j,ln in enumerate(a): p.append(_t(x+10,yy+j*15,ln,FT,700,INK))
        yy+=len(a)*15+1
        for j,ln in enumerate(bb): p.append(_t(x+10,yy+j*13.5,ln,FS,400,SOFT))
    H=base+6
    if note: p.append(_t(W/2,H+12,note,12,700,ACCENT,"middle")); H+=20
    return _svg(H,"".join(p))

# ------------------------------------------------------------------ two (twee panelen)
def two(left, right, mid="→"):
    gap=36; bw=(W-6-gap)/2; p=[]
    lines=[[l for r in side[2] for l in wrap(r,_chars(bw-26,FS))] for side in (left,right)]
    bh=max(len(l) for l in lines)*14.5+70
    for k,side in enumerate((left,right)):
        x=3+k*(bw+gap)
        key=side[3] if len(side)>3 and side[3] else ("b" if k==0 else "w")
        f,b=TONES[key]
        p.append(f'<rect x="{x:.1f}" y="4" width="{bw:.1f}" height="{bh:.1f}" rx="0" fill="{f}" stroke="{b}" stroke-width="1.5"/>')
        p.append(_t(x+13,24,side[0],FK,700,b))
        p.append(_t(x+13,45,side[1],16,700,INK,family="Literata, Georgia, serif"))
        p.append(f'<line x1="{x+13:.1f}" y1="55" x2="{x+bw-13:.1f}" y2="55" stroke="{RULE}"/>')
        for j,ln in enumerate(lines[k]): p.append(_t(x+13,73+j*14.5,ln,FS,400,SOFT))
    p.append(_t(W/2,4+bh/2+8,mid,22,700,ACCENT2,"middle"))
    return _svg(bh+10,"".join(p))

# ------------------------------------------------------------------ drie knoppen
def knoppen():
    rows=[("1. MODEL","licht / snel","sterk / traag","korte vraag","lange tekst, moeilijke analyse",0.30),
          ("2. DENKKRACHT","laag","hoog","eenvoudige taak","echt complex probleem",0.62),
          ("3. ZOEKMODUS","uit","aan","algemene kennis","actuele info nodig",0.80)]
    tx=128; tw=W-tx-8; p=[]
    for i,(nm,l,r,sl,sr,pos) in enumerate(rows):
        cy=32+i*72
        p.append(_t(2,cy+5,nm,12.4,700,ACCENT))
        p.append(f'<rect x="{tx}" y="{cy-3}" width="{tw}" height="6" rx="0" fill="{RULE}"/>')
        p.append(f'<rect x="{tx}" y="{cy-3}" width="{tw*pos:.1f}" height="6" rx="0" fill="{ACCENT}"/>')
        p.append(f'<rect x="{tx+tw*pos-9:.1f}" y="{cy-9}" width="18" height="18" fill="{GEEL}"/>')
        p.append(_t(tx,cy-13,l,12,700,INK)); p.append(_t(tx+tw,cy-13,r,12,700,INK,"end"))
        p.append(_t(tx,cy+23,sl,FS,400,SOFT)); p.append(_t(tx+tw,cy+23,sr,FS,400,SOFT,"end"))
    return _svg(230,"".join(p))

# ------------------------------------------------------------------ kaart van de cursus (wegwijzer)
MODULES=["AI om je heen","Voice & snelheid","Leren met AI","Diep onderzoek","Documenten & presentaties",
         "Data & spreadsheets","Beeld & video","Foto's op schaal","Klussen & vakwerk","Second brain"]
def kaart():
    p=[]; lw=200; rx=262; rw=W-rx-2
    p.append(_t(2,14,"DE LADDER · KLIMT",FK,700,ACCENT)); p.append(_t(2,30,"in volgorde, van onder naar boven",FS,400,SOFT))
    for i,(t,s) in enumerate(reversed(LADDER)):
        y=42+i*54
        p.append(f'<rect x="2" y="{y}" width="{lw}" height="46" rx="0" fill="#20262b"/>')
        p.append(_t(13,y+20,t,14.5,700,"#fff",family="Literata, Georgia, serif")); p.append(_t(13,y+37,s,FS,400,"#e6e8e3"))
    p.append(_t(lw/2+2,272,"START HIER · GEEN VOORKENNIS",FK,700,INK,"middle"))
    p.append(f'<path d="M{lw+6} 152 C {lw+34} 152, {lw+30} 120, {rx-6} 120" fill="none" stroke="{ACCENT2}" stroke-width="1.6" stroke-dasharray="4 3" marker-end="url(#ar2)"/>')
    p.append(_t(lw+8,172,"na Deel 2",11,700,SOFT))
    p.append(_t(rx,14,"DE MODULES · VERBREDEN",FK,700,INK)); p.append(_t(rx,30,"kies op behoefte, geen volgorde",FS,400,SOFT))
    for i,m in enumerate(MODULES):
        y=40+i*23.5; first=(i==0)
        f,b=(LIGHT,ACCENT) if first else (WARM,ACCENT2)
        p.append(f'<rect x="{rx}" y="{y:.1f}" width="{rw}" height="20" rx="0" fill="{f}" stroke="{b}" stroke-width="1"/>')
        p.append(_t(rx+9,y+14.5,m,12.2,700,INK))
        if first: p.append(_t(rx+rw-7,y+14.5,"ook vóór Deel 1",10.8,400,ACCENT,"end"))
    p.append(f'<rect x="2" y="290" width="{W-4}" height="58" rx="0" fill="#e8eae4" stroke="{SOFT}" stroke-width="1"/>')
    p.append(_t(13,309,"DE NASLAG",FK,700,SOFT))
    p.append(_t(13,326,"Levende Toolgids · Veiligheidskaart · AI-afspraken",13,700,INK))
    p.append(_t(13,341,"Erbij nemen wanneer nodig. Bij de toolgids eerst de peildatum checken.",FS,400,SOFT))
    return _svg(354,"".join(p))

# ------------------------------------------------------------------ cover-motieven (licht op donker)
def anchor(kind, n=None):
    p=[]
    def svg(w,h): return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">{"".join(p)}</svg>'
    if kind=="ladder":
        bw=30; gap=5; base=96
        for i in range(4):
            x=4+i*(bw+gap); h=(i+1)*21; y=base-h; on=(n==i+1)
            p.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{h}" rx="0" fill="#ffffff" fill-opacity="{1 if on else 0.28+i*0.08:.2f}"/>')
            p.append(f'<text x="{x+bw/2}" y="{base-6}" text-anchor="middle" font-family="Atkinson, Atkinson Hyperlegible Next, Arial, sans-serif" font-size="11" font-weight="700" fill="#20262b">{i+1}</text>')
        p.append(f'<rect x="4" y="{base+6}" width="{4*bw+3*gap}" height="5" rx="0" fill="#cfd3cc"/>')
        return svg(150,110)
    if kind=="grid":
        for i in range(4):
            x=4+i*35
            p.append(f'<rect x="{x}" y="30" width="30" height="62" rx="0" fill="#ffffff" fill-opacity="{0.38+i*0.14:.2f}"/>')
        p.append('<rect x="4" y="98" width="135" height="5" rx="0" fill="#cfd3cc"/>')
        return svg(150,110)
    if kind=="combo":
        for i in range(4):
            x=4+i*21; h=(i+1)*17; y=92-h
            p.append(f'<rect x="{x}" y="{y}" width="17" height="{h}" rx="0" fill="#ffffff" fill-opacity="{0.35+i*0.15:.2f}"/>')
        for r in range(3):
            for c in range(3):
                p.append(f'<rect x="{100+c*17}" y="{30+r*17}" width="14" height="13" rx="0" fill="#cfd3cc" fill-opacity="0.85"/>')
        p.append('<rect x="4" y="98" width="100" height="5" rx="0" fill="#cfd3cc"/>')
        return svg(160,110)
    if kind=="sliders":
        for i,pos in enumerate([0.3,0.62,0.8]):
            y=30+i*28
            p.append(f'<rect x="4" y="{y}" width="130" height="4" rx="0" fill="#cfd3cc" fill-opacity=".5"/>')
            p.append(f'<rect x="4" y="{y}" width="{130*pos}" height="4" rx="0" fill="#ffffff"/>')
            p.append(f'<circle cx="{4+130*pos}" cy="{y+2}" r="7" fill="#ffffff"/>')
        return svg(150,110)
    if kind=="shield":
        p.append('<path d="M70 8 L120 22 L120 58 C120 82 98 98 70 106 C42 98 20 82 20 58 L20 22 Z" fill="#ffffff" fill-opacity=".28" stroke="#cfd3cc" stroke-width="2"/>')
        for i,w in enumerate([56,48,36]):
            p.append(f'<rect x="{70-w/2}" y="{40+i*16}" width="{w}" height="6" rx="0" fill="#ffffff" fill-opacity=".85"/>')
        return svg(150,110)
    if kind=="check":
        for i in range(4):
            y=18+i*22
            p.append(f'<rect x="6" y="{y}" width="14" height="14" rx="0" fill="none" stroke="#ffffff" stroke-width="2"/>')
            if i<2: p.append(f'<path d="M9 {y+7} L12 {y+11} L18 {y+3}" fill="none" stroke="#ffffff" stroke-width="2.2"/>')
            p.append(f'<rect x="30" y="{y+4}" width="{100-i*12}" height="6" rx="0" fill="#ffffff" fill-opacity=".55"/>')
        return svg(150,110)
    if kind=="eye":
        p.append('<path d="M10 55 C 40 15, 110 15, 140 55 C 110 95, 40 95, 10 55 Z" fill="none" stroke="#cfd3cc" stroke-width="2.5"/>')
        p.append('<circle cx="75" cy="55" r="20" fill="#ffffff" fill-opacity=".8"/><circle cx="75" cy="55" r="8" fill="#20262b"/>')
        return svg(150,110)
    return ""
