"""
Descarga de OpenStreetMap (Overpass API) la geometría usada por el plano 3D.

  1. osm_vias_nombradas.json  → todas las vías con nombre del sector (para cortar los 27 CIV)
  2. osm_contexto.json        → edificios, parques, vías y rieles alrededor de los frentes (contexto urbano)

Datos © colaboradores de OpenStreetMap, licencia ODbL (https://www.openstreetmap.org/copyright).
Uso: python plano3d/scripts/descargar_osm.py   (tarda ~1-3 min; prueba varios servidores espejo)
"""
import json
import math
import time
import urllib.parse
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "datos" / "osm"
ESPEJOS = [
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass-api.de/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
]
# Centro de la proyección local (metros) — el mismo que usa generar_plano3d.py
LAT0, LON0 = 4.6385, -74.1150
KX = math.cos(math.radians(LAT0)) * 111320
KY = 110540


def bbox(x0, x1, y0, y1):
    return f"{LAT0 + y0 / KY:.5f},{LON0 + x0 / KX:.5f},{LAT0 + y1 / KY:.5f},{LON0 + x1 / KX:.5f}"


CONSULTAS = {
    "osm_vias_nombradas.json": '[out:json][timeout:90];(way["highway"]["name"](4.615,-74.130,4.655,-74.095););out geom tags;',
    "osm_contexto.json": '[out:json][timeout:120];(way["building"]({b});way["leisure"~"park|pitch"]({b});way["landuse"~"grass|recreation_ground"]({b});'
                         'way["railway"]({b});way["highway"]({b}););out geom tags;'.format(b=bbox(-600, 1150, -750, 1450)),
}


def pedir(q):
    for url in ESPEJOS:
        try:
            data = urllib.parse.urlencode({"data": q}).encode()
            req = urllib.request.Request(url, data=data, headers={"User-Agent": "consorcio-montevideo-045-plano3d/1.0"})
            with urllib.request.urlopen(req, timeout=180) as r:
                txt = r.read().decode("utf-8")
            j = json.loads(txt)
            if j.get("elements"):
                print(f"  ok {url} · {len(j['elements'])} elementos")
                return j
        except Exception as e:  # siguiente espejo
            print(f"  falla {url}: {str(e)[:80]}")
        time.sleep(2)
    raise SystemExit("Ningún servidor Overpass respondió")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for nombre, q in CONSULTAS.items():
        print("Descargando", nombre)
        j = pedir(q)
        (OUT / nombre).write_text(json.dumps(j, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
