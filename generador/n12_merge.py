#!/usr/bin/env python3
# Fusiona metadatos (n12_sel.json) + textos de los 5 lotes (n12_dataN.json) -> n12_data.json
import json, os, glob
B = os.path.dirname(os.path.abspath(__file__))
SEL = {o['key']: o for o in json.load(open(B+'/n12_sel.json'))}
TXT = {}
for f in sorted(glob.glob(B+'/n12_data[0-4].json')):
    TXT.update(json.load(open(f)))

# El documento conjunto se dedujo a la versión de Circulation, cuyo título incluye la coletilla
# "On Behalf of the Joint ESC/ACC/AHA/WHF Task Force". Se usa el título canónico corto (el de
# Eur Heart J y JACC), que es el MISMO documento, para no arrastrar una cabecera larguísima.
FIXT = {"a16": ("Fifth Universal Definition of Myocardial Infarction (2026)",
                "Quinta Definición Universal del Infarto de Miocardio (2026)")}

out = {}
missing = []
for k, s in SEL.items():
    t = TXT.get(k)
    if not t: missing.append(k); continue
    ten, tes = t['title_en'], t['title_es']
    if k in FIXT: ten, tes = FIXT[k]
    out[k] = dict(key=k, sec=s['sec'], ptype=s['ptype'], journal=s['journal'], doi=s['doi'],
                  total=s['total'], prio=s['prio'], title_en=ten, title_es=tes,
                  es=t['es'], en=t['en'])
if missing: raise SystemExit("FALTAN fichas: " + ", ".join(missing))
json.dump(out, open(B+'/n12_data.json','w'), ensure_ascii=False, indent=1)
print(f"n12_data.json: {len(out)} fichas")
from collections import Counter
print("por sección:", dict(sorted(Counter(v['sec'] for v in out.values()).items())))
print("prioridad:", dict(Counter(v['prio'] for v in out.values())))
