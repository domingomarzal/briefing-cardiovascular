#!/usr/bin/env python3
# N17 · Incorporación en el Mac de los originales de EuroIntervention que la nube no pudo leer
# (n17_cobertura_pendiente.json). Abstracts obtenidos con curl + User-Agent de navegador desde
# eurointervention.pcronline.com (05-oct-2026). Idempotente.
#  · Elegibles (con abstract): 00889 SELUTION DeNovo HBR, 00413 Multivessel TALENT, 00460 DanGer Shock.
#  · No elegibles: 01027, 01084, 01050 (editoriales/expert review sin abstract) y 00382, 00326
#    (cartas de investigación: el texto arranca sin abstract).
#  · Atherosclerosis 121916: sin abstract accesible (no indexado en PubMed; ScienceDirect 403).
# Entran en el top 5: a43 (sec 9, 5,25), a44 (sec 9, 4,68), a45 (sec 5, 4,80); salen por
# «fuera del top 5 de su sección» a36 y a37 (sec 9) y a17 (sec 5).
import json, os, re, html, glob
B = os.path.dirname(os.path.abspath(__file__))
SCR = "/private/tmp/claude-501/-Users-dmarzal-Documents-UICAR/2785da19-1e6f-48ba-89d0-590cb91fccb1/scratchpad"

def abstract(eid):
    p = f"{SCR}/{eid}.html"
    if not os.path.exists(p): return ""
    s = open(p, encoding="utf-8", errors="ignore").read()
    i = s.find(">Abstract<")
    if i < 0: return ""
    t = re.sub(r"\s+", " ", html.unescape(re.sub("<[^>]+>", " ", s[i:i + 8000])))
    t = t.split("Sign in to read")[0]
    t = t.split("Approximately 40% to 44%")[0]          # 00889: el cuerpo sigue sin corte
    t = re.sub(r"^>?\s*Abstract\s*", "", t).strip()
    return t

TIT = {
 "eij-d-26-00889": "Percutaneous coronary intervention using sirolimus-eluting balloons in patients at high bleeding risk: the SELUTION DeNovo HBR substudy",
 "eij-d-26-00413": "Standardised versus visual assessment of device success after percutaneous coronary intervention",
 "eij-d-26-00460": "Complexity of coronary artery disease in infarct-related cardiogenic shock and multivessel disease: a substudy of the DanGer Shock trial",
 "eij-d-26-01027": "Drug-coated balloons in high bleeding risk PCI: can we safely drop the scaffold?",
 "eij-d-26-01084": "Cardiogenic shock with multivessel disease: should we leave non-culprit lesions unattended?",
 "eij-d-26-01050": "Beyond the visual estimate: standardising device success after PCI",
 "eij-d-26-00382": "Longitudinal progression of coronary calcium density on serial computed tomography",
 "eij-d-26-00326": "Remodelling of distal coronary vessels in chronic total occlusions",
}
PT = {"eij-d-26-00889": ["Journal Article", "Randomized Controlled Trial"],
      "eij-d-26-00413": ["Journal Article"], "eij-d-26-00460": ["Journal Article"],
      "eij-d-26-01027": ["Editorial"], "eij-d-26-01084": ["Editorial"], "eij-d-26-01050": ["Editorial"],
      "eij-d-26-00382": ["Letter"], "eij-d-26-00326": ["Letter"]}

# 1) EL: registros recuperados por Crossref (los usa gen_audit para el listado completo)
EL = json.load(open(B + "/n17_el.json"))
have = {e.get("doi", "").lower() for e in EL}
for eid, t in TIT.items():
    doi = "10.4244/" + eid
    if doi in have: continue
    ab = abstract(eid) if PT[eid][0] == "Journal Article" else ""
    EL.append(dict(pmid="CR:" + doi, journal="EuroIntervention", title=t, ptypes=PT[eid], abstract=ab,
                   doi=doi, adate="2026/09/28", _rec="crossref"))
doi = "10.1016/j.atherosclerosis.2026.121916"
if doi not in have:
    EL.append(dict(pmid="CR:" + doi, journal="Atherosclerosis",
                   title="Inflammation and Lipoprotein(a) as Predictors of Cardiovascular Events Across Baseline Risk Levels",
                   ptypes=["Journal Article"], abstract="", doi=doi, adate="2026/10/02", _rec="crossref"))
json.dump(EL, open(B + "/n17_el.json", "w"), ensure_ascii=False, indent=1)

# 2) Selección
S = json.load(open(B + "/n17_sel.json"))
S = [o for o in S if o["key"] not in ("a17", "a36", "a37")]
NEW = [
 dict(key="a43", eid="eij-d-26-00889", sec=9, rel=7, cambio=5, evid=5, efecto=4, rep=5, fi=5, acr=""),
 dict(key="a44", eid="eij-d-26-00413", sec=9, rel=6, cambio=4, evid=5, efecto=4, rep=4, fi=5, acr="Multivessel TALENT"),
 dict(key="a45", eid="eij-d-26-00460", sec=5, rel=6, cambio=4, evid=5, efecto=4, rep=5, fi=5, acr=""),
]
keys = {o["key"] for o in S}
for n in NEW:
    if n["key"] in keys: continue
    tot = round(.20*n["rel"] + .25*n["cambio"] + .20*n["evid"] + .15*n["efecto"] + .12*n["rep"] + .08*n["fi"], 2)
    prio = "Imprescindible" if (n["cambio"] >= 8 or tot >= 8) else ("Relevante" if tot >= 5 else "Complementario")
    doi = "10.4244/" + n["eid"]
    S.append(dict(key=n["key"], idx=None, pmid="CR:" + doi, doi=doi, pii="", journal="EuroIntervention",
                  sec=n["sec"], ptype="Análisis secundario de ensayo clínico", acr=n["acr"], rel=n["rel"],
                  cambio=n["cambio"], evid=n["evid"], efecto=n["efecto"], rep=n["rep"], fi=n["fi"], total=tot,
                  prio=prio, oblig=False, noabs=False, alt=None, rec="crossref", title=TIT[n["eid"]],
                  abstract=abstract(n["eid"])))
    print(n["key"], tot, prio)
json.dump(S, open(B + "/n17_sel.json", "w"), ensure_ascii=False, indent=1)

# 3) Acrónimos
A = json.load(open(B + "/n17_acr.json")); A["a44"] = "Multivessel TALENT"
json.dump(A, open(B + "/n17_acr.json", "w"), ensure_ascii=False, indent=1)
print("sel:", len(S), "· EL:", len(EL))
