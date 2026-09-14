#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PASO 7b (paso 2) — ENLACE DIRECTO DEL EDITOR, AUTOMÁTICO.

POR QUÉ EXISTE (hallazgo del 14-sep-2026, N14).
El PASO 5 de la SKILL manda desde junio de 2026 enlazar «prefiriendo la URL DIRECTA
del editor, para que abra sin saltos». Nunca se implementó: `jlink()` de
`gen_bilingue.py` mandaba el 100 % de los enlaces a `https://doi.org/<DOI>`
(comprobado en N14: 102 de 102). De ahí venía el problema que el PASO 7b intentaba
cazar a mano cada semana:

    doi.org  ->  linkinghub.elsevier.com  ->  (salto por JavaScript)  ->  raíz de jacc.org

Crossref lo confirma: para toda la familia JACC y para Heart Rhythm,
`resource.primary.URL` es `https://linkinghub.elsevier.com/retrieve/pii/<PII>`.
Es decir, NO era un fallo aleatorio de unos artículos sí y otros no: TODOS los
artículos alojados en Elsevier salían por la pasarela que rebota. Por eso la avería
reaparecía cada pocas semanas (N7: 4 · N8: 2 · N9: 3 · N10: 6 · N11: 2), siempre en
la familia JACC.

LA SOLUCIÓN NO ES MIRARLOS A OJO, ES NO PASAR POR AHÍ.
Este script escribe `n<n>_jlinks.json` = {clave: URL directa del editor}, que
`gen_bilingue.py` aplica en `jlink()`. Rutas por plataforma:

  · Familia JACC .......... https://www.jacc.org/doi/<DOI>            (PASO 5)
  · Revistas AHA .......... https://www.ahajournals.org/doi/<DOI>     (PASO 5; Crossref
                            devuelve exactamente esa URL como resource.primary.URL)
  · N Engl J Med .......... https://www.nejm.org/doi/full/<DOI>       (PASO 5)
  · Resto de Elsevier ..... https://www.sciencedirect.com/science/article/pii/<PII>
                            con el PII que el propio editor registra en Crossref; es
                            el destino al que linkinghub intenta llegar, sin el salto.
  · Todo lo demás ......... se omite -> `jlink()` usa doi.org, que para OUP, JAMA,
                            BMJ y Nature resuelve bien y además es más duradero que
                            la URL de «advance-article» de OUP, que cambia al salir
                            el fascículo.

Uso:  python3 enlaces_directos.py <n>        (p. ej. 14)
Es idempotente y solo lee Crossref (api.crossref.org), accesible desde la nube.
"""
import urllib.request, json, os, re, sys, time

B = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "BriefingCardiovascular/1.0 (mailto:domingo.marzal@gmail.com)"}

JACC = {"J Am Coll Cardiol", "JACC Cardiovasc Interv", "JACC Cardiovasc Imaging",
        "JACC Clin Electrophysiol", "JACC Heart Fail", "JACC Adv", "JACC CardioOncol",
        "JACC Basic Transl Sci"}
AHA = {"Circulation", "Circ Heart Fail", "Circ Cardiovasc Interv", "Circ Res", "Hypertension",
       "J Am Heart Assoc", "Circ Arrhythm Electrophysiol", "Circ Cardiovasc Imaging",
       "Circ Cardiovasc Qual Outcomes", "Circ Genom Precis Med", "Stroke", "Arterioscler Thromb Vasc Biol"}


def crossref(doi):
    req = urllib.request.Request("https://api.crossref.org/works/" + doi, headers=UA)
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())["message"]
        except Exception:
            time.sleep(2)
    return {}


def pii_de_crossref(doi):
    """Devuelve el PII que el editor registra en Crossref, o '' si no lo hay."""
    m = crossref(doi)
    url = (m.get("resource", {}) or {}).get("primary", {}).get("URL", "") or ""
    mt = re.search(r"/retrieve/pii/([A-Za-z0-9]+)", url)
    if mt:
        return mt.group(1)
    for l in m.get("link", []) or []:
        mt = re.search(r"PII:([A-Za-z0-9]+)", l.get("URL", "") or "")
        if mt:
            return mt.group(1)
    return ""


def main():
    n = sys.argv[1] if len(sys.argv) > 1 else ""
    if not n:
        raise SystemExit("uso: python3 enlaces_directos.py <n>")
    sel = json.load(open(os.path.join(B, f"n{n}_sel.json")))
    out, sin_pii = {}, []
    for o in sel:
        doi, j, k = (o.get("doi") or "").strip(), o["journal"], o["key"]
        if not doi:
            continue
        if j in JACC:
            out[k] = "https://www.jacc.org/doi/" + doi
        elif j in AHA:
            out[k] = "https://www.ahajournals.org/doi/" + doi
        elif j == "N Engl J Med":
            out[k] = "https://www.nejm.org/doi/full/" + doi
        elif doi.startswith("10.1016"):           # Elsevier no-JACC: Heart Rhythm, Rev Esp Cardiol…
            pii = o.get("pii") or pii_de_crossref(doi)
            if pii:
                out[k] = "https://www.sciencedirect.com/science/article/pii/" + pii
            else:
                sin_pii.append((k, j, doi))
            time.sleep(0.4)
        # el resto se queda con doi.org (lo pone jlink por defecto)
    p = os.path.join(B, f"n{n}_jlinks.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print(f"n{n}_jlinks.json: {len(out)} enlaces directos de editor "
          f"(de {len(sel)} artículos; el resto usa doi.org)")
    from collections import Counter
    c = Counter(u.split("/")[2] for u in out.values())
    for host, v in c.most_common():
        print(f"   {v:3}  {host}")
    if sin_pii:
        print("\n  SIN PII (se quedan en doi.org y siguen en el grupo de riesgo):")
        for k, j, d in sin_pii:
            print(f"   {k}  {j}  {d}")


if __name__ == "__main__":
    main()
