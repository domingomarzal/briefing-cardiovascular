URL="https://domingomarzal.github.io/briefing-cardiovascular/n0/"
CAB="https://domingomarzal.github.io/briefing-cardiovascular/n0/cabecera.png"
def doi(d): return "https://doi.org/"+d
banner=f'''<table width="100%" bgcolor="#0a3d62" style="border-radius:12px;border-collapse:separate"><tr>
<td style="padding:18px 22px">
<a href="{URL}" style="text-decoration:none;color:#ffffff;font-size:27px;font-weight:bold;letter-spacing:-.5px">Briefing <span style="color:#0f9aa0">Cardiovascular</span></a>
<div style="margin-top:8px;font-size:13px;color:#c4d4df">N0 · 3 al 10 de junio de 2026</div></td>
<td width="62" bgcolor="#0f9aa0" align="center" style="border-radius:0 12px 12px 0"><a href="{URL}" style="color:#fff;font-size:26px;text-decoration:none">&#10095;</a></td>
</tr></table>'''
dest=f'''<p style="margin:20px 0 6px;font-size:11px;font-weight:bold;color:#0f9aa0;letter-spacing:1px">DESTACADO DE LA SEMANA</p>
<p style="margin:0;font-size:15px;color:#103a47;font-weight:bold">Guía CKM 2026 (AHA/ACC/ADA/ASN) — síndrome cardiovascular-renal-metabólico</p>
<p style="margin:2px 0 0"><a href="{doi('10.1161/CIR.0000000000001453')}" style="font-size:13px;color:#0f9aa0;text-decoration:underline">Circulation ›</a></p>'''
items=[
("Finerenona en enfermedad renal crónica sin diabetes (FIND-CKD)","N Engl J Med","10.1056/NEJMoa2604625"),
("Monoterapia con inhibidor de P2Y12 tras DAPT abreviada post-ICP: metaanálisis","Eur Heart J","10.1093/eurheartj/ehag381"),
("iSGLT2 e insuficiencia cardíaca incidente en portadores de variantes de miocardiopatía (DECLARE-TIMI 58)","Nat Med","10.1038/s41591-026-04439-x"),
]
rows=""
for i,(t,j,d) in enumerate(items,1):
    bb="border-bottom:1px solid #eef1f6;" if i<3 else ""
    rows+=f'''<tr><td width="30" valign="top" style="padding:9px 0;{bb}font-size:14px;font-weight:bold;color:#0f9aa0">{i}</td>
<td style="padding:9px 0;{bb}"><div style="font-size:14px;color:#103a47">{t}</div><div style="margin-top:2px"><a href="{doi(d)}" style="font-size:12.5px;color:#0f9aa0;text-decoration:underline">{j} ›</a></div></td></tr>'''
ntp=f'<p style="margin:22px 0 4px;font-size:11px;font-weight:bold;color:#0a3d62;letter-spacing:.5px">NO TE LOS PUEDES PERDER</p><table width="100%">{rows}</table>'
html=f'<div style="font-family:Arial,Helvetica,sans-serif;max-width:680px;margin:0;color:#103a47">{banner}{dest}{ntp}</div>'
plain=f"""Briefing Cardiovascular — N0 · 3 al 10 de junio de 2026.

DESTACADO: Guía CKM 2026 (AHA/ACC/ADA/ASN) — Circulation — {doi('10.1161/CIR.0000000000001453')}

NO TE LOS PUEDES PERDER:
1. Finerenona en ERC sin diabetes (FIND-CKD) — N Engl J Med — {doi('10.1056/NEJMoa2604625')}
2. Monoterapia P2Y12 tras DAPT abreviada post-ICP: metaanálisis — Eur Heart J — {doi('10.1093/eurheartj/ehag381')}
3. iSGLT2 e IC incidente en portadores de variantes de miocardiopatía (DECLARE-TIMI 58) — Nat Med — {doi('10.1038/s41591-026-04439-x')}"""
import json
print(json.dumps({"html":html,"plain":plain}))
