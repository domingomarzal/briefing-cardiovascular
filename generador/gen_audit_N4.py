# -*- coding: utf-8 -*-
import json,io,html,re,os,importlib.util
BASE="/Users/dmarzal/Documents/Claude/Briefing Cardiovascular/briefing-cardiovascular-repo"
GEN=BASE+"/generador"
SP="/private/tmp/claude-501/-Users-dmarzal-Documents-UICAR/49faa331-711d-4cc5-9ce2-35319ac12483/scratchpad"
corpus=json.load(open(SP+"/n4_corpus.json"))["recs"]
dec={d["pmid"]:d for d in json.load(open(SP+"/n4_decisions.json"))}
SECN={1:"Cardiología preventiva",2:"Cardiometabolismo",3:"Dislipemia",4:"Cardiopatía isquémica",5:"Insuficiencia cardíaca",6:"Miocardiopatías",7:"Valvulopatías",8:"Imagen cardíaca",9:"Cardiología intervencionista",10:"Arritmias y electrofisiología"}
def esc(s): return html.escape(s or "",quote=False)
def num(x): return ("%.1f"%x).replace(".",",")
PTYPE_EN={"Journal Article":"Investigación original","Review":"Artículo de revisión","Meta-Analysis":"Metaanálisis","Systematic Review":"Revisión sistemática","Randomized Controlled Trial":"Ensayo clínico aleatorizado","Editorial":"Editorial","Letter":"Carta al editor","Comment":"Comentario","Published Erratum":"Corrección/Errata","Observational Study":"Estudio observacional","Multicenter Study":"Estudio observacional","Case Reports":"Caso clínico","Practice Guideline":"Guía de práctica clínica","Guideline":"Guía de práctica clínica","Clinical Trial":"Ensayo clínico aleatorizado","Comparative Study":"Investigación original","Validation Study":"Estudio diagnóstico","News":"Noticia"}
def entype(pts):
    for p in ["Randomized Controlled Trial","Meta-Analysis","Systematic Review","Practice Guideline","Guideline","Review","Observational Study","Clinical Trial","Multicenter Study"]:
        if p in pts: return PTYPE_EN[p]
    for p in pts:
        if p in PTYPE_EN: return PTYPE_EN[p]
    return esc(pts[0]) if pts else "—"
rows=[]
for a in corpus:
    d=dec[a["pmid"]]
    rec=dict(pmid=a["pmid"],title=a["title"],journal=a["journal"],adate=a.get("adate",""),doi=a.get("doi",""))
    if d["sel"]:
        pr={"Imprescindible":"alto","Relevante":"medio","Complementario":"bajo"}[d["prio"]]
        rec.update(scored=True,sec=d["sec"],ptype=d["ptype"],REL=d["REL"],CA=d["CAMBIO"],EV=d["EVID"],EF=d["EFECTO"],REP=d["REP"],FI=d["FI"],tot=d["total"],pri=pr,pril=d["prio"],sel=True,star=d["star"],mot="")
    else:
        rec.update(scored=False,sel=False,mot=d["mot"],ptype=entype(a["ptypes"]))
    rows.append(rec)
order_mot={"":0,"top5":1,"dup":2,"basica":3,"nocv":3,"tipo":4,"periodo":5}
rows.sort(key=lambda r:(0 if r["scored"] else 1, -(r.get("tot",0) if r["scored"] else 0), order_mot.get(r["mot"],6), r["journal"].lower()))
MOTTXT={"top5":"fuera del top 5 de su sección","dup":"duplicado (publicado también en otra revista del scope)","basica":"ciencia básica / sin traslación clínica","nocv":"no cardiovascular","tipo":"tipo no elegible / sin resumen"}
def motcell(r):
    if r["sel"]: return '<td class="estado"><span class="est-sel">Seleccionado</span></td>'
    if r["mot"]=="periodo":
        return f'<td class="estado"><span class="est-desc">Descartado</span><span class="est-mot">fuera de periodo (online {esc(r["adate"] or "s/f")})</span></td>'
    return f'<td class="estado"><span class="est-desc">Descartado</span><span class="est-mot">{MOTTXT.get(r["mot"],"descartado")}</span></td>'
