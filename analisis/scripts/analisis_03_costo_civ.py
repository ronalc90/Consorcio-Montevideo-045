"""
Análisis 03 · Costo por CIV (obras + componentes → 75.426.575.199)

Genera:
  analisis/hallazgos/03_costo_civ.md
  analisis/hallazgos/03_costo_civ.json
"""
import json
import math
import statistics
from pathlib import Path

ROOT = Path(r"C:\Users\johan albeiro\Documents\Johan\Consorcio-Montevideo-045")
OUT_MD = ROOT / "analisis" / "hallazgos" / "03_costo_civ.md"
OUT_JSON = ROOT / "analisis" / "hallazgos" / "03_costo_civ.json"

AIU = 0.31849
AIU_FACTOR = 1 + AIU  # 1.31849

# --- Cargar datos canónicos ---
presu = json.load(open(ROOT / "analisis" / "datos" / "presupuesto_2026_09.json", "r", encoding="utf-8"))
comp = json.load(open(ROOT / "comparativa.json", "r", encoding="utf-8"))
data = json.load(open(ROOT / "data.json", "r", encoding="utf-8"))

# Verificar estructura de data.json
if isinstance(data, dict) and "civs" in data:
    data_civs = data["civs"]
elif isinstance(data, list):
    data_civs = data
else:
    data_civs = data.get("civs", [])

# --- Componentes no-obra (V4) ---
componentes_v4 = {
    "PMA-SST": 4110277014,
    "Dialogo ciudadano": 2430023370,
    "PMT": 2007577162,
    "Fondo compensaciones": 0,
    "Ajustes cambio vigencia": 4555525079,
    "Actividades acero": 2977517840,
    "Ensayos laboratorio": 299267609,
    "SDA": 31328679,
    "Fase obras iniciales": 758734334,
    "Bioseguridad": 59390312,
}
TOTAL_COMPONENTES = sum(componentes_v4.values())  # 17.229.641.399
TOTAL_GENERAL_ESPERADO = 75426575199
TOTAL_OBRAS_ESPERADO = 58196933800  # fila 688 col M

# --- Mapa CIVs (id → subgrupo, nomenclatura, area, longitud) ---
civ_meta = {}

# 1) Del presupuesto (subgrupo y orden)
for c in presu["civs"]:
    civ_meta[c["id"]] = {
        "id": c["id"],
        "subgrupo": c["subgrupo"],
        "codigo_seg": c["codigo_seg"],
        "nomenclatura": None,
        "desde_hasta": None,
        "area_m2": None,
        "longitud_m": None,
        "ancho_m": None,
    }

# 2) Enriquecer con data.json (áreas y nomenclatura)
def norm_id(cid):
    if cid is None:
        return None
    s = str(cid).strip()
    # normalizar "16004876 (50002375)" → clave principal
    if " " in s:
        parts = s.split(" ")
        return parts[0]
    return s

for c in data_civs:
    cid_raw = c.get("id") or c.get("civ") or c.get("CIV")
    cid = norm_id(cid_raw)
    if not cid:
        continue
    # también intentar como "500002375" vs "50002375"
    keys_try = [cid_raw and str(cid_raw).strip(), cid]
    matched = None
    for k in keys_try:
        if k in civ_meta:
            matched = k
            break
    # también probar alias 50002375 → 500002375 y viceversa
    if not matched:
        if cid == "50002375" and "500002375" in civ_meta:
            matched = "500002375"
        elif cid == "500002375" and "50002375" in civ_meta:
            matched = "50002375"
        elif cid == "16004876" and "500002375" in civ_meta:
            # 16004876 y 500002375 comparten segmento pero son CIVs distintos según BRIEF; no mapear
            pass
    if not matched:
        continue
    m = civ_meta[matched]
    m["nomenclatura"] = c.get("nomenclatura") or c.get("via") or m["nomenclatura"]
    m["desde_hasta"] = c.get("desde_hasta") or c.get("tramo") or m["desde_hasta"]
    m["area_m2"] = c.get("area") or c.get("area_m2") or m["area_m2"]
    m["longitud_m"] = c.get("longitud") or c.get("longitud_m") or m["longitud_m"]
    m["ancho_m"] = c.get("ancho") or c.get("ancho_m") or m["ancho_m"]
    m["subgrupo_data"] = c.get("subgrupo")

