"""
Genera los datos del Plano 3D (plano3d/datos/plano3d_datos.json y plano3d/datos/contexto.json).

Qué hace
  1. Corta de OpenStreetMap el eje real de cada uno de los 27 CIV (entre sus dos cruces) y compara la
     longitud medida con la del presupuesto.
  2. Construye el contexto urbano: vías, manzanas (polígonos que encierra la red vial), edificios,
     parques y rieles, en metros locales.
  3. Calcula por CIV el presupuesto ANTERIOR (V0: cantidad contractual repartida por CIV con el reparto
     del contrato, igual que el análisis 02) y el ACTUAL (V4: matriz ítem × CIV del Excel radicado),
     ambos con el mismo VU con AIU (col L), y los agrupa por material, por fase constructiva, la
     estructura de pavimento (espesor equivalente = m³ ÷ área del CIV) y las redes (ml).
  4. Deja los insumos de la simulación por plazos (valor por fase y por frente).

Entradas: presupuesto_2026_09.json, data.json, analisis_2026_09.json, plano3d/datos/osm/*.json
Uso: python plano3d/scripts/generar_plano3d.py
Datos de vías y edificios © colaboradores de OpenStreetMap (ODbL).
"""
import json
import math
import re
from collections import defaultdict
from pathlib import Path

from shapely.geometry import LineString, Polygon, MultiPolygon, box
from shapely.ops import polygonize, unary_union

ROOT = Path(__file__).resolve().parents[2]
OSM = ROOT / "plano3d" / "datos" / "osm"
OUT_DATA = ROOT / "plano3d" / "datos" / "plano3d_datos.json"
OUT_CTX = ROOT / "plano3d" / "datos" / "contexto.json"

LAT0, LON0 = 4.6385, -74.1150
KX = math.cos(math.radians(LAT0)) * 111320
KY = 110540
AIU = 1.31849


def P(lat, lon):
    return ((lon - LON0) * KX, (lat - LAT0) * KY)


def r1(v):
    return round(v, 1)


# ───────────────────────────── 1. Geometría de los CIV ─────────────────────────────
vias = json.load(open(OSM / "osm_vias_nombradas.json", encoding="utf-8"))
WAYS = [{"name": w["tags"].get("name", ""), "pts": [P(g["lat"], g["lon"]) for g in w["geometry"]]} for w in vias["elements"] if "geometry" in w]
BY = defaultdict(list)
for w in WAYS:
    BY[w["name"]].append(w)


def near(p, q, tol=3):
    return math.hypot(p[0] - q[0], p[1] - q[1]) < tol


def seg_inter(p1, p2, p3, p4):
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(d) < 1e-9:
        return None
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / d
    if -1e-6 <= t <= 1 + 1e-6 and -1e-6 <= u <= 1 + 1e-6:
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    return None


def chains_for(name):
    ws = [list(w["pts"]) for w in BY[name]]
    chains = []
    while ws:
        c = ws.pop(0)
        changed = True
        while changed:
            changed = False
            for i, w in enumerate(ws):
                if near(c[-1], w[0]): c = c + w[1:]
                elif near(c[-1], w[-1]): c = c + w[::-1][1:]
                elif near(c[0], w[-1]): c = w + c[1:]
                elif near(c[0], w[0]): c = w[::-1] + c[1:]
                else: continue
                ws.pop(i); changed = True; break
        chains.append(c)
    return chains


def cum_len(c):
    cum = [0.0]
    for a, b in zip(c, c[1:]):
        cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    return cum


def inters(chain, cross):
    cum = cum_len(chain); out = []
    for o in BY[cross]:
        for i, (a, b) in enumerate(zip(chain, chain[1:])):
            for c, d in zip(o["pts"], o["pts"][1:]):
                p = seg_inter(a, b, c, d)
                if p:
                    out.append((cum[i] + math.hypot(p[0] - a[0], p[1] - a[1]), p))
    out.sort(); ded = []
    for x in out:
        if ded and abs(ded[-1][0] - x[0]) < 25:
            continue
        ded.append(x)
    return ded


