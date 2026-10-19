# -*- coding: utf-8 -*-
# Auditoría N19 (12-18 oct 2026). Parte del audit de N17 como plantilla y sustituye filas + datos.
import json, io, html, re, os, importlib.util, glob
_MACBASE = "/Users/dmarzal/Documents/Claude/Briefing Cardiovascular/briefing-cardiovascular-repo"
BASE = _MACBASE if os.path.isdir(_MACBASE) else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = BASE + "/generador"
D1, D2 = "2026/10/12", "2026/10/18"
BADT = {'Editorial', 'Comment', 'Letter', 'Published Erratum', 'News', 'Case Reports'}
corpus = json.load(open(GEN + "/n19_corpus.json"))["recs"]
EL = json.load(open(GEN + "/n19_el.json"))
_selraw = json.load(open(GEN + "/n19_sel.json"))
# Artículos RECUPERADOS POR CROSSREF (el editor los publicó pero PubMed aún no los indexaba,
# PASO 1b de la SKILL): no están en el corpus de PubMed y no tienen PMID. Se añaden como
# registros sintéticos para que figuren en la auditoría con su origen declarado.
_recuperados = {}
for e in EL:
    if e.get("_rec"):
        p = e.get("pmid") or ("CR:" + (e["doi"] or e["title"][:20]))
        e["pmid"] = p
        _recuperados[e["title"].rstrip(".")] = p
        if any((c.get("doi") or "").lower()==(e["doi"] or "").lower() for c in corpus): continue
        corpus.append(dict(pmid=p, journal=e["journal"], title=e["title"], ptypes=e["ptypes"],
                           abstract=e["abstract"], doi=e["doi"], pii="", adate=e["adate"], _crossref=True))
for s in _selraw:
    if not s.get("pmid"):
        s["pmid"] = _recuperados.get(s["title"], "CR:" + s["key"])
sel = {s["pmid"]: s for s in _selraw}
DEST = "a16"; TOP3 = ("a21", "a1", "a17")
SECN = {1: "Cardiología preventiva", 2: "Cardiometabolismo", 3: "Dislipemia", 4: "Cardiopatía isquémica",
        5: "Insuficiencia cardíaca", 6: "Miocardiopatías", 7: "Valvulopatías", 8: "Imagen cardíaca",
        9: "Cardiología intervencionista", 10: "Arritmias y electrofisiología"}
def esc(s): return html.escape(s or "", quote=False)
def num(x): return ("%.1f" % x).replace(".", ",")
PTYPE_EN = {"Journal Article": "Investigación original", "Review": "Artículo de revisión", "Meta-Analysis": "Metaanálisis",
    "Systematic Review": "Revisión sistemática", "Network Meta-Analysis": "Metaanálisis",
    "Randomized Controlled Trial": "Ensayo clínico aleatorizado", "Editorial": "Editorial", "Letter": "Carta al editor",
    "Comment": "Comentario", "Published Erratum": "Corrección/Errata", "Observational Study": "Estudio observacional",
    "Multicenter Study": "Estudio observacional", "Case Reports": "Caso clínico", "Practice Guideline": "Guía de práctica clínica",
    "Guideline": "Guía de práctica clínica", "Clinical Trial": "Ensayo clínico aleatorizado",
    "Comparative Study": "Investigación original", "Validation Study": "Estudio diagnóstico", "News": "Noticia",
    "Equivalence Trial": "Ensayo clínico aleatorizado", "Consensus Development Conference": "Documento de consenso"}
def entype(pts):
    for p in ["Randomized Controlled Trial", "Meta-Analysis", "Network Meta-Analysis", "Systematic Review",
              "Practice Guideline", "Guideline", "Editorial", "Letter", "Comment", "Published Erratum", "News",
              "Case Reports", "Review", "Observational Study", "Clinical Trial", "Multicenter Study"]:
        if p in pts: return PTYPE_EN[p]
    for p in pts:
        if p in PTYPE_EN: return PTYPE_EN[p]
    return esc(pts[0]) if pts else "—"
# Motivos de descarte procedentes del CRIBADO (n17_out*.json), no de listas escritas a mano.
NOCV, BASICA, NOELIG, DUPN = set(), set(), set(), set()
for f in sorted(glob.glob(GEN + "/n19_out[0-9].json")):
    for o in json.load(open(f)):
        if o.get("elegible"): continue
        p = EL[o["idx"]]["pmid"]; m = o.get("motivo_descarte", "")
        if "duplicado" in m: DUPN.add(p)
        elif "no cardiovascular" in m: NOCV.add(p)
        elif "básica" in m: BASICA.add(p)
        else: NOELIG.add(p)
