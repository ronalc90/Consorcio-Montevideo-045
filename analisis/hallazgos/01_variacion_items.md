# 01 - Variacion de cantidades por item (inicial vs final)

Fuente: `analisis/datos/presupuesto_2026_09.json` (hoja **PRESUPUESTO TODOS LOS CIV 84 NP**).
Excluye capitulo 8 ACEROS (filas 680-687). Todos los valores con AIU 31,849 %.

## Resumen ejecutivo

- Renglones analizados: **644** (filas 7-679).
- Total valor inicial (N): **$44.303.294.799**.
- Total valor final (M): **$58.196.933.800**.
- Delta total: **$13.893.639.001**.

### Conteos por estado

| Estado | Renglones | Delta valor |
|---|---:|---:|
| eliminado | 118 | $-19.443.722.236 |
| nuevo_contractual | 93 | $15.200.542.240 |
| np_nuevo | 105 | $14.150.924.549 |
| aumento | 27 | $8.809.106.675 |
| disminucion | 39 | $-4.823.212.227 |
| sin_cambio | 25 | $0 |
| np_vacio | 68 | $0 |
| vacio | 169 | $0 |

## Bloque de conciliacion al peso

- Obras (calc) valor inicial: **$44.303.294.799**  vs  teorico BRIEF **$44.303.294.799**  (diff $0).
- Obras (calc) valor final:   **$58.196.933.800**  vs  teorico BRIEF **$58.196.933.800**  (diff $0).
- Delta obras: **$13.893.639.001** vs teorico **$13.893.639.001** (diff $0).
- Conciliaciones: inicial OK, final OK, delta OK.

Descomposicion del delta (por columnas del Excel):

- Suma balance mayores/menores (col O): **$-257.285.548**
- Suma incorporacion NP (col P):        **$14.150.924.549**
- Suma O + P = **$13.893.639.001** (debe igualar delta 13.893.639.001)

Discrepancias en formulas linea a linea:
- J = I - H  no cuadra en **0** renglones.
- O = (I-H) x L  no cuadra en **1** renglones (tol $10).
- Q = O + P  no cuadra en **0** renglones (tol $10).

## Resumen por capitulo

| Capitulo | Valor inicial | Valor final | Delta | Balance may/men | Incorp. NP |
|---|---:|---:|---:|---:|---:|
| 1. PRELIMINARES | $6.508.713.086 | $9.296.447.391 | $2.787.734.305 | $152.930.303 | $2.634.804.002 |
| 2. PAVIMENTOS | $15.328.367.366 | $18.884.475.147 | $3.556.107.781 | $286.507.169 | $3.269.600.612 |
| 3. ESPACIO PÚBLICO | $7.252.761.854 | $6.737.451.907 | $-515.309.947 | $-1.678.948.466 | $1.163.638.519 |
| 4. SEÑALIZACIÓN Y DEMARCACIÓN | $1.198.662.405 | $1.198.662.405 | $0 | $0 | $0 |
| 5. REDES HIDROSANITARIAS | $9.324.763.052 | $16.102.615.589 | $6.777.852.537 | $1.613.102.643 | $5.164.749.894 |
| 6. REDES SECAS | $4.363.449.811 | $5.977.281.361 | $1.613.831.550 | $-304.299.972 | $1.918.131.522 |
| 7. DESVÍOS | $326.577.225 | $0 | $-326.577.225 | $-326.577.225 | $0 |
| **TOTAL** | **$44.303.294.799** | **$58.196.933.800** | **$13.893.639.001** | **$-257.285.548** | **$14.150.924.549** |

## Resumen por subcapitulo (ordenado por |delta|)

| Capitulo | Subcapitulo | Valor inicial | Valor final | Delta |
|---|---|---:|---:|---:|
| 5. REDES HIDROSANITARIAS | OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DEL IDU | $8.612.662.417 | $166.012.072 | $-8.446.650.345 |
| 5. REDES HIDROSANITARIAS | OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DEL IDU | $0 | $5.631.704.208 | $5.631.704.208 |
| 6. REDES SECAS | INSTALACIONES ELECTRICAS A CARGO DE  ENEL MEDIA Y BAJA TENSIÓN | $0 | $5.216.792.124 | $5.216.792.124 |
| 5. REDES HIDROSANITARIAS | OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DE LA EAAB | $0 | $4.776.120.914 | $4.776.120.914 |
| 5. REDES HIDROSANITARIAS | OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DE LA EAAB | $0 | $3.673.810.682 | $3.673.810.682 |
| 2. PAVIMENTOS | (sin subcapitulo) | $15.328.367.366 | $18.884.475.147 | $3.556.107.781 |
| 6. REDES SECAS | INSTALACIONES ELECTRICAS A CARGO DEL IDU MEDIA Y BAJA TENSIÓN | $3.438.433.262 | $160.731.747 | $-3.277.701.515 |
| 1. PRELIMINARES | RELLENOS Y CAPAS GRANULARES (BASE Y SUBBASE) | $3.914.090.603 | $5.960.991.057 | $2.046.900.454 |
| 1. PRELIMINARES | EXCAVACIONES | $2.316.052.200 | $3.237.957.951 | $921.905.751 |
| 5. REDES HIDROSANITARIAS | OBRAS PARA LA RED DE ACUEDUCTO A CARGO DE LA ESP EAAB | $0 | $602.616.128 | $602.616.128 |
| 6. REDES SECAS | INSTALACIONES RED TELEFÓNICA DE ETB - A CARGO IDU | $817.993.544 | $267.308.256 | $-550.685.288 |
| 5. REDES HIDROSANITARIAS | OBRAS PARA LA RED DE ACUEDUCTO OBRAS A CARGO DEL IDU | $712.100.635 | $1.252.351.585 | $540.250.950 |
| 3. ESPACIO PÚBLICO | Andenes, Prefabricados y Pisos | $4.094.854.546 | $3.693.746.676 | $-401.107.870 |
| 7. DESVÍOS | (sin subcapitulo) | $326.577.225 | $0 | $-326.577.225 |
| 6. REDES SECAS | INSTALACIONES ELECTRICAS A CARGO DE ENEL ALUMBRADO PUBLICO | $0 | $202.318.124 | $202.318.124 |
| 1. PRELIMINARES | (sin subcapitulo) | $278.570.283 | $97.498.383 | $-181.071.900 |
| 3. ESPACIO PÚBLICO | Excavaciones, Demoliciones y Rellenos | $2.583.364.292 | $2.457.123.923 | $-126.240.369 |
| 6. REDES SECAS | INSTALACIONES RED TELEFÓNICA DE ETB A CARGO ESP | $0 | $26.054.596 | $26.054.596 |
| 6. REDES SECAS | INSTALACIONES UNE EPM | $18.752.584 | $0 | $-18.752.584 |
| 6. REDES SECAS | INSTALACIONES VANTI | $0 | $13.510.687 | $13.510.687 |
| 3. ESPACIO PÚBLICO | Mobiliario y Paisajismo | $574.543.016 | $586.581.308 | $12.038.292 |
| 6. REDES SECAS | INSTALACIONES MOVISTAR | $88.270.421 | $90.565.827 | $2.295.406 |
| 4. SEÑALIZACIÓN Y DEMARCACIÓN | (sin subcapitulo) | $1.198.662.405 | $1.198.662.405 | $0 |
| 6. REDES SECAS | INSTALACIONES ELECTRICAS A CARGO DEL IDU ALUMBRADO PUBLICO | $0 | $0 | $0 |
| 7. DESVÍOS | INSTALACIONES ELECTRICAS | $0 | $0 | $0 |

## Hallazgos por severidad

### ALTA (30)

#### H01-013 - Variacion capitulo 5. REDES HIDROSANITARIAS: 6.777.852.537

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: capitulo
- **Impacto**: $6.777.852.537
- **Descripcion**: 5. REDES HIDROSANITARIAS: valor inicial 9.324.763.052 -> final 16.102.615.589. Balance mayores/menores 1.613.102.643 + incorporacion NP 5.164.749.894.
- **Recomendacion**: Revisar composicion del capitulo, especialmente aumentos que se apoyen mayormente en NPs.

#### H01-014 - Variacion capitulo 2. PAVIMENTOS: 3.556.107.781

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: capitulo
- **Impacto**: $3.556.107.781
- **Descripcion**: 2. PAVIMENTOS: valor inicial 15.328.367.366 -> final 18.884.475.147. Balance mayores/menores 286.507.169 + incorporacion NP 3.269.600.612.
- **Recomendacion**: Revisar composicion del capitulo, especialmente aumentos que se apoyen mayormente en NPs.

#### H01-035 - NP de alto valor (fila 39)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 39
- **Impacto**: $3.269.600.612
- **Descripcion**: NP NP-123 'MEZCLA ASFÁLTICA EN CALIENTE DENSA MD19 CON CEMENTO ASFÁLTICO CA 14 (Suministro, Extendido, Nivelación y Compactación
mecánica con vibrocompactador y compactador de llantas)' incorpora cantidad 2089.45 M3 por 3.269.600.612.
- **Recomendacion**: Revisar aprobacion IDU del NP, analisis de precio unitario y sustento tecnico. Verificar que no exista un item contractual equivalente.

#### H01-015 - Variacion capitulo 1. PRELIMINARES: 2.787.734.305

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: capitulo
- **Impacto**: $2.787.734.305
- **Descripcion**: 1. PRELIMINARES: valor inicial 6.508.713.086 -> final 9.296.447.391. Balance mayores/menores 152.930.303 + incorporacion NP 2.634.804.002.
- **Recomendacion**: Revisar composicion del capitulo, especialmente aumentos que se apoyen mayormente en NPs.

#### H01-020 - Variacion relativa alta (fila 33)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 33
- **Impacto**: $-2.584.929.953
- **Descripcion**: Item 2.002 'MEZCLA ASFÁLTICA DENSA EN CALIENTE MD12 CON CEMENTO ASFÁLTICO 60-70 (SUMINISTRO, EXTENDIDO, NIVELACIÓN Y COMPACTACIÓN MECANICA CON VIBROCOMPACTADOR Y COMPACTADOR DE LLANTAS)': H=1721.0, I=0.0 (M3), variacion relativa 100%. Impacto -2.584.929.953.
- **Recomendacion**: Solicitar memoria detallada de cantidad y respaldo tecnico. Cruzar con planos as-built.

#### H01-030 - Item contractual eliminado (fila 33)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 33
- **Impacto**: $-2.584.929.953
- **Descripcion**: Item 2.002 'MEZCLA ASFÁLTICA DENSA EN CALIENTE MD12 CON CEMENTO ASFÁLTICO 60-70 (SUMINISTRO, EXTENDIDO, NIVELACIÓN Y COMPACTACIÓN MECANICA CON VIBROCOMPACTADOR Y COMPACTADOR DE LLANTAS)' pasa de 1721.0 a 0 (M3). Reduccion -2.584.929.953.
- **Recomendacion**: Confirmar que la actividad efectivamente no se ejecutara o se reemplaza por otra. Si se reemplaza, aparear con NP correspondiente.

