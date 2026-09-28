# 04 - Aritmetica, precios unitarios y formulas
Fuente: `4. PRESUPUESTO 01-09-2026 75MM (8 MESES).xlsx` - Hoja: `PRESUPUESTO TODOS LOS CIV 84 NP` - AIU contractual: **31,849%**  
Fecha analisis: 2026-09-26

## 1. Formulas vs celdas digitadas a mano

- **Formulas encontradas**: 30456
- **Valores hardcoded**: 16394
- **Ratio formulas/total**: 65.0%

### Celdas con errores (0)

Sin celdas con errores tipo #REF!, #DIV/0!, etc.

### Ejemplos de formulas (10)

| Celda | Formula |
|---|---|
| `T7` | `=SUM(T8:T11)` |
| `V7` | `=SUM(V8:V11)` |
| `X7` | `=SUM(X8:X11)` |
| `Z7` | `=SUM(Z8:Z11)` |
| `AB7` | `=SUM(AB8:AB11)` |
| `AD7` | `=SUM(AD8:AD11)` |
| `AF7` | `=SUM(AF8:AF11)` |
| `AH7` | `=SUM(AH8:AH11)` |
| `AK7` | `=SUM(AK8:AK11)` |
| `AM7` | `=SUM(AM8:AM11)` |

## 2. Consistencia aritmetica por fila

### AIU aplicado (L = round(K * 1.31849))
Filas con desviacion > $1: **0**

### M/N/O/Q
Total desviaciones > $1: **2**

Distribucion: {'N': 1, 'O': 1}

| Fila | Columna | Actual | Esperado | delta |
|---|---|---|---|---|
| 34 | N | 12.357.428.721 | 12.357.342.504 | 86.217 |
| 34 | O | 2.351.966.086 | 2.352.052.303 | -86.217 |

### CB (total general por fila) vs M
Desviaciones: **0**

## 3. Consistencia entre hojas

Discrepancias detectadas: **0**

## 4. Duplicados por codigo IDU

Codigos IDU con >1 renglon: **174**

| Codigo IDU | Filas | Reubicacion? |
|---|---|---|
| `5196` | [10, 58] | Si |
| `3017` | [14, 47, 124, 194, 266, 318, 370, 427, 495, 536, 575, 599, 613, 632, 654, 667] | Si |
| `4390` | [15, 46] | Si |
| `NO` | [16, 17, 313, 365] | Si |
| `6486` | [21, 49] | Si |
| `4030` | [22, 60] | Si |
| `5380` | [29, 59] | Si |
| `3837` | [36, 84] | Si |
| `4032` | [38, 52] | Si |
| `4754` | [54, 157, 227, 301, 353, 405, 462, 504, 665] | Si |
| `4907` | [55, 158, 228, 503, 544, 583, 607, 634] | Si |
| `3009` | [123, 193, 263, 315, 367, 424, 494, 535, 574, 598, 612, 636, 666] | Si |
| `3539` | [125, 195] | Si |
| `3523` | [126, 196] | Si |
| `3515` | [127, 197] | Si |
| `3540` | [128, 198] | Si |
| `3315` | [129, 199] | Si |
| `3524` | [130, 200] | Si |
| `3516` | [131, 201] | Si |
| `7419` | [132, 202] | Si |
| `7421` | [133, 203] | Si |
| `7423` | [134, 204] | Si |
| `4402` | [135, 205] | Si |
| `3324` | [136, 206] | Si |
| `4979` | [137, 207] | Si |
| `4841` | [138, 186, 208, 256] | Si |
| `4839` | [139, 209] | Si |
| `4842` | [140, 210] | Si |
| `3328` | [141, 211] | Si |
| `3329` | [142, 212] | Si |

## 5. VU vs referencias

### VU V4 vs VISOR 07-05-25
Desviaciones > 2%: **0**

### VU V4 vs PRESUPUESTO CONTRACTUAL MAYO 25
Desviaciones > 2%: **367**

