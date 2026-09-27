"""
Analisis 02 - Variacion de cantidades por CIV.

Genera:
  analisis/hallazgos/02_variacion_civ.md
  analisis/hallazgos/02_variacion_civ.json

Reglas:
- Todo numero sale de codigo.
- Fuente principal: analisis/datos/presupuesto_2026_09.json (V4 - hoja principal).
- Linea base inicial por CIV: se toma de data.json (items[*].cantidades), mapeando por codigo_idu.
- Trampas de mapeo: CIV 500002375 (V4) = 50002375 (MEMORIA) = 16004876 (data.json/comparativa) = 16004876 (Hoja1).
"""
import csv
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRES = ROOT / "analisis" / "datos" / "presupuesto_2026_09.json"
DATA = ROOT / "data.json"
COMP = ROOT / "comparativa.json"
HOJAS = ROOT / "analisis" / "datos" / "hojas"
OUT_MD = ROOT / "analisis" / "hallazgos" / "02_variacion_civ.md"
OUT_JSON = ROOT / "analisis" / "hallazgos" / "02_variacion_civ.json"

# Normalizador: en V4 el CIV se llama 500002375 pero en data.json / comparativa.json
# a veces aparece como 16004876 (con o sin sufijo). Este par se refiere al mismo tramo
# KR65 CL17-CL18 en zona Puente Aranda.
#
# El id canonico usado en presupuesto V4 y en toda la app es 500002375.

def norm_civ(cid):
    """Devuelve el id canonico usado en presupuesto V4."""
    s = str(cid).strip()
    if s.startswith("16004876"):
        return "500002375"
    if s == "50002375":
        return "500002375"
    return s

def load_data_civ_area():
    """Devuelve dict id_v4 -> {area, longitud, ancho, nomenclatura, subgrupo}."""
    d = json.load(open(DATA, encoding="utf-8"))
    r = {}
    for c in d["civs"]:
        id_v4 = norm_civ(c["id"])
        r[id_v4] = {
            "id_data": c["id"],
            "nomenclatura": c.get("nomenclatura"),
            "desde_hasta": c.get("desde_hasta"),
            "area": c.get("area") or 0,
            "longitud": c.get("longitud") or 0,
            "ancho": c.get("ancho") or 0,
            "subgrupo": c.get("subgrupo"),
        }
    return r, d

def load_v4():
    return json.load(open(PRES, encoding="utf-8"))

def load_data_json():
    return json.load(open(DATA, encoding="utf-8"))

def load_comparativa():
    return json.load(open(COMP, encoding="utf-8"))

def load_memoria_civs():
    """Extrae de MEMORIA CANTIDADES los CIVs listados. Devuelve set de ids."""
    ids = set()
    p = HOJAS / "MEMORIA_CANTIDADES.csv"
    if not p.exists():
        return ids
    with open(p, encoding="utf-8") as f:
        for row in csv.reader(f):
            for cell in row:
                s = str(cell).strip()
                if s.isdigit() and (s.startswith("16") or s.startswith("9") or s.startswith("50")):
                    if len(s) in (7, 8):
                        ids.add(s)
    return ids

