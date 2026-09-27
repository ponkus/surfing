# Proyecto: Parte de olas Playa Grande

## La idea en una línea
Un aparato que Maiky mira todas las mañanas y le dice **a qué pico de Playa Grande ir (Biología o Yacht), a qué hora y por qué**, con un modelo que aprende de sus propias calificaciones.

## Por qué no alcanza con Surfline / Windguru
- Los pronósticos dan el mar **mar adentro**; lo que importa es cómo rompe en cada pico.
- En Playa Grande, **si rompe en Biología rara vez rompe en el Yacht y viceversa**, según swell, viento y marea. Ninguna app lo resuelve bien.
- Surfline tiene spots separados (Biología / Yacht) y sirvió para validar, pero es otro modelo, no la verdad.
- El diferencial: **geometría real de las escolleras + conocimiento local de Maiky + calibración con sus ratings**.

## Usuario
Maiky (Juan Luis Grassi), bodyboarder de Mar del Plata. Usa también las cámaras de estadodelmar (ver páginas viejas del repo).

## Fases
1. **Tablet (ahora)** — web app en `parte/`, publicada en GitHub Pages, abierta en una tablet dedicada en modo kiosco.
   Objetivo: usarla todos los días y juntar ratings (2–3 meses) para calibrar.
2. **ESP32 (después)** — portar el modelo ya calibrado a una placa con pantalla para regalar/vender a amigos.
   Candidata: Guition **JC3248W535** (ESP32-S3, 16 MB flash, 8 MB PSRAM, 3.5" 480×320 táctil capacitiva, con carcasa).
   Las tablas de geometría (`model/tables.json`) están pensadas para pasar tal cual a la placa (lookup tables).

## Hardware de la fase 1
- Tablet **TJD MT-1025** (modelo MT-1025QU, firmware `MT-1025QU_V1.00_20221125`), Android 11, 10.1", chip **Allwinner** `sun50iw10p1` (probablemente A133, 4 núcleos), **4 GB RAM**, batería 2800 mAh según Android. Estaba muerta por descarga profunda; revivió con cargador **USB-A 5V 2A** (el cargador USB-C del iPhone no le entrega carga).
- Plan: **sin root**. Debloat con ADB (`pm uninstall -k --user 0`), modo kiosco (p. ej. Fully Kiosk Browser).
- Protección de batería (va a estar enchufada 24/7): sin root Android no puede cortar la carga. Plan: **ESP32 + módulo relé** que corta el USB, comandado por **MacroDroid** (lee batería: corta al 80 %, reconecta al 40 %).

## Hosting y datos
- App: GitHub Pages de este repo → `https://ponkus.github.io/surfing/parte/`
- Datos: Open-Meteo (gratis, sin key). Marine API (swell, mar de viento, nivel del mar, temperatura del agua) + Forecast API (viento, clima, amanecer/atardecer).
- Ratings: hoy en `localStorage` de la tablet + botón Exportar (JSON). Plan: además a una **Google Sheet** vía Apps Script (`CFG.SHEETS_URL`).

## Qué muestra la app (v2)
Pico recomendado + tamaño + puntaje 0–5 · chips de swell/viento/marea/bombeo · próxima ventana buena · dial por pico (de dónde le entra ola) · curva de marea del día con ventanas de bombeo · agua, aire/sensación, amanecer · hoy + 2 días con mini-curvas de calidad · botón Calificar. Cielo según la hora, mar animado con los datos reales (altura, período, marea) y viento.
