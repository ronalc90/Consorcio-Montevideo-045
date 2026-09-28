# INFORME DE INTERVENTORÍA — Presupuesto 01-09-2026
## Contrato IDU 1752 de 2021 · Grupo 2 · Consorcio Montevideo 045

**Objeto del contrato**: Construcción de vías y espacio público en las zonas industriales de Montevideo y Puente Aranda, Bogotá D.C.
**Contratista**: Consorcio VICON 024
**Fuente única del análisis**: `fuentes/4. PRESUPUESTO 01-09-2026 75MM (8 MESES).xlsx`
**Fecha del informe**: 27 de septiembre de 2026

---

## 1. Resumen ejecutivo

El contratista radicó un presupuesto con adición neta de **$16.000.000.000** y un plazo adicional de **8 meses**. El total del contrato pasa de $59.426.575.199 (V0 contrato firmado) a **$75.426.575.199** (V4). El componente de obras con AIU (fila 688) crece de $44.303.294.799 a **$58.196.933.800** (+$13.893.639.001), y los componentes de gestión suben en +$2.106M.

| Componente | V0 firma | V4 01-09-2026 | Δ |
|---|---:|---:|---:|
| Obras + AIU 31,849% | 44.303.294.799 | 58.196.933.800 | **+13.893.639.001** |
| PMA-SST (AIU 20,006%) | 2.943.115.324 | 4.110.277.014 | +1.167.161.690 |
| Diálogo ciudadano (AIU 19,566%) | 1.874.965.632 | 2.430.023.370 | +555.057.738 |
| PMT (AIU 19,566%) | 1.623.435.591 | 2.007.577.162 | +384.141.571 |
| Ajustes cambio vigencia | 4.555.525.079 | 4.555.525.079 | 0 |
| Actividades acero (bolsa F) | 2.977.517.840 | 2.977.517.840 | 0 |
| Ensayos laboratorio | 299.267.609 | 299.267.609 | 0 |
| Evaluaciones SDA | 31.328.679 | 31.328.679 | 0 |
| Fase obras iniciales | 758.734.334 | 758.734.334 | 0 |
| Bioseguridad | 59.390.312 | 59.390.312 | 0 |
| Fondo compensaciones | 0 | 0 | 0 |
| **Total** | **59.426.575.199** | **75.426.575.199** | **+16.000.000.000** |

Cifras verificadas al peso contra la fila 703 del Excel (`PRESUPUESTO TODOS LOS CIV 84 NP`). El AIU contractual de 31,849% se mantiene para el capítulo 1-7; los componentes de gestión conservan su AIU específico (20,006% para PMA-SST; 19,566% para Diálogo y PMT).

### Los 10 hallazgos más críticos

| # | ID | Severidad | Impacto $ | Título |
|---|---|---|---:|---|
| 1 | H06-02 | ALTA | 19.347.297.314 | El capítulo 7 DESVÍOS de V2 era un contenedor mal clasificado; en V4 quedó en $0 |
| 2 | H06-03 | ALTA | 16.000.000.000 | Ritmo mensual propuesto (~$2.000M/mes) es 3× el ritmo histórico del contrato |
| 3 | H04 (análisis 04) | ALTA | 15.086.222.761 | Los VU vigentes están +49,0% (mediana) sobre los pactados en la propuesta 2021; la actualización ya está en el "valor actual" y hay que ver con qué acto se formalizó (registro de auditoría A-24) |
| 4 | H01-013 | ALTA | 6.777.852.537 | Redes hidrosanitarias absorben el 49% del crecimiento de obras (cap. 5) |
| 5 | H03-OUT · 16000024 | ALTA | 5.899.197.969 | CIV 16000024 KR 65A es outlier: $2.454.941/m² obras (2,4× mediana) |
| 6 | H03-OUT · 16000010 | ALTA | 3.950.103.092 | CIV 16000010 CL18B es outlier: $2.317.646/m² obras (2,3× mediana) |
| 7 | H02-101 | ALTA | 3.672.527.262 | CIV 16000024 KR 65A concentra el Δ obras más grande de los 27 CIVs (+165%) |
| 8 | H01-014 | ALTA | 3.556.107.781 | Pavimentos (cap. 2) sube por reemplazo MD12 → NP-123 MD19 |
| 9 | H01-035 | ALTA | 3.269.600.612 | NP-123 MEZCLA ASFÁLTICA MD19 · $3.269M (reemplaza al contractual 2.002 MD12) |
| 10 | H01-015 | ALTA | 2.787.734.305 | Preliminares (cap. 1) sube por rajón (fila 20: 965 → 14.163 m³) |

> **Corrección 2026-09-28.** La versión anterior de esta tabla incluía H06-01 como "riesgo de doble pago en acero por $2.977M". Las fórmulas del libro (`M688 = SUM(M8:M679)`) demuestran que el bloque ACEROS (filas 680-687) está fuera del total de obras: no hay doble conteo. H06-01 pasa a MEDIA con impacto $75.469.677 (diferencia bloque − bolsa F). Detalle en el registro de auditoría, asiento B-08.

---

## 2. Variación de cantidades (col H → col I)

### 2.1 Conciliación al peso

Suma de renglones (excluyendo el bloque ACEROS 680-687):

- Total valor inicial (col N): **$44.303.294.799** — cuadra con V0 obras+AIU del contrato firmado.
- Total valor final (col M): **$58.196.933.800** — cuadra con la fila 688 col M.
- Delta obras: **+$13.893.639.001** = −$257.285.548 balance mayores/menores (col O agregada) + $14.150.924.549 incorporación NP (col P agregada).

