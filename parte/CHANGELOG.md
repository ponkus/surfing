# Changelog — parte/

Formato: `## fecha · quién` + qué cambió y por qué. Lo más nuevo arriba.

## 2026-09-27 · Claude app — cámaras por pico
- Pedido de Maiky: al tocar un pico, ver sus dos cámaras, en pantalla dividida o una sola en grande.
- **Tocar la tarjeta de Biología o Yacht abre sus 2 cámaras** (pantalla dividida). Tocar una → grande; tocar de nuevo → las dos. Pestañas Biología / Yacht, botones "Dividida" / "Una", "‹ Parte" para volver. Botón de cámara arriba (al lado del reloj) abre las del pico recomendado.
- "Calificar" desde las cámaras abre el formulario con el pico y "Por cámara" ya marcados.
- La brújula del pico pasa al botón "brújula ›" de la tarjeta.
- Fuentes (`CFG.CAMS`): streams de **lineup.surf** (los favoritos de Maiky) y de respaldo los de **estadodelmar** (los de `surf.html`). Reproductor nativo (Android reproduce HLS solo, igual que `surf.html`); si una fuente no conecta en 12 s pasa a la siguiente; si ninguna, "Sin señal · tocá para reintentar". En navegadores sin HLS nativo (compu) carga hls.js de jsdelivr.
- Los videos solo se cargan con la vista abierta; al cerrar se cortan. Se cierra sola a los 10 min sin tocar. El mar animado de fondo se pausa mientras tanto.
- **Sin probar en la tablet todavía**: en la compu (Chrome) lineup rechazó el video pedido desde otra web (503) y hls.js no pudo por CORS; el reproductor nativo de Android pide distinto y puede andar. Validar en la tablet.
- Tests: recorrido de cámaras (abrir, una/dividida, cambiar de pico, calificar, cerrar) con los videos bloqueados.

## 2026-09-27 · Claude Code — leyenda de la brújula visible en la tablet
- Las muestras de la leyenda (spans con fondo) no se veían en el WebView de la tablet; ahora son pequeños SVG. Probado en la tablet.

## 2026-09-27 · Claude Code — "Le entra X %" en vez de la brújula (y la brújula corregida)
- La brújula de cada pico no se leía a 2 m y era lo más técnico de la pantalla. La tarjeta del pico ahora muestra: altura, estrellas, **"Le entra ▓▓▓ 86 %"** (cuánto del swell principal entra al pico) y una flecha con la dirección y el período. Tocando el pico se abre la brújula grande con una leyenda (se cierra sola al minuto).
- Corrección: la mancha de la brújula se dibujaba siempre para 8 s; ahora usa el período real del swell principal (el mismo que el %). Modelo sin cambios.

## 2026-09-27 · Claude Code — "Hoy no" legible
- Maiky: "Hoy no" se veía parcialmente (el degradé se calculaba sobre todo el ancho del cuadro y en la tablet "no" quedaba apagado). Ahora "Hoy no"/motivo va en blanco sólido y el degradé de los nombres de pico se ajusta al ancho de la palabra.

## 2026-09-27 · Claude Code — corrección: "soplado" ≠ "movido"
- Maiky corrigió la definición: soplado es el VIENTO (fuerte, ola bien formada pero "tocada"); movido es el MAR (desordenado). Son independientes. Corregido en DECISIONES.md y en el comentario del código.

## 2026-09-27 · Claude Code — definición de "soplado"
- Definido con Maiky y anotado en DECISIONES.md: viento fuerte que pega en el mar y lo desarma; además cuesta agarrar la ola. Solo documentación + comentario en el código.

## 2026-09-27 · Claude Code — calificar v2 + "por qué no" en vez de "Sin ola"
- Maiky: hoy "Sin ola" no era cierto (había ola, mar movido); no podía calificar 0; el tamaño en un día así es relativo.
- Formulario: botón rápido **"Hoy no se puede · guardar 0 ★"**; calidad **0–5** (0 = no se puede); **"Cómo estaba el mar"**: Glass · Prolijo · Soplado · Algo movido · Movido (vocabulario de Maiky); tamaño **opcional**; pico opcional solo con 0 ★ (se guarda `"ambos"`).
- Rating: campos NUEVOS `mar`, `pred_all` (predicción para los dos picos); `stars` admite 0; `size`/`size_m` pueden ser null; `spot` puede ser `"ambos"`. No cambió ningún campo existente (ver DECISIONES.md). Modelo sin cambios (`pred.model` v2).
- Donde decía "Sin ola", ahora dice el factor que más limita según el modelo: Plano · Muy chico · Movido · Sin agua · Mucha agua.

## 2026-09-27 · Claude Code — horario personal por URL (`?horario=0630-1200`)
- Maiky casi siempre puede ir de 6:30 a 12, pero la app la pueden ver otros: el horario NO es fijo en la app, va en la URL. Sin parámetro, todo igual que antes (todo el día).
- Con horario: "En tu horario" (en vez de "Próxima buena"), las tarjetas de los días, "Franja buena" y la mejor hora de mañana (de noche / día elegido) buscan solo dentro del horario, recortando la franja (06:00–08:00 → 06:30–08:00). Aparte, en chiquito, "Fuera de tu horario: …" si afuera hay algo ≥ 2,5 ★ y ≥ 0,5 ★ mejor (en "Próxima", solo si llega antes). El horario se ve sombreado en el gráfico de marea. Si el horario de hoy ya pasó, la tarjeta de Hoy lo dice y muestra lo que queda del día.
- Las estrellas de cada hora no cambian con el horario: solo cambia qué hora se elige.
- El cuadro central se compacta solo (`.hero.tight`) si el contenido no entra, en vez de cortarse; sin ola no se muestra la etiqueta de bombeo.
- Tests OK con y sin `?horario`.

