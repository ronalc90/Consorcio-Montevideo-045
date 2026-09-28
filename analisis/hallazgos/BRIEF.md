# Brief — Análisis Presupuesto 01-09-2026 (75MM · 8 meses)

## Contexto
- Contrato IDU 1752 de 2021 · Grupo 2 · zonas industriales Montevideo y Puente Aranda.
- Contratista: Consorcio VICON 024 · Interventoría: Consorcio Montevideo 045.
- El contratista presentó un presupuesto nuevo el 01-09-2026 (archivo `fuentes/4. PRESUPUESTO 01-09-2026 75MM (8 MESES).xlsx`) pidiendo adición de $16.000.000.000 y 8 meses de plazo. Total pasa de $59.426.575.199 (V0 contrato firmado) a **$75.426.575.199** (V4).

## Datos ya extraídos
- `analisis/datos/presupuesto_2026_09.json` — hoja principal ítem × CIV, 27 CIVs, 649 renglones, obras con AIU = 58.196.933.800 (verificado).
- `analisis/datos/hojas/*.csv` — todas las 18 hojas del Excel (visibles y ocultas). Columna 0 = A. Fila n del CSV = fila n de Excel.

Hojas ocultas útiles: `MEMORIA CANTIDADES`, `FASE 1 (2)`, `PRESUPUESTO CONTRACTUAL MAYO 25`, `CONSOLIDADO CTO 1752 AJUSTADO`, `VISOR 07-05-25`, `NPs Objetados`, `EJECUTIVO`, `Hoja1`, `PRESUPUESTO 63 mm`, `Aceros`, `CALCULO DE ANDENES`, `CALCULO ESTRUCTURA`, `MEMORIA ETB`, `MOBILIARIOS`.

## Estructura del Excel principal `PRESUPUESTO TODOS LOS CIV 84 NP`
- Columnas: B código IDU · C ítem de pago · F descripción · G unidad · **H cantidad contractual (inicial)** · **I cantidad actualizada (final)** · J = I − H · K VU costo directo · L VU CD+AIU (AIU 31,849%) · M valor final con AIU · N valor inicial con AIU · O balance mayores/menores · P incorporación NP · Q adición.
- Fila 3 = IDs de CIV. Subgrupo 2 (7 CIVs) en columnas S..AF en pares cantidad/valor. Subgrupo 5 (20 CIVs) en AJ..BW. Total general en CA/CB. Chequeo en CC.
- Filas: 7-679 ítems (capítulos 1-7). 680-687 bloque ACEROS (**no** suma en obras). 688 total obras+AIU = 58.196.933.800. 692-701 componentes no-obra. 703 total 75.426.575.199. 729-738 detalle SST 8 meses (AIU 20,006%).

## Versiones a comparar
| Ver | Total | Fuente |
|---|---|---|
| V0 Contrato firmado | 59.426.575.199 (obras+AIU 44.303.294.799) | `comparativa.json → globales.contrato_original_firma`; col N |
| V1 IDU oficial 25-02-2026 | 61.411.887.929 | `comparativa.json → globales.iniciales`, `civs_idu`, ítems `cant_idu`/`valor_idu_cd` |
| V2 VICON 21-04-2026 (Alt 1) | 77.944.220.992 | `comparativa.json → globales.actualizadas_alt1`, `civs_cont`, `civ_items_cont`, ítems `cant_cont`/`valor_cont_cd` |
| V3 intermedia "63MM" | ~63.749M | hoja oculta `PRESUPUESTO 63 mm` |
| **V4 nueva 01-09-2026** | **75.426.575.199** | hoja principal |

Los ítems de `comparativa.json` están en **costo directo (sin AIU)**; V4 viene con AIU.

## Cifras ya verificadas (punto de partida — profundizar)
### Obras con AIU
44.303.294.799 → 58.196.933.800 (+13.893.639.001) = −257.285.548 balance mayores/menores + 14.150.924.549 NPs.

### Componentes no-obra
| Concepto | V0 | V4 | Δ |
|---|---|---|---|
| PMA-SST | 2.943.115.324 | 4.110.277.014 | +1.167.161.690 |
| Diálogo ciudadano | 1.874.965.632 | 2.430.023.370 | +555.057.738 |
| PMT | 1.623.435.591 | 2.007.577.162 | +384.141.571 |
| Fondo compensaciones | 0 | 0 | 0 |
| Ajustes cambio vigencia | 4.555.525.079 | 4.555.525.079 | 0 |
| Actividades acero | 2.977.517.840 | 2.977.517.840 | 0 |
| Ensayos laboratorio | 299.267.609 | 299.267.609 | 0 |
| SDA | 31.328.679 | 31.328.679 | 0 |
| Fase obras iniciales | 758.734.334 | 758.734.334 | 0 |
| Bioseguridad | 59.390.312 | 59.390.312 | 0 |

