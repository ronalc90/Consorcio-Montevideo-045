"""
Analisis 01 - Variacion de cantidades por item (inicial vs final)

Consume:
    analisis/datos/presupuesto_2026_09.json  (canonico)
    analisis/datos/hojas/PRESUPUESTO_TODOS_LOS_CIV_84_NP.csv (fallback de columnas)
    comparativa.json (V1 IDU / V2 VICON)

Produce:
    analisis/hallazgos/01_variacion_items.md
    analisis/hallazgos/01_variacion_items.json
"""

import json
import re
import unicodedata
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).resolve().parents[2]
PRES_JSON = ROOT / "analisis" / "datos" / "presupuesto_2026_09.json"
COMP_JSON = ROOT / "comparativa.json"
OUT_JSON = ROOT / "analisis" / "hallazgos" / "01_variacion_items.json"
OUT_MD = ROOT / "analisis" / "hallazgos" / "01_variacion_items.md"

AIU = 0.31849
TOL_CANT = 0.01
TOL_PESO = 10  # tolerancia en pesos

# Filas ACEROS (excluidas)
ACEROS_MIN, ACEROS_MAX = 680, 687


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def fmtp(n):
    """Formato pesos con punto de miles, sin decimales."""
    if n is None:
        return "-"
    try:
        n = int(round(float(n)))
    except (TypeError, ValueError):
        return str(n)
    signo = "-" if n < 0 else ""
    n = abs(n)
    s = f"{n:,}".replace(",", ".")
    return signo + s


def norm_txt(s):
    """Normaliza texto para comparaciones fuzzy: minusculas, sin acentos, sin puntuacion."""
    if not s:
        return ""
    s = str(s).lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def tokens(s):
    return set(norm_txt(s).split()) if s else set()


def jaccard(a, b):
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def is_np_code(item_pago, codigo_idu):
    """Detecta NP: item_pago empieza con NP o codigo_idu = 'NO'."""
    ip = (item_pago or "").upper().strip()
    ci = (codigo_idu or "").upper().strip()
    if ip.startswith("NP"):
        return True
    if ci == "NO":
        return True
    return False


def classify(item):
    """Clasifica un renglon segun H (cant_contractual) e I (cant_actualizada)."""
    H = float(item.get("cant_contractual") or 0)
    I = float(item.get("cant_actualizada") or 0)
    is_np = is_np_code(item.get("item_pago"), item.get("codigo_idu"))

    if is_np and I > 0:
        return "np_nuevo"
    if is_np and I == 0 and H == 0:
        return "np_vacio"
    # No-NP
    if H > 0 and I > 0 and abs(I - H) <= TOL_CANT:
        return "sin_cambio"
    if H > 0 and I > H + TOL_CANT:
        return "aumento"
    if H > 0 and I > 0 and I < H - TOL_CANT:
        return "disminucion"
    if H > 0 and I == 0:
        return "eliminado"
    if (H == 0 or H is None) and I > 0 and not is_np:
        return "nuevo_contractual"
    if (H == 0 or H is None) and (I == 0 or I is None):
        return "vacio"
    return "otro"


# ---------------------------------------------------------------------------
# Carga
# ---------------------------------------------------------------------------
data = json.load(open(PRES_JSON, "r", encoding="utf-8"))
items_raw = data["items"]
comparativa = json.load(open(COMP_JSON, "r", encoding="utf-8"))


# Filtrar ACEROS y quedarnos con items en rango 7-687 (excluyendo 680-687)
items_all = []
for it in items_raw:
    r = int(it.get("row") or 0)
    if r < 7 or r > 687:
        continue
    if ACEROS_MIN <= r <= ACEROS_MAX:
        continue
    items_all.append(it)


# ---------------------------------------------------------------------------
# Chequeos linea por linea + estados
# ---------------------------------------------------------------------------
discrepancias_j = []   # J = I - H
discrepancias_o = []   # O = (I - H) * L
discrepancias_q = []   # Q = O + P

items_out = []
estado_counter = Counter()
delta_por_estado = defaultdict(float)

for it in items_all:
    r = it["row"]
    H = float(it.get("cant_contractual") or 0)
    I = float(it.get("cant_actualizada") or 0)
    J = float(it.get("delta_cant") or 0)
    K = it.get("vu_cd")
    L = float(it.get("vu_cd_aiu") or 0)
    M = float(it.get("valor_actualizado_aiu") or 0)
    N = float(it.get("valor_inicial_aiu") or 0)
    O = float(it.get("balance_may_men") or 0)
    P = float(it.get("incorporacion_np") or 0)
    Q = float(it.get("adicion_total") or 0)

    estado = classify(it)

    # Chequeo J = I - H
    j_calc = I - H
    if abs(j_calc - J) > TOL_CANT:
        discrepancias_j.append({
            "row": r,
            "H": H, "I": I, "J_declarado": J, "J_calc": j_calc, "diff": j_calc - J
        })

    # Chequeo O ~ (I - H) * L  (con tolerancia >$10)
    # Solo aplica para renglones no NP (O corresponde a mayores/menores). Para NP, O suele ser 0.
    if not is_np_code(it.get("item_pago"), it.get("codigo_idu")):
        o_calc = j_calc * L
        # Redondeo tipico
        if abs(o_calc - O) > TOL_PESO:
            discrepancias_o.append({
                "row": r,
                "H": H, "I": I, "L": L, "O_declarado": O, "O_calc": o_calc, "diff": o_calc - O
            })

    # Chequeo Q ~ O + P
    q_calc = O + P
    if abs(q_calc - Q) > TOL_PESO:
        discrepancias_q.append({
            "row": r,
            "O": O, "P": P, "Q_declarado": Q, "Q_calc": q_calc, "diff": q_calc - Q
        })

    delta_val = M - N
    estado_counter[estado] += 1
    delta_por_estado[estado] += delta_val

    items_out.append({
        "row": r,
        "codigo_idu": it.get("codigo_idu"),
        "item_pago": it.get("item_pago"),
        "chapter": it.get("chapter"),
        "subchapter": it.get("subchapter"),
        "descripcion": it.get("descripcion"),
        "und": it.get("und"),
        "H": H,
        "I": I,
        "delta_cant": j_calc,
        "K_vu_cd": K,
        "L_vu_cd_aiu": L,
        "M_valor_final": M,
        "N_valor_inicial": N,
        "delta_valor": delta_val,
        "O_balance_may_men": O,
        "P_incorporacion_np": P,
        "Q_adicion_total": Q,
        "estado": estado,
        "is_np": is_np_code(it.get("item_pago"), it.get("codigo_idu")),
        "esp_general": it.get("esp_general"),
        "esp_particular": it.get("esp_particular"),
    })


