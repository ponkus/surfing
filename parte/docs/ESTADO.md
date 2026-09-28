# Estado del proyecto

**Leer primero.** Actualizar al terminar cada tarea. Última actualización: 2026-09-28 (Claude app, cámaras).

## Hecho
- Geometría real de Playa Grande (OSM) y tablas de exposición/viento por pico (`model/`).
- Modelo físico v2 (ahora v3, ver abajo): 3 componentes de ola, sombra de escolleras, viento por fetch, marea con γ, bombeo (ver `docs/MODELO.md`).
- App v2 (`src/app.template.html` → `index.html`): diseño nuevo con cielo según la hora, mar animado con datos reales, dial por pico, marea con ventanas de bombeo, clima, hoy + 2 días, "próxima buena", ratings con exportación.
- Tests headless con datos reales (`tests/run.py`): 4 horarios, flujo de rating. Pasan.
- Documentación y memoria compartida (este archivo, `CLAUDE.md`, `DECISIONES.md`, `CHANGELOG.md`).
- **Tablet preparada por ADB** (27/09, Claude Code): diagnóstico, 14 apps de Google desactivadas + Opera Mini desinstalada, animaciones 0,5×, pantalla siempre prendida enchufada, 30 min a batería, brillo 50 %. Play Store actualiza solo por Wi-Fi. Después: WebView y Play Store actualizados, Chrome exento de ahorro de batería, voz de Google y Files desactivadas (3,1 GB libres tras reiniciar). Todo reversible: `docs/tablet/revertir.sh`.
- **Fully Kiosk Browser** instalado (versión gratis): abre `https://ponkus.github.io/surfing/parte/?horario=0630-1200` (horario de Maiky) en pantalla completa y arranca solo al prender. La tablet mantiene PIN (Maiky): después de un reinicio hay que desbloquearla a mano. La depuración inalámbrica se apaga en cada reinicio (Android 11); el USB no sirve para ADB en esta tablet. Detalle y diagnóstico en `docs/tablet/`.
- **Diseño v3 (27/09)**: legible a 2 m (tarjetas oscuras, tipografía grande), días tocables (el cuadro central muestra el día elegido; vuelve solo a "ahora" a los 90 s), clima del momento + aviso de lluvia, carga a prueba de cortes de Open-Meteo, arreglo del zoom en Fully. PRs #9–#11.
- **Actualización automática** (27/09): la app se recarga sola cuando se publica una versión nueva (`version.json`, cada 5 min) + botón ↻. Desde esta versión no hace falta tocar la tablet para ver cambios.
- **Modelo v3** (28/09): período medio del mar (calidad y tamaño), ráfagas, reparo que se pierde con viento fuerte. Corrige el 2.5★ que dio con mar de temporal el 28/09. Test de regresión incluido. PR `modelo-v3-periodo`.
- **Publicada** en `https://ponkus.github.io/surfing/parte/` (PR #4). Probada en la tablet: fluida, pero se pisaba dentro de Chrome → arreglado (encaje 1280×800 escalado + pantalla completa + app instalable), en PR #5.

## En curso
- **Tablet TJD MT-1025** (en realidad MT-1025QU): Android 11, chip **Allwinner** (`sun50iw10p1`, probablemente A133), 4 GB RAM. Es **Android Go**, parche de seguridad 2022-03, sin más actualizaciones de sistema (ni fabricante ni Google). Chrome y **WebView 153** al día, Play Store 53. Anda fluida en la versión completa (no hace falta `?lite` por ahora).
- PR #5 publicado: en la tablet se ve bien, sin bloques pisados.
- **ADB por USB es inestable** en esta tablet (se desconecta / queda `offline` con 2 cables y 2 puertos). Se usó **depuración inalámbrica** (Android 11: `adb pair` + `adb connect`), anda perfecto. Ver `docs/TABLET.md`.
- Batería baja rápido: probablemente degradada por la descarga profunda (hardware). La limpieza no lo arregla; va a vivir enchufada.

## Siguiente (en orden)
1. Ratings a **Google Sheet** (Apps Script Web App → `CFG.SHEETS_URL`), para no depender de la tablet.
2. **Marea oficial del SHN** (Mar del Plata): reemplazar/corregir `TIDE_OFFSET_MIN`.
3. **Cámaras** (28/09): mis cámaras = estadodelmar `video2` en vivo; lineup = su página completa en Fully (botón "Abrir en lineup", se vuelve con atrás). **Falta en la tablet**: iniciar sesión en lineup una vez dentro de Fully y confirmar que "atrás" vuelve al parte. Pendiente: `video4 …/P.Grande` rota (526, certificado SSL) — volver a sumarla cuando ande.
4. Calibración: script que lea los ratings exportados y ajuste `SIZE_CAL`, `D_BAR`, bombeo (después de ~20 ratings).
5. Protección de batería: ESP32 + relé + MacroDroid.
6. Fase 2: portar a ESP32-S3 (JC3248W535).

## Abierto / dudas
- Push/merge: desde el 27/09 **Claude hace el merge a `main`** (pedido de Maiky), con tests en OK. Claude Code en la Mac puede (usa `gh`). La app de Claude puede tener bloqueado mergear sin revisión humana: en ese caso, dejar el PR listo y avisar para que lo mergee Claude Code.
- Netlify (`UNMDP/surfcam`) está conectado al repo y falla en cada PR porque busca la carpeta `surf2`, que no existe. No afecta a GitHub Pages. Arreglo: vaciar "Base directory" en Netlify o desconectarlo.
- Sobreestimación con mar corto (5–6 s): corregida en v3 con coeficientes provisorios (`sizeT`, `periodQ`). Validar con ratings, sobre todo días de 6–7 s (el límite dudoso).
- ¿Tamaño real de los bancos (`D_BAR`)? Se calibra con ratings.
- ¿El bombeo es real o memoria selectiva? Se mide con ratings.
