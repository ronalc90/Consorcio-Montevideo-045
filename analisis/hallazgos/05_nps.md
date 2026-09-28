# 05 - Análisis de Ítems No Previstos (NP) - V4 01-09-2026

**Fuente:** hoja `PRESUPUESTO TODOS LOS CIV 84 NP` + `NPs Objetados` + `comparativa.json` (V1/V2)
**AIU contractual:** 31,849%

## 1. Inventario de NPs en V4

- Renglones NP con cantidad actualizada > 0: **105**
- Códigos NP únicos por `item_pago`: **81**
- Códigos NP únicos incluyendo `codigo_idu` (para renglones con codigo_idu='NO' y sin NP en item_pago): **81**
- Suma total valor con AIU: **$14.150.924.549**

La hoja se llama '84 NP' pero solo hay 81 códigos NP con cantidad porque varios códigos NP se replican en más de un renglón (renglones con distinto ítem_pago que comparten el mismo código NP en subcapítulos distintos, y renglones con codigo_idu='NO' que reciben un NP-# en item_pago).

### Desglose por unidad

| Unidad | Renglones | Valor con AIU |
|---|---:|---:|
| M3 | 7 | $5.857.209.779 |
| UN | 56 | $4.005.241.645 |
| ML | 30 | $2.431.794.663 |
| M2 | 1 | $1.107.150.225 |
| UND | 6 | $544.744.650 |
| HR | 1 | $103.278.240 |
| GLB/MES | 2 | $64.475.225 |
| KG | 1 | $26.838.000 |
| VIAJE | 1 | $10.192.122 |

### Desglose por capítulo

| Capítulo | Renglones | Valor con AIU |
|---|---:|---:|
| 5. REDES HIDROSANITARIAS | 77 | $5.164.749.894 |
| 2. PAVIMENTOS | 1 | $3.269.600.612 |
| 1. PRELIMINARES | 4 | $2.634.804.002 |
| 6. REDES SECAS | 18 | $1.918.131.522 |
| 3. ESPACIO PÚBLICO | 5 | $1.163.638.519 |

## 2. Cambios frente a V2 (21-04-2026)

- NPs en V2 (keys): **103**
- NPs en V4 (keys): **81**
- Comunes (aparecen en ambos): **81**
- Eliminados (V2 → ya no en V4): **22**
- Nuevos (aparecen solo en V4): **0**

### Top 15 eliminados (por valor V2 CD)

| code | descripción | und | cant V2 | valor V2 CD | capítulo |
|---|---|---|---:|---:|---|
| NP-82 | TUBERIA CONCRETO REFORZADO  D=32" (INCLUYE SUMINISTRO E INSTALACIÓN). INCLUYE MO | ML | 235.10 | $369.257.464 | 5. REDES HIDROSANITARIAS (Acueducto/Alcantarillado) |
| NP-95 | FRESADO PAVIMENTO ASFÁLTICO (INCLUYE CARGUE) INCLUYE AGUA, PUNTAS. NO INCLUYE TR | M3 | 1045.58 | $137.998.785 | 1. PRELIMINARES |
| NP-128 | INSTALACIÓN DE MATERIAL DE FRESADO. (EXTENDIDO Y COMPACTACIÓN CON VIBROCOMPACTAD | M3 | 4383.93 | $113.622.568 | 1. PRELIMINARES |
| NP-135 | CONTRATO 1752-2021 - BOX CULVERT TIPO POZO, Ancho Int: 1.88 m, Alto Int: 1.80m,  | UN | 3.00 | $103.358.232 | 5. REDES HIDROSANITARIAS (Acueducto/Alcantarillado) |
| NP-67 | ESTABILIZACIÓN DE SUBRASANTE CON RAJÓN, INCLUYE EQUIPO DE COMPACTACIÓN (SUMINIST | M3 | 526.39 | $80.682.954 | 3. ESPACIO PÚBLICO |
| NP-70 | CONTRATO 1752 - 2021 - APUNTALAMIENTO TEMPORAL DE MURO PREDIO IDPAC CON PLANCHON | ML | 103.00 | $62.686.006 | 1. PRELIMINARES |
| NP-25 | TUBERIA CONCRETO D=36" CL. IV REFORZADO (INCLUYE SUMINISTRO E INSTALACIÓN) | ML | 26.17 | $46.115.047 | 5. REDES HIDROSANITARIAS (Acueducto/Alcantarillado) |
| NP-129 | CONTRATO 1752 - 2021 - DETECCIÓN DEL REFUERZO UTILIZANDO FERROSCAN (POR ELEMNTO) | UN | 20.00 | $5.221.620 | 5. REDES HIDROSANITARIAS (Acueducto/Alcantarillado) |
| NP-132 | CONTRATO 1752 - 2021 - METODO PARA DETERMINAR EL NUMERO DE REBOTE (INDICE ESCLER | UN | 15.00 | $2.138.355 | 5. REDES HIDROSANITARIAS (Acueducto/Alcantarillado) |
| NP-130 | CONTRATO 1752 - 2021 - OBTENCION DE NUCLEOS DE CONCRETO ENDURECIDO (NUCLEOS DE 3 | UN | 7.00 | $1.972.334 | 5. REDES HIDROSANITARIAS (Acueducto/Alcantarillado) |
| NP-76 | TRANSPORTE DE PETREOS | M3 | 16.94 | $640.332 | 5. REDES HIDROSANITARIAS (Acueducto/Alcantarillado) |
| NP-131 | CONTRATO 1752 - 2021 - DETERMINACION DE LA PROFUNDIDAD DE CARBONATACION EN CONCR | UN | 7.00 | $624.715 | 5. REDES HIDROSANITARIAS (Acueducto/Alcantarillado) |
| NP-06 | 2 DUCTOS D=6" + 2 DUCTOS D=3" PVC TDP (Incluye suministro e instalación. No Incl | ML | 0.00 | $0 | 6. REDES SECAS (ENEL, ETB, Vanti) |
| NP-08 | 4 DUCTOS D=4" + 2 DUCTOS D=3" PVC TDP (Incluye suministro e instalación. No Incl | ML | 0.00 | $0 | 6. REDES SECAS (ENEL, ETB, Vanti) |
| NP-106 | CARCAMO DE PROTECCION CON ELEMENTOS PREFABRICADOS PARA PROTECCION DE 6 DUCTOS D= | ML | 0.00 | $0 | 6. REDES SECAS (ENEL, ETB, Vanti) |

### Top 15 nuevos (por valor V4 con AIU)

| code | fila | descripción | und | cant V4 | valor V4 AIU |
|---|---:|---|---|---:|---:|

### Top 15 comunes con mayor Δvalor

| code | fila V4 | descripción | und | cant V2 | cant V4 | valor V2 CD | valor V4 CD | Δ CD |
|---|---:|---|---|---:|---:|---:|---:|---:|
| NP-03 | 547 | CONSTRUCCION DE CAJA DE INSPECCION DOBLE PARA CANALIZACION D | UN | 0.00 | 165.00 | $0 | $590.381.611 | $590.381.611 |
| NP-124 | 30 | BASE GRANULAR CLASE A (BG_A) CON RECICLADO DE CONCRETO HIDRA | M3 | 7495.05 | 10476.55 | $1.448.148.591 | $1.910.156.251 | $462.007.660 |
| NP-16 | 87 | ESTAMPADO PARA CONCRETO MR DE POMPEYANOS, ACCESOS VEHICULARE | M2 | 9540.78 | 18100.45 | $442.615.866 | $839.710.749 | $397.094.883 |
| NP-123 | 39 | MEZCLA ASFÁLTICA EN CALIENTE DENSA MD19 CON CEMENTO ASFÁLTIC | M3 | 1686.10 | 2089.45 | $2.120.591.109 | $2.479.806.909 | $359.215.800 |
| NP-122 | 561 | CONSTRUCCION DE CAJA DE INSPECCION DOBLE PARA CANALIZACION D | UN | 0.00 | 73.00 | $0 | $245.165.536 | $245.165.536 |
| NP-07 | 551 | 6 DUCTOS D=6" PVC-TDP (INCLUYE SUMINISTRO E INSTALACIÓN. NO  | ML | 0.00 | 619.86 | $0 | $229.500.851 | $229.500.851 |
| NP-71 | 418 | TUBERIA CONCRETO ALTA RESISTENCIA D= 10" (INCLUYE SUMINISTRO | ML | 0.00 | 599.07 | $0 | $208.326.184 | $208.326.184 |
| NP-19 | 465 | TUBERIA PVC U.M. EXT CORRUGADO/INT LISO U.M. NORMA NTC 3722- | ML | 52.29 | 122.01 | $98.468.659 | $229.760.222 | $131.291.563 |
| NP-133 | 479 | CONTRATO 1752-2021 - BOX CULVERT PREFABRICADO TIPO 1, Ancho  | UN | 126.00 | 110.00 | $1.555.213.842 | $1.425.680.392 | $-129.533.450 |
| NP-42 | 172 | CODO HD 45° EXTREMO LISO PARA PVC D=6" (SUMINISTRO E INSTALA | UN | 0.00 | 220.00 | $0 | $106.777.147 | $106.777.147 |
| NP-18 | 464 | TUBERIA PVC U.M. EXT CORRUGADO/INT LISO U.M. NORMA NTC 3722- | ML | 0.00 | 108.96 | $0 | $93.320.216 | $93.320.216 |
| NP-12 | 562 | ADAPTADOR TERMINAL CAMPANA PVC D=6" (SUMINISTRO E INSTALACIÓ | UN | 0.00 | 2688.00 | $0 | $83.747.584 | $83.747.584 |
| NP-22 | 411 | TUBERIA CONCRETO D=18" CL. II SIN REFUERZO (INCLUYE SUMINIST | ML | 0.00 | 199.94 | $0 | $83.498.670 | $83.498.670 |
| NP-62 | 360 | CONTRATO DE OBRA IDU-1752-2021 - SERVICIO DE VÁCTOR PARA LIM | HR | 0.00 | 216.00 | $0 | $78.330.696 | $78.330.696 |
| NP-72 | 419 | TUBERIA DE CONCRETO DE ALTA RESISTENCIA D= 16" (INCLUYE MORT | ML | 0.00 | 119.01 | $0 | $78.254.746 | $78.254.746 |

## 3. NPs objetados que siguen incluidos

De los **14** NPs de la hoja `NPs Objetados`, **0** aparecen en V4 con cantidad > 0.
Valor total (AIU) de los objetados que siguen incluidos: **$0**

| # | item_pago | codigo_idu | descripción | und | fila V4 | cant V4 | valor V4 AIU | VU V2 CD | VU V4 CD | Δ VU% |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | NP-68 | 10074 | VALLA UNA CARA, DE 3.0M X 6.0M CON ESTRUCTURA METÁLICA - ESTRUCTURA TI | UN | *no aparece en V4* | - | - | $6.942.537 | - | - |
| 2 | NP-69 | 4946 | ALQUILER DE CERRAMIENTO TIPO 2: CONSTA DE POSTES ROLLIZOS DE 1.90MT DE | ML/MES | *no aparece en V4* | - | - | $33.864 | - | - |
| 3 | NP-90 | NO | SUMINISTRO E INSTALACION DE PLASTICO NEGRO CALIBRE 6 PARA CONTROL DE P | M2 | *no aparece en V4* | - | - | $2.187 | - | - |
| 4 | NP-91 | NO | SUMINISTRO E INSTALACION DE PUNTO ECOLOGICO 12 LITROS ESTRUCTURA 3 PUE | UN | *no aparece en V4* | - | - | $145.000 | - | - |
| 5 | NP-92 | NO | CAPACITACION NIVEL ENTRANTE ESPACIOS CONFINADOS | UN | *no aparece en V4* | - | - | $320.000 | - | - |
| 6 | NP-93 | NO | CAPACITACION NIVEL VIGIA ESPACIOS CONFINADOS | UN | *no aparece en V4* | - | - | $250.000 | - | - |
| 7 | NP-94 | NO | CAPACITACION NIVEL SUPERVISOR ESPACIOS CONFINADOS | UN | *no aparece en V4* | - | - | $330.000 | - | - |
| 8 | NP-97 | NO | PUNTO DE HIDRATACION, (SUMINISTRO DE BOTELLON DE 20000 ML, 20 LITROS O | UN | *no aparece en V4* | - | - | $17.483 | - | - |
| 9 | NP-100 | NO | SUMINISTRO DE KIT ANTIDERRAMES DE 5 GALONES |  | *no aparece en V4* | - | - | $171.083 | - | - |
| 10 | NP-96 | NO | CAPACITACION NIVEL SUPERVISOR DE IZAJES | UN | *no aparece en V4* | - | - | $400.000 | - | - |
| 11 | NP-98 | 7873 | TRATAMIENTO Y DISPOSICIÓN FINAL DE RESIDUOS PELIGROSOS. | KG | *no aparece en V4* | - | - | $1.314 | - | - |
| 12 | NP-108 | 6874 | ENCUESTA DE PERCEPCIÓN CIUDADANA. INCL. FORMATO DE ENCUESTA DE PERCEPC | UN | *no aparece en V4* | - | - | $105.494 | - | - |
| 13 | NP-99 | NO | FLECHA LUMINOSA INTERMITENTE DE 1.10 MTS DE LONGITUD Y 40 CMS DE ANCHO | UN | *no aparece en V4* | - | - | $1.251.176 | - | - |
| 14 | NP-107 | 7508 | BARRERA RELLENABLE (2.00X0.55X1.00M) CON CINTA REFLECTIVA (INCLUYE SUM | UN | *no aparece en V4* | - | - | $522.726 | - | - |

## 4. NPs GLB / MES

No hay NPs con unidad GLB o MES en V4.

## 5. Top 20 NPs por valor con AIU

| # | fila | item_pago | codigo_idu | descripción | und | cant | K (VU CD) | L (VU CD+AIU) | valor AIU | capítulo | # CIVs |
|---:|---:|---|---|---|---|---:|---:|---:|---:|---|---:|
| 1 | 39 | NP-123 | 8618 | MEZCLA ASFÁLTICA EN CALIENTE DENSA MD19 CON CEMENTO ASFÁLTICO CA 14 (S | M3 | 2089.45 | $1.186.823 | $1.564.814 | $3.269.600.612 | 2. PAVIMENTOS | 27 |
| 2 | 30 | NP-124 | 4744 | BASE GRANULAR CLASE A (BG_A) CON RECICLADO DE CONCRETO HIDRAULICO (SUM | M3 | 10476.554999999998 | $182.327 | $240.396 | $2.518.521.916 | 1. PRELIMINARES | 27 |
| 3 | 479 | NP-133 | N/A | CONTRATO 1752-2021 - BOX CULVERT PREFABRICADO TIPO 1, Ancho Int: 1.875 | UN | 110 | $12.960.731 | $17.088.594 | $1.879.745.340 | 5. REDES HIDROSANITARIAS | 1 |
| 4 | 87 | NP-16 | 10271 | ESTAMPADO PARA CONCRETO MR DE POMPEYANOS, ACCESOS VEHICULARES A PREDIO | M2 | 18100.45 | $46.392 | $61.167 | $1.107.150.225 | 3. ESPACIO PÚBLICO | 27 |
| 5 | 547 | NP-03 | 9032 | CONSTRUCCION DE CAJA DE INSPECCION DOBLE PARA CANALIZACION DE M.T. Y B | UN | 165 | $3.578.070 | $4.717.650 | $778.412.250 | 6. REDES SECAS | 27 |
| 6 | 561 | NP-122 | N/A | CONSTRUCCION DE CAJA DE INSPECCION DOBLE PARA CANALIZACION DE M.T. Y B | UN | 73 | $3.358.432 | $4.428.059 | $323.248.307 | 6. REDES SECAS | 26 |
| 7 | 465 | NP-19 | 7435 | TUBERIA PVC U.M. EXT CORRUGADO/INT LISO U.M. NORMA NTC 3722-1 D=36" (I | ML | 122.00999999999999 | $1.883.126 | $2.482.883 | $302.936.555 | 5. REDES HIDROSANITARIAS | 2 |
| 8 | 551 | NP-07 | 3408 | 6 DUCTOS D=6" PVC-TDP (INCLUYE SUMINISTRO E INSTALACIÓN. NO INCLUYE RE | ML | 619.86 | $370.246 | $488.166 | $302.594.577 | 6. REDES SECAS | 15 |
| 9 | 418 | NP-71 | 4892 | TUBERIA CONCRETO ALTA RESISTENCIA D= 10" (INCLUYE SUMINISTRO, INSTALAC | ML | 599.07 | $347.749 | $458.504 | $274.675.991 | 5. REDES HIDROSANITARIAS | 15 |
| 10 | 355 | NP-27 | 3878 | PLACA CUBIERTA D=1.70M POZO INSPEC. (PREFABRICADA. INCLUYE SUMINISTRO  | UND | 73 | $1.877.362 | $2.475.283 | $180.695.659 | 5. REDES HIDROSANITARIAS | 25 |
| 11 | 357 | NP-29 | 3471 | CILINDRO POZO INSP. EN MAMPOSTERIA E=0.25M (INC. SUMIN. Y CONST, ACERO | ML | 157.63 | $755.788 | $996.499 | $157.078.137 | 5. REDES HIDROSANITARIAS | 25 |
| 12 | 463 | NP-17 | 7432 | TUBERIA PVC U.M. EXT CORRUGADO/INT LISO U.M. NORMA NTC 3722-1 D=24" (I | ML | 148.03 | $722.427 | $952.513 | $141.000.499 | 5. REDES HIDROSANITARIAS | 3 |
| 13 | 172 | NP-42 | 3306 | CODO HD 45° EXTREMO LISO PARA PVC D=6" (SUMINISTRO E INSTALACIÓN) | UN | 220 | $485.351 | $639.930 | $140.784.600 | 5. REDES HIDROSANITARIAS | 22 |
| 14 | 408 | NP-19 | 7435 | TUBERIA PVC U.M. EXT CORRUGADO/INT LISO U.M. NORMA NTC 3722-1 D=36" (I | ML | 52.29 | $1.883.126 | $2.482.883 | $129.829.952 | 5. REDES HIDROSANITARIAS | 2 |
| 15 | 464 | NP-18 | 7433 | TUBERIA PVC U.M. EXT CORRUGADO/INT LISO U.M. NORMA NTC 3722-1 D=27" (I | ML | 108.96 | $856.463 | $1.129.238 | $123.041.772 | 5. REDES HIDROSANITARIAS | 1 |
| 16 | 562 | NP-12 | 8081 | ADAPTADOR TERMINAL CAMPANA PVC D=6" (SUMINISTRO E INSTALACIÓN) | UN | 2688 | $31.156 | $41.079 | $110.420.352 | 6. REDES SECAS | 27 |
| 17 | 411 | NP-22 | 3937 | TUBERIA CONCRETO D=18" CL. II SIN REFUERZO (INCLUYE SUMINISTRO E INSTA | ML | 199.94 | $417.619 | $550.626 | $110.092.162 | 5. REDES HIDROSANITARIAS | 2 |
| 18 | 354 | NP-26 | 3879 | PLACA FONDO D=1.70M POZO INSPEC. (PREFABRICADA. INCL. SUMIN, INST.) | UND | 73 | $1.116.536 | $1.472.142 | $107.466.366 | 5. REDES HIDROSANITARIAS | 25 |
| 19 | 415 | NP-27 | 3878 | PLACA CUBIERTA D=1.70M POZO INSPEC. (PREFABRICADA. INCLUYE SUMINISTRO  | UND | 43.2 | $1.877.362 | $2.475.283 | $106.932.226 | 5. REDES HIDROSANITARIAS | 21 |
| 20 | 413 | NP-24 | 3993 | TUBERIA CONCRETO D=27" CL. IV REFORZADO (INCLUYE SUMINISTRO E INSTALAC | ML | 70.9 | $1.136.270 | $1.498.161 | $106.219.615 | 5. REDES HIDROSANITARIAS | 1 |

### Preguntas al contratista (top 20)

1. **fila 39 · NP-123 · MEZCLA ASFÁLTICA EN CALIENTE DENSA MD19 CON CEMENTO ASFÁLTICO CA 14 (Suministro,** (M3 × 2089.45) → ¿APU actualizado y justificación de la memoria de cantidad para este material?
2. **fila 30 · NP-124 · BASE GRANULAR CLASE A (BG_A) CON RECICLADO DE CONCRETO HIDRAULICO (SUMINISTRO, E** (M3 × 10476.554999999998) → ¿APU actualizado y justificación de la memoria de cantidad para este material?
3. **fila 479 · NP-133 · CONTRATO 1752-2021 - BOX CULVERT PREFABRICADO TIPO 1, Ancho Int: 1.875 m, Alto I** (UN × 110) → ¿Cotizaciones de mercado (mínimo 3) y APU detallado?
4. **fila 87 · NP-16 · ESTAMPADO PARA CONCRETO MR DE POMPEYANOS, ACCESOS VEHICULARES A PREDIOS Y VÍAS (** (M2 × 18100.45) → ¿Cuál es el CIV de referencia con el área que respalda la cantidad y su categoría de intervención?
5. **fila 547 · NP-03 · CONSTRUCCION DE CAJA DE INSPECCION DOBLE PARA CANALIZACION DE M.T. Y B.T. TIPO C** (UN × 165) → ¿Cotizaciones de mercado (mínimo 3) y APU detallado?
6. **fila 561 · NP-122 · CONSTRUCCION DE CAJA DE INSPECCION DOBLE PARA CANALIZACION DE M.T. Y B.T. TIPO C** (UN × 73) → ¿Cotizaciones de mercado (mínimo 3) y APU detallado?
7. **fila 465 · NP-19 · TUBERIA PVC U.M. EXT CORRUGADO/INT LISO U.M. NORMA NTC 3722-1 D=36" (INCLUYE SUM** (ML × 122.00999999999999) → ¿Traza de la longitud sobre plano IDU y coincidencia con longitudes contractuales?
8. **fila 551 · NP-07 · 6 DUCTOS D=6" PVC-TDP (INCLUYE SUMINISTRO E INSTALACIÓN. NO INCLUYE RELLENOS). N** (ML × 619.86) → ¿Traza de la longitud sobre plano IDU y coincidencia con longitudes contractuales?
9. **fila 418 · NP-71 · TUBERIA CONCRETO ALTA RESISTENCIA D= 10" (INCLUYE SUMINISTRO, INSTALACIÓN Y MORT** (ML × 599.07) → ¿Traza de la longitud sobre plano IDU y coincidencia con longitudes contractuales?
10. **fila 355 · NP-27 · PLACA CUBIERTA D=1.70M POZO INSPEC. (PREFABRICADA. INCLUYE SUMINISTRO E INSTALAC** (UND × 73) → ¿APU actualizado, memoria de cantidad y soporte del precio unitario?
11. **fila 357 · NP-29 · CILINDRO POZO INSP. EN MAMPOSTERIA E=0.25M (INC. SUMIN. Y CONST, ACERO PARA ESCA** (ML × 157.63) → ¿Traza de la longitud sobre plano IDU y coincidencia con longitudes contractuales?
12. **fila 463 · NP-17 · TUBERIA PVC U.M. EXT CORRUGADO/INT LISO U.M. NORMA NTC 3722-1 D=24" (INCLUYE SUM** (ML × 148.03) → ¿Traza de la longitud sobre plano IDU y coincidencia con longitudes contractuales?
13. **fila 172 · NP-42 · CODO HD 45° EXTREMO LISO PARA PVC D=6" (SUMINISTRO E INSTALACIÓN)** (UN × 220) → ¿Cotizaciones de mercado (mínimo 3) y APU detallado?
14. **fila 408 · NP-19 · TUBERIA PVC U.M. EXT CORRUGADO/INT LISO U.M. NORMA NTC 3722-1 D=36" (INCLUYE SUM** (ML × 52.29) → ¿Traza de la longitud sobre plano IDU y coincidencia con longitudes contractuales?
15. **fila 464 · NP-18 · TUBERIA PVC U.M. EXT CORRUGADO/INT LISO U.M. NORMA NTC 3722-1 D=27" (INCLUYE SUM** (ML × 108.96) → ¿Traza de la longitud sobre plano IDU y coincidencia con longitudes contractuales?
16. **fila 562 · NP-12 · ADAPTADOR TERMINAL CAMPANA PVC D=6" (SUMINISTRO E INSTALACIÓN)** (UN × 2688) → ¿Cotizaciones de mercado (mínimo 3) y APU detallado?
17. **fila 411 · NP-22 · TUBERIA CONCRETO D=18" CL. II SIN REFUERZO (INCLUYE SUMINISTRO E INSTALACIÓN)** (ML × 199.94) → ¿Traza de la longitud sobre plano IDU y coincidencia con longitudes contractuales?
18. **fila 354 · NP-26 · PLACA FONDO D=1.70M POZO INSPEC. (PREFABRICADA. INCL. SUMIN, INST.)** (UND × 73) → ¿APU actualizado, memoria de cantidad y soporte del precio unitario?
19. **fila 415 · NP-27 · PLACA CUBIERTA D=1.70M POZO INSPEC. (PREFABRICADA. INCLUYE SUMINISTRO E INSTALAC** (UND × 43.2) → ¿APU actualizado, memoria de cantidad y soporte del precio unitario?
20. **fila 413 · NP-24 · TUBERIA CONCRETO D=27" CL. IV REFORZADO (INCLUYE SUMINISTRO E INSTALACIÓN)** (ML × 70.9) → ¿Traza de la longitud sobre plano IDU y coincidencia con longitudes contractuales?

## 6. Clasificación de todos los NPs de V4

| categoría | renglones | valor con AIU |
|---|---:|---:|
| aprobado | 0 | $0 |
| en_revision | 105 | $14.150.924.549 |
| objetado | 0 | $0 |
| nuevo | 0 | $0 |

**Categorías:**
- `aprobado`: NP con cant_idu > 0 en V1 IDU 25-02-2026.
- `en_revision`: NP con cant_cont > 0 en V2 pero cant_idu = 0 en V1.
- `objetado`: NP listado en la hoja oculta `NPs Objetados`.
- `nuevo`: NP que no aparece en V1 ni V2 ni en la lista de objetados.

## 7. Hallazgos

### H-NP-06 · [INFO] 22 NPs de V2 fueron eliminados en V4
- **Hoja/Fila:** PRESUPUESTO TODOS LOS CIV 84 NP / None
- **Impacto:** $-924.318.412
- **Descripción:** Reduce en $924.318.412 (CD) frente a V2. Verificar si son NPs anulados o solo re-etiquetados.
- **Recomendación:** Revisar en el balance de NPs anulados / rechazados que estos coincidan con los eliminados.

### H-NP-07 · [ALTA] 2 NPs con salto >50% en cantidad y >$100M CD entre V2 y V4
- **Hoja/Fila:** PRESUPUESTO TODOS LOS CIV 84 NP / 87,465
- **Impacto:** $528.386.446
- **Descripción:** NP-16 Δcant=8559.7 (M2) ΔCD=$397.094.883; NP-19 Δcant=69.7 (ML) ΔCD=$131.291.563
- **Recomendación:** Solicitar memoria de cantidad actualizada para cada NP con salto y explicación del cambio.
