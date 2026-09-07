# -*- coding: utf-8 -*-
"""N13 · PASO 0.2.b — incorporación de los artículos recuperados por la auditoría de
cobertura (Crossref) que PubMed no había indexado. Ver n13_cobertura.json.
Fuente del contenido: abstract del editor (EuroIntervention). Idempotente."""
import json, io

DATA = "n13_data.json"; SEL = "n13_sel.json"
d = json.load(io.open(DATA, encoding="utf-8"))
s = json.load(io.open(SEL, encoding="utf-8"))

# --- a40 sale: desplazado de las 5 mejores de Cardiología intervencionista por a48 (5,56 > 4,75)
d.pop("a40", None)
s = [o for o in s if o["key"] != "a40"]

NEW = {}

# ============================ a46 · Imagen cardíaca ============================
NEW["a46"] = dict(
 key="a46", sec=8, ptype="Documento de consenso", journal="EuroIntervention",
 doi="10.4244/EIJ-D-25-01372", total=6.48, prio="Relevante",
 title_en="Multimodality imaging for pre-, intra-, and postprocedural guidance of left atrial appendage closure: a European Left Atrial Appendage Closure Club (ELAACC) expert consensus statement",
 title_es="Imagen multimodalidad para la guía pre-, intra- y posprocedimiento del cierre de la orejuela izquierda: documento de consenso de expertos del European Left Atrial Appendage Closure Club (ELAACC)",
 es=dict(
  resumen="Primer documento de consenso europeo que unifica la imagen en todo el recorrido del cierre de la orejuela izquierda. Nace de un problema concreto: la variabilidad entre centros en cómo se adquieren, miden y comunican las imágenes, que genera flujos de trabajo y resultados inconsistentes. Prioriza la imagen tridimensional y la reconstrucción multiplanar, y estandariza terminología, parámetros anatómicos y criterios de seguimiento.",
  why="el cierre de orejuela es un procedimiento cuyo éxito depende casi por completo de la imagen —del dimensionado previo, de la guía en tiempo real y de la vigilancia posterior—, y hasta ahora cada centro lo hacía a su manera. Este consenso pone nombre común a las medidas, fija qué necesita cada dispositivo y armoniza los criterios ecocardiográficos y de TC para valorar trombo sobre dispositivo, fuga peridispositivo y estabilidad. Para el clínico que deriva o sigue a estos pacientes, significa que los informes deberían empezar a decir lo mismo y a medir lo mismo entre hospitales.",
  deque="Documento de consenso de expertos del European Left Atrial Appendage Closure Club (ELAACC) sobre la imagen en el cierre de la orejuela izquierda (LAAC), alternativa establecida para la prevención del ictus en pacientes con fibrilación auricular no valvular que no son candidatos a anticoagulación oral prolongada. Va dirigido a los equipos que indican, realizan y siguen el procedimiento —intervencionistas estructurales, especialistas en imagen y electrofisiólogos— y busca reducir la variabilidad, estandarizar los flujos de trabajo y mejorar la reproducibilidad clínica a lo largo de todo el recorrido: antes, durante y después del procedimiento.",
  resultados=[
   "Se establece un marco unificado de imagen para las tres fases del procedimiento —preprocedimiento, intraprocedimiento y posprocedimiento— en lugar de recomendaciones sueltas por técnica.",
   "Se prioriza de forma explícita la imagen tridimensional y la reconstrucción multiplanar frente a las proyecciones bidimensionales convencionales para la planificación.",
   "Se define una terminología estandarizada y un conjunto nuclear de parámetros anatómicos, de modo que las medidas sean comparables entre centros y entre exploraciones.",
   "Se fijan los requisitos de imagen orientados al dispositivo, para que la planificación y la elección del dispositivo partan de las mismas mediciones.",
   "Se insiste en la calidad de adquisición y en la reproducibilidad de las medidas como condición previa, no como un detalle técnico.",
   "En el intraprocedimiento, la guía en tiempo real se apoya en ecocardiografía transesofágica tridimensional, ecocardiografía intracardiaca e imagen de fusión para la punción transeptal, la alineación del dispositivo, su liberación y la valoración del sellado.",
   "En el posprocedimiento se armonizan los criterios ecocardiográficos y de tomografía computarizada cardiaca, hasta ahora dispares entre ambas técnicas.",
   "Se proponen vías de seguimiento estructuradas para valorar el trombo relacionado con el dispositivo, la fuga peridispositivo y la estabilidad del dispositivo.",
  ],
  conclusiones="Al promover una nomenclatura consistente y estrategias de imagen estructuradas e informadas por la evidencia a lo largo de todo el recorrido del cierre de orejuela, el consenso aspira a mejorar la seguridad del procedimiento, aumentar la reproducibilidad y sostener una práctica uniforme y de alta calidad entre centros."),
 en=dict(
  resumen="First European consensus document unifying imaging across the entire left atrial appendage closure pathway. It addresses a concrete problem: between-centre variability in how images are acquired, measured and reported, which drives inconsistent workflows and outcomes. It prioritises three-dimensional imaging and multiplanar reconstruction, and standardises terminology, anatomical parameters and follow-up criteria.",
  why="left atrial appendage closure is a procedure whose success depends almost entirely on imaging — on pre-procedural sizing, real-time guidance and post-procedural surveillance — and until now each centre did it its own way. This consensus gives measurements a common name, sets out device-specific requirements, and harmonises echocardiographic and CT criteria for assessing device-related thrombus, peridevice leak and device stability. For the clinician referring or following these patients, it means reports should start saying and measuring the same things across hospitals.",
  deque="Expert consensus statement from the European Left Atrial Appendage Closure Club (ELAACC) on imaging in left atrial appendage closure (LAAC), an established alternative for stroke prevention in patients with non-valvular atrial fibrillation who are not suitable candidates for long-term oral anticoagulation. It is aimed at the teams who indicate, perform and follow up the procedure — structural interventionalists, imaging specialists and electrophysiologists — and seeks to reduce variability, standardise workflows and improve clinical reproducibility across the whole pathway: before, during and after the procedure.",
  resultados=[
   "A unified imaging framework is established for all three procedural phases — pre-, intra- and postprocedural — rather than separate recommendations per technique.",
   "Three-dimensional imaging techniques and multiplanar reconstruction are explicitly prioritised over conventional two-dimensional projections for planning.",
   "Standardised terminology and a set of core anatomical parameters are defined, so that measurements are comparable across centres and across studies.",
   "Device-oriented imaging requirements are set out, so that procedural planning and device selection start from the same measurements.",
   "High-quality image acquisition and reproducible measurement are stressed as a precondition, not as a technical detail.",
   "Intraprocedurally, real-time guidance rests on three-dimensional transoesophageal echocardiography, intracardiac echocardiography and fusion imaging for transseptal puncture, device alignment, deployment and sealing assessment.",
   "Postprocedurally, echocardiographic and cardiac computed tomography criteria are harmonised, having so far diverged between the two techniques.",
   "Structured follow-up pathways are proposed for the assessment of device-related thrombus, peridevice leak and device stability.",
  ],
  conclusiones="By promoting consistent nomenclature and structured, evidence-informed imaging strategies across the entire LAAC pathway, the consensus aims to enhance procedural safety, improve reproducibility and support uniform, high-quality LAAC practice across centres."))

