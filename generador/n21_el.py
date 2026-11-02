#!/usr/bin/env python3
# Elegibles N21 (26 oct - 1 nov 2026). Semana del congreso TCT 2026.
import json, os, re
D1, D2 = '2026/10/26', '2026/11/01'
BAD = {'Editorial','Comment','Letter','Published Erratum','News','Case Reports'}
B = os.path.dirname(os.path.abspath(__file__))
recs = json.load(open(B+'/n21_corpus.json'))['recs']
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

# ⭐ RECUPERADO POR CROSSREF (PASO 1b) — N Engl J Med, INCLUSIÓN OBLIGATORIA.
# El ensayo P4 (CCTA frente a IVUS para guiar la ICP) se presentó como late-breaker en el
# TCT 2026 el 1-nov y se publicó el mismo día en NEJM (Crossref: online 2026-11-01).
# PubMed NO lo había indexado (0 registros por DOI el 2-nov). Como es un artículo CV de NEJM,
# es de INCLUSIÓN OBLIGATORIA y la falta de abstract NO lo descarta (PASO 2, excepción crítica).
# La nube NO alcanza a nejm.org ni a escardio/TCTMD (egreso denegado), así que la ficha se
# redacta con el diseño verificado (registro del ensayo + artículo de diseño del propio
# equipo en EuroIntervention 10.4244/EIJ-D-26-00924) y SIN cifras: las cifras del resultado
# primario solo constan en la nota de prensa del patrocinador y venían truncadas, así que se
# OMITEN (regla de rigor del usuario) y se remite al artículo original.
EL.append(dict(pmid='', journal='N Engl J Med', title='Coronary CT Angiography versus Intravascular Ultrasound Guidance for PCI',
    ptypes=['Randomized Controlled Trial'], abstract='', doi='10.1056/NEJMoa2610771', pii='',
    adate='2026/11/01', _oblig=True, _noabs=True,
    _rec='recuperado por Crossref (PASO 1b): late-breaker del TCT 2026 publicado en NEJM el 1-nov; PubMed no lo había indexado'))

def norm(t): return re.sub(r'[^a-z0-9]+','',(t or '').lower())[:70]
seen={}; DEDUP=[]
for r in EL:
    k=norm(r['title'])
    if k in seen:
        seen[k]['_alt']=seen[k].get('_alt',[])+[(r['journal'], r['doi'])]; continue
    seen[k]=r; DEDUP.append(r)
EL=DEDUP
json.dump(EL, open(B+'/n21_el.json','w'), ensure_ascii=False)
print(f"En ventana: {len(win)} | ELEGIBLES tras dedup: {len(EL)}")
print(f"  de inclusión obligatoria: {sum(1 for r in EL if r['_oblig'])}")
print(f"  sin abstract (solo obligatorios): {sum(1 for r in EL if r['_noabs'])}")
for r in EL:
    if r['_oblig']: print('   OBLIG:', r['journal'],'|', r['title'][:95])