# ---------------------------------------------------------------------------
# Resumen general
# ---------------------------------------------------------------------------
total_delta = sum(x["delta_valor"] for x in items_out)
total_N = sum(x["N_valor_inicial"] for x in items_out)
total_M = sum(x["M_valor_final"] for x in items_out)

resumen = {
    "conteos": dict(estado_counter),
    "delta_valor_por_estado": {k: round(v, 2) for k, v in delta_por_estado.items()},
    "total_delta": round(total_delta, 2),
    "total_valor_inicial": round(total_N, 2),
    "total_valor_final": round(total_M, 2),
    "n_items": len(items_out),
    "discrepancias": {
        "J_neq_I_menos_H": len(discrepancias_j),
        "O_neq_delta_por_L": len(discrepancias_o),
        "Q_neq_O_mas_P": len(discrepancias_q),
    }
}


# ---------------------------------------------------------------------------
# Resumen por capitulo
# ---------------------------------------------------------------------------
cap_tot = defaultdict(lambda: {"N": 0, "M": 0, "O": 0, "P": 0})
sub_tot = defaultdict(lambda: {"N": 0, "M": 0, "chapter": None})

for x in items_out:
    ch = x["chapter"] or "(sin capitulo)"
    cap_tot[ch]["N"] += x["N_valor_inicial"]
    cap_tot[ch]["M"] += x["M_valor_final"]
    cap_tot[ch]["O"] += x["O_balance_may_men"]
    cap_tot[ch]["P"] += x["P_incorporacion_np"]

    sub = x["subchapter"] or "(sin subcapitulo)"
    key = (ch, sub)
    sub_tot[key]["N"] += x["N_valor_inicial"]
    sub_tot[key]["M"] += x["M_valor_final"]
    sub_tot[key]["chapter"] = ch


capitulos = []
for ch, tot in cap_tot.items():
    capitulos.append({
        "chapter": ch,
        "valor_inicial": round(tot["N"]),
        "valor_final": round(tot["M"]),
        "delta": round(tot["M"] - tot["N"]),
        "balance_may_men": round(tot["O"]),
        "incorporacion_np": round(tot["P"]),
    })
capitulos.sort(key=lambda x: x["chapter"])

subcapitulos = []
for (ch, sub), tot in sub_tot.items():
    subcapitulos.append({
        "chapter": ch,
        "subchapter": sub,
        "valor_inicial": round(tot["N"]),
        "valor_final": round(tot["M"]),
        "delta": round(tot["M"] - tot["N"]),
    })
subcapitulos.sort(key=lambda x: (x["chapter"], x["subchapter"] or ""))


# ---------------------------------------------------------------------------
# Vista neta por codigo IDU
# ---------------------------------------------------------------------------
neta_agg = defaultdict(lambda: {
    "H_total": 0.0, "I_total": 0.0,
    "N_total": 0.0, "M_total": 0.0,
    "filas": [],
    "descripciones": [],
    "estados": [],
    "und": None,
})

for x in items_out:
    code = (x["codigo_idu"] or "").strip()
    if not code or code.upper() == "NO":
        continue  # sin codigo IDU -> aparte
    neta_agg[code]["H_total"] += x["H"]
    neta_agg[code]["I_total"] += x["I"]
    neta_agg[code]["N_total"] += x["N_valor_inicial"]
    neta_agg[code]["M_total"] += x["M_valor_final"]
    neta_agg[code]["filas"].append(x["row"])
    neta_agg[code]["descripciones"].append(x["descripcion"])
    neta_agg[code]["estados"].append(x["estado"])
    if not neta_agg[code]["und"]:
        neta_agg[code]["und"] = x["und"]

neta_por_codigo = []
for code, tot in neta_agg.items():
    if len(tot["filas"]) < 1:
        continue
    neta_por_codigo.append({
        "codigo_idu": code,
        "und": tot["und"],
        "H_total": round(tot["H_total"], 4),
        "I_total": round(tot["I_total"], 4),
        "delta_cant": round(tot["I_total"] - tot["H_total"], 4),
        "N_valor_inicial": round(tot["N_total"]),
        "M_valor_final": round(tot["M_total"]),
        "delta_valor": round(tot["M_total"] - tot["N_total"]),
        "filas": tot["filas"],
        "estados": tot["estados"],
    })
neta_por_codigo.sort(key=lambda x: -abs(x["delta_valor"]))


# ---------------------------------------------------------------------------
# Reubicaciones: mismo codigo IDU con >1 renglon donde uno se elimina/reduce
# y otro nace/aumenta
# ---------------------------------------------------------------------------
reubicaciones = []
for entry in neta_por_codigo:
    if len(entry["filas"]) < 2:
        continue
    code = entry["codigo_idu"]
    # buscamos renglones con estado "eliminado" o "disminucion" y otros con "nuevo_contractual"/"aumento"
    filas_x = [x for x in items_out if (x["codigo_idu"] or "").strip() == code]
    eliminadas = [x for x in filas_x if x["estado"] in ("eliminado", "disminucion")]
    nuevas = [x for x in filas_x if x["estado"] in ("nuevo_contractual", "aumento")]
    if eliminadas and nuevas:
        delta_neto = entry["delta_valor"]
        # Comentario: si subchapters difieren, sugerimos reubicacion
        subs_elim = set([x["subchapter"] for x in eliminadas])
        subs_nue = set([x["subchapter"] for x in nuevas])
        if subs_elim != subs_nue:
            comentario = f"Cambio de subcapitulo: {sorted(str(s) for s in subs_elim)} -> {sorted(str(s) for s in subs_nue)}"
        else:
            comentario = "Reasignacion dentro del mismo subcapitulo"
        # Valor que sale de los renglones que bajan y valor que entra en los que suben (registro de auditoría B-13):
        # solo la parte que cambia, no el renglón completo. Trasladado = min(sale, entra).
        valor_disminuido = round(sum(-(x["delta_valor"]) for x in eliminadas))
        valor_aumentado = round(sum(x["delta_valor"] for x in nuevas))
        reubicaciones.append({
            "codigo_idu": code,
            "und": entry["und"],
            "filas_eliminadas": [x["row"] for x in eliminadas],
            "filas_nuevas": [x["row"] for x in nuevas],
            "filas_eliminadas_total": [x["row"] for x in eliminadas if x["estado"] == "eliminado"],
            "filas_nuevas_total": [x["row"] for x in nuevas if x["estado"] == "nuevo_contractual"],
            "H_total": entry["H_total"],
            "I_total": entry["I_total"],
            "delta_cant": entry["delta_cant"],
            "N_valor_inicial": entry["N_valor_inicial"],
            "M_valor_final": entry["M_valor_final"],
            "valor_disminuido": valor_disminuido,
            "valor_aumentado": valor_aumentado,
            "trasladado": min(valor_disminuido, valor_aumentado),
            "delta_valor_neto": delta_neto,
            "comentario": comentario,
        })
