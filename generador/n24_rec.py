#!/usr/bin/env python3
# Recuperacion PASO 1b N24: PMIDs hallados por Crossref que no estaban en el corpus de PubMed.
import urllib.request,urllib.parse,json,time,xml.etree.ElementTree as ET,os
EU="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
B=os.path.dirname(os.path.abspath(__file__))
PMIDS=["43037562","42969104"]  # NEJM semaglutide ninos; Circulation vein harvesting CABG (fasciculo)
d=json.load(open(B+"/n24_corpus.json"))
have={r["pmid"] for r in d["recs"]}
new=[p for p in PMIDS if p not in have]
if new:
    xml=urllib.request.urlopen(urllib.request.Request(EU+"efetch.fcgi",
        urllib.parse.urlencode({"db":"pubmed","id":",".join(new),"retmode":"xml"}).encode()),timeout=90).read()
    root=ET.fromstring(xml)
    for a in root.findall(".//PubmedArticle"):
        t=a.find(".//ArticleTitle"); ttl="".join(t.itertext()) if t is not None else ""
        jr=a.findtext(".//Journal/ISOAbbreviation") or ""
        pts=[p.text for p in a.findall(".//PublicationType") if p.text]
        ab=" ".join((((x.get("Label")+": ") if x.get("Label") else "")+"".join(x.itertext())) for x in a.findall(".//Abstract/AbstractText")).strip()
        doi=next((e.text for e in a.findall(".//Article/ELocationID") if e.get("EIdType")=="doi"),"")
        pii=""
        pe=a.find("./PubmedData/ArticleIdList/ArticleId[@IdType='pii']")
        if pe is not None: pii=pe.text
        ad=a.find(".//Article/ArticleDate")
        adate=""
        if ad is not None:
            y,m,dd=ad.findtext("Year"),ad.findtext("Month"),ad.findtext("Day")
            if y and m and dd: adate=f"{y}/{int(m):02d}/{int(dd):02d}"
        pmid=a.findtext("./MedlineCitation/PMID","")
        d["recs"].append(dict(pmid=pmid,journal=jr,title=ttl,ptypes=pts,abstract=ab,doi=doi,pii=pii,
                              adate=adate,_rec="recuperado por Crossref"))
        print("RECUPERADO:",pmid,jr,adate,doi,"|",ttl[:80],"| abstract:",len(ab))
    json.dump(d,open(B+"/n24_corpus.json","w"),ensure_ascii=False)
else:
    print("nada que recuperar")
