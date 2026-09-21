#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PASO 7b — LISTA DE TRABAJO PARA REVISAR **TODOS** LOS ENLACES DEL NÚMERO.

REGLA DURA DEL USUARIO (14-sep-2026): «quiero que todos los enlaces los revises
siempre, uno por uno, para comprobar que funcionan bien. No se puede dar por hecho.
Y si un enlace no funciona —a JACC o a cualquier revista— hay que dirigirlo a
ScienceDirect.»

O sea: NO hay subconjunto «de riesgo». Se revisan los 49, todas las semanas, en un
navegador REAL. Esto no es opcional ni se puede sustituir por una comprobación
automática: `curl` y Chrome headless reciben el muro de Cloudflare («Just a
moment...») EXACTAMENTE IGUAL para un enlace bueno que para uno roto, así que no
distinguen nada. Crossref solo dice que el DOI existe, no que la página aterrice.

CÓMO SE HACE (con el Chrome real del usuario, que sí atraviesa Cloudflare y no pide
aprobación por origen; el panel de navegador está denegado en sesiones programadas):
  1. `python3 generador/revisar_enlaces.py <n>` -> imprime las URL finales, en tandas.
  2. Con `mcp__Control_Chrome__open_url`, de 4 en 4 (más de 5 a la vez ha llegado a
     tumbar Chrome). Esperar ~20 s y leer con `mcp__Control_Chrome__list_tabs`.
     ⚠️ `get_current_tab` devuelve la pestaña ACTIVA, que no es la tuya: usa list_tabs
     y busca por URL. Cierra cada tanda con `close_tab` antes de abrir la siguiente.
  3. La señal de enlace roto es el `<title>`: **«Page Not Found»**. Ojo con
     «Just a moment...»: eso NO es un fallo, es el reto de Cloudflare a medias —
     vuelve a abrir esa URL y léela otra vez (le pasó a a1 en N14 y estaba bien).
  4. Los rotos se redirigen:
       python3 generador/enlaces_directos.py <n> --pii <clave> <clave> ...
     y si alguno no tuviera PII (no es de Elsevier), entonces a PubMed:
       python3 generador/check_links.py <n> <clave>
  5. Regenerar: `gen_bilingue.py n<n>` y `gen_audit_N<n>.py`, y republicar.

RESULTADO EN N14 (primera vez que se revisaron los 49): 46 correctos y 3 rotos, todos
en jacc.org — a13, a39 y a49 —, que abren bien en ScienceDirect por PII. Los 3 rotos
no tenían nada en común ni eran previsibles: a37 (jcmg…018) funciona y a39 (jcmg…017)
no, con DOI consecutivos del mismo fascículo. Justo por eso hay que mirarlos todos.

Uso:  python3 revisar_enlaces.py <n> [--tanda 4]
"""
import json, os, sys

B = os.path.dirname(os.path.abspath(__file__))


def main():
    args = sys.argv[1:]
    if not args:
        raise SystemExit("uso: python3 revisar_enlaces.py <n> [--tanda 4]")
    n = args[0]
    tanda = int(args[args.index("--tanda") + 1]) if "--tanda" in args else 4

    data = json.load(open(os.path.join(B, f"n{n}_data.json")))
    jl_p = os.path.join(B, f"n{n}_jlinks.json")
    fx_p = os.path.join(B, f"n{n}_linkfix.json")
    jlinks = json.load(open(jl_p)) if os.path.exists(jl_p) else {}
    linkfix = json.load(open(fx_p)) if os.path.exists(fx_p) else {}
    ex_p = os.path.join(B, f"n{n}_pii.json")
    excep = set(json.load(open(ex_p))) if os.path.exists(ex_p) else set()

    filas = []
    for k in sorted(data, key=lambda x: int("".join(c for c in x if c.isdigit()) or 0)):
        a = data[k]
        # MISMA PRECEDENCIA que jlink() de gen_bilingue.py: linkfix > jlinks > doi.org.
        url = linkfix.get(k) or jlinks.get(k) or ("https://doi.org/" + a["doi"])
        filas.append((k, a["journal"], url))

    print(f"REVISIÓN DE ENLACES · N{n} · {len(filas)} enlaces · TODOS, uno por uno\n")
    for i in range(0, len(filas), tanda):
        lote = filas[i:i + tanda]
        print(f"--- tanda {i // tanda + 1} ({len(lote)}) " + "-" * 40)
        for k, j, u in lote:
            marca = "  [excepción PII]" if k in excep else ("  [linkfix]" if k in linkfix else "")
            print(f"  {k:<5}{j[:26]:<28}{u}{marca}")
        print()
    from collections import Counter
    c = Counter(u.split("/")[2] for _, _, u in filas)
    print("por destino:", ", ".join(f"{h} {v}" for h, v in c.most_common()))
    if excep:
        print("excepciones ya marcadas (van a ScienceDirect):", ", ".join(sorted(excep)))
    print("\nLa señal de roto es el <title> «Page Not Found». «Just a moment...» NO es un "
          "fallo: es el reto de Cloudflare a medias, vuelve a abrir esa URL.")


if __name__ == "__main__":
    main()