tr=[]
for i,r in enumerate(rows,1):
    if r["scored"]:
        sec=f'{r["sec"]:02d} {SECN[r["sec"]]}'; cat=f'c{r["sec"]}'
        scs="".join(f'<td class="sc">{v if v is not None else "—"}</td>' for v in [r["REL"],r["CA"],r["EV"],r["EF"],r["REP"],r["FI"]])
        tot=f'<td class="tot">{num(r["tot"])}</td>'; pric=f'<td class="pri"><span class="dot d-{r["pri"]}"></span>{r["pril"]}</td>'; dpri=r["pri"]
        stars=("★★" if r["star"]=="dest" else ("★" if r["star"]=="top3" else ""))
    else:
        sec="—"; cat=""; scs='<td class="sc">—</td>'*6; tot='<td class="tot">—</td>'; pric='<td class="pri">—</td>'; dpri=""; stars=""
    star_html="".join(f'<span class="star">{ch}</span>' for ch in stars)
    badge='<span class="selbadge">Sel</span>' if r["sel"] else '<span class="descbadge">Desc</span>'
    cls_tr="sel" if r["sel"] else "desc"; dsel="1" if r["sel"] else "0"; dest="sel" if r["sel"] else "desc"
    art=f'{esc(r["title"])} {star_html}{badge}'
    tr.append(f'<tr class="{cls_tr}" data-pri="{dpri}" data-sel="{dsel}" data-estado="{dest}" data-cat="{cat}" data-mot="{r["mot"] if not r["sel"] else ""}"><td class="num">{i}</td><td class="art">{art}</td><td class="rev">{esc(r["journal"])}</td><td class="sec">{esc(sec)}</td><td class="tipo">{esc(r["ptype"])}</td>{scs}{tot}{pric}{motcell(r)}</tr>')
rows_html="\n".join(tr)
ntot=len(rows); nsel=sum(1 for r in rows if r["sel"]); nsco=nsel
from collections import Counter
rev_tot=Counter(r["journal"] for r in rows); rev_sel=Counter(r["journal"] for r in rows if r["sel"])
parts=" · ".join(f"<b>{esc(jr)}</b> {rev_tot[jr]}/{rev_sel[jr]}" for jr in sorted(rev_tot, key=lambda s:(-rev_sel[s],-rev_tot[s],s.lower())))
box_html=f'Revisados / seleccionados por revista (PubMed, 29 jun–5 jul 2026; n.º revisados/seleccionados): {parts}. <b>Total = {ntot} revisados · {nsel} seleccionados.</b>'
src=io.open(BASE+"/n3/articulos-revisados.html",encoding="utf-8").read()
sp=src.find("<tbody>")+len("<tbody>"); ep=src.rfind("</tbody>")
head=src[:sp]; tail=src[ep:]
head=head.replace("· Briefing Cardiovascular · N3","· Briefing Cardiovascular · N4")
head=head.replace('<span class="num">N3</span>','<span class="num">N4</span>')
head=head.replace("Artículos revisados · 22 al 28 de junio de 2026","Artículos revisados · 29 de junio al 5 de julio de 2026")
head=head.replace("2026/06/22–2026/06/28","2026/06/29–2026/07/05")
head=head.replace("22–28 jun 2026","29 jun–5 jul 2026")
head=head.replace("Reglas de selección (N3).","Reglas de selección (N4).")
head=re.sub(r'da <b>\d+ seleccionados</b> esta semana',f'da <b>{nsel} seleccionados</b> esta semana',head)
head=re.sub(r'<div class="box">.*?</div>', '<div class="box">'+box_html+'</div>', head, count=1, flags=re.S)
head=re.sub(r'Listado completo de artículos revisados \(\d+\); puntuados los \d+ seleccionados',
            f'Listado completo de artículos revisados ({ntot}); puntuados los {nsco} seleccionados',head)
head=re.sub(r'mostrando \d+ de \d+ · \d+ seleccionados',f'mostrando {ntot} de {ntot} · {nsel} seleccionados',head)
head=re.sub(r'Se recuperaron <b>\d+ referencias</b>',f'Se recuperaron <b>{ntot} referencias</b>',head)
head=re.sub(r'\b254\b',str(ntot),head)
new_data=[{"p":a["pmid"],"d":a.get("doi","") or "","i":a["pmid"],"t":a["title"],"a":a["abstract"] or "[Abstract not available]"} for a in corpus]
tail=re.sub(r'window\.PUBMED_DATA =\[.*?\];', "window.PUBMED_DATA ="+json.dumps(new_data,ensure_ascii=False)+";", tail, count=1, flags=re.S)
full=head+"\n"+rows_html+"\n"+tail
outs=[BASE+"/n4/articulos-revisados.html",
      "/Users/dmarzal/Documents/Claude/Briefing Cardiovascular/Briefing Cardiovascular_N4/Briefing Cardiovascular_N4_artículos revisados.html"]
for outp in outs:
    os.makedirs(os.path.dirname(outp),exist_ok=True)
    io.open(outp,"w",encoding="utf-8").write(full)
print("audit N4:",ntot,"filas,",nsel,"sel")
spec=importlib.util.spec_from_file_location("aaf",GEN+"/add_audit_filters.py")
aaf=importlib.util.module_from_spec(spec); spec.loader.exec_module(aaf)
for p in outs: aaf.process(p)
spec2=importlib.util.spec_from_file_location("aal",GEN+"/add_audit_links.py")
aal=importlib.util.module_from_spec(spec2); spec2.loader.exec_module(aal)
for p in outs:
    try: aal.process(p)
    except Exception as e: print("links warn:",e)
print("filtros + enlaces añadidos")