Verificaciones aritméticas ejecutadas por renglón (fila 7 a 679):
- 0 renglones con `J ≠ I − H` — perfecto.
- 0 renglones con `L ≠ redondeo(K × 1,31849)` — precio unitario con AIU cuadra.
- 1 renglón con `O ≠ (I−H) × L` (diferencia menor de peso).
- 0 renglones con `Q ≠ O + P` — la columna de adición cuadra.

### 2.2 Distribución por estado del renglón

| Estado | Renglones | Δ valor |
|---|---:|---:|
| Eliminado (H>0, I=0) | 118 | **−19.443.722.236** |
| Nuevo contractual (H=0, I>0) | 93 | +15.200.542.240 |
| NP nuevo (código NP) | 105 | +14.150.924.549 |
| Aumentó | 27 | +8.809.106.675 |
| Disminuyó | 39 | −4.823.212.227 |
| Sin cambio | 25 | 0 |
| Total | **407 activos** | **+13.893.639.001** |

La incorporación bruta (NP + nuevo contractual + aumentos = $38.160.573.464) financia una eliminación bruta (eliminados + disminuciones = $24.266.934.463). El balance NETO es +$13.893.639.001.

### 2.3 Variación por capítulo (conciliada al peso)

| Capítulo | Valor inicial | Valor final | Δ |
|---|---:|---:|---:|
| 1. Preliminares | 6.508.713.086 | 9.296.447.391 | **+2.787.734.305** |
| 2. Pavimentos | 15.328.367.366 | 18.884.475.147 | **+3.556.107.781** |
| 3. Espacio público | 7.252.761.854 | 6.737.451.907 | −515.309.947 |
| 4. Señalización | 1.198.662.405 | 1.198.662.405 | 0 |
| 5. Redes hidrosanitarias | 9.324.763.052 | 16.102.615.589 | **+6.777.852.537** |
| 6. Redes secas | 4.363.449.811 | 5.977.281.361 | **+1.613.831.550** |
| 7. Desvíos | 326.577.225 | 0 | −326.577.225 |
| **Total capítulos 1-7** | **44.303.294.799** | **58.196.933.800** | **+13.893.639.001** |

**Nota importante — desvíos**: en V2 (VICON 21-04-2026) el capítulo 7 llegó a $19.347M en costo directo, pero era un contenedor mal clasificado donde el contratista había metido componentes no-obra. En V4 el capítulo queda en $0. No es un ahorro real, es reordenamiento contable.

### 2.4 Movimientos más grandes

**Top 5 aumentos** (por Δ valor absoluto):

| Fila | Código | Descripción | Δ Valor |
|---:|---|---|---:|
| 39 | NP-123 | MEZCLA ASFÁLTICA MD19 (reemplaza MD12) | +$3.269.600.612 |
| 34 | 2.003 | Losa MR-45 (concreto rígido) | +$2.351M |
| 20 | 1.008 | Rajón (965 → 14.163 m³) | +$2.100M+ |
| 30 | NP-124 | BG_A reciclado (reemplaza 1.012 BG_A) | +$2.518.521.916 |
| 85 | 3.039 | Andén concreto (114 → 15.469 m²) | +$1.500M+ |

**Reemplazos contractual → NP detectados** (12 pares):

| Contractual | Δ contractual | NP | Δ NP | Sobrecosto |
|---|---:|---|---:|---:|
| fila 33 · 2.002 MD12 | −$2.585M | fila 39 · NP-123 MD19 | +$3.270M | **+$684M** |
| fila 24 · 1.012 BG_A | −$1.811M | fila 30 · NP-124 BG_A reciclado | +$2.519M | **+$707M** |
| ... (10 más en el JSON) | | | | |

**Recomendación**: solicitar la justificación técnica y estudio comparativo de precios para cada reemplazo; los NPs deben tener APU justificado y precios de mercado.

---

## 3. Costo por CIV (27 CIVs)

### 3.1 Verificaciones

- Suma de los 27 CIVs (obras con AIU) = **$58.196.933.869** (esperado 58.196.933.800; Δ +$69 porque cada celda por CIV es ROUND(cantidad × L) y el total del renglón es ROUND(L × I); documentado en el registro de auditoría A-12).
- Suma total con componentes = **$75.426.575.268** (esperado 75.426.575.199; Δ +$69 por el mismo redondeo).

### 3.2 Criterio de reparto de componentes no-obra

Los $17.229.641.399 de componentes (PMA-SST, Diálogo, PMT, ajustes, acero, laboratorio, SDA, fase inicial, bioseguridad) se reparten **proporcional al costo directo de obras por CIV**. Es el criterio más neutro porque el AIU es proporcional y el área lineal no captura la intensidad real de redes/señalización/NPs.

### 3.3 Distribución por subgrupo

| Subgrupo | # CIVs | Obras+AIU | Total con componentes | $/m² total |
|---|---:|---:|---:|---:|
| SG2 Montevideo | 7 | 14.938.689.502 | 19.361.401.249 | ~1.032.000 |
| SG5 Puente Aranda | 20 | 43.258.244.367 | 56.065.174.019 | ~1.552.000 |
| **Total** | **27** | **58.196.933.869** | **75.426.575.268** | **1.442.601** |

### 3.4 Top / bottom de costo por CIV

**Top 5 más caros (total con AIU + componentes)**:

| CIV | Nomenclatura | SG | Área m² | Total con AIU | $/m² total |
|---|---|---|---:|---:|---:|
| 16000024 | KR 65A | 5 | 2.402,99 | **$7.645.700.040** | $3.181.744 |
| 16000010 | CL18B | 5 | 1.704,36 | **$5.119.560.918** | $3.003.803 |
| 16000017 | KR 65A | 5 | 1.361,36 | $3.586.267.660 | $2.634.327 |
| 9003990 | CL20 | 2 | 2.980,72 | $3.514.011.416 | $1.179.266 |
| 9003980 | CL20 | 2 | 2.373,20 | $3.336.609.882 | $1.405.711 |

