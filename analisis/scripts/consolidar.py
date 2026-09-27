"""
Consolida los 6 hallazgos en analisis/analisis_2026_09.json y copia
presupuesto_2026_09.json a la raiz para que la app lo cargue.
"""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HALLAZGOS = ROOT / "analisis" / "hallazgos"
OUT = ROOT / "analisis" / "analisis_2026_09.json"
PRES_SRC = ROOT / "analisis" / "datos" / "presupuesto_2026_09.json"
PRES_DST = ROOT / "presupuesto_2026_09.json"

def load(name):
    p = HALLAZGOS / name
    if not p.exists():
        return {}
    return json.load(open(p, encoding="utf-8"))

def slim_matriz(matriz, top_n=200):
    """Reducir la matriz a los top-N renglones por Delta absoluto para no
    inflar el JSON. Deja los demas identificables por row."""
    filtered = []
    for m in matriz:
        total_delta = sum(abs(c.get("delta_valor_aiu", 0) or 0) for c in m["celdas"])
        m2 = dict(m)
        m2["_delta_abs"] = total_delta
        filtered.append(m2)
    filtered.sort(key=lambda x: -x["_delta_abs"])
    return filtered[:top_n]

def main():
    v1 = load("01_variacion_items.json")
    v2 = load("02_variacion_civ.json")
    v3 = load("03_costo_civ.json")
    v4 = load("04_aritmetica.json")
    v5 = load("05_nps.json")
    v6 = load("06_versiones_plazo.json")

    # Consolidacion global de hallazgos
    all_hallazgos = []
    for src_name, src in [("01", v1), ("02", v2), ("03", v3), ("04", v4), ("05", v5), ("06", v6)]:
        for h in src.get("hallazgos", []):
            h["origen"] = src_name
            all_hallazgos.append(h)

    # Ordenar por severidad y luego impacto
    SEV = {"ALTA": 0, "MEDIA": 1, "BAJA": 2, "INFO": 3}
    all_hallazgos.sort(key=lambda h: (SEV.get(h.get("severidad", "INFO"), 4), -abs(h.get("impacto_pesos") or 0)))

    consolidated = {
        "meta": {
            "fuente": "fuentes/4. PRESUPUESTO 01-09-2026 75MM (8 MESES).xlsx",
            "fecha_analisis": "2026-09-26",
            "aiu_contractual": 0.31849,
            "aiu_ambiental_sst": 0.20006,
            "obras_finales_aiu": 58196933800,
            "obras_iniciales_aiu": 44303294799,
            "total_v0": 59426575199,
            "total_v4": 75426575199,
            "adicion_solicitada": 16000000000,
            "plazo_meses_adicion": 8,
        },
        # 01 - Variacion items
        "variacion_items": {
            "resumen": v1.get("resumen"),
            "capitulos": v1.get("capitulos"),
            "subcapitulos": v1.get("subcapitulos"),
            "top_aumentos": v1.get("top_aumentos"),
            "top_disminuciones": v1.get("top_disminuciones"),
            "variacion_relativa_grande": v1.get("variacion_relativa_grande"),
            "saltos_extremos": v1.get("saltos_extremos"),
            "reubicaciones": v1.get("reubicaciones"),
            "reemplazos_np": v1.get("reemplazos_np"),
            "cruce_v2_v4": v1.get("cruce_v2_v4"),
            "items": v1.get("items"),  # todos los renglones
            "neta_por_codigo": v1.get("neta_por_codigo"),
        },
        # 02 - Variacion por CIV
        "variacion_civ": {
            "mapeo_civs": v2.get("mapeo_civs"),
            "conciliacion_total": v2.get("conciliacion_total"),
            "resumen_por_civ": v2.get("resumen_por_civ"),
            "descomposicion_delta_civ": v2.get("descomposicion_delta_civ"),
            "outliers_por_civ": v2.get("outliers_por_civ"),
            "metricas_por_m2": v2.get("metricas_por_m2"),
            "top_delta_por_celda": v2.get("top_delta_por_celda"),
            "matriz_item_civ_top": slim_matriz(v2.get("matriz_item_civ", []), top_n=200),
        },
        # 03 - Costo por CIV
        "costo_civ": {
            "criterio_reparto": v3.get("criterio_reparto"),
            "verificacion_688": v3.get("verificacion_688"),
            "verificacion_total": v3.get("verificacion_total"),
            "costo_por_civ": v3.get("costo_por_civ"),
            "desglose_por_capitulo_civ": v3.get("desglose_por_capitulo_civ"),
            "desglose_np_vs_contractual": v3.get("desglose_np_vs_contractual"),
            "redes_vs_sin_redes": v3.get("redes_vs_sin_redes"),
            "comparativa_v1_v2_v4": v3.get("comparativa_v1_v2_v4"),
            "grupos_hoja1": v3.get("grupos_hoja1"),
            "estadistica_dolarm2": v3.get("estadistica_dolarm2"),
            "outliers": v3.get("outliers"),
        },
        # 04 - Aritmetica y precios
        "aritmetica": {
            "formulas": v4.get("formulas"),
            "duplicados": v4.get("duplicados"),
            "desviaciones_vu_visor": v4.get("desviaciones_vu_visor"),
            "desviaciones_vu_contractual": v4.get("desviaciones_vu_contractual"),
            "efecto_precio_cantidad_total": v4.get("resumen_efecto_precio_cantidad_total"),
            "consistencia_hojas": v4.get("consistencia_hojas"),
            "desviaciones_MNOQ_top": (v4.get("desviaciones_M_N_O_Q") or [])[:20],
            "desviaciones_aiu_L_top": (v4.get("desviaciones_aiu_L") or [])[:20],
        },
        # 05 - NPs
        "nps": {
            "inventario": v5.get("inventario"),
            "objetados_incluidos": v5.get("objetados_incluidos"),
            "nps_glb_mes": v5.get("nps_glb_mes"),
            "top20": v5.get("top20"),
            "clasificacion": v5.get("clasificacion"),
            "cambios_v2_v4": v5.get("cambios_v2_v4"),
            "comparacion_precios": v5.get("comparacion_precios"),
        },
        # 06 - Versiones, componentes, plazo
        "versiones_plazo": {
            "waterfall": v6.get("waterfall"),
            "desvios_analisis": v6.get("desvios_analisis"),
            "sst_detalle": v6.get("sst_detalle"),
            "componentes_sin_cambio": v6.get("componentes_sin_cambio"),
            "acero_diferencia": v6.get("acero_diferencia"),
            "ritmo_mensual": v6.get("ritmo_mensual"),
            "v3_a_v4": v6.get("v3_a_v4"),
        },
        "hallazgos": all_hallazgos,
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(consolidated, f, ensure_ascii=False, indent=1, default=str)
    print(f"Escrito: {OUT}")

    # Copiar presupuesto_2026_09.json a la raiz
    shutil.copy2(PRES_SRC, PRES_DST)
    print(f"Copiado: {PRES_SRC.name} -> {PRES_DST}")
    # La app carga analisis_2026_09.json desde la raiz: mantener ambas copias iguales
    shutil.copy2(OUT, ROOT / OUT.name)
    print(f"Copiado: {OUT.name} -> {ROOT / OUT.name}")

    # Resumen
    print()
    print(f"Consolidado con {len(all_hallazgos)} hallazgos:")
    from collections import Counter
    sev_counts = Counter(h.get("severidad", "?") for h in all_hallazgos)
    for sev in ["ALTA", "MEDIA", "BAJA", "INFO"]:
        print(f"  {sev}: {sev_counts.get(sev, 0)}")


if __name__ == "__main__":
    main()
