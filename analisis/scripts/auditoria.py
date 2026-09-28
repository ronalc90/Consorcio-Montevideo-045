"""
Registro de auditoría del análisis del presupuesto 01-09-2026 (75MM · 8 meses).

Genera, a partir del Excel radicado y de los JSON del análisis, un registro
reproducible con cuatro tipos de asiento:

  A  Errores e inconsistencias en la FUENTE (el Excel del contratista)
  B  Correcciones hechas al ANÁLISIS (con el commit que las introdujo)
  C  Dudas ABIERTAS que deben resolver el contratista o el IDU
  D  LIMITACIONES del análisis (lo que el revisor debe saber antes de citar una cifra)

y un paquete de auditoría (hashes SHA-256, versiones, comandos de reproducción).

Toda la evidencia numérica de la sección A se calcula aquí, leyendo el libro con
openpyxl (fórmulas y valores guardados), de modo que un tercero pueda repetirla.

Salidas:
  analisis/auditoria/registro_auditoria.json
  analisis/auditoria/registro_auditoria.csv
  analisis/REGISTRO_AUDITORIA.md

Uso: python analisis/scripts/auditoria.py
"""
import csv
import difflib
import hashlib
import json
import platform
import re
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

import openpyxl
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[2]
XLSX = ROOT / "fuentes" / "4. PRESUPUESTO 01-09-2026 75MM (8 MESES).xlsx"
OUT_DIR = ROOT / "analisis" / "auditoria"
OUT_JSON = OUT_DIR / "registro_auditoria.json"
OUT_CSV = OUT_DIR / "registro_auditoria.csv"
OUT_MD = ROOT / "analisis" / "REGISTRO_AUDITORIA.md"
HOJA = "PRESUPUESTO TODOS LOS CIV 84 NP"
AIU = 1.31849
FECHA = "2026-09-28"

TOTAL_OBRAS = 58_196_933_800
TOTAL_V4 = 75_426_575_199
TOTAL_V0 = 59_426_575_199


# ─────────────────────────────── utilidades ───────────────────────────────
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def num(v):
    if v is None or isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(str(v).replace(",", "").strip())
    except Exception:
        return None


def fmt(n):
    if n is None:
        return "-"
    neg = n < 0
    n = abs(n)
    if abs(n - round(n)) < 1e-9:
        s = f"{int(round(n)):,}".replace(",", ".")
    else:
        s = f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("-" if neg else "") + s


