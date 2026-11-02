#!/usr/bin/env python3
# Selección y ponderación N21 (26 oct - 1 nov 2026). Semana del congreso TCT 2026.
import json, os, glob
from collections import defaultdict, Counter
B = os.path.dirname(os.path.abspath(__file__))
EL = json.load(open(B + '/n21_el.json'))

# ⭐ REUBICACIÓN POR LA REGLA DURA DE ASIGNACIÓN (PASO 4): «adiposidad y obesidad → SIEMPRE
# Cardiometabolismo». idx4 (Europace, impacto de la obesidad en la seguridad y los resultados
# a 1 año de la ablación por campo pulsado) llegó del cribado en la sección 10 por un criterio
# razonable —el objeto es la ablación y el desenlace es electrofisiológico—, pero la regla del
# usuario es explícita y el lote 2 ya había aplicado ese mismo criterio a idx53 (obesidad y
# efecto de la ablación en CABANA). Se homogeneizan los dos en la sección 2.
MOVE = {4: 2}
# ⭐ DECISIÓN EDITORIAL DEL DR. MARZAL (2-nov-2026): el ensayo SEASON-AR (TAVI en la insuficiencia
# aórtica pura, Circulation, idx43) pasa de Valvulopatías a Cardiología intervencionista, donde
# además debe salir el PRIMERO de la sección (lo fija PIN_FIRST en gen_bilingue.py).
MOVE[43] = 9

# ⭐ INCLUSIÓN OBLIGATORIA AÑADIDA A MANO (PASO 2, apartado b: «documento equivalente de las
# principales sociedades científicas»). El patrón de títulos de n21_el.py reconoce «Scientific
# Statement», «consensus statement» y «Guidelines», pero NO los rótulos «Presidential Advisory»
# ni «Science Advisory» de la AHA, que son documentos de sociedad de pleno derecho:
#   idx29 — «A Female-Specific Life Course Approach ...: A Presidential Advisory From the AHA,
#           AAP, ACOG and SMFM»
#   idx49 — «Comprehensive Centers of Excellence for Women's Cardiovascular Care: A Science
#           Advisory From the AHA»
# Junto con idx66 (el Scientific Statement de la misma iniciativa multisociedad) forman el
# paquete de la AHA sobre salud cardiovascular de la mujer publicado esta semana. Son TRES
# documentos DISTINTOS, no publicaciones simultáneas del mismo texto: no se deduplican.
OBLIG_EXTRA = {29, 49}

# TIPO: los tres son documentos de la AHA, así que llevan la misma denominación canónica
# («Scientific Statement», que es la designación de la AHA/ACC en la lista cerrada del PASO 5).
PTYPE_FIX = {29: 'Scientific Statement'}
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
    if '/n21_' in f: continue
    try: d = json.load(open(f))
    except Exception: continue
    it = d.values() if isinstance(d, dict) else d
    for v in it:
        if isinstance(v, dict) and v.get('doi'):
            PREV[v['doi'].lower()] = os.path.basename(f).split('_')[0].upper()

cand, descartes, _dups = {}, {}, []
for f in sorted(glob.glob(B+'/n21_out[0-9].json')):
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
json.dump(out, open(B+'/n21_sel.json','w'), ensure_ascii=False, indent=1)
json.dump({o['key']:o['acr'] for o in out if o['acr']}, open(B+'/n21_acr.json','w'), ensure_ascii=False, indent=1)
print(f"CANDIDATOS elegibles: {len(cand)} | descartados: {len(descartes)} (duplicados de números previos: {len(_dups)} {_dups})")
print(f"SELECCIONADOS: {len(out)}  (obligatorios: {sum(1 for o in out if o['oblig'])})")
print("por sección:", dict(sorted(Counter(o['sec'] for o in out).items())))
print("prioridad:", dict(Counter(o['prio'] for o in out)))
print("\n=== TOP 10 (Destacado + Top 3) ===")
for o in sorted(out,key=lambda x:(-x['total'],-x['cambio'],-x['efecto']))[:10]:
    print(f"  {o['key']:4} {o['total']:5} C{o['cambio']:<3}E{o['efecto']:<3} s{o['sec']:<3}{o['journal'][:22]:24}{o['title'][:62]}")
print("\n=== SECCIÓN 3 (vigilar: semana pobre en dislipemia) ===")
for o in out:
    if o['sec']==3: print('  ',o['key'],o['total'],o['journal'],'|',o['title'][:70])