# ============================ a47 · Imagen cardíaca ============================
NEW["a47"] = dict(
 key="a47", sec=8, ptype="Análisis secundario de ensayo clínico", journal="EuroIntervention",
 doi="10.4244/EIJ-D-25-01383", total=5.43, prio="Relevante",
 title_en="Sex differences in computed tomography-derived fractional flow reserve-guided management of stable coronary artery disease: a subgroup analysis of the TARGET trial",
 title_es="Diferencias por sexo en el manejo guiado por reserva fraccional de flujo derivada de tomografía computarizada en la enfermedad coronaria estable: análisis de subgrupos del ensayo TARGET",
 es=dict(
  resumen="Subanálisis post hoc del ensayo aleatorizado TARGET (1.216 pacientes con estenosis coronaria del 30-90% en angio-TC) que compara la estrategia guiada por CT-FFR con la atención estándar según el sexo. La guía por CT-FFR redujo las coronariografías sin enfermedad obstructiva y aumentó la revascularización precoz en hombres, pero no en mujeres; a 2 años, en cambio, se asoció a menos eventos en mujeres (HR ajustada 0,48; IC95% 0,27-0,87) y a ninguna diferencia en hombres.",
  why="la enfermedad coronaria de la mujer sigue siendo un punto ciego: presenta menos lesiones obstructivas en la coronariografía y, aun así, peor pronóstico. Este análisis sugiere que el rendimiento de la CT-FFR podría no ser el mismo en uno y otro sexo —evitando cateterismos innecesarios sobre todo en hombres y asociándose a menos eventos sobre todo en mujeres—, pero los propios autores frenan la lectura: no hubo interacción estadísticamente significativa entre sexo y estrategia. Es una señal para diseñar el estudio que lo responda, no para cambiar hoy la indicación.",
  deque="Las mujeres con enfermedad coronaria estable presentan con frecuencia enfermedad menos obstructiva en la coronariografía invasiva y, pese a ello, peores resultados que los hombres. La reserva fraccional de flujo derivada de angio-TC (CT-FFR) mejora la valoración fisiológica de las lesiones coronarias más allá de la angio-TC, pero su impacto clínico según el sexo sigue siendo incierto. En este subanálisis post hoc del ensayo aleatorizado TARGET, 1.216 pacientes con estenosis coronaria del 30-90% en angio-TC se aleatorizaron a manejo guiado por CT-FFR in situ o a atención estándar. El objetivo principal fue la proporción de pacientes que se sometieron a coronariografía invasiva sin enfermedad coronaria obstructiva o que no recibieron intervención pese a tener enfermedad obstructiva en la coronariografía, dentro de los 90 días de la angio-TC. El objetivo secundario fueron los eventos cardiovasculares adversos mayores (MACE) a 2 años.",
  resultados="Las mujeres eran mayores que los hombres (62,3 ± 8,1 frente a 58,2 ± 10,7 años; p < 0,001), pero con una gravedad anatómica de la enfermedad coronaria comparable. El manejo guiado por CT-FFR redujo significativamente la coronariografía sin enfermedad obstructiva y aumentó la revascularización precoz en hombres, pero no en mujeres. A lo largo de 2 años, el manejo guiado por CT-FFR se asoció a una tasa de MACE significativamente menor en mujeres frente a la atención estándar (HR ajustada 0,48; IC95% 0,27-0,87; p = 0,015), mientras que no se observó diferencia significativa en hombres (HR ajustada 0,89; IC95% 0,59-1,33; p = 0,574).",
  conclusiones="El manejo guiado por CT-FFR se asoció a patrones clínicos distintos entre mujeres y hombres. En particular en los hombres, la guía por CT-FFR redujo la coronariografía innecesaria. Entre las mujeres del grupo CT-FFR se observó una menor tasa de eventos adversos a 2 años. No obstante, dada la ausencia de una interacción estadísticamente significativa entre el sexo y la estrategia de tratamiento, estos hallazgos deben considerarse exploratorios y generadores de hipótesis."),
 en=dict(
  resumen="Post hoc subanalysis of the randomised TARGET trial (1,216 patients with 30-90% coronary stenosis on CCTA) comparing a CT-FFR-guided strategy with standard care by sex. CT-FFR guidance reduced invasive angiography without obstructive disease and increased early revascularisation in males but not in females; at 2 years, conversely, it was associated with fewer events in females (adjusted HR 0.48, 95% CI 0.27-0.87) and no difference in males.",
  why="coronary disease in women remains a blind spot: they present with less obstructive disease at angiography and still fare worse. This analysis suggests CT-FFR may not perform identically in both sexes — avoiding unnecessary catheterisation mainly in men, and associating with fewer events mainly in women — but the authors themselves rein the reading in: there was no statistically significant interaction between sex and strategy. It is a signal to design the trial that answers this, not to change indications today.",
  deque="Females with stable coronary artery disease often present with less obstructive disease on invasive coronary angiography yet experience worse outcomes than males. Coronary computed tomography-derived fractional flow reserve (CT-FFR) guidance improves the physiological assessment of coronary lesions beyond coronary computed tomography angiography, but its sex-specific clinical impact remains uncertain. In this post hoc subanalysis of the randomised TARGET trial, 1,216 patients with 30-90% coronary stenosis on CCTA were randomised to onsite CT-FFR-guided care or standard care. The primary endpoint was the proportion of patients who underwent invasive coronary angiography without obstructive CAD or had no intervention despite obstructive CAD on angiography within 90 days of CCTA. The secondary endpoint was major adverse cardiovascular events (MACE) at 2 years.",
  resultados="Females were older than males (62.3 ± 8.1 vs 58.2 ± 10.7 years; p < 0.001) but had comparable anatomical CAD severity. CT-FFR-guided care significantly reduced invasive angiography without obstructive CAD and increased early revascularisation in males but not in females. Over 2 years, CT-FFR-guided management was associated with a significantly lower MACE rate in females compared with standard care (adjusted HR 0.48, 95% CI 0.27-0.87; p = 0.015), whereas no significant difference was observed in males (adjusted HR 0.89, 95% CI 0.59-1.33; p = 0.574).",
  conclusiones="CT-FFR-guided management was associated with different clinical patterns between females and males. Particularly in males, CT-FFR guidance reduced unnecessary angiography. A lower 2-year adverse event rate was observed among females in the CT-FFR group. However, given the absence of a statistically significant interaction between sex and treatment strategy, these findings should be considered exploratory and hypothesis-generating."))

