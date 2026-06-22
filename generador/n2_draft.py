# -*- coding: utf-8 -*-
URL="https://domingomarzal.github.io/briefing-cardiovascular/n2/"
def doi(d): return "https://doi.org/"+d
banner=f'''<table width="100%" bgcolor="#0a3d62" style="border-radius:12px;border-collapse:separate"><tr>
<td style="padding:18px 22px">
<a href="{URL}" style="text-decoration:none;color:#ffffff;font-size:27px;font-weight:bold;letter-spacing:-.5px">Briefing <span style="color:#0f9aa0">Cardiovascular</span></a>
<div style="margin-top:8px;font-size:13px;color:#c4d4df">N2 · 15 al 21 de junio de 2026</div></td>
<td width="62" bgcolor="#0f9aa0" align="center" style="border-radius:0 12px 12px 0"><a href="{URL}" style="color:#fff;font-size:26px;text-decoration:none">&#10095;</a></td>
</tr></table>'''
dest=f'''<p style="margin:20px 0 6px;font-size:11px;font-weight:bold;color:#0f9aa0;letter-spacing:1px">DESTACADO DE LA SEMANA</p>
<p style="margin:0;font-size:15px;color:#103a47;font-weight:bold">TAVR frente a cirugía a 10 años en estenosis aórtica de riesgo intermedio (PARTNER 2A)</p>
<p style="margin:2px 0 0"><a href="{doi('10.1016/j.jacc.2026.03.169')}" style="font-size:13px;color:#0f9aa0;text-decoration:underline">J Am Coll Cardiol ›</a></p>'''
items=[
("Tratamiento farmacológico del sobrepeso y la obesidad — Guía ACP 2026 (semaglutida y tirzepatida, primera línea)","Ann Intern Med","10.7326/ANNALS-25-02714"),
("Aficamtén frente a metoprolol en miocardiopatía hipertrófica obstructiva (MAPLE-HCM)","JAMA Cardiol","10.1001/jamacardio.2026.1730"),
("Balón liberador de sirólimus con stent provisional frente a DES sistemático en lesiones de novo","Circulation","10.1161/CIRCULATIONAHA.126.079033"),
]
rows=""
for i,(t,j,d) in enumerate(items,1):
    bb="border-bottom:1px solid #eef1f6;" if i<3 else ""
    rows+=f'''<tr><td width="30" valign="top" style="padding:9px 0;{bb}font-size:14px;font-weight:bold;color:#0f9aa0">{i}</td>
<td style="padding:9px 0;{bb}"><div style="font-size:14px;color:#103a47">{t}</div><div style="margin-top:2px"><a href="{doi(d)}" style="font-size:12.5px;color:#0f9aa0;text-decoration:underline">{j} ›</a></div></td></tr>'''
ntp=f'<p style="margin:22px 0 4px;font-size:11px;font-weight:bold;color:#0a3d62;letter-spacing:.5px">NO TE LOS PUEDES PERDER</p><table width="100%">{rows}</table>'
foot='<p style="margin:24px 0 0;font-size:11px;color:#8c97a6">Briefing completo (10 secciones, 49 artículos) en el enlace de la cabecera. Revisión semanal de la evidencia cardiovascular publicada más relevante.</p>'
html=f'<div style="font-family:Arial,Helvetica,sans-serif;max-width:680px;margin:0;color:#103a47">{banner}{dest}{ntp}{foot}</div>'
plain=f"""Briefing Cardiovascular — N2 · 15 al 21 de junio de 2026
{URL}

DESTACADO: TAVR frente a cirugía a 10 años en estenosis aórtica de riesgo intermedio (PARTNER 2A) — J Am Coll Cardiol — {doi('10.1016/j.jacc.2026.03.169')}

NO TE LOS PUEDES PERDER:
1. Tratamiento farmacológico del sobrepeso y la obesidad — Guía ACP 2026 (semaglutida y tirzepatida, primera línea) — Ann Intern Med — {doi('10.7326/ANNALS-25-02714')}
2. Aficamtén frente a metoprolol en miocardiopatía hipertrófica obstructiva (MAPLE-HCM) — JAMA Cardiol — {doi('10.1001/jamacardio.2026.1730')}
3. Balón liberador de sirólimus con stent provisional frente a DES sistemático en lesiones de novo — Circulation — {doi('10.1161/CIRCULATIONAHA.126.079033')}

Briefing completo (10 secciones, 49 artículos) en el enlace."""
open("/tmp/n2_body.txt","w").write(plain)
open("/tmp/n2_htmlbody.html","w").write(html)
print("HTML len:",len(html))
