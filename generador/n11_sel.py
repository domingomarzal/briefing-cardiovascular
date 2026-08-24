#!/usr/bin/env python3
# Selección y ponderación N11 (semana 17 - 23 ago 2026). Índices = posición en la lista de elegibles.
import json, os
D1, D2 = '2026/08/17', '2026/08/23'
BAD = {'Editorial','Comment','Letter','Published Erratum','News','Case Reports'}
recs = json.load(open(os.path.dirname(__file__)+'/n11_corpus.json'))['recs']
EL = [r for r in recs if D1 <= r['adate'] <= D2 and r['abstract'] and not (set(r['ptypes']) & BAD)]

# Rúbrica de 6 ejes SIN retocar. Destacado y Top 3 salen del ranking TOTAL.
# idx, sec, ptype, REL, CAMBIO, EVID, EFECTO(None=guía/consenso), REP, FI, acronimo
SEL = [
 # 01 Cardiología preventiva
 (92,  1, "Estudio de cohorte",                    8,6,7,7,7,10, " (ASPREE)"),
 (113, 1, "Metaanálisis",                          8,7,8,7,5,7,  ""),
 (87,  1, "Estudio de cohorte",                    8,6,7,6,6,7,  ""),
 (41,  1, "Artículo de revisión",                  8,6,6,4,7,7,  ""),
 (29,  1, "Estudio de cohorte",                    7,5,7,6,6,6,  ""),
 # 02 Cardiometabolismo
 (43,  2, "Análisis secundario de ensayo clínico", 9,7,8,7,9,7,  ""),
 (81,  2, "Análisis secundario de ensayo clínico", 8,7,8,6,6,6,  " (FINEARTS-HF)"),
 (82,  2, "Análisis secundario de ensayo clínico", 8,6,8,6,7,7,  ""),
 (73,  2, "Estudio de cohorte",                    7,5,6,7,5,6,  " (CRISPS-2)"),
 (108, 2, "Artículo de revisión",                  9,5,5,4,7,6,  ""),
 # 03 Dislipemia
 (112, 3, "Análisis secundario de ensayo clínico", 8,7,8,7,7,7,  ""),
 (65,  3, "Registro",                              9,6,6,6,6,6,  " (cvMOBIUS-2)"),
 (8,   3, "Estudio observacional",                 5,7,4,8,6,6,  ""),
 (100, 3, "Metaanálisis",                          8,5,6,5,5,6,  ""),
 (22,  3, "Registro",                              7,5,6,5,5,6,  " (CLARIFY)"),
 # 04 Cardiopatía isquémica
 (109, 4, "Análisis secundario de ensayo clínico", 8,7,8,6,6,6,  ""),
 (2,   4, "Estudio de cohorte",                    8,7,5,7,6,6,  ""),
 (59,  4, "Estudio diagnóstico",                   7,6,7,6,5,6,  ""),
 (50,  4, "Estudio pronóstico",                    6,5,6,6,5,6,  ""),
 (63,  4, "Registro",                              6,5,6,5,6,6,  " (SR-SCAD)"),
 # 05 Insuficiencia cardíaca
 (69,  5, "Ensayo clínico aleatorizado",           6,7,6,6,9,10, " (HEAL-CHF)"),
 (116, 5, "Estudio de cohorte",                    6,7,6,6,5,7,  ""),
 (77,  5, "Registro",                              7,5,6,7,5,6,  " (STRATS-HF-ARNI)"),
 (5,   5, "Estudio de cohorte",                    7,5,6,6,5,6,  ""),
 (72,  5, "Registro",                              6,5,6,6,5,6,  " (UNLOADERS-PVAD)"),
 # 06 Miocardiopatías
 (1,   6, "Análisis secundario de ensayo clínico", 7,7,8,7,7,7,  ""),
 (104, 6, "Inteligencia artificial / modelo predictivo", 8,7,7,7,6,6, ""),
 (90,  6, "Documento de consenso",                 7,6,7,None,6,6, ""),
 (115, 6, "Ensayo clínico aleatorizado",           6,7,7,6,6,6,  ""),
 (89,  6, "Artículo de revisión",                  5,5,5,4,5,6,  ""),
 # 07 Valvulopatías
 (54,  7, "Metaanálisis",                          8,7,6,8,6,6,  ""),
 (119, 7, "Ensayo clínico aleatorizado",           7,7,8,5,6,6,  ""),
 (49,  7, "Inteligencia artificial / modelo predictivo", 7,6,7,6,6,7, ""),
 (35,  7, "Estudio de cohorte",                    6,6,6,7,5,6,  ""),
 (34,  7, "Registro",                              5,6,5,7,6,6,  " (TRINITY)"),
 # 08 Imagen cardíaca
 (84,  8, "Estudio pronóstico",                    8,7,7,7,6,6,  " (SPINS)"),
 (25,  8, "Análisis secundario de ensayo clínico", 7,6,7,6,6,6,  ""),
 (66,  8, "Inteligencia artificial / modelo predictivo", 6,5,6,6,5,6, ""),
 (55,  8, "Artículo de revisión",                  7,6,5,4,5,6,  ""),
 (96,  8, "Inteligencia artificial / modelo predictivo", 5,5,5,5,5,6, ""),
 # 09 Cardiología intervencionista
 (16,  9, "Ensayo clínico aleatorizado",           7,8,9,7,8,10, ""),
 (40,  9, "Ensayo clínico aleatorizado",           6,8,9,7,8,10, ""),
 (121, 9, "Ensayo clínico aleatorizado",           7,7,7,6,6,6,  ""),
 (14,  9, "Estudio pronóstico",                    5,5,6,6,4,6,  ""),
 (118, 9, "Análisis secundario de ensayo clínico", 5,4,6,4,4,6,  ""),
 # 10 Arritmias y electrofisiología
 (37, 10, "Scientific Statement",                  9,7,7,None,7,7, ""),
 (38, 10, "Estudio de cohorte",                    8,7,5,7,6,6,  ""),
 (23, 10, "Estudio de cohorte",                    7,5,7,6,7,7,  ""),
 (67, 10, "Metaanálisis",                          6,6,6,6,6,6,  ""),
 (98, 10, "Investigación original",                7,6,5,5,6,6,  ""),
]
W = dict(rel=.20, cambio=.25, evid=.20, efecto=.15, rep=.12, fi=.08)

