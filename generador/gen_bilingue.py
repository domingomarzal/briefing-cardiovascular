# -*- coding: utf-8 -*-
import json, io, os, html
from urllib.parse import quote

DATA = json.load(open("/tmp/n2_data.json")) if os.path.exists("/tmp/n2_data.json") else {}
NUM = "Nº 2"
PERIOD = ("15 al 21 de junio de 2026", "June 15–21, 2026")
DESTACADO_KEY = "a017"
TOP3 = ["a004", "a009", "a023"]
_ACR_N2 = {"a017":" (PARTNER 2A)","a018":" (PARTNER 2 · SAPIEN 3)","a009":" (MAPLE-HCM)","a130":" (SPYRAL HTN-ON MED)","a022":" (SAFEHEART)","a015":" (VRONI)","a052":" (PRIME-MR)","a045":" (SINGLE SHOT CHAMPION)","a085":" (ROMIAE)","a093":" (DAN-RSV)","a116":" (ISACS-TC)","a050":" (OCEAN-Mitral)","a121":" (CRCS-K-NIH)","a109":" (FOURIER-OLE)","a019":" (PREVUE-VALVE)","a035":" (PULSTA)","a136":" (SUPPRESS-AF)","a028":" (CAMERA-MRI)"}

_ACR = _ACR_N2
SECES = {1:"Cardiología preventiva",2:"Cardiometabolismo",3:"Dislipemia",4:"Cardiopatía isquémica",5:"Insuficiencia cardíaca",6:"Miocardiopatías",7:"Valvulopatías",8:"Imagen cardíaca",9:"Cardiología intervencionista",10:"Arritmias y electrofisiología"}
SECEN = {1:"Preventive cardiology",2:"Cardiometabolic",3:"Lipids",4:"Ischemic heart disease",5:"Heart failure",6:"Cardiomyopathies",7:"Valvular heart disease",8:"Cardiac imaging",9:"Interventional cardiology",10:"Arrhythmias and electrophysiology"}
PTEN = {"Ensayo clínico aleatorizado":"Randomized controlled trial","Análisis secundario de ensayo clínico":"Secondary analysis of a clinical trial","Metaanálisis":"Meta-analysis","Revisión sistemática":"Systematic review","Artículo de revisión":"Review article","Guía de práctica clínica":"Clinical practice guideline","Scientific Statement":"Scientific Statement","Documento de consenso":"Consensus document","Estudio de cohorte":"Cohort study","Registro":"Registry","Estudio de casos y controles":"Case-control study","Estudio observacional":"Observational study","Emulación de ensayo diana":"Target trial emulation","Estudio diagnóstico":"Diagnostic study","Estudio pronóstico":"Prognostic study","Inteligencia artificial / modelo predictivo":"Artificial intelligence / predictive model","Investigación original":"Original research","Evaluación económica":"Economic evaluation"}
SECTION_COLORS = {1:"#0fa6ae",2:"#e08e0b",3:"#5aa82f",4:"#e0443c",5:"#2f7fe6",6:"#8b54d6",7:"#11a87d",8:"#e2670c",9:"#d43d8c",10:"#4b57c9"}
IMP = {"Imprescindible":"alto","Relevante":"medio","Complementario":"bajo"}
DISC = ("Revisión e interpretación semanal de la evidencia científica publicada más relevante en medicina cardiovascular. Los artículos originales deben consultarse en el contexto de las guías de práctica clínica vigentes antes de modificar la práctica asistencial.",
        "Weekly review and interpretation of the most relevant published evidence in cardiovascular medicine. Original articles should be consulted in the context of current clinical practice guidelines before changing clinical practice.")

def ae(s): return html.escape(s or "", quote=True)
def he(s): return html.escape(s or "", quote=False)
def T(es, en, cls=""):
    c = (" "+cls) if cls else ""
    return '<span class="i18n%s" data-es="%s" data-en="%s">%s</span>' % (c, ae(es), ae(en), he(es))

def jlink(doi, title, key=None):
    # LINKFIX: destino alternativo para los artículos cuyo DOI NO aterriza en el artículo.
    # Caso conocido (N7): doi.org -> linkinghub.elsevier.com -> raíz de jacc.org "Page Not Found"
    # en algunos artículos de la familia JACC. Se sustituye por su página de PubMed, que
    # siempre resuelve y ofrece el enlace al editor. El mapa lo genera check_links.py.
    if key and key in LINKFIX:
        return LINKFIX[key]
    return ("https://doi.org/"+doi) if doi else ("https://pubmed.ncbi.nlm.nih.gov/?term="+quote(title))

def titles(a):
    en = a["title_en"].rstrip(); en = en[:-1].rstrip() if en.endswith(".") else en
    es = a["title_es"].rstrip(); es = es[:-1].rstrip() if es.endswith(".") else es
    ac = _ACR.get(a["key"], "")
    if ac and ac.strip(" ()") not in en: en += ac
    if ac and ac.strip(" ()") not in es: es += ac
    return es, en

VARIANTS = {
 "briefing": dict(
   fname="index", title_html='Briefing <span class="ac">Cardiovascular</span>',
   foot_html='Briefing <span class="ac">Cardiovascular</span>',
   root="--headbg:linear-gradient(135deg,#0a3d62 0%,#072b46 100%);--titleac:#0f9aa0;--top3bg:#0a3d62;--top3star:#0f9aa0;--numborder:#0f9aa0;--numtext:#bdeaeb;--periodoc:#aac3d1;",
   title_lang="es"),  # briefing: en ESP los títulos van en ESPAÑOL (regla del usuario, 31/08/2026)
 "ciencia": dict(
   fname="cardio-al-dia", title_html='Cardio al d<span class="ac iabig">IA</span>',
   foot_html='Cardio al d<span class="ac">IA</span>',
   root="--headbg:linear-gradient(135deg,#0a3d62 0%,#072b46 100%);--titleac:#0f9aa0;--top3bg:#0a3d62;--top3star:#0f9aa0;--numborder:#0f9aa0;--numtext:#bdeaeb;--periodoc:#aac3d1;",
   title_lang="es"),  # ciencia: ES mode = Spanish titles
}

# ---- build per-article presentation ----
BY = {}; ALL = {}; VIZ = ""; LINKFIX = {}
def setup(cfg):
    global DATA, NUM, PERIOD, DESTACADO_KEY, TOP3, _ACR, VIZ, BY, ALL, LINKFIX
    DATA = json.load(open(cfg["data"])); NUM = cfg["num"]; PERIOD = cfg["period"]
    DESTACADO_KEY = cfg["dest"]; TOP3 = cfg["top3"]; _ACR = cfg["acr"]; VIZ = cfg["viz"]
    LINKFIX = cfg.get("linkfix", {})
    BY = {}
    for k, a in DATA.items():
        es, en = titles(a); a["_t_es"], a["_t_en"] = es, en
        BY.setdefault(a["sec"], []).append(a)
    for s in BY: BY[s].sort(key=lambda x:-x["total"])
    ALL = {k:a for k,a in DATA.items()}

