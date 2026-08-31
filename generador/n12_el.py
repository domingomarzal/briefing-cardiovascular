#!/usr/bin/env python3
# Elegibles N12 (24-30 ago 2026, semana ESC). Incluye INCLUSIÓN OBLIGATORIA sin abstract.
import json, os, re
D1, D2 = '2026/08/24', '2026/08/30'
BAD = {'Editorial','Comment','Letter','Published Erratum','News','Case Reports'}
B = os.path.dirname(os.path.abspath(__file__))
recs = json.load(open(B+'/n12_corpus.json'))['recs']

OBLIG_J = {'N Engl J Med','Lancet'}
# Guía/documento REAL de sociedad: patrones estrictos (evita confundir COMENTARIOS que
# solo mencionan "guidelines" en el título con la guía de verdad).
GUIA = re.compile(r'^\d{4} ESC Guidelines|ESC/\w+ Guidelines|clinical consensus statement of the|'
                  r'consensus statement of the|Scientific Statement From the|position statement of the|'
                  r'Universal Definition of Myocardial Infarction|Focused Update of the', re.I)
# Comentario/editorial sin abstract: NO entra aunque sea de NEJM/Lancet (el filtro de TIPO manda).
def es_guia(r): return bool(GUIA.search(r['title'] or ''))
def es_oblig(r):
    if es_guia(r): return True
    if r['journal'] in OBLIG_J and r['abstract']: return True   # artículo real, no comentario
    return False

win = [r for r in recs if D1 <= r['adate'] <= D2]
EL = []
for r in win:
    if set(r['ptypes']) & BAD:      # tipo no elegible -> fuera siempre
        continue
    if r['abstract'] or es_oblig(r):  # con abstract, O de inclusión obligatoria
        r['_oblig'] = es_oblig(r)
        r['_noabs'] = not bool(r['abstract'])
        EL.append(r)

# Dedup: mismo documento publicado en varias revistas (p.ej. Definición Universal en EHJ/Circulation/JACC)
def norm(t):
    s=re.sub(r'[^a-z0-9]+','',(t or '').lower())
    m=re.match(r'(fifthuniversaldefinitionofmyocardialinfarction2026)',s)
    if m: return m.group(1)
    return s[:70]
seen={}; DEDUP=[]
for r in EL:
    k=norm(r['title'])
    if k in seen:
        seen[k]['_alt']=seen[k].get('_alt',[])+[(r['journal'], r['doi'])]
        continue
    seen[k]=r; DEDUP.append(r)
EL=DEDUP
json.dump(EL, open(B+'/n12_el.json','w'), ensure_ascii=False)
print(f"En ventana: {len(win)} | ELEGIBLES tras dedup: {len(EL)}")
print(f"  de inclusión obligatoria: {sum(1 for r in EL if r['_oblig'])}")
print(f"  sin abstract (solo obligatorios): {sum(1 for r in EL if r['_noabs'])}")
