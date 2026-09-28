"""
Corrección documentada del análisis 06 (versiones, componentes y plazo).

El análisis 06 fue producido sin script (JSON y MD escritos por el agente) y sus
referencias de fila a la hoja principal quedaron desplazadas +4 (y +5 en la
hoja "PRESUPUESTO 63 mm"). Además, el hallazgo H06-01 afirmaba que el bloque
de aceros está "cargado dentro de obras"; la fórmula M688 = SUM(M8:M679)
demuestra que el bloque (filas 680-687) está FUERA del rango de suma, así que
no hay doble conteo en el libro. Este script corrige las referencias en el JSON
y en el MD, reescribe H06-01 con el hecho verificado y deja el cambio anotado
(meta_correcciones). El registro de auditoría lo referencia como B-07 y B-08.

Filas reales verificadas con openpyxl (27/28-09-2026), hoja PRESUPUESTO TODOS LOS CIV 84 NP:
  675-676 cap. 7 DESVÍOS · 680-687 bloque ACEROS · 688 VALOR TOTAL OBRA + AIU (M688 = SUM(M8:M679))
  689 AIU 0,31849 · 690 O690 literal · 692-701 componentes · 703 total · 705 valor actual · 707 diferencia
  729-738 detalle SST/diálogo/PMT 8 meses (736 = AIU 20,006%)
Hoja PRESUPUESTO 63 mm: 652 total obras · 656-665 componentes · 667 total · 669 actual · 671 diferencia · 693-702 detalle 3 meses

Uso: python analisis/scripts/corregir_06.py   (luego consolidar.py, generar_excel.py y verificacion.py)
Idempotente: si ya se aplicó (meta_correcciones presente) no vuelve a tocar los archivos.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "analisis" / "hallazgos" / "06_versiones_plazo.json"
SRC_MD = ROOT / "analisis" / "hallazgos" / "06_versiones_plazo.md"

MAPA_PRINCIPAL = {  # fila citada -> fila real (hoja principal, desplazamiento +4)
    679: 675, 680: 676,
    685: 681, 686: 682, 687: 683, 688: 684, 689: 685, 690: 686, 691: 687,
    692: 688, 696: 692, 697: 693, 698: 694, 699: 695, 700: 696, 701: 697, 702: 698,
    703: 699, 704: 700, 705: 701, 707: 703, 740: 736, 741: 737,
}
MAPA_63MM = {657: 652, 661: 656, 662: 657, 663: 658}
RANGOS = [  # reemplazos literales de rangos (antes del regex de filas sueltas)
    ("filas 685-690", "filas 680-687"), ("685-690", "680-687"),
    ("filas 733-742", "filas 729-738"), ("733-742", "729-738"),
    ("filas 696-705", "filas 692-701"),
    ("filas 692-707 (columnas M y N)", "filas 688-707 (columnas M y N)"),
    ("hoja PRESUPUESTO 63 mm filas 657-672", "hoja PRESUPUESTO 63 mm filas 652-671"),
    ("filas 685-707 (componentes)", "filas 680-707 (bloque ACEROS, totales y componentes)"),
    ("filas 649-672 (V3), 698-707 (detalle SST 3 meses)", "filas 650-671 (V3), 693-702 (detalle SST 3 meses)"),
]

EXPLICACION_ACERO = (
    "El bloque ACEROS (filas 680-687, subtotal 3.052.987.517 con AIU 31,849%) lista acero de refuerzo, acero liso y dovelas repartidos por CIV, con cantidades actualizadas "
    "(247.985 -> 211.290,08 kg refuerzo pavimentos; 43.297 -> 52.320,56 kg refuerzo espacio público; 52.558 -> 81.288,82 kg acero liso 1 1/4; 0 -> 19.704,6 kg dovelas 1 1/2; 473 -> 0 kg malla). "
    "Está FUERA del rango de suma de obras: M688 = SUM(M8:M679) y CB688 = SUM(CB7:CB679)/2, de modo que el libro NO lo suma en los 58.196.933.800. "
    "El acero se paga por la bolsa fija F 'Costos de actividades acero' (fila 697) de 2.977.517.840, que no cambia desde V0. "
    "La diferencia de 75.469.677 (+2,5%) entre el bloque y la bolsa debe aclararse: si el bloque es la memoria de la bolsa, la bolsa quedaría corta; si es alcance adicional, requeriría adición."
)
RIESGO_ACERO = (
    "Con las fórmulas actuales no hay doble conteo en el libro. El riesgo aparecería solo si en el otrosí o en las actas de obra se pagara el bloque por ítems y además la bolsa F. "
    "La interventoría debe dejar por escrito cuál de los dos rige y que el otro no se factura."
)
H0601 = {
    "severidad": "MEDIA",
    "titulo": "Bloque de aceros (3.053M) fuera del total de obras vs bolsa fija F (2.978M): aclarar cuál rige",
    "descripcion": (
        "El bloque ACEROS (filas 680-687) suma 3.052.987.517 con AIU y reparte acero de refuerzo, acero liso y dovelas por CIV con cantidades actualizadas. "
        "Verificado con las fórmulas del libro: M688 = SUM(M8:M679) y CB688 = SUM(CB7:CB679)/2, por lo que el bloque NO está incluido en los 58.196.933.800 de obras; no hay doble conteo en el Excel. "
        "El acero se paga por la bolsa fija F (fila 697, 2.977.517.840), sin cambio desde V0. Diferencia bloque - bolsa: 75.469.677 (+2,5%). "
        "La memoria de la hoja Aceros muestra cantidades teóricas menores (~2.500M)."
    ),
    "recomendacion": (
        "Pedir al contratista que aclare por escrito si el bloque ACEROS es la memoria de cantidades de la bolsa F o alcance adicional; en el primer caso, justificar la diferencia de 75.469.677 y confirmar que la bolsa alcanza; "
        "en el segundo, tramitarlo como adición. Dejar en el otrosí que el acero se paga únicamente por la bolsa F (o únicamente por ítems), nunca por ambos."
    ),
    "fila": "680-687 y 697",
    "impacto_pesos": 75469677,
}
MOTIVO_ACERO = (
    "Bolsa fija contractual que incluye AIU y cambio de vigencia; unidad global del contrato. El bloque ACEROS (filas 680-687, 3.052.987.517 en V4) es un detalle por CIV que está FUERA del "
    "rango de suma de obras (M688 = SUM(M8:M679)); no se paga dos veces en el libro, pero la diferencia de 75.469.677 frente a la bolsa debe aclararse. Ver acero_diferencia."
)
NOTA_MD = """> **Corrección 2026-09-28 (registro de auditoría B-07 y B-08).** Las referencias de fila de este documento y de `06_versiones_plazo.json` estaban desplazadas +4 en la hoja principal y +5 en la hoja PRESUPUESTO 63 mm; se corrigieron a las filas reales verificadas con openpyxl (`analisis/scripts/corregir_06.py`). El hallazgo H06-01 afirmaba que el bloque ACEROS estaba "cargado dentro de obras": la fórmula `M688 = SUM(M8:M679)` demuestra que el bloque (filas 680-687) está fuera del total, así que no hay doble conteo en el libro. H06-01 pasa de ALTA a MEDIA y su impacto es la diferencia bloque − bolsa F (75.469.677). El texto original se conserva en el historial de git (commit 5cb90b9 y anteriores).

