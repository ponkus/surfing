"""Prueba la app en un Chromium headless con datos reales guardados (tests/fixtures).

Uso (desde la raíz del repo):
    python3 parte/tests/run.py                          # 4 horarios típicos
    python3 parte/tests/run.py 2026-09-27T06:45:00-03:00  # un horario puntual

- Intercepta Open-Meteo y responde con fixtures/marine.json y fixtures/weather.json
  (capturados el 26/09/2026, cubren 25→29/09/2026: los horarios de prueba tienen que caer ahí).
- Congela el reloj en el horario pedido y la zona horaria en Buenos Aires.
- Guarda capturas en parte/tests/out/, prueba el flujo de calificar y que los bloques no se pisen en varios tamaños de pantalla.
- Falla (exit 1) si hay errores de JavaScript. Los "Failed to load resource" (Google Fonts bloqueado en el test) se ignoran.
Requiere: pip install playwright && playwright install chromium
"""
import asyncio, datetime, os, sys
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.environ.get("APP") or os.path.join(HERE, "..", "index.html")
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
TIMES = sys.argv[1:] or ["2026-09-26T23:30:00-03:00", "2026-09-27T06:45:00-03:00",
                          "2026-09-27T10:30:00-03:00", "2026-09-28T09:00:00-03:00"]
# Pantallas: pantalla completa de la tablet, tablet dentro de Chrome (con barras), tablet chica, compu, celular vertical
SIZES = [(1280, 800), (1280, 590), (1024, 600), (1508, 812), (390, 844)]

# Verifica que ningún bloque se pise con otro ni se salga de la pantalla
OVERLAP_JS = """() => {
  const r = s => document.querySelector(s).getBoundingClientRect();
  const hero = r('#hero'), side = r('.side'), d0 = r('#d0'), rate = r('#rateBtn');
  const mobile = document.body.classList.contains('mobile');
  const errs = [];
  if (hero.bottom > d0.top + 1) errs.push('hero pisa los días');
  if (side.bottom > d0.top + 1) errs.push('marea/clima pisa los días');
  if (!mobile) {
    if (hero.right > side.left + 1) errs.push('hero pisa la marea');
    if (d0.bottom > innerHeight + 1 || rate.right > innerWidth + 1) errs.push('se sale de la pantalla');
    const h = document.querySelector('#hero'); if (h.scrollHeight > h.clientHeight + 2) errs.push('contenido del hero cortado');
  }
  return errs;
}"""

async def one(p, T, W=1280, H=800):
    b = await p.chromium.launch()
    ctx = await b.new_context(viewport={"width": W, "height": H},
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
    tag = T[5:16].replace(":", "") + f"_{W}x{H}"
    errs += await page.evaluate(OVERLAP_JS)
    await page.screenshot(path=os.path.join(OUT, f"{tag}.png"))
    hero = await page.inner_text("#spotname"); h = await page.inner_text("#height")
    # flujo de rating
    await page.click("#rateBtn"); await page.click('[data-k="spot"] [data-v="Yacht"]')
    await page.click('[data-k="size"] [data-v="cintura"]'); await page.click('[data-k="stars"] [data-v="3"]')
    await page.click("#save"); await page.wait_for_timeout(300)
    n = await page.evaluate("JSON.parse(localStorage.getItem('pg_ratings')||'[]').length")
    await b.close()
    print(f"{T} {W}x{H}  →  {hero} {h.strip()}  · rating guardado: {n==1}  · errores: {errs or 'ninguno'}")
    return not errs and n == 1

async def main():
    async with async_playwright() as p:
        ok = [await one(p, T) for T in TIMES]                                   # horarios a 1280×800
        ok += [await one(p, TIMES[-1], W, H) for (W, H) in SIZES[1:]]          # tamaños de pantalla
    print("OK" if all(ok) else "FALLÓ")
    sys.exit(0 if all(ok) else 1)

asyncio.run(main())