# ====================== a48 · Cardiología intervencionista ======================
NEW["a48"] = dict(
 key="a48", sec=9, ptype="Estudio de cohorte", journal="EuroIntervention",
 doi="10.4244/EIJ-D-26-00102", total=5.56, prio="Relevante",
 title_en="Reduced-dose direct oral anticoagulant versus antiplatelet strategies after left atrial appendage occlusion",
 title_es="Anticoagulante oral directo a dosis reducida frente a estrategias antiagregantes tras la oclusión de la orejuela izquierda",
 es=dict(
  resumen="Cohorte global (red TriNetX) de pacientes con fibrilación auricular sometidos a cierre percutáneo de orejuela entre 2010 y 2025, con tres comparaciones emparejadas por puntuación de propensión. Frente a la doble antiagregación, el anticoagulante oral directo a dosis reducida se asoció a menor mortalidad total (HR 0,79; IC95% 0,65-0,96) y menos sangrado mayor (HR 0,87; IC95% 0,77-0,98), sin ventaja clara sobre la antiagregación simple.",
  why="tras cerrar una orejuela hay que decidir con qué se cubre al paciente, y esa decisión se toma hoy sin ensayos que la respalden. Este trabajo aporta la comparación directa que faltaba entre las tres opciones que se usan en la práctica y encuentra un mensaje doble: la doble antiagregación es la peor parada, y el anticoagulante a dosis reducida no supera a la antiagregación simple —de hecho, frente a ella los datos son compatibles con algo más de sangrado mayor—. Apunta a simplificar el tratamiento tras el implante y a individualizarlo, más que a sustituir una pauta fija por otra.",
  deque="El tratamiento antitrombótico óptimo tras la oclusión de la orejuela izquierda (LAAO) en pacientes con fibrilación auricular sigue sin estar establecido. La anticoagulación oral directa (ACOD) a dosis reducida se utiliza cada vez más en la práctica clínica como alternativa a las estrategias basadas en antiagregantes, pero los datos comparativos de resultados son limitados. El estudio se propuso comparar los resultados clínicos del ACOD a dosis baja frente a la doble antiagregación (DAPT) o la antiagregación simple (SAPT) tras LAAO. Usando la red global TriNetX se identificaron pacientes adultos con fibrilación auricular sometidos a LAAO percutánea entre 2010 y 2025, y se realizaron tres análisis paralelos emparejados por puntuación de propensión: ACOD a dosis reducida frente a DAPT, SAPT frente a DAPT, y ACOD a dosis reducida frente a SAPT. Los resultados incluyeron mortalidad por cualquier causa, eventos tromboembólicos, trombosis relacionada con el dispositivo, eventos hemorrágicos y beneficio clínico neto (NCB).",
  resultados="Tras el emparejamiento se incluyeron 1.773 pacientes en cada grupo para la comparación de ACOD a dosis reducida frente a DAPT (seguimiento medio 1,4 ± 1,0 años). El ACOD a dosis reducida se asoció a menor riesgo de mortalidad por cualquier causa (HR 0,79; IC95% 0,65-0,96) y de sangrado mayor (HR 0,87; IC95% 0,77-0,98), sin diferencias significativas en ictus isquémico, tromboembolismo ni trombosis relacionada con el dispositivo. El beneficio clínico neto favoreció al ACOD a dosis reducida (HR 0,87; IC95% 0,78-0,96). La SAPT también se asoció a menos eventos hemorrágicos y a resultados favorables frente a la DAPT. En la comparación de ACOD a dosis reducida frente a SAPT (1.582 pacientes emparejados por grupo), el ACOD a dosis reducida mostró estimaciones compatibles con un riesgo ligeramente mayor de sangrado mayor frente a la SAPT (HR 1,14; IC95% 1,00-1,30; p = 0,06), mientras que la mortalidad, los resultados tromboembólicos y el beneficio clínico neto no difirieron significativamente.",
  conclusiones="En la práctica contemporánea tras la oclusión de la orejuela izquierda, el tratamiento con anticoagulante oral directo a dosis reducida se asoció a resultados más favorables que la doble antiagregación, pero no mostró una ventaja clara sobre la antiagregación simple, lo que apoya estrategias antitrombóticas posimplante simplificadas e individualizadas."),
 en=dict(
  resumen="Global cohort (TriNetX network) of patients with atrial fibrillation undergoing percutaneous left atrial appendage occlusion between 2010 and 2025, with three propensity score-matched comparisons. Versus dual antiplatelet therapy, reduced-dose direct oral anticoagulation was associated with lower all-cause mortality (HR 0.79, 95% CI 0.65-0.96) and less major bleeding (HR 0.87, 95% CI 0.77-0.98), with no clear advantage over single antiplatelet therapy.",
  why="after closing an appendage, someone must decide what to cover the patient with, and that decision is currently made without trials to support it. This work provides the missing head-to-head comparison between the three options used in practice, with a twofold message: dual antiplatelet therapy comes off worst, and reduced-dose anticoagulation does not beat single antiplatelet therapy — indeed, against it the data are compatible with slightly more major bleeding. It points towards simplifying and individualising post-implantation therapy rather than swapping one fixed regimen for another.",
  deque="The optimal antithrombotic therapy after left atrial appendage occlusion (LAAO) in patients with atrial fibrillation (AF) remains uncertain. Reduced-dose direct oral anticoagulation (DOAC) is increasingly used in clinical practice as an alternative to antiplatelet-based strategies, but comparative outcome data are limited. The study sought to compare clinical outcomes associated with low-dose DOAC therapy versus dual antiplatelet therapy (DAPT) or single antiplatelet therapy (SAPT) after LAAO. Using the TriNetX Global Network, adult patients with AF who underwent percutaneous LAAO between 2010 and 2025 were identified, and three parallel propensity score-matched analyses were conducted: reduced-dose DOAC versus DAPT, SAPT versus DAPT, and reduced-dose DOAC versus SAPT. Outcomes included all-cause death, thromboembolic events, device-related thrombosis, bleeding events and net clinical benefit (NCB).",
  resultados="After matching, 1,773 patients were included in each group for the reduced-dose DOAC versus DAPT comparison (mean follow-up 1.4 ± 1.0 years). Reduced-dose DOAC was associated with lower risks of all-cause death (HR 0.79, 95% CI 0.65-0.96) and major bleeding (HR 0.87, 95% CI 0.77-0.98), with no significant differences in ischaemic stroke, thromboembolism or device-related thrombosis. NCB favoured reduced-dose DOAC (HR 0.87, 95% CI 0.78-0.96). SAPT was also associated with fewer bleeding events and favourable outcomes compared with DAPT. In the reduced-dose DOAC versus SAPT comparison (1,582 matched patients per group), reduced-dose DOAC showed estimates compatible with a slightly higher risk of major bleeding compared with SAPT (HR 1.14, 95% CI 1.00-1.30; p = 0.06), while mortality, thromboembolic outcomes and NCB did not differ significantly.",
  conclusiones="In contemporary practice after LAAO, reduced-dose DOAC therapy was associated with more favourable outcomes than DAPT but showed no clear advantage over SAPT, supporting simplified and individualised post-implantation antithrombotic strategies."))