#### H01-036 - NP de alto valor (fila 30)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 30
- **Impacto**: $2.518.521.916
- **Descripcion**: NP NP-124 'BASE GRANULAR CLASE A (BG_A) CON RECICLADO DE CONCRETO HIDRAULICO (SUMINISTRO, EXTENDIDO, NIVELACIÓN, HUMEDECIMIENTO Y COMPACTACIÓN CON VIBROCOMPACTADOR)' incorpora cantidad 10476.554999999998 M3 por 2.518.521.916.
- **Recomendacion**: Revisar aprobacion IDU del NP, analisis de precio unitario y sustento tecnico. Verificar que no exista un item contractual equivalente.

#### H01-010 - Salto extremo de cantidad (I/H = 14.6764x) - fila 20

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 20
- **Impacto**: $2.348.873.855
- **Descripcion**: Item 1.008 'ESTABILIZACIÓN DE SUBRASANTE CON RAJÓN, INCLUYE EQUIPO DE COMPACTACIÓN (SUMINISTRO, EXTENDIDO, NIVELACIÓN Y COMPACTACIÓN CON EQUIPO MECÁNICO)' paso de 965.0 a 14162.699999999997 M3. Impacto 2.348.873.855.
- **Recomendacion**: Pedir memoria de cantidades actualizada por CIV y validar con actas de campo/planos. Verificar que no se trate de reasignacion desde otro item.

#### H01-021 - Variacion relativa alta (fila 20)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 20
- **Impacto**: $2.348.873.855
- **Descripcion**: Item 1.008 'ESTABILIZACIÓN DE SUBRASANTE CON RAJÓN, INCLUYE EQUIPO DE COMPACTACIÓN (SUMINISTRO, EXTENDIDO, NIVELACIÓN Y COMPACTACIÓN CON EQUIPO MECÁNICO)': H=965.0, I=14162.699999999997 (M3), variacion relativa 1368%. Impacto 2.348.873.855.
- **Recomendacion**: Solicitar memoria detallada de cantidad y respaldo tecnico. Cruzar con planos as-built.

#### H01-022 - Variacion relativa alta (fila 490)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 490
- **Impacto**: $-1.883.363.119
- **Descripcion**: Item 6.007 '6 DUCTOS D=6" + 2 DUCTOS D=3" PVC TDP. SUMINISTRO E INSTALACION. (NO INCLUYE RELLENOS).': H=3399.0, I=7.6 (ML), variacion relativa 100%. Impacto -1.883.363.119.
- **Recomendacion**: Solicitar memoria detallada de cantidad y respaldo tecnico. Cruzar con planos as-built.

#### H01-037 - NP de alto valor (fila 479)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 479
- **Impacto**: $1.879.745.340
- **Descripcion**: NP NP-133 'CONTRATO 1752-2021 - BOX CULVERT PREFABRICADO TIPO 1, Ancho Int: 1.875 m, Alto Int: 1.80m, Longitud: 1.00m, Espesores de muros y placa fondo : 0,30m, Espesor de placa superior 0,25 m, Cuantía : 206,5 Kg/m3 - MEZCLA SECA (Incluye transporte, descargue e instalación. No incluye excavación, mejoramiento de subrasante, solado de limpieza ni entibado)' incorpora cantidad 110.0 UN por 1.879.745.340.
- **Recomendacion**: Revisar aprobacion IDU del NP, analisis de precio unitario y sustento tecnico. Verificar que no exista un item contractual equivalente.

#### H01-023 - Variacion relativa alta (fila 24)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 24
- **Impacto**: $-1.811.267.958
- **Descripcion**: Item 1.012 'BASE GRANULAR CLASE A (BG_A) (SUMINISTRO, EXTENDIDO, NIVELACIÓN, HUMEDECIMIENTO Y COMPACTACIÓN CON VIBROCOMPACTADOR)': H=7718.0, I=0.0 (M3), variacion relativa 100%. Impacto -1.811.267.958.
- **Recomendacion**: Solicitar memoria detallada de cantidad y respaldo tecnico. Cruzar con planos as-built.

#### H01-031 - Item contractual eliminado (fila 24)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 24
- **Impacto**: $-1.811.267.958
- **Descripcion**: Item 1.012 'BASE GRANULAR CLASE A (BG_A) (SUMINISTRO, EXTENDIDO, NIVELACIÓN, HUMEDECIMIENTO Y COMPACTACIÓN CON VIBROCOMPACTADOR)' pasa de 7718.0 a 0 (M3). Reduccion -1.811.267.958.
- **Recomendacion**: Confirmar que la actividad efectivamente no se ejecutara o se reemplaza por otra. Si se reemplaza, aparear con NP correspondiente.

#### H01-016 - Variacion capitulo 6. REDES SECAS: 1.613.831.550

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: capitulo
- **Impacto**: $1.613.831.550
- **Descripcion**: 6. REDES SECAS: valor inicial 4.363.449.811 -> final 5.977.281.361. Balance mayores/menores -304.299.972 + incorporacion NP 1.918.131.522.
- **Recomendacion**: Revisar composicion del capitulo, especialmente aumentos que se apoyen mayormente en NPs.

#### H01-006 - Salto extremo de cantidad (I/H = 135.6897x) - fila 85

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 85
- **Impacto**: $1.542.541.484
- **Descripcion**: Item 3.039 'ANDEN CONCRETO GRAVA COMÚN DE 3000 PSI (210 KG/CM2) PREMEZCLADO E=0.10M (INCLUYE SUMINISTRO, FORMALETEO, FUNDIDA Y CURADO)' paso de 114.0 a 15468.629999999994 M2. Impacto 1.542.541.484.
- **Recomendacion**: Pedir memoria de cantidades actualizada por CIV y validar con actas de campo/planos. Verificar que no se trate de reasignacion desde otro item.

#### H01-024 - Variacion relativa alta (fila 85)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 85
- **Impacto**: $1.542.541.484
- **Descripcion**: Item 3.039 'ANDEN CONCRETO GRAVA COMÚN DE 3000 PSI (210 KG/CM2) PREMEZCLADO E=0.10M (INCLUYE SUMINISTRO, FORMALETEO, FUNDIDA Y CURADO)': H=114.0, I=15468.629999999994 (M2), variacion relativa 13469%. Impacto 1.542.541.484.
- **Recomendacion**: Solicitar memoria detallada de cantidad y respaldo tecnico. Cruzar con planos as-built.

#### H01-038 - NP de alto valor (fila 87)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 87
- **Impacto**: $1.107.150.225
- **Descripcion**: NP NP-16 'ESTAMPADO PARA CONCRETO MR DE POMPEYANOS, ACCESOS VEHICULARES A PREDIOS Y VÍAS (ACABADO Y CURADO, SUMINISTRO Y MANO DE OBRA. INCLUYE JUEGO DE MOLDES, COLOR ENDURECEDOR DE CUARZO, DESMOLDANTE EN POLVO COLOR, SELLADOR ACRÍLICO TRANSPARENTE SEMILUSTRE)' incorpora cantidad 18100.45 M2 por 1.107.150.225.
- **Recomendacion**: Revisar aprobacion IDU del NP, analisis de precio unitario y sustento tecnico. Verificar que no exista un item contractual equivalente.

#### H01-025 - Variacion relativa alta (fila 281)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 281
- **Impacto**: $-1.059.297.570
- **Descripcion**: Item 5.053 'TUBERIA CONCRETO ALTA RESISTENCIA D= 12" (INCLUYE SUMINISTRO, INSTALACIÓN Y MORTERO 2000 PSI PARA RECUBRIMIENTO DE JUNTA).': H=1945.0, I=0.0 (ML), variacion relativa 100%. Impacto -1.059.297.570.
- **Recomendacion**: Solicitar memoria detallada de cantidad y respaldo tecnico. Cruzar con planos as-built.

#### H01-032 - Item contractual eliminado (fila 281)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 281
- **Impacto**: $-1.059.297.570
- **Descripcion**: Item 5.053 'TUBERIA CONCRETO ALTA RESISTENCIA D= 12" (INCLUYE SUMINISTRO, INSTALACIÓN Y MORTERO 2000 PSI PARA RECUBRIMIENTO DE JUNTA).' pasa de 1945.0 a 0 (ML). Reduccion -1.059.297.570.
- **Recomendacion**: Confirmar que la actividad efectivamente no se ejecutara o se reemplaza por otra. Si se reemplaza, aparear con NP correspondiente.

#### H01-026 - Variacion relativa alta (fila 295)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 295
- **Impacto**: $-840.308.079
- **Descripcion**: Item 5.067 'SUMIDERO LATERAL SL-250A, H=1.7M (FUNDIDO EN SITIO, CONCRETO PREMEZCLADO. INCL. SUMIN, FORM, REF. Y CONSTR. INCL. TAPA)': H=123.0, I=0.0 (UN), variacion relativa 100%. Impacto -840.308.079.
- **Recomendacion**: Solicitar memoria detallada de cantidad y respaldo tecnico. Cruzar con planos as-built.

#### H01-033 - Item contractual eliminado (fila 295)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 295
- **Impacto**: $-840.308.079
- **Descripcion**: Item 5.067 'SUMIDERO LATERAL SL-250A, H=1.7M (FUNDIDO EN SITIO, CONCRETO PREMEZCLADO. INCL. SUMIN, FORM, REF. Y CONSTR. INCL. TAPA)' pasa de 123.0 a 0 (UN). Reduccion -840.308.079.
- **Recomendacion**: Confirmar que la actividad efectivamente no se ejecutara o se reemplaza por otra. Si se reemplaza, aparear con NP correspondiente.

#### H01-039 - NP de alto valor (fila 547)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 547
- **Impacto**: $778.412.250
- **Descripcion**: NP NP-03 'CONSTRUCCION DE CAJA DE INSPECCION DOBLE PARA CANALIZACION DE M.T. Y B.T. TIPO CS 276 (Norma 2018) (Incluye concreto de base, muro de espesor 0.25m, pañete, recebo común, escalera de gato, concreto para viga de soporte de marco y marco y tapa. No incluye tubería). Medidas Externas: 1.69 x 1.99m. Medidas Internas: 1.19 x 1.49m. Altura total: 1.85m' incorpora cantidad 165.0 UN por 778.412.250.
- **Recomendacion**: Revisar aprobacion IDU del NP, analisis de precio unitario y sustento tecnico. Verificar que no exista un item contractual equivalente.