def point_at(chain, s):
    cum = cum_len(chain)
    s = max(0, min(cum[-1], s))
    for i in range(len(chain) - 1):
        if cum[i] <= s <= cum[i + 1]:
            t = (s - cum[i]) / max(1e-9, cum[i + 1] - cum[i]); a, b = chain[i], chain[i + 1]
            return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
    return chain[-1]


def sub(chain, s0, s1):
    rev = s0 > s1
    a, b = (s1, s0) if rev else (s0, s1)
    cum = cum_len(chain)
    pts = [point_at(chain, a)] + [chain[i] for i in range(len(chain)) if a < cum[i] < b] + [point_at(chain, b)]
    return pts[::-1] if rev else pts


def pick_chain(street, need, near_pt=None, prefer_short=False):
    cands = []
    for c in chains_for(street):
        hits = {n: inters(c, n) for n in need}
        if all(hits.values()):
            score = 0
            if near_pt:
                score = min(math.hypot(p[0] - near_pt[0], p[1] - near_pt[1]) for n in need for _, p in hits[n])
            if prefer_short:
                score = cum_len(c)[-1]
            cands.append((score, c, hits))
    if not cands:
        raise ValueError(f"Sin cadena para {street} con {need}")
    cands.sort(key=lambda x: x[0])
    return cands[0][1], cands[0][2]


def s_of(hits, name, ref=None, exclude=None):
    opts = [s for s, _ in hits[name] if exclude is None or abs(s - exclude) > 5]
    if ref is None:
        return opts[0]
    return min(opts, key=lambda s: abs(s - ref))


GEOM_NOTAS = {}


def exacto(street, a, b, **kw):
    c, h = pick_chain(street, [a, b] if a != b else [a], **kw)
    sa = s_of(h, a)
    sb = s_of(h, b, ref=sa, exclude=sa)
    return sub(c, sa, sb)


def caminar(street, desde, hacia, largo, extra_need=(), **kw):
    need = [desde] + ([hacia] if hacia not in ("inicio", "fin") else []) + list(extra_need)
    c, h = pick_chain(street, need, **kw)
    sa = s_of(h, desde)
    if hacia == "inicio":
        sgn = -1
    elif hacia == "fin":
        sgn = 1
    else:
        sgn = 1 if s_of(h, hacia, ref=sa, exclude=sa) > sa else -1
    return sub(c, sa, sa + sgn * largo)


