#!/usr/bin/env python3
# Selección y ponderación N6 (semana 13-19 jul 2026). Índices = posición en la lista de elegibles.
import json, os
D1, D2 = '2026/07/13', '2026/07/19'
BAD = {'Editorial','Comment','Letter','Published Erratum','News','Case Reports'}
recs = json.load(open(os.path.dirname(__file__)+'/n6_corpus.json'))['recs']
EL = [r for r in recs if D1 <= r['adate'] <= D2 and r['abstract'] and not (set(r['ptypes']) & BAD)]

# idx, sec, ptype, REL, CAMBIO, EVID, EFECTO(None=guía/consenso), REP, FI, acronimo
SEL = [
 # 01 Cardiología preventiva
 (63, 1, "Investigación original",            9,5,7,6,7,7, ""),
 (41, 1, "Ensayo clínico aleatorizado",       7,6,8,5,8,10, " (LatAm-FINGERS)"),
 (18, 1, "Documento de consenso",             8,6,7,None,6,8, ""),
 (15, 1, "Documento de consenso",             6,6,6,None,5,6, " (STRIDE BP)"),
 (22, 1, "Artículo de revisión",              7,5,6,4,6,8, ""),
 # 02 Cardiometabolismo
 (48, 2, "Emulación de ensayo diana",         9,7,7,5,8,9, ""),
 (52, 2, "Registro",                          8,4,6,5,5,6, " (SWEDEHEART)"),
 (49, 2, "Estudio de cohorte",                8,5,5,5,5,5, ""),
 (100,2, "Análisis secundario de ensayo clínico", 6,4,7,5,4,6, " (STRIP)"),
 (64, 2, "Estudio de cohorte",                6,3,6,5,4,5, ""),
 # 03 Dislipemia
 (68, 3, "Estudio de cohorte",                8,6,7,6,6,6, " (SCAPIS)"),
 (102,3, "Inteligencia artificial / modelo predictivo", 8,6,7,6,5,7, ""),
 (19, 3, "Estudio de cohorte",                7,3,5,4,3,5, ""),
 # 04 Cardiopatía isquémica
 (28, 4, "Ensayo clínico aleatorizado",       9,9,9,7,9,10, " (DAPT-MVD)"),
 (83, 4, "Análisis secundario de ensayo clínico", 7,6,5,6,5,6, " (XIENCE Short DAPT)"),
 (94, 4, "Análisis secundario de ensayo clínico", 7,5,6,5,4,6, " (MASTER DAPT)"),
 (66, 4, "Estudio observacional",             6,3,4,4,9,8, ""),
 (16, 4, "Estudio pronóstico",                5,3,5,4,3,5, ""),
 # 05 Insuficiencia cardíaca
 (45, 5, "Metaanálisis",                      8,6,7,6,5,6, " (NET-COST-HFrEF)"),
 (103,5, "Estudio diagnóstico",               7,6,6,5,4,6, ""),
 (37, 5, "Estudio diagnóstico",               7,5,6,5,4,6, ""),
 (7,  5, "Registro",                          6,4,5,5,4,6, " (ITAMACS)"),
 (82, 5, "Estudio de cohorte",                6,4,5,4,4,6, ""),
 # 06 Miocardiopatías
 (71, 6, "Ensayo clínico aleatorizado",       6,7,8,6,8,8, " (TEMPEST)"),
 (44, 6, "Estudio de cohorte",                5,5,6,5,4,6, ""),
 (110,6, "Estudio de cohorte",                6,4,5,4,3,6, ""),
 (73, 6, "Estudio de cohorte",                5,4,5,4,3,5, ""),
 (3,  6, "Estudio de cohorte",                4,4,4,4,3,5, ""),
 # 07 Valvulopatías
 (67, 7, "Análisis secundario de ensayo clínico", 7,6,7,7,6,6, " (TRISCEND II)"),
 (25, 7, "Documento de consenso",             8,6,6,None,5,6, ""),
 (98, 7, "Registro",                          7,5,6,5,5,6, " (STS/ACC TVT)"),
 (57, 7, "Artículo de revisión",              7,4,5,4,4,6, ""),
 (97, 7, "Estudio de cohorte",                5,3,5,4,3,6, ""),
 # 08 Imagen cardíaca
 (2,  8, "Ensayo clínico aleatorizado",       6,5,7,6,5,6, ""),
 (59, 8, "Estudio diagnóstico",               6,5,6,5,4,6, " (HERZCHECK)"),
 (9,  8, "Artículo de revisión",              8,4,5,4,5,6, ""),
 (70, 8, "Estudio diagnóstico",               6,5,5,5,4,6, ""),
 (111,8, "Investigación original",            4,3,4,3,3,6, ""),
 # 09 Cardiología intervencionista
 (85, 9, "Ensayo clínico aleatorizado",       8,8,8,7,8,10, " (OPTIMA-AF)"),
 (93, 9, "Análisis secundario de ensayo clínico", 7,6,6,6,5,6, " (ADAPT AF-DES)"),
 (89, 9, "Documento de consenso",             6,7,5,None,6,6, ""),
 (0,  9, "Metaanálisis",                      6,6,7,5,4,6, ""),
 (90, 9, "Ensayo clínico aleatorizado",       5,6,6,5,4,6, " (FAIR)"),
 # 10 Arritmias y electrofisiología
 (36, 10, "Metaanálisis",                     8,7,7,7,6,6, ""),
 (51, 10, "Análisis secundario de ensayo clínico", 6,6,6,5,4,5, " (CAMERA-MRI)"),
 (21, 10, "Registro",                         5,5,6,5,5,8, ""),
 (12, 10, "Estudio de cohorte",               6,5,5,5,4,5, ""),
 (105,10, "Estudio de cohorte",               7,4,5,4,4,5, ""),
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
json.dump(out, open(os.path.dirname(__file__)+'/n6_sel.json', 'w'), ensure_ascii=False, indent=1)
for o in sorted(out, key=lambda x: -x['total'])[:8]:
    print(f"{o['total']:5} {o['prio'][:14]:15} s{o['sec']:<3}{o['journal'][:22]:24}{o['title'][:70]}")
print('TOTAL seleccionados:', len(out))