| Codigo IDU | Fila V4 | K_v4 | K_contractual | delta_pct |
|---|---|---|---|---|
| `4878` | 299 | 203.484 | 119.332 | 70.52% |
| `4878` | 351 | 203.484 | 119.332 | 70.52% |
| `4878` | 403 | 203.484 | 119.332 | 70.52% |
| `4878` | 460 | 203.484 | 119.332 | 70.52% |
| `8406` | 89 | 2.875.373 | 2.024.856 | 42.0% |
| `4849` | 166 | 3.492 | 2.689 | 29.86% |
| `4849` | 236 | 3.492 | 2.689 | 29.86% |
| `8643` | 265 | 50.435 | 39.997 | 26.1% |
| `8643` | 317 | 50.435 | 39.997 | 26.1% |
| `8643` | 369 | 50.435 | 39.997 | 26.1% |
| `8643` | 426 | 50.435 | 39.997 | 26.1% |
| `4841` | 186 | 288.548 | 239.369 | 20.55% |
| `4841` | 256 | 288.548 | 239.369 | 20.55% |
| `8131` | 487 | 3.164 | 2.675 | 18.28% |
| `8131` | 528 | 3.164 | 2.675 | 18.28% |

## 6. Efecto precio vs efecto cantidad

- **Efecto precio total**: 2.391.076.226
- **Efecto cantidad total**: 3.802.952.844
- **Interaccion**: 183.052.834
- **Suma P+Q+I**: 6.377.081.904
- **Delta valor M-N total**: 3.985.894.448
- **Verificacion**: 2.391.187.456

### Items con mayor efecto

| Codigo IDU | Fila | Delta valor | Efecto precio | Efecto cantidad | Interaccion |
|---|---|---|---|---|---|
| `7785` | 34 | 2.351.966.086 | 1.673.513.595 | 2.033.522.234 | 318.530.582 |
| `6016` | 20 | 2.348.873.855 | 2.128.630 | 2.319.766.841 | 29.111.932 |
| `5182` | 490 | -1.883.363.119 | 142.020.241 | -1.741.659.761 | -141.702.690 |
| `3425` | 85 | 1.542.541.484 | 448.519 | 1.482.131.040 | 60.410.860 |
| `3017` | 14 | 766.340.249 | 76.692.049 | 738.707.772 | 27.630.313 |
| `4159` | 27 | 660.384.913 | 5.094.392 | 603.293.164 | 57.091.332 |
| `3380` | 626 | -420.761.696 | 44.739.016 | -376.116.402 | -44.645.485 |
| `5181` | 73 | 413.740.072 | 248.558 | 404.046.825 | 9.692.484 |
| `3017` | 266 | -286.229.798 | 12.134.491 | -275.909.006 | -10.319.984 |
| `3017` | 495 | -240.922.948 | 9.120.254 | -232.235.817 | -8.686.450 |
| `3043` | 273 | -199.696.983 | 21.904.438 | -178.829.189 | -20.868.220 |
| `3009` | 494 | -196.376.002 | 19.432.397 | -177.831.077 | -18.543.401 |
| `4390` | 46 | -195.309.174 | 58.211.782 | -183.257.980 | -12.051.408 |
| `3159` | 489 | -167.940.640 | 14.224.432 | -153.771.962 | -14.169.610 |
| `3046` | 277 | -164.102.112 | 17.866.178 | -146.679.650 | -17.422.548 |
| `3227` | 150 | 149.220.614 | 9.336.942 | 135.691.182 | 13.529.409 |
| `3010` | 9 | -148.475.199 | 7.164.084 | -141.995.948 | -6.478.268 |
| `8655` | 282 | -108.832.918 | 8.717.729 | -100.278.859 | -8.554.365 |
| `3024` | 496 | -104.460.681 | 2.363.915 | -102.291.053 | -2.169.678 |
| `3748` | 81 | 96.526.178 | 61.208.343 | 83.804.656 | 12.721.548 |

## 7. Hallazgos con recomendaciones

### H01 - Inconsistencias aritmeticas en columnas M/N/O/Q (2 filas) [ALTA]

