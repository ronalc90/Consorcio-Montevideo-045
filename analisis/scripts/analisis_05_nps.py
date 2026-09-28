"""Analisis 05 - NPs (Items No Previstos) - V4 (PRESUPUESTO 01-09-2026)."""
import json
import csv
import re
from pathlib import Path
from collections import defaultdict, OrderedDict

ROOT = Path(r"C:\Users\johan albeiro\Documents\Johan\Consorcio-Montevideo-045")
DATOS = ROOT / "analisis" / "datos"
HOJAS = DATOS / "hojas"
OUT = ROOT / "analisis" / "hallazgos"

# ---------- helpers ----------
def fmt(n):
    if n is None:
        return "-"
    return f"{int(round(n)):,}".replace(",", ".")

def norm_code(c):
    if c is None:
        return ""
    s = str(c).strip().upper()
    return s

def is_np_row(item):
    """Un renglon es NP si item_pago inicia con NP o codigo_idu == NO."""
    ip = norm_code(item.get("item_pago"))
    ci = norm_code(item.get("codigo_idu"))
    return ip.startswith("NP") or ci == "NO"

def key_np(item):
    """Clave estable de un NP para join V2<->V4: item_pago si empieza con NP, si no codigo_idu."""
    ip = norm_code(item.get("item_pago"))
    if ip.startswith("NP"):
        return ip
    return norm_code(item.get("codigo_idu"))

# ---------- cargar V4 ----------
v4 = json.load(open(DATOS / "presupuesto_2026_09.json", encoding="utf-8"))
items_v4 = v4["items"]

# ---------- cargar comparativa (V1 IDU, V2 VICON) ----------
comp = json.load(open(ROOT / "comparativa.json", encoding="utf-8"))
nps_objetados = comp["nps_objetados"]
nps_resumen = comp["nps_resumen"]

# ---------- civs V4 map ----------
civs_v4 = v4["civs"]  # lista con id, codigo_seg, subgrupo
civ_ids_v4 = [c["id"] for c in civs_v4]

# ==============================================================
# 1) INVENTARIO DE NPs EN V4
# ==============================================================
np_rows = [it for it in items_v4 if is_np_row(it) and (it.get("cant_actualizada") or 0) > 0]

# subset distinct por item_pago
codes_unicos_ip = set()
codes_unicos_all = set()  # union item_pago + codigo_idu para NPs con codigo_idu=NO
suma_valor_aiu = 0.0
por_unidad = defaultdict(lambda: {"renglones": 0, "valor_aiu": 0.0})
por_capitulo = defaultdict(lambda: {"renglones": 0, "valor_aiu": 0.0})
por_subcapitulo = defaultdict(lambda: {"renglones": 0, "valor_aiu": 0.0})

for it in np_rows:
    codes_unicos_ip.add(norm_code(it.get("item_pago")))
    codes_unicos_all.add(key_np(it))
    v = it.get("valor_actualizado_aiu") or 0
    suma_valor_aiu += v
    und = norm_code(it.get("und")) or "SIN_UND"
    por_unidad[und]["renglones"] += 1
    por_unidad[und]["valor_aiu"] += v
    cap = it.get("chapter") or "SIN_CAPITULO"
    por_capitulo[cap]["renglones"] += 1
    por_capitulo[cap]["valor_aiu"] += v
    sub = it.get("subchapter") or ""
    if sub:
        por_subcapitulo[sub]["renglones"] += 1
        por_subcapitulo[sub]["valor_aiu"] += v

# ==============================================================
# 2) CAMBIOS FRENTE A V2 (items_alt1 en comparativa)
# ==============================================================
# items_alt1.by_chapter[cap].items -> lista de items con is_np
items_v2 = []
for cap_name, cap_data in comp["items_alt1"]["by_chapter"].items():
    for it in cap_data.get("items", []):
        items_v2.append({**it, "chapter": cap_name})

nps_v2 = [it for it in items_v2 if it.get("is_np")]

def key_np_v2(it):
    ip = norm_code(it.get("item_pago"))
    if ip.startswith("NP"):
        return ip
    return norm_code(it.get("codigo_idu"))

# indexes
map_v4 = {key_np(it): it for it in np_rows}
map_v2 = {key_np_v2(it): it for it in nps_v2}

set_v4 = set(map_v4.keys())
set_v2 = set(map_v2.keys())

