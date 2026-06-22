# -*- coding: utf-8 -*-
import re,io,sys,html
def process(path):
    t=io.open(path,encoding="utf-8").read()
    # distinct journals + types from rows
    revs=sorted({html.unescape(m).strip() for m in re.findall(r'<td class="rev">([^<]*)</td>',t) if m.strip()}, key=lambda s:s.lower())
    tipos=sorted({html.unescape(m).strip() for m in re.findall(r'<td class="tipo">([^<]*)</td>',t) if m.strip()}, key=lambda s:s.lower())
    def opts(label,vals):
        o=f'<option value="all">{label}</option>'+''.join(f'<option value="{html.escape(v)}">{html.escape(v)}</option>' for v in vals)
        return o
    revsel=f'\n      <select id="revsel" title="Filtrar por revista">{opts("Todas las revistas",revs)}</select>'
    tiposel=f'\n      <select id="tiposel" title="Filtrar por tipo">{opts("Todos los tipos",tipos)}</select>'
    # remove any previous revsel/tiposel selects (idempotent)
    t=re.sub(r'\n?\s*<select id="revsel".*?</select>','',t,flags=re.S)
    t=re.sub(r'\n?\s*<select id="tiposel".*?</select>','',t,flags=re.S)
    # insert after catsel </select> (the first </select> after id="catsel")
    m=re.search(r'(<select id="catsel".*?</select>)',t,flags=re.S)
    if not m: raise SystemExit("catsel no encontrado en "+path)
    t=t[:m.end()]+revsel+tiposel+t[m.end():]
    # JS: declare vars (idempotent)
    if "getElementById('revsel')" not in t:
        t=t.replace("var catsel = document.getElementById('catsel');",
                    "var catsel = document.getElementById('catsel');\n  var revsel = document.getElementById('revsel');\n  var tiposel = document.getElementById('tiposel');")
        # add filtering logic before 'return true;' in pasa()
        t=t.replace(
"    if(c !== 'all' && tr.getAttribute('data-cat') !== c) return false;\n    return true;",
"    if(c !== 'all' && tr.getAttribute('data-cat') !== c) return false;\n"
"    var rv = revsel ? revsel.value : 'all';\n"
"    if(rv !== 'all'){ var rc = tr.querySelector('.rev'); if(!rc || rc.textContent.trim() !== rv) return false; }\n"
"    var tp = tiposel ? tiposel.value : 'all';\n"
"    if(tp !== 'all'){ var tc = tr.querySelector('.tipo'); if(!tc || tc.textContent.trim() !== tp) return false; }\n"
"    return true;")
        # listeners
        t=t.replace("if(catsel) catsel.addEventListener('change', aplica);",
                    "if(catsel) catsel.addEventListener('change', aplica);\n  if(revsel) revsel.addEventListener('change', aplica);\n  if(tiposel) tiposel.addEventListener('change', aplica);")
    io.open(path,"w",encoding="utf-8").write(t)
    return len(revs),len(tipos)
if __name__=="__main__":
    for p in sys.argv[1:]:
        r,ti=process(p); print(f"{r:3d} revistas · {ti:3d} tipos  ←  {p}")
