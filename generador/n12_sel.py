#!/usr/bin/env python3
# Selección y ponderación N12 (24-30 ago 2026, semana congreso ESC).
# Los 19 de INCLUSIÓN OBLIGATORIA los pondera el editor (abajo); el resto viene del cribado por lotes.
import json, os, glob
from collections import defaultdict
B = os.path.dirname(os.path.abspath(__file__))
EL = json.load(open(B + '/n12_el.json'))

# --- Ponderación editorial de los documentos de INCLUSIÓN OBLIGATORIA ---
# idx: (sec, ptype, REL, CAMBIO, EVID, EFECTO(None=guía), REP, FI, acronimo)
OBL = {
 131: (5, "Guía de práctica clínica",              10,10, 9, None,10, 8, ""),   # Guía ESC 2026 IC
  80: (4, "Guía de práctica clínica",              10,10, 9, None, 9, 8, ""),   # 5ª Definición Universal IAM
 165: (2, "Guía de práctica clínica",               9, 9, 8, None, 8, 8, ""),   # Guía ESC/ERA ECV-ERC
  32: (1, "Guía de práctica clínica",               8, 7, 7, None, 7, 7, ""),   # Guía ESC rehabilitación cardiaca
  23: (6, "Documento de consenso",                  6, 6, 6, None, 6, 6, ""),   # Consenso EHRA miocarditis
 160:(10, "Documento de consenso",                  5, 5, 6, None, 5, 6, ""),   # Consenso EHRA arritmias raras
 127: (1, "Scientific Statement",                   4, 4, 6, None, 4, 7, ""),   # AHA Raynaud
  16: (6, "Ensayo clínico aleatorizado",            7, 9, 9, 8, 9, 10, ""),     # Eplontersen ATTR-CM
 169: (6, "Ensayo clínico aleatorizado",            6, 8, 9, 7, 8, 10, ""),     # Aficamten HCM no obstructiva
  75:(10, "Ensayo clínico aleatorizado",           10, 9, 9, 7, 9, 10, ""),     # Anticoagulación FA riesgo intermedio
  94:(10, "Ensayo clínico aleatorizado",            9, 9, 9, 8, 9, 10, ""),     # PVI-SHAM-AF
 177: (4, "Ensayo clínico aleatorizado",            9, 9, 9, 7, 9, 10, ""),     # Retirada betabloqueantes post-IAM
 125: (3, "Ensayo clínico aleatorizado",            7, 7, 7, 8, 8, 10, ""),     # Kylo-11 Lp(a)
  71: (7, "Ensayo clínico aleatorizado",            6, 8, 8, 7, 7, 10, ""),     # Endocarditis antibiótico adaptado
  45: (4, "Ensayo clínico aleatorizado",            8, 7, 8, 7, 7, 10, ""),     # Vía 0/1 h IAM
 109: (5, "Registro",                               5, 5, 6, 5, 6, 10, ""),     # THESUS-HF II África
  18: (1, "Estudio de cohorte",                     7, 6, 7, 6, 6, 10, ""),     # Complicaciones gestación y riesgo CV
 134: (1, "Artículo de revisión",                   7, 5, 6, 4, 6, 10, ""),     # ECV en el embarazo
 135: (1, "Artículo de revisión",                   6, 4, 6, 4, 5, 10, ""),     # Preeclampsia
}
# Reubicación editorial: EUROASPIRE VI trata prevención secundaria en coronarios -> sección 4
MOVE = {24: 4, 191: 6}

W = dict(rel=.20, cambio=.25, evid=.20, efecto=.15, rep=.12, fi=.08)
def score(rel,cam,evi,efe,rep,fi):
    if efe is None:
        t=(W['rel']*rel+W['cambio']*cam+W['evid']*evi+W['rep']*rep+W['fi']*fi)/0.85
    else:
        t=(W['rel']*rel+W['cambio']*cam+W['evid']*evi+W['efecto']*efe+W['rep']*rep+W['fi']*fi)
    return round(t,2)
def prio(t,c):
    if c>=8 or t>=8: return "Imprescindible"
    if t>=5: return "Relevante"
    return "Complementario"

cand={}
# 1) obligatorios
for idx,(sec,pt,rel,cam,evi,efe,rep,fi,acr) in OBL.items():
    cand[idx]=dict(idx=idx,sec=sec,ptype=pt,rel=rel,cambio=cam,evid=evi,efecto=efe,rep=rep,fi=fi,acr=acr,oblig=True)
# 2) cribado por lotes
for f in sorted(glob.glob(B+'/n12_out*.json')):
    for o in json.load(open(f)):
        if not o.get('elegible'): continue
        i=o['idx']
        if i in cand: continue
        cand[i]=dict(idx=i,sec=MOVE.get(i,o['sec']),ptype=o['ptype'],rel=o['rel'],cambio=o['cambio'],
                     evid=o['evid'],efecto=o['efecto'],rep=o['rep'],fi=o['fi'],acr=o.get('acr',''),oblig=False)
for c in cand.values():
    c['total']=score(c['rel'],c['cambio'],c['evid'],c['efecto'],c['rep'],c['fi'])
    c['prio']=prio(c['total'],c['cambio'])

# 3) top 5 por sección, AMPLIANDO si hay más de 5 obligatorios
bysec=defaultdict(list)
for c in cand.values(): bysec[c['sec']].append(c)
SELECT=[]
for s in range(1,11):
    arts=sorted(bysec[s], key=lambda x:(-x['total'],-x['cambio']))
    obl=[a for a in arts if a['oblig']]
    rest=[a for a in arts if not a['oblig']]
    keep = obl + rest[:max(0, 5-len(obl))]      # todos los obligatorios + completar hasta 5
    keep = sorted(keep, key=lambda x:(-x['total'],-x['cambio']))
    SELECT.extend(keep)

out=[]
for i,c in enumerate(sorted(SELECT,key=lambda x:(x['sec'],-x['total'])),1):
    r=EL[c['idx']]
    out.append(dict(key=f"a{i}", idx=c['idx'], pmid=r['pmid'], doi=r['doi'], pii=r['pii'],
                    journal=r['journal'], sec=c['sec'], ptype=c['ptype'], acr=c['acr'],
                    rel=c['rel'],cambio=c['cambio'],evid=c['evid'],efecto=c['efecto'],rep=c['rep'],fi=c['fi'],
                    total=c['total'], prio=c['prio'], oblig=c['oblig'], noabs=r['_noabs'],
                    title=r['title'].rstrip('.'), abstract=r['abstract']))
json.dump(out, open(B+'/n12_sel.json','w'), ensure_ascii=False, indent=1)
json.dump({o['key']:o['acr'] for o in out if o['acr']}, open(B+'/n12_acr.json','w'), ensure_ascii=False, indent=1)

print(f"SELECCIONADOS: {len(out)}  (obligatorios: {sum(1 for o in out if o['oblig'])})")
from collections import Counter
print("por sección:", dict(sorted(Counter(o['sec'] for o in out).items())))
print("prioridad:", dict(Counter(o['prio'] for o in out)))
print("\n=== TOP 8 (Destacado + Top 3 salen de aquí) ===")
for o in sorted(out,key=lambda x:(-x['total'],-x['cambio']))[:8]:
    print(f"  {o['key']:4} {o['total']:5}  s{o['sec']:<3}{o['journal'][:20]:22}{o['title'][:66]}")
