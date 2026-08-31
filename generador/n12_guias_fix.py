#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# N12: rehace las NOVEDADES de las 4 guías (viñetas, seleccionando lo esencial, sin referencias
# a tablas/figuras que el lector no tiene), corrige el enlace de la guía de rehabilitación a
# Eur Heart J y REPONDERA las guías puntuando EFECTO (decisión del usuario, 31/08/2026).
import json, os
B = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(B+'/n12_data.json'))
S = {o['key']: o for o in json.load(open(B+'/n12_sel.json'))}

NOV = {
"a21": (  # Guía ESC 2026 de insuficiencia cardiaca
 ["Desaparece la fracción de eyección levemente reducida: quedan dos fenotipos, reducida (<50%) y preservada (≥50%).",
  "El antagonista del receptor mineralocorticoide pasa a terapia fundacional en todo el rango de fracción de eyección, junto al inhibidor de SGLT2.",
  "Nueva nomenclatura del tratamiento: fundacional, adicional e intervencionista, en sustitución de «terapia médica dirigida por guías».",
  "La insuficiencia cardiaca «aguda» pasa a denominarse «descompensada».",
  "Titulación rápida: subir la terapia fundacional al menos cada 1-2 semanas hasta la dosis diana, y mantenerla aunque el paciente mejore o quede asintomático (I C).",
  "La obesidad entra en el algoritmo farmacológico: semaglutida o tirzepatida si hay síntomas, fracción de eyección ≥45% e índice de masa corporal ≥30 (IIa B1).",
  "Inhibidor de SGLT2 iniciado durante el ingreso, tras la estabilización (I B1).",
  "Cribado sistemático de amiloidosis cardiaca ante sospecha (I B) y test genético en miocardiopatía (I C).",
  "Estrena un sistema de gradación de la evidencia con niveles A, B1, B2 y C."],
 ["Heart failure with mildly reduced ejection fraction disappears: two phenotypes remain, reduced (<50%) and preserved (≥50%).",
  "Mineralocorticoid receptor antagonists become foundational therapy across the whole ejection fraction range, alongside SGLT2 inhibitors.",
  "New treatment nomenclature: foundational, additional and interventional, replacing “guideline-directed medical therapy”.",
  "“Acute” heart failure is renamed “decompensated”.",
  "Rapid titration: up-titrate foundational therapy at least every 1-2 weeks to target dose, and maintain it even if the patient improves or becomes asymptomatic (I C).",
  "Obesity enters the drug algorithm: semaglutide or tirzepatide if symptomatic, ejection fraction ≥45% and body mass index ≥30 (IIa B1).",
  "SGLT2 inhibitor started in hospital, after stabilisation (I B1).",
  "Systematic screening for cardiac amyloidosis when suspected (I B) and genetic testing in cardiomyopathy (I C).",
  "Introduces an evidence grading system with levels A, B1, B2 and C."]),

"a6": (  # Guía ESC/ERA de ECV y enfermedad renal crónica
 ["Primera guía conjunta de la Sociedad Europea de Cardiología y la European Renal Association dedicada a la intersección entre enfermedad renal crónica y enfermedad cardiovascular.",
  "Cribado renal a todo paciente con enfermedad cardiovascular: filtrado glomerular estimado y cociente albúmina/creatinina en orina desde el diagnóstico.",
  "Marco de actuación en cinco pasos: cribar, estadificar, tratar el riesgo renal, adaptar el manejo cardiovascular y planificar los servicios asistenciales.",
  "Método de medida (I A): ecuación validada —CKD-EPI 2009 preferida en Europa—, muestra de primera orina de la mañana y confirmación de cronicidad con dos determinaciones separadas al menos tres meses.",
  "Cistatina C cuando la creatinina no es fiable, como en los extremos de masa muscular (IIa).",
  "Algoritmo institucional de uso seguro del contraste yodado (I), en lugar de decisiones caso a caso.",
  "La enfermedad renal deja de ser una contraindicación difusa y pasa a ser un modificador explícito del manejo de cada síndrome cardiovascular.",
  "Revascularización selectiva en la enfermedad coronaria estable, manteniendo la intervención urgente en las presentaciones agudas."],
 ["First joint guideline from the European Society of Cardiology and the European Renal Association devoted to the overlap between chronic kidney disease and cardiovascular disease.",
  "Kidney screening for every patient with cardiovascular disease: estimated glomerular filtration rate and urine albumin-to-creatinine ratio from diagnosis.",
  "A five-step framework: screen, triage, address kidney risk, modify cardiovascular management and plan health services.",
  "Measurement method (I A): validated equation —CKD-EPI 2009 preferred in Europe—, first morning urine sample and confirmation of chronicity with two measurements at least three months apart.",
  "Cystatin C when creatinine is unreliable, such as at the extremes of muscle mass (IIa).",
  "An institutional protocol for safe iodinated contrast use (I), rather than case-by-case decisions.",
  "Kidney disease stops being a vague contraindication and becomes an explicit modifier of the management of each cardiovascular syndrome.",
  "Selective revascularisation in stable coronary disease, while urgent intervention is maintained in acute presentations."]),

"a1": (  # Guía ESC 2026 de rehabilitación cardiaca
 ["Primera guía de la Sociedad Europea de Cardiología dedicada íntegramente a la rehabilitación cardiaca; hasta ahora las recomendaciones estaban dispersas en las guías de síndrome coronario, insuficiencia cardiaca y prevención.",
  "Amplía las indicaciones mucho más allá del post-infarto y la insuficiencia cardiaca: valvulopatía, cardiopatía congénita del adulto, fibrilación auricular, portadores de dispositivos implantables, miocardiopatías, cardio-oncología y fragilidad.",
  "Evaluación sistemática de los resultados percibidos por el paciente en todos los candidatos a rehabilitación (I A), con cuestionarios validados (I C).",
  "Define doce componentes nucleares e incorpora ámbitos habitualmente desatendidos: consejo sexual, reincorporación laboral, exposición ambiental y fragilidad.",
  "Formaliza cinco modos de entrega, incluidas la telerrehabilitación y los modelos híbridos, con el matiz explícito de que la modalidad remota es una opción adicional y no un sustituto de la presencial.",
  "Señala la financiación como principal barrera: cerca del 40% de los programas carece de cobertura pública pese a la evidencia de coste-efectividad.",
  "Cubre también a los pacientes oncológicos que reciben tratamientos cardiotóxicos; quedan fuera de alcance el ictus, la arteriopatía periférica y la patología aórtica."],
 ["First European Society of Cardiology guideline devoted entirely to cardiac rehabilitation; until now the recommendations were scattered across the coronary syndrome, heart failure and prevention guidelines.",
  "Indications are widened well beyond post-infarction and heart failure: valvular disease, adult congenital heart disease, atrial fibrillation, implantable device carriers, cardiomyopathies, cardio-oncology and frailty.",
  "Systematic assessment of patient-reported outcomes in all candidates for rehabilitation (I A), using validated questionnaires (I C).",
  "Defines twelve core components and includes areas that are usually neglected: sexual counselling, return to work, environmental exposure and frailty.",
  "Formalises five delivery modes, including telerehabilitation and hybrid models, with the explicit caveat that the remote option is additional and not a replacement for centre-based rehabilitation.",
  "Funding is identified as the main barrier: close to 40% of programmes lack public coverage despite the cost-effectiveness evidence.",
  "It also covers oncology patients receiving cardiotoxic treatments; stroke, peripheral artery disease and aortic disease are out of scope."]),

"a16": (  # Quinta Definición Universal del Infarto de Miocardio
 ["Se abandona la numeración de tipos 1 a 5 y se pasa a tres categorías clínicas: infarto primario, secundario y relacionado con procedimiento.",
  "El infarto primario deja de limitarse a la aterotrombosis e incluye toda la patología coronaria aguda: disección coronaria espontánea, embolia y vasoespasmo.",
  "El infarto secundario exige ahora criterios objetivos y deja de ser un diagnóstico de contexto ante taquicardia, anemia o sepsis.",
  "Desaparece el tipo 3 —muerte súbita— como categoría propia: se clasifica según el contexto o los hallazgos post mortem.",
  "El infarto periprocedimiento deja de definirse por múltiplos de troponina y exige complicación coronaria o hallazgos de imagen, con criterios idénticos para el intervencionismo y la cirugía.",
  "Umbrales de troponina específicos por sexo, para corregir la infradetección del infarto en mujeres.",
  "El MINOCA pasa a denominarse lesión miocárdica con arterias coronarias no obstructivas y se reconoce como diagnóstico de trabajo, con la resonancia como técnica de elección.",
  "La trombosis de stent o la reestenosis más allá de 30 días pasan a contabilizarse como infarto primario.",
  "Primera alineación con la clasificación internacional de enfermedades CIE-11, con código propio para la disección coronaria espontánea."],
 ["The type 1 to 5 numbering is abandoned in favour of three clinical categories: primary, secondary and procedure-related myocardial infarction.",
  "Primary infarction is no longer restricted to atherothrombosis and now covers all acute coronary pathology: spontaneous coronary artery dissection, embolism and vasospasm.",
  "Secondary infarction now requires objective criteria and is no longer a contextual diagnosis in the setting of tachycardia, anaemia or sepsis.",
  "Type 3 —sudden death— disappears as a separate category: it is classified according to the clinical context or post-mortem findings.",
  "Procedure-related infarction is no longer defined by troponin multiples and requires a coronary complication or imaging findings, with identical criteria for percutaneous intervention and surgery.",
  "Sex-specific troponin thresholds, to correct the under-detection of infarction in women.",
  "MINOCA is renamed myocardial injury with non-obstructive coronary arteries and is recognised as a working diagnosis, with cardiac magnetic resonance as the technique of choice.",
  "Stent thrombosis or restenosis beyond 30 days now count as primary infarction.",
  "First alignment with the ICD-11 international classification of diseases, including a dedicated code for spontaneous coronary artery dissection."]),
}

