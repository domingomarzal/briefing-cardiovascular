#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Barrido COMPLEMENTARIO por Crossref de N Engl J Med y Lancet para la ventana del número.
Motivo (31/08/2026): PubMed NO indexa a tiempo los late-breakers de NEJM del congreso ESC
(en la semana 24-30 ago PubMed solo tenía 6 registros de NEJM; faltaban 9 artículos originales).
Crossref sí los tiene desde el minuto uno porque el editor deposita el DOI al publicar."""
import urllib.request, urllib.parse, json, time, sys

D1, D2 = "2026-08-24", "2026-08-30"
JOURNALS = {"N Engl J Med": "0028-4793", "Lancet": "0140-6736"}
UA = {"User-Agent": "BriefingCardiovascular/1.0 (mailto:domingo.marzal@gmail.com)"}

def get(u):
    req = urllib.request.Request(u, headers=UA)
    for _ in range(4):
        try:
            with urllib.request.urlopen(req, timeout=90) as r: return r.read()
        except Exception: time.sleep(3)
    return b"{}"

# Tipo por prefijo del DOI de NEJM (el editor lo codifica ahí)
NEJM_OK  = ("nejmoa", "nejmra", "nejmcp", "nejmsa", "nejmsr")      # originales, revisiones, práctica clínica
NEJM_BAD = ("nejme", "nejmc", "nejmp", "nejmicm", "nejmclde")      # editorial, carta, perspectiva, imagen

out = []
for jname, issn in JOURNALS.items():
    off = 0
    while True:
        u = (f"https://api.crossref.org/journals/{issn}/works?"
             f"filter=from-online-pub-date:{D1},until-online-pub-date:{D2}&rows=200&offset={off}")
        d = json.loads(get(u)).get("message", {})
        items = d.get("items", [])
        if not items: break
        for m in items:
            doi = (m.get("DOI") or "").lower()
            ttl = (m.get("title") or [""])[0]
            if not ttl: continue
            tipo = "?"
            if jname == "N Engl J Med":
                base = doi.split("/")[-1]
                if base.startswith(NEJM_BAD): tipo = "NO ELEGIBLE (editorial/carta/perspectiva)"
                elif base.startswith(NEJM_OK): tipo = "ELEGIBLE"
                else: tipo = "revisar"
            else:
                tipo = "revisar"
            pub = m.get("published-online", {}).get("date-parts", [[None]])[0]
            out.append(dict(journal=jname, doi=m.get("DOI"), title=ttl, tipo=tipo,
                            online="-".join(str(x) for x in pub) if pub and pub[0] else ""))
        off += 200
        time.sleep(0.4)

json.dump(out, open("n12_crossref.json", "w"), ensure_ascii=False, indent=1)
print(f"Crossref: {len(out)} registros de NEJM/Lancet publicados online entre {D1} y {D2}")
for j in JOURNALS:
    sub = [o for o in out if o["journal"] == j]
    print(f"  {j}: {len(sub)}  (elegibles por prefijo: {sum(1 for o in sub if o['tipo']=='ELEGIBLE')})")