CSS = """
*{box-sizing:border-box;} html{scroll-behavior:smooth;}
body{margin:0;background:#eceff4;color:#16202e;font-family:"Segoe UI",-apple-system,BlinkMacSystemFont,Roboto,Helvetica,Arial,sans-serif;line-height:1.55;font-size:16px;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
:root{--ink:#16202e;--gris:#5d6878;--suave:#8c97a6;--linea:#e7ebf1;--linea2:#eef1f6;--papel:#fff;--navy:#0a3d62;--teal:#0f9aa0;--teal-soft:#f2f9f9;--titulo:#103a47;--jhover:#0a3d62;--imp-alto:#b23b46;--imp-medio:#c08416;--imp-bajo:#3a8a63;}
.wrap{max-width:1040px;margin:24px auto;background:var(--papel);box-shadow:0 4px 22px rgba(16,21,31,.09);border-radius:14px;overflow:hidden;}
.mast{background:var(--headbg);color:#fff;padding:24px 40px 20px;}
.mast-title{margin:0;font-size:36px;font-weight:800;letter-spacing:-.02em;line-height:1;}
.mast-title .ac{color:var(--titleac);} .mast-title .iabig{font-size:inherit;}
.mast-bottom{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-top:20px;}
.lang{display:inline-flex;border:1px solid rgba(255,255,255,.32);border-radius:20px;overflow:hidden;}
.lang button{font-family:inherit;border:none;background:transparent;color:#cdd8e0;font-size:11px;font-weight:700;letter-spacing:.05em;padding:5px 13px;cursor:pointer;}
.lang button.on{background:var(--titleac);color:#fff;}
.mast-meta{display:flex;align-items:center;gap:12px;}
.mast-meta .periodo{font-size:13px;color:var(--periodoc);white-space:nowrap;}
.mast-meta .num{border:1.5px solid var(--numborder);color:var(--numtext);font-weight:700;font-size:13px;padding:4px 15px;border-radius:30px;letter-spacing:.04em;white-space:nowrap;}
.mast-rule{height:1px;background:rgba(255,255,255,.16);margin-top:18px;}
main{padding:24px 40px 0;}
.destacado{margin:0 0 6px;border:1px solid var(--linea);border-left:4px solid var(--titleac);border-radius:10px;background:#fbfdfd;padding:18px 22px;}
.destacado .d-top{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-bottom:4px;}
.destacado .d-kicker{font-size:13px;font-weight:700;font-family:Arial,Helvetica,sans-serif;color:var(--titleac);}
.destacado .d-grid{display:grid;grid-template-columns:minmax(0,1fr) 180px;gap:22px;align-items:center;margin-top:6px;}
.destacado .d-viz{max-width:180px;overflow:hidden;}
.destacado .d-viz svg{width:100%;height:auto;display:block;}
.destacado .d-viz img{max-width:100%;height:auto;display:block;}
.destacado .d-viz-open{display:block;max-width:180px;position:relative;border-radius:8px;transition:box-shadow .15s;cursor:pointer;}
.destacado .d-viz-open:hover{box-shadow:0 0 0 2px var(--titleac);}
.cmodal-viz{max-width:600px;text-align:center;}
.cmodal-viz .d-viz{max-width:100%;overflow:visible;margin:6px auto 0;}
.cmodal-viz .d-viz svg{width:100%;height:auto;display:block;}
.d-viz-cap{margin:12px 4px 0;font-size:12.5px;color:var(--suave);text-align:center;}
.destacado h2{margin:4px 0 8px;font-size:20px;line-height:1.25;color:var(--titulo);font-weight:800;text-align:justify;}
.destacado p{margin:6px 0;font-size:14.5px;text-align:justify;}
.top3{margin:26px 0 4px;border:1px solid var(--linea);border-radius:12px;overflow:hidden;}
.top3 .t3h{display:flex;align-items:center;gap:8px;padding:11px 18px;background:var(--top3bg);color:#fff;}
.top3 .t3h .star{color:var(--top3star);font-size:15px;}
.top3 .t3h h3{margin:0;font-size:14px;font-weight:800;}
.top3 ol{margin:0;padding:4px 22px;list-style:none;}
.top3 li{display:grid;grid-template-columns:1fr 180px;gap:22px;align-items:start;padding:13px 0;border-bottom:1px solid var(--linea2);}
.top3 li:last-child{border-bottom:none;}
.top3 .t3main{display:flex;gap:13px;align-items:flex-start;min-width:0;}
.top3 .rk{flex:0 0 auto;width:23px;height:23px;border-radius:50%;background:var(--teal-soft);color:var(--teal);font-weight:800;font-size:13px;display:flex;align-items:center;justify-content:center;margin-top:2px;}
.top3 .t3t{font-size:16px;font-weight:700;color:var(--titulo);text-decoration:none;line-height:1.32;text-align:justify;display:block;cursor:pointer;}
.top3 .t3t:hover{color:var(--titleac);}
.top3 .t3aside{text-align:right;display:flex;flex-direction:column;align-items:flex-end;gap:5px;padding-top:2px;}
.top3 .t3s{font-size:13px;font-weight:700;font-family:Arial,Helvetica,sans-serif;color:var(--suave);}
.indice{margin:24px 0 4px;border:1px solid var(--linea);border-radius:10px;padding:6px;}
.indice h3{margin:6px 12px 8px;font-size:13px;font-weight:700;font-family:Arial,Helvetica,sans-serif;color:var(--suave);}
.indice ol{margin:0;padding:0;list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:1px;}
.indice li .ix{display:flex;justify-content:flex-start;align-items:center;gap:8px;cursor:pointer;text-decoration:none;color:var(--ink);font-size:14.5px;padding:8px 16px;border-radius:7px;}
.indice li .ix:hover{background:#f5f7fa;}
.indice .nn{font-weight:800;font-size:12px;margin-right:11px;display:inline-flex;align-items:center;justify-content:center;width:25px;height:19px;border-radius:5px;}
.filtros{display:flex;gap:8px;flex-wrap:wrap;margin:20px 2px 4px;align-items:center;justify-content:flex-end;}
.filtro{cursor:pointer;border:1px solid var(--linea);background:#fff;border-radius:30px;padding:6px 13px;font-size:12.5px;color:var(--gris);display:inline-flex;align-items:center;gap:7px;}
.filtro:hover{border-color:var(--titleac);color:var(--navy);}
.filtro.on{background:var(--navy);border-color:var(--navy);color:#fff;}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;}
.d-alto{background:var(--imp-alto);} .d-medio{background:var(--imp-medio);} .d-bajo{background:var(--imp-bajo);}
.ptype{font-size:13px;font-weight:700;font-family:Arial,Helvetica,sans-serif;color:var(--teal);}
.jwrap{margin-top:14px;display:flex;align-items:center;justify-content:flex-end;gap:8px;flex-wrap:wrap;}
.j{display:inline-flex;align-items:center;gap:6px;text-decoration:none;font-size:13px;font-family:Arial,Helvetica,sans-serif;font-weight:700;color:var(--teal);text-align:right;}
.j:hover{color:var(--jhover);text-decoration:underline;text-underline-offset:3px;}
.sec{margin-top:0;} .sec:first-of-type{margin-top:18px;} .sec:last-of-type .sec-head{border-bottom:none;}
.sec,.indice{scroll-margin-top:22px;}
.sec-head{display:flex;align-items:center;gap:14px;padding:21px 4px;border-bottom:1px solid var(--linea);cursor:pointer;text-decoration:none;color:inherit;user-select:none;}
.sec-num{flex:0 0 auto;width:30px;height:30px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;}
.sec-head h2{margin:0;font-size:17px;color:var(--navy);font-weight:800;}
.sec-head .chev{flex:0 0 auto;margin-left:auto;font-size:30px;line-height:1;position:relative;top:-2px;transition:transform .18s ease;}
.sec-body{display:none;} .sec:target .sec-body{display:block;} .sec:target .chev{transform:rotate(90deg);}
body.filtering .sec-body{display:block;} body.filtering .sec .chev{transform:rotate(90deg);}
.sec-foot{padding:12px 0 2px;text-align:right;} body.filtering .sec-foot{display:none;}
article{padding:20px 0;border-bottom:1px solid var(--linea2);} .sec-body article:last-of-type{border-bottom:none;}
.nonews{margin:6px 0 2px;padding:14px 16px;font-size:14px;font-style:italic;color:var(--suave);background:#f5f7fa;border:1px dashed var(--linea);border-radius:8px;}
.card-top{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:7px;flex-wrap:wrap;}
article h4{margin:0 0 8px;font-size:17px;font-weight:700;line-height:1.34;color:var(--titulo);text-align:justify;}
.a-body p{margin:5px 0;font-size:14.5px;color:#37414f;text-align:justify;}
.why{margin-top:8px;padding-left:13px;border-left:2px solid var(--titleac);} .why b{color:var(--titleac);}
footer{background:#eef3f6;color:#5d6878;padding:22px 40px;border-top:3px solid var(--titleac);font-size:12.5px;}
footer .ftable{width:100%;border-collapse:collapse;}
footer .fleft{vertical-align:middle;padding-right:40px;} footer .fright{vertical-align:middle;text-align:right;border-left:1px solid #d4dde3;padding-left:40px;width:1%;white-space:nowrap;}
footer .fmark{font-weight:800;color:var(--navy);font-size:17px;} footer .fmark .ac{color:var(--titleac);}
footer .fbody{margin-top:8px;line-height:1.5;font-size:10.5px;color:#5d6878;text-align:justify;}
footer .fsign{width:auto;max-height:68px;height:auto;display:inline-block;}
.toindex{font-size:22px;color:var(--titleac);text-decoration:none;font-weight:700;}
.backtop{position:fixed;bottom:20px;right:20px;z-index:60;width:48px;height:48px;background:var(--navy);color:#fff;border-radius:50%;text-decoration:none;font-size:23px;display:inline-flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(0,0,0,.28);}
.backtop:hover{background:var(--titleac);}
.ml{color:inherit;text-decoration:none;cursor:pointer;} .ml:hover{color:var(--titleac);}
.cmodal{position:fixed;top:0;left:0;right:0;bottom:0;z-index:300;display:none;align-items:center;justify-content:center;padding:24px 18px;}
.mcb{position:absolute;width:1px;height:1px;opacity:0;pointer-events:none;}
.mcb:checked + .cmodal{display:flex;}
.cmodal-bg{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(16,21,31,.55);cursor:pointer;}
.cmodal-box{position:relative;z-index:1;background:#fff;max-width:700px;width:100%;max-height:88vh;overflow-y:auto;border-radius:14px;padding:26px 30px 30px;box-shadow:0 18px 50px rgba(0,0,0,.35);}
.cmodal-x{position:absolute;top:6px;right:16px;font-size:30px;color:var(--suave);text-decoration:none;cursor:pointer;}
.modal-body ul.mnov{margin:4px 0 14px;padding-left:22px;}
/* ---- Audio (Web Speech API): mejora progresiva, el texto sigue estando sin JS ---- */
.abtn{display:none;align-items:center;justify-content:center;width:30px;height:30px;flex:0 0 30px;border:none;background:transparent;padding:0;border-radius:50%;cursor:pointer;color:var(--teal);transition:background .15s;}
body.has-audio .abtn{display:inline-flex;}
.abtn:hover{background:color-mix(in srgb, currentColor 13%, transparent);}
.abtn:focus-visible{outline:2px solid currentColor;outline-offset:1px;}
.abtn svg{display:block;pointer-events:none;}
/* REPRODUCIENDO = la onda se mueve · PAUSA = dos barras quietas */
.abtn .ic-p{display:none;}
.abtn.paused .ic-w{display:none;} .abtn.paused .ic-p{display:block;}
.abtn .wv line{stroke:currentColor;stroke-width:1.9;stroke-linecap:round;transform-origin:12px 12px;}
@keyframes wvb{0%,100%{transform:scaleY(.42)}50%{transform:scaleY(1.12)}}
.abtn.live .wv line{animation:wvb .85s ease-in-out infinite;}
.abtn.live .wv line:nth-of-type(1){animation-delay:0s}
.abtn.live .wv line:nth-of-type(2){animation-delay:.13s}
.abtn.live .wv line:nth-of-type(3){animation-delay:.26s}
.abtn.live .wv line:nth-of-type(4){animation-delay:.39s}
.abtn.live .wv line:nth-of-type(5){animation-delay:.52s}
@media (prefers-reduced-motion:reduce){.abtn.live .wv line{animation:none;}}
/* en la cabecera, sobre fondo navy */
.mast .abtn{color:#bdeaeb;border:1px solid rgba(255,255,255,.32);}
.sec-head-row{display:flex;align-items:center;}
.sec-head-row .sec-head{flex-grow:1;min-width:0;}
.sec-head-row .abtn{margin:0 4px 0 8px;}
.chevlink{display:inline-flex;align-items:center;text-decoration:none;padding:0 2px;}
.langwrap{display:flex;align-items:center;gap:8px;}
.cmodal-head{display:flex;align-items:center;gap:10px;margin-bottom:2px;}
.cmodal-head .modal-type{flex-grow:1;min-width:0;}
.cmodal-head .cmodal-x{position:static;font-size:26px;line-height:1;}
.cmodal-box{padding-top:20px;}
.mast .abtn:hover{background:rgba(255,255,255,.14);}
/* dentro del pop-up, a la izquierda de la X */

/* barra de audio flotante mientras suena */
.abar{position:fixed;left:50%;transform:translateX(-50%);bottom:18px;z-index:400;display:none;align-items:center;gap:12px;background:var(--navy);color:#fff;border-radius:30px;padding:9px 10px 9px 18px;box-shadow:0 8px 26px rgba(10,61,98,.34);max-width:min(560px,92vw);}
body.audio-live .abar{display:flex;}
.abar .txt{font-size:12.5px;line-height:1.35;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.abar button{border:none;background:rgba(255,255,255,.16);color:#fff;width:30px;height:30px;flex:0 0 30px;border-radius:50%;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;padding:0;}
.abar button:hover{background:rgba(255,255,255,.28);}
@media print{.abtn,.abar{display:none!important;}}

.modal-body ul.mnov li{margin:6px 0;text-align:justify;}
.modal-type{font-size:13px;font-weight:700;font-family:Arial,Helvetica,sans-serif;color:var(--teal);margin-bottom:8px;}
.modal-title{margin:0 0 16px;font-size:20px;font-weight:800;color:var(--titulo);line-height:1.3;text-align:justify;}
.modal-body{font-size:14.5px;color:#37414f;line-height:1.6;text-align:justify;}
.modal-body p{margin:0 0 11px;} .modal-body b{color:var(--navy);}
.modal-links{margin-top:18px;display:flex;gap:8px;justify-content:flex-end;}
@media(max-width:620px){.wrap{margin:0;border-radius:0;}.mast{padding:22px 18px 18px;}main{padding:18px 18px 0;}footer{padding:22px 18px;}.indice ol{grid-template-columns:1fr;}.mast-title{font-size:27px;}.destacado .d-grid{grid-template-columns:1fr;gap:14px;}.top3 li{grid-template-columns:1fr;gap:7px;}.top3 .t3aside{text-align:left;align-items:flex-start;flex-direction:row;gap:12px;}.fleft,.fright{display:block;width:100%;border-left:0;padding:0;}.fright{margin-top:16px;border-top:1px solid #d4dde3;padding-top:16px;text-align:left;}}
@media print{.backtop,.filtros,.lang{display:none;}.sec-body{display:block!important;}.chev{display:none;}.cmodal{display:none!important;}}
"""

