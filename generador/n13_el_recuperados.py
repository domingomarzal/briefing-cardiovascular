# -*- coding: utf-8 -*-
"""N13 · PASO 0.2.b — añade a n13_el.json los artículos detectados por la auditoría de
cobertura (Crossref) que PubMed no indexó, tanto los INCORPORADOS al número como los
DESCARTADOS, para que la auditoría los muestre con su motivo. Idempotente."""
import json, io
P = "n13_el.json"
e = json.load(io.open(P, encoding="utf-8"))
have = {x.get("doi", "").lower() for x in e}
AD = "2026/09/03"   # dentro de la ventana 31 ago - 6 sep

NUEVOS = [
 # --- INCORPORADOS al número (abstract verificado en la web del editor)
 dict(doi="10.4244/EIJ-D-25-01372", journal="EuroIntervention", ptypes=["Consensus Development Conference"],
      title="Multimodality imaging for pre-, intra-, and postprocedural guidance of left atrial appendage closure: a European Left Atrial Appendage Closure Club (ELAACC) expert consensus statement",
      abstract="Expert consensus statement of the European Left Atrial Appendage Closure Club providing a unified framework for pre-, intra- and postprocedural imaging in left atrial appendage closure."),
 dict(doi="10.4244/EIJ-D-25-01383", journal="EuroIntervention", ptypes=["Randomized Controlled Trial"],
      title="Sex differences in computed tomography-derived fractional flow reserve-guided management of stable coronary artery disease: a subgroup analysis of the TARGET trial",
      abstract="Post hoc subanalysis of the randomised TARGET trial assessing sex-based differences between CT-FFR-guided and standard care in stable coronary artery disease."),
 dict(doi="10.4244/EIJ-D-26-00102", journal="EuroIntervention", ptypes=["Observational Study"],
      title="Reduced-dose direct oral anticoagulant versus antiplatelet strategies after left atrial appendage occlusion",
      abstract="Propensity score-matched TriNetX cohort comparing reduced-dose DOAC with dual and single antiplatelet therapy after left atrial appendage occlusion."),
 # --- DESCARTADOS (constan en la auditoría con su motivo)
 dict(doi="10.1093/ejhf/xuag282", journal="Eur J Heart Fail", ptypes=["Letter"], abstract="",
      title="RSV vaccine for preventing respiratory and cardiovascular hospitalizations in heart failure: a prespecified analysis of the extended DAN-RSV trial"),
 dict(doi="10.1093/eurheartj/ehag711", journal="Eur Heart J", ptypes=["Case Reports"], abstract="",
      title="Novel oblique dynamic chest radiography for retrocardiac pulmonary blood flow imaging in chronic thromboembolic pulmonary hypertension"),
 dict(doi="10.4244/EIJ-D-26-00112", journal="EuroIntervention", ptypes=["Journal Article"], abstract="",
      title="Lower noradrenaline-mediated mean arterial pressure target in patients with acute myocardial infarction-related cardiogenic shock: rationale and design of the NORshock study"),
 dict(doi="10.4244/EIJ-D-26-00883", journal="EuroIntervention", ptypes=["Editorial"], abstract="",
      title="CT-FFR in females: a benefit in search of a mechanism?"),
 dict(doi="10.4244/EIJ-D-26-00863", journal="EuroIntervention", ptypes=["Editorial"], abstract="",
      title="Dual antiplatelet therapy after left atrial appendage closure: time to move on"),
 dict(doi="10.1016/j.atherosclerosis.2026.121897", journal="Atherosclerosis", ptypes=["Journal Article"], abstract="",
      title="Associations Between Vascular Aging and 12 Lipid Composite Indices: A Large Cross-Sectional Study"),
 dict(doi="10.1016/j.atherosclerosis.2026.121899", journal="Atherosclerosis", ptypes=["Journal Article"], abstract="",
      title="IL-21R blockade reduces inflammation and atherosclerosis in LDL receptor deficient mice"),
]
add = 0
for n in NUEVOS:
    if n["doi"].lower() in have: continue
    e.append(dict(pmid="", journal=n["journal"], title=n["title"], ptypes=n["ptypes"],
                  abstract=n["abstract"], doi=n["doi"], pii="", adate=AD,
                  _oblig=False, _noabs=not bool(n["abstract"]), _rec="crossref"))
    add += 1
json.dump(e, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("añadidos:", add, "| total el.json:", len(e))
