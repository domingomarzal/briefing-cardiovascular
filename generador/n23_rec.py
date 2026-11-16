#!/usr/bin/env python3
# PASO 1b — RECUPERACION por Crossref de los elegibles que PubMed no trajo al corpus (N23).
import json,os,re,time,urllib.request,urllib.parse,xml.etree.ElementTree as ET
B=os.path.dirname(os.path.abspath(__file__)); EU="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
DOIS=["10.1016/j.jacc.2026.10.063","10.1016/j.jacc.2026.10.070","10.1016/j.jacc.2026.11.118",
 "10.1016/j.jchf.2026.103575","10.1016/j.jchf.2026.103574","10.1016/j.jchf.2026.103500",
 "10.1016/j.atherosclerosis.2026.121955","10.1016/j.atherosclerosis.2026.121954",
 "10.1016/j.jacadv.2026.103470","10.1016/S0140-6736(26)02043-X",
 "10.1001/jama.2026.23420","10.1001/jama.2026.23448","10.1001/jama.2026.22895",
 "10.1038/s41591-026-04752-5"]
BAD={'Editorial','Comment','Letter','Published Erratum','News','Case Reports'}
def g(u,d=None):
    for _ in range(4):
        try:
            with urllib.request.urlopen(u,data=d,timeout=90) as r: return r.read()
        except Exception: time.sleep(3)
    return b""
EL=json.load(open(B+"/n23_el.json"))
have={(r.get("doi") or "").lower() for r in EL}
add=[]
for doi in DOIS:
    if doi.lower() in have: print("ya en EL:",doi); continue
    try:
        ids=json.loads(g(EU+"esearch.fcgi?db=pubmed&retmode=json&term="+urllib.parse.quote(doi+"[doi]")))["esearchresult"]["idlist"]
    except Exception: ids=[]
    if not ids: print("NO en PubMed:",doi); continue
    x=ET.fromstring(g(EU+"efetch.fcgi",urllib.parse.urlencode({"db":"pubmed","id":ids[0],"retmode":"xml"}).encode()))
    a=x.find(".//PubmedArticle")
    t=a.find(".//ArticleTitle"); ttl="".join(t.itertext()) if t is not None else ""
    jr=a.findtext(".//Journal/ISOAbbreviation") or ""
    pts=[p.text for p in a.findall(".//PublicationType") if p.text]
    ab=" ".join((((y.get("Label")+": ") if y.get("Label") else "")+"".join(y.itertext())) for y in a.findall(".//Abstract/AbstractText")).strip()
    pii=""; pe=a.find("./PubmedData/ArticleIdList/ArticleId[@IdType='pii']")
    if pe is not None: pii=pe.text
    ad=a.find(".//Article/ArticleDate"); adate=""
    if ad is not None and ad.findtext("Year"): adate="%s/%02d/%02d"%(ad.findtext("Year"),int(ad.findtext("Month")),int(ad.findtext("Day")))
    if set(pts)&BAD: print("descartado por tipo:",doi,pts,"|",ttl[:60]); continue
    if not ab: print("descartado sin abstract:",doi,"|",ttl[:60]); continue
    add.append(dict(pmid=a.findtext("./MedlineCitation/PMID",""),journal=jr,title=ttl,ptypes=pts,
                    abstract=ab,doi=doi,pii=pii,adate=adate,_oblig=(jr in("N Engl J Med","Lancet")),
                    _noabs=False,_rec="Crossref+editor (PubMed no lo trajo al corpus)"))
    print("RECUPERADO:",jr,"|",ttl[:70],"| adate",adate)
    time.sleep(0.4)
EL.extend(add)
json.dump(EL,open(B+"/n23_el.json","w"),ensure_ascii=False)
print("\nEL final:",len(EL),"| recuperados:",len(add))
