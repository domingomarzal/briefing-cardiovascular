#!/usr/bin/env python3
# PASO 7b (1) — ENLACES DIRECTOS DEL EDITOR, version nube (User-Agent generico, sin datos
# personales). Equivalente a enlaces_directos.py: escribe n<N>_jlinks.json {clave: URL}.
#   familia JACC -> jacc.org (salvo las excepciones de n<N>_jacc_pii.json, que van por PII)
#   revistas AHA (10.1161) -> ahajournals.org · NEJM -> nejm.org/doi/full
#   Lancet -> thelancet.com/.../PII<pii puntuado>/fulltext
#   resto de Elsevier -> sciencedirect.com/science/article/pii/<pii plano>
#   EuroIntervention (10.4244) -> eurointervention.pcronline.com/doi/<DOI>
#   lo demas se queda en doi.org (no se escribe)
import json,os,re,sys,time,urllib.request
B=os.path.dirname(os.path.abspath(__file__)); N=sys.argv[1] if len(sys.argv)>1 else "23"
UA="BriefingCardiovascular/1.0 (academic literature monitoring)"
SEL=json.load(open(f"{B}/n{N}_sel.json"))
EXC=set(json.load(open(f"{B}/n{N}_jacc_pii.json"))) if os.path.exists(f"{B}/n{N}_jacc_pii.json") else set()
if len(sys.argv)>2 and sys.argv[2]=="--pii":
    EXC |= set(sys.argv[3:]); json.dump(sorted(EXC),open(f"{B}/n{N}_jacc_pii.json","w"))
JACC=re.compile(r"^10\.1016/j\.(jacc|jacadv|jchf|jcin|jcmg|jacep)\.",re.I)
def pii_plano(p): return re.sub(r"[^A-Za-z0-9]","",p or "")
def pii_punt(p):
    # Lancet: la forma puntuada canonica es S0140-6736(26)02140-9. Si el PII de origen ya
    # viene puntuado se respeta tal cual; si viene plano se reconstruye.
    if p and "(" in p: return p
    q=pii_plano(p)
    if len(q)==17 and q[0].upper()=="S":
        return f"{q[0:5]}-{q[5:9]}({q[9:11]}){q[11:16]}-{q[16:]}"
    return p
def crossref_pii(doi):
    try:
        rq=urllib.request.Request("https://api.crossref.org/works/"+doi,headers={"User-Agent":UA})
        m=json.loads(urllib.request.urlopen(rq,timeout=45).read())["message"]
        for a in m.get("alternative-id",[]):
            if a.upper().startswith("S"): return a
    except Exception: pass
    return ""
out={}
for s in SEL:
    doi=(s.get("doi") or "").strip(); k=s["key"]
    if not doi: continue
    if doi.lower().startswith("10.1056/"): out[k]=f"https://www.nejm.org/doi/full/{doi}"
    elif doi.lower().startswith("10.1161/"): out[k]=f"https://www.ahajournals.org/doi/{doi}"
    elif doi.lower().startswith("10.4244/"): out[k]=f"https://eurointervention.pcronline.com/doi/{doi}"
    elif JACC.match(doi) and k not in EXC: out[k]=f"https://www.jacc.org/doi/{doi}"
    elif doi.lower().startswith("10.1016/"):
        pii=s.get("pii") or crossref_pii(doi); time.sleep(0.3)
        if not pii: continue
        if re.match(r"^10\.1016/s0140-6736",doi,re.I):
            out[k]=f"https://www.thelancet.com/journals/lancet/article/PII{pii_punt(pii)}/fulltext"
        else:
            out[k]=f"https://www.sciencedirect.com/science/article/pii/{pii_plano(pii)}"
json.dump(out,open(f"{B}/n{N}_jlinks.json","w"),ensure_ascii=False,indent=1)
import collections,urllib.parse
print(len(out),"enlaces directos ->",f"n{N}_jlinks.json")
print(collections.Counter(urllib.parse.urlparse(v).netloc for v in out.values()))
for k,v in list(out.items())[:4]: print("  ",k,v)
