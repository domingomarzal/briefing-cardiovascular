# -*- coding: utf-8 -*-
import json,io,html,re,os,importlib.util
BASE="/Users/dmarzal/Documents/Claude/Briefing Cardiovascular/briefing-cardiovascular-repo"
GEN=BASE+"/generador"
SP="/private/tmp/claude-501/-Users-dmarzal-Documents-UICAR/30d28734-015e-4355-aa4e-87c85f916ac5/scratchpad/n5"
corpus=json.load(open(SP+"/corpus.json"))
assign={a["key"]:a for a in json.load(open(SP+"/assign.json"))}
pmid2key={a["pmid"]:k for k,a in assign.items()}
SECN={1:"Cardiología preventiva",2:"Cardiometabolismo",3:"Dislipemia",4:"Cardiopatía isquémica",5:"Insuficiencia cardíaca",6:"Miocardiopatías",7:"Valvulopatías",8:"Imagen cardíaca",9:"Cardiología intervencionista",10:"Arritmias y electrofisiología"}
def esc(s): return html.escape(s or "",quote=False)
def num(x): return ("%.1f"%x).replace(".",",")
PTYPE_EN={"Journal Article":"Investigación original","Review":"Artículo de revisión","Meta-Analysis":"Metaanálisis","Systematic Review":"Revisión sistemática","Network Meta-Analysis":"Metaanálisis","Randomized Controlled Trial":"Ensayo clínico aleatorizado","Editorial":"Editorial","Letter":"Carta al editor","Comment":"Comentario","Published Erratum":"Corrección/Errata","Observational Study":"Estudio observacional","Multicenter Study":"Estudio observacional","Case Reports":"Caso clínico","Practice Guideline":"Guía de práctica clínica","Guideline":"Guía de práctica clínica","Clinical Trial":"Ensayo clínico aleatorizado","Comparative Study":"Investigación original","Validation Study":"Estudio diagnóstico","News":"Noticia","Equivalence Trial":"Ensayo clínico aleatorizado"}
def entype(pts):
    for p in ["Randomized Controlled Trial","Meta-Analysis","Network Meta-Analysis","Systematic Review","Practice Guideline","Guideline","Review","Observational Study","Clinical Trial","Multicenter Study"]:
        if p in pts: return PTYPE_EN[p]
    for p in pts:
        if p in PTYPE_EN: return PTYPE_EN[p]
    return esc(pts[0]) if pts else "—"
# --- axis scores for selected (REL,CAMBIO,EVID,EFECTO,REP,FI); EF None for review/statement/consensus ---
AX={
"a1":(9,8,9,8,9,9),"a2":(8,7,8,None,8,9),"a3":(8,6,8,8,7,7),"a4":(7,7,8,6,6,7),
"a5":(8,6,6,7,7,7),"a6":(7,6,7,None,7,7),"a7":(7,6,7,None,6,7),"a8":(6,5,7,6,5,7),"a9":(6,5,7,6,5,6),
"a10":(9,6,6,None,7,8),"a11":(7,5,7,6,6,6),"a12":(6,5,7,6,6,7),"a13":(6,5,6,6,6,7),
"a14":(6,5,7,6,6,7),"a15":(6,5,7,6,6,6),"a16":(6,5,7,6,6,7),"a17":(6,5,6,6,5,6),
"a18":(6,5,6,6,6,7),"a19":(6,5,7,6,5,7),"a20":(6,5,7,6,5,6),"a21":(6,5,6,5,5,7),
"a22":(7,6,8,7,7,7),"a23":(6,6,6,None,6,7),"a24":(6,6,5,7,6,6),"a25":(5,4,6,5,4,7),
"a26":(6,5,6,6,5,6),"a27":(6,5,6,6,5,6),"a28":(7,5,7,6,6,7),"a29":(6,5,7,6,5,6),"a30":(5,4,6,6,5,6),
"a31":(6,6,7,None,6,7),"a32":(6,6,7,6,6,6),"a33":(6,5,6,6,5,6),"a34":(6,5,6,6,5,6),
"a35":(6,6,7,6,6,7),"a36":(6,5,7,6,6,6),"a37":(6,5,7,6,5,6),"a38":(6,6,5,6,5,6),"a39":(6,5,6,6,5,6)}
STAR={"a1":"dest","a2":"top3","a3":"top3","a4":"top3"}
def total(ax):
    R,CA,EV,EF,REP,FI=ax
    if EF is None: return (R*.20+CA*.25+EV*.20+REP*.12+FI*.08)/0.85
    return R*.20+CA*.25+EV*.20+EF*.15+REP*.12+FI*.08
