#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""¿Cuánto tarda PubMed en indexar cada revista? Compara, para la MISMA ventana,
cuántos artículos tiene Crossref (el editor) frente a los que tiene PubMed."""
import urllib.request, urllib.parse, json, time
D1, D2 = "2026-08-24", "2026-08-30"
P1, P2 = "2026/08/24", "2026/08/30"
UA = {"User-Agent": "BriefingCardiovascular/1.0 (mailto:domingo.marzal@gmail.com)"}
REV = [  # (nombre PubMed, ISSN)
 ("N Engl J Med","0028-4793"), ("Lancet","0140-6736"), ("JAMA","0098-7484"),
 ("Eur Heart J","0195-668X"), ("Circulation","0009-7322"), ("J Am Coll Cardiol","0735-1097"),
 ("JAMA Cardiol","2380-6583"), ("Eur J Heart Fail","1388-9842"), ("Europace","1099-5129"),
 ("Heart Rhythm","1547-5271"), ("JACC Cardiovasc Interv","1936-8798"), ("Eur J Prev Cardiol","2047-4873"),
 ("J Am Heart Assoc","2047-9980"), ("Heart","1355-6037"), ("JACC Adv","2772-963X"),
]
def get(u, hdr=None):
    req = urllib.request.Request(u, headers=hdr or {})
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r: return r.read()
        except Exception: time.sleep(2)
    return b"{}"
print(f"Ventana {D1} a {D2}\n")
print(f"{'Revista':26}{'Crossref':>9}{'PubMed':>8}{'  gap':>7}   estado")
print("-"*72)
tot_cr = tot_pm = 0
for name, issn in REV:
    u = (f"https://api.crossref.org/journals/{issn}/works?"
         f"filter=from-created-date:{D1},until-created-date:{D2},type:journal-article&rows=0")
    cr = json.loads(get(u, UA)).get("message", {}).get("total-results", 0)
    time.sleep(0.4)
    term = f'"{name}"[ta] AND {P1}:{P2}[edat]'
    pm = int(json.loads(get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
          f"db=pubmed&term={urllib.parse.quote(term)}&retmax=0&retmode=json"))["esearchresult"]["count"])
    time.sleep(0.35)
    tot_cr += cr; tot_pm += pm
    gap = cr - pm
    if cr == 0: est = "sin datos en Crossref"
    elif gap <= 0: est = "PubMed al día ✓"
    elif gap / max(cr,1) >= .5: est = "*** PubMed MUY retrasado ***"
    else: est = "PubMed incompleto"
    print(f"{name:26}{cr:>9}{pm:>8}{gap:>7}   {est}")
print("-"*72)
print(f"{'TOTAL':26}{tot_cr:>9}{tot_pm:>8}{tot_cr-tot_pm:>7}")