CIV_OSM = {  # id del Excel V4 -> cómo se corta del eje OSM (verificado contra la longitud del presupuesto)
    "9004002": lambda: exacto("Calle 20", "Carrera 68A", "Carrera 68B"),
    "9003990": lambda: exacto("Calle 20", "Carrera 68B", "Carrera 68C"),
    "9003980": lambda: exacto("Calle 20", "Carrera 68C", "Carrera 68D"),
    "9003989": lambda: exacto("Carrera 68B", "Calle 20", "Calle 21"),
    "9003981": None,  # se calcula abajo (dos cruces con "Calle 21" en OSM)
    "9003967": None,
    "9003968": None,
    "16000016": lambda: exacto("Carrera 66", "Calle 17A", "Calle 18"),
    "16000007": lambda: exacto("Carrera 66", "Calle 18A", "Calle 18B"),
    "16000023": lambda: exacto("Calle 17A", "Carrera 65B", "Carrera 66"),
    "16000012": lambda: exacto("Calle 18A", "Carrera 65B", "Carrera 66"),
    "16000010": lambda: exacto("Calle 18B", "Carrera 65B", "Carrera 66"),
    "16000013": lambda: exacto("Calle 18B", "Carrera 65B", "Carrera 64"),
    "16000024": lambda: exacto("Carrera 64", "Calle 18", "Calle 18A"),
    "16000017": lambda: exacto("Carrera 64", "Calle 18A", "Calle 18B"),
    "16000029": lambda: caminar("Calle 18", "Carrera 65", "Carrera 64", 69.1),
    "16000028": lambda: caminar("Calle 18A", "Carrera 63", "Carrera 64", 139.7),
    "16000038": lambda: exacto("Calle 18A", "Carrera 62", "Carrera 63"),
    "16000060": lambda: caminar("Carrera 63", "Avenida Calle 17", "Calle 17B", 79.69),
    "16000052": lambda: caminar("Carrera 63", "Calle 17B", "Avenida Calle 17", 89.12),
    "16000043": lambda: caminar("Carrera 63", "Calle 17B", "Calle 18A", 75.97),
    "16000032": lambda: caminar("Carrera 63", "Calle 18A", "Calle 17B", 92.06),
    "16000027": lambda: caminar("Carrera 63", "Calle 18A", "inicio", 78.47, extra_need=["Calle 17B"]),
    "16000057": lambda: exacto("Calle 17B", "Carrera 63", "Carrera 62"),
    "16000047": lambda: caminar("Carrera 65", "Calle 18", "Avenida Calle 17", 118.2),
    "500002375": lambda: caminar("Carrera 65", "Avenida Calle 17", "Calle 18", 71.6),
    "16000077": lambda: caminar("Calle 14", "Carrera 65", "fin", 107.1, prefer_short=True),
}
NOTAS = {
    "9003981": "En OSM la Carrera 68B cruza dos vías llamadas «Calle 21»; el tramo va entre ambas (la del norte corresponde a la Calle 22 del inventario IDU).",
    "9003967": "Carrera 68C entre los dos cruces llamados «Calle 21» en OSM (el del norte corresponde a la Calle 22 del inventario IDU).",
    "9003968": "Calle 21 (la del sur en OSM) entre Carreras 68C y 68D.",
    "16000013": "La «KR 65A» del inventario IDU corresponde en OSM a la Carrera 64 en este sector.",
    "16000024": "La «KR 65A» del inventario IDU corresponde en OSM a la Carrera 64 (entre Calles 18 y 18A).",
    "16000017": "La «KR 65A» del inventario IDU corresponde en OSM a la Carrera 64 (entre Calles 18A y 18B).",
    "16000029": "Calle 18 desde la Carrera 65 hacia la Carrera 64 (OSM «KR 65A»), con la longitud del presupuesto.",
    "16000028": "Calle 18A desde la Carrera 63 hacia la Carrera 64 (OSM «KR 65A»), con la longitud del presupuesto.",
    "16000060": "Carrera 63 desde el acceso a la Av. Calle 17; la cuadra Av. Calle 17 – Calle 17B se reparte entre este CIV y el 16000052 según sus longitudes.",
    "16000052": "Carrera 63 desde la Calle 17B hacia el acceso a la Av. Calle 17 (comparte cuadra con el 16000060).",
    "16000043": "Carrera 63 desde la Calle 17B; la cuadra 17B – 18A se reparte entre este CIV y el 16000032 (la Calle 18 no está mapeada en OSM en este cruce).",
    "16000032": "Carrera 63 desde la Calle 18A hacia la 17B (comparte cuadra con el 16000043).",
    "16000027": "Carrera 63 desde la Calle 18A hacia el norte, con la longitud del presupuesto.",
    "16000047": "Carrera 65 desde la Calle 18 hacia la Av. Calle 17; la cuadra se reparte con el CIV 500002375 (orden supuesto: el inventario los nombra igual «KR65 CL17 – CL18»).",
    "500002375": "Carrera 65 desde la Av. Calle 17 hacia la Calle 18 (comparte cuadra con el 16000047; orden supuesto). Alias 50002375 / 16004876.",
    "16000077": "Calle 14 desde la Carrera 65 hasta el cierre (calle ciega).",
}


