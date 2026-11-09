#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PASO 1b — INCORPORACIÓN DE LOS ARTÍCULOS RECUPERADOS POR CROSSREF (N22).

El barrido de Crossref detectó 9 documentos publicados en la ventana 2-8 nov 2026 que PubMed
NO había indexado (0 resultados por DOI el 9-nov) y que son de INCLUSIÓN OBLIGATORIA:
8 artículos originales cardiovasculares de N Engl J Med (late-breakers del AHA 2026) y el
CoSTR 2026 del ILCOR publicado en Circulation (documento de consenso de sociedad).

Su contenido se reconstruyó desde fuentes secundarias con DOBLE FUENTE OBLIGATORIA para cada
cifra (notas de prensa de la AHA, TCTMD, Healio, Medscape, HCPLive, Radcliffe, ClinicalTrials.gov);
lo que no se pudo confirmar con dos fuentes independientes quedó OMITIDO y anotado en el campo
`omitido` de n22_recA.json / n22_recB.json. Ni una cifra inventada.

Se añaden al FINAL de n22_el.json para no desplazar los índices de los lotes de cribado ya
escritos (n22_out0..4.json); su ponderación va a mano en n22_out9.json.
Es idempotente: no duplica un DOI ya presente.
"""
import json, os
B = os.path.dirname(os.path.abspath(__file__))
EL = json.load(open(B+'/n22_el.json'))
have = {(r.get('doi') or '').lower() for r in EL}

# Normalización al tipo canónico del PASO 5 (la lista es CERRADA)
PTYPE_CANON = {
 '10.1056/nejmoa2602919': 'Estudio observacional',          # ON-SCENE: despliegue escalonado NO aleatorizado
 '10.1056/nejmoa2612757': 'Ensayo clínico aleatorizado',    # RACE-CARS: aleatorizado por conglomerados
}
nuevos = 0
for f in ('n22_recA.json', 'n22_recB.json'):
    for e in json.load(open(B+'/'+f)):
        doi = (e['doi'] or '')
        if doi.lower() in have: continue
        EL.append(dict(pmid='', journal=e['journal'], title=e['title'].rstrip('.'),
                       ptypes=['Randomized Controlled Trial'], abstract=e['abstract'],
                       doi=doi, pii='', adate='2026/11/07', _oblig=True, _noabs=False,
                       _ptype=PTYPE_CANON.get(doi.lower(), e['ptype']),
                       _acr=e.get('acr',''), _conf=e.get('confianza',''),
                       _rec=('recuperado por Crossref (PASO 1b): publicado en la ventana y no '
                             'indexado por PubMed; contenido verificado por doble fuente '
                             'secundaria, con las cifras no confirmadas omitidas')))
        have.add(doi.lower()); nuevos += 1
json.dump(EL, open(B+'/n22_el.json','w'), ensure_ascii=False)
print(f"n22_el.json: {len(EL)} elegibles (+{nuevos} recuperados por Crossref)")
for i, r in enumerate(EL):
    if r.get('_rec'): print(f"   idx {i:3} {r['journal'][:16]:17}{r.get('_acr','') or '-':16}{r['title'][:62]}")
