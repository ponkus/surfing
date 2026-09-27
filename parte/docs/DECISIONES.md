# Decisiones

Formato: fecha · decisión · por qué · (quién). Lo más nuevo arriba.

- **2026-09-27** · Diseño fijo 1280×800 escalado con `transform: scale` (no layout fluido), y app instalable (PWA) en pantalla completa. · En la tablet, con las barras de Chrome, el layout fluido se pisaba. Escalar garantiza la misma composición en cualquier pantalla; la PWA elimina las barras sin root ni apps de kiosco. · (Claude app, a partir de la foto de Maiky)
- **2026-09-27** · El proyecto vive en `ponkus/surfing/parte/` y se publica con el GitHub Pages que ya existía. · Hosting gratis ya andando; las cámaras de estadodelmar del mismo repo se pueden integrar a la app. · (Claude app)
- **2026-09-27** · Memoria compartida: `CLAUDE.md` + `parte/docs/*` + `CHANGELOG.md`, actualizados en cada cambio. · Que Claude Code, la app de Claude y Maiky sepan siempre qué se hizo y por qué. · (Maiky / Claude app)
- **2026-09-26** · Animación ligada a datos reales (mar = altura/período/marea, rayas = viento, cielo = hora) y no video de fondo ni Higgsfield. · Tablet modesta; y la animación comunica información. Higgsfield queda para logo/marca en la fase ESP32. · (Claude app)
- **2026-09-26** · Web app en un solo HTML, sin frameworks; tablet en modo kiosco **sin root**. · Iterar rápido, correr en tablet/celu/compu; root en tablet genérica = riesgo de brickearla sin beneficio seguro. · (Maiky / Claude app)
- **2026-09-26** · Fase 1 en tablet TJD MT-1025; la ESP32 después, con el modelo calibrado. · Pantalla grande y cero espera de hardware para juntar ratings. · (Maiky)
- **2026-09-26** · Protección de batería con ESP32 + relé + MacroDroid (80 %/40 %) en vez de root o enchufe temporizado. · Sin root Android no corta la carga; más barato que un enchufe inteligente; le da uso a la ESP32. · (Claude app)
- **2026-09-26** · Rating con 3 datos separados: tamaño observado, estrellas y fuente. · Tamaño calibra la física; estrellas calibran el gusto; mezclarlos en un número no deja aprender. · (Claude app, a partir de la idea de Maiky)
- **2026-09-26** · Marea modelada con γ (altura/profundidad sobre el banco) en vez de "media marea = mejor". · Explica lo que Maiky observa en Biología y predice que la marea ideal depende del tamaño. · (Maiky + Claude app)
- **2026-09-26** · Bombeo como bonus chico que se valida con datos. · Plausible físicamente, pero puede ser sesgo de memoria. · (Maiky + Claude app)
- **2026-09-26** · Usar swell primario + secundario + mar de viento, no solo el primario. · Con un solo swell el modelo se perdía el NE que favorece al Yacht (comparado con Surfline). · (Claude app)
- **2026-09-26** · Geometría calculada desde OpenStreetMap en vez de pedirle reglas a Maiky. · Maiky: "do your math". Y reprodujo sus reglas de viento sola. · (Maiky)
- **2026-09-26** · Datos de Open-Meteo; no scrapear Surfline. · Gratis, sin key, CORS; Surfline lo prohíbe en sus términos. · (Claude app)
- **2026-09-26** · Placa ESP32 recomendada para fase 2: Guition JC3248W535 (S3, 3.5", PSRAM). · Más pantalla y memoria que la S3 1.47" y la CYD 2.4" por poca diferencia de precio. · (Claude app)