#### H01-001 - Posible reemplazo contractual->NP (filas 24 -> 30)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 24 / 30
- **Impacto**: $707.253.958
- **Descripcion**: Item contractual '1.012 - BASE GRANULAR CLASE A (BG_A) (SUMINISTRO, EXTENDIDO, NIVELACIÓN, HUMEDECIMIENTO Y COMPACTACIÓN CON VIBROCOMPACTADOR)' (delta -1.811.267.958) parece reemplazado por NP 'NP-124 - BASE GRANULAR CLASE A (BG_A) CON RECICLADO DE CONCRETO HIDRAULICO (SUMINISTRO, EXTENDIDO, NIVELACIÓN, HUMEDECIMIENTO Y COMPACTACIÓN CON VIBROCOMPACTADOR)' (delta 2.518.521.916). Sobrecosto neto 707.253.958.
- **Recomendacion**: Solicitar al contratista justificacion tecnica del cambio, precio del NP con analisis unitario, y evidenciar por que no aplica el item contractual del pliego. Comparar con VU visor IDU.

#### H01-002 - Posible reemplazo contractual->NP (filas 33 -> 39)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 33 / 39
- **Impacto**: $684.670.659
- **Descripcion**: Item contractual '2.002 - MEZCLA ASFÁLTICA DENSA EN CALIENTE MD12 CON CEMENTO ASFÁLTICO 60-70 (SUMINISTRO, EXTENDIDO, NIVELACIÓN Y COMPACTACIÓN MECANICA CON VIBROCOMPACTADOR Y COMPACTADOR DE LLANTAS)' (delta -2.584.929.953) parece reemplazado por NP 'NP-123 - MEZCLA ASFÁLTICA EN CALIENTE DENSA MD19 CON CEMENTO ASFÁLTICO CA 14 (Suministro, Extendido, Nivelación y Compactación
mecánica con vibrocompactador y compactador de llantas)' (delta 3.269.600.612). Sobrecosto neto 684.670.659.
- **Recomendacion**: Solicitar al contratista justificacion tecnica del cambio, precio del NP con analisis unitario, y evidenciar por que no aplica el item contractual del pliego. Comparar con VU visor IDU.

#### H01-027 - Variacion relativa alta (fila 21)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 21
- **Impacto**: $-671.669.280
- **Descripcion**: Item 1.009 'ESTABILIZACIÓN CON RCD. INCLUYE TRASIEGO INTERNO, NIVELACIÓN Y COMPACTACIÓN.': H=8688.0, I=0.0 (M3), variacion relativa 100%. Impacto -671.669.280.
- **Recomendacion**: Solicitar memoria detallada de cantidad y respaldo tecnico. Cruzar con planos as-built.

#### H01-034 - Item contractual eliminado (fila 21)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 21
- **Impacto**: $-671.669.280
- **Descripcion**: Item 1.009 'ESTABILIZACIÓN CON RCD. INCLUYE TRASIEGO INTERNO, NIVELACIÓN Y COMPACTACIÓN.' pasa de 8688.0 a 0 (M3). Reduccion -671.669.280.
- **Recomendacion**: Confirmar que la actividad efectivamente no se ejecutara o se reemplaza por otra. Si se reemplaza, aparear con NP correspondiente.

#### H01-028 - Variacion relativa alta (fila 68)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 68
- **Impacto**: $-661.011.828
- **Descripcion**: Item 3.022 'LOSETA DE CONCRETO A20 TR. LIVIANO 20X20X6CM COLOR GRIS (SUMINISTRO E INSTALACIÓN. INCLUYE BASE 4CM ARENA NIVELACIÓN Y ARENA DE SELLO)': H=5631.0, I=0.0 (M2), variacion relativa 100%. Impacto -661.011.828.
- **Recomendacion**: Solicitar memoria detallada de cantidad y respaldo tecnico. Cruzar con planos as-built.

#### H01-011 - Salto extremo de cantidad (I/H = 12.2067x) - fila 27

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 27
- **Impacto**: $660.384.913
- **Descripcion**: Item 1.015 'SUBBASE GRANULAR CLASE C (SBG_C) (SUMINISTRO, EXTENDIDO, NIVELACIÓN, HUMEDECIMIENTO Y COMPACTACIÓN CON VIBROCOMPACTADOR)' paso de 288.0 a 3515.53 M3. Impacto 660.384.913.
- **Recomendacion**: Pedir memoria de cantidades actualizada por CIV y validar con actas de campo/planos. Verificar que no se trate de reasignacion desde otro item.

#### H01-029 - Variacion relativa alta (fila 27)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 27
- **Impacto**: $660.384.913
- **Descripcion**: Item 1.015 'SUBBASE GRANULAR CLASE C (SBG_C) (SUMINISTRO, EXTENDIDO, NIVELACIÓN, HUMEDECIMIENTO Y COMPACTACIÓN CON VIBROCOMPACTADOR)': H=288.0, I=3515.53 (M3), variacion relativa 1121%. Impacto 660.384.913.
- **Recomendacion**: Solicitar memoria detallada de cantidad y respaldo tecnico. Cruzar con planos as-built.

#### H01-017 - Variacion capitulo 3. ESPACIO PÚBLICO: -515.309.947

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: capitulo
- **Impacto**: $-515.309.947
- **Descripcion**: 3. ESPACIO PÚBLICO: valor inicial 7.252.761.854 -> final 6.737.451.907. Balance mayores/menores -1.678.948.466 + incorporacion NP 1.163.638.519.
- **Recomendacion**: Revisar composicion del capitulo, especialmente aumentos que se apoyen mayormente en NPs.

### MEDIA (7)

#### H01-007 - Salto extremo de cantidad (I/H = 39.9949x) - fila 73

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 73
- **Impacto**: $413.740.072
- **Descripcion**: Item 3.027 'SARDINEL FUNDIDO EN SITIO EN CONCRETO PREMEZCLADO DE 3000PSI. SUMINISTRO Y CONSTRUCCION. (GRAVA COMÚN) E=0.20M H=0.35M (INCLUYE FORMALETA METÁLICA, ACERO DE REFUERZO Y ALAMBRE NEGRO).' paso de 141.0 a 5639.28 ML. Impacto 413.740.072.
- **Recomendacion**: Pedir memoria de cantidades actualizada por CIV y validar con actas de campo/planos. Verificar que no se trate de reasignacion desde otro item.

#### H01-018 - Variacion capitulo 7. DESVÍOS: -326.577.225

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: capitulo
- **Impacto**: $-326.577.225
- **Descripcion**: 7. DESVÍOS: valor inicial 326.577.225 -> final 0. Balance mayores/menores -326.577.225 + incorporacion NP 0.
- **Recomendacion**: Revisar composicion del capitulo, especialmente aumentos que se apoyen mayormente en NPs.

#### H01-003 - Posible reemplazo contractual->NP (filas 489 -> 551)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 489 / 551
- **Impacto**: $134.653.937
- **Descripcion**: Item contractual '6.006 - 2 DUCTOS D=3" PVC-EB (INCLUYE SUMINISTRO E INSTALACIÓN. NO INCLUYE RELLENOS). NORMA CS207.' (delta -167.940.640) parece reemplazado por NP 'NP-07 - 6 DUCTOS D=6" PVC-TDP (INCLUYE SUMINISTRO E INSTALACIÓN. NO INCLUYE RELLENOS). NORMA CS212.' (delta 302.594.577). Sobrecosto neto 134.653.937.
- **Recomendacion**: Solicitar al contratista justificacion tecnica del cambio, precio del NP con analisis unitario, y evidenciar por que no aplica el item contractual del pliego. Comparar con VU visor IDU.

#### H01-004 - Posible reemplazo contractual->NP (filas 272 -> 463)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 272 / 463
- **Impacto**: $97.188.465
- **Descripcion**: Item contractual '5.044 - TUBERIA PVC U.M. EXT/INT LISO NORMA NTC 5070 D=39" (INCLUYE SUMINISTRO E INSTALACIÓN)' (delta -43.812.034) parece reemplazado por NP 'NP-17 - TUBERIA PVC U.M. EXT CORRUGADO/INT LISO U.M. NORMA NTC 3722-1 D=24" (INCLUYE SUMINISTRO E INSTALACIÓN)' (delta 141.000.499). Sobrecosto neto 97.188.465.
- **Recomendacion**: Solicitar al contratista justificacion tecnica del cambio, precio del NP con analisis unitario, y evidenciar por que no aplica el item contractual del pliego. Comparar con VU visor IDU.

#### H01-012 - Salto extremo de cantidad (I/H = 11.9861x) - fila 48

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 48
- **Impacto**: $68.652.015
- **Descripcion**: Item 3.006 'ESTABILIZACIÓN DE SUBRASANTE CON RAJÓN (SUMINISTRO, EXTENDIDO, NIVELACIÓN Y COMPACTACIÓN MANUAL)' paso de 44.0 a 527.39 M3. Impacto 68.652.015.
- **Recomendacion**: Pedir memoria de cantidades actualizada por CIV y validar con actas de campo/planos. Verificar que no se trate de reasignacion desde otro item.

#### H01-009 - Salto extremo de cantidad (I/H = 28.5588x) - fila 35

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 35
- **Impacto**: $51.924.500
- **Descripcion**: Item 2.004 'CORTE DE PAVIMENTO - INCLUYE EQUIPO: CORTADORA DE CONCRETO INCLUYE OPERARIO Y COMBUSTIBLE. INCLUYE DISCO DIAMANTADO ASFALTO-CONCRETO 350 MM, AGUA Y MANO DE OBRA' paso de 597.0 a 17049.629999999997 ML. Impacto 51.924.500.
- **Recomendacion**: Pedir memoria de cantidades actualizada por CIV y validar con actas de campo/planos. Verificar que no se trate de reasignacion desde otro item.

#### H01-040 - Discrepancias formulas O = (I-H) x L

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 34
- **Impacto**: $0
- **Descripcion**: 1 renglones donde el balance mayores/menores O no coincide con (I-H)xL (>$10 dif).
- **Recomendacion**: Solicitar aclaracion de que precio se uso para el balance de mayores/menores (VU visor vs VU contractual).

### BAJA (3)

#### H01-005 - Posible reemplazo contractual->NP (filas 269 -> 464)

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 269 / 464
- **Impacto**: $34.474.692
- **Descripcion**: Item contractual '5.041 - TUBERIA PVC U.M. EXT/INT LISO NORMA NTC 5070 D=27" (INCLUYE SUMINISTRO E INSTALACIÓN)' (delta -88.567.080) parece reemplazado por NP 'NP-18 - TUBERIA PVC U.M. EXT CORRUGADO/INT LISO U.M. NORMA NTC 3722-1 D=27" (INCLUYE SUMINISTRO E INSTALACIÓN)' (delta 123.041.772). Sobrecosto neto 34.474.692.
- **Recomendacion**: Solicitar al contratista justificacion tecnica del cambio, precio del NP con analisis unitario, y evidenciar por que no aplica el item contractual del pliego. Comparar con VU visor IDU.