# 3) Enriquecer con comparativa.civs (V0-derivado dashboard) como fallback
for c in comp.get("civs", []):
    cid = norm_id(c["id"])
    if cid == "16004876":
        # este es 500002375 en el presupuesto V4
        target = "500002375"
    else:
        target = cid
    if target in civ_meta:
        m = civ_meta[target]
        if not m["nomenclatura"]:
            m["nomenclatura"] = c.get("nomenclatura")
        if not m["desde_hasta"]:
            m["desde_hasta"] = c.get("desde_hasta")
        if not m["area_m2"]:
            m["area_m2"] = c.get("area")
        if not m["longitud_m"]:
            m["longitud_m"] = c.get("longitud")
        if not m["ancho_m"]:
            m["ancho_m"] = c.get("ancho")

# --- Mapear V1 IDU y V2 VICON por CIV ---
def build_map(rows, id_key="id"):
    out = {}
    for r in rows:
        cid_raw = str(r[id_key]).strip()
        cid_norm = norm_id(cid_raw)
        # tratar "16004876 (50002375)" → mapear a 500002375
        if cid_norm == "16004876":
            cid_norm = "500002375"
        out[cid_norm] = r
    return out

civs_idu = build_map(comp["civs_idu"])
civs_cont = build_map(comp["civs_cont"])
civs_dash = build_map(comp["civs"])

# --- 1) Obras con AIU por CIV desde presupuesto_2026_09.json ---
# Excluir bloque ACEROS (chapter "8. ACTIVIDADES ACERO")
items = [it for it in presu["items"] if it.get("chapter") != "8. ACTIVIDADES ACERO"]

# Suma por CIV desde it.civ[cid].valor
obras_aiu_por_civ = {cid: 0.0 for cid in civ_meta}
for it in items:
    for cid, cv in it.get("civ", {}).items():
        if cid in obras_aiu_por_civ:
            v = cv.get("valor") or 0
            obras_aiu_por_civ[cid] += v

total_obras_aiu_calc = sum(obras_aiu_por_civ.values())

# --- Desglose por capítulo por CIV ---
capitulos = ["1. PRELIMINARES", "2. PAVIMENTOS", "3. ESPACIO PÚBLICO",
             "4. SEÑALIZACIÓN Y DEMARCACIÓN", "5. REDES HIDROSANITARIAS",
             "6. REDES SECAS", "7. DESVÍOS"]

desglose_cap_civ = {cid: {cap: 0.0 for cap in capitulos} for cid in civ_meta}
np_por_civ = {cid: 0.0 for cid in civ_meta}
contractual_por_civ = {cid: 0.0 for cid in civ_meta}
redes_por_civ = {cid: 0.0 for cid in civ_meta}
sin_redes_por_civ = {cid: 0.0 for cid in civ_meta}

for it in items:
    cap = it.get("chapter")
    is_np = it.get("is_np", False)
    for cid, cv in it.get("civ", {}).items():
        if cid not in civ_meta:
            continue
        v = cv.get("valor") or 0
        if cap in desglose_cap_civ[cid]:
            desglose_cap_civ[cid][cap] += v
        if is_np:
            np_por_civ[cid] += v
        else:
            contractual_por_civ[cid] += v
        if cap in ("5. REDES HIDROSANITARIAS", "6. REDES SECAS"):
            redes_por_civ[cid] += v
        else:
            sin_redes_por_civ[cid] += v

# CD y AIU separados
obras_cd_por_civ = {cid: v / AIU_FACTOR for cid, v in obras_aiu_por_civ.items()}
obras_aiu_solo_por_civ = {cid: obras_aiu_por_civ[cid] - obras_cd_por_civ[cid] for cid in civ_meta}

# --- 2) Verificación fila 688 ---
verif_688 = {
    "calculado": round(total_obras_aiu_calc),
    "esperado_58196933800": TOTAL_OBRAS_ESPERADO,
    "delta": round(total_obras_aiu_calc - TOTAL_OBRAS_ESPERADO),
}

# --- 3) Reparto componentes no-obra ---
# Criterio: proporcional al costo directo de obras por CIV (V4)
denom_reparto = sum(obras_cd_por_civ.values())
componentes_asignados_por_civ = {}
for cid in civ_meta:
    frac = obras_cd_por_civ[cid] / denom_reparto if denom_reparto else 0
    componentes_asignados_por_civ[cid] = TOTAL_COMPONENTES * frac

total_civ = {cid: obras_aiu_por_civ[cid] + componentes_asignados_por_civ[cid] for cid in civ_meta}
sum_total_civ = sum(total_civ.values())

verif_total = {
    "calculado": round(sum_total_civ),
    "esperado_75426575199": TOTAL_GENERAL_ESPERADO,
    "delta": round(sum_total_civ - TOTAL_GENERAL_ESPERADO),
}

