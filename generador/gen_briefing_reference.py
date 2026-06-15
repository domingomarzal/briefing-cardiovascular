# -*- coding: utf-8 -*-
from urllib.parse import quote

# ---- section colors (elegant, mutually distinguishable) ----
SECTION_COLORS = {  # paleta viva (jun 2026): vívida y alegre, blanco legible sobre el badge
 1:"#0fa6ae", 2:"#e08e0b", 3:"#5aa82f", 4:"#e0443c", 5:"#2f7fe6",
 6:"#8b54d6", 7:"#11a87d", 8:"#e2670c", 9:"#d43d8c", 10:"#4b57c9",
}

IMP = {"Imprescindible":"alto","Relevante":"medio","Complementario":"bajo"}

def jlink(doi, title):
    if doi:
        return "https://doi.org/"+doi
    return "https://pubmed.ncbi.nlm.nih.gov/?term="+quote(title)

# Each article:
# key, title, ptype, prio, journal(short), doi, resumen, why, modal=[(label,text),...]
import json as _json
_sel=_json.load(open("/tmp/n1_selected.json"))
_fi=_json.load(open("/tmp/n1_fichas.json"))
_ACR={"e078":" (LOGICAL)","e018":" (ABYSS)","e068":" (OPTION)","e026":" (DECLARE-TIMI 58)","e053":" (REDUCE LAP-HF II)","e066":" (CRESCENT)","e103":" (REIMAGINE 3)"}
SECNAMES={1:"Cardiolog\u00eda preventiva",2:"Cardiometabolismo",3:"Dislipemia",4:"Cardiopat\u00eda isqu\u00e9mica",5:"Insuficiencia card\u00edaca",6:"Miocardiopat\u00edas",7:"Valvulopat\u00edas",8:"Imagen card\u00edaca",9:"Cardiolog\u00eda intervencionista y estructural",10:"Arritmias y electrofisiolog\u00eda"}
_by={}
for a in _sel:
    k=a["key"]; f=_fi.get(k,{})
    _ac=_ACR.get(k,""); ttl=a["title"]+(_ac if _ac.strip(" ()") not in a["title"] else "")
    art=dict(key=k,title=ttl,ptype=a["ptype"],prio=a["prio"],journal=a["journal"],doi=a.get("doi","") or "",
             resumen=f.get("resumen",""),why=f.get("why",""),
             modal=[("De qu\u00e9 va.",f.get("deque","")),("Resultados.",f.get("resultados","")),("Conclusiones.",f.get("conclusiones",""))],
             _total=a["total"])
    _by.setdefault(a["sec"],[]).append(art)
SECTIONS=[]
for _sn in range(1,11):
    _arts=sorted(_by.get(_sn,[]),key=lambda x:-x["_total"])
    SECTIONS.append((_sn,SECNAMES[_sn],_arts))
DESTACADO_KEY="e002"
TOP3=["e061","e004","e103"]
ALL={}
for snum,sname,arts in SECTIONS:
    for a in arts:
        ALL[a["key"]]=a; a["_section"]=sname

def esc(s):
    return s  # text already HTML-safe (entities pre-encoded where needed)

def journal_anchor(a, extra=""):
    href = jlink(a["doi"], a["title"])
    cls = "j t3j" if extra=="t3" else "j"
    return f'<a class="{cls}" href="{href}" target="_blank">{a["journal"]} <span class="go">↗</span></a>'

def modal_html(a):
    body = "".join(f'<p><b>{lab}</b> {txt}</p>' for lab,txt in a["modal"])
    cid = "cb-a-"+a["key"]
    return (f'<input type="checkbox" id="{cid}" class="mcb"><div class="cmodal">'
            f'<label class="cmodal-bg" for="{cid}"></label><div class="cmodal-box">'
            f'<label class="cmodal-x" for="{cid}" aria-label="Cerrar">&times;</label>'
            f'<div class="modal-type">{a["ptype"]}</div>'
            f'<h3 class="modal-title">{a["title"]}</h3>'
            f'<div class="modal-body">{body}</div>'
            f'<div class="modal-links">{journal_anchor(a)}</div></div></div>')