**Bottom 5 más económicos**:

| CIV | Nomenclatura | SG | Área m² | Total con AIU | $/m² total |
|---|---|---|---:|---:|---:|
| 16000007 | KR66 | 5 | 1.045,72 | $935.401.136 | $894.325 |
| 16000029 | CL18 | 5 | 939,74 | $1.052.979.891 | $1.120.477 |
| 16000077 | CL14 | 5 | 1.236,89 | $1.423.483.419 | $1.150.745 |
| 500002375 | KR65 | 5 | 1.159,92 | $1.926.977.139 | $1.661.302 |
| 16000060 | KR63 | 5 | 1.593,55 | $2.105.149.024 | $1.320.836 |

### 3.5 Estadística $/m² obras con AIU

- Media: $1.132.564/m² · Mediana: $1.019.119/m² · IQR: [$898.938 · $1.170.422].
- SG2 Montevideo: media $992.651 (bandas estrechas, σ $128.303).
- SG5 Puente Aranda: media $1.181.533 (bandas anchas, σ $505.062 — hay outliers).
- **Outliers (> mediana + 1,5·IQR = $1.426.345/m² obras)**:
  - 16000024 KR 65A: $2.454.941/m² (2,4× mediana) — 58% del CIV son NPs.
  - 16000010 CL18B: $2.317.646/m² (2,3× mediana) — 58% del CIV son NPs.
  - 16000017 KR 65A: $2.032.570/m² (2,0× mediana).
  - 500002375 KR65: $1.661.302/m² — impacto de reubicación de segmento con 16000047.

### 3.6 Grupos alcance (Hoja1)

| Grupo | # CIVs | Obras+AIU | Total con componentes |
|---|---:|---:|---:|
| Ya iniciados | 8 | ~$15.100M | ~$19.652M |
| Por iniciar | 10 | ~$14.700M | ~$19.034M |
| No alcanza (excluidos Alt 2) | 9 | ~$15.000M | ~$19.511M |

**Recomendación**: pedir al contratista un cronograma con el ritmo mensual real de las 8 CIVs iniciadas, para contrastar con el ritmo propuesto de $2.000M/mes en la adición.

---

## 4. Variación por CIV — descomposición del Δ

La línea base inicial por CIV se reconstruye así: **cantidad contractual de cada fila V4 (col H) × proporción del CIV** para ese código IDU según el reparto del contrato (`data.json → items[*].cantidades`). Con esto la suma por CIV de cada fila cuadra con la col H y el Δ por CIV se valora al mismo precio (VU V4) en inicial y final, aislando el efecto cantidad. El Δ de cada CIV se descompone en 5 fuentes:

- **Δ Aumentos**: renglones donde la cantidad final V4 supera la inicial.
- **Δ Disminuciones**: renglones donde la cantidad final V4 es menor a la inicial.
- **Δ NP**: renglones no previstos (105 en total, $14.150.924.549).
- **Δ Contractual nuevo**: renglones contractuales sin cantidad inicial en ese CIV que ahora tienen cantidad.
- **Δ Eliminado**: renglones con cantidad inicial en ese CIV que quedan en 0.

CIVs con mayor Δ de obras con AIU (inicial → final):

| CIV | Tramo | Inicial | Final V4 | Δ | Δ % | NPs agregados | Eliminado |
|---|---|---:|---:|---:|---:|---:|---:|
| 16000024 | KR 65A CL18 - CL18A | $2.226.670.707 | $5.899.197.969 | **+$3.672.527.262** | +165% | $1.016.703.547 | −$1.071.759.634 |
| 16000010 | CL18B KR65B - KR66 | $2.291.612.786 | $3.950.103.092 | **+$1.658.490.306** | +72% | $2.308.849.811 | −$1.428.432.706 |
| 16000017 | KR 65A CL18A - CL18B | $1.441.265.454 | $2.767.058.972 | **+$1.325.793.518** | +92% | $539.293.095 | −$866.960.011 |
| 16000013 | CL18B KR65A - KR65B | $828.228.169 | $2.149.935.500 | **+$1.321.707.331** | +160% | $457.445.474 | −$381.837.675 |
| 9003980 | CL20 KR68C - AK68D | $1.773.268.906 | $2.574.430.351 | **+$801.161.445** | +45% | $495.791.541 | −$781.934.933 |
| 16000052 | KR63 ACCESO VIA 17B - CL17B | $1.504.006.937 | $2.190.004.906 | **+$685.997.969** | +46% | $565.653.522 | −$741.865.242 |

Los CIVs que menos cambian o bajan: 16000060 KR63 (−$87.706.928), 16000027 KR 63 (−$15.989.547), 16000047 KR65 (+$36.137.000).

**Conciliación**: la línea base por CIV suma $41.842.985.108. La diferencia con la col N global ($44.303.294.799) son 40 filas contractuales por $2.460.223.472 cuyo código IDU no tiene reparto por CIV en el contrato (accesorios de redes, viga de cimentación, SBG_B, losa MR43, entre otras); se listan en `analisis/hallazgos/02_variacion_civ.json → conciliacion_total.detalle_sin_reparto`. El residual de $86.217 está en la fila 34 (2.003 losa MR45): su valor inicial en col N ($12.357.428.721) no es igual a H × L (8.276 × $1.493.154 = $12.357.342.504). Por eso la suma de los Δ por CIV (+$16.353.948.692) es mayor que el Δ global (+$13.893.639.001).

