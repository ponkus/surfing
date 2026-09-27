"""Modelo de pico para Playa Grande: Biología vs Yacht.

Entradas por hora (Open-Meteo, punto mar adentro):
  swell H0 [m], T [s], dir [°];  viento vel [km/h], dir [°];  mar de viento [m];  nivel del mar [m]
Salida: altura estimada en rompiente por pico + puntaje 0-5 + motivo.
"""
import math
from geo import SPOTS, NORMAL, ray_hit

G = 9.81
OFFSHORE = (NORMAL + 180) % 360          # 285°

def angdiff(a, b):
    return abs((a - b + 180) % 360 - 180)

# ---------- 1. Exposición al swell por pico (geometría + difracción) ----------
def blocked_factor(dist):
    """Cuánta ola pasa detrás de un obstáculo (difracción), según qué tan lejos está."""
    if dist < 300:   return 0.20     # escollera pegada al pico: sombra profunda
    if dist < 1000:  return 0.45
    return 0.65                        # obstáculo lejano: la ola se reabre por difracción

def refraction(theta):
    """Pérdida por entrar cruzado: Kr = sqrt(cos Δ) respecto de la normal de la playa."""
    d = angdiff(theta, NORMAL)
    if d < 90:
        return max(math.sqrt(math.cos(math.radians(d))), 0.25 if d > 60 else 0)
    return 0.25 * max(0.0, (130 - d) / 40)   # 90–130°: la plataforma poco profunda la sigue doblando algo

_cache = {}
def spread_for(T):
    """Dispersión direccional: mar de viento corto se abre mucho, swell de fondo viene ordenado."""
    return 45 if T < 8 else 30 if T < 11 else 20

def exposure(spot, theta, spread=25):
    """Factor de altura (0-1) para swell desde `theta`, promediado en ±spread (dispersión direccional)."""
    key = (spot, round(theta), spread)
    if key in _cache:
        return _cache[key]
    p = SPOTS[spot]
    num = den = 0.0
    for k in range(-spread, spread + 1, 5):
        w = math.cos(math.radians(k * 90 / (spread + 5))) ** 2
        phi = (theta + k) % 360
        dist, obst = ray_hit(p, phi)
        f = refraction(phi) * (1.0 if obst is None else blocked_factor(dist))
        num += w * f; den += w
    _cache[key] = num / den
    return _cache[key]

# ---------- 2. Viento: fetch local por pico ----------
def local_wind_factor(spot, wdir):
    """Qué fracción del viento 'llega' a ensuciar la ola en el pico.
    Viento de tierra -> 0 (no genera picado). Viento de mar -> según fetch hasta el primer obstáculo."""
    if angdiff(wdir, NORMAL) >= 115:      # viento claramente de tierra
        return 0.0
    dist, obst = ray_hit(SPOTS[spot], wdir)
    fetch = 3000 if obst is None else (dist if "Costa" not in obst or dist > 150 else 0)
    return min(1.0, math.sqrt(fetch / 1500))

# ---------- 3. Altura en rompiente (Komar & Gaillard 1973) ----------
def breaking_height(H0, T):
    return 0.39 * G ** 0.2 * (T * H0 ** 2) ** 0.4

# ---------- 4. Puntaje ----------
def size_score(hb):          # bodyboard: arranca a 0.5 m, ideal 0.9–2.0 m, se cierra arriba de 2.5
    if hb < 0.45: return 0.0
    if hb < 0.9:  return (hb - 0.45) / 0.45
    if hb <= 2.0: return 1.0
    return max(0.3, 1 - (hb - 2.0) / 1.5)

def wind_score(spot, spd, wdir):
    on = math.cos(math.radians(angdiff(wdir, NORMAL)))       # +1 onshore puro, -1 offshore puro
    if on <= -0.3:                                            # offshore / side-off
        return 1.0 if spd < 30 else max(0.5, 1 - (spd - 30) / 40)
    eff = spd * local_wind_factor(spot, wdir) * max(on, 0.35)
    return max(0.0, 1 - eff / 22)

def tide_score(level, lo, hi):
    if hi - lo < 0.1: return 1.0
    p = (level - lo) / (hi - lo)
    return 1 - 0.35 * abs(2 * p - 1)                        # media marea = 1, extremos = 0.65

def evaluate(hour, lo, hi):
    out = {}
    for spot in SPOTS:
        ex = exposure(spot, hour["sw_dir"], spread_for(hour["sw_t"]))
        hb = breaking_height(hour["sw_h"], hour["sw_t"]) * ex
        chop = hour["ww_h"] * exposure(spot, hour["w_dir"]) if angdiff(hour["w_dir"], NORMAL) < 90 else 0
        s = size_score(hb) * wind_score(spot, hour["w_spd"], hour["w_dir"]) \
            * max(0.3, 1 - chop / 0.8) * tide_score(hour["tide"], lo, hi)
        if hour["sw_t"] >= 9: s = min(1.0, s * 1.15)
        out[spot] = {"hb": hb, "exp": ex, "score": round(5 * s, 1),
                     "lw": local_wind_factor(spot, hour["w_dir"])}
    return out

def compass(d):
    return ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSO","SO","OSO","O","ONO","NO","NNO"][int((d % 360) / 22.5 + 0.5) % 16]

if __name__ == "__main__":
    print(f"Normal de la playa {NORMAL:.0f}° ({compass(NORMAL)}), offshore puro {OFFSHORE:.0f}° ({compass(OFFSHORE)})\n")
    print("SWELL: factor de altura por dirección (1.0 = entra de frente sin obstáculos)")
    print(" dir      Biología  Yacht   ganador")
    for d in range(0, 211, 15):
        b, y = exposure("Biologia", d, 30), exposure("Yacht", d, 30)
        win = "—" if max(b, y) < 0.08 else ("Biología" if b > y * 1.15 else "Yacht" if y > b * 1.15 else "parejo")
        print(f" {d:3d}° {compass(d):>3}   {b:5.2f}   {y:5.2f}   {win}")
    print("\nVIENTO: fracción del viento que ensucia cada pico (0 = limpio, 1 = expuesto)")
    print(" dir      Biología  Yacht   más reparado")
    for d in range(0, 360, 22):
        d = round(d / 22.5) * 22.5
        b, y = local_wind_factor("Biologia", d), local_wind_factor("Yacht", d)
        tag = "offshore, limpio ambos" if b == y == 0 else ("Biología" if b < y - 0.1 else "Yacht" if y < b - 0.1 else "parejo")
        print(f" {d:5.1f}° {compass(d):>3}   {b:5.2f}   {y:5.2f}   {tag}")