def civ_geoms():
    g = {k: f() for k, f in CIV_OSM.items() if f}
    c, h = pick_chain("Carrera 68B", ["Calle 20", "Calle 21"])
    s20 = s_of(h, "Calle 20"); s21a = s_of(h, "Calle 21", ref=s20); s21b = s_of(h, "Calle 21", ref=s21a, exclude=s21a)
    g["9003981"] = sub(c, s21a, s21b)
    c, h = pick_chain("Carrera 68C", ["Calle 20", "Calle 21"])
    s20 = s_of(h, "Calle 20"); s21a = s_of(h, "Calle 21", ref=s20); s21b = s_of(h, "Calle 21", ref=s21a, exclude=s21a)
    g["9003967"] = sub(c, s21a, s21b)
    p_sur = point_at(c, s21a)
    g["9003968"] = exacto("Calle 21", "Carrera 68C", "Carrera 68D", near_pt=p_sur)
    return g


# ───────────────────────────── 2. Contexto urbano ─────────────────────────────
ANCHO_VIA = {"motorway": 24, "trunk": 24, "primary": 20, "primary_link": 9, "secondary": 15, "secondary_link": 8, "tertiary": 12,
             "tertiary_link": 7, "residential": 9, "unclassified": 8, "living_street": 7, "service": 5, "busway": 8, "construction": 9,
             "pedestrian": 5, "footway": 2.2, "cycleway": 2.4, "path": 1.8, "steps": 2}
ALTURA_TIPO = {"warehouse": 10, "industrial": 10, "apartments": 16, "commercial": 9, "residential": 7, "house": 6, "roof": 4, "construction": 6,
               "pavilion": 5, "school": 9, "retail": 7, "office": 14, "church": 11, "hospital": 14, "yes": 7}
XMIN, XMAX, YMIN, YMAX = -600, 1150, -750, 1450


def contexto():
    ctx = json.load(open(OSM / "osm_contexto.json", encoding="utf-8"))
    roads, bldgs, parks, rails, lines_for_blocks, road_polys = [], [], [], [], [], []
    for e in ctx["elements"]:
        if "geometry" not in e:
            continue
        t = e["tags"]; pts = [P(g["lat"], g["lon"]) for g in e["geometry"]]
        if "building" in t and len(pts) >= 4:
            try:
                lv = float(str(t.get("building:levels", "")).split(";")[0])
            except ValueError:
                lv = 0
            h = float(t["height"]) if re.match(r"^[\d.]+$", str(t.get("height", ""))) else (lv * 3.2 if lv else ALTURA_TIPO.get(t["building"], 7))
            poly = Polygon(pts).simplify(0.4)
            if poly.is_valid and poly.area > 12:
                bldgs.append({"p": [[r1(x), r1(y)] for x, y in list(poly.exterior.coords)[:-1]], "h": r1(min(h, 70)), "t": t["building"]})
        elif "highway" in t:
            hw = t["highway"]; w = ANCHO_VIA.get(hw, 6)
            if t.get("area") == "yes":
                continue
            roads.append({"p": [[r1(x), r1(y)] for x, y in pts], "w": w, "c": hw, "n": t.get("name", "")})
            if hw not in ("footway", "cycleway", "path", "steps", "pedestrian", "construction"):
                ls = LineString(pts); lines_for_blocks.append(ls); road_polys.append(ls.buffer(w / 2, cap_style=2, join_style=2))
        elif "railway" in t:
            if t["railway"] in ("rail", "light_rail", "tram", "subway", "construction", "proposed"):
                rails.append({"p": [[r1(x), r1(y)] for x, y in pts], "k": t["railway"]})
        elif len(pts) >= 4:
            poly = Polygon(pts)
            if poly.is_valid and poly.area > 30:
                parks.append({"p": [[r1(x), r1(y)] for x, y in list(poly.simplify(0.5).exterior.coords)[:-1]], "t": t.get("leisure") or t.get("landuse")})
    # Manzanas: polígonos que encierra la red vial, menos el ancho de las vías
    frame = box(XMIN, YMIN, XMAX, YMAX)
    merged = unary_union(lines_for_blocks + [frame.exterior])
    road_area = unary_union(road_polys)
    blocks = []
    for pg in polygonize(merged):
        if not pg.within(frame.buffer(1)):
            continue
        b = pg.difference(road_area).buffer(-1.5, join_style=2)
        geoms = list(b.geoms) if isinstance(b, MultiPolygon) else [b]
        for gg in geoms:
            if gg.is_empty or gg.area < 150 or gg.area > 90000:
                continue
            gg = gg.simplify(0.8)
            if gg.geom_type != "Polygon":
                continue
            blocks.append({"p": [[r1(x), r1(y)] for x, y in list(gg.exterior.coords)[:-1]], "a": round(gg.area)})
    return {"roads": roads, "blocks": blocks, "buildings": bldgs, "parks": parks, "rails": rails,
            "frame": [XMIN, YMIN, XMAX, YMAX]}