verif_componentes = {
    "suma_componentes": TOTAL_COMPONENTES,
    "esperado_17229641399": 17229641399,
    "delta": TOTAL_COMPONENTES - 17229641399,
}

# --- 4) $/m² y $/ml ---
dolarm2_obras_por_civ = {}
dolarm2_total_por_civ = {}
dolarml_obras_por_civ = {}
dolarml_total_por_civ = {}
for cid, m in civ_meta.items():
    a = m.get("area_m2")
    l = m.get("longitud_m")
    if a and a > 0:
        dolarm2_obras_por_civ[cid] = obras_aiu_por_civ[cid] / a
        dolarm2_total_por_civ[cid] = total_civ[cid] / a
    if l and l > 0:
        dolarml_obras_por_civ[cid] = obras_aiu_por_civ[cid] / l
        dolarml_total_por_civ[cid] = total_civ[cid] / l

# Estadística $/m² obras
vals_dolarm2_obras = list(dolarm2_obras_por_civ.values())
def pct(lst, p):
    if not lst:
        return None
    s = sorted(lst)
    k = (len(s) - 1) * p
    f = int(math.floor(k))
    c = int(math.ceil(k))
    if f == c:
        return s[f]
    return s[f] * (c - k) + s[c] * (k - f)

def stats(lst):
    if not lst:
        return {}
    return {
        "media": round(statistics.mean(lst)),
        "mediana": round(statistics.median(lst)),
        "p25": round(pct(lst, 0.25)),
        "p75": round(pct(lst, 0.75)),
        "min": round(min(lst)),
        "max": round(max(lst)),
        "std": round(statistics.stdev(lst)) if len(lst) > 1 else 0,
    }

est_obras = stats(vals_dolarm2_obras)
est_total = stats(list(dolarm2_total_por_civ.values()))

# Por subgrupo
sub2_vals = [dolarm2_obras_por_civ[c] for c in civ_meta if civ_meta[c]["subgrupo"] == "2" and c in dolarm2_obras_por_civ]
sub5_vals = [dolarm2_obras_por_civ[c] for c in civ_meta if civ_meta[c]["subgrupo"] == "5" and c in dolarm2_obras_por_civ]
est_sub2 = stats(sub2_vals)
est_sub5 = stats(sub5_vals)

# Outliers: mediana ± 1.5 IQR
med = est_obras["mediana"]
iqr = est_obras["p75"] - est_obras["p25"]
lim_sup = med + 1.5 * iqr
lim_inf = med - 1.5 * iqr

outliers_ids = []
for cid, dm2 in dolarm2_obras_por_civ.items():
    if dm2 > lim_sup or dm2 < lim_inf:
        outliers_ids.append((cid, dm2))
outliers_ids.sort(key=lambda x: -x[1])

# Top 5 items por CIV outlier
def top_items_civ(cid, k=5):
    lst = []
    for it in items:
        v = (it.get("civ") or {}).get(cid, {}).get("valor")
        if v and v > 0:
            lst.append({
                "row": it["row"],
                "item_pago": it.get("item_pago"),
                "descripcion": (it.get("descripcion") or "")[:120],
                "und": it.get("und"),
                "chapter": it.get("chapter"),
                "is_np": it.get("is_np"),
                "valor_aiu": round(v),
                "cantidad": (it.get("civ") or {}).get(cid, {}).get("cant"),
            })
    lst.sort(key=lambda r: -r["valor_aiu"])
    return lst[:k]

outliers_detalle = []
for cid, dm2 in outliers_ids:
    outliers_detalle.append({
        "id": cid,
        "nomenclatura": civ_meta[cid].get("nomenclatura"),
        "subgrupo": civ_meta[cid]["subgrupo"],
        "area_m2": civ_meta[cid].get("area_m2"),
        "dolarm2_obras": round(dm2),
        "obras_aiu": round(obras_aiu_por_civ[cid]),
        "veces_sobre_mediana": round(dm2 / med, 2) if med else None,
        "explicacion_top_5_items": top_items_civ(cid, 5),
    })

