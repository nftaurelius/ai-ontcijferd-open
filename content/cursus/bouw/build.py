#!/usr/bin/env python3
"""AI-Cursus — bouwscript (AI Ontcijferd, huisstijl 1.0).

Bron = één leesbaar tekstbestand per onderdeel in src/ (eigen lichte opmaak, zie BRONFORMAAT.md).
Gebruik:
    python3 build.py deel1          # één onderdeel  -> out/<bestand>.pdf
    python3 build.py all            # alle onderdelen + volledige band
"""
import re, sys, os, html, shlex, glob
from weasyprint import HTML
from pypdf import PdfReader, PdfWriter

ROOT=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(ROOT,"..","src")
OUT=os.environ.get("CURSUS_UIT", os.path.join(ROOT,"..","..","materiaal","ai-cursus","bestanden"))
sys.path.insert(0, os.path.join(ROOT,"assets"))
import diagrams as D

CSS=open(os.path.join(ROOT,"assets","cursus.css"),encoding="utf-8").read()

# ---------------------------------------------------------------- inline opmaak
def inl(s):
    s=html.escape(s, quote=False)
    s=re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s=re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    return s

def paras(lines):
    out=[]; cur=[]; lst=None; items=[]
    def flush_p():
        nonlocal cur
        if cur: out.append(f"<p>{inl(' '.join(cur))}</p>"); cur=[]
    def flush_l():
        nonlocal lst, items
        if lst:
            out.append(f"<{lst}>"+"".join(f"<li>{inl(i)}</li>" for i in items)+f"</{lst}>"); lst=None; items=[]
    for ln in lines:
        s=ln.strip()
        if not s: flush_p(); flush_l(); continue
        m=re.match(r"^(-|\d+\.)\s+(.*)$", s)
        if m:
            flush_p(); kind="ul" if m.group(1)=="-" else "ol"
            if lst and lst!=kind: flush_l()
            lst=kind; items.append(m.group(2)); continue
        if lst and ln.startswith("  "): items[-1]+=" "+s; continue
        flush_l(); cur.append(s)
    flush_p(); flush_l()
    return "".join(out)

def opts(head):
    toks=shlex.split(head); kw={}; pos=[]
    for t in toks:
        if "=" in t: k,v=t.split("=",1); kw[k]=v
        else: pos.append(t)
    return pos, kw

def figure(head, body, cap):
    pos,kw=opts(head); kind=pos[0]
    rows=[[c.strip() for c in l.split("|")] for l in body if l.strip()]
    hl=int(kw["hl"]) if "hl" in kw and kw["hl"].isdigit() else ([int(x) for x in kw["hl"].split(",")] if "hl" in kw else None)
    if kind=="ladder": svg=D.ladder(hl=int(kw.get("hl",0)) or None)
    elif kind=="methode": svg=D.methode(scope=int(kw.get("scope",1)))
    elif kind=="knoppen": svg=D.knoppen()
    elif kind=="kaart": svg=D.kaart()
    elif kind=="flow": svg=D.flow([(r[0], r[1] if len(r)>1 else "") for r in rows], hl=hl,
                                  foot=kw.get("foot"), loop=kw.get("loop"), num="num" in pos, tone=kw.get("tone"), lf=int(kw["lf"]) if "lf" in kw else None)
    elif kind=="cards": svg=D.cards([(r[0], r[1], [x.strip() for x in r[2].split(";")] if len(r)>2 else [],
                                      r[3] if len(r)>3 else "") for r in rows], tone=kw.get("tone"), num="num" in pos)
    elif kind=="hub": svg=D.hub(kw.get("center",""), [r[0] for r in rows], kw.get("sub",""))
    elif kind=="bars": svg=D.bars([(r[0],r[1],r[2]) for r in rows], hl=hl, note=kw.get("note"))
    elif kind=="stack": svg=D.stack([(r[0], r[1] if len(r)>1 else "") for r in rows], note=kw.get("note"))
    elif kind=="two":
        sides=[(r[0], r[1], [x.strip() for x in r[2].split(";")], r[3] if len(r)>3 else None) for r in rows]
        sides=[s if s[3] else s[:3] for s in sides]
        svg=D.two(*sides, mid=kw.get("mid","→"))
    else: raise ValueError("onbekend diagram: "+kind)
    c=f'<div class="cap">{inl(cap)}</div>' if cap else ""
    return f'<div class="figure">{svg}{c}</div>'