def colorcss():
    return "\n".join(".c%d{background:%s;color:#fff;} .indice .nn.c%d{background:transparent;color:%s;} .chev.t%d{color:%s;}"%(n,c,n,c,n,c) for n,c in SECTION_COLORS.items())

def jl(a, t3=False):
    href = jlink(a["doi"], a["title_en"], a["key"]); cls = "j t3j" if t3 else "j"
    return '<a class="%s" href="%s" target="_blank">%s</a>' % (cls, href, he(a["journal"]))

def ptype_span(a):
    return T(a["ptype"], PTEN.get(a["ptype"], a["ptype"]), "ptype")

def abtn(kind, ref="", color="", extra=""):
    """Botón de audio (icono de onda de sonido). kind: art | sec | all.
    color: color CSS a heredar (el de la sección cuando procede)."""
    sty = (' style="color:%s"' % color) if color else ""
    lab = {"art": "Escuchar este artículo", "sec": "Escuchar esta sección",
           "all": "Escuchar el briefing"}[kind]
    return ('<button class="abtn" type="button" data-a="%s" data-ref="%s" aria-label="%s"%s%s>'
            '<svg class="ic-w wv" width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
            '<line x1="4.5" y1="10" x2="4.5" y2="14"/><line x1="8.2" y1="7.4" x2="8.2" y2="16.6"/>'
            '<line x1="12" y1="5" x2="12" y2="19"/><line x1="15.8" y1="7.4" x2="15.8" y2="16.6"/>'
            '<line x1="19.5" y1="10" x2="19.5" y2="14"/></svg>'
            '<svg class="ic-p" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.9" stroke-linecap="round" aria-hidden="true">'
            '<line x1="9" y1="7" x2="9" y2="17"/><line x1="15" y1="7" x2="15" y2="17"/></svg>'
            '</button>') % (kind, ref, lab, sty, extra)