# --- 5) Comparativa V1/V2/V4 ---
comparativa_v1_v2_v4 = []
for cid in civ_meta:
    v1 = civs_idu.get(cid, {})
    v2 = civs_cont.get(cid, {})
    v1_total = v1.get("cd_aiu")
    v2_total = v2.get("cd_aiu")
    v4_obras_aiu = obras_aiu_por_civ[cid]
    comparativa_v1_v2_v4.append({
        "id": cid,
        "nomenclatura": civ_meta[cid].get("nomenclatura"),
        "subgrupo": civ_meta[cid]["subgrupo"],
        "area_m2": civ_meta[cid].get("area_m2"),
        "v1_cd": v1.get("costo_directo"),
        "v1_aiu": v1.get("aiu"),
        "v1_total": v1_total,
        "v1_dolarm2": v1.get("vr_m2"),
        "v2_cd": v2.get("costo_directo"),
        "v2_aiu": v2.get("aiu"),
        "v2_total": v2_total,
        "v2_dolarm2": v2.get("vr_m2"),
        "v4_obras_cd": round(obras_cd_por_civ[cid]),
        "v4_obras_aiu_solo": round(obras_aiu_solo_por_civ[cid]),
        "v4_obras_aiu": round(v4_obras_aiu),
        "v4_dolarm2": round(dolarm2_obras_por_civ[cid]) if cid in dolarm2_obras_por_civ else None,
        "delta_v4_v1": round(v4_obras_aiu - v1_total) if v1_total else None,
        "delta_v4_v1_pct": round((v4_obras_aiu / v1_total - 1) * 100, 2) if v1_total else None,
        "delta_v4_v2": round(v4_obras_aiu - v2_total) if v2_total else None,
        "delta_v4_v2_pct": round((v4_obras_aiu / v2_total - 1) * 100, 2) if v2_total else None,
    })

# --- 6) Grupos alcance Hoja1 (comparativa.alcance_alt2) ---
grupos_raw = comp["alcance_alt2"]
def normaliza_id_grupo(gid):
    # 16004876 → 500002375 en V4
    return "500002375" if gid == "16004876" else gid

grupos_hoja1 = {}
for gname, ids in grupos_raw.items():
    ids_norm = [normaliza_id_grupo(i) for i in ids]
    obras_total = sum(obras_aiu_por_civ.get(cid, 0) for cid in ids_norm)
    componentes_total = sum(componentes_asignados_por_civ.get(cid, 0) for cid in ids_norm)
    total = obras_total + componentes_total
    grupos_hoja1[gname] = {
        "ids_originales": ids,
        "ids_normalizados": ids_norm,
        "cantidad_civs": len(ids_norm),
        "obras_total": round(obras_total),
        "componentes_total": round(componentes_total),
        "total": round(total),
    }

# --- Serializar costo_por_civ ---
costo_por_civ = []
for cid in civ_meta:
    m = civ_meta[cid]
    obras_aiu = obras_aiu_por_civ[cid]
    pct_np = (np_por_civ[cid] / obras_aiu * 100) if obras_aiu else 0
    row = {
        "id": cid,
        "nomenclatura": m.get("nomenclatura"),
        "desde_hasta": m.get("desde_hasta"),
        "subgrupo": m["subgrupo"],
        "area_m2": m.get("area_m2"),
        "longitud_m": m.get("longitud_m"),
        "obras_cd": round(obras_cd_por_civ[cid]),
        "obras_aiu": round(obras_aiu_solo_por_civ[cid]),
        "obras_total": round(obras_aiu),
        "componentes_asignados": round(componentes_asignados_por_civ[cid]),
        "total": round(total_civ[cid]),
        "dolarm2_obras": round(dolarm2_obras_por_civ[cid]) if cid in dolarm2_obras_por_civ else None,
        "dolarm2_total": round(dolarm2_total_por_civ[cid]) if cid in dolarm2_total_por_civ else None,
        "dolarml_obras": round(dolarml_obras_por_civ[cid]) if cid in dolarml_obras_por_civ else None,
        "dolarml_total": round(dolarml_total_por_civ[cid]) if cid in dolarml_total_por_civ else None,
        "pct_np_en_obras": round(pct_np, 2),
    }
    costo_por_civ.append(row)

# Desglose por capítulo x CIV (aplanado)
desglose_cap_civ_flat = []
for cid in civ_meta:
    for cap in capitulos:
        v_aiu = desglose_cap_civ[cid][cap]
        if v_aiu != 0:
            desglose_cap_civ_flat.append({
                "id": cid,
                "capitulo": cap,
                "cd": round(v_aiu / AIU_FACTOR),
                "aiu": round(v_aiu - v_aiu / AIU_FACTOR),
                "total": round(v_aiu),
            })

desglose_np_flat = []
for cid in civ_meta:
    o = obras_aiu_por_civ[cid]
    npv = np_por_civ[cid]
    cv = contractual_por_civ[cid]
    desglose_np_flat.append({
        "id": cid,
        "contractual_total": round(cv),
        "np_total": round(npv),
        "pct_np": round((npv / o * 100), 2) if o else 0,
    })

