"""Arma parte/index.html (lo que publica GitHub Pages) a partir de:
    parte/src/app.template.html  +  parte/model/tables.json

Uso (desde la raíz del repo):  python3 parte/build.py
NUNCA editar parte/index.html a mano: se pisa en cada build. Editar src/app.template.html.
También escribe parte/version.json (la app lo consulta para recargarse sola cuando hay versión nueva).
"""
import hashlib, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(HERE, "src", "app.template.html"), encoding="utf-8").read()
tables = open(os.path.join(HERE, "model", "tables.json"), encoding="utf-8").read()
assert "__TABLES__" in tpl, "Falta el marcador __TABLES__ en el template"
html = tpl.replace("__TABLES__", tables)
# Versión de la app = hash del contenido. La app compara la suya con version.json y se recarga sola si cambió.
assert "__BUILD__" in html, "Falta el marcador __BUILD__ en el template"
build = hashlib.sha1(html.encode("utf-8")).hexdigest()[:10]
html = html.replace("__BUILD__", build)
with open(os.path.join(HERE, "version.json"), "w", encoding="utf-8") as f:
    json.dump({"build": build}, f)
banner = "<!-- ARCHIVO GENERADO por parte/build.py — no editar a mano. Fuente: parte/src/app.template.html -->\n"
with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
    f.write(banner + html)
print(f"parte/index.html generado ({len(html)//1024} KB) · versión {build}")
