# Briefing Cardiovascular N21 (26 oct - 1 nov 2026) — REDACCIÓN DE FICHAS

Trabajas en ESPAÑOL (y en inglés para la versión `en`). Audiencia: cardiólogos clínicos generales.
NO uses la palabra «newsletter». RIGOR ABSOLUTO: fidelidad estricta al abstract. **NUNCA inventes
cifras, clases de recomendación, niveles de evidencia, valores p ni intervalos de confianza.** Si un
dato no está en el abstract, se omite. No editorialices en «conclusiones».

## Entrada / salida
Lees `n21_w<B>.json` (lista de artículos con key, journal, doi, seccion, ptype, acr, prio, title,
abstract) y escribes `n21_data<B>.json`: un DICCIONARIO {key: ficha}. Una entrada por artículo, con
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

## ⚠️ NOTA ESPECÍFICA DE ESTA EJECUCIÓN (nube, 2-nov-2026)
La red de este entorno **solo** alcanza api.crossref.org, eutils.ncbi.nlm.nih.gov y
domingomarzal.github.io. doi.org, nejm.org, jacc.org, sciencedirect.com, ahajournals.org,
jamanetwork.com, escardio.org y eurointervention.pcronline.com devuelven HTTP 000, y `WebFetch`
falla con ENOTFOUND. **No pierdas tiempo intentándolo.** `WebSearch` sí funciona, pero úsalo como
mucho una vez y SOLO para contexto del «por qué importa»: **ninguna cifra puede salir de ahí**.

### ⭐ El artículo `a33` (si está en tu lote): N Engl J Med, ensayo P4, SIN ABSTRACT
`a33` = «Coronary CT Angiography versus Intravascular Ultrasound Guidance for PCI»
(10.1056/NEJMoa2610771). Llega con el campo `abstract` **VACÍO**. Es un late-breaker del congreso
TCT 2026 publicado en NEJM el 1-nov-2026 que PubMed no había indexado; entra por INCLUSIÓN
OBLIGATORIA (todo artículo cardiovascular de NEJM entra siempre), y la regla del abstract no lo
descarta. **No se ha podido verificar ninguna cifra**: nejm.org es inaccesible y las únicas fuentes
secundarias localizadas son notas de prensa del patrocinador con los valores truncados.
Redacta su ficha ASÍ, y SIN INVENTAR NADA:
- `deque`: es un ensayo aleatorizado de NO INFERIORIDAD que compara la planificación de la
  intervención coronaria percutánea guiada por **angio-TC coronaria** frente a la guiada por
  **ecografía intravascular (IVUS)**; se presentó como late-breaker en el TCT 2026 y se publicó
  simultáneamente en N Engl J Med. Di explícitamente que el detalle del diseño, el tamaño de la
  muestra y el margen de no inferioridad deben consultarse en el artículo original.
- `resultados`: **NO pongas ninguna cifra.** Escribe únicamente que el ensayo alcanzó su objetivo
  de no inferioridad —la guía por angio-TC no fue inferior a la guía por IVUS en el objetivo
  primario clínico a 12 meses— y que los resultados numéricos (incidencias, intervalos de confianza
  y margen de no inferioridad) **no han podido verificarse en la fuente original y deben consultarse
  en el artículo**. Añade que en las comunicaciones del congreso se describieron además
  procedimientos más cortos y menos contraste con la guía por angio-TC, sin dar cifras.
- `conclusiones`: refleja solo lo anterior, sin añadir matices propios.
- `why`: por qué importa que una técnica NO invasiva de planificación pueda sustituir a la imagen
  intracoronaria; y advierte de la limitación de que la ficha se ha redactado sin acceso al texto
  completo.
⛔ Ni un solo número en `resultados` de `a33`. Es preferible una ficha honesta y corta.

### ⭐ Los documentos de sociedad de esta semana (`ptype` "Scientific Statement")
Tres documentos de la AHA/AAP/ACOG/SMFM sobre salud cardiovascular de la mujer (el Scientific
Statement de la «Consensus Guidance», el Presidential Advisory del «Female-Specific Life Course
Approach» y el Science Advisory de los «Comprehensive Centers of Excellence»). Sus abstracts SÍ
están completos: redacta sus `resultados` como **LISTA de cadenas** con las novedades y mensajes
clave **que consten en el abstract**. Si el abstract no enumera recomendaciones con clase y nivel,
NO los inventes: escribe los puntos que sí constan (alcance, construcción de las 4 etapas vitales
—perimenarquia, ciclo ovárico, perimenopausia, posmenopausia—, dominios hormonal/psicosocial/
cardiovascular, el papel del embarazo como evento modificador, la llamada a la acción) y cierra con
un punto honesto del tipo «El detalle de las recomendaciones por etapa vital debe consultarse en el
documento original.» ⛔ JAMÁS inventes clases de recomendación (I/IIa/IIb/III) ni niveles (A/B/C).
