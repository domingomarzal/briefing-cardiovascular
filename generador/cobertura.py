#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PASO 1b — AUDITORÍA DE COBERTURA (se ejecuta EN EL MAC, donde Crossref sí es accesible).

Compara, revista a revista y para la ventana del número, lo que el EDITOR ha publicado
(Crossref, filtro `created` = fecha de depósito del DOI) con lo que el número recogió.
Sirve para detectar artículos que PubMed no había indexado a tiempo.

Medición real del 31-ago-2026 (ventana 24-30 ago, semana del congreso ESC):
  N Engl J Med .... 23 en Crossref vs 6 en PubMed  -> faltaban 17 (CASO GRAVE)
  J Am Coll Cardiol 34 vs 24 -> 10 · JAMA 46 vs 42 -> 4 · Lancet 40 vs 37 -> 3
  El resto de revistas: PubMed al día.
Conclusión: el agujero grande es NEJM, pero conviene auditar todas.

Uso:  python3 cobertura.py <n> [--faltantes]
      n = número del briefing (p. ej. 12). --faltantes lista los DOI no recogidos.
"""
import urllib.request, urllib.parse, json, time, sys, os, re, datetime

B = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "BriefingCardiovascular/1.0 (mailto:domingo.marzal@gmail.com)"}

REVISTAS = [
 ("N Engl J Med","0028-4793"), ("Lancet","0140-6736"), ("JAMA","0098-7484"),
 ("Eur Heart J","0195-668X"), ("Circulation","0009-7322"), ("J Am Coll Cardiol","0735-1097"),
 ("JAMA Cardiol","2380-6583"), ("Nat Rev Cardiol","1759-5002"), ("Eur J Heart Fail","1388-9842"),
 ("JACC Heart Fail","2213-1779"), ("Circ Heart Fail","1941-3289"), ("EuroIntervention","1774-024X"),
 ("JACC Cardiovasc Interv","1936-8798"), ("Circ Cardiovasc Interv","1941-7640"),
 ("Heart Rhythm","1547-5271"), ("Europace","1099-5129"), ("JACC Clin Electrophysiol","2405-500X"),
 ("JACC Cardiovasc Imaging","1936-878X"), ("Eur Heart J Cardiovasc Imaging","2047-2404"),
 ("Eur J Prev Cardiol","2047-4873"), ("Hypertension","0194-911X"), ("Heart","1355-6037"),
 ("Rev Esp Cardiol","0300-8932"), ("Atherosclerosis","0021-9150"),
 ("J Am Heart Assoc","2047-9980"), ("JACC Adv","2772-963X"),
]
# Prefijos de DOI de NEJM que SÍ son artículo (el editor codifica el tipo en el DOI)
NEJM_OK = ("nejmoa","nejmra","nejmcp","nejmsa","nejmsr")

def get(u, hdr=None):
    req = urllib.request.Request(u, headers=hdr or {})
    for _ in range(4):
        try:
            with urllib.request.urlopen(req, timeout=90) as r: return r.read()
        except Exception: time.sleep(2)
    return b"{}"

def ventana(n):
    """Deduce la ventana del número n a partir del periodo guardado, o la calcula."""
    p = os.path.join(B, f"n{n}_corpus.json")
    if os.path.exists(p):
        per = json.load(open(p)).get("periodo","")
        m = re.match(r"(\d{4})/(\d{2})/(\d{2})-(\d{4})/(\d{2})/(\d{2})", per)
        if m:
            a = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"; b = f"{m.group(4)}-{m.group(5)}-{m.group(6)}"
            return a, b
    hoy = datetime.date.today(); lun = hoy - datetime.timedelta(days=hoy.weekday())
    return str(lun - datetime.timedelta(days=7)), str(lun - datetime.timedelta(days=1))

def main():
    n = sys.argv[1] if len(sys.argv) > 1 else "12"
    detalle = "--faltantes" in sys.argv
    D1, D2 = ventana(n)
    # DOIs ya presentes en el número
    tengo = set()
    for f in (f"n{n}_corpus.json", "n%s_data.json" % n):
        p = os.path.join(B, f)
        if not os.path.exists(p): continue
        d = json.load(open(p))
        recs = d.get("recs", d) if isinstance(d, dict) else d
        it = recs.values() if isinstance(recs, dict) else recs
        for r in it:
            if isinstance(r, dict) and r.get("doi"): tengo.add(r["doi"].lower())

    print(f"AUDITORÍA DE COBERTURA · N{n} · ventana {D1} a {D2}")
    print(f"(DOI ya recogidos en el número: {len(tengo)})\n")
    print(f"{'Revista':32}{'editor':>7}{'míos':>7}{'faltan':>8}")
    print("-"*56)
    faltantes = []
    for name, issn in REVISTAS:
        off, items = 0, []
        while True:
            u = (f"https://api.crossref.org/journals/{issn}/works?"
                 f"filter=from-created-date:{D1},until-created-date:{D2},type:journal-article"
                 f"&rows=200&offset={off}&select=DOI,title,created,issued,published-online")
            msg = json.loads(get(u, UA)).get("message", {})
            got = msg.get("items", [])
            if not got: break
            items += got; off += 200
            if off >= msg.get("total-results", 0): break
            time.sleep(0.35)
        falt = []
        for m in items:
            doi = (m.get("DOI") or "").lower()
            if not doi or doi in tengo: continue
            # ⚠️ `created` es la fecha de DEPÓSITO en Crossref, y algunas revistas REDEPOSITAN
            # metadatos de artículos ANTIGUOS (EuroIntervention volcó en ago-2026 artículos de
            # 2023). Hay que confirmar con la fecha real de publicación: si `issued` o
            # `published-online` son de un AÑO/MES anterior a la ventana, NO es material nuevo.
            def _ym(key):
                v = m.get(key, {}).get("date-parts", [[None]])[0]
                return (v[0], v[1] if len(v) > 1 else 1) if v and v[0] else None
            real = _ym("published-online") or _ym("issued")
            if real:
                ym_win = (int(D1[:4]), int(D1[5:7]))
                if real < (ym_win[0], ym_win[1]):      # publicado antes del mes de la ventana
                    continue
            if name == "N Engl J Med" and not doi.split("/")[-1].startswith(NEJM_OK):
                continue                       # editorial/carta/perspectiva: no elegible
            falt.append(dict(journal=name, doi=m.get("DOI"), title=(m.get("title") or [""])[0]))
        mark = "  <-- REVISAR" if len(falt) >= 5 else ""
        print(f"{name:32}{len(items):>7}{len(items)-len(falt):>7}{len(falt):>8}{mark}")
        faltantes += falt
        time.sleep(0.35)
    print("-"*56)
    print(f"\nTOTAL de DOI publicados por el editor y NO recogidos: {len(faltantes)}")
    out = os.path.join(B, f"n{n}_cobertura.json")
    json.dump(faltantes, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"Detalle guardado en {os.path.basename(out)}")
    if detalle:
        print("\n=== FALTANTES ===")
        for f in faltantes:
            print(f"  [{f['journal']}] {f['doi']}\n      {f['title'][:88]}")

if __name__ == "__main__":
    main()