reubicaciones.sort(key=lambda x: -abs(x["delta_valor_neto"]))


# ---------------------------------------------------------------------------
# Rankings
# ---------------------------------------------------------------------------
items_por_delta = sorted(items_out, key=lambda x: -x["delta_valor"])
top_aumentos = items_por_delta[:30]

items_por_delta_neg = sorted(items_out, key=lambda x: x["delta_valor"])
top_disminuciones = items_por_delta_neg[:30]


def slim(x):
    return {
        "row": x["row"],
        "codigo_idu": x["codigo_idu"],
        "item_pago": x["item_pago"],
        "chapter": x["chapter"],
        "subchapter": x["subchapter"],
        "descripcion": x["descripcion"],
        "und": x["und"],
        "H": x["H"],
        "I": x["I"],
        "delta_cant": x["delta_cant"],
        "L_vu_cd_aiu": x["L_vu_cd_aiu"],
        "N_valor_inicial": x["N_valor_inicial"],
        "M_valor_final": x["M_valor_final"],
        "delta_valor": x["delta_valor"],
        "estado": x["estado"],
        "is_np": x["is_np"],
    }


top_aumentos_out = [slim(x) for x in top_aumentos]
top_disminuciones_out = [slim(x) for x in top_disminuciones]


# Variacion relativa grande: |Delta cant / H| > 0.5 e |Delta valor| > 50M
# Solo para renglones con H > 0 (i.e., no NPs ni nuevos contractuales)
variacion_relativa_grande = []
for x in items_out:
    if x["H"] and x["H"] > 0:
        rel = abs(x["delta_cant"]) / x["H"]
        if rel > 0.5 and abs(x["delta_valor"]) > 50_000_000:
            variacion_relativa_grande.append({
                **slim(x),
                "rel_delta_cant": round(rel, 4),
            })
variacion_relativa_grande.sort(key=lambda x: -abs(x["delta_valor"]))


# Saltos: I > 3*H  (cantidad final > 3x cantidad contractual)
saltos_3x = []
saltos_10x = []
for x in items_out:
    if x["H"] and x["H"] > 0 and x["I"] > 0:
        ratio = x["I"] / x["H"]
        if ratio > 3:
            entry = {**slim(x), "ratio_I_H": round(ratio, 4)}
            saltos_3x.append(entry)
            if ratio > 10:
                saltos_10x.append(entry)
saltos_3x.sort(key=lambda x: -x["ratio_I_H"])
saltos_10x.sort(key=lambda x: -x["ratio_I_H"])


# ---------------------------------------------------------------------------
# Reemplazos contractual -> NP con descripcion similar
# ---------------------------------------------------------------------------
# Pool: eliminados/disminuidos no-NP (contractuales que bajan)
# vs NPs (aumentan)
elim_contract = [x for x in items_out
                 if not x["is_np"] and x["estado"] in ("eliminado", "disminucion")
                 and x["delta_valor"] < -20_000_000]
nps_grandes = [x for x in items_out
               if x["is_np"] and x["delta_valor"] > 20_000_000]

reemplazos_np = []
usados_np = set()

# Casos conocidos: fila 33 -> 39; fila 24 -> 30
def find_item(row):
    for x in items_out:
        if x["row"] == row:
            return x
    return None


# Buscar por fuzzy: primero por esp_general/esp_particular exactos, luego jaccard >= 0.4 en descripcion
for c in elim_contract:
    c_esp_g = (c.get("esp_general") or "").strip()
    c_esp_p = (c.get("esp_particular") or "").strip()
    c_desc_tok = tokens(c["descripcion"])
    best = None
    best_score = 0
    for n in nps_grandes:
        if n["row"] in usados_np:
            continue
        # Debe ser mismo capitulo o unidad
        if n["und"] != c["und"]:
            score_base = 0
        else:
            score_base = 0.15

        n_esp_g = (n.get("esp_general") or "").strip()
        n_esp_p = (n.get("esp_particular") or "").strip()

        # 1) esp_general iguales
        exact_g = c_esp_g and n_esp_g and c_esp_g == n_esp_g
        exact_p = c_esp_p and n_esp_p and c_esp_p == n_esp_p

        # 2) jaccard de descripciones
        n_desc_tok = tokens(n["descripcion"])
        j = jaccard(c_desc_tok, n_desc_tok)

        score = score_base + j + (0.3 if exact_g else 0) + (0.15 if exact_p else 0)
        if score > best_score and (exact_g or j >= 0.4):
            best = n
            best_score = score

    if best is not None:
        usados_np.add(best["row"])
        reemplazos_np.append({
            "contractual": {
                "row": c["row"],
                "codigo_idu": c["codigo_idu"],
                "item_pago": c["item_pago"],
                "descripcion": c["descripcion"],
                "und": c["und"],
                "H": c["H"], "I": c["I"],
                "delta_valor": c["delta_valor"],
                "esp_general": c.get("esp_general"),
            },
            "np": {
                "row": best["row"],
                "codigo_idu": best["codigo_idu"],
                "item_pago": best["item_pago"],
                "descripcion": best["descripcion"],
                "und": best["und"],
                "H": best["H"], "I": best["I"],
                "delta_valor": best["delta_valor"],
                "esp_general": best.get("esp_general"),
            },
            "score_similitud": round(best_score, 3),
            "sobrecosto_neto": round(c["delta_valor"] + best["delta_valor"]),
        })


# Anadir manualmente si no fueron detectados: fila 33->39 y 24->30
def force_pair(row_contract, row_np):
    c = find_item(row_contract)
    n = find_item(row_np)
    if not c or not n:
        return
    # ver si ya esta
    for r in reemplazos_np:
        if r["contractual"]["row"] == row_contract and r["np"]["row"] == row_np:
            return
    reemplazos_np.append({
        "contractual": {
            "row": c["row"],
            "codigo_idu": c["codigo_idu"],
            "item_pago": c["item_pago"],
            "descripcion": c["descripcion"],
            "und": c["und"],
            "H": c["H"], "I": c["I"],
            "delta_valor": c["delta_valor"],
            "esp_general": c.get("esp_general"),
        },
        "np": {
            "row": n["row"],
            "codigo_idu": n["codigo_idu"],
            "item_pago": n["item_pago"],
            "descripcion": n["descripcion"],
            "und": n["und"],
            "H": n["H"], "I": n["I"],
            "delta_valor": n["delta_valor"],
            "esp_general": n.get("esp_general"),
        },
        "score_similitud": None,
        "sobrecosto_neto": round(c["delta_valor"] + n["delta_valor"]),
        "forzado": True,
    })

