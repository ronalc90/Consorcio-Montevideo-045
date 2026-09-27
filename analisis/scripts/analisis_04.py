"""
Analisis 04 - Aritmetica, precios unitarios y formulas
Genera: analisis/hallazgos/04_aritmetica.md y analisis/hallazgos/04_aritmetica.json
"""
import csv
import json
import re
from pathlib import Path
from collections import defaultdict, Counter

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
XLSX = ROOT / "fuentes" / "4. PRESUPUESTO 01-09-2026 75MM (8 MESES).xlsx"
DATOS = ROOT / "analisis" / "datos"
HOJAS = DATOS / "hojas"
OUT_MD = ROOT / "analisis" / "hallazgos" / "04_aritmetica.md"
OUT_JSON = ROOT / "analisis" / "hallazgos" / "04_aritmetica.json"
HOJA_PPAL = "PRESUPUESTO TODOS LOS CIV 84 NP"

AIU = 0.31849
TOL = 1.0


def col_letter(idx0):
    """0-based column index to Excel letter."""
    n = idx0 + 1
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def num(v):
    if v is None or v == "":
        return None
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(str(v).replace(",", ""))
    except Exception:
        return None


def fmt_pesos(n):
    if n is None:
        return "-"
    n = round(n)
    s = f"{abs(int(n)):,}".replace(",", ".")
    return ("-" if n < 0 else "") + s


def load_csv(name):
    p = HOJAS / name
    if not p.exists():
        return []
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.reader(f))


