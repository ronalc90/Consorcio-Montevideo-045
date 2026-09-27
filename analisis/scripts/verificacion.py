"""
Verificacion independiente. Recalcula desde el Excel fuente las cifras clave
del informe, la app y el Excel de salida. Reporta cualquier diferencia.
"""
import json
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
XLSX = ROOT / "fuentes" / "4. PRESUPUESTO 01-09-2026 75MM (8 MESES).xlsx"
JSON = ROOT / "analisis" / "analisis_2026_09.json"
PRES = ROOT / "analisis" / "datos" / "presupuesto_2026_09.json"


def ok(label, calc, esperado, tol=100):
    diff = calc - esperado
    marker = "OK" if abs(diff) <= tol else "OFF"
    print(f"  [{marker:3}] {label:60} calc={calc:>18,.0f} esp={esperado:>18,.0f} delta={diff:>+15,.0f}")
    return abs(diff) <= tol


def main():
    p = json.load(open(JSON, encoding="utf-8"))
    pres = json.load(open(PRES, encoding="utf-8"))

    wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)
    ws = wb["PRESUPUESTO TODOS LOS CIV 84 NP"]
    rows = list(ws.iter_rows(values_only=True))

    print("=== VERIFICACION INDEPENDIENTE ===\n")

    # 1. Fila 688 col M (obras con AIU final)
    print("1. TOTALES OFICIALES DEL EXCEL")
    m_688 = rows[687][12]  # col M
    n_688 = rows[687][13]  # col N
    ok("Fila 688 col M (obras finales con AIU)", m_688, 58196933800)
    ok("Fila 688 col N (obras iniciales con AIU)", n_688, 44303294799)

    # 2. Fila 703 (total con AIU 75.426...)
    m_703 = rows[702][12] if rows[702][12] else 0
    ok("Fila 703 col M (total contrato)", m_703, 75426575199)

    # 3. Sumar obras con AIU recorriendo renglones 7..679
    total_M = 0
    total_N = 0
    for n in range(6, 679):
        r = rows[n]
        # Detectar chapter ACEROS (bloque 680-687 lo excluimos con el rango)
        m = r[12] if isinstance(r[12], (int, float)) else 0
        nn = r[13] if isinstance(r[13], (int, float)) else 0
        # Los renglones que suman en obras son los que tienen unidad no vacia
        und = r[6]
        if und not in (None, ""):
            total_M += m
            total_N += nn
    print()
    print("2. RECALCULO POR RENGLON (excluyendo ACEROS)")
    ok("Sum col M (7-679)", total_M, 58196933800)
    ok("Sum col N (7-679)", total_N, 44303294799)

    # 4. Sumar por CIV en la matriz S:BW (columnas pares valor)
    # Columnas de valor: T=19, V=21, X=23, Z=25, AB=27, AD=29, AF=31 (SG2: 7 CIVs)
    # Luego AH=33 (total SG2), y AK=36, AM=38,..., BW=74 (SG5: 20 CIVs)
    civ_val_cols = list(range(19, 32, 2))  # SG2 7 CIVs -> cols 19,21,23,25,27,29,31
    civ_val_cols += list(range(36, 75, 2))  # SG5 20 CIVs -> cols 36..74 pares
    if len(civ_val_cols) != 27:
        print(f"  [OFF] Detección de columnas: {len(civ_val_cols)} CIVs (esperado 27)")
    total_por_civ = 0
    for n in range(6, 679):
        r = rows[n]
        und = r[6]
        if und in (None, ""):
            continue
        for col in civ_val_cols:
            v = r[col] if col < len(r) else 0
            if isinstance(v, (int, float)):
                total_por_civ += v
    print()
    print("3. SUM POR CIV EN MATRIZ S:BW")
    ok("Sum de valor por CIV (27 columnas)", total_por_civ, 58196933800, tol=200)

    # 5. Componentes fila 692..701
    print()
    print("4. COMPONENTES NO-OBRA (filas 692-701)")
    components_expected = {
        692: ("PMA-SST", 4110277014),
        693: ("Diálogo ciudadano", 2430023370),
        694: ("PMT", 2007577162),
        695: ("Ajustes cambio vigencia", 4555525079),
        696: ("Ensayos laboratorio", 299267609),
        697: ("Actividades acero", 2977517840),
        698: ("SDA", 31328679),
        699: ("Bioseguridad", 59390312),
        700: ("Fondo compensaciones", 0),
        701: ("Fase obras iniciales", 758734334),
    }
    for row_num, (label, esperado) in components_expected.items():
        val = rows[row_num - 1][12] if rows[row_num - 1][12] else 0
        try:
            val = float(val) if not isinstance(val, (int, float)) else val
        except (ValueError, TypeError):
            val = 0
        ok(f"Fila {row_num} {label}", val, esperado)

    # 6. Consolidado JSON: hallazgos por severidad
    print()
    print("5. CONSOLIDADO ANALISIS_2026_09.JSON")
    hall = p.get("hallazgos") or []
    sev_count = {}
    for h in hall:
        sev_count[h.get("severidad")] = sev_count.get(h.get("severidad"), 0) + 1
    for s in ["ALTA", "MEDIA", "BAJA", "INFO"]:
        print(f"  Hallazgos {s}: {sev_count.get(s, 0)}")
    print(f"  Total hallazgos: {len(hall)}")

    # 7. Costo por CIV
    print()
    print("6. COSTO POR CIV")
    costos = p.get("costo_civ", {}).get("costo_por_civ") or []
    tot_obras = sum(c.get("obras_total") or 0 for c in costos)
    tot_total = sum(c.get("total") or 0 for c in costos)
    ok(f"Suma 27 CIVs obras con AIU", tot_obras, 58196933800, tol=200)
    ok(f"Suma 27 CIVs total con componentes", tot_total, 75426575199, tol=200)

    # 8. Waterfall V0-V4
    print()
    print("7. WATERFALL V0-V4")
    wf = p.get("versiones_plazo", {}).get("waterfall") or []
    v0_total = sum(w.get("v0", 0) or 0 for w in wf if w.get("componente", "").upper() != "TOTAL GENERAL")
    v4_total = sum(w.get("v4", 0) or 0 for w in wf if w.get("componente", "").upper() != "TOTAL GENERAL")
    ok("Sum V0 componentes", v0_total, 59426575199)
    ok("Sum V4 componentes", v4_total, 75426575199)

    # 9. Renglones NP
    print()
    print("8. NPs")
    npc = 0
    npval = 0
    for it in pres["items"]:
        if it.get("is_np") and (it.get("cant_actualizada") or 0) > 0:
            npc += 1
            npval += it.get("valor_actualizado_aiu") or 0
    ok("Renglones NP con cantidad > 0", npc, 105)
    ok("Suma valor NP con AIU", npval, 14150924549, tol=100)

    # 10. Reporte final
    print()
    print("=" * 60)
    print("VERIFICACION COMPLETA")
    print("=" * 60)


if __name__ == "__main__":
    main()