NOCV={"42406571","42425121","42419784","42414621","42432468","42432457","42432455","42432445","42432425","42432424","42432462","42417071","42437322"}
BASICA={"42412527","42422961","42422943","42432441","42432438","42432421","42432461","42427318","42422954","42422944","42411285","42411280","42414613","42414612"}
rows=[]
for a in corpus:
    p=a["pmid"]
    rec=dict(pmid=p,title=a["title"],journal=a["j"],adate=a.get("adate",""),doi=a.get("doi","") or "",abstract=a.get("abs",""))
    if p in pmid2key:
        k=pmid2key[p]; g=assign[k]; ax=AX[k]; R,CA,EV,EF,REP,FI=ax
        pr={"Imprescindible":"alto","Relevante":"medio","Complementario":"bajo"}[g["prio"]]
        rec.update(scored=True,sel=True,sec=g["sec"],ptype=g["ptype"],REL=R,CA=CA,EV=EV,EF=EF,REP=REP,FI=FI,
                   tot=total(ax),pri=pr,pril=g["prio"],star=STAR.get(k,""),mot="")
    else:
        if not a["inwin"]: mot="periodo"
        elif not (a["etype"] and a["has_abs"]): mot="tipo"
        elif p in NOCV: mot="nocv"
        elif p in BASICA: mot="basica"
        else: mot="top5"
        rec.update(scored=False,sel=False,mot=mot,ptype=entype(a["types"]))
    rows.append(rec)
order_mot={"":0,"top5":1,"basica":3,"nocv":3,"tipo":4,"periodo":5}
rows.sort(key=lambda r:(0 if r["scored"] else 1, -(r.get("tot",0) if r["scored"] else 0), order_mot.get(r["mot"],6), r["journal"].lower()))
MOTTXT={"top5":"fuera del top 5 de su sección","basica":"ciencia básica / sin traslación clínica","nocv":"no cardiovascular","tipo":"tipo no elegible / sin resumen"}
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
box_html=f'Revisados / seleccionados por revista (PubMed, 6–12 jul 2026; n.º revisados/seleccionados): {parts}. <b>Total = {ntot} revisados · {nsel} seleccionados.</b>'
src=io.open(BASE+"/n4/articulos-revisados.html",encoding="utf-8").read()
sp=src.find("<tbody>")+len("<tbody>"); ep=src.rfind("</tbody>")
head=src[:sp]; tail=src[ep:]
head=head.replace("· Briefing Cardiovascular · N4","· Briefing Cardiovascular · N5")
head=head.replace('<span class="num">N4</span>','<span class="num">N5</span>')
head=head.replace("Artículos revisados · 29 de junio al 5 de julio de 2026","Artículos revisados · 6 al 12 de julio de 2026")
head=head.replace("2026/06/29–2026/07/05","2026/07/06–2026/07/12")
head=head.replace("29 jun–5 jul 2026","6–12 jul 2026")
head=head.replace("Reglas de selección (N4).","Reglas de selección (N5).")
head=re.sub(r'da <b>\d+ seleccionados</b> esta semana',f'da <b>{nsel} seleccionados</b> esta semana',head)
head=re.sub(r'<div class="box">.*?</div>', '<div class="box">'+box_html+'</div>', head, count=1, flags=re.S)
head=re.sub(r'Listado completo de artículos revisados \(\d+\); puntuados los \d+ seleccionados',
            f'Listado completo de artículos revisados ({ntot}); puntuados los {nsco} seleccionados',head)
head=re.sub(r'mostrando \d+ de \d+ · \d+ seleccionados',f'mostrando {ntot} de {ntot} · {nsel} seleccionados',head)
head=re.sub(r'Se recuperaron <b>\d+ referencias</b>',f'Se recuperaron <b>{ntot} referencias</b>',head)
new_data=[{"p":a["pmid"],"d":a.get("doi","") or "","i":a["pmid"],"t":a["title"],"a":a["abs"] or "[Abstract not available]"} for a in corpus]
tail=re.sub(r'window\.PUBMED_DATA =\[.*?\];', "window.PUBMED_DATA ="+json.dumps(new_data,ensure_ascii=False)+";", tail, count=1, flags=re.S)
full=head+"\n"+rows_html+"\n"+tail
outs=[BASE+"/n5/articulos-revisados.html",
      "/Users/dmarzal/Documents/Claude/Briefing Cardiovascular/Briefing Cardiovascular_N5/Briefing Cardiovascular_N5_artículos revisados.html"]
for outp in outs:
    os.makedirs(os.path.dirname(outp),exist_ok=True)
    io.open(outp,"w",encoding="utf-8").write(full)
print("audit N5:",ntot,"filas,",nsel,"sel")
spec=importlib.util.spec_from_file_location("aaf",GEN+"/add_audit_filters.py")
aaf=importlib.util.module_from_spec(spec); spec.loader.exec_module(aaf)
for p in outs: aaf.process(p)
spec2=importlib.util.spec_from_file_location("aal",GEN+"/add_audit_links.py")
aal=importlib.util.module_from_spec(spec2); spec2.loader.exec_module(aal)
for p in outs:
    try: aal.process(p)
    except Exception as e: print("links warn:",e)
print("filtros + enlaces añadidos")
