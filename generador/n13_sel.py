#!/usr/bin/env python3
# Selección y ponderación N13 (31 ago - 6 sep 2026).
# Los obligatorios (NEJM/Lancet CV + guías/consensos/statements de sociedad) entran SIEMPRE,
# salvo los descartados por TIPO o por no ser cardiovasculares (regla de encaje 6).
import json, os, glob
from collections import defaultdict, Counter
B = os.path.dirname(os.path.abspath(__file__))
EL = json.load(open(B + '/n13_el.json'))

# Reubicaciones editoriales (sección) tras revisar el cribado por lotes.
# 60: enfermedad aórtica torácica -> Valvulopatías (valvulo-aortopatía), no miocardiopatía.
# 61: revisión de imagen intracoronaria -> Imagen cardíaca.
MOVE = {60: 7, 61: 8}

W = dict(rel=.20, cambio=.25, evid=.20, efecto=.15, rep=.12, fi=.08)
def score(rel,cam,evi,efe,rep,fi):
    return round(W['rel']*rel+W['cambio']*cam+W['evid']*evi+W['efecto']*efe+W['rep']*rep+W['fi']*fi, 2)
def prio(t,c):
    if c>=8 or t>=8: return "Imprescindible"
    if t>=5: return "Relevante"
    return "Complementario"

cand, descartes = {}, {}
for f in sorted(glob.glob(B+'/n13_out?.json')):
    for o in json.load(open(f)):
        i = o['idx']
        if not o.get('elegible'):
            descartes[i] = o.get('motivo_descarte','tipo no elegible')
            continue
        cand[i] = dict(idx=i, sec=MOVE.get(i, o['sec']), ptype=o['ptype'], rel=o['rel'], cambio=o['cambio'],
                       evid=o['evid'], efecto=o['efecto'], rep=o['rep'], fi=o['fi'], acr=o.get('acr',''),
                       frase=o.get('frase',''), oblig=bool(EL[i].get('_oblig')))
for c in cand.values():
    c['total'] = score(c['rel'],c['cambio'],c['evid'],c['efecto'],c['rep'],c['fi'])
    c['prio']  = prio(c['total'], c['cambio'])

# top 5 por sección, AMPLIANDO si hay más de 5 obligatorios
bysec = defaultdict(list)
for c in cand.values(): bysec[c['sec']].append(c)
SELECT = []
for s in range(1,11):
    arts = sorted(bysec[s], key=lambda x:(-x['total'],-x['cambio']))
    obl  = [a for a in arts if a['oblig']]
    rest = [a for a in arts if not a['oblig']]
    keep = obl + rest[:max(0, 5-len(obl))]
    SELECT.extend(sorted(keep, key=lambda x:(-x['total'],-x['cambio'])))

out=[]
for i,c in enumerate(sorted(SELECT,key=lambda x:(x['sec'],-x['total'])),1):
    r = EL[c['idx']]
    out.append(dict(key=f"a{i}", idx=c['idx'], pmid=r['pmid'], doi=r['doi'], pii=r['pii'],
                    journal=r['journal'], sec=c['sec'], ptype=c['ptype'], acr=c['acr'],
                    rel=c['rel'],cambio=c['cambio'],evid=c['evid'],efecto=c['efecto'],rep=c['rep'],fi=c['fi'],
                    total=c['total'], prio=c['prio'], oblig=c['oblig'], noabs=r['_noabs'],
                    alt=r.get('_alt'), rec=r.get('_rec',''),
                    title=r['title'].rstrip('.'), abstract=r['abstract']))
json.dump(out, open(B+'/n13_sel.json','w'), ensure_ascii=False, indent=1)
json.dump({o['key']:o['acr'] for o in out if o['acr']}, open(B+'/n13_acr.json','w'), ensure_ascii=False, indent=1)

print(f"CANDIDATOS elegibles: {len(cand)} | descartados en cribado: {len(descartes)}")
print(f"SELECCIONADOS: {len(out)}  (obligatorios: {sum(1 for o in out if o['oblig'])})")
print("por sección:", dict(sorted(Counter(o['sec'] for o in out).items())))
print("prioridad:", dict(Counter(o['prio'] for o in out)))
print("\n=== TOP 8 (Destacado + Top 3 salen de aquí) ===")
for o in sorted(out,key=lambda x:(-x['total'],-x['cambio'],-x['efecto']))[:8]:
    print(f"  {o['key']:4} {o['total']:5} C{o['cambio']:<3}E{o['efecto']:<3} s{o['sec']:<3}{o['journal'][:22]:24}{o['title'][:64]}")