def modal(a):
    es, en = a["_t_es"], a["_t_en"]; cid = "cb-a-"+a["key"]
    e, n = a["es"], a["en"]
    # Las guías/consensos/statements no tienen "Resultados" ni "Conclusiones": llevan
    # "Novedades" (recomendaciones nuevas o modificadas) y "Qué cambia en la práctica".
    if a["ptype"] in ("Guía de práctica clínica", "Documento de consenso", "Scientific Statement"):
        l2 = T("Novedades.", "What’s new.")
        l3 = T("Qué cambia en la práctica.", "What changes in practice.")
    else:
        l2 = T("Resultados.", "Results.")
        l3 = T("Conclusiones.", "Conclusions.")
    def blk(label, kes, ken):
        # Si el contenido es una LISTA, se pinta como viñetas (cada <li> con su propio span i18n)
        # para que las novedades de las guías se lean de un vistazo. Si es texto, párrafo normal.
        if isinstance(kes, list):
            lis = "".join("<li>%s</li>" % T(a, b) for a, b in zip(kes, ken))
            return "<p><b>%s</b></p><ul class=\"mnov\">%s</ul>" % (label, lis)
        return "<p><b>%s</b> %s</p>" % (label, T(kes, ken))
    body = (blk(T("De qué va.","What it’s about."), e.get("deque",""), n.get("deque",""))
          + blk(l2, e.get("resultados",""), n.get("resultados",""))
          + blk(l3, e.get("conclusiones",""), n.get("conclusiones","")))
    mt = '<h3 class="modal-title" data-es="%s" data-en="%s">%s</h3>' % (ae(es if VAR["title_lang"]=="es" else en), ae(en), he(es if VAR["title_lang"]=="es" else en))
    return ('<input type="checkbox" id="%s" class="mcb"><div class="cmodal"><label class="cmodal-bg" for="%s"></label>'
            '<div class="cmodal-box"><div class="cmodal-head"><div class="modal-type">%s</div>' + abtn("art", a["key"], SECTION_COLORS[a["sec"]]) + '<label class="cmodal-x" for="%s" aria-label="Cerrar">&times;</label></div>'
            '%s<div class="modal-body">%s</div>'
            '<div class="modal-links">%s</div></div></div>') % (cid, cid, ptype_span(a), cid, mt, body, jl(a))

def article(a):
    imp = IMP[a["prio"]]; es, en = a["_t_es"], a["_t_en"]
    dt = es if VAR["title_lang"]=="es" else en
    title = '<label class="ml" for="cb-a-%s" data-es="%s" data-en="%s">%s</label>' % (a["key"], ae(es if VAR["title_lang"]=="es" else en), ae(en), he(dt))
    return ('<article id="a-%s" data-impact="%s"><div class="card-top">%s<span class="impact"><span class="dot d-%s"></span></span></div>'
            '<h4>%s</h4><div class="a-body"><p>%s</p><p class="why"><b>%s</b> %s</p><div class="jwrap">%s</div></div></article>') % (
            a["key"], imp, ptype_span(a), imp, title,
            T(a["es"].get("resumen",""), a["en"].get("resumen","")),
            T("Por qué importa:","Why it matters:"), T(a["es"].get("why",""), a["en"].get("why","")), jl(a))