# Ya publicados en N17 (EuroIntervention recuperados por Crossref en el Mac): fuera de N19 (Mac, 12-oct-2026).
DUPN |= {"42837204", "42837205", "42837202"}
# Excluidos por DECISIÓN EDITORIAL (ámbito). En N19 no hay ninguno.
FUERA_AMBITO = set()
rows = []
for a in corpus:
    p = a["pmid"]
    inwin = D1 <= a["adate"] <= D2
    has_abs = bool(a["abstract"])
    etype = not (set(a["ptypes"]) & BADT) and p not in NOELIG
    rec = dict(pmid=p, title=a["title"].rstrip("."), journal=a["journal"], adate=a["adate"], doi=a["doi"] or "",
               abstract=a["abstract"])
    if p in sel:
        g = sel[p]
        pr = {"Imprescindible": "alto", "Relevante": "medio", "Complementario": "bajo"}[g["prio"]]
        star = "dest" if g["key"] == DEST else ("top3" if g["key"] in TOP3 else "")
        rec.update(scored=True, sel=True, sec=g["sec"], ptype=g["ptype"], REL=g["rel"], CA=g["cambio"], EV=g["evid"],
                   EF=g["efecto"], REP=g["rep"], FI=g["fi"], tot=g["total"], pri=pr, pril=g["prio"], star=star, mot="")
    else:
        if p in FUERA_AMBITO: mot = "ambito"
        elif p in DUPN: mot = "dup"
        elif not inwin: mot = "periodo"
        elif not (etype and has_abs): mot = "tipo"
        elif p in NOCV: mot = "nocv"
        elif p in BASICA: mot = "basica"
        else: mot = "top5"
        rec.update(scored=False, sel=False, mot=mot, ptype=entype(a["ptypes"]))
    rows.append(rec)
order_mot = {"": 0, "top5": 1, "ambito": 2, "dup": 2, "basica": 3, "nocv": 3, "tipo": 4, "periodo": 5}
rows.sort(key=lambda r: (0 if r["scored"] else 1, -(r.get("tot", 0) if r["scored"] else 0),
                         order_mot.get(r["mot"], 6), r["journal"].lower()))
MOTTXT = {"top5": "fuera del top 5 de su sección", "basica": "ciencia básica / sin traslación clínica",
          "ambito": "fuera del ámbito de la cardiología clínica",
          "dup": "ya publicado en el número anterior (N17)",
          "nocv": "no cardiovascular", "tipo": "tipo no elegible / sin resumen"}
def motcell(r):
    if r["sel"]: return '<td class="estado"><span class="est-sel">Seleccionado</span></td>'
    if r["mot"] == "periodo":
        return f'<td class="estado"><span class="est-desc">Descartado</span><span class="est-mot">fuera de periodo (online {esc(r["adate"] or "s/f")})</span></td>'
    return f'<td class="estado"><span class="est-desc">Descartado</span><span class="est-mot">{MOTTXT.get(r["mot"], "descartado")}</span></td>'
tr = []
for i, r in enumerate(rows, 1):
    if r["scored"]:
        sec = f'{r["sec"]:02d} {SECN[r["sec"]]}'; cat = f'c{r["sec"]}'
        scs = "".join(f'<td class="sc">{v if v is not None else "—"}</td>'
                      for v in [r["REL"], r["CA"], r["EV"], r["EF"], r["REP"], r["FI"]])
        tot = f'<td class="tot">{num(r["tot"])}</td>'
        pric = f'<td class="pri"><span class="dot d-{r["pri"]}"></span>{r["pril"]}</td>'; dpri = r["pri"]
        stars = ("★★" if r["star"] == "dest" else ("★" if r["star"] == "top3" else ""))
    else:
        sec = "—"; cat = ""; scs = '<td class="sc">—</td>' * 6; tot = '<td class="tot">—</td>'
        pric = '<td class="pri">—</td>'; dpri = ""; stars = ""
    star_html = "".join(f'<span class="star">{ch}</span>' for ch in stars)
    badge = '<span class="selbadge">Sel</span>' if r["sel"] else '<span class="descbadge">Desc</span>'
    cls_tr = "sel" if r["sel"] else "desc"; dsel = "1" if r["sel"] else "0"; dest = "sel" if r["sel"] else "desc"
    art = f'{esc(r["title"])} {star_html}{badge}'
    tr.append(f'<tr class="{cls_tr}" data-pri="{dpri}" data-sel="{dsel}" data-estado="{dest}" data-cat="{cat}" '
              f'data-mot="{r["mot"] if not r["sel"] else ""}"><td class="num">{i}</td><td class="art">{art}</td>'
              f'<td class="rev">{esc(r["journal"])}</td><td class="sec">{esc(sec)}</td><td class="tipo">{esc(r["ptype"])}</td>'
              f'{scs}{tot}{pric}{motcell(r)}</tr>')