### Variación por renglón (V4 hoja principal)
| Estado | Renglones | Δ valor |
|---|---|---|
| Eliminado | 118 | −19.443.722.236 |
| Contractual con cantidad inicial 0 que ahora tiene cantidad | 93 | +15.200.542.240 |
| NP nuevo (81 códigos únicos) | 105 | +14.150.924.549 |
| Aumentó | 27 | +8.809.106.675 |
| Disminuyó | 39 | −4.823.212.227 |
| Sin cambio | 25 | 0 |

### Δ por capítulo
- Redes hidrosanitarias +6.777.852.537
- Pavimentos +3.556.107.781
- Preliminares +2.787.734.305
- Redes secas +1.613.831.550
- Espacio público −515.309.947
- Desvíos −326.577.225
- Señalización 0

### Costo por CIV (obras con AIU)
Promedio $1.113.048/m² · mediana $1.019.119/m² sobre 52.286 m² (áreas de V1).

Outliers:
- 16000024 KR 65A: $2.454.941/m², $5.899M, +$1.661M vs V2.
- 16000010 CL18B: $2.317.646/m², 58% en NPs.
- 16000017: $2.032.570/m².
- 16000013: +$891M vs V2.

Grupos `Hoja1`: ya iniciados $19.652M, por iniciar $19.034M, no alcanza $19.511M.

## Trampas conocidas (validarlas todas)
- El CIV `500002375` (V4) = `50002375` (MEMORIA) = `16004876 (50002375)` (comparativa.json) = `16004876` (Hoja1) = KR65 CL17-CL18. Comparte segmento 91029906 con el 16000047.
- La hoja se llama "84 NP" pero hay 81 códigos NP con cantidad en 105 renglones.
- El bloque de aceros suma 3.052.987.517; el componente fijo de acero es 2.977.517.840.
- La fila 703 dice "04-05-2026" pero el archivo es del 01-09-2026.
- Diferencias de pocos pesos: .780 vs .800, .017 vs .014 y .268 vs .199.

## Patrones a validar
### Reubicaciones (misma actividad, cambia el subcapítulo)
- 6.007 en filas 490 → 531
- 5.067 en filas 295 → 399

### Posibles reemplazos de ítem contractual por NP más caro
- Fila 33 (2.002 MD12, −2.585M) → fila 39 (NP-123 MD19, +3.270M)
- Fila 24 (1.012 BG_A, −1.811M) → fila 30 (NP-124 BG_A reciclado, +2.519M)

### Saltos extremos de cantidad
- Fila 20 (1.008 rajón, 965 → 14.163 m³)
- Fila 85 (3.039 andén, 114 → 15.469 m²)

### Descripción rara
- Fila 317 (5.037 "estudios y diseños de aceras" en M2 dentro de redes)

## Reglas para TODOS los agentes
1. **Todo número sale de código**; nada estimado ni redondeado a mano. Usar `analisis/datos/*.csv` y `analisis/datos/presupuesto_2026_09.json` como insumo canónico. Cuando haga falta releer del Excel usar `openpyxl` con `data_only=True`.
2. **Citar hoja y fila** de Excel de cada hallazgo. Ej: `PRESUPUESTO TODOS LOS CIV 84 NP fila 33`.
3. **Severidad**: ALTA (bloqueante o >$500M), MEDIA (>$50M o riesgo técnico), BAJA (<$50M), INFO (nota o discrepancia menor).
4. **Recomendación** concreta de la interventoría en cada hallazgo (qué pedir al contratista).
5. **Formato de pesos**: punto de miles (`1.234.567.890`).
6. **NO modificar los archivos fuente**. Escribir sólo en `analisis/hallazgos/NN_tema.{md,json}`.
7. Los JSON de salida deben tener estructura pensada para consumo en la app (tablas y arrays).

## Notas de la app
- `index.html` usa Chart.js 4.4.7, xlsx-js-style 1.2.0, todo cliente. Login sólo cliente. Repo público.
- Helpers globales: `fmt(n)`, `fmtD(n,d)`, `fmtB(n)`. AIU visor = 34,01% pero **AIU contractual = 31,849%** (el que rige V0-V4).
- Bug conocido a corregir en la integración: en `renderCompbaAlcance` (línea 1471) la lookup falla para `16004876` cuando el id de `civs_cont` es `16004876 (50002375)`. La búsqueda funciona en `renderCompbaCIV` línea 1430 gracias a `cont.id.split(' ')[0]`. Hay que replicar la normalización en `renderCompbaAlcance` para que el CIV aparezca en "No alcanza".
