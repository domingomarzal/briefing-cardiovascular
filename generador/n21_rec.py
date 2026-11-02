#!/usr/bin/env python3
# Recuperación PASO 1b: artículos que Crossref/el editor publicó en ventana y PubMed no dio.
import urllib.request,urllib.parse,json,time,xml.etree.ElementTree as ET
EU="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
DOIS=[
 "10.1056/NEJMoa2610771",
 "10.1001/jama.2026.19090",
 "10.1016/j.jacc.2026.10.064","10.1016/j.jacc.2026.10.058","10.1016/j.jacc.2026.10.069","10.1016/j.jacc.2026.10.065",
 "10.1016/j.jcin.2026.10.001","10.1016/j.jcin.2026.09.030","10.1016/j.jcin.2026.10.024",
 "10.1016/j.jcin.2026.10.023","10.1016/j.jcin.2026.10.002","10.1016/j.jcin.2026.10.025",
 "10.1016/j.atherosclerosis.2026.121940","10.1016/j.atherosclerosis.2026.121939",
 "10.1016/j.atherosclerosis.2026.121945","10.1016/j.atherosclerosis.2026.121946",
 "10.1016/j.atherosclerosis.2026.121941","10.1016/j.atherosclerosis.2026.121944",
 "10.1016/j.atherosclerosis.2026.121947",
 "10.1093/eurjpc/zwag575",
 "10.4244/EIJ-D-26-00473","10.4244/EIJ-D-26-00575","10.4244/EIJ-D-26-00457","10.4244/EIJ-D-26-00924",
]
def get(u,data=None):
    for _ in range(4):
        try:
            with urllib.request.urlopen(u,data=data,timeout=90) as r: return r.read()
        except Exception: time.sleep(3)
    return b""
def articledate(a):
    ad=a.find(".//Article/ArticleDate")
    if ad is not None:
        y=ad.findtext("Year");m=ad.findtext("Month");d=ad.findtext("Day")
        if y and m and d: return f"{y}/{int(m):02d}/{int(d):02d}"
    for t in ("pubmed","entrez"):
        pd=a.find(f".//PubMedPubDate[@PubStatus='{t}']")
        if pd is not None:
            y=pd.findtext("Year");m=pd.findtext("Month");d=pd.findtext("Day")
            if y and m and d: return f"{y}/{int(m):02d}/{int(d):02d}"
    return ""
out=[];nf=[]
for doi in DOIS:
    ids=json.loads(get(EU+f"esearch.fcgi?db=pubmed&term={urllib.parse.quote(doi+'[aid]')}&retmode=json")).get("esearchresult",{}).get("idlist",[])
    time.sleep(0.35)
    if not ids:
        nf.append(doi); continue
    xml=get(EU+"efetch.fcgi",urllib.parse.urlencode({"db":"pubmed","id":ids[0],"retmode":"xml"}).encode())
    time.sleep(0.35)
    try: root=ET.fromstring(xml)
    except Exception: nf.append(doi); continue
    for a in root.findall(".//PubmedArticle"):
        t=a.find(".//ArticleTitle"); ttl="".join(t.itertext()) if t is not None else ""
        jr=a.findtext(".//Journal/ISOAbbreviation") or ""
        pts=[p.text for p in a.findall(".//PublicationType") if p.text]
        ab=" ".join((((x.get("Label")+": ") if x.get("Label") else "")+"".join(x.itertext())) for x in a.findall(".//Abstract/AbstractText")).strip()
        d2=next((e.text for e in a.findall(".//Article/ELocationID") if e.get("EIdType")=="doi"),doi)
        pii=""
        pe=a.find("./PubmedData/ArticleIdList/ArticleId[@IdType='pii']")
        if pe is not None: pii=pe.text
        out.append(dict(pmid=a.findtext("./MedlineCitation/PMID",""),journal=jr,title=ttl,ptypes=pts,
                        abstract=ab,doi=d2,pii=pii,adate=articledate(a),origen="crossref-cobertura"))
json.dump(out,open("n21_rec.json","w"),ensure_ascii=False,indent=1)
print("RECUPERADOS con abstract en PubMed:",sum(1 for r in out if r['abstract']),"/",len(out))
for r in out: print(f"  [{r['journal']}] {r['adate']} ab={len(r['abstract'])} {r['title'][:85]}")
print("\nNO EN PUBMED (%d):"%len(nf))
for d in nf: print("  ",d)