redes_flat = []
for cid in civ_meta:
    o = obras_aiu_por_civ[cid]
    r = redes_por_civ[cid]
    sr = sin_redes_por_civ[cid]
    redes_flat.append({
        "id": cid,
        "redes_total": round(r),
        "sin_redes_total": round(sr),
        "pct_redes": round((r / o * 100), 2) if o else 0,
    })

# --- Distribución subgrupo ---
distr_sub = {"2": {"civs": 0, "obras": 0, "total": 0}, "5": {"civs": 0, "obras": 0, "total": 0}}
for cid, m in civ_meta.items():
    sg = m["subgrupo"]
    distr_sub[sg]["civs"] += 1
    distr_sub[sg]["obras"] += obras_aiu_por_civ[cid]
    distr_sub[sg]["total"] += total_civ[cid]

# --- Hallazgos ---
hallazgos = []

# H1: Verificación fila 688
sev = "INFO" if abs(verif_688["delta"]) <= 100 else ("MEDIA" if abs(verif_688["delta"]) < 1_000_000 else "ALTA")
hallazgos.append({
    "id": "H03-01",
    "severidad": sev,
    "titulo": "Suma de obras con AIU por CIV cuadra a fila 688",
    "descripcion": f"Suma de it.civ[cid].valor (excluye ACEROS) = ${verif_688['calculado']:,.0f}. Esperado (fila 688 col M) = ${TOTAL_OBRAS_ESPERADO:,.0f}. Δ = ${verif_688['delta']:,.0f}",
    "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
    "fila": 688,
    "impacto_pesos": verif_688["delta"],
    "recomendacion": "Cuadre verificado; no requiere acción si Δ es residual (<$1.000). Si es mayor, revisar redondeos por CIV.",
})

# H2: Verificación total 75.426M
sev = "INFO" if abs(verif_total["delta"]) <= 100 else ("MEDIA" if abs(verif_total["delta"]) < 1_000_000 else "ALTA")
hallazgos.append({
    "id": "H03-02",
    "severidad": sev,
    "titulo": "Suma total con componentes cuadra a fila 703",
    "descripcion": f"Obras+componentes por CIV = ${verif_total['calculado']:,.0f}. Esperado = ${TOTAL_GENERAL_ESPERADO:,.0f}. Δ = ${verif_total['delta']:,.0f}",
    "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
    "fila": 703,
    "impacto_pesos": verif_total["delta"],
    "recomendacion": "Cuadre verificado si Δ residual. En caso contrario, revisar reparto de componentes.",
})

# H3: Outliers
for od in outliers_detalle[:5]:
    top_desc = "; ".join(f"[{it['chapter'].split('.')[0]}] {it['descripcion'][:60]} ${it['valor_aiu']:,.0f}" for it in od["explicacion_top_5_items"][:3])
    hallazgos.append({
        "id": f"H03-OUT-{od['id']}",
        "severidad": "ALTA" if od["dolarm2_obras"] > lim_sup * 1.2 else "MEDIA",
        "titulo": f"CIV {od['id']} ({od['nomenclatura']}) es outlier de $/m² con ${od['dolarm2_obras']:,.0f}/m²",
        "descripcion": f"$/m² = ${od['dolarm2_obras']:,.0f} ({od['veces_sobre_mediana']}× mediana ${med:,.0f}/m²). Obras con AIU = ${od['obras_aiu']:,.0f}. Top 3 renglones: {top_desc}",
        "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
        "fila": "múltiples",
        "impacto_pesos": od["obras_aiu"],
        "recomendacion": "Solicitar al contratista soporte técnico y de cantidades para renglones dominantes. Comparar con V1/V2 y verificar consistencia con memorias de cantidades.",
    })

# H4: NP muy alto en algún CIV
np_sorted = sorted(desglose_np_flat, key=lambda r: -r["pct_np"])
for r in np_sorted[:3]:
    if r["pct_np"] >= 40:
        hallazgos.append({
            "id": f"H03-NP-{r['id']}",
            "severidad": "MEDIA" if r["pct_np"] < 60 else "ALTA",
            "titulo": f"CIV {r['id']}: {r['pct_np']}% del valor viene de NPs",
            "descripcion": f"Contractual ${r['contractual_total']:,.0f} + NP ${r['np_total']:,.0f} = obras totales. Alta dependencia de precios no pactados.",
            "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
            "fila": "múltiples",
            "impacto_pesos": r["np_total"],
            "recomendacion": "Auditar NPs asignados a este CIV, verificar códigos IDU, análisis de precios unitarios y actas de fijación.",
        })