def norm_txt(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    s = s.upper().replace("PESOS M/CTE", "").replace("PESOS", "")
    s = re.sub(r"\s+", " ", s).strip()
    s = s.replace("UNO MIL", "UN MIL").replace("VEINTIUNO MIL", "VEINTIUN MIL").replace("VEINTI UN", "VEINTIUN")
    return s


def git(*args):
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    except Exception:
        return ""


# ─────────────────────────────── carga ───────────────────────────────
print("Leyendo libro (fórmulas y valores)...")
wbf = openpyxl.load_workbook(XLSX, data_only=False)
wbv = openpyxl.load_workbook(XLSX, data_only=True)
wsf, wsv = wbf[HOJA], wbv[HOJA]
pres = json.load(open(ROOT / "presupuesto_2026_09.json", encoding="utf-8"))
data = json.load(open(ROOT / "data.json", encoding="utf-8"))
h04 = json.load(open(ROOT / "analisis" / "hallazgos" / "04_aritmetica.json", encoding="utf-8"))
h02 = json.load(open(ROOT / "analisis" / "hallazgos" / "02_variacion_civ.json", encoding="utf-8"))
h06 = json.load(open(ROOT / "analisis" / "hallazgos" / "06_versiones_plazo.json", encoding="utf-8"))
items = pres["items"]
civ_sub = {c["id"]: str(c["subgrupo"]) for c in pres["civs"]}

links = {i + 1: (el.file_link.Target if el.file_link is not None else "?") for i, el in enumerate(wbf._external_links)}


def f(cell):  # fórmula (o constante) de la hoja principal
    return wsf[cell].value


def v(cell):  # valor guardado de la hoja principal
    return wsv[cell].value


def ext_cells(ws):
    out = []
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("=") and "[" in c.value:
                out.append(c)
    return out


registro = []


def add(tipo, sev, titulo, detalle, *, categoria, evidencia=None, impacto=None, tratamiento="", estado, responsable, pregunta="", soporte="", commit="", verificable="", hallazgo=""):
    n = sum(1 for r in registro if r["tipo"] == tipo) + 1
    registro.append({
        "id": f"{tipo}-{n:02d}", "tipo": tipo, "categoria": categoria, "severidad": sev, "titulo": titulo, "detalle": detalle,
        "evidencia": evidencia or [], "impacto_pesos": impacto, "tratamiento": tratamiento, "estado": estado, "responsable": responsable,
        "pregunta": pregunta, "soporte_a_pedir": soporte, "commit": commit, "verificable_con": verificable, "hallazgo_relacionado": hallazgo, "fecha": FECHA,
    })


# ══════════════════════════ A · FUENTE ══════════════════════════
# A-01 base de precios unitarios vinculada a un libro externo
cons_f = wbf["CONSOLIDADO CTO 1752 AJUSTADO"]
cons_ext = ext_cells(cons_f)
cons_cols = Counter(c.column_letter for c in cons_ext)
cons_targets = Counter(int(m) for c in cons_ext for m in re.findall(r"\[(\d+)\]", c.value))
k_formula = Counter()
k_const_rows = []
for r in range(7, 680):
    kv = f(f"K{r}")
    if isinstance(kv, str) and kv.startswith("="):
        k_formula["formula"] += 1
    elif kv in (None, ""):
        k_formula["vacio"] += 1
    else:
        k_formula["constante"] += 1
        k_const_rows.append(r)
add("A", "ALTA", "La base de precios unitarios (columna K) depende de un libro externo que no viene en el archivo",
    "La columna K (VU costo directo) de la hoja principal se calcula con VLOOKUP sobre la hoja oculta CONSOLIDADO CTO 1752 AJUSTADO, columna 16 (Q, 'VALOR ITEM COSTO DIRECTO ACTUALIZACION'). "
    f"Esa columna Q es a su vez un VLOOKUP a un libro externo ('[190]OBRAS CIVILES'!C2:Q234, columna 14) que no está en el archivo radicado: {links.get(190, '?')}. "
    f"Sin ese libro los VU no se pueden recalcular: lo que se ve son valores guardados ('congelados'). Celdas con vínculo externo en CONSOLIDADO: {dict(cons_cols)}. "
    f"Filas de la hoja principal con K por fórmula: {k_formula['formula']}; con K digitado como constante: {k_formula['constante']} (ver A-03).",
    categoria="trazabilidad",
    evidencia=[{"hoja": HOJA, "celda": "K8", "formula": f("K8"), "valor": v("K8")},
               {"hoja": "CONSOLIDADO CTO 1752 AJUSTADO", "celda": "Q12", "formula": cons_f["Q12"].value, "valor": wbv["CONSOLIDADO CTO 1752 AJUSTADO"]["Q12"].value},
               {"vinculo_externo": 190, "destino": links.get(190, "?")},
               {"vinculo_externo": 188, "destino": links.get(188, "?"), "uso": "hoja PRESUPUESTO CONTRACTUAL MAYO 25 (columna Q)"}],
    tratamiento="El análisis usa los valores guardados de K (los mismos que muestra Excel al abrir sin actualizar vínculos). La comparación de VU (sección H de la app) se hace contra la columna 'actualización APU 13-09-2024' de la hoja PRESUPUESTO CONTRACTUAL MAYO 25 y contra el VISOR 07-05-25 (data.json).",
    estado="ABIERTO", responsable="Contratista",
    pregunta="¿Cuál es el libro 'ANEXO APU MODIF 28-07-2025.xlsx' y qué VISOR/insumos usa? ¿Fue revisado por la interventoría y aprobado por el IDU como base de precios de la adición?",
    soporte="Libro ANEXO APU MODIF 28-07-2025.xlsx completo; APU FO-GI-19 de cada ítem con VU distinto al contractual; acta o comunicación IDU que autorice la actualización de VU.",
    verificable="openpyxl: wb['PRESUPUESTO TODOS LOS CIV 84 NP']['K8'].value ; wb['CONSOLIDADO CTO 1752 AJUSTADO']['Q12'].value ; wb._external_links[189].file_link.Target",
    hallazgo="H03 (análisis 04)")

# A-02 cantidades por CIV vinculadas a libros externos
main_ext = ext_cells(wsf)
by_row = defaultdict(list)
for c in main_ext:
    by_row[c.row].append(c)
ev = []
for r, cells in sorted(by_row.items()):
    tgt = sorted({int(m) for c in cells for m in re.findall(r"\[(\d+)\]", c.value)})
    ev.append({"hoja": HOJA, "fila": r, "codigo": v(f"B{r}"), "item": str(v(f"C{r}")), "descripcion": str(v(f"F{r}"))[:70], "celdas": len(cells),
               "ejemplo": f"{cells[0].coordinate} {cells[0].value}", "cant_final_I": v(f"I{r}"), "valor_M": v(f"M{r}"), "libros": [links.get(t, "?") for t in tgt]})
add("A", "ALTA", f"{len(main_ext)} cantidades por CIV de la hoja principal están vinculadas a libros externos no entregados",
    f"Las cantidades por CIV del NP-101 'Transporte de material fresado' (filas 29 y 59, {len(by_row[29]) + len(by_row[59])} celdas) se leen del libro externo "
    f"'PRESUPUESTO TOTAL $80 MIL.xlsx' ({links.get(186, '?')}), hojas CALCULO ESTRUCTURA y CALCULO DE ANDENES. Las filas 489, 510 y 511 (ductos ENEL/TDP, {len(by_row[489]) + len(by_row[510]) + len(by_row[511])} celdas, todas en 0) "
    f"se leen del acta de competencia ENEL del 03-10-2025 ({links.get(187, '?')}). El nombre del primer libro ('$80 MIL') sugiere una versión del presupuesto cercana a $80.000 millones que no fue radicada. "
    "Los valores que se ven son los guardados en el último recálculo del contratista.",
    categoria="trazabilidad", evidencia=ev,
    impacto=round((v("M29") or 0) + (v("M59") or 0)),
    tratamiento="Se toman los valores guardados. El NP-101 queda marcado en la ficha del ítem y en la lista de chequeo como cantidad de origen externo.",
    estado="ABIERTO", responsable="Contratista",
    pregunta="¿Qué es 'PRESUPUESTO TOTAL $80 MIL.xlsx'? ¿Hubo una versión del presupuesto de $80.000M? ¿Las memorias CALCULO ESTRUCTURA / CALCULO DE ANDENES del libro radicado (hojas ocultas) son las mismas que las del libro externo?",
    soporte="Libro PRESUPUESTO TOTAL $80 MIL.xlsx y memoria de cantidades del NP-101 por CIV; acta de competencia ENEL 03-10-2025.",
    verificable="openpyxl: [c.coordinate for c in ws.iter_rows() ... if '[' in str(c.value)] sobre la hoja principal → 81 celdas", hallazgo="")

# A-03 VU digitados a mano
cons_v = wbv["CONSOLIDADO CTO 1752 AJUSTADO"]
cons_q = {}
for r in range(11, cons_v.max_row + 1):
    code = cons_v.cell(r, 2).value
    if code not in (None, ""):
        cons_q.setdefault(str(code).strip(), cons_v.cell(r, 17).value)  # Q
kc = []
for r in k_const_rows:
    code = str(v(f"B{r}") or "").strip()
    item = str(v(f"C{r}") or "")
    is_np = item.startswith("NP") or code.upper() in ("N/A", "NO", "")
    kval = num(v(f"K{r}"))
    ref = num(cons_q.get(code)) if code in cons_q else None
    kc.append({"fila": r, "codigo": code, "item": item[:8], "descripcion": str(v(f"F{r}"))[:60], "und": v(f"G{r}"), "K": kval, "K_consolidado": ref,
               "difiere_de_consolidado": (ref is not None and kval is not None and abs(kval - ref) > 0.5), "es_np": is_np, "valor_M": num(v(f"M{r}")) or 0})
kc_np = [x for x in kc if x["es_np"]]
kc_con = [x for x in kc if not x["es_np"]]
kc_dif = [x for x in kc_con if x["difiere_de_consolidado"]]
kc_sin = [x for x in kc_con if x["K_consolidado"] is None]
add("A", "ALTA" if kc_dif else "MEDIA", f"{len(k_const_rows)} renglones tienen el VU (K) digitado como constante en vez de fórmula",
    f"De los {len(k_const_rows)} renglones con K constante, {len(kc_np)} son NP (no existen en CONSOLIDADO, así que el VU tiene que venir de un APU nuevo) y {len(kc_con)} son códigos contractuales. "
    f"De estos últimos, {len(kc_sin)} no aparecen en CONSOLIDADO y {len(kc_dif)} tienen un K distinto al que daría la fórmula (VLOOKUP a CONSOLIDADO Q). "
    f"Valor con AIU de los renglones con K constante: {fmt(sum(x['valor_M'] for x in kc))}; solo NP: {fmt(sum(x['valor_M'] for x in kc_np))}.",
    categoria="precios",
    evidencia=sorted(kc, key=lambda x: -x["valor_M"])[:40],
    impacto=round(sum(x["valor_M"] for x in kc)),
    tratamiento="Los VU de los NP se contrastan con V2 (comparativa.json) en la sección de NPs; los contractuales con K constante quedan listados aquí para que el revisor pida el soporte.",
    estado="ABIERTO", responsable="Contratista",
    pregunta="Para cada renglón con VU digitado: ¿de qué APU sale el valor y quién lo aprobó? Si el código existe en CONSOLIDADO, ¿por qué no se usa la fórmula?",
    soporte="APU FO-GI-19 de los 84 NP y de los códigos contractuales con VU digitado; comunicación de aprobación de VU por la interventoría/IDU.",
    verificable="openpyxl: [r for r in range(7,680) if not str(ws[f'K{r}'].value).startswith('=') and ws[f'K{r}'].value not in (None,'')]", hallazgo="")

# A-04 totales por subgrupo (/2) y control de CIVs
sum_sg = {"2": 0.0, "5": 0.0}
row_diff = []
ITEMS_OBRAS = [it for it in items if it["row"] < 680]  # el bloque ACEROS (680-687) está fuera de M688
for it in ITEMS_OBRAS:
    s = 0.0
    for cid, d in (it.get("civ") or {}).items():
        val = d.get("valor") or 0
        s += val
        sub = civ_sub.get(cid)
        if sub in sum_sg:
            sum_sg[sub] += val
    m = it.get("valor_actualizado_aiu") or 0
    if abs(s - m) > 0.5:
        row_diff.append({"fila": it["row"], "codigo": it["codigo_idu"], "M": m, "suma_civ": round(s, 2), "delta": round(s - m, 2)})
AH, BY, CB, M688 = num(v("AH688")), num(v("BY688")), num(v("CB688")), num(v("M688"))
ej = wbv["EJECUTIVO"]
add("A", "MEDIA", "El total del subgrupo 5 (BY688) no coincide con la suma de sus CIVs y AH688 + BY688 no da CB688",
    f"Los totales por CIV en la fila 688 usan la fórmula SUM(col7:col679)/2: se divide entre dos porque las filas de subtotal de capítulo repiten el valor de sus ítems. El truco solo cuadra si cada ítem está cubierto exactamente una vez por un subtotal. "
    f"Resultado: BY688 (SG5) = {fmt(BY)} frente a la suma de los CIV del subgrupo 5 = {fmt(sum_sg['5'])} (Δ {fmt(BY - sum_sg['5'])}); AH688 (SG2) = {fmt(AH)} frente a {fmt(sum_sg['2'])} (Δ {fmt(AH - sum_sg['2'])}); "
    f"AH688 + BY688 = {fmt(AH + BY)} ≠ CB688 = {fmt(CB)} (Δ {fmt(AH + BY - CB)}). CB688 sí coincide con M688 = {fmt(M688)}. La hoja EJECUTIVO usa {fmt(num(ej['H40'].value))} como total del subgrupo 5 (H40) y {fmt(num(ej['I45'].value))} de obras (I45): suma de los CIV redondeados, no la fila 688.",
    categoria="aritmética",
    evidencia=[{"hoja": HOJA, "celda": "BY688", "formula": f("BY688"), "valor": BY, "esperado_suma_civ_sg5": round(sum_sg["5"], 2)},
               {"hoja": HOJA, "celda": "AH688", "formula": f("AH688"), "valor": AH, "esperado_suma_civ_sg2": round(sum_sg["2"], 2)},
               {"hoja": HOJA, "celda": "CB688", "formula": f("CB688"), "valor": CB}, {"hoja": HOJA, "celda": "M688", "formula": f("M688"), "valor": M688},
               {"hoja": HOJA, "celda": "T688", "formula": f("T688")}],
    impacto=round(abs(BY - sum_sg["5"])),
    tratamiento="El análisis no usa la fila 688 por CIV: suma los renglones ítem × CIV (presupuesto_2026_09.json) y verifica contra M688 (Δ +69 por redondeo, ver A-12).",
    estado="ABIERTO", responsable="Contratista",
    pregunta="¿Cuál es el total oficial del subgrupo 5: 43.258.118.071,5 (BY688) o 43.258.244.367 (suma de CIVs / EJECUTIVO)? Corregir la fórmula /2 por una suma directa de renglones.",
    soporte="Libro corregido con totales por CIV calculados por SUMIF sobre renglones de ítem.",
    verificable="python analisis/scripts/verificacion.py (sección 6) y este script (sum_sg)", hallazgo="H03-01")

# A-05 bloque aceros vs bolsa F
bloque = sum((num(v(f"M{r}")) or 0) for r in range(682, 688) if isinstance(v(f"M{r}"), (int, float)))
bolsa = num(v("M697"))
add("A", "MEDIA", "Bloque ACEROS (filas 680-687) fuera del total de obras, con $75,5M más que la bolsa fija F",
    f"El bloque ACEROS reparte acero de refuerzo, acero liso y dovelas por CIV con cantidades actualizadas y suma {fmt(bloque)} con AIU (M682:M687). Está fuera del rango de M688 = {f('M688')}, así que no está dentro de los {fmt(TOTAL_OBRAS)}. "
    f"El acero se paga por la bolsa fija F (fila 697) de {fmt(bolsa)}, igual desde la firma. Diferencia bloque − bolsa = {fmt(bloque - bolsa)}. Si el bloque es la memoria de la bolsa, la bolsa queda corta; si es alcance adicional, requiere adición.",
    categoria="alcance",
    evidencia=[{"hoja": HOJA, "celda": "M688", "formula": f("M688")}, {"hoja": HOJA, "celda": "M697", "valor": bolsa},
               *[{"hoja": HOJA, "fila": r, "codigo": v(f"B{r}"), "descripcion": str(v(f"F{r}"))[:50], "H": v(f"H{r}"), "I": v(f"I{r}"), "M": v(f"M{r}")} for r in range(680, 688)]],
    impacto=round(bloque - bolsa),
    tratamiento="Hallazgo H06-01 reescrito (ver B-08). La app lo muestra en la ficha del componente F, en el resumen ejecutivo y en la lista de chequeo.",
    estado="ABIERTO", responsable="Contratista",
    pregunta="¿El bloque ACEROS es la memoria de cantidades de la bolsa F o alcance adicional? ¿Por qué la memoria de la hoja Aceros (~$2.500M teóricos) es menor que el bloque?",
    soporte="Memoria de acero por CIV (kg por elemento) conciliada con la bolsa F; constancia en el otrosí de que el acero se paga por una sola vía.",
    verificable="openpyxl: ws['M688'].value == '=SUM(M8:M679)'; sum(ws[f'M{r}'].value for r in 682..687)", hallazgo="H06-01")

# A-06 ítem 8643 (5.037)
contr_v = wbv["PRESUPUESTO CONTRACTUAL MAYO 25"]
contr = {}
for r in range(1, contr_v.max_row + 1):
    code = contr_v.cell(r, 2).value
    if code not in (None, ""):
        contr.setdefault(str(code).strip(), {"fila": r, "und": contr_v.cell(r, 7).value, "cant": contr_v.cell(r, 8).value, "vu": contr_v.cell(r, 9).value, "desc": str(contr_v.cell(r, 6).value)[:90]})
visor_v = wbv["VISOR 07-05-25"]
visor_codes = {str(visor_v.cell(r, 2).value).strip() for r in range(1, visor_v.max_row + 1) if visor_v.cell(r, 2).value not in (None, "")}
rows_8643 = [it for it in items if str(it["codigo_idu"]) == "8643"]
val_8643 = sum((it["valor_actualizado_aiu"] or 0) for it in rows_8643)
c8643 = contr.get("8643", {})
add("A", "ALTA", "Ítem 8643 (5.037): descripción de consultoría, unidad cambiada (M2/MES → M2) y VU +33,8 %, por $2.718M",
    f"El código 8643 aparece en {len(rows_8643)} filas ({', '.join(str(it['row']) for it in rows_8643)}) con la descripción '{rows_8643[0]['descripcion'][:95]}…', que corresponde a un estudio o diseño, no a una obra de redes. "
    f"En la hoja PRESUPUESTO CONTRACTUAL MAYO 25 (fila {c8643.get('fila')}) el mismo código tiene unidad '{c8643.get('und')}', cantidad {fmt(num(c8643.get('cant')))} y VU {fmt(num(c8643.get('vu')))}; en V4 la unidad es 'M2', el VU es {fmt(rows_8643[0]['vu_cd'])} "
    f"({(rows_8643[0]['vu_cd'] / num(c8643.get('vu')) - 1) * 100:.1f} %) y las cantidades pasan de {fmt(sum(it['cant_contractual'] or 0 for it in rows_8643))} a {fmt(sum(it['cant_actualizada'] or 0 for it in rows_8643))}. "
    f"El código {'NO está' if '8643' not in visor_codes else 'está'} en el VISOR 07-05-25. Valor V4 con AIU: {fmt(val_8643)}.",
    categoria="alcance",
    evidencia=[{"hoja": HOJA, "fila": it["row"], "subcapitulo": it.get("subchapter"), "und": it["und"], "H": it["cant_contractual"], "I": it["cant_actualizada"], "K": it["vu_cd"], "M": it["valor_actualizado_aiu"]} for it in rows_8643]
    + [{"hoja": "PRESUPUESTO CONTRACTUAL MAYO 25", **c8643}],
    impacto=round(val_8643),
    tratamiento="Se analiza como cualquier ítem (aparece en las fichas y en la sección H de precios). Se deja aquí como duda prioritaria porque la descripción no permite saber qué se está pagando.",
    estado="ABIERTO", responsable="Contratista",
    pregunta="¿Qué obra se paga con el código 8643? ¿Por qué la descripción es la de un estudio de factibilidad/diseño? ¿Por qué cambió la unidad de M2/MES a M2 y el VU de 37.694 a 50.435?",
    soporte="Especificación particular, APU y memoria de cantidades del 8643 por CIV; acta que autorice el cambio de unidad.",
    verificable="python: [it for it in pres['items'] if it['codigo_idu']=='8643']", hallazgo="")

# A-07 ajustes por cambio de vigencia sin recálculo
res = wbv["resumen"]
add("A", "MEDIA", "'Ajustes por cambio de vigencia' ($4.555M) no se recalcula pese a que la adición lleva la obra a la vigencia 2027",
    f"La hoja resumen muestra el componente E con valor actual {fmt(num(res['D11'].value))}, adición {fmt(num(res['E11'].value))} y total {fmt(num(res['F11'].value))}. El componente fue dimensionado en la firma (2021) para el plazo original; "
    "8 meses adicionales desde el vencimiento actual llevan la ejecución a 2027, y el manual IDU GUDP017 prevé el ajuste de precios por cambio de vigencia con el ICCP. Ni el componente E ni los VU incluyen ese efecto.",
    categoria="alcance",
    evidencia=[{"hoja": "resumen", "celda": "D11:F11", "valores": [res["D11"].value, res["E11"].value, res["F11"].value]}, {"hoja": HOJA, "celda": "M695", "valor": v("M695")}],
    impacto=None,
    tratamiento="El simulador (sección J) permite un recálculo ilustrativo; el informe lo lista como pregunta. No se estima un valor porque depende del cronograma real.",
    estado="ABIERTO", responsable="Contratista / IDU",
    pregunta="¿La adición incluye o excluye ajustes por cambio de vigencia para 2027? Si los excluye, ¿quién asume el mayor valor y con qué fórmula (ICCP)?",
    soporte="Cronograma de la adición por vigencia y cálculo del ajuste según GUDP017.", verificable="openpyxl: wb['resumen']['E11'].value == 0", hallazgo="")

# A-08 bioseguridad
add("A", "MEDIA", "Bioseguridad ($59,4M) no se extiende a los 8 meses aunque es proporcional al plazo",
    f"M699 = {fmt(num(v('M699')))} igual que en V0 (resumen E15 = {fmt(num(res['E15'].value))}). PMA-SST, diálogo y PMT sí se recalculan por 8 meses.",
    categoria="alcance", evidencia=[{"hoja": HOJA, "celda": "M699", "valor": v("M699")}, {"hoja": "resumen", "celda": "E15", "valor": res["E15"].value}],
    impacto=40_000_000,
    tratamiento="Hallazgo H06-04 (MEDIA, impacto estimado ~$40M = 59,4M × 8/12 aprox.).",
    estado="ABIERTO", responsable="Contratista",
    pregunta="¿El contratista renuncia expresamente a pedir bioseguridad por el plazo adicional o el renglón debe incorporarse?",
    soporte="Comunicación del contratista.", verificable="openpyxl: ws['M699'].value", hallazgo="H06-04")

# A-09 fondo de compensaciones
add("A", "MEDIA", "El Fondo de Compensaciones apareció en V2 ($5.943M) y vuelve a 0 en V4 sin trazabilidad",
    "En la propuesta del 21-04-2026 (V2) el contratista incluyó un Fondo de Compensaciones de 5.942.657.520; en V3 y V4 el componente K vale 0 (M700). No hay comunicación que explique su origen ni su retiro; "
    "podría relacionarse con compensaciones ambientales o arqueológicas que ahora aparecen como NP dentro de obras.",
    categoria="trazabilidad", evidencia=[{"hoja": HOJA, "celda": "M700", "valor": v("M700")}, {"fuente": "comparativa.json (V2)", "fondo_compensaciones": 5942657520}],
    impacto=5_942_657_520,
    tratamiento="Hallazgo H06-06; waterfall V0→V4 lo muestra como componente que entra y sale.",
    estado="ABIERTO", responsable="Contratista",
    pregunta="¿Qué compensaciones financiaba el fondo de V2, por qué se retiró y dónde quedaron esos costos (NP-109/NP-110 arqueología)?",
    soporte="Trazabilidad documental del componente K entre V2, V3 y V4.", verificable="comparativa.json → globales; ws['M700']", hallazgo="H06-06")

# A-10 O690
o690_refs = [c.coordinate for row in wsf.iter_rows() for c in row if isinstance(c.value, str) and "O690" in c.value]
add("A", "BAJA", "Celda O690 con una constante mal digitada (…779 en vez de …799): 58.196.933.780",
    f"O690 = {f('O690')} = {fmt(num(v('O690')))}, frente a N688 + Q688 = {fmt(num(v('N689')))} (N689). El primer sumando debía ser 44.303.294.799 (N688). "
    f"Celdas que referencian O690: {o690_refs or 'ninguna'} → es una celda de control sin efecto en los totales.",
    categoria="aritmética", evidencia=[{"hoja": HOJA, "celda": "O690", "formula": f("O690"), "valor": v("O690")}, {"hoja": HOJA, "celda": "N689", "formula": f("N689"), "valor": v("N689")}],
    impacto=round(num(v("N689")) - num(v("O690"))),
    tratamiento="Sin efecto en el análisis; se documenta como indicio de digitación manual en celdas de control.",
    estado="DOCUMENTADO", responsable="Contratista", pregunta="Corregir la celda o eliminarla.", verificable="openpyxl: ws['O690'].value", hallazgo="")

# A-11 fila 34
d34 = [d for d in h04.get("desviaciones_M_N_O_Q", [])]
add("A", "BAJA", f"Fila {d34[0]['row'] if d34 else 34}: N y O se desvían $86.217 de la fórmula (valor inicial = H × L)",
    f"N{d34[0]['row'] if d34 else 34} = {fmt(d34[0]['actual']) if d34 else '-'} frente a H × L = {fmt(d34[0]['esperado']) if d34 else '-'} (Δ {fmt(d34[0]['delta']) if d34 else '-'}); O compensa con el mismo Δ negativo. "
    f"Fórmula de N34: {f('N34')} ; O34: {f('O34')} ; H34 = {v('H34')} ; L34 = {v('L34')}. El total Q (M − N) no se ve afectado.",
    categoria="aritmética",
    evidencia=[{"hoja": HOJA, "celda": "N34", "formula": f("N34"), "valor": v("N34")}, {"hoja": HOJA, "celda": "O34", "formula": f("O34"), "valor": v("O34")}, {"hoja": HOJA, "celda": "H34", "valor": v("H34")}, {"hoja": HOJA, "celda": "L34", "valor": v("L34")}, {"hoja": HOJA, "celda": "M34", "valor": v("M34")}],
    impacto=86_217, tratamiento="Detectado por el análisis 04 (H01). La verificación global cuadra con tolerancia de $86.217 por esta fila.",
    estado="DOCUMENTADO", responsable="Contratista", pregunta="Confirmar si H34 o L34 fueron modificados después de calcular N34 (¿celda pegada como valor?).", verificable="python analisis/scripts/analisis_04.py → desviaciones_M_N_O_Q", hallazgo="H01 (análisis 04)")

# A-12 redondeo por CIV
tot_civ = sum(sum((d.get("valor") or 0) for d in (it.get("civ") or {}).values()) for it in ITEMS_OBRAS)
add("A", "BAJA", f"Redondeo por CIV: la suma de los 27 CIV da {fmt(tot_civ)} frente a {fmt(M688)} (Δ {fmt(tot_civ - M688)})",
    f"Cada celda de valor por CIV es ROUND(cantidad_CIV × L, 0) y el total del renglón es ROUND(L × I, 0); las dos rutas difieren en unos pesos por renglón. Renglones con diferencia: {len(row_diff)}; "
    f"máxima diferencia por renglón: {fmt(max((abs(x['delta']) for x in row_diff), default=0))}. La hoja EJECUTIVO (que suma CIV) muestra por eso {fmt(num(ej['I45'].value))} de obras y {fmt(num(ej['I56'].value))} de total (Δ +69).",
    categoria="aritmética", evidencia=row_diff[:30] + [{"hoja": "EJECUTIVO", "celda": "I45", "valor": ej["I45"].value}, {"hoja": "EJECUTIVO", "celda": "I56", "valor": ej["I56"].value}],
    impacto=round(tot_civ - M688), tratamiento="verificacion.py acepta Δ ≤ $100 y lo reporta; todas las cifras del análisis citan M688 / M703 como totales oficiales.",
    estado="DOCUMENTADO", responsable="Analista", pregunta="", verificable="python analisis/scripts/verificacion.py (sección 6)", hallazgo="H03-01, H03-02")

# A-13 etiquetas con fecha vieja
add("A", "BAJA", "Etiquetas con fecha desactualizada: fila 703 '04-05-2026' y EJECUTIVO '11/05/2026' en un archivo del 01-09-2026",
    f"B703 = '{v('B703')}'; EJECUTIVO!C1 = '{ej['C1'].value}'. El nombre del archivo y el radicado son del 01-09-2026 (versión 75MM · 8 meses). Indica que el libro se construyó sobre la versión de mayo (63MM) sin actualizar rótulos.",
    categoria="etiqueta", evidencia=[{"hoja": HOJA, "celda": "B703", "valor": v("B703")}, {"hoja": "EJECUTIVO", "celda": "C1", "valor": ej["C1"].value}],
    impacto=None, tratamiento="Hallazgo H06-08 (BAJA). Sin efecto numérico.", estado="DOCUMENTADO", responsable="Contratista", pregunta="Actualizar los rótulos en la versión que se anexe al otrosí.", verificable="openpyxl", hallazgo="H06-08")

# A-14 cifras en letras
try:
    from num2words import num2words
except Exception:
    num2words = None
pe = wbv["Presupuesto estimado"]
letras = []
for r in range(1, pe.max_row + 1):
    a, b = pe.cell(r, 1).value, pe.cell(r, 2).value
    if isinstance(a, (int, float)) and isinstance(b, str) and "PESO" in b.upper():
        esperado = norm_txt(num2words(int(a), lang="es")) if num2words else ""
        actual = norm_txt(b)
        ratio = difflib.SequenceMatcher(None, esperado, actual).ratio() if esperado else None
        letras.append({"hoja": "Presupuesto estimado", "celda": f"B{r}", "numero": int(a), "texto": b.strip(), "esperado": esperado, "similitud": round(ratio, 3) if ratio is not None else None, "ok": (esperado == actual) if esperado else None})
malas = [x for x in letras if x["ok"] is False]
add("A", "BAJA", f"Cifras en letras del 'Presupuesto estimado': {len(malas)} de {len(letras)} no coinciden con el número",
    "La hoja Presupuesto estimado escribe cada valor en letras (texto que suele copiarse al otrosí). " + ("; ".join(f"{x['celda']}: '{x['texto'][:60]}…' vs {fmt(x['numero'])}" for x in malas) if malas else "Todas coinciden.")
    + " Comparación exacta tras normalizar acentos, espacios y 'PESOS M/CTE' (num2words, lang=es).",
    categoria="etiqueta", evidencia=letras, impacto=None,
    tratamiento="Sin efecto numérico. Se lista para que el texto del otrosí no herede el error.", estado="DOCUMENTADO", responsable="Contratista", pregunta="Corregir los textos en letras antes de firmar.",
    verificable="python: num2words(n, lang='es') vs hoja Presupuesto estimado", hallazgo="")

# A-15 NP: 84 códigos, 81 con cantidad
np_rows = [it for it in items if str(it.get("item_pago", "")).startswith("NP")]
np_codes = defaultdict(list)
for it in np_rows:
    np_codes[str(it["item_pago"])].append(it)
np_sin = sorted(k for k, rs in np_codes.items() if all(not (r["cant_actualizada"] or 0) for r in rs))
np_rows_0 = [it for it in np_rows if not (it["cant_actualizada"] or 0)]
add("A", "INFO", f"'84 NP' del nombre de la hoja = {len(np_codes)} códigos NP listados; {len(np_codes) - len(np_sin)} tienen cantidad ({len(np_rows) - len(np_rows_0)} renglones) y {len(np_sin)} nunca se cuantifican",
    f"Renglones NP: {len(np_rows)}; con cantidad 0 en V4: {len(np_rows_0)} (quedan como plantilla). NP sin cantidad en ninguna fila: {', '.join(np_sin)}. "
    "Los renglones en 0 no suman, pero dejan abierta la puerta a incorporarlos después sin nuevo trámite.",
    categoria="estructura", evidencia=[{"np": k, "filas": [r["row"] for r in rs], "descripcion": rs[0]["descripcion"][:70]} for k, rs in np_codes.items() if k in np_sin] + [{"renglones_np_en_cero": [r["row"] for r in np_rows_0]}],
    impacto=None, tratamiento="El análisis cuenta 105 renglones NP con cantidad, 81 códigos, $14.150.924.549 con AIU (verificado al peso).",
    estado="DOCUMENTADO", responsable="Contratista", pregunta="¿Los NP en cero se retiran del anexo del otrosí o se dejan como 'aprobados sin cantidad'?", verificable="python: agrupar pres['items'] por item_pago NP", hallazgo="H-NP-06")

# A-16 alias CIV
ids_xl = [str(wsv.cell(3, c).value) for c in range(19, 80) if wsv.cell(3, c).value not in (None, "")]
ids_dj = [c["id"] for c in data["civs"]]
add("A", "INFO", "Identificadores de CIV: 500002375 en la hoja principal frente a 50002375 en el VISOR/dashboard (y 16004876 en la comparativa de abril)",
    f"Fila 3 de la hoja principal: {len(ids_xl)} CIV ({', '.join(sorted(set(ids_xl) - set(ids_dj)) or ['-'])} no está en data.json); data.json: {', '.join(sorted(set(ids_dj) - set(ids_xl)) or ['-'])} no está en el Excel. "
    "Es el mismo tramo (KR 65A). El código SEG de la fila 4 sí coincide.",
    categoria="estructura", evidencia=[{"hoja": HOJA, "fila": 3, "ids": ids_xl}, {"fuente": "data.json", "ids": ids_dj}],
    impacto=None, tratamiento="Alias explícito en analisis_02_variacion_civ.py y en la app (mapeo H02-300).", estado="DOCUMENTADO", responsable="Analista", pregunta="Confirmar con el IDU el CIV oficial del tramo.", verificable="analisis/scripts/analisis_02_variacion_civ.py", hallazgo="H02-300")

# A-17 numeración por fórmula
floaty = [(r, v(f"C{r}")) for r in range(7, 680) if isinstance(v(f"C{r}"), float) and round(v(f"C{r}"), 3) != v(f"C{r}")]
add("A", "INFO", f"Numeración de ítems generada por fórmula con artefactos de coma flotante ({len(floaty)} celdas, p. ej. 1.0019999999999998)",
    "La columna C (ítem de pago) se genera sumando 0,001 al ítem anterior; Excel la muestra con 3 decimales pero guarda valores como 1.0019999999999998 o 5.037000000000012. Cualquier cruce por 'ítem' debe redondear a 3 decimales.",
    categoria="estructura", evidencia=[{"hoja": HOJA, "celda": f"C{r}", "valor": val} for r, val in floaty[:12]], impacto=None,
    tratamiento="extraer_presupuesto.py redondea item_pago a 3 decimales.", estado="DOCUMENTADO", responsable="Analista", verificable="openpyxl: ws['C9'].value", hallazgo="")

# A-18 encabezados contradictorios en la hoja de referencia de precios
contr_f = wbf["PRESUPUESTO CONTRACTUAL MAYO 25"]
add("A", "INFO", "La hoja de referencia de precios rotula la misma columna como 'VISOR 07 MAYO DE 2025' (fila 8) y 'VISOR 13 SEPTIEMBRE 2024' (fila 9)",
    f"PRESUPUESTO CONTRACTUAL MAYO 25!Q8 = '{contr_v['Q8'].value}' y Q9 = '{str(contr_v['Q9'].value).strip()}'. Los valores de la columna Q coinciden con el 'precio original' del dashboard de mayo de 2025 (APU actualizado con insumos del VISOR 13-09-2024), así que el rótulo correcto es el de la fila 9. "
    "Las columnas I (oficial IDU), M (propuesta VICON = VU pactado) y Q (APU 13-09-2024) son tres referencias distintas de VU; el análisis las nombra explícitamente (ver A-24).",
    categoria="etiqueta", evidencia=[{"hoja": "PRESUPUESTO CONTRACTUAL MAYO 25", "celda": "Q8", "valor": contr_v["Q8"].value}, {"hoja": "PRESUPUESTO CONTRACTUAL MAYO 25", "celda": "Q9", "valor": contr_v["Q9"].value}, {"hoja": "PRESUPUESTO CONTRACTUAL MAYO 25", "celda": "M9", "valor": contr_v["M9"].value}, {"hoja": "PRESUPUESTO CONTRACTUAL MAYO 25", "celda": "I9", "valor": contr_v["I9"].value}],
    impacto=None, tratamiento="La app llama a la columna Q 'referencia APU 13-09-2024' y a la M 'VU pactado (propuesta)'.", estado="DOCUMENTADO", responsable="Contratista", verificable="openpyxl: wb['PRESUPUESTO CONTRACTUAL MAYO 25']['Q8'].value", hallazgo="")

# A-19 códigos repetidos / reubicaciones (definición única: analisis_01 → reubicaciones[].trasladado)
dups = h04.get("duplicados", [])
h01 = json.load(open(ROOT / "analisis" / "hallazgos" / "01_variacion_items.json", encoding="utf-8"))
reub = h01.get("reubicaciones", [])
tras = sum(x.get("trasladado", 0) for x in reub)
add("A", "INFO", f"{len(dups)} códigos IDU con más de un renglón (ítem × subcapítulo) y {len(reub)} reubicaciones entre renglones por {fmt(tras)}",
    "La hoja repite el mismo código en subcapítulos distintos (IDU vs ESP, pavimentos vs espacio público). Un código que baja en un renglón y sube en otro no es eliminación ni alcance nuevo: es un traslado. "
    f"Trasladado = min(valor que sale de los renglones que bajan, valor que entra en los que suben), sumado por código: {fmt(tras)} en {len(reub)} códigos "
    f"({sum(1 for x in reub if x.get('filas_eliminadas_total') and x.get('filas_nuevas_total'))} con renglones eliminados del todo y nuevos del todo). Sin esta lectura, la 'eliminación' y el 'alcance nuevo' se sobreestiman.",
    categoria="estructura", evidencia=sorted(reub, key=lambda x: -x.get("trasladado", 0))[:32], impacto=round(tras),
    tratamiento="Sección I de la app (reubicaciones) e informe 8C; H02 del análisis 04 pasa a INFO (B-09); el cálculo de 'trasladado' se corrigió (B-13).", estado="DOCUMENTADO", responsable="Contratista",
    pregunta="Entregar la conciliación código a código de los traslados entre subcapítulos.", verificable="python analisis/scripts/analisis_01_variacion_items.py → reubicaciones", hallazgo="H02 (análisis 04)")

# A-20 decimales en totales
fracs = []
for r in range(688, 739):
    for c in range(1, 82):
        x = wsv.cell(r, c).value
        if isinstance(x, float) and abs(x - round(x)) > 1e-9:
            fracs.append({"celda": f"{get_column_letter(c)}{r}", "valor": x})
add("A", "INFO", f"{len(fracs)} celdas de totales y del detalle SST con decimales de peso (p. ej. BY688 = …071,5)",
    "Los totales por CIV (fila 688, /2) y el detalle de SST/diálogo/PMT a 8 meses (filas 730-738) no están redondeados a pesos; M692 sí redondea (ROUND(2943115324 + S738, 0)). "
    "En un otrosí las cifras deben ir en pesos enteros.",
    categoria="aritmética", evidencia=fracs[:25], impacto=None, tratamiento="El análisis redondea al peso donde corresponde y reporta las diferencias.", estado="DOCUMENTADO", responsable="Contratista", verificable="openpyxl", hallazgo="")

# A-21 hojas ocultas y recálculo
hidden = [n for n in wbv.sheetnames if wbv[n].sheet_state != "visible"]
calc = wbf.calculation
add("A", "INFO", f"{len(hidden)} de {len(wbv.sheetnames)} hojas están ocultas; el libro tiene {len(links)} vínculos externos y fullCalcOnLoad = {getattr(calc, 'fullCalcOnLoad', None)}",
    f"Hojas ocultas: {', '.join(hidden)}. Varias son la base del cálculo (CONSOLIDADO, PRESUPUESTO CONTRACTUAL MAYO 25, VISOR 07-05-25, NPs Objetados, PRESUPUESTO 63 mm, EJECUTIVO). "
    f"Vínculos externos declarados: {len(links)} (la mayoría heredados de libros antiguos; los que afectan el cálculo son [186], [187], [188] y [190], ver A-01 y A-02). "
    "fullCalcOnLoad = True obliga a Excel a recalcular al abrir: si el usuario no actualiza vínculos, verá los valores guardados; si los actualiza sin tener los libros, verá #REF!.",
    categoria="trazabilidad", evidencia=[{"hojas_ocultas": hidden}, {"vinculos_externos": len(links)}, {"vinculos_que_afectan_calculo": {i: links[i] for i in (186, 187, 188, 190) if i in links}}],
    impacto=None, tratamiento="El análisis lee las hojas ocultas como cualquier otra y usa siempre los valores guardados.", estado="DOCUMENTADO", responsable="Contratista",
    pregunta="Entregar el libro con vínculos rotos convertidos a valores y sin hojas ocultas, o entregar los libros vinculados.", verificable="openpyxl: [ws.sheet_state for ws in wb]; len(wb._external_links)", hallazgo="")

# A-22 fórmula auxiliar en T699
t699_refs = [c.coordinate for row in wsf.iter_rows() for c in row if isinstance(c.value, str) and re.search(r"\bT699\b", c.value)]
add("A", "INFO", "Fórmula auxiliar suelta en T699 (=T7+T12+…; R699 = 'SIN REDES') dentro de la fila de bioseguridad",
    f"T699 = {f('T699')} → {fmt(num(v('T699')))}: suma de subtotales de capítulo del primer CIV, aparentemente un cálculo de 'obra sin redes' que quedó en la fila de un componente. Referenciada por: {t699_refs or 'ninguna celda'}.",
    categoria="estructura", evidencia=[{"hoja": HOJA, "celda": "T699", "formula": f("T699"), "valor": v("T699")}, {"hoja": HOJA, "celda": "R699", "valor": v("R699")}],
    impacto=None, tratamiento="Sin efecto en totales.", estado="DOCUMENTADO", responsable="Contratista", verificable="openpyxl", hallazgo="")

# A-23 mismo código con VU o unidad distintos
byc = defaultdict(list)
for it in items:
    c = str(it.get("codigo_idu") or "").strip()
    if c and c.upper() not in ("N/A", "NO"):
        byc[c].append(it)
multi_k = []
und_dif = []
for c, rs in byc.items():
    ks = sorted({r["vu_cd"] for r in rs if isinstance(r.get("vu_cd"), (int, float)) and r["vu_cd"]})
    if len(ks) > 1:
        multi_k.append({"codigo": c, "filas": [r["row"] for r in rs], "vu_distintos": ks, "descripcion": rs[0]["descripcion"][:60]})
    u_xl = {str(r["und"]).strip().upper() for r in rs if r.get("und")}
    u_c = str(contr.get(c, {}).get("und") or "").strip().upper()
    if u_c and u_xl and u_c not in u_xl:
        und_dif.append({"codigo": c, "filas": [r["row"] for r in rs], "und_v4": sorted(u_xl), "und_contractual": u_c, "descripcion": rs[0]["descripcion"][:60]})
add("A", "MEDIA" if (multi_k or und_dif) else "INFO", f"{len(multi_k)} códigos con VU distinto entre renglones y {len(und_dif)} códigos con unidad distinta a la contractual",
    "Un mismo código IDU debe tener un solo VU y una sola unidad en todo el presupuesto. " + (("VU distintos: " + ", ".join(x["codigo"] for x in multi_k[:15]) + ". ") if multi_k else "") + (("Unidad distinta: " + ", ".join("%s (%s→%s)" % (x["codigo"], x["und_contractual"], "/".join(x["und_v4"])) for x in und_dif[:15]) + ".") if und_dif else ""),
    categoria="precios", evidencia=multi_k[:30] + und_dif[:30], impacto=None,
    tratamiento="Se listan para revisión; la sección H de la app compara VU por renglón.", estado="ABIERTO" if (multi_k or und_dif) else "DOCUMENTADO", responsable="Contratista",
    pregunta="Justificar cada código con más de un VU o con cambio de unidad frente al contractual.", soporte="APU y especificación de cada código afectado.", verificable="este script (multi_k, und_dif)", hallazgo="")

# A-24 precios unitarios de V4 frente a tres referencias
dvc = h04.get("desviaciones_vu_contractual", [])
rvp = h04.get("resumen_vu_propuesta", {})
dvp = h04.get("desviaciones_vu_propuesta", [])
imp_q = round(sum((d["K_v4"] - d["K_contractual"]) * (num(v(f"I{d['row']}")) or 0) * AIU for d in dvc))
add("A", "ALTA", f"Los VU de V4 están +{str(round(rvp.get('mediana_delta_pct', 0), 1)).replace('.', ',')} % (mediana) sobre los VU pactados en la propuesta ({fmt(rvp.get('impacto_aiu_total'))} con AIU) y +4,2 % sobre el APU actualizado de 2024 ({fmt(imp_q)} en {len(dvc)} renglones con Δ > 2 %)",
    f"La hoja PRESUPUESTO CONTRACTUAL MAYO 25 trae tres VU por código: I (oficial IDU 2021), M (propuesta VICON = VU pactado) y Q (APU actualizado con insumos VISOR 13-09-2024). Frente a M: {rvp.get('renglones')} renglones, mediana {rvp.get('mediana_delta_pct')} %, "
    f"valor V4 {fmt(rvp.get('valor_v4_aiu'))} frente a {fmt(rvp.get('valor_a_vu_pactado_aiu'))} si se valorara al VU pactado (Δ {fmt(rvp.get('impacto_aiu_total'))}). Frente a Q: {len(dvc)} renglones con Δ > 2 %, efecto {fmt(imp_q)} a cantidades finales. "
    "Dato clave: el valor actual de obras del contrato (N688 = 44.303.294.799 = H × L) ya está calculado con los VU de V4, así que la actualización de precios se formalizó ANTES de esta solicitud (el libro externo se llama 'EJERCICIO ACTUALIZACIÓN IDU / ANEXO MODIF'). "
    "La pregunta no es si V4 cambia los precios (no lo hace dentro de V4: N y M usan el mismo K) sino con qué acto se pasó de los VU pactados a los actualizados y si ese mayor valor cuenta como adición para el tope del 50 %.",
    categoria="precios", evidencia=dvp[:25] + [rvp] + sorted(dvc, key=lambda d: -abs(d.get("delta_pct") or 0))[:10],
    impacto=rvp.get("impacto_aiu_total"), tratamiento="Sección H (precios) muestra las dos referencias y exporta CSV; hallazgos H03 y H04 del análisis 04; el simulador permite valorar al VU de referencia de 2024.",
    estado="ABIERTO", responsable="Contratista / IDU", pregunta="¿Qué otrosí o acta autorizó actualizar los VU pactados a insumos 13-09-2024? ¿Ese incremento se contabilizó como adición o como reajuste? ¿Se aplica además el componente 'ajustes por cambio de vigencia' sobre los mismos ítems (doble ajuste)?",
    soporte="Otrosí de actualización de precios; comparación VU pactado vs actualizado firmada por la interventoría; APU FO-GI-19 de los ítems de mayor impacto (losa MR45, estabilización con rajón, transporte de escombros, ductos TDP).",
    verificable="python analisis/scripts/analisis_04.py → resumen_vu_propuesta, desviaciones_vu_contractual", hallazgo="H03 y H04 (análisis 04)")

# A-25 historia del valor del contrato
c_o = lambda r, col: num(contr_v.cell(r, col).value)
hist = [
    {"concepto": "Obras civiles + redes con AIU (A)", "fila": 246, "oficial_K": c_o(246, 11), "propuesta_O": c_o(246, 15), "actualizado_T": c_o(246, 20), "V0_actual": num(v("N688")), "V4": num(v("M688"))},
    {"concepto": "SST (B)", "fila": 248, "oficial_K": c_o(248, 11), "propuesta_O": c_o(248, 15), "actualizado_T": c_o(248, 20), "V0_actual": num(res["D8"].value), "V4": num(v("M692"))},
    {"concepto": "Diálogo ciudadano (C)", "fila": 252, "oficial_K": c_o(252, 11), "propuesta_O": c_o(252, 15), "actualizado_T": c_o(252, 20), "V0_actual": num(res["D9"].value), "V4": num(v("M693"))},
    {"concepto": "PMT (D)", "fila": 256, "oficial_K": c_o(256, 11), "propuesta_O": c_o(256, 15), "actualizado_T": c_o(256, 20), "V0_actual": num(res["D10"].value), "V4": num(v("M694"))},
    {"concepto": "Ajustes por cambio de vigencia (E)", "fila": 262, "oficial_K": c_o(262, 11), "propuesta_O": c_o(262, 15), "actualizado_T": c_o(262, 20), "V0_actual": num(res["D11"].value), "V4": num(v("M695"))},
    {"concepto": "Actividades acero (F)", "fila": 264, "oficial_K": c_o(264, 11), "propuesta_O": c_o(264, 15), "actualizado_T": c_o(264, 20), "V0_actual": num(res["D13"].value), "V4": num(v("M697"))},
    {"concepto": "Fondo de compensaciones (K)", "fila": 277, "oficial_K": c_o(277, 11), "propuesta_O": c_o(277, 15), "actualizado_T": c_o(277, 20), "V0_actual": num(res["D16"].value), "V4": num(v("M700"))},
    {"concepto": "Fase de obras iniciales (I)", "fila": 270, "oficial_K": c_o(270, 11), "propuesta_O": c_o(270, 15), "actualizado_T": c_o(270, 20), "V0_actual": num(res["D17"].value), "V4": num(v("M701"))},
    {"concepto": "COSTO TOTAL DEL PROYECTO", "fila": 279, "oficial_K": c_o(279, 11), "propuesta_O": c_o(279, 15), "actualizado_T": c_o(279, 20), "V0_actual": TOTAL_V0, "V4": TOTAL_V4},
]
orig = c_o(279, 15)
def _lab(r):
    return " ".join(str(contr_v.cell(r, c).value).strip() for c in range(2, 7) if contr_v.cell(r, c).value not in (None, ""))
adiciones_prev = [{"fila": r, "concepto": _lab(r), "valor_T": c_o(r, 20)} for r in range(240, 280) if _lab(r).upper().startswith("ADICI")]
add("A", "ALTA", f"El valor inicial del contrato fue {fmt(orig)}, no {fmt(TOTAL_V0)}: el 'valor actual' ya trae +{fmt(TOTAL_V0 - orig)} (+{str(round((TOTAL_V0 / orig - 1) * 100, 1)).replace('.', ',')} %) y con la solicitud el acumulado llega a {str(round((TOTAL_V4 / orig - 1) * 100, 1)).replace('.', ',')} % del inicial",
    f"La hoja PRESUPUESTO CONTRACTUAL MAYO 25 (fila 279) muestra el COSTO TOTAL DEL PROYECTO de la licitación y de la propuesta: {fmt(orig)} (coincide con el boletín del IDU de 2021: $50.793M de obra). Su columna T ('actualizada por insumos VISOR 13-09-2024') llega a {fmt(c_o(279, 20))} e incluye tres adiciones previas para la fase de obras iniciales y gestiones preliminares "
    f"(adiciones 1, 2 y 3 repartidas en SST, diálogo, PMT y fase inicial: {len([a for a in adiciones_prev if a['valor_T']])} renglones que suman {fmt(sum(a['valor_T'] or 0 for a in adiciones_prev))}; la 'adición 3' está ajustada al VISOR del 19-06-2024). El libro radicado toma como 'valor actual' {fmt(TOTAL_V0)} (M705). "
    f"Entre la propuesta y el valor actual: obras+redes pasan de {fmt(hist[0]['propuesta_O'])} a {fmt(hist[0]['V0_actual'])} (+{(hist[0]['V0_actual'] / hist[0]['propuesta_O'] - 1) * 100:.1f} % con las MISMAS cantidades contractuales H: es efecto precio, ver A-24) y el fondo de compensaciones pasa de {fmt(hist[6]['propuesta_O'])} a 0. "
    f"Para el tope del 50 % del art. 40 de la Ley 80 la base es el valor inicial: {fmt(TOTAL_V0 - orig)} previos + {fmt(TOTAL_V4 - TOTAL_V0)} solicitados = {fmt(TOTAL_V4 - orig)} = {(TOTAL_V4 - orig) / orig * 100:.1f} % en pesos nominales (margen {fmt(round(orig * 0.5 - (TOTAL_V4 - orig)))}); en SMMLV el resultado depende de la fecha de cada adición previa, que el libro no trae.",
    categoria="trazabilidad", evidencia=hist + adiciones_prev, impacto=round(TOTAL_V0 - orig),
    tratamiento="La app corrige el chequeo del tope (B-11): base $50.793.789.333, incremento previo $8.632.785.866 contado íntegramente como adición (supuesto conservador) y escenario en SMMLV con el incremento previo a SMMLV 2025.",
    estado="ABIERTO", responsable="IDU", pregunta="¿Cuáles son los otrosíes del contrato (fecha, valor, naturaleza: adición, reajuste, actualización de precios, prórroga)? ¿Cuánto de los $8.632.785.866 previos cuenta como adición para el tope del 50 %?",
    soporte="Expediente contractual: contrato, otrosíes 1 a n, actas de modificación, CDP/RP de cada adición.", verificable="openpyxl: wb['PRESUPUESTO CONTRACTUAL MAYO 25']['O279'].value", hallazgo="H04 (análisis 04)")

# ══════════════════════════ B · CORRECCIONES DEL ANÁLISIS ══════════════════════════
B = [
    ("cf7bdd7", "ALTA", "La app no cargaba ('Cargando…' indefinido) con el JSON consolidado", "clasificacion.totales es un objeto y el código lo recorría como arreglo (forEach). Se agregó Array.isArray antes de iterar.", "CORREGIDO"),
    ("cf7bdd7", "ALTA", "La tabla de ítems mostraba $0 en todas las columnas de valor", "Los campos del JSON (K_vu_cd, L_vu_cd_aiu, M_valor_final, N_valor_inicial) no coincidían con los que leía la app; se creó _p75NormalizeItems para unificar nombres.", "CORREGIDO"),
    ("cf7bdd7", "ALTA", "Costo por CIV: Δ V4 − V2 comparaba el total con componentes contra las obras de V2, y el % NP iba multiplicado por 100", "El CIV 9004002 mostraba +$413M cuando la diferencia real de obras es −$215.494.094. Se usa delta_v4_v2 (obras vs obras) y el porcentaje se divide por 100.", "CORREGIDO"),
    ("cf7bdd7", "ALTA", "El CIV 500002375 tenía línea base $0 por el alias de identificador", "La hoja usa 500002375; data.json usa 50002375 y la comparativa 16004876. Se creó el alias y la línea base por CIV se ancló a la columna H repartida con la participación de data.json; 40 renglones sin reparto ($2.460.223.472) quedan explícitos en la conciliación.", "CORREGIDO"),
    ("ad5b438", "MEDIA", "El waterfall incluía la fila TOTAL GENERAL y duplicaba los totales; los negativos en miles de millones perdían el signo", "WF() filtra la fila total; fmtB respeta el signo; los códigos 'NO'/'N/A' de los NP se excluyen del conteo de repetidos; se corrigió una precedencia ||/+ en el explorador.", "CORREGIDO"),
    ("5cb90b9", "BAJA", "Prioridad de revisión demasiado estricta (5 ítems 'Alta') y desbordes en móvil", "La prioridad pasó a materialidad (|Δ| en miles de millones) → 48 ítems Alta; grid minmax(min(480px,100%),1fr); padding superior en gráficas para las etiquetas.", "CORREGIDO"),
    ("0a1bae6", "ALTA", "Análisis 06: todas las referencias de fila estaban desplazadas (+4 en la hoja principal, +5 en PRESUPUESTO 63 mm)", "El JSON y el MD del análisis 06 se escribieron a mano por el agente sin verificar contra openpyxl. corregir_06.py remapea 692→688, 696→692, …, 707→703, 733-742→729-738, 657→652 (63 mm), etc., y deja meta_correcciones. Las filas reales se verificaron celda a celda.", "CORREGIDO"),
    ("0a1bae6", "ALTA", "H06-01 afirmaba un 'riesgo de doble pago en acero por $2.977M–$3.053M' que el libro no sustenta", "La premisa era que el bloque ACEROS estaba 'cargado dentro de obras'. M688 = SUM(M8:M679) y CB688 = SUM(CB7:CB679)/2 excluyen las filas 680-687: no hay doble conteo en el Excel. El hallazgo se reescribe como MEDIA con impacto = diferencia bloque − bolsa F (75.469.677) y pregunta de cuál rige. Se ajustan resumen ejecutivo, XP, checklist e informe.", "CORREGIDO"),
    ("0a1bae6", "MEDIA", "Análisis 04: dos falsos positivos de consistencia entre hojas y 16 'duplicados reales' que no lo eran", "EJECUTIVO!H56 (59.426.575.199) es el valor actual del contrato, no el total de obras; Presupuesto estimado!A11 (74.667.840.865) excluye por definición la fase de obras iniciales (758.734.334). Los subcapítulos se truncaban a 50 caracteres y '…A CARGO DEL IDU' se confundía con '…A CARGO DE LA ESP'. H02 pasa de ALTA a INFO y H04 de MEDIA a INFO; las diferencias explicadas quedan en observaciones_hojas.", "CORREGIDO"),
    ("0a1bae6", "INFO", "Consolidado de hallazgos recontado", "Tras B-07 a B-09 y B-12 el consolidado pasó de 44 ALTA / 16 MEDIA / 4 BAJA / 6 INFO a 44 / 15 / 4 / 8 (71); con B-14 queda en 44 / 18 / 4 / 8 (74). Ninguna cifra del waterfall, de la variación por ítem ni del costo por CIV cambia.", "CORREGIDO"),
    ("0a1bae6", "ALTA", "El chequeo del tope del 50 % (Ley 80 art. 40) usaba $59.426.575.199 como 'valor inicial'", "El valor inicial del contrato es $50.793.789.333 (hoja PRESUPUESTO CONTRACTUAL MAYO 25 fila 279 = boletín IDU 2021); el 'valor actual' ya incluye $8.632.785.866 de incremento. normCheck() pasa a usar la base original y a acumular el incremento previo: 48,5 % nominal (antes se mostraba 26,9 %) y ~54 % del tope en SMMLV si el incremento previo se cuenta a SMMLV 2025. Tarjeta, ficha legal, XP y lista de chequeo actualizados; la duda queda como C-01.", "CORREGIDO"),
    ("0a1bae6", "ALTA", "El análisis 04 llamaba 'VU contractual' a la columna Q (APU actualizado 13-09-2024) y truncaba la lista a 200 renglones", "El VU pactado en el contrato es la columna M (propuesta VICON). Se agrega la comparación contra M (H04 nuevo: mediana +49,0 %, $15.086M con AIU), se retitula H03 y se guardan las listas completas (367 renglones vs referencia 2024; la sección H de la app mostraba 200 y un total de $3.259M que ahora es el total real).", "CORREGIDO"),
    ("0a1bae6", "MEDIA", "'Trasladado' de las reubicaciones (sección I e informe 8C) usaba el valor completo de los renglones", "Se computaba min(Σ N de las filas que bajan, Σ M de las filas que suben), lo que contaba renglones que solo disminuyen o solo aumentan como si se movieran enteros ($6.462.266.802). Ahora trasladado = min(valor que sale, valor que entra), calculado en analisis_01 (campos valor_disminuido / valor_aumentado / trasladado): $5.807.343.956 en 32 códigos. Cambian 'eliminación real' y 'alcance nuevo real' del informe 8C.", "CORREGIDO"),
    ("git log --grep=B-14", "MEDIA", "Análisis 02: las métricas de intensidad de obra por m² (rajón, andén, MD12, BG_A) daban 0 en los 27 CIV", "El script buscaba \"1005\", \"3039\", \"2002\" y \"1012\" como código IDU, pero son números de ítem sin punto (y 1.005 no es el rajón). Solo la métrica MD19 (buscada por NP-123) tenía datos, por eso la tabla \"Intensidad de obra por m²\" de cada ficha de CIV mostraba 0,000. Ahora se buscan por código IDU verificado: rajón 6016, andén 3425, mezcla asfáltica MD12 6313 + NP-123 8618 y base granular BG_A 4158 + NP-124 4744 (los contractuales fueron reemplazados por los NP). Los atípicos pasan de 2 a 5 hallazgos MEDIA (H02-200 a H02-204); el más alto es el andén del CIV 16000013 (5,5× la mediana). Ninguna cifra monetaria cambia.", "CORREGIDO"),
]
for commit, sev, tit, det, est in B:
    add("B", sev, tit, det, categoria="análisis", estado=est, responsable="Analista", commit=commit, verificable=(commit if commit.startswith("git ") else f"git show {commit}"))

# ══════════════════════════ C · DUDAS ABIERTAS ══════════════════════════
C = [
    ("ALTA", "IDU", "¿Cuáles otrosíes llevaron el contrato de $50.793.789.333 (propuesta 2021) a $59.426.575.199 y qué parte de esos $8.632.785.866 es adición (cuenta para el tope del 50 %) y qué parte reajuste o actualización de precios?", "A-25: con la solicitud el acumulado nominal es 48,5 % del valor inicial; en SMMLV depende de la fecha de cada adición previa.", "Historial de otrosíes y adiciones del contrato 1752-2021 con valores, fechas y naturaleza; CDP/RP."),
    ("ALTA", "Contratista", "¿Qué APU y qué fecha de insumos (VISOR) sustentan los VU de V4? ¿Están aprobados?", "A-01, A-03 y A-24: el efecto precio es +$3.259M en 200 ítems.", "Libro APU 28-07-2025; FO-GI-19 por ítem; acta de aprobación de VU."),
    ("ALTA", "Contratista", "¿Qué obra es el código 8643 (5.037) por $2.718M con descripción de 'factibilidad, estudios y diseños'?", "A-06.", "Especificación, APU y memoria por CIV."),
    ("ALTA", "Contratista", "¿Cuál es la fecha de terminación vigente y el plazo ejecutado? Sin ella no se puede juzgar si 8 meses son suficientes para $16.000M (ritmo de $2.000M/mes, 3,3 veces el histórico).", "H06-03.", "Cronograma vigente, curva S y facturación mensual certificada de los últimos 24 meses."),
    ("ALTA", "Contratista", "¿La adición incluye ajustes por cambio de vigencia 2027? ¿Con qué fórmula?", "A-07.", "Cálculo GUDP017 / ICCP por vigencia."),
    ("MEDIA", "Contratista", "¿Cuál es el total oficial del subgrupo 5: BY688 (…071,5) o la suma de CIVs (…244.367)?", "A-04.", "Libro con totales por CIV recalculados."),
    ("MEDIA", "Contratista", "¿El bloque ACEROS es la memoria de la bolsa F o alcance adicional? ¿Cuál rige para pagar?", "A-05 / H06-01.", "Memoria de acero conciliada y constancia en el otrosí."),
    ("MEDIA", "Contratista", "¿Cuáles de los 84 NP siguen objetados por la interventoría? La hoja 'NPs Objetados' se cruza por descripción, no por código.", "Limitación D-05.", "Lista de NP objetados con código, estado y fecha."),
    ("MEDIA", "Contratista", "¿Cuál es la cantidad contractual por CIV (columna H desagregada)? El libro solo trae el total.", "Limitación D-01: la línea base por CIV es reconstruida.", "Presupuesto contractual por CIV (matriz ítem × CIV de la firma)."),
    ("MEDIA", "Contratista", "¿Qué compensaciones financiaba el fondo de V2 ($5.943M) y dónde quedaron?", "A-09.", "Trazabilidad V2→V3→V4 del componente K."),
    ("MEDIA", "Contratista", "¿Qué es el libro 'PRESUPUESTO TOTAL $80 MIL.xlsx' al que están vinculadas las cantidades del NP-101?", "A-02.", "Copia del libro y explicación de la versión."),
    ("MEDIA", "Contratista", "¿Los 68 renglones NP en cero y los 3 NP sin cantidad se retiran del anexo?", "A-15.", "Anexo depurado."),
    ("BAJA", "Contratista", "¿El contratista renuncia a pedir bioseguridad por los 8 meses o se incorpora?", "A-08.", "Comunicación expresa."),
    ("BAJA", "Contratista", "Corregir O690, rótulos con fecha de mayo, 'SISETE' y decimales en totales antes de anexar el libro al otrosí.", "A-10, A-13, A-14, A-20.", "Libro corregido."),
    ("BAJA", "Interventoría", "¿Los 9 CIV 'no alcanza' de la Alternativa 2 siguen fuera del alcance con la adición o vuelven a entrar?", "El simulador (sección J) los excluye por −$19.511M de obras.", "Acta de alcance por CIV firmada."),
    ("BAJA", "IDU", "¿Rige el SMMLV 2026 del Decreto 1469/2025 o el transitorio, para convertir el tope del 50 %?", "El decreto está suspendido provisionalmente (12-02-2026).", "Concepto jurídico del IDU."),
]
for sev, resp, preg, ctx, sop in C:
    add("C", sev, preg, ctx, categoria="duda", estado="ABIERTO", responsable=resp, pregunta=preg, soporte=sop)

# ══════════════════════════ D · LIMITACIONES ══════════════════════════
conc = h02.get("conciliacion_total", {}) if isinstance(h02, dict) else {}
D = [
    ("ALTA", "La línea base (cantidad contractual) por CIV es reconstruida, no radicada", f"El Excel trae la cantidad contractual solo como total del renglón (columna H). El análisis 02 la reparte por CIV con la participación de cada CIV en el VISOR de mayo de 2025 (data.json). {conc.get('detalle_sin_reparto', {}).get('n_renglones', 40) if isinstance(conc.get('detalle_sin_reparto'), dict) else 40} renglones no tienen participación (código nuevo o sin CIV en el VISOR) y suman {fmt(2_460_223_472)} que quedan sin repartir y se muestran aparte. Toda cifra 'Δ por CIV' hereda este supuesto; el Δ total por renglón no."),
    ("ALTA", "Los valores del Excel son los guardados; el libro no se recalculó", "Se lee con openpyxl (data_only). Los VU y algunas cantidades dependen de libros externos ausentes (A-01, A-02), así que ni el analista ni el revisor pueden recalcular el libro completo. Si Excel actualiza vínculos sin los archivos, mostrará #REF!."),
    ("MEDIA", "El cruce con V1 (IDU 25-02-2026) y V2 (VICON 21-04-2026) se hace por código IDU agregado y en costo directo", "comparativa.json no tiene renglones por subcapítulo ni por CIV. Un código que en V4 está en varias filas se compara con su suma. Las cifras V1/V2 se llevan a AIU con 1,31849 (V4) aunque V1 y V2 tenían su propio AIU (34,01 % en el VISOR de mayo)."),
    ("MEDIA", "La comparación de precios (sección H) cubre 200 de 649 renglones", "Solo los códigos con VU en la hoja PRESUPUESTO CONTRACTUAL MAYO 25 (columna 'actualización APU 13-09-2024') o en el VISOR 07-05-25. Los NP no tienen referencia contractual: su VU se compara solo con V2."),
    ("MEDIA", "La hoja 'NPs Objetados' se cruza por descripción normalizada, no por código", "El estado 'objetado' de un NP en la app es indicativo. Confirmar con la lista oficial (C-08)."),
    ("MEDIA", "Los componentes (SST, diálogo, PMT, etc.) se reparten por CIV en proporción al costo directo de obras", "Es una convención del análisis para llegar a un 'costo total por CIV'; el contratista no reparte componentes por CIV. Usar solo para comparar CIVs entre sí."),
    ("MEDIA", "Las áreas por CIV para el $/m² provienen del dashboard (data.json: longitud × ancho)", "Son las áreas del VISOR de mayo de 2025, no las de diseño detallado. El $/m² sirve para detectar atípicos, no para tarifar."),
    ("MEDIA", "Los índices 'atención' y 'prioridad' y el simulador son heurísticos del analista", "Pesos declarados en la app (ATT_W, itemPriority, SIM). Cambiarlos cambia el orden, no las cifras de origen. El simulador es ilustrativo: no sustituye el recálculo del contratista."),
    ("MEDIA", "El marco normativo se consultó el 27-09-2026 y puede cambiar", "Fuentes públicas (Ley 80/1993, Ley 1474/2011, CCE C-466/2024, Consejo de Estado exp. 67.508, manuales IDU MG-GC-06 v19, GUDP017, PR-IC-01). El MG-GC-01 no pudo leerse. El SMMLV 2026 (Decreto 1469/2025) está suspendido provisionalmente: el tope del 50 % se muestra con ambos escenarios."),
    ("BAJA", "El análisis 05 (NPs) y el 06 (versiones) usan datos de V2 que ya fueron objeto de conciliación en abril", "Las cifras de V2 vienen de comparativa.json (trabajo de abril de 2026); si ese archivo se corrige, deben regenerarse 05 y 06."),
    ("BAJA", "El repositorio y la página son públicos; la clave de acceso de la app es solo de interfaz", "Los JSON y el informe pueden descargarse sin autenticación desde GitHub Pages. No publicar aquí datos que el contrato o la ley protejan; el Excel fuente no está en el repositorio (está en .gitignore) y se identifica solo por su SHA-256."),
    ("BAJA", "Redondeos", "Las verificaciones aceptan Δ ≤ $100 (redondeo por CIV) y $86.217 (fila 34). Ninguna cifra del informe se redondea salvo donde se indica 'M' (millones)."),
]
for sev, tit, det in D:
    add("D", sev, tit, det, categoria="limitación", estado="LIMITACION", responsable="Analista")

# ══════════════════════════ PAQUETE DE AUDITORÍA ══════════════════════════
salidas = ["analisis_2026_09.json", "presupuesto_2026_09.json", "comparativa.json", "data.json", "analisis/Analisis_Presupuesto_2026-09.xlsx", "analisis/INFORME_PRESUPUESTO_2026-09.md",
           "analisis/hallazgos/01_variacion_items.json", "analisis/hallazgos/02_variacion_civ.json", "analisis/hallazgos/03_costo_civ.json", "analisis/hallazgos/04_aritmetica.json", "analisis/hallazgos/05_nps.json", "analisis/hallazgos/06_versiones_plazo.json"]
paquete = {
    "fecha": FECHA,
    "fuente": {"archivo": XLSX.name, "sha256": sha256(XLSX), "bytes": XLSX.stat().st_size, "hojas": len(wbv.sheetnames), "hojas_ocultas": len(hidden), "vinculos_externos": len(links),
               "nota": "El Excel no está en el repositorio (.gitignore *.xlsx). Quien audite debe verificar que su copia tenga este SHA-256."},
    "salidas": [{"archivo": s, "sha256": sha256(ROOT / s), "bytes": (ROOT / s).stat().st_size} for s in salidas if (ROOT / s).exists()],
    "entorno": {"python": sys.version.split()[0], "openpyxl": openpyxl.__version__, "plataforma": platform.platform(), "num2words": bool(num2words)},
    "git": {"commit_base": git("rev-parse", "--short", "HEAD"), "rama": git("rev-parse", "--abbrev-ref", "HEAD"), "repositorio": "https://github.com/ronalc90/Consorcio-Montevideo-045"},
    "reproducir": [
        "pip install openpyxl num2words   # (pandas y xlsxwriter para generar_excel.py)",
        "python analisis/scripts/extraer_presupuesto.py      # Excel -> analisis/datos/hojas/*.csv + presupuesto_2026_09.json",
        "python analisis/scripts/analisis_01_variacion_items.py", "python analisis/scripts/analisis_02_variacion_civ.py", "python analisis/scripts/analisis_03_costo_civ.py",
        "python analisis/scripts/analisis_04.py", "python analisis/scripts/analisis_05_nps.py",
        "python analisis/scripts/corregir_06.py               # corrige filas y H06-01 del análisis 06 (idempotente)",
        "python analisis/scripts/consolidar.py", "python analisis/scripts/generar_excel.py", "python analisis/scripts/verificacion.py   # debe terminar en 'VERIFICACION COMPLETA' con todos [OK ]",
        "python analisis/scripts/auditoria.py                 # este registro",
    ],
    "tolerancias": {"suma_civ_vs_M688": 69, "fila_34": 86217, "waterfall": 0, "nps": 0},
    "cifras_control": {"total_obras_M688": TOTAL_OBRAS, "total_V4_M703": TOTAL_V4, "valor_actual_M705": TOTAL_V0, "adicion": TOTAL_V4 - TOTAL_V0, "delta_obras": 13_893_639_001, "balance": -257_285_548, "np_con_aiu": 14_150_924_549,
                      "suma_civ_obras": round(tot_civ), "bloque_aceros": round(bloque), "bolsa_F": round(bolsa or 0)},
}

resumen = {
    "total": len(registro),
    "por_tipo": dict(Counter(r["tipo"] for r in registro)),
    "por_severidad": dict(Counter(r["severidad"] for r in registro)),
    "por_estado": dict(Counter(r["estado"] for r in registro)),
    "abiertos_alta": [r["id"] for r in registro if r["estado"] == "ABIERTO" and r["severidad"] == "ALTA"],
}

OUT_DIR.mkdir(parents=True, exist_ok=True)
json.dump({"meta": {"titulo": "Registro de auditoría · presupuesto 01-09-2026 (75MM · 8 meses)", "fecha": FECHA, "generado_por": "analisis/scripts/auditoria.py", "hoja": HOJA,
                    "tipos": {"A": "Errores e inconsistencias en la fuente (Excel del contratista)", "B": "Correcciones hechas al análisis", "C": "Dudas abiertas para el contratista / IDU", "D": "Limitaciones del análisis"},
                    "estados": {"ABIERTO": "Requiere respuesta del contratista o del IDU", "DOCUMENTADO": "Verificado y sin acción pendiente; se deja constancia", "CORREGIDO": "Error del análisis ya corregido en el commit indicado", "LIMITACION": "Supuesto o alcance del análisis que el revisor debe conocer"}},
           "resumen": resumen, "registro": registro, "paquete": paquete}, open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=2, default=str)

with open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as fcsv:
    w = csv.writer(fcsv, delimiter=";")
    w.writerow(["id", "tipo", "categoria", "severidad", "estado", "responsable", "titulo", "detalle", "impacto_pesos", "tratamiento", "pregunta", "soporte_a_pedir", "commit", "hallazgo_relacionado", "verificable_con"])
    for r in registro:
        w.writerow([r["id"], r["tipo"], r["categoria"], r["severidad"], r["estado"], r["responsable"], r["titulo"], r["detalle"], r["impacto_pesos"] if r["impacto_pesos"] is not None else "", r["tratamiento"], r["pregunta"], r["soporte_a_pedir"], r["commit"], r["hallazgo_relacionado"], r["verificable_con"]])

# ─────────────────────────────── Markdown ───────────────────────────────
md = []
md.append("# Registro de auditoría — presupuesto 01-09-2026 (75MM · 8 meses)\n\n")
md.append(f"**Contrato IDU 1752-2021 · Grupo 2 · Interventoría Consorcio Montevideo 045** · generado el {FECHA} por `analisis/scripts/auditoria.py` · fuente `{XLSX.name}` · SHA-256 `{paquete['fuente']['sha256']}`\n\n")
md.append("Este registro deja por escrito (A) lo que está mal o es dudoso en el Excel del contratista, (B) lo que el propio análisis tuvo que corregir y en qué commit, (C) las preguntas que deben responder el contratista o el IDU antes de emitir concepto y (D) los supuestos del análisis. Cada asiento de la sección A se calcula leyendo el libro con openpyxl; el revisor puede repetirlo con la columna *Verificable con*.\n\n")
md.append(f"**Resumen:** {resumen['total']} asientos · por tipo {resumen['por_tipo']} · por severidad {resumen['por_severidad']} · por estado {resumen['por_estado']}.\n\n")
md.append(f"**Abiertos de severidad ALTA (resolver antes de firmar):** {', '.join(resumen['abiertos_alta'])}.\n")
md.append("\n## Cifras de control\n\n| Concepto | Valor | Celda |\n|---|---:|---|\n")
for k, cell in [("total_obras_M688", "M688"), ("total_V4_M703", "M703"), ("valor_actual_M705", "M705"), ("adicion", "M707 (signo invertido)"), ("delta_obras", "Q688"), ("balance", "O688"), ("np_con_aiu", "P688"), ("suma_civ_obras", "Σ ítem × CIV"), ("bloque_aceros", "M682:M687"), ("bolsa_F", "M697")]:
    md.append(f"| {k} | {fmt(paquete['cifras_control'][k])} | {cell} |\n")
for tipo, titulo in [("A", "A · Errores e inconsistencias en la fuente (Excel del contratista)"), ("B", "B · Correcciones hechas al análisis"), ("C", "C · Dudas abiertas para el contratista / IDU"), ("D", "D · Limitaciones del análisis")]:
    rows = [r for r in registro if r["tipo"] == tipo]
    md.append(f"\n## {titulo}\n\n")
    if tipo == "A":
        md.append("| ID | Sev. | Estado | Título | Impacto | Pregunta / soporte |\n|---|---|---|---|---:|---|\n")
        for r in rows:
            md.append(f"| {r['id']} | {r['severidad']} | {r['estado']} | {r['titulo']} | {fmt(r['impacto_pesos']) if r['impacto_pesos'] is not None else '—'} | {r['pregunta']} {('· *Soporte:* ' + r['soporte_a_pedir']) if r['soporte_a_pedir'] else ''} |\n")
        md.append("\n### Detalle\n\n")
        for r in rows:
            md.append(f"**{r['id']} · {r['titulo']}** [{r['severidad']} · {r['estado']} · {r['categoria']}]\n\n{r['detalle']}\n\n")
            if r["tratamiento"]:
                md.append(f"*Cómo lo trata el análisis:* {r['tratamiento']}\n\n")
            if r["verificable_con"]:
                md.append(f"*Verificable con:* `{r['verificable_con']}`\n\n")
            evs = r["evidencia"][:8]
            if evs:
                md.append("<details><summary>Evidencia (primeras filas)</summary>\n\n```json\n" + json.dumps(evs, ensure_ascii=False, indent=1, default=str)[:3500] + "\n```\n</details>\n\n")
    elif tipo == "B":
        md.append("| ID | Sev. | Commit | Qué estaba mal | Qué se hizo |\n|---|---|---|---|---|\n")
        for r in rows:
            md.append(f"| {r['id']} | {r['severidad']} | `{r['commit']}` | {r['titulo']} | {r['detalle']} |\n")
    elif tipo == "C":
        md.append("| ID | Sev. | Para | Pregunta | Por qué importa | Soporte a pedir |\n|---|---|---|---|---|---|\n")
        for r in rows:
            md.append(f"| {r['id']} | {r['severidad']} | {r['responsable']} | {r['pregunta']} | {r['detalle']} | {r['soporte_a_pedir']} |\n")
    else:
        md.append("| ID | Sev. | Limitación | Detalle |\n|---|---|---|---|\n")
        for r in rows:
            md.append(f"| {r['id']} | {r['severidad']} | {r['titulo']} | {r['detalle']} |\n")
md.append("\n## Paquete de auditoría\n\n")
md.append(f"- Fuente: `{XLSX.name}` · {paquete['fuente']['bytes']:,} bytes · SHA-256 `{paquete['fuente']['sha256']}` · {paquete['fuente']['hojas']} hojas ({paquete['fuente']['hojas_ocultas']} ocultas) · {paquete['fuente']['vinculos_externos']} vínculos externos.\n")
md.append("- Salidas (SHA-256):\n\n| Archivo | SHA-256 | Bytes |\n|---|---|---:|\n")
for s in paquete["salidas"]:
    md.append(f"| `{s['archivo']}` | `{s['sha256']}` | {s['bytes']:,} |\n")
md.append(f"\n- Entorno: Python {paquete['entorno']['python']} · openpyxl {paquete['entorno']['openpyxl']} · {paquete['entorno']['plataforma']} · commit base `{paquete['git']['commit_base']}` ({paquete['git']['rama']}).\n")
md.append("- Tolerancias aceptadas: Σ CIV vs M688 ≤ $100 (real +69); fila 34 $86.217; waterfall y NP al peso.\n")
md.append("- Reproducir todo:\n\n```bash\n" + "\n".join(paquete["reproducir"]) + "\n```\n")
md.append("\n*Cada asiento B indica el commit de git que introdujo la corrección; `git show <commit>` muestra el cambio exacto.*\n")
OUT_MD.write_text("".join(md), encoding="utf-8")

print(f"Registro: {len(registro)} asientos → {OUT_JSON}, {OUT_CSV}, {OUT_MD}")
print(json.dumps(resumen, ensure_ascii=False, indent=1))
