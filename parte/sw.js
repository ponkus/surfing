// Service worker de la app (necesario para "Agregar a pantalla principal" y para abrir sin conexión).
// Estrategia: primero la red (así las actualizaciones llegan siempre), si no hay red, la última copia guardada.
// Solo cachea archivos de esta carpeta; los datos de Open-Meteo los maneja la app (localStorage "pg_cache").
const CACHE = "pg-v1";
const SHELL = ["./", "./index.html", "./manifest.webmanifest", "./icon-192.png", "./icon-512.png"];
self.addEventListener("install", e => { self.skipWaiting(); e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL))); });
self.addEventListener("activate", e => e.waitUntil(self.clients.claim()));
self.addEventListener("fetch", e => {
  const u = new URL(e.request.url);
  if (e.request.method !== "GET" || u.origin !== location.origin) return;
  e.respondWith(
    fetch(e.request)
      .then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return r; })
      .catch(() => caches.match(e.request).then(m => m || caches.match("./index.html")))
  );
});
