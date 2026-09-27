"""Arma parte/index.html (lo que publica GitHub Pages) a partir de:
    parte/src/app.template.html  +  parte/model/tables.json

Uso (desde la raíz del repo):  python3 parte/build.py
NUNCA editar parte/index.html a mano: se pisa en cada build. Editar src/app.template.html.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(HERE, "src", "app.template.html"), encoding="utf-8").read()
tables = open(os.path.join(HERE, "model", "tables.json"), encoding="utf-8").read()
assert "__TABLES__" in tpl, "Falta el marcador __TABLES__ en el template"
html = tpl.replace("__TABLES__", tables)
banner = "<!-- ARCHIVO GENERADO por parte/build.py — no editar a mano. Fuente: parte/src/app.template.html -->\n"
with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
    f.write(banner + html)
print(f"parte/index.html generado ({len(html)//1024} KB)")