def article_html(a):
    imp = IMP[a["prio"]]
    return (f'<article id="a-{a["key"]}" data-impact="{imp}">'
            f'<div class="card-top"><span class="ptype">{a["ptype"]}</span>'
            f'<span class="impact"><span class="dot d-{imp}"></span></span></div>'
            f'<h4><label class="ml" for="cb-a-{a["key"]}">{a["title"]}</label></h4>'
            f'<div class="a-body"><p>{a["resumen"]}</p>'
            f'<p class="why"><b>Por qué importa:</b> {a["why"]}</p>'
            f'<div class="jwrap">{journal_anchor(a)}</div></div></article>')

# ---------- assemble index ----------
index_items = ""
for snum, sname, arts in SECTIONS:
    index_items += (f'<li><a class="ix" href="#s{snum}">'
                    f'<span><span class="nn c{snum}">{snum:02d}</span>{sname}</span></a></li>\n')

# ---------- top3 ----------
top3_li = ""
for i,k in enumerate(TOP3,1):
    a = ALL[k]
    top3_li += (f'<li><div class="t3main"><span class="rk">{i}</span>'
                f'<label class="t3t" for="cb-a-{k}">{a["title"]}</label></div>'
                f'<div class="t3aside">{journal_anchor(a,"t3")}'
                f'<span class="t3s">{a["_section"]}</span></div></li>\n')

# ---------- sections ----------
sections_html = ""
PRIO_RANK = {"alto":0, "medio":1, "bajo":2}
def _grp(a):
    return 0 if a["key"]==DESTACADO_KEY else (1 if a["key"] in TOP3 else 2)
for snum, sname, arts in SECTIONS:
    # Las 10 secciones se muestran SIEMPRE. Una sección sin ningún artículo esa semana
    # muestra una nota en lugar de fichas (con 1 o más, se muestran las fichas).
    if len(arts) == 0:
        arts_html = '<p class="nonews">Sin novedades relevantes esta semana.</p>'
    else:
        # Orden: prioridad (Imprescindible→Relevante→Complementario); dentro de la misma
        # prioridad, Destacado → "No te los puedes perder" → resto; a igualdad, mayor TOTAL
        # (el orden original de la lista ya está en TOTAL descendente).
        ordered = [a for _, a in sorted(enumerate(arts),
            key=lambda t: (PRIO_RANK[IMP[t[1]["prio"]]], _grp(t[1]), -t[1]["_total"]))]
        arts_html = "\n".join(article_html(a) for a in ordered)
    sections_html += f'''
    <section class="sec" id="s{snum}">
      <a class="sec-head" href="#s{snum}" data-sec="{snum}">
        <span class="sec-num c{snum}">{snum:02d}</span><h2>{sname}</h2>
<span class="chev t{snum}">▸</span>
      </a>
      <div class="sec-body">
        {arts_html}
        <div class="sec-foot"><a href="#indice" class="toindex" title="Volver a Secciones" aria-label="Volver a Secciones">↩︎</a></div>
      </div>
    </section>
'''

# ---------- modals ----------
modals_html = "\n  ".join(modal_html(a) for _,_,arts in SECTIONS for a in arts)

# section color CSS
color_css = "\n".join(
    f'  .c{n}{{background:{c};color:#fff;}} .indice .nn.c{n}{{background:transparent;color:{c};}} .chev.t{n}{{color:{c};}}'
    for n,c in SECTION_COLORS.items())

dest = ALL[DESTACADO_KEY]
dest_href = jlink(dest["doi"], dest["title"])

