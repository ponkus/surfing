# Modelo físico — cómo se pasa del pronóstico mar adentro a la ola en cada pico

Versión del modelo en la app: **v3** (28/09/2026) (`pred.model` en cada rating).

## 1. Geometría (medida, no supuesta)
Fuente: OpenStreetMap (Overpass), 26/09/2026. Coordenadas en `model/geo.py`.
- Costa de Playa Grande: rumbo **15°** (NNE–SSO). La playa **mira a 105° (ESE)** = `NORMAL`. Offshore puro **285° (ONO)**.
- Escollera **Norte** (larga, al sur de la playa, apunta al SE) → le queda a 77–200 m al pico **Yacht**.
- Escollera de **Biología** (chica, al norte) → ~100 m del pico Biología. Más al norte, Cabo Corrientes.
- Escollera **Sur** del puerto, más lejos (1–1.5 km).
- Picos (`SPOTS`): ~120 m mar adentro de la orilla, pegados a cada escollera.

## 2. Exposición al swell por pico (`exposure`)
Para cada dirección se tira un rayo desde el pico: si pega en una escollera o costa, la ola llega difractada
(0.20 si el obstáculo está a <300 m, 0.45 si a <1 km, 0.65 si más lejos). Además pierde por entrar cruzada:
`Kr = sqrt(cos Δ)` con Δ = ángulo contra 105° (mínimo 0.25 entre 60–90°, y cae a 0 hasta 130° por refracción en la plataforma).
Se promedia con dispersión direccional según período: ±45° (<8 s), ±30° (8–11 s), ±20° (≥11 s).

| Swell desde | Biología | Yacht | Gana |
|---|---|---|---|
| NE 45° | 0.26 | 0.68 | Yacht |
| ENE 60° | 0.57 | 0.82 | Yacht |
| E–ESE 90–120° | ~0.97 | ~0.95 | parejo |
| SE 135° | 0.83 | 0.54 | Biología |
| SSE 150° | 0.59 | 0.26 | Biología |
| S 180° | 0.23 | 0.10 | Biología |

→ ventanas complementarias: explica por qué "si rompe en uno, rara vez rompe en el otro".

## 3. Viento (`local_wind_factor`, `windScore`)
Fracción del viento que ensucia el pico según el agua libre que tiene a barlovento (fetch hasta la primera escollera/costa):
`min(1, sqrt(fetch/1500 m))`; viento de tierra (>115° de la normal) = 0.
**Reproduce las reglas de Maiky sin habérselas cargado**:
- S, SSE, SE, SSO → Yacht reparado (la escollera Norte le deja ~100 m de fetch).
- N, NNE, NE → Biología reparado.
- SO, O, NO → offshore, limpio en los dos. (Maiky dijo "NO repara Biología"; el modelo lo ve como offshore en ambos.)
- ENE, E, ESE → onshore en ambos.
Puntaje: offshore → 1 (baja si >30 km/h); si no, `1 − v × reparo × max(onshore, 0.35) / 22`.
**v3**: `v = máx(sostenido, 0.65 × ráfaga)` y `reparo = factor + (1 − factor) × 0.6 × clamp((v − 15)/25, 0, 1)`:
la escollera tapa el picado de cerca, pero con 30–40 km/h el mar revuelto entra igual (caso 28/09: NE 21, ráfagas 44 → Biología ya no "reparado").

## 4. Altura en rompiente
Por cada componente (swell 1, swell 2, mar de viento): `Hb = 0.39 · g^0.2 · (T · H0²)^0.4` (Komar & Gaillard 1973) × exposición × `sizeT(T)`.
**v3** `sizeT(T) = clamp(0.5 + 0.125·(T − 5), 0.5, 1)`: la ola de 5 s o menos rinde la mitad como ola surfeable (se rompe desordenada, espuma), la de 9 s o más entera.
Antes era mar de viento ×0.6 y swell ×1, que sobreestimaba días de temporal (28/09: 0.9–1.4 m pronosticado, mucho menos real). Provisorio: calibrar con ratings.
Se combinan: `Hb = sqrt(Σ Hb_i²) × SIZE_CAL[pico]`. Se muestra como rango `0.8·Hb – 1.2·Hb`.

