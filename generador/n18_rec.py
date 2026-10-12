#!/usr/bin/env python3
# PASO 1b / regla "no te fíes del edat en revistas nucleares": recuperación N18.
# JACC devolvió solo 1 elegible por edat -> comprobado el fascículo (vol 88, issue 14,
# print oct-2026, dentro de la ventana) por Crossref. Un solo candidato nuevo con abstract
# y no publicado en números previos.
import json, os, urllib.request, xml.etree.ElementTree as ET
B = os.path.dirname(os.path.abspath(__file__))
EU = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
PMIDS = ["42524810"]   # 10.1016/j.jacc.2026.06.022
EL = json.load(open(B+'/n18_el.json'))
have = {(r.get('doi') or '').lower() for r in EL}
rec = []
with urllib.request.urlopen(EU+f"efetch.fcgi?db=pubmed&id={','.join(PMIDS)}&retmode=xml", timeout=90) as r:
    root = ET.fromstring(r.read())
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
    if doi.lower() in have: continue
    rec.append(dict(pmid=pmid, journal=jr, title=ttl, ptypes=pts, abstract=ab, doi=doi, pii=pii,
                    adate='2026/10/05', _oblig=False, _noabs=False,
                    _rec='recuperado del fascículo de JACC (vol 88, nº 14) vía Crossref; PubMed no lo indexó en la ventana'))
json.dump(rec, open(B+'/n18_rec.json','w'), ensure_ascii=False, indent=1)
EL += rec
json.dump(EL, open(B+'/n18_el.json','w'), ensure_ascii=False)
print(f"recuperados: {len(rec)} | ELEGIBLES totales: {len(EL)}")