def score(rel, cambio, evid, efecto, rep, fi):
    if efecto is None:  # guías/consensos: el 15% de EFECTO se reparte (factor 1/0,85)
        t = (W['rel']*rel + W['cambio']*cambio + W['evid']*evid + W['rep']*rep + W['fi']*fi) / 0.85
    else:
        t = (W['rel']*rel + W['cambio']*cambio + W['evid']*evid + W['efecto']*efecto
             + W['rep']*rep + W['fi']*fi)
    return round(t, 2)

def prio(total, cambio):
    if cambio >= 8 or total >= 8: return "Imprescindible"
    if total >= 5: return "Relevante"
    return "Complementario"

out = []
for i, (idx, sec, ptype, rel, cam, evi, efe, rep, fi, acr) in enumerate(SEL, 1):
    r = EL[idx]
    tot = score(rel, cam, evi, efe, rep, fi)
    out.append(dict(key=f"a{i}", idx=idx, pmid=r['pmid'], doi=r['doi'], pii=r['pii'],
                    journal=r['journal'], sec=sec, ptype=ptype, acr=acr,
                    rel=rel, cambio=cam, evid=evi, efecto=efe, rep=rep, fi=fi,
                    total=tot, prio=prio(tot, cam),
                    title=r['title'].rstrip('.'), abstract=r['abstract']))

json.dump(out, open(os.path.dirname(__file__)+'/n11_sel.json', 'w'), ensure_ascii=False, indent=1)
acr = {o["key"]: o["acr"] for o in out if o["acr"]}
json.dump(acr, open(os.path.dirname(__file__)+'/n11_acr.json', 'w'), ensure_ascii=False, indent=1)
for o in sorted(out, key=lambda x: (-x['total'], -x['cambio']))[:12]:
    print(f"{o['key']:5}{o['total']:6} {o['prio'][:14]:15} s{o['sec']:<3}{o['journal'][:22]:24}{o['title'][:62]}")
from collections import Counter
print('TOTAL seleccionados:', len(out), dict(sorted(Counter(o['sec'] for o in out).items())))
print('prioridad:', dict(Counter(o['prio'] for o in out)))
