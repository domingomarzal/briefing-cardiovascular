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
SECTIONS = [
 (1,"Cardiología preventiva",[
   dict(key="track",
     title="Low-Dose Rivaroxaban and Cardiovascular Events in Advanced Kidney Disease: The TRACK Randomized Clinical Trial",
     ptype="Ensayo clínico aleatorizado", prio="Relevante", journal="JAMA", doi="10.1001/jama.2026.9379",
     resumen="ECA doble ciego en ERC avanzada (estadio 4-5/diálisis) de alto riesgo CV: rivaroxabán 2,5 mg/12 h frente a placebo. No redujo eventos CV (HR 1,09) y aumentó el sangrado mayor (HR 1,51).",
     why="cierra la puerta a la anticoagulación a dosis vascular en ERC avanzada: ni beneficio isquémico ni seguridad; refuerza no extrapolar COMPASS a esta población.",
     modal=[("De qué va.","En la ERC avanzada el 10-15% sufre un evento CV anual y el efecto de los antitrombóticos era desconocido. Ensayo aleatorizado, doble ciego, controlado con placebo en 90 centros de 12 países; adultos con ERC estadio 4-5 o diálisis y comorbilidad vascular o ≥65 años, asignados 1:1 a rivaroxabán 2,5 mg dos veces al día o placebo. Objetivo primario: compuesto de muerte CV, IAM no fatal, ictus o evento de arteriopatía periférica; seguridad: sangrado mayor."),
            ("Resultados.","De 1.458 pacientes (edad media 63,2 años; 29,6% mujeres), 93,3% completó seguimiento. En mediana de 1,7 años el evento primario ocurrió en el 22,6% con rivaroxabán y el 20,7% con placebo (HR 1,09; IC95% 0,87-1,36; P=0,46). El sangrado mayor fue del 8,8% frente al 6,0% (HR 1,51; IC95% 1,02-2,22; P=0,04). El ensayo se detuvo precozmente por falta de eficacia."),
            ("Conclusiones.","En pacientes con ERC avanzada y alto riesgo CV, el rivaroxabán a dosis baja no redujo el evento CV compuesto y aumentó significativamente el sangrado mayor respecto a placebo.")]),
   dict(key="mk7",
     title="Two Years of Menaquinone-7 Supplementation and Coronary Artery Calcification: A Randomized Clinical Trial (VitaK-CAC)",
     ptype="Ensayo clínico aleatorizado", prio="Relevante", journal="JAMA Cardiol", doi="10.1001/jamacardio.2026.1279",
     resumen="ECA con placebo de menaquinona-7 (vitamina K2, 360 µg/día, 2 años) en EC sintomática con CAC 50-400 UA. Atenuó la progresión del calcio coronario (P=0,02).",
     why="primera señal aleatorizada de que la vitamina K2 frena la calcificación coronaria en EC sintomática; abre una vía barata, aunque sin traducción clínica demostrada todavía.",
     modal=[("De qué va.","Se sabía que la vitamina K reduce la calcificación vascular en diabetes o ERC terminal, pero no en EC sintomática. ECA con placebo (VitaK-CAC) en 2 hospitales de Países Bajos: pacientes sintomáticos con CAC 50-400 UA, MK-7 360 µg/día o placebo durante 2 años. Objetivo: evolución del CAC y de la masa de calcio por TC al año y a los 2 años."),
            ("Resultados.","180 aleatorizados (85 MK-7, 82 placebo). Los niveles plasmáticos de MK-7 subieron de 0,50 a 6,56 µg/L (P&lt;0,001). En placebo el CAC pasó de 145 a 173 (1 año) y 214 UA (2 años); con MK-7, de 135 a 150 y 184 UA. La diferencia entre grupos fue significativa (P=0,02), también tras ajuste, con resultado similar para la masa de calcio. El aumento del CAC se correlacionó con el número de placas no calcificadas que se calcificaron parcialmente (R²=0,17; P=0,04). Sin efectos adversos relevantes."),
            ("Conclusiones.","La suplementación con MK-7 durante 2 años puede enlentecer la calcificación de placas no calcificadas en pacientes con EC sintomática; su significado clínico en términos de estabilidad de placa queda por determinar.")]),
   dict(key="estatinas",
     title="Statins and survival free of incident frailty among older US veterans",
     ptype="Cohorte observacional", prio="Relevante", journal="Eur Heart J", doi="10.1093/eurheartj/ehag451",
     resumen="Cohorte de 987.301 veteranos ≥67 años naïve a estatinas con ponderación por propensión. Iniciar estatinas se asoció a menor riesgo de fragilidad incidente o muerte (HR 0,76).",
     why="sugiere un beneficio «extra-lipídico» de las estatinas sobre la fragilidad en mayores, un argumento frente al desprescriptor sistemático por edad.",
     modal=[("De qué va.","La fragilidad comparte fisiopatología con la ECV y es modificable. Veteranos de EE. UU. ≥67 años, naïve a estatinas, atendidos en la VA 2002-2018; excluidos los ya frágiles (VA-FI &gt;0,2). Ponderación por solapamiento de propensión para confusión por indicación; Cox sobre el compuesto fragilidad incidente con censura por muerte."),
            ("Resultados.","De 987.301 veteranos (edad 72±6 años; 98% varones), 290.729 iniciaron estatinas. En seguimiento medio de 5,3 años hubo 636.195 eventos de fragilidad; tasas brutas de 153,1 (iniciadores) frente a 111,4 (no iniciadores) por 1.000 personas-año. Tras ponderación, los nuevos usuarios tuvieron menor riesgo de fragilidad incidente (HR 0,76; IC95% 0,75-0,76); resultados similares en prefrágiles."),
            ("Conclusiones.","El inicio de estatinas se asoció a un riesgo significativamente menor de fragilidad incidente o muerte en veteranos mayores, incluidos los prefrágiles al inicio.")]),
   dict(key="prevent",
     title="Use of Predicted Risk and Expected Benefit to Guide Decision-Making in Cardiovascular-Kidney-Metabolic Syndrome for the Primary Prevention of Cardiovascular Disease: A Scientific Statement From the AHA and ACC",
     ptype="Scientific Statement", prio="Relevante", journal="Circulation", doi="10.1161/CIR.0000000000001447",
     resumen="Documento de posición AHA/ACC sobre el uso de las ecuaciones PREVENT (CVD, ASCVD, HF) con umbrales específicos por desenlace para estadificar y decidir tratamiento en el síndrome CKM.",
     why="operativiza la toma de decisiones en prevención primaria CKM combinando riesgo predicho (PREVENT) con el beneficio absoluto esperado del fármaco.",
     modal=[("De qué va.","Las guías recientes (HTA 2025, dislipemia 2026) incorporan PREVENT para guiar el inicio e intensificación de antihipertensivos e hipolipemiantes. Ante el clustering de factores cardio-reno-metabólicos, el documento propone un enfoque armonizado que integra riesgo predicho con la reducción relativa esperada del tratamiento para estimar el beneficio absoluto."),
            ("Resultados.","Detalla el racional de usar ecuaciones PREVENT específicas por desenlace (PREVENT-CVD, PREVENT-ASCVD, PREVENT-HF), la base de evidencia de los umbrales de riesgo seleccionados y el impacto poblacional potencial; ofrece guía práctica para aplicar la valoración del riesgo como primer paso de la decisión compartida."),
            ("Conclusiones.","Recomienda usar PREVENT con umbrales por desenlace para estadificar, detectar enfermedad subclínica y decidir el inicio/intensificación de terapias CKM, abordando las brechas de concienciación, comunicación del riesgo e implementación.")]),
   dict(key="hta",
     title="Hypertension (In the Clinic)",
     ptype="Revisión (In the Clinic)", prio="Relevante", journal="Ann Intern Med", doi="10.7326/ANNALS-26-01311",
     resumen="Revisión práctica que sintetiza las guías de HTA de EE. UU. e internacionales 2025: objetivos de PA más bajos, mayor uso de PA fuera de consulta y nuevos tratamientos para HTA resistente.",
     why="resume en clave clínica el giro hacia objetivos de PA más estrictos (incluida prevención del deterioro cognitivo) y el nuevo abordaje de la HTA severa.",
     modal=[("De qué va.","Revisión tipo «In the Clinic» sobre el diagnóstico y manejo actualizado de la hipertensión según las guías estadounidenses e internacionales de 2025."),
            ("Resultados.","La guía estadounidense 2025 recomienda objetivos de PA más bajos, mayor uso de PA fuera de consulta para diagnóstico y titulación, y un abordaje distinto de la HTA severa sin síntomas/signos de ECV aguda; se recomiendan nuevos tratamientos para la HTA resistente. La evidencia de ensayos respalda el beneficio del control más estricto para prevenir deterioro cognitivo leve y demencia."),
            ("Conclusiones.","El control tensional más intensivo, con objetivos más bajos y medición ambulatoria, es central en el manejo moderno de la HTA, incluyendo la prevención del deterioro cognitivo.")]),
 ]),
 (2,"Cardiometabolismo",[
   dict(key="findckd",
     title="Finerenone in Persons with Chronic Kidney Disease without Diabetes (FIND-CKD)",
     ptype="Ensayo clínico aleatorizado", prio="Imprescindible", journal="N Engl J Med", doi="10.1056/NEJMoa2604625",
     resumen="ECA con placebo de finerenona en ERC sin diabetes (n=1.584). Enlenteció la caída del FGe (+0,7 ml/min/1,73 m²/año) y redujo el compuesto renal/CV (HR 0,77).",
     why="extiende el beneficio de la finerenona más allá de la nefropatía diabética: la ERC no diabética albuminúrica entra en el área de la finerenona.",
     modal=[("De qué va.","La finerenona mejora desenlaces renales y CV en ERC y DM2; se desconocía su efecto en ERC sin diabetes. Adultos sin diabetes con FGe 25-&lt;90 y albuminuria (cociente albúmina-creatinina 200-≤3.500) con IECA/ARA, aleatorizados a finerenona (10/20 mg) o placebo. Primario: pendiente total del FGe a 32 meses."),
            ("Resultados.","1.584 participantes (793 finerenona, 791 placebo); FGe basal medio 46,8±16,2 vs 46,6±16,0. La caída anual del FGe fue -3,3 (IC95% -3,6 a -3,1) con finerenona frente a -4,0 (-4,3 a -3,8) con placebo (diferencia 0,7; IC95% 0,3-1,1; P&lt;0,001). El compuesto renal o CV fue menor con finerenona (HR 0,77; IC95% 0,60-0,99; P=0,04); HR 0,78 (0,60-1,01) para el compuesto renal y 0,60 (0,27-1,33) para el CV. Hiperpotasemia 17,0% vs 13,3%, con discontinuación en 1,5% vs 0,1% y hospitalización en 0,9% vs 0,6%."),
            ("Conclusiones.","En adultos con ERC sin diabetes, la finerenona produjo una caída más lenta del FGe que placebo a lo largo de 32 meses.")]),
   dict(key="ckm",
     title="2026 AHA/ACC/ADA/ASN Guideline for the Prevention, Detection, Evaluation, and Management of Cardiovascular-Kidney-Metabolic Syndrome",
     ptype="Guía de práctica clínica", prio="Imprescindible", journal="Circulation", doi="10.1161/CIR.0000000000001453",
     resumen="Primera guía conjunta AHA/ACC/ADA/ASN del síndrome cardiovascular-renal-metabólico (CKM); retira y amplía la guía de obesidad de 2013.",
     why="documento estructural del año: unifica obesidad, DM2, ERC y ECV en un marco único de prevención y manejo integrados.",
     modal=[("De qué va.","«Documento vivo» dirigido a clínicos que atienden todo el espectro del síndrome CKM, condición interrelacionada entre factores metabólicos (obesidad, DM2), ERC y ECV. Retira, reemplaza y amplía la guía AHA/ACC/TOS 2013 de sobrepeso y obesidad."),
            ("Resultados.","Basada en una búsqueda bibliográfica exhaustiva (29 oct 2024-14 abr 2025) en MEDLINE, EMBASE, Cochrane, AHRQ y otras, de estudios en humanos publicados desde 2015. Integra estadificación, detección y manejo de los factores cardio-reno-metabólicos interconectados."),
            ("Conclusiones.","Crea un marco unificado y actualizado del síndrome CKM para cardiólogos, endocrinólogos, nefrólogos y atención primaria, con conocimiento actual sobre prevención, detección, evaluación y manejo.")]),
   dict(key="synch1",
     title="Survodutide Once Weekly for the Treatment of Adults with Obesity (SYNCHRONIZE-1)",
     ptype="Ensayo clínico fase 3", prio="Imprescindible", journal="N Engl J Med", doi="10.1056/NEJMoa2600751",
     resumen="ECA fase 3 (n=725) de survodutida (doble agonista glucagón/GLP-1) en obesidad sin diabetes. Pérdida de peso de -13,0% (6 mg) frente a -5,4% con placebo a las 76 semanas.",
     why="suma un doble agonista glucagón-GLP-1 a la carrera de fármacos antiobesidad, con eficacia robusta sobre placebo.",
     modal=[("De qué va.","La survodutida es un doble agonista del receptor de glucagón y de GLP-1. Fase 3 doble ciego: adultos con IMC ≥30, o ≥27 con complicación (sin diabetes), aleatorizados 1:1:1 a survodutida 3,6 mg, 6,0 mg o placebo semanal con consejo de estilo de vida. Coprimarios: % de cambio de peso y reducción ≥5% a la semana 76."),
            ("Resultados.","725 participantes (edad media 47,1 años; IMC medio 37,9; peso 108,8 kg). A la semana 76 el cambio de peso fue -12,2% (3,6 mg), -13,0% (6,0 mg) y -5,4% (placebo); el 72,6%, 71,9% y 46,3% alcanzaron ≥5% de pérdida (P&lt;0,001 frente a placebo). Eventos adversos gastrointestinales (típicamente leves-moderados) en 80,9%, 89,7% y 47,9%. Sin muertes."),
            ("Conclusiones.","La survodutida produjo reducciones de peso significativamente mayores que placebo en adultos con obesidad sin diabetes.")]),
   dict(key="infinity",
     title="Efficacy and safety of finerenone in patients with chronic kidney disease: an individual participant data pooled analysis (INFINITY)",
     ptype="Metaanálisis de datos individuales", prio="Relevante", journal="Lancet", doi="10.1016/S0140-6736(26)01009-3",
     resumen="Metaanálisis de datos individuales de FIDELIO, FIGARO y FIND-CKD (n=14.574). Finerenona redujo el compuesto renal un 24% (HR 0,76), el CV un 20% (HR 0,80) y la mortalidad total (HR 0,88).",
     why="consolida la finerenona como terapia fundacional en ERC a través de etiologías y niveles de glucemia, FGe y albuminuria.",
     modal=[("De qué va.","La sobreactivación del receptor mineralocorticoide es vía común de progresión de ERC. Metaanálisis de datos individuales de tres ECA con placebo (FIDELIO-DKD, FIGARO-DKD, FIND-CKD); Cox para desenlaces renales (fallo renal o caída ≥57% FGe) y CV (hospitalización por IC o muerte CV)."),
            ("Resultados.","14.574 participantes (edad media 63,7 años; 30,7% mujeres; FGe medio 56,4; CAC mediana 567,4 mg/g). Finerenona redujo el compuesto renal 24% (HR 0,76; IC95% 0,68-0,86) y el fallo renal aislado (HR 0,85). El compuesto CV bajó (HR 0,80), incluyendo hospitalización por IC (0,78) y muerte CV (0,82), y la mortalidad total (HR 0,88). Efectos consistentes según glucemia, etiología, FGe, albuminuria y uso de iSGLT2; más hiperpotasemia, con baja hospitalización por ella."),
            ("Conclusiones.","La finerenona reduce la progresión de la ERC, la hospitalización por IC, la muerte CV y la mortalidad total, apoyando su uso como terapia fundacional de la ERC en un amplio rango de etiologías y niveles de glucemia, FGe y albuminuria.")]),
   dict(key="synchmasld",
     title="Survodutide in adults with obesity and metabolic dysfunction-associated steatotic liver disease (SYNCHRONIZE-MASLD)",
     ptype="Ensayo clínico fase 3", prio="Relevante", journal="Nat Med", doi="10.1038/s41591-026-04479-3",
     resumen="ECA fase 3 (n=216) de survodutida en obesidad con MASLD/MASH. El 84,2% logró reducción ≥30% de grasa hepática (vs 24,3%) y -12,2% de peso (vs -1,0%) a la semana 48.",
     why="extiende la survodutida al eje obesidad-hígado graso, un territorio cardiometabólico de creciente interés.",
     modal=[("De qué va.","Survodutida (doble agonista glucagón/GLP-1) en obesidad con MASLD en riesgo (inflamación/fibrosis por pruebas no invasivas o MASH por biopsia). 216 adultos aleatorizados 2:1 a survodutida 6,0 mg semanal (n=146) o placebo (n=70). Coprimarios: reducción ≥30% de grasa hepática por MRI-PDFF y % cambio de peso (basal a semana 48)."),
            ("Resultados.","Ambos coprimarios alcanzados: ≥30% de reducción de grasa hepática en 84,2% (survodutida) vs 24,3% (placebo) (P&lt;0,0001); cambio medio de peso -12,2% vs -1,0% (P&lt;0,0001). Eventos adversos más frecuentes gastrointestinales durante la escalada, leves-moderados. Limitaciones: 48 semanas y reclutamiento solo en EE. UU. y España."),
            ("Conclusiones.","En adultos con obesidad y MASLD en riesgo, la survodutida fue estadística y clínicamente superior a placebo en reducción de grasa hepática y de peso.")]),
 ]),
 (3,"Dislipemia",[
   dict(key="fourier",
     title="Safety of low lipoprotein(a) levels: the FOURIER trial",
     ptype="Análisis de ECA", prio="Relevante", journal="Eur Heart J", doi="10.1093/eurheartj/ehag398",
     resumen="Análisis de FOURIER (25.090 con Lp(a) basal). Una Lp(a) baja no se asoció a más eventos adversos, salvo a mayor riesgo de diabetes prevalente e incidente.",
     why="tranquiliza sobre la seguridad de bajar mucho la Lp(a) con las nuevas terapias, matizando solo la señal con diabetes.",
     modal=[("De qué va.","La Lp(a) es factor causal de aterogénesis, pero se había descrito más diabetes con concentraciones bajas. FOURIER aleatorizó 27.564 pacientes con ECV aterosclerótica estable a evolocumab vs placebo sobre estatina; se evaluó la Lp(a) en 25.090 (mediana 37 nmol/L)."),
            ("Resultados.","No hubo asociación entre la Lp(a) y el riesgo de ictus hemorrágico, sangrado grave, eventos neurocognitivos, malignidad o fibrilación auricular. Sí una asociación inversa entre Lp(a) más baja y diabetes prevalente (OR ajustado 1,03 por cada 50 nmol/L menos) e incidente (HR ajustado 1,05). El evolocumab no aumentó el riesgo de diabetes con independencia de la Lp(a) basal."),
            ("Conclusiones.","En ECV aterosclerótica, una Lp(a) baja no se asoció a más eventos adversos de seguridad, pero sí a mayor riesgo de diabetes prevalente e incidente.")]),
   dict(key="aavhofh",
     title="AAV gene therapy for homozygous familial hypercholesterolemia: a phase 1 trial (NGGT006)",
     ptype="Ensayo fase 1", prio="Relevante", journal="Nat Med", doi="10.1038/s41591-026-04441-3",
     resumen="Terapia génica AAV8 (NGGT006) que expresa LDLR hepático en HoFH. En el paciente con dosis alta, el LDL-C bajó de 11 a &lt;1,8 mmol/L de forma sostenida.",
     why="prueba de concepto de terapia génica para corregir el déficit de LDLR en la HoFH, la dislipemia más grave.",
     modal=[("De qué va.","La HoFH cursa con LDL-C muy elevado y aterosclerosis acelerada; &gt;80% portan mutaciones de LDLR. NGGT006 es un vector AAV8 con LDLR-cDNA optimizado. Ensayo abierto, un brazo, escalado de dosis: tres pacientes con HoFH recibieron 7,5×10¹², 1,5×10¹³ y 3×10¹³ vg/kg. Primarios: seguridad y reducción de LDL-C a 52 semanas."),
            ("Resultados.","Bien tolerado, sin eventos adversos graves relacionados con el vector. Los tres pacientes mostraron elevación de enzimas hepáticas, resueltas con sirolimus y metilprednisolona. El paciente con dosis más alta tuvo reducción sostenida de LDL-C de 11 mmol/L a &lt;1,8 mmol/L desde la semana 3."),
            ("Conclusiones.","Ofrece una primera visión de la seguridad y el potencial terapéutico de NGGT006 y justifica estudios futuros de seguridad y eficacia.")]),
   dict(key="metilacion",
     title="Blood DNA Methylation Patterns Across Carotid, Coronary, and Peripheral Atherosclerosis: A Comparative Analysis in 2 Prospective Cohorts",
     ptype="Investigación original (epigenómica, EWAS)", prio="Relevante", journal="J Am Coll Cardiol", doi="10.1016/j.jacc.2026.04.009",
     resumen="EWAS en 3.688 individuos de 2 cohortes prospectivas que mapea la metilación del ADN (767.735 sitios CpG) en aterosclerosis carotídea, coronaria y periférica. Los scores epigenéticos predijeron MACE (HR 1,23-1,39), pero &gt;90% de los sitios solapaban con factores de riesgo, sobre todo tabaquismo.",
     why="la firma epigenética de la aterosclerosis refleja sobre todo la exposición acumulada (tabaco, disregulación cardiometabólica) más que procesos vasculares específicos.",
     modal=[("De qué va.","Estudio que identifica sitios CpG diferencialmente metilados relacionados con la aterosclerosis en distintos lechos vasculares y evalúa en qué medida estas firmas epigenéticas reflejan factores de riesgo cardiovascular (FRCV). Se analizó la metilación del ADN en sangre en 767.735 sitios CpG en 3.688 individuos de 2 cohortes prospectivas (aterosclerosis carotídea, coronaria y periférica), con EWAS corregidos al 5% de FDR y scores de metilación validados en una cohorte independiente."),
            ("Resultados.","Se asociaron significativamente 1.687, 3.131 y 5.852 sitios CpG con aterosclerosis carotídea, coronaria y periférica, respectivamente; 2.155 en ≥2 territorios. Las señales más fuertes mapearon a loci cercanos a ALPP/ALPG, AHRR, PRSS23 y F2RL3, con señales adicionales en ABCG1 y DHCR24 en la coronaria. Los scores epigenéticos predijeron MACE (HR 1,23-1,39; todos P&lt;0,001). Más del 90% de los sitios CpG asociados a aterosclerosis solapaban con sitios asociados a FRCV, especialmente tabaquismo (hasta 90%), inflamación (60%) y rasgos metabólicos (44%)."),
            ("Conclusiones.","La firma epigenética de la aterosclerosis en sangre refleja en gran medida la exposición acumulada, particularmente tabaquismo y disregulación cardiometabólica, más que procesos biológicos específicos de cada territorio vascular.")]),
   dict(key="lpaukb",
     title="Lipoprotein(a) and residual cardiovascular risk in statin-treated patients (UK Biobank)",
     ptype="Cohorte observacional", prio="Complementario", journal="Eur J Prev Cardiol", doi="10.1093/eurjpc/zwag296",
     resumen="Cohorte UK Biobank (n=17.376) en estatinas. Una Lp(a) moderadamente elevada (&gt;46,8 nmol/L), por debajo de los umbrales actuales, se asoció a 20% más de MACE.",
     why="sugiere que los umbrales actuales de Lp(a) infraestiman el riesgo residual, sobre todo sin ECV establecida.",
     modal=[("De qué va.","Evalúa el riesgo asociado a una Lp(a) moderadamente elevada por debajo de los umbrales actuales en población tratada con estatinas. 17.376 pacientes ≥45 años con ECV establecida o DM2 (UK Biobank); MACE = IAM no fatal, ictus no fatal o muerte CV; comparando terciles inferior y superior de Lp(a) (&lt;12,5 vs &gt;46,8 nmol/L)."),
            ("Resultados.","El tercil superior se asoció a 20% más de MACE (P&lt;0,01), 27% más de hospitalización por IAM, 34% más de revascularización coronaria y 30% más de mortalidad CV. El efecto fue más pronunciado en quienes no tenían ECV establecida."),
            ("Conclusiones.","Una Lp(a) moderadamente elevada por debajo de los umbrales de guía se asocia a más eventos CV en población en estatinas, con efecto mayor en quienes no tienen ECV establecida; los umbrales actuales pueden infraestimar el riesgo residual.")]),
   dict(key="vesiculas",
     title="Extracellular vesicles in atherosclerotic cardiovascular disease: mechanisms and therapeutic implications",
     ptype="Revisión", prio="Complementario", journal="Eur Heart J", doi="10.1093/eurheartj/ehag404",
     resumen="Revisión sobre el papel de las vesículas extracelulares (EVs) en la aterosclerosis: comunicación intercelular, formación de células espumosas, manejo del colesterol, inestabilidad y calcificación de la placa, y su potencial como biomarcadores y dianas terapéuticas.",
     why="sitúa a las vesículas extracelulares como reguladores del manejo del colesterol y la estabilidad de la placa, abriendo una vía terapéutica y de biomarcadores.",
     modal=[("De qué va.","Revisión que examina el papel de las vesículas extracelulares (EVs) como reguladores centrales de la comunicación intercelular en la patología cardiovascular, con foco en su participación en el inicio y la progresión de la inflamación de la pared arterial en la aterosclerosis."),
            ("Resultados.","Las EVs derivadas de endotelio, leucocitos, plaquetas, eritrocitos y células musculares lisas vasculares (CMLV) participan activamente: las endoteliales transportan proteínas proinflamatorias y microARN que deterioran la función endotelial; las plaquetarias y leucocitarias amplifican el reclutamiento de monocitos y la señalización trombótica. Al madurar la lesión, contribuyen a la formación de células espumosas y al cambio fenotípico de las CMLV, transportando lípidos, enzimas y ácidos nucleicos que influyen en el manejo del colesterol, el remodelado de matriz y la apoptosis, favoreciendo la inestabilidad de la placa; son además impulsoras de la calcificación vascular."),
            ("Conclusiones.","Por su accesibilidad en circulación y su implicación mecanística, las EVs ofrecen oportunidades como biomarcadores y como dianas terapéuticas (modular su liberación, modificar su composición o ingeniería de sistemas de entrega basados en EVs).")]),
 ]),
 (4,"Cardiopatía isquémica",[
   dict(key="p2y12",
     title="P2Y12 inhibitor monotherapy after abbreviated dual antiplatelet therapy following percutaneous coronary intervention: a meta-analysis",
     ptype="Metaanálisis", prio="Imprescindible", journal="Eur Heart J", doi="10.1093/eurheartj/ehag381",
     resumen="Metaanálisis de 11 ECA (37.443 pacientes). Suspender la aspirina a ≤1 o 3 meses con monoterapia P2Y12 igualó el MACE y redujo el sangrado frente a DAPT 12 meses.",
     why="refuerza la monoterapia P2Y12 tras DAPT corta como estándar; matiza el riesgo de trombosis del stent con suspensión muy precoz en SCA.",
     modal=[("De qué va.","Tras ICP crece la evidencia de monoterapia P2Y12 tras DAPT corta, pero el momento óptimo de suspender la aspirina es incierto. Revisión sistemática y metaanálisis (pareado y en red) de ECA que comparan tiempos de suspensión de aspirina frente a DAPT continuada. Primario: MACE; secundarios: sangrado, NACE, muerte, IAM."),
            ("Resultados.","11 ECA, 37.443 pacientes. Frente a DAPT 12 meses, sin diferencias en MACE al suspender aspirina a ≤1 mes (RR 1,01) o 3 meses (RR 0,95). El sangrado mayor o menor se redujo con ≤1 mes (RR 0,43) y 3 meses (RR 0,57). El NACE bajó con ≤1 mes. En SCA, la suspensión muy precoz (&lt;1 mes) se asoció a más trombosis del stent (RR 1,81; IC95% 1,15-2,84; P=0,019)."),
            ("Conclusiones.","Suspender la aspirina a ≤1 o 3 meses con monoterapia P2Y12 logra un MACE similar con menos sangrado y menor NACE que la DAPT continuada; la suspensión en el primer mes añade beneficio hemorrágico pero a costa de exceso de trombosis del stent, sobre todo en alto riesgo isquémico.")]),
   dict(key="favor3",
     title="Angiographic Quantitative Flow Ratio-Guided Coronary Intervention: 5-Year Follow-Up From the FAVOR III China Randomized Trial",
     ptype="ECA (seguimiento)", prio="Imprescindible", journal="J Am Coll Cardiol", doi="10.1016/j.jacc.2026.04.037",
     resumen="Seguimiento a 5 años del ECA FAVOR III China: ICP guiada por QFR vs angiografía. MACE 17,5% vs 21,1% (HR 0,80), con menos IAM y revascularización.",
     why="confirma a largo plazo el beneficio de la guía fisiológica con QFR, acumulado sobre todo en los 2 primeros años.",
     modal=[("De qué va.","FAVOR III China había mostrado mejores resultados con ICP guiada por QFR a 1-2 años; se evaluó si el beneficio se mantiene a 5 años. Pacientes con lesión intermedia (50-90%) en vaso ≥2,5 mm aleatorizados a estrategia guiada por QFR (ICP si QFR ≤0,80) o por angiografía."),
            ("Resultados.","A 5 años, el MACE fue menor con QFR (17,5% vs 21,1%; HR 0,80; IC95% 0,69-0,92; P=0,002), por menos IAM (5,8% vs 9,0%; HR 0,63; P&lt;0,0001) y revascularización guiada por isquemia (9,6% vs 12,0%; HR 0,78; P=0,02). Sin diferencias en mortalidad total. El beneficio se acumuló en los primeros 2 años (8,5% vs 12,5%; HR 0,66; P&lt;0,0001) y se igualó entre 2 y 5 años (10,2% vs 11,2%; HR 0,90; P interacción=0,001)."),
            ("Conclusiones.","La estrategia guiada por QFR mejoró los resultados clínicos a 5 años frente a la guía angiográfica, con el beneficio logrado principalmente en los primeros 2 años.")]),
   dict(key="abyss",
     title="Heart Rate and Cardiovascular Outcomes in Post-Myocardial Infarction Patients Treated by β-Blockers: A Secondary Analysis of the ABYSS Trial",
     ptype="Subanálisis de ECA", prio="Relevante", journal="Circulation", doi="10.1161/CIRCULATIONAHA.125.078635",
     resumen="Subanálisis de ABYSS (3.698 post-IAM, FEVI ≥40%). Interrumpir el betabloqueante subió la FC ~10-13 lpm y se asoció a peores desenlaces, con mayor riesgo a FC alta.",
     why="apoya mantener el betabloqueante tras IAM en la era de reperfusión, ligando la interrupción al ascenso de FC y a peor pronóstico.",
     modal=[("De qué va.","Análisis secundario preespecificado del ECA ABYSS: 3.698 pacientes estables post-IAM con FEVI ≥40% aleatorizados a continuar o interrumpir el betabloqueante, agrupados por terciles de FC prerandomización (&lt;60, 60-&lt;68, ≥68 lpm). Primario: muerte, IAM, ictus o rehospitalización CV."),
            ("Resultados.","Edad mediana 63,5 años; 17,1% mujeres. La FC basal no se asoció al primario (22,4% vs 21,8% vs 21,6%; P=0,867), pero una FC mayor se asoció a más muerte/IAM/ictus (5,5% vs 6,4% vs 9,2%; T3 vs T1 HR ajustado 1,55; IC95% 1,14-2,12) y a más mortalidad total (2,9% vs 3,4% vs 5,9%; P=0,004). Interrumpir el betabloqueante elevó la FC ~10-13 lpm y se asoció consistentemente a peores desenlaces, sin interacción por tercil de FC ni por FEVI."),
            ("Conclusiones.","En post-IAM estabilizado con FEVI preservada, una FC más alta sigue asociándose a eventos CV y mortalidad; interrumpir el betabloqueante sube la FC y se vincula a peores desenlaces, apoyando su continuación.")]),
   dict(key="complete",
     title="Impact of Revascularization Completeness on Cardiovascular Outcomes in STEMI With Multivessel Disease (COMPLETE)",
     ptype="Observacional (post hoc ECA)", prio="Relevante", journal="Circ Cardiovasc Interv", doi="10.1161/CIRCINTERVENTIONS.126.016515",
     resumen="Análisis post hoc de COMPLETE: el beneficio de la revascularización completa en STEMI multivaso depende del grado de completitud anatómica (R'SS=0).",
     why="matiza que el beneficio de la estrategia completa solo se materializa cuando la revascularización es realmente completa (residual SYNTAX score 0).",
     modal=[("De qué va.","La revascularización completa es superior a tratar solo la lesión culpable en STEMI multivaso, pero la relación entre el grado de completitud y el beneficio no estaba clara. Subestudio post hoc exploratorio de COMPLETE (n=3.738), estratificando el brazo de revascularización completa según el residual SYNTAX modificado (R'SS), con el brazo culpable-solo como referencia."),
            ("Resultados.","El 90% logró revascularización completa (R'SS=0) y el 10% no. En R'SS=0, el primer coprimario (muerte CV/IAM) ocurrió menos (6,6%) que en culpable-solo (10,7%; HR ajustado 0,61; IC95% 0,47-0,78). En R'SS&gt;0, fue similar a culpable-solo (10,7% vs 10,7%; HR 1,01)."),
            ("Conclusiones.","El beneficio de la estrategia de revascularización completa en STEMI multivaso parece depender del grado de completitud anatómica alcanzado.")]),
   dict(key="tncronica",
     title="Improving the diagnostic performance of troponin assays for acute myocardial infarction in renal impairment",
     ptype="Estudio diagnóstico", prio="Relevante", journal="Heart", doi="10.1136/heartjnl-2025-327658",
     resumen="Estudio diagnóstico en 221.175 pacientes: la performance de la troponina para IAM cae con el FGe; se proponen umbrales específicos por FGe (73/112/184 ng/L).",
     why="ofrece cortes de troponina T-hs específicos por función renal para reducir falsos positivos sin perder demasiada detección.",
     modal=[("De qué va.","La interpretación de una primera troponina elevada en insuficiencia renal es difícil. Se analizó la relación FGe-troponina, el rendimiento de distintos ensayos y se derivaron umbrales específicos por FGe; 221.175 pacientes (2010-2017) de cuatro hospitales terciarios de Londres."),
            ("Resultados.","FGe &lt;60 en 20,6% y diagnóstico de IAM en 6,4%. Relación log-lineal inversa entre FGe y troponina en no-IAM. Rendimiento mejor con FGe&gt;90 (C 0,93) y peor con FGe&lt;15 (C 0,81). Con el corte convencional de 14 ng/L, los falsos positivos fueron del 68-93% para FGe 15-60. Restringiendo el falso positivo al 15%, los cortes específicos fueron 73, 112 y 184 ng/L."),
            ("Conclusiones.","El rendimiento de un corte único de troponina cae al empeorar la función renal; se propone considerar cortes específicos por FGe para mejorar el triaje y el manejo precoz del IAM sospechado en insuficiencia renal.")]),
 ]),
 (5,"Insuficiencia cardíaca",[
   dict(key="shock",
     title="Acute Myocardial Infarction versus Acute Decompensated Heart Failure in Cardiogenic Shock: A Systematic Review and Meta-Analysis of Clinical Phenotypes and Mortality",
     ptype="Revisión sistemática y metaanálisis", prio="Relevante", journal="Eur J Heart Fail", doi="10.1093/ejhf/xuag186",
     resumen="Metaanálisis de 29 estudios (497.368 pacientes) comparando shock cardiogénico por IAM vs por IC descompensada. El AMI-CS se presenta más fulminante y con mayor mortalidad a corto plazo (OR 1,58).",
     why="aporta un marco de doble eje (gravedad × etiología) para abordar fenotipos distintos del shock cardiogénico.",
     modal=[("De qué va.","El shock cardiogénico tiene fenotipos distintos según IAM (AMI-CS) o IC descompensada (ADHF-CS), con evidencia comparativa limitada. Metaanálisis (PRISMA 2020) de estudios observacionales 2019-2025; primario: mortalidad a corto plazo (intrahospitalaria/30 días)."),
            ("Resultados.","29 estudios, 497.368 pacientes. AMI-CS más mayores (MD 4,76 años) y con mayor FEVI al ingreso; presentación más fulminante (parada cardiaca OR 2,03; SCAI D/E OR 1,50). Más soporte circulatorio temporal en AMI-CS (cualquier dispositivo OR 5,44). La mortalidad a corto plazo fue mayor en AMI-CS (OR 1,58; IC95% 1,06-2,37)."),
            ("Conclusiones.","El AMI-CS se presenta más fulminante que el ADHF-CS, con mucho mayor uso de soporte mecánico y mayor mortalidad a corto plazo; se propone un marco de doble eje (gravedad × etiología), pendiente de validación prospectiva.")]),
   dict(key="hm3",
     title="Survival Outcomes in Middle-Aged and Older Patients With Advanced Heart Failure: A Propensity-Matched Analysis of HeartMate 3 LVAD and Heart Transplant Using MOMENTUM 3 and UNOS Registry",
     ptype="Análisis de registro", prio="Relevante", journal="JACC Heart Fail", doi="10.1016/j.jchf.2026.103159",
     resumen="Análisis pareado por propensión (HM3 n=1.763; UNOS n=5.336). El trasplante tuvo mayor supervivencia a 2 años desde el tratamiento, pero al incluir la lista de espera el HM3 superó en supervivencia.",
     why="reposiciona el tiempo en lista como variable clave al elegir entre LVAD HM3 y trasplante en mayores.",
     modal=[("De qué va.","Compara supervivencia y eventos adversos en adultos de mediana edad (50-64) y mayores (≥65) con IC avanzada que recibieron HeartMate 3 o fueron listados/trasplantados. Cohortes MOMENTUM 3 (HM3) y registro UNOS 2014-2018, con emparejamiento por propensión."),
            ("Resultados.","Tras emparejar, el trasplante tuvo mayor supervivencia a 2 años desde el tratamiento (mediana edad: 90,7% vs 83,8%; HR 1,76; mayores: 87,5% vs 77,7%; HR 1,89). Pero incorporando la lista de espera, el HM3 superó a la supervivencia libre de exclusión por deterioro en mediana edad (83,0% vs 75,0%; HR 0,62) y numéricamente en mayores (HR 0,81; P=0,064)."),
            ("Conclusiones.","La supervivencia a 2 años fue mayor post-trasplante que con HM3; pero incluyendo el tiempo en lista, el HM3 mostró mayor supervivencia que la libre de exclusión por deterioro en candidatos a trasplante, subrayando el peso del tiempo de espera.")]),
   dict(key="c2d",
     title="Ambulatory Stage C2D Heart Failure Definitions and Current Therapeutic Approaches: JACC: Heart Failure Position Statement",
     ptype="Documento de posición", prio="Relevante", journal="JACC Heart Fail", doi="10.1016/j.jchf.2026.103101",
     resumen="Documento de posición que define el estadio C2D de la IC: población ambulatoria que progresa más allá del estadio C sin ser aún estadio D terminal.",
     why="crea una categoría útil (C2D) para reconocer y tratar al paciente que escapa al control con TMOG pero aún no es candidato a trasplante/asistencia.",
     modal=[("De qué va.","La IC con FEr se ha dibujado en 2 estadios sintomáticos. El documento propone reconocer el estadio C2D: población ambulatoria que progresa más allá de la respuesta sostenida a TMOG pero que aún busca y puede ganar años de vida significativos."),
            ("Resultados.","Encarga mejorar el reconocimiento de C2D, mapear las brechas de conocimiento sobre cómo extender las terapias del estadio C a C2D, e impulsar próximos pasos: identificación y curación de cohortes C2D y disección de fenotipos fisiológicos con determinantes sociales y preferencias del paciente como modificadores."),
            ("Conclusiones.","Definir y enfocar el estadio C2D inspirará nuevas estrategias para revisar trayectorias más allá del estadio C y a lo largo del recorrido de la IC.")]),
   dict(key="reducelap",
     title="Heart Failure Duration, Cardiac Remodeling, Dysfunction, and Hemodynamic Severity in HFpEF and HFmrEF: Insights From REDUCE LAP-HF II",
     ptype="Análisis de ECA", prio="Relevante", journal="JACC Heart Fail", doi="10.1016/j.jchf.2026.103167",
     resumen="Análisis de REDUCE LAP-HF II (n=626): mayor duración de la IC se asoció a más remodelado, peor strain y mayor riesgo de empeoramiento (HR 1,70 para &gt;3 años vs &lt;1 año).",
     why="refuerza el diagnóstico precoz de HFpEF: el tiempo de enfermedad marca remodelado y pronóstico.",
     modal=[("De qué va.","Determina cómo la duración del diagnóstico de IC influye en estructura/función cardiaca, hemodinámica, riesgo de empeoramiento y respuesta al tratamiento. Participantes de REDUCE LAP-HF II (N=626; FEVI ≥40% y PCP de ejercicio ≥25 mmHg) por duración de IC: &lt;1, 1-3 y &gt;3 años."),
            ("Resultados.","Mayor duración → más remodelado: menor GLS del VI (16,4% vs 17,7% vs 18,4%; P&lt;0,0001) y del VD (20,8% vs 22,2% vs 24,4%; P&lt;0,0001), más miopatía biauricular (48,8% vs 40,8% vs 28,2%; P&lt;0,0001) y más elevación de PCP en reposo (75,8% vs 70,7% vs 64,9%; P=0,024). El riesgo de eventos de IC aumentó con la duración (HR 1,70; IC95% 1,17-2,48 para &gt;3 años vs &lt;1 año). Sin heterogeneidad en la respuesta al shunt auricular."),
            ("Conclusiones.","Mayor duración de la HFpEF se asocia a remodelado y disfunción más avanzados y a mayor riesgo de empeoramiento, subrayando la prioridad del diagnóstico precoz.")]),
   dict(key="dcd",
     title="Long-Term Outcomes From a Decade of Donation After Circulatory Death Heart Transplantation in Australia",
     ptype="Registro / cohorte", prio="Relevante", journal="JACC Heart Fail", doi="10.1016/j.jchf.2026.103168",
     resumen="Cohorte de una década (DCD n=118 vs DBD n=385): supervivencia a 10 años similar (67% vs 64%) y libertad de vasculopatía del injerto comparable.",
     why="establece la seguridad y eficacia a largo plazo del trasplante con donante en asistolia, clave para expandir el pool de donantes.",
     modal=[("De qué va.","El trasplante con donante tras muerte circulatoria (DCD) amplía el pool con buena supervivencia a corto plazo, pero con incertidumbre a largo plazo. Receptores consecutivos en St Vincent's (Sídney) de julio 2014 a diciembre 2024: DCD (n=118; perfusión normotérmica) vs DBD (n=385)."),
            ("Resultados.","Sin diferencias significativas en supervivencia (1 año: 94% vs 88%; 10 años: 67% vs 64%; HR 0,9; P=0,5). Libertad de vasculopatía del injerto a 10 años 61% (DCD) vs 41% (DBD). Disfunción primaria grave similar (14% vs 14%); el tiempo de isquemia caliente asistólica fue el único factor de riesgo independiente en DCD (OR 1,4; P=0,03)."),
            ("Conclusiones.","Los receptores de corazón DCD tienen supervivencia y libertad de vasculopatía a 10 años similares a los DBD contemporáneos, estableciendo la seguridad y eficacia a largo plazo del DCD.")]),
 ]),
 (6,"Miocardiopatías",[
   dict(key="sglt2gen",
     title="Effects of SGLT2 inhibition on incident heart failure in carriers of cardiomyopathy-associated genetic variants (DECLARE-TIMI 58)",
     ptype="Subanálisis genético de ECA", prio="Relevante", journal="Nat Med", doi="10.1038/s41591-026-04439-x",
     resumen="Secuenciación exómica en DECLARE-TIMI 58: en portadores de variantes patógenas de miocardiopatía, la dapagliflozina redujo más la hospitalización por IC (HR 0,18 vs 0,70; reducción absoluta 13,0% vs 1,0%).",
     why="sugiere que los iSGLT2 podrían iniciarse precozmente para prevenir IC en portadores de variantes de miocardiopatía.",
     modal=[("De qué va.","Se desconocía si la inhibición de SGLT2 beneficia a portadores de variantes raras en genes de miocardiopatía. Se analizó la secuenciación exómica de DECLARE-TIMI 58 (DM2 y riesgo CV, dapagliflozina vs placebo); variantes patógenas/probablemente patógenas en genes de alta confianza; efecto sobre hospitalización por IC en portadores vs no portadores."),
            ("Resultados.","De 12.685 pacientes secuenciados, 121 portaban una variante de miocardiopatía (76 DCM, 25 HCM, 25 arritmogénica). En mediana de 4,2 años, la dapagliflozina redujo más la hospitalización por IC en portadores (HR 0,18; IC95% 0,04-0,86) que en no portadores (HR 0,70; P interacción 0,03). Reducción absoluta 13,0% vs 1,0%. El 82% no tenía IC previa."),
            ("Conclusiones.","Los hallazgos plantean que el tratamiento con iSGLT2 podría iniciarse precozmente para prevenir IC en portadores de variantes patógenas de miocardiopatía; debe confirmarse en un ensayo prospectivo dedicado.")]),
   dict(key="mavacamten",
     title="Safety and efficacy of mavacamten in obstructive versus non-obstructive hypertrophic cardiomyopathy: a meta-analysis of randomised controlled trials",
     ptype="Metaanálisis de ECA", prio="Relevante", journal="Heart", doi="10.1136/heartjnl-2025-327651",
     resumen="Metaanálisis de 5 ECA (1.083 pacientes). Mavacamten mejoró síntomas y obstrucción en MCH obstructiva; en no obstructiva no aportó beneficio funcional y elevó el riesgo de FEVI &lt;50% (OR 14,35).",
     why="apoya una terapia guiada por fenotipo y advierte sobre el uso off-label en MCH no obstructiva.",
     modal=[("De qué va.","Mavacamten (inhibidor selectivo de miosina cardiaca) es opción en MCH, pero su efecto diferencial por fenotipo estaba incompletamente caracterizado. Metaanálisis de ECA hasta octubre 2025; desenlaces: NYHA, KCCQ-CSS, pico VO₂, gradiente TSVI, biomarcadores y eventos adversos, estratificado por fenotipo (oHCM vs nHCM)."),
            ("Resultados.","5 ECA (1.083 pacientes; 444 oHCM, 639 nHCM). En oHCM, mejoró NYHA (OR 4,94) y KCCQ-CSS (MD 8,99) con reducciones marcadas del gradiente. El riesgo de FEVI &lt;50% se elevó mucho en nHCM (OR 14,35; IC95% 5,92-34,77), no en oHCM. En nHCM, sin beneficio funcional. Los biomarcadores (NT-proBNP, hs-cTnI) bajaron en ambos."),
            ("Conclusiones.","Mavacamten es eficaz en oHCM con perfil de seguridad tranquilizador; en nHCM produce remodelado bioquímico/estructural sin beneficio sintomático y con posible mayor riesgo de disfunción sistólica, apoyando una terapia de precisión guiada por fenotipo y cautela con el uso off-label.")]),
   dict(key="arvc",
     title="Arrhythmogenic right ventricular cardiomyopathy",
     ptype="Revisión", prio="Relevante", journal="Eur Heart J", doi="10.1093/eurheartj/ehag297",
     resumen="Revisión de la miocardiopatía arritmogénica (ACM): scarring ventricular y reemplazo fibro-graso, con riesgo de muerte súbita, sobre todo en jóvenes y atletas de resistencia.",
     why="sintetiza el cambio de paradigma de un diagnóstico «fenotipo-primero» a uno «genotipo-primero».",
     modal=[("De qué va.","Revisión sobre la miocardiopatía arritmogénica, forma heredable caracterizada por cicatrización ventricular y/o reemplazo fibro-graso, asociada a riesgo significativo de muerte súbita por arritmias ventriculares, especialmente en jóvenes y atletas de resistencia."),
            ("Resultados.","Resume el cambio en la comprensión y encuadre de esta enfermedad multifacética, destacando la transición actual de un marco «fenotipo-primero» a uno «genotipo-primero» para el diagnóstico y el manejo."),
            ("Conclusiones.","El diagnóstico y manejo de la ACM evolucionan hacia un enfoque genotipo-primero.")]),
   dict(key="genohcm",
     title="Genotype Predicts Heart Failure Independent of LVEF, Peak VO2, and NT-proBNP Levels in Hypertrophic Cardiomyopathy",
     ptype="Cohorte / genética", prio="Relevante", journal="JACC Heart Fail", doi="10.1016/j.jchf.2026.103149",
     resumen="Cohorte de 505 pacientes con MCH genotipados. El estatus gen-positivo predijo IC-muerte/trasplante independientemente de FEVI, pico VO₂ y NT-proBNP (HR 5,86).",
     why="el genotipo añade valor pronóstico independiente sobre los marcadores clásicos en MCH, útil para monitorización y selección de ensayos.",
     modal=[("De qué va.","~40% de las MCH se deben a variantes sarcoméricas. Cohorte observacional unicéntrica de 505 pacientes genotipados (52 años; 33% mujeres), estratificados en gen-positivos (G+) y gen-elusivos (G-). Primario: muerte por IC o trasplante."),
            ("Resultados.","En mediana de 10,6 años, 34 pacientes (6,7%) tuvieron el evento primario. El endpoint de IC ocurrió en 12,8% de G+ vs 2,1% de G-. En Cox multivariable, fueron independientes: G+ (HR 5,86; IC95% 2,26-15,25), log NT-proBNP (HR 2,46), pico VO₂ (HR 0,90) y FEVI (HR 0,74 por 5%)."),
            ("Conclusiones.","Genotipo, pico VO₂, log NT-proBNP y FEVI predicen de forma independiente los desenlaces de IC en MCH; combinar genotipo con biomarcadores y capacidad funcional identifica a los pacientes de mayor riesgo y puede apoyar monitorización dirigida y selección para ensayos.")]),
   dict(key="takotsubo",
     title="Independent prognostic value of left ventricular stroke volume index in patients with takotsubo syndrome: insights from the EVOLUTION registry",
     ptype="Registro (cohorte observacional, RMC)", prio="Complementario", journal="Heart", doi="10.1136/heartjnl-2026-327797",
     resumen="Registro multicéntrico (376 pacientes con síndrome de takotsubo y RMC precoz). Un volumen latido indexado del VI bajo (&lt;35 mL/m²) predijo de forma independiente eventos (HR 0,96 por unidad); un LVSVi alto con FEVI recuperada identificó un subgrupo de bajo riesgo.",
     why="aporta un marcador de RMC precoz pronóstico en takotsubo, más allá de la FEVI, que ayuda a separar a los pacientes de bajo riesgo.",
     modal=[("De qué va.","Estudio observacional (registro EVOLUTION) que evalúa el valor pronóstico del volumen latido del VI indexado derivado de RMC (LVSVi) en el síndrome de takotsubo (TTS). Pacientes consecutivos con TTS se sometieron a RMC a una mediana de 5 días (3-7) del ingreso; análisis centralizado y categorización por LVSVi (&lt;35 vs ≥35 mL/m²). Objetivo primario: compuesto de eventos cardiovasculares mayores y muerte por cualquier causa."),
            ("Resultados.","Se incluyeron 376 pacientes (edad media 70±11 años; 9% varones). La FEVI al ingreso fue del 43%, ascendiendo al 48% en la RMC. 172 (46%) tenían LVSVi &lt;35 mL/m²: eran mayores, con más hipertensión, disnea y menor FEVI. El grupo de LVSVi bajo presentó mayores tasas del objetivo primario y secundario (ambos log-rank P&lt;0,01); los de LVSVi alto y FEVI normal tuvieron las tasas más bajas. En Cox multivariable, el LVSVi fue predictor independiente del objetivo primario (HR 0,96; IC95% 0,92-0,98) y secundario (HR 0,95; IC95% 0,90-0,99)."),
            ("Conclusiones.","La RMC precoz tras el ingreso en TTS muestra recuperación de la FEVI con LVSVi relativamente bajo. Un LVSVi bajo predijo de forma independiente el pronóstico a medio plazo, y la combinación de LVSVi alto con FEVI recuperada identificó un subgrupo de bajo riesgo.")]),
 ]),
 (7,"Valvulopatías",[
   dict(key="coapt",
     title="Estimating the Effects of MTEER in U.S. Practice: A Transportability Analysis of the COAPT Trial",
     ptype="Análisis de ECA (transportabilidad)", prio="Relevante", journal="J Am Coll Cardiol", doi="10.1016/j.jacc.2026.04.025",
     resumen="Análisis de transportabilidad de COAPT al registro TVT (15.275 pacientes). El MTEER en práctica real lograría reducciones absolutas a 2 años del 17,0% en hospitalización por IC y 15,4% en muerte.",
     why="apoya la generalización de los resultados de COAPT a la práctica clínica estadounidense actual, pese a perfiles basales distintos.",
     modal=[("De qué va.","Tras COAPT, el MTEER se aprobó para insuficiencia mitral secundaria, pero otros ensayos dieron resultados mixtos. Se usaron métodos de transportabilidad para estimar los efectos de las intervenciones de COAPT en 2 poblaciones diana del registro TVT. Primario: hospitalización por IC a 2 años."),
            ("Resultados.","614 pacientes de COAPT y 15.275 del TVT (7.289 elegibles). Los elegibles del TVT tenían menos miocardiopatía isquémica y más IM 4+. Frente a tratamiento médico, el MTEER lograría reducciones absolutas a 2 años de 17,0% en hospitalización por IC y 15,4% en muerte, similares al ensayo."),
            ("Conclusiones.","Pese a características basales distintas, los efectos del tratamiento serían similares si los pacientes del mundo real recibieran las intervenciones de COAPT, bajo los supuestos de transportabilidad.")]),
   dict(key="itmeta",
     title="Prevalence and prognostic role of untreated moderate-to-severe tricuspid regurgitation: a systematic review and meta-analysis",
     ptype="Revisión sistemática y metaanálisis", prio="Relevante", journal="Eur J Heart Fail", doi="10.1093/ejhf/xuag192",
     resumen="Metaanálisis de 106 estudios (961.136 pacientes). La IT moderada-grave no tratada duplicó la mortalidad total (HR 2,07), con incremento escalonado por gravedad.",
     why="cuantifica con enorme casuística el peso pronóstico de la IT no tratada y respalda el diagnóstico y manejo oportunos.",
     modal=[("De qué va.","Evalúa el papel pronóstico de la insuficiencia tricúspide (IT) moderada-grave no tratada. Búsqueda en PubMed hasta el 14 de agosto de 2025; primario: mortalidad total; secundarios: mortalidad CV y hospitalización por IC; modelos de efectos aleatorios."),
            ("Resultados.","106 estudios (107 comparaciones; 961.136 pacientes). Prevalencia global de IT moderada-grave no tratada 13,5%. Se asoció a mayor mortalidad total frente a IT nula-leve (HR 2,07; IC95% 1,89-2,26; P&lt;0,001), confirmado en modelos ajustados y subgrupos, con incremento escalonado por gravedad. También mayor mortalidad CV (HR 1,92) y hospitalización por IC (HR 1,63)."),
            ("Conclusiones.","La IT moderada-grave no tratada se asocia a mayor mortalidad total, CV y hospitalización por IC, subrayando el diagnóstico oportuno y el manejo adecuado.")]),
   dict(key="earlytavr",
     title="Age and Procedural Timing for Asymptomatic Severe Aortic Stenosis: Analysis From the EARLY TAVR Trial",
     ptype="Análisis de ECA", prio="Relevante", journal="Circ Cardiovasc Interv", doi="10.1161/CIRCINTERVENTIONS.125.016370",
     resumen="Análisis por edad de EARLY TAVR (estenosis aórtica severa asintomática). El beneficio relativo del TAVR precoz fue consistente en todos los grupos ≥65 años.",
     why="apoya considerar el TAVR precoz en toda la EAo severa asintomática a partir de los 65 años, sin penalización por edad.",
     modal=[("De qué va.","EARLY TAVR mostró que el TAVR precoz fue superior a la vigilancia clínica en EAo severa asintomática; se desconocía el efecto por edad. Se estratificó la población en 4 grupos: 65-69, 70-74, 75-79 y ≥80 años."),
            ("Resultados.","Sin interacción entre edad y efecto del TAVR precoz. Menor ictus con TAVR precoz en los más jóvenes (65-69: reducción absoluta 13%; P=0,008) y los más mayores (≥80: 12,3%; P=0,029). La mayor diferencia absoluta en hospitalización por IC a 2 años fue en ≥80 (9,1%). En vigilancia, ~un tercio de los jóvenes presentó síndrome valvular agudo al convertir a AVR."),
            ("Conclusiones.","El beneficio relativo del TAVR precoz fue consistente en todas las edades; la mayor reducción absoluta de ictus apareció en los grupos más joven y más mayor, sugiriendo considerar el TAVR precoz en todos los ≥65 años.")]),
   dict(key="claspiid",
     title="Impact of Residual Mitral Regurgitation and Gradient After M-TEER: 1-Year Outcomes From the CLASP IID Trial",
     ptype="Análisis de ECA", prio="Relevante", journal="JACC Cardiovasc Imaging", doi="10.1016/j.jcmg.2026.04.005",
     resumen="Análisis a 1 año del ECA CLASP IID (284 pacientes con M-TEER, sistema PASCAL). Un resultado óptimo (IM ≤1+ y gradiente ≤5 mmHg) se asoció a mayor libertad de eventos adversos mayores (89,5% vs 79,7%) y de mortalidad.",
     why="ante un resultado subóptimo, prima reducir la IM (≤1+) sobre preservar un gradiente bajo: optimizar la regurgitación pesa más que el gradiente.",
     modal=[("De qué va.","La reducción de la insuficiencia mitral (IM) en la reparación borde a borde transcatéter mitral (M-TEER) mejora los desenlaces, pero se equilibra con el ascenso del gradiente transmitral (MVG). Análisis a 1 año del ECA aleatorizado CLASP IID (sistema PASCAL) según la IM y el MVG al alta."),
            ("Resultados.","De 284 pacientes con eco al alta, el 72,5% (n=206) logró un resultado óptimo (IM ≤1+ y MVG ≤5 mmHg) y el 27,5% (n=78) uno subóptimo. Los de resultado óptimo tuvieron mejor flujo venoso pulmonar y TAPSE y mayor libertad de eventos adversos mayores (89,5% vs 79,7%; P=0,023), mortalidad (94,1% vs 85,4%; P=0,016) y del compuesto muerte/hospitalización por IC/reintervención (88,6% vs 78,7%; P=0,022) al año. Dentro del subóptimo, la libertad de eventos fue mayor con IM ≤1+ y MVG &gt;5 mmHg que con IM ≥2+ y MVG ≤5 mmHg (eventos adversos mayores: 87,7% vs 75,5%)."),
            ("Conclusiones.","Un resultado óptimo tras M-TEER se asoció a mejor hemodinámica y mayor libertad de eventos mayores, mortalidad y eventos compuestos al año. Ante un resultado subóptimo, lograr IM ≤1+ con MVG &gt;5 mmHg ofreció mejor pronóstico que IM ≥2+ con MVG ≤5 mmHg, sugiriendo que conviene optimizar la IM por encima de preservar un gradiente bajo.")]),
   dict(key="glsiao",
     title="Left Ventricular Global Longitudinal Strain Improves Risk Stratification in Chronic Aortic Regurgitation",
     ptype="Cohorte de imagen", prio="Complementario", journal="Eur Heart J Cardiovasc Imaging", doi="10.1093/ehjci/jeag135",
     resumen="Cohorte CMR (385 pacientes con IAo moderada-grave poco sintomáticos). El GLS por feature-tracking aportó valor pronóstico incremental sobre los parámetros de guía ESC/EACTS (corte 12%).",
     why="posiciona el GLS por RM como refinador del momento quirúrgico en la insuficiencia aórtica crónica.",
     modal=[("De qué va.","Evalúa el valor pronóstico del GLS del VI por feature-tracking de CMR en IAo crónica moderada-grave y su valor incremental sobre los parámetros de indicación quirúrgica ESC/EACTS 2025. Cohorte retrospectiva: 707 cribados, 385 poco o nada sintomáticos (NYHA I-II) como cohorte primaria. Primario: MACE."),
            ("Resultados.","En mediana de 52,9 meses, 45 pacientes tuvieron MACE. El FT-LVGLS se asoció de forma independiente con MACE (HR ajustado 1,210 por cada 1% de descenso del valor absoluto; P&lt;0,007). Incorporarlo a los modelos de guía mejoró la discriminación (C-index de 0,730-0,768 a 0,783-0,791). Un corte absoluto de GLS del 12% refinó la estratificación."),
            ("Conclusiones.","En pacientes NYHA I-II con IAo crónica moderada-grave, el FT-LVGLS aportó valor pronóstico incremental más allá de los parámetros de indicación quirúrgica basados en guía.")]),
 ]),
 (8,"Imagen cardíaca",[
   dict(key="tctavi",
     title="CT-Based Risk Stratification of Coronary Obstruction During TAVR: Clinical Utility and a New Volumetric Parameter (Leipzig TAVR Registry)",
     ptype="Estudio de imagen", prio="Relevante", journal="JACC Cardiovasc Interv", doi="10.1016/j.jcin.2026.04.015",
     resumen="Estudio prospectivo (164 pacientes) de un algoritmo de TC para riesgo de obstrucción coronaria en TAVR; un nuevo parámetro volumétrico (VTCV) predijo la obstrucción (AUC 0,841).",
     why="introduce un parámetro volumétrico TC que mejora la predicción de obstrucción coronaria sobre la distancia VTC clásica.",
     modal=[("De qué va.","La obstrucción coronaria (CO) en TAVR es rara pero potencialmente fatal. Estudio prospectivo: 164 pacientes en riesgo de CO; TC preprocedimiento para clasificar el riesgo con un algoritmo publicado y un nuevo parámetro volumétrico, valve-to-coronary volume (VTCV), en casos de alto riesgo. Endpoints VARC-3."),
            ("Resultados.","58,5% bajo riesgo, 24,4% intermedio, 17,1% alto. Protección coronaria en 12,8%, 52,8% y 93,9% respectivamente. Los 7 eventos de CO ocurrieron en el grupo de alto riesgo. La distancia VTC y el VTCV fueron menores en CO; el VTCV predijo CO de forma independiente (AUC 0,841; P&lt;0,001), superando a la distancia VTC, validado en una cohorte externa de 11 centros europeos."),
            ("Conclusiones.","El algoritmo de TC estratifica en 3 categorías de riesgo; aunque la protección coronaria reduce el riesgo de CO, su eficacia es limitada en pacientes con VTCV muy pequeño, predecible por TC preprocedimiento.")]),
   dict(key="mfr",
     title="Incremental Prognostic Value of Subendocardial Myocardial Flow Reserve in Patients With Normal Perfusion",
     ptype="Investigación original (PET)", prio="Relevante", journal="Circulation", doi="10.1161/CIRCULATIONAHA.125.078816",
     resumen="Registro PET multicéntrico (6.603 pacientes con perfusión normal). Una reserva de flujo subendocárdica baja (discordante) se asoció a más MACE (HR 1,41) pese a flujo transmural preservado.",
     why="añade información de riesgo «oculta» en pacientes con perfusión PET normal, refinando la estratificación.",
     modal=[("De qué va.","La utilidad pronóstica de la MFR por PET está establecida, pero el valor incremental de la MFR subendocárdica sobre la transmural era incierto. Pacientes de un registro PET multicéntrico con perfusión normal en Rb-82; 3 grupos: concordante-normal, discordante (subendocárdica baja, MFR normal) y MFR anormal."),
            ("Resultados.","6.603 pacientes (edad 66,3 años; 54% mujeres). Los discordantes con MFR subendocárdica baja eran mayores y con más comorbilidad. En mediana de 4,9 años, 1.661 MACE. Los discordantes tuvieron más MACE (HR 1,41; IC95% 1,22-1,64) y mortalidad total (HR 1,36) que los concordantes-normal."),
            ("Conclusiones.","La MFR subendocárdica revela heterogeneidad de riesgo clínicamente significativa entre pacientes con reserva de flujo transmural preservada, refinando la estratificación más allá de las métricas PET tradicionales.")]),
   dict(key="itph",
     title="Prognostic Value of Tricuspid Regurgitation in Pulmonary Hypertension and Among the Different WHO Groups",
     ptype="Observacional de imagen", prio="Complementario", journal="JACC Cardiovasc Imaging", doi="10.1016/j.jcmg.2026.04.016",
     resumen="Cohorte de imagen (1.318 pacientes con HP). La IT secundaria moderada-grave se asoció a mortalidad independiente de la disfunción del VD, en todos los grupos WHO.",
     why="sugiere que la IT podría ser un objetivo terapéutico adicional en subgrupos de HP, más allá de la disfunción del VD.",
     modal=[("De qué va.","Evalúa el valor pronóstico de la IT secundaria en HP no relacionada con valvulopatía izquierda ni FEr, y por grupos WHO. Pacientes con presión sistólica del VD ≥50 mmHg (2010-2023) con strain de pared libre del VD medido; seguimiento por mortalidad total."),
            ("Resultados.","1.318 pacientes (67 años; 61% mujeres; 29% con IT moderada o mayor); WHO 1/2/3/4 en 33%/11%/32%/12%. En mediana de 1,5 años, 454 muertes. La IT moderada-grave se asoció a mortalidad independiente de medidas de función del VD o acoplamiento VD-arteria pulmonar, en todos los grupos WHO."),
            ("Conclusiones.","La IT moderada-grave confiere riesgo de mortalidad en HP (sin valvulopatía izquierda ni FEr), más allá de la disfunción del VD; si puede ser objetivo terapéutico en subgrupos requiere investigación futura.")]),
   dict(key="aselap",
     title="Comparison of the 2016 ASE/EACVI and 2025 ASE Guidelines for Assessing Left Atrial Pressure in Patients with Normal Left Ventricular Ejection Fraction",
     ptype="Estudio diagnóstico (validación prospectiva)", prio="Complementario", journal="Eur Heart J Cardiovasc Imaging", doi="10.1093/ehjci/jeag134",
     resumen="Estudio prospectivo de validación (119 pacientes con FEVI normal y medición invasiva de presión auricular izquierda) que compara las guías ASE 2025 frente a las ASE/EACVI 2016. Las 2025 mejoraron sensibilidad (86,4% vs 54,0%) y factibilidad (100% vs 78,1%), con menor especificidad (81,8% vs 94,8%).",
     why="primera validación frente a presión auricular invasiva del nuevo algoritmo diastólico ASE 2025, que detecta más presión elevada manteniendo la precisión global.",
     modal=[("De qué va.","Estudio prospectivo que evalúa el rendimiento diagnóstico de las guías ASE 2025 para la estimación de la presión auricular izquierda (PAI) y lo compara con el de las guías ASE/EACVI 2016, en pacientes con FEVI normal. Se recogieron datos ecocardiográficos y mediciones invasivas de PAI en 119 pacientes, clasificados en PAI elevada (&gt;15 mmHg) y normal (≤15 mmHg)."),
            ("Resultados.","Las guías 2025 mostraron una sensibilidad significativamente mayor (86,4% vs 54,0%) y mayor factibilidad (100% vs 78,1%), pero menor especificidad (81,8% vs 94,8%) frente a las guías 2016. El valor predictivo negativo y la precisión global mejoraron de forma modesta."),
            ("Conclusiones.","Las guías ASE 2025 mejoraron de forma significativa la factibilidad de la evaluación de la PAI y la tasa de detección de PAI elevada, manteniendo una precisión comparable.")]),
   dict(key="taaimg",
     title="Beyond diameter: emerging imaging biomarkers for risk stratification in thoracic aortic aneurysms",
     ptype="Revisión", prio="Complementario", journal="Heart", doi="10.1136/heartjnl-2025-327480",
     resumen="Revisión sobre biomarcadores de imagen más allá del diámetro absoluto para estratificar el riesgo en el aneurisma de aorta torácica, donde muchas disecciones ocurren por debajo del umbral quirúrgico, sobre todo en mujeres.",
     why="propone una imagen aórtica de precisión e informada por sexo (métricas indexadas, geometría, biomecánica, 4D-flow) frente al diámetro aislado.",
     modal=[("De qué va.","Revisión que sintetiza la evidencia sobre biomarcadores de imagen para estratificar el riesgo en el aneurisma de aorta torácica (AAT), una entidad frecuente, infradiagnosticada y potencialmente letal cuyo manejo sigue anclado en el diámetro absoluto pese a que muchas disecciones ocurren por debajo de los umbrales quirúrgicos, particularmente en mujeres."),
            ("Resultados.","Revisa métricas indexadas (Aortic Size Index, Aortic Height Index, área aórtica indexada) que ajustan por hábito corporal; descriptores morfológicos (longitud ascendente, tortuosidad del arco, volumen aórtico); medidas dinámicas y biomecánicas (tasa de crecimiento, deformación regional, distensibilidad/rigidez) y modalidades avanzadas (RM de flujo 4D, mapeo de deformación). Marcadores funcionales (presión central, rigidez aórtica, edad arterial) predicen la expansión de forma independiente y mejoran la estratificación al combinarse con el diámetro."),
            ("Conclusiones.","El diámetro aislado es insuficiente; las prioridades futuras incluyen validación multicéntrica prospectiva, umbrales específicos por sexo y un abordaje multidisciplinar para una vigilancia personalizada.")]),
 ]),
 (9,"Cardiología intervencionista y estructural",[
   dict(key="fetalav",
     title="Technical Success of Fetal Aortic Valvuloplasty in Relation to Center Volumes: A Report From the International Fetal Cardiac Intervention Registry",
     ptype="Registro internacional", prio="Relevante", journal="Circ Cardiovasc Interv", doi="10.1161/CIRCINTERVENTIONS.125.015593",
     resumen="Registro internacional (162 valvuloplastias aórticas fetales, 11 centros). Éxito técnico del 80,2%; el mayor volumen no mejoró el éxito pero sí redujo las muertes fetales periprocedimiento.",
     why="informa el debate sobre regionalización de la intervención cardiaca fetal: el volumen importa para la supervivencia, no tanto para el éxito técnico.",
     modal=[("De qué va.","Se examina la relación entre el volumen del centro de valvuloplastia aórtica fetal y los resultados usando el International Fetal Cardiac Intervention Registry. Centros con ≥3 procedimientos (2001-2018). Primario: éxito técnico."),
            ("Resultados.","11 centros (6-31 casos) realizaron 162 valvuloplastias con éxito técnico del 80,2%. Mayor volumen no se asoció a mejor éxito ni menos complicaciones, pero sí a menos muertes fetales periprocedimiento. Los mayores determinantes fueron el peso fetal estimado y la edad gestacional; una sola punción cardiaca se asoció a mayor éxito y menos complicaciones."),
            ("Conclusiones.","Los centros de mayor volumen no tuvieron mayor éxito técnico ni menos complicaciones, pero sí menos muertes fetales periprocedimiento; la edad gestacional y el número de punciones influyeron en los resultados.")]),
   dict(key="avlm",
     title="Aortic Valve Leaflet Modification: A Working Group Position Statement on Best Practices and Step-by-Step Guide",
     ptype="Documento de posición", prio="Relevante", journal="JACC Cardiovasc Interv", doi="10.1016/j.jcin.2026.03.033",
     resumen="Documento de posición internacional con mejores prácticas y guía paso a paso de BASILICA y técnicas de modificación de velos para prevenir obstrucción coronaria en TAVR.",
     why="estandariza una técnica (BASILICA) infrautilizada por su complejidad percibida, clave para prevenir obstrucción coronaria.",
     modal=[("De qué va.","La obstrucción coronaria es una complicación potencialmente letal del TAVR (nativo, valve-in-valve y redo-TAVR), identificable en TC; BASILICA la previene eficazmente pero su adopción está limitada. El documento sintetiza la experiencia internacional para dar guía contemporánea de BASILICA y técnicas relacionadas."),
            ("Resultados.","Revisión del estado del arte: principios de electrocirugía transcatéter; análisis del riesgo y planificación por TC; guía paso a paso de BASILICA electroquirúrgica; trucos para retos infrecuentes; escenarios donde BASILICA no funcionará; y técnicas variantes."),
            ("Conclusiones.","Estas mejores prácticas contemporáneas pueden ayudar a los operadores a adquirir o mantener competencia en la modificación de velos.")]),
   dict(key="eurobasilica",
     title="Leaflet Splitting to Prevent TAVR-Induced Coronary Obstruction in Stented vs Stentless Surgical Bioprosthetic Valves (EURO-BASILICA)",
     ptype="Estudio técnico (registro)", prio="Relevante", journal="JACC Cardiovasc Interv", doi="10.1016/j.jcin.2026.01.312",
     resumen="Registro EURO-BASILICA (131 pacientes). Las prótesis stentless tuvieron más obstrucción coronaria relacionada con el velo diana tras BASILICA (44,4% vs 7,1%), mayormente parcial.",
     why="identifica las prótesis stentless como un escenario de mayor riesgo residual de obstrucción tras BASILICA, que puede requerir protección adicional.",
     modal=[("De qué va.","El leaflet splitting electroquirúrgico previene la obstrucción coronaria tras TAVR, sobre todo en valve-in-valve, pero faltan datos comparativos entre prótesis con y sin stent. 131 pacientes con BASILICA y valve-in-valve TAVR del registro multicéntrico EURO-BASILICA, con desenlaces VARC-3."),
            ("Resultados.","115 (87,8%) stented y 16 (12,2%) stentless. Las stentless tenían velos más largos y requirieron más contraste y fluoroscopia. Éxito técnico similar, pero las stentless tuvieron más obstrucción coronaria del velo diana (44,4% vs 7,1%; P&lt;0,001), mayormente parcial y no limitante de flujo. Sin obstrucción tardía ni IAM al año."),
            ("Conclusiones.","BASILICA es factible en válvulas stented y stentless, pero las stentless tuvieron mayor tasa de obstrucción parcial y pueden requerir protección coronaria adicional o alternativa en pacientes seleccionados.")]),
   dict(key="halt",
     title="Impact of Leaflet Modification on the Occurrence of Hypoattenuated Leaflet Thickening After Valve-in-Valve Transcatheter Aortic Valve Replacement",
     ptype="Estudio técnico", prio="Relevante", journal="JACC Cardiovasc Interv", doi="10.1016/j.jcin.2026.01.313",
     resumen="Análisis retrospectivo (141 pacientes ViV-TAVR). La modificación de velos se asoció a menos HALT (19,7% vs 40%) y menores gradientes residuales.",
     why="sugiere un beneficio hemodinámico de la modificación de velos más allá de la prevención de obstrucción coronaria.",
     modal=[("De qué va.","El ViV-TAVR conlleva riesgo de obstrucción coronaria y de trombosis subclínica (HALT en TC). Se evaluó la asociación entre modificación intencional de velos y la incidencia de HALT en 141 pacientes ViV-TAVR con TC posprocedimiento (61 con modificación, 80 sin ella)."),
            ("Resultados.","La modificación fue más frecuente en mujeres y prótesis pequeñas ≤21 mm. Los modificados tuvieron menores gradientes medios (13±6 vs 18±9 mmHg; P&lt;0,001) y menos HALT (19,7% vs 40%; P&lt;0,01), persistiendo en válvulas autoexpandibles. Sin HALT en modificación de doble velo."),
            ("Conclusiones.","En ViV-TAVR, la modificación intencional de velos se asocia a menos HALT, sugiriendo una asociación protectora con la trombosis subclínica y un posible beneficio hemodinámico más allá de la prevención de obstrucción coronaria.")]),
   dict(key="algvelos",
     title="Current Evidence, Emerging Evidence, and Decision-Making: An Algorithm for Leaflet Modification Procedures",
     ptype="Revisión", prio="Relevante", journal="JACC Cardiovasc Interv", doi="10.1016/j.jcin.2026.04.023",
     resumen="Revisión con algoritmos sistemáticos de modificación de velos aórticos y mitrales para guiar al operador estructural según anatomía, patología y objetivos.",
     why="ofrece un marco de decisión práctico para elegir entre técnicas de modificación de velos (splitting vs intraleaflet).",
     modal=[("De qué va.","La modificación de velos es un elemento necesario del intervencionismo estructural. La revisión propone algoritmos sistemáticos para los procedimientos de modificación de velos aórticos y mitrales."),
            ("Resultados.","Aunque el leaflet splitting está probado, tiene limitaciones en casos extremos; las técnicas intraleaflet emergen con mayor aplicabilidad potencial pero persisten preocupaciones de seguridad. Los algoritmos guían la selección del abordaje según anatomía, patología y objetivos."),
            ("Conclusiones.","Los algoritmos propuestos sirven de guía a los operadores estructurales para seleccionar el abordaje apropiado en la modificación de velos.")]),
 ]),
 (10,"Arritmias y electrofisiología",[
   dict(key="option",
     title="Outcomes of left atrial appendage closure versus oral anticoagulation after catheter ablation among patients with higher and lower stroke risk: A sub-analysis of the OPTION clinical trial",
     ptype="Subanálisis de ECA", prio="Relevante", journal="Heart Rhythm", doi="10.1016/j.hrthm.2026.05.057",
     resumen="Subanálisis de OPTION (1.600 pacientes tras ablación de FA). El cierre de orejuela igualó la eficacia de la ACO en alto y bajo riesgo y redujo el sangrado en ambos.",
     why="apoya el LAAC tras ablación de FA con menos sangrado que la ACO, con riesgo de ictus bajo incluso en CHA₂DS₂-VASc ≤3.",
     modal=[("De qué va.","OPTION mostró que, tras ablación de FA, el cierre de orejuela (LAAC) reduce el sangrado no procedimental y es no inferior a la ACO en muerte/ictus/embolia. Se evaluaron las tasas de eventos según el riesgo basal, estratificando por CHA₂DS₂-VASc ≥4 vs ≤3."),
            ("Resultados.","1.600 pacientes (70±8 años; 738 con CHA₂DS₂-VASc ≥4 y 862 con ≤3). La eficacia fue similar entre ACO y LAAC con ≥4 (9,4% vs 7,8%) y con ≤3 (2,7% vs 3,3%). Con ≤3, el riesgo anual de ictus isquémico fue 0,3% (LAAC) y 0,1% (ACO). El sangrado fue más frecuente con ACO con ≥4 (18,4% vs 11,5%) y con ≤3 (17,9% vs 6,0%)."),
            ("Conclusiones.","Tras ablación de FA, los eventos CV son bajos en CHA₂DS₂-VASc ≤3 con LAAC o ACO; el riesgo de sangrado con ACO es similar en alto y bajo riesgo y significativamente menor con LAAC en ambos.")]),
   dict(key="smartbeats",
     title="Precardioversion Heart Rhythm Monitoring Using Smartphone Photoplethysmography: The SMARTBEATS Randomized Clinical Trial",
     ptype="Ensayo clínico aleatorizado", prio="Relevante", journal="JAMA Cardiol", doi="10.1001/jamacardio.2026.1269",
     resumen="ECA (206 pacientes) de monitorización pre-cardioversión con fotopletismografía por smartphone. Redujo las cancelaciones el mismo día (4,8% vs 23,2%).",
     why="intervención digital escalable que reduce drásticamente cancelaciones de cardioversión por reversión espontánea.",
     modal=[("De qué va.","La cardioversión programada consume recursos; las cancelaciones por reversión espontánea a ritmo sinusal son comunes. ECA simple ciego en un hospital terciario sueco: adultos con FA/flutter persistente programados para cardioversión; monitorización ambulatoria pre-cardioversión con fotopletismografía por smartphone y recordatorios de adherencia vs estándar."),
            ("Resultados.","206 aleatorizados (104 intervención, 99 control). Cancelaciones el mismo día: 4,8% (5/104) vs 23,2% (23/99) (P&lt;0,001). Por reversión espontánea a sinusal: 1,0% vs 18,2% (P&lt;0,001)."),
            ("Conclusiones.","La monitorización pre-cardioversión con fotopletismografía por smartphone es una intervención digital altamente escalable que redujo significativamente las cancelaciones el mismo día.")]),
   dict(key="persepolis",
     title="Pulmonary Vein and Posterior Wall Isolation Using the Circular Multielectrode Catheter for Treatment of Atrial Fibrillation: Acute and Long-Term Outcomes (PERSEPOLIS Trial)",
     ptype="Ensayo (agudo / largo plazo)", prio="Relevante", journal="Heart Rhythm", doi="10.1016/j.hrthm.2026.06.002",
     resumen="Análisis de 178 pacientes con PVI±PWI usando PFA multielectrodo circular (PulseSelect). PVI agudo 100%; libertad de arritmia al año 81,6% (paroxística) y 66,6% (persistente).",
     why="datos de mundo real de eficacia y seguridad de un sistema PFA circular, con tiempos de procedimiento cortos.",
     modal=[("De qué va.","Faltan datos de mundo real de la ablación de FA con el sistema PFA multielectrodo circular (PulseSelect). Análisis retrospectivo de pacientes consecutivos con FA paroxística/persistente sintomática sometidos a PVI o PVI+PWI; desenlaces procedimentales, seguridad, biomarcadores renales y recurrencia."),
            ("Resultados.","178 pacientes (69±11 años; 62% varones; 61% paroxística), procedimiento 66±11 min. PVI agudo 100%; 96,6% recibió PVI+PWI. 4 eventos adversos (2,2%; 2 menores). Aumento transitorio de bilirrubina y un caso de IRA estadio 1, resueltos en 48-72 h. Libertad de recurrencia al año: 81,6% (paroxística) y 66,6% (persistente)."),
            ("Conclusiones.","La PVI con/sin PWI mediante PFA multielectrodo circular es segura, factible y eficaz en FA paroxística y persistente sintomática, con bajo riesgo de complicaciones, incluida la hemólisis.")]),
   dict(key="camera2",
     title="CA in AF With LVSD With and Without LV Fibrosis: Results From the CAMERA-MRI II Trial",
     ptype="Ensayo", prio="Relevante", journal="JACC Clin Electrophysiol", doi="10.1016/j.jacep.2026.04.028",
     resumen="Análisis del ECA CAMERA-MRI II (80 pacientes con FA y disfunción del VI). La ablación mejoró la FEVI con y sin fibrosis (+20,3% vs +21,7%), aunque la normalización fue menor con LGE.",
     why="apoya la ablación en FA con disfunción del VI incluso con fibrosis, modulando expectativas según la carga de cicatriz.",
     modal=[("De qué va.","La ablación mejora desenlaces en FA con disfunción sistólica del VI (LVSD), pero la influencia de la fibrosis del VI era incierta. Pacientes de CAMERA-MRI II clasificados como LGE positivo (≥5%) o negativo (&lt;5%), todos ablacionados; desenlaces a 12 meses."),
            ("Resultados.","80 pacientes (40 LGE+, 40 LGE-). Mejora sustancial de FEVI en ambos (+20,3±11,0% vs +21,7±11,8%; P=0,578). FEVI a 12 meses menor en LGE+ (49,1% vs 54,5%; P=0,019), pero tras ajuste el LGE no se asoció de forma independiente. Menor normalización en LGE+ (52% vs 82%; P=0,004); una carga de LGE &gt;20% se asoció a recuperación atenuada."),
            ("Conclusiones.","En FA con LVSD, la ablación se asocia a mejora sustancial de la función sistólica con independencia del LGE; la FEVI absoluta y la normalización son menores en LGE+, y una mayor carga de cicatriz modula la magnitud de la recuperación.")]),
   dict(key="sentinel",
     title="Impact of Adjunctive Posterior Left Atrial Ablation using Pulsed Field Ablation on Healthcare Utilization in Patients Undergoing First-time Catheter Ablation for Atrial Fibrillation (SENTINEL Registry)",
     ptype="Registro multicéntrico", prio="Complementario", journal="Heart Rhythm", doi="10.1016/j.hrthm.2026.05.053",
     resumen="Registro SENTINEL (1.611 pacientes). Añadir ablación de pared posterior (PLAA) con PFA redujo la utilización de recursos sanitarios (HR ajustado 0,52) sin más eventos adversos.",
     why="sugiere que la PLAA adjunta con PFA reduce rehospitalizaciones/recurrencias en la primera ablación de FA, sin penalizar seguridad.",
     modal=[("De qué va.","Hay pocos datos de mundo real de la PLAA adjunta con PFA pese a su rápida adopción. Análisis retrospectivo del registro Australia-Nueva Zelanda (sistema Farapulse) en primera ablación; primario: utilización sanitaria (rehospitalización por arritmias, cardioversión y/o reablación)."),
            ("Resultados.","De 1.611 pacientes, 30% recibió PLAA adjunta; eran mayores, con más FA no paroxística. Sin diferencia en eventos adversos a 30 días (0,8% vs 0,5%). Tras ajuste, la utilización sanitaria fue menor con PVI+PLAA (HR 0,52; IC95% 0,31-0,89; P=0,016); resultado mantenido tras emparejamiento por propensión (HR 0,57)."),
            ("Conclusiones.","En el mayor análisis comparativo de PLAA+PVI vs PVI con PFA hasta la fecha, la PLAA adjunta fue segura y se asoció a menor utilización de recursos en la primera ablación de FA.")]),
 ]),
]