rows_html = "\n".join(tr)
ntot = len(rows); nsel = sum(1 for r in rows if r["sel"])
from collections import Counter
rev_tot = Counter(r["journal"] for r in rows); rev_sel = Counter(r["journal"] for r in rows if r["sel"])
parts = " · ".join(f"<b>{esc(jr)}</b> {rev_tot[jr]}/{rev_sel[jr]}"
                   for jr in sorted(rev_tot, key=lambda s: (-rev_sel[s], -rev_tot[s], s.lower())))
box_html = (f'Revisados / seleccionados por revista (PubMed, 5 – 11 oct 2026; n.º revisados/seleccionados): {parts}. '
            f'<b>Total = {ntot} revisados · {nsel} seleccionados.</b>')
src = io.open(BASE + "/n17/articulos-revisados.html", encoding="utf-8").read()
sp = src.find("<tbody>") + len("<tbody>"); ep = src.rfind("</tbody>")
head = src[:sp]; tail = src[ep:]
head = head.replace("· Briefing Cardiovascular · N17", "· Briefing Cardiovascular · N19")
head = head.replace('<span class="num">N17</span>', '<span class="num">N19</span>')
# El periodo de la plantilla se sustituye por REGEX (no por cadena literal): así el generador
# sigue funcionando aunque se corrija el periodo del número que sirve de plantilla.
head = re.sub(r'Artículos revisados · \d+[^<]*?de \d{4}',
              'Artículos revisados · 12 al 18 de octubre de 2026', head)
head = re.sub(r'2026/\d\d/\d\d–2026/\d\d/\d\d', '2026/10/12–2026/10/18', head)
head = re.sub(r'\d+\s*[–-]\s*\d+ (?:ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic) 2026',
              '12 – 18 oct 2026', head)
head = head.replace("Reglas de selección (N17).", "Reglas de selección (N19).")
NOTA_TOP3 = ('<p class="intro" style="margin-top:10px;"><b>Nota sobre la selección de N19.</b> '
 'Semana sin congreso y sin guías mayores: <b>ningún artículo alcanza el umbral de Imprescindible</b> '
 '(CAMBIO ≥ 8 o TOTAL ≥ 8), igual que ocurrió en N18. El ★ <b>Destacado</b> y los tres titulares de '
 '«No te los puedes perder» son, esta semana, <b>exactamente los cuatro primeros de la rúbrica de 6 ejes</b>, '
 'sin ninguna corrección editorial: a16 (7,48), el <i>Scientific Statement</i> de la AHA sobre el abordaje '
 'multidisciplinar de la antiagregación en los síndromes coronarios (<i>Circulation</i>), seguido del documento '
 'de consenso EAPCI/ACVC sobre soporte circulatorio mecánico temporal en el shock cardiogénico '
 '(<i>Eur Heart J</i>, a21, 7,00), el <i>Scientific Statement</i> 2026 del ACC sobre prescripción de ejercicio '
 '(<i>J Am Coll Cardiol</i>, a1, 6,95) y la comparación de revascularización completa inmediata frente a '
 'diferida en el IAMCEST con enfermedad multivaso (<i>JACC Cardiovasc Interv</i>, a17, 6,92). '
 '<b>Decisión editorial de ámbito:</b> el ensayo ICRAKI de <i>N Engl J Med</i> (hemodiálisis intermitente '
 'frente a terapia continua de reemplazo renal en el fracaso renal agudo del paciente crítico, '
 'NEJMoa2608397) se descartó con el motivo «no cardiovascular»: la inclusión obligatoria de <i>NEJM</i> y '
 '<i>Lancet</i> cubre los artículos <i>de medicina cardiovascular</i>, y este es un ensayo de nefrología y '
 'cuidados críticos con objetivo primario renal. Por el mismo criterio salió la revisión de <i>NEJM</i> sobre '
 'el trastorno por déficit de atención del adulto. '
 'La <b>auditoría de cobertura por Crossref</b> (PASO 1b) recuperó un artículo que la búsqueda por <i>edat</i> '
 'no vio porque el filtro temático generalista no lo capturó: el ensayo de <i>N Engl J Med</i> de '
 'monitorización continua de glucosa en la diabetes tipo 2 no tratada con insulina (CONNECT, a6). '
 'Las ausencias de <i>Lancet</i> (28), <i>JAMA</i> (40) y <i>N Engl J Med</i> (4) se revisaron una a una: son '
 'correspondencia, editoriales, obituarios, resúmenes de investigación o material no cardiovascular. '
 'Quedan <b>pendientes para el Mac</b> siete artículos de <i>EuroIntervention</i> que el editor depositó en la '
 'ventana y que no están en PubMed ni traen resumen en Crossref: el egreso de red de la nube no alcanza a '
 'eurointervention.pcronline.com, así que por la regla del resumen quedan fuera de este número y se anotan en '
 '<i>n19_euro.json</i> y <i>n19_pendiente_mac.json</i>. '
 'Valvulopatías se queda con <b>3 fichas</b> por no reunir más artículos elegibles esa semana: no se rellena.</p>')
