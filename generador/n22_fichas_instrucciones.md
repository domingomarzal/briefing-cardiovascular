# Briefing Cardiovascular N22 (2 - 8 nov 2026) — REDACCIÓN DE FICHAS

Trabajas en ESPAÑOL (y en inglés para la versión `en`). Audiencia: cardiólogos clínicos generales.
NO uses la palabra «newsletter». RIGOR ABSOLUTO: fidelidad estricta al abstract. **NUNCA inventes
cifras, clases de recomendación, niveles de evidencia, valores p ni intervalos de confianza.** Si un
dato no está en el abstract, se omite. No editorialices en «conclusiones».

## Entrada / salida
Lees `n22_w<B>.json` (lista de artículos con key, journal, doi, seccion, ptype, acr, prio, title,
abstract) y escribes `n22_data<B>.json`: un DICCIONARIO {key: ficha}. Una entrada por artículo, con
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

## ⚠️ NOTA ESPECÍFICA DE ESTA EJECUCIÓN (nube, 9-nov-2026)
La red de este entorno **solo** alcanza api.crossref.org, eutils.ncbi.nlm.nih.gov y
domingomarzal.github.io. doi.org, nejm.org, jacc.org, sciencedirect.com, ahajournals.org,
jamanetwork.com, escardio.org y eurointervention.pcronline.com devuelven HTTP 000, y `WebFetch`
falla con ENOTFOUND. **No pierdas tiempo intentándolo.** `WebSearch` sí funciona, pero úsalo como
mucho una vez por artículo y SOLO para contexto del «por qué importa»: **ninguna cifra puede salir
de ahí**: las cifras, solo del `abstract` que te doy.

Es la semana del congreso **AHA Scientific Sessions 2026**: muchos de tus artículos son
late-breakers. Varios son ensayos pivotales **NEUTROS** (Lp(a)HORIZON con pelacarsen, ZEUS con
ziltivekimab, RACE-CARS, OPTIMAL-DIABETES): un resultado neutro NO es un resultado menor. Redacta
el «por qué importa» explicando qué hipótesis queda en entredicho y qué se deja de hacer o de
esperar a partir de ahora; no lo maquilles buscando una lectura positiva que el abstract no
sostiene, y no insinúes beneficio donde el intervalo de confianza cruza el 1.

### ⭐⭐ ARTÍCULOS RECUPERADOS POR CROSSREF — LEE ESTO SI TU LOTE TRAE ALGUNO
Algunas entradas de tu `n22_w<B>.json` llevan tres campos extra: `nota_recuperado`,
`cifras_omitidas` y `fuentes`. Son artículos que **PubMed no había indexado** (late-breakers del
AHA publicados el 7-8 de noviembre) y cuyo contenido se reconstruyó desde fuentes secundarias
aplicando **doble fuente obligatoria** para cada cifra. Reglas para ellos:
- El campo `abstract` contiene **SOLO lo verificado por dos fuentes independientes**. Trátalo
  exactamente igual que un abstract de PubMed: es tu única fuente de cifras.
- **El campo `cifras_omitidas` dice qué cifras se descartaron a propósito** por venir de fuente
  única o por discrepar entre fuentes. ⛔ Esas cifras están PROHIBIDAS: no las reintroduzcas, ni
  siquiera si las recuerdas o las encuentras en una búsqueda. No «completes» un IC95% ni un valor
  de p que no esté en el `abstract`.
- En `resultados` escribe lo verificado y, cuando falte un dato que el lector esperaría (p. ej. el
  valor de p o el IC95%), dilo con naturalidad: «el valor de p no consta en las fuentes
  disponibles y debe consultarse en el artículo original». Es preferible una ficha honesta y corta.
- En `why` añade una frase final advirtiendo de que la ficha se ha redactado **sin acceso al texto
  completo**, a partir de la presentación en el congreso y de fuentes secundarias concordantes.
- `a46` es el **CoSTR 2026 del ILCOR** (`ptype` "Documento de consenso"): va con la estructura de
  documento de sociedad (`resultados` = LISTA de cadenas). ⛔ ILCOR usa **GRADE** (recomendación
  fuerte/débil + certeza de la evidencia), **NO** clases I/IIa/IIb/III ni niveles A/B/C: no
  escribas ninguna clase ni nivel. Solo está verificado textualmente el bloque de **parámetros de
  ventilación** del adulto; de las demás áreas (vía aérea, desfibrilación, calidad de las
  compresiones) consta únicamente que son las áreas actualizadas, así que dilo así y cierra con un
  punto honesto remitiendo al documento original.
- `a48` (ON-SCENE, soporte vital extracorpóreo prehospitalario) **NO es un ensayo aleatorizado**:
  es un estudio nacional no aleatorizado con despliegue escalonado. Dilo en `deque` y trátalo como
  tal en `why` (asociación con reserva de confusión por indicación), sin lenguaje causal.
