# Pipeline semanal — Briefing Cardiovascular (para rutina en la nube de Claude Code)

Objetivo: cada lunes, generar el número N<n> de la semana natural anterior y PUBLICARLO en GitHub Pages
(carpeta `n<n>/`). NO se crea borrador de Gmail en la nube (eso se hace en el Mac o a mano).

Numeración: la semana 8-14 jun 2026 = N1; cada semana +1. N0 fue la prueba (3-10 jun).

Pasos:
1. `python3 generador/fetch_pubmed.py` → genera `corpus.json` (PubMed E-utilities, 25 revistas, semana anterior).
   (Requiere que la red permita eutils.ncbi.nlm.nih.gov.)
2. CRIBADO: descarta sin abstract y tipos no elegibles (editorial, carta, comentario, corrección, caso,
   noticia, reporte breve, ciencia básica/animal/in vitro). Los criterios completos están en `metodologia.html`.
3. CLASIFICA cada elegible en una de las 10 secciones (reglas en metodologia.html) y PUNTÚA los 6 ejes
   (REL 20 · CAMBIO 25 · EVID 20 · EFECTO 15 · REP 12 · FI 8) con las 3 anulaciones. Descarta lo no cardiovascular.
   FI por nivel de revista (N1=10, N2=7, N3=5). TOTAL ponderado; etiqueta 🔴≥8 o CAMBIO≥8 · 🟠 5-7,9 · 🟢 <5.
4. SELECCIONA el top 5 de cada sección por TOTAL (si hay <5 elegibles, los que haya; NO rellenar con no elegibles).
   Destacado = mayor TOTAL global; Top 3 = los 3 siguientes.
REGLA DE ACRÓNIMOS: si vas a añadir el acrónimo del estudio (p. ej. LOGICAL) al título, hazlo SOLO si NO está ya en el título de PubMed; nunca lo dupliques.
5. REDACTA cada ficha (resumen 2 líneas · por qué importa · "De qué va" · "Resultados" con TODAS las cifras,
   abreviado · "Conclusiones" FIEL al abstract). Verifica fidelidad frente al abstract.
6. GENERA el HTML replicando EXACTAMENTE el diseño de `n0/` (briefing y articulos-revisados.html) como PLANTILLA DE REFERENCIA FIJA — copia su bloque <style> tal cual (anchos de columna, filtros y modales idénticos) y solo cambia los datos
   (auditoría, con sus filtros y modales). Usa `gen_briefing_reference.py` como referencia del generador del briefing.
   Fecha el número como "N<n> · <periodo>".
7. Escribe en `n<n>/index.html`, `n<n>/articulos-revisados.html`, `n<n>/cabecera.png`.
8. `git add -A && git commit -m "N<n>" && git push` → GitHub Pages publica en .../n<n>/.
9. Avisa de que el N<n> está publicado y de que el borrador de Gmail se hará en el Mac.

## Regla de acrónimos
Al añadir el acrónimo del estudio al título de un artículo (p. ej. (LOGICAL), (DECLARE-TIMI 58)), hazlo SOLO si ese acrónimo NO aparece ya en el título de PubMed. Nunca lo dupliques: estudios como REIMAGINE 3, ABYSS, OPTION o REDUCE LAP-HF II ya lo traen en el título original.

## Secciones siempre visibles
Las 10 secciones temáticas se muestran SIEMPRE, aunque una semana no tengan material. Una sección que esa semana quede con 0 artículos se muestra con la nota «Sin novedades relevantes esta semana.» (clase .nonews) en lugar de fichas; con 1 o más, se muestran sus fichas. No se rellena artificialmente ni se omiten secciones.

## Enlaces: verificación obligatoria antes de publicar (27-jul-2026 · RESUELTO DE RAÍZ el 14-sep-2026)

Desde N7 reaparecía cada pocas semanas la misma avería: artículos de la familia JACC que llevaban
a "Page Not Found" (N7: 4 · N8: 2 · N9: 3 · N10: 6 · N11: 2). Se creía que era impredecible y se
comprobaba A OJO cada lunes. **No era impredecible.** El PASO 5 de la SKILL manda desde junio de
2026 enlazar a la URL directa del editor, pero `jlink()` de `gen_bilingue.py` nunca lo hizo: el
100 % de los enlaces salía por `https://doi.org/<DOI>` (en N14, 102 de 102). Y doi.org manda todo
lo alojado en Elsevier a `linkinghub.elsevier.com`, que salta por JavaScript y a veces rebota a la
raíz de la revista. Crossref lo confirma: para la familia JACC y Heart Rhythm
`resource.primary.URL` es `linkinghub.elsevier.com/retrieve/pii/<PII>`; para Circulation es
exactamente `www.ahajournals.org/doi/<DOI>`.

Antes de publicar cualquier número (los dos pasos corren en la nube, sin intervención):
1. `python3 generador/enlaces_directos.py <n>` — escribe `n<n>_jlinks.json` con la URL directa del
   editor de cada artículo (JACC → jacc.org/doi/<DOI> · AHA → ahajournals.org/doi/<DOI> · NEJM →
   nejm.org/doi/full/<DOI> · resto de Elsevier → sciencedirect.com/science/article/pii/<PII>, con
   el PII que el editor registra en Crossref). El resto se queda en doi.org. Ningún enlace vuelve
   a pasar por linkinghub.
2. `python3 generador/check_links.py n<n>` — valida contra Crossref que todos los DOI existen y que
   el título registrado cuadra con el nuestro (caza DOI equivocados). Sus avisos de "DOI NO
   REGISTRADO" sobre el número entero son falsos positivos por rate-limiting: confirma el DOI suelto
   con `curl api.crossref.org/works/<doi>` antes de tocar nada.
3. Regenera con `gen_bilingue.py n<n>`.

Ya NO hay que abrir enlaces a ojo en el panel de navegador: ese paso existía solo para cazar el
rebote de linkinghub. `n<n>_linkfix.json` (vía `check_links.py n<n> <clave> …`) se conserva como
red de seguridad manual y tiene prioridad sobre `jlinks`.

## Permisos: la tarea del lunes debe correr sin pedir nada (regla dura, 27-jul-2026)

`~/.claude/settings.json` tiene `defaultMode: bypassPermissions` y ahora también allow explícito
para ToolSearch, Agent/Task/Skill, el MCP de Gmail y las herramientas del panel de navegador.

PERO la tarjeta de aprobación POR ORIGEN del panel de navegador es una puerta de seguridad aparte
que settings.json NO gobierna: abrir un dominio nuevo puede seguir preguntando. Por eso, en la
ejecución automática del lunes:
- Para capturas y comprobación visual usa SIEMPRE Chrome headless por Bash
  (`--headless --screenshot`), que no pide nada. NO uses el panel de navegador para esto.
- El panel de navegador queda reservado al paso 2 de la verificación de enlaces, que es el único
  que necesita atravesar Cloudflare. Si ese paso pidiera permiso en una ejecución desatendida, NO
  bloquees la tarea: publica, y avisa en el PASO 9 de que la verificación de enlaces quedó
  pendiente para que el usuario la lance a mano.