**Corrección 27-09-2026**: la primera versión de este informe reportaba el CIV 500002375 (KR65 CL17–CL18) con inicial $0 y Δ +$1.486.799.059, porque la línea base se buscaba con el ID 16004876 cuando en el contrato ese CIV figura como 50002375. Corregido: su Δ real es +$563.530.517 (+61%).

**Recomendación**: solicitar al contratista el reparto oficial de la cantidad inicial (col H) por CIV para poder auditar al peso la variación por frente.

---

## 5. Ítems No Previstos (NP)

- **105 renglones** con cantidad > 0 · **81 códigos NP únicos** (la hoja se llama "84 NP" pero hay 3 códigos que no aparecen en el V4 final).
- Total con AIU: **$14.150.924.549** (100% del Δ obras neto proviene de NPs).
- 0 de los 14 NPs objetados por el IDU (`comparativa.json → nps_objetados`) aparecen en V4 — se retiraron.

### Top 5 NPs por valor

| Ítem | Código | Descripción | Valor con AIU |
|---|---|---|---:|
| NP-123 | (sin código IDU) | MEZCLA ASFÁLTICA MD19 CON CEMENTO ASFÁLTICO | $3.269.600.612 |
| NP-124 | (sin código IDU) | BASE GRANULAR CLASE A (BG_A) CON RECICLADO DE CONCRETO | $2.518.521.916 |
| NP-133 | (sin código IDU) | BOX CULVERT PREFABRICADO TIPO 1 | $1.879.745.340 |
| NP-16 | (sin código IDU) | CONCRETO ESTAMPADO 3.000 PSI | +$1.107M |
| NP-107 | (sin código IDU) | (redes hidrosanitarias) | ~$1.100M |

### Cambios frente a V2 (216 NPs)

El contratista redujo de 216 NPs (V2 abril) a 81 códigos (V4 septiembre). Se retiraron los 14 objetados, algunos GLB/MES excesivos, y varios que el IDU había marcado como sobrecosto injustificado.

**Recomendación**: pedir el APU detallado de cada uno de los top 20 NPs con precios de mercado documentados, cronograma de ejecución y CIVs específicos donde se aplicará. Cruzar contra el VISOR 07-05-25 para verificar precios de referencia.

---

## 6. Componentes y plazo (8 meses)

### 6.1 Distribución del incremento

| Componente | Δ | % del total | Ritmo mensual (÷8) |
|---|---:|---:|---:|
| Obras con AIU | +13.893.639.001 | 86,8% | $1.737M/mes |
| PMA-SST | +1.167.161.690 | 7,3% | $146M/mes |
| Diálogo ciudadano | +555.057.738 | 3,5% | $69M/mes |
| PMT | +384.141.571 | 2,4% | $48M/mes |
| **Total** | **+15.999.999.999** ≈ +$16.000M | **100%** | **$2.000M/mes** |

### 6.2 Componentes que NO crecen

- **Ajustes cambio vigencia $4.555M**: bolsa fija contractual, no depende del avance.
- **Actividades acero $2.977M**: bolsa fija F contractual (fila 697). El bloque ACEROS (filas 680-687) suma $3.052.987.517 con AIU pero está **fuera** del total de obras (`M688 = SUM(M8:M679)`), así que el libro no lo cobra dos veces. Lo que debe aclararse es cuál de las dos representaciones rige para pagar y por qué el bloque supera la bolsa en $75.469.677 (+2,5%): si el bloque es la memoria de la bolsa, la bolsa queda corta; si es alcance adicional, requiere adición (H06-01, corregido; registro de auditoría A-05 y B-08).
- **Ensayos laboratorio $299M · SDA $31M · Fase inicial $758M · Bioseguridad $59M**: bolsas fijas no ajustadas.
- **Fondo compensaciones $0**: en V2 aparecía por $5.942.657.520 (10% del contrato); en V4 desaparece sin trazabilidad documental.

**Recomendación**: pedir soporte explícito de dónde quedó el Fondo de compensaciones y por qué se retiró.

### 6.3 Detalle SST 8 meses (filas 718-739)

- AIU aplicado: **20,006%** (diferente al 31,849% del resto).
- Subtotales ABCDE = $972.586.112 en costo directo.
- Con AIU: $972.586.112 × 1,20006 = $1.167.161.690 — cuadra con el Δ PMA-SST al peso.
- Total componente PMA-SST V4 = $4.110.277.014 (esperado exacto).

### 6.4 Ritmo mensual vs histórico

El ritmo propuesto de **$2.000M/mes** es aproximadamente **3× el ritmo histórico** del contrato (~$650M/mes según los datos del EJECUTIVO). La adición asume una aceleración de obra que no aparece justificada en el archivo. **Recomendación**: pedir cronograma detallado con hitos mensuales y capacidad instalada (personal, maquinaria, frentes activos simultáneos).

### 6.5 V3 → V4 ($63.749M → $75.426M en 4 meses = +$11.677M)

VU idénticos en la mayoría de renglones — no es reindexación. El crecimiento V3→V4 es puramente efecto **cantidad + NPs**:
- Obras: +$10.361M (88,7%)
- SST: +$729M
- Diálogo: +$347M
- PMT: +$240M

---

## 7. Hallazgos por severidad

**Distribución**: ALTA 44 · MEDIA 18 · BAJA 4 · INFO 8 (74 hallazgos).

**Intensidad de obra por m² (corregida el 28-09-2026, registro de auditoría B-14).** Cantidad final V4 del CIV ÷ área del CIV, frente a la mediana de los 27 frentes. Cinco atípicos (> 2× la mediana), todos MEDIA:

