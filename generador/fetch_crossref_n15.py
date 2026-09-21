#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PASO 1b — barrido Crossref de N Engl J Med, Lancet y EuroIntervention (ventana N15)."""
import urllib.request, json, time

D1, D2 = "2026-09-14", "2026-09-20"
UA = {"User-Agent": "BriefingCardiovascular/1.0 (mailto:domingo.marzal@gmail.com)"}
NEJM_OK  = ("nejmoa", "nejmra", "nejmcp", "nejmsa", "nejmsr")
NEJM_BAD = ("nejme", "nejmc", "nejmp", "nejmicm", "nejmclde")

def get(u):
    req = urllib.request.Request(u, headers=UA)
    for _ in range(4):
        try:
            with urllib.request.urlopen(req, timeout=90) as r: return r.read()
        except Exception: time.sleep(3)
    return b"{}"

def barre(url):
    out, off = [], 0
    while True:
        d = json.loads(get(url + f"&offset={off}")).get("message", {})
        items = d.get("items", [])
        if not items: break
        out += items
        off += 200
        time.sleep(0.4)
        if off > 1000: break
    return out

out = []
for jname, issn in (("N Engl J Med", "0028-4793"), ("Lancet", "0140-6736")):
    u = (f"https://api.crossref.org/journals/{issn}/works?"
         f"filter=from-online-pub-date:{D1},until-online-pub-date:{D2}&rows=200")
    for m in barre(u):
        doi = (m.get("DOI") or "").lower(); ttl = (m.get("title") or [""])[0]
        if not ttl: continue
        tipo = "revisar"
        if jname == "N Engl J Med":
            base = doi.split("/")[-1]
            tipo = ("NO ELEGIBLE (editorial/carta/perspectiva)" if base.startswith(NEJM_BAD)
                    else "ELEGIBLE" if base.startswith(NEJM_OK) else "revisar")
        pub = m.get("published-online", {}).get("date-parts", [[None]])[0]
        out.append(dict(journal=jname, doi=m.get("DOI"), title=ttl, tipo=tipo,
                        online="-".join(str(x) for x in pub) if pub and pub[0] else ""))

# EuroIntervention: no deposita online-pub-date -> filtro por created + descarte de redepósitos
u = ("https://api.crossref.org/journals/1969-6213/works?"
     f"filter=from-created-date:{D1},until-created-date:{D2},type:journal-article&rows=200"
     "&select=DOI,title,created,issued,published-online")
for m in barre(u):
    ttl = (m.get("title") or [""])[0]
    if not ttl: continue
    iss = m.get("published-online") or m.get("issued") or {}
    dp = (iss.get("date-parts") or [[None]])[0]
    fecha = "-".join(str(x) for x in dp) if dp and dp[0] else ""
    # descarta redepósitos de artículos antiguos: solo mes de la ventana
    if fecha and not fecha.startswith("2026-9") and not fecha.startswith("2026-09"): continue
    out.append(dict(journal="EuroIntervention", doi=m.get("DOI"), title=ttl,
                    tipo="revisar", online=fecha))

json.dump(out, open("n15_crossref.json", "w"), ensure_ascii=False, indent=1)
print(f"Crossref: {len(out)} registros {D1}..{D2}")
for j in ("N Engl J Med", "Lancet", "EuroIntervention"):
    sub = [o for o in out if o["journal"] == j]
    print(f"  {j}: {len(sub)} (elegibles por prefijo: {sum(1 for o in sub if o['tipo']=='ELEGIBLE')})")
