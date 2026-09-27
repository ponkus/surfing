# Changelog — parte/

Formato: `## fecha · quién` + qué cambió y por qué. Lo más nuevo arriba.

## 2026-09-27 · Claude app
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
