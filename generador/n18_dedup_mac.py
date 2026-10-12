#!/usr/bin/env python3
# Mac 12-oct-2026: a17, a37 y a39 de N18 (EuroIntervention EIJ-D-26-00460/00889/00413) ya se
# publicaron en N17 (el Mac los recuperó por Crossref, created 28-sep; PubMed les puso ArticleDate
# 5-oct y la nube los volvió a seleccionar). Se sustituyen por los siguientes del ranking de su
# sección (n18_out*.json) y se marcan en la auditoría como «ya publicado en N17».
import json, os, glob
B = os.path.dirname(os.path.abspath(__file__))
EL = json.load(open(B + '/n18_el.json'))
W = dict(rel=.20, cambio=.25, evid=.20, efecto=.15, rep=.12, fi=.08)
OUT = {o['idx']: o for f in sorted(glob.glob(B + '/n18_out[0-9].json')) for o in json.load(open(f))}
REPL = {"a17": 26, "a37": 9, "a39": 7}
sel = json.load(open(B + '/n18_sel.json'))
for s in sel:
    if s['key'] in REPL:
        i = REPL[s['key']]; o = OUT[i]; r = EL[i]
        t = round(sum(W[k] * o[k] for k in W), 2)
        s.update(idx=i, pmid=r['pmid'], doi=r['doi'], pii=r['pii'], journal=r['journal'], sec=o['sec'],
                 ptype=o['ptype'], acr=o.get('acr', ''), rel=o['rel'], cambio=o['cambio'], evid=o['evid'],
                 efecto=o['efecto'], rep=o['rep'], fi=o['fi'], total=t,
                 prio="Imprescindible" if (o['cambio'] >= 8 or t >= 8) else ("Relevante" if t >= 5 else "Complementario"),
                 oblig=False, noabs=False, alt=None, rec="", title=r['title'].rstrip('.'), abstract=r['abstract'])
        print(s['key'], s['journal'], s['doi'], s['total'], s['prio'])
json.dump(sel, open(B + '/n18_sel.json', 'w'), ensure_ascii=False, indent=1)
acr = json.load(open(B + '/n18_acr.json')); acr.pop('a39', None)
json.dump(acr, open(B + '/n18_acr.json', 'w'), ensure_ascii=False)
