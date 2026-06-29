# -*- coding: utf-8 -*-
# Construye metadatos + puntuación 6 ejes para los artículos seleccionados de N3 y
# emite n3_tasks.json (un registro por artículo con abstract + metadatos para redactar fichas).
import json
e = json.load(open("n3_eligible.json"))

PT = {  # ptype canónico
 48:"Emulación de ensayo diana",6:"Estudio de cohorte",47:"Scientific Statement",86:"Estudio de cohorte",85:"Estudio de cohorte",
 0:"Ensayo clínico aleatorizado",23:"Estudio de cohorte",55:"Estudio de cohorte",26:"Estudio de cohorte",52:"Estudio de cohorte",
 112:"Estudio de cohorte",75:"Análisis secundario de ensayo clínico",67:"Investigación original",
 110:"Metaanálisis",35:"Metaanálisis",34:"Estudio de cohorte",76:"Inteligencia artificial / modelo predictivo",30:"Artículo de revisión",
 18:"Metaanálisis",115:"Ensayo clínico aleatorizado",19:"Análisis secundario de ensayo clínico",9:"Scientific Statement",108:"Estudio observacional",
 119:"Análisis secundario de ensayo clínico",21:"Análisis secundario de ensayo clínico",20:"Estudio de cohorte",12:"Estudio observacional",71:"Registro",
 113:"Análisis secundario de ensayo clínico",50:"Estudio de cohorte",10:"Registro",87:"Registro",2:"Estudio de casos y controles",
 16:"Documento de consenso",14:"Documento de consenso",15:"Estudio de cohorte",17:"Inteligencia artificial / modelo predictivo",13:"Estudio de cohorte",
 1:"Ensayo clínico aleatorizado",99:"Documento de consenso",104:"Registro",101:"Registro",98:"Estudio observacional",
 106:"Registro",29:"Metaanálisis",37:"Estudio observacional",28:"Análisis secundario de ensayo clínico",41:"Estudio de cohorte",
}
SEC = {  # sección 1-10
 48:1,6:1,47:1,86:1,85:1, 0:2,23:2,55:2,26:2,52:2, 112:3,75:3,67:3,
 110:4,35:4,34:4,76:4,30:4, 18:5,115:5,19:5,9:5,108:5, 119:6,21:6,20:6,12:6,71:6,
 113:7,50:7,10:7,87:7,2:7, 16:8,14:8,15:8,17:8,13:8, 1:9,99:9,104:9,101:9,98:9, 106:10,29:10,37:10,28:10,41:10,
}
# (REL,CAMBIO,EVID,EFECTO,REP,FI)  EFECTO=None para guías/statements/consenso
SC = {
 48:(8,5,7,5,5,7),6:(8,6,7,6,6,7),47:(7,5,6,None,5,7),86:(7,5,7,7,6,5),85:(6,4,6,5,5,5),
 0:(7,5,8,5,6,9),23:(7,5,7,6,6,6),55:(7,6,7,6,6,5),26:(6,5,6,6,5,6),52:(6,4,6,5,5,5),
 112:(8,6,7,6,7,7),75:(7,6,7,6,6,5),67:(5,3,5,4,4,5),
 110:(9,8,8,7,8,7),35:(8,6,8,6,7,6),34:(7,4,7,6,5,6),76:(6,4,6,6,5,5),30:(6,4,5,None,5,6),
 18:(9,7,8,7,8,7),115:(7,5,6,5,7,10),19:(7,5,7,5,6,7),9:(7,6,6,None,6,8),108:(7,5,6,5,5,7),
 119:(7,7,5,6,9,9),21:(7,5,7,6,6,7),20:(7,6,5,6,6,7),12:(6,4,5,5,5,7),71:(6,4,6,5,5,5),
 113:(9,8,9,7,9,7),50:(7,6,7,7,6,8),10:(7,6,6,None,6,8),87:(7,5,6,6,5,5),2:(6,5,6,6,5,6),
 16:(7,6,6,None,6,7),14:(7,6,6,None,6,7),15:(6,5,7,6,5,7),17:(6,4,6,5,5,7),13:(6,4,6,6,5,7),
 1:(7,6,7,7,6,6),99:(6,6,5,None,6,7),104:(6,5,6,6,5,7),101:(6,5,6,5,5,7),98:(5,4,5,5,5,7),
 106:(8,6,7,7,7,7),29:(7,6,7,6,6,6),37:(8,6,7,7,6,6),28:(6,4,6,5,5,6),41:(6,4,5,5,5,6),
}
W=dict(REL=.20,CAMBIO=.25,EVID=.20,EFECTO=.15,REP=.12,FI=.08)
def total(s):
    rel,cam,ev,ef,rep,fi=s
    if ef is None:  # sin EFECTO: reparte 0.15 entre los otros 5 (factor 1/0.85)
        base=rel*W["REL"]+cam*W["CAMBIO"]+ev*W["EVID"]+rep*W["REP"]+fi*W["FI"]
        return round(base/0.85,2)
    return round(rel*W["REL"]+cam*W["CAMBIO"]+ev*W["EVID"]+ef*W["EFECTO"]+rep*W["REP"]+fi*W["FI"],2)
def prio(s,t):
    cam=s[1]
    if cam>=8 or t>=8: return "Imprescindible"
    if t>=5: return "Relevante"
    return "Complementario"
ACR={"a6":" (GUTS)"}

order=[48,6,47,86,85, 0,23,55,26,52, 112,75,67, 110,35,34,76,30, 18,115,19,9,108,
       119,21,20,12,71, 113,50,10,87,2, 16,14,15,17,13, 1,99,104,101,98, 106,29,37,28,41]
tasks={}
for i in order:
    r=e[str(i)]; s=SC[i]; t=total(s); key="a%d"%i
    tasks[key]=dict(key=key, idx=i, sec=SEC[i], ptype=PT[i], journal=r["journal"], doi=r["doi"],
                    title=r["title"], abstract=r["abstract"],
                    scores=dict(REL=s[0],CAMBIO=s[1],EVID=s[2],EFECTO=s[3],REP=s[4],FI=s[5]),
                    total=t, prio=prio(s,t))
json.dump(tasks,open("n3_tasks.json","w"),ensure_ascii=False,indent=1)
# resumen ranking
rk=sorted(tasks.values(),key=lambda x:-x["total"])
print("TOP 8 por TOTAL:")
for x in rk[:8]: print(f'  {x["key"]:5} {x["total"]:.2f} {x["prio"]:14} s{x["sec"]:>2} {x["journal"]}')
print("DESTACADO=a113  TOP3=a110,a18,a106")
print("total seleccionados:",len(tasks))
from collections import Counter
print("por sección:",dict(sorted(Counter(x["sec"] for x in tasks.values()).items())))
