#!/usr/bin/env python3
# N24 · PASO 0.2.b en el Mac (23-nov-2026, ejecución supervisora de las 10:00).
# La nube dejó 9 artículos de Crossref sin abstract (n24_cobertura_pendiente.json).
# PubMed seguía sin indexarlos; sciencedirect/jacc.org/atherosclerosis-journal.com devuelven el
# reto de Cloudflare a curl. OpenAlex sí trae el abstract del editor de 2 de ellos:
#   a48 · radial wall strain en lesiones diferidas por fisiología (Atherosclerosis) -> sección 4
#   a49 · estenosis aórtica en hipercolesterolemia familiar, metaanálisis (Atherosclerosis) -> sección 3
# Isquémica tenía 3 y Dislipemia 4, así que entran sin desplazar a nadie.
# Los otros 7 se registran en la auditoría como descartados por «sin resumen» (regla del abstract).
# Idempotente: no duplica si se ejecuta dos veces.
import json, os
B = os.path.dirname(os.path.abspath(__file__))
SC = B + "/n24_cobertura_abs.json"  # abstracts del editor obtenidos de OpenAlex
ABS = json.load(open(SC))
PEND = json.load(open(B + "/n24_cobertura_pendiente.json"))["pendientes"]

EL = json.load(open(B + "/n24_el.json"))
have = {(e.get("doi") or "").lower() for e in EL}
for p in PEND:
    if p["doi"].lower() in have: continue
    ab = ABS.get(p["doi"]) or ""
    EL.append(dict(pmid="", journal=p["journal"], title=p["title"], ptypes=["Journal Article"],
                   abstract=ab, doi=p["doi"], pii=p["pii"], adate="2026/11/19",
                   _rec="recuperado por Crossref (abstract vía OpenAlex, en el Mac)" if ab else
                         "recuperado por Crossref; sin abstract accesible (PubMed no indexado, editor tras Cloudflare)",
                   _oblig=False, _noabs=not ab))
json.dump(EL, open(B + "/n24_el.json", "w"), ensure_ascii=False, indent=1)

T48 = "Prognostic implications of angiography-derived radial wall strain in physiologically deferred non-flow limiting coronary lesions"
T49 = "Aortic Stenosis in Familial Hypercholesterolemia: A Meta-Analysis"
def tot(r, c, e, f, rp, fi): return round(.20*r + .25*c + .20*e + .15*f + .12*rp + .08*fi, 2)
NEW_SEL = [
 dict(key="a48", idx=None, pmid="", doi="10.1016/j.atherosclerosis.2026.121960", pii="S0021915026013262",
      journal="Atherosclerosis", sec=4, ptype="Estudio pronóstico", acr="", rel=6, cambio=3, evid=4, efecto=5, rep=2, fi=4,
      total=tot(6,3,4,5,2,4), prio="Complementario", oblig=False, noabs=False, alt=None,
      rec="recuperado por Crossref; abstract del editor vía OpenAlex", title=T48,
      abstract=ABS["10.1016/j.atherosclerosis.2026.121960"]),
 dict(key="a49", idx=None, pmid="", doi="10.1016/j.atherosclerosis.2026.121966", pii="S0021915026013328",
      journal="Atherosclerosis", sec=3, ptype="Metaanálisis", acr="", rel=6, cambio=3, evid=5, efecto=6, rep=2, fi=4,
      total=tot(6,3,5,6,2,4), prio="Complementario", oblig=False, noabs=False, alt=None,
      rec="recuperado por Crossref; abstract del editor vía OpenAlex", title=T49,
      abstract=ABS["10.1016/j.atherosclerosis.2026.121966"]),
]
SEL = json.load(open(B + "/n24_sel.json"))
keys = {s["key"] for s in SEL}
SEL += [s for s in NEW_SEL if s["key"] not in keys]
json.dump(SEL, open(B + "/n24_sel.json", "w"), ensure_ascii=False, indent=1)