Distribucion por columna: {'N': 1, 'O': 1}. M=I*L, N=H*L, O=(I-H)*L, Q=O+P.

- Impacto estimado: 172.434
- Recomendacion: Solicitar re-calculo de columnas M/N/O/Q con formulas. Detectar filas de digitacion manual.

### H02 - Codigos IDU repetidos en la hoja principal (174) [INFO]

Total codigos con mas de un renglon: 174. En subcapitulos distintos (estructura item x subcapitulo, p. ej. IDU vs ESP): 174. Duplicados reales en el mismo subcapitulo: 0. No implican doble suma: cada renglon tiene su propia cantidad. Si afectan el cruce con V1/V2, que se hace por codigo agregado (ver limitaciones del registro de auditoria).

- Recomendacion: Pedir al contratista la conciliacion de los codigos que pasan de un subcapitulo a otro (reubicaciones, seccion I de la app); si hay duplicados en el mismo subcapitulo, exigir consolidacion.

### H03 - VU V4 desviado >2% de la referencia APU actualizado 13-09-2024 (367 renglones) [ALTA]

Referencia: columna Q 'VALOR ITEM COSTO DIRECTO ACTUALIZACION DE APU INSUMOS VISOR 13-09-2024' de la hoja PRESUPUESTO CONTRACTUAL MAYO 25 (es el 'precio original' del dashboard). Top: 4878 70.52%, 4878 70.52%, 4878 70.52%, 4878 70.52%, 8406 42.0%

- Recomendacion: Pedir el APU (FO-GI-19) de cada renglon con VU distinto a la referencia y la autorizacion del IDU para usarlo en la adicion.

### H04 - Los VU de V4 estan +49.0% (mediana) sobre los VU pactados en la propuesta: 15.086.222.761 con AIU a cantidades finales [ALTA]

469 renglones contractuales tienen VU pactado (col M de PRESUPUESTO CONTRACTUAL MAYO 25). Valorados al VU pactado valdrian 28.959.881.218 en vez de 44.046.009.245. El valor actual de obras del contrato (N688 = 44.303.294.799) ya esta calculado con los VU de V4 sobre las cantidades contractuales, asi que la actualizacion de precios (a insumos VISOR 13-09-2024) se formalizo antes de esta solicitud; el presupuesto original de la propuesta (fila 246 col O) era 28.420.960.042 de obras y 50.793.789.333 en total. Top impacto: 7785 fila 34 +76.0%, 6016 fila 20 +39.7%, 3017 fila 14 +32.5%, 5182 fila 531 +48.0%, 3425 fila 85 +50.6%

- Impacto estimado: 15.086.222.761
- Recomendacion: Pedir el otrosi o acta que autorizo actualizar los VU pactados a insumos 13-09-2024 y confirmar si ese incremento se contabilizo como adicion (cuenta para el tope del 50% del art. 40 de la Ley 80) o como reajuste.

### H05 - Consistencia entre hojas OK (3 diferencias explicadas) [INFO]

Los totales de resumen, EJECUTIVO y Presupuesto estimado coinciden con la hoja principal. Diferencias explicadas: Presupuesto estimado!A11 = 74.667.840.865 (Excluye 'VALOR ESTIMADO DE FASE DE OBRAS INICIALES' (M701 = 758.734.334); la etiqueta A10 lo dice: valor para la etapa de construccion.); EJECUTIVO!I45 = 58.196.933.869 (Diferencia de redondeo: la hoja EJECUTIVO suma los 27 CIV redondeados uno a uno (ROUND por CIV) y la hoja principal redondea el total del renglon.); EJECUTIVO!I56 = 75.426.575.268 (Diferencia de redondeo: la hoja EJECUTIVO suma los 27 CIV redondeados uno a uno (ROUND por CIV) y la hoja principal redondea el total del renglon.)

- Recomendacion: Sin accion. La hoja EJECUTIVO conserva el encabezado 11/05/2026: pedir que se actualice a la fecha del radicado.