# ───────────────────────────── 3. Presupuesto por CIV ─────────────────────────────
MATERIALES = [  # orden = orden de apilado (abajo → arriba) = orden de ranura categórica validada
    {"k": "hidro", "n": "Redes hidrosanitarias", "fase": "redes"},
    {"k": "secas", "n": "Redes secas (energía, telecom., gas)", "fase": "redes"},
    {"k": "tierras", "n": "Demoliciones y movimiento de tierras", "fase": "tierras"},
    {"k": "estab", "n": "Estabilización de subrasante (rajón, RCD, geotextil)", "fase": "estructura"},
    {"k": "granular", "n": "Subbase y base granular", "fase": "estructura"},
    {"k": "asfalto", "n": "Carpeta asfáltica (MD12 / MD19)", "fase": "carpeta"},
    {"k": "losa", "n": "Losa de concreto (pavimento rígido)", "fase": "carpeta"},
    {"k": "anden", "n": "Andenes, espacio público y paisajismo", "fase": "espacio"},
    {"k": "otros", "n": "Señalización y otros", "fase": "acabados"},
]
FASES = [
    {"k": "tierras", "n": "Demoliciones y movimiento de tierras"},
    {"k": "redes", "n": "Redes subterráneas"},
    {"k": "estructura", "n": "Estructura de pavimento (subrasante, subbase, base)"},
    {"k": "carpeta", "n": "Carpeta (asfalto o losa de concreto)"},
    {"k": "espacio", "n": "Andenes y espacio público"},
    {"k": "acabados", "n": "Señalización y acabados"},
]


def material(it):
    d = (it.get("descripcion") or "").upper(); ch = (it.get("chapter") or " ")[:1]; u = (it.get("und") or "").upper()
    if ch == "5": return "hidro"
    if ch == "6": return "secas"
    if ch in ("4", "7"): return "otros"
    if re.search(r"GUAYAC|CAUCHO|CHICAL|HIEDRA|PASTO|ÁRBOL|ARBOL|CESPED|GRAMA|SIEMBRA", d): return "anden"
    if ch == "3" and u == "UN": return "anden"
    if re.search(r"LOSA DE CONCRETO|PAVIMENTO DE CONCRETO|JUNTA|CURADO DE LOSA", d): return "losa"
    if re.search(r"MEZCLA ASF|RIEGO DE (LIGA|IMPRIMACI)|IMPRIMACI|CARPETA ASF|BACHEO", d): return "asfalto"
    if re.search(r"SUBBASE|BASE GRANULAR|MATERIAL SELECCIONADO|MATERIAL ADECUADO", d): return "granular"
    if re.search(r"RAJ[OÓ]N|ESTABILIZACI|RCD|GEOTEXTIL|GEOMALLA|SUBRASANTE|RELLENO", d): return "estab"
    if re.search(r"DEMOLICI|EXCAVACI|TRANSPORTE|RETIRO|FRESADO|REPLANTEO|DESCAPOTE|CORTE|DESMONTE|LIMPIEZA|DISPOSICI", d): return "tierras"
    if ch == "3" or re.search(r"AND[EÉ]N|LOSETA|ADOQU|SARDINEL|BORDILLO|CICLO|PLAZOLETA|RAMPA|BOLARDO|CAÑUELA", d): return "anden"
    return "otros"


