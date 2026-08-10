#!/usr/bin/env python3
# Selección y ponderación N9 (semana 3 - 9 ago 2026). Índices = posición en la lista de elegibles.
import json, os
D1, D2 = '2026/08/03', '2026/08/09'
BAD = {'Editorial','Comment','Letter','Published Erratum','News','Case Reports'}
recs = json.load(open(os.path.dirname(__file__)+'/n9_corpus.json'))['recs']
EL = [r for r in recs if D1 <= r['adate'] <= D2 and r['abstract'] and not (set(r['ptypes']) & BAD)]

# idx, sec, ptype, REL, CAMBIO, EVID, EFECTO(None=guía/consenso), REP, FI, acronimo
SEL = [
 # 01 Cardiología preventiva
 (73, 1, "Estudio de cohorte",                    8,7,7,6,7,7, ""),
 (26, 1, "Estudio de cohorte",                    7,6,7,6,6,7, ""),
 (54, 1, "Estudio de cohorte",                    8,5,6,5,8,7, ""),
 (89, 1, "Estudio de cohorte",                    7,7,6,5,5,6, ""),
 (41, 1, "Investigación original",                7,5,7,5,6,7, ""),
 # 02 Cardiometabolismo
 (34, 2, "Estudio de cohorte",                    9,8,7,8,9,10, ""),
 (16, 2, "Documento de consenso",                 7,6,7,None,7,10, ""),
 (31, 2, "Registro",                              8,6,6,6,6,6, " (SWEDEHEART)"),
 (94, 2, "Estudio de cohorte",                    8,6,6,6,5,6, " (CARDIA)"),
 (86, 2, "Artículo de revisión",                  7,5,6,5,7,10, ""),
 # 03 Dislipemia
 (65, 3, "Investigación original",                8,7,6,7,6,6, ""),
 (35, 3, "Artículo de revisión",                  9,6,5,4,7,6, ""),
 # 04 Cardiopatía isquémica
 (99, 4, "Metaanálisis",                          8,7,7,6,6,6, ""),
 (4,  4, "Análisis secundario de ensayo clínico", 7,6,7,6,7,7, ""),
 (52, 4, "Estudio observacional",                 6,5,5,5,5,6, ""),
 (19, 4, "Estudio de cohorte",                    6,4,6,5,5,6, ""),
 (75, 4, "Estudio de cohorte",                    5,3,5,4,4,6, " (COPDGene)"),
 # 05 Insuficiencia cardíaca
 (88, 5, "Metaanálisis",                          7,7,9,7,6,6, ""),
 (67, 5, "Metaanálisis",                          8,7,8,7,5,6, ""),
 (11, 5, "Scientific Statement",                  6,7,7,None,7,7, ""),
 (2,  5, "Artículo de revisión",                  8,6,6,5,7,7, ""),
 (63, 5, "Estudio de cohorte",                    7,5,6,6,6,7, ""),
 # 06 Miocardiopatías
 (72, 6, "Estudio de cohorte",                    7,7,7,7,7,7, ""),
 (42, 6, "Análisis secundario de ensayo clínico", 7,6,6,7,7,7, ""),
 (12, 6, "Estudio de cohorte",                    7,7,5,6,6,6, ""),
 (29, 6, "Estudio de cohorte",                    6,6,5,6,6,6, ""),
 (0,  6, "Artículo de revisión",                  7,6,5,4,6,7, ""),
 # 07 Valvulopatías
 (68, 7, "Estudio diagnóstico",                   7,6,5,6,5,6, ""),
 (64, 7, "Registro",                              6,6,5,6,6,6, ""),
 (91, 7, "Registro",                              4,5,6,5,5,6, ""),
 (77, 7, "Estudio de cohorte",                    5,4,5,5,5,6, ""),
 (32, 7, "Estudio de cohorte",                    4,5,5,5,4,6, ""),
 # 08 Imagen cardíaca
 (92, 8, "Metaanálisis",                          7,7,6,6,5,6, ""),
 (44, 8, "Estudio diagnóstico",                   6,6,6,6,6,7, ""),
 (101,8, "Artículo de revisión",                  8,6,5,4,6,7, ""),
 (100,8, "Investigación original",                6,6,6,6,5,6, ""),
 (33, 8, "Artículo de revisión",                  5,4,5,4,6,7, ""),
 # 09 Cardiología intervencionista
 (95, 9, "Ensayo clínico aleatorizado",           5,6,6,6,6,7, ""),
 (38, 9, "Estudio de cohorte",                    6,6,5,6,6,6, ""),
 (97, 9, "Análisis secundario de ensayo clínico", 6,5,6,5,5,6, ""),
 (45, 9, "Registro",                              6,5,5,5,5,6, ""),
 (51, 9, "Inteligencia artificial / modelo predictivo", 5,5,5,5,5,6, ""),
 # 10 Arritmias y electrofisiología
 (40, 10, "Ensayo clínico aleatorizado",          8,9,9,8,9,10, ""),
 (28, 10, "Análisis secundario de ensayo clínico",9,6,8,6,7,7, ""),
 (62, 10, "Emulación de ensayo diana",            8,7,6,6,6,6, ""),
 (112,10, "Artículo de revisión",                 9,5,6,4,8,10, ""),
 (110,10, "Estudio de cohorte",                   7,7,6,6,6,6, ""),
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

json.dump(out, open(os.path.dirname(__file__)+'/n9_sel.json', 'w'), ensure_ascii=False, indent=1)
acr = {o["key"]: o["acr"] for o in out if o["acr"]}
json.dump(acr, open(os.path.dirname(__file__)+'/n9_acr.json', 'w'), ensure_ascii=False, indent=1)
for o in sorted(out, key=lambda x: -x['total'])[:10]:
    print(f"{o['key']:5}{o['total']:6} {o['prio'][:14]:15} s{o['sec']:<3}{o['journal'][:22]:24}{o['title'][:60]}")
from collections import Counter
print('TOTAL seleccionados:', len(out), dict(sorted(Counter(o['sec'] for o in out).items())))
print('prioridad:', dict(Counter(o['prio'] for o in out)))