#### H01-008 - Salto extremo de cantidad (I/H = 37.0x) - fila 129

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: 129
- **Impacto**: $17.856.000
- **Descripcion**: Item 5.007 'CODO HD 22.5° EXTREMO LISO PARA PVC D=6" (SUMINISTRO E INSTALACIÓN)' paso de 1.0 a 37.0 UN. Impacto 17.856.000.
- **Recomendacion**: Pedir memoria de cantidades actualizada por CIV y validar con actas de campo/planos. Verificar que no se trate de reasignacion desde otro item.

#### H01-019 - Variacion capitulo 4. SEÑALIZACIÓN Y DEMARCACIÓN: 0

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: capitulo
- **Impacto**: $0
- **Descripcion**: 4. SEÑALIZACIÓN Y DEMARCACIÓN: valor inicial 1.198.662.405 -> final 1.198.662.405. Balance mayores/menores 0 + incorporacion NP 0.
- **Recomendacion**: Revisar composicion del capitulo, especialmente aumentos que se apoyen mayormente en NPs.

### INFO (1)

#### H01-041 - Conciliacion global de obras OK

- **Hoja**: PRESUPUESTO TODOS LOS CIV 84 NP  **Fila**: totales
- **Impacto**: $0
- **Descripcion**: Inicial 44.303.294.799, final 58.196.933.800, delta 13.893.639.001.
- **Recomendacion**: Sin observaciones.

## Top 30 aumentos (por delta valor)