## 2026-09-27 · Claude Code — "Próxima buena" y la tarjeta del día dicen lo mismo
- Maiky vio "Próxima buena: martes 07:00 · 2.5 ★" y en la tarjeta del martes 4 ★. No era un dato inventado: eran dos cuentas distintas del modelo ("próxima buena" = la PRIMERA hora que llega a 2,5 ★; la tarjeta = la MEJOR hora del día).
- Ahora hay una sola cuenta, `bestWindow()`: mejor hora del día con luz + franja continua alrededor (≤ 0,5 ★ de la mejor). La usan "Próxima buena" (primer día con alguna hora ≥ 2,5 ★), la tarjeta del día y "Franja buena". Con los datos del 27/09: las dos dicen martes 11:00–13:00 · Yacht · 4 ★.

## 2026-09-27 · Claude Code — diseño legible a 2 m + días interactivos
- Pedido de Maiky: mal contraste ("todo muy azul"), datos importantes que hay que acercarse para ver; la tablet va como portarretratos y se tiene que leer a 2 m.
  - Tarjetas oscuras y neutras (casi opacas) en vez de vidrio azul; textos claros (muted .86, dim .64); cielo de día menos azul.
  - Todo más grande: pico 84 px, altura 50, chips 18, marea 30, clima 36, días 25; textos secundarios 15–18.
  - La columna derecha ya no deja franja vacía (la marea crece y el gráfico es más alto, con horas más grandes). Sin anillo "0 de 5" cuando no hay ola. En cada pico, una sola línea técnica.
- **Días interactivos**: tocar Mañana / otro día muestra ese día en el cuadro central (mejor hora), la marea y el clima de esa hora, y "Franja buena" de ese día. "✕ Ahora" o tocar Hoy vuelve; vuelve solo a los 90 s (es una pantalla fija).
- **Clima real del momento**: la tarjeta de Hoy muestra el clima de ahora y avisa "lluvia desde las HH:MM"; los otros días muestran el clima que predomina con luz (Open-Meteo daily da el peor momento del día: una hora de llovizna pintaba todo el día de lluvia).
- Probado en la tablet con datos en vivo y tocando la pantalla. Tests OK. Modelo sin cambios (`pred.model` sigue v2).

## 2026-09-27 · Claude Code — botón de pantalla completa inteligente + carga a prueba de cortes
- El botón de pantalla completa se esconde solo cuando la página ya ocupa toda la pantalla (Fully Kiosk, F11) y en equipos sin esa función (iPhone). Sigue apareciendo en celulares Android, iPad y compus.
- Carga de datos: corte a los 20 s si Open-Meteo no responde (el 27/09 la API de pronóstico se colgó y la pantalla quedaba vacía hasta el próximo ciclo de 30 min); reintento cada 1 min si falla; al arrancar se muestran enseguida los últimos datos guardados (`pg_cache`) mientras llegan los nuevos. Probado simulando la API colgada.

## 2026-09-27 · Claude Code — arreglo: la web arrancaba agrandada en Fully Kiosk
- Problema (Maiky): en la tablet, al abrir Fully la web aparecía ~16 % más grande y cortada; había que achicarla con los dedos. Reproducido con captura por ADB: Fully arranca con zoom = densidad de pantalla (186/160 = 1,16) e `innerWidth/innerHeight` dan un área mayor que la visible.
- `fit()` ahora usa el área realmente visible (`visualViewport`), se recalcula al cargar y cuando cambia el zoom. Viewport con `maximum-scale=1, user-scalable=no` (no se agranda con los dedos por accidente).
- Probado en la tablet (servida desde la Mac) antes de publicar: entra justa. Tests OK.
- Fully Kiosk instalado y configurado: pantalla completa sin barras, Launch on Boot, Keep Screen On desactivado (manda Android: siempre prendida enchufada, 30 min a batería), exento de ahorro de batería. El PIN de bloqueo se queda (decisión de Maiky).

## 2026-09-27 · Claude Code — tablet: actualizaciones y optimización
- ¿Subir de Android 11? Oficial: no hay (fabricante y Google Play dicen "actualizado"; parche de seguridad 2022-03). No oficial (GSI): posible en teoría (Treble, bootloader desbloqueable) pero borra todo, drivers de Allwinner suelen fallar y no hay firmware de fábrica para recuperar → descartado (`DECISIONES.md`).
- La tablet es **Android Go**. El módulo de sistema de Google Play queda en 2021-10 (Google no le manda más).
- Actualizado lo que importa para la web: **WebView 124 → 153** (el que usará Fully Kiosk), **Play Store 43 → 53**. Chrome ya estaba en 153.
- Registro de fallos: sin crashes ni reinicios; solo avisos internos (Chrome, `com.yhk.qeota`) y 3 demoras de Play Services.
- Chrome exento de la optimización de batería (`deviceidle whitelist`); desactivadas voz de Google (`tts`) y Files de Google (`nbu.files`).
- Después de reiniciar: memoria libre 2,8 → 3,1 GB; CPU en reposo ~94 % libre. Ajustes anteriores persisten.

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
