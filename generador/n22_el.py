#!/usr/bin/env python3
# Elegibles N22 (2 - 8 nov 2026). Semana del congreso AHA 2026.
import json, os, re
D1, D2 = '2026/11/02', '2026/11/08'
BAD = {'Editorial','Comment','Letter','Published Erratum','News','Case Reports'}
B = os.path.dirname(os.path.abspath(__file__))
recs = json.load(open(B+'/n22_corpus.json'))['recs']
EXCL = set()
OBLIG_J = {'N Engl J Med','Lancet'}
GUIA = re.compile(r'^\d{4} [A-Z/]{2,} Guideline|^\d{4} ESC Guidelines|ESC/\w+ Guidelines|'
                  r'clinical consensus statement|consensus statement|Scientific Statement|'
                  r'position statement|position paper|consensus document|'
                  r'Universal Definition of|Focused Update of the', re.I)
def es_guia(r): return bool(GUIA.search(r['title'] or ''))
def es_oblig(r):
    if (r.get('doi') or '').lower() in EXCL: return False
    if es_guia(r): return True
    if r['journal'] in OBLIG_J and r['abstract']: return True
    return False
win = [r for r in recs if D1 <= r['adate'] <= D2]
EL = []
for r in win:
    if (r.get('doi') or '').lower() in EXCL: continue
    if set(r['ptypes']) & BAD: continue
    if r['abstract'] or es_oblig(r):
        r['_oblig'] = es_oblig(r); r['_noabs'] = not bool(r['abstract'])
        EL.append(r)

def norm(t): return re.sub(r'[^a-z0-9]+','',(t or '').lower())[:70]
seen={}; DEDUP=[]
for r in EL:
    k=norm(r['title'])
    if k in seen:
        seen[k]['_alt']=seen[k].get('_alt',[])+[(r['journal'], r['doi'])]; continue
    seen[k]=r; DEDUP.append(r)
EL=DEDUP
json.dump(EL, open(B+'/n22_el.json','w'), ensure_ascii=False)
print(f"En ventana: {len(win)} | ELEGIBLES tras dedup: {len(EL)}")
print(f"  de inclusión obligatoria: {sum(1 for r in EL if r['_oblig'])}")
print(f"  sin abstract (solo obligatorios): {sum(1 for r in EL if r['_noabs'])}")
for r in EL:
    if r['_oblig']: print('   OBLIG:', r['journal'],'|', r['title'][:95])
