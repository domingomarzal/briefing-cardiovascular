#!/usr/bin/env python3
# Fusiona metadatos (n13_sel.json) + textos de los 5 lotes (n13_dataN.json) -> n13_data.json
import json, os, glob
B = os.path.dirname(os.path.abspath(__file__))
SEL = {o['key']: o for o in json.load(open(B+'/n13_sel.json'))}
TXT = {}
for f in sorted(glob.glob(B+'/n13_data[0-4].json')):
    TXT.update(json.load(open(f)))
out, missing = {}, []
for k, s in SEL.items():
    t = TXT.get(k)
    if not t: missing.append(k); continue
    out[k] = dict(key=k, sec=s['sec'], ptype=s['ptype'], journal=s['journal'], doi=s['doi'],
                  total=s['total'], prio=s['prio'], title_en=t['title_en'], title_es=t['title_es'],
                  es=t['es'], en=t['en'])
if missing: raise SystemExit("FALTAN fichas: " + ", ".join(missing))
json.dump(out, open(B+'/n13_data.json','w'), ensure_ascii=False, indent=1)
print(f"n13_data.json: {len(out)} fichas")
from collections import Counter
print("por sección:", dict(sorted(Counter(v['sec'] for v in out.values()).items())))
print("prioridad:", dict(Counter(v['prio'] for v in out.values())))