HTML = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Briefing Cardiovascular · UICAR · Quirónsalud — N1</title>
<style>
  :root{{
    --ink:#16202e; --gris:#5d6878; --suave:#8c97a6; --linea:#e7ebf1; --linea2:#eef1f6;
    --fondo:#eceff4; --papel:#ffffff;
    --navy:#0a3d62; --navy2:#072b46; --teal:#0f9aa0; --teal-soft:#f2f9f9;
    --titulo:#103a47; --jhover:#0a3d62;
    --imp-alto:#b23b46; --imp-medio:#c08416; --imp-bajo:#3a8a63;
  }}
  *{{box-sizing:border-box;}}
  html{{scroll-behavior:smooth;}}
  body{{margin:0;background:var(--fondo);color:var(--ink);
    font-family:"Segoe UI",-apple-system,BlinkMacSystemFont,Roboto,Helvetica,Arial,sans-serif;
    line-height:1.55;font-size:16px;-webkit-font-smoothing:antialiased;
    -webkit-print-color-adjust:exact;print-color-adjust:exact;}}
  @media print{{
    body{{background:#ffffff;}}
    .wrap{{max-width:100%;margin:0;border-radius:0;box-shadow:none;}}
    .filtros{{display:none;}}
    .sec-body{{display:block!important;}}
    .chev{{display:none;}}
    article{{break-inside:avoid;}}
    .destacado,.top3,.indice{{break-inside:avoid;}}
  }}
  @page{{margin:14mm 12mm;}}
  .wrap{{max-width:1040px;margin:24px auto;background:var(--papel);
    box-shadow:0 4px 22px rgba(16,21,31,.09);border-radius:14px;overflow:hidden;}}

  /* MASTHEAD */
  .mast{{background:linear-gradient(135deg,var(--navy) 0%,var(--navy2) 100%);color:#fff;padding:30px 40px 24px;}}
  .mast-row{{display:flex;justify-content:space-between;align-items:flex-start;gap:20px;}}
  .mast-title{{margin:0;font-size:37px;font-weight:800;letter-spacing:-.02em;line-height:1.0;}}
  .mast-title .ac{{color:var(--teal);}}
  .mast-sub{{margin-top:11px;font-size:16px;color:#c4d4df;font-weight:500;}}
  .mast-sub b{{color:#fff;font-weight:700;letter-spacing:.02em;}}
  .mast-sub .md{{color:var(--teal);font-weight:700;margin:0 5px;}}
  .mast-right{{flex:0 0 auto;display:flex;flex-direction:column;align-items:flex-end;gap:9px;padding-top:4px;}}
  .mast-right .num{{border:1.5px solid var(--teal);color:#bdeaeb;font-weight:700;font-size:14px;
    padding:5px 16px;border-radius:30px;letter-spacing:.04em;white-space:nowrap;}}
  .mast-right .periodo{{font-size:13px;color:#aac3d1;white-space:nowrap;}}
  .mast-rule{{height:1px;background:rgba(255,255,255,.16);margin-top:20px;}}

  main{{padding:24px 40px 0;}}

  /* DESTACADO */
  .destacado{{margin:0 0 6px;border:1px solid var(--linea);border-left:4px solid var(--teal);
    border-radius:10px;background:#fbfdfd;padding:18px 22px;}}
  .destacado .d-top{{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-bottom:4px;}}
  .destacado .d-kicker{{font-size:13px;font-weight:700;letter-spacing:.02em;font-family:Arial,Helvetica,sans-serif;text-transform:none;color:var(--teal);}}
  .destacado .d-grid{{display:grid;grid-template-columns:1fr 180px;gap:22px;align-items:center;margin-top:6px;}}
  .destacado h2{{margin:4px 0 8px;font-size:20px;line-height:1.25;color:var(--titulo);font-weight:800;text-align:justify;}}
  .destacado p{{margin:6px 0;font-size:14.5px;text-align:justify;}}

  /* TOP 3 — dos columnas como el Destacado */
  .top3{{margin:26px 0 4px;border:1px solid var(--linea);border-radius:12px;overflow:hidden;}}
  .top3 .t3h{{display:flex;align-items:center;gap:8px;padding:11px 18px;background:var(--navy);color:#fff;}}
  .top3 .t3h .star{{color:var(--teal);font-size:15px;}}
  .top3 .t3h h3{{margin:0;font-size:14px;font-weight:800;letter-spacing:.02em;}}
  .top3 ol{{margin:0;padding:4px 22px;list-style:none;}}
  .top3 li{{display:grid;grid-template-columns:1fr 180px;gap:22px;align-items:start;
    padding:13px 0;border-bottom:1px solid var(--linea2);}}
  .top3 li:last-child{{border-bottom:none;}}
  .top3 .t3main{{display:flex;gap:13px;align-items:flex-start;min-width:0;}}
  .top3 .rk{{flex:0 0 auto;width:23px;height:23px;border-radius:50%;background:var(--teal-soft);
    color:var(--teal);font-weight:800;font-size:13px;display:flex;align-items:center;justify-content:center;margin-top:2px;}}
  .top3 .t3t{{font-size:16px;font-weight:700;color:var(--titulo);text-decoration:none;line-height:1.32;
    text-align:justify;display:block;cursor:pointer;}}
  .top3 .t3t:hover{{color:var(--teal);}}
  .top3 .t3aside{{text-align:right;display:flex;flex-direction:column;align-items:flex-end;gap:5px;padding-top:2px;}}
  .top3 .t3s{{font-size:13px;font-weight:700;letter-spacing:.02em;font-family:Arial,Helvetica,sans-serif;text-transform:none;color:var(--suave);}}

  /* ÍNDICE / SECCIONES */
  .indice{{margin:24px 0 4px;border:1px solid var(--linea);border-radius:10px;padding:6px;}}
  .indice h3{{margin:6px 12px 8px;font-size:13px;font-weight:700;letter-spacing:.02em;font-family:Arial,Helvetica,sans-serif;text-transform:none;color:var(--suave);}}
  .indice ol{{margin:0;padding:0;list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:1px;}}
  .indice li .ix{{display:flex;justify-content:flex-start;align-items:center;gap:8px;cursor:pointer;text-decoration:none;
    color:var(--ink);font-size:14.5px;padding:8px 16px;border-radius:7px;}}
  .indice li .ix:hover{{background:#f5f7fa;}}
  .indice .nn{{font-weight:800;font-size:12px;margin-right:11px;display:inline-flex;align-items:center;justify-content:center;
    width:25px;height:19px;border-radius:5px;letter-spacing:.02em;vertical-align:middle;}}

  /* FILTROS */
  .filtros{{display:flex;gap:8px;flex-wrap:wrap;margin:20px 2px 4px;align-items:center;justify-content:flex-end;}}
  .filtros .fl-lab{{display:none;}}
  .filtro{{cursor:pointer;border:1px solid var(--linea);background:#fff;border-radius:30px;
    padding:6px 13px;font-size:12.5px;color:var(--gris);display:inline-flex;align-items:center;gap:7px;transition:all .12s ease;}}
  .filtro:hover{{border-color:var(--teal);color:var(--navy);}}
  .filtro.on{{background:var(--navy);border-color:var(--navy);color:#fff;}}
  .dot{{display:inline-block;width:9px;height:9px;border-radius:50%;}}
  .d-alto{{background:var(--imp-alto);}} .d-medio{{background:var(--imp-medio);}} .d-bajo{{background:var(--imp-bajo);}}

  .ptype{{font-size:13px;font-weight:700;letter-spacing:.02em;font-family:Arial,Helvetica,sans-serif;text-transform:none;color:var(--teal);}}
  .impact{{display:inline-flex;align-items:center;gap:6px;font-size:11px;color:var(--suave);letter-spacing:.02em;}}

  /* WORDMARK DE REVISTA (= enlace) — verde turquesa, hover elegante + subrayado */
  .jwrap{{margin-top:14px;display:flex;align-items:center;justify-content:flex-end;gap:8px;flex-wrap:wrap;}}
  .j{{display:inline-flex;align-items:center;justify-content:flex-end;gap:6px;text-decoration:none;
    background:#fff;font-size:13px;line-height:1.1;font-family:Arial,Helvetica,sans-serif;font-weight:700;
    color:var(--teal);letter-spacing:.02em;text-align:right;transition:color .12s ease;}}
  .j:hover{{color:var(--jhover);text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1.5px;}}
  .j .go{{display:none;}}

  /* SECCIONES — acordeón EXCLUSIVO con :target (sin JS): abrir al pulsar + SCROLL a la
     sección + solo una abierta; en iPhone Quick Look funciona igual (anclas + :target). */
  .sec{{margin-top:0;}}
  .sec:first-of-type{{margin-top:18px;}}
  .sec:last-of-type .sec-head{{border-bottom:none;}}
  .sec,.indice{{scroll-margin-top:22px;}}
  .sec-head{{display:flex;align-items:center;gap:14px;padding:21px 4px;border-bottom:1px solid var(--linea);
    cursor:pointer;text-decoration:none;color:inherit;-webkit-tap-highlight-color:rgba(15,154,160,.12);user-select:none;}}
  .sec-num{{flex:0 0 auto;width:30px;height:30px;border-radius:8px;
    display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;letter-spacing:.02em;}}
  .sec-head h2{{margin:0;font-size:17px;color:var(--navy);font-weight:800;letter-spacing:-.01em;}}
  .sec-head .chev{{flex:0 0 auto;margin-left:auto;font-size:30px;line-height:1;position:relative;top:4px;transition:transform .18s ease;}}
  .sec-body{{display:none;}}
  .sec:target .sec-body{{display:block;}}
  .sec:target .chev{{transform:rotate(90deg);}}
  /* Modo filtro (JS): se abren TODAS las secciones con artículos que cumplen el filtro */
  body.filtering .sec-body{{display:block;}}
  body.filtering .sec .chev{{transform:rotate(90deg);}}
  .sec-foot{{padding:12px 0 2px;text-align:right;}}
  body.filtering .sec-foot{{display:none;}}

  article{{padding:20px 0;border-bottom:1px solid var(--linea2);}}
  .sec-body article:last-of-type{{border-bottom:none;}}
  .nonews{{margin:6px 0 2px;padding:14px 16px;font-size:14px;font-style:italic;color:var(--suave);
    background:#f5f7fa;border:1px dashed var(--linea);border-radius:8px;}}
  .card-top{{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:7px;flex-wrap:wrap;}}
  article h4{{margin:0 0 8px;font-size:17px;font-weight:700;line-height:1.34;color:var(--titulo);letter-spacing:-.01em;}}
  .a-body p{{margin:5px 0;font-size:14.5px;color:#37414f;text-align:justify;}}
  .why{{margin-top:8px;padding-left:13px;border-left:2px solid var(--teal);}}
  .why b{{color:var(--teal);}}

  .nota{{margin:32px 0 0;padding-top:16px;border-top:1px solid var(--linea);font-size:9px;color:var(--gris);line-height:1.5;text-align:justify;}}
  footer{{background:var(--navy2);color:#aabccd;padding:26px 40px;font-size:12.5px;}}
  footer .fmark{{font-weight:800;color:#fff;font-size:17px;letter-spacing:-.01em;}}
  footer .fmark .ac{{color:var(--teal);}}
  footer .fsub{{font-size:12px;color:#7e93a6;margin-top:3px;}}
  footer .fbody{{margin-top:10px;line-height:1.55;}}

  @media(max-width:620px){{
    .wrap{{margin:0;border-radius:0;}}
    .mast{{padding:24px 20px 20px;}}
    main{{padding:18px 20px 0;}}
    footer{{padding:22px 20px;}}
    .indice ol{{grid-template-columns:1fr;}}
    .mast-title{{font-size:28px;}}
    .mast-row{{flex-direction:column;}}
    .mast-right{{align-items:flex-start;}}
    .destacado{{padding:16px;}}
    .destacado .d-grid{{grid-template-columns:1fr;gap:14px;}}
    .destacado .d-viz{{max-width:170px;margin:2px auto 0;}}
    .destacado h2{{font-size:18px;}}
    .top3 ol{{padding:4px 16px;}}
    .top3 li{{grid-template-columns:1fr;gap:7px;}}
    .top3 .t3aside{{text-align:left;align-items:flex-start;flex-direction:row;gap:12px;padding-left:36px;}}
    .top3 .j{{text-align:left;}}
    .filtros{{gap:6px;}}
  }}
  @media(max-width:400px){{
    .mast-title{{font-size:24px;}}
    .mast-sub{{font-size:14px;}}
    article h4{{font-size:16px;}}
    .a-body p{{font-size:14px;}}
    .destacado p{{font-size:14px;}}
    .sec-head h2{{font-size:16px;}}
  }}
  .toindex{{font-size:22px;line-height:1;color:var(--teal);text-decoration:none;font-weight:700;white-space:nowrap;display:inline-block;padding:2px 4px;}}
  .toindex:hover{{color:var(--navy);}}
  .toindex:hover{{text-decoration:underline;}}
  .backtop{{position:fixed;bottom:20px;right:20px;z-index:60;width:48px;height:48px;background:var(--navy);color:#fff;
    border-radius:50%;text-decoration:none;font-size:23px;line-height:1;
    box-shadow:0 4px 14px rgba(0,0,0,.28);display:inline-flex;align-items:center;justify-content:center;}}
  .backtop:hover{{background:var(--teal);}}
  @media print{{.backtop{{display:none;}}}}
  .ml{{color:inherit;text-decoration:none;cursor:pointer;}} .ml:hover{{color:var(--teal);}}

  /* POP-UPS (checkbox-hack, sin JS, sin scroll) */
  .cmodal{{position:fixed;top:0;left:0;right:0;bottom:0;z-index:300;display:none;align-items:center;justify-content:center;padding:24px 18px;}}
  .mcb{{position:absolute;width:1px;height:1px;opacity:0;pointer-events:none;}}
  .mcb:checked + .cmodal{{display:flex;}}
  .cmodal-bg{{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(16,21,31,.55);cursor:pointer;}}
  .cmodal-box{{position:relative;z-index:1;background:#fff;max-width:700px;width:100%;max-height:88vh;overflow-y:auto;-webkit-overflow-scrolling:touch;border-radius:14px;padding:26px 30px 30px;box-shadow:0 18px 50px rgba(0,0,0,.35);}}
  .cmodal-x{{position:absolute;top:6px;right:16px;font-size:30px;line-height:1;color:var(--suave);text-decoration:none;cursor:pointer;}}
  .cmodal-x:hover{{color:var(--navy);}}
  .modal-type{{font-size:13px;font-weight:700;letter-spacing:.02em;font-family:Arial,Helvetica,sans-serif;text-transform:none;color:var(--teal);margin-bottom:8px;}}
  .modal-title{{margin:0 0 16px;font-size:20px;font-weight:800;color:var(--titulo);line-height:1.3;padding-right:26px;}}
  .modal-body{{font-size:14.5px;color:#37414f;line-height:1.6;text-align:justify;}}
  .modal-body p{{margin:0 0 11px;}} .modal-body b{{color:var(--navy);}}
  .modal-links{{margin-top:18px;display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end;}}
  @media print{{.cmodal{{display:none!important;}}}}

  /* COLORES DE SECCIÓN */
{color_css}
</style>
</head>
<body>
<div class="wrap">

  <div class="mast">
    <div class="mast-row">
      <div class="mast-left">
        <h1 class="mast-title">Briefing <span class="ac">Cardiovascular</span></h1>
        <div class="mast-sub"><b>UICAR</b><span class="md">·</span>Quirónsalud</div>
      </div>
      <div class="mast-right">
        <span class="num">N1</span>
        <span class="periodo">8 al 14 de junio de 2026</span>
      </div>
    </div>
    <div class="mast-rule"></div>
  </div>

  <main>

    <!-- DESTACADO -->
    <div class="destacado">
      <div class="d-top">
        <span class="d-kicker">★ Destacado de la semana</span>
        <span class="ptype">{dest["ptype"]}</span>
      </div>
      <div class="d-grid">
        <div class="d-text">
          <h2><label class="ml" for="cb-a-{DESTACADO_KEY}">{dest["title"]}</label></h2>
          <p>Primera guía conjunta de AHA/ACC/ADA/ASN sobre el continuum CKM (jubila y amplía la guía de obesidad de 2013). Estadificación por estadios, calculadora de riesgo PREVENT y posicionamiento transversal de SGLT2i, agonistas GLP-1 y finerenona en el paciente con obesidad, diabetes tipo 2 o enfermedad renal crónica.</p>
          <p class="why"><b>Por qué importa:</b> sustituye las guías separadas de lípidos, HTA, diabetes y ERC por <b>un único algoritmo de cribado-estratificación-tratamiento</b>. Pasa a ser la hoja de ruta de referencia para la prevención en el paciente cardiometabólico.</p>
          <div class="jwrap"><a class="j" href="{dest_href}" target="_blank">Circulation <span class="go">↗</span></a></div>
        </div>
        <div class="d-viz">
          <svg viewBox="0 0 200 190" xmlns="http://www.w3.org/2000/svg">
            <circle cx="80" cy="74" r="56" fill="#0a3d62" fill-opacity="0.10" stroke="#0a3d62" stroke-width="1.4"/>
            <circle cx="120" cy="74" r="56" fill="#0f9aa0" fill-opacity="0.12" stroke="#0f9aa0" stroke-width="1.4"/>
            <circle cx="100" cy="116" r="56" fill="#7fb6c4" fill-opacity="0.14" stroke="#5b93a6" stroke-width="1.4"/>
            <text x="55" y="54" font-size="10.5" font-weight="700" fill="#0a3d62" text-anchor="middle">Cardio</text>
            <text x="148" y="54" font-size="10.5" font-weight="700" fill="#0f9aa0" text-anchor="middle">Renal</text>
            <text x="100" y="160" font-size="10.5" font-weight="700" fill="#4d7c8c" text-anchor="middle">Metabólico</text>
            <text x="100" y="92" font-size="15" font-weight="800" fill="#0a3d62" text-anchor="middle">CKM</text>
          </svg>
          <div style="text-align:center;font-size:10.5px;color:var(--gris);margin-top:-4px;">Un solo continuum de riesgo</div>
        </div>
      </div>
    </div>

    <!-- TOP 3 -->
    <div class="top3">
      <div class="t3h"><span class="star">★</span><h3>No te los puedes perder</h3></div>
      <ol>
{top3_li}      </ol>
    </div>

    <!-- SECCIONES (índice) -->
    <div class="indice" id="indice">
      <h3>Secciones</h3>
      <ol>
{index_items}      </ol>
    </div>

    <!-- FILTROS -->
    <div class="filtros">
      <span class="fl-lab">Filtrar</span>
      <span class="filtro on" data-f="all">Todos</span>
      <span class="filtro" data-f="alto"><span class="dot d-alto"></span> Imprescindible</span>
      <span class="filtro" data-f="medio"><span class="dot d-medio"></span> Relevante</span>
      <span class="filtro" data-f="bajo"><span class="dot d-bajo"></span> Complementario</span>
    </div>
{sections_html}

  </main>

  <!-- POP-UPS -->
  {modals_html}

  <footer>
    <div class="fmark">Briefing <span class="ac">Cardiovascular</span></div>
    <div class="fsub">UICAR · Quirónsalud · N1</div>
    <div class="fbody">Revisión semanal de la evidencia científica publicada en medicina cardiovascular. Los resúmenes son una síntesis orientativa; recomendamos consultar siempre el artículo original antes de modificar la práctica clínica.</div>
  </footer>

</div>

<a href="#indice" class="backtop" title="Volver a Secciones">↩︎</a>

<script>
  (function(){{
    var body = document.body;
    var btns = document.querySelectorAll('.filtro');
    function setActive(f){{ btns.forEach(function(x){{ x.classList.toggle('on', x.getAttribute('data-f')===f); }}); }}
    function clearFilter(){{
      body.classList.remove('filtering');
      document.querySelectorAll('article[data-impact]').forEach(function(a){{ a.style.display=''; }});
      document.querySelectorAll('section.sec').forEach(function(s){{ s.style.display=''; }});
    }}
    function collapse(){{ if(location.hash !== '#_'){{ location.hash = '_'; }} }}  // colapsa la sección :target SIN scroll (#_ no existe)
    // Filtros por prioridad: muestran los artículos de esa prioridad en TODAS las secciones
    // y ocultan las secciones sin coincidencias.
    btns.forEach(function(b){{
      b.addEventListener('click', function(){{
        var f = b.getAttribute('data-f');
        setActive(f);
        if(f === 'all'){{ clearFilter(); collapse(); return; }}
        body.classList.add('filtering');
        document.querySelectorAll('article[data-impact]').forEach(function(a){{
          a.style.display = (a.getAttribute('data-impact') === f) ? '' : 'none';
        }});
        document.querySelectorAll('section.sec').forEach(function(s){{
          var any = false;
          s.querySelectorAll('article[data-impact]').forEach(function(a){{ if(a.style.display !== 'none') any = true; }});
          s.style.display = any ? '' : 'none';
        }});
      }});
    }});
    // Índice "Secciones": resetea el filtro a "Todos"; el ancla (:target) abre SOLO esa
    // sección y hace scroll hasta ella (también en iPhone Quick Look, sin JS).
    document.querySelectorAll('.indice .ix').forEach(function(a){{
      a.addEventListener('click', function(){{ clearFilter(); setActive('all'); }});
    }});
    // Cabecera de sección (ancla #sN): si ya está abierta y sin filtro → se REPLIEGA en su
    // sitio; si no → resetea a "Todos" y :target la despliega completa + scroll.
    document.querySelectorAll('.sec-head').forEach(function(a){{
      a.addEventListener('click', function(e){{
        if(location.hash === a.getAttribute('href') && !body.classList.contains('filtering')){{
          // Re-pulsar la cabecera de la sección abierta = "Volver a Secciones":
          // se repliega y se vuelve al índice (mismo comportamiento que la flecha).
          e.preventDefault(); clearFilter(); setActive('all'); location.hash = 'indice'; return;
        }}
        clearFilter(); setActive('all');
      }});
    }});
    // "Volver a Secciones" (flecha de pie + botón flotante, href="#indice"): al ir a #indice
    // la sección deja de ser :target (se repliega) + scroll al índice; resetea a "Todos".
    document.querySelectorAll('.toindex, .backtop').forEach(function(a){{
      a.addEventListener('click', function(){{ clearFilter(); setActive('all'); }});
    }});
  }})();
</script>

</body>
</html>
'''

import io, os
# Cada número vive en su subcarpeta: "Briefing Cardiovascular/Briefing Cardiovascular_N<n>/"
OUTDIR = "/Users/dmarzal/Documents/UICAR/Briefing Cardiovascular/Briefing Cardiovascular_N1"
os.makedirs(OUTDIR, exist_ok=True)
with io.open(OUTDIR + "/Briefing Cardiovascular_N1.html","w",encoding="utf-8") as f:
    f.write(HTML)

# sanity counts
nart = sum(len(a) for _,_,a in SECTIONS)
print("Artículos:", nart)
print("Modales:", HTML.count('class="mcb"'))
print("Secciones:", HTML.count('class="sec-head"'))
print("Bytes:", len(HTML.encode("utf-8")))
print("OUT:", OUTDIR)
