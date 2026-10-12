#!/usr/bin/env python3
# PASO 1b (2.ª vuelta) — recuperación tras la auditoría de cobertura de N18.
# El position statement de la HRS sobre autorización previa en electrofisiología tiene
# ArticleDate 2026/10/06 (DENTRO de la ventana) pero su edat es 2026/09/17, fuera de la
# red amplia del PASO 1: por eso no estaba en el corpus. Tiene abstract y es tipo elegible.
import json, os, urllib.request, xml.etree.ElementTree as ET
B = os.path.dirname(os.path.abspath(__file__))
EU = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
PMIDS = ["42754239"]   # 10.1016/j.hrthm.2026.08.046
EL = json.load(open(B+'/n18_el.json'))
have = {(r.get('doi') or '').lower() for r in EL}
with urllib.request.urlopen(EU+f"efetch.fcgi?db=pubmed&id={','.join(PMIDS)}&retmode=xml", timeout=90) as r:
    root = ET.fromstring(r.read())
add = []
for a in root.findall('.//PubmedArticle'):
    t = a.find('.//ArticleTitle'); ttl = ''.join(t.itertext()) if t is not None else ''
    jr = a.findtext('.//Journal/ISOAbbreviation') or ''
    pts = [p.text for p in a.findall('.//PublicationType') if p.text]
    ab = ' '.join((((x.get('Label')+': ') if x.get('Label') else '')+''.join(x.itertext()))
                  for x in a.findall('.//Abstract/AbstractText')).strip()
    doi = next((e.text for e in a.findall('.//Article/ELocationID') if e.get('EIdType')=='doi'), '')
    pii = ''
    pe = a.find("./PubmedData/ArticleIdList/ArticleId[@IdType='pii']")
    if pe is not None: pii = pe.text
    pmid = a.findtext('./MedlineCitation/PMID','')
    ad = a.find('.//Article/ArticleDate')
    adate = f"{ad.findtext('Year')}/{int(ad.findtext('Month')):02d}/{int(ad.findtext('Day')):02d}" if ad is not None else ''
    if doi.lower() in have: continue
    add.append(dict(pmid=pmid, journal=jr, title=ttl, ptypes=pts, abstract=ab, doi=doi, pii=pii,
                    adate=adate, _oblig=False, _noabs=False,
                    _rec='recuperado por la auditoría de cobertura (Crossref); PubMed lo indexó con edat 17-sep, fuera de la red amplia, pero su fecha de publicación online es 6-oct, dentro de la ventana'))
rec = json.load(open(B+'/n18_rec.json')); rec += add
json.dump(rec, open(B+'/n18_rec.json','w'), ensure_ascii=False, indent=1)
idx0 = len(EL)
EL += add
json.dump(EL, open(B+'/n18_el.json','w'), ensure_ascii=False)
# ponderación manual (no hay lote de cribado para él): documento de posición de la HRS,
# alcance limitado y muy centrado en el sistema sanitario de EE. UU.
out5 = [dict(idx=idx0, elegible=True, motivo_descarte="", sec=10,
             ptype="Documento de consenso", rel=4, cambio=3, evid=6, efecto=6, rep=4, fi=4, acr="",
             frase="Documento de posición de la Heart Rhythm Society: la autorización previa de las aseguradoras retrasa o deniega procedimientos de electrofisiología indicados por guía, con daño medible al paciente.")]
json.dump(out5, open(B+'/n18_out5.json','w'), ensure_ascii=False, indent=1)
print(f"añadidos: {len(add)} | ELEGIBLES totales: {len(EL)} | idx asignado: {idx0}")
