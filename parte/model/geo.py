"""Geometría real de Playa Grande (OSM) y cálculo de exposición por pico."""
import math
from shapely.geometry import LineString, Point, Polygon

LAT0, LON0 = -38.0300, -57.5300
KX = 111320 * math.cos(math.radians(LAT0))
KY = 110540

def xy(lat, lon):
    return ((lon - LON0) * KX, (lat - LAT0) * KY)

def parse(s):
    return [xy(*map(float, p.split(','))) for p in s.split(';')]

EN = parse("-38.03710,-57.52263;-38.03700,-57.52278;-38.03542,-57.52524;-38.03510,-57.52574;-38.03467,-57.52640;-38.03416,-57.52721;-38.03352,-57.52821;-38.03326,-57.52860;-38.03291,-57.52919;-38.03270,-57.52954;-38.03242,-57.53003;-38.03228,-57.53030;-38.03214,-57.53058;-38.03212,-57.53062")
BIO = parse("-38.02634,-57.52981;-38.02649,-57.52962;-38.02678,-57.52861;-38.02706,-57.52776;-38.02721,-57.52769;-38.02728,-57.52784;-38.02703,-57.52873;-38.02683,-57.52927;-38.02674,-57.52949;-38.02668,-57.52965;-38.02668,-57.52972;-38.02657,-57.53000;-38.02654,-57.52995;-38.02654,-57.52991;-38.02644,-57.52986;-38.02634,-57.52981")
ES = parse("-38.0504,-57.5344;-38.0500,-57.5336;-38.0497,-57.5330;-38.0492,-57.5322;-38.0488,-57.5317;-38.0480,-57.5309;-38.0443,-57.5276;-38.0437,-57.5270;-38.0431,-57.5264;-38.0423,-57.5253;-38.0417,-57.5245;-38.0411,-57.5235;-38.0405,-57.5223;-38.0400,-57.5213;-38.0396,-57.5203;-38.0391,-57.5186;-38.0388,-57.5178")
# costa Playa Grande (sur→norte) y costa norte hasta Cabo Corrientes / Varese
PG = parse("-38.03190,-57.53322;-38.03257,-57.53172;-38.03223,-57.53018;-38.03117,-57.53138;-38.03014,-57.53130;-38.02918,-57.53102;-38.02798,-57.53048;-38.02727,-57.53004;-38.02674,-57.52949")
NORTE = parse("-38.02562,-57.52972;-38.02544,-57.52951;-38.02505,-57.52867;-38.02485,-57.52845;-38.02457,-57.52776;-38.02445,-57.52753;-38.0237,-57.5271;-38.0228,-57.5270;-38.0210,-57.5269;-38.0207,-57.5261;-38.0201,-57.5253;-38.0194,-57.5250;-38.0183,-57.5245;-38.0171,-57.5239;-38.0168,-57.5238;-38.0163,-57.5244;-38.0157,-57.5254;-38.0152,-57.5260;-38.0158,-57.5283;-38.0147,-57.5295;-38.0134,-57.5297;-38.0126,-57.5290;-38.0119,-57.5305;-38.0106,-57.5316;-38.0095,-57.5321;-37.9950,-57.5425")

OBST = {
    "Escollera Norte": LineString(EN),
    "Escollera Sur": LineString(ES),
    "Escollera Biologia": Polygon(BIO).exterior,
    "Costa norte (Cabo Corrientes)": LineString(NORTE),
    "Costa Playa Grande": LineString(PG),
}

# Orientación de la playa: recta de ajuste a la costa de Playa Grande (sin las escolleras)
beach = PG[3:8]
dx = beach[-1][0] - beach[0][0]; dy = beach[-1][1] - beach[0][1]
az_costa = (math.degrees(math.atan2(dx, dy)) + 360) % 360      # rumbo S→N
NORMAL = (az_costa + 90) % 360                                  # hacia el mar

def offset(p, az, d):
    return (p[0] + d * math.sin(math.radians(az)), p[1] + d * math.cos(math.radians(az)))

# Picos: zona de rompiente ~120 m mar adentro de la orilla, pegados a cada escollera
SPOTS = {
    "Biologia": offset(xy(-38.02760, -57.53030), NORMAL, 120),
    "Yacht":    offset(xy(-38.03150, -57.53100), NORMAL, 120),
}

def ray_hit(p, az, maxd=15000):
    """Primer obstáculo en la dirección `az` (de donde viene la ola/viento)."""
    end = offset(p, az, maxd)
    ray = LineString([p, end])
    best = (maxd, None)
    for name, g in OBST.items():
        inter = ray.intersection(g)
        if inter.is_empty:
            continue
        pts = [inter] if inter.geom_type == "Point" else list(getattr(inter, "geoms", [inter]))
        for q in pts:
            d = Point(p).distance(q if q.geom_type == "Point" else Point(q.coords[0]))
            if 1 < d < best[0]:
                best = (d, name)
    return best

def edge_angles(p, geom):
    """Ángulos (az) hacia los vértices de un obstáculo vistos desde el pico."""
    return [(math.degrees(math.atan2(x - p[0], y - p[1])) + 360) % 360 for x, y in geom.coords]

if __name__ == "__main__":
    print(f"Rumbo de la costa S→N: {az_costa:.0f}°   Normal (hacia donde mira la playa): {NORMAL:.0f}°")
    for s, p in SPOTS.items():
        print(f"\n== {s} ==")
        for name, g in OBST.items():
            a = edge_angles(p, g)
            d = min(Point(p).distance(Point(c)) for c in g.coords)
            print(f"  {name:32s} ángulos {min(a):5.0f}°–{max(a):5.0f}°  dist mín {d:5.0f} m")
        row = []
        for az in range(0, 360, 10):
            d, n = ray_hit(p, az)
            row.append(f"{az:3d}:{'open' if n is None else (n.split()[1][:4] if ' ' in n else n[:4])+f'@{d:.0f}'}")
        print("  " + "  ".join(row))