TXT = {
 "a48": dict(
  title_en=T48,
  title_es="Implicaciones pronósticas del strain radial de la pared derivado de la angiografía en lesiones coronarias no limitantes del flujo diferidas por fisiología",
  es=dict(
   resumen="Análisis post hoc, ciego, de un registro unicéntrico con 509 vasos (417 pacientes) en los que se difirió la revascularización tras la evaluación fisiológica. El strain radial de la pared máximo, obtenido de la angiografía convencional, predijo de forma independiente los eventos orientados al vaso (HR ajustado 1,22 por cada 1% de aumento); la FFR y los índices no hiperémicos no discriminaron.",
   why="señala un posible punto ciego de la estrategia de diferir según la fisiología: vasos con FFR o índices no hiperémicos tranquilizadores que, sin embargo, acumulan eventos, y propone una medida obtenida de la angiografía habitual, sin guía de presión ni imagen intracoronaria, para identificarlos. La discriminación aislada es solo moderada (AUC 0,69) y procede de un único centro, así que es una señal para estudiar, no una herramienta para cambiar hoy la decisión de diferir.",
   deque="La revascularización diferida guiada por fisiología está recomendada por las guías, pero puede pasar por alto la vulnerabilidad residual de la placa. Los autores evaluaron el valor pronóstico del strain radial de la pared (RWS) derivado de la angiografía en vasos coronarios diferidos tras la evaluación fisiológica invasiva. Análisis post hoc, ciego, de un registro unicéntrico (NCT07186582) que incluyó vasos en los que se difirió la revascularización. El RWS máximo se obtuvo de la coronariografía estándar, con un RWS alto predefinido como ≥13%. El objetivo primario fue el compuesto orientado al vaso: muerte cardiaca, infarto relacionado con el vaso diana o revascularización del vaso diana por indicación clínica.",
   resultados="509 vasos de 417 pacientes. Seguimiento mediano 3,3 años (RIC 1,8-6,0). Compuesto orientado al vaso: 50 vasos (9,8%). La FFR y los índices de presión no hiperémicos no difirieron entre vasos con y sin eventos; el RWS máximo fue mayor en los vasos con eventos (15,4 ± 3,9% frente a 13,4 ± 2,9%; p < 0,001). Predictor independiente del compuesto: HR ajustado 1,22 por cada 1% de aumento (IC 95% 1,14-1,31; p < 0,001). RWS máximo ≥13%: HR 3,60 (IC 95% 1,96-6,60; p < 0,001). Discriminación moderada (AUC 0,69); añadido a un modelo clínico-fisiológico, el índice C de Harrell pasó de 0,648 a 0,732.",
   conclusiones="El RWS aportó información pronóstica incremental más allá de la fisiología invasiva, pese a una discriminación aislada moderada. Estos hallazgos respaldan seguir evaluando el RWS integrado con variables clínicas y fisiológicas para afinar la estratificación del riesgo y guiar un manejo individualizado."),
  en=dict(
   resumen="A blinded post hoc analysis of a single-centre registry of 509 vessels (417 patients) in which revascularisation was deferred after physiological assessment. Maximum angiography-derived radial wall strain independently predicted vessel-oriented events (adjusted HR 1.22 per 1% increase); FFR and non-hyperaemic indices did not discriminate.",
   why="it points to a possible blind spot of physiology-guided deferral: vessels with reassuring FFR or non-hyperaemic indices that nonetheless accumulate events, and it proposes a measure taken from routine angiography, without a pressure wire or intracoronary imaging, to identify them. Standalone discrimination is only moderate (AUC 0.69) and comes from a single centre, so this is a signal to study, not a tool to change the deferral decision today.",
   deque="Physiology-guided deferral of coronary revascularisation is guideline-recommended but may overlook residual plaque vulnerability. The authors evaluated the prognostic value of angiography-derived radial wall strain (RWS) in coronary vessels deferred after invasive physiological assessment. This blinded post hoc analysis of a single-centre registry (NCT07186582) included vessels in which revascularisation was deferred. Maximum RWS was derived from standard coronary angiography, with high RWS predefined as ≥13%. The primary endpoint was the vessel-oriented composite of cardiac death, target vessel-related myocardial infarction or clinically driven target vessel revascularisation.",
   resultados="509 vessels from 417 patients. Median follow-up 3.3 years (IQR 1.8-6.0). Vessel-oriented composite: 50 vessels (9.8%). FFR and non-hyperaemic pressure ratios did not differ between vessels with and without events; maximum RWS was higher in vessels with events (15.4 ± 3.9% vs 13.4 ± 2.9%; p < 0.001). Independent predictor of the composite: adjusted HR 1.22 per 1% increase (95% CI 1.14-1.31; p < 0.001). Maximum RWS ≥13%: HR 3.60 (95% CI 1.96-6.60; p < 0.001). Moderate discrimination (AUC 0.69); added to a clinical-physiological model, Harrell's C-index rose from 0.648 to 0.732.",
   conclusiones="RWS provided incremental prognostic information beyond invasive physiology despite moderate standalone discrimination. These findings support further evaluation of RWS integrated with clinical and physiological variables to refine risk stratification and guide individualised management.")),
 "a49": dict(
  title_en=T49,
  title_es="Estenosis aórtica en la hipercolesterolemia familiar: metaanálisis",
  es=dict(
   resumen="Revisión sistemática con metaanálisis de 53 estudios sobre la prevalencia de estenosis aórtica y la incidencia de sustitución valvular aórtica en la hipercolesterolemia familiar. En cohortes de edad media ≤75 años, la estenosis aórtica afectó al 32,7% en la forma homocigota y al 3,4% en la heterocigota, frente al 0,9% de la población general.",
   why="cuantifica por primera vez de forma agregada un fenotipo que suele quedar fuera del foco de la hipercolesterolemia familiar: la valvulopatía aórtica. El gradiente es claro y escalonado (homocigota > heterocigota > población general), también en la tasa de recambio valvular, y aparece a edades relativamente jóvenes. Para el clínico, refuerza vigilar la válvula aórtica en estos pacientes, sobre todo en la forma homocigota, y apoya el argumento de reducir pronto y de forma sostenida la exposición al c-LDL.",
   deque="La hipercolesterolemia familiar (HF) se caracteriza por una exposición de por vida a un c-LDL elevado y por enfermedad cardiovascular aterosclerótica prematura; la forma homocigota se asocia a estenosis aórtica grave que a menudo exige una sustitución valvular compleja. Revisión sistemática (PROSPERO CRD42024611618) para caracterizar la prevalencia de estenosis aórtica y la incidencia de sustitución valvular aórtica en la HF homocigota y heterocigota frente a la población general. Se buscó en MEDLINE, Embase, Cochrane Central, PubMed, Web of Science, Scopus y BIOSIS desde el inicio hasta el 25 de septiembre de 2025.",
   resultados="2024 registros únicos; 53 estudios elegibles. En cohortes con edad media ≤75 años, prevalencia agrupada de estenosis aórtica leve a grave: HF homocigota 32,7% (IC 95% 26,0-40,2%; 18 estudios), HF heterocigota 3,4% (IC 95% 1,5-7,6%; 7 estudios) y población general 0,9% (IC 95% 0,5-1,4%; 7 estudios) (p < 0,0001 para ambas comparaciones). Prevalencia también mayor en la homocigota que en la heterocigota (p < 0,0001). Incidencia de sustitución valvular aórtica: 5,89, 1,56 y 0,18 por 1000 pacientes-año en la homocigota, la heterocigota y la población general, respectivamente.",
   conclusiones="Se observó un aumento marcado y escalonado de la carga de estenosis aórtica entre la HF homocigota, la heterocigota y la población general, con una prevalencia de estenosis y unas tasas de sustitución valvular especialmente altas en la forma homocigota a edades relativamente jóvenes. Estos hallazgos amplían el fenotipo cardiovascular reconocido de la HF más allá de la enfermedad aterosclerótica y subrayan la importancia de un tratamiento hipolipemiante precoz y sostenido para reducir la exposición al c-LDL y mitigar las complicaciones valvulares a largo plazo."),
  en=dict(
   resumen="A systematic review and meta-analysis of 53 studies on aortic stenosis prevalence and aortic valve replacement incidence in familial hypercholesterolaemia. In cohorts with a mean age ≤75 years, aortic stenosis affected 32.7% of homozygous and 3.4% of heterozygous patients, versus 0.9% of the general population.",
   why="it is the first pooled quantification of a phenotype that usually sits outside the focus of familial hypercholesterolaemia: aortic valve disease. The gradient is clear and stepwise (homozygous > heterozygous > general population), also for valve replacement rates, and it appears at relatively young ages. For clinicians, it supports monitoring the aortic valve in these patients, especially in the homozygous form, and strengthens the case for early and sustained LDL-C lowering.",
   deque="Familial hypercholesterolaemia (FH) is characterised by lifelong exposure to elevated LDL-C and premature atherosclerotic cardiovascular disease; the homozygous form is associated with severe aortic stenosis, often requiring complex aortic valve replacement. Systematic review (PROSPERO CRD42024611618) to characterise aortic stenosis prevalence and aortic valve replacement incidence in homozygous and heterozygous FH compared with the general population. MEDLINE, Embase, Cochrane Central, PubMed, Web of Science, Scopus and BIOSIS were searched from inception to 25 September 2025.",
   resultados="2024 unique records; 53 eligible studies. In cohorts with a mean age ≤75 years, pooled prevalence of mild-to-severe aortic stenosis: homozygous FH 32.7% (95% CI 26.0-40.2%; 18 studies), heterozygous FH 3.4% (95% CI 1.5-7.6%; 7 studies) and general population 0.9% (95% CI 0.5-1.4%; 7 studies) (p < 0.0001 for both comparisons). Prevalence also higher in homozygous than heterozygous FH (p < 0.0001). Aortic valve replacement incidence: 5.89, 1.56 and 0.18 per 1,000 patient-years in homozygous FH, heterozygous FH and the general population, respectively.",
   conclusiones="A marked and graded increase in aortic stenosis burden was observed across homozygous FH, heterozygous FH and the general population, with particularly high prevalence of aortic stenosis and valve replacement rates in homozygous FH at relatively young ages. These findings extend the recognised cardiovascular phenotype of FH beyond atherosclerotic disease and highlight the importance of early and sustained lipid-lowering therapy to reduce LDL-C exposure and mitigate long-term valvular complications.")),
}
D4 = json.load(open(B + "/n24_data4.json"))
D4.update({k: v for k, v in TXT.items() if k not in D4})
json.dump(D4, open(B + "/n24_data4.json", "w"), ensure_ascii=False, indent=1)
print("EL", len(EL), "| sel", len(SEL), "| data4", len(D4), "| totales", [s["total"] for s in NEW_SEL])