# Destacado + Top3 reference existing article keys
DESTACADO_KEY = "ckm"
TOP3 = ["infinity","findckd","logical"]

# ---- reevaluación exhaustiva (jun 2026): bajas y altas por sección ----
_DROP = {'taaimg', 'mk7', 'tncronica', 'estatinas', 'synchmasld', 'takotsubo', 'complete', 'c2d', 'persepolis'}
_NEW = [{'key': 'smartreach2', 'sec': 1, 'title': 'Predicting lifetime cardiovascular risk and benefits of preventive treatment in established ASCVD: the SMART-REACH2 model', 'ptype': 'Desarrollo y validación de modelo de predicción', 'prio': 'Relevante', 'journal': 'Eur Heart J', 'doi': '10.1093/eurheartj/ehag400', 'resumen': 'Desarrollo y validación del modelo SMART-REACH2 para estimar el riesgo de eventos CV recurrentes de por vida y el beneficio del tratamiento preventivo en enfermedad aterosclerótica establecida, recalibrado por regiones de riesgo.', 'why': 'actualiza la herramienta recomendada por las guías ESC para la decisión compartida en prevención secundaria, con recalibración geográfica y por sexo.', 'modal': [['De qué va.', 'Las guías ESC 2021 recomiendan el modelo SMART-REACH en enfermedad aterosclerótica establecida. Se desarrolló SMART-REACH2 en 8.708 personas de 40-90 años con enfermedad coronaria, cerebrovascular, arterial periférica o aneurisma de aorta abdominal (cohorte UCC-SMART), con modelos de Cox específicos por causa y sexo, recalibrado a las regiones de riesgo europeas y globales.'], ['Resultados.', 'En la derivación hubo 2.057 eventos CV recurrentes (mediana 8,5 años). En la validación externa (2.085.780 pacientes de 54 países) ocurrieron 307.706 eventos. El estadístico C combinado fue 0,68 (IC95% 0,66-0,69), de 0,66 en la región europea de bajo riesgo a 0,72 en Latinoamérica, con calibración adecuada. Para un paciente de 50 años, la ganancia estimada de esperanza de vida libre de ECV con tratamiento intensivo (−15 mmHg de PAS y −1,0 mmol/L de cLDL) osciló entre 2 años (bajo riesgo) y 4,4 años (muy alto riesgo).'], ['Conclusiones.', 'SMART-REACH2 estima el riesgo a corto y largo plazo de eventos CV recurrentes y el beneficio del tratamiento teniendo en cuenta variaciones geográficas y por sexo, facilitando la decisión compartida que recomiendan las guías.']], '_total': 7.0}, {'key': 'mgfr', 'sec': 1, 'title': 'Measured and Estimated Glomerular Filtration Rates and Risk of Adverse Health Outcomes', 'ptype': 'Cohorte observacional', 'prio': 'Relevante', 'journal': 'JAMA', 'doi': '10.1001/jama.2026.9639', 'resumen': 'Cohorte de 6.174 adultos (Estocolmo) con FG medido por aclaramiento de iohexol: un FGm de 60 frente a 90 ml/min/1,73 m² se asoció a más mortalidad (HR 1,21) y fracaso renal (HR 2,85), validando el umbral de 60.', 'why': 'respalda el umbral de FG de 60 ml/min/1,73 m² para definir ERC y muestra que la ecuación creatinina-cistatina C es la que mejor refleja el riesgo de mortalidad.', 'modal': [['De qué va.', 'Un FGe bajo se asocia a más eventos, pero la relación del FG medido (FGm) con los desenlaces es incierta. Cohorte observacional retrospectiva de 6.174 adultos de Estocolmo (2011-2021) con FGm por aclaramiento plasmático de iohexol; se compararon FGm y FGe (creatinina, cistatina C o ambas, CKD-EPI). Desenlaces: mortalidad por cualquier causa y fracaso renal con tratamiento sustitutivo.'], ['Resultados.', 'De 6.174 participantes (mediana 59 años; 60% varones), 1.977 (32%) murieron y 426 (6,9%) desarrollaron fracaso renal (mediana 5,9 años). Frente a un FGm de 90, un FGm de 60 ml/min/1,73 m² se asoció a más mortalidad (27,6 vs 22,4 por 1.000 personas-año; HR 1,21; IC95% 1,14-1,28) y más fracaso renal (HR 2,85; IC95% 2,06-3,94). La asociación con mortalidad del FGe creatinina-cistatina C no difirió de la del FGm (RHR 1,03); el FGe-creatinina la infraestimó (0,87) y el FGe-cistatina la sobreestimó (1,17).'], ['Conclusiones.', 'Un FGm de 60 ml/min/1,73 m² se asocia a mayor mortalidad y fracaso renal frente a 90, lo que apoya el umbral actual de 60 para definir ERC; la ecuación creatinina-cistatina C es la que mejor representa el riesgo de mortalidad.']], '_total': 6.27}, {'key': 'flowckd', 'sec': 2, 'title': 'Kidney and Survival Benefits of Semaglutide in Diabetes With CKD: FLOW Trial Cardiovascular Subgroup Analyses', 'ptype': 'Subanálisis de ECA (FLOW)', 'prio': 'Relevante', 'journal': 'J Am Coll Cardiol', 'doi': '10.1016/j.jacc.2026.02.5125', 'resumen': 'Subanálisis del FLOW (semaglutida 1,0 mg/sem en DM2 con ERC) por estado CV basal: redujo el desenlace renal compuesto y la mortalidad con o sin ECV aterosclerótica, IC o alto riesgo CV (HR 0,74-0,82).', 'why': 'confirma que el beneficio renal y de supervivencia de la semaglutida en ERC con diabetes es consistente exista o no enfermedad CV previa, ampliando a quién tratar.', 'modal': [['De qué va.', 'La ECV aumenta el riesgo de progresión de ERC y de muerte en la DM2. Subanálisis del FLOW (semaglutida 1,0 mg semanal s.c. vs placebo en DM2 con ERC) según ECV aterosclerótica, insuficiencia cardíaca o alto riesgo CV total (PREVENT a 10 años ≥20%). Desenlace primario: descenso del FGe ≥50%, FGe inferior a 15, diálisis/trasplante o muerte renal o CV; secundario confirmatorio: muerte por cualquier causa.'], ['Resultados.', 'De los participantes, 1.198 (33,9%) tenían ECV aterosclerótica, 678 (19,2%) insuficiencia cardíaca y 1.329 (66,5%) alto riesgo CV sin ECV establecida. La semaglutida redujo el desenlace primario con o sin ECV aterosclerótica (HR 0,80 y 0,74), con o sin IC (HR 0,67 y 0,79) y con o sin alto riesgo CV (HR 0,73 y 0,73); interacciones no significativas. NNT a 3 años: 22 (ECV), 13 (IC) y 17 (PREVENT≥20%). También redujo la mortalidad por cualquier causa de forma consistente entre subgrupos.'], ['Conclusiones.', 'La semaglutida mejoró los desenlaces renales y de supervivencia en DM2 con ERC, con independencia de ECV aterosclerótica, insuficiencia cardíaca o alto riesgo CV total establecido.']], '_total': 6.83}, {'key': 'logical', 'sec': 4, 'title': 'Conservative Oxygen for Unresponsive Patients after Cardiac Arrest (LOGICAL)', 'ptype': 'Ensayo clínico aleatorizado', 'prio': 'Relevante', 'journal': 'N Engl J Med', 'doi': '10.1056/NEJMoa2513814', 'resumen': 'ECA (1.840 adultos) de oxígeno conservador frente a liberal en ventilación mecánica tras parada cardíaca: sin diferencias en supervivencia con buen resultado funcional a 180 días (38,2% vs 39,7%; RR 0,97).', 'why': 'ensayo neutro que no respalda limitar el oxígeno tras la parada cardíaca: la oxigenación conservadora no mejora el pronóstico funcional frente a la liberal.', 'modal': [['De qué va.', 'Limitar el oxígeno tras la reanimación podría mejorar la supervivencia funcional. ECA en adultos no respondedores con ventilación mecánica en UCI tras parada cardíaca: grupo conservador (alarma de SpO₂ superior al 95%, FiO₂ reducible a 0,21) frente a liberal (sin límite superior, FiO₂ mínima 0,3); límite inferior de SpO₂ del 90% en ambos. Primario: supervivencia con resultado funcional favorable a 180 días (GOS-E ≥5).'], ['Resultados.', '1.840 pacientes de 53 UCI de Australia, Nueva Zelanda e Irlanda (882 conservador, 958 liberal). Resultado funcional favorable a 180 días en el 38,2% (313/819) con oxígeno conservador frente al 39,7% (353/890) con liberal (RR 0,97; IC95% 0,87-1,09; P=0,65). No se notificaron eventos adversos.'], ['Conclusiones.', 'En adultos no respondedores ventilados en UCI tras una parada cardíaca, el oxígeno conservador no aumentó la supervivencia con buen resultado funcional frente al oxígeno liberal.']], '_total': 7.79}, {'key': 'secprev', 'sec': 4, 'title': 'Socioeconomic Differences in Patient Pathways of Secondary Prevention after Ischaemic Heart Disease: A Nationwide Cohort Study', 'ptype': 'Cohorte poblacional', 'prio': 'Relevante', 'journal': 'Eur J Prev Cardiol', 'doi': '10.1093/eurjpc/zwag309', 'resumen': 'Cohorte nacional (93.159 pacientes con cardiopatía isquémica): solo el 25,9% recibió los 3 componentes de prevención secundaria; renta baja (RR 0,70), vivir solo (0,77) y desempleo (0,82) reducen el acceso.', 'why': 'cuantifica la enorme brecha socioeconómica en la prevención secundaria tras cardiopatía isquémica, incluso en un sistema sanitario universal.', 'modal': [['De qué va.', 'Las diferencias socioeconómicas en prevención secundaria tras cardiopatía isquémica (CI) están poco estudiadas, sobre todo en la transición del hospital a primaria. Cohorte retrospectiva nacional de 93.159 personas hospitalizadas por CI (2016-2022); se midió rehabilitación cardíaca, antiagregante y estatina dispensados, seguimiento anual en primaria y un indicador de los 3 componentes; RR por regresión de Poisson modificada.'], ['Resultados.', 'A los 6 meses, el 41,2% inició rehabilitación cardíaca (73,7% adherente); el 86,1% retiró antiagregante, el 77,0% estatina y el 56,0% acudió a revisión anual. Solo el 25,9% logró los tres componentes. La probabilidad de recibir los tres fue menor con educación baja (RR 0,91), vivir solo (0,77), renta baja (0,70) y desempleo (0,82); la mayor brecha fue en rehabilitación cardíaca. El 7,6% no recibió ninguno.'], ['Conclusiones.', 'Persisten diferencias socioeconómicas sustanciales en la prevención secundaria tras cardiopatía isquémica pese a un sistema universal, lo que exige estrategias equitativas e intersectoriales en los puntos de transición asistencial.']], '_total': 5.7}, {'key': 'defineht', 'sec': 5, 'title': 'Donor-Derived Cell-Free DNA as a Prognostic Biomarker After Heart Transplantation: The DEFINE-HT Study', 'ptype': 'Estudio observacional prospectivo (DEFINE-HT)', 'prio': 'Relevante', 'journal': 'JACC Heart Fail', 'doi': '10.1016/j.jchf.2026.103152', 'resumen': 'Estudio prospectivo (110 receptores de trasplante cardíaco): el ADN libre derivado del donante (dd-cfDNA) por encima del umbral multiplicó por 4,4 el riesgo del desenlace compuesto (rechazo tratado, disfunción del injerto, retrasplante o muerte) a 1 año.', 'why': 'apoya el dd-cfDNA como biomarcador no invasivo pronóstico tras el trasplante cardíaco, hacia sustituir parte de las biopsias endomiocárdicas.', 'modal': [['De qué va.', 'El dd-cfDNA es un biomarcador no invasivo de rechazo agudo en el trasplante cardíaco, pero su valor pronóstico más allá de la histología es incierto. DEFINE-HT, estudio prospectivo observacional en 10 centros de EE. UU., siguió a receptores adultos 1 año; se extrajo sangre para dd-cfDNA (Prospera Heart) independientemente de la decisión clínica. Desenlace compuesto: rechazo tratado, disfunción del injerto, retrasplante o muerte al año.'], ['Resultados.', 'De 110 pacientes (mediana 55 años; 25,5% mujeres), 38 (34,5%) alcanzaron el desenlace compuesto: rechazo tratado 20%, disfunción del injerto 10,9%, muerte 3,6%. Solo el 4,6% de las biopsias mostró rechazo y el 90% de los dd-cfDNA estaban por debajo del umbral. El dd-cfDNA% y el DQS fueron mayores en el rechazo tratado (0,23% vs 0,085%; P=0,045). Cada aumento de 1 DE intrapaciente se asoció a un 19% y 12% más de riesgo (P&lt;0,001); los valores por encima del umbral multiplicaron por 4,42 el riesgo del compuesto (P&lt;0,001).'], ['Conclusiones.', 'DEFINE-HT respalda el papel del dd-cfDNA como biomarcador pronóstico de la salud del injerto e informa un ensayo aleatorizado que compare la monitorización por dd-cfDNA frente a la biopsia.']], '_total': 5.15}, {'key': 'cyanotic', 'sec': 6, 'title': 'Survivors of Cyanotic Congenital Heart Disease: A Review', 'ptype': 'Revisión', 'prio': 'Complementario', 'journal': 'JAMA', 'doi': '10.1001/jama.2026.8806', 'resumen': 'Revisión JAMA sobre los supervivientes adultos de cardiopatías congénitas cianóticas (tetralogía de Fallot, transposición de grandes arterias y ventrículo único), su supervivencia con cirugía y sus complicaciones tardías.', 'why': 'orienta al cardiólogo general sobre el seguimiento de una población creciente de adultos con cardiopatía congénita cianótica reparada y sus riesgos (arritmias, disfunción ventricular, muerte súbita).', 'modal': [['De qué va.', 'Las cardiopatías congénitas cianóticas afectan a ~0,2% de los nacidos vivos; con la cirugía actual la supervivencia a la edad adulta es habitual. Revisión sobre las tres entidades que suponen ~80%: tetralogía de Fallot (TOF), transposición de grandes arterias en D (D-TGA) y ventrículo único.'], ['Resultados.', 'El 90% de los pacientes con TOF sobrevive más de 30 años tras la cirugía; casi todos desarrollan sobrecarga de volumen del ventrículo derecho por insuficiencia pulmonar, y un 20-45% presenta taquiarritmias auriculares hacia los 45 años. En la D-TGA, el switch arterial logra supervivencias del 93-97% a los 30 años; tras switch auricular, un 30-50% desarrolla disfunción del ventrículo derecho a los 25 años y hasta un 15% sufre muerte súbita (media 30-35 años). Tras Fontan por ventrículo único, la supervivencia es del 50-80% a los 40-50 años.'], ['Conclusiones.', 'Con cirugía, la supervivencia a la edad adulta es común en TOF, D-TGA y ventrículo único, pero estos pacientes tienen riesgo de disfunción valvular, arritmias, insuficiencia cardíaca y muerte prematura, y requieren manejo multidisciplinar.']], '_total': 4.79}, {'key': 'cctaprev', 'sec': 8, 'title': 'The emerging role of coronary computed tomography for prevention of cardiovascular disease in asymptomatic individuals', 'ptype': 'Revisión', 'prio': 'Relevante', 'journal': 'Eur J Prev Cardiol', 'doi': '10.1093/eurjpc/zwag314', 'resumen': 'Revisión sobre el papel emergente de la TC coronaria (calcio coronario y angio-TC) en prevención primaria: permite pasar de un riesgo poblacional a una estratificación personalizada basada en la aterosclerosis visualizada.', 'why': 'sitúa la angio-TC coronaria como herramienta para personalizar la prevención (carga y composición de placa), a la espera de tres grandes ensayos en marcha.', 'modal': [['De qué va.', 'El aumento global de la enfermedad aterosclerótica reta a los algoritmos de riesgo por factores; la mayoría de los infartos ocurren sin síntomas previos ni factores clásicos. Revisión del papel de la TC coronaria —calcio coronario (CACS) y angio-TC (CCTA)— para visualizar directamente la aterosclerosis y orientar la prevención personalizada.'], ['Resultados.', 'La CCTA evalúa carga, composición y gravedad de la estenosis y rasgos de placa de alto riesgo. La carga total de placa es el principal marcador para guiar el tratamiento; la placa no calcificada y los rasgos de alto riesgo pueden apoyar su intensificación. La TC de conteo de fotones y la inteligencia artificial pueden mejorar la cuantificación. Ningún ensayo aleatorizado ha demostrado aún que el cribado por CCTA mejore desenlaces en asintomáticos (tampoco los scores tradicionales); hay tres grandes ensayos en marcha.'], ['Conclusiones.', 'La TC coronaria permite una prevención personalizada basada en la enfermedad; tres ensayos aleatorizados en curso determinarán si la estrategia guiada por CCTA reduce los eventos en personas asintomáticas.']], '_total': 5.24}, {'key': 'anxafib', 'sec': 10, 'title': 'Impact of Anxiety and Depression in Patients with Atrial Fibrillation: Insights from Two International Prospective Registries', 'ptype': 'Análisis post hoc de registros', 'prio': 'Relevante', 'journal': 'Heart Rhythm', 'doi': '10.1016/j.hrthm.2026.06.001', 'resumen': 'Análisis de dos registros (12.614 pacientes con FA): los síntomas de ansiedad/depresión (38,3%) se asociaron a más mortalidad y MACE (HR del compuesto 1,26; muerte CV 1,87), con gradiente por gravedad.', 'why': 'señala que la ansiedad y la depresión empeoran el pronóstico en la fibrilación auricular, abogando por incorporar la valoración psicológica al manejo de la FA.', 'modal': [['De qué va.', 'Se dispone de pocos datos sobre el impacto de la ansiedad o la depresión en los desenlaces de la fibrilación auricular (FA). Análisis post hoc de dos registros prospectivos (Europa y Asia-Pacífico); pacientes clasificados como sintomáticos o no para ansiedad/depresión. Primario: compuesto de muerte por cualquier causa y MACE.'], ['Resultados.', 'De 12.614 pacientes (69±12 años; 38% mujeres), 4.825 (38,3%) eran sintomáticos para ansiedad/depresión. Tras una mediana de 569 días, los sintomáticos tuvieron mayor riesgo del compuesto (HR 1,26; IC95% 1,10-1,45), muerte por cualquier causa (HR 1,31), MACE (HR 1,44) y muerte CV (HR 1,87; IC95% 1,41-2,47). El riesgo aumentó con la gravedad de los síntomas, sin interacción por región.'], ['Conclusiones.', 'En la fibrilación auricular, los síntomas de ansiedad o depresión se asociaron a peores desenlaces, con mayor fuerza en los moderados-graves, lo que subraya la necesidad de incorporar la valoración psicológica al manejo de la FA.']], '_total': 5.5}]

