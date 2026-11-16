#!/usr/bin/env python3
# PASO 1b/0.2.b — AUDITORIA DE COBERTURA N23 (version nube, User-Agent generico sin datos
# personales). Compara, revista a revista, lo que el EDITOR deposito en Crossref dentro de la
# ventana con lo que el corpus de PubMed recogio. Descarta REDEPOSITOS comparando la fecha real
# de publicacion (published-online / published-print / issued) con la ventana.
import json,urllib.request,urllib.parse,time,sys,os
B=os.path.dirname(os.path.abspath(__file__))
UA="BriefingCardiovascular/1.0 (academic literature monitoring; https://domingomarzal.github.io/briefing-cardiovascular/)"
D1,D2="2026-11-09","2026-11-15"
WINMONTHS={(2026,11)}
ISSN={
 "N Engl J Med":"0028-4793","Lancet":"0140-6736","JAMA":"0098-7484","Eur Heart J":"0195-668X",
 "Circulation":"0009-7322","J Am Coll Cardiol":"0735-1097","JAMA Cardiol":"2380-6583",
 "Nat Rev Cardiol":"1759-5002","Eur J Heart Fail":"1388-9842","JACC Heart Fail":"2213-1779",
 "Circ Heart Fail":"1941-3289","EuroIntervention":"1969-6213","JACC Cardiovasc Interv":"1936-8798",
 "Circ Cardiovasc Interv":"1941-7640","Heart Rhythm":"1547-5271","Europace":"1099-5129",
 "JACC Clin Electrophysiol":"2405-500X","JACC Cardiovasc Imaging":"1936-878X",
 "Eur Heart J Cardiovasc Imaging":"2047-2404","Eur J Prev Cardiol":"2047-4873",
 "Hypertension":"0194-911X","Heart":"1355-6037","Rev Esp Cardiol (Engl Ed)":"1885-5857",
 "Atherosclerosis":"0021-9150","J Am Heart Assoc":"2047-9980","JACC Adv":"2772-963X",
 "BMJ":"0959-8138","Ann Intern Med":"0003-4819","Nat Med":"1078-8956",
 "Circ Res":"0009-7330","Nat Cardiovasc Res":"2731-0590"}
def get(u):
    for _ in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA}),timeout=90) as r:
                return json.loads(r.read())
        except Exception: time.sleep(4)
    return {}
def realdate(it):
    for k in ("published-online","published-print","issued"):
        dp=(it.get(k) or {}).get("date-parts") or []
        if dp and dp[0] and dp[0][0]: return dp[0]
    return None
def en_ventana(it):
    dp=realdate(it)
    if not dp: return False
    if len(dp)>=3:
        d="%04d-%02d-%02d"%(dp[0],dp[1],dp[2])
        return D1<=d<=D2
    if len(dp)==2: return (dp[0],dp[1]) in WINMONTHS
    return False
corpus=json.load(open(B+"/n23_corpus.json"))["recs"]
have={(r.get("doi") or "").lower() for r in corpus if r.get("doi")}
res={}; faltan=[]
for nm,issn in ISSN.items():
    u=(f"https://api.crossref.org/journals/{issn}/works?filter=from-created-date:{D1},"
       f"until-created-date:{D2},type:journal-article&rows=300"
       f"&select=DOI,title,created,issued,published-online,published-print,type")
    items=get(u).get("message",{}).get("items",[])
    pub=[i for i in items if en_ventana(i)]
    miss=[i for i in pub if i["DOI"].lower() not in have]
    res[nm]=dict(depositados=len(items),en_ventana=len(pub),recogidos=len(pub)-len(miss),faltantes=len(miss),
                 faltantes_detalle=[dict(doi=i["DOI"],title=(i.get("title") or [""])[0]) for i in miss])
    for i in miss: faltan.append((nm,i["DOI"],(i.get("title") or [""])[0]))
    print(f"{nm:32} depos {len(items):4} | ventana {len(pub):4} | recogidos {len(pub)-len(miss):4} | FALTAN {len(miss):4}")
    time.sleep(1)
json.dump(res,open(B+"/n23_cobertura.json","w"),ensure_ascii=False,indent=1)
print("\n=== FALTANTES (detalle) ===")
for nm,doi,t in faltan: print(f"  {nm:28} {doi:36} {t[:78]}")
print("TOTAL faltantes:",len(faltan))
