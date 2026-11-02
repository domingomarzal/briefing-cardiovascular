#!/usr/bin/env python3
# N21 · RECUPERACIÓN DESDE EL MAC (2-nov-2026). La nube dejó en n21_pendiente_mac.json 20 artículos
# que el editor publicó en la ventana y PubMed no había indexado (semana del TCT 2026). Su resumen
# se leyó en la web del editor (jacc.org, atherosclerosis-journal.com, eurointervention.pcronline.com)
# con un navegador real y se guarda en n21_mac_abs.json. Este script los añade a n21_el.json
# (idempotente) y escribe su cribado/ponderación en n21_out9.json, que lee n21_sel.py.
# Quedan FUERA, con su motivo en la auditoría:
#   · 10.1001/jama.2026.19090 = «Research Summary» del ECA de JAMA que ya es a38 (no es otro artículo).
#   · LIPSIA-STRATEGY (10.1016/j.jacc.2026.10.064) y «Moderate Aortic Stenosis with At-Risk Features»
#     (10.1016/j.jacc.2026.10.069): ni jacc.org ni ScienceDirect los sirven todavía (404/403) y no hay
#     resumen verificable → regla del resumen.
import json, os
B = os.path.dirname(os.path.abspath(__file__))
P = {p['doi'].lower(): p for p in json.load(open(B+'/n21_pendiente_mac.json'))['pendientes']}
A = json.load(open(B+'/n21_mac_abs.json'))
# (doi, sección, tipo, REL, CAMBIO, EVID, EFECTO, REP, FI, acrónimo)
S = [("10.1016/j.jacc.2026.10.058",4,"Análisis secundario de ensayo clínico",8,5,6,4,7,7,""),
("10.1016/j.jcin.2026.10.001",9,"Ensayo clínico aleatorizado",5,5,5,5,7,6,""),
("10.1016/j.jcin.2026.09.030",9,"Ensayo clínico aleatorizado",7,5,8,6,7,6,""),
("10.1016/j.jcin.2026.10.024",7,"Investigación original",4,5,4,5,6,6,""),
("10.1016/j.jcin.2026.10.023",10,"Investigación original",6,4,4,5,6,6,"VERITAS"),
("10.1016/j.jcin.2026.10.025",7,"Registro",3,3,3,3,4,6,""),
("10.1016/j.jcin.2026.10.002",9,"Investigación original",5,5,5,6,7,6,""),
("10.4244/eij-d-26-00473",9,"Estudio de cohorte",6,4,4,3,4,5,""),
("10.4244/eij-d-26-00575",8,"Estudio pronóstico",5,4,5,7,4,5,""),
("10.4244/eij-d-26-00457",9,"Análisis secundario de ensayo clínico",5,4,6,5,4,5,"FAVOR III China"),
("10.1016/j.atherosclerosis.2026.121940",8,"Estudio pronóstico",4,3,4,6,3,4,""),
("10.1016/j.atherosclerosis.2026.121939",2,"Artículo de revisión",4,2,4,3,3,4,""),
("10.1016/j.atherosclerosis.2026.121945",1,"Estudio de cohorte",5,3,4,5,3,4,""),
("10.1016/j.atherosclerosis.2026.121946",4,"Estudio pronóstico",5,3,4,5,3,4,""),
("10.1016/j.atherosclerosis.2026.121941",3,"Estudio observacional",6,4,4,5,4,4,""),
("10.1016/j.atherosclerosis.2026.121944",3,"Estudio de cohorte",7,5,6,7,5,4,""),
("10.1016/j.atherosclerosis.2026.121947",3,"Estudio de cohorte",7,4,6,6,5,4,"")]
EL = json.load(open(B+'/n21_el.json'))
have = {(e.get('doi') or '').lower(): i for i, e in enumerate(EL)}
out = []
for d, sec, pt, rel, cam, evi, efe, rep, fi, acr in S:
    if d not in have:
        p, a = P[d], A[d]
        EL.append(dict(pmid='', journal=p['journal'], title=a['title'], ptypes=['Journal Article'],
                       abstract=a['abstract'], doi=p['doi'], pii=p.get('pii') or '', adate=p['online'].replace('-', '/'),
                       _oblig=False, _noabs=False,
                       _rec='recuperado por Crossref (PASO 1b); resumen leído en %s desde el Mac el 2-nov-2026 (PubMed no lo había indexado)' % a['fuente']))
        have[d] = len(EL) - 1
    out.append(dict(idx=have[d], elegible=True, motivo_descarte='', sec=sec, ptype=pt, rel=rel, cambio=cam,
                    evid=evi, efecto=efe, rep=rep, fi=fi, acr=acr, frase=''))
json.dump(EL, open(B+'/n21_el.json', 'w'), ensure_ascii=False)
json.dump(out, open(B+'/n21_out9.json', 'w'), ensure_ascii=False, indent=1)
print('EL:', len(EL), '| recuperados puntuados:', len(out))