CAPA_ESTRUCTURA = {  # capas del pavimento vehicular (capítulos 1-2), de abajo hacia arriba
    "estab": "Estabilización de subrasante", "subbase": "Subbase granular", "base": "Base granular",
    "asfalto": "Carpeta asfáltica", "losa": "Losa de concreto"}


def capa(it, mat):
    d = (it.get("descripcion") or "").upper(); ch = (it.get("chapter") or " ")[:1]; u = (it.get("und") or "").upper()
    if u != "M3" or ch not in ("1", "2"):
        return None
    if mat == "estab": return "estab"
    if mat == "granular": return "subbase" if "SUBBASE" in d else "base"
    if mat == "asfalto": return "asfalto"
    if mat == "losa" and "LOSA" in d: return "losa"
    return None


def presupuesto(geoms):
    pres = json.load(open(ROOT / "presupuesto_2026_09.json", encoding="utf-8"))
    dj = json.load(open(ROOT / "data.json", encoding="utf-8"))
    an = json.load(open(ROOT / "analisis_2026_09.json", encoding="utf-8"))
    alias = {"500002375": "50002375"}
    dj_civ = {c["id"]: c for c in dj["civs"]}
    # reparto contractual por código (igual que el análisis 02)
    share = defaultdict(lambda: defaultdict(float))
    for it in dj["items"]:
        if it.get("type") != "item":
            continue
        for cid, q in (it.get("cantidades") or {}).items():
            share[str(it["codigo_idu"]).strip()][cid] += q or 0
    grupos = {}
    for g, v in (an["costo_civ"].get("grupos_hoja1") or {}).items():
        for cid in v.get("ids_normalizados", []):
            grupos["500002375" if cid in ("50002375", "16004876") else cid] = g
    costo = {c["id"]: c for c in an["costo_civ"]["costo_por_civ"]}
    res_civ = {r["id"]: r for r in an["variacion_civ"]["resumen_por_civ"]}
    desc = {r["id"]: r for r in an["variacion_civ"]["descomposicion_delta_civ"]}
    metr = {r["id"]: r for r in an["variacion_civ"]["metricas_por_m2"]}
    hall = an.get("hallazgos") or []

    civs = []
    sin_reparto = 0.0
    for c in pres["civs"]:
        cid = c["id"]; djid = alias.get(cid, cid); base = dj_civ.get(djid, {})
        area = base.get("area") or 0
        v0 = defaultdict(float); v4 = defaultdict(float)
        q0 = defaultdict(float); q4 = defaultdict(float)
        fase0 = defaultdict(float); fase4 = defaultdict(float); fase_add = defaultdict(float)
        np4 = 0.0; red_ml = {"hidro": [0.0, 0.0], "secas": [0.0, 0.0]}; red_un = {"hidro": [0.0, 0.0], "secas": [0.0, 0.0]}
        anden_m2 = [0.0, 0.0]
        items = []
        for it in pres["items"]:
            if it["row"] >= 680:
                continue  # bloque ACEROS: fuera del total de obras
            L = it.get("vu_cd_aiu") or 0
            mat = material(it); fase = next(m["fase"] for m in MATERIALES if m["k"] == mat)
            cell = (it.get("civ") or {}).get(cid) or {}
            qv4 = cell.get("cant") or 0; vv4 = cell.get("valor") or 0
            code = str(it.get("codigo_idu") or "").strip(); H = it.get("cant_contractual") or 0
            tot = sum(share[code].values()) if code in share else 0
            qv0 = H * share[code].get(djid, 0) / tot if (tot and H) else 0.0
            vv0 = round(qv0 * L)
            if not qv0 and not qv4:
                continue
            v0[mat] += vv0; v4[mat] += vv4; fase0[fase] += vv0; fase4[fase] += vv4; fase_add[fase] += max(0, vv4 - vv0)
            if it.get("is_np"):
                np4 += vv4
            cp = capa(it, mat)
            if cp:
                q0[cp] += qv0; q4[cp] += qv4
            u = (it.get("und") or "").upper()
            if mat in red_ml and u == "ML":
                red_ml[mat][0] += qv0; red_ml[mat][1] += qv4
            if mat in red_un and u == "UN":
                red_un[mat][0] += qv0; red_un[mat][1] += qv4
            if mat == "anden" and u == "M2" and "AND" in (it.get("descripcion") or "").upper():
                anden_m2[0] += qv0; anden_m2[1] += qv4
            items.append({"f": it["row"], "i": str(it.get("item_pago") or ""), "c": code, "d": (it.get("descripcion") or "")[:90], "u": it.get("und"),
                          "m": mat, "q0": round(qv0, 2), "q4": round(qv4, 2), "v0": vv0, "v4": vv4, "np": bool(it.get("is_np"))})
        tot0 = sum(v0.values()); tot4 = sum(v4.values())
        items.sort(key=lambda x: -abs(x["v4"] - x["v0"]))
        top_delta = items[:10]
        top_valor = sorted(items, key=lambda x: -x["v4"])[:10]
        estructura = {k: {"cm0": round(q0[k] / area * 100, 1) if area else 0, "cm4": round(q4[k] / area * 100, 1) if area else 0,
                          "m3_0": round(q0[k], 1), "m3_4": round(q4[k], 1)} for k in CAPA_ESTRUCTURA}
        cc = costo.get(cid, {}); rr = res_civ.get(cid, {}); dd = desc.get(cid, {})
        hs = [{"id": h["id"], "t": h.get("titulo", ""), "s": h.get("severidad", "")} for h in hall if cid in f"{h.get('titulo','')} {h.get('descripcion','')} {h.get('fila','')}" or (cid == "500002375" and re.search(r"16004876|50002375", f"{h.get('titulo','')} {h.get('descripcion','')}"))]
        g = geoms[cid]
        L_osm = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(g, g[1:]))
        civs.append({
            "id": cid, "sg": str(c.get("subgrupo") or base.get("subgrupo") or ""), "nom": base.get("nomenclatura", ""), "tramo": base.get("desde_hasta", ""),
            "longitud": base.get("longitud"), "ancho": base.get("ancho"), "area": area, "grupo": grupos.get(cid, "sin_dato"),
            "geom": [[r1(x), r1(y)] for x, y in g], "long_osm": r1(L_osm), "nota_geom": NOTAS.get(cid, "Eje de OpenStreetMap entre los dos cruces del inventario IDU."),
            "v0": {k: round(v) for k, v in v0.items()}, "v4": {k: round(v) for k, v in v4.items()},
            "tot0": round(tot0), "tot4": round(tot4), "delta": round(tot4 - tot0), "np4": round(np4),
            "fase0": {k: round(v) for k, v in fase0.items()}, "fase4": {k: round(v) for k, v in fase4.items()}, "faseAdd": {k: round(v) for k, v in fase_add.items()},
            "estructura": estructura, "redes": {"ml": {k: [round(a, 1), round(b, 1)] for k, (a, b) in red_ml.items()}, "un": {k: [round(a, 1), round(b, 1)] for k, (a, b) in red_un.items()}},
            "andenM2": [round(anden_m2[0], 1), round(anden_m2[1], 1)],
            "componentes": cc.get("componentes_asignados"), "totalConComp": cc.get("total"), "dm2": cc.get("dolarm2_obras"), "pctNP": cc.get("pct_np_en_obras"),
            "obras0_analisis": rr.get("obras_iniciales_aiu"), "obras4_analisis": rr.get("obras_finales_aiu"),
            "desc": {k: dd.get(k) for k in ("delta_por_aumentos", "delta_por_disminuciones", "delta_por_np", "delta_por_contractual_nuevo", "delta_por_eliminado")},
            "ratios": (metr.get(cid) or {}).get("ratios", {}), "hallazgos": hs[:12],
            "topDelta": top_delta, "topValor": top_valor,
        })
    return civs, an


