#!/usr/bin/env python3
# N19 · Incorporación en el Mac de los originales de EuroIntervention que la nube no pudo leer
# (n19_pendiente_mac.json). Páginas obtenidas con curl + User-Agent de navegador desde
# eurointervention.pcronline.com (19-oct-2026); el tipo sale del rótulo de cabecera de la página.
# Idempotente.
#  · Elegibles (con abstract): 00602 metaanálisis de ECA sobre EC en TAVI · 00454 SPIRARE II
#    (ensayo pivotal de un solo brazo) · 00347 registro de extracción de masas por vacío (TVME).
#  · No elegibles: 01199, 01011, 01104 (Editorial) y 00334 (Research Correspondence = carta).
# Ponderación (rúbrica de 6 ejes):
#  · 00602 → sec 9 (como el subestudio PRO-TAVI a40), 7·6·7·6·5·5 = 6,20 → ENTRA (a49);
#    sale a43 (4,35) por «fuera de las 5 mejores de su sección».
#  · 00454 SPIRARE II 5·4·4·5·4·5 = 4,43 y 00347 TVME 4·3·3·3·3·5 = 3,36 → por debajo del 5.º de
#    la sección 9 (a42, 5,08): fuera del top 5.
import json, os, re, html, sys
B = os.path.dirname(os.path.abspath(__file__))
SCR = sys.argv[1] if len(sys.argv) > 1 else ""

def abstract(eid):
    p = f"{SCR}/{eid.upper()}.html"
    if not SCR or not os.path.exists(p): return ""
    s = open(p, encoding="utf-8", errors="ignore").read()
    i = s.find('abstract">')
    if i < 0: return ""
    t = re.sub(r"\s+", " ", html.unescape(re.sub("<[^>]+>", " ", s[i + 10:i + 9000])))
    t = t.split("Sign in to read")[0]
    t = re.sub(r"^\s*Abstract\s*", "", t).strip()
    t = re.split(r"\(ClinicalTrials\.gov: NCT\d+\)|\(PROSPERO: CRD\d+\)", t)[0].strip()
    return t

TIT = {
 "eij-d-26-00602": "Coronary artery disease management in patients with severe aortic stenosis undergoing transcatheter aortic valve implantation: a systematic review and meta-analysis of randomised controlled trials",
 "eij-d-26-00454": "Safety and effectiveness of the Vertex Pulmonary Embolectomy System in acute intermediate-risk pulmonary embolism: the SPIRARE II pivotal trial",
 "eij-d-26-00347": "Early outcomes of transcatheter vacuum-assisted mass extraction in the left heart and the aortic arch",
 "eij-d-26-01199": "Coronary revascularisation in patients undergoing transcatheter aortic valve implantation: from anatomy to physiology guidance?",
 "eij-d-26-01011": "Prolonged inflation instead of a double tap: pursuing the optimal deployment strategy for the SAPIEN 3 Ultra RESILIA",
 "eij-d-26-01104": "Reproducible haemodynamics, unresolved indication: where does thrombectomy for acute pulmonary embolism stand?",
 "eij-d-26-00334": "Life expectancy after aortic valve replacement: a nationwide analysis",
}
PT = {"eij-d-26-00602": ["Journal Article", "Meta-Analysis"],
      "eij-d-26-00454": ["Journal Article"],
      "eij-d-26-00347": ["Journal Article", "Multicenter Study"],
      "eij-d-26-01199": ["Editorial"], "eij-d-26-01011": ["Editorial"], "eij-d-26-01104": ["Editorial"],
      "eij-d-26-00334": ["Letter"]}

# 0) Que no estén ya publicados en números anteriores
import glob
prev = set()
for f in glob.glob(B + "/n*_data.json"):
    if os.path.basename(f).startswith("n19"): continue
    try: d = json.load(open(f))
    except Exception: continue
    for v in (d.values() if isinstance(d, dict) else d):
        if isinstance(v, dict) and v.get("doi"): prev.add(v["doi"].lower())
dup = [e for e in TIT if ("10.4244/" + e) in prev]
if dup: raise SystemExit("Ya publicados antes: " + ", ".join(dup))

# 1) EL: registros recuperados por Crossref (los usa gen_audit para el listado completo)
EL = json.load(open(B + "/n19_el.json"))
have = {(e.get("doi") or "").lower() for e in EL}
for eid, t in TIT.items():
    doi = "10.4244/" + eid
    if doi in have: continue
    ab = abstract(eid) if PT[eid][0] == "Journal Article" else ""
    if PT[eid][0] == "Journal Article" and not ab: raise SystemExit("Sin abstract: " + eid)
    EL.append(dict(pmid="CR:" + doi, journal="EuroIntervention", title=t, ptypes=PT[eid], abstract=ab,
                   doi=doi, pii="", adate="2026/10/12", _oblig=False, _noabs=False,
                   _rec="recuperado en el Mac por auditoría de cobertura (Crossref + web del editor): PubMed no lo indexaba"))
json.dump(EL, open(B + "/n19_el.json", "w"), ensure_ascii=False, indent=1)

# 2) Selección: sale a43, entra a49
S = json.load(open(B + "/n19_sel.json"))
S = [o for o in S if o["key"] != "a43"]
n = dict(key="a49", eid="eij-d-26-00602", sec=9, rel=7, cambio=6, evid=7, efecto=6, rep=5, fi=5)
if not any(o["key"] == "a49" for o in S):
    tot = round(.20*n["rel"] + .25*n["cambio"] + .20*n["evid"] + .15*n["efecto"] + .12*n["rep"] + .08*n["fi"], 2)
    prio = "Imprescindible" if (n["cambio"] >= 8 or tot >= 8) else ("Relevante" if tot >= 5 else "Complementario")
    doi = "10.4244/" + n["eid"]
    S.append(dict(key="a49", idx=None, pmid="CR:" + doi, doi=doi, pii="", journal="EuroIntervention",
                  sec=9, ptype="Metaanálisis", acr="", rel=n["rel"], cambio=n["cambio"], evid=n["evid"],
                  efecto=n["efecto"], rep=n["rep"], fi=n["fi"], total=tot, prio=prio, oblig=False,
                  noabs=False, alt=None, rec="crossref", title=TIT[n["eid"]], abstract=abstract(n["eid"])))
    print("a49", tot, prio)
json.dump(S, open(B + "/n19_sel.json", "w"), ensure_ascii=False, indent=1)
print("sel:", len(S), "· EL:", len(EL))
