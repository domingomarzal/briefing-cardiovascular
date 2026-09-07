# -*- coding: utf-8 -*-
"""N13 · reorden editorial pedido por el usuario (7-sep-2026):
  · a36 (PRAGUE-26, trombólisis dirigida por catéter en embolia pulmonar) SALE del número:
    decisión del usuario — es embolia de pulmón, fuera del ámbito de la cardiología clínica.
  · Al liberarse plaza en Cardiología intervencionista, vuelve a40 (mejor candidato, 4,75).
  · Nuevo Destacado: a11 (VESALIUS-CV). Nuevo Top 3: a12 (VICTORION-Challenge), a41, a42.
Idempotente."""
import json, io
d = json.load(io.open("n13_data.json", encoding="utf-8"))
s = json.load(io.open("n13_sel.json", encoding="utf-8"))

# --- a36 fuera
d.pop("a36", None)
s = [o for o in s if o["key"] != "a36"]

# --- a40 vuelve (se recupera del estado previo del número, sin reescribir su ficha)
if "a40" not in d:
    orig_d = json.load(io.open("/tmp/n13_data_orig.json", encoding="utf-8"))
    orig_s = {o["key"]: o for o in json.load(io.open("/tmp/n13_sel_orig.json", encoding="utf-8"))}
    d["a40"] = orig_d["a40"]
    s.append(orig_s["a40"])

json.dump(d, io.open("n13_data.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(s, io.open("n13_sel.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

from collections import Counter
print("data:", len(d), "| sel:", len(s))
print("por sección:", dict(sorted(Counter(o["sec"] for o in s).items())))
print("a36 fuera:", "a36" not in d, "| a40 dentro:", "a40" in d)
top = sorted(s, key=lambda o: -o["total"])[:6]
print("--- 6 mejores por TOTAL:")
for o in top: print("   ", o["key"], o["total"], "| sec", o["sec"], "|", o["journal"], "|", o["title"][:62])