PRIO_RANK = {"alto":0,"medio":1,"bajo":2}
def _grp(a): return 0 if a["key"]==DESTACADO_KEY else (1 if a["key"] in TOP3 else 2)

def build(variant):
    global VAR; VAR = VARIANTS[variant]
    sections=[]
    for s in range(1,11):
        sections.append((s, BY.get(s, [])))
    # index
    idx = ""
    for s,arts in sections:
        idx += '<li><a class="ix" href="#s%d"><span><span class="nn c%d">%02d</span>%s</span></a></li>\n' % (s,s,s,T(SECES[s],SECEN[s]))
    # top3
    t3 = ""
    for i,k in enumerate(TOP3,1):
        a=ALL[k]; es,en=a["_t_es"],a["_t_en"]; dt = es if VAR["title_lang"]=="es" else en
        t3 += ('<li><div class="t3main"><span class="rk">%d</span><label class="t3t" for="cb-a-%s" data-es="%s" data-en="%s">%s</label></div>'
               '<div class="t3aside">%s%s</div></li>\n') % (i,k, ae(es if VAR["title_lang"]=="es" else en), ae(en), he(dt), jl(a,True), '<span class="t3s">%s</span>'%T(SECES[a["sec"]],SECEN[a["sec"]]))
    # sections
    AB_SEC = {s: abtn("sec", str(s), SECTION_COLORS[s]) for s in range(1,11)}
    secs=""
    for s,arts in sections:
        if not arts:
            ah = '<p class="nonews">%s</p>' % T("Sin novedades relevantes esta semana.","No relevant updates this week.")
        else:
            ordered=sorted(arts, key=lambda a:(PRIO_RANK[IMP[a["prio"]]], _grp(a), -a["total"]))
            ah="\n".join(article(a) for a in ordered)
        secs += ('<section class="sec" id="s%d"><div class="sec-head-row"><a class="sec-head" href="#s%d"><span class="sec-num c%d">%02d</span><h2>%s</h2></a>' + AB_SEC[s] + '<a class="chevlink" href="#s%d" aria-label="Desplegar"><span class="chev t%d">▸</span></a></div>'
                 '<div class="sec-body">%s<div class="sec-foot"><a href="#indice" class="toindex" aria-label="Secciones">↩︎</a></div></div></section>\n') % (s,s,s,s,T(SECES[s],SECEN[s]),s,s,ah)
    modals="\n".join(modal(a) for _,arts in sections for a in arts)
    # Figura del Destacado ampliable como pop-up (mismo checkbox-hack sin JS que las fichas;
    # funciona en Quick Look del iPhone). El cambio de idioma actúa sobre TODOS los [data-es],
    # así que la copia grande del modal también traduce sola.
    if VIZ.strip():
        viz_open = '<label class="d-viz-open" for="cb-viz" aria-label="Ampliar figura">%s</label>' % VIZ
        viz_modal = ('<input type="checkbox" id="cb-viz" class="mcb"><div class="cmodal">'
                     '<label class="cmodal-bg" for="cb-viz"></label>'
                     '<div class="cmodal-box cmodal-viz"><label class="cmodal-x" for="cb-viz" aria-label="Cerrar">&times;</label>'
                     '<div class="d-viz-big">%s</div>'
                     '<p class="d-viz-cap" data-es="%s" data-en="%s">%s</p></div></div>') % (
                     VIZ, ae("Figura del Destacado de la semana"), ae("Highlight of the week — figure"),
                     he("Figura del Destacado de la semana"))
        modals = modals + viz_modal
    else:
        viz_open = VIZ
    dest=ALL[DESTACADO_KEY]; de,den=dest["_t_es"],dest["_t_en"]; ddt = de if VAR["title_lang"]=="es" else den
    svg = ('<svg viewBox="0 0 200 190" xmlns="http://www.w3.org/2000/svg">'
      '<text x="100" y="16" font-size="11" font-weight="700" fill="#5d6878" text-anchor="middle" data-es="Mortalidad a 10 años" data-en="10-year mortality">Mortalidad a 10 años</text>'
      '<rect x="40" y="34" width="48" height="96" rx="3" fill="#0a3d62" fill-opacity="0.12" stroke="#0a3d62" stroke-width="1.4"/><rect x="40" y="40" width="48" height="90" fill="#0a3d62" fill-opacity="0.85"/>'
      '<rect x="112" y="34" width="48" height="96" rx="3" fill="#0f9aa0" fill-opacity="0.12" stroke="#0f9aa0" stroke-width="1.4"/><rect x="112" y="44" width="48" height="86" fill="#0f9aa0" fill-opacity="0.85"/>'
      '<text x="64" y="120" font-size="14" font-weight="800" fill="#fff" text-anchor="middle">86%</text><text x="136" y="120" font-size="14" font-weight="800" fill="#fff" text-anchor="middle">83%</text>'
      '<text x="64" y="148" font-size="11" font-weight="700" fill="#0a3d62" text-anchor="middle">TAVR</text><text x="136" y="148" font-size="11" font-weight="700" fill="#0f9aa0" text-anchor="middle" data-es="Cirugía" data-en="Surgery">Cirugía</text>'
      '<text x="100" y="172" font-size="9.5" fill="#8c97a6" text-anchor="middle">HR 1,13 (1,02-1,25)</text></svg>')
    destacado = ('<div class="destacado"><div class="d-top"><span class="d-kicker">%s</span>%s</div>'
      '<div class="d-grid"><div class="d-text"><h2><label class="ml" for="cb-a-%s" data-es="%s" data-en="%s">%s</label></h2>'
      '<p>%s</p><p class="why"><b>%s</b> %s</p><div class="jwrap">%s</div></div>'
      '%s</div></div>') % (
      T("★ Destacado de la semana","★ Highlight of the week"), ptype_span(dest), DESTACADO_KEY,
      ae(de if VAR["title_lang"]=="es" else den), ae(den), he(ddt),
      T(dest["es"].get("resumen",""), dest["en"].get("resumen","")),
      T("Por qué importa:","Why it matters:"), T(dest["es"].get("why",""), dest["en"].get("why","")), jl(dest), viz_open)

    # Datos para el motor de audio: qué leer y en qué orden
    _sec_keys = {s: [a["key"] for a in sorted(BY.get(s, []), key=lambda x: -x["total"])] for s in range(1, 11)}
    AUDIO_DATA = ('<script>window.BRIEF_AUDIO=' + json.dumps({
        "dest": DESTACADO_KEY, "top3": list(TOP3), "secs": _sec_keys,
        "names": {"es": SECES, "en": SECEN},
        "i18n": {
          "es": {"dest": "Vamos a comenzar con la publicación destacada de la semana.",
                 "top3": "Continuamos con las publicaciones que no te puedes perder.",
                 "sec": "Continuamos con la sección de %s.",
                 "secOnly": "Sección de %s.",
                 "end": "Fin del briefing.", "lang": "es-ES", "voz": "Voz"},
          "en": {"dest": "Let us begin with the highlight of the week.",
                 "top3": "Next, the articles you should not miss.",
                 "sec": "Now the section on %s.",
                 "secOnly": "Section: %s.",
                 "end": "End of the briefing.", "lang": "en-GB", "voz": "Voice"}}
    }, ensure_ascii=False) + ';</script>')
    root = ":root{"+VAR["root"]+"}"
    HTML = ('<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
      '<title>%s</title><style>%s\n%s\n%s</style></head><body><div class="wrap">'
      '<div class="mast"><h1 class="mast-title">%s</h1><div class="mast-bottom">'
      '<div class="langwrap"><div class="lang"><button data-l="es" class="on">ESP</button><button data-l="en">ENG</button></div>' + abtn("all") + '</div>' +
      '<div class="mast-meta"><span class="periodo" data-es="%s" data-en="%s">%s</span><span class="num">%s</span></div>'
      '</div><div class="mast-rule"></div></div><main>%s'
      '<div class="top3"><div class="t3h"><span class="star">★</span><h3>%s</h3></div><ol>%s</ol></div>'
      '<div class="indice" id="indice"><h3>%s</h3><ol>%s</ol></div>'
      '<div class="filtros"><span class="filtro on" data-f="all">%s</span><span class="filtro" data-f="alto"><span class="dot d-alto"></span> %s</span>'
      '<span class="filtro" data-f="medio"><span class="dot d-medio"></span> %s</span><span class="filtro" data-f="bajo"><span class="dot d-bajo"></span> %s</span></div>'
      '%s</main>%s'
      '<footer><table class="ftable"><tr><td class="fleft"><div class="fmark">%s</div>'
      '<div class="fbody" data-es="%s" data-en="%s">%s</div></td>'
      '<td class="fright"><img class="fsign" src="data:image/png;base64,%s" alt="Domingo Marzal"></td></tr></table></footer>'
      '</div><a href="#indice" class="backtop" aria-label="Secciones">↩︎</a>'
      '<div class="abar" role="status"><span class="txt"></span>'
      '<button data-ab="pp" aria-label="Pausar o reanudar"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="9" y1="7" x2="9" y2="17"/><line x1="15" y1="7" x2="15" y2="17"/></svg></button>'
      '<button data-ab="st" aria-label="Detener"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg></button></div>'
      '%s</body></html>') % (
        ("Cardio al día" if variant=="ciencia" else "Briefing Cardiovascular"), CSS, colorcss(), root,
        VAR["title_html"], ae(PERIOD[0]), ae(PERIOD[1]), he(PERIOD[0]), NUM,
        destacado, T("No te los puedes perder","Don’t miss these"), t3,
        T("Secciones","Sections"), idx,
        T("Todos","All"), T("Imprescindible","Essential"), T("Relevante","Relevant"), T("Complementario","Complementary"),
        secs, modals, VAR["foot_html"], ae(DISC[0]), ae(DISC[1]), he(DISC[0]), LOGO_B64, AUDIO_DATA + SCRIPT)
    return HTML

