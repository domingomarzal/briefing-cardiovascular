# -*- coding: utf-8 -*-
import json
GEN="/Users/dmarzal/Documents/Claude/Briefing Cardiovascular/briefing-cardiovascular-repo/generador"
SP="/private/tmp/claude-501/-Users-dmarzal-Documents-UICAR/d72a7364-4254-40c2-a2e4-1fca2373b5ec/scratchpad"
tasks=json.load(open(GEN+"/n3_tasks.json"))
fichas={}
for b in "ABCDE":
    fichas.update(json.load(open(f"{SP}/n3_out_{b}.json")))
data={}
missing=[]
for k,t in tasks.items():
    f=fichas.get(k)
    if not f: missing.append(k); continue
    rec=dict(key=k, sec=t["sec"], ptype=t["ptype"], prio=t["prio"], journal=t["journal"],
             doi=t["doi"], total=t["total"], title_en=f["title_en"], title_es=f["title_es"],
             es=f["es"], en=f["en"])
    data[k]=rec
# validate fields
FIELDS=["resumen","why","deque","resultados","conclusiones"]
bad=[]
for k,r in data.items():
    for lang in ("es","en"):
        for fld in FIELDS:
            if not r[lang].get(fld): bad.append(f"{k}.{lang}.{fld}")
json.dump(data,open(GEN+"/n3_data.json","w"),ensure_ascii=False,indent=1)
json.dump({"a6":" (GUTS)"},open(GEN+"/n3_acr.json","w"),ensure_ascii=False)
print("merged:",len(data),"/ expected",len(tasks))
if missing: print("MISSING fichas:",missing)
if bad: print("EMPTY fields:",bad)
# sanity: dest + top3 present
for k in ["a113","a110","a18","a106"]:
    print(" key",k,"present:",k in data)