| Hallazgo | CIV | Indicador | Valor | Veces la mediana |
|---|---|---|---:|---:|
| H02-200 | 16000013 (CL18B KR65A-KR65B) | Andén (m² por m² de CIV) | 1,209 | 5,5× |
| H02-201 | 16000017 (KR 65A CL18A-CL18B) | Andén | 0,842 | 3,8× |
| H02-202 | 16000024 (KR 65A CL18-CL18A) | Andén | 0,732 | 3,3× |
| H02-203 | 16000017 | Rajón (m³ por m²) | 0,721 | 2,8× |
| H02-204 | 16000017 | Mezcla asfáltica MD12 + MD19 (m³ por m²) | 0,103 | 2,8× |

En 16000017 y 16000024 el rajón, la mezcla asfáltica y la base granular salen todos con el mismo múltiplo de la mediana (2,79× y 2,65×): las cantidades de pavimento se repartieron entre CIVs con una misma proporción, no con una memoria por frente. Pedir la memoria de cantidades de pavimentos y andenes por CIV.

Ver `analisis/analisis_2026_09.json → hallazgos` y las tablas de la app pestaña "Presupuesto 01-09-2026 · 75MM · 8 meses" para el listado completo con recomendación por hallazgo.

Los 10 más críticos ya están listados en el Resumen ejecutivo.

---

## 8. Preguntas para el contratista

1. **Reparto por CIV de la cantidad contractual**: entregar la col H desagregada por los 27 CIVs para poder auditar al peso el Δ cantidad por frente.
2. **Reemplazos ítem contractual → NP**: soporte técnico y económico de los 12 pares detectados (MD12→NP-123, BG_A→NP-124, y 10 más). Debe justificarse por qué el APU del NP es superior al VU del contractual reemplazado.
3. **NP-123 MD19**: por qué se cambia MD12 (contractual) por MD19 (NP) — ¿el diseño lo exigía desde el inicio? ¿Qué costo de campo lo motivó? Aportar el APU con precios de mercado y comparación con VISOR 07-05-25.
4. **Fila 20 rajón**: la cantidad pasa de 965 a 14.163 m³ (14,7× el contractual). ¿Existe estudio geotécnico que soporte esta cantidad? ¿En qué CIVs se distribuye?
5. **Fila 85 andén 3.039**: la cantidad pasa de 114 a 15.469 m². ¿Es error de digitación? ¿Se reasignó de otro código?
6. **Ritmo $2.000M/mes**: cronograma detallado con hitos mensuales, personal, maquinaria y frentes activos simultáneos.
7. **CIVs outliers 16000024 y 16000010**: por qué el $/m² es >2× la mediana. ¿Diseño con mayor complejidad de redes? Soporte de campo.
8. **Fondo de compensaciones**: en V2 estaba en $5.942M, en V4 en $0. ¿Se subrogó a otro componente? ¿Se cerró como sobrecosto no reembolsable?
9. **Acero: bloque vs bolsa F**: el bloque ACEROS (filas 680-687) suma $3.052M y está fuera del total de obras; la bolsa fija F vale $2.977M. ¿Cuál rige para pagar y por qué difieren en $75,5M? Dejar en el otrosí que el acero se paga por una sola vía.
10. **CIV 500002375**: unificar la nomenclatura (500002375 IDU actual = 16004876 en data.json = 50002375 en MEMORIA CANTIDADES = 16004876 en Hoja1). Documentar el segmento compartido con 16000047 (91029906) y cómo se factura para no duplicar.
11. **Desvíos capítulo 7**: en V2 subió a $19.347M en CD, en V4 quedó en $0. Confirmar que ningún ítem de desvíos fue reasignado a los capítulos 1-6 con cambio de código para no duplicar.
12. **NPs objetados**: los 14 NPs que el IDU rechazó no aparecen en V4 — verificar oficialmente que ninguno se reintroduzca con otro código o descripción.

---

## 8A. Marco normativo y chequeo legal de la solicitud

Fuentes consultadas el 27-09-2026 (verificar vigencia antes de citar en el informe oficial):