def main():
    print("Cargando workbook con formulas y con valores...")
    wb_f = openpyxl.load_workbook(XLSX, data_only=False)
    wb_v = openpyxl.load_workbook(XLSX, data_only=True)
    ws_f = wb_f[HOJA_PPAL]
    ws_v = wb_v[HOJA_PPAL]

    max_row = ws_f.max_row
    max_col = ws_f.max_column
    print(f"Hoja principal: {max_row} filas x {max_col} columnas")

    # ==========================
    # 1) Formulas vs hardcoded
    # ==========================
    conteo_formulas = 0
    conteo_hardcoded = 0
    ejemplos_formulas = []
    celdas_error = []
    rangos_incompletos = []

    # Errores estandar Excel
    err_patterns = ["#REF!", "#DIV/0!", "#N/A", "#VALUE!", "#NAME?", "#NULL!", "#NUM!"]

    # Recorrer solo celdas con valor
    for row in ws_f.iter_rows(min_row=1, max_row=max_row, max_col=max_col):
        for cell in row:
            v = cell.value
            if v is None or v == "":
                continue
            if isinstance(v, str) and v.startswith("="):
                conteo_formulas += 1
                if len(ejemplos_formulas) < 30:
                    ejemplos_formulas.append({"celda": cell.coordinate, "formula": v})
                # Rangos incompletos: buscar =SUM(X:Y) que no cubran hasta max_row de datos
                m = re.findall(r"([A-Z]+)(\d+):([A-Z]+)(\d+)", v)
                for c1, r1, c2, r2 in m:
                    r1i, r2i = int(r1), int(r2)
                    # Chequeo simple: si el rango termina antes de fila 679 y esta en total (fila 688+)
                    if cell.row >= 688 and r2i < 679:
                        rangos_incompletos.append({
                            "celda": cell.coordinate, "formula": v,
                            "filas_faltantes": f"rango termina en fila {r2i}, datos llegan hasta 679"
                        })
                        break
            else:
                if isinstance(v, str) and any(e in v for e in err_patterns):
                    celdas_error.append({"celda": cell.coordinate, "tipo": v.strip()})
                else:
                    conteo_hardcoded += 1

    # Errores tambien en valores
    for row in ws_v.iter_rows(min_row=1, max_row=max_row, max_col=max_col):
        for cell in row:
            v = cell.value
            if isinstance(v, str) and any(e in v for e in err_patterns):
                key = (cell.coordinate, v.strip())
                if not any(c["celda"] == cell.coordinate for c in celdas_error):
                    celdas_error.append({"celda": cell.coordinate, "tipo": v.strip()})

    print(f"Formulas: {conteo_formulas} | Hardcoded: {conteo_hardcoded} | Errores: {len(celdas_error)}")

    # =====================================
    # 2) Consistencia aritmetica por fila
    # =====================================
    # Columnas 1-based: H=8, I=9, J=10, K=11, L=12, M=13, N=14, O=15, P=16, Q=17
    # CB = columna 80 (total general por fila)
    desviaciones_aiu_L = []
    desviaciones_M_N_O_Q = []
    desviaciones_CB = []

    # Recorrer filas de items 7..679
    for r in range(7, 680):
        H = num(ws_v.cell(r, 8).value)
        I = num(ws_v.cell(r, 9).value)
        K = num(ws_v.cell(r, 11).value)
        L = num(ws_v.cell(r, 12).value)
        M = num(ws_v.cell(r, 13).value)
        N = num(ws_v.cell(r, 14).value)
        O = num(ws_v.cell(r, 15).value)
        P = num(ws_v.cell(r, 16).value)
        Q = num(ws_v.cell(r, 17).value)
        CB = num(ws_v.cell(r, 80).value)  # columna 80 = CB
        und = ws_v.cell(r, 7).value

        # Solo filas de items (con unidad)
        if und in (None, "") or not isinstance(und, str) or und.strip() == "":
            continue

        # L = redondeo(K * 1.31849)
        if K is not None and L is not None:
            esperado_L = round(K * (1 + AIU))
            if abs(L - esperado_L) > TOL:
                if len(desviaciones_aiu_L) < 100:
                    desviaciones_aiu_L.append({
                        "row": r, "K": K, "L": L,
                        "esperado_L": esperado_L, "delta": round(L - esperado_L, 2)
                    })

        # M = I * L
        if I is not None and L is not None and M is not None:
            esp = round(I * L)
            if abs(M - esp) > TOL:
                desviaciones_M_N_O_Q.append({
                    "row": r, "columna": "M", "actual": M, "esperado": esp,
                    "delta": round(M - esp, 2)
                })

        # N = H * L
        if H is not None and L is not None and N is not None:
            esp = round(H * L)
            if abs(N - esp) > TOL:
                desviaciones_M_N_O_Q.append({
                    "row": r, "columna": "N", "actual": N, "esperado": esp,
                    "delta": round(N - esp, 2)
                })

        # O = (I - H) * L
        if H is not None and I is not None and L is not None and O is not None:
            esp = round((I - H) * L)
            if abs(O - esp) > TOL:
                desviaciones_M_N_O_Q.append({
                    "row": r, "columna": "O", "actual": O, "esperado": esp,
                    "delta": round(O - esp, 2)
                })

        # Q = O + P
        if O is not None and P is not None and Q is not None:
            esp = round(O + P)
            if abs(Q - esp) > TOL:
                desviaciones_M_N_O_Q.append({
                    "row": r, "columna": "Q", "actual": Q, "esperado": esp,
                    "delta": round(Q - esp, 2)
                })

        # CB (columna 80) debe ser igual a M
        if CB is not None and M is not None:
            if abs(CB - M) > TOL:
                desviaciones_CB.append({
                    "row": r, "columna": "CB", "actual": CB, "esperado": M,
                    "delta": round(CB - M, 2)
                })

    print(f"Desviaciones L (AIU): {len(desviaciones_aiu_L)}")
    print(f"Desviaciones M/N/O/Q: {len(desviaciones_M_N_O_Q)}")
    print(f"Desviaciones CB vs M: {len(desviaciones_CB)}")

    # =====================================
    # 3) Consistencia entre hojas
    # =====================================
    consistencia_hojas = []
    # fila 688 principal
    obras_total_ppal = num(ws_v.cell(688, 13).value)  # M688
    total_final_ppal = num(ws_v.cell(703, 13).value)  # M703 (total general)

    # Buscar por texto en las filas 692-707
    componentes_ppal = {}
    for r in range(688, 710):
        etiqueta = ws_v.cell(r, 3).value or ws_v.cell(r, 6).value or ws_v.cell(r, 2).value
        val = num(ws_v.cell(r, 13).value)
        if etiqueta and val is not None:
            componentes_ppal[str(etiqueta).strip()] = {"row": r, "valor": val}

    # Hoja resumen
    try:
        ws_res = wb_v["resumen"]
        for r in range(1, ws_res.max_row + 1):
            for c in range(1, ws_res.max_column + 1):
                v = ws_res.cell(r, c).value
                if isinstance(v, str):
                    v_norm = v.strip().upper()
                    if "TOTAL" in v_norm and "PRESUPUESTO" in v_norm:
                        # buscar valor adyacente
                        for cc in range(c, min(c + 10, ws_res.max_column + 1)):
                            valn = num(ws_res.cell(r, cc).value)
                            if valn is not None and valn > 1e9:
                                # comparar con 75.426.575.199
                                esperado = 75_426_575_199
                                if abs(valn - esperado) > 100:
                                    consistencia_hojas.append({
                                        "hoja": "resumen",
                                        "celda": f"{col_letter(cc-1)}{r}",
                                        "valor": valn, "esperado": esperado,
                                        "delta": round(valn - esperado, 2)
                                    })
                                break
    except Exception as e:
        print(f"resumen: {e}")

    # Hoja Presupuesto estimado
    try:
        ws_est = wb_v["Presupuesto estimado"]
        for r in range(1, ws_est.max_row + 1):
            for c in range(1, ws_est.max_column + 1):
                v = ws_est.cell(r, c).value
                if isinstance(v, (int, float)) and 70e9 < v < 80e9:
                    # asumimos total del presupuesto
                    esperado = 75_426_575_199
                    if abs(v - esperado) > 100:
                        consistencia_hojas.append({
                            "hoja": "Presupuesto estimado",
                            "celda": f"{col_letter(c-1)}{r}",
                            "valor": v, "esperado": esperado,
                            "delta": round(v - esperado, 2)
                        })
    except Exception as e:
        print(f"Presupuesto estimado: {e}")

    # Hoja EJECUTIVO
    try:
        ws_ej = wb_v["EJECUTIVO"]
        # Buscar totales especificos
        for r in range(1, ws_ej.max_row + 1):
            for c in range(1, ws_ej.max_column + 1):
                v = ws_ej.cell(r, c).value
                if isinstance(v, (int, float)):
                    if 70e9 < v < 80e9:
                        esperado = 75_426_575_199
                        if abs(v - esperado) > 100:
                            consistencia_hojas.append({
                                "hoja": "EJECUTIVO",
                                "celda": f"{col_letter(c-1)}{r}",
                                "valor": v, "esperado": esperado,
                                "delta": round(v - esperado, 2)
                            })
                    elif 55e9 < v < 60e9:
                        # esperado obras 58.196.933.800
                        esperado_obras = 58_196_933_800
                        if abs(v - esperado_obras) > 100:
                            consistencia_hojas.append({
                                "hoja": "EJECUTIVO",
                                "celda": f"{col_letter(c-1)}{r}",
                                "valor": v, "esperado": esperado_obras,
                                "delta": round(v - esperado_obras, 2)
                            })
    except Exception as e:
        print(f"EJECUTIVO: {e}")

    # =====================================
    # 4) Duplicados por codigo_idu
    # =====================================
    duplicados = []
    codigo_rows = defaultdict(list)
    for r in range(7, 680):
        cod = ws_v.cell(r, 2).value
        und = ws_v.cell(r, 7).value
        if cod and und:
            codigo_rows[str(cod).strip()].append(r)

    for cod, rows in codigo_rows.items():
        if len(rows) > 1:
            # Determinar si son reubicacion (cantidades opuestas o distintos subcapitulos)
            H_vals = [num(ws_v.cell(r, 8).value) or 0 for r in rows]
            I_vals = [num(ws_v.cell(r, 9).value) or 0 for r in rows]
            # Buscar capitulo/subcapitulo
            subs = []
            for r in rows:
                # buscar hacia arriba subcapitulo (celda con texto en col F sin unidad)
                r_up = r - 1
                while r_up >= 7:
                    und_up = ws_v.cell(r_up, 7).value
                    desc_up = ws_v.cell(r_up, 6).value
                    if (und_up in (None, "")) and desc_up:
                        subs.append(str(desc_up).strip()[:50])
                        break
                    r_up -= 1
                else:
                    subs.append("?")
            distinct_subs = len(set(subs)) > 1
            # heuristica reubicacion: cant contractual >0 en una y cant actualizada 0 en otra? o subcapitulos distintos
            comentario = f"Filas {rows} subcapitulos={subs} H={H_vals} I={I_vals}"
            is_reub = distinct_subs and any(h > 0 and i == 0 for h, i in zip(H_vals, I_vals))
            duplicados.append({
                "codigo_idu": cod, "filas": rows,
                "es_reubicacion": bool(distinct_subs),
                "comentario": comentario
            })

    print(f"Duplicados: {len(duplicados)}")

    # =====================================
    # 5) VU vs VISOR y VU contractual
    # =====================================
    desviaciones_vu_visor = []
    desviaciones_vu_contractual = []

    # Cargar VISOR
    visor = load_csv("VISOR_07-05-25.csv")
    # Detectar col con codigo IDU y con VU CD
    # Vamos a inspeccionar encabezados
    visor_map = {}  # codigo -> VU CD
    if visor:
        # Buscar fila header
        hdr_row_idx = None
        for i, row in enumerate(visor[:20]):
            joined = " ".join(str(x) for x in row).upper()
            if "IDU" in joined and ("V/UNIT" in joined or "VR UNIT" in joined or "COSTO DIRECTO" in joined or "V. UNIT" in joined or "VU" in joined):
                hdr_row_idx = i
                break
        if hdr_row_idx is None:
            hdr_row_idx = 5  # fallback
        hdr = visor[hdr_row_idx]
        # buscar col codigo IDU y VU CD
        col_cod = None
        col_vu = None
        for j, h in enumerate(hdr):
            hn = str(h).upper()
            if col_cod is None and ("IDU" in hn or "CODIGO" in hn or "CÓDIGO" in hn):
                col_cod = j
            if "V/UNIT" in hn or "VR. UNIT" in hn or "V.UNIT" in hn or "COSTO DIRECTO" in hn or "V UNIT" in hn:
                col_vu = j
        for row in visor[hdr_row_idx + 1:]:
            if len(row) <= max(col_cod or 0, col_vu or 0):
                continue
            cod = str(row[col_cod]).strip() if col_cod is not None else ""
            vu = num(row[col_vu]) if col_vu is not None else None
            if cod and vu:
                visor_map[cod] = vu

    # Cargar PRESUPUESTO CONTRACTUAL MAYO 25
    contr = load_csv("PRESUPUESTO_CONTRACTUAL_MAYO_25.csv")
    contr_map = {}  # item_pago o codigo -> VU CD
    contr_by_ip = {}  # item_pago -> VU CD
    if contr:
        # Buscar encabezado
        hdr_row_idx = None
        for i, row in enumerate(contr[:20]):
            joined = " ".join(str(x) for x in row).upper()
            if ("ITEM" in joined or "ÍTEM" in joined) and ("V/UNIT" in joined or "COSTO DIRECTO" in joined or "V UNIT" in joined or "VR UNIT" in joined):
                hdr_row_idx = i
                break
        if hdr_row_idx is None:
            hdr_row_idx = 5
        hdr = contr[hdr_row_idx]
        col_cod = None
        col_ip = None
        col_vu = None
        for j, h in enumerate(hdr):
            hn = str(h).upper()
            if col_cod is None and "IDU" in hn:
                col_cod = j
            if col_ip is None and ("ITEM" in hn or "ÍTEM" in hn):
                col_ip = j
            if col_vu is None and ("V/UNIT" in hn or "V.UNIT" in hn or "COSTO DIRECTO" in hn or "VR UNIT" in hn or "V UNIT" in hn):
                col_vu = j
        for row in contr[hdr_row_idx + 1:]:
            if len(row) <= max(filter(lambda x: x is not None, [col_cod, col_ip, col_vu])):
                continue
            cod = str(row[col_cod]).strip() if col_cod is not None else ""
            ip = str(row[col_ip]).strip() if col_ip is not None else ""
            vu = num(row[col_vu]) if col_vu is not None else None
            if vu:
                if cod:
                    contr_map[cod] = vu
                if ip:
                    contr_by_ip[ip] = vu

    # Cargar comparativa.json para VU V0
    comp_path = ROOT / "comparativa.json"
    v0_map = {}  # codigo -> vu contractual
    v0_cant_map = {}  # codigo -> cant contractual
    if comp_path.exists():
        try:
            with open(comp_path, encoding="utf-8") as f:
                comp = json.load(f)
            items = comp.get("items") or []
            for it in items:
                cod = str(it.get("codigo") or it.get("item_pago") or "").strip()
                if not cod:
                    continue
                vu = num(it.get("valor_cont_cd") or it.get("valor_ini_cd") or it.get("vu_cd"))
                cn = num(it.get("cant_cont") or it.get("cant_ini"))
                if vu:
                    v0_map[cod] = vu
                if cn is not None:
                    v0_cant_map[cod] = cn
        except Exception as e:
            print(f"comparativa.json: {e}")

    # Iterar filas de la hoja principal para cruzar
    for r in range(7, 680):
        cod = ws_v.cell(r, 2).value
        ip = ws_v.cell(r, 3).value
        K = num(ws_v.cell(r, 11).value)
        und = ws_v.cell(r, 7).value
        if not (cod and K and und):
            continue
        cod_s = str(cod).strip()
        ip_s = str(ip).strip() if ip else ""
        # Visor
        vu_visor = visor_map.get(cod_s)
        if vu_visor:
            delta_pct = ((K - vu_visor) / vu_visor) * 100 if vu_visor else 0
            if abs(delta_pct) > 2:
                desviaciones_vu_visor.append({
                    "codigo_idu": cod_s, "row": r,
                    "K_v4": K, "K_visor": vu_visor,
                    "delta_pct": round(delta_pct, 2)
                })
        # Contractual
        vu_contr = contr_map.get(cod_s) or contr_by_ip.get(ip_s) or v0_map.get(cod_s) or v0_map.get(ip_s)
        if vu_contr:
            delta_pct = ((K - vu_contr) / vu_contr) * 100 if vu_contr else 0
            if abs(delta_pct) > 2:
                desviaciones_vu_contractual.append({
                    "codigo_idu": cod_s, "row": r,
                    "K_v4": K, "K_contractual": vu_contr,
                    "delta_pct": round(delta_pct, 2)
                })

    print(f"Desviaciones VU vs VISOR: {len(desviaciones_vu_visor)}")
    print(f"Desviaciones VU vs Contractual: {len(desviaciones_vu_contractual)}")

    # =====================================
    # 6) Efecto precio vs efecto cantidad
    # =====================================
    efecto_pc = []
    ef_precio_total = 0
    ef_cant_total = 0
    inter_total = 0
    delta_valor_total = 0

    # Necesitamos: K_V0 (contractual) y cant_V0. Y K_V4=K, cant_V4=I
    for r in range(7, 680):
        cod = ws_v.cell(r, 2).value
        ip = ws_v.cell(r, 3).value
        H = num(ws_v.cell(r, 8).value)  # cant contractual
        I = num(ws_v.cell(r, 9).value)  # cant actualizada
        K = num(ws_v.cell(r, 11).value)  # VU CD V4
        M = num(ws_v.cell(r, 13).value)
        N = num(ws_v.cell(r, 14).value)
        if cod is None:
            continue
        cod_s = str(cod).strip()
        ip_s = str(ip).strip() if ip else ""
        # K_V0 (costo directo contractual) - preferir contr_map, sino v0_map
        K_V0_cd = contr_map.get(cod_s) or contr_by_ip.get(ip_s) or v0_map.get(cod_s)
        if K_V0_cd is None or H is None or I is None or K is None:
            continue
        if H <= 0 or I <= 0:
            continue
        # Ambas cantidades > 0
        # Trabajar en costo directo, luego escalar por AIU
        K_V4_cd = K
        cant_V0 = H
        cant_V4 = I
        ef_precio = (K_V4_cd - K_V0_cd) * cant_V0 * (1 + AIU)
        ef_cant = (cant_V4 - cant_V0) * K_V0_cd * (1 + AIU)
        interaccion = (K_V4_cd - K_V0_cd) * (cant_V4 - cant_V0) * (1 + AIU)
        delta_val = (M or 0) - (N or 0)
        ef_precio_total += ef_precio
        ef_cant_total += ef_cant
        inter_total += interaccion
        delta_valor_total += delta_val
        if abs(delta_val) > 1e6 or abs(ef_precio) > 1e6 or abs(ef_cant) > 1e6:
            efecto_pc.append({
                "codigo_idu": cod_s, "row": r,
                "delta_valor": round(delta_val),
                "efecto_precio": round(ef_precio),
                "efecto_cantidad": round(ef_cant),
                "interaccion": round(interaccion)
            })

    resumen_ef = {
        "efecto_precio_total": round(ef_precio_total),
        "efecto_cantidad_total": round(ef_cant_total),
        "interaccion_total": round(inter_total),
        "delta_valor_total_M_menos_N": round(delta_valor_total),
        "suma_p_q_i": round(ef_precio_total + ef_cant_total + inter_total),
        "verificacion_delta": round((ef_precio_total + ef_cant_total + inter_total) - delta_valor_total)
    }
    print(f"Efecto precio: {resumen_ef}")

    # =====================================
    # HALLAZGOS
    # =====================================
    hallazgos = []
    hid = 1

    if celdas_error:
        hallazgos.append({
            "id": f"H{hid:02d}", "severidad": "ALTA",
            "titulo": f"Celdas con errores de Excel ({len(celdas_error)})",
            "descripcion": "Se detectaron celdas con errores tipo #REF!, #DIV/0!, #N/A, etc. Ejemplos: " +
                           ", ".join(f"{c['celda']}={c['tipo']}" for c in celdas_error[:5]),
            "hoja": HOJA_PPAL, "fila": None, "impacto_pesos": None,
            "recomendacion": "Solicitar al contratista corregir las celdas con errores antes de aceptar la version V4. Revisar cadenas de dependencias."
        })
        hid += 1

    if desviaciones_aiu_L:
        top_impacto = sum(abs(d["delta"]) for d in desviaciones_aiu_L)
        hallazgos.append({
            "id": f"H{hid:02d}", "severidad": "ALTA" if len(desviaciones_aiu_L) > 5 else "MEDIA",
            "titulo": f"AIU aplicado no coincide en columna L ({len(desviaciones_aiu_L)} filas)",
            "descripcion": f"Filas donde L != round(K * 1.31849). Filas afectadas (primeras 5): " +
                           ", ".join(f"row {d['row']} L={fmt_pesos(d['L'])} esp={fmt_pesos(d['esperado_L'])}" for d in desviaciones_aiu_L[:5]),
            "hoja": HOJA_PPAL, "fila": desviaciones_aiu_L[0]["row"] if desviaciones_aiu_L else None,
            "impacto_pesos": round(top_impacto),
            "recomendacion": "Verificar por que L != K*(1+AIU_31.849%). Puede ser AIU distinto (obras vs SST 20.006%) o error de digitacion."
        })
        hid += 1

    if desviaciones_M_N_O_Q:
        by_col = Counter(d["columna"] for d in desviaciones_M_N_O_Q)
        hallazgos.append({
            "id": f"H{hid:02d}", "severidad": "ALTA",
            "titulo": f"Inconsistencias aritmeticas en columnas M/N/O/Q ({len(desviaciones_M_N_O_Q)} filas)",
            "descripcion": f"Distribucion por columna: {dict(by_col)}. M=I*L, N=H*L, O=(I-H)*L, Q=O+P.",
            "hoja": HOJA_PPAL, "fila": desviaciones_M_N_O_Q[0]["row"] if desviaciones_M_N_O_Q else None,
            "impacto_pesos": round(sum(abs(d["delta"]) for d in desviaciones_M_N_O_Q)),
            "recomendacion": "Solicitar re-calculo de columnas M/N/O/Q con formulas. Detectar filas de digitacion manual."
        })
        hid += 1

    if desviaciones_CB:
        hallazgos.append({
            "id": f"H{hid:02d}", "severidad": "MEDIA",
            "titulo": f"Total general CB no cuadra con M ({len(desviaciones_CB)} filas)",
            "descripcion": "Filas donde columna CB (total general por fila) != M (valor con AIU).",
            "hoja": HOJA_PPAL, "fila": desviaciones_CB[0]["row"] if desviaciones_CB else None,
            "impacto_pesos": round(sum(abs(d["delta"]) for d in desviaciones_CB)),
            "recomendacion": "Verificar suma de columnas por CIV vs M. Diferencias indican renglones parcialmente asignados."
        })
        hid += 1

    if duplicados:
        # Filtrar duplicados con impacto real
        dup_reales = [d for d in duplicados if not d["es_reubicacion"]]
        hallazgos.append({
            "id": f"H{hid:02d}", "severidad": "ALTA" if dup_reales else "MEDIA",
            "titulo": f"Codigos IDU repetidos en la hoja principal ({len(duplicados)})",
            "descripcion": f"Total duplicados: {len(duplicados)}. Aparentes reubicaciones: {len(duplicados)-len(dup_reales)}. Duplicados reales: {len(dup_reales)}.",
            "hoja": HOJA_PPAL, "fila": None, "impacto_pesos": None,
            "recomendacion": "Revisar cada duplicado. Si son reubicaciones justificar el cambio de subcapitulo; si son sumas paralelas exigir consolidacion."
        })
        hid += 1

    if desviaciones_vu_visor:
        top = sorted(desviaciones_vu_visor, key=lambda x: abs(x["delta_pct"]), reverse=True)[:5]
        hallazgos.append({
            "id": f"H{hid:02d}", "severidad": "MEDIA",
            "titulo": f"VU V4 desviado >2% del VISOR ({len(desviaciones_vu_visor)} items)",
            "descripcion": "Top desviaciones: " + ", ".join(f"{t['codigo_idu']} {t['delta_pct']}%" for t in top),
            "hoja": HOJA_PPAL, "fila": None,
            "impacto_pesos": None,
            "recomendacion": "Solicitar justificacion del contratista para desviaciones importantes vs VISOR IDU."
        })
        hid += 1

    if desviaciones_vu_contractual:
        top = sorted(desviaciones_vu_contractual, key=lambda x: abs(x["delta_pct"]), reverse=True)[:5]
        hallazgos.append({
            "id": f"H{hid:02d}", "severidad": "ALTA",
            "titulo": f"VU V4 desviado >2% del PRESUPUESTO CONTRACTUAL ({len(desviaciones_vu_contractual)} items)",
            "descripcion": "Top: " + ", ".join(f"{t['codigo_idu']} {t['delta_pct']}%" for t in top),
            "hoja": HOJA_PPAL, "fila": None,
            "impacto_pesos": None,
            "recomendacion": "Verificar autorizacion de cambio de VU respecto al contrato firmado. Los VU deben coincidir con el contractual."
        })
        hid += 1

    if consistencia_hojas:
        hallazgos.append({
            "id": f"H{hid:02d}", "severidad": "MEDIA",
            "titulo": f"Inconsistencia entre hojas ({len(consistencia_hojas)})",
            "descripcion": "Totales no coinciden entre hojas de resumen y la hoja principal.",
            "hoja": None, "fila": None,
            "impacto_pesos": round(sum(abs(c["delta"]) for c in consistencia_hojas)),
            "recomendacion": "Alinear hojas resumen/EJECUTIVO/Presupuesto estimado con el total final $75.426.575.199."
        })
        hid += 1

    if rangos_incompletos:
        hallazgos.append({
            "id": f"H{hid:02d}", "severidad": "MEDIA",
            "titulo": f"Rangos de formulas potencialmente incompletos ({len(rangos_incompletos)})",
            "descripcion": "Formulas SUM que no cubren todo el rango de datos.",
            "hoja": HOJA_PPAL, "fila": None, "impacto_pesos": None,
            "recomendacion": "Ajustar rangos para cubrir todos los items."
        })
        hid += 1

    # Guardar JSON
    out_json = {
        "meta": {
            "fuente": XLSX.name,
            "hoja": HOJA_PPAL,
            "aiu_factor": AIU,
            "fecha_analisis": "2026-09-26"
        },
        "formulas": {
            "conteo_formulas": conteo_formulas,
            "conteo_hardcoded": conteo_hardcoded,
            "ejemplos_formulas": ejemplos_formulas[:20],
            "celdas_error": celdas_error[:100]
        },
        "rangos_incompletos": rangos_incompletos[:50],
        "desviaciones_aiu_L": desviaciones_aiu_L[:100],
        "desviaciones_M_N_O_Q": desviaciones_M_N_O_Q[:200],
        "desviaciones_CB_vs_M": desviaciones_CB[:100],
        "consistencia_hojas": consistencia_hojas[:100],
        "duplicados": duplicados,
        "desviaciones_vu_visor": desviaciones_vu_visor[:200],
        "desviaciones_vu_contractual": desviaciones_vu_contractual[:200],
        "efecto_precio_cantidad": sorted(efecto_pc, key=lambda x: abs(x["delta_valor"]), reverse=True)[:100],
        "resumen_efecto_precio_cantidad_total": resumen_ef,
        "hallazgos": hallazgos
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out_json, f, ensure_ascii=False, indent=1, default=str)
    print(f"JSON escrito: {OUT_JSON}")

    # =========================
    # MD
    # =========================
    md = []
    md.append("# 04 - Aritmetica, precios unitarios y formulas\n")
    md.append(f"Fuente: `{XLSX.name}` - Hoja: `{HOJA_PPAL}` - AIU contractual: **31,849%**  \n")
    md.append(f"Fecha analisis: 2026-09-26\n\n")

    md.append("## 1. Formulas vs celdas digitadas a mano\n\n")
    md.append(f"- **Formulas encontradas**: {conteo_formulas}\n")
    md.append(f"- **Valores hardcoded**: {conteo_hardcoded}\n")
    md.append(f"- **Ratio formulas/total**: {conteo_formulas/(conteo_formulas+conteo_hardcoded)*100:.1f}%\n\n")
    md.append(f"### Celdas con errores ({len(celdas_error)})\n\n")
    if celdas_error:
        md.append("| Celda | Tipo |\n|---|---|\n")
        for c in celdas_error[:20]:
            md.append(f"| `{c['celda']}` | {c['tipo']} |\n")
        md.append("\n")
    else:
        md.append("Sin celdas con errores tipo #REF!, #DIV/0!, etc.\n\n")
    md.append(f"### Ejemplos de formulas ({len(ejemplos_formulas[:10])})\n\n")
    md.append("| Celda | Formula |\n|---|---|\n")
    for e in ejemplos_formulas[:10]:
        f_short = e["formula"] if len(e["formula"]) < 80 else e["formula"][:77] + "..."
        md.append(f"| `{e['celda']}` | `{f_short}` |\n")
    md.append("\n")

    md.append("## 2. Consistencia aritmetica por fila\n\n")
    md.append(f"### AIU aplicado (L = round(K * 1.31849))\n")
    md.append(f"Filas con desviacion > $1: **{len(desviaciones_aiu_L)}**\n\n")
    if desviaciones_aiu_L:
        md.append("| Fila | K | L actual | L esperado | delta |\n|---|---|---|---|---|\n")
        for d in desviaciones_aiu_L[:15]:
            md.append(f"| {d['row']} | {fmt_pesos(d['K'])} | {fmt_pesos(d['L'])} | {fmt_pesos(d['esperado_L'])} | {fmt_pesos(d['delta'])} |\n")
        md.append("\n")

    md.append(f"### M/N/O/Q\n")
    md.append(f"Total desviaciones > $1: **{len(desviaciones_M_N_O_Q)}**\n\n")
    if desviaciones_M_N_O_Q:
        by_col = Counter(d["columna"] for d in desviaciones_M_N_O_Q)
        md.append(f"Distribucion: {dict(by_col)}\n\n")
        md.append("| Fila | Columna | Actual | Esperado | delta |\n|---|---|---|---|---|\n")
        for d in desviaciones_M_N_O_Q[:20]:
            md.append(f"| {d['row']} | {d['columna']} | {fmt_pesos(d['actual'])} | {fmt_pesos(d['esperado'])} | {fmt_pesos(d['delta'])} |\n")
        md.append("\n")

    md.append(f"### CB (total general por fila) vs M\n")
    md.append(f"Desviaciones: **{len(desviaciones_CB)}**\n\n")
    if desviaciones_CB:
        md.append("| Fila | CB | M | delta |\n|---|---|---|---|\n")
        for d in desviaciones_CB[:20]:
            md.append(f"| {d['row']} | {fmt_pesos(d['actual'])} | {fmt_pesos(d['esperado'])} | {fmt_pesos(d['delta'])} |\n")
        md.append("\n")

    md.append("## 3. Consistencia entre hojas\n\n")
    md.append(f"Discrepancias detectadas: **{len(consistencia_hojas)}**\n\n")
    if consistencia_hojas:
        md.append("| Hoja | Celda | Valor | Esperado | Delta |\n|---|---|---|---|---|\n")
        for c in consistencia_hojas[:30]:
            md.append(f"| {c['hoja']} | `{c['celda']}` | {fmt_pesos(c['valor'])} | {fmt_pesos(c['esperado'])} | {fmt_pesos(c['delta'])} |\n")
        md.append("\n")

    md.append("## 4. Duplicados por codigo IDU\n\n")
    md.append(f"Codigos IDU con >1 renglon: **{len(duplicados)}**\n\n")
    if duplicados:
        md.append("| Codigo IDU | Filas | Reubicacion? |\n|---|---|---|\n")
        for d in duplicados[:30]:
            md.append(f"| `{d['codigo_idu']}` | {d['filas']} | {'Si' if d['es_reubicacion'] else 'No'} |\n")
        md.append("\n")

    md.append("## 5. VU vs referencias\n\n")
    md.append(f"### VU V4 vs VISOR 07-05-25\n")
    md.append(f"Desviaciones > 2%: **{len(desviaciones_vu_visor)}**\n\n")
    if desviaciones_vu_visor:
        top = sorted(desviaciones_vu_visor, key=lambda x: abs(x["delta_pct"]), reverse=True)[:15]
        md.append("| Codigo IDU | Fila V4 | K_v4 | K_VISOR | delta_pct |\n|---|---|---|---|---|\n")
        for t in top:
            md.append(f"| `{t['codigo_idu']}` | {t.get('row','-')} | {fmt_pesos(t['K_v4'])} | {fmt_pesos(t['K_visor'])} | {t['delta_pct']}% |\n")
        md.append("\n")
    md.append(f"### VU V4 vs PRESUPUESTO CONTRACTUAL MAYO 25\n")
    md.append(f"Desviaciones > 2%: **{len(desviaciones_vu_contractual)}**\n\n")
    if desviaciones_vu_contractual:
        top = sorted(desviaciones_vu_contractual, key=lambda x: abs(x["delta_pct"]), reverse=True)[:15]
        md.append("| Codigo IDU | Fila V4 | K_v4 | K_contractual | delta_pct |\n|---|---|---|---|---|\n")
        for t in top:
            md.append(f"| `{t['codigo_idu']}` | {t.get('row','-')} | {fmt_pesos(t['K_v4'])} | {fmt_pesos(t['K_contractual'])} | {t['delta_pct']}% |\n")
        md.append("\n")

    md.append("## 6. Efecto precio vs efecto cantidad\n\n")
    md.append(f"- **Efecto precio total**: {fmt_pesos(resumen_ef['efecto_precio_total'])}\n")
    md.append(f"- **Efecto cantidad total**: {fmt_pesos(resumen_ef['efecto_cantidad_total'])}\n")
    md.append(f"- **Interaccion**: {fmt_pesos(resumen_ef['interaccion_total'])}\n")
    md.append(f"- **Suma P+Q+I**: {fmt_pesos(resumen_ef['suma_p_q_i'])}\n")
    md.append(f"- **Delta valor M-N total**: {fmt_pesos(resumen_ef['delta_valor_total_M_menos_N'])}\n")
    md.append(f"- **Verificacion**: {fmt_pesos(resumen_ef['verificacion_delta'])}\n\n")
    md.append("### Items con mayor efecto\n\n")
    md.append("| Codigo IDU | Fila | Delta valor | Efecto precio | Efecto cantidad | Interaccion |\n|---|---|---|---|---|---|\n")
    for e in sorted(efecto_pc, key=lambda x: abs(x["delta_valor"]), reverse=True)[:20]:
        md.append(f"| `{e['codigo_idu']}` | {e['row']} | {fmt_pesos(e['delta_valor'])} | {fmt_pesos(e['efecto_precio'])} | {fmt_pesos(e['efecto_cantidad'])} | {fmt_pesos(e['interaccion'])} |\n")
    md.append("\n")

    md.append("## 7. Hallazgos con recomendaciones\n\n")
    for h in hallazgos:
        md.append(f"### {h['id']} - {h['titulo']} [{h['severidad']}]\n\n")
        md.append(f"{h['descripcion']}\n\n")
        if h['impacto_pesos']:
            md.append(f"- Impacto estimado: {fmt_pesos(h['impacto_pesos'])}\n")
        md.append(f"- Recomendacion: {h['recomendacion']}\n\n")

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("".join(md))
    print(f"MD escrito: {OUT_MD}")

    # Reporte final 5 lineas
    print("\n===== RESUMEN 5 LINEAS =====")
    print(f"Formulas OK: {conteo_formulas} | Hardcoded: {conteo_hardcoded} | Errores celdas: {len(celdas_error)}")
    print(f"Duplicados codigo_idu: {len(duplicados)}")
    print("Top 3 desviaciones VU vs VISOR:")
    for t in sorted(desviaciones_vu_visor, key=lambda x: abs(x["delta_pct"]), reverse=True)[:3]:
        print(f"  {t['codigo_idu']}: {t['delta_pct']}%")
    print(f"Efecto precio total: {fmt_pesos(resumen_ef['efecto_precio_total'])}")
    print(f"Efecto cantidad total: {fmt_pesos(resumen_ef['efecto_cantidad_total'])}")


if __name__ == "__main__":
    main()