comunes_keys = set_v4 & set_v2
solo_v2 = set_v2 - set_v4  # eliminados en V4
solo_v4 = set_v4 - set_v2  # nuevos en V4

comunes = []
for k in sorted(comunes_keys):
    a = map_v2[k]; b = map_v4[k]
    cant_v2 = a.get("cant_cont") or 0
    cant_v4 = b.get("cant_actualizada") or 0
    valor_v2_cd = a.get("valor_cont_cd") or 0
    valor_v4_aiu = b.get("valor_actualizado_aiu") or 0
    valor_v4_cd = valor_v4_aiu / 1.31849 if valor_v4_aiu else 0
    comunes.append({
        "code": k,
        "descripcion": (b.get("descripcion") or a.get("descripcion") or "")[:180],
        "und": b.get("und") or a.get("und"),
        "cant_v2": cant_v2,
        "cant_v4": cant_v4,
        "delta_cant": cant_v4 - cant_v2,
        "valor_v2_cd": valor_v2_cd,
        "valor_v4_cd": valor_v4_cd,
        "delta_valor_cd": valor_v4_cd - valor_v2_cd,
        "fila_v4": b.get("row"),
    })

eliminados = []
for k in sorted(solo_v2):
    a = map_v2[k]
    eliminados.append({
        "code": k,
        "descripcion": (a.get("descripcion") or "")[:180],
        "und": a.get("und"),
        "cant_v2": a.get("cant_cont") or 0,
        "valor_v2_cd": a.get("valor_cont_cd") or 0,
        "chapter": a.get("chapter"),
    })

nuevos = []
for k in sorted(solo_v4):
    b = map_v4[k]
    nuevos.append({
        "code": k,
        "descripcion": (b.get("descripcion") or "")[:180],
        "und": b.get("und"),
        "cant_v4": b.get("cant_actualizada") or 0,
        "valor_v4_aiu": b.get("valor_actualizado_aiu") or 0,
        "chapter": b.get("chapter"),
        "fila_v4": b.get("row"),
    })

# ==============================================================
# 3) NPs OBJETADOS QUE SIGUEN INCLUIDOS
# ==============================================================
objetados_incluidos = []
for obj in nps_objetados:
    ip = norm_code(obj["item_pago"])
    ci = norm_code(obj["codigo_idu"])
    # buscar en V4 por item_pago primero, luego codigo_idu, luego descripcion
    hit = None
    for it in np_rows:
        if norm_code(it.get("item_pago")) == ip:
            hit = it; break
    if not hit and ci and ci != "NO":
        for it in np_rows:
            if norm_code(it.get("codigo_idu")) == ci:
                hit = it; break
    if not hit:
        # fallback por descripcion (primeros 40 chars)
        desc_key = re.sub(r"[^A-Z0-9]", "", (obj["descripcion"] or "").upper())[:40]
        for it in np_rows:
            desc_it = re.sub(r"[^A-Z0-9]", "", (it.get("descripcion") or "").upper())[:40]
            if desc_key and desc_it == desc_key:
                hit = it; break
    if hit:
        vu_cd_v2 = obj["vu_cd"]
        vu_cd_v4 = (hit.get("vu_cd") or 0)
        objetados_incluidos.append({
            "item_pago_objetado": obj["item_pago"],
            "codigo_idu_objetado": obj["codigo_idu"],
            "descripcion": obj["descripcion"][:200],
            "und": obj["und"],
            "categoria": obj["categoria"],
            "fila_v4": hit.get("row"),
            "item_pago_v4": hit.get("item_pago"),
            "codigo_idu_v4": hit.get("codigo_idu"),
            "cant_v4": hit.get("cant_actualizada"),
            "valor_v4_aiu": hit.get("valor_actualizado_aiu"),
            "vu_cd_v2": vu_cd_v2,
            "vu_cd_v4": vu_cd_v4,
            "delta_vu_pct": ((vu_cd_v4 - vu_cd_v2) / vu_cd_v2 * 100) if vu_cd_v2 else None,
            "chapter_v4": hit.get("chapter"),
        })
    else:
        objetados_incluidos.append({
            "item_pago_objetado": obj["item_pago"],
            "codigo_idu_objetado": obj["codigo_idu"],
            "descripcion": obj["descripcion"][:200],
            "und": obj["und"],
            "categoria": obj["categoria"],
            "fila_v4": None,
            "vu_cd_v2": obj["vu_cd"],
            "estado": "NO_APARECE_EN_V4",
        })