LOGO_B64 = __import__("base64").b64encode(open("/Users/dmarzal/Documents/Claude/Briefing Cardiovascular/briefing-cardiovascular-repo/generador/firma_DM_horizontal.png","rb").read()).decode()

SCRIPT = """<script>
(function(){
 function setLang(l){
  document.querySelectorAll('[data-es]').forEach(function(e){var v=e.getAttribute('data-'+l); if(v!==null) e.textContent=v;});
  document.documentElement.setAttribute('lang', l==='en'?'en':'es');
  document.querySelectorAll('.lang button').forEach(function(b){b.classList.toggle('on', b.getAttribute('data-l')===l);});
 }
 document.querySelectorAll('.lang button').forEach(function(b){b.addEventListener('click',function(){setLang(b.getAttribute('data-l'));});});
 var body=document.body, btns=document.querySelectorAll('.filtro');
 function setActive(f){btns.forEach(function(x){x.classList.toggle('on',x.getAttribute('data-f')===f);});}
 function clearFilter(){body.classList.remove('filtering');document.querySelectorAll('article[data-impact]').forEach(function(a){a.style.display='';});document.querySelectorAll('section.sec').forEach(function(s){s.style.display='';});}
 function collapse(){if(location.hash!=='#_')location.hash='_';}
 btns.forEach(function(b){b.addEventListener('click',function(){var f=b.getAttribute('data-f');setActive(f);if(f==='all'){clearFilter();collapse();return;}body.classList.add('filtering');document.querySelectorAll('article[data-impact]').forEach(function(a){a.style.display=(a.getAttribute('data-impact')===f)?'':'none';});document.querySelectorAll('section.sec').forEach(function(s){var any=false;s.querySelectorAll('article[data-impact]').forEach(function(a){if(a.style.display!=='none')any=true;});s.style.display=any?'':'none';});});});
 document.querySelectorAll('.indice .ix').forEach(function(a){a.addEventListener('click',function(){clearFilter();setActive('all');});});
 document.querySelectorAll('.sec-head').forEach(function(a){a.addEventListener('click',function(e){if(location.hash===a.getAttribute('href')&&!body.classList.contains('filtering')){e.preventDefault();clearFilter();setActive('all');location.hash='indice';return;}clearFilter();setActive('all');});});
 document.querySelectorAll('.toindex, .backtop').forEach(function(a){a.addEventListener('click',function(){clearFilter();setActive('all');});});

 /* ================= AUDIO (Web Speech API) — mejora progresiva ================= */
 (function(){
  var SS = window.speechSynthesis, D = window.BRIEF_AUDIO;
  if (!SS || !D || typeof SpeechSynthesisUtterance === 'undefined') return;
  document.body.classList.add('has-audio');

  var Q = [], qi = 0, mode = null, ref = null, st = 'idle', btn = null, voz = null;

  function lang(){ return document.documentElement.getAttribute('lang') === 'en' ? 'en' : 'es'; }
  function T(k){ return D.i18n[lang()][k]; }
  function clean(s){ return (s||'').replace(/\s+/g,' ').replace(/ /g,' ').trim(); }

  /* --- voces: elige la mejor del idioma y recuerda la preferida --- */
  function voces(){
    var L = lang() === 'en' ? 'en' : 'es';
    return (SS.getVoices()||[]).filter(function(v){ return (v.lang||'').toLowerCase().indexOf(L) === 0; });
  }
  function mejorVoz(){
    var vs = voces(); if (!vs.length) return null;
    var pref = null;
    try { pref = localStorage.getItem('brief-voz-' + lang()); } catch(e){}
    if (pref){ for (var i=0;i<vs.length;i++) if (vs[i].name === pref) return vs[i]; }
    var exact = lang()==='en' ? 'en-gb' : 'es-es';
    var score = function(v){
      var n=(v.name||'').toLowerCase(), s=0;
      if ((v.lang||'').toLowerCase() === exact) s += 4;
      if (/premium|enhanced|neural|siri/.test(n)) s += 3;
      if (v.localService) s += 1;
      return s;
    };
    return vs.slice().sort(function(a,b){ return score(b)-score(a); })[0];
  }
  function decir(txt){
    var u = new SpeechSynthesisUtterance(txt);
    u.lang = T('lang'); u.rate = 1; u.pitch = 1;
    var v = voz || mejorVoz(); if (v) u.voice = v;
    return u;
  }

  /* --- de dónde sale el texto: título + cuerpo del pop-up del artículo --- */
  function ficha(k){
    var cb = document.getElementById('cb-a-' + k); if (!cb) return null;
    var box = cb.nextElementSibling && cb.nextElementSibling.querySelector('.cmodal-box');
    if (!box) return null;
    var ti = clean(box.querySelector('.modal-title') && box.querySelector('.modal-title').textContent);
    var bo = clean(box.querySelector('.modal-body') && box.querySelector('.modal-body').textContent);
    if (!ti && !bo) return null;
    return ti + '. ' + bo;
  }
  function nombreSec(s){ return D.names[lang()][s] || ('' + s); }

  /* --- construcción de la cola --- */
  function cola(m, r){
    var out = [], dicho = {};
    function push(txt, et){ if (txt) out.push({ t: txt, e: et }); }
    if (m === 'all'){
      push(T('dest'), '★');
      var d = ficha(D.dest); if (d){ push(d, '★'); dicho[D.dest] = 1; }
      push(T('top3'), '★');
      D.top3.forEach(function(k){ var f = ficha(k); if (f){ push(f, '★'); dicho[k] = 1; } });
      for (var s = 1; s <= 10; s++){
        var ks = (D.secs[s] || []).filter(function(k){ return !dicho[k]; });
        if (!ks.length) continue;                       /* ya sonó entera arriba */
        push(T('sec').replace('%s', nombreSec(s)), nombreSec(s));
        ks.forEach(function(k){ var f = ficha(k); if (f) push(f, nombreSec(s)); });
      }
      push(T('end'), '');
    } else if (m === 'sec'){
      var n = parseInt(r, 10);
      push(T('secOnly').replace('%s', nombreSec(n)), nombreSec(n));
      (D.secs[n] || []).forEach(function(k){ var f = ficha(k); if (f) push(f, nombreSec(n)); });
    } else {
      var f2 = ficha(r); if (f2) push(f2, '');
    }
    return out;
  }

  /* --- reproducción --- */
  var bar = document.querySelector('.abar'), barTxt = bar && bar.querySelector('.txt');
  /* la voz se puede cambiar en cualquier momento en que la barra esté visible */
  function pinta(){
    document.querySelectorAll('.abtn').forEach(function(b){ b.classList.remove('on','live','paused'); });
    document.body.classList.toggle('audio-live', st !== 'idle');
    if (btn && st !== 'idle'){
      btn.classList.add('on');
      btn.classList.add(st === 'playing' ? 'live' : 'paused');
    }
    if (barTxt && Q[qi]) barTxt.textContent = (Q[qi].e ? Q[qi].e + ' · ' : '') + Q[qi].t.slice(0, 90);
  }
  function siguiente(){
    if (qi >= Q.length){ parar(); return; }
    var u = decir(Q[qi].t);
    u.onend = function(){ if (st === 'playing'){ qi++; pinta(); siguiente(); } };
    u.onerror = function(){ if (st === 'playing'){ qi++; siguiente(); } };
    SS.speak(u); pinta();
  }
  function arranca(m, r, b){
    SS.cancel(); Q = cola(m, r); qi = 0; mode = m; ref = r; btn = b; st = 'playing';
    if (!Q.length){ parar(); return; }
    siguiente();
  }
  function parar(){ SS.cancel(); st = 'idle'; Q = []; qi = 0; btn = null; pinta(); }
  function pausa(){ if (st === 'playing'){ SS.pause(); st = 'paused'; } else if (st === 'paused'){ SS.resume(); st = 'playing'; } pinta(); }

  document.addEventListener('click', function(ev){
    var b = ev.target.closest && ev.target.closest('.abtn');
    if (b){
      ev.preventDefault(); ev.stopPropagation();
      var m = b.getAttribute('data-a'), r = b.getAttribute('data-ref');
      if (btn === b && st !== 'idle') pausa();      /* mismo botón: pausa / reanuda */
      else arranca(m === 'all' ? 'all' : (m === 'sec' ? 'sec' : 'art'), r, b);
      return;
    }
    var ab = ev.target.closest && ev.target.closest('.abar button');
    if (ab){ ev.preventDefault(); (ab.getAttribute('data-ab') === 'pp') ? pausa() : parar(); }
  }, true);

  /* al cambiar de idioma o cerrar el pop-up, se detiene: el texto ya no es el mismo */
  document.querySelectorAll('.lang button').forEach(function(x){
    x.addEventListener('click', function(){ voz = null; parar(); setTimeout(montaVoces, 60); });
  });
  window.addEventListener('beforeunload', function(){ SS.cancel(); });
  if (SS.onvoiceschanged !== undefined) SS.onvoiceschanged = function(){};

  /* selector de voz: aparece en la barra si el sistema ofrece más de una */
  function montaVoces(){
    if (!bar) return;
    var viejo = bar.querySelector('select');
    var vs = voces();
    if (vs.length < 2){ if (viejo) viejo.remove(); return; }
    /* se RECONSTRUYE siempre: al cambiar de idioma y cuando el sistema añade voces nuevas */
    if (viejo) viejo.remove();
    var sel = document.createElement('select');
    sel.setAttribute('aria-label', T('voz'));
    sel.style.cssText = 'background:rgba(255,255,255,.16);color:#fff;border:none;border-radius:15px;font:inherit;font-size:11.5px;padding:5px 8px;max-width:130px;cursor:pointer';
    vs.forEach(function(v){ var o = document.createElement('option'); o.value = v.name; o.textContent = v.name; o.style.color = '#16202e'; sel.appendChild(o); });
    var actual = mejorVoz(); if (actual) sel.value = actual.name;
    sel.addEventListener('change', function(){
      voz = vs.filter(function(v){ return v.name === sel.value; })[0] || null;
      try { localStorage.setItem('brief-voz-' + lang(), sel.value); } catch(e){}
      if (st !== 'idle'){ SS.cancel(); st = 'playing'; siguiente(); }   /* re-lee con la voz nueva */
    });
    bar.insertBefore(sel, bar.querySelector('button'));
  }
  setTimeout(montaVoces, 400);
  setTimeout(montaVoces, 1500);          /* getVoices() se puebla en diferido en Safari */
  if (SS.addEventListener) SS.addEventListener('voiceschanged', montaVoces);
  else SS.onvoiceschanged = montaVoces;
 })();

})();
</script>"""

