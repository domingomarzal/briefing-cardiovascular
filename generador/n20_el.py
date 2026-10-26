#!/usr/bin/env python3
# Elegibles N20 (19-25 oct 2026). Incluye INCLUSIÓN OBLIGATORIA sin abstract.
import json, os, re
D1, D2 = '2026/10/19', '2026/10/25'
BAD = {'Editorial','Comment','Letter','Published Erratum','News','Case Reports'}
B = os.path.dirname(os.path.abspath(__file__))
recs = json.load(open(B+'/n20_corpus.json'))['recs']

# ⛔ EXCLUSIONES POR TIPO VERIFICADO EN LA FUENTE (PASO 2, regla de encaje 6):
# 10.1093/eurheartj/ehag840 = editorial semanal «Issue @ a glance» del editor de Eur Heart J
# (pp. 5893-5898, sin abstract, online 26-oct en Crossref). Su título menciona la «Fifth
# Universal Definition of Myocardial Infarction», pero NO es el documento: es el comentario
# del fascículo. Sin esta exclusión el patrón de guía lo colaría como inclusión obligatoria.
EXCL = {'10.1093/eurheartj/ehag840'}

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
        r['_oblig'] = es_oblig(r)
        r['_noabs'] = not bool(r['abstract'])
        EL.append(r)

# ⭐ RECUPERADOS (PASO 1 — «no te fíes solo del edat en las revistas nucleares»):
# J Am Coll Cardiol quedó con 0 elegibles por `edat`. El fascículo en curso es el vol 88
# núm 16, cuyo contenido de fascículo (Contents y Full Issue PDF) Crossref registró dentro
# de la ventana 19-25 oct. De ese fascículo se incorporan los dos ARTÍCULOS ORIGINALES que
# nunca habían salido en el briefing y que tienen abstract en PubMed (los de pp. e2665 son
# correspondencia y los de 2025.12.084/092 no tienen abstract: se descartan).
for f in ('/tmp/rec_j.jacc.2026.04.049.json', '/tmp/rec_j.jacc.2026.08.014.json'):
    if not os.path.exists(f): continue
    r = json.load(open(f))
    if any((e.get('doi') or '').lower() == r['doi'].lower() for e in EL): continue
    r['_oblig'] = False; r['_noabs'] = False
    r['_rec'] = 'recuperado del fascículo en curso de J Am Coll Cardiol (vol 88, nº 16) por Crossref; PubMed no lo indexó en la ventana'
    r['adate'] = '2026/10/21'
    EL.append(r)

def norm(t):
    s = re.sub(r'[^a-z0-9]+','',(t or '').lower())
    return s[:70]
seen={}; DEDUP=[]
for r in EL:
    k=norm(r['title'])
    if k in seen:
        seen[k]['_alt']=seen[k].get('_alt',[])+[(r['journal'], r['doi'])]
        continue
    seen[k]=r; DEDUP.append(r)
EL=DEDUP
json.dump(EL, open(B+'/n20_el.json','w'), ensure_ascii=False)
print(f"En ventana: {len(win)} | ELEGIBLES tras dedup: {len(EL)}")
print(f"  de inclusión obligatoria: {sum(1 for r in EL if r['_oblig'])}")
print(f"  sin abstract (solo obligatorios): {sum(1 for r in EL if r['_noabs'])}")
print(f"  recuperados: {sum(1 for r in EL if r.get('_rec'))}")
