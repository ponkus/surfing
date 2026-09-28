# Proxy de lineup (Cloudflare Worker `olas-cams`)

**Qué es:** el CloudFront de lineup solo entrega el video a lineup.surf (403 a cualquier otra web). Maiky tiene permiso de lineup
para usar sus cámaras en su app. El Worker pide el video como si fuera lineup.surf y se lo devuelve a la app.

- URL: `https://olas-cams.jlgrassi.workers.dev/<CLAVE>/<camara>.stream/playlist.m3u8` (cuenta Cloudflare de Maiky, plan gratis).
- Solo deja pasar las 4 cámaras de Playa Grande y solo con la clave. Sin clave: 403. Otra cámara: 404.
- La **clave no va en el repo** (Pages es público). Vive solo en la URL de inicio de Fully en la tablet: `...&lu=<CLAVE>`.
  Si se pierde: está en el código del Worker, en el panel de Cloudflare (constante `KEY`). Para cambiarla: editar `KEY` en el Worker y la URL de Fully.
- Sin `?lu=` la app muestra en "Lineup" un aviso y las cámaras abren en "Mis cámaras".
- Probado 28/09 desde Chrome: las 4 cámaras dan 200 en playlist, chunklist y segmentos.
- Límite plan gratis: 100.000 pedidos/día. Cada cámara abierta ≈ 1 pedido/s → 2 cámaras ≈ 7.200/h. Sobra (las cámaras se cierran solas a los 10 min sin tocar).

Código del Worker (sin la clave):

```js
const KEY = "<CLAVE>";
const ORIGEN = "https://d1pn38aa7xeaye.cloudfront.net/ArgentinaCameras/";
const CAMS = ["ar-bue-mardelplata-pg1-overwiew.stream/", "ar-bue-mardelplataplayagrandebiologia.stream/",
              "ar-bue-mardelplata-pg2-overwiew.stream/", "ar-bue-mardelplataplayagrandeelyacht.stream/"];
const CORS = { "Access-Control-Allow-Origin": "*" };
export default {
  async fetch(req) {
    if (req.method === "OPTIONS") return new Response(null, { headers: { ...CORS, "Access-Control-Allow-Headers": "*" } });
    const partes = new URL(req.url).pathname.split("/");
    if (partes[1] !== KEY) return new Response("no", { status: 403 });
    const resto = partes.slice(2).join("/");
    if (!CAMS.some(c => resto.startsWith(c))) return new Response("no", { status: 404 });
    const r = await fetch(ORIGEN + resto, { headers: { "Referer": "https://lineup.surf/", "Origin": "https://lineup.surf",
                                                      "User-Agent": req.headers.get("User-Agent") || "" } });
    const h = new Headers(r.headers); h.set("Access-Control-Allow-Origin", "*"); h.delete("set-cookie");
    return new Response(r.body, { status: r.status, headers: h });
  },
};
```
