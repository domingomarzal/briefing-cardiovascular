#!/usr/bin/env python3
# Fetch corpus N3: semana 2026/06/22 - 2026/06/28 (lun-dom), 31 revistas, con ArticleDate.
import urllib.request,urllib.parse,json,time,datetime,xml.etree.ElementTree as ET
EU="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
D1,D2="2026/06/22","2026/06/28"
# Revistas con filtro temático generalista
GENERAL=["N Engl J Med","Lancet","JAMA","BMJ","Ann Intern Med","Nat Med"]
CV=["Eur Heart J","Circulation","J Am Coll Cardiol","JAMA Cardiol","Nat Rev Cardiol",
"Eur J Heart Fail","JACC Heart Fail","Circ Heart Fail","EuroIntervention","JACC Cardiovasc Interv",
"Circ Cardiovasc Interv","Heart Rhythm","Europace","JACC Clin Electrophysiol","JACC Cardiovasc Imaging",
"Eur Heart J Cardiovasc Imaging","Eur J Prev Cardiol","Hypertension","Heart","Rev Esp Cardiol",
"Atherosclerosis","J Am Heart Assoc","JACC Adv","Circ Res","Nat Cardiovasc Res"]
THEME='(cardiovascular OR cardiac OR heart OR coronary OR myocardial OR atrial OR valvular OR hypertension OR cholesterol OR lipid OR "heart failure" OR arrhythmia)'
def get(u,data=None):
    for _ in range(4):
        try:
            with urllib.request.urlopen(u,data=data,timeout=90) as r: return r.read()
        except Exception as e: time.sleep(3)
    return b""
pmids=set()
def esearch(term):
    try:
        return json.loads(get(EU+f"esearch.fcgi?db=pubmed&term={urllib.parse.quote(term)}&retmax=400&retmode=json"))["esearchresult"]["idlist"]
    except: return []
for j in CV:
    pmids.update(esearch(f'"{j}"[ta] AND {D1}:{D2}[edat]')); time.sleep(0.34)
for j in GENERAL:
    pmids.update(esearch(f'"{j}"[ta] AND {D1}:{D2}[edat] AND {THEME}')); time.sleep(0.34)
pmids=list(pmids); recs=[]
def articledate(a):
    ad=a.find(".//Article/ArticleDate")
    if ad is not None:
        y=ad.findtext("Year");m=ad.findtext("Month");d=ad.findtext("Day")
        if y and m and d: return f"{y}/{int(m):02d}/{int(d):02d}"
    # respaldo: entrez/pubmed history
    for t in ("pubmed","entrez"):
        pd=a.find(f".//PubMedPubDate[@PubStatus='{t}']")
        if pd is not None:
            y=pd.findtext("Year");m=pd.findtext("Month");d=pd.findtext("Day")
            if y and m and d: return f"{y}/{int(m):02d}/{int(d):02d}"
    return ""
for i in range(0,len(pmids),120):
    xml=get(EU+"efetch.fcgi",urllib.parse.urlencode({"db":"pubmed","id":",".join(pmids[i:i+120]),"retmode":"xml"}).encode())
    try: root=ET.fromstring(xml)
    except: continue
    for a in root.findall(".//PubmedArticle"):
        t=a.find(".//ArticleTitle"); ttl="".join(t.itertext()) if t is not None else ""
        jr=a.findtext(".//Journal/ISOAbbreviation") or ""
        pts=[p.text for p in a.findall(".//PublicationType") if p.text]
        ab=" ".join((((x.get("Label")+": ") if x.get("Label") else "")+"".join(x.itertext())) for x in a.findall(".//Abstract/AbstractText")).strip()
        doi=next((e.text for e in a.findall(".//Article/ELocationID") if e.get("EIdType")=="doi"),"")
        if not doi:
            ai=a.find("./PubmedData/ArticleIdList/ArticleId[@IdType='doi']"); doi=ai.text if ai is not None else ""
        pii=""
        pe=a.find("./PubmedData/ArticleIdList/ArticleId[@IdType='pii']")
        if pe is not None: pii=pe.text
        pmid=a.findtext("./MedlineCitation/PMID","")
        recs.append(dict(pmid=pmid,journal=jr,title=ttl,ptypes=pts,abstract=ab,doi=doi,pii=pii,adate=articledate(a)))
    time.sleep(0.34)
json.dump(dict(periodo=f"{D1}-{D2}",recs=recs),open("n3_corpus.json","w"),ensure_ascii=False)
inwin=sum(1 for r in recs if D1<=r["adate"]<=D2)
print(f"semana {D1}-{D2}: {len(recs)} arts ({sum(1 for r in recs if r['abstract'])} con abstract); {inwin} con ArticleDate en ventana -> n3_corpus.json")