_NEW = _NEW + [{'key': 'n021', 'sec': 3, 'title': 'Safety of very low LDL-cholesterol: Ten common concerns, misconceptions, and evidence-based clarifications.', 'ptype': 'Revisión', 'prio': 'Relevante', 'journal': 'Atherosclerosis', 'doi': '10.1016/j.atherosclerosis.2026.120783', 'resumen': 'Revisión que sintetiza la evidencia (epidemiología, aleatorización mendeliana, ECA y metaanálisis) sobre la seguridad de alcanzar cLDL muy bajo, sobre todo por vía farmacológica. Los ECA y metaanálisis no respaldan un aumento de riesgos mayores con la reducción intensiva.', 'why': 'respalda perseguir objetivos de cLDL muy bajos en pacientes de alto riesgo, ayudando a vencer la inercia terapéutica y la desinformación.', 'modal': [['De qué va.', 'Las guías actuales (incluida la actualización ESC/EAS 2025) recomiendan objetivos de cLDL más bajos en pacientes de alto riesgo, reavivando dudas sobre la seguridad del cLDL muy bajo logrado con fármacos. Revisión narrativa de estudios epidemiológicos, aleatorización mendeliana, ECA y metaanálisis que evalúa preocupaciones frecuentes: deterioro cognitivo, cáncer, ictus hemorrágico, diabetes, cataratas, efectos hormonales y síntomas musculares.'], ['Resultados.', 'ECA y metaanálisis NO apoyan mayor riesgo de deterioro cognitivo, cáncer, cataratas, hemorragia intracerebral ni disfunción hormonal clínicamente relevante con la reducción intensiva del cLDL, incluso a niveles muy bajos. Dos consideraciones sí merecen atención: disglucemia/diabetes de nueva aparición asociada a estatinas (modesta en términos absolutos, mayor en quienes parten de más riesgo glucémico) y síntomas musculares. Ambas deben sopesarse frente a la mayor reducción absoluta de eventos de ECVA. Con iPCSK9, los ensayos de desenlaces no han mostrado exceso clínicamente relevante de diabetes ni toxicidad muscular, incluso a cLDL ultrabajo.'], ['Conclusiones.', 'En pacientes seleccionados con riesgo elevado de ECVA, alcanzar cLDL muy bajo está respaldado por evidencia de beneficio cardiovascular sin evidencia consistente de daño mayor; definiciones claras del cLDL, comunicación transparente de riesgos y beneficios absolutos y la decisión compartida son esenciales para reducir la inercia terapéutica y mejorar la adherencia.']], '_total': 6.94}, {'key': 'n003', 'sec': 3, 'title': 'New and Emerging Therapeutic Targets for ApoB-Containing Particles Lowering.', 'ptype': 'Revisión', 'prio': 'Relevante', 'journal': 'Circ Res', 'doi': '10.1161/CIRCRESAHA.126.327270', 'resumen': 'Revisión sobre las dianas terapéuticas para reducir las partículas con apoB. Como cada partícula aterogénica porta una sola apoB, su concentración refleja el número de partículas y es un determinante causal de ECVA más exacto que el cLDL aislado.', 'why': 'apoya el cambio de un marco centrado en el cLDL a uno centrado en apoB para reducir tanto la ECVA como la pancreatitis mediada por triglicéridos.', 'modal': [['De qué va.', 'apoB es la proteína estructural de todas las lipoproteínas aterogénicas (VLDL, IDL, LDL, remanentes y Lp(a)); como cada partícula contiene una sola apoB, su concentración refleja el número de partículas aterogénicas. Revisión de las dianas establecidas y emergentes para reducirlas, integrando evidencia genética, epidemiológica y de ECA.'], ['Resultados.', 'Por partícula, apoB es un determinante causal de ECVA más exacto que el cLDL aislado. Los quilomicrones con apoB48 son centrales en la hipertrigliceridemia grave y la pancreatitis aguda. Terapias establecidas (estatinas, ezetimiba, iPCSK9, ácido bempedoico) actúan aumentando el aclaramiento de partículas con apoB vía receptor de LDL; lomitapida (inhibidor de MTP) y evinacumab (anti-ANGPTL3) reducen lipoproteínas con apoB por mecanismos independientes del receptor de LDL (hipercolesterolemia familiar homocigota). Dianas emergentes: proteínas similares a angiopoyetina, apoCIII, Lp(a), CETP, flujo lipídico hepático e incretinas. Enfoques dirigidos a genes: edición génica, edición epigenómica, siRNA, oligonucleótidos antisentido y nuevas combinaciones orales/inyectables.'], ['Conclusiones.', 'La transición de un marco centrado en el cLDL a uno centrado en apoB puede representar una estrategia biológicamente integrada para reducir el riesgo tanto de enfermedad cardiovascular aterosclerótica como de pancreatitis mediada por triglicéridos.']], '_total': 6.85}, {'key': 'n002', 'sec': 3, 'title': 'CETP Inhibitors: Back With a New Target.', 'ptype': 'Revisión', 'prio': 'Relevante', 'journal': 'Circ Res', 'doi': '10.1161/CIRCRESAHA.125.327271', 'resumen': 'Revisión sobre los inhibidores de CETP, proteína que intercambia colesterol esterificado por triglicéridos entre lipoproteínas. Se replantea su desarrollo: ya no para subir el cHDL, sino para reducir lípidos aterogénicos y mejorar el control glucémico.', 'why': 'redefine el papel de la inhibición de CETP, posicionando a obicetrapib como herramienta potencial en prevención cardiovascular.', 'modal': [['De qué va.', 'La CETP facilita el intercambio de colesterol esterificado por triglicéridos entre lipoproteínas; los estudios genéticos y de cohortes asocian la CETP baja con menos enfermedad cardiovascular, diabetes y neurodegeneración. Los primeros inhibidores fracasaron por toxicidad fuera de diana, futilidad o beneficio marginal. Revisión de la vía de desarrollo reorientada y el potencial actual.'], ['Resultados.', 'La CETP baja (genética/cohortes) se asocia a menos enfermedad cardiovascular, diabetes y neurodegeneración. Los programas iniciales fracasaron (toxicidad fuera de diana, futilidad o beneficio marginal con acumulación en tejido adiposo). La evidencia posterior señala una vía: reducir lípidos/lipoproteínas aterogénicas y mejorar el control glucémico (en vez de elevar el cHDL) podría reducir el riesgo. Obicetrapib es un inhibidor de CETP altamente selectivo con efectos favorables sobre lípidos aterogénicos, control glucémico y biomarcadores de patología beta-amiloide en Alzheimer preclínico.'], ['Conclusiones.', 'Se revisa el potencial vigente de la inhibición de CETP como herramienta eficaz en la clínica de prevención y en otras aplicaciones emergentes.']], '_total': 6.08}, {'key': 'n010', 'sec': 3, 'title': 'Translating Lipoprotein Genetics Into New Therapies.', 'ptype': 'Revisión', 'prio': 'Relevante', 'journal': 'Circ Res', 'doi': '10.1161/CIRCRESAHA.126.328828', 'resumen': 'Revisión sobre cómo la genética humana se ha convertido en el motor principal para identificar dianas hipolipemiantes y predecir el éxito o fracaso terapéutico, mediante el paradigma del knockout humano (variantes de pérdida de función de por vida).', 'why': 'muestra que la genética de variantes raras valida dianas con alto rendimiento traslacional, guiando el desarrollo de terapias hipolipemiantes duraderas.', 'modal': [['De qué va.', 'La genética humana es hoy el motor principal para identificar dianas hipolipemiantes y predecir éxito o fracaso. Los estudios monogénicos y la secuenciación poblacional identifican personas con variantes de pérdida de función de por vida (knockout humano). Revisión de cómo este enfoque traduce la validación genética en nuevas terapias.'], ['Resultados.', 'Ha impulsado aprobaciones en varias clases: PCSK9 (reducción de cLDL con beneficio cardiovascular); APOC3 (olezarsen y plozasiran, aprobados para reducir triglicéridos en el síndrome de quilomicronemia familiar); ANGPTL3 (evinacumab, aprobado para hipercolesterolemia familiar homocigota). La aleatorización mendeliana identificó el cHDL como biomarcador no causal, prediciendo el fracaso de las terapias que lo elevan. La farmacología basada en ARN (siRNA con N-acetilgalactosamina y antisentido) permite terapias duraderas de dosificación infrecuente, con ensayos de desenlaces pendientes; la edición génica extiende la lógica hacia intervenciones permanentes. Los GWAS y las puntuaciones poligénicas aún no logran el rendimiento traslacional de la genética de variantes raras.'], ['Conclusiones.', 'La genética de variantes raras (knockout humano) es el motor principal de identificación y validación de dianas hipolipemiantes, con rendimiento traslacional superior al de los GWAS y las puntuaciones poligénicas; la farmacología basada en ARN y la edición génica amplían las oportunidades de modulación lipídica duradera.']], '_total': 6.08}, {'key': 'n040', 'sec': 3, 'title': 'Electronic Health Record Alerts\xa0to Improve Lipid Lowering After a Recent Myocardial Infarction.', 'ptype': 'Estudio observacional', 'prio': 'Relevante', 'journal': 'J Am Heart Assoc', 'doi': '10.1161/JAHA.125.047116', 'resumen': 'Iniciativa de calidad que comparó una alerta pasiva (descartable) frente a una activa (no descartable sin acción) en la historia clínica para intensificar el tratamiento hipolipemiante tras IAM reciente. La alerta activa multiplicó por más de 4 el uso de ezetimiba e iPCSK9.', 'why': 'convertir las alertas en obligatorias (no descartables) impulsa el uso de hipolipemiantes no estatínicos tras un IAM, aunque persiste margen de mejora.', 'modal': [['De qué va.', 'Tras un IAM reciente el riesgo de nuevos eventos es alto y la intensificación hipolipemiante es subóptima. Comparación de una cohorte con alerta pasiva (feb 2018-jul 2019; n=733) frente a otra con alerta activa (ago 2020-ene 2022; n=587) en pacientes con IAM en los 12 meses previos y cLDL ≥70 mg/dl o ausente; se registraron los tratamientos y la consecución de objetivos de cLDL.'], ['Resultados.', 'Alerta pasiva (n=733): a 24 meses estatina 59%→87% y alta intensidad 39%→69%. Alerta activa (n=587): estatina 79%→80% y alta intensidad 70%→73% (cambios mínimos); ezetimiba 12%→35% (OR 4,69; IC95% 3,22-6,96) e iPCSK9 2%→8% (OR 4,07; IC95% 1,92-9,46). Mejoró la determinación y consecución de objetivos de cLDL en ambas. Motivo más frecuente para no intensificar: cLDL no actualizado (41,7%).'], ['Conclusiones.', 'Se siguen necesitando esfuerzos para fomentar la intensificación del tratamiento hipolipemiante dirigido por guías en pacientes con IAM reciente y riesgo de nuevos eventos cardiacos.']], '_total': 5.76}, {'key': 'n019', 'sec': 4, 'title': 'Long-term prognostic value of residual lipid burden in acute myocardial infarction.', 'ptype': 'Estudio observacional', 'prio': 'Relevante', 'journal': 'Atherosclerosis', 'doi': '10.1016/j.atherosclerosis.2026.120795', 'resumen': 'Estudio observacional en 1.312 pacientes con IAM y OCT de tres vasos, divididos según la carga lipídica residual (RLB) en lesiones no culpables. Una RLB alta predijo de forma independiente eventos a 5 años (HR ajustado 3,84).', 'why': 'la carga lipídica residual coronaria por OCT podría refinar la estratificación del riesgo tras IAM más allá del fibroateroma de capa fina.', 'modal': [['De qué va.', 'Se desconoce el valor pronóstico de la carga lipídica residual (RLB) total de las arterias no culpables tras ICP en el IAM. Estudio observacional de 1.312 pacientes con IAM y OCT de tres vasos, divididos en RLB baja (n=656) y alta (n=656) según la mediana del índice lipídico total de las lesiones no culpables. Seguimiento hasta 5 años (mediana 4,1); desenlace: MACE.'], ['Resultados.', 'El grupo de RLB alta tuvo más enfermedad multivaso, rotura de placa no culpable, fibroateroma de capa fina (TCFA 53,8% vs 11,0%) y placa vulnerable (todos p<0,001). Tras ajuste, la RLB alta predijo de forma independiente rotura, TCFA y placa vulnerable, y más MACE relacionados con lesión no culpable a 5 años (8,4% vs 2,6%; HR ajustado 3,84; IC95% 1,98-7,45), mayormente revascularización guiada por isquemia. Al incluir RLB alta y TCFA no culpable juntos, la RLB siguió siendo predictiva (p=0,002) y el TCFA no (p=0,079). Como variable continua, su valor se atenuó (AUC 0,63). La asociación se observó en ambos sexos.'], ['Conclusiones.', 'La carga lipídica residual derivada de OCT se asoció con las características de placa pancoronaria en el IAM y, cuando fue alta, predijo eventos adversos a 5 años de forma independiente del fibroateroma de capa fina.']], '_total': 5.86}, {'key': 'n036', 'sec': 5, 'title': 'Barriers to Optimization of Medical Therapy and the Role of Checklist-Based Decision Support in Heart Failure.', 'ptype': 'Estudio multicéntrico', 'prio': 'Relevante', 'journal': 'J Am Heart Assoc', 'doi': '10.1161/JAHA.125.047062', 'resumen': 'Análisis de transcripciones del ensayo POCKET-COST-HF: 247 pacientes con IC y FE reducida y 39 clínicos usando una herramienta tipo checklist. Se identificaron barreras a la optimización del tratamiento en el 61,5% de los encuentros, mayoritariamente médicas (74,3%).', 'why': 'las barreras no médicas (coste, inercia, deseo de minimizar fármacos) son abordables con herramientas de apoyo a la decisión y deberían priorizarse en su diseño.', 'modal': [['De qué va.', 'El tratamiento médico dirigido por guías (TMDG) reduce morbimortalidad en la ICFEr pero está infrautilizado. Análisis secundario de transcripciones del ensayo POCKET-COST-HF (checklist con transparencia de precios, 2 centros académicos), con análisis de contenido para identificar barreras y oportunidades de mejora.'], ['Resultados.', '247 pacientes (edad media 62,9; 29,5% mujeres; 26,3% negros) y 39 clínicos. Uso basal alto: betabloqueantes 95%, IECA/ARA-II/ARNI 81%, antagonistas mineralocorticoides 63%, iSGLT2 43%. Checklist mencionado en 48,6% de encuentros; optimización discutida en 75,7%. Barreras en 61,5% de encuentros: médicas 74,3% (p. ej. hipotensión); no médicas: coste 29,6% y resistencia de pacientes/clínicos 13,8%.'], ['Conclusiones.', 'Las barreras no médicas a la optimización del TMDG pueden abordarse con herramientas de apoyo a la decisión como los checklists; la atención al coste, la inercia clínica y el deseo de minimizar la medicación debería priorizarse en futuras iteraciones.']], '_total': 5.61}, {'key': 'n029', 'sec': 5, 'title': 'Cardio-Oncologic Considerations in Heart Failure With Mildly Reduced Ejection Fraction: Prevalence and Prognostic Impact of Malignancies.', 'ptype': 'Estudio observacional', 'prio': 'Complementario', 'journal': 'J Am Heart Assoc', 'doi': '10.1161/JAHA.125.047798', 'resumen': 'Estudio observacional retrospectivo en 2.184 pacientes hospitalizados por IC con FE levemente reducida. Las neoplasias, presentes en el 15,3%, se asociaron de forma independiente con mayor mortalidad por cualquier causa a 30 meses (HR ajustado 2,568).', 'why': 'en la IC con FE levemente reducida, las neoplasias concomitantes marcan un peor pronóstico vital impulsado por la mortalidad no cardiaca.', 'modal': [['De qué va.', 'Los pacientes con neoplasias solían excluirse de los ensayos de IC, con datos limitados sobre sus desenlaces. Estudio observacional retrospectivo unicéntrico de pacientes consecutivos hospitalizados por IC con FE levemente reducida (2016-2022). Primario: mortalidad por cualquier causa a 30 meses; secundario: rehospitalización por empeoramiento de IC.'], ['Resultados.', 'De 2.184 pacientes, el 15,3% (n=335) tenía neoplasias; activas en 257 (sólidas 175, hematológicas 73), IC por terapia oncológica 3,9%. Los pacientes con neoplasias tenían menos miocardiopatía isquémica y recibían menos betabloqueantes, bloqueo del sistema renina-angiotensina-aldosterona y estatinas. Las neoplasias se asociaron a mayor mortalidad por cualquier causa (59,4% vs 26,2%; HR ajustado 2,568; IC95% 2,101-3,138; P=0,001), ya visible en la hospitalización índice (8,4% vs 2,5%; P=0,001) y atribuida sobre todo a mortalidad no cardiaca. La rehospitalización por IC no difirió entre grupos.'], ['Conclusiones.', 'Las neoplasias estaban presentes en el 15% de los pacientes con IC con FE levemente reducida y se asociaron de forma independiente con la mortalidad por cualquier causa a largo plazo, atribuida principalmente a mayor mortalidad no cardiaca; la rehospitalización por IC no se vio afectada.']], '_total': 4.84}, {'key': 'n026', 'sec': 6, 'title': 'Diagnostic Trends and Geographic Health Care Disparities Among Patients With Transthyretin Amyloid Cardiomyopathy.', 'ptype': 'Estudio transversal', 'prio': 'Complementario', 'journal': 'J Am Heart Assoc', 'doi': '10.1161/JAHA.125.048943', 'resumen': 'Análisis geoespacial y de cohorte (Komodo Healthcare Map, 2016-2024) de 14 980 pacientes con miocardiopatía amiloide por transtiretina (ATTR-CM) en EE. UU. La prevalencia diagnosticada fue 35,68/100 000 y se cuadruplicó, con disparidades raciales y geográficas.', 'why': 'el diagnóstico de ATTR-CM ha aumentado mucho pero persisten desigualdades raciales y geográficas en el acceso a cardiólogos y centros especializados.', 'modal': [['De qué va.', 'La ATTR-CM es una miocardiopatía restrictiva rara y potencialmente mortal cuyo diagnóstico depende del acceso a cardiólogos y centros de amiloidosis. Análisis geoespacial transversal de centros y cardiólogos, y cohorte retrospectiva de pacientes con ATTR-CM del Komodo Healthcare Map (jul 2016-jun 2024).'], ['Resultados.', '14 980 pacientes (edad media 74,8; 62,3% varones; 54,1% blancos; 28,8% negros). Prevalencia 35,68/100 000; mayor en negros (102,17) y en el Noreste (52,63); se cuadruplicó en el periodo. Distancia media a un cardiólogo 4,3 millas y a un centro de amiloidosis 48,5 millas; amplias zonas (sobre todo Medio Oeste) con escasez.'], ['Conclusiones.', 'La prevalencia de ATTR-CM ha aumentado sustancialmente desde 2017, con diferencias raciales notables; persisten disparidades geográficas y es necesario identificar estrategias para abordarlas.']], '_total': 4.66}, {'key': 'n054', 'sec': 7, 'title': 'Sex-Specific and Time-Dependent Outcomes After TAVR Versus SAVR: A Meta-Analysis of Randomized Trials.', 'ptype': 'Metaanálisis', 'prio': 'Relevante', 'journal': 'JACC Adv', 'doi': '10.1016/j.jacadv.2026.102856', 'resumen': 'Metaanálisis de 9 ECA (N=9583; 44,2% mujeres) de TAVI frente a SAVR según sexo y tiempo. En mujeres, la TAVI se asoció a menor riesgo a 1 y 2 años (RR 0,67 y 0,80), sin diferencias a 5 años; en varones, sin diferencias significativas.', 'why': 'los resultados de la sustitución valvular aórtica dependen del sexo, el riesgo quirúrgico y el tiempo, apoyando una selección TAVI vs SAVR individualizada.', 'modal': [['De qué va.', 'Se han descrito diferencias por sexo en TAVI vs SAVR, pero su variación temporal y según riesgo quirúrgico es incierta. Metaanálisis (PubMed, Embase, Cochrane hasta ene 2026) de ECA con desenlaces estratificados por sexo, mortalidad y seguimiento ≥1 año; RR combinados con efectos aleatorios y análisis por sexo y riesgo.'], ['Resultados.', '9 ensayos (N=9583; 44,2% mujeres). Mujeres: TAVI con menor riesgo a 1 año (RR 0,67; IC95% 0,55-0,81) y 2 años (RR 0,80; IC95% 0,69-0,94), sin diferencia a 5 años (RR 1,03; IC95% 0,89-1,18). Varones: sin diferencias en ningún momento. El beneficio precoz en mujeres fue mayor en riesgo intermedio-alto; a 5 años, mayor riesgo con TAVI en varones de riesgo intermedio-alto. Metarregresión sin modificación significativa por edad, riesgo o FA.'], ['Conclusiones.', 'Los resultados tras la sustitución valvular aórtica varían según el sexo, el riesgo quirúrgico y el tiempo: la TAVI se asoció a beneficio precoz en mujeres (sobre todo de riesgo intermedio-alto) con convergencia a largo plazo, mientras que los varones no mostraron diferencias significativas, con mayor riesgo con TAVI a 5 años en riesgo intermedio-alto.']], '_total': 6.83}, {'key': 'n056', 'sec': 10, 'title': 'Female Sex Is Not a Uniform Risk Factor in Atrial Fibrillation.', 'ptype': 'Estudio de cohorte', 'prio': 'Relevante', 'journal': 'JACC Adv', 'doi': '10.1016/j.jacadv.2026.102826', 'resumen': 'Estudio de cohorte (TriNetX) en FA no valvular emparejado por propensión. El sexo femenino se asoció con mayor riesgo de ictus solo en mayores de 75 años (HR 1,244 sin factores adicionales; HR 1,065 con un factor adicional).', 'why': 'el sexo femenino actúa como modificador del riesgo más que como factor independiente, lo que cuestiona su peso uniforme en la estratificación del ictus en FA.', 'modal': [['De qué va.', 'El sexo femenino forma parte de la estratificación del riesgo de ictus en la FA, aunque podría ser un modificador más que un factor independiente. Con TriNetX se identificaron pacientes con FA no valvular, estratificados por sexo y edad (<65, 65-74, ≥75) y emparejados por propensión (comorbilidades y anticoagulación). Desenlace: ictus y embolia arterial a 1 año.'], ['Resultados.', 'Sin factores CHA2DS2-VA adicionales ni anticoagulación (n=252.528): el sexo femenino se asoció a más ictus solo en ≥75 años (HR 1,244; IC95% 1,087-1,423; P=0,001). Con un factor adicional (n=607.612): riesgo aumentado en mujeres ≥75 años (HR 1,065; IC95% 1,014-1,118; P=0,012).'], ['Conclusiones.', 'El sexo femenino actúa como un modificador modesto del riesgo de ictus tromboembólico en la fibrilación auricular; el aumento se observa principalmente en pacientes con mayor carga de comorbilidad o edad avanzada (≥75 años).']], '_total': 5.73}]
_DROP = _DROP | {'aavhofh', 'glsiao', 'lpaukb', 'metilacion', 'sentinel', 'dcd', 'secprev', 'reducelap', 'vesiculas', 'fourier', 'arvc'}
for _snum,_sname,_arts in SECTIONS:
    _arts[:] = [a for a in _arts if a['key'] not in _DROP]
    for _na in _NEW:
        if _na['sec']==_snum:
            _arts.append({k:v for k,v in _na.items() if k!='sec'})