# --- Escribir JSON ---
out = {
    "meta": {
        "fuente_hoja_principal": "PRESUPUESTO TODOS LOS CIV 84 NP",
        "fuente_json_canonico": "analisis/datos/presupuesto_2026_09.json",
        "aiu_factor": AIU,
        "fecha_analisis": "2026-09-26",
    },
    "criterio_reparto": {
        "criterio": "Proporcional al costo directo de obras por CIV (V4, hoja principal, excluyendo bloque ACEROS filas 682-687).",
        "formula": "componentes_civ = 17.229.641.399 × (obras_cd_civ / Σ obras_cd_civ)",
        "notas": [
            "Se descartó reparto proporcional al área porque las áreas de data.json difieren entre subgrupos y no reflejan intensidad real de obra (redes, señalización).",
            "El costo directo es más representativo que el AIU porque el AIU es proporcional (mismo factor 31,849%) y no aporta información adicional al reparto.",
            "Componentes fijos que no dependen del CIV (Ajustes vigencia $4.555M, Actividades acero $2.977M, SDA, ensayos, etc.) se reparten con el mismo criterio; una vez seleccionado se aplica homogéneo a los 10 conceptos.",
            "Alternativa evaluada: reparto por área. Se documenta en `dolarm2_total` para trazabilidad, pero no se usa como base."
        ],
    },
    "verificacion_688": verif_688,
    "verificacion_total": verif_total,
    "verificacion_componentes": verif_componentes,
    "costo_por_civ": costo_por_civ,
    "desglose_por_capitulo_civ": desglose_cap_civ_flat,
    "desglose_np_vs_contractual": desglose_np_flat,
    "redes_vs_sin_redes": redes_flat,
    "comparativa_v1_v2_v4": comparativa_v1_v2_v4,
    "grupos_hoja1": grupos_hoja1,
    "estadistica_dolarm2": {
        "obras": est_obras,
        "total": est_total,
        "subgrupo_2_obras": est_sub2,
        "subgrupo_5_obras": est_sub5,
        "limite_outlier_sup": round(lim_sup),
        "limite_outlier_inf": round(lim_inf),
        "iqr": round(iqr),
    },
    "outliers": outliers_detalle,
    "distribucion_subgrupo": {
        "sg2": {"civs": distr_sub["2"]["civs"], "obras_aiu": round(distr_sub["2"]["obras"]), "total": round(distr_sub["2"]["total"])},
        "sg5": {"civs": distr_sub["5"]["civs"], "obras_aiu": round(distr_sub["5"]["obras"]), "total": round(distr_sub["5"]["total"])},
    },
    "hallazgos": hallazgos,
}

OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)

# --- Escribir Markdown ---
def fmt_cop(n):
    if n is None:
        return "-"
    try:
        return f"${int(round(n)):,}".replace(",", ".")
    except Exception:
        return str(n)

def fmt_pct(n, d=2):
    if n is None:
        return "-"
    return f"{n:.{d}f}%"

lines = []
lines.append("# 03 · Costo por CIV — Obras + componentes → $75.426.575.199")
lines.append("")
lines.append("**Fuente principal**: `PRESUPUESTO TODOS LOS CIV 84 NP` (V4 01-09-2026) vía `analisis/datos/presupuesto_2026_09.json`.")
lines.append(f"**AIU**: 31,849%. **Componentes no-obra**: {fmt_cop(TOTAL_COMPONENTES)}. **Total esperado**: {fmt_cop(TOTAL_GENERAL_ESPERADO)}.")
lines.append("")

lines.append("## Verificaciones globales")
lines.append("")
lines.append("| Concepto | Calculado | Esperado | Δ |")
lines.append("|---|---:|---:|---:|")
lines.append(f"| Obras con AIU (fila 688) | {fmt_cop(verif_688['calculado'])} | {fmt_cop(TOTAL_OBRAS_ESPERADO)} | {fmt_cop(verif_688['delta'])} |")
lines.append(f"| Total obras+componentes (fila 703) | {fmt_cop(verif_total['calculado'])} | {fmt_cop(TOTAL_GENERAL_ESPERADO)} | {fmt_cop(verif_total['delta'])} |")
lines.append(f"| Suma de los 10 componentes | {fmt_cop(TOTAL_COMPONENTES)} | {fmt_cop(17229641399)} | {fmt_cop(verif_componentes['delta'])} |")
lines.append("")