# Reponderación: EFECTO SÍ se puntúa en las guías. Su magnitud y solidez proceden del respaldo
# de la sociedad científica (ESC y sociedades nacionales europeas) y de que sintetizan la mejor
# evidencia disponible (decisión del usuario, 31/08/2026).
REPOND = {          # REL CAMBIO EVID EFECTO REP FI
 "a21": (10, 10, 10, 10, 10, 8),   # Guía ESC IC — Destacado
 "a6":  ( 9,  9,  9,  9,  9, 8),   # Guía ESC/ERA ECV-ERC
 "a1":  ( 8,  9,  9,  9,  8, 8),   # Guía ESC rehabilitación cardiaca
 "a16": (10, 10,  9,  9,  9, 8),   # Quinta Definición Universal de IAM
}
W = dict(rel=.20, cambio=.25, evid=.20, efecto=.15, rep=.12, fi=.08)
def score(rel,cam,evi,efe,rep,fi):
    return round(W['rel']*rel+W['cambio']*cam+W['evid']*evi+W['efecto']*efe+W['rep']*rep+W['fi']*fi, 2)
def prio(t,c):
    if c>=8 or t>=8: return "Imprescindible"
    return "Relevante" if t>=5 else "Complementario"

for k,(nes,nen) in NOV.items():
    D[k]['es']['resultados'] = nes
    D[k]['en']['resultados'] = nen

# La guía de rehabilitación se enlaza a su publicación en Eur Heart J (no a Eur J Prev Cardiol)
D['a1']['journal'] = 'Eur Heart J'; D['a1']['doi'] = '10.1093/eurheartj/ehag099'
S['a1']['journal'] = 'Eur Heart J'; S['a1']['doi'] = '10.1093/eurheartj/ehag099'

for k,(rel,cam,evi,efe,rep,fi) in REPOND.items():
    t = score(rel,cam,evi,efe,rep,fi); p = prio(t,cam)
    D[k]['total'] = t; D[k]['prio'] = p
    S[k].update(rel=rel,cambio=cam,evid=evi,efecto=efe,rep=rep,fi=fi,total=t,prio=p)
    print(f"  {k}: EFECTO={efe} -> TOTAL {t}  {p}")

json.dump(D, open(B+'/n12_data.json','w'), ensure_ascii=False, indent=1)
json.dump(sorted(S.values(), key=lambda x:(x['sec'],-x['total'])), open(B+'/n12_sel.json','w'), ensure_ascii=False, indent=1)
print("\nn12_data.json y n12_sel.json actualizados")