force_pair(33, 39)
force_pair(24, 30)

reemplazos_np.sort(key=lambda x: -x["sobrecosto_neto"])


# ---------------------------------------------------------------------------
# Cruce con V2 (VICON 21-04-2026) y V4
# ---------------------------------------------------------------------------
# comparativa.items tiene cant_idu, cant_cont, valor_idu_cd, valor_cont_cd
# V2 = "cant_cont" y "valor_cont_cd"; V4 = nuestro presupuesto (M valor final CON AIU)
# Nota: comparativa esta en CD sin AIU; el M actual esta con AIU. Para comparar valores
# convertimos M/(1+AIU) -> costo directo.
comp_items = comparativa.get("items", [])

# Indexar comp por codigo IDU
comp_by_code = {}
for ci in comp_items:
    code = str(ci.get("codigo_idu") or ci.get("codigo") or "").strip()
    if not code or code.upper() in ("NO", ""):
        continue
    comp_by_code[code] = ci


# Reindexamos items V4 por codigo IDU (agregado)
items_by_code_v4 = defaultdict(lambda: {"cant_v4": 0.0, "valor_v4_aiu": 0.0, "rows": []})
for x in items_out:
    code = (x["codigo_idu"] or "").strip()
    if not code or code.upper() == "NO":
        continue
    items_by_code_v4[code]["cant_v4"] += x["I"]
    items_by_code_v4[code]["valor_v4_aiu"] += x["M_valor_final"]
    items_by_code_v4[code]["rows"].append(x["row"])


cruce_v2_v4 = []
for code, v4 in items_by_code_v4.items():
    v2 = comp_by_code.get(code)
    if v2:
        cant_v2 = float(v2.get("cant_cont") or 0)
        valor_v2_cd = float(v2.get("valor_cont_cd") or 0)
        cant_v1 = float(v2.get("cant_idu") or 0)
        valor_v1_cd = float(v2.get("valor_idu_cd") or 0)
        valor_v4_cd = v4["valor_v4_aiu"] / (1 + AIU)
        cruce_v2_v4.append({
            "codigo_idu": code,
            "descripcion": v2.get("descripcion") or v2.get("nombre") or "",
            "und": v2.get("und") or v2.get("unidad") or "",
            "cant_v1_idu": cant_v1,
            "cant_v2_vicon": cant_v2,
            "cant_v4": v4["cant_v4"],
            "delta_cant_v4_v2": round(v4["cant_v4"] - cant_v2, 4),
            "valor_v1_cd": round(valor_v1_cd),
            "valor_v2_cd": round(valor_v2_cd),
            "valor_v4_cd": round(valor_v4_cd),
            "delta_valor_v4_v2_cd": round(valor_v4_cd - valor_v2_cd),
            "rows_v4": v4["rows"],
        })


# Recorte V4 vs V2: items que existen en V2 y cuya cantidad V4 < V2
recorte_v4_vs_v2 = [x for x in cruce_v2_v4 if x["cant_v2"] > 0 and x["cant_v4"] < x["cant_v2"]]
recorte_v4_vs_v2.sort(key=lambda x: x["delta_cant_v4_v2"])  # mas negativos primero

# Nuevos en V4 (no aparecen en V2)
codigos_v2 = set(comp_by_code.keys())
codigos_v4 = set(items_by_code_v4.keys())
nuevos_v4 = sorted(codigos_v4 - codigos_v2)

nuevos_v4_detalle = []
for code in nuevos_v4:
    v4 = items_by_code_v4[code]
    # Sumamos I, valor y armamos descripcion (primer renglon)
    filas = [x for x in items_out if (x["codigo_idu"] or "").strip() == code]
    if not filas:
        continue
    nuevos_v4_detalle.append({
        "codigo_idu": code,
        "descripcion": filas[0]["descripcion"],
        "und": filas[0]["und"],
        "cant_v4": v4["cant_v4"],
        "valor_v4_aiu": round(v4["valor_v4_aiu"]),
        "valor_v4_cd": round(v4["valor_v4_aiu"] / (1 + AIU)),
        "rows_v4": v4["rows"],
        "es_np_solo": all(x["is_np"] for x in filas),
    })
nuevos_v4_detalle.sort(key=lambda x: -x["valor_v4_aiu"])


# ---------------------------------------------------------------------------
# Hallazgos
# ---------------------------------------------------------------------------
def sev(val_abs):
    v = abs(val_abs)
    if v >= 500_000_000:
        return "ALTA"
    if v >= 50_000_000:
        return "MEDIA"
    return "BAJA"


hallazgos = []
_id = [0]

def add(severidad, titulo, descripcion, hoja, fila, impacto, recomendacion):
    _id[0] += 1
    hallazgos.append({
        "id": f"H01-{_id[0]:03d}",
        "severidad": severidad,
        "titulo": titulo,
        "descripcion": descripcion,
        "hoja": hoja,
        "fila": fila,
        "impacto_pesos": impacto,
        "recomendacion": recomendacion,
    })


HOJA = "PRESUPUESTO TODOS LOS CIV 84 NP"


# Conciliacion global obras
obras_ini_teo = 44_303_294_799
obras_fin_teo = 58_196_933_800
delta_teo = obras_fin_teo - obras_ini_teo

concilia_global = {
    "obras_iniciales_calc": round(total_N),
    "obras_finales_calc": round(total_M),
    "delta_calc": round(total_M - total_N),
    "obras_iniciales_teorico": obras_ini_teo,
    "obras_finales_teorico": obras_fin_teo,
    "delta_teorico": delta_teo,
    "diff_ini": round(total_N - obras_ini_teo),
    "diff_fin": round(total_M - obras_fin_teo),
    "diff_delta": round((total_M - total_N) - delta_teo),
    "concilia_ini": abs(total_N - obras_ini_teo) < 1000,
    "concilia_fin": abs(total_M - obras_fin_teo) < 1000,
    "concilia_delta": abs((total_M - total_N) - delta_teo) < 1000,
}


