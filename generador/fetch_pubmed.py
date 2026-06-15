#!/usr/bin/env python3
# Recupera el corpus de la semana natural anterior (lun-dom) en las 25 revistas.
# Uso: python3 fetch_pubmed.py [YYYY/MM/DD YYYY/MM/DD]  (opcional; por defecto, semana anterior)
import urllib.request,urllib.parse,json,time,sys,datetime,xml.etree.ElementTree as ET
EU="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
JOURNALS=["N Engl J Med","Lancet","JAMA","BMJ","Ann Intern Med","Nat Med","Circulation","Eur Heart J",
"J Am Coll Cardiol","JAMA Cardiol","Rev Esp Cardiol","JACC Cardiovasc Imaging","JACC Cardiovasc Interv",
"Eur J Heart Fail","JACC Heart Fail","Circ Heart Fail","Eur J Prev Cardiol","EuroIntervention","Hypertension",
"Circ Cardiovasc Interv","Eur Heart J Cardiovasc Imaging","Europace","Heart Rhythm","JACC Clin Electrophysiol","Heart"]
if len(sys.argv)>=3: d1,d2=sys.argv[1],sys.argv[2]
else:
    today=datetime.date.today(); mon=today-datetime.timedelta(days=today.weekday())
    d1=(mon-datetime.timedelta(days=7)).strftime("%Y/%m/%d"); d2=(mon-datetime.timedelta(days=1)).strftime("%Y/%m/%d")
def get(u,data=None):
    for _ in range(3):
        try:
            with urllib.request.urlopen(u,data=data,timeout=60) as r: return r.read()
        except Exception: time.sleep(2)
    return b""
pmids=set()
for j in JOURNALS:
    term=urllib.parse.quote(f'"{j}"[ta] AND {d1}:{d2}[edat]')
    try: pmids.update(json.loads(get(EU+f"esearch.fcgi?db=pubmed&term={term}&retmax=300&retmode=json"))["esearchresult"]["idlist"])
    except: pass
    time.sleep(0.34)
pmids=list(pmids); recs=[]
for i in range(0,len(pmids),120):
    xml=get(EU+"efetch.fcgi",urllib.parse.urlencode({"db":"pubmed","id":",".join(pmids[i:i+120]),"retmode":"xml"}).encode())
    try: root=ET.fromstring(xml)
    except: continue
    for a in root.findall(".//PubmedArticle"):
        t=a.find(".//ArticleTitle"); ttl="".join(t.itertext()) if t is not None else ""
        jr=a.findtext(".//Journal/ISOAbbreviation") or ""
        pts=[p.text for p in a.findall(".//PublicationType") if p.text]
        ab=" ".join((((x.get("Label")+": ") if x.get("Label") else "")+"".join(x.itertext())) for x in a.findall(".//Abstract/AbstractText")).strip()
        # DOI PROPIO del artículo: ELocationID es inequívoco (está dentro de <Article>, nunca en la
        # lista de referencias). Respaldo: el ArticleIdList PROPIO (PubmedData), NO el de las referencias
        # citadas. Usar ".//ArticleId" a secas captura los DOI de la bibliografía y enlaza al paper equivocado.
        doi=next((e.text for e in a.findall(".//Article/ELocationID") if e.get("EIdType")=="doi"),"")
        if not doi:
            ai=a.find("./PubmedData/ArticleIdList/ArticleId[@IdType='doi']")
            doi=ai.text if ai is not None else ""
        pmid=a.findtext("./MedlineCitation/PMID","")
        recs.append(dict(pmid=pmid,journal=jr,title=ttl,ptypes=pts,abstract=ab,doi=doi))
    time.sleep(0.34)
json.dump(dict(periodo=f"{d1}-{d2}",recs=recs),open("corpus.json","w"),ensure_ascii=False)
print(f"semana {d1}-{d2}: {len(recs)} artículos, {sum(1 for r in recs if r['abstract'])} con abstract -> corpus.json")
