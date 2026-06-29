# -*- coding: utf-8 -*-
import json,io,html,re,os,importlib.util
BASE="/Users/dmarzal/Documents/Claude/Briefing Cardiovascular/briefing-cardiovascular-repo"
GEN=BASE+"/generador"
corpus=json.load(open(GEN+"/n3_corpus.json"))["recs"]
elig=json.load(open(GEN+"/n3_eligible.json"))             # idx->record (in-window, abstract, eligible type)
tasks=json.load(open(GEN+"/n3_tasks.json"))               # selected, with scores
D1,D2="2026/06/22","2026/06/28"
SECN={1:"Cardiología preventiva",2:"Cardiometabolismo",3:"Dislipemia",4:"Cardiopatía isquémica",5:"Insuficiencia cardíaca",6:"Miocardiopatías",7:"Valvulopatías",8:"Imagen cardíaca",9:"Cardiología intervencionista",10:"Arritmias y electrofisiología"}
DEST="hel"; TOP3={"avg","a110","a18"}
# editorial discards among eligible (by n3_eligible index)
BASIC={5,42,43,49,51,60,62,63,68,72,78,116,117}
NONCV={114,118}
DUP={24,25}
sel_by_pmid={tasks[k]["doi"]:None for k in tasks}  # placeholder
sel_idx={tasks[k]["idx"] for k in tasks}
task_by_idx={tasks[k]["idx"]:tasks[k] for k in tasks}
elig_pmids={r["pmid"]:int(i) for i,r in elig.items()}
def esc(s): return html.escape(s or "",quote=False)
def num(x): return ("%.1f"%x).replace(".",",")
PTYPE_EN={"Journal Article":"Investigación original","Review":"Revisión","Meta-Analysis":"Metaanálisis","Systematic Review":"Revisión sistemática","Randomized Controlled Trial":"Ensayo clínico aleatorizado","Editorial":"Editorial","Letter":"Carta al editor","Comment":"Comentario","Published Erratum":"Corrección/Errata","Observational Study":"Estudio observacional","Multicenter Study":"Estudio multicéntrico","Case Reports":"Caso clínico","Practice Guideline":"Guía de práctica clínica","Clinical Trial":"Ensayo clínico","Comparative Study":"Estudio comparativo","Validation Study":"Estudio de validación","News":"Noticia"}
def entype(pts):
    for p in ["Randomized Controlled Trial","Meta-Analysis","Systematic Review","Practice Guideline","Review","Observational Study","Multicenter Study"]:
        if p in pts: return PTYPE_EN[p]
    for p in pts:
        if p in PTYPE_EN: return PTYPE_EN[p]
    return esc(pts[0]) if pts else "—"
rows=[]
for a in corpus:
    pmid=a["pmid"]; j=a["journal"]; adate=a.get("adate") or ""
    inwin = bool(adate and D1<=adate<=D2)
    eidx = elig_pmids.get(pmid)   # eligible index or None
    rec=dict(pmid=pmid,title=a["title"],journal=j,adate=adate)
    if eidx is not None and eidx in sel_idx:
        t=task_by_idx[eidx]; sc=t["scores"]
        pr={"Imprescindible":"alto","Relevante":"medio","Complementario":"bajo"}[t["prio"]]
        rec.update(scored=True,sec=t["sec"],ptype=t["ptype"],REL=sc["REL"],CA=sc["CAMBIO"],EV=sc["EVID"],EF=sc["EFECTO"],REP=sc["REP"],FI=sc["FI"],tot=t["total"],pri=pr,pril=t["prio"],sel=True,key=t["key"],mot="")
    elif eidx is not None and eidx in BASIC:
        rec.update(scored=False,sel=False,mot="basica",ptype=entype(a["ptypes"]))
    elif eidx is not None and eidx in NONCV:
        rec.update(scored=False,sel=False,mot="nocv",ptype=entype(a["ptypes"]))
    elif eidx is not None and eidx in DUP:
        rec.update(scored=False,sel=False,mot="dup",ptype=entype(a["ptypes"]))
    elif eidx is not None:
        rec.update(scored=False,sel=False,mot="top5",ptype=entype(a["ptypes"]))
    elif inwin:
        rec.update(scored=False,sel=False,mot="tipo",ptype=entype(a["ptypes"]))
    else:
        rec.update(scored=False,sel=False,mot="periodo",ptype=entype(a["ptypes"]))
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
        stars=("★★" if r["key"]==DEST else ("★" if r["key"] in TOP3 else ""))
    else:
        sec="—"; cat=""; scs='<td class="sc">—</td>'*6; tot='<td class="tot">—</td>'; pric='<td class="pri">—</td>'; dpri=""; stars=""
    star_html="".join(f'<span class="star">{ch}</span>' for ch in stars)
    badge='<span class="selbadge">Sel</span>' if r["sel"] else '<span class="descbadge">Desc</span>'
    cls_tr="sel" if r["sel"] else "desc"; dsel="1" if r["sel"] else "0"; dest="sel" if r["sel"] else "desc"
    art=f'{esc(r["title"])} {star_html}{badge}'
    tr.append(f'<tr class="{cls_tr}" data-pri="{dpri}" data-sel="{dsel}" data-estado="{dest}" data-cat="{cat}" data-mot="{r["mot"] if not r["sel"] else ""}"><td class="num">{i}</td><td class="art">{art}</td><td class="rev">{esc(r["journal"])}</td><td class="sec">{esc(sec)}</td><td class="tipo">{esc(r["ptype"])}</td>{scs}{tot}{pric}{motcell(r)}</tr>')