"""


def fix_text(t, hoja_63=None):
    """Remapea 'fila NNN' / 'filas NNN' y los rangos conocidos. Los rangos se protegen con
    centinelas para que el regex no vuelva a desplazar un número ya corregido."""
    if not isinstance(t, str):
        return t
    if hoja_63 is None:
        hoja_63 = "63 mm" in t or "63_mm" in t
    sent = {}
    for i, (a, b) in enumerate(RANGOS):
        if a in t:
            key = f"\x00{i}\x00"
            t = t.replace(a, key)
            sent[key] = b
    m = MAPA_63MM if hoja_63 else MAPA_PRINCIPAL

    def rep(mo):
        n = int(mo.group(2))
        return f"{mo.group(1)}{m.get(n, n)}"
    t = re.sub(r"(fila[s]?\s*)(\d{3})\b", rep, t, flags=re.I)
    for k, b in sent.items():
        t = t.replace(k, b)
    return t


def walk_fix(o):
    """Aplica fix_text a todas las cadenas de una estructura (primer paso, antes de las reescrituras explícitas)."""
    if isinstance(o, dict):
        return {k: walk_fix(v) for k, v in o.items()}
    if isinstance(o, list):
        return [walk_fix(v) for v in o]
    return fix_text(o) if isinstance(o, str) else o


def fix_fila(f):
    """Campo 'fila' suelto: '703', '679-680', '657 y 692'... remapea cada número."""
    if isinstance(f, int):
        return MAPA_PRINCIPAL.get(f, f)
    if not isinstance(f, str):
        return f
    return re.sub(r"\d{3}", lambda mo: str(MAPA_PRINCIPAL.get(int(mo.group(0)), int(mo.group(0)))), f)


def fix_json():
    j = json.load(open(SRC, encoding="utf-8"))
    if j.get("meta_correcciones"):
        print("06 JSON ya corregido; sin cambios")
        return
    j = walk_fix(j)  # 1) todas las cadenas: 'fila NNN' y rangos conocidos
    for c in j.get("componentes_sin_cambio", []):
        c["fila"] = fix_fila(c.get("fila"))
        if c.get("componente", "").startswith("Actividades acero"):
            c["motivo"] = MOTIVO_ACERO
    sst = j.get("sst_detalle", {})
    if sst.get("filas") == "733-742":
        sst["filas"] = "729-738"
    ac = j.get("acero_diferencia", {})
    if ac:
        ac.pop("bloque_680_687_referencia_brief", None)
        blk = ac.pop("bloque_interno_v4_filas_685_690", None)
        if blk:
            ac["bloque_interno_v4_filas_680_687"] = {re.sub(r"fila_(\d{3})", lambda mo: f"fila_{MAPA_PRINCIPAL.get(int(mo.group(1)), int(mo.group(1)))}", k): v for k, v in blk.items()}
        ac["explicacion"] = EXPLICACION_ACERO
        ac["riesgo_doble_pago"] = RIESGO_ACERO
        ac["verificacion_formulas"] = {"M688": "=SUM(M8:M679)", "CB688": "=SUM(CB7:CB679)/2", "fila_697_bolsa_F": 2977517840, "bloque_680_687": 3052987517, "delta": 75469677}
    for h in j.get("hallazgos", []):
        h["fila"] = fix_fila(h.get("fila"))
        if h["id"] == "H06-01":
            h.update(H0601)
        if h["id"] == "H06-05":
            h["fila"] = "652 (63 mm) y 688"
    j.setdefault("meta_correcciones", []).append({
        "fecha": "2026-09-28", "script": "corregir_06.py",
        "cambios": [
            "Referencias de fila desplazadas +4 (hoja principal) y +5 (PRESUPUESTO 63 mm) corregidas a las filas reales del libro",
            "H06-01 reescrito: el bloque ACEROS está fuera del rango de suma de obras (M688 = SUM(M8:M679)); severidad ALTA -> MEDIA; impacto = diferencia bloque vs bolsa (75.469.677)",
        ],
        "registro_auditoria": ["B-07", "B-08"],
    })
    json.dump(j, open(SRC, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("06 JSON corregido:", SRC)


def fix_md():
    t = SRC_MD.read_text(encoding="utf-8")
    if "Corrección 2026-09-28" in t:
        print("06 MD ya corregido; sin cambios")
        return
    out = []
    in_acero_table = False
    for line in t.split("\n"):
        line = fix_text(line)
        # tabla del bloque de aceros (primera columna = fila)
        if line.startswith("| Fila | Item |"):
            in_acero_table = True
        elif in_acero_table and line.startswith("| ") and re.match(r"\| (\d{3}) \|", line):
            n = int(re.match(r"\| (\d{3}) \|", line).group(1))
            line = line.replace(f"| {n} |", f"| {MAPA_PRINCIPAL.get(n, n)} |", 1)
        elif in_acero_table and not line.startswith("|"):
            in_acero_table = False
        # textos de H06-01
        if line.startswith("| H06-01 |"):
            line = "| H06-01 | MEDIA | Bloque ACEROS (fuera del total de obras) vs bolsa fija F: aclarar cuál rige y justificar 75.469.677 | $75,5M |"
        if "Coexiste con items reales de acero" in line:
            line = line.replace("Coexiste con items reales de acero en filas 680-687.", "El bloque ACEROS (filas 680-687) está fuera del total de obras (M688 = SUM(M8:M679)).")
        if line.startswith("1. **Items reales dentro de obras**"):
            line = "1. **Bloque ACEROS fuera del total de obras** (filas 680-687, con AIU 31,849%): detalle por CIV con las cantidades actualizadas y los VU vigentes al 01-09-2026. La fórmula `M688 = SUM(M8:M679)` no lo incluye, así que no está dentro de los 58.196.933.800."
        if line.startswith("### Riesgo de doble pago (hallazgo H06-01)"):
            line = "### Bloque vs bolsa: qué rige (hallazgo H06-01, corregido)"
        if line.startswith("Si ambos importes se pagan (bloque interno dentro de obras"):
            line = ("Con las fórmulas actuales del libro no hay doble conteo: el bloque no está sumado en obras y la bolsa F es la única partida de acero dentro de los 75.426.575.199. "
                    "El riesgo aparecería únicamente si el otrosí o las actas pagaran el acero por ítems y además la bolsa. La interventoría debe pedir por escrito cuál de las dos representaciones rige, "
                    "justificar la diferencia de 75.469.677 y dejar constancia de que la otra no se factura.")
        if line.startswith("2. **Acero (H06-01)**"):
            line = "2. **Acero (H06-01)**: pedir por escrito al contratista si el bloque ACEROS es la memoria de la bolsa F o alcance adicional; dejar en el otrosí que el acero se paga por una sola vía."
        out.append(line)
    t2 = "\n".join(out)
    # nota al inicio (después del título y la línea de contrato)
    t2 = t2.replace("\n---\n", "\n" + NOTA_MD + "---\n", 1)
    SRC_MD.write_text(t2, encoding="utf-8")
    print("06 MD corregido:", SRC_MD)


def main():
    fix_json()
    fix_md()


if __name__ == "__main__":
    main()
