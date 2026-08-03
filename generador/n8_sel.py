#!/usr/bin/env python3
# Selección y ponderación N8 (semana 27 jul - 2 ago 2026). Índices = posición en la lista de elegibles.
import json, os
D1, D2 = '2026/07/27', '2026/08/02'
BAD = {'Editorial','Comment','Letter','Published Erratum','News','Case Reports'}
recs = json.load(open(os.path.dirname(__file__)+'/n8_corpus.json'))['recs']
EL = [r for r in recs if D1 <= r['adate'] <= D2 and r['abstract'] and not (set(r['ptypes']) & BAD)]

# idx, sec, ptype, REL, CAMBIO, EVID, EFECTO(None=guía/consenso), REP, FI, acronimo
SEL = [
 # 01 Cardiología preventiva
 (105,1, "Estudio de cohorte",                    9,7,6,7,7,6, ""),
 (10, 1, "Estudio de cohorte",                    8,7,7,6,6,7, " (MESA)"),
 (87, 1, "Estudio pronóstico",                    8,6,6,5,5,6, ""),
 (44, 1, "Registro",                              8,5,6,5,6,6, ""),
 (58, 1, "Estudio de cohorte",                    6,4,6,5,6,6, ""),
 # 02 Cardiometabolismo
 (48, 2, "Ensayo clínico aleatorizado",           8,9,9,9,8,10, ""),
 (39, 2, "Artículo de revisión",                  9,6,6,5,7,7, ""),
 (23, 2, "Ensayo clínico aleatorizado",           7,6,7,6,6,7, " (PRESTIGE-AMI)"),
 (46, 2, "Estudio de cohorte",                    8,5,6,6,6,6, ""),
 (83, 2, "Artículo de revisión",                  8,5,5,5,7,6, ""),
 # 03 Dislipemia
 (3,  3, "Investigación original",                9,6,8,7,9,10, ""),
 (35, 3, "Metaanálisis",                          9,6,8,7,6,6, ""),
 (33, 3, "Estudio de cohorte",                    8,6,6,6,6,6, ""),
 (55, 3, "Estudio de cohorte",                    5,3,5,5,4,6, ""),
 # 04 Cardiopatía isquémica
 (65, 4, "Ensayo clínico aleatorizado",           8,7,8,5,8,10, ""),
 (97, 4, "Ensayo clínico aleatorizado",           7,7,7,6,6,7, ""),
 (16, 4, "Metaanálisis",                          8,6,7,6,6,7, ""),
 (21, 4, "Estudio pronóstico",                    6,5,6,6,6,7, ""),
 (37, 4, "Estudio diagnóstico",                   6,5,6,5,6,6, ""),
 # 05 Insuficiencia cardíaca
 (17, 5, "Ensayo clínico aleatorizado",           6,9,9,9,8,10, ""),
 (40, 5, "Documento de consenso",                 8,7,7,None,6,7, ""),
 (93, 5, "Análisis secundario de ensayo clínico", 7,7,7,7,6,7, ""),
 (94, 5, "Estudio de cohorte",                    7,6,5,6,6,6, " (JROAD-DPC)"),
 (8,  5, "Análisis secundario de ensayo clínico", 7,5,6,6,5,7, ""),
 # 06 Miocardiopatías
 (104,6, "Análisis secundario de ensayo clínico", 8,7,8,8,7,7, ""),
 (69, 6, "Ensayo clínico aleatorizado",           5,8,9,6,8,10, ""),
 (47, 6, "Estudio de cohorte",                    7,6,6,6,6,6, ""),
 (20, 6, "Artículo de revisión",                  7,6,6,5,6,7, ""),
 (66, 6, "Estudio de cohorte",                    6,6,5,5,5,6, " (GenbaseHTx)"),
 # 07 Valvulopatías
 (73, 7, "Estudio de cohorte",                    8,8,6,7,7,7, ""),
 (41, 7, "Análisis secundario de ensayo clínico", 7,6,7,6,6,7, ""),
 (59, 7, "Registro",                              7,6,6,5,6,7, ""),
 (75, 7, "Estudio de cohorte",                    6,4,6,5,5,6, ""),
 (29, 7, "Registro",                              6,4,5,5,5,6, ""),
 # 08 Imagen cardíaca
 (89, 8, "Inteligencia artificial / modelo predictivo", 6,6,6,6,7,7, ""),
 (68, 8, "Estudio de cohorte",                    7,6,6,6,5,6, ""),
 (71, 8, "Inteligencia artificial / modelo predictivo", 7,5,5,5,5,6, ""),
 (60, 8, "Estudio observacional",                 6,5,5,5,5,6, " (PECTUS-obs)"),
 (27, 8, "Artículo de revisión",                  6,4,5,4,5,6, ""),
 # 09 Cardiología intervencionista
 (62, 9, "Ensayo clínico aleatorizado",           7,8,7,8,8,10, ""),
 (42, 9, "Ensayo clínico aleatorizado",           7,8,8,6,7,7, ""),
 (12, 9, "Registro",                              6,5,5,5,5,6, ""),
 (78, 9, "Análisis secundario de ensayo clínico", 5,4,6,4,4,6, ""),
 (74, 9, "Artículo de revisión",                  5,4,4,4,5,7, ""),
 # 10 Arritmias y electrofisiología
 (72, 10, "Inteligencia artificial / modelo predictivo", 9,8,8,7,7,7, " (FIND-AF 2.0)"),
 (14, 10, "Estudio de cohorte",                   9,7,5,6,6,6, ""),
 (108,10, "Artículo de revisión",                 8,6,5,5,6,10, ""),
 (98, 10, "Estudio observacional",                7,6,6,6,6,6, ""),
 (0,  10, "Estudio observacional",                8,6,4,5,7,6, ""),
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

json.dump(out, open(os.path.dirname(__file__)+'/n8_sel.json', 'w'), ensure_ascii=False, indent=1)
acr = {o["key"]: o["acr"] for o in out if o["acr"]}
json.dump(acr, open(os.path.dirname(__file__)+'/n8_acr.json', 'w'), ensure_ascii=False, indent=1)
for o in sorted(out, key=lambda x: -x['total'])[:10]:
    print(f"{o['key']:5}{o['total']:6} {o['prio'][:14]:15} s{o['sec']:<3}{o['journal'][:22]:24}{o['title'][:60]}")
from collections import Counter
print('TOTAL seleccionados:', len(out), dict(sorted(Counter(o['sec'] for o in out).items())))
print('prioridad:', dict(Counter(o['prio'] for o in out)))