BASE = "/Users/dmarzal/Documents/Claude/Briefing Cardiovascular/briefing-cardiovascular-repo"
LOCALBASE = "/Users/dmarzal/Documents/Claude/Briefing Cardiovascular"
def _acr(p): return json.load(open(p)) if os.path.exists(p) else {}
def _viz(p): return io.open(p, encoding="utf-8").read() if os.path.exists(p) else ""
CONFIGS = [
 dict(n="n0", data=BASE+"/generador/n0_data.json", num="Nº 0", period=("3 al 10 de junio de 2026","June 3–10, 2026"), dest="m021", top3=["m101","m060","m151"], acr=_acr(BASE+"/generador/n0_acr.json"), viz=_viz(BASE+"/generador/n0_viz.html"), local="Briefing Cardiovascular_N0", lnum="N0"),
 dict(n="n1", data=BASE+"/generador/n1_data.json", num="Nº 1", period=("8 al 14 de junio de 2026","June 8–14, 2026"), dest="e002", top3=["e061","e004","x2"], acr=_acr(BASE+"/generador/n1_acr.json"), viz=_viz(BASE+"/generador/n1_viz.html"), local="Briefing Cardiovascular_N1", lnum="N1"),
 dict(n="n2", data=BASE+"/generador/n2_data.json", num="Nº 2", period=("15 al 21 de junio de 2026","June 15–21, 2026"), dest="a017", top3=["a004","a009","a023"], acr=_ACR_N2, viz="", local="Briefing Cardiovascular_N2", lnum="N2"),
 dict(n="n3", data=BASE+"/generador/n3_data.json", num="Nº 3", period=("22 al 28 de junio de 2026","June 22–28, 2026"), dest="hel", top3=["avg","a110","a18"], acr=_acr(BASE+"/generador/n3_acr.json"), viz=_viz(BASE+"/generador/n3_viz.html"), local="Briefing Cardiovascular_N3", lnum="N3"),
 dict(n="n4", data=BASE+"/generador/n4_data.json", num="Nº 4", period=("29 de junio al 5 de julio de 2026","June 29 – July 5, 2026"), dest="a1", top3=["a2","a3","a4"], acr=_acr(BASE+"/generador/n4_acr.json"), viz=_viz(BASE+"/generador/n4_viz.html"), local="Briefing Cardiovascular_N4", lnum="N4"),
 dict(n="n5", data=BASE+"/generador/n5_data.json", num="Nº 5", period=("6 al 12 de julio de 2026","July 6–12, 2026"), dest="a1", top3=["a2","a3","a4"], acr=_acr(BASE+"/generador/n5_acr.json"), viz=_viz(BASE+"/generador/n5_viz.html"), local="Briefing Cardiovascular_N5", lnum="N5"),
 dict(n="n6", data=BASE+"/generador/n6_data.json", num="Nº 6", period=("13 al 19 de julio de 2026","July 13–19, 2026"), dest="a14", top3=["a39","a6","a24"], acr=_acr(BASE+"/generador/n6_acr.json"), viz=_viz(BASE+"/generador/n6_viz.html"), local="Briefing Cardiovascular_N6", lnum="N6"),
 dict(n="n7", linkfix=_acr(BASE+"/generador/n7_linkfix.json"), data=BASE+"/generador/n7_data.json", num="Nº 7", period=("20 al 26 de julio de 2026","July 20–26, 2026"), dest="a51", top3=["a11","a46","a6"], acr=_acr(BASE+"/generador/n7_acr.json"), viz=_viz(BASE+"/generador/n7_viz.html"), local="Briefing Cardiovascular_N7", lnum="N7"),
 dict(n="n8", linkfix=_acr(BASE+"/generador/n8_linkfix.json"), data=BASE+"/generador/n8_data.json", num="Nº 8", period=("27 de julio al 2 de agosto de 2026","July 27 – August 2, 2026"), dest="a6", top3=["a20","a45","a11"], acr=_acr(BASE+"/generador/n8_acr.json"), viz=_viz(BASE+"/generador/n8_viz.html"), local="Briefing Cardiovascular_N8", lnum="N8"),
 dict(n="n9", linkfix=_acr(BASE+"/generador/n9_linkfix.json"), data=BASE+"/generador/n9_data.json", num="Nº 9", period=("3 al 9 de agosto de 2026","August 3–9, 2026"), dest="a43", top3=["a6","a18","a44"], acr=_acr(BASE+"/generador/n9_acr.json"), viz=_viz(BASE+"/generador/n9_viz.html"), local="Briefing Cardiovascular_N9", lnum="N9"),
 dict(n="n10", linkfix=_acr(BASE+"/generador/n10_linkfix.json"), data=BASE+"/generador/n10_data.json", num="Nº 10", period=("10 al 16 de agosto de 2026","August 10–16, 2026"), dest="a6", top3=["a39","a16","a24"], acr=_acr(BASE+"/generador/n10_acr.json"), viz=_viz(BASE+"/generador/n10_viz.html"), local="Briefing Cardiovascular_N10", lnum="N10"),
 dict(n="n11", linkfix=_acr(BASE+"/generador/n11_linkfix.json"), data=BASE+"/generador/n11_data.json", num="Nº 11", period=("17 al 23 de agosto de 2026","August 17–23, 2026"), dest="a41", top3=["a6","a42","a46"], acr=_acr(BASE+"/generador/n11_acr.json"), viz=_viz(BASE+"/generador/n11_viz.html"), local="Briefing Cardiovascular_N11", lnum="N11"),
 dict(n="n12", linkfix=_acr(BASE+"/generador/n12_linkfix.json"), data=BASE+"/generador/n12_data.json", num="Nº 12", period=("24 al 30 de agosto de 2026","August 24–30, 2026"), dest="a21", top3=["a6","a1","a16"], acr=_acr(BASE+"/generador/n12_acr.json"), viz=_viz(BASE+"/generador/n12_viz.html"), local="Briefing Cardiovascular_N12", lnum="N12"),
]
import sys as _sys
ONLY = _sys.argv[1] if len(_sys.argv) > 1 else None
for cfg in CONFIGS:
    if ONLY and cfg["n"] != ONLY: continue
    setup(cfg)
    os.makedirs(BASE+"/"+cfg["n"], exist_ok=True)
    os.makedirs(LOCALBASE+"/"+cfg["local"], exist_ok=True)
    for variant in ("briefing","ciencia"):
        h = build(variant); fn = VARIANTS[variant]["fname"]
        io.open(BASE+"/"+cfg["n"]+"/"+fn+".html","w",encoding="utf-8").write(h)
        if variant=="briefing":
            io.open(LOCALBASE+"/"+cfg["local"]+"/"+cfg["local"]+".html","w",encoding="utf-8").write(h)
        else:
            io.open(LOCALBASE+"/"+cfg["local"]+"/Cardio al día_"+cfg["lnum"]+".html","w",encoding="utf-8").write(h)
        print(cfg["n"], variant, len(h.encode()), "bytes")
print("OK")
