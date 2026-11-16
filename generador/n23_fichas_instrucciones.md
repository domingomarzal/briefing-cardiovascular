# Briefing Cardiovascular N23 (9 - 15 nov 2026) — REDACCIÓN DE FICHAS

Trabajas en ESPAÑOL (y en inglés para la versión `en`). Audiencia: cardiólogos clínicos generales.
NO uses la palabra «newsletter». RIGOR ABSOLUTO: fidelidad estricta al abstract. **NUNCA inventes
cifras, clases de recomendación, niveles de evidencia, valores p ni intervalos de confianza.** Si un
dato no está en el abstract, se omite. No editorialices en «conclusiones».

## Entrada / salida
Lees `n23_w<B>.json` (lista de artículos con key, journal, doi, seccion, ptype, acr, prio, title,
abstract) y escribes `n23_data<B>.json`: un DICCIONARIO {key: ficha}. Una entrada por artículo, con
la key EXACTA. Valida con python3 que el JSON carga y que tiene tantas claves como artículos.

## Estructura de cada ficha
```
{"title_en": "...", "title_es": "...",
 "es": {"resumen": "...", "why": "...", "deque": "...", "resultados": "...", "conclusiones": "..."},
 "en": {"resumen": "...", "why": "...", "deque": "...", "resultados": "...", "conclusiones": "..."}}
```

### Títulos
- `title_en` = el título ORIGINAL en inglés, TAL CUAL lo da PubMed, **sin punto final**. Si el campo
  `acr` no está vacío y el acrónimo NO aparece ya en el título, añádelo al final entre paréntesis:
  `... after myocardial infarction (TARGET-D)`.
- `title_es` = traducción al español del mismo título, sin punto final, con el mismo acrónimo entre
  paréntesis si procede. Traducción profesional, terminología cardiológica española.

### Campos de texto (español en `es`, inglés en `en`; el contenido debe ser el MISMO)
- `resumen`: directo, SIN etiquetas tipo «En 2 líneas:» ni «Publicado en». De qué va + el RESULTADO
  PRINCIPAL con su cifra y dirección del efecto. Ideal 2 líneas, máximo 3.
- `why`: el «Por qué importa». **Empieza en MINÚSCULA** (la plantilla ya antepone «Por qué importa:»).
  Qué aporta de NUEVO o DIFERENTE frente a lo que se sabía; matiza las limitaciones reales (objetivo
  secundario, multiplicidad, observacional, etc.). 3-6 frases.
- `deque`: el párrafo «De qué va.» del pop-up = contexto + objetivo + método (el porqué del estudio).
- `resultados`: TODOS los resultados numéricos del abstract, traducidos y TRIMADOS de paja: n, %,
  HR/OR/RR con IC95% y p, objetivo primario y secundarios. Lo más conciso posible **sin omitir
  ninguna cifra**. En español usa coma decimal (0,85) y «IC95%»; en inglés punto decimal y «95% CI».
- `conclusiones`: traducción FIEL de la sección Conclusions del abstract. No añadas matices propios.

### ⚠️ Documentos de sociedad (`ptype` = "Guía de práctica clínica", "Scientific Statement" o
"Documento de consenso")
Cambian la estructura del pop-up:
- `deque` = alcance del documento, a quién va dirigido y a quién sustituye (versión previa y año, si
  consta).
- `resultados` = **UNA LISTA DE CADENAS** (no un párrafo), con las NOVEDADES / recomendaciones nuevas
  o modificadas / mensajes clave. Orientativo 6-9 puntos, cada uno una idea autosuficiente. Incluye
  clase de recomendación y nivel de evidencia entre paréntesis SOLO si constan verificados en la
  fuente. ⛔ PROHIBIDO remitir a tablas o figuras del documento original («ver Tabla 1», «según la
  Figura 2»): el lector no las tiene delante.
- `conclusiones` = «Qué cambia en la práctica» para el cardiólogo clínico general.
En `en`, `resultados` es también una lista, con los mismos puntos traducidos.

### Reglas de formato
- Escribe los símbolos TAL CUAL: `<50%`, `≥50%`, `≤`, `×`. **NUNCA** entidades HTML (`&lt;`, `&ge;`).
- Nada de negritas ni HTML dentro de los textos (la plantilla ya pone los rótulos en negrita).
- Comillas tipográficas normales; evita saltos de línea dentro de los campos.

## Fuentes
El abstract que te doy es la fuente principal y suficiente. Puedes usar WebSearch/WebFetch para
afinar el «por qué importa» (contexto, cobertura en Medscape/TCTMD), pero **ninguna cifra puede
salir de ahí**: las cifras, solo del abstract. No pierdas tiempo si la red falla.

No toques ningún otro fichero. No hagas commit. No lances subagentes.

## ⚠️ NOTA ESPECÍFICA DE ESTA EJECUCIÓN (nube, 16-nov-2026)
La red de este entorno **solo** alcanza api.crossref.org, eutils.ncbi.nlm.nih.gov y
domingomarzal.github.io. doi.org, nejm.org, jacc.org, sciencedirect.com, ahajournals.org,
jamanetwork.com y escardio.org devuelven HTTP 000, y `WebFetch` falla con ENOTFOUND. **No pierdas
tiempo intentándolo.** `WebSearch` SÍ funciona, pero úsalo como mucho una vez por artículo y SOLO
para contexto del «por qué importa»: **ninguna cifra puede salir de ahí**; las cifras, solo del
`abstract` que te doy.

Es la semana SIGUIENTE al congreso **AHA Scientific Sessions 2026** (6-9 nov, Chicago): varios de
tus artículos son late-breakers publicados el 9 de noviembre (SYNCHRONIZE-CVOT de survodutida en
Lancet, ATTAIN-OSA de orforglipron y SURMOUNT-ADOLESCENTS de tirzepatida en JAMA, el inhibidor de
ANGPTL4 TYDAL-TIMI 78 en NEJM, PEPPER de tromboprofilaxis tras artroplastia en NEJM). Varios
ensayos de la semana son **NEUTROS** o de **seguridad cardiovascular** (no inferioridad): un
resultado neutro NO es un resultado menor. Redacta el «por qué importa» explicando qué hipótesis
queda en entredicho o qué queda demostrado (p. ej. la ausencia de exceso de riesgo CV), sin
maquillarlo buscando una lectura positiva que el abstract no sostenga, y sin insinuar beneficio
donde el intervalo de confianza cruza el 1.

Si tu lote trae un artículo de tipo «Guía de práctica clínica», «Scientific Statement» o
«Documento de consenso», recuerda que su `resultados` es una LISTA de cadenas (novedades), también
en `en`, y que NO se escriben clases ni niveles de recomendación que no consten verificados.