# Build lookup
ALL = {}
for snum, sname, arts in SECTIONS:
    for a in arts:
        ALL[a["key"]] = a
        a["_section"] = sname
        a["title"] = a["title"].rstrip()
        if a["title"].endswith("."): a["title"] = a["title"][:-1].rstrip()

# ---- re-evaluación 6 ejes (REL20·CAMBIO25·EVID20·EFECTO15·REP12·FI8) ----
_NEWPRIO = {"track": "Imprescindible", "mk7": "Complementario", "estatinas": "Complementario", "prevent": "Relevante", "hta": "Relevante", "findckd": "Imprescindible", "ckm": "Imprescindible", "synch1": "Relevante", "infinity": "Imprescindible", "synchmasld": "Relevante", "fourier": "Relevante", "aavhofh": "Complementario", "metilacion": "Complementario", "lpaukb": "Complementario", "vesiculas": "Complementario", "p2y12": "Relevante", "favor3": "Relevante", "abyss": "Relevante", "complete": "Relevante", "tncronica": "Relevante", "shock": "Complementario", "hm3": "Complementario", "c2d": "Complementario", "reducelap": "Complementario", "dcd": "Complementario", "sglt2gen": "Relevante", "mavacamten": "Relevante", "arvc": "Complementario", "genohcm": "Complementario", "takotsubo": "Complementario", "coapt": "Relevante", "itmeta": "Relevante", "earlytavr": "Relevante", "claspiid": "Complementario", "glsiao": "Complementario", "tctavi": "Complementario", "mfr": "Complementario", "itph": "Complementario", "aselap": "Complementario", "taaimg": "Complementario", "fetalav": "Complementario", "avlm": "Complementario", "eurobasilica": "Complementario", "halt": "Complementario", "algvelos": "Complementario", "option": "Relevante", "smartbeats": "Relevante", "persepolis": "Complementario", "camera2": "Relevante", "sentinel": "Complementario"}
_TOTAL = {"track": 7.72, "mk7": 4.39, "estatinas": 4.94, "prevent": 7.04, "hta": 7.32, "findckd": 7.86, "ckm": 8.81, "synch1": 7.76, "infinity": 8.36, "synchmasld": 6.67, "fourier": 5.26, "aavhofh": 4.25, "metilacion": 3.62, "lpaukb": 4.83, "vesiculas": 2.18, "p2y12": 7.6, "favor3": 6.68, "abyss": 6.08, "complete": 5.5, "tncronica": 5.63, "shock": 4.98, "hm3": 4.9, "c2d": 4.27, "reducelap": 4.78, "dcd": 4.58, "sglt2gen": 5.7, "mavacamten": 5.55, "arvc": 4.46, "genohcm": 4.53, "takotsubo": 4.06, "coapt": 6.38, "itmeta": 5.45, "earlytavr": 6.44, "claspiid": 4.98, "glsiao": 4.63, "tctavi": 4.46, "mfr": 4.74, "itph": 4.06, "aselap": 4.83, "taaimg": 3.66, "fetalav": 2.74, "avlm": 4.56, "eurobasilica": 3.66, "halt": 3.31, "algvelos": 3.42, "option": 6.64, "smartbeats": 5.14, "persepolis": 4.3, "camera2": 5.1, "sentinel": 4.75}
for _k,_a in ALL.items():
    _a['prio'] = _NEWPRIO.get(_k, _a.get('prio'))
    _a['_total'] = _TOTAL.get(_k, _a.get('_total', 0))

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
<title>Briefing Cardiovascular · UICAR · Quirónsalud — N0</title>
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
  .sec-head .chev{{flex:0 0 auto;margin-left:auto;font-size:30px;line-height:1;position:relative;top:-2px;transition:transform .18s ease;}}
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
  article h4{{margin:0 0 8px;font-size:17px;font-weight:700;line-height:1.34;color:var(--titulo);letter-spacing:-.01em;text-align:justify;}}
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
  .modal-title{{margin:0 0 16px;font-size:20px;font-weight:800;color:var(--titulo);line-height:1.3;text-align:justify;}}
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
        <span class="num">N0</span>
        <span class="periodo">3 al 10 de junio de 2026</span>
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
OUTDIR = "/Users/dmarzal/Documents/UICAR/Briefing Cardiovascular/Briefing Cardiovascular_N0"
os.makedirs(OUTDIR, exist_ok=True)
with io.open(OUTDIR + "/Briefing Cardiovascular_N0.html","w",encoding="utf-8") as f:
    f.write(HTML)

# sanity counts
nart = sum(len(a) for _,_,a in SECTIONS)
print("Artículos:", nart)
print("Modales:", HTML.count('class="mcb"'))
print("Secciones:", HTML.count('class="sec-head"'))
print("Bytes:", len(HTML.encode("utf-8")))
print("OUT:", OUTDIR)