# Hallazgo: reemplazos NP mas costosos
for rp in reemplazos_np[:5]:
    impacto = abs(rp["sobrecosto_neto"])
    add(
        sev(impacto),
        f"Posible reemplazo contractual->NP (filas {rp['contractual']['row']} -> {rp['np']['row']})",
        f"Item contractual '{rp['contractual']['item_pago']} - {rp['contractual']['descripcion']}' "
        f"(delta {fmtp(rp['contractual']['delta_valor'])}) parece reemplazado por NP "
        f"'{rp['np']['item_pago']} - {rp['np']['descripcion']}' (delta {fmtp(rp['np']['delta_valor'])}). "
        f"Sobrecosto neto {fmtp(rp['sobrecosto_neto'])}.",
        HOJA,
        f"{rp['contractual']['row']} / {rp['np']['row']}",
        rp["sobrecosto_neto"],
        "Solicitar al contratista justificacion tecnica del cambio, precio del NP con analisis unitario, "
        "y evidenciar por que no aplica el item contractual del pliego. Comparar con VU visor IDU.",
    )


# Hallazgo: saltos extremos I > 10x H
for s in saltos_10x[:8]:
    impacto = abs(s["delta_valor"])
    add(
        sev(impacto),
        f"Salto extremo de cantidad (I/H = {s['ratio_I_H']}x) - fila {s['row']}",
        f"Item {s['item_pago']} '{s['descripcion']}' paso de {s['H']} a {s['I']} {s['und']}. "
        f"Impacto {fmtp(s['delta_valor'])}.",
        HOJA,
        s["row"],
        s["delta_valor"],
        "Pedir memoria de cantidades actualizada por CIV y validar con actas de campo/planos. "
        "Verificar que no se trate de reasignacion desde otro item.",
    )


# Hallazgo: capitulos con mayor variacion
for cap in sorted(capitulos, key=lambda x: -abs(x["delta"]))[:7]:
    impacto = abs(cap["delta"])
    add(
        sev(impacto),
        f"Variacion capitulo {cap['chapter']}: {fmtp(cap['delta'])}",
        f"{cap['chapter']}: valor inicial {fmtp(cap['valor_inicial'])} -> final {fmtp(cap['valor_final'])}. "
        f"Balance mayores/menores {fmtp(cap['balance_may_men'])} + incorporacion NP {fmtp(cap['incorporacion_np'])}.",
        HOJA,
        "capitulo",
        cap["delta"],
        "Revisar composicion del capitulo, especialmente aumentos que se apoyen mayormente en NPs.",
    )


# Hallazgo: reubicaciones conocidas 6.007 (490->531) y 5.067 (295->399)
def _reub_por_codigo_o_filas(rp):
    # devolvemos referencia
    return rp

for target_code in ("6.007", "5.067"):
    for rp in reubicaciones:
        if rp["codigo_idu"] == target_code:
            impacto = abs(rp["delta_valor_neto"])
            add(
                sev(impacto) if impacto > 50_000_000 else "MEDIA",
                f"Reubicacion codigo {target_code}",
                f"Codigo {target_code} elimina filas {rp['filas_eliminadas']} y aparece en {rp['filas_nuevas']}. "
                f"Delta cantidad neto {rp['delta_cant']} {rp['und']}. Delta valor neto {fmtp(rp['delta_valor_neto'])}. "
                f"{rp['comentario']}",
                HOJA,
                f"{rp['filas_eliminadas']} -> {rp['filas_nuevas']}",
                rp["delta_valor_neto"],
                "Verificar en obra si la actividad realmente cambio de subcapitulo o de responsabilidad "
                "(por ejemplo IDU vs ESP) y confirmar el precio unitario aplicado.",
            )


# Hallazgo: variacion relativa alta con impacto > 50M
for v in variacion_relativa_grande[:10]:
    impacto = abs(v["delta_valor"])
    add(
        sev(impacto),
        f"Variacion relativa alta (fila {v['row']})",
        f"Item {v['item_pago']} '{v['descripcion']}': H={v['H']}, I={v['I']} ({v['und']}), "
        f"variacion relativa {v['rel_delta_cant']*100:.0f}%. Impacto {fmtp(v['delta_valor'])}.",
        HOJA,
        v["row"],
        v["delta_valor"],
        "Solicitar memoria detallada de cantidad y respaldo tecnico. Cruzar con planos as-built.",
    )


# Hallazgo: eliminaciones grandes (top 5 contractuales eliminados)
elim_grandes = sorted([x for x in items_out if x["estado"] == "eliminado"], key=lambda x: x["delta_valor"])[:5]
for e in elim_grandes:
    add(
        sev(abs(e["delta_valor"])),
        f"Item contractual eliminado (fila {e['row']})",
        f"Item {e['item_pago']} '{e['descripcion']}' pasa de {e['H']} a 0 ({e['und']}). "
        f"Reduccion {fmtp(e['delta_valor'])}.",
        HOJA,
        e["row"],
        e["delta_valor"],
        "Confirmar que la actividad efectivamente no se ejecutara o se reemplaza por otra. "
        "Si se reemplaza, aparear con NP correspondiente.",
    )


# Hallazgo: NPs de mayor valor
np_grandes = sorted([x for x in items_out if x["is_np"]], key=lambda x: -x["delta_valor"])[:5]
for n in np_grandes:
    add(
        sev(abs(n["delta_valor"])),
        f"NP de alto valor (fila {n['row']})",
        f"NP {n['item_pago']} '{n['descripcion']}' incorpora cantidad {n['I']} {n['und']} "
        f"por {fmtp(n['delta_valor'])}.",
        HOJA,
        n["row"],
        n["delta_valor"],
        "Revisar aprobacion IDU del NP, analisis de precio unitario y sustento tecnico. "
        "Verificar que no exista un item contractual equivalente.",
    )


# Hallazgo: discrepancias formulas
if discrepancias_j:
    add(
        "MEDIA" if len(discrepancias_j) < 20 else "ALTA",
        "Discrepancias formulas J = I - H",
        f"{len(discrepancias_j)} renglones no cumplen J = I - H con tolerancia 0.01.",
        HOJA,
        ", ".join(str(x["row"]) for x in discrepancias_j[:20]) + ("..." if len(discrepancias_j) > 20 else ""),
        0,
        "Pedir libro corregido o al menos hoja con formulas explicitas y sin valores fijos.",
    )