| Fila | Cap | Cod IDU | Item | Descripcion | Und | H | I | Delta cant | Delta valor | Estado |
|---:|---|---|---|---|---|---:|---:|---:|---:|---|
| 39 | 2. PAVIMENTOS | 8618 | NP-123 | MEZCLA ASFÁLTICA EN CALIENTE DENSA MD19 CON CEMENTO ASFÁLTIC | M3 | 0.0 | 2089.45 | 2089.45 | $3.269.600.612 | np_nuevo |
| 30 | 1. PRELIMINARES | 4744 | NP-124 | BASE GRANULAR CLASE A (BG_A) CON RECICLADO DE CONCRETO HIDRA | M3 | 0.0 | 10476.554999999998 | 10476.55 | $2.518.521.916 | np_nuevo |
| 34 | 2. PAVIMENTOS | 7785 | 2.003 | LOSA DE CONCRETO MR45 (SUMINISTRO, FORMALETEADO, COLOCACIÓN, | M3 | 8276.0 | 9851.224192000001 | 1575.22 | $2.351.966.086 | aumento |
| 20 | 1. PRELIMINARES | 6016 | 1.008 | ESTABILIZACIÓN DE SUBRASANTE CON RAJÓN, INCLUYE EQUIPO DE CO | M3 | 965.0 | 14162.699999999997 | 13197.70 | $2.348.873.855 | aumento |
| 531 | 6. REDES SECAS | 5182 | 6.007 | 6 DUCTOS D=6" + 2 DUCTOS D=3" PVC TDP. SUMINISTRO E INSTALAC | ML | 0.0 | 3912.249999999999 | 3912.25 | $2.172.609.354 | nuevo_contractual |
| 479 | 5. REDES HIDROSANITARIAS | N/A | NP-133 | CONTRATO 1752-2021 - BOX CULVERT PREFABRICADO TIPO 1, Ancho  | UN | 0.0 | 110.0 | 110.00 | $1.879.745.340 | np_nuevo |
| 85 | 3. ESPACIO PÚBLICO | 3425 | 3.039 | ANDEN CONCRETO GRAVA COMÚN DE 3000 PSI (210 KG/CM2) PREMEZCL | M2 | 114.0 | 15468.629999999994 | 15354.63 | $1.542.541.484 | aumento |
| 399 | 5. REDES HIDROSANITARIAS | 3895 | 5.067 | SUMIDERO LATERAL SL-250A, H=1.7M (FUNDIDO EN SITIO, CONCRETO | UN | 0.0 | 194.0 | 194.00 | $1.325.363.962 | nuevo_contractual |
| 317 | 5. REDES HIDROSANITARIAS | 8643 | 5.037 | Proyecto: factibilidad, estudios y diseños de aceras, ciclor | M2 | 0.0 | 18442.509999999995 | 18442.51 | $1.226.390.030 | nuevo_contractual |
| 353 | 5. REDES HIDROSANITARIAS | 4754 | 3.012 | SUBBASE GRANULAR CLASE B (SBG_B) CON RECICLADO DE CONCRETO H | M3 | 0.0 | 5904.465176464074 | 5904.47 | $1.205.408.375 | nuevo_contractual |
| 369 | 5. REDES HIDROSANITARIAS | 8643 | 5.037 | Proyecto: factibilidad, estudios y diseños de aceras, ciclor | M2 | 0.0 | 17457.17 | 17457.17 | $1.160.866.891 | nuevo_contractual |
| 87 | 3. ESPACIO PÚBLICO | 10271 | NP-16 | ESTAMPADO PARA CONCRETO MR DE POMPEYANOS, ACCESOS VEHICULARE | M2 | 0.0 | 18100.45 | 18100.45 | $1.107.150.225 | np_nuevo |
| 405 | 5. REDES HIDROSANITARIAS | 4754 | 3.012 | SUBBASE GRANULAR CLASE B (SBG_B) CON RECICLADO DE CONCRETO H | M3 | 0.0 | 3917.669999999999 | 3917.67 | $799.800.166 | nuevo_contractual |
| 547 | 6. REDES SECAS | 9032 | NP-03 | CONSTRUCCION DE CAJA DE INSPECCION DOBLE PARA CANALIZACION D | UN | 0.0 | 165.0 | 165.00 | $778.412.250 | np_nuevo |
| 14 | 1. PRELIMINARES | 3017 | 1.006 | TRANSPORTE Y DISPOSICIÓN FINAL DE ESCOMBROS EN SITIO AUTORIZ | M3 | 38572.0 | 52468.569999999985 | 13896.57 | $766.340.249 | aumento |
| 318 | 5. REDES HIDROSANITARIAS | 3017 | 5.038 | TRANSPORTE Y DISPOSICIÓN FINAL DE ESCOMBROS EN SITIO AUTORIZ | M3 | 0.0 | 12747.180000000002 | 12747.18 | $702.955.988 | nuevo_contractual |
| 27 | 1. PRELIMINARES | 4159 | 1.015 | SUBBASE GRANULAR CLASE C (SBG_C) (SUMINISTRO, EXTENDIDO, NIV | M3 | 288.0 | 3515.53 | 3227.53 | $660.384.913 | aumento |
| 370 | 5. REDES HIDROSANITARIAS | 3017 | 5.038 | TRANSPORTE Y DISPOSICIÓN FINAL DE ESCOMBROS EN SITIO AUTORIZ | M3 | 0.0 | 10058.77 | 10058.77 | $554.700.930 | nuevo_contractual |
| 38 | 2. PAVIMENTOS | 4032 | 3.010 | GEOTEXTIL T, RESIST. ULTIMA (TIRA ANCHA)=40 KN/M PARA SEPARA | M2 | 0.0 | 36885.9 | 36885.90 | $440.196.331 | nuevo_contractual |
| 73 | 3. ESPACIO PÚBLICO | 5181 | 3.027 | SARDINEL FUNDIDO EN SITIO EN CONCRETO PREMEZCLADO DE 3000PSI | ML | 141.0 | 5639.28 | 5498.28 | $413.740.072 | aumento |
| 47 | 3. ESPACIO PÚBLICO | 3017 | 1.006 | TRANSPORTE Y DISPOSICIÓN FINAL DE ESCOMBROS EN SITIO AUTORIZ | M3 | 0.0 | 6026.9400000000005 | 6026.94 | $332.361.633 | nuevo_contractual |
| 426 | 5. REDES HIDROSANITARIAS | 8643 | 5.037 | Proyecto: factibilidad, estudios y diseños de aceras, ciclor | M2 | 0.0 | 4973.43 | 4973.43 | $330.723.148 | nuevo_contractual |
| 544 | 6. REDES SECAS | 4907 | 3.013 | SUBBASE GRANULAR PEATONAL SBG_PEA. SUMINISTRO, EXTENDIDO MAN | M3 | 0.0 | 1635.21 | 1635.21 | $327.710.801 | nuevo_contractual |
| 561 | 6. REDES SECAS | N/A | NP-122 | CONSTRUCCION DE CAJA DE INSPECCION DOBLE PARA CANALIZACION D | UN | 0.0 | 73.0 | 73.00 | $323.248.307 | np_nuevo |
| 536 | 6. REDES SECAS | 3017 | 6.012 | TRANSPORTE Y DISPOSICIÓN FINAL DE ESCOMBROS EN SITIO AUTORIZ | M3 | 0.0 | 5842.25 | 5842.25 | $322.176.719 | nuevo_contractual |
| 465 | 5. REDES HIDROSANITARIAS | 7435 | NP-19 | TUBERIA PVC U.M. EXT CORRUGADO/INT LISO U.M. NORMA NTC 3722- | ML | 0.0 | 122.00999999999999 | 122.01 | $302.936.555 | np_nuevo |
| 551 | 6. REDES SECAS | 3408 | NP-07 | 6 DUCTOS D=6" PVC-TDP (INCLUYE SUMINISTRO E INSTALACIÓN. NO  | ML | 0.0 | 619.86 | 619.86 | $302.594.577 | np_nuevo |
| 418 | 5. REDES HIDROSANITARIAS | 4892 | NP-71 | TUBERIA CONCRETO ALTA RESISTENCIA D= 10" (INCLUYE SUMINISTRO | ML | 0.0 | 599.07 | 599.07 | $274.675.991 | np_nuevo |
| 535 | 6. REDES SECAS | 3009 | 6.011 | EXCAVACION MANUAL PARA REDES PROFUNDIDAD 0M - 2M (INCLUYE CA | M3 | 0.0 | 4494.0 | 4494.00 | $252.063.966 | nuevo_contractual |
| 325 | 5. REDES HIDROSANITARIAS | 3043 | 5.045 | TUBERIA PVC U.M. EXT CORRUGADO/INT LISO U.M. NORMA NTC 3722- | ML | 0.0 | 2304.44 | 2304.44 | $247.840.218 | nuevo_contractual |

## Top 30 disminuciones (por delta valor)

| Fila | Cap | Cod IDU | Item | Descripcion | Und | H | I | Delta cant | Delta valor | Estado |
|---:|---|---|---|---|---|---:|---:|---:|---:|---|
| 33 | 2. PAVIMENTOS | 6313 | 2.002 | MEZCLA ASFÁLTICA DENSA EN CALIENTE MD12 CON CEMENTO ASFÁLTIC | M3 | 1721.0 | 0.0 | -1721.00 | $-2.584.929.953 | eliminado |
| 490 | 6. REDES SECAS | 5182 | 6.007 | 6 DUCTOS D=6" + 2 DUCTOS D=3" PVC TDP. SUMINISTRO E INSTALAC | ML | 3399.0 | 7.6 | -3391.40 | $-1.883.363.119 | disminucion |
| 24 | 1. PRELIMINARES | 4158 | 1.012 | BASE GRANULAR CLASE A (BG_A) (SUMINISTRO, EXTENDIDO, NIVELAC | M3 | 7718.0 | 0.0 | -7718.00 | $-1.811.267.958 | eliminado |
| 281 | 5. REDES HIDROSANITARIAS | 4896 | 5.053 | TUBERIA CONCRETO ALTA RESISTENCIA D= 12" (INCLUYE SUMINISTRO | ML | 1945.0 | 0.0 | -1945.00 | $-1.059.297.570 | eliminado |
| 295 | 5. REDES HIDROSANITARIAS | 3895 | 5.067 | SUMIDERO LATERAL SL-250A, H=1.7M (FUNDIDO EN SITIO, CONCRETO | UN | 123.0 | 0.0 | -123.00 | $-840.308.079 | eliminado |
| 21 | 1. PRELIMINARES | 6486 | 1.009 | ESTABILIZACIÓN CON RCD. INCLUYE TRASIEGO INTERNO, NIVELACIÓN | M3 | 8688.0 | 0.0 | -8688.00 | $-671.669.280 | eliminado |
| 68 | 3. ESPACIO PÚBLICO | 8212 | 3.022 | LOSETA DE CONCRETO A20 TR. LIVIANO 20X20X6CM COLOR GRIS (SUM | M2 | 5631.0 | 0.0 | -5631.00 | $-661.011.828 | eliminado |
| 283 | 5. REDES HIDROSANITARIAS | 4792 | 5.055 | RELLENO EN RECEBO COMUN (SUMINISTRO E INSTALACIÓN EXTENDIDO  | M3 | 5348.0 | 0.0 | -5348.00 | $-643.107.696 | eliminado |
| 271 | 5. REDES HIDROSANITARIAS | 3923 | 5.043 | TUBERIA PVC U.M. EXT/INT LISO NORMA NTC 5070 D=36" (INCLUYE  | ML | 257.0 | 0.0 | -257.00 | $-605.539.802 | eliminado |
| 268 | 5. REDES HIDROSANITARIAS | 3919 | 5.040 | TUBERIA PVC U.M. EXT/INT LISO NORMA NTC 5070 D=24" (INCLUYE  | ML | 639.0 | 0.0 | -639.00 | $-564.421.032 | eliminado |
| 280 | 5. REDES HIDROSANITARIAS | 7447 | 5.052 | TUBERIA PVC U.M. EXT CORRUGADO/INT LISO U.M. NORMA NTC 3722- | ML | 120.0 | 0.0 | -120.00 | $-557.919.840 | eliminado |
| 28 | 1. PRELIMINARES | 4748 | 1.016 | SUBBASE GRANULAR CLASE C (SBG_C) CON RECICLADO DE CONCRETO H | M3 | 2594.0 | 0.0 | -2594.00 | $-495.334.676 | eliminado |
| 293 | 5. REDES HIDROSANITARIAS | 4553 | 5.065 | POZO DE INSPECCION D=1.7 M (INCL. SUMINISTRO E INSTALACION). | UN | 99.0 | 0.0 | -99.00 | $-464.985.675 | eliminado |
| 66 | 3. ESPACIO PÚBLICO | 8452 | 3.020 | DEMARCACIÓN DE FRANJA TIPO A55 Y A56 MEDIANTE LA APLICACIÓN  | ML | 1317.0 | 0.0 | -1317.00 | $-453.743.376 | eliminado |
| 62 | 3. ESPACIO PÚBLICO | 3027 | 3.016 | SARDINEL TIPO A10 (SUMINISTRO E INSTALACIÓN. INCLUYE 3CM MOR | ML | 4597.0 | 0.0 | -4597.00 | $-446.538.789 | eliminado |
| 285 | 5. REDES HIDROSANITARIAS | 7876 | 5.057 | CÁRCAMO DE PROTECCION EN TUBERÍA Ø 12" NORMA EAAB NS-090 ver | ML | 247.0 | 0.0 | -247.00 | $-439.644.192 | eliminado |
| 626 | 6. REDES SECAS | 3380 | 6.031 | 4 DUCTOS D=4" PVC-TDP (INCLUYE SUMINISTRO E INSTALACIÓN. NO  | ML | 2870.0 | 6.0 | -2864.00 | $-420.761.696 | disminucion |
| 70 | 3. ESPACIO PÚBLICO | 3210 | 3.024 | BORDILLO PREFABRICADO A80 (SUMINISTRO E INSTALACIÓN. INCLUYE | ML | 4958.0 | 0.0 | -4958.00 | $-413.968.210 | eliminado |
| 22 | 1. PRELIMINARES | 4030 | 1.010 | GEOTEXTIL T, RESIST. ULTIMA (TIRA ANCHA)=30 KN/M PARA SEPARA | M2 | 36297.0 | 0.0 | -36297.00 | $-401.844.087 | eliminado |
| 265 | 5. REDES HIDROSANITARIAS | 8643 | 5.037 | Proyecto: factibilidad, estudios y diseños de aceras, ciclor | M2 | 5801.0 | 0.0 | -5801.00 | $-385.754.898 | eliminado |
| 499 | 6. REDES SECAS | 4107 | 6.016 | CAJA DE INSPECCIÓN DOBLE PARA CANALIZACIÓN NORMA CODENSA CS  | UN | 167.0 | 0.0 | -167.00 | $-349.626.190 | eliminado |
| 69 | 3. ESPACIO PÚBLICO | 8464 | 3.023 | BORDILLO EN CONCRETO GRAVA COMÚN 1" 2000 PSI, FUNDIDO EN SIT | ML | 4956.0 | 0.0 | -4956.00 | $-348.258.120 | eliminado |
| 284 | 5. REDES HIDROSANITARIAS | 4291 | 5.056 | CARCAMO PROTECCIÓN DE TUBERÍA Ø 8" NORMA EAAB NS-090 . 3V.2 | ML | 454.0 | 0.0 | -454.00 | $-337.708.354 | eliminado |
| 676 | 7. DESVÍOS | 6184 | 7.001 | MANTENIMIENTO RUTINARIO DE CALZADA EN PAVIMENTO FLEXIBLE. IN | M2 | 13481.0 | 0.0 | -13481.00 | $-326.577.225 | eliminado |
| 65 | 3. ESPACIO PÚBLICO | 4856 | 3.019 | PISOS EN LOSETA PREFABRICADA A55 TÁCTIL ALERTA O A56 GUIA 40 | M2 | 2201.0 | 0.0 | -2201.00 | $-306.079.864 | eliminado |
| 270 | 5. REDES HIDROSANITARIAS | 3922 | 5.042 | TUBERIA PVC U.M. EXT/INT LISO NORMA NTC 5070 D=33" (INCLUYE  | ML | 172.0 | 0.0 | -172.00 | $-303.925.032 | eliminado |
| 289 | 5. REDES HIDROSANITARIAS | 4297 | 5.061 | CARCAMO DE PROTECCIÓN DE TUBERÍA Ø 24" NORMA EAAB NS-090 V.  | ML | 214.0 | 0.0 | -214.00 | $-291.444.246 | eliminado |
| 266 | 5. REDES HIDROSANITARIAS | 3017 | 5.038 | TRANSPORTE Y DISPOSICIÓN FINAL DE ESCOMBROS EN SITIO AUTORIZ | M3 | 6103.0 | 912.5999999999999 | -5190.40 | $-286.229.798 | disminucion |
| 86 | 3. ESPACIO PÚBLICO | 8476 | 3.040 | CONTENEDOR DE RAICES DE 2,50M X 2,50M H=1,40 M. (INCLUYE CON | UN | 106.0 | 0.0 | -106.00 | $-267.643.534 | eliminado |
| 52 | 3. ESPACIO PÚBLICO | 4032 | 3.010 | GEOTEXTIL T, RESIST. ULTIMA (TIRA ANCHA)=40 KN/M PARA SEPARA | M2 | 20379.0 | 0.0 | -20379.00 | $-243.202.986 | eliminado |

## Variacion relativa alta (|Delta cant / H| > 50%  y  |Delta valor| > $50M)

| Fila | Cod IDU | Item | Descripcion | H | I | % var | Delta valor |
|---:|---|---|---|---:|---:|---:|---:|
| 33 | 6313 | 2.002 | MEZCLA ASFÁLTICA DENSA EN CALIENTE MD12 CON CEMENTO ASFÁLTIC | 1721.0 | 0.0 | 100% | $-2.584.929.953 |
| 20 | 6016 | 1.008 | ESTABILIZACIÓN DE SUBRASANTE CON RAJÓN, INCLUYE EQUIPO DE CO | 965.0 | 14162.699999999997 | 1368% | $2.348.873.855 |
| 490 | 5182 | 6.007 | 6 DUCTOS D=6" + 2 DUCTOS D=3" PVC TDP. SUMINISTRO E INSTALAC | 3399.0 | 7.6 | 100% | $-1.883.363.119 |
| 24 | 4158 | 1.012 | BASE GRANULAR CLASE A (BG_A) (SUMINISTRO, EXTENDIDO, NIVELAC | 7718.0 | 0.0 | 100% | $-1.811.267.958 |
| 85 | 3425 | 3.039 | ANDEN CONCRETO GRAVA COMÚN DE 3000 PSI (210 KG/CM2) PREMEZCL | 114.0 | 15468.629999999994 | 13469% | $1.542.541.484 |
| 281 | 4896 | 5.053 | TUBERIA CONCRETO ALTA RESISTENCIA D= 12" (INCLUYE SUMINISTRO | 1945.0 | 0.0 | 100% | $-1.059.297.570 |
| 295 | 3895 | 5.067 | SUMIDERO LATERAL SL-250A, H=1.7M (FUNDIDO EN SITIO, CONCRETO | 123.0 | 0.0 | 100% | $-840.308.079 |
| 21 | 6486 | 1.009 | ESTABILIZACIÓN CON RCD. INCLUYE TRASIEGO INTERNO, NIVELACIÓN | 8688.0 | 0.0 | 100% | $-671.669.280 |
| 68 | 8212 | 3.022 | LOSETA DE CONCRETO A20 TR. LIVIANO 20X20X6CM COLOR GRIS (SUM | 5631.0 | 0.0 | 100% | $-661.011.828 |
| 27 | 4159 | 1.015 | SUBBASE GRANULAR CLASE C (SBG_C) (SUMINISTRO, EXTENDIDO, NIV | 288.0 | 3515.53 | 1121% | $660.384.913 |
| 283 | 4792 | 5.055 | RELLENO EN RECEBO COMUN (SUMINISTRO E INSTALACIÓN EXTENDIDO  | 5348.0 | 0.0 | 100% | $-643.107.696 |
| 271 | 3923 | 5.043 | TUBERIA PVC U.M. EXT/INT LISO NORMA NTC 5070 D=36" (INCLUYE  | 257.0 | 0.0 | 100% | $-605.539.802 |
| 268 | 3919 | 5.040 | TUBERIA PVC U.M. EXT/INT LISO NORMA NTC 5070 D=24" (INCLUYE  | 639.0 | 0.0 | 100% | $-564.421.032 |
| 280 | 7447 | 5.052 | TUBERIA PVC U.M. EXT CORRUGADO/INT LISO U.M. NORMA NTC 3722- | 120.0 | 0.0 | 100% | $-557.919.840 |
| 28 | 4748 | 1.016 | SUBBASE GRANULAR CLASE C (SBG_C) CON RECICLADO DE CONCRETO H | 2594.0 | 0.0 | 100% | $-495.334.676 |
| 293 | 4553 | 5.065 | POZO DE INSPECCION D=1.7 M (INCL. SUMINISTRO E INSTALACION). | 99.0 | 0.0 | 100% | $-464.985.675 |
| 66 | 8452 | 3.020 | DEMARCACIÓN DE FRANJA TIPO A55 Y A56 MEDIANTE LA APLICACIÓN  | 1317.0 | 0.0 | 100% | $-453.743.376 |
| 62 | 3027 | 3.016 | SARDINEL TIPO A10 (SUMINISTRO E INSTALACIÓN. INCLUYE 3CM MOR | 4597.0 | 0.0 | 100% | $-446.538.789 |
| 285 | 7876 | 5.057 | CÁRCAMO DE PROTECCION EN TUBERÍA Ø 12" NORMA EAAB NS-090 ver | 247.0 | 0.0 | 100% | $-439.644.192 |
| 626 | 3380 | 6.031 | 4 DUCTOS D=4" PVC-TDP (INCLUYE SUMINISTRO E INSTALACIÓN. NO  | 2870.0 | 6.0 | 100% | $-420.761.696 |
| 70 | 3210 | 3.024 | BORDILLO PREFABRICADO A80 (SUMINISTRO E INSTALACIÓN. INCLUYE | 4958.0 | 0.0 | 100% | $-413.968.210 |
| 73 | 5181 | 3.027 | SARDINEL FUNDIDO EN SITIO EN CONCRETO PREMEZCLADO DE 3000PSI | 141.0 | 5639.28 | 3899% | $413.740.072 |
| 22 | 4030 | 1.010 | GEOTEXTIL T, RESIST. ULTIMA (TIRA ANCHA)=30 KN/M PARA SEPARA | 36297.0 | 0.0 | 100% | $-401.844.087 |
| 265 | 8643 | 5.037 | Proyecto: factibilidad, estudios y diseños de aceras, ciclor | 5801.0 | 0.0 | 100% | $-385.754.898 |
| 499 | 4107 | 6.016 | CAJA DE INSPECCIÓN DOBLE PARA CANALIZACIÓN NORMA CODENSA CS  | 167.0 | 0.0 | 100% | $-349.626.190 |
| 69 | 8464 | 3.023 | BORDILLO EN CONCRETO GRAVA COMÚN 1" 2000 PSI, FUNDIDO EN SIT | 4956.0 | 0.0 | 100% | $-348.258.120 |
| 284 | 4291 | 5.056 | CARCAMO PROTECCIÓN DE TUBERÍA Ø 8" NORMA EAAB NS-090 . 3V.2 | 454.0 | 0.0 | 100% | $-337.708.354 |
| 676 | 6184 | 7.001 | MANTENIMIENTO RUTINARIO DE CALZADA EN PAVIMENTO FLEXIBLE. IN | 13481.0 | 0.0 | 100% | $-326.577.225 |
| 65 | 4856 | 3.019 | PISOS EN LOSETA PREFABRICADA A55 TÁCTIL ALERTA O A56 GUIA 40 | 2201.0 | 0.0 | 100% | $-306.079.864 |
| 270 | 3922 | 5.042 | TUBERIA PVC U.M. EXT/INT LISO NORMA NTC 5070 D=33" (INCLUYE  | 172.0 | 0.0 | 100% | $-303.925.032 |
| 289 | 4297 | 5.061 | CARCAMO DE PROTECCIÓN DE TUBERÍA Ø 24" NORMA EAAB NS-090 V.  | 214.0 | 0.0 | 100% | $-291.444.246 |
| 266 | 3017 | 5.038 | TRANSPORTE Y DISPOSICIÓN FINAL DE ESCOMBROS EN SITIO AUTORIZ | 6103.0 | 912.5999999999999 | 85% | $-286.229.798 |
| 86 | 8476 | 3.040 | CONTENEDOR DE RAICES DE 2,50M X 2,50M H=1,40 M. (INCLUYE CON | 106.0 | 0.0 | 100% | $-267.643.534 |
| 52 | 4032 | 3.010 | GEOTEXTIL T, RESIST. ULTIMA (TIRA ANCHA)=40 KN/M PARA SEPARA | 20379.0 | 0.0 | 100% | $-243.202.986 |
| 495 | 3017 | 6.012 | TRANSPORTE Y DISPOSICIÓN FINAL DE ESCOMBROS EN SITIO AUTORIZ | 4587.0 | 218.18 | 95% | $-240.922.948 |
| 67 | 8499 | 3.021 | LOSETA PREFABRICADA EN CONCRETO A20 TIPO PANOT DE 20X20X6CM  | 1413.0 | 0.0 | 100% | $-227.230.182 |
| 64 | 4919 | 3.018 | ADOQUIN EN CONCRETO 200X100X60MM A25 (SUMINISTRO E INSTALACI | 1449.0 | 0.0 | 100% | $-224.177.688 |
| 43 | 8606 | 3.002 | DEMOLICIÓN PISOS DE CONCRETO - RAMPAS VEHICULARES Y PEATONAL | 13108.0 | 0.0 | 100% | $-203.265.756 |
| 290 | 4299 | 5.062 | CARCAMO DE PROTECCIÓN DE TUBERÍA Ø 30" NORMA EAAB NS-090 V.  | 98.0 | 0.0 | 100% | $-200.938.220 |
| 273 | 3043 | 5.045 | TUBERIA PVC U.M. EXT CORRUGADO/INT LISO U.M. NORMA NTC 3722- | 1949.0 | 92.2 | 95% | $-199.696.983 |

## Saltos criticos (I > 10 x H)

| Fila | Cod IDU | Item | Descripcion | H | I | Ratio | Delta valor |
|---:|---|---|---|---:|---:|---:|---:|
| 85 | 3425 | 3.039 | ANDEN CONCRETO GRAVA COMÚN DE 3000 PSI (210 KG/CM2) PREMEZCL | 114.0 | 15468.629999999994 | 135.6897x | $1.542.541.484 |
| 73 | 5181 | 3.027 | SARDINEL FUNDIDO EN SITIO EN CONCRETO PREMEZCLADO DE 3000PSI | 141.0 | 5639.28 | 39.9949x | $413.740.072 |
| 129 | 3315 | 5.007 | CODO HD 22.5° EXTREMO LISO PARA PVC D=6" (SUMINISTRO E INSTA | 1.0 | 37.0 | 37.0x | $17.856.000 |
| 35 | 3811 | 2.004 | CORTE DE PAVIMENTO - INCLUYE EQUIPO: CORTADORA DE CONCRETO I | 597.0 | 17049.629999999997 | 28.5588x | $51.924.500 |
| 20 | 6016 | 1.008 | ESTABILIZACIÓN DE SUBRASANTE CON RAJÓN, INCLUYE EQUIPO DE CO | 965.0 | 14162.699999999997 | 14.6764x | $2.348.873.855 |
| 27 | 4159 | 1.015 | SUBBASE GRANULAR CLASE C (SBG_C) (SUMINISTRO, EXTENDIDO, NIV | 288.0 | 3515.53 | 12.2067x | $660.384.913 |
| 48 | 3454 | 3.006 | ESTABILIZACIÓN DE SUBRASANTE CON RAJÓN (SUMINISTRO, EXTENDID | 44.0 | 527.39 | 11.9861x | $68.652.015 |

## Saltos altos (I > 3 x H)  -- todos

| Fila | Cod IDU | Item | Descripcion | H | I | Ratio | Delta valor |
|---:|---|---|---|---:|---:|---:|---:|
| 85 | 3425 | 3.039 | ANDEN CONCRETO GRAVA COMÚN DE 3000 PSI (210 KG/CM2) PREMEZCL | 114.0 | 15468.629999999994 | 135.6897x | $1.542.541.484 |
| 73 | 5181 | 3.027 | SARDINEL FUNDIDO EN SITIO EN CONCRETO PREMEZCLADO DE 3000PSI | 141.0 | 5639.28 | 39.9949x | $413.740.072 |
| 129 | 3315 | 5.007 | CODO HD 22.5° EXTREMO LISO PARA PVC D=6" (SUMINISTRO E INSTA | 1.0 | 37.0 | 37.0x | $17.856.000 |
| 35 | 3811 | 2.004 | CORTE DE PAVIMENTO - INCLUYE EQUIPO: CORTADORA DE CONCRETO I | 597.0 | 17049.629999999997 | 28.5588x | $51.924.500 |
| 20 | 6016 | 1.008 | ESTABILIZACIÓN DE SUBRASANTE CON RAJÓN, INCLUYE EQUIPO DE CO | 965.0 | 14162.699999999997 | 14.6764x | $2.348.873.855 |
| 27 | 4159 | 1.015 | SUBBASE GRANULAR CLASE C (SBG_C) (SUMINISTRO, EXTENDIDO, NIV | 288.0 | 3515.53 | 12.2067x | $660.384.913 |
| 48 | 3454 | 3.006 | ESTABILIZACIÓN DE SUBRASANTE CON RAJÓN (SUMINISTRO, EXTENDID | 44.0 | 527.39 | 11.9861x | $68.652.015 |
| 45 | 4592 | 3.004 | RETIRO DE ADOQUIN SOBRE ARENA | 197.0 | 666.11 | 3.3813x | $998.735 |
| 149 | 3226 | 5.027 | TUBERIA PVC D=4" TIPO U.M. RDE 21 (SUMINISTRO E INSTALACIÓN) | 283.0 | 860.56 | 3.0408x | $51.995.417 |

## Reubicaciones detectadas (mismo codigo IDU, filas distintas)

| Cod IDU | Filas eliminadas | Filas nuevas | H_tot | I_tot | Delta cant | Delta valor | Comentario |
|---|---|---|---:|---:|---:|---:|---|
| 3017 | [124, 266, 495] | [14, 47, 194, 318, 370, 427, 536, 599, 613, 654, 667] | 50328.00 | 94762.40 | 44434.40 | $2.450.379.420 | Cambio de subcapitulo: ['INSTALACIONES ELECTRICAS A CARGO DEL IDU MEDIA Y BAJA TENSIÓN', 'OBRAS PARA LA RED DE ACUEDUCTO OBRAS A CARGO DEL IDU', 'OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DEL IDU'] -> ['EXCAVACIONES', 'Excavaciones, Demoliciones y Rellenos', 'INSTALACIONES ELECTRICAS A CARGO DE  ENEL MEDIA Y BAJA TENSIÓN', 'INSTALACIONES ELECTRICAS A CARGO DE ENEL ALUMBRADO PUBLICO', 'INSTALACIONES MOVISTAR', 'INSTALACIONES RED TELEFÓNICA DE ETB - A CARGO IDU', 'INSTALACIONES RED TELEFÓNICA DE ETB A CARGO ESP', 'OBRAS PARA LA RED DE ACUEDUCTO A CARGO DE LA ESP EAAB', 'OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DE LA EAAB', 'OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DEL IDU', 'OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DE LA EAAB'] |
| 8643 | [265] | [317, 369, 426] | 5801.00 | 40873.11 | 35072.11 | $2.332.225.171 | Cambio de subcapitulo: ['OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DEL IDU'] -> ['OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DE LA EAAB', 'OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DEL IDU', 'OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DE LA EAAB'] |
| 3895 | [295] | [399] | 123.00 | 194.00 | 71.00 | $485.055.883 | Cambio de subcapitulo: ['OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DEL IDU'] -> ['OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DEL IDU'] |
| 3380 | [491, 626] | [505] | 3025.00 | 19.60 | -3005.40 | $-441.535.336 | Cambio de subcapitulo: ['INSTALACIONES ELECTRICAS A CARGO DEL IDU MEDIA Y BAJA TENSIÓN', 'INSTALACIONES RED TELEFÓNICA DE ETB - A CARGO IDU'] -> ['INSTALACIONES ELECTRICAS A CARGO DEL IDU MEDIA Y BAJA TENSIÓN'] |
| 4907 | [55] | [158, 228, 503, 544, 607, 634] | 2274.00 | 4419.73 | 2145.73 | $430.023.604 | Cambio de subcapitulo: ['Excavaciones, Demoliciones y Rellenos'] -> ['INSTALACIONES ELECTRICAS A CARGO DE  ENEL MEDIA Y BAJA TENSIÓN', 'INSTALACIONES ELECTRICAS A CARGO DE ENEL ALUMBRADO PUBLICO', 'INSTALACIONES ELECTRICAS A CARGO DEL IDU MEDIA Y BAJA TENSIÓN', 'INSTALACIONES RED TELEFÓNICA DE ETB - A CARGO IDU', 'OBRAS PARA LA RED DE ACUEDUCTO A CARGO DE LA ESP EAAB', 'OBRAS PARA LA RED DE ACUEDUCTO OBRAS A CARGO DEL IDU'] |
| 8655 | [282] | [161, 231, 334, 386, 443] | 936.00 | 3475.07 | 2539.07 | $300.867.100 | Cambio de subcapitulo: ['OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DEL IDU'] -> ['OBRAS PARA LA RED DE ACUEDUCTO A CARGO DE LA ESP EAAB', 'OBRAS PARA LA RED DE ACUEDUCTO OBRAS A CARGO DEL IDU', 'OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DE LA EAAB', 'OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DEL IDU', 'OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DE LA EAAB'] |
| 5182 | [490] | [531] | 3399.00 | 3919.85 | 520.85 | $289.246.235 | Cambio de subcapitulo: ['INSTALACIONES ELECTRICAS A CARGO DEL IDU MEDIA Y BAJA TENSIÓN'] -> ['INSTALACIONES ELECTRICAS A CARGO DE  ENEL MEDIA Y BAJA TENSIÓN'] |
| 3024 | [496] | [160, 230, 537, 600, 614, 633, 655, 668] | 609.00 | 2110.42 | 1501.42 | $280.591.375 | Cambio de subcapitulo: ['INSTALACIONES ELECTRICAS A CARGO DEL IDU MEDIA Y BAJA TENSIÓN'] -> ['INSTALACIONES ELECTRICAS A CARGO DE  ENEL MEDIA Y BAJA TENSIÓN', 'INSTALACIONES ELECTRICAS A CARGO DE ENEL ALUMBRADO PUBLICO', 'INSTALACIONES MOVISTAR', 'INSTALACIONES RED TELEFÓNICA DE ETB - A CARGO IDU', 'INSTALACIONES RED TELEFÓNICA DE ETB A CARGO ESP', 'OBRAS PARA LA RED DE ACUEDUCTO A CARGO DE LA ESP EAAB', 'OBRAS PARA LA RED DE ACUEDUCTO OBRAS A CARGO DEL IDU'] |
| 4030 | [22] | [60] | 36297.00 | 17109.11 | -19187.89 | $-212.429.130 | Cambio de subcapitulo: ['RELLENOS Y CAPAS GRANULARES (BASE Y SUBBASE)'] -> ['Excavaciones, Demoliciones y Rellenos'] |
| 4032 | [52] | [38] | 20379.00 | 36885.90 | 16506.90 | $196.993.345 | Cambio de subcapitulo: ['Excavaciones, Demoliciones y Rellenos'] -> ['None'] |
| 4390 | [46] | [15] | 7383.00 | 5882.14 | -1500.86 | $-191.779.890 | Cambio de subcapitulo: ['Excavaciones, Demoliciones y Rellenos'] -> ['EXCAVACIONES'] |
| 5196 | [10] | [58] | 418.00 | 1765.90 | 1347.90 | $169.985.017 | Cambio de subcapitulo: ['None'] -> ['Excavaciones, Demoliciones y Rellenos'] |
| 3044 | [274] | [326, 378] | 239.00 | 1177.84 | 938.84 | $143.004.109 | Cambio de subcapitulo: ['OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DEL IDU'] -> ['OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DEL IDU', 'OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DE LA EAAB'] |
| 3009 | [123, 263, 494] | [193, 315, 367, 424, 535, 598, 612, 636, 666] | 5993.00 | 8155.82 | 2162.82 | $121.310.523 | Cambio de subcapitulo: ['INSTALACIONES ELECTRICAS A CARGO DEL IDU MEDIA Y BAJA TENSIÓN', 'OBRAS PARA LA RED DE ACUEDUCTO OBRAS A CARGO DEL IDU', 'OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DEL IDU'] -> ['INSTALACIONES ELECTRICAS A CARGO DE  ENEL MEDIA Y BAJA TENSIÓN', 'INSTALACIONES ELECTRICAS A CARGO DE ENEL ALUMBRADO PUBLICO', 'INSTALACIONES MOVISTAR', 'INSTALACIONES RED TELEFÓNICA DE ETB - A CARGO IDU', 'INSTALACIONES RED TELEFÓNICA DE ETB A CARGO ESP', 'OBRAS PARA LA RED DE ACUEDUCTO A CARGO DE LA ESP EAAB', 'OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DE LA EAAB', 'OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DEL IDU', 'OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DE LA EAAB'] |
| 4262 | [264] | [316, 368, 425] | 3411.00 | 19811.98 | 16400.98 | $113.872.005 | Cambio de subcapitulo: ['OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DEL IDU'] -> ['OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DE LA EAAB', 'OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DEL IDU', 'OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DE LA EAAB'] |
| 3048 | [279] | [383, 440] | 43.00 | 148.26 | 105.26 | $66.292.748 | Cambio de subcapitulo: ['OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DEL IDU'] -> ['OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DE LA EAAB', 'OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DEL IDU'] |
| 3045 | [275] | [327, 379] | 712.00 | 979.75 | 267.75 | $57.208.268 | Cambio de subcapitulo: ['OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DEL IDU'] -> ['OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DEL IDU', 'OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DE LA EAAB'] |
| 3043 | [273] | [325] | 1949.00 | 2396.64 | 447.64 | $48.143.235 | Cambio de subcapitulo: ['OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DEL IDU'] -> ['OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DE LA EAAB'] |
| 5023 | [493] | [534, 597, 653] | 1080.00 | 1665.29 | 585.29 | $20.169.679 | Cambio de subcapitulo: ['INSTALACIONES ELECTRICAS A CARGO DEL IDU MEDIA Y BAJA TENSIÓN'] -> ['INSTALACIONES ELECTRICAS A CARGO DE  ENEL MEDIA Y BAJA TENSIÓN', 'INSTALACIONES ELECTRICAS A CARGO DE ENEL ALUMBRADO PUBLICO', 'INSTALACIONES RED TELEFÓNICA DE ETB A CARGO ESP'] |
| 5015 | [298] | [350] | 101.00 | 128.00 | 27.00 | $20.121.426 | Cambio de subcapitulo: ['OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DEL IDU'] -> ['OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DE LA EAAB'] |
| 5253 | [502] | [543] | 5.00 | 4.00 | -1.00 | $-18.491.485 | Cambio de subcapitulo: ['INSTALACIONES ELECTRICAS A CARGO DEL IDU MEDIA Y BAJA TENSIÓN'] -> ['INSTALACIONES ELECTRICAS A CARGO DE  ENEL MEDIA Y BAJA TENSIÓN'] |
| 3329 | [142] | [212] | 13.00 | 17.00 | 4.00 | $15.309.964 | Cambio de subcapitulo: ['OBRAS PARA LA RED DE ACUEDUCTO OBRAS A CARGO DEL IDU'] -> ['OBRAS PARA LA RED DE ACUEDUCTO A CARGO DE LA ESP EAAB'] |
| 4858 | [143] | [213] | 9.00 | 17.00 | 8.00 | $12.694.728 | Cambio de subcapitulo: ['OBRAS PARA LA RED DE ACUEDUCTO OBRAS A CARGO DEL IDU'] -> ['OBRAS PARA LA RED DE ACUEDUCTO A CARGO DE LA ESP EAAB'] |
| 7512 | [292, 630] | [344, 396] | 74.00 | 58.00 | -16.00 | $-11.508.768 | Cambio de subcapitulo: ['INSTALACIONES RED TELEFÓNICA DE ETB - A CARGO IDU', 'OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DEL IDU'] -> ['OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DEL IDU', 'OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DE LA EAAB'] |
| 4878 | [299] | [351, 403] | 101.00 | 64.00 | -37.00 | $-9.926.804 | Cambio de subcapitulo: ['OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DEL IDU'] -> ['OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DEL IDU', 'OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DE LA EAAB'] |
| 3328 | [141] | [211] | 8.00 | 10.00 | 2.00 | $6.841.756 | Cambio de subcapitulo: ['OBRAS PARA LA RED DE ACUEDUCTO OBRAS A CARGO DEL IDU'] -> ['OBRAS PARA LA RED DE ACUEDUCTO A CARGO DE LA ESP EAAB'] |
| 4848 | [267] | [159, 319, 371] | 3537.00 | 3038.28 | -498.72 | $-6.329.754 | Cambio de subcapitulo: ['OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DEL IDU'] -> ['OBRAS PARA LA RED DE ACUEDUCTO OBRAS A CARGO DEL IDU', 'OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DEL IDU', 'OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DE LA EAAB'] |
| 6538 | [276] | [380] | 119.00 | 134.41 | 15.41 | $4.829.864 | Cambio de subcapitulo: ['OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DEL IDU'] -> ['OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DEL IDU'] |
| 3046 | [277] | [329, 381, 438] | 443.00 | 433.45 | -9.55 | $-3.627.720 | Cambio de subcapitulo: ['OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DEL IDU'] -> ['OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DE LA EAAB', 'OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DEL IDU', 'OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DE LA EAAB'] |
| 4901 | [144] | [214] | 8.00 | 10.00 | 2.00 | $2.892.142 | Cambio de subcapitulo: ['OBRAS PARA LA RED DE ACUEDUCTO OBRAS A CARGO DEL IDU'] -> ['OBRAS PARA LA RED DE ACUEDUCTO A CARGO DE LA ESP EAAB'] |

## Posibles reemplazos contractual -> NP

| Fila contract | Item contract | Fila NP | Item NP | Delta contract | Delta NP | Sobrecosto neto |
|---:|---|---:|---|---:|---:|---:|
| 24 | 1.012 - BASE GRANULAR CLASE A (BG_A) (SUMIN | 30 | NP-124 - BASE GRANULAR CLASE A (BG_A) CON RE | $-1.811.267.958 | $2.518.521.916 | $707.253.958 |
| 33 | 2.002 - MEZCLA ASFÁLTICA DENSA EN CALIENTE  | 39 | NP-123 - MEZCLA ASFÁLTICA EN CALIENTE DENSA  | $-2.584.929.953 | $3.269.600.612 | $684.670.659 |
| 489 | 6.006 - 2 DUCTOS D=3" PVC-EB (INCLUYE SUMIN | 551 | NP-07 - 6 DUCTOS D=6" PVC-TDP (INCLUYE SUMI | $-167.940.640 | $302.594.577 | $134.653.937 |
| 272 | 5.044 - TUBERIA PVC U.M. EXT/INT LISO NORMA | 463 | NP-17 - TUBERIA PVC U.M. EXT CORRUGADO/INT  | $-43.812.034 | $141.000.499 | $97.188.465 |
| 269 | 5.041 - TUBERIA PVC U.M. EXT/INT LISO NORMA | 464 | NP-18 - TUBERIA PVC U.M. EXT CORRUGADO/INT  | $-88.567.080 | $123.041.772 | $34.474.692 |
| 300 | 5.072 - TUBERIA PVC SANITARIA D=6" TIPO U.S | 562 | NP-12 - ADAPTADOR TERMINAL CAMPANA PVC D=6" | $-90.833.622 | $110.420.352 | $19.586.730 |
| 151 | 5.029 - TUBERIA PVC D=6" TIPO U.M. RDE 41 ( | 358 | NP-30 - TUBERIA PVC U.M. EXT CORRUGADO/INT  | $-69.845.272 | $83.303.712 | $13.458.440 |
| 501 | 6.018 - CONSTRUCCION DE CAJA DE INSPECCION  | 548 | NP-04 - CONSTRUCCION  DE  CAJA  DE INSPECCI | $-160.975.754 | $75.007.860 | $-85.967.894 |
| 270 | 5.042 - TUBERIA PVC U.M. EXT/INT LISO NORMA | 408 | NP-19 - TUBERIA PVC U.M. EXT CORRUGADO/INT  | $-303.925.032 | $129.829.952 | $-174.095.080 |
| 271 | 5.043 - TUBERIA PVC U.M. EXT/INT LISO NORMA | 465 | NP-19 - TUBERIA PVC U.M. EXT CORRUGADO/INT  | $-605.539.802 | $302.936.555 | $-302.603.247 |
| 268 | 5.040 - TUBERIA PVC U.M. EXT/INT LISO NORMA | 406 | NP-17 - TUBERIA PVC U.M. EXT CORRUGADO/INT  | $-564.421.032 | $93.308.173 | $-471.112.859 |
| 281 | 5.053 - TUBERIA CONCRETO ALTA RESISTENCIA D | 418 | NP-71 - TUBERIA CONCRETO ALTA RESISTENCIA D | $-1.059.297.570 | $274.675.991 | $-784.621.579 |

## Cruce V2 (VICON 21-04-2026) vs V4 (01-09-2026)

- Codigos IDU en V2 (con cantidad): 0
- Codigos IDU en V4 (agregados): 266
- Recorte V4<V2 (por cantidad): **0 codigos**
- Nuevos en V4 no presentes en V2: **266 codigos**

### Recortes V4 vs V2 (top 25 por delta cant)

| Cod IDU | Und | Cant V2 | Cant V4 | Delta cant | Valor V2 CD | Valor V4 CD | Delta valor CD |
|---|---|---:|---:|---:|---:|---:|---:|

### Nuevos codigos en V4 (top 25 por valor)

| Cod IDU | Descripcion | Und | Cant V4 | Valor V4 (con AIU) | Solo NP? |
|---|---|---|---:|---:|---:|
| 7785 | LOSA DE CONCRETO MR45 (SUMINISTRO, FORMALETEADO, C | M3 | 9851.224192000001 | $14.709.394.807 | False |
| 3017 | TRANSPORTE Y DISPOSICIÓN FINAL DE ESCOMBROS EN SIT | M3 | 94762.39997999996 | $5.225.767.308 | False |
| 8618 | MEZCLA ASFÁLTICA EN CALIENTE DENSA MD19 CON CEMENT | M3 | 2089.45 | $3.269.600.612 | True |
| 8643 | Proyecto: factibilidad, estudios y diseños de acer | M2 | 40873.10999999999 | $2.717.980.069 | False |
| 6016 | ESTABILIZACIÓN DE SUBRASANTE CON RAJÓN, INCLUYE EQ | M3 | 14162.699999999997 | $2.520.620.695 | False |
| 4744 | BASE GRANULAR CLASE A (BG_A) CON RECICLADO DE CONC | M3 | 10476.554999999998 | $2.518.521.916 | True |
| 4754 | SUBBASE GRANULAR CLASE B (SBG_B) CON RECICLADO DE  | M3 | 11948.835176464074 | $2.439.378.599 | False |
| N/A | CAÑUELA EN CONCRETO 2500 PSI IMPERMEABILIZADO, PAR | UN | 380.8 | $2.314.363.081 | True |
| 5182 | 6 DUCTOS D=6" + 2 DUCTOS D=3" PVC TDP. SUMINISTRO  | ML | 3919.849999999999 | $2.176.829.900 | False |
| 3425 | ANDEN CONCRETO GRAVA COMÚN DE 3000 PSI (210 KG/CM2 | M2 | 15468.629999999994 | $1.553.994.038 | False |
| 3895 | SUMIDERO LATERAL SL-250A, H=1.7M (FUNDIDO EN SITIO | UN | 194.0 | $1.325.363.962 | False |
| 10271 | ESTAMPADO PARA CONCRETO MR DE POMPEYANOS, ACCESOS  | M2 | 18100.45 | $1.107.150.225 | True |
| 4907 | SUBBASE GRANULAR PEATONAL SBG_PEA. SUMINISTRO, EXT | M3 | 4419.73 | $885.753.670 | False |
| 9032 | CONSTRUCCION DE CAJA DE INSPECCION DOBLE PARA CANA | UN | 165.0 | $778.412.250 | True |
| 4390 | EXCAVACIÓN MANUAL EN MATERIAL COMÚN (INCL CARGUE,  | M3 | 5882.14 | $751.619.850 | False |
| 4159 | SUBBASE GRANULAR CLASE C (SBG_C) (SUMINISTRO, EXTE | M3 | 3515.53 | $719.312.593 | False |
| 3748 | LOSA DE CONCRETO MR45 (SUMINISTRO, FORMALETEADO, C | M3 | 500.0458 | $560.951.378 | False |
| 3009 | EXCAVACION MANUAL PARA REDES PROFUNDIDAD 0M - 2M ( | M3 | 8155.821979999999 | $457.451.900 | False |
| 4032 | GEOTEXTIL T, RESIST. ULTIMA (TIRA ANCHA)=40 KN/M P | M2 | 36885.9 | $440.196.331 | False |
| 7435 | TUBERIA PVC U.M. EXT CORRUGADO/INT LISO U.M. NORMA | ML | 174.29999999999998 | $432.766.507 | True |
| 5181 | SARDINEL FUNDIDO EN SITIO EN CONCRETO PREMEZCLADO  | ML | 5639.28 | $424.350.181 | False |
| 3227 | TUBERIA PVC D=6" TIPO U.M. RDE 21 (SUMINISTRO E IN | ML | 2305.4699999999993 | $415.793.820 | False |
| 8655 | GRAVILLA DE 3/4" - SUMINISTRO E INSTALACIÓN. | M3 | 3475.0699999999997 | $411.778.420 | False |
| 3024 | RELLENO PARA REDES EN ARENA DE PEÑA (SUMINISTRO, E | M3 | 2110.4200000000005 | $394.403.731 | False |
| 3878 | PLACA CUBIERTA D=1.70M POZO INSPEC. (PREFABRICADA. | UND | 138.0 | $341.589.054 | True |

## Metodologia

- Fuente unica: `analisis/datos/presupuesto_2026_09.json`, extraido con `analisis/scripts/extraer_presupuesto.py` de `fuentes/4. PRESUPUESTO 01-09-2026 75MM (8 MESES).xlsx`.
- Se filtran filas 7-679 (capitulos 1-7). Se excluye capitulo 8 ACEROS (filas 680-687).
- Estados por renglon:
  - `sin_cambio`: H = I > 0 (tolerancia 0,01).
  - `aumento`: I > H > 0.
  - `disminucion`: 0 < I < H.
  - `eliminado`: H > 0 e I = 0.
  - `nuevo_contractual`: H = 0, I > 0, codigo no-NP.
  - `np_nuevo`: item_pago inicia con 'NP' o codigo_idu = 'NO', con I > 0.
- Verificaciones formulas linea a linea: J = I - H (tol 0,01), O ~ (I - H) x L (tol $10), Q ~ O + P (tol $10).
- Reubicaciones: mismo codigo_idu con al menos un renglon eliminado/reducido y otro nuevo/aumentado.
- Reemplazos contractual -> NP: fuzzy match por Jaccard >= 0,4 sobre tokens de descripcion, misma unidad y capitulo; casos conocidos (33->39, 24->30) forzados si no fueron detectados.
- Cruce V4 vs V2 (VICON 21-04-2026): se convierte el valor V4 con AIU a costo directo dividiendo entre 1,31849 para comparar contra `valor_cont_cd` de comparativa.json.
- Todo el detalle esta en `01_variacion_items.json`.