def block(kind, head, body):
    label, _, cap = head.partition("|")
    label=label.strip(); cap=cap.strip()
    if kind=="prompt":
        txt="\n".join(body).strip("\n")
        return f'<div class="prompt"><div class="p-lbl">{inl(label or "KOPIEER DIT")}</div><pre>{html.escape(txt)}</pre></div>'
    if kind=="donow":
        return f'<div class="donow"><div class="dn-head">{inl(label)}</div><div class="dn-body">{paras(body)}</div></div>'
    if kind=="deeper":
        return f'<div class="deeper"><div class="dp-lbl">GA DIEPER — {inl(label)}</div>{paras(body)}</div>'
    if kind in ("note","warn"):
        cls={"note":"co-note","warn":"co-warn"}[kind]
        return f'<div class="callout {cls}"><div class="co-lbl">{inl(label or ("Onthoud" if kind=="note" else "Let op"))}</div>{paras(body)}</div>'
    if kind=="sample":
        return f'<div class="sample"><div class="s-lbl">{inl(label)}</div>{paras(body)}</div>'
    if kind=="refbox":
        return f'<div class="refbox">{paras(body)}</div>'
    if kind=="vs":
        a,b=[x.strip() for x in head.split("|")]
        i=body.index("---"); w,s=body[:i],body[i+1:]
        return (f'<div class="vs"><div class="card weak"><div class="vs-lbl">{inl(a)}</div>{paras(w)}</div>'
                f'<div class="card strong"><div class="vs-lbl">{inl(b)}</div>{paras(s)}</div></div>')
    if kind=="recap":
        items=[l.strip()[2:] for l in body if l.strip().startswith("- ")]
        return (f'<div class="recap"><div class="r-lbl">{inl(label or "IN HET KORT")}</div><ul>'
                + "".join(f"<li>{inl(i)}</li>" for i in items)+"</ul></div>")
    if kind=="fig": return figure(label, body, cap)
    if kind=="fill":
        n=int(label or 1)
        return f'<div class="fill" style="height:{8*n+2}mm"></div>'
    if kind=="checks":
        return '<div class="checks">'+"".join(f"<div>{inl(l.strip()[2:])}</div>" for l in body if l.strip().startswith("- "))+"</div>"
    raise ValueError("onbekend blok: "+kind)

def table(lines):
    rows=[[c.strip() for c in l.strip().strip("|").split("|")] for l in lines if not re.match(r"^\|\s*:?-{3,}",l.strip())]
    h="<tr>"+"".join(f"<th>{inl(c)}</th>" for c in rows[0])+"</tr>"
    b="".join("<tr>"+"".join(f"<td>{inl(c)}</td>" for c in r)+"</tr>" for r in rows[1:])
    return f"<table>{h}{b}</table>"

# ---------------------------------------------------------------- document
def parse(path):
    raw=open(path,encoding="utf-8").read()
    m=re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    meta={}
    for l in m.group(1).splitlines():
        if ":" in l: k,v=l.split(":",1); meta[k.strip()]=v.strip()
    return meta, m.group(2).splitlines()

