# Briefing Cardiovascular · Cardio al día — Documento de arranque

> Para abrir el proyecto en una sesión NUEVA de Claude y continuarlo. Léelo entero
> antes de tocar nada. Última actualización: **16-jul-2026** (tras N5 + mudanza de la
> tarea a esta carpeta, ver §4.1).

---

## 1. Qué es el proyecto

Boletín semanal de cardiología del **Dr. Domingo Marzal**. Cada **lunes a las 8:00**
(Europe/Madrid) se genera, de forma **automática**, un número nuevo con lo más
relevante publicado la semana anterior en 31 revistas cardiovasculares. Cada número
tiene **dos ediciones con el mismo contenido**, bilingües (ESP por defecto / ENG):

- **Briefing Cardiovascular** → azul marino + turquesa. En ESP, títulos en inglés.
- **Cardio al día** → mismos colores; título/pie «Cardio al d**IA**» (IA en turquesa,
  mismo tamaño). En ESP, todo en español (títulos incluidos).

Además se genera la **Auditoría (Artículos Revisados)** y un **borrador de correo** en Gmail.

---

## 2. Estado actual (cronología)

| Nº | Semana | Estado |
|----|--------|--------|
| N0 | 3–10 jun 2026 (prueba) | ✓ |
| N1 | 8–14 jun | ✓ |
| N2 | 15–21 jun | ✓ |
| N3 | 22–28 jun | ✓ |
| N4 | 29 jun–5 jul | ✓ (generado 6-jul) |
| N5 | 6–12 jul | ✓ (generado 13-jul · 39 art. de 203 revisados) |
| **N6** | **13–19 jul** | ✓ (generado 20-jul · 48 art. de 248 revisados) · WhatsApp PENDIENTE |
| **N7** | **20–26 jul** | → **lunes 27-jul** (siguiente) |

**Regla de numeración/fecha:** el número y el periodo se CALCULAN de la fecha real
del sistema (`date`), NUNCA de memoria. Ventana = semana natural anterior (lunes-domingo).
N1 = semana 8-14 jun; cada semana suma 1. Contrasta siempre con el repo (`ls n*`).

---

## 3. Dónde está todo

- **Carpeta del proyecto:** `~/Documents/Claude/Briefing Cardiovascular/`
  - Subcarpeta por número: `Briefing Cardiovascular_N<n>/` con los HTML locales
    (`Briefing Cardiovascular_N<n>.html`, `Cardio al día_N<n>.html`,
    `Briefing Cardiovascular_N<n>_artículos revisados.html`).
  - `Briefing Cardiovascular_metodología y criterios.html` — FIJO (no se regenera).
- **Repo (= carpeta de publicación en GitHub Pages):**
  `~/Documents/Claude/Briefing Cardiovascular/briefing-cardiovascular-repo/`
  (rama `main`, origin = github.com/domingomarzal/briefing-cardiovascular, push por llavero).
  - `n<n>/index.html` (Briefing), `n<n>/cardio-al-dia.html` (Cardio al día),
    `n<n>/articulos-revisados.html` (auditoría). `metodologia.html` en la raíz (FIJO).
  - `generador/` — todos los scripts (ver §5).
- **URLs en vivo:** `https://domingomarzal.github.io/briefing-cardiovascular/n<n>/`
  y `.../n<n>/cardio-al-dia.html` y `.../n<n>/articulos-revisados.html`.
- **La SKILL (instrucciones maestras de la tarea):**
  `~/.claude/scheduled-tasks/pulso-cardiologico-semanal/SKILL.md` — **fuente de verdad
  del pipeline**. Léela entera; recoge TODAS las reglas acordadas.

---

## 4. La tarea automática

- **taskId:** `pulso-cardiologico-semanal` · cron `0 8 * * 1` (lunes 08:00, dispara ~08:06).
- **Activa.** Última: 13-jul (N5). Próxima: **20-jul (N6)**.
- Requiere que el **Mac esté encendido y con Claude abierto** a esa hora (tarea local).
  Si algún lunes no termina sola, se lanza a mano siguiendo la SKILL.