lines.append("## Criterio de reparto de componentes")
lines.append("")
lines.append(f"- **Base**: proporcional al costo directo de obras (V4) por CIV. Σ CD obras = {fmt_cop(round(denom_reparto))}.")
lines.append(f"- **Fórmula**: `componentes_civ = 17.229.641.399 × (obras_cd_civ / Σ obras_cd_civ)`.")
lines.append(f"- **Razón**: el CD refleja intensidad de obra real (redes, señalización, cantidades). El AIU es proporcional (mismo factor 31,849%) y no aporta información al reparto. El área lineal no representa peso de las 30 partidas contractuales ni de los NPs, por lo cual se descarta.")
lines.append("")

lines.append("## Distribución por subgrupo")
lines.append("")
lines.append("| Subgrupo | # CIVs | Obras con AIU | Total (con componentes) |")
lines.append("|---|---:|---:|---:|")
lines.append(f"| SG2 (Puente Aranda) | {distr_sub['2']['civs']} | {fmt_cop(distr_sub['2']['obras'])} | {fmt_cop(distr_sub['2']['total'])} |")
lines.append(f"| SG5 (Montevideo) | {distr_sub['5']['civs']} | {fmt_cop(distr_sub['5']['obras'])} | {fmt_cop(distr_sub['5']['total'])} |")
lines.append(f"| **Total** | **{distr_sub['2']['civs']+distr_sub['5']['civs']}** | **{fmt_cop(distr_sub['2']['obras']+distr_sub['5']['obras'])}** | **{fmt_cop(distr_sub['2']['total']+distr_sub['5']['total'])}** |")
lines.append("")

