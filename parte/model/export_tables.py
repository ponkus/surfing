"""Precalcula las tablas de geometría que usa la app (parte/model/tables.json).

Correr cuando cambie geo.py o las funciones exposure / local_wind_factor de model.py:
    cd parte/model && python3 export_tables.py
Después reconstruir la app:  python3 parte/build.py
Requiere: pip install shapely numpy
"""
import json
import os
from model import exposure, local_wind_factor
from geo import NORMAL

HERE = os.path.dirname(os.path.abspath(__file__))
out = {"normal": round(NORMAL, 1), "exp": {}, "wind": {}}
for spot in ["Biologia", "Yacht"]:
    # exposición al swell por dirección (0-359°) para 3 dispersiones direccionales (20/30/45°)
    out["exp"][spot] = {str(sp): [round(exposure(spot, d, sp), 3) for d in range(360)] for sp in (20, 30, 45)}
    # fracción del viento que ensucia el pico por dirección (0 = reparado/offshore, 1 = expuesto)
    out["wind"][spot] = [round(local_wind_factor(spot, d), 3) for d in range(360)]

with open(os.path.join(HERE, "tables.json"), "w") as f:
    json.dump(out, f, separators=(",", ":"))
print("tables.json actualizado · normal de la playa:", out["normal"])