head = re.sub(r'<p class="intro" style="margin-top:10px;"><b>Nota sobre el bloque.*?</p>', lambda _m: NOTA_TOP3, head, count=1, flags=re.S)
head = re.sub(r'da <b>\d+ seleccionados</b> esta semana', f'da <b>{nsel} seleccionados</b> esta semana', head)
head = re.sub(r'<div class="box">.*?</div>', lambda _m: '<div class="box">' + box_html + '</div>', head, count=1, flags=re.S)
head = re.sub(r'Listado completo de artículos revisados \(\d+\); puntuados los \d+ seleccionados',
              f'Listado completo de artículos revisados ({ntot}); puntuados los {nsel} seleccionados', head)
head = re.sub(r'mostrando \d+ de \d+ · \d+ seleccionados', f'mostrando {ntot} de {ntot} · {nsel} seleccionados', head)
head = re.sub(r'Se recuperaron <b>\d+ referencias</b>', f'Se recuperaron <b>{ntot} referencias</b>', head)
# --- Correcciones de la metodología heredada de la plantilla (7-sep-2026):
# 1) La anulación «las guías no puntúan EFECTO» fue DEROGADA el 31/08/2026: ahora SÍ lo puntúan
#    (8-10 una guía mayor de ESC/ACC/AHA), con la fórmula normal de 6 ejes.
head = head.replace("guías —sin EFECTO— y ensayos negativos",
                    "guías y consensos —que puntúan EFECTO por su respaldo institucional— y ensayos negativos")
# 1b) Y la frase gemela de la leyenda: en N14 los tres documentos de sociedad (a2, a39, a46)
#     SÍ llevan EFECTO puntuado (7, 6 y 7), así que anunciar «EFECTO = —» era falso.
head = re.sub(r'En las guías/consensos y los documentos sin resultado cuantitativo, <b>EFECTO = «—»</b>',
              'En los documentos sin resultado cuantitativo, <b>EFECTO = «—»</b>; las guías, consensos y '
              'statements de sociedad SÍ puntúan EFECTO (8-10 una guía mayor de ESC/ACC/AHA; 6-8 un '
              'consenso o statement de alcance más limitado)', head)
# 2) El corpus ya no sale solo de PubMed: la auditoría de cobertura (PASO 0.2.b) incorpora
#    los artículos que el editor publicó y PubMed no indexó, recuperados por Crossref.
head = head.replace(
  "Auditoría completa de la búsqueda semanal en PubMed",
  "Auditoría completa de la búsqueda semanal en PubMed, ampliada con los artículos que el editor "
  "publicó en la ventana y PubMed no había indexado, recuperados por Crossref y verificados en la "
  "web del editor (auditoría de cobertura)")
try:
    _fix = json.load(open(GEN + "/n19_linkfix.json"))
    NO_DOI = {s["pmid"] for s in sel.values() if s["key"] in _fix}
except FileNotFoundError:
    NO_DOI = set()
new_data = [{"p": a["pmid"], "d": ("" if a["pmid"] in NO_DOI else (a["doi"] or "")), "i": a["pmid"],
             "t": a["title"].rstrip("."), "a": a["abstract"] or "[Abstract not available]"} for a in corpus]
_pd = "window.PUBMED_DATA =" + json.dumps(new_data, ensure_ascii=False) + ";"
tail = re.sub(r'window\.PUBMED_DATA =\[.*?\];', lambda _m: _pd, tail, count=1, flags=re.S)
full = head + "\n" + rows_html + "\n" + tail
outs = [BASE + "/n19/articulos-revisados.html"]
_localdir = "/Users/dmarzal/Documents/Claude/Briefing Cardiovascular/Briefing Cardiovascular_N19"
if os.path.isdir(os.path.dirname(_localdir)):
    outs.append(_localdir + "/Briefing Cardiovascular_N19_artículos revisados.html")
for outp in outs:
    os.makedirs(os.path.dirname(outp), exist_ok=True)
    io.open(outp, "w", encoding="utf-8").write(full)
print("audit N19:", ntot, "filas,", nsel, "sel")
spec = importlib.util.spec_from_file_location("aaf", GEN + "/add_audit_filters.py")
aaf = importlib.util.module_from_spec(spec); spec.loader.exec_module(aaf)
for p in outs: aaf.process(p)
spec2 = importlib.util.spec_from_file_location("aal", GEN + "/add_audit_links.py")
aal = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(aal)
for p in outs:
    try: aal.process(p)
    except Exception as e: print("links warn:", e)
print("filtros + enlaces añadidos")
