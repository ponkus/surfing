# Estado del proyecto

**Leer primero.** Actualizar al terminar cada tarea. Última actualización: 2026-09-27 (Claude app).

## Hecho
- Geometría real de Playa Grande (OSM) y tablas de exposición/viento por pico (`model/`).
- Modelo físico v2: 3 componentes de ola, sombra de escolleras, viento por fetch, marea con γ, bombeo (ver `docs/MODELO.md`).
- App v2 (`src/app.template.html` → `index.html`): diseño nuevo con cielo según la hora, mar animado con datos reales, dial por pico, marea con ventanas de bombeo, clima, hoy + 2 días, "próxima buena", ratings con exportación.
- Tests headless con datos reales (`tests/run.py`): 4 horarios, flujo de rating. Pasan.
- Documentación y memoria compartida (este archivo, `CLAUDE.md`, `DECISIONES.md`, `CHANGELOG.md`).

## En curso
- **Tablet TJD MT-1025**: revivió con cargador USB-A. Falta: versión exacta de Android, RAM y chip (Ajustes → Acerca de). Con eso: ¿versión completa o `?lite`?
- **Publicar**: la rama `parte-app` está lista; falta mergearla a `main` para que Pages publique `ponkus.github.io/surfing/parte/`.
  (La app de Claude no tiene permiso de push al repo todavía — ver "Abierto".)

## Siguiente (en orden)
1. Mergear a `main` y abrir `https://ponkus.github.io/surfing/parte/` en la tablet.
2. Configurar la tablet: debloat por ADB, modo kiosco, que abra la app al prender.
3. Ratings a **Google Sheet** (Apps Script Web App → `CFG.SHEETS_URL`), para no depender de la tablet.
4. **Marea oficial del SHN** (Mar del Plata): reemplazar/corregir `TIDE_OFFSET_MIN`.
5. Integrar las **cámaras** de estadodelmar (Playa Grande / Yacht) en la app, al lado de "Calificar" — ya están en `surf.html`.
6. Calibración: script que lea los ratings exportados y ajuste `SIZE_CAL`, `D_BAR`, bombeo (después de ~20 ratings).
7. Protección de batería: ESP32 + relé + MacroDroid.
8. Fase 2: portar a ESP32-S3 (JC3248W535).

## Abierto / dudas
- Push desde la app de Claude: falta instalar la **Claude GitHub App** en la cuenta `ponkus` (o reconectar GitHub en claude.ai → Conectores). Mientras tanto, Claude Code o Maiky mergean.
- Sobreestimación de tamaño con mar corto (5–6 s): esperar ratings antes de tocar `SIZE_CAL`.
- ¿Tamaño real de los bancos (`D_BAR`)? Se calibra con ratings.
- ¿El bombeo es real o memoria selectiva? Se mide con ratings.
