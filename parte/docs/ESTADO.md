# Estado del proyecto

**Leer primero.** Actualizar al terminar cada tarea. Última actualización: 2026-09-27 11:30 (Claude app).

## Hecho
- Geometría real de Playa Grande (OSM) y tablas de exposición/viento por pico (`model/`).
- Modelo físico v2: 3 componentes de ola, sombra de escolleras, viento por fetch, marea con γ, bombeo (ver `docs/MODELO.md`).
- App v2 (`src/app.template.html` → `index.html`): diseño nuevo con cielo según la hora, mar animado con datos reales, dial por pico, marea con ventanas de bombeo, clima, hoy + 2 días, "próxima buena", ratings con exportación.
- Tests headless con datos reales (`tests/run.py`): 4 horarios, flujo de rating. Pasan.
- Documentación y memoria compartida (este archivo, `CLAUDE.md`, `DECISIONES.md`, `CHANGELOG.md`).
- **Publicada** en `https://ponkus.github.io/surfing/parte/` (PR #4). Probada en la tablet: fluida, pero se pisaba dentro de Chrome → arreglado (encaje 1280×800 escalado + pantalla completa + app instalable), en PR #5.

## En curso
- **Tablet TJD MT-1025**: revivió con cargador USB-A. Anda fluida en la versión completa (no hace falta `?lite` por ahora). Falta dato de Android/RAM/chip (no urgente).
- PR #5 publicado: en la tablet se ve bien, sin bloques pisados.
- **Preparar la tablet por ADB** (lo hace Claude Code desde la Mac): seguir `docs/TABLET.md`. Pendiente que Maiky active la depuración USB.
- Batería baja rápido: probablemente degradada por la descarga profunda (hardware). La limpieza no lo arregla; va a vivir enchufada.

## Siguiente (en orden)
1. Preparar la tablet por ADB (`docs/TABLET.md`) — Claude Code en la Mac.
2. Instalar **Fully Kiosk Browser** y apuntarlo a la app (Chrome no ofrece "Agregar a pantalla principal" en esta tablet).
3. Ratings a **Google Sheet** (Apps Script Web App → `CFG.SHEETS_URL`), para no depender de la tablet.
4. **Marea oficial del SHN** (Mar del Plata): reemplazar/corregir `TIDE_OFFSET_MIN`.
5. Integrar las **cámaras** de estadodelmar (Playa Grande / Yacht) en la app, al lado de "Calificar" — ya están en `surf.html`.
6. Calibración: script que lea los ratings exportados y ajuste `SIZE_CAL`, `D_BAR`, bombeo (después de ~20 ratings).
7. Protección de batería: ESP32 + relé + MacroDroid.
8. Fase 2: portar a ESP32-S3 (JC3248W535).

## Abierto / dudas
- Push: la app de Claude ya puede pushear ramas y abrir PRs. **El merge a `main` lo hace Maiky** (el sistema no deja que Claude mergee sin revisión humana).
- Netlify (`UNMDP/surfcam`) está conectado al repo y falla en cada PR porque busca la carpeta `surf2`, que no existe. No afecta a GitHub Pages. Arreglo: vaciar "Base directory" en Netlify o desconectarlo.
- Sobreestimación de tamaño con mar corto (5–6 s): esperar ratings antes de tocar `SIZE_CAL`.
- ¿Tamaño real de los bancos (`D_BAR`)? Se calibra con ratings.
- ¿El bombeo es real o memoria selectiva? Se mide con ratings.