- Para verla/editarla: herramientas `mcp__scheduled-tasks__list_scheduled_tasks` /
  `update_scheduled_task`.

### 4.1 Dónde vive la tarea (y cómo se ata a esta carpeta) — investigado 16-jul-2026

La rutina tiene **dos piezas y ninguna está en la carpeta del proyecto**:

1. **La definición** — `~/.claude/scheduled-tasks/pulso-cardiologico-semanal/SKILL.md`
   (+ los `gen_briefing_N0/N1*.py` históricos). Es **global**. Todas sus rutas son
   ABSOLUTAS, así que la rutina no depende de dónde se ejecute.
2. **El registro del planificador** — un JSON **único para toda la app**:
   `~/Library/Application Support/Claude/claude-code-sessions/<workspace>/<proyecto>/scheduled-tasks.json`
   (hoy: `7e761a9f-…/e4f4ae28-…/`). Ahí están `cronExpression`, `enabled`, `lastRunAt`
   y — lo importante — **`cwd`**.

**`cwd` es lo ÚNICO que ata la rutina a una carpeta** (determina el directorio donde
arranca la sesión del lunes). Da igual para que el número salga: la SKILL usa rutas
ABSOLUTAS y el lunes se ejecuta bien desde cualquier carpeta (N1–N5 salieron desde UICAR).

**Estado (16-jul-2026):** se intentó fijar `cwd` en `…/Briefing Cardiovascular`, pero el
registro **revierte a `~/Documents/UICAR` en algunos reinicios de la app** (la app reescribe
ese JSON desde su estado en memoria). No se pelea: el lunes funciona igual. Efecto colateral:
la sesión automática del lunes puede reaparecer etiquetada «UICAR» en la barra lateral —
**solo la etiqueta**; el número y su publicación son correctos.

**Reglas duras (si algún día se toca el planificador):**
- `update_scheduled_task` NO expone `cwd`; solo se cambia editando el JSON con Claude
  CERRADO (⌘Q) — con la app abierta, la pisa al salir.
- NUNCA "borrar y recrear" la tarea: `create_scheduled_task` reescribe el `SKILL.md`
  (50 KB de reglas afinadas).
- Sin riesgo de permisos: `~/.claude/settings.json` global tiene `bypassPermissions`.

### 4.2 Migración del historial de sesiones — 16-jul-2026 (hecho)

Las 6 sesiones del briefing (lunes N1–N5 + la manual) se movieron del proyecto UICAR al
proyecto «Briefing Cardiovascular» para que no cuelguen de UICAR en la barra lateral. Una
sesión = metadatos `…/claude-code-sessions/<ws>/<proj>/local_<id>.json` (campos `cwd`/
`originCwd` = el chip) + transcript `~/.claude/projects/<slug-del-cwd>/<id>.jsonl` (carpeta
derivada del cwd). Migrar = mover el `.jsonl` al proyecto correcto + poner `cwd`/`originCwd`
a la ruta del Briefing. NO hay herramienta de "mover de proyecto"; el script de un solo uso
ya se borró. Mover sesiones es INDEPENDIENTE del planificador (no afecta al lunes).
Backup completo en `…/Briefing Cardiovascular/backup-sesiones-20260716-175210.tgz` — se
autoborra el 27-jul si N6 y N7 salieron (tarea `limpiar-backups-migracion`); restaurar con
`tar xzf <bk> -C ~` con Claude cerrado.

### 4.3 La sesión automática del lunes queda bajo Briefing (automático) — 16-jul-2026

