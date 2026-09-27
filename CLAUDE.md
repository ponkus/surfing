# CLAUDE.md — repo `ponkus/surfing`

Leé este archivo entero antes de tocar nada. Lo leen **todas** las instancias de Claude que trabajan en este repo
(Claude Code, la app de Claude, etc.). Es la forma de que lo que hace una la entienda la otra.

## Qué es este repo

Sitio estático publicado con **GitHub Pages** (`.github/workflows/static.yml` publica TODO el repo en cada push a `main`).
URL: `https://ponkus.github.io/surfing/`

Tiene dos cosas independientes:

| Parte | Archivos | Qué es |
|---|---|---|
| Cámaras (lo viejo) | `index.html`, `cams.html`, `cams2.html`, `surf.html`, `resources/` | Visor de cámaras en vivo de Mar del Plata (streams `.m3u8` de estadodelmar.com.ar). Hecho a mano, jQuery. |
| **Parte de olas** (lo nuevo) | `parte/` | App que recomienda **en qué pico de Playa Grande meterse (Biología o Yacht)**, con modelo físico propio, marea, clima y ratings para entrenar el modelo. Corre en una tablet dedicada. |

**No romper las páginas de cámaras.** Si un cambio en `parte/` necesita tocar algo fuera de `parte/`, avisar primero.

## Regla de oro: memoria compartida del proyecto

1. **Al empezar**: leer `parte/docs/ESTADO.md` (qué está hecho, qué sigue, qué está abierto).
2. **Al terminar cualquier cambio**:
   - agregar una entrada arriba de todo en `parte/CHANGELOG.md` (fecha, quién — "Claude Code" / "Claude app" / "Maiky" —, qué y por qué);
   - actualizar `parte/docs/ESTADO.md`;
   - si se tomó una decisión de diseño o de modelo, agregarla a `parte/docs/DECISIONES.md`;
   - si cambió la física o un parámetro del modelo, actualizar `parte/docs/MODELO.md`.
3. Commits chicos con mensaje en español que diga qué y por qué.

Si no se actualizan estos archivos, la próxima instancia de Claude trabaja a ciegas.

## Estructura de `parte/`

```
parte/
  index.html              ← GENERADO. Lo que publica Pages y abre la tablet. NO editar a mano.
  build.py                ← arma index.html = src/app.template.html + model/tables.json
  src/app.template.html   ← LA APP (HTML+CSS+JS en un solo archivo). Se edita acá.
  model/
    geo.py                ← geometría real de Playa Grande (escolleras y costa de OpenStreetMap)
    model.py              ← física: exposición al swell por pico, reparo del viento, puntaje
    export_tables.py      ← precalcula model/tables.json (lookup tables que usa la app)
    tables.json           ← GENERADO por export_tables.py
    plot.py               ← gráfico diagnóstico de la geometría (opcional)
  tests/
    run.py                ← prueba headless con datos reales guardados + capturas en tests/out/
    fixtures/             ← respuestas reales de Open-Meteo (26/09/2026)
  docs/
    PROYECTO.md           ← visión, usuario, hardware, fases
    MODELO.md             ← la física y los parámetros, con fórmulas
    DECISIONES.md         ← registro de decisiones con fecha y motivo
    ESTADO.md             ← hecho / siguiente / abierto  (leer primero)
  CHANGELOG.md
```

## Comandos

```bash
python3 parte/build.py                      # SIEMPRE después de editar src/app.template.html
python3 parte/tests/run.py                  # SIEMPRE antes de commitear (tiene que decir OK)
cd parte/model && python3 export_tables.py  # solo si cambió geo.py / model.py (requiere shapely, numpy)
```
Tests requieren `pip install playwright` y Chromium. Las capturas quedan en `parte/tests/out/` (ignorado por git): miralas.

## Reglas técnicas de `parte/`

- **Un solo archivo HTML, sin npm ni bundlers ni frameworks.** Vanilla JS. Única dependencia externa: Google Fonts (Outfit). Tiene que andar si la fuente no carga.
- **Datos**: Open-Meteo (gratis, sin API key, permite CORS desde el navegador). Marine API + Forecast API. No usar APIs pagas ni scrapear Surfline (va contra sus términos).
- **Hardware objetivo**: tablet TJD MT-1025, Android 11, 10.1", apaisada 1280×800, siempre prendida en modo kiosco. Es modesta: animación limitada a ~30 fps, pausa cuando la pestaña está oculta, modo `?lite` (sin blur, 15 fps). No agregar nada pesado (videos de fondo, librerías grandes).
- **Todo lo configurable está en el objeto `CFG`** al principio del `<script>` (coordenadas, desfase de marea, profundidad de bancos, calibración de tamaño, etc.).
- **Textos de la interfaz en español rioplatense.** Horarios 24 h. Metros y km/h.
- **Ratings = datos de entrenamiento. No romper su formato.** Se guardan en `localStorage["pg_ratings"]` con: hora exacta, pico, tamaño observado, estrellas, fuente (agua/cámara/orilla), **el pronóstico que la app tenía en ese momento** y la predicción del modelo (`pred.model` = versión). Si se cambia el modelo, subir la versión en `pred.model`. Si se cambia el formato, escribir migración y anotarlo en DECISIONES.md.
- La física en JS (`src/app.template.html`, sección FÍSICA/MODELO) y en Python (`model/model.py`) tienen que decir lo mismo. Si cambiás una, cambiá la otra o dejá anotado por qué difieren.

## Sobre Maiky (el usuario)

- Hace bodyboard en **Playa Grande, Mar del Plata**. Dos picos: **Biología** (escollera chica, al norte) y **Yacht** (pegado a la escollera Norte, larga, al sur, junto a la boca del puerto).
- Consultor de marketing, no programador: explicar en simple, en español, sin jerga innecesaria.
- Quiere que lo desafíen: si una idea suya tiene un supuesto flojo, decírselo con argumentos.
- Cuando se le dan pasos para hacer a mano, **de a uno** y esperar que confirme antes del siguiente.
- Su conocimiento local vale oro: está anotado en `parte/docs/MODELO.md` (reglas de viento, marea, "bombeo").

## Glosario

- **Biología / Yacht**: los dos picos de Playa Grande. En el código: `"Biologia"` y `"Yacht"`.
- **Swell**: tren de olas que viene de lejos (altura, período, dirección). Open-Meteo da primario, secundario y mar de viento.
- **Período (s)**: segundos entre olas. Más largo = más energía.
- **Offshore / onshore**: viento de tierra al mar (bueno) / del mar a tierra (malo). En Playa Grande offshore puro ≈ 285° (ONO).
- **γ (gamma)**: altura de ola ÷ profundidad sobre el banco. ~0.7–1.05 rompe bien; bajo = ola "gorda"; alto = rompe afuera.
- **Bombeo**: término local — en el cambio de marea suelen entrar olas, más con período largo. El modelo le da un bonus chico que se valida con ratings.
- **Rating**: calificación que carga Maiky (pico + tamaño + estrellas + fuente) para calibrar el modelo.
