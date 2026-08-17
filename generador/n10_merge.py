#!/usr/bin/env python3
# Fusiona n10_sel.json + n10_out{0..4}.json -> n10_data.json (formato que consume gen_bilingue.py)
import json, os
G = os.path.dirname(os.path.abspath(__file__))
sel = {s["key"]: s for s in json.load(open(G + "/n10_sel.json"))}
fich = {}
for b in range(5):
    for o in json.load(open(f"{G}/n10_out{b}.json")):
        fich[o["key"]] = o
data = {}
FIELDS = ("resumen", "why", "deque", "resultados", "conclusiones")
missing = []
for k, s in sel.items():
    f = fich.get(k)
    if not f: missing.append(k); continue
    for lang in ("es", "en"):
        for fl in FIELDS:
            if not (f.get(lang, {}).get(fl) or "").strip():
                missing.append(f"{k}.{lang}.{fl}")
    data[k] = dict(key=k, sec=s["sec"], ptype=s["ptype"], journal=s["journal"], doi=s["doi"],
                   total=s["total"], prio=s["prio"],
                   title_en=s["title"], title_es=f["title_es"].rstrip().rstrip("."),
                   es=f["es"], en=f["en"])
if missing:
    raise SystemExit("FALTAN CAMPOS: " + ", ".join(missing))
json.dump(data, open(G + "/n10_data.json", "w"), ensure_ascii=False, indent=1)
from collections import Counter
print("n10_data.json:", len(data), "fichas ·", dict(sorted(Counter(a["sec"] for a in data.values()).items())))
print("prioridad:", dict(Counter(a["prio"] for a in data.values())))