Como el `cwd` del planificador revierte a UICAR (§4.1), cada lunes la sesión automática nace
etiquetada «UICAR». Para corregirlo SIN pelear con el planificador hay un **trabajo del sistema
(launchd)** que cada **lunes a las 10:00** (tras la ejecución de las 08:06) mueve esa sesión al
proyecto «Briefing Cardiovascular». No crea ninguna sesión de Claude y sobrevive a reinicios
(por eso se usa launchd y no una tarea de Claude, que además revierten/desaparecen).
- Agente: `~/Library/LaunchAgents/com.dmarzal.briefing-relabel.plist`
- Script: `~/Library/Application Support/briefing-relabel/relabel.py` — solo toca sesiones con
  título EXACTO «Pulso cardiologico semanal» y `cwd`=UICAR, salta las activas (mtime <30 min);
  idempotente. Se apoya en que la app NO reescribe metadatos de sesiones inactivas (comprobado).
- Log: `~/Library/Logs/briefing-relabel.log`
- Comprobar: `launchctl print gui/$(id -u)/com.dmarzal.briefing-relabel`
- Quitar: `launchctl bootout gui/$(id -u)/com.dmarzal.briefing-relabel` + borrar el plist y el script.
NO toca el planificador, el `SKILL.md` ni el repo → no afecta a la generación del lunes.

---

## 5. Pipeline (cada lunes, en este orden)

1. **Auditoría PRIMERO** (es la fuente de verdad; de su ranking salen Destacado, Top 3 y los 50).
2. **Briefing + Cardio al día** (bilingües) desde esa selección.
3. **Borrador de correo** al final.

Scripts en `generador/`:
- `gen_bilingue.py` — genera las **dos variantes bilingües** (Briefing + Cardio al día)
  de un número. Añade la config del número nuevo en `CONFIGS` (data, num, period, dest,
  top3, acr, viz, rutas). Se ejecuta `python3 gen_bilingue.py n<n>`.
- `gen_audit_N<n>.py` — genera la auditoría del número (a partir de corpus/eligible/tasks).
- `add_audit_filters.py <audit>` — (re)construye los desplegables Revista y Tipo.
- `add_audit_links.py <audit>` — pone enlace clicable en TODOS los artículos revisados.

**Dos trampas del `gen_audit_N<n>.py` (detectadas y corregidas en N6 — al copiar el script
del número anterior, comprobar que siguen corregidas):**
1. Al inyectar `window.PUBMED_DATA`, usar `re.sub(..., lambda _m: json_str, ...)`, NUNCA
   pasar el JSON como cadena de reemplazo: `re.sub` interpreta sus barras invertidas y
   rompe el JSON (`add_audit_links.py` falla con «Invalid \escape»).
2. `add_audit_links.py` casa por TÍTULO EXACTO. Las filas llevan el título sin punto final,
   así que `PUBMED_DATA` debe llevarlo también (`title.rstrip(".")`); si no, solo enlaza un
   puñado de filas. Comprobar siempre: nº de `class="artlink"` == nº de filas.

---

## 6. Reglas duras (NO romper)

- **Fecha = publicación ONLINE en la web de la revista.** El `ArticleDate` de PubMed puede
  engañar (fecha antigua aunque el número online sea de esta semana): verifica en la web de
  la revista (NEJM «updated on… at NEJM.org»; JACC/Elsevier «Available online»…). Esa fecha
  online MANDA. (Ej. HELIUS/AVANT GUARD entraron en N3 por esto.)
- **31 revistas** de nivel 1-3 (lista en la SKILL, PASO 1).
- **Tipos de artículo canónicos** (18 elegibles + no elegibles), homogéneos. Documentos de
  sociedad por su designación real: **Scientific Statement** (AHA/ACC) vs **Documento de
  consenso** (ESC/grupos) vs **Guía de práctica clínica**.
- **Sección 9 = «Cardiología intervencionista»** (sin «y estructural»).
- **5 artículos por sección** (si una no reúne 5, deja los que haya).
- **Rúbrica 6 ejes** REL 20 · CAMBIO 25 · EVID 20 · EFECTO 15 · REP 12 · FI 8.
  Prioridad: 🔴 Imprescindible (CAMBIO≥8 o TOTAL≥8) · 🟠 Relevante 5-7,9 · 🟢 Complementario <5.