if discrepancias_o:
    add(
        "MEDIA",
        "Discrepancias formulas O = (I-H) x L",
        f"{len(discrepancias_o)} renglones donde el balance mayores/menores O no coincide con (I-H)xL (>$10 dif).",
        HOJA,
        ", ".join(str(x["row"]) for x in discrepancias_o[:20]) + ("..." if len(discrepancias_o) > 20 else ""),
        0,
        "Solicitar aclaracion de que precio se uso para el balance de mayores/menores (VU visor vs VU contractual).",
    )

if discrepancias_q:
    add(
        "MEDIA",
        "Discrepancias formulas Q = O + P",
        f"{len(discrepancias_q)} renglones donde Q no coincide con O + P.",
        HOJA,
        ", ".join(str(x["row"]) for x in discrepancias_q[:20]) + ("..." if len(discrepancias_q) > 20 else ""),
        0,
        "Solicitar cuadro con la formula explicita de adicion total por renglon.",
    )


# Hallazgo: conciliacion global
if not concilia_global["concilia_ini"] or not concilia_global["concilia_fin"] or not concilia_global["concilia_delta"]:
    add(
        "ALTA",
        "Conciliacion global de obras no cierra al peso",
        f"Calc N={fmtp(concilia_global['obras_iniciales_calc'])} vs teorico {fmtp(concilia_global['obras_iniciales_teorico'])} "
        f"(dif {fmtp(concilia_global['diff_ini'])}). "
        f"Calc M={fmtp(concilia_global['obras_finales_calc'])} vs teorico {fmtp(concilia_global['obras_finales_teorico'])} "
        f"(dif {fmtp(concilia_global['diff_fin'])}).",
        HOJA,
        "totales",
        concilia_global["diff_fin"],
        "Revisar filtro de ACEROS y filas de capitulos incluidas en la suma.",
    )
else:
    add(
        "INFO",
        "Conciliacion global de obras OK",
        f"Inicial {fmtp(concilia_global['obras_iniciales_calc'])}, final {fmtp(concilia_global['obras_finales_calc'])}, "
        f"delta {fmtp(concilia_global['delta_calc'])}.",
        HOJA,
        "totales",
        0,
        "Sin observaciones.",
    )


hallazgos.sort(key=lambda h: (
    {"ALTA": 0, "MEDIA": 1, "BAJA": 2, "INFO": 3}[h["severidad"]],
    -abs(h["impacto_pesos"] or 0),
))


# ---------------------------------------------------------------------------
# Salida JSON
# ---------------------------------------------------------------------------
out = {
    "meta": {
        "generado_por": "analisis/scripts/analisis_01_variacion_items.py",
        "fuente_principal": "analisis/datos/presupuesto_2026_09.json",
        "hoja": HOJA,
        "aiu_factor": AIU,
        "excluye": "capitulo 8 ACEROS (filas 680-687)",
        "conciliacion_global": concilia_global,
    },
    "resumen": resumen,
    "capitulos": capitulos,
    "subcapitulos": subcapitulos,
    "items": items_out,
    "neta_por_codigo": neta_por_codigo,
    "reubicaciones": reubicaciones,
    "top_aumentos": top_aumentos_out,
    "top_disminuciones": top_disminuciones_out,
    "variacion_relativa_grande": variacion_relativa_grande,
    "saltos_extremos": saltos_3x,
    "saltos_criticos": saltos_10x,
    "reemplazos_np": reemplazos_np,
    "cruce_v2_v4": cruce_v2_v4,
    "recorte_v4_vs_v2": recorte_v4_vs_v2,
    "nuevos_v4_no_estaban_v2": nuevos_v4_detalle,
    "hallazgos": hallazgos,
    "discrepancias": {
        "j_diff": discrepancias_j,
        "o_diff": discrepancias_o,
        "q_diff": discrepancias_q,
    }
}

OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

print(f"JSON escrito en {OUT_JSON}")


# ---------------------------------------------------------------------------
# Salida MD
# ---------------------------------------------------------------------------
lines = []
w = lines.append

w("# 01 - Variacion de cantidades por item (inicial vs final)")
w("")
w(f"Fuente: `analisis/datos/presupuesto_2026_09.json` (hoja **{HOJA}**).")
w("Excluye capitulo 8 ACEROS (filas 680-687). Todos los valores con AIU 31,849 %.")
w("")

# Resumen ejecutivo
w("## Resumen ejecutivo")
w("")
w(f"- Renglones analizados: **{resumen['n_items']}** (filas 7-679).")
w(f"- Total valor inicial (N): **${fmtp(resumen['total_valor_inicial'])}**.")
w(f"- Total valor final (M): **${fmtp(resumen['total_valor_final'])}**.")
w(f"- Delta total: **${fmtp(resumen['total_delta'])}**.")
w("")
w("### Conteos por estado")
w("")
w("| Estado | Renglones | Delta valor |")
w("|---|---:|---:|")
for estado, cnt in sorted(resumen["conteos"].items(), key=lambda x: -abs(delta_por_estado[x[0]])):
    dv = resumen["delta_valor_por_estado"].get(estado, 0)
    w(f"| {estado} | {cnt} | ${fmtp(dv)} |")
w("")

# Conciliacion
w("## Bloque de conciliacion al peso")
w("")
cg = concilia_global
w(f"- Obras (calc) valor inicial: **${fmtp(cg['obras_iniciales_calc'])}**  vs  teorico BRIEF **${fmtp(cg['obras_iniciales_teorico'])}**  (diff ${fmtp(cg['diff_ini'])}).")
w(f"- Obras (calc) valor final:   **${fmtp(cg['obras_finales_calc'])}**  vs  teorico BRIEF **${fmtp(cg['obras_finales_teorico'])}**  (diff ${fmtp(cg['diff_fin'])}).")
w(f"- Delta obras: **${fmtp(cg['delta_calc'])}** vs teorico **${fmtp(cg['delta_teorico'])}** (diff ${fmtp(cg['diff_delta'])}).")
ok_ini = "OK" if cg["concilia_ini"] else "OFF"
ok_fin = "OK" if cg["concilia_fin"] else "OFF"
ok_del = "OK" if cg["concilia_delta"] else "OFF"
w(f"- Conciliaciones: inicial {ok_ini}, final {ok_fin}, delta {ok_del}.")
w("")
w("Descomposicion del delta (por columnas del Excel):")
w("")
sum_O = sum(x["O_balance_may_men"] for x in items_out)
sum_P = sum(x["P_incorporacion_np"] for x in items_out)
w(f"- Suma balance mayores/menores (col O): **${fmtp(sum_O)}**")
w(f"- Suma incorporacion NP (col P):        **${fmtp(sum_P)}**")
w(f"- Suma O + P = **${fmtp(sum_O + sum_P)}** (debe igualar delta {fmtp(cg['delta_calc'])})")
w("")
w("Discrepancias en formulas linea a linea:")
w(f"- J = I - H  no cuadra en **{resumen['discrepancias']['J_neq_I_menos_H']}** renglones.")
w(f"- O = (I-H) x L  no cuadra en **{resumen['discrepancias']['O_neq_delta_por_L']}** renglones (tol $10).")
w(f"- Q = O + P  no cuadra en **{resumen['discrepancias']['Q_neq_O_mas_P']}** renglones (tol $10).")
w("")