def main():
    v4 = load_v4()
    civs_area, data_full = load_data_civ_area()
    comp = load_comparativa()
    memoria_civs = load_memoria_civs()

    civ_ids_v4 = [c["id"] for c in v4["civs"]]

    # ---- 1. MAPEO DE CIVS ----
    civs_cont_map = {norm_civ(c["id"]): c for c in comp.get("civs_cont", [])}
    civs_idu_map = {norm_civ(c["id"]): c for c in comp.get("civs_idu", [])}

    mapeo_civs = []
    for cid in civ_ids_v4:
        cn = norm_civ(cid)
        area = civs_area.get(cn, {})
        mapeo_civs.append({
            "id_v4": cid,
            "id_data": area.get("id_data"),
            "id_comparativa_cont": civs_cont_map.get(cn, {}).get("id"),
            "id_comparativa_idu": civs_idu_map.get(cn, {}).get("id"),
            "id_memoria_probable": "50002375" if cid == "500002375" else cid,
            "nomenclatura": area.get("nomenclatura"),
            "desde_hasta": area.get("desde_hasta"),
            "area_m2": area.get("area"),
            "longitud_m": area.get("longitud"),
            "subgrupo": area.get("subgrupo"),
            "notas": ("Tramo compartido con 16000047 (segmento 91029906)" if cid == "500002375" else None),
        })

    # ---- 2. LINEA BASE INICIAL POR CIV (data.json) ----
    # Recorremos data.json y agrupamos por codigo_idu. La cantidad_por_civ del ítem
    # inicial la tomamos tal cual de data.json.cantidades.
    data_items_by_code = {}
    for it in data_full["items"]:
        if it.get("type") != "item":
            continue
        code = str(it.get("codigo_idu") or "").strip()
        if not code:
            continue
        # Cada ítem en data.json es único por (codigo_idu, item_pago). Guardamos
        # con codigo_idu como llave; si hay varios, acumulamos.
        entry = data_items_by_code.setdefault(code, [])
        entry.append(it)

    def cant_ini_civ(codigo_idu, cid_v4, num_filas_v4=1):
        """Cantidad inicial (V0) para (codigo_idu, cid) desde data.json, prorrateando
        entre las N filas de V4 que tienen ese mismo codigo_idu (evita doble conteo
        cuando el codigo se repite en varios subcapitulos)."""
        if not codigo_idu:
            return 0.0
        cid_data = "16004876" if cid_v4 == "500002375" else cid_v4
        items = data_items_by_code.get(str(codigo_idu).strip(), [])
        s = 0.0
        for it in items:
            q = it.get("cantidades", {}).get(cid_data)
            if q:
                try:
                    s += float(q)
                except (ValueError, TypeError):
                    pass
        # Prorrateo: si el codigo aparece N veces en V4 (num_filas_v4), cada fila V4
        # se lleva 1/N de la cantidad inicial total (evita multiplicar por N).
        return s / max(num_filas_v4, 1)

    # ---- 3. MATRIZ ITEM x CIV con INICIAL, FINAL, DELTA ----
    matriz = []
    resumen_por_civ = {cid: {
        "id": cid,
        "obras_iniciales_cd": 0.0,
        "obras_iniciales_aiu": 0.0,
        "obras_finales_cd": 0.0,
        "obras_finales_aiu": 0.0,
    } for cid in civ_ids_v4}

    descomp = {cid: {
        "id": cid,
        "delta_por_aumentos": 0.0,
        "delta_por_disminuciones": 0.0,
        "delta_por_np": 0.0,
        "delta_por_contractual_nuevo": 0.0,
        "delta_por_eliminado": 0.0,
        "delta_por_capitulo": {},
    } for cid in civ_ids_v4}

    AIU_FACTOR = 1.31849

    # Contar cuantas veces aparece cada codigo_idu no-NP en V4 (para prorratear la
    # cantidad inicial data.json entre esas filas)
    codigo_filas_v4 = {}
    for it in v4["items"]:
        if it.get("chapter") == "8. ACTIVIDADES ACERO":
            continue
        if it.get("is_np"):
            continue
        code = str(it.get("codigo_idu") or "").strip()
        if code:
            codigo_filas_v4[code] = codigo_filas_v4.get(code, 0) + 1

    for it in v4["items"]:
        if it.get("chapter") == "8. ACTIVIDADES ACERO":
            continue
        code = str(it.get("codigo_idu") or "").strip()
        K = it.get("vu_cd") or 0
        L = it.get("vu_cd_aiu") or 0
        is_np = it.get("is_np")
        chapter = it.get("chapter") or ""
        celdas = []
        n_filas = codigo_filas_v4.get(code, 1)
        for cid in civ_ids_v4:
            v = it["civ"].get(cid, {})
            q_fin = v.get("cant") or 0
            v_aiu = v.get("valor") or 0
            v_cd = round(v_aiu / AIU_FACTOR) if v_aiu else 0
            q_ini = cant_ini_civ(code, cid, n_filas) if not is_np else 0.0
            dq = q_fin - q_ini
            dv_cd = dq * K
            dv_aiu = dq * L if L else round(dv_cd * AIU_FACTOR)
            v_ini_aiu = q_ini * L if L else round(q_ini * K * AIU_FACTOR)
            v_ini_cd = q_ini * K
            # acumulados
            resumen_por_civ[cid]["obras_finales_cd"] += v_cd
            resumen_por_civ[cid]["obras_finales_aiu"] += v_aiu
            if not is_np:
                resumen_por_civ[cid]["obras_iniciales_cd"] += v_ini_cd
                resumen_por_civ[cid]["obras_iniciales_aiu"] += v_ini_aiu
            # descomposicion
            if is_np:
                descomp[cid]["delta_por_np"] += v_aiu
            elif q_ini == 0 and q_fin > 0:
                descomp[cid]["delta_por_contractual_nuevo"] += v_aiu
            elif q_ini > 0 and q_fin == 0:
                descomp[cid]["delta_por_eliminado"] -= v_ini_aiu
            elif q_fin > q_ini:
                descomp[cid]["delta_por_aumentos"] += (q_fin - q_ini) * (L or 0)
            elif q_fin < q_ini:
                descomp[cid]["delta_por_disminuciones"] += (q_fin - q_ini) * (L or 0)
            ch_key = chapter.split(".")[0] if chapter else "?"
            descomp[cid]["delta_por_capitulo"][ch_key] = descomp[cid]["delta_por_capitulo"].get(ch_key, 0.0) + (v_aiu - v_ini_aiu)
            if q_ini or q_fin:
                celdas.append({
                    "id_civ": cid,
                    "cant_ini": q_ini,
                    "cant_fin": q_fin,
                    "delta_cant": dq,
                    "delta_valor_cd": dv_cd,
                    "delta_valor_aiu": v_aiu - v_ini_aiu,
                })
        if celdas:
            matriz.append({
                "row": it["row"],
                "codigo_idu": code,
                "item_pago": it.get("item_pago"),
                "descripcion": it.get("descripcion"),
                "chapter": chapter,
                "und": it.get("und"),
                "K": K,
                "L": L,
                "is_np": is_np,
                "celdas": celdas,
            })

    # Redondear resumen_por_civ y descomp
    for cid, r in resumen_por_civ.items():
        r["obras_iniciales_cd"] = round(r["obras_iniciales_cd"])
        r["obras_iniciales_aiu"] = round(r["obras_iniciales_aiu"])
        r["obras_finales_cd"] = round(r["obras_finales_cd"])
        r["obras_finales_aiu"] = round(r["obras_finales_aiu"])
        r["delta_cd"] = r["obras_finales_cd"] - r["obras_iniciales_cd"]
        r["delta_aiu"] = r["obras_finales_aiu"] - r["obras_iniciales_aiu"]
        r["delta_pct"] = ((r["delta_aiu"] / r["obras_iniciales_aiu"]) * 100) if r["obras_iniciales_aiu"] else None
        # nomenclatura
        area_info = civs_area.get(norm_civ(cid), {})
        r["nomenclatura"] = area_info.get("nomenclatura")
        r["desde_hasta"] = area_info.get("desde_hasta")
        r["area_m2"] = area_info.get("area")
        r["longitud_m"] = area_info.get("longitud")
        r["subgrupo"] = area_info.get("subgrupo")

    resumen_por_civ_lst = [resumen_por_civ[cid] for cid in civ_ids_v4]
    descomp_lst = []
    for cid in civ_ids_v4:
        rec = descomp[cid]
        # redondear
        for k in ["delta_por_aumentos", "delta_por_disminuciones", "delta_por_np",
                  "delta_por_contractual_nuevo", "delta_por_eliminado"]:
            rec[k] = round(rec[k])
        rec["delta_neto"] = (
            rec["delta_por_aumentos"] + rec["delta_por_disminuciones"] + rec["delta_por_np"]
            + rec["delta_por_contractual_nuevo"] + rec["delta_por_eliminado"]
        )
        rec["delta_por_capitulo"] = {k: round(v) for k, v in rec["delta_por_capitulo"].items()}
        descomp_lst.append(rec)

    # ---- 4. CONCILIACION LINEA BASE ----
    # Referencia canonica: col N del V4 (valor_inicial_aiu por renglon) = $44.303.294.799 global.
    # La suma por CIV reconstruida (cant_inicial_data_json * L_V4) puede diferir globalmente
    # porque (a) ítems eliminados en V4 desaparecen de la matriz por CIV, (b) items con codigo NP
    # no tienen linea base. Aqui documentamos ambas medidas.
    col_N_global = 0
    for it in v4["items"]:
        if it.get("chapter") == "8. ACTIVIDADES ACERO":
            continue
        col_N_global += it.get("valor_inicial_aiu") or 0

    conciliacion = []
    total_v4_ini = 0
    for cid in civ_ids_v4:
        v4_ini = resumen_por_civ[cid]["obras_iniciales_aiu"]
        total_v4_ini += v4_ini
        conciliacion.append({
            "civ": cid,
            "obras_iniciales_v4_reconstruidas_por_civ": v4_ini,
        })
    conciliacion_total = {
        "col_N_global_v4": round(col_N_global),
        "obras_v0_contractual_firma": 44303294799,
        "total_v4_reconstruidas_ini_por_civ": total_v4_ini,
        "delta_reconstruida_vs_col_N": round(total_v4_ini - col_N_global),
        "nota": ("La col N total del V4 (excluyendo ACEROS) es la referencia canonica de la linea base. "
                 "La suma por CIV reconstruida difiere porque los items ELIMINADOS en V4 (H>0 e I=0) "
                 "no se reparten por CIV en la matriz S:BW; a nivel global la col N ya los incluye. "
                 "La cifra a reportar en la app es la col N global ($44.303.294.799)."),
    }

    # ---- 5. METRICAS POR M2 y OUTLIERS ----
    # Ratios: rajon m3/m2, anden m2/m2, MD12 m2/m2, MD19 m2/m2, BG_A m3/m2
    KEYS = {
        "rajon_m3_por_m2": ("1005", "rajon"),
        "anden_m2_por_m2": ("3039", "anden"),
        "md12_m2_por_m2": ("2002", "md12"),
        "md19_m2_por_m2": ("NP-123", "md19"),
        "bg_a_m3_por_m2": ("1012", "bg_a"),
    }
    ratios_por_civ = []
    for cid in civ_ids_v4:
        area = civs_area.get(norm_civ(cid), {}).get("area", 0)
        row = {"id": cid, "area_m2": area, "ratios": {}}
        if not area:
            ratios_por_civ.append(row)
            continue
        # Buscar cantidad final por CIV para cada codigo
        for name, (code_or_np, _) in KEYS.items():
            tot = 0.0
            for it in v4["items"]:
                match = False
                if code_or_np.startswith("NP-"):
                    if str(it.get("item_pago") or "") == code_or_np:
                        match = True
                else:
                    if str(it.get("codigo_idu") or "") == code_or_np:
                        match = True
                if match:
                    q = it["civ"].get(cid, {}).get("cant") or 0
                    tot += float(q)
            row["ratios"][name] = round(tot / area, 4) if area else None
        ratios_por_civ.append(row)

    # Outliers por metrica (mediana y >2x mediana)
    outliers = []
    for name in KEYS:
        vals = [r["ratios"][name] for r in ratios_por_civ if r["ratios"].get(name) is not None and r["ratios"][name] > 0]
        if not vals:
            continue
        med = statistics.median(vals)
        if med == 0:
            continue
        for r in ratios_por_civ:
            v = r["ratios"].get(name)
            if v and v > 2 * med:
                outliers.append({
                    "id": r["id"],
                    "ratio_metric": name,
                    "valor": v,
                    "veces_sobre_mediana": round(v / med, 2),
                })

    outliers.sort(key=lambda x: -x["veces_sobre_mediana"])

    # ---- 6. HALLAZGOS ----
    hallazgos = []
    # H1 Conciliacion línea base
    delta_recon = conciliacion_total["delta_reconstruida_vs_col_N"]
    hallazgos.append({
        "id": "H02-001",
        "severidad": "MEDIA",
        "titulo": "Reparto de la linea base por CIV no publicado por el contratista",
        "descripcion": (
            f"La col N del Excel suma ${conciliacion_total['col_N_global_v4']:,} de valor inicial con AIU global. "
            f"La reconstruccion por CIV (multiplicando cantidad_inicial_data_json * VU actualizado L) suma "
            f"${conciliacion_total['total_v4_reconstruidas_ini_por_civ']:,} (delta ${delta_recon:,}). "
            f"El Excel no reparte la cantidad contractual (col H) por CIV, por lo que la linea base por CIV "
            f"se estima con data.json (contrato firmado); es un pixel-perfect solo para los ítems que "
            f"mantuvieron el codigo_idu."
        ),
        "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
        "fila": "col H (linea base) vs bloque S:BW (matriz por CIV)",
        "impacto_pesos": abs(delta_recon),
        "recomendacion": "Pedir al contratista el reparto oficial de la cantidad contractual por CIV (col H desagregada) para auditar al peso el Delta por CIV.",
    })

    # H2 Top CIVs con mayor Δ absoluto
    top_delta = sorted(resumen_por_civ_lst, key=lambda x: -abs(x["delta_aiu"]))[:5]
    for i, c in enumerate(top_delta, 1):
        hallazgos.append({
            "id": f"H02-{100+i:03d}",
            "severidad": "ALTA" if abs(c["delta_aiu"]) > 500_000_000 else "MEDIA",
            "titulo": f"CIV {c['id']} ({c['nomenclatura']}) con Δ obras ${c['delta_aiu']:,}",
            "descripcion": f"Obras iniciales ${c['obras_iniciales_aiu']:,} -> finales ${c['obras_finales_aiu']:,}. Delta = ${c['delta_aiu']:,} ({(c['delta_pct'] or 0):.1f}%).",
            "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
            "fila": "columnas del CIV",
            "impacto_pesos": c["delta_aiu"],
            "recomendacion": "Solicitar justificacion tecnica del Δ por CIV con documentacion de campo y tramites IDU.",
        })

    # H3 Outliers
    for o in outliers[:5]:
        hallazgos.append({
            "id": f"H02-{200+outliers.index(o):03d}",
            "severidad": "MEDIA",
            "titulo": f"CIV {o['id']} outlier en {o['ratio_metric']} ({o['veces_sobre_mediana']}x mediana)",
            "descripcion": f"Ratio {o['ratio_metric']} = {o['valor']:.4f}, {o['veces_sobre_mediana']}x sobre la mediana de los 27 CIVs.",
            "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
            "fila": "columnas del CIV",
            "impacto_pesos": 0,
            "recomendacion": "Verificar en campo si la cantidad final del renglon corresponde al tramo real.",
        })

    # H4 CIV 500002375
    hallazgos.append({
        "id": "H02-300",
        "severidad": "INFO",
        "titulo": "Mapeo especial CIV 500002375 = 16004876 = 50002375",
        "descripcion": "El CIV V4 500002375 corresponde al tramo KR65 CL17-CL18 y se llama 16004876 en data.json, 16004876 en Hoja1 y 50002375 en MEMORIA CANTIDADES. Comparte segmento 91029906 con el CIV 16000047.",
        "hoja": "hoja principal + MEMORIA CANTIDADES + Hoja1",
        "fila": "fila 3 IDs",
        "impacto_pesos": 0,
        "recomendacion": "Unificar la nomenclatura en documentos futuros (usar siempre el 500002375 IDU actual).",
    })

    # ---- 7. TOP 20 renglones por Δ por CIV (para app) ----
    top_delta_ciV = []
    for m in matriz:
        for c in m["celdas"]:
            if abs(c["delta_valor_aiu"]) < 100_000_000:
                continue
            top_delta_ciV.append({
                "row": m["row"],
                "codigo_idu": m["codigo_idu"],
                "item_pago": m["item_pago"],
                "descripcion": (m["descripcion"] or "")[:80],
                "chapter": m["chapter"],
                "id_civ": c["id_civ"],
                "cant_ini": c["cant_ini"],
                "cant_fin": c["cant_fin"],
                "delta_cant": c["delta_cant"],
                "delta_valor_aiu": c["delta_valor_aiu"],
            })
    top_delta_ciV.sort(key=lambda x: -abs(x["delta_valor_aiu"]))
    top_delta_ciV_50 = top_delta_ciV[:50]

    # ---- ESCRITURA ----
    out = {
        "meta": {
            "fuente": "presupuesto_2026_09.json + data.json + comparativa.json",
            "unidad_valor": "pesos con AIU (1.31849)",
            "nota_linea_base": "La cantidad inicial por CIV se reconstruye desde data.json[items[*].cantidades] mapeando por codigo_idu; los renglones NP no tienen linea base.",
            "aliases_civ": {"500002375": "16004876/50002375 (KR65 CL17-CL18)"},
        },
        "mapeo_civs": mapeo_civs,
        "conciliacion_linea_base": conciliacion,
        "conciliacion_total": conciliacion_total,
        "resumen_por_civ": resumen_por_civ_lst,
        "descomposicion_delta_civ": descomp_lst,
        "matriz_item_civ": matriz,
        "metricas_por_m2": ratios_por_civ,
        "outliers_por_civ": outliers,
        "top_delta_por_celda": top_delta_ciV_50,
        "hallazgos": hallazgos,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    print(f"JSON escrito: {OUT_JSON}")

    # ---- MD ----
    def fmt(n):
        try:
            return f"{int(n):,}".replace(",", ".")
        except (ValueError, TypeError):
            return str(n)

    md = []
    md.append("# 02 - Variacion de cantidades por CIV")
    md.append("")
    md.append("## Resumen ejecutivo")
    md.append("")
    md.append(f"- 27 CIVs analizados (mapeo especial 500002375 -> 16004876).")
    md.append(f"- Obras iniciales globales (col N Excel): ${fmt(conciliacion_total['col_N_global_v4'])}")
    md.append(f"- Contrato firmado (obras+AIU V0): ${fmt(conciliacion_total['obras_v0_contractual_firma'])}")
    md.append(f"- Reconstruccion por CIV (cant_data * L_v4): ${fmt(conciliacion_total['total_v4_reconstruidas_ini_por_civ'])}")
    md.append(f"- Delta reconstruccion vs col N: ${fmt(conciliacion_total['delta_reconstruida_vs_col_N'])}")
    md.append(f"- Obras finales V4 (col M): ${fmt(sum(r['obras_finales_aiu'] for r in resumen_por_civ_lst))}")
    md.append("")

    md.append("## Mapeo de CIVs")
    md.append("| id_v4 | id_data | id_cont | id_memoria | nomenclatura | desde_hasta | area_m2 | notas |")
    md.append("|---|---|---|---|---|---|---:|---|")
    for m in mapeo_civs:
        md.append(f"| {m['id_v4']} | {m['id_data']} | {m['id_comparativa_cont']} | {m['id_memoria_probable']} | {m['nomenclatura']} | {m['desde_hasta']} | {fmt(m['area_m2'] or 0)} | {m['notas'] or '-'} |")
    md.append("")

    md.append("## Resumen por CIV (obras con AIU)")
    md.append("| CIV | Nomenclatura | Area m2 | Iniciales | Finales V4 | Delta | Delta % |")
    md.append("|---|---|---:|---:|---:|---:|---:|")
    for r in resumen_por_civ_lst:
        dp = f"{r['delta_pct']:.1f}%" if r['delta_pct'] is not None else "-"
        md.append(f"| {r['id']} | {r['nomenclatura']} | {fmt(r['area_m2'])} | ${fmt(r['obras_iniciales_aiu'])} | ${fmt(r['obras_finales_aiu'])} | ${fmt(r['delta_aiu'])} | {dp} |")
    md.append("")

    md.append("## Descomposicion del Δ por CIV")
    md.append("| CIV | Δ Aumentos | Δ Disminuciones | Δ NP | Δ Contractual nuevo | Δ Eliminado | Δ Neto |")
    md.append("|---|---:|---:|---:|---:|---:|---:|")
    for d in descomp_lst:
        md.append(f"| {d['id']} | ${fmt(d['delta_por_aumentos'])} | ${fmt(d['delta_por_disminuciones'])} | ${fmt(d['delta_por_np'])} | ${fmt(d['delta_por_contractual_nuevo'])} | ${fmt(d['delta_por_eliminado'])} | ${fmt(d['delta_neto'])} |")
    md.append("")

    md.append("## Outliers de cantidad por m2")
    md.append("| CIV | Metrica | Valor | Veces sobre mediana |")
    md.append("|---|---|---:|---:|")
    for o in outliers[:20]:
        md.append(f"| {o['id']} | {o['ratio_metric']} | {o['valor']} | {o['veces_sobre_mediana']}x |")
    md.append("")

    md.append("## Top 30 celdas (item x CIV) con mayor Δ absoluto")
    md.append("| Row | Codigo | Item | CIV | Cant ini | Cant fin | Δ Cant | Δ Valor AIU |")
    md.append("|---:|---|---|---|---:|---:|---:|---:|")
    for t in top_delta_ciV[:30]:
        md.append(f"| {t['row']} | {t['codigo_idu']} | {t['item_pago']} | {t['id_civ']} | {t['cant_ini']:.2f} | {t['cant_fin']:.2f} | {t['delta_cant']:.2f} | ${fmt(t['delta_valor_aiu'])} |")
    md.append("")

    md.append("## Hallazgos")
    for h in hallazgos:
        md.append(f"### {h['id']} - [{h['severidad']}] {h['titulo']}")
        md.append(f"- **Fuente**: {h['hoja']} · {h['fila']}")
        md.append(f"- **Impacto**: ${fmt(h['impacto_pesos'])}")
        md.append(f"- **Descripcion**: {h['descripcion']}")
        md.append(f"- **Recomendacion**: {h['recomendacion']}")
        md.append("")

    md.append("## Metodologia")
    md.append("- Fuente V4: analisis/datos/presupuesto_2026_09.json (matriz ítem x CIV con AIU).")
    md.append("- Fuente V0 (linea base): data.json → items[*].cantidades. Los NPs no tienen linea base.")
    md.append("- El mapeo CIV 500002375 <-> 16004876 <-> 50002375 (KR65 CL17-CL18) se aplica en todas las tablas.")
    md.append("- AIU contractual = 1,31849. Los valores por celda del JSON estan con AIU; el CD se obtiene dividiendo.")
    md.append("- Los ratios por m2 usan el area de data.json[civs].")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"MD escrito: {OUT_MD}")

    # ---- RESUMEN DE CONSOLA ----
    print()
    print("=== RESUMEN ===")
    print(f"CIVs: {len(civ_ids_v4)}")
    print(f"Delta reconstruccion vs col N: ${fmt(conciliacion_total['delta_reconstruida_vs_col_N'])}")
    print("Top 3 CIVs con mayor Delta:")
    for c in top_delta[:3]:
        print(f"  {c['id']} ({c['nomenclatura']}) - Delta ${fmt(c['delta_aiu'])}")
    print(f"Top 3 outliers:")
    for o in outliers[:3]:
        print(f"  {o['id']} {o['ratio_metric']} {o['veces_sobre_mediana']}x")


if __name__ == "__main__":
    main()