# ==============================================================
# 4) COMPARACION DE PRECIOS con VISOR y CONTRACTUAL
# ==============================================================
# Cargar VISOR
visor_map = {}  # codigo_idu -> {"vu_cd": .., "descripcion": .., "und": ..}
with open(HOJAS / "VISOR_07-05-25.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    rows = list(reader)
# Buscar cabecera. Miremos las primeras filas.
# (procesamos abajo)
# Cargar PRESUPUESTO CONTRACTUAL MAYO 25
cont_map = {}
with open(HOJAS / "PRESUPUESTO_CONTRACTUAL_MAYO_25.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    cont_rows = list(reader)

# ==============================================================
# 5) NPs GLB / MES
# ==============================================================
nps_glb_mes = []
for it in np_rows:
    und = norm_code(it.get("und"))
    if und in ("GLB", "MES", "GL"):
        cant = it.get("cant_actualizada") or 0
        # coherencia con 8 meses si es MES
        coment = ""
        if und == "MES":
            if abs(cant - 8) < 0.01:
                coment = "Cant = 8 (coherente con adicion de 8 meses)"
            elif abs(cant - 4) < 0.01 or abs(cant - 5) < 0.01:
                coment = f"Cant = {cant} (parece plazo original, no adicion 8 meses)"
            else:
                coment = f"Cant = {cant} (no coincide con 8 meses ni plazo original 4-5)"
        else:
            coment = "Global (GLB) - requiere justificacion desglosada"
        nps_glb_mes.append({
            "item_pago": it.get("item_pago"),
            "codigo_idu": it.get("codigo_idu"),
            "descripcion": (it.get("descripcion") or "")[:180],
            "und": it.get("und"),
            "cantidad": cant,
            "vu_cd": it.get("vu_cd"),
            "valor_aiu": it.get("valor_actualizado_aiu"),
            "fila": it.get("row"),
            "comentario": coment,
        })

# ==============================================================
# 6) TOP 20 NPs POR VALOR
# ==============================================================
np_sorted = sorted(np_rows, key=lambda x: x.get("valor_actualizado_aiu") or 0, reverse=True)
top20 = []
for it in np_sorted[:20]:
    # CIVs donde aplica: aquellos con cant > 0
    civs_aplican = []
    for civ_id, cd in (it.get("civ") or {}).items():
        if (cd.get("cant") or 0) > 0:
            civs_aplican.append(civ_id)
    top20.append({
        "item_pago": it.get("item_pago"),
        "codigo_idu": it.get("codigo_idu"),
        "descripcion": (it.get("descripcion") or "")[:220],
        "und": it.get("und"),
        "cantidad": it.get("cant_actualizada"),
        "K_vu_cd": it.get("vu_cd"),
        "L_vu_cd_aiu": it.get("vu_cd_aiu"),
        "valor_aiu": it.get("valor_actualizado_aiu"),
        "chapter": it.get("chapter"),
        "fila": it.get("row"),
        "civs_count": len(civs_aplican),
        "civs": civs_aplican[:6],  # muestra
    })

# ==============================================================
# 7) CLASIFICACION APROBADO / EN_REVISION / OBJETADO / NUEVO
# ==============================================================
# V1 IDU: items en items_alt1 con is_np=True y cant_idu>0
nps_v1_keys = set()
for it in items_v2:
    if it.get("is_np") and (it.get("cant_idu") or 0) > 0:
        nps_v1_keys.add(key_np_v2(it))

# V2 keys (cant_cont>0)
nps_v2_keys = set()
for it in items_v2:
    if it.get("is_np") and (it.get("cant_cont") or 0) > 0:
        nps_v2_keys.add(key_np_v2(it))

objetados_keys = set()
for obj in nps_objetados:
    ip = norm_code(obj["item_pago"])
    if ip.startswith("NP"):
        objetados_keys.add(ip)
    else:
        objetados_keys.add(norm_code(obj["codigo_idu"]))

clasificacion = {"aprobado": [], "en_revision": [], "objetado": [], "nuevo": []}
for it in np_rows:
    k = key_np(it)
    reg = {
        "item_pago": it.get("item_pago"),
        "codigo_idu": it.get("codigo_idu"),
        "descripcion": (it.get("descripcion") or "")[:140],
        "und": it.get("und"),
        "cantidad": it.get("cant_actualizada"),
        "valor_aiu": it.get("valor_actualizado_aiu"),
        "fila": it.get("row"),
        "chapter": it.get("chapter"),
    }
    if k in objetados_keys:
        clasificacion["objetado"].append(reg)
    elif k in nps_v1_keys:
        clasificacion["aprobado"].append(reg)
    elif k in nps_v2_keys:
        clasificacion["en_revision"].append(reg)
    else:
        clasificacion["nuevo"].append(reg)

# Totales por categoria
totales_clas = {}
for cat, lst in clasificacion.items():
    tot = sum(x["valor_aiu"] or 0 for x in lst)
    totales_clas[cat] = {"renglones": len(lst), "valor_aiu": tot}

# ==============================================================
# HALLAZGOS
# ==============================================================
hallazgos = []

# Objetados incluidos con valor
tot_objetados_incluidos_valor = sum(
    o.get("valor_v4_aiu") or 0 for o in objetados_incluidos if o.get("fila_v4")
)
n_objetados_incluidos = sum(1 for o in objetados_incluidos if o.get("fila_v4"))

if n_objetados_incluidos > 0:
    hallazgos.append({
        "id": "H-NP-01",
        "severidad": "ALTA",
        "titulo": f"{n_objetados_incluidos} NPs objetados por IDU/Interventoría siguen incluidos en V4",
        "descripcion": (
            f"De los 14 NPs listados en la hoja oculta 'NPs Objetados', {n_objetados_incluidos} "
            f"aparecen todavía en V4 con cantidad > 0 y valor con AIU total "
            f"${fmt(tot_objetados_incluidos_valor)}. IDU los rechazó previamente pero el "
            f"contratista los mantiene en el presupuesto de $75.426M."
        ),
        "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP + NPs Objetados",
        "fila": None,
        "impacto_pesos": tot_objetados_incluidos_valor,
        "recomendacion": (
            "Solicitar al contratista soporte formal de la desobjeción (acta o comunicación IDU) "
            "para cada NP objetado que sigue presente; retirar del presupuesto los que no logren "
            "levantar la objeción."
        ),
    })

# Objetados con salto de VU
saltos_vu = [o for o in objetados_incluidos if o.get("delta_vu_pct") is not None and abs(o["delta_vu_pct"]) > 1]
if saltos_vu:
    delta_str = "; ".join(
        f"{s['item_pago_objetado']}: {s['delta_vu_pct']:.1f}% (VU {fmt(s['vu_cd_v2'])} -> {fmt(s['vu_cd_v4'])})"
        for s in saltos_vu[:8]
    )
    hallazgos.append({
        "id": "H-NP-02",
        "severidad": "MEDIA",
        "titulo": f"{len(saltos_vu)} NP(s) objetado(s) con cambio de VU en V4 vs presentación objetada",
        "descripcion": f"Delta VU (CD) V2 vs V4: {delta_str}",
        "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
        "fila": ",".join(str(s.get("fila_v4")) for s in saltos_vu[:8]),
        "impacto_pesos": None,
        "recomendacion": "Cotejar APU actualizado de cada uno de estos NPs; explicar la razón del ajuste de precio."
    })

# NPs nuevos (no aparecen en V1 ni V2 ni objetados)
nuevos_ren = totales_clas["nuevo"]["renglones"]
nuevos_val = totales_clas["nuevo"]["valor_aiu"]
if nuevos_ren > 0:
    hallazgos.append({
        "id": "H-NP-03",
        "severidad": "ALTA" if nuevos_val > 500_000_000 else "MEDIA",
        "titulo": f"{nuevos_ren} NPs completamente nuevos en V4 (no estaban en V1 ni V2)",
        "descripcion": (
            f"Estos NPs aparecen por primera vez en V4 (01-09-2026); no habían sido reconocidos "
            f"en V1 IDU (25-02-2026) ni presentados en V2 VICON (21-04-2026). Valor con AIU: ${fmt(nuevos_val)}."
        ),
        "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
        "fila": None,
        "impacto_pesos": nuevos_val,
        "recomendacion": "Solicitar APUs y actas de fijación de estos NPs; sin dichos soportes no deben incorporarse al presupuesto de adición."
    })

# NPs GLB/MES con incoherencia 8 meses
inc_mes = [x for x in nps_glb_mes if x["und"] and norm_code(x["und"]) == "MES" and not ("coherente" in x["comentario"])]
if inc_mes:
    hallazgos.append({
        "id": "H-NP-04",
        "severidad": "MEDIA",
        "titulo": f"{len(inc_mes)} NP(s) con unidad MES cuya cantidad no cuadra con 8 meses",
        "descripcion": "; ".join(f"{x['item_pago']} cant={x['cantidad']}" for x in inc_mes[:10]),
        "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
        "fila": ",".join(str(x["fila"]) for x in inc_mes[:10]),
        "impacto_pesos": sum(x.get("valor_aiu") or 0 for x in inc_mes),
        "recomendacion": "Ajustar cantidades MES a los 8 meses de la adición o justificar por qué se mantiene otro plazo."
    })

# NPs GLB en general
n_glb = sum(1 for x in nps_glb_mes if norm_code(x["und"]) in ("GLB", "GL"))
if n_glb > 0:
    v_glb = sum(x.get("valor_aiu") or 0 for x in nps_glb_mes if norm_code(x["und"]) in ("GLB", "GL"))
    hallazgos.append({
        "id": "H-NP-05",
        "severidad": "MEDIA",
        "titulo": f"{n_glb} NP(s) con unidad GLB (global) por ${fmt(v_glb)}",
        "descripcion": "Las unidades globales impiden verificar la razonabilidad del valor: cantidad = 1 y precio unitario = valor total.",
        "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
        "fila": ",".join(str(x["fila"]) for x in nps_glb_mes if norm_code(x["und"]) in ("GLB", "GL"))[:200],
        "impacto_pesos": v_glb,
        "recomendacion": "Exigir descomposición del GLB en subactividades medibles con unidades trazables (m², ml, un, etc.)."
    })

# NPs eliminados frente a V2 (esperado tras rechazos IDU)
if eliminados:
    v_elim = sum(x["valor_v2_cd"] for x in eliminados)
    hallazgos.append({
        "id": "H-NP-06",
        "severidad": "INFO",
        "titulo": f"{len(eliminados)} NPs de V2 fueron eliminados en V4",
        "descripcion": f"Reduce en ${fmt(v_elim)} (CD) frente a V2. Verificar si son NPs anulados o solo re-etiquetados.",
        "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
        "fila": None,
        "impacto_pesos": -v_elim,
        "recomendacion": "Revisar en el balance de NPs anulados / rechazados que estos coincidan con los eliminados."
    })

# NPs comunes con incremento fuerte de cantidad
saltos_cant = [c for c in comunes if c["cant_v2"] and c["delta_cant"] / c["cant_v2"] > 0.5 and c["delta_valor_cd"] > 100_000_000]
if saltos_cant:
    hallazgos.append({
        "id": "H-NP-07",
        "severidad": "ALTA",
        "titulo": f"{len(saltos_cant)} NPs con salto >50% en cantidad y >$100M CD entre V2 y V4",
        "descripcion": "; ".join(f"{s['code']} Δcant={s['delta_cant']:.1f} ({s['und']}) ΔCD=${fmt(s['delta_valor_cd'])}" for s in saltos_cant[:8]),
        "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
        "fila": ",".join(str(s["fila_v4"]) for s in saltos_cant[:8]),
        "impacto_pesos": sum(s["delta_valor_cd"] for s in saltos_cant),
        "recomendacion": "Solicitar memoria de cantidad actualizada para cada NP con salto y explicación del cambio."
    })

# ==============================================================
# ESCRIBIR JSON
# ==============================================================
salida = OrderedDict([
    ("meta", {
        "fuente": "PRESUPUESTO 01-09-2026 75MM 8 MESES (V4) vs comparativa.json (V1/V2)",
        "aiu_factor": 0.31849,
        "fecha_analisis": "2026-09-26",
    }),
    ("inventario", {
        "renglones_np": len(np_rows),
        "codigos_np_unicos_item_pago": len(codes_unicos_ip),
        "codigos_np_unicos_incluye_codigo_idu": len(codes_unicos_all),
        "suma_valor_aiu": suma_valor_aiu,
        "por_unidad": {u: {"renglones": d["renglones"], "valor_aiu": d["valor_aiu"]} for u, d in sorted(por_unidad.items(), key=lambda x: -x[1]["valor_aiu"])},
        "por_capitulo": {c: {"renglones": d["renglones"], "valor_aiu": d["valor_aiu"]} for c, d in sorted(por_capitulo.items(), key=lambda x: -x[1]["valor_aiu"])},
        "por_subcapitulo": {c: {"renglones": d["renglones"], "valor_aiu": d["valor_aiu"]} for c, d in sorted(por_subcapitulo.items(), key=lambda x: -x[1]["valor_aiu"])},
    }),
    ("cambios_v2_v4", {
        "nps_v2_total_keys": len(set_v2),
        "nps_v4_total_keys": len(set_v4),
        "comunes_count": len(comunes),
        "eliminados_v2_ausentes_v4_count": len(eliminados),
        "nuevos_solo_v4_count": len(nuevos),
        "eliminados_v2_ausentes_v4": eliminados,
        "nuevos_solo_v4": nuevos,
        "comunes": comunes,
    }),
    ("objetados_incluidos", objetados_incluidos),
    ("nps_glb_mes", nps_glb_mes),
    ("top20", top20),
    ("clasificacion", {
        "totales": totales_clas,
        "aprobado": clasificacion["aprobado"],
        "en_revision": clasificacion["en_revision"],
        "objetado": clasificacion["objetado"],
        "nuevo": clasificacion["nuevo"],
    }),
    ("hallazgos", hallazgos),
])

OUT.mkdir(parents=True, exist_ok=True)
with open(OUT / "05_nps.json", "w", encoding="utf-8") as f:
    json.dump(salida, f, ensure_ascii=False, indent=2)

# ==============================================================
# ESCRIBIR MARKDOWN
# ==============================================================
md = []
md.append("# 05 - Análisis de Ítems No Previstos (NP) - V4 01-09-2026")
md.append("")
md.append(f"**Fuente:** hoja `PRESUPUESTO TODOS LOS CIV 84 NP` + `NPs Objetados` + `comparativa.json` (V1/V2)")
md.append(f"**AIU contractual:** 31,849%")
md.append("")

# Inventario
md.append("## 1. Inventario de NPs en V4")
md.append("")
md.append(f"- Renglones NP con cantidad actualizada > 0: **{len(np_rows)}**")
md.append(f"- Códigos NP únicos por `item_pago`: **{len(codes_unicos_ip)}**")
md.append(f"- Códigos NP únicos incluyendo `codigo_idu` (para renglones con codigo_idu='NO' y sin NP en item_pago): **{len(codes_unicos_all)}**")
md.append(f"- Suma total valor con AIU: **${fmt(suma_valor_aiu)}**")
md.append("")
md.append("La hoja se llama '84 NP' pero solo hay 81 códigos NP con cantidad porque varios códigos NP se replican en más de un renglón (renglones con distinto ítem_pago que comparten el mismo código NP en subcapítulos distintos, y renglones con codigo_idu='NO' que reciben un NP-# en item_pago).")
md.append("")

# Por unidad
md.append("### Desglose por unidad")
md.append("")
md.append("| Unidad | Renglones | Valor con AIU |")
md.append("|---|---:|---:|")
for u, d in sorted(por_unidad.items(), key=lambda x: -x[1]["valor_aiu"]):
    md.append(f"| {u} | {d['renglones']} | ${fmt(d['valor_aiu'])} |")
md.append("")

# Por capitulo
md.append("### Desglose por capítulo")
md.append("")
md.append("| Capítulo | Renglones | Valor con AIU |")
md.append("|---|---:|---:|")
for c, d in sorted(por_capitulo.items(), key=lambda x: -x[1]["valor_aiu"]):
    md.append(f"| {c} | {d['renglones']} | ${fmt(d['valor_aiu'])} |")
md.append("")

# Cambios V2 vs V4
md.append("## 2. Cambios frente a V2 (21-04-2026)")
md.append("")
md.append(f"- NPs en V2 (keys): **{len(set_v2)}**")
md.append(f"- NPs en V4 (keys): **{len(set_v4)}**")
md.append(f"- Comunes (aparecen en ambos): **{len(comunes)}**")
md.append(f"- Eliminados (V2 → ya no en V4): **{len(eliminados)}**")
md.append(f"- Nuevos (aparecen solo en V4): **{len(nuevos)}**")
md.append("")
md.append("### Top 15 eliminados (por valor V2 CD)")
md.append("")
md.append("| code | descripción | und | cant V2 | valor V2 CD | capítulo |")
md.append("|---|---|---|---:|---:|---|")
for e in sorted(eliminados, key=lambda x: -x["valor_v2_cd"])[:15]:
    md.append(f"| {e['code']} | {e['descripcion'][:80]} | {e['und']} | {e['cant_v2']:.2f} | ${fmt(e['valor_v2_cd'])} | {e['chapter']} |")
md.append("")

md.append("### Top 15 nuevos (por valor V4 con AIU)")
md.append("")
md.append("| code | fila | descripción | und | cant V4 | valor V4 AIU |")
md.append("|---|---:|---|---|---:|---:|")
for n in sorted(nuevos, key=lambda x: -x["valor_v4_aiu"])[:15]:
    md.append(f"| {n['code']} | {n['fila_v4']} | {n['descripcion'][:80]} | {n['und']} | {n['cant_v4']:.2f} | ${fmt(n['valor_v4_aiu'])} |")
md.append("")

md.append("### Top 15 comunes con mayor Δvalor")
md.append("")
md.append("| code | fila V4 | descripción | und | cant V2 | cant V4 | valor V2 CD | valor V4 CD | Δ CD |")
md.append("|---|---:|---|---|---:|---:|---:|---:|---:|")
for c in sorted(comunes, key=lambda x: -abs(x["delta_valor_cd"]))[:15]:
    md.append(f"| {c['code']} | {c['fila_v4']} | {c['descripcion'][:60]} | {c['und']} | {c['cant_v2']:.2f} | {c['cant_v4']:.2f} | ${fmt(c['valor_v2_cd'])} | ${fmt(c['valor_v4_cd'])} | ${fmt(c['delta_valor_cd'])} |")
md.append("")

# Objetados
md.append("## 3. NPs objetados que siguen incluidos")
md.append("")
md.append(f"De los **14** NPs de la hoja `NPs Objetados`, **{n_objetados_incluidos}** aparecen en V4 con cantidad > 0.")
md.append(f"Valor total (AIU) de los objetados que siguen incluidos: **${fmt(tot_objetados_incluidos_valor)}**")
md.append("")
md.append("| # | item_pago | codigo_idu | descripción | und | fila V4 | cant V4 | valor V4 AIU | VU V2 CD | VU V4 CD | Δ VU% |")
md.append("|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|")
for i, o in enumerate(objetados_incluidos, 1):
    if o.get("fila_v4"):
        delta = f"{o['delta_vu_pct']:.1f}%" if o.get("delta_vu_pct") is not None else "-"
        md.append(f"| {i} | {o['item_pago_objetado']} | {o['codigo_idu_objetado']} | {o['descripcion'][:70]} | {o['und']} | {o['fila_v4']} | {o['cant_v4']} | ${fmt(o['valor_v4_aiu'])} | ${fmt(o['vu_cd_v2'])} | ${fmt(o['vu_cd_v4'])} | {delta} |")
    else:
        md.append(f"| {i} | {o['item_pago_objetado']} | {o['codigo_idu_objetado']} | {o['descripcion'][:70]} | {o['und']} | *no aparece en V4* | - | - | ${fmt(o['vu_cd_v2'])} | - | - |")
md.append("")

# GLB/MES
md.append("## 4. NPs GLB / MES")
md.append("")
if nps_glb_mes:
    md.append("| item_pago | codigo_idu | descripción | und | cantidad | vu_cd | valor AIU | fila | comentario |")
    md.append("|---|---|---|---|---:|---:|---:|---:|---|")
    for x in nps_glb_mes:
        md.append(f"| {x['item_pago']} | {x['codigo_idu']} | {x['descripcion'][:60]} | {x['und']} | {x['cantidad']} | ${fmt(x['vu_cd'])} | ${fmt(x['valor_aiu'])} | {x['fila']} | {x['comentario']} |")
else:
    md.append("No hay NPs con unidad GLB o MES en V4.")
md.append("")

# Top 20
md.append("## 5. Top 20 NPs por valor con AIU")
md.append("")
md.append("| # | fila | item_pago | codigo_idu | descripción | und | cant | K (VU CD) | L (VU CD+AIU) | valor AIU | capítulo | # CIVs |")
md.append("|---:|---:|---|---|---|---|---:|---:|---:|---:|---|---:|")
for i, t in enumerate(top20, 1):
    md.append(f"| {i} | {t['fila']} | {t['item_pago']} | {t['codigo_idu']} | {t['descripcion'][:70]} | {t['und']} | {t['cantidad']} | ${fmt(t['K_vu_cd'])} | ${fmt(t['L_vu_cd_aiu'])} | ${fmt(t['valor_aiu'])} | {t['chapter']} | {t['civs_count']} |")
md.append("")

# Preguntas por NP top20
md.append("### Preguntas al contratista (top 20)")
md.append("")
pregs = {
    "M3": "¿APU actualizado y justificación de la memoria de cantidad para este material?",
    "M2": "¿Cuál es el CIV de referencia con el área que respalda la cantidad y su categoría de intervención?",
    "ML": "¿Traza de la longitud sobre plano IDU y coincidencia con longitudes contractuales?",
    "UN": "¿Cotizaciones de mercado (mínimo 3) y APU detallado?",
    "KG": "¿Cuál es la memoria de acero/material que genera este peso y su cronograma?",
    "GLB": "¿Descomposición del global en subactividades medibles con unidades trazables?",
    "MES": "¿Justificación del número de meses vs los 8 meses de la adición?",
    "H": "¿Base de horas efectivas requeridas y perfil del recurso?",
}
for i, t in enumerate(top20, 1):
    u = norm_code(t["und"])
    p = pregs.get(u, "¿APU actualizado, memoria de cantidad y soporte del precio unitario?")
    md.append(f"{i}. **fila {t['fila']} · {t['item_pago']} · {t['descripcion'][:80]}** ({t['und']} × {t['cantidad']}) → {p}")
md.append("")

# Clasificacion
md.append("## 6. Clasificación de todos los NPs de V4")
md.append("")
md.append("| categoría | renglones | valor con AIU |")
md.append("|---|---:|---:|")
for cat in ["aprobado", "en_revision", "objetado", "nuevo"]:
    d = totales_clas[cat]
    md.append(f"| {cat} | {d['renglones']} | ${fmt(d['valor_aiu'])} |")
md.append("")
md.append("**Categorías:**")
md.append("- `aprobado`: NP con cant_idu > 0 en V1 IDU 25-02-2026.")
md.append("- `en_revision`: NP con cant_cont > 0 en V2 pero cant_idu = 0 en V1.")
md.append("- `objetado`: NP listado en la hoja oculta `NPs Objetados`.")
md.append("- `nuevo`: NP que no aparece en V1 ni V2 ni en la lista de objetados.")
md.append("")

# Hallazgos
md.append("## 7. Hallazgos")
md.append("")
for h in hallazgos:
    md.append(f"### {h['id']} · [{h['severidad']}] {h['titulo']}")
    md.append(f"- **Hoja/Fila:** {h['hoja']} / {h['fila']}")
    md.append(f"- **Impacto:** ${fmt(h['impacto_pesos'])}" if h.get("impacto_pesos") is not None else "- **Impacto:** N/A")
    md.append(f"- **Descripción:** {h['descripcion']}")
    md.append(f"- **Recomendación:** {h['recomendacion']}")
    md.append("")

with open(OUT / "05_nps.md", "w", encoding="utf-8") as f:
    f.write("\n".join(md))

# Reporte 5 lineas
top3 = np_sorted[:3]
mayor_cat = max(totales_clas.items(), key=lambda x: x[1]["valor_aiu"])
print("=" * 60)
print(f"Total renglones NP en V4: {len(np_rows)} ({len(codes_unicos_ip)} codigos NP unicos)")
print(f"Suma valor con AIU: ${fmt(suma_valor_aiu)}")
print(f"Objetados que siguen incluidos: {n_objetados_incluidos}/14 = ${fmt(tot_objetados_incluidos_valor)}")
print(f"Top 3 por valor:")
for t in top3:
    print(f"  {t.get('item_pago')} | {(t.get('descripcion') or '')[:60]} = ${fmt(t.get('valor_actualizado_aiu'))}")
print(f"Categoria mas pesada: {mayor_cat[0]} con {mayor_cat[1]['renglones']} renglones = ${fmt(mayor_cat[1]['valor_aiu'])}")