- **Fichas:** Resultados = cifras del abstract, esquemáticas (sin omitir ninguna);
  Conclusiones = fieles al abstract. Sin inventar nada.
- **Cabecera nueva:** Nº + fecha abajo-derecha, pestaña ESP/ENG a esa altura abajo-izquierda.
- **Figura del Destacado SIEMPRE dentro de `<div class="d-viz">…</div>`** (si el `<svg>` va
  suelto, sale gigante y rompe la cabecera).
- **Enlaces de revista SIN flecha ↗** (solo subrayado al pasar el cursor).
- **Auditoría:** enlace clicable en cada artículo revisado (seleccionado y descartado).
- **Borrador:** solo `create_draft` (NUNCA enviar). Asunto **«Cardio al día_N<n>»**, con el
  HTML de Cardio al día (banner navy nativo, sin imagen; Gmail borra las `<img>`). **No se
  genera imagen de cabecera.**
- **Distribución del Cardio al día (regla 13-jul, act. 16-jul-2026):** el `Cardio al día_N<n>.html` va a `~/Documents/UICAR/Cardio al dIA/` (PERMANENTE, fuente de verdad) + una COPIA TEMPORAL en `~/Desktop/` (para comprobar que se generó; el usuario la revisa y la borra — es normal que luego no esté; NO re-copiar). NO se queda en la subcarpeta de trabajo. El repo (`n<n>/cardio-al-dia.html`, web en vivo), el Briefing y la Auditoría se quedan como están. (N0–N5 ya migrados.)
- **WhatsApp (regla 16-jul-2026, PASO 8c — PROBADO en seco el 16-jul, funciona):** cada lunes, tras generar, abrir WhatsApp Desktop y dejar el `Cardio al día_N<n>.html` (desde UICAR) ADJUNTO en la pantalla de envío —listo para que el usuario pulse Enviar— en dos chats CONFIRMADOS: grupo «Sesiones y Esclavos» (aparece «…😅»; buscar sin emoji lo encuentra) y contacto «Álvaro Fernández». No enviar; solo dejar preparado y avisar. WhatsApp RENDERIZA el HTML como vista previa (no es un fichero mudo). Ojo: no guarda adjuntos como borrador persistente → solo uno a la vez y con el usuario presente. Si falla, no bloquea el pipeline: se informa en el resumen. Pasos exactos verificados en la SKILL, PASO 8c.
  **Por qué falla en las ejecuciones automáticas (N6, 20-jul-2026):** `request_access` responde
  «can't be approved during a scheduled run» — la tarjeta de permiso de macOS no puede salir dentro
  de una ejecución programada. NO es que la app esté cerrada ni el Mac bloqueado. Reintentar no sirve
  y `update_scheduled_task` no expone la lista de apps. **Arreglo (una vez, lo hace el usuario):**
  añadir WhatsApp a las apps autorizadas en los AJUSTES DE LA TAREA PROGRAMADA de la app de Claude.
  Mientras tanto: arrastrar el HTML (Escritorio o UICAR) a cada chat, o compartir el enlace en vivo.
- **Publicación:** `git add -A && commit -m "N<n>…" && push` en el repo.
- No introducir credenciales/tokens (push por llavero).

---

## 7. Prompt para pegar en la sesión NUEVA

```
Abrimos el proyecto "Briefing Cardiovascular · Cardio al día". Lee primero
~/Documents/Claude/Briefing Cardiovascular/LEEME_CONTINUAR.md y la SKILL en
~/.claude/scheduled-tasks/pulso-cardiologico-semanal/SKILL.md para cargar todo el
contexto y las reglas. Luego confírmame: (1) la fecha de hoy (con `date`), (2) qué
número toca y su semana, (3) que la tarea automática de los lunes a las 8:00 sigue
activa y cuándo es la próxima ejecución. No regeneres nada salvo que te lo pida;
solo ponte al día del estado del proyecto.
```
