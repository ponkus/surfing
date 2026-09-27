# Changelog — parte/

Formato: `## fecha · quién` + qué cambió y por qué. Lo más nuevo arriba.

## 2026-09-27 · Claude Code — tablet preparada por ADB
- Diagnóstico: MT-1025QU, Android 11, chip Allwinner (`sun50iw10p1`), 4 GB RAM, batería "buena" según Android. Lo que más consume: pantalla y Chrome. Archivos en `docs/tablet/`.
- ADB por USB inestable (desconexiones y `offline` con 2 cables/puertos) → se usó depuración inalámbrica. Documentado en `TABLET.md`.
- Con OK de Maiky: desactivadas 14 apps de Google (YouTube, YT Music, Google TV, Gmail, Calendar, Contactos, Meet, Maps, Drive, Fotos Go, Google Go, Asistente Go, Bienestar digital, Feedback); Opera Mini desinstalada para el usuario 0. No se tocaron apps de Allwinner/Softwinner ni del fabricante (`com.yhk.*`, `com.DeviceTest`).
- Ajustes: animaciones 0,5×, pantalla siempre prendida enchufada (ya estaba), apagado a batería 1 min → 30 min, brillo 100 % → 50 % (no tiene sensor de luz). Play Store: actualizar solo por Wi-Fi (Maiky).
- `docs/tablet/revertir.sh` deshace todo.
- Regla nueva (pedido de Maiky): el merge a `main` lo hace Claude, con tests en OK (`CLAUDE.md`, `DECISIONES.md`).

## 2026-09-27 · Claude app — plan de preparación de la tablet
- `docs/TABLET.md`: instrucciones para que Claude Code prepare la tablet por ADB desde la Mac (diagnóstico, limpieza reversible, ajustes), con lista de paquetes que no se tocan.
- Chrome en la tablet no ofrece "Agregar a pantalla principal" (ni en ⋮ ni en Compartir): se usará Fully Kiosk Browser.
- PR #5 publicado (encaje en pantalla + pantalla completa + PWA). Maiky confirmó que en la tablet se ve bien.

## 2026-09-27 · Claude app — encaje en pantalla + pantalla completa
- Problema (foto de Maiky en la tablet): dentro de Chrome las barras le sacan ~200 px de alto y los bloques se pisaban.
- La app ahora se diseña a 1280×800 y `fit()` la escala para que entre justa en cualquier pantalla. En celular vertical (`body.mobile`) se apila y scrollea.
- Botón de pantalla completa (arriba a la derecha) y en pantallas táctiles el primer toque pasa a pantalla completa.
- App instalable: `manifest.webmanifest` (display fullscreen, apaisada), `sw.js` (red primero, copia offline), íconos `icon-192/512.png`. "Agregar a pantalla principal" la abre sin barras de Chrome ni de Android.
- Tests: ahora prueban 5 tamaños de pantalla y fallan si un bloque pisa a otro o el contenido queda cortado (verificado: la versión anterior falla en 1280×590).

## 2026-09-27 · Claude app
- Publicada en `https://ponkus.github.io/surfing/parte/` (PR #4 mergeado por Maiky).
- El proyecto pasa al repo `ponkus/surfing` en `parte/` (antes vivía en archivos sueltos).
- `build.py` (arma `index.html`), `model/export_tables.py`, `tests/run.py` con fixtures reales.
- Documentación: `CLAUDE.md` (raíz), `docs/PROYECTO.md`, `docs/MODELO.md`, `docs/DECISIONES.md`, `docs/ESTADO.md`.

## 2026-09-26 · Claude app — v2 (diseño)
- Rediseño completo: cielo que cambia con la hora (noche/amanecer/día/atardecer), mar animado en canvas con altura, período y marea reales, rayas de viento.
- Anillo de puntaje 0–5, chips de color (swell/viento/marea/bombeo), "Próxima buena", dial por pico con abanico de exposición y flechas de swell/viento.
- Curva de marea con degradé, punto "ahora" animado y ventanas de bombeo. Íconos SVG propios, tipografía Outfit, reloj grande.
- De noche la tarjeta principal muestra la mejor hora de mañana. Amanecer en grande (pedido de Maiky).
- Modo `?lite` para tablets lentas.

## 2026-09-26 · Claude app — v1
- Primera app: datos de Open-Meteo, modelo por pico, marea con desfase +45 min, bombeo, clima, próximos días, ratings en localStorage con exportación.
