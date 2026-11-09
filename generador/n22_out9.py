#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ponderación A MANO de los 9 documentos recuperados por Crossref (PASO 1b) -> n22_out9.json.

No pasan por los lotes de cribado porque llegaron DESPUÉS de construirlos (PubMed no los había
indexado). Los pondera el editor con la misma rúbrica de 6 ejes del PASO 3, aplicando:
 · ANULACIÓN (c): los pivotales NEUTROS que zanjan una controversia puntúan ALTO en CAMBIO y
   EFECTO (Lp(a)HORIZON y ZEUS retiran, de facto, dos hipótesis terapéuticas enteras).
 · Reglas fijas de asignación del PASO 4: inflamación cardiovascular -> SIEMPRE 2;
   hipertensión -> SIEMPRE 1; lípidos (incl. Lp(a)) -> 3; muerte súbita/reanimación -> 10.
 · El eje EFECTO de un documento de consenso de sociedad SÍ se puntúa (anulación (b) derogada).
"""
import json, os
B = os.path.dirname(os.path.abspath(__file__))
EL = json.load(open(B+'/n22_el.json'))
#          idx: (sec, rel, cambio, evid, efecto, rep, fi, frase)
W = {
 110: (3, 9, 10, 10, 9, 10, 10,
   'Pelacarsen bajó la Lp(a) pero NO redujo los eventos cardiovasculares en prevención '
   'secundaria: 12,3% frente a 12,1%, HR 1,02 (IC95% 0,90-1,15) en 8.350 pacientes.'),
 111: (2, 8, 9, 10, 9, 10, 10,
   'La inhibición de la IL-6 con ziltivekimab no redujo el MACE a 3 puntos en enfermedad '
   'ateroesclerótica con ERC e inflamación: 17,6% frente a 17,7%, HR 0,99 (IC95% 0,88-1,11).'),
 112: (1, 9, 9, 8, 8, 9, 10,
   'Bajar la presión sistólica por debajo de 120 mmHg tras un ictus isquémico redujo los '
   'eventos cardiovasculares un 21%: 10,9% frente a 13,5%, HR 0,79 (IC95% 0,67-0,94).'),
 113: (1, 9, 7, 8, 6, 8, 10,
   'En diabetes tipo 2 de alto riesgo, el objetivo de PAS <120 mmHg no redujo '
   'significativamente los eventos cardiovasculares: 6,0% frente a 6,7%, HR 0,90 (P=0,20).'),
 114: (3, 8, 8, 8, 7, 8, 10,
   'Retirar la estatina de prevención primaria en mayores de 70 años con multimorbilidad fue '
   'NO INFERIOR a mantenerla a 2 años: -2,0 semanas de supervivencia libre de eventos '
   '(IC95% -3,7 a -0,3), dentro del margen de -5,2 semanas.'),
 115: (10, 8, 9, 8, 9, 9, 10,
   'La estimulación de rama izquierda redujo un 59% el compuesto de muerte, hospitalización por '
   'insuficiencia cardíaca o miocardiopatía inducida frente a la estimulación ventricular '
   'derecha en el bloqueo AV: HR 0,41 (IC95% 0,23-0,75).'),
 116: (10, 6, 7, 5, 8, 8, 10,
   'Iniciar el soporte vital extracorpóreo en el propio lugar de la parada, con equipos '
   'aéreos, dobló la supervivencia al alta en la parada extrahospitalaria refractaria de '
   'menores de 50 años: 40% frente a 20%, OR 2,72 (IC95% 1,59-4,66).'),
 117: (10, 7, 6, 8, 6, 7, 10,
   'Un programa comunitario y de emergencias de formación en RCP y uso de desfibriladores no '
   'mejoró la supervivencia neurológicamente favorable de la parada extrahospitalaria en un '
   'ensayo aleatorizado por conglomerados con 22.459 pacientes.'),
 118: (10, 8, 7, 9, 8, 8, 8,
   'El CoSTR 2026 del ILCOR actualiza la evidencia en reanimación con 16 revisiones '
   'sistemáticas y centra sus novedades en la CALIDAD de la RCP: ventilación, vía aérea, '
   'desfibrilación y compresiones.'),
}
Wt = dict(rel=.20, cambio=.25, evid=.20, efecto=.15, rep=.12, fi=.08)
out = []
for idx, (sec, rel, cam, evi, efe, rep, fi, frase) in sorted(W.items()):
    r = EL[idx]
    out.append(dict(idx=idx, elegible=True, motivo_descarte='', sec=sec,
                    ptype=r['_ptype'], rel=rel, cambio=cam, evid=evi, efecto=efe,
                    rep=rep, fi=fi, acr=r.get('_acr',''), frase=frase.replace('\n',' ')))
json.dump(out, open(B+'/n22_out9.json','w'), ensure_ascii=False, indent=1)
for o in out:
    t = round(sum(Wt[k]*o[k] for k in Wt), 2)
    print(f"  idx {o['idx']} s{o['sec']:<3}TOTAL {t:5}  {EL[o['idx']].get('_acr') or '-':18}{EL[o['idx']]['title'][:58]}")
print(f"n22_out9.json: {len(out)} entradas")
