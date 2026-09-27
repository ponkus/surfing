"""Prueba la app en un Chromium headless con datos reales guardados (tests/fixtures).

Uso (desde la raíz del repo):
    python3 parte/tests/run.py                          # 4 horarios típicos
    python3 parte/tests/run.py 2026-09-27T06:45:00-03:00  # un horario puntual

- Intercepta Open-Meteo y responde con fixtures/marine.json y fixtures/weather.json
  (capturados el 26/09/2026, cubren 25→29/09/2026: los horarios de prueba tienen que caer ahí).
- Congela el reloj en el horario pedido y la zona horaria en Buenos Aires.
- Guarda capturas en parte/tests/out/ y prueba el flujo de calificar.
- Falla (exit 1) si hay errores de JavaScript. Los "Failed to load resource" (Google Fonts bloqueado en el test) se ignoran.
Requiere: pip install playwright && playwright install chromium
"""
import asyncio, datetime, os, sys
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, "..", "index.html")
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
TIMES = sys.argv[1:] or ["2026-09-26T23:30:00-03:00", "2026-09-27T06:45:00-03:00",
                          "2026-09-27T10:30:00-03:00", "2026-09-28T09:00:00-03:00"]

async def one(p, T):
    b = await p.chromium.launch()
    ctx = await b.new_context(viewport={"width": 1280, "height": 800},
                              timezone_id="America/Argentina/Buenos_Aires", locale="es-AR")
    await ctx.clock.install(time=datetime.datetime.fromisoformat(T))
    page = await ctx.new_page()
    errs = []
    page.on("pageerror", lambda e: errs.append(f"PAGEERROR: {e}"))
    page.on("console", lambda m: errs.append(m.text) if m.type == "error" and "Failed to load resource" not in m.text else None)
    async def route(r):
        f = "marine.json" if "marine-api" in r.request.url else "weather.json"
        await r.fulfill(path=os.path.join(HERE, "fixtures", f), content_type="application/json",
                        headers={"access-control-allow-origin": "*"})
    await ctx.route("**/*open-meteo.com/**", route)
    await ctx.route("**/fonts.googleapis.com/**", lambda r: r.abort())
    await page.goto("file://" + os.path.abspath(APP))
    await page.wait_for_timeout(2500)
    tag = T[5:16].replace(":", "")
    await page.screenshot(path=os.path.join(OUT, f"{tag}.png"))
    hero = await page.inner_text("#spotname"); h = await page.inner_text("#height")
    # flujo de rating
    await page.click("#rateBtn"); await page.click('[data-k="spot"] [data-v="Yacht"]')
    await page.click('[data-k="size"] [data-v="cintura"]'); await page.click('[data-k="stars"] [data-v="3"]')
    await page.click("#save"); await page.wait_for_timeout(300)
    n = await page.evaluate("JSON.parse(localStorage.getItem('pg_ratings')||'[]').length")
    await b.close()
    print(f"{T}  →  {hero} {h.strip()}  · rating guardado: {n==1}  · errores: {errs or 'ninguno'}")
    return not errs and n == 1

async def main():
    async with async_playwright() as p:
        ok = [await one(p, T) for T in TIMES]
    print("OK" if all(ok) else "FALLÓ")
    sys.exit(0 if all(ok) else 1)

asyncio.run(main())
