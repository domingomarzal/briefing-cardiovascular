#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificador de enlaces del briefing.

  python3 check_links.py n7                 -> valida DOIs y lista lo que hay que mirar a ojo
  python3 check_links.py n7 a20 a33 a44     -> escribe n7_linkfix.json con esas claves rotas

POR QUÉ EXISTE (N7, 27-jul-2026)
--------------------------------
Cuatro artículos de la familia JACC tenían el DOI correcto y registrado, pero el enlace no
aterrizaba en el artículo: doi.org redirige a linkinghub.elsevier.com y este, mediante un
salto por JavaScript, rebotaba a la RAÍZ de jacc.org mostrando "Page Not Found". No es un
problema de DOI: es un hueco de la plataforma del editor, y afecta a unos artículos sí y a
otros no dentro del mismo fascículo, sin patrón previsible por metadatos (se comprobó: ni el
fascículo ni el estado "in press / Just Accepted" lo explican).

CÓMO SE COMPRUEBA (importante para no perder el tiempo)
------------------------------------------------------
- curl NO sirve: linkinghub devuelve 200 y el salto final lo hace JavaScript.
- Chrome headless NO sirve: jacc.org, sciencedirect, ahajournals, OUP y BMJ responden con el
  reto antibot de Cloudflare ("Just a moment...") y todo saldría como OK falso.
- Lo único que atraviesa Cloudflare es el panel de navegador (mcp__Claude_Browser__*), con un
  navegador real. Por eso el paso 2 de abajo es semiautomático: se abre cada enlace del
  subconjunto de riesgo y se mira el <title>. Si pone "Page Not Found", esa clave va rota.

QUÉ HACE ESTE SCRIPT
--------------------
PASO 1 (automático): valida contra Crossref que TODOS los DOIs existen y que el título
registrado se corresponde con el nuestro. Esto caza DOIs equivocados o intercambiados.
PASO 2 (te dice qué mirar): imprime la lista de artículos "de riesgo" — los alojados en
Elsevier, que son los que enrutan por linkinghub — con su URL, para abrirlos en el panel de
navegador. El resto (AHA, JAMA, OUP, BMJ, Nature) resuelve directo y no ha dado problemas.
PASO 3 (cuando le pasas claves): escribe n<n>_linkfix.json apuntando a PubMed, que siempre
resuelve y ofrece el enlace al editor. gen_bilingue.py lo aplica automáticamente.
"""
import json, os, sys, urllib.request, urllib.parse, concurrent.futures as cf

G = os.path.dirname(os.path.abspath(__file__))
NUM = sys.argv[1] if len(sys.argv) > 1 else "n7"
ROTOS = sys.argv[2:]
UA = {"User-Agent": "BriefingCV/1.0 (mailto:domingo.marzal@gmail.com)"}
# Revistas alojadas en Elsevier -> enrutan por linkinghub -> subconjunto de riesgo
ELSEVIER = ("JACC", "J Am Coll Cardiol", "Heart Rhythm", "Atherosclerosis", "EuroIntervention")

data = json.load(open(f"{G}/{NUM}_data.json"))
sel = {s["key"]: s for s in json.load(open(f"{G}/{NUM}_sel.json"))}
norm = lambda s: "".join(c.lower() for c in s if c.isalnum())[:55]


def crossref(k):
    try:
        req = urllib.request.Request(
            "https://api.crossref.org/works/" + urllib.parse.quote(data[k]["doi"]), headers=UA)
        with urllib.request.urlopen(req, timeout=45) as f:
            m = json.loads(f.read())["message"]
        return k, 200, (m.get("title") or [""])[0]
    except urllib.error.HTTPError as e:
        return k, e.code, ""
    except Exception as e:
        return k, "ERR", type(e).__name__


def pubmed_ok(pmid, title):
    try:
        req = urllib.request.Request(f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                                     headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=45) as f:
            return title[:40].lower() in f.read().decode("utf-8", "replace").lower()
    except Exception:
        return False


print(f"PASO 1 — validación de DOIs contra Crossref ({len(data)} artículos)")
res = {}
with cf.ThreadPoolExecutor(8) as ex:
    for k, st, t in ex.map(crossref, data): res[k] = (st, t)
sin = [k for k, v in res.items() if v[0] != 200]
mal = [k for k, v in res.items() if v[0] == 200 and norm(v[1]) and norm(v[1]) not in norm(data[k]["title_en"])]
for k in sorted(sin): print(f"   DOI NO REGISTRADO  {k:5} {data[k]['doi']}")
for k in sorted(mal):
    print(f"   TÍTULO NO CUADRA   {k:5} {data[k]['doi']}\n      nuestro : {data[k]['title_en'][:70]}\n      crossref: {res[k][1][:70]}")
print(f"   -> {len(data)-len(sin)-len(mal)}/{len(data)} DOIs correctos\n")

riesgo = [k for k in data if any(e in data[k]["journal"] for e in ELSEVIER)]
print(f"PASO 2 — abrir a ojo en el panel de navegador ({len(riesgo)} de riesgo, alojados en Elsevier).")
print("         Si el <title> dice 'Page Not Found', anota la clave.")
for k in sorted(riesgo, key=lambda x: int(x[1:])):
    mark = "  [YA MARCADO ROTO]" if k in ROTOS else ""
    print(f"   {k:5} {data[k]['journal'][:22]:24} https://doi.org/{data[k]['doi']}{mark}")

if ROTOS:
    fix = {}
    print(f"\nPASO 3 — sustituyendo {len(ROTOS)} enlaces rotos por su página de PubMed")
    for k in ROTOS:
        pmid = sel[k]["pmid"]
        ok = pubmed_ok(pmid, data[k]["title_en"])
        print(f"   {k:5} pmid={pmid} verificado={ok}")
        if not ok: raise SystemExit(f"ABORTADO: PubMed no confirma {k}")
        fix[k] = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
    json.dump(fix, open(f"{G}/{NUM}_linkfix.json", "w"), ensure_ascii=False, indent=1)
    print(f"   -> {NUM}_linkfix.json ({len(fix)} sustituciones). Regenera con gen_bilingue.py.")
else:
    print(f"\n(Para escribir el mapa: python3 check_links.py {NUM} <clave> <clave> ...)")