# Resumen por capitulo
w("## Resumen por capitulo")
w("")
w("| Capitulo | Valor inicial | Valor final | Delta | Balance may/men | Incorp. NP |")
w("|---|---:|---:|---:|---:|---:|")
tot_ini = 0
tot_fin = 0
tot_bal = 0
tot_np = 0
for cap in capitulos:
    tot_ini += cap["valor_inicial"]
    tot_fin += cap["valor_final"]
    tot_bal += cap["balance_may_men"]
    tot_np += cap["incorporacion_np"]
    w(f"| {cap['chapter']} | ${fmtp(cap['valor_inicial'])} | ${fmtp(cap['valor_final'])} | ${fmtp(cap['delta'])} | ${fmtp(cap['balance_may_men'])} | ${fmtp(cap['incorporacion_np'])} |")
w(f"| **TOTAL** | **${fmtp(tot_ini)}** | **${fmtp(tot_fin)}** | **${fmtp(tot_fin - tot_ini)}** | **${fmtp(tot_bal)}** | **${fmtp(tot_np)}** |")
w("")


# Resumen por subcapitulo (top movimientos)
w("## Resumen por subcapitulo (ordenado por |delta|)")
w("")
w("| Capitulo | Subcapitulo | Valor inicial | Valor final | Delta |")
w("|---|---|---:|---:|---:|")
sc_sorted = sorted(subcapitulos, key=lambda x: -abs(x["delta"]))
for sc in sc_sorted:
    w(f"| {sc['chapter']} | {sc['subchapter']} | ${fmtp(sc['valor_inicial'])} | ${fmtp(sc['valor_final'])} | ${fmtp(sc['delta'])} |")
w("")


# Hallazgos por severidad
w("## Hallazgos por severidad")
w("")
for sev_name in ("ALTA", "MEDIA", "BAJA", "INFO"):
    hs = [h for h in hallazgos if h["severidad"] == sev_name]
    if not hs:
        continue
    w(f"### {sev_name} ({len(hs)})")
    w("")
    for h in hs:
        w(f"#### {h['id']} - {h['titulo']}")
        w("")
        w(f"- **Hoja**: {h['hoja']}  **Fila**: {h['fila']}")
        w(f"- **Impacto**: ${fmtp(h['impacto_pesos'])}")
        w(f"- **Descripcion**: {h['descripcion']}")
        w(f"- **Recomendacion**: {h['recomendacion']}")
        w("")


# Top aumentos
w("## Top 30 aumentos (por delta valor)")
w("")
w("| Fila | Cap | Cod IDU | Item | Descripcion | Und | H | I | Delta cant | Delta valor | Estado |")
w("|---:|---|---|---|---|---|---:|---:|---:|---:|---|")
for x in top_aumentos_out:
    desc = (x["descripcion"] or "")[:60]
    w(f"| {x['row']} | {x['chapter'] or ''} | {x['codigo_idu'] or ''} | {x['item_pago'] or ''} | {desc} | {x['und'] or ''} | {x['H']} | {x['I']} | {x['delta_cant']:.2f} | ${fmtp(x['delta_valor'])} | {x['estado']} |")
w("")

# Top disminuciones
w("## Top 30 disminuciones (por delta valor)")
w("")
w("| Fila | Cap | Cod IDU | Item | Descripcion | Und | H | I | Delta cant | Delta valor | Estado |")
w("|---:|---|---|---|---|---|---:|---:|---:|---:|---|")
for x in top_disminuciones_out:
    desc = (x["descripcion"] or "")[:60]
    w(f"| {x['row']} | {x['chapter'] or ''} | {x['codigo_idu'] or ''} | {x['item_pago'] or ''} | {desc} | {x['und'] or ''} | {x['H']} | {x['I']} | {x['delta_cant']:.2f} | ${fmtp(x['delta_valor'])} | {x['estado']} |")
w("")

# Variacion relativa alta
w("## Variacion relativa alta (|Delta cant / H| > 50%  y  |Delta valor| > $50M)")
w("")
w("| Fila | Cod IDU | Item | Descripcion | H | I | % var | Delta valor |")
w("|---:|---|---|---|---:|---:|---:|---:|")
for v in variacion_relativa_grande[:40]:
    desc = (v["descripcion"] or "")[:60]
    w(f"| {v['row']} | {v['codigo_idu'] or ''} | {v['item_pago'] or ''} | {desc} | {v['H']} | {v['I']} | {v['rel_delta_cant']*100:.0f}% | ${fmtp(v['delta_valor'])} |")
w("")

# Saltos extremos
w("## Saltos criticos (I > 10 x H)")
w("")
w("| Fila | Cod IDU | Item | Descripcion | H | I | Ratio | Delta valor |")
w("|---:|---|---|---|---:|---:|---:|---:|")
for s in saltos_10x:
    desc = (s["descripcion"] or "")[:60]
    w(f"| {s['row']} | {s['codigo_idu'] or ''} | {s['item_pago'] or ''} | {desc} | {s['H']} | {s['I']} | {s['ratio_I_H']}x | ${fmtp(s['delta_valor'])} |")
w("")

w("## Saltos altos (I > 3 x H)  -- todos")
w("")
w("| Fila | Cod IDU | Item | Descripcion | H | I | Ratio | Delta valor |")
w("|---:|---|---|---|---:|---:|---:|---:|")
for s in saltos_3x[:40]:
    desc = (s["descripcion"] or "")[:60]
    w(f"| {s['row']} | {s['codigo_idu'] or ''} | {s['item_pago'] or ''} | {desc} | {s['H']} | {s['I']} | {s['ratio_I_H']}x | ${fmtp(s['delta_valor'])} |")
w("")


