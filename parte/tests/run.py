"""Prueba la app en un Chromium headless con datos reales guardados (tests/fixtures).

Uso (desde la raíz del repo):
    python3 parte/tests/run.py                          # 4 horarios típicos
    python3 parte/tests/run.py 2026-09-27T06:45:00-03:00  # un horario puntual

- Intercepta Open-Meteo y responde con fixtures/marine.json y fixtures/weather.json
  (capturados el 26/09/2026, cubren 25→29/09/2026: los horarios de prueba tienen que caer ahí).
- Congela el reloj en el horario pedido y la zona horaria en Buenos Aires.
- Guarda capturas en parte/tests/out/, prueba el flujo de calificar, la vista de cámaras y que los bloques no se pisen en varios tamaños de pantalla.
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
    page.on("console", lambda m: errs.append(m.text) if m.type == "error" and "Failed to load resource" not in m.text
            and "permissions policy violation" not in m.text else None)  # aviso de Chrome por los marcos de lineup bloqueados en el test
    async def route(r):
        f = "marine.json" if "marine-api" in r.request.url else "weather.json"
        await r.fulfill(path=os.path.join(HERE, "fixtures", f), content_type="application/json",
                        headers={"access-control-allow-origin": "*"})
    await ctx.route("**/*open-meteo.com/**", route)
    await ctx.route("**/fonts.googleapis.com/**", lambda r: r.abort())
    for pat in ("**/*cloudfront.net/**", "**/*estadodelmar.com.ar/**", "**/cdn.jsdelivr.net/**", "**/*lineup.surf/**"):
        await ctx.route(pat, lambda r: r.abort())                        # cámaras: sin red en el test
    await page.goto("file://" + os.path.abspath(APP))
    await page.wait_for_timeout(2500)
    tag = T[5:16].replace(":", "") + f"_{W}x{H}"
    errs += await page.evaluate(OVERLAP_JS)
    await page.screenshot(path=os.path.join(OUT, f"{tag}.png"))
    hero = await page.inner_text("#spotname"); h = await page.inner_text("#height")
    # regresión modelo v3: 28/09 09:00 fue mar de temporal (período 5–6 s, NE con ráfagas 44), no apto → ≤1★ en los dos picos
    if W == 1280 and H == 800 and T.startswith("2026-09-28T09:00"):
        st = await page.evaluate("""() => { const h=D.H.find(x=>x.t.startsWith('2026-09-28T09:00'));
          return ['Biologia','Yacht'].map(s=>evalHour(h,s).stars); }""")
        if max(st) > 1: errs.append(f"modelo: 28/09 09:00 da {st}★ y ese día no era apto (máx 1★)")
    # vista de cámaras (los videos se bloquean en el test: se verifica la interfaz, no la señal)
    if W == 1280 and H == 800 and T == TIMES[-1]:
        await page.click("#spots .sp[data-spot='Biologia']")
        await page.wait_for_timeout(600)
        cam_ok = await page.evaluate("""() => { const c=document.querySelector('#cams');
          const t=[...c.querySelectorAll('.tile .lbl')].map(x=>x.textContent);
          return c.classList.contains('open') && t.join('|')==='Biología|La Normandina'
            && document.querySelectorAll('#camsGrid video').length===2; }""")
        await page.wait_for_timeout(1500)
        await page.screenshot(path=os.path.join(OUT, f"{tag}_camaras.png"))
        await page.click("#camsOne"); single = await page.evaluate("document.querySelector('#camsGrid').classList.contains('single')")
        await page.click("#cams .tabs [data-cs='Yacht']"); await page.wait_for_timeout(300)
        yacht = await page.evaluate("""() => [...document.querySelectorAll('#cams .tile .lbl')].map(x=>x.textContent).join('|')==='Yacht'
          && document.querySelectorAll('#camsGrid video').length===1""")
        await page.click("#grpLU"); await page.wait_for_timeout(300)
        await page.screenshot(path=os.path.join(OUT, f"{tag}_camaras_lineup.png"))
        lineup = await page.evaluate("""() => [...document.querySelectorAll('#cams .tile.lu .big')].map(x=>x.textContent).join('|')==='Yacht 1|Yacht 2'
          && !document.querySelector('#camsGrid video')""")
        async with page.expect_request(lambda r: r.url.startswith("https://lineup.surf/spots/") and r.url.endswith("el-yacht/camera1")) as req:
            await page.click("#camsGrid .tile.lu[data-i='0']")
        lineup = lineup and bool(await req.value)
        await page.goto("file://" + os.path.abspath(APP)); await page.wait_for_timeout(1200)
        await page.click("#spots .sp[data-spot='Yacht']"); await page.wait_for_timeout(300)
        propias = True
        await page.click("#camsRate"); pre = await page.evaluate("document.querySelector('#modal').classList.contains('open') && document.querySelector('[data-k=spot] .sel')?.dataset.v==='Yacht' && document.querySelector('[data-k=src] .sel')?.dataset.v==='camara'")
        await page.click("#cancel"); await page.click("#camsBack")
        closed = await page.evaluate("!document.querySelector('#cams').classList.contains('open') && !document.querySelector('#camsGrid video')")
        for name, okk in [("abre las 2 cámaras de Biología", cam_ok), ("modo una sola", single), ("cambia a Yacht", yacht), ("lineup abre su página", lineup), ("calificar desde cámaras", pre), ("cierra y corta los videos", closed)]:
            if not okk: errs.append("cámaras: falla " + name)
        # volver a dejar el formulario de rating como al principio
        await page.evaluate("document.querySelectorAll('.opts:not([data-k=src]) .opt').forEach(x=>x.classList.remove('sel'))")
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
