import json,io,html,re
corpus=json.load(open("/tmp/n2_corpus.json"))
elig=json.load(open("/tmp/n2_eligibles.json"))
cls={}
for i in range(4): cls.update(json.load(open(f"/tmp/n2_cls{i}.json")))
selset={a["key"] for a in json.load(open("/tmp/n2_selected.json"))}
elig_by_pmid={a["pmid"]:a for a in elig}
DEST="a017"; TOP3={"a004","a009","a023"}
SECN={1:"Cardiología preventiva",2:"Cardiometabolismo",3:"Dislipemia",4:"Cardiopatía isquémica",5:"Insuficiencia cardíaca",6:"Miocardiopatías",7:"Valvulopatías",8:"Imagen cardíaca",9:"Cardiología intervencionista",10:"Arritmias y electrofisiología"}
FI={"N Engl J Med":10,"Lancet":10,"JAMA":9,"BMJ":9,"Nat Med":9,"Ann Intern Med":9,"Nat Rev Cardiol":9,"Eur Heart J":8,"Circulation":8,"J Am Coll Cardiol":8,"JAMA Cardiol":7,"Eur J Heart Fail":6,"JACC Heart Fail":6,"EuroIntervention":6,"JACC Cardiovasc Interv":6,"Heart Rhythm":6,"Hypertension":6,"JACC Cardiovasc Imaging":6,"Circ Res":6,"Nat Cardiovasc Res":6,"Circ Heart Fail":5,"Circ Cardiovasc Interv":5,"Europace":5,"JACC Clin Electrophysiol":5,"Eur Heart J Cardiovasc Imaging":5,"Eur J Prev Cardiol":5,"Heart":5,"Atherosclerosis":5,"Rev Esp Cardiol":4,"J Am Heart Assoc":4,"JACC Adv":4}
def fi(j): return FI.get(j,4)
def total(c,j):
    REL,CA,EV,EF,REP,F=c["REL"],c["CAMBIO"],c["EVID"],c["EFECTO"],c["REP"],fi(j)
    if EF is None: return (REL*.20+CA*.25+EV*.20+REP*.12+F*.08)/0.85
    return REL*.20+CA*.25+EV*.20+EF*.15+REP*.12+F*.08
def prio(c,t):
    if (c["CAMBIO"] or 0)>=8 or t>=8: return ("alto","Imprescindible")
    return ("medio","Relevante") if t>=5 else ("bajo","Complementario")
def esc(s): return html.escape(s or "",quote=False)
def num(x): return ("%.1f"%x).replace(".",",")
PTYPE_EN={"Journal Article":"Investigación original","Review":"Revisión","Meta-Analysis":"Metaanálisis","Systematic Review":"Revisión sistemática","Randomized Controlled Trial":"Ensayo clínico aleatorizado","Editorial":"Editorial","Letter":"Carta","Comment":"Comentario","Observational Study":"Estudio observacional","Multicenter Study":"Estudio multicéntrico","Case Reports":"Caso clínico","Practice Guideline":"Guía de práctica clínica","Clinical Trial":"Ensayo clínico"}
def entype(pts):
    for p in ["Randomized Controlled Trial","Meta-Analysis","Systematic Review","Practice Guideline","Review","Observational Study"]:
        if p in pts: return PTYPE_EN[p]
    for p in pts:
        if p in PTYPE_EN: return PTYPE_EN[p]
    return pts[0] if pts else "—"
rows=[]
for a in corpus:
    pmid=a["pmid"]; j=a["journal"]; online=a.get("online") or a.get("entrez")
    inwin = bool(online and "2026-06-15"<=online<="2026-06-21")
    e=elig_by_pmid.get(pmid); c=cls.get(e["nid"]) if e else None
    rec=dict(pmid=pmid,title=a["title"],journal=j,online=online)
    if c and c.get("cv")==1 and c.get("sec"):
        t=total(c,j); pr,prl=prio(c,t); k=e["nid"]
        rec.update(scored=True,sec=c["sec"],ptype=c["ptype"],REL=c["REL"],CA=c["CAMBIO"],EV=c["EVID"],EF=c["EFECTO"],REP=c["REP"],FI=fi(j),tot=t,pri=pr,pril=prl,sel=(k in selset),key=k,mot="" if k in selset else "top5")
    elif c and c.get("cv")==0:
        rec.update(scored=False,sel=False,mot="nocv",ptype=entype(a["ptypes"]))
    elif inwin:
        rec.update(scored=False,sel=False,mot="tipo",ptype=entype(a["ptypes"]))
    else:
        rec.update(scored=False,sel=False,mot="periodo",ptype=entype(a["ptypes"]))
    rows.append(rec)
