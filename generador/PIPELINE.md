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