## 5. Marea (γ sobre el banco) — conocimiento local de Maiky
"Con marea muy baja en Biología la ola es muy chica; con muy alta se ve más grande pero es gorda y cuesta remarla."
Modelo: `γ = Hb / (D_BAR[pico] + η)`, η = nivel del mar respecto de la media.
- γ > 1.05 → rompe afuera / poca agua (penaliza) · 0.7–1.05 → rompe en el banco (ideal) · 0.55–0.7 → algo gorda · <0.55 → gorda.
- Consecuencia: **la marea ideal sube con el tamaño de la ola** (día chico → marea baja; día grande → marea alta). Validar con ratings.
- `D_BAR` inicial: Biología 1.0 m, Yacht 1.1 m. Los bancos cambian con temporales → calibrar con ratings recientes.
- Datos de marea: `sea_level_height_msl` de Open-Meteo **+ 45 min** (`TIDE_OFFSET_MIN`). Medido el 26/09 vs tabla: altura OK, pleamares ~1 h adelantadas. **Pendiente: tabla oficial del SHN.**

## 6. Bombeo — conocimiento local de Maiky
"En el cambio de marea se producen olas, sobre todo con olas medianas o períodos largos."
Hipótesis física: corriente de marea que se invierte (la boca del puerto está al lado del Yacht → más efecto ahí) + ola larga más sensible al fondo.
Modelo: dentro de ±45 min de pleamar/bajamar y con Hb 0.5–1.6 m → puntaje × (1 + 0.07, o 0.15 si T ≥ 9 s), ×1.3 en Yacht.
**Puede ser memoria selectiva**: se valida comparando ratings cerca del cambio de marea vs el resto.

## 7. Puntaje final (0–5)
`tamaño(Hb) × viento × picado × marea(γ) × período × bombeo × (1.15 si T ≥ 9 s)` → ×5.
**Período (v3)**: `Tm = Σ(H²·T)/Σ(H²)` sobre los 3 componentes (período medio pesado por energía). Factor: 5 s 0.35 · 6 s 0.55 · 7 s 0.75 · 8 s 0.9 · 9 s+ 1 (lineal entre medio).
Mar de 5–6 s = temporal / mar de viento: aunque tenga altura, no hay ola ordenada.
Tamaño para bodyboard: 0 bajo 0.45 m, sube hasta 0.9 m, ideal 0.9–2.0 m, baja arriba de 2.5 m.

## 8. Validación hecha
- 26/09/2026 20 h, con los 3 swells de Surfline (S 0.9 m 8 s · NE 0.5 m 8 s · SE 0.2 m 10 s):
  modelo **Biología 0.62 m / Yacht 0.67 m** vs Surfline **Biología 0.3–0.6 / Yacht 0.6–0.9**. Mismo ganador.
- Probable **sobreestimación con mar corto (5–6 s)**: para el martes 29/09 el modelo da Yacht 1.1–1.6 m y Surfline 0.6–1.1 m. Candidato a corregir con `SIZE_CAL` o con ratings.

- **28/09/2026 09 h** (Maiky por cámara: mar destruido, no apto). v2: Biología 2.5★ / Yacht 1★, 0.9–1.4 m. **v3: 0–0.5★, 0.6–0.9 m.** Queda como test de regresión en `tests/run.py`.

**Referencia**: el puntaje que vale es el de la app (JS). El `evaluate` de `model.py` es simplificado (un solo swell) y sirve para diagnóstico; la geometría y las tablas sí son las de Python.

## 9. Calibración (plan)
Cada rating guarda pronóstico + predicción. Con ~20–30 ratings: ajustar `SIZE_CAL` y `D_BAR` por pico, tolerancia al viento,
factores de sombra por sector y el bonus de bombeo, con regresión simple (parámetros con sentido físico, no caja negra).
Más peso a ratings recientes (los bancos se mueven). Rateá también días malos: si no, el modelo aprende que "siempre está bueno".
