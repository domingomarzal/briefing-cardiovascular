#!/usr/bin/env python3
# Selección y ponderación N22 (2 - 8 nov 2026). Semana del congreso AHA 2026.
import json, os, glob
from collections import defaultdict, Counter
B = os.path.dirname(os.path.abspath(__file__))
EL = json.load(open(B + '/n22_el.json'))

# ⭐ SIN REUBICACIONES NI AJUSTES MANUALES ESTA SEMANA. Los 9 documentos recuperados por
# Crossref (PASO 1b) se ponderan en n22_out9.py, que ya aplica las reglas fijas de asignación
# del PASO 4 (inflamación CV -> 2, hipertensión -> 1, Lp(a) -> 3, muerte súbita/reanimación -> 10).
MOVE = {}
OBLIG_EXTRA = set()
PTYPE_FIX = {}
ADJUST = {}

W = dict(rel=.20, cambio=.25, evid=.20, efecto=.15, rep=.12, fi=.08)
def score(rel,cam,evi,efe,rep,fi):
    return round(W['rel']*rel+W['cambio']*cam+W['evid']*evi+W['efecto']*efe+W['rep']*rep+W['fi']*fi, 2)
def prio(t,c):
    if c>=8 or t>=8: return "Imprescindible"
    if t>=5: return "Relevante"
    return "Complementario"

# ⛔ DEDUPLICACIÓN CON LOS NÚMEROS ANTERIORES (regla de encaje 7 / PASO 1)
PREV = {}
for f in glob.glob(B+'/n*_data.json'):
    if '/n22_' in f: continue
    try: d = json.load(open(f))
    except Exception: continue
    it = d.values() if isinstance(d, dict) else d
    for v in it:
        if isinstance(v, dict) and v.get('doi'):
            PREV[v['doi'].lower()] = os.path.basename(f).split('_')[0].upper()

cand, descartes, _dups = {}, {}, []
for f in sorted(glob.glob(B+'/n22_out[0-9].json')):
    for o in json.load(open(f)):
        i = o['idx']
        if not o.get('elegible'):
            descartes[i] = o.get('motivo_descarte','tipo no elegible'); continue
        _doi = (EL[i].get('doi') or '').lower()
        if _doi in PREV:
            descartes[i] = 'ya publicado en un número anterior (%s)' % PREV[_doi]
            _dups.append(i); continue
        aj = ADJUST.get(i, {})
        cand[i] = dict(idx=i, sec=MOVE.get(i, o['sec']), ptype=PTYPE_FIX.get(i, o['ptype']),
                       rel=aj.get('rel',o['rel']), cambio=aj.get('cambio',o['cambio']),
                       evid=aj.get('evid',o['evid']), efecto=aj.get('efecto',o['efecto']),
                       rep=aj.get('rep',o['rep']), fi=aj.get('fi',o['fi']), acr=o.get('acr',''),
                       frase=o.get('frase',''), oblig=bool(EL[i].get('_oblig')) or i in OBLIG_EXTRA)
for c in cand.values():
    c['total'] = score(c['rel'],c['cambio'],c['evid'],c['efecto'],c['rep'],c['fi'])
    c['prio']  = prio(c['total'], c['cambio'])

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
                    rel=c['rel'],cambio=c['cambio'],evid=c['evid'],efecto=c['efecto'],
                    rep=c['rep'],fi=c['fi'], total=c['total'], prio=c['prio'],
                    oblig=c['oblig'], noabs=r['_noabs'], alt=r.get('_alt'), rec=r.get('_rec',''),
                    title=r['title'].rstrip('.'), abstract=r['abstract']))
json.dump(out, open(B+'/n22_sel.json','w'), ensure_ascii=False, indent=1)
json.dump({o['key']:o['acr'] for o in out if o['acr']}, open(B+'/n22_acr.json','w'), ensure_ascii=False, indent=1)
print(f"CANDIDATOS elegibles: {len(cand)} | descartados: {len(descartes)} (duplicados de números previos: {len(_dups)} {_dups})")
print(f"SELECCIONADOS: {len(out)}  (obligatorios: {sum(1 for o in out if o['oblig'])})")
print("por sección:", dict(sorted(Counter(o['sec'] for o in out).items())))
print("prioridad:", dict(Counter(o['prio'] for o in out)))
print("\n=== TOP 10 (Destacado + Top 3) ===")
for o in sorted(out,key=lambda x:(-x['total'],-x['cambio'],-x['efecto']))[:10]:
    print(f"  {o['key']:4} {o['total']:5} C{o['cambio']:<3}E{o['efecto']:<3} s{o['sec']:<3}{o['journal'][:22]:24}{o['title'][:62]}")
print("\n=== RECUPERADOS POR CROSSREF EN LA SELECCIÓN ===")
for o in out:
    if o.get('rec'): print('  ',o['key'],o['total'],o['prio'],'| s%d |'%o['sec'],o['journal'],'|',o['title'][:62])
print("\n=== DESPLAZADOS POR LA INCLUSIÓN OBLIGATORIA (quedaron fuera del top-5 de su sección) ===")
_sel={o['idx'] for o in out}
for c in sorted(cand.values(), key=lambda x:-x['total']):
    if c['idx'] not in _sel and c['total']>=7:
        print(f"   idx {c['idx']:3} s{c['sec']:<3}{c['total']:5} {EL[c['idx']]['journal'][:18]:19}{EL[c['idx']]['title'][:60]}")