d.update(NEW)

# --- filas de ponderación para la auditoría (rúbrica de 6 ejes)
SCORES = {
 "a46": dict(rel=6, cambio=7, evid=7, efecto=7, rep=5, fi=6),
 "a47": dict(rel=7, cambio=4, evid=6, efecto=5, rep=5, fi=6),
 "a48": dict(rel=6, cambio=6, evid=5, efecto=6, rep=4, fi=6),
}
W = dict(rel=.20, cambio=.25, evid=.20, efecto=.15, rep=.12, fi=.08)
for k, sc in SCORES.items():
    tot = round(sum(sc[x]*W[x] for x in W), 2)
    assert abs(tot - NEW[k]["total"]) < 0.01, (k, tot, NEW[k]["total"])
    a = NEW[k]
    s.append(dict(key=k, idx=None, pmid="", doi=a["doi"], pii="", journal=a["journal"],
                  sec=a["sec"], ptype=a["ptype"], acr="", **sc, total=tot, prio=a["prio"],
                  oblig=False, noabs=False, alt=None,
                  rec="recuperado por la auditoría de cobertura (Crossref); no indexado en PubMed",
                  title=a["title_en"], abstract=""))

json.dump(d, io.open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(s, io.open(SEL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

from collections import Counter
print("data:", len(d), "| sel:", len(s))
print("por sección:", dict(sorted(Counter(o["sec"] for o in s).items())))
print("a40 fuera:", "a40" not in d)
