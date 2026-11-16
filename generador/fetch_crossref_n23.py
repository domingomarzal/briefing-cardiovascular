#!/usr/bin/env python3
# Barrido Crossref N23 (ventana 2026-11-09..2026-11-15): NEJM, Lancet, EuroIntervention
# + fasciculo en curso de JACC / Eur Heart J / Circulation.
import urllib.request,json,time
UA="BriefingCardiovascular/1.0 (academic literature monitoring; https://domingomarzal.github.io/briefing-cardiovascular/)"
D1,D2="2026-11-09","2026-11-15"
def get(u):
    for _ in range(4):
        try:
            rq=urllib.request.Request(u,headers={"User-Agent":UA})
            with urllib.request.urlopen(rq,timeout=90) as r: return json.loads(r.read())
        except Exception as e:
            time.sleep(3)
    return {}
out={}
SEL="DOI,title,created,issued,published-online,published-print,type,volume,issue,container-title"
for name,issn in [("N Engl J Med","0028-4793"),("Lancet","0140-6736")]:
    u=f"https://api.crossref.org/journals/{issn}/works?filter=from-online-pub-date:{D1},until-online-pub-date:{D2}&rows=200&select={SEL}"
    out[name]=get(u).get("message",{}).get("items",[]); time.sleep(1)
u=f"https://api.crossref.org/journals/1969-6213/works?filter=from-created-date:{D1},until-created-date:{D2},type:journal-article&rows=200&select={SEL}"
out["EuroIntervention"]=get(u).get("message",{}).get("items",[]); time.sleep(1)
for name,issn in [("J Am Coll Cardiol","0735-1097"),("Eur Heart J","0195-668X"),("Circulation","0009-7322")]:
    u=(f"https://api.crossref.org/journals/{issn}/works?filter=from-pub-date:2026-11-01,until-pub-date:{D2},"
       f"type:journal-article&rows=150&select={SEL}&sort=published&order=desc")
    out[name+" (fasciculo)"]=get(u).get("message",{}).get("items",[]); time.sleep(1)
json.dump(out,open("n23_crossref.json","w"),ensure_ascii=False)
for k,v in out.items(): print(k,len(v))