rows_html="\n".join(tr)
ntot=len(rows); nsel=sum(1 for r in rows if r["sel"]); nsco=sum(1 for r in rows if r["scored"])
# per-journal revisados/seleccionados (apartado 1)
from collections import Counter, defaultdict
rev_tot=Counter(r["journal"] for r in rows); rev_sel=Counter(r["journal"] for r in rows if r["sel"])
parts=" · ".join(f"<b>{esc(jr)}</b> {rev_tot[jr]}/{rev_sel[jr]}" for jr in sorted(rev_tot, key=lambda s:(-rev_sel[s],-rev_tot[s],s.lower())))
box_html=f'Revisados / seleccionados por revista (PubMed, 22–28 jun 2026; n.º revisados/seleccionados): {parts}. <b>Total = {ntot} revisados · {nsel} seleccionados.</b>'

# --- head/tail from N2 audit ---
src=io.open(BASE+"/n2/articulos-revisados.html",encoding="utf-8").read()
sp=src.find("<tbody>")+len("<tbody>"); ep=src.rfind("</tbody>")
head=src[:sp]; tail=src[ep:]
# replacements in head
head=head.replace("· Briefing Cardiovascular · N2","· Briefing Cardiovascular · N3")
head=head.replace('<span class="num">N2</span>','<span class="num">N3</span>')
head=head.replace("Artículos revisados · 15 al 21 de junio de 2026","Artículos revisados · 22 al 28 de junio de 2026")
head=head.replace("2026/06/15–2026/06/21","2026/06/22–2026/06/28")
head=head.replace("Se recuperaron <b>272 referencias</b>",f"Se recuperaron <b>{ntot} referencias</b>")
head=head.replace("Reglas de selección (N1).","Reglas de selección (N3).")
head=head.replace("da <b>45 seleccionados</b> esta semana",f"da <b>{nsel} seleccionados</b> esta semana")
# replace the breakdown box
head=re.sub(r'<div class="box">.*?</div>', '<div class="box">'+box_html+'</div>', head, count=1, flags=re.S)
head=head.replace("Listado completo de artículos revisados (272); puntuados los 126 elegibles",
                  f"Listado completo de artículos revisados ({ntot}); puntuados los {nsco} seleccionados")
head=head.replace("mostrando 272 de 272 · 49 seleccionados",f"mostrando {ntot} de {ntot} · {nsel} seleccionados")
head=re.sub(r'\b272\b',str(ntot),head)
# PUBMED_DATA in tail
new_data=[{"p":a["pmid"],"d":a.get("doi","") or "","i":a["pmid"],"t":a["title"],"a":a["abstract"] or "[Abstract not available]"} for a in corpus]
tail=re.sub(r'window\.PUBMED_DATA =\[.*?\];', "window.PUBMED_DATA ="+json.dumps(new_data,ensure_ascii=False)+";", tail, count=1, flags=re.S)
full=head+"\n"+rows_html+"\n"+tail
outs=[BASE+"/n3/articulos-revisados.html",
      "/Users/dmarzal/Documents/Claude/Briefing Cardiovascular/Briefing Cardiovascular_N3/Briefing Cardiovascular_N3_artículos revisados.html"]
for outp in outs:
    os.makedirs(os.path.dirname(outp),exist_ok=True)
    io.open(outp,"w",encoding="utf-8").write(full)
print("audit N3:",ntot,"filas,",nsel,"sel,",nsco,"puntuados")
spec=importlib.util.spec_from_file_location("aaf",GEN+"/add_audit_filters.py")
aaf=importlib.util.module_from_spec(spec); spec.loader.exec_module(aaf)
for p in outs: aaf.process(p)
print("filtros revista+tipo añadidos")