| Norma / concepto | Qué dice | Cómo aplica a este presupuesto |
|---|---|---|
| Ley 80 de 1993, art. 40 parágrafo | Los contratos no podrán adicionarse en más del 50% de su valor inicial, expresado en SMMLV. | **Base corregida (registro de auditoría B-11):** el valor inicial del contrato es **$50.793.789.333** (hoja PRESUPUESTO CONTRACTUAL MAYO 25, fila 279; coincide con el boletín del IDU de 2021), no los $59.426.575.199 "actuales", que ya traen $8.632.785.866 de incremento (adiciones 1-3 de la fase inicial, actualización de VU a insumos 13-09-2024 y reasignación del fondo de compensaciones). En pesos: $8.632.785.866 previos + $16.000.000.000 = $24.632.785.866 = **48,5% del valor inicial** (margen $764.108.801). En SMMLV: 55.908 SMMLV iniciales (2021, $908.526) → tope 27.954; adición 9.138 SMMLV (2026, $1.750.905) + incremento previo ≈ 6.064 SMMLV (si se cuenta a SMMLV 2025, $1.423.500) = 15.203 SMMLV = 54,4% del tope. Cabe en SMMLV pero queda al límite en pesos: el IDU debe precisar qué parte del incremento previo fue adición (cuenta) y qué parte reajuste (no cuenta). Duda C-01 del registro. |
| Colombia Compra Eficiente, concepto C-466 de 2024 | En contratos a precios unitarios las mayores cantidades de obra no son adición ni cuentan para el tope; las obras adicionales sí. | El balance de mayores/menores cantidades es −$257.285.548 (no hay mayores cantidades netas). La adición se compone de NP ($14.150.924.549) y componentes por plazo (+$2.106.360.999): es adición en sentido estricto. |
| Consejo de Estado, Sección Tercera, 10-10-2024, exp. 67.508 | Mayores cantidades se reconocen con medición y recibo; las obras adicionales exigen acuerdo escrito previo al pago. | Los 81 códigos NP (105 renglones) requieren otrosí y acta de fijación de precios antes de ejecutarse o pagarse. |
| Ley 1474 de 2011, arts. 83–84 | Deber del interventor de informar oportunamente; responsabilidad solidaria si no lo hace (par. 3); falta gravísima (par. 1). | Los 44 hallazgos ALTA y 18 MEDIA, y los asientos ABIERTOS de severidad ALTA del registro de auditoría (A-01, A-02, A-06, A-24, A-25), deben quedar informados por escrito al IDU con soporte. |
| IDU, Manual de Gestión Contractual MG-GC-06 v19, §11.1.3 y §11.2.1 | Los ítems no previstos obligan a modificación contractual y cuentan para el tope del art. 40; las mayores cantidades no son modificación, pero el interventor verifica que el balanceo no afecte la funcionalidad. | Certificar funcionalidad tras eliminar 118 renglones (incluido todo el cap. 7 desvíos) y crear 93. |
| IDU, Guía GUDP017 (presupuestos) | AIU = A + I + U; los imprevistos cubren contingencias normales; ajustes por cambio de vigencia = (valor ÷ meses) × meses en la nueva vigencia × inflación (ICCP para obra). | El componente de ajustes ($4.555.525.079) no cambia en V4 aunque los 8 meses cruzan a 2027: pedir recálculo o justificación. |
| IDU, PR-IC-01 (base de precios / VISOR) | Base actualizada al menos una vez al año; ítems fuera de la base se soportan con APU (FO-GI-19) y cotizaciones. | Los 81 NP deben venir con APU y compararse con el VISOR vigente y con el ítem contractual más cercano. |
| Actas de fijación de precios no previstos (IDU FOEO24 / CCE GCON-FM-015) | Registro por NP de descripción, unidad, cantidad, VU y APU aprobado; firmas de contratista, interventor y ordenador del gasto. | En V4 no hay actas: los 105 renglones NP quedan "en revisión". |
| SMMLV 2026 ($1.750.905, Decreto 1469 de 2025) | Suspendido provisionalmente por el Consejo de Estado el 12-02-2026; decreto transitorio mantiene el valor. | Dejar constancia del SMMLV usado en el otrosí. |

## 8B. Precios unitarios: V4 frente a referencias

Dentro de V4 el VU es el mismo para la cantidad inicial (col N) y la final (col M): la variación es 100% cantidad. Pero el nivel de precios de V4 difiere de tres referencias de la hoja PRESUPUESTO CONTRACTUAL MAYO 25 y del VISOR:

| Referencia | Columna | Renglones | Mediana Δ VU V4 | Efecto a cantidad final (con AIU) |
|---|---|---:|---:|---:|
| VU pactado en la propuesta del contratista (2021) | M | 469 | **+49,0%** | **+$15.086.222.761** (los ítems contractuales valen $44.046M en V4 y valdrían $28.960M al VU pactado) |
| APU actualizado con insumos VISOR 13-09-2024 (= "precio original" del dashboard) | Q | 367 con Δ > 2% | +8,1% | +$3.639.050.739 sobre 126 renglones con cantidad |
| VISOR IDU 07-05-2025 (data.json) | — | según código | −8% aprox. | ver sección H de la app |

**Dato clave (registro de auditoría A-24 y A-25):** el valor actual de obras del contrato (N688 = $44.303.294.799 = H × L) ya está calculado con los VU de V4, de modo que la actualización de los precios pactados a insumos 13-09-2024 se formalizó **antes** de esta solicitud (el libro externo vinculado se llama "EJERCICIO ACTUALIZACIÓN IDU / ANEXO MODIF"). La pregunta para el IDU no es si V4 cambia precios, sino con qué otrosí se pasó de los VU pactados a los actualizados y si ese mayor valor contó como adición para el tope del 50%.

> La versión anterior de esta sección llamaba "presupuesto contractual" a la columna Q (APU 2024) y mostraba 200 ítems / +$3.259M porque la lista estaba truncada a 200 renglones (registro de auditoría B-12).

Top 10 frente a la referencia APU 13-09-2024:

