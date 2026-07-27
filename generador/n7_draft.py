#!/usr/bin/env python3
# Genera el cuerpo (texto plano + htmlBody) del borrador de Gmail "Cardio al día_N7".
import json, os, html
G = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(G + "/n7_data.json"))
ACR = json.load(open(G + "/n7_acr.json"))
DEST = "a51"; TOP3 = ["a11", "a46", "a6"]
PERIOD = "20 al 26 de julio de 2026"
URL = "https://domingomarzal.github.io/briefing-cardiovascular/n7/cardio-al-dia.html"
SEC = {1:"Cardiología preventiva",2:"Cardiometabolismo",3:"Dislipemia",4:"Cardiopatía isquémica",
       5:"Insuficiencia cardíaca",6:"Miocardiopatías",7:"Valvulopatías",8:"Imagen cardíaca",
       9:"Cardiología intervencionista",10:"Arritmias y electrofisiología"}
def t(k):
    a = D[k]; s = a["title_es"].rstrip().rstrip(".")
    ac = ACR.get(k, "")
    if ac and ac.strip(" ()") not in s: s += ac
    return s
def doi(k): return "https://doi.org/" + D[k]["doi"]
def e(s): return html.escape(s, quote=False)

rows = ""
for i, k in enumerate(TOP3, 1):
    br = "border-bottom:1px solid #eef1f6;" if i < 3 else ""
    rows += (f'<tr><td width="30" valign="top" style="{br}padding:11px 0;font-size:14px;font-weight:bold;color:#0f9aa0;">{i}</td>'
             f'<td style="{br}padding:11px 0;"><div style="font-size:14px;color:#103a47;">{e(t(k))}</div>'
             f'<div style="margin-top:4px;"><a href="{doi(k)}" style="font-size:13px;color:#0f9aa0;text-decoration:underline;">{e(D[k]["journal"])} &rsaquo;</a></div></td></tr>')

htmlbody = (
 f'<table width="100%" bgcolor="#0a3d62" style="border-radius:12px;border-collapse:separate;">'
 f'<tr><td style="padding:18px 22px;">'
 f'<a href="{URL}" style="text-decoration:none;">'
 f'<div style="font-size:27px;font-weight:bold;color:#ffffff;">Cardio al d<span style="color:#0f9aa0">IA</span></div>'
 f'<div style="font-size:13px;color:#c4d4df;margin-top:5px;">N7 &middot; {PERIOD}</div></a></td>'
 f'<td width="62" bgcolor="#0f9aa0" align="center" style="border-radius:0 12px 12px 0;">'
 f'<a href="{URL}" style="text-decoration:none;font-size:26px;color:#ffffff;">&#10095;</a></td></tr></table>'
 f'<table width="100%" bgcolor="#f1f9f9" style="border-radius:10px;border-collapse:separate;margin-top:18px;">'
 f'<tr><td style="padding:16px 20px;">'
 f'<div style="font-size:11px;color:#0f9aa0;font-weight:bold;">DESTACADO DE LA SEMANA</div>'
 f'<div style="font-size:15px;font-weight:bold;color:#103a47;margin-top:6px;">{e(t(DEST))}</div>'
 f'<div style="margin-top:8px;"><a href="{doi(DEST)}" style="font-size:13px;color:#0f9aa0;text-decoration:underline;">{e(D[DEST]["journal"])} &rsaquo;</a></div>'
 f'</td></tr></table>'
 f'<div style="font-size:11px;font-weight:bold;color:#0a3d62;margin:22px 0 4px;">NO TE LOS PUEDES PERDER</div>'
 f'<table width="100%" style="border-collapse:collapse;">{rows}</table>')

plain = (f"Cardio al día · N7 · {PERIOD}\n{URL}\n\n"
         f"DESTACADO DE LA SEMANA\n{t(DEST)}\n{D[DEST]['journal']}: {doi(DEST)}\n\n"
         f"NO TE LOS PUEDES PERDER\n")
for i, k in enumerate(TOP3, 1):
    plain += f"{i}. {t(k)}\n   {D[k]['journal']}: {doi(k)}\n"

json.dump(dict(subject="Cardio al día_N7", to="domingo.marzal@gmail.com",
               body=plain, htmlBody=htmlbody),
          open(G + "/n7_draft.json", "w"), ensure_ascii=False, indent=1)
print(plain)
print("--- htmlBody:", len(htmlbody), "chars -> n7_draft.json")