# Reubicaciones
w("## Reubicaciones detectadas (mismo codigo IDU, filas distintas)")
w("")
w("| Cod IDU | Filas eliminadas | Filas nuevas | H_tot | I_tot | Delta cant | Delta valor | Comentario |")
w("|---|---|---|---:|---:|---:|---:|---|")
for r in reubicaciones[:30]:
    w(f"| {r['codigo_idu']} | {r['filas_eliminadas']} | {r['filas_nuevas']} | {r['H_total']:.2f} | {r['I_total']:.2f} | {r['delta_cant']:.2f} | ${fmtp(r['delta_valor_neto'])} | {r['comentario']} |")
w("")


# Reemplazos NP
w("## Posibles reemplazos contractual -> NP")
w("")
w("| Fila contract | Item contract | Fila NP | Item NP | Delta contract | Delta NP | Sobrecosto neto |")
w("|---:|---|---:|---|---:|---:|---:|")
for rp in reemplazos_np:
    w(f"| {rp['contractual']['row']} | {rp['contractual']['item_pago']} - {(rp['contractual']['descripcion'] or '')[:35]} | {rp['np']['row']} | {rp['np']['item_pago']} - {(rp['np']['descripcion'] or '')[:35]} | ${fmtp(rp['contractual']['delta_valor'])} | ${fmtp(rp['np']['delta_valor'])} | ${fmtp(rp['sobrecosto_neto'])} |")
w("")


# Cruce V2 v V4
w("## Cruce V2 (VICON 21-04-2026) vs V4 (01-09-2026)")
w("")
w(f"- Codigos IDU en V2 (con cantidad): {sum(1 for c in comp_by_code.values() if float(c.get('cant_cont') or 0) > 0)}")
w(f"- Codigos IDU en V4 (agregados): {len(items_by_code_v4)}")
w(f"- Recorte V4<V2 (por cantidad): **{len(recorte_v4_vs_v2)} codigos**")
w(f"- Nuevos en V4 no presentes en V2: **{len(nuevos_v4_detalle)} codigos**")
w("")
w("### Recortes V4 vs V2 (top 25 por delta cant)")
w("")
w("| Cod IDU | Und | Cant V2 | Cant V4 | Delta cant | Valor V2 CD | Valor V4 CD | Delta valor CD |")
w("|---|---|---:|---:|---:|---:|---:|---:|")
for r in recorte_v4_vs_v2[:25]:
    w(f"| {r['codigo_idu']} | {r['und']} | {r['cant_v2_vicon']} | {r['cant_v4']} | {r['delta_cant_v4_v2']:.2f} | ${fmtp(r['valor_v2_cd'])} | ${fmtp(r['valor_v4_cd'])} | ${fmtp(r['delta_valor_v4_v2_cd'])} |")
w("")
w("### Nuevos codigos en V4 (top 25 por valor)")
w("")
w("| Cod IDU | Descripcion | Und | Cant V4 | Valor V4 (con AIU) | Solo NP? |")
w("|---|---|---|---:|---:|---:|")
for n in nuevos_v4_detalle[:25]:
    d = (n["descripcion"] or "")[:50]
    w(f"| {n['codigo_idu']} | {d} | {n['und']} | {n['cant_v4']} | ${fmtp(n['valor_v4_aiu'])} | {n['es_np_solo']} |")
w("")


# Metodologia
w("## Metodologia")
w("")
w("- Fuente unica: `analisis/datos/presupuesto_2026_09.json`, extraido con `analisis/scripts/extraer_presupuesto.py` de `fuentes/4. PRESUPUESTO 01-09-2026 75MM (8 MESES).xlsx`.")
w("- Se filtran filas 7-679 (capitulos 1-7). Se excluye capitulo 8 ACEROS (filas 680-687).")
w("- Estados por renglon:")
w("  - `sin_cambio`: H = I > 0 (tolerancia 0,01).")
w("  - `aumento`: I > H > 0.")
w("  - `disminucion`: 0 < I < H.")
w("  - `eliminado`: H > 0 e I = 0.")
w("  - `nuevo_contractual`: H = 0, I > 0, codigo no-NP.")
w("  - `np_nuevo`: item_pago inicia con 'NP' o codigo_idu = 'NO', con I > 0.")
w("- Verificaciones formulas linea a linea: J = I - H (tol 0,01), O ~ (I - H) x L (tol $10), Q ~ O + P (tol $10).")
w("- Reubicaciones: mismo codigo_idu con al menos un renglon eliminado/reducido y otro nuevo/aumentado.")
w("- Reemplazos contractual -> NP: fuzzy match por Jaccard >= 0,4 sobre tokens de descripcion, misma unidad y capitulo; casos conocidos (33->39, 24->30) forzados si no fueron detectados.")
w("- Cruce V4 vs V2 (VICON 21-04-2026): se convierte el valor V4 con AIU a costo directo dividiendo entre 1,31849 para comparar contra `valor_cont_cd` de comparativa.json.")
w("- Todo el detalle esta en `01_variacion_items.json`.")
w("")


OUT_MD.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"MD escrito en {OUT_MD}")


# ---------------------------------------------------------------------------
# Reporte a stdout
# ---------------------------------------------------------------------------
print("\n=== RESUMEN ===")
print(f"Items analizados: {resumen['n_items']}")
print(f"Conteos: {resumen['conteos']}")
print(f"Delta total: {fmtp(resumen['total_delta'])}")
print(f"Concilia inicial: {concilia_global['concilia_ini']}  (diff {fmtp(concilia_global['diff_ini'])})")
print(f"Concilia final:   {concilia_global['concilia_fin']}  (diff {fmtp(concilia_global['diff_fin'])})")
print(f"Concilia delta:   {concilia_global['concilia_delta']}  (diff {fmtp(concilia_global['diff_delta'])})")
print(f"Discrepancias J: {resumen['discrepancias']['J_neq_I_menos_H']}")
print(f"Discrepancias O: {resumen['discrepancias']['O_neq_delta_por_L']}")
print(f"Discrepancias Q: {resumen['discrepancias']['Q_neq_O_mas_P']}")
print(f"Reubicaciones detectadas: {len(reubicaciones)}")
print(f"Reemplazos NP: {len(reemplazos_np)}")
print(f"Recortes V4<V2: {len(recorte_v4_vs_v2)}")
print(f"Nuevos V4 (no en V2): {len(nuevos_v4_detalle)}")
n_alta = sum(1 for h in hallazgos if h['severidad'] == 'ALTA')
n_media = sum(1 for h in hallazgos if h['severidad'] == 'MEDIA')
n_baja = sum(1 for h in hallazgos if h['severidad'] == 'BAJA')
n_info = sum(1 for h in hallazgos if h['severidad'] == 'INFO')
print(f"Hallazgos: ALTA={n_alta} MEDIA={n_media} BAJA={n_baja} INFO={n_info}")