| Fila | Ítem | Descripción | VU ref. | VU V4 | Δ % | Cant. final | Impacto con AIU |
|---:|---|---|---:|---:|---:|---:|---:|
| 34 | 2.003 | LOSA DE CONCRETO MR45 (SUMINISTRO, FORMALETEA | $979.106 | $1.132.473 | +15,7% | 9.851 | +$1.992.044.177 |
| 317 | 5.037 | Proyecto: factibilidad, estudios y diseños de | $39.997 | $50.435 | +26,1% | 18.443 | +$253.813.174 |
| 369 | 5.037 | Proyecto: factibilidad, estudios y diseños de | $39.997 | $50.435 | +26,1% | 17.457 | +$240.252.532 |
| 531 | 6.007 | 6 DUCTOS D=6" + 2 DUCTOS D=3" PVC TDP | $389.500 | $421.190 | +8,1% | 3.912 | +$163.465.339 |
| 14 | 1.006 | TRANSPORTE Y DISPOSICIÓN FINAL DE ESCOMBROS E | $40.317 | $41.825 | +3,7% | 52.469 | +$104.322.362 |
| 81 | 3.035 | LOSA DE CONCRETO MR45 (SUMINISTRO, FORMALETEA | $738.689 | $850.822 | +15,2% | 500 | +$73.929.891 |
| 426 | 5.037 | Proyecto: factibilidad, estudios y diseños de | $39.997 | $50.435 | +26,1% | 4.973 | +$68.446.326 |
| 27 | 1.015 | SUBBASE GRANULAR CLASE C (SBG_C) (SUMINISTRO, | $141.769 | $155.185 | +9,5% | 3.516 | +$62.185.724 |
| 85 | 3.039 | ANDEN CONCRETO GRAVA COMÚN DE 3000 PSI (210 K | $73.210 | $76.194 | +4,1% | 15.469 | +$60.859.378 |
| 46 | 3.005 | EXCAVACIÓN MANUAL EN MATERIAL COMÚN (INCL CAR | $90.934 | $96.914 | +6,6% | 5.855 | +$46.160.374 |

Recomendación: pedir el APU que soporta el VU de V4 para los 20 ítems de mayor impacto (losa MR45, ítem 5.037, ductos TDP, transporte de escombros, andenes), el otrosí que autorizó actualizar los VU pactados y dejar explícito en el otrosí de la adición qué base de precios rige. El ítem 5.037 (código 8643) merece revisión aparte: descripción de consultoría, unidad M2/MES → M2, VU +33,8% y $2.718M en V4 (registro de auditoría A-06).

## 8C. Reubicaciones: lo "eliminado" que reaparece

Un mismo código IDU baja en un renglón (se elimina o disminuye) y sube en otro (nace o aumenta), casi siempre en otro subcapítulo. Renglón a renglón parece eliminado + nuevo; por código es un traslado.

- 32 códigos reubicados. Trasladado = Σ min(valor que sale de los renglones que bajan, valor que entra en los que suben) = **$5.807.343.956** de los $19.443.722.236 "eliminados" (29,9%).
- Eliminación real de alcance contractual: **$13.636.378.280**. Alcance realmente nuevo en ítems del contrato: **$9.393.198.284** (de $15.200.542.240 de "contractual nuevo").

> Corrección 2026-09-28 (registro de auditoría B-13): la versión anterior computaba el traslado con el valor completo de los renglones (Σ N de los que bajan, Σ M de los que suben) y mostraba $6.462.266.802; ahora solo cuenta la parte que cambia. Columnas de la tabla: "valor que sale" y "valor que entra".

| Código | Valor que sale | Valor que entra | Trasladado | Δ neto del código |
|---|---:|---:|---:|---:|
| 5182 | $1.883.363.119 | $2.172.609.354 | $1.883.363.119 | +289.246.235 |
| 3895 | $840.308.079 | $1.325.363.962 | $840.308.079 | +485.055.883 |
| 3017 | $527.403.109 | $2.977.782.529 | $527.403.109 | +2.450.379.420 |
| 8643 | $385.754.898 | $2.717.980.069 | $385.754.898 | +2.332.225.171 |
| 3009 | $269.572.707 | $390.883.230 | $269.572.707 | +121.310.523 |
| 4032 | $243.202.986 | $440.196.331 | $243.202.986 | +196.993.345 |
| 3043 | $199.696.983 | $247.840.218 | $199.696.983 | +48.143.235 |
| 4030 | $401.844.087 | $189.414.957 | $189.414.957 | -212.429.130 |
| 9035 | $160.975.754 | $160.975.754 | $160.975.754 | 0 |
| 3046 | $164.102.112 | $160.474.392 | $160.474.392 | -3.627.720 |

Reemplazos contractual → NP (12 pares por similitud de descripción ≥ 0,7): 7 encarecen (+$1.691.286.881) y 5 abaratan (−$1.818.400.659); neto −$127.113.778. Los mayores sobrecostos: BG_A → NP-124 BG_A con reciclado (+$707.253.958) y MD12 → NP-123 MD19 (+$684.670.659).

## 8D. Lista de chequeo del revisor (resumen)

Soportes del contratista: memoria de cantidades por CIV; APU (FO-GI-19) y actas de los 81 NP; justificación de los 12 reemplazos; conciliación de las 32 reubicaciones (origen → destino); cronograma con curva S y flujo mensual de los 8 meses; conciliación V2 → V4 (cap. 7 y fondo de compensaciones); recálculo de ajustes por vigencia 2027; aclaración de qué rige para pagar el acero (bolsa F o bloque ACEROS); libros externos vinculados (APU 28-07-2025 y "PRESUPUESTO TOTAL $80 MIL"); soporte del código 8643; confirmación de que los 14 NP objetados no reingresan; diseños, permisos de ESP y predios de los 9 CIVs "no alcanza".

Verificaciones de la interventoría: aritmética del libro (hecha, cuadra al peso); revisión de los 3 CIVs outlier; saltos extremos (rajón ×14,7; andén ×135); contraste de VU con VISOR y referencia; funcionalidad del balanceo (manual IDU §11.2.1).

Aspectos legales: tope del 50% en SMMLV sobre el valor inicial de $50.793.789.333 con el incremento previo de $8.633M; expediente de otrosíes y acto que autorizó la actualización de VU; minuta de otrosí (adición + prórroga) con justificación técnica, económica y jurídica, CDP y garantías; informe escrito al IDU (Ley 1474 art. 84); antelación de la radicación.

La app (pestaña "Presupuesto 01-09-2026") trae esta lista con casillas, notas por ítem y exportación a CSV, además de un simulador de escenarios (plazo, % de NP aceptados, rechazo de reemplazos, VU de referencia, exclusión de los 9 CIVs "no alcanza"), un índice de atención por CIV, prioridad de revisión por renglón, búsqueda global y enlaces directos a cada ficha (por ejemplo `#p75/civ/16000024`).

---

## 10. Registro de auditoría

Todo lo que el análisis encontró mal o dudoso en la fuente, lo que tuvo que corregir de sí mismo y lo que no puede resolver solo quedó en un registro reproducible (`python analisis/scripts/auditoria.py` → `analisis/auditoria/registro_auditoria.json`, `.csv` y `analisis/REGISTRO_AUDITORIA.md`; sección N de la app). Cada asiento de la sección A se calcula leyendo el libro con openpyxl e indica hoja, celda y fórmula. Resumen: 66 asientos — 25 sobre la fuente (A), 13 correcciones del análisis con su commit (B), 16 dudas abiertas (C) y 12 limitaciones (D).

Los asientos que cambian la lectura de la solicitud:

| ID | Sev. | Qué dice | Qué se pide |
|---|---|---|---|
| A-25 | ALTA | El valor inicial del contrato fue $50.793.789.333 (hoja PRESUPUESTO CONTRACTUAL MAYO 25, fila 279). El "valor actual" ($59.426.575.199) ya trae +$8.632.785.866; con la solicitud el acumulado es 48,5% del inicial en pesos. | Expediente de otrosíes: qué parte del incremento previo fue adición. |
| A-24 | ALTA | Los VU vigentes están +49,0% (mediana) sobre los pactados en la propuesta (Δ $15.086M con AIU a cantidades finales); la actualización ya está en el valor actual. | Acto que autorizó actualizar los VU y si contó para el tope. |
| A-01 | ALTA | La columna K (VU) depende de un libro externo no entregado ("ANEXO APU MODIF 28-07-2025.xlsx") vía CONSOLIDADO!Q; sin él el libro no se recalcula. | El libro APU y los FO-GI-19. |
| A-02 | ALTA | 81 cantidades por CIV (NP-101 y ductos ENEL) están vinculadas a "PRESUPUESTO TOTAL $80 MIL.xlsx" y al acta ENEL 03-10-2025, no entregados. | Los libros vinculados; explicar la versión "$80 MIL". |
| A-06 | ALTA | Código 8643 (ítem 5.037, $2.718M): descripción de consultoría, unidad M2/MES → M2, VU +33,8%, no está en el VISOR. | Especificación, APU y memoria por CIV. |
| A-04 | MEDIA | BY688 (total SG5, fórmula /2) = 43.258.118.071,5 ≠ Σ CIV SG5 = 43.258.244.367; AH688 + BY688 ≠ CB688. | Libro con totales por CIV recalculados. |
| A-05 | MEDIA | Bloque ACEROS ($3.053M, fuera del total) supera en $75,5M la bolsa fija F. | Cuál rige para pagar. |
| A-03 | MEDIA | 175 renglones con VU digitado (los NP): $14.151M con AIU sin fórmula. | APU de cada NP. |

Correcciones del propio análisis registradas en esta versión (todas verificables con `git log`): B-07 referencias de fila del análisis 06 desplazadas +4/+5; B-08 H06-01 "doble pago" retirado; B-09 falsos positivos del análisis 04; B-11 base del tope del 50%; B-12 "VU contractual" era el APU 2024 y la lista estaba truncada a 200; B-13 cálculo de "trasladado" en reubicaciones.

## 9. Anexos

### 9.1 Datos que soportan este informe

- `analisis/datos/presupuesto_2026_09.json` — hoja principal V4 estructurada (27 CIVs × 649 renglones).
- `analisis/datos/hojas/*.csv` — las 18 hojas del Excel exportadas (col 0 = A, fila n = fila n de Excel).
- `analisis/hallazgos/01_variacion_items.{md,json}` — análisis de variación por ítem.
- `analisis/hallazgos/02_variacion_civ.{md,json}` — análisis de variación por CIV.
- `analisis/hallazgos/03_costo_civ.{md,json}` — costo por CIV.
- `analisis/hallazgos/04_aritmetica.{md,json}` — aritmética, fórmulas y precios unitarios.
- `analisis/hallazgos/05_nps.{md,json}` — análisis de NPs.
- `analisis/hallazgos/06_versiones_plazo.{md,json}` — waterfall V0-V4, componentes y plazo.
- `analisis/analisis_2026_09.json` — consolidado (insumo de la pestaña web).
- `analisis/auditoria/registro_auditoria.{json,csv}` y `analisis/REGISTRO_AUDITORIA.md` — registro de auditoría (sección 10).

### 9.2 Metodología

- Todos los números salen del Excel `4. PRESUPUESTO 01-09-2026 75MM (8 MESES).xlsx` extraído con `openpyxl`. Ningún dato es estimado.
- Cada hallazgo cita la hoja y la fila de Excel de donde se obtiene.
- El AIU contractual usado es **31,849%** (factor 1,31849) — no el 34,01% del dashboard heredado.
- Los componentes SST/Diálogo/PMT usan sus AIU específicos (20,006% y 19,566%).
- La línea base por CIV se reconstruye desde `data.json` (contrato firmado) porque el Excel V4 no distribuye la col H por CIV.

### 9.3 Trampas conocidas

- El CIV `500002375` (V4) = `16004876` (data.json) = `50002375` (MEMORIA) = `16004876` (Hoja1) — todos son el tramo KR65 CL17-CL18.
- La hoja se llama "84 NP": lista 84 códigos NP, de los cuales 81 tienen cantidad (105 renglones); NP-06, NP-08 y NP-11 nunca se cuantifican y 68 renglones NP quedan en cero.
- Diferencias de redondeo de peso: la suma de los 27 CIV da $58.196.933.869 y $75.426.575.268 (ROUND por celda) frente a M688 = $58.196.933.800 y M703 = $75.426.575.199 (ROUND por renglón); O690 tiene una constante mal digitada (…780). Detalle en el registro de auditoría A-10 y A-12.
- La fila 703 dice "04-05-2026" pero el archivo es del 01-09-2026 (probable copia de una versión anterior).

---

*Informe preparado por Consorcio Montevideo 045 · Interventoría del Contrato IDU 1752 de 2021*
