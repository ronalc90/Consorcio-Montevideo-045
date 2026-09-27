"""
Genera analisis/Analisis_Presupuesto_2026-09.xlsx con formato profesional.
Hojas: Resumen, Variación ítems, Variación neta por código, Variación por CIV (matriz),
       Costo por CIV, NPs, Hallazgos.
"""
import json
from pathlib import Path
from datetime import date

import xlsxwriter

ROOT = Path(__file__).resolve().parents[2]
JSON = ROOT / "analisis" / "analisis_2026_09.json"
OUT = ROOT / "analisis" / "Analisis_Presupuesto_2026-09.xlsx"


def main():
    p = json.load(open(JSON, encoding="utf-8"))
    wb = xlsxwriter.Workbook(str(OUT))

    # Formats
    fmt_h1 = wb.add_format({"bold": True, "bg_color": "#1a365d", "font_color": "#fff", "font_size": 14, "align": "left", "valign": "vcenter", "border": 1})
    fmt_h2 = wb.add_format({"bold": True, "bg_color": "#2c5282", "font_color": "#fff", "font_size": 11, "align": "center", "valign": "vcenter", "border": 1, "text_wrap": True})
    fmt_money = wb.add_format({"num_format": '"$"#,##0;[Red]"-$"#,##0', "border": 1})
    fmt_money_bold = wb.add_format({"num_format": '"$"#,##0;[Red]"-$"#,##0', "bold": True, "border": 1, "bg_color": "#edf2f7"})
    fmt_num = wb.add_format({"num_format": "#,##0.00;-#,##0.00;\"0\"", "border": 1})
    fmt_txt = wb.add_format({"border": 1, "text_wrap": True, "valign": "top"})
    fmt_pct = wb.add_format({"num_format": "+0.00%;[Red]-0.00%;0.00%", "border": 1})
    fmt_int = wb.add_format({"num_format": "#,##0", "border": 1})
    fmt_delta = wb.add_format({"num_format": '[Green]"+$"#,##0;[Red]"-$"#,##0;"$"0', "border": 1})

    # ---------- Hoja Resumen ----------
    ws = wb.add_worksheet("Resumen")
    ws.set_column("A:A", 45)
    ws.set_column("B:G", 20)
    ws.merge_range("A1:G1", "Análisis Presupuesto 01-09-2026 · 75MM · 8 meses", fmt_h1)
    ws.write("A2", "Fuente:", fmt_txt); ws.write("B2", "4. PRESUPUESTO 01-09-2026 75MM (8 MESES).xlsx", fmt_txt)
    ws.write("A3", "Fecha del análisis:", fmt_txt); ws.write("B3", str(date.today()), fmt_txt)
    ws.write("A4", "Contratista:", fmt_txt); ws.write("B4", "Consorcio VICON 024", fmt_txt)
    ws.write("A5", "Interventoría:", fmt_txt); ws.write("B5", "Consorcio Montevideo 045", fmt_txt)

    # Waterfall
    row = 7
    ws.write(row, 0, "Waterfall de versiones por componente", fmt_h1)
    row += 1
    headers = ["Componente", "V0 firma", "V1 IDU 25-02-2026", "V2 VICON 21-04-2026", "V3 63MM intermedia", "V4 01-09-2026", "Δ V0-V4"]
    for i, h in enumerate(headers):
        ws.write(row, i, h, fmt_h2)
    row += 1
    for w in (p.get("versiones_plazo", {}).get("waterfall") or []):
        ws.write(row, 0, w.get("componente"), fmt_txt)
        ws.write(row, 1, w.get("v0") or 0, fmt_money)
        ws.write(row, 2, w.get("v1") or 0, fmt_money)
        ws.write(row, 3, w.get("v2") or 0, fmt_money)
        ws.write(row, 4, w.get("v3") or 0, fmt_money)
        ws.write(row, 5, w.get("v4") or 0, fmt_money_bold)
        ws.write(row, 6, (w.get("v4") or 0) - (w.get("v0") or 0), fmt_delta)
        row += 1

    row += 2
    ws.write(row, 0, "Verificaciones al peso", fmt_h1); row += 1
    verif = [
        ("Obras con AIU V4 fila 688", 58196933800),
        ("Total contrato V4 fila 703", 75426575199),
        ("Adición neta solicitada", 16000000000),
        ("Plazo adicional (meses)", 8),
        ("Renglones activos", 407),
        ("Códigos NP únicos", 81),
        ("Renglones NP con cantidad", 105),
    ]
    for label, val in verif:
        ws.write(row, 0, label, fmt_txt)
        ws.write(row, 1, val, fmt_int)
        row += 1

    # Capítulos
    row += 2
    ws.write(row, 0, "Variación de obras con AIU por capítulo", fmt_h1); row += 1
    ws.write(row, 0, "Capítulo", fmt_h2)
    ws.write(row, 1, "Valor inicial", fmt_h2)
    ws.write(row, 2, "Valor final", fmt_h2)
    ws.write(row, 3, "Δ", fmt_h2)
    ws.write(row, 4, "Balance may/men", fmt_h2)
    ws.write(row, 5, "Incorp. NP", fmt_h2)
    row += 1
    for c in (p.get("variacion_items", {}).get("capitulos") or []):
        ws.write(row, 0, c.get("chapter"), fmt_txt)
        ws.write(row, 1, c.get("valor_inicial") or 0, fmt_money)
        ws.write(row, 2, c.get("valor_final") or 0, fmt_money)
        ws.write(row, 3, c.get("delta") or 0, fmt_delta)
        ws.write(row, 4, c.get("balance_may_men") or 0, fmt_delta)
        ws.write(row, 5, c.get("incorporacion_np") or 0, fmt_delta)
        row += 1

    # ---------- Hoja Variación ítems ----------
    ws = wb.add_worksheet("Variación ítems")
    ws.freeze_panes(1, 0)
    ws.autofilter(0, 0, 800, 14)
    headers = ["Fila", "Cap", "Código", "Ítem", "Descripción", "Und",
               "Cant inicial H", "Cant final I", "Δ Cant J",
               "VU CD K", "VU CD+AIU L",
               "Valor inicial N", "Valor final M", "Δ Valor", "Estado"]
    widths = [7, 6, 10, 10, 55, 6, 14, 14, 14, 14, 14, 18, 18, 18, 18]
    for i, (h, w) in enumerate(zip(headers, widths)):
        ws.write(0, i, h, fmt_h2)
        ws.set_column(i, i, w)
    ws.set_row(0, 32)
    items = p.get("variacion_items", {}).get("items") or []
    for r, it in enumerate(items, 1):
        H = it.get("H") if "H" in it else it.get("cant_contractual")
        I = it.get("I") if "I" in it else it.get("cant_actualizada")
        N = it.get("N") if "N" in it else it.get("valor_inicial_aiu")
        M = it.get("M") if "M" in it else it.get("valor_actualizado_aiu")
        K = it.get("K") if "K" in it else it.get("vu_cd")
        L = it.get("L") if "L" in it else it.get("vu_cd_aiu")
        estado = it.get("estado") or (
            "np_nuevo" if it.get("is_np") else
            ("nuevo_contractual" if (H or 0) == 0 and (I or 0) > 0 else
             ("eliminado" if (H or 0) > 0 and (I or 0) == 0 else
              ("sin_cambio" if (H or 0) == (I or 0) else
               ("aumento" if (I or 0) > (H or 0) else "disminucion"))))
        )
        ws.write(r, 0, it.get("row"), fmt_int)
        ws.write(r, 1, (it.get("chapter") or "").split(".")[0], fmt_txt)
        ws.write(r, 2, it.get("codigo_idu") or "", fmt_txt)
        ws.write(r, 3, it.get("item_pago") or "", fmt_txt)
        ws.write(r, 4, it.get("descripcion") or "", fmt_txt)
        ws.write(r, 5, it.get("und") or "", fmt_txt)
        ws.write(r, 6, H or 0, fmt_num)
        ws.write(r, 7, I or 0, fmt_num)
        ws.write(r, 8, (I or 0) - (H or 0), fmt_num)
        ws.write(r, 9, K or 0, fmt_money)
        ws.write(r, 10, L or 0, fmt_money)
        ws.write(r, 11, N or 0, fmt_money)
        ws.write(r, 12, M or 0, fmt_money)
        ws.write(r, 13, (M or 0) - (N or 0), fmt_delta)
        ws.write(r, 14, estado, fmt_txt)

    # ---------- Hoja Variación neta por código ----------
    ws = wb.add_worksheet("Variación neta por código")
    ws.freeze_panes(1, 0)
    headers = ["Código IDU", "H total", "I total", "Δ Cant", "Δ Valor", "Filas"]
    widths = [14, 14, 14, 14, 18, 40]
    for i, (h, w) in enumerate(zip(headers, widths)):
        ws.write(0, i, h, fmt_h2)
        ws.set_column(i, i, w)
    neta = p.get("variacion_items", {}).get("neta_por_codigo") or []
    ws.autofilter(0, 0, len(neta), 5)
    for r, n in enumerate(neta, 1):
        ws.write(r, 0, n.get("codigo_idu") or "", fmt_txt)
        ws.write(r, 1, n.get("H_total") or 0, fmt_num)
        ws.write(r, 2, n.get("I_total") or 0, fmt_num)
        ws.write(r, 3, n.get("delta_cant") or 0, fmt_num)
        ws.write(r, 4, n.get("delta_valor") or 0, fmt_delta)
        ws.write(r, 5, ", ".join(str(x) for x in (n.get("filas") or [])), fmt_txt)

    # ---------- Hoja Variación por CIV (matriz) ----------
    ws = wb.add_worksheet("Variación por CIV")
    ws.freeze_panes(1, 0)
    civs = p.get("variacion_civ", {}).get("resumen_por_civ") or []
    descs = p.get("variacion_civ", {}).get("descomposicion_delta_civ") or []
    dm = {d.get("id"): d for d in descs}
    headers = ["CIV", "Nomenclatura", "Tramo", "SG", "Área m²",
               "Obras iniciales", "Obras finales", "Δ", "Δ %",
               "Δ Aumentos", "Δ Disminuciones", "Δ NP", "Δ Nuevo contractual", "Δ Eliminado"]
    widths = [12, 14, 20, 5, 12, 18, 18, 18, 10, 16, 18, 16, 20, 16]
    for i, (h, w) in enumerate(zip(headers, widths)):
        ws.write(0, i, h, fmt_h2)
        ws.set_column(i, i, w)
    ws.autofilter(0, 0, len(civs), 13)
    for r, c in enumerate(civs, 1):
        d = dm.get(c.get("id"), {})
        ws.write(r, 0, c.get("id"), fmt_txt)
        ws.write(r, 1, c.get("nomenclatura") or "-", fmt_txt)
        ws.write(r, 2, c.get("desde_hasta") or "-", fmt_txt)
        ws.write(r, 3, c.get("subgrupo") or "-", fmt_txt)
        ws.write(r, 4, c.get("area_m2") or 0, fmt_num)
        ws.write(r, 5, c.get("obras_iniciales_aiu") or 0, fmt_money)
        ws.write(r, 6, c.get("obras_finales_aiu") or 0, fmt_money)
        ws.write(r, 7, c.get("delta_aiu") or 0, fmt_delta)
        ws.write(r, 8, (c.get("delta_pct") or 0) / 100 if c.get("delta_pct") is not None else 0, fmt_pct)
        ws.write(r, 9, d.get("delta_por_aumentos") or 0, fmt_money)
        ws.write(r, 10, d.get("delta_por_disminuciones") or 0, fmt_money)
        ws.write(r, 11, d.get("delta_por_np") or 0, fmt_money)
        ws.write(r, 12, d.get("delta_por_contractual_nuevo") or 0, fmt_money)
        ws.write(r, 13, d.get("delta_por_eliminado") or 0, fmt_money)

    # ---------- Hoja Costo por CIV ----------
    ws = wb.add_worksheet("Costo por CIV")
    ws.freeze_panes(1, 0)
    costos = p.get("costo_civ", {}).get("costo_por_civ") or []
    comp = p.get("costo_civ", {}).get("comparativa_v1_v2_v4") or []
    cmap = {c.get("id"): c for c in comp}
    headers = ["CIV", "Nomenclatura", "SG", "Área m²",
               "Obras CD", "Obras+AIU", "Componentes asignados", "Total con AIU",
               "$/m² obras", "$/m² total", "% NP obras",
               "V1 total", "V2 total", "Δ V4-V2"]
    widths = [12, 14, 5, 12, 18, 18, 20, 18, 14, 14, 12, 18, 18, 18]
    for i, (h, w) in enumerate(zip(headers, widths)):
        ws.write(0, i, h, fmt_h2)
        ws.set_column(i, i, w)
    ws.autofilter(0, 0, len(costos), 13)
    for r, c in enumerate(costos, 1):
        cv = cmap.get(c.get("id"), {})
        dv = (c.get("total") or 0) - (cv.get("v2_total") or 0)
        ws.write(r, 0, c.get("id"), fmt_txt)
        ws.write(r, 1, c.get("nomenclatura") or "-", fmt_txt)
        ws.write(r, 2, c.get("subgrupo") or "-", fmt_txt)
        ws.write(r, 3, c.get("area_m2") or 0, fmt_num)
        ws.write(r, 4, c.get("obras_cd") or 0, fmt_money)
        ws.write(r, 5, c.get("obras_total") or c.get("obras_aiu") or 0, fmt_money)
        ws.write(r, 6, c.get("componentes_asignados") or 0, fmt_money)
        ws.write(r, 7, c.get("total") or 0, fmt_money_bold)
        ws.write(r, 8, c.get("dolarm2_obras") or 0, fmt_money)
        ws.write(r, 9, c.get("dolarm2_total") or 0, fmt_money)
        ws.write(r, 10, c.get("pct_np_en_obras") or 0, fmt_pct)
        ws.write(r, 11, cv.get("v1_total") or 0, fmt_money)
        ws.write(r, 12, cv.get("v2_total") or 0, fmt_money)
        ws.write(r, 13, dv, fmt_delta)
    # Totales
    tr = len(costos) + 1
    ws.write(tr, 0, "TOTAL 27 CIVs", fmt_h2)
    ws.write_formula(tr, 5, f"=SUM(F2:F{tr})", fmt_money_bold)
    ws.write_formula(tr, 6, f"=SUM(G2:G{tr})", fmt_money_bold)
    ws.write_formula(tr, 7, f"=SUM(H2:H{tr})", fmt_money_bold)

    # ---------- Hoja NPs ----------
    ws = wb.add_worksheet("NPs")
    ws.freeze_panes(1, 0)
    nps = p.get("nps", {}).get("top20") or []
    headers = ["Fila", "Ítem NP", "Código IDU", "Descripción", "Und",
               "Cantidad", "VU CD", "VU CD+AIU", "Valor con AIU",
               "Capítulo", "Clasificación", "Pregunta contratista"]
    widths = [7, 12, 12, 55, 6, 12, 12, 12, 16, 25, 15, 40]
    for i, (h, w) in enumerate(zip(headers, widths)):
        ws.write(0, i, h, fmt_h2)
        ws.set_column(i, i, w)
    ws.autofilter(0, 0, len(nps), 11)
    for r, n in enumerate(nps, 1):
        ws.write(r, 0, n.get("row") or "", fmt_int)
        ws.write(r, 1, n.get("item_pago") or "", fmt_txt)
        ws.write(r, 2, n.get("codigo_idu") or "-", fmt_txt)
        ws.write(r, 3, n.get("descripcion") or "", fmt_txt)
        ws.write(r, 4, n.get("und") or "", fmt_txt)
        ws.write(r, 5, n.get("cantidad") or 0, fmt_num)
        ws.write(r, 6, n.get("K") or 0, fmt_money)
        ws.write(r, 7, n.get("L") or 0, fmt_money)
        ws.write(r, 8, n.get("valor_aiu") or 0, fmt_money_bold)
        ws.write(r, 9, (n.get("chapter") or "")[:25], fmt_txt)
        ws.write(r, 10, "nuevo", fmt_txt)
        ws.write(r, 11, n.get("pregunta_contratista") or "", fmt_txt)

    # ---------- Hoja Hallazgos ----------
    ws = wb.add_worksheet("Hallazgos")
    ws.freeze_panes(1, 0)
    hall = p.get("hallazgos") or []
    headers = ["ID", "Severidad", "Origen", "Título", "Descripción", "Fuente (hoja)", "Fila", "Impacto $", "Recomendación"]
    widths = [12, 12, 10, 45, 60, 30, 15, 18, 60]
    for i, (h, w) in enumerate(zip(headers, widths)):
        ws.write(0, i, h, fmt_h2)
        ws.set_column(i, i, w)
    ws.autofilter(0, 0, len(hall), 8)
    fmt_alta = wb.add_format({"border": 1, "bg_color": "#fed7d7", "font_color": "#c53030", "bold": True, "align": "center"})
    fmt_media = wb.add_format({"border": 1, "bg_color": "#fefcbf", "font_color": "#975a16", "bold": True, "align": "center"})
    fmt_baja = wb.add_format({"border": 1, "bg_color": "#c6f6d5", "font_color": "#276749", "align": "center"})
    fmt_info = wb.add_format({"border": 1, "bg_color": "#e2e8f0", "font_color": "#4a5568", "align": "center"})
    sev_fmt = {"ALTA": fmt_alta, "MEDIA": fmt_media, "BAJA": fmt_baja, "INFO": fmt_info}
    for r, h in enumerate(hall, 1):
        ws.write(r, 0, h.get("id") or "", fmt_txt)
        ws.write(r, 1, h.get("severidad") or "", sev_fmt.get(h.get("severidad"), fmt_txt))
        ws.write(r, 2, h.get("origen") or "", fmt_txt)
        ws.write(r, 3, h.get("titulo") or "", fmt_txt)
        ws.write(r, 4, h.get("descripcion") or "", fmt_txt)
        ws.write(r, 5, h.get("hoja") or "", fmt_txt)
        ws.write(r, 6, str(h.get("fila") or "") , fmt_txt)
        ws.write(r, 7, h.get("impacto_pesos") or 0, fmt_money)
        ws.write(r, 8, h.get("recomendacion") or "", fmt_txt)

    wb.close()
    print(f"Excel escrito: {OUT}")
    print(f"Tamaño: {OUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