def main():
    geoms = civ_geoms()
    civs, an = presupuesto(geoms)
    ctx = contexto()
    # verificación
    print(f"{'CIV':>10} {'nom':>8} {'tramo':>22} {'L pres':>7} {'L OSM':>7} {'dif%':>6}  V0 recon.      V4")
    for c in civs:
        dif = (c["long_osm"] / c["longitud"] - 1) * 100 if c["longitud"] else 0
        print(f"{c['id']:>10} {c['nom']:>8} {c['tramo'][:22]:>22} {c['longitud']:7.1f} {c['long_osm']:7.1f} {dif:6.1f}  {c['tot0']:>14,} {c['tot4']:>14,}")
    t0 = sum(c["tot0"] for c in civs); t4 = sum(c["tot4"] for c in civs)
    a0 = sum(c["obras0_analisis"] or 0 for c in civs); a4 = sum(c["obras4_analisis"] or 0 for c in civs)
    print(f"Σ V0 reconstruido {t0:,} (análisis 02: {a0:,}) · Σ V4 {t4:,} (análisis 02: {a4:,}; M688 58.196.933.800)")
    rm = an["versiones_plazo"]["ritmo_mensual"]
    meta = {
        "generado": "2026-09-28", "fuente": "4. PRESUPUESTO 01-09-2026 75MM (8 MESES).xlsx (hoja PRESUPUESTO TODOS LOS CIV 84 NP) + data.json (reparto contractual por CIV) + analisis_2026_09.json",
        "osm": "Geometría © colaboradores de OpenStreetMap (ODbL) · descargada vía Overpass API",
        "proyeccion": {"lat0": LAT0, "lon0": LON0, "m_por_grado_lon": round(KX, 3), "m_por_grado_lat": KY, "nota": "x = este, y = norte, en metros"},
        "aiu": AIU,
        "totales": {"v0_reconstruido": t0, "v4": t4, "v4_M688": 58196933800, "v0_N688": 44303294799, "v0_sin_reparto": 44303294799 - t0,
                    "delta": t4 - t0, "adicion": 16000000000, "np": 14150924549},
        "ritmo": {"meses": rm.get("meses", 8), "mensual_pedido": rm.get("mensual"), "obras_mensual": rm.get("mensualidad_obras_pura"),
                  "gestion_mensual": (rm.get("mensualidad_pma_sst") or 0) + (rm.get("mensualidad_dialogo") or 0) + (rm.get("mensualidad_pmt") or 0),
                  "historico_mensual_aprox": 600000000, "nota_historico": "Cota superior estimada en el hallazgo H06-03 (el libro no trae ejecución mes a mes)."},
        "materiales": MATERIALES, "fases": FASES, "capas": CAPA_ESTRUCTURA,
        "grupos": {"ya_iniciados": "Ya iniciados (Hoja1)", "por_iniciar": "Por iniciar (Hoja1)", "no_alcanza": "No alcanza (excluidos en Alt. 2)"},
        "notas": [
            "V0 (anterior) = cantidad contractual de cada renglón (col H) repartida por CIV con el reparto del contrato (data.json), valorada con el VU con AIU de V4 (col L), igual que el análisis 02. Hay renglones sin reparto por CIV que no se pueden ubicar en el plano (ver totales.v0_sin_reparto).",
            "V4 (actual) = matriz ítem × CIV del Excel radicado el 01-09-2026 (columnas S…BW).",
            "Espesor equivalente de cada capa = m³ del CIV ÷ área del CIV. Es una medida de intensidad, no el espesor de diseño.",
            "La simulación por plazos es ilustrativa: el contratista no entregó cronograma (registro de auditoría C-04).",
        ],
    }
    OUT_DATA.write_text(json.dumps({"meta": meta, "civs": civs}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    OUT_CTX.write_text(json.dumps(ctx, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"escrito {OUT_DATA.name} ({OUT_DATA.stat().st_size/1024:.0f} KB) y {OUT_CTX.name} ({OUT_CTX.stat().st_size/1024:.0f} KB): "
          f"{len(ctx['roads'])} vías, {len(ctx['blocks'])} manzanas, {len(ctx['buildings'])} edificios, {len(ctx['parks'])} zonas verdes, {len(ctx['rails'])} rieles")


if __name__ == "__main__":
    main()
