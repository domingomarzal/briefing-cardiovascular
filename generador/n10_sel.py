#!/usr/bin/env python3
# Selección y ponderación N10 (semana 10 - 16 ago 2026). Índices = posición en la lista de elegibles.
import json, os
D1, D2 = '2026/08/10', '2026/08/16'
BAD = {'Editorial','Comment','Letter','Published Erratum','News','Case Reports'}
recs = json.load(open(os.path.dirname(__file__)+'/n10_corpus.json'))['recs']
EL = [r for r in recs if D1 <= r['adate'] <= D2 and r['abstract'] and not (set(r['ptypes']) & BAD)]

# idx, sec, ptype, REL, CAMBIO, EVID, EFECTO(None=guía/consenso), REP, FI, acronimo
SEL = [
 # 01 Cardiología preventiva
 (46, 1, "Ensayo clínico aleatorizado",           8,8,8,7,6,6, " (CONCRETE)"),
 (39, 1, "Scientific Statement",                  8,7,7,None,7,7, ""),
 (37, 1, "Estudio de cohorte",                    8,6,7,7,7,7, ""),
 (26, 1, "Artículo de revisión",                  7,4,5,4,6,6, ""),
 (38, 1, "Estudio observacional",                 5,4,4,3,4,6, ""),
 # 02 Cardiometabolismo
 (29, 2, "Estudio de cohorte",                    9,8,8,7,9,7, ""),
 (8,  2, "Artículo de revisión",                  8,6,6,4,8,10, ""),
 (32, 2, "Análisis secundario de ensayo clínico", 8,6,5,6,8,6, " (SURMOUNT-1)"),
 (6,  2, "Estudio de cohorte",                    7,6,6,6,5,6, ""),
 (10, 2, "Estudio de casos y controles",          5,4,5,4,6,7, " (LURIC)"),
 # 03 Dislipemia
 (50, 3, "Artículo de revisión",                  9,6,5,4,7,6, ""),
 (44, 3, "Investigación original",                8,6,5,5,6,6, ""),
 # 04 Cardiopatía isquémica
 (60, 4, "Metaanálisis",                          8,8,7,7,6,6, ""),
 (23, 4, "Análisis secundario de ensayo clínico", 7,5,7,5,6,6, ""),
 # 05 Insuficiencia cardíaca
 (48, 5, "Inteligencia artificial / modelo predictivo", 5,6,7,7,5,7, ""),
 (47, 5, "Estudio pronóstico",                    8,8,8,8,8,6, ""),   # repoderado (Top 3, decisión editorial 17-ago)
 (49, 5, "Artículo de revisión",                  6,4,5,4,6,7, ""),
 (12, 5, "Artículo de revisión",                  4,3,4,3,4,6, ""),
 # 06 Miocardiopatías
 (61, 6, "Análisis secundario de ensayo clínico", 8,8,6,7,8,7, " (HELIOS-B)"),
 (24, 6, "Estudio de cohorte",                    7,7,6,7,6,6, ""),
 (40, 6, "Estudio de cohorte",                    7,7,6,6,6,6, ""),
 (7,  6, "Estudio diagnóstico",                   6,5,7,4,7,7, ""),
 (52, 6, "Estudio diagnóstico",                   6,6,5,6,5,6, ""),
 # 07 Valvulopatías
 (19, 7, "Registro",                              8,8,8,8,7,6, " (OCEAN-Mitral)"),   # repoderado (Top 3, decisión editorial 17-ago)
 (55, 7, "Estudio de cohorte",                    6,6,5,6,5,6, ""),
 (28, 7, "Artículo de revisión",                  6,5,5,4,5,6, ""),
 (43, 7, "Registro",                              4,5,6,5,4,6, ""),
 # 08 Imagen cardíaca
 (16, 8, "Inteligencia artificial / modelo predictivo", 7,6,6,7,5,6, ""),
 (58, 8, "Análisis secundario de ensayo clínico", 6,5,6,5,5,6, ""),
 (65, 8, "Estudio de cohorte",                    4,4,5,5,4,6, ""),
 # 09 Cardiología intervencionista
 (9,  9, "Ensayo clínico aleatorizado",           7,7,7,6,6,6, " (PROVISION)"),
 (5,  9, "Registro",                              7,6,6,6,5,6, " (J-PRIDE)"),
 (25, 9, "Estudio de cohorte",                    5,5,5,5,5,6, ""),
 (27, 9, "Estudio de cohorte",                    5,5,5,5,4,6, ""),
 # 10 Arritmias y electrofisiología
 (41, 10, "Emulación de ensayo diana",            8,8,7,7,7,10, ""),
 (64, 10, "Metaanálisis",                         8,8,8,7,7,6, ""),
 (36, 10, "Metaanálisis",                         8,7,7,6,6,6, ""),
 (63, 10, "Estudio de cohorte",                   8,7,6,6,7,7, ""),
 (42, 10, "Estudio de cohorte",                   9,8,7,8,9,6, ""),   # repoderado (Top 3, decisión editorial 17-ago)
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

json.dump(out, open(os.path.dirname(__file__)+'/n10_sel.json', 'w'), ensure_ascii=False, indent=1)
acr = {o["key"]: o["acr"] for o in out if o["acr"]}
json.dump(acr, open(os.path.dirname(__file__)+'/n10_acr.json', 'w'), ensure_ascii=False, indent=1)
for o in sorted(out, key=lambda x: -x['total'])[:10]:
    print(f"{o['key']:5}{o['total']:6} {o['prio'][:14]:15} s{o['sec']:<3}{o['journal'][:22]:24}{o['title'][:60]}")
from collections import Counter
print('TOTAL seleccionados:', len(out), dict(sorted(Counter(o['sec'] for o in out).items())))
print('prioridad:', dict(Counter(o['prio'] for o in out)))