def render_body(lines):
    """Geeft (intro_html, chapters[ (id, num, kicker, title, html) ])."""
    intro=[]; chapters=[]; cur=intro; buf=[]; i=0; chn=0
    def flush():
        nonlocal buf
        if buf: cur.append(paras(buf)); buf=[]
    while i<len(lines):
        ln=lines[i]; s=ln.strip()
        if s.startswith(":::") and len(s)>3:
            flush(); kind,_,head=s[3:].partition(" "); body=[]; i+=1
            while lines[i].strip()!=":::": body.append(lines[i]); i+=1
            cur.append(block(kind.strip(), head.strip(), body)); i+=1; continue
        if s.startswith("# "):
            flush(); t=s[2:]; kick=None
            mk=re.match(r"^\[(.+?)\]\s*(.*)$", t)
            if mk: kick, t = mk.group(1), mk.group(2)
            title,_,sub=t.partition("|")
            if kick is None: chn+=1; kick=f"HOOFDSTUK {chn}"; num=chn
            else: num=None
            cid=f"ch{len(chapters)+1}"
            ch={"id":cid,"num":num,"kicker":kick,"title":title.strip(),"sub":sub.strip(),"parts":[]}
            chapters.append(ch); cur=ch["parts"]; i+=1; continue
        if s.startswith("### "): flush(); cur.append(f"<h4>{inl(s[4:])}</h4>"); i+=1; continue
        if s.startswith("## "): flush(); cur.append(f"<h3>{inl(s[3:])}</h3>"); i+=1; continue
        if s.startswith(">> "): flush(); cur.append(f'<div class="pullquote">{inl(s[3:])}</div>'); i+=1; continue
        if s.startswith("> "): flush(); cur.append(f'<div class="anchor-line">{inl(s[2:])}</div>'); i+=1; continue
        if s.startswith("? "): flush(); cur.append(f'<p class="why">{inl(s[2:])}</p>'); i+=1; continue
        if s=="@pb": flush(); cur.append('<div class="pb"></div>'); i+=1; continue
        if s=="@toc": flush(); cur.append("@@TOC@@"); i+=1; continue
        if s.startswith("|"):
            flush(); tl=[]
            while i<len(lines) and lines[i].strip().startswith("|"): tl.append(lines[i]); i+=1
            cur.append(table(tl)); continue
        buf.append(ln); i+=1
    flush()
    return intro, chapters

def build_doc(meta, lines, extra_intro=""):
    intro, chapters = render_body(lines)
    title=meta["title"]; sub=meta.get("subtitle","")
    a=meta.get("anchor","ladder:1"); ak,_,an=a.partition(":")
    anchor=D.anchor(ak, int(an) if an else None)
    h1=inl(title)+(f'<span class="h1sub">{inl(sub)}</span>' if sub else "")
    cover=(f'<div class="cover"><div class="merk"><span class="ai">AI</span><span class="naam">Ontcijferd</span></div><div class="kicker">{inl(meta["kicker"])}</div><h1>{h1}</h1>'
           f'<div class="tagline">{inl(meta.get("tagline",""))}</div><div class="ladder-anchor">{anchor}</div>'
           f'<div class="footstrip"><div>{inl(meta.get("foot","Tool-onafhankelijk · helder · praktisch · veilig"))}</div>'
           f'<div>{inl(meta.get("version",""))}</div></div></div>')
    toc=""
    if meta.get("toc"):
        lis="".join(f'<li><span class="n">{c["num"]}.</span><span class="t">{inl(c["title"])}</span><a class="pg" href="#{c["id"]}"></a></li>'
                    for c in chapters if c["num"] is not None)
        toc=f'<div class="toc-kicker">{inl(meta["toc"])}</div><div class="toc"><ol>{lis}</ol></div>'
    ih="".join(intro)
    ih=ih.replace("@@TOC@@",toc) if "@@TOC@@" in ih else ih+toc
    ih+=extra_intro
    body=[cover]
    if ih.strip(): body.append(f'<div class="intro-page">{ih}</div>')
    for c in chapters:
        s=(f'<section class="chapter" id="{c["id"]}"><div class="ch-kicker">{inl(c["kicker"])}</div>'
           f'<h2 class="ch-title">{inl(c["title"])}</h2>'+(f'<div class="ch-sub">{inl(c["sub"])}</div>' if c["sub"] else "")
           +"".join(c["parts"])+"</section>")
        body.append(s)
    css=CSS.replace("__RUNHEAD__", meta.get("runhead",title).replace('"','\\"')).replace("__VERSIE__", meta.get("version","").replace('"',''))
    return f'<!DOCTYPE html><html lang="nl"><head><meta charset="utf-8"><title>{html.escape(title)}</title><style>{css}</style></head><body>{"".join(body)}</body></html>'