order_mot={"":0,"top5":0,"nocv":1,"tipo":2,"periodo":3}
rows.sort(key=lambda r:(0 if r["scored"] else 1, -(r.get("tot",0) if r["scored"] else 0), order_mot.get(r["mot"],4)))
MOTTXT={"top5":"fuera del top 5 de su sección","nocv":"no cardiovascular","tipo":"tipo no elegible / sin resumen"}
def motcell(r):
    if r["sel"]: return '<td class="estado"><span class="est-sel">Seleccionado</span></td>'
    if r["mot"]=="periodo":
        return f'<td class="estado"><span class="est-desc">Descartado</span><span class="est-mot">fuera de periodo (online {esc(r["online"] or "s/f")})</span></td>'
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
nsel=sum(1 for r in rows if r["sel"]); ntot=len(rows); nsco=sum(1 for r in rows if r["scored"])
head=io.open("/tmp/audit_head.txt",encoding="utf-8").read()
tail=io.open("/tmp/audit_tail.txt",encoding="utf-8").read()
head=head.replace("<title>Artículos revisados · Briefing Cardiovascular · N0</title>","<title>Artículos revisados · Briefing Cardiovascular · N2</title>")
head=head.replace('<span class="num">N1</span>','<span class="num">N2</span>')
head=head.replace("Artículos revisados · 8 al 14 de junio de 2026","Artículos revisados · 15 al 21 de junio de 2026")
head=head.replace("2026/06/08–2026/06/14","2026/06/15–2026/06/21")
head=head.replace("Se recuperaron <b>376 artículos</b>",f"Se recuperaron <b>{ntot} referencias</b>")
head=head.replace("Listado completo de artículos revisados, puntuados (376)",f"Listado completo de artículos revisados ({ntot}); puntuados los {nsco} elegibles")
head=head.replace("mostrando 376 de 376 · 45 seleccionados",f"mostrando {ntot} de {ntot} · {nsel} seleccionados")
head=re.sub(r'\b376\b',str(ntot),head)
new_data=[{"p":a["pmid"],"d":a.get("doi","") or "","i":a["pmid"],"t":a["title"],"a":a["abstract"] or "[Abstract not available]"} for a in corpus]
tail=re.sub(r'window\.PUBMED_DATA =\[.*?\];', "window.PUBMED_DATA ="+json.dumps(new_data,ensure_ascii=False)+";", tail, count=1, flags=re.S)
full=head+"\n"+rows_html+"\n"+tail
for outp in ["/Users/dmarzal/Documents/Claude/Briefing Cardiovascular/briefing-cardiovascular-repo/n2/articulos-revisados.html",
             "/Users/dmarzal/Documents/Claude/Briefing Cardiovascular/Briefing Cardiovascular_N2/Briefing Cardiovascular_N2_artículos revisados.html"]:
    io.open(outp,"w",encoding="utf-8").write(full)
print("audit regenerado:",ntot,"filas,",nsel,"sel,",nsco,"puntuados")

# --- filtros por revista y tipo (post-proceso, ver add_audit_filters.py) ---
import os as _os, importlib.util as _ilu
_spec=_ilu.spec_from_file_location("aaf",_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),"add_audit_filters.py"))
_aaf=_ilu.module_from_spec(_spec); _spec.loader.exec_module(_aaf)
for _p in ["/Users/dmarzal/Documents/Claude/Briefing Cardiovascular/briefing-cardiovascular-repo/n2/articulos-revisados.html",
           "/Users/dmarzal/Documents/Claude/Briefing Cardiovascular/Briefing Cardiovascular_N2/Briefing Cardiovascular_N2_artículos revisados.html"]:
    _aaf.process(_p)
print("filtros revista+tipo añadidos al audit")