lines.append("## Costo por CIV")
lines.append("")
lines.append("| CIV | Nom. | SG | Área m² | Obras CD | AIU | Obras total | Componentes | Total | $/m² obras | $/m² total | %NP |")
lines.append("|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
# Ordenar por obras_total desc
costo_por_civ_sorted = sorted(costo_por_civ, key=lambda r: -r["obras_total"])
for r in costo_por_civ_sorted:
    lines.append(
        f"| {r['id']} | {r.get('nomenclatura') or '-'} | {r['subgrupo']} | "
        f"{r.get('area_m2') or '-'} | {fmt_cop(r['obras_cd'])} | {fmt_cop(r['obras_aiu'])} | "
        f"{fmt_cop(r['obras_total'])} | {fmt_cop(r['componentes_asignados'])} | {fmt_cop(r['total'])} | "
        f"{fmt_cop(r['dolarm2_obras'])} | {fmt_cop(r['dolarm2_total'])} | {r['pct_np_en_obras']}% |"
    )
lines.append("")

lines.append("## Estadística $/m² (obras con AIU)")
lines.append("")
lines.append("| Segmento | Media | Mediana | P25 | P75 | Min | Max | Std |")
lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
for label, s in [("Global", est_obras), ("Subgrupo 2", est_sub2), ("Subgrupo 5", est_sub5)]:
    lines.append(f"| {label} | {fmt_cop(s['media'])} | {fmt_cop(s['mediana'])} | {fmt_cop(s['p25'])} | {fmt_cop(s['p75'])} | {fmt_cop(s['min'])} | {fmt_cop(s['max'])} | {fmt_cop(s['std'])} |")
lines.append("")
lines.append(f"**Límites outlier**: superior {fmt_cop(lim_sup)}, inferior {fmt_cop(lim_inf)} (mediana ± 1,5·IQR = ±{fmt_cop(1.5*iqr)}).")
lines.append("")

lines.append("## Outliers")
lines.append("")
if not outliers_detalle:
    lines.append("Ningún CIV supera mediana ± 1,5·IQR.")
else:
    for od in outliers_detalle:
        lines.append(f"### CIV {od['id']} ({od['nomenclatura']}) — {fmt_cop(od['dolarm2_obras'])}/m² ({od['veces_sobre_mediana']}× mediana)")
        lines.append(f"- Subgrupo {od['subgrupo']} · Área {od['area_m2']} m² · Obras con AIU {fmt_cop(od['obras_aiu'])}")
        lines.append("- Top 5 renglones que inflan el $/m²:")
        for it in od["explicacion_top_5_items"]:
            np_tag = " [NP]" if it["is_np"] else ""
            lines.append(f"  - Fila {it['row']} · ítem {it['item_pago']}{np_tag} · {it['chapter']} · {it['descripcion']} · cant {it['cantidad']} {it['und']} · **{fmt_cop(it['valor_aiu'])}**")
        lines.append("")

lines.append("## Comparativa V1 (IDU 25-02-2026) vs V2 (VICON 21-04-2026) vs V4 (01-09-2026)")
lines.append("")
lines.append("| CIV | V1 total | V2 total | V4 obras AIU | Δ V4−V1 | %V4/V1 | Δ V4−V2 | %V4/V2 |")
lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
for r in comparativa_v1_v2_v4:
    lines.append(
        f"| {r['id']} | {fmt_cop(r['v1_total'])} | {fmt_cop(r['v2_total'])} | {fmt_cop(r['v4_obras_aiu'])} | "
        f"{fmt_cop(r['delta_v4_v1'])} | {fmt_pct(r['delta_v4_v1_pct'])} | "
        f"{fmt_cop(r['delta_v4_v2'])} | {fmt_pct(r['delta_v4_v2_pct'])} |"
    )
lines.append("")
lines.append("Nota: en `civs_cont` el CIV `16004876 (50002375)` se normaliza a `500002375` en V4 (mismo segmento 91029906).")
lines.append("")

lines.append("## Grupos alcance (Hoja1 / alcance_alt2)")
lines.append("")
lines.append("| Grupo | # CIVs | Obras con AIU | Componentes | Total | Referencia BRIEF |")
lines.append("|---|---:|---:|---:|---:|---:|")
ref_val = {"ya_iniciados": 19_652_000_000, "por_iniciar": 19_034_000_000, "no_alcanza": 19_511_000_000}
for gname, g in grupos_hoja1.items():
    lines.append(f"| {gname} | {g['cantidad_civs']} | {fmt_cop(g['obras_total'])} | {fmt_cop(g['componentes_total'])} | {fmt_cop(g['total'])} | ~{fmt_cop(ref_val.get(gname))} |")
lines.append("")

lines.append("## Redes vs sin redes por CIV")
lines.append("")
lines.append("| CIV | Redes (cap 5+6) | Sin redes (1-4+7) | %redes |")
lines.append("|---|---:|---:|---:|")
for r in sorted(redes_flat, key=lambda x: -x["pct_redes"]):
    lines.append(f"| {r['id']} | {fmt_cop(r['redes_total'])} | {fmt_cop(r['sin_redes_total'])} | {r['pct_redes']}% |")
lines.append("")

lines.append("## NP vs Contractual por CIV")
lines.append("")
lines.append("| CIV | Contractual | NP | %NP |")
lines.append("|---|---:|---:|---:|")
for r in sorted(desglose_np_flat, key=lambda x: -x["pct_np"]):
    lines.append(f"| {r['id']} | {fmt_cop(r['contractual_total'])} | {fmt_cop(r['np_total'])} | {r['pct_np']}% |")
lines.append("")

lines.append("## Hallazgos y recomendaciones")
lines.append("")
for h in hallazgos:
    lines.append(f"### {h['id']} · [{h['severidad']}] {h['titulo']}")
    lines.append(f"- Descripción: {h['descripcion']}")
    lines.append(f"- Fuente: {h['hoja']} fila {h['fila']}")
    lines.append(f"- Impacto: {fmt_cop(h['impacto_pesos'])}")
    lines.append(f"- Recomendación: {h['recomendacion']}")
    lines.append("")

OUT_MD.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# --- Report final ---
print("=== VERIFICACIONES ===")
print(f"[{'OK' if abs(verif_688['delta']) < 100 else 'OFF'}] Fila 688: calc={verif_688['calculado']:,} esperado={TOTAL_OBRAS_ESPERADO:,} Δ={verif_688['delta']:,}")
print(f"[{'OK' if abs(verif_total['delta']) < 100 else 'OFF'}] Total 703: calc={verif_total['calculado']:,} esperado={TOTAL_GENERAL_ESPERADO:,} Δ={verif_total['delta']:,}")

print()
print("=== TOP 5 OUTLIERS $/m² ===")
for od in outliers_detalle[:5]:
    print(f"  {od['id']} ({od['nomenclatura']}): ${od['dolarm2_obras']:,}/m² = {od['veces_sobre_mediana']}× mediana")

print()
print("=== DISTRIBUCION SUBGRUPO ===")
for sg in ["2", "5"]:
    d = distr_sub[sg]
    print(f"  SG{sg}: {d['civs']} CIVs · obras ${d['obras']:,.0f} · total ${d['total']:,.0f}")

print()
print(f"Escrito: {OUT_MD}")
print(f"Escrito: {OUT_JSON}")