def render(src, extra_intro=""):
    meta, lines = parse(src)
    os.makedirs(OUT, exist_ok=True); out=os.path.join(OUT,meta["file"]+".pdf")
    HTML(string=build_doc(meta, lines, extra_intro), base_url=os.path.join(ROOT,"assets")+"/").write_pdf(out)
    return meta, out, len(PdfReader(out).pages)

# ---------------------------------------------------------------- band
GROUPS=[("Start",["wegwijzer"]),
        ("De ladder — lees deze in volgorde",["deel1","deel2","deel3","deel4"]),
        ("De modules — kies op behoefte",["m-omjeheen","m-voice","m-leren","m-onderzoek","m-documenten","m-data","m-beeld","m-fotos","m-klussen","m-brein"]),
        ("Naslag — hou erbij, print wat je nodig hebt",["toolgids","veiligheid","afspraken"])]

def sources():
    d={}
    for f in sorted(glob.glob(os.path.join(SRC,"*.txt"))):
        meta,_=parse(f)
        if meta.get("id"): d[meta["id"]]=(f,meta)
    return d

def build_all():
    S=sources(); built={}
    for _,ids in GROUPS:
        for i in ids:
            meta,out,n=render(S[i][0]); built[i]=(meta,out,n); print(f"{i:14s} {n:4d} p  {out}")
    band_src=S["band"][0]
    def bandtoc(offset):
        h='<p class="why">De nummers rechts zijn de bladzijden in deze band. Elk document heeft daarnaast zijn eigen nummering onderaan, zodat het ook los te gebruiken is.</p>'; k=0; pg=offset
        pages={}
        for _,ids in GROUPS:
            for i in ids: pages[i]=pg; pg+=built[i][2]
        for g,ids in GROUPS:
            h+=f'<h3>{inl(g)}</h3><div class="btoc">'
            for i in ids:
                k+=1; m=built[i][0]
                h+=(f'<div class="row"><div class="n">{k}</div><div class="t"><b>{inl(m["toctitle"])}</b>'
                    f'<span>{inl(m.get("tocline",""))}</span></div><div class="pg">{pages[i]}</div></div>')
            h+="</div>"
        return h
    meta,out,n=render(band_src, extra_intro=bandtoc(100))
    meta,out,n=render(band_src, extra_intro=bandtoc(n+1))
    w=PdfWriter()
    for f in [out]+[built[i][1] for _,ids in GROUPS for i in ids]:
        for p in PdfReader(f).pages: w.add_page(p)
    final=os.path.join(OUT,"AI-Cursus-volledig.pdf")
    w.add_metadata({"/Title":"De complete AI-cursus — AI Ontcijferd","/Author":"Duncan Panis, AI Ontcijferd","/Subject":"CC BY 4.0, aiontcijferd.be"})
    with open(final,"wb") as fh: w.write(fh)
    print("BAND", len(PdfReader(final).pages), "p", final)
    os.remove(out)  # het voorwerk zit al in de band

if __name__=="__main__":
    arg=sys.argv[1] if len(sys.argv)>1 else "all"
    if arg=="all": build_all()
    else:
        S=sources(); meta,out,n=render(S[arg][0]); print(arg, n, "p", out)
