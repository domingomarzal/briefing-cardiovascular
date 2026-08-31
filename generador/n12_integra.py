#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""N12 · Integra los artículos recuperados por CROSSREF (12 originales de NEJM que PubMed no
había indexado) + EUROASPIRE VI, y rehace la selección por secciones.
Regla: los de INCLUSIÓN OBLIGATORIA entran todos; si una sección supera 5, se amplía."""
import json, os, glob
from collections import defaultdict
B = os.path.dirname(os.path.abspath(__file__))

D = json.load(open(B+'/n12_data.json'))                 # 50 fichas actuales
S = {o['key']: o for o in json.load(open(B+'/n12_sel.json'))}
NEW = []
for f in sorted(glob.glob(B+'/n12_xout*.json')):
    NEW.extend(json.load(open(f)))
print(f"Recuperados para integrar: {len(NEW)} -> {[o['key'] for o in NEW]}")

W = dict(rel=.20, cambio=.25, evid=.20, efecto=.15, rep=.12, fi=.08)
def score(rel,cam,evi,efe,rep,fi):
    if efe is None:
        return round((W['rel']*rel+W['cambio']*cam+W['evid']*evi+W['rep']*rep+W['fi']*fi)/0.85,2)
    return round(W['rel']*rel+W['cambio']*cam+W['evid']*evi+W['efecto']*efe+W['rep']*rep+W['fi']*fi,2)
def prio(t,c):
    if c>=8 or t>=8: return "Imprescindible"
    return "Relevante" if t>=5 else "Complementario"

ACR = json.load(open(B+'/n12_acr.json'))
for o in NEW:
    k=o['key']
    tot=score(o['rel'],o['cambio'],o['evid'],o['efecto'],o['rep'],o['fi'])
    jr = 'Eur Heart J' if k=='x13' else 'N Engl J Med'
    doi = o.get('doi') or ''
    if k=='x13' and not doi: doi='10.1093/eurheartj/ehag262'
    D[k]=dict(key=k, sec=o['sec'], ptype=o['ptype'], journal=jr, doi=doi,
              total=tot, prio=prio(tot,o['cambio']),
              title_en=o['title_en'], title_es=o['title_es'], es=o['es'], en=o['en'])
    S[k]=dict(key=k, idx=-1, pmid='', doi=doi, pii='', journal=jr, sec=o['sec'], ptype=o['ptype'],
              acr=o.get('acr',''), rel=o['rel'], cambio=o['cambio'], evid=o['evid'], efecto=o['efecto'],
              rep=o['rep'], fi=o['fi'], total=tot, prio=prio(tot,o['cambio']), oblig=True, noabs=False,
              title=o['title_en'], abstract='')
    if o.get('acr'): ACR[k]=o['acr']

# --- Reselección por secciones: obligatorios TODOS + completar hasta 5 ---
bysec=defaultdict(list)
for k,v in D.items(): bysec[v['sec']].append(k)
KEEP=set()
print("\nSección  oblig  total  -> se muestran")
for s in range(1,11):
    ks=sorted(bysec[s], key=lambda k:-D[k]['total'])
    ob=[k for k in ks if S[k].get('oblig')]
    no=[k for k in ks if not S[k].get('oblig')]
    keep = ob + no[:max(0,5-len(ob))]
    KEEP.update(keep)
    extra = f"  (AMPLIADA de 5 a {len(keep)})" if len(keep)>5 else ""
    print(f"   {s:2}      {len(ob):2}     {len(ks):2}   ->   {len(keep)}{extra}")

D={k:v for k,v in D.items() if k in KEEP}
S={k:v for k,v in S.items() if k in KEEP}
ACR={k:v for k,v in ACR.items() if k in KEEP}
json.dump(D, open(B+'/n12_data.json','w'), ensure_ascii=False, indent=1)
json.dump(sorted(S.values(), key=lambda x:(x['sec'],-x['total'])), open(B+'/n12_sel.json','w'), ensure_ascii=False, indent=1)
json.dump(ACR, open(B+'/n12_acr.json','w'), ensure_ascii=False, indent=1)
from collections import Counter
print(f"\nTOTAL en el número: {len(D)}  (antes 50)")
print("prioridad:", dict(Counter(v['prio'] for v in D.values())))
print("\n=== TOP 10 por puntuación ===")
for k in sorted(D, key=lambda k:-D[k]['total'])[:10]:
    v=D[k]; print(f"  {v['total']:5}  {k:4} s{v['sec']:<3}{v['journal'][:16]:18}{v['title_es'][:58]}")
