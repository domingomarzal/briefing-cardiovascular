#!/usr/bin/env python3
# Selección y ponderación N7 (semana 20-26 jul 2026). Índices = posición en la lista de elegibles.
import json, os
D1, D2 = '2026/07/20', '2026/07/26'
BAD = {'Editorial','Comment','Letter','Published Erratum','News','Case Reports'}
recs = json.load(open(os.path.dirname(__file__)+'/n7_corpus.json'))['recs']
EL = [r for r in recs if D1 <= r['adate'] <= D2 and r['abstract'] and not (set(r['ptypes']) & BAD)]

# idx, sec, ptype, REL, CAMBIO, EVID, EFECTO(None=guía/consenso), REP, FI, acronimo
SEL = [
 # 01 Cardiología preventiva
 (65, 1, "Scientific Statement",                 8,6,7,None,9,8, ""),
 (81, 1, "Metaanálisis",                         9,6,7,6,6,6, ""),
 (106,1, "Estudio de cohorte",                   7,6,6,6,5,6, ""),
 (29, 1, "Estudio de cohorte",                   8,5,5,5,6,6, " (MESA)"),
 (40, 1, "Estudio diagnóstico",                  7,5,6,5,5,6, ""),
 # 02 Cardiometabolismo
 (108,2, "Emulación de ensayo diana",            9,7,7,7,9,6, ""),
 (90, 2, "Estudio diagnóstico",                  7,7,8,6,7,10, ""),
 (80, 2, "Ensayo clínico aleatorizado",          7,6,8,5,7,8, ""),
 (69, 2, "Emulación de ensayo diana",            6,4,6,5,8,10, ""),
 (14, 2, "Registro",                             8,5,5,5,5,6, " (WET-HF2)"),
 # 03 Dislipemia
 (44, 3, "Investigación original",               9,8,7,7,9,10, ""),
 (63, 3, "Ensayo clínico aleatorizado",          8,7,8,6,6,7, ""),
 (78, 3, "Análisis secundario de ensayo clínico",6,6,6,7,5,6, " (ARCHES-2)"),
 (8,  3, "Metaanálisis",                         7,5,7,6,5,6, ""),
 (93, 3, "Investigación original",               6,4,5,5,4,6, ""),
 # 04 Cardiopatía isquémica
 (37, 4, "Estudio de casos y controles",         8,6,6,6,6,8, ""),
 (94, 4, "Emulación de ensayo diana",            9,6,6,5,6,6, " (START-ANTIPLATELET)"),
 (86, 4, "Registro",                             7,6,5,6,6,7, ""),
 (49, 4, "Análisis secundario de ensayo clínico",7,5,6,5,5,6, " (XIENCE Short DAPT)"),
 (1,  4, "Estudio diagnóstico",                  6,5,5,5,6,6, ""),
 # 05 Insuficiencia cardíaca
 (107,5, "Registro",                             9,7,6,7,6,7, ""),
 (13, 5, "Documento de consenso",                8,7,7,None,6,7, ""),
 (16, 5, "Artículo de revisión",                 8,6,6,5,7,8, ""),
 (21, 5, "Registro",                             7,4,6,5,5,7, ""),
 (88, 5, "Análisis secundario de ensayo clínico",6,4,6,4,4,6, ""),
 # 06 Miocardiopatías
 (9,  6, "Estudio de cohorte",                   8,6,6,6,6,6, ""),
 (62, 6, "Artículo de revisión",                 7,6,6,5,6,8, ""),
 (11, 6, "Estudio de cohorte",                   6,5,6,5,5,7, ""),
 (60, 6, "Inteligencia artificial / modelo predictivo", 5,5,5,5,7,6, ""),
 (31, 6, "Estudio de cohorte",                   5,4,5,4,4,6, ""),
 # 07 Valvulopatías
 (98, 7, "Análisis secundario de ensayo clínico",8,7,7,6,7,7, ""),
 (50, 7, "Estudio observacional",                6,6,5,6,5,6, ""),
 (33, 7, "Estudio de cohorte",                   7,5,5,5,5,6, ""),
 (23, 7, "Artículo de revisión",                 6,4,4,4,4,6, ""),
 (110,7, "Estudio de cohorte",                   5,4,5,4,4,6, ""),
 # 08 Imagen cardíaca
 (39, 8, "Registro",                             8,6,6,6,6,6, ""),
 (67, 8, "Estudio de cohorte",                   6,4,6,5,5,8, ""),
 (46, 8, "Ensayo clínico aleatorizado",          6,5,6,4,4,6, ""),
 (102,8, "Estudio pronóstico",                   6,5,5,5,4,6, ""),
 (28, 8, "Estudio observacional",                5,4,5,4,5,6, ""),
 # 09 Cardiología intervencionista
 (70, 9, "Metaanálisis",                         8,7,8,6,7,7, ""),
 (55, 9, "Análisis secundario de ensayo clínico",7,6,7,6,6,6, ""),
 (17, 9, "Registro",                             6,4,6,4,5,6, ""),
 (85, 9, "Registro",                             7,4,5,4,4,6, ""),
 (54, 9, "Inteligencia artificial / modelo predictivo", 6,4,5,4,4,6, ""),
 # 10 Arritmias y electrofisiología
 (58, 10, "Metaanálisis",                        8,8,8,7,7,7, ""),
 (79, 10, "Metaanálisis",                        8,7,8,6,6,7, ""),
 (77, 10, "Ensayo clínico aleatorizado",         7,6,7,6,5,6, ""),
 (72, 10, "Análisis secundario de ensayo clínico",7,5,7,5,5,6, " (COMBINE-AF)"),
 (32, 10, "Estudio de cohorte",                  7,5,5,6,6,6, ""),
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
json.dump(out, open(os.path.dirname(__file__)+'/n7_sel.json', 'w'), ensure_ascii=False, indent=1)
for o in sorted(out, key=lambda x: -x['total'])[:10]:
    print(f"{o['total']:5} {o['prio'][:14]:15} s{o['sec']:<3}{o['journal'][:22]:24}{o['title'][:66]}")
print('TOTAL seleccionados:', len(out))
