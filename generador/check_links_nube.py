#!/usr/bin/env python3
# PASO 7b (2) — VALIDACION DE ENLACES, version nube (User-Agent generico, sin datos personales).
# Equivalente a la parte de Crossref de check_links.py: comprueba que cada DOI del numero existe
# en Crossref y que el titulo registrado cuadra con el nuestro (caza DOI equivocados).
# NO sustituye a la revision uno a uno en navegador real (regla dura del usuario del 14/09/2026),
# que la nube NO puede hacer: su red no alcanza a los editores. Esa parte queda anotada en
# n<N>_linkcheck_pendiente.json para que la cierre el Mac.
import json, os, re, sys, time, urllib.request, urllib.parse
B = os.path.dirname(os.path.abspath(__file__))
N = (sys.argv[1] if len(sys.argv) > 1 else "n23").lstrip("n")
UA = "BriefingCardiovascular/1.0 (academic literature monitoring)"
SEL = json.load(open(f"{B}/n{N}_sel.json"))
JL = json.load(open(f"{B}/n{N}_jlinks.json")) if os.path.exists(f"{B}/n{N}_jlinks.json") else {}
FIX = json.load(open(f"{B}/n{N}_linkfix.json")) if os.path.exists(f"{B}/n{N}_linkfix.json") else {}

def norm(t):
    return re.sub(r"[^a-z0-9]+", "", (t or "").lower())[:60]

def crossref(doi):
    try:
        rq = urllib.request.Request("https://api.crossref.org/works/" + urllib.parse.quote(doi),
                                    headers={"User-Agent": UA})
        with urllib.request.urlopen(rq, timeout=45) as r:
            return json.loads(r.read())["message"]
    except Exception as e:
        return {"_err": str(e)}

ok, avisos, sinregistro = 0, [], []
for s in SEL:
    doi, k = (s.get("doi") or "").strip(), s["key"]
    if not doi:
        avisos.append((k, "SIN DOI", s["title"][:70])); continue
    m = crossref(doi); time.sleep(0.35)
    if "_err" in m:
        # Puede ser rate-limiting de Crossref: se reintenta una vez antes de dar el aviso.
        time.sleep(3); m = crossref(doi)
    if "_err" in m:
        sinregistro.append((k, doi, m["_err"][:40])); continue
    tit = (m.get("title") or [""])[0]
    if norm(tit) and norm(tit)[:40] != norm(s["title"])[:40]:
        avisos.append((k, "TITULO NO CUADRA", f"{doi} -> {tit[:70]}"))
    else:
        ok += 1

print(f"DOI verificados en Crossref: {ok}/{len(SEL)}")
for k, m, d in avisos:
    print(f"  AVISO {k}: {m} | {d}")
for k, d, e in sinregistro:
    print(f"  NO RESUELTO {k}: {d} ({e}) — comprobar suelto antes de tocar nada (falso positivo habitual por rate-limiting)")

# Subconjunto de RIESGO para la revision en navegador real del Mac: todo lo que NO va por doi.org
# (editores con muro de Cloudflare: jacc.org, sciencedirect, ahajournals, nejm.org, thelancet).
riesgo = {}
for s in SEL:
    k = s["key"]
    url = FIX.get(k) or JL.get(k)
    if url:
        riesgo[k] = dict(url=url, journal=s["journal"], doi=s.get("doi", ""), title=s["title"][:110])
pend = dict(
    numero=f"n{N}",
    motivo="nube",
    explicacion=("La revisión uno a uno de los enlaces en un navegador real (PASO 7b) NO se puede "
                 "completar desde la nube: la política de red del entorno no permite el CONNECT a "
                 "doi.org, jacc.org, sciencedirect.com, ahajournals.org, nejm.org ni thelancet.com "
                 "(fallan con HTTP 000 / ENOTFOUND). La validación de DOI contra Crossref SÍ se hizo "
                 "y está resumida arriba."),
    verificado_crossref=f"{ok}/{len(SEL)} DOI registrados y con título coincidente",
    avisos=[{"clave": k, "aviso": m, "detalle": d} for k, m, d in avisos],
    no_resueltos=[{"clave": k, "doi": d, "error": e} for k, d, e in sinregistro],
    pendientes=riesgo,
    que_hacer_en_el_mac=("python3 generador/revisar_enlaces.py %s y abrir las tandas con Chrome real; "
                         "los que den «Page Not Found» se redirigen con "
                         "python3 generador/enlaces_directos.py %s --pii <claves> y se regenera." % (N, N)))
json.dump(pend, open(f"{B}/n{N}_linkcheck_pendiente.json", "w"), ensure_ascii=False, indent=1)
print(f"\nn{N}_linkcheck_pendiente.json escrito: {len(riesgo)} enlaces del subconjunto de riesgo "
      f"(editores con Cloudflare) pendientes de revisión en el Mac.")
