# Registro de auditoría — presupuesto 01-09-2026 (75MM · 8 meses)

**Contrato IDU 1752-2021 · Grupo 2 · Interventoría Consorcio Montevideo 045** · generado el 2026-09-28 por `analisis/scripts/auditoria.py` · fuente `4. PRESUPUESTO 01-09-2026 75MM (8 MESES).xlsx` · SHA-256 `e17f0f39efe2288d4fb56f340b5e95a4445b0b9cc3ee9b7b170fc885514f570a`

Este registro deja por escrito (A) lo que está mal o es dudoso en el Excel del contratista, (B) lo que el propio análisis tuvo que corregir y en qué commit, (C) las preguntas que deben responder el contratista o el IDU antes de emitir concepto y (D) los supuestos del análisis. Cada asiento de la sección A se calcula leyendo el libro con openpyxl; el revisor puede repetirlo con la columna *Verificable con*.

**Resumen:** 67 asientos · por tipo {'A': 25, 'B': 14, 'C': 16, 'D': 12} · por severidad {'ALTA': 20, 'MEDIA': 25, 'BAJA': 13, 'INFO': 9} · por estado {'ABIERTO': 28, 'DOCUMENTADO': 13, 'CORREGIDO': 14, 'LIMITACION': 12}.

**Abiertos de severidad ALTA (resolver antes de firmar):** A-01, A-02, A-06, A-24, A-25, C-01, C-02, C-03, C-04, C-05.

## Cifras de control

| Concepto | Valor | Celda |
|---|---:|---|
| total_obras_M688 | 58.196.933.800 | M688 |
| total_V4_M703 | 75.426.575.199 | M703 |
| valor_actual_M705 | 59.426.575.199 | M705 |
| adicion | 16.000.000.000 | M707 (signo invertido) |
| delta_obras | 13.893.639.001 | Q688 |
| balance | -257.285.548 | O688 |
| np_con_aiu | 14.150.924.549 | P688 |
| suma_civ_obras | 58.196.933.869 | Σ ítem × CIV |
| bloque_aceros | 3.052.987.517 | M682:M687 |
| bolsa_F | 2.977.517.840 | M697 |

## A · Errores e inconsistencias en la fuente (Excel del contratista)

| ID | Sev. | Estado | Título | Impacto | Pregunta / soporte |
|---|---|---|---|---:|---|
| A-01 | ALTA | ABIERTO | La base de precios unitarios (columna K) depende de un libro externo que no viene en el archivo | — | ¿Cuál es el libro 'ANEXO APU MODIF 28-07-2025.xlsx' y qué VISOR/insumos usa? ¿Fue revisado por la interventoría y aprobado por el IDU como base de precios de la adición? · *Soporte:* Libro ANEXO APU MODIF 28-07-2025.xlsx completo; APU FO-GI-19 de cada ítem con VU distinto al contractual; acta o comunicación IDU que autorice la actualización de VU. |
| A-02 | ALTA | ABIERTO | 81 cantidades por CIV de la hoja principal están vinculadas a libros externos no entregados | 57.269.689 | ¿Qué es 'PRESUPUESTO TOTAL $80 MIL.xlsx'? ¿Hubo una versión del presupuesto de $80.000M? ¿Las memorias CALCULO ESTRUCTURA / CALCULO DE ANDENES del libro radicado (hojas ocultas) son las mismas que las del libro externo? · *Soporte:* Libro PRESUPUESTO TOTAL $80 MIL.xlsx y memoria de cantidades del NP-101 por CIV; acta de competencia ENEL 03-10-2025. |
| A-03 | MEDIA | ABIERTO | 175 renglones tienen el VU (K) digitado como constante en vez de fórmula | 14.150.924.549 | Para cada renglón con VU digitado: ¿de qué APU sale el valor y quién lo aprobó? Si el código existe en CONSOLIDADO, ¿por qué no se usa la fórmula? · *Soporte:* APU FO-GI-19 de los 84 NP y de los códigos contractuales con VU digitado; comunicación de aprobación de VU por la interventoría/IDU. |
| A-04 | MEDIA | ABIERTO | El total del subgrupo 5 (BY688) no coincide con la suma de sus CIVs y AH688 + BY688 no da CB688 | 126.296 | ¿Cuál es el total oficial del subgrupo 5: 43.258.118.071,5 (BY688) o 43.258.244.367 (suma de CIVs / EJECUTIVO)? Corregir la fórmula /2 por una suma directa de renglones. · *Soporte:* Libro corregido con totales por CIV calculados por SUMIF sobre renglones de ítem. |
| A-05 | MEDIA | ABIERTO | Bloque ACEROS (filas 680-687) fuera del total de obras, con $75,5M más que la bolsa fija F | 75.469.677 | ¿El bloque ACEROS es la memoria de cantidades de la bolsa F o alcance adicional? ¿Por qué la memoria de la hoja Aceros (~$2.500M teóricos) es menor que el bloque? · *Soporte:* Memoria de acero por CIV (kg por elemento) conciliada con la bolsa F; constancia en el otrosí de que el acero se paga por una sola vía. |
| A-06 | ALTA | ABIERTO | Ítem 8643 (5.037): descripción de consultoría, unidad cambiada (M2/MES → M2) y VU +33,8 %, por $2.718M | 2.717.980.069 | ¿Qué obra se paga con el código 8643? ¿Por qué la descripción es la de un estudio de factibilidad/diseño? ¿Por qué cambió la unidad de M2/MES a M2 y el VU de 37.694 a 50.435? · *Soporte:* Especificación particular, APU y memoria de cantidades del 8643 por CIV; acta que autorice el cambio de unidad. |
| A-07 | MEDIA | ABIERTO | 'Ajustes por cambio de vigencia' ($4.555M) no se recalcula pese a que la adición lleva la obra a la vigencia 2027 | — | ¿La adición incluye o excluye ajustes por cambio de vigencia para 2027? Si los excluye, ¿quién asume el mayor valor y con qué fórmula (ICCP)? · *Soporte:* Cronograma de la adición por vigencia y cálculo del ajuste según GUDP017. |
| A-08 | MEDIA | ABIERTO | Bioseguridad ($59,4M) no se extiende a los 8 meses aunque es proporcional al plazo | 40.000.000 | ¿El contratista renuncia expresamente a pedir bioseguridad por el plazo adicional o el renglón debe incorporarse? · *Soporte:* Comunicación del contratista. |
| A-09 | MEDIA | ABIERTO | El Fondo de Compensaciones apareció en V2 ($5.943M) y vuelve a 0 en V4 sin trazabilidad | 5.942.657.520 | ¿Qué compensaciones financiaba el fondo de V2, por qué se retiró y dónde quedaron esos costos (NP-109/NP-110 arqueología)? · *Soporte:* Trazabilidad documental del componente K entre V2, V3 y V4. |
| A-10 | BAJA | DOCUMENTADO | Celda O690 con una constante mal digitada (…779 en vez de …799): 58.196.933.780 | 20 | Corregir la celda o eliminarla.  |
| A-11 | BAJA | DOCUMENTADO | Fila 34: N y O se desvían $86.217 de la fórmula (valor inicial = H × L) | 86.217 | Confirmar si H34 o L34 fueron modificados después de calcular N34 (¿celda pegada como valor?).  |
| A-12 | BAJA | DOCUMENTADO | Redondeo por CIV: la suma de los 27 CIV da 58.196.933.869 frente a 58.196.933.800 (Δ 69) | 69 |   |
| A-13 | BAJA | DOCUMENTADO | Etiquetas con fecha desactualizada: fila 703 '04-05-2026' y EJECUTIVO '11/05/2026' en un archivo del 01-09-2026 | — | Actualizar los rótulos en la versión que se anexe al otrosí.  |
| A-14 | BAJA | DOCUMENTADO | Cifras en letras del 'Presupuesto estimado': 1 de 17 no coinciden con el número | — | Corregir los textos en letras antes de firmar.  |
| A-15 | INFO | DOCUMENTADO | '84 NP' del nombre de la hoja = 84 códigos NP listados; 81 tienen cantidad (105 renglones) y 3 nunca se cuantifican | — | ¿Los NP en cero se retiran del anexo del otrosí o se dejan como 'aprobados sin cantidad'?  |
| A-16 | INFO | DOCUMENTADO | Identificadores de CIV: 500002375 en la hoja principal frente a 50002375 en el VISOR/dashboard (y 16004876 en la comparativa de abril) | — | Confirmar con el IDU el CIV oficial del tramo.  |
| A-17 | INFO | DOCUMENTADO | Numeración de ítems generada por fórmula con artefactos de coma flotante (452 celdas, p. ej. 1.0019999999999998) | — |   |
| A-18 | INFO | DOCUMENTADO | La hoja de referencia de precios rotula la misma columna como 'VISOR 07 MAYO DE 2025' (fila 8) y 'VISOR 13 SEPTIEMBRE 2024' (fila 9) | — |   |
| A-19 | INFO | DOCUMENTADO | 174 códigos IDU con más de un renglón (ítem × subcapítulo) y 32 reubicaciones entre renglones por 5.807.343.956 | 5.807.343.956 | Entregar la conciliación código a código de los traslados entre subcapítulos.  |
| A-20 | INFO | DOCUMENTADO | 47 celdas de totales y del detalle SST con decimales de peso (p. ej. BY688 = …071,5) | — |   |
| A-21 | INFO | DOCUMENTADO | 15 de 18 hojas están ocultas; el libro tiene 190 vínculos externos y fullCalcOnLoad = True | — | Entregar el libro con vínculos rotos convertidos a valores y sin hojas ocultas, o entregar los libros vinculados.  |
| A-22 | INFO | DOCUMENTADO | Fórmula auxiliar suelta en T699 (=T7+T12+…; R699 = 'SIN REDES') dentro de la fila de bioseguridad | — |   |
| A-23 | MEDIA | ABIERTO | 5 códigos con VU distinto entre renglones y 1 códigos con unidad distinta a la contractual | — | Justificar cada código con más de un VU o con cambio de unidad frente al contractual. · *Soporte:* APU y especificación de cada código afectado. |
| A-24 | ALTA | ABIERTO | Los VU de V4 están +49,0 % (mediana) sobre los VU pactados en la propuesta (15.086.222.761 con AIU) y +4,2 % sobre el APU actualizado de 2024 (3.639.050.739 en 367 renglones con Δ > 2 %) | 15.086.222.761 | ¿Qué otrosí o acta autorizó actualizar los VU pactados a insumos 13-09-2024? ¿Ese incremento se contabilizó como adición o como reajuste? ¿Se aplica además el componente 'ajustes por cambio de vigencia' sobre los mismos ítems (doble ajuste)? · *Soporte:* Otrosí de actualización de precios; comparación VU pactado vs actualizado firmada por la interventoría; APU FO-GI-19 de los ítems de mayor impacto (losa MR45, estabilización con rajón, transporte de escombros, ductos TDP). |
| A-25 | ALTA | ABIERTO | El valor inicial del contrato fue 50.793.789.333, no 59.426.575.199: el 'valor actual' ya trae +8.632.785.866 (+17,0 %) y con la solicitud el acumulado llega a 48,5 % del inicial | 8.632.785.866 | ¿Cuáles son los otrosíes del contrato (fecha, valor, naturaleza: adición, reajuste, actualización de precios, prórroga)? ¿Cuánto de los $8.632.785.866 previos cuenta como adición para el tope del 50 %? · *Soporte:* Expediente contractual: contrato, otrosíes 1 a n, actas de modificación, CDP/RP de cada adición. |

### Detalle

**A-01 · La base de precios unitarios (columna K) depende de un libro externo que no viene en el archivo** [ALTA · ABIERTO · trazabilidad]

La columna K (VU costo directo) de la hoja principal se calcula con VLOOKUP sobre la hoja oculta CONSOLIDADO CTO 1752 AJUSTADO, columna 16 (Q, 'VALOR ITEM COSTO DIRECTO ACTUALIZACION'). Esa columna Q es a su vez un VLOOKUP a un libro externo ('[190]OBRAS CIVILES'!C2:Q234, columna 14) que no está en el archivo radicado: file:///C:\Users\Estudios\Documents\CONTRATO%201752-2021\Técnicos\PRESUPUESTO\ANEXO%20APU%20MODIF%2028-07-2025.xlsx. Sin ese libro los VU no se pueden recalcular: lo que se ve son valores guardados ('congelados'). Celdas con vínculo externo en CONSOLIDADO: {'Q': 213, 'R': 209, 'T': 8}. Filas de la hoja principal con K por fórmula: 469; con K digitado como constante: 175 (ver A-03).

*Cómo lo trata el análisis:* El análisis usa los valores guardados de K (los mismos que muestra Excel al abrir sin actualizar vínculos). La comparación de VU (sección H de la app) se hace contra la columna 'actualización APU 13-09-2024' de la hoja PRESUPUESTO CONTRACTUAL MAYO 25 y contra el VISOR 07-05-25 (data.json).

*Verificable con:* `openpyxl: wb['PRESUPUESTO TODOS LOS CIV 84 NP']['K8'].value ; wb['CONSOLIDADO CTO 1752 AJUSTADO']['Q12'].value ; wb._external_links[189].file_link.Target`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "K8",
  "formula": "=IF(C8=0,\"0 \",VLOOKUP(B8,'CONSOLIDADO CTO 1752 AJUSTADO'!$B:$U,16,FALSE))",
  "valor": 833
 },
 {
  "hoja": "CONSOLIDADO CTO 1752 AJUSTADO",
  "celda": "Q12",
  "formula": "=VLOOKUP(B12,'[190]OBRAS CIVILES'!C2:Q234,14,0)",
  "valor": 833
 },
 {
  "vinculo_externo": 190,
  "destino": "file:///C:\\Users\\Estudios\\Documents\\CONTRATO%201752-2021\\Técnicos\\PRESUPUESTO\\ANEXO%20APU%20MODIF%2028-07-2025.xlsx"
 },
 {
  "vinculo_externo": 188,
  "destino": "file:///E:\\JUAN%20CARLOS%20BETANCOURT%20GARCÍA\\GRUPO%20EMPRESARIAL\\INCSAS\\PROYECTOS%20EN%20EJECUCIÓN\\CONSORCIO%20VICON%20024\\EJERCICIO%20ACTUALIZACIÓN%20IDU\\ANEXO%20MODIFICACIÓN%20INCLUIDO%20APU´S%20PRESUPUESTO%20(AJUSTADOS%20VISOR%20SEPT%202024)%20CTO%201752%20(19-09-2024).xlsx?C0B19B7B",
  "uso": "hoja PRESUPUESTO CONTRACTUAL MAYO 25 (columna Q)"
 }
]
```
</details>

**A-02 · 81 cantidades por CIV de la hoja principal están vinculadas a libros externos no entregados** [ALTA · ABIERTO · trazabilidad]

Las cantidades por CIV del NP-101 'Transporte de material fresado' (filas 29 y 59, 52 celdas) se leen del libro externo 'PRESUPUESTO TOTAL $80 MIL.xlsx' (file:///Z:\6.%20TÉCNICO\6.06%20PRESUPUESTO%202025\PRESUPUESTO%20TOTAL%20$80%20MIL.xlsx), hojas CALCULO ESTRUCTURA y CALCULO DE ANDENES. Las filas 489, 510 y 511 (ductos ENEL/TDP, 29 celdas, todas en 0) se leen del acta de competencia ENEL del 03-10-2025 (file:///C:\SynologyDrive\4.%20TÉCNICO\ACTAS%20DE%20COMPETENCIA%202025\ENEL\ACTA%20DE%20COMPETENCIA%20ENEL%20-%20CTO%20IDU1752-2021%20(03-10-2025).xlsx). El nombre del primer libro ('$80 MIL') sugiere una versión del presupuesto cercana a $80.000 millones que no fue radicada. Los valores que se ven son los guardados en el último recálculo del contratista.

*Cómo lo trata el análisis:* Se toman los valores guardados. El NP-101 queda marcado en la ficha del ítem y en la lista de chequeo como cantidad de origen externo.

*Verificable con:* `openpyxl: [c.coordinate for c in ws.iter_rows() ... if '[' in str(c.value)] sobre la hoja principal → 81 celdas`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "fila": 29,
  "codigo": 5380,
  "item": "NP-101",
  "descripcion": "TRANSPORTE DE MATERIAL FRESADO PROVENIENTE DE SITIO DE OBRA AL SITIO D",
  "celdas": 26,
  "ejemplo": "S29 ='[186]CALCULO ESTRUCTURA'!S1",
  "cant_final_I": 4423.4,
  "valor_M": 51806861,
  "libros": [
   "file:///Z:\\6.%20TÉCNICO\\6.06%20PRESUPUESTO%202025\\PRESUPUESTO%20TOTAL%20$80%20MIL.xlsx"
  ]
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "fila": 59,
  "codigo": 5380,
  "item": "NP-101",
  "descripcion": "TRANSPORTE DE MATERIAL FRESADO PROVENIENTE DE SITIO DE OBRA AL SITIO D",
  "celdas": 26,
  "ejemplo": "S59 ='[186]CALCULO DE ANDENES'!L34",
  "cant_final_I": 466.43,
  "valor_M": 5462828,
  "libros": [
   "file:///Z:\\6.%20TÉCNICO\\6.06%20PRESUPUESTO%202025\\PRESUPUESTO%20TOTAL%20$80%20MIL.xlsx"
  ]
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "fila": 489,
  "codigo": 3159,
  "item": "6.006000000000002",
  "descripcion": "2 DUCTOS D=3\" PVC-EB (INCLUYE SUMINISTRO E INSTALACIÓN. NO INCLUYE REL",
  "celdas": 1,
  "ejemplo": "BJ489 ='[187]MEMORIA ENEL PTE ARANDA'!$AU$763",
  "cant_final_I": 13.1,
  "valor_M": 649760,
  "libros": [
   "file:///C:\\SynologyDrive\\4.%20TÉCNICO\\ACTAS%20DE%20COMPETENCIA%202025\\ENEL\\ACTA%20DE%20COMPETENCIA%20ENEL%20-%20CTO%20IDU1752-2021%20(03-10-2025).xlsx"
  ]
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "fila": 510,
  "codigo": 3382,
  "item": "NP-05",
  "descripcion": "\n'1 DUCTO D=3\" PVC-TDP (INCLUYE SUMINISTRO E INSTALACIÓN. NO INCLUYE R",
  "celdas": 4,
  "ejemplo": "Y510 ='[187]MEMORIA ENEL PTE ARANDA'!$L$778",
  "cant_final_I": 0,
  "valor_M": 0,
  "libros": [
   "file:///C:\\SynologyDrive\\4.%20TÉCNICO\\ACTAS%20DE%20COMPETENCIA%202025\\ENEL\\ACTA%20DE%20COMPETENCIA%20ENEL%20-%20CTO%20IDU1752-2021%20(03-10-2025).xlsx"
  ]
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "fila": 511,
  "codigo": 8739,
  "item": "NP-06",
  "descripcion": "2 DUCTOS D=6\" + 2 DUCTOS D=3\" PVC TDP (Incluye suministro e instalació",
  "celdas": 24,
  "ejemplo": "Y511 ='[187]MEMORIA ENEL PTE ARANDA'!$L$779",
  "cant_final_I": 0,
  "valor_M": 0,
  "libros": [
   "file:///C:\\SynologyDrive\\4.%20TÉCNICO\\ACTAS%20DE%20COMPETENCIA%202025\\ENEL\\ACTA%20DE%20COMPETENCIA%20ENEL%20-%20CTO%20IDU1752-2021%20(03-10-2025).xlsx"
  ]
 }
]
```
</details>

**A-03 · 175 renglones tienen el VU (K) digitado como constante en vez de fórmula** [MEDIA · ABIERTO · precios]

De los 175 renglones con K constante, 174 son NP (no existen en CONSOLIDADO, así que el VU tiene que venir de un APU nuevo) y 1 son códigos contractuales. De estos últimos, 1 no aparecen en CONSOLIDADO y 0 tienen un K distinto al que daría la fórmula (VLOOKUP a CONSOLIDADO Q). Valor con AIU de los renglones con K constante: 14.150.924.549; solo NP: 14.150.924.549.

*Cómo lo trata el análisis:* Los VU de los NP se contrastan con V2 (comparativa.json) en la sección de NPs; los contractuales con K constante quedan listados aquí para que el revisor pida el soporte.

*Verificable con:* `openpyxl: [r for r in range(7,680) if not str(ws[f'K{r}'].value).startswith('=') and ws[f'K{r}'].value not in (None,'')]`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "fila": 39,
  "codigo": "8618",
  "item": "NP-123",
  "descripcion": "MEZCLA ASFÁLTICA EN CALIENTE DENSA MD19 CON CEMENTO ASFÁLTIC",
  "und": "M3",
  "K": 1186823.0,
  "K_consolidado": null,
  "difiere_de_consolidado": false,
  "es_np": true,
  "valor_M": 3269600612.0
 },
 {
  "fila": 30,
  "codigo": "4744",
  "item": "NP-124",
  "descripcion": "BASE GRANULAR CLASE A (BG_A) CON RECICLADO DE CONCRETO HIDRA",
  "und": "M3",
  "K": 182327.0,
  "K_consolidado": null,
  "difiere_de_consolidado": false,
  "es_np": true,
  "valor_M": 2518521916.0
 },
 {
  "fila": 479,
  "codigo": "N/A",
  "item": "NP-133",
  "descripcion": "CONTRATO 1752-2021 - BOX CULVERT PREFABRICADO TIPO 1, Ancho ",
  "und": "UN",
  "K": 12960731.0,
  "K_consolidado": null,
  "difiere_de_consolidado": false,
  "es_np": true,
  "valor_M": 1879745340.0
 },
 {
  "fila": 87,
  "codigo": "10271",
  "item": "NP-16",
  "descripcion": "ESTAMPADO PARA CONCRETO MR DE POMPEYANOS, ACCESOS VEHICULARE",
  "und": "M2",
  "K": 46392.0,
  "K_consolidado": null,
  "difiere_de_consolidado": false,
  "es_np": true,
  "valor_M": 1107150225.0
 },
 {
  "fila": 547,
  "codigo": "9032",
  "item": "NP-03",
  "descripcion": "CONSTRUCCION DE CAJA DE INSPECCION DOBLE PARA CANALIZACION D",
  "und": "UN",
  "K": 3578070.0,
  "K_consolidado": null,
  "difiere_de_consolidado": false,
  "es_np": true,
  "valor_M": 778412250.0
 },
 {
  "fila": 561,
  "codigo": "N/A",
  "item": "NP-122",
  "descripcion": "CONSTRUCCION DE CAJA DE INSPECCION DOBLE PARA CANALIZACION D",
  "und": "UN",
  "K": 3358432.0,
  "K_consolidado": null,
  "difiere_de_consolidado": false,
  "es_np": true,
  "valor_M": 323248307.0
 },
 {
  "fila": 465,
  "codigo": "7435",
  "item": "NP-19",
  "descripcion": "TUBERIA PVC U.M. EXT CORRUGADO/INT LISO U.M. NORMA NTC 3722-",
  "und": "ML",
  "K": 1883126.0,
  "K_consolidado": null,
  "difiere_de_consolidado": false,
  "es_np": true,
  "valor_M": 302936555.0
 },
 {
  "fila": 551,
  "codigo": "3408",
  "item": "NP-07",
  "descripcion": "6 DUCTOS D=6\" PVC-TDP (INCLUYE SUMINISTRO E INSTALACIÓN. NO ",
  "und": "ML",
  "K": 370246.0,
  "K_consolidado": null,
  "difiere_de_consolidado": false,
  "es_np": true,
  "valor_M": 302594577.0
 }
]
```
</details>

**A-04 · El total del subgrupo 5 (BY688) no coincide con la suma de sus CIVs y AH688 + BY688 no da CB688** [MEDIA · ABIERTO · aritmética]

Los totales por CIV en la fila 688 usan la fórmula SUM(col7:col679)/2: se divide entre dos porque las filas de subtotal de capítulo repiten el valor de sus ítems. El truco solo cuadra si cada ítem está cubierto exactamente una vez por un subtotal. Resultado: BY688 (SG5) = 43.258.118.071,50 frente a la suma de los CIV del subgrupo 5 = 43.258.244.367 (Δ -126.295,50); AH688 (SG2) = 14.938.689.480 frente a 14.938.689.502 (Δ -22); AH688 + BY688 = 58.196.807.551,50 ≠ CB688 = 58.196.933.800 (Δ -126.248,50). CB688 sí coincide con M688 = 58.196.933.800. La hoja EJECUTIVO usa 43.258.244.367 como total del subgrupo 5 (H40) y 58.196.933.869 de obras (I45): suma de los CIV redondeados, no la fila 688.

*Cómo lo trata el análisis:* El análisis no usa la fila 688 por CIV: suma los renglones ítem × CIV (presupuesto_2026_09.json) y verifica contra M688 (Δ +69 por redondeo, ver A-12).

*Verificable con:* `python analisis/scripts/verificacion.py (sección 6) y este script (sum_sg)`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "BY688",
  "formula": "=SUM(BY7:BY679)/2",
  "valor": 43258118071.5,
  "esperado_suma_civ_sg5": 43258244367.0
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "AH688",
  "formula": "=SUM(AH7:AH679)/2",
  "valor": 14938689480.0,
  "esperado_suma_civ_sg2": 14938689502.0
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "CB688",
  "formula": "=SUM(CB7:CB679)/2",
  "valor": 58196933800.0
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "M688",
  "formula": "=SUM(M8:M679)",
  "valor": 58196933800.0
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "T688",
  "formula": "=SUM(T7:T679)/2"
 }
]
```
</details>

**A-05 · Bloque ACEROS (filas 680-687) fuera del total de obras, con $75,5M más que la bolsa fija F** [MEDIA · ABIERTO · alcance]

El bloque ACEROS reparte acero de refuerzo, acero liso y dovelas por CIV con cantidades actualizadas y suma 3.052.987.517 con AIU (M682:M687). Está fuera del rango de M688 = =SUM(M8:M679), así que no está dentro de los 58.196.933.800. El acero se paga por la bolsa fija F (fila 697) de 2.977.517.840, igual desde la firma. Diferencia bloque − bolsa = 75.469.677. Si el bloque es la memoria de la bolsa, la bolsa queda corta; si es alcance adicional, requiere adición.

*Cómo lo trata el análisis:* Hallazgo H06-01 reescrito (ver B-08). La app lo muestra en la ficha del componente F, en el resumen ejecutivo y en la lista de chequeo.

*Verificable con:* `openpyxl: ws['M688'].value == '=SUM(M8:M679)'; sum(ws[f'M{r}'].value for r in 682..687)`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "M688",
  "formula": "=SUM(M8:M679)"
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "M697",
  "valor": 2977517840.0
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "fila": 680,
  "codigo": null,
  "descripcion": "ACEROS",
  "H": null,
  "I": null,
  "M": null
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "fila": 681,
  "codigo": null,
  "descripcion": "PAVIMENTOS ",
  "H": null,
  "I": null,
  "M": null
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "fila": 682,
  "codigo": 3708,
  "descripcion": "ACERO DE REFUERZO FY=60000 PSI. SUMINISTRO E INSTA",
  "H": 247985,
  "I": 211290.08000000002,
  "M": 1557630470
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "fila": 683,
  "codigo": 4959,
  "descripcion": "ACERO LISO PARA TRANSFERENCIA DE LOSAS D= 1 1/4\" (",
  "H": 52558,
  "I": 81288.82,
  "M": 900761414
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "fila": 684,
  "codigo": 7713,
  "descripcion": "(DOVELAS) ACERO LISO PARA TRANSFERENCIA DE LOSAS D",
  "H": 0,
  "I": 19704.6,
  "M": 208888465
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "fila": 685,
  "codigo": null,
  "descripcion": "ESPACIO PÚBLICO",
  "H": null,
  "I": null,
  "M": null
 }
]
```
</details>

**A-06 · Ítem 8643 (5.037): descripción de consultoría, unidad cambiada (M2/MES → M2) y VU +33,8 %, por $2.718M** [ALTA · ABIERTO · alcance]

El código 8643 aparece en 4 filas (265, 317, 369, 426) con la descripción 'Proyecto: factibilidad, estudios y diseños de aceras, ciclorutas y conexiones peatonales en la …', que corresponde a un estudio o diseño, no a una obra de redes. En la hoja PRESUPUESTO CONTRACTUAL MAYO 25 (fila 149) el mismo código tiene unidad 'M2/MES', cantidad 5.801 y VU 37.694; en V4 la unidad es 'M2', el VU es 50.435 (33.8 %) y las cantidades pasan de 5.801 a 40.873,11. El código NO está en el VISOR 07-05-25. Valor V4 con AIU: 2.717.980.069.

*Cómo lo trata el análisis:* Se analiza como cualquier ítem (aparece en las fichas y en la sección H de precios). Se deja aquí como duda prioritaria porque la descripción no permite saber qué se está pagando.

*Verificable con:* `python: [it for it in pres['items'] if it['codigo_idu']=='8643']`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "fila": 265,
  "subcapitulo": "OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DEL IDU",
  "und": "M2",
  "H": 5801,
  "I": 0,
  "K": 50435,
  "M": 0
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "fila": 317,
  "subcapitulo": "OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DE LA EAAB",
  "und": "M2",
  "H": 0,
  "I": 18442.509999999995,
  "K": 50435,
  "M": 1226390030
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "fila": 369,
  "subcapitulo": "OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DEL IDU",
  "und": "M2",
  "H": 0,
  "I": 17457.17,
  "K": 50435,
  "M": 1160866891
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "fila": 426,
  "subcapitulo": "OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DE LA EAAB",
  "und": "M2",
  "H": 0,
  "I": 4973.43,
  "K": 50435,
  "M": 330723148
 },
 {
  "hoja": "PRESUPUESTO CONTRACTUAL MAYO 25",
  "fila": 149,
  "und": "M2/MES",
  "cant": 5801,
  "vu": 37694,
  "desc": "Proyecto: factibilidad, estudios y diseños de aceras, ciclorutas y conexiones peatonales e"
 }
]
```
</details>

**A-07 · 'Ajustes por cambio de vigencia' ($4.555M) no se recalcula pese a que la adición lleva la obra a la vigencia 2027** [MEDIA · ABIERTO · alcance]

La hoja resumen muestra el componente E con valor actual 4.555.525.079, adición 0 y total 4.555.525.079. El componente fue dimensionado en la firma (2021) para el plazo original; 8 meses adicionales desde el vencimiento actual llevan la ejecución a 2027, y el manual IDU GUDP017 prevé el ajuste de precios por cambio de vigencia con el ICCP. Ni el componente E ni los VU incluyen ese efecto.

*Cómo lo trata el análisis:* El simulador (sección J) permite un recálculo ilustrativo; el informe lo lista como pregunta. No se estima un valor porque depende del cronograma real.

*Verificable con:* `openpyxl: wb['resumen']['E11'].value == 0`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "hoja": "resumen",
  "celda": "D11:F11",
  "valores": [
   4555525079,
   0,
   4555525079
  ]
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "M695",
  "valor": 4555525079
 }
]
```
</details>

**A-08 · Bioseguridad ($59,4M) no se extiende a los 8 meses aunque es proporcional al plazo** [MEDIA · ABIERTO · alcance]

M699 = 59.390.312 igual que en V0 (resumen E15 = 0). PMA-SST, diálogo y PMT sí se recalculan por 8 meses.

*Cómo lo trata el análisis:* Hallazgo H06-04 (MEDIA, impacto estimado ~$40M = 59,4M × 8/12 aprox.).

*Verificable con:* `openpyxl: ws['M699'].value`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "M699",
  "valor": 59390312
 },
 {
  "hoja": "resumen",
  "celda": "E15",
  "valor": 0
 }
]
```
</details>

**A-09 · El Fondo de Compensaciones apareció en V2 ($5.943M) y vuelve a 0 en V4 sin trazabilidad** [MEDIA · ABIERTO · trazabilidad]

En la propuesta del 21-04-2026 (V2) el contratista incluyó un Fondo de Compensaciones de 5.942.657.520; en V3 y V4 el componente K vale 0 (M700). No hay comunicación que explique su origen ni su retiro; podría relacionarse con compensaciones ambientales o arqueológicas que ahora aparecen como NP dentro de obras.

*Cómo lo trata el análisis:* Hallazgo H06-06; waterfall V0→V4 lo muestra como componente que entra y sale.

*Verificable con:* `comparativa.json → globales; ws['M700']`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "M700",
  "valor": 0
 },
 {
  "fuente": "comparativa.json (V2)",
  "fondo_compensaciones": 5942657520
 }
]
```
</details>

**A-10 · Celda O690 con una constante mal digitada (…779 en vez de …799): 58.196.933.780** [BAJA · DOCUMENTADO · aritmética]

O690 = =44303294779+13893639001 = 58.196.933.780, frente a N688 + Q688 = 58.196.933.800 (N689). El primer sumando debía ser 44.303.294.799 (N688). Celdas que referencian O690: ['AO691', 'BO691', 'AO696', 'BO696'] → es una celda de control sin efecto en los totales.

*Cómo lo trata el análisis:* Sin efecto en el análisis; se documenta como indicio de digitación manual en celdas de control.

*Verificable con:* `openpyxl: ws['O690'].value`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "O690",
  "formula": "=44303294779+13893639001",
  "valor": 58196933780
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "N689",
  "formula": "=+N688+Q688",
  "valor": 58196933800
 }
]
```
</details>

**A-11 · Fila 34: N y O se desvían $86.217 de la fórmula (valor inicial = H × L)** [BAJA · DOCUMENTADO · aritmética]

N34 = 12.357.428.721 frente a H × L = 12.357.342.504 (Δ 86.217); O compensa con el mismo Δ negativo. Fórmula de N34: =ROUND(L34*H34,0)+86217 ; O34: =Q34 ; H34 = 8276 ; L34 = 1493154. El total Q (M − N) no se ve afectado.

*Cómo lo trata el análisis:* Detectado por el análisis 04 (H01). La verificación global cuadra con tolerancia de $86.217 por esta fila.

*Verificable con:* `python analisis/scripts/analisis_04.py → desviaciones_M_N_O_Q`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "N34",
  "formula": "=ROUND(L34*H34,0)+86217",
  "valor": 12357428721
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "O34",
  "formula": "=Q34",
  "valor": 2351966086
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "H34",
  "valor": 8276
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "L34",
  "valor": 1493154
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "M34",
  "valor": 14709394807
 }
]
```
</details>

**A-12 · Redondeo por CIV: la suma de los 27 CIV da 58.196.933.869 frente a 58.196.933.800 (Δ 69)** [BAJA · DOCUMENTADO · aritmética]

Cada celda de valor por CIV es ROUND(cantidad_CIV × L, 0) y el total del renglón es ROUND(L × I, 0); las dos rutas difieren en unos pesos por renglón. Renglones con diferencia: 92; máxima diferencia por renglón: 13. La hoja EJECUTIVO (que suma CIV) muestra por eso 58.196.933.869 de obras y 75.426.575.268 de total (Δ +69).

*Cómo lo trata el análisis:* verificacion.py acepta Δ ≤ $100 y lo reporta; todas las cifras del análisis citan M688 / M703 como totales oficiales.

*Verificable con:* `python analisis/scripts/verificacion.py (sección 6)`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "fila": 9,
  "codigo": "3010",
  "M": 15718200,
  "suma_civ": 15718199.0,
  "delta": -1.0
 },
 {
  "fila": 13,
  "codigo": "3710",
  "M": 276521681,
  "suma_civ": 276521682.0,
  "delta": 1.0
 },
 {
  "fila": 14,
  "codigo": "3017",
  "M": 2893431761,
  "suma_civ": 2893431763.0,
  "delta": 2.0
 },
 {
  "fila": 19,
  "codigo": "3800",
  "M": 115336067,
  "suma_civ": 115336069.0,
  "delta": 2.0
 },
 {
  "fila": 20,
  "codigo": "6016",
  "M": 2520620695,
  "suma_civ": 2520620697.0,
  "delta": 2.0
 },
 {
  "fila": 27,
  "codigo": "4159",
  "M": 719312593,
  "suma_civ": 719312594.0,
  "delta": 1.0
 },
 {
  "fila": 30,
  "codigo": "4744",
  "M": 2518521916,
  "suma_civ": 2518521917.0,
  "delta": 1.0
 },
 {
  "fila": 34,
  "codigo": "7785",
  "M": 14709394807,
  "suma_civ": 14709394808.0,
  "delta": 1.0
 }
]
```
</details>

**A-13 · Etiquetas con fecha desactualizada: fila 703 '04-05-2026' y EJECUTIVO '11/05/2026' en un archivo del 01-09-2026** [BAJA · DOCUMENTADO · etiqueta]

B703 = 'VALOR TOTAL CONTRATO PRESUPUESTO 04-05-2026'; EJECUTIVO!C1 = 'RESUMEN EJECUTIVO POR CIV 11/05/2026'. El nombre del archivo y el radicado son del 01-09-2026 (versión 75MM · 8 meses). Indica que el libro se construyó sobre la versión de mayo (63MM) sin actualizar rótulos.

*Cómo lo trata el análisis:* Hallazgo H06-08 (BAJA). Sin efecto numérico.

*Verificable con:* `openpyxl`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "B703",
  "valor": "VALOR TOTAL CONTRATO PRESUPUESTO 04-05-2026"
 },
 {
  "hoja": "EJECUTIVO",
  "celda": "C1",
  "valor": "RESUMEN EJECUTIVO POR CIV 11/05/2026"
 }
]
```
</details>

**A-14 · Cifras en letras del 'Presupuesto estimado': 1 de 17 no coinciden con el número** [BAJA · DOCUMENTADO · etiqueta]

La hoja Presupuesto estimado escribe cada valor en letras (texto que suele copiarse al otrosí). B7: 'SEISCIENTOS TREINTA Y SISETE MILLONES QUINIENTOS NOVENTA Y U…' vs 637.591.877 Comparación exacta tras normalizar acentos, espacios y 'PESOS M/CTE' (num2words, lang=es).

*Cómo lo trata el análisis:* Sin efecto numérico. Se lista para que el texto del otrosí no herede el error.

*Verificable con:* `python: num2words(n, lang='es') vs hoja Presupuesto estimado`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "hoja": "Presupuesto estimado",
  "celda": "B2",
  "numero": 75426575199,
  "texto": "SETENTA Y CINCO MIL CUATROCIENTOS VEINTISÉIS MILLONES QUINIENTOS SETENTA Y CINCO MIL CIENTO NOVENTA Y NUEVE PESOS M/CTE",
  "esperado": "SETENTA Y CINCO MIL CUATROCIENTOS VEINTISEIS MILLONES QUINIENTOS SETENTA Y CINCO MIL CIENTO NOVENTA Y NUEVE",
  "similitud": 1.0,
  "ok": true
 },
 {
  "hoja": "Presupuesto estimado",
  "celda": "B5",
  "numero": 758734334,
  "texto": "SETECIENTOS CINCUENTA Y OCHO MILLONES SETECIENTOS TREINTA Y CUATRO MIL TRESCIENTOS TREINTA Y CUATRO  PESOS M/CTE",
  "esperado": "SETECIENTOS CINCUENTA Y OCHO MILLONES SETECIENTOS TREINTA Y CUATRO MIL TRESCIENTOS TREINTA Y CUATRO",
  "similitud": 1.0,
  "ok": true
 },
 {
  "hoja": "Presupuesto estimado",
  "celda": "B7",
  "numero": 637591877,
  "texto": "SEISCIENTOS TREINTA Y SISETE MILLONES QUINIENTOS NOVENTA Y UN MIL OCHOCIENTOS SETENTA Y SIETE  PESOS M/CTE",
  "esperado": "SEISCIENTOS TREINTA Y SIETE MILLONES QUINIENTOS NOVENTA Y UN MIL OCHOCIENTOS SETENTA Y SIETE",
  "similitud": 0.995,
  "ok": false
 },
 {
  "hoja": "Presupuesto estimado",
  "celda": "B9",
  "numero": 121142457,
  "texto": "CIENTO VEINTI UN MILLONES CIENTO CUARENTA Y DOS MIL CUATROCIENTOS CINCUENTA Y SIETE PESOS M/CTE",
  "esperado": "CIENTO VEINTIUN MILLONES CIENTO CUARENTA Y DOS MIL CUATROCIENTOS CINCUENTA Y SIETE",
  "similitud": 1.0,
  "ok": true
 },
 {
  "hoja": "Presupuesto estimado",
  "celda": "B11",
  "numero": 74667840865,
  "texto": "SETENTA Y CUATRO MIL SEISCIENTOS SESENTA Y SIETE MILLONES OCHOCIENTOS CUARENTA MIL OCHOCIENTOS SESENTA Y CINCO PESOS M/CTE",
  "esperado": "SETENTA Y CUATRO MIL SEISCIENTOS SESENTA Y SIETE MILLONES OCHOCIENTOS CUARENTA MIL OCHOCIENTOS SESENTA Y CINCO",
  "similitud": 1.0,
  "ok": true
 },
 {
  "hoja": "Presupuesto estimado",
  "celda": "B14",
  "numero": 36117036850,
  "texto": "TREINTA Y SEIS MIL CIENTO DIECISIETE MILLONES TREINTA Y SEIS MIL OCHOCIENTOS CINCUENTA PESOS M/CTE",
  "esperado": "TREINTA Y SEIS MIL CIENTO DIECISIETE MILLONES TREINTA Y SEIS MIL OCHOCIENTOS CINCUENTA",
  "similitud": 1.0,
  "ok": true
 },
 {
  "hoja": "Presupuesto estimado",
  "celda": "B16",
  "numero": 22079896950,
  "texto": "VEINTIDÓS MIL SETENTA Y NUEVE MILLONES OCHOCIENTOS NOVENTA Y SEIS  MIL NOVECIENTOS CINCUENTA PESOS M/CTE",
  "esperado": "VEINTIDOS MIL SETENTA Y NUEVE MILLONES OCHOCIENTOS NOVENTA Y SEIS MIL NOVECIENTOS CINCUENTA",
  "similitud": 1.0,
  "ok": true
 },
 {
  "hoja": "Presupuesto estimado",
  "celda": "B18",
  "numero": 58196933800,
  "texto": "CINCUENTA Y OCHO MIL CIENTO NOVENTA Y SEIS MILLONES NOVECIENTOS TREINTA Y TRES MIL OCHOCIENTOS PESOS M/CTE",
  "esperado": "CINCUENTA Y OCHO MIL CIENTO NOVENTA Y SEIS MILLONES NOVECIENTOS TREINTA Y TRES MIL OCHOCIENTOS",
  "similitud": 1.0,
  "ok": true
 }
]
```
</details>

**A-15 · '84 NP' del nombre de la hoja = 84 códigos NP listados; 81 tienen cantidad (105 renglones) y 3 nunca se cuantifican** [INFO · DOCUMENTADO · estructura]

Renglones NP: 173; con cantidad 0 en V4: 68 (quedan como plantilla). NP sin cantidad en ninguna fila: NP-06, NP-08, NP-11. Los renglones en 0 no suman, pero dejan abierta la puerta a incorporarlos después sin nuevo trámite.

*Cómo lo trata el análisis:* El análisis cuenta 105 renglones NP con cantidad, 81 códigos, $14.150.924.549 con AIU (verificado al peso).

*Verificable con:* `python: agrupar pres['items'] por item_pago NP`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "np": "NP-06",
  "filas": [
   511,
   550
  ],
  "descripcion": "2 DUCTOS D=6\" + 2 DUCTOS D=3\" PVC TDP (Incluye suministro e instalació"
 },
 {
  "np": "NP-08",
  "filas": [
   513,
   552
  ],
  "descripcion": "4 DUCTOS D=4\" + 2 DUCTOS D=3\" PVC TDP (Incluye suministro e instalació"
 },
 {
  "np": "NP-11",
  "filas": [
   516,
   555
  ],
  "descripcion": "ADAPTADOR TERMINAL CAMPANA PVC D=4\" (SUMINISTRO E INSTALACIÓN)"
 },
 {
  "renglones_np_en_cero": [
   162,
   163,
   187,
   234,
   235,
   236,
   237,
   238,
   239,
   241,
   242,
   243,
   247,
   248,
   251,
   252,
   253,
   254,
   255,
   256,
   259,
   260,
   302,
   303,
   304,
   305,
   306,
   307,
   308,
   309,
   310,
   311,
   312,
   313,
   407,
   466,
   467,
   468,
   469,
   475,
   476,
   477,
   481,
   506,
   507,
   508,
   509,
   510,
   511,
   512,
   513,
   515,
   516,
   517,
   522,
   523,
   545,
   549,
   550,
   552,
   555,
   557,
   558,
   559,
   560,
   584,
   585,
   586
  ]
 }
]
```
</details>

**A-16 · Identificadores de CIV: 500002375 en la hoja principal frente a 50002375 en el VISOR/dashboard (y 16004876 en la comparativa de abril)** [INFO · DOCUMENTADO · estructura]

Fila 3 de la hoja principal: 27 CIV (500002375 no está en data.json); data.json: 50002375 no está en el Excel. Es el mismo tramo (KR 65A). El código SEG de la fila 4 sí coincide.

*Cómo lo trata el análisis:* Alias explícito en analisis_02_variacion_civ.py y en la app (mapeo H02-300).

*Verificable con:* `analisis/scripts/analisis_02_variacion_civ.py`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "fila": 3,
  "ids": [
   "9004002",
   "9003990",
   "9003980",
   "9003989",
   "9003981",
   "9003967",
   "9003968",
   "16000016",
   "16000007",
   "16000023",
   "16000012",
   "16000010",
   "16000013",
   "16000024",
   "16000017",
   "16000029",
   "16000028",
   "16000060",
   "16000052",
   "16000043",
   "16000032",
   "16000027",
   "16000038",
   "16000057",
   "500002375",
   "16000047",
   "16000077"
  ]
 },
 {
  "fuente": "data.json",
  "ids": [
   "9004002",
   "9003990",
   "9003980",
   "9003989",
   "9003981",
   "9003967",
   "9003968",
   "16000016",
   "16000007",
   "16000023",
   "16000012",
   "16000010",
   "16000013",
   "16000024",
   "16000017",
   "16000029",
   "16000028",
   "16000060",
   "16000052",
   "16000043",
   "16000032",
   "16000027",
   "16000038",
   "16000057",
   "50002375",
   "16000047",
   "16000077"
  ]
 }
]
```
</details>

**A-17 · Numeración de ítems generada por fórmula con artefactos de coma flotante (452 celdas, p. ej. 1.0019999999999998)** [INFO · DOCUMENTADO · estructura]

La columna C (ítem de pago) se genera sumando 0,001 al ítem anterior; Excel la muestra con 3 decimales pero guarda valores como 1.0019999999999998 o 5.037000000000012. Cualquier cruce por 'ítem' debe redondear a 3 decimales.

*Cómo lo trata el análisis:* extraer_presupuesto.py redondea item_pago a 3 decimales.

*Verificable con:* `openpyxl: ws['C9'].value`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "C9",
  "valor": 1.0019999999999998
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "C10",
  "valor": 1.0029999999999997
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "C11",
  "valor": 1.0039999999999996
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "C13",
  "valor": 1.0049999999999994
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "C14",
  "valor": 1.0059999999999993
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "C15",
  "valor": 3.0049999999999994
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "C19",
  "valor": 1.0069999999999992
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "C20",
  "valor": 1.0079999999999991
 }
]
```
</details>

**A-18 · La hoja de referencia de precios rotula la misma columna como 'VISOR 07 MAYO DE 2025' (fila 8) y 'VISOR 13 SEPTIEMBRE 2024' (fila 9)** [INFO · DOCUMENTADO · etiqueta]

PRESUPUESTO CONTRACTUAL MAYO 25!Q8 = 'ACTUALIZACIÓN DE APU´S CON INSUMOS VISOR 07 MAYO DE 2025' y Q9 = 'VALOR ITEM COSTO DIRECTO ACTUALIZACION DE APU´S INSUMOS VISOR 13 SEPTIEMBRE 2024'. Los valores de la columna Q coinciden con el 'precio original' del dashboard de mayo de 2025 (APU actualizado con insumos del VISOR 13-09-2024), así que el rótulo correcto es el de la fila 9. Las columnas I (oficial IDU), M (propuesta VICON = VU pactado) y Q (APU 13-09-2024) son tres referencias distintas de VU; el análisis las nombra explícitamente (ver A-24).

*Cómo lo trata el análisis:* La app llama a la columna Q 'referencia APU 13-09-2024' y a la M 'VU pactado (propuesta)'.

*Verificable con:* `openpyxl: wb['PRESUPUESTO CONTRACTUAL MAYO 25']['Q8'].value`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "hoja": "PRESUPUESTO CONTRACTUAL MAYO 25",
  "celda": "Q8",
  "valor": "ACTUALIZACIÓN DE APU´S CON INSUMOS VISOR 07 MAYO DE 2025"
 },
 {
  "hoja": "PRESUPUESTO CONTRACTUAL MAYO 25",
  "celda": "Q9",
  "valor": "VALOR ITEM COSTO DIRECTO ACTUALIZACION DE APU´S INSUMOS VISOR 13 SEPTIEMBRE 2024 "
 },
 {
  "hoja": "PRESUPUESTO CONTRACTUAL MAYO 25",
  "celda": "M9",
  "valor": "VALOR UNITARIO PROPUESTA CONTRATISTA SIN AIU"
 },
 {
  "hoja": "PRESUPUESTO CONTRACTUAL MAYO 25",
  "celda": "I9",
  "valor": "VALOR UNITARIO SIN AIU"
 }
]
```
</details>

**A-19 · 174 códigos IDU con más de un renglón (ítem × subcapítulo) y 32 reubicaciones entre renglones por 5.807.343.956** [INFO · DOCUMENTADO · estructura]

La hoja repite el mismo código en subcapítulos distintos (IDU vs ESP, pavimentos vs espacio público). Un código que baja en un renglón y sube en otro no es eliminación ni alcance nuevo: es un traslado. Trasladado = min(valor que sale de los renglones que bajan, valor que entra en los que suben), sumado por código: 5.807.343.956 en 32 códigos (15 con renglones eliminados del todo y nuevos del todo). Sin esta lectura, la 'eliminación' y el 'alcance nuevo' se sobreestiman.

*Cómo lo trata el análisis:* Sección I de la app (reubicaciones) e informe 8C; H02 del análisis 04 pasa a INFO (B-09); el cálculo de 'trasladado' se corrigió (B-13).

*Verificable con:* `python analisis/scripts/analisis_01_variacion_items.py → reubicaciones`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "codigo_idu": "5182",
  "und": "ML",
  "filas_eliminadas": [
   490
  ],
  "filas_nuevas": [
   531
  ],
  "filas_eliminadas_total": [],
  "filas_nuevas_total": [
   531
  ],
  "H_total": 3399.0,
  "I_total": 3919.85,
  "delta_cant": 520.85,
  "N_valor_inicial": 1887583665,
  "M_valor_final": 2176829900,
  "valor_disminuido": 1883363119,
  "valor_aumentado": 2172609354,
  "trasladado": 1883363119,
  "delta_valor_neto": 289246235,
  "comentario": "Cambio de subcapitulo: ['INSTALACIONES ELECTRICAS A CARGO DEL IDU MEDIA Y BAJA TENSIÓN'] -> ['INSTALACIONES ELECTRICAS A CARGO DE  ENEL MEDIA Y BAJA TENSIÓN']"
 },
 {
  "codigo_idu": "3895",
  "und": "UN",
  "filas_eliminadas": [
   295
  ],
  "filas_nuevas": [
   399
  ],
  "filas_eliminadas_total": [
   295
  ],
  "filas_nuevas_total": [
   399
  ],
  "H_total": 123.0,
  "I_total": 194.0,
  "delta_cant": 71.0,
  "N_valor_inicial": 840308079,
  "M_valor_final": 1325363962,
  "valor_disminuido": 840308079,
  "valor_aumentado": 1325363962,
  "trasladado": 840308079,
  "delta_valor_neto": 485055883,
  "comentario": "Cambio de subcapitulo: ['OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DEL IDU'] -> ['OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DEL IDU']"
 },
 {
  "codigo_idu": "3017",
  "und": "M3",
  "filas_eliminadas": [
   124,
   266,
   495
  ],
  "filas_nuevas": [
   14,
   47,
   194,
   318,
   370,
   427,
   536,
   599,
   613,
   654,
   667
  ],
  "filas_eliminadas_total": [],
  "filas_nuevas_total": [
   47,
   194,
   318,
   370,
   427,
   536,
   599,
   613,
   654,
   667
  ],
  "H_total": 50328.0,
  "I_total": 94762.4,
  "delta_cant": 44434.4,
  "N_valor_inicial": 2775387888,
  "M_valor_final": 5225767308,
  "valor_disminuido": 527403109,
  "valor_aumentado": 2977782529,
  "trasladado": 527403109,
  "delta_valor_neto": 2450379420,
  "comentario": "Cambio de subcapitulo: ['INSTALACIONES ELECTRICAS A CARGO DEL IDU MEDIA Y BAJA TENSIÓN', 'OBRAS PARA LA RED DE ACUEDUCTO OBRAS A CARGO DEL IDU', 'OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DEL IDU'] -> ['EXCAVACIONES', 'Excavaciones, Demoliciones y Rellenos', 'INSTALACIONES ELECTRICAS A CARGO DE  ENEL MEDIA Y BAJA TENSIÓN', 'INSTALACIONES ELECTRICAS A CARGO DE ENEL ALUMBRADO PUBLICO', 'INSTALACIONES MOVISTAR', 'INSTALACIONES RED TELEFÓNICA DE ETB - A CARGO IDU', 'INSTALACIONES RED TELEFÓNICA DE ETB A CARGO ESP', 'OBRAS PARA LA RED DE ACUEDUCTO A CARGO DE LA ESP EAAB', 'OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DE LA EAAB', 'OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DEL IDU', 'OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DE LA EAAB']"
 },
 {
  "codigo_idu": "8643",
  "und": "M2",
  "filas_eliminadas": [
   265
  ],
  "filas_nuevas": [
   317,
   369,
   426
  ],
  "filas_eliminadas_total": [
   265
  ],
  "filas_nuevas_total": [
   317,
   369,
   426
  ],
  "H_total": 5801.0,
  "I_total": 40873.11,
  "delta_cant": 35072.11,
  "N_valor_inicial": 385754898,
  "M_valor_final": 2717980069,
  "valor_disminuido": 385754898,
  "valor_aumentado": 2717980069,
  "trasladado": 385754898,
  "delta_valor_neto": 2332225171,
  "comentario": "Cambio de subcapitulo: ['OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DEL IDU'] -> ['OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DE LA EAAB', 'OBRAS PARA LA RED DE ALCANTARILLADO PLUVIAL A CARGO DEL IDU', 'OBRAS PARA LA RED DE ALCANTARILLADO SANITARIO A CARGO DE LA EAAB']"
 },
 {
  "codigo_idu": "3009",
  "und": "M3",
  "filas_elim
```
</details>

**A-20 · 47 celdas de totales y del detalle SST con decimales de peso (p. ej. BY688 = …071,5)** [INFO · DOCUMENTADO · aritmética]

Los totales por CIV (fila 688, /2) y el detalle de SST/diálogo/PMT a 8 meses (filas 730-738) no están redondeados a pesos; M692 sí redondea (ROUND(2943115324 + S738, 0)). En un otrosí las cifras deben ir en pesos enteros.

*Cómo lo trata el análisis:* El análisis redondea al peso donde corresponde y reporta las diferencias.

*Verificable con:* `openpyxl`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "celda": "BY688",
  "valor": 43258118071.5
 },
 {
  "celda": "K689",
  "valor": 0.31849
 },
 {
  "celda": "BY690",
  "valor": 43258118071.5
 },
 {
  "celda": "T691",
  "valor": 0.03650654564210048
 },
 {
  "celda": "V691",
  "valor": 0.04658850554425601
 },
 {
  "celda": "X691",
  "valor": 0.04423652902139666
 },
 {
  "celda": "Z691",
  "valor": 0.02805898215551693
 },
 {
  "celda": "AB691",
  "valor": 0.03502517658413131
 }
]
```
</details>

**A-21 · 15 de 18 hojas están ocultas; el libro tiene 190 vínculos externos y fullCalcOnLoad = True** [INFO · DOCUMENTADO · trazabilidad]

Hojas ocultas: PRESUPUESTO CONTRACTUAL MAYO 25, MEMORIA CANTIDADES, MEMORIA ETB, PRESUPUESTO 63 mm, EJECUTIVO, NPs Objetados, CALCULO ESTRUCTURA, Resumen estructura, CALCULO DE ANDENES, MOBILIARIOS, Aceros, Hoja1, CONSOLIDADO CTO 1752 AJUSTADO, VISOR 07-05-25, FASE 1 (2). Varias son la base del cálculo (CONSOLIDADO, PRESUPUESTO CONTRACTUAL MAYO 25, VISOR 07-05-25, NPs Objetados, PRESUPUESTO 63 mm, EJECUTIVO). Vínculos externos declarados: 190 (la mayoría heredados de libros antiguos; los que afectan el cálculo son [186], [187], [188] y [190], ver A-01 y A-02). fullCalcOnLoad = True obliga a Excel a recalcular al abrir: si el usuario no actualiza vínculos, verá los valores guardados; si los actualiza sin tener los libros, verá #REF!.

*Cómo lo trata el análisis:* El análisis lee las hojas ocultas como cualquier otra y usa siempre los valores guardados.

*Verificable con:* `openpyxl: [ws.sheet_state for ws in wb]; len(wb._external_links)`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "hojas_ocultas": [
   "PRESUPUESTO CONTRACTUAL MAYO 25",
   "MEMORIA CANTIDADES",
   "MEMORIA ETB",
   "PRESUPUESTO 63 mm",
   "EJECUTIVO",
   "NPs Objetados",
   "CALCULO ESTRUCTURA",
   "Resumen estructura",
   "CALCULO DE ANDENES",
   "MOBILIARIOS",
   "Aceros",
   "Hoja1",
   "CONSOLIDADO CTO 1752 AJUSTADO",
   "VISOR 07-05-25",
   "FASE 1 (2)"
  ]
 },
 {
  "vinculos_externos": 190
 },
 {
  "vinculos_que_afectan_calculo": {
   "186": "file:///Z:\\6.%20TÉCNICO\\6.06%20PRESUPUESTO%202025\\PRESUPUESTO%20TOTAL%20$80%20MIL.xlsx",
   "187": "file:///C:\\SynologyDrive\\4.%20TÉCNICO\\ACTAS%20DE%20COMPETENCIA%202025\\ENEL\\ACTA%20DE%20COMPETENCIA%20ENEL%20-%20CTO%20IDU1752-2021%20(03-10-2025).xlsx",
   "188": "file:///E:\\JUAN%20CARLOS%20BETANCOURT%20GARCÍA\\GRUPO%20EMPRESARIAL\\INCSAS\\PROYECTOS%20EN%20EJECUCIÓN\\CONSORCIO%20VICON%20024\\EJERCICIO%20ACTUALIZACIÓN%20IDU\\ANEXO%20MODIFICACIÓN%20INCLUIDO%20APU´S%20PRESUPUESTO%20(AJUSTADOS%20VISOR%20SEPT%202024)%20CTO%201752%20(19-09-2024).xlsx?C0B19B7B",
   "190": "file:///C:\\Users\\Estudios\\Documents\\CONTRATO%201752-2021\\Técnicos\\PRESUPUESTO\\ANEXO%20APU%20MODIF%2028-07-2025.xlsx"
  }
 }
]
```
</details>

**A-22 · Fórmula auxiliar suelta en T699 (=T7+T12+…; R699 = 'SIN REDES') dentro de la fila de bioseguridad** [INFO · DOCUMENTADO · estructura]

T699 = =T7+T12+T18+T31+T41+T61+T88+T101 → 1.362.951.062: suma de subtotales de capítulo del primer CIV, aparentemente un cálculo de 'obra sin redes' que quedó en la fila de un componente. Referenciada por: ninguna celda.

*Cómo lo trata el análisis:* Sin efecto en totales.

*Verificable con:* `openpyxl`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "T699",
  "formula": "=T7+T12+T18+T31+T41+T61+T88+T101",
  "valor": 1362951062
 },
 {
  "hoja": "PRESUPUESTO TODOS LOS CIV 84 NP",
  "celda": "R699",
  "valor": "SIN REDES"
 }
]
```
</details>

**A-23 · 5 códigos con VU distinto entre renglones y 1 códigos con unidad distinta a la contractual** [MEDIA · ABIERTO · precios]

Un mismo código IDU debe tener un solo VU y una sola unidad en todo el presupuesto. VU distintos: 4841, 4849, 3937, 4892, 8737. Unidad distinta: 8643 (M2/MES→M2).

*Cómo lo trata el análisis:* Se listan para revisión; la sección H de la app compara VU por renglón.

*Verificable con:* `este script (multi_k, und_dif)`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "codigo": "4841",
  "filas": [
   138,
   186,
   208,
   256
  ],
  "vu_distintos": [
   267066,
   288548
  ],
  "descripcion": "EMPATES DE TUBERÍA EN PVC A PVC 4\" LINEAL SEGÚN NORMA NS-023"
 },
 {
  "codigo": "4849",
  "filas": [
   166,
   236,
   488,
   529,
   568,
   592,
   620,
   642
  ],
  "vu_distintos": [
   2977,
   3492
  ],
  "descripcion": "DEMOLICION O RETIRO MANUAL DE TUBERIAS DE AC Ø < 12\" (INCLUY"
 },
 {
  "codigo": "3937",
  "filas": [
   411,
   468
  ],
  "vu_distintos": [
   417619,
   711194
  ],
  "descripcion": "TUBERIA CONCRETO D=18\" CL. II SIN REFUERZO (INCLUYE SUMINIST"
 },
 {
  "codigo": "4892",
  "filas": [
   418,
   475,
   519,
   558
  ],
  "vu_distintos": [
   347749,
   802152
  ],
  "descripcion": "TUBERIA CONCRETO ALTA RESISTENCIA D= 10\" (INCLUYE SUMINISTRO"
 },
 {
  "codigo": "8737",
  "filas": [
   514,
   553
  ],
  "vu_distintos": [
   8324,
   8342
  ],
  "descripcion": "ADAPTADOR TERMINAL CAMPANA PVC D=2\" (Suministro e Instalació"
 },
 {
  "codigo": "8643",
  "filas": [
   265,
   317,
   369,
   426
  ],
  "und_v4": [
   "M2"
  ],
  "und_contractual": "M2/MES",
  "descripcion": "Proyecto: factibilidad, estudios y diseños de aceras, ciclor"
 }
]
```
</details>

**A-24 · Los VU de V4 están +49,0 % (mediana) sobre los VU pactados en la propuesta (15.086.222.761 con AIU) y +4,2 % sobre el APU actualizado de 2024 (3.639.050.739 en 367 renglones con Δ > 2 %)** [ALTA · ABIERTO · precios]

La hoja PRESUPUESTO CONTRACTUAL MAYO 25 trae tres VU por código: I (oficial IDU 2021), M (propuesta VICON = VU pactado) y Q (APU actualizado con insumos VISOR 13-09-2024). Frente a M: 469 renglones, mediana 49.0 %, valor V4 44.046.009.245 frente a 28.959.881.218 si se valorara al VU pactado (Δ 15.086.222.761). Frente a Q: 367 renglones con Δ > 2 %, efecto 3.639.050.739 a cantidades finales. Dato clave: el valor actual de obras del contrato (N688 = 44.303.294.799 = H × L) ya está calculado con los VU de V4, así que la actualización de precios se formalizó ANTES de esta solicitud (el libro externo se llama 'EJERCICIO ACTUALIZACIÓN IDU / ANEXO MODIF'). La pregunta no es si V4 cambia los precios (no lo hace dentro de V4: N y M usan el mismo K) sino con qué acto se pasó de los VU pactados a los actualizados y si ese mayor valor cuenta como adición para el tope del 50 %.

*Cómo lo trata el análisis:* Sección H (precios) muestra las dos referencias y exporta CSV; hallazgos H03 y H04 del análisis 04; el simulador permite valorar al VU de referencia de 2024.

*Verificable con:* `python analisis/scripts/analisis_04.py → resumen_vu_propuesta, desviaciones_vu_contractual`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "codigo_idu": "7785",
  "row": 34,
  "K_v4": 1132473.0,
  "K_propuesta": 643402.0,
  "delta_pct": 76.01,
  "cant_final": 9851.224192000001,
  "impacto_aiu": 6352416347,
  "valor_v4_aiu": 14709394807,
  "valor_a_vu_pactado_aiu": 8356980655
 },
 {
  "codigo_idu": "6016",
  "row": 20,
  "K_v4": 134985.0,
  "K_propuesta": 96609.0,
  "delta_pct": 39.72,
  "cant_final": 14162.699999999997,
  "impacto_aiu": 716609567,
  "valor_v4_aiu": 2520620695,
  "valor_a_vu_pactado_aiu": 1804016401
 },
 {
  "codigo_idu": "3017",
  "row": 14,
  "K_v4": 41825.0,
  "K_propuesta": 31579.0,
  "delta_pct": 32.45,
  "cant_final": 52468.569999999985,
  "impacto_aiu": 708810953,
  "valor_v4_aiu": 2893431761,
  "valor_a_vu_pactado_aiu": 2184633849
 },
 {
  "codigo_idu": "5182",
  "row": 531,
  "K_v4": 421190.0,
  "K_propuesta": 284569.0,
  "delta_pct": 48.01,
  "cant_final": 3912.249999999999,
  "impacto_aiu": 704726981,
  "valor_v4_aiu": 2172609354,
  "valor_a_vu_pactado_aiu": 1467880112
 },
 {
  "codigo_idu": "3425",
  "row": 85,
  "K_v4": 76194.0,
  "K_propuesta": 50583.0,
  "delta_pct": 50.63,
  "cant_final": 15468.629999999994,
  "impacto_aiu": 522342337,
  "valor_v4_aiu": 1553994038,
  "valor_a_vu_pactado_aiu": 1031649341
 },
 {
  "codigo_idu": "3895",
  "row": 399,
  "K_v4": 5181513.0,
  "K_propuesta": 3209926.0,
  "delta_pct": 61.42,
  "cant_final": 194.0,
  "impacto_aiu": 504306442,
  "valor_v4_aiu": 1325363962,
  "valor_a_vu_pactado_aiu": 821057470
 },
 {
  "codigo_idu": "8643",
  "row": 317,
  "K_v4": 50435.0,
  "K_propuesta": 34574.0,
  "delta_pct": 45.88,
  "cant_final": 18442.509999999995,
  "impacto_aiu": 385680279,
  "valor_v4_aiu": 1226390030,
  "valor_a_vu_pactado_aiu": 840701818
 },
 {
  "codigo_idu": "8643",
  "row": 369,
  "K_v4": 50435.0,
  "K_propuesta": 34574.0,
  "delta_pct": 45.88,
  "cant_final": 17457.17,
  "impacto_aiu": 365074288,
  "valor_v4_aiu": 1160866891,
  "valor_a_vu_pactado_aiu": 795785094
 }
]
```
</details>

**A-25 · El valor inicial del contrato fue 50.793.789.333, no 59.426.575.199: el 'valor actual' ya trae +8.632.785.866 (+17,0 %) y con la solicitud el acumulado llega a 48,5 % del inicial** [ALTA · ABIERTO · trazabilidad]

La hoja PRESUPUESTO CONTRACTUAL MAYO 25 (fila 279) muestra el COSTO TOTAL DEL PROYECTO de la licitación y de la propuesta: 50.793.789.333 (coincide con el boletín del IDU de 2021: $50.793M de obra). Su columna T ('actualizada por insumos VISOR 13-09-2024') llega a 58.748.569.461 e incluye tres adiciones previas para la fase de obras iniciales y gestiones preliminares (adiciones 1, 2 y 3 repartidas en SST, diálogo, PMT y fase inicial: 12 renglones que suman 1.024.988.000; la 'adición 3' está ajustada al VISOR del 19-06-2024). El libro radicado toma como 'valor actual' 59.426.575.199 (M705). Entre la propuesta y el valor actual: obras+redes pasan de 28.420.960.042 a 44.303.294.799 (+55.9 % con las MISMAS cantidades contractuales H: es efecto precio, ver A-24) y el fondo de compensaciones pasa de 10.721.788.800 a 0. Para el tope del 50 % del art. 40 de la Ley 80 la base es el valor inicial: 8.632.785.866 previos + 16.000.000.000 solicitados = 24.632.785.866 = 48.5 % en pesos nominales (margen 764.108.800); en SMMLV el resultado depende de la fecha de cada adición previa, que el libro no trae.

*Cómo lo trata el análisis:* La app corrige el chequeo del tope (B-11): base $50.793.789.333, incremento previo $8.632.785.866 contado íntegramente como adición (supuesto conservador) y escenario en SMMLV con el incremento previo a SMMLV 2025.

*Verificable con:* `openpyxl: wb['PRESUPUESTO CONTRACTUAL MAYO 25']['O279'].value`

<details><summary>Evidencia (primeras filas)</summary>

```json
[
 {
  "concepto": "Obras civiles + redes con AIU (A)",
  "fila": 246,
  "oficial_K": 30985979786.0,
  "propuesta_O": 28420960042.0,
  "actualizado_T": 44179372800.0,
  "V0_actual": 44303294799.0,
  "V4": 58196933800.0
 },
 {
  "concepto": "SST (B)",
  "fila": 248,
  "oficial_K": 1901484913.0,
  "propuesta_O": 1901484913.0,
  "actualizado_T": 2565369055.0,
  "V0_actual": 2943115324.0,
  "V4": 4110277014.0
 },
 {
  "concepto": "Diálogo ciudadano (C)",
  "fila": 252,
  "oficial_K": 1093605003.0,
  "propuesta_O": 1093605003.0,
  "actualizado_T": 1436153211.0,
  "V0_actual": 1874965632.0,
  "V4": 2430023370.0
 },
 {
  "concepto": "PMT (D)",
  "fila": 256,
  "oficial_K": 927168448.0,
  "propuesta_O": 927168448.0,
  "actualizado_T": 1319123175.0,
  "V0_actual": 1623435591.0,
  "V4": 2007577162.0
 },
 {
  "concepto": "Ajustes por cambio de vigencia (E)",
  "fila": 262,
  "oficial_K": 4555525079.0,
  "propuesta_O": 4555525079.0,
  "actualizado_T": 4555525079.0,
  "V0_actual": 4555525079.0,
  "V4": 4555525079.0
 },
 {
  "concepto": "Actividades acero (F)",
  "fila": 264,
  "oficial_K": 2460542988.0,
  "propuesta_O": 2460542988.0,
  "actualizado_T": 2955324081.0,
  "V0_actual": 2977517840.0,
  "V4": 2977517840.0
 },
 {
  "concepto": "Fondo de compensaciones (K)",
  "fila": 277,
  "oficial_K": 8156769056.0,
  "propuesta_O": 10721788800.0,
  "actualizado_T": 0.0,
  "V0_actual": 0.0,
  "V4": 0.0
 },
 {
  "concepto": "Fase de obras iniciales (I)",
  "fila": 270,
  "oficial_K": 322727460.0,
  "propuesta_O": 322727460.0,
  "actualizado_T": 322727460.0,
  "V0_actual": 758734334.0,
  "V4": 758734334.0
 }
]
```
</details>


## B · Correcciones hechas al análisis

| ID | Sev. | Commit | Qué estaba mal | Qué se hizo |
|---|---|---|---|---|
| B-01 | ALTA | `cf7bdd7` | La app no cargaba ('Cargando…' indefinido) con el JSON consolidado | clasificacion.totales es un objeto y el código lo recorría como arreglo (forEach). Se agregó Array.isArray antes de iterar. |
| B-02 | ALTA | `cf7bdd7` | La tabla de ítems mostraba $0 en todas las columnas de valor | Los campos del JSON (K_vu_cd, L_vu_cd_aiu, M_valor_final, N_valor_inicial) no coincidían con los que leía la app; se creó _p75NormalizeItems para unificar nombres. |
| B-03 | ALTA | `cf7bdd7` | Costo por CIV: Δ V4 − V2 comparaba el total con componentes contra las obras de V2, y el % NP iba multiplicado por 100 | El CIV 9004002 mostraba +$413M cuando la diferencia real de obras es −$215.494.094. Se usa delta_v4_v2 (obras vs obras) y el porcentaje se divide por 100. |
| B-04 | ALTA | `cf7bdd7` | El CIV 500002375 tenía línea base $0 por el alias de identificador | La hoja usa 500002375; data.json usa 50002375 y la comparativa 16004876. Se creó el alias y la línea base por CIV se ancló a la columna H repartida con la participación de data.json; 40 renglones sin reparto ($2.460.223.472) quedan explícitos en la conciliación. |
| B-05 | MEDIA | `ad5b438` | El waterfall incluía la fila TOTAL GENERAL y duplicaba los totales; los negativos en miles de millones perdían el signo | WF() filtra la fila total; fmtB respeta el signo; los códigos 'NO'/'N/A' de los NP se excluyen del conteo de repetidos; se corrigió una precedencia ||/+ en el explorador. |
| B-06 | BAJA | `5cb90b9` | Prioridad de revisión demasiado estricta (5 ítems 'Alta') y desbordes en móvil | La prioridad pasó a materialidad (|Δ| en miles de millones) → 48 ítems Alta; grid minmax(min(480px,100%),1fr); padding superior en gráficas para las etiquetas. |
| B-07 | ALTA | `0a1bae6` | Análisis 06: todas las referencias de fila estaban desplazadas (+4 en la hoja principal, +5 en PRESUPUESTO 63 mm) | El JSON y el MD del análisis 06 se escribieron a mano por el agente sin verificar contra openpyxl. corregir_06.py remapea 692→688, 696→692, …, 707→703, 733-742→729-738, 657→652 (63 mm), etc., y deja meta_correcciones. Las filas reales se verificaron celda a celda. |
| B-08 | ALTA | `0a1bae6` | H06-01 afirmaba un 'riesgo de doble pago en acero por $2.977M–$3.053M' que el libro no sustenta | La premisa era que el bloque ACEROS estaba 'cargado dentro de obras'. M688 = SUM(M8:M679) y CB688 = SUM(CB7:CB679)/2 excluyen las filas 680-687: no hay doble conteo en el Excel. El hallazgo se reescribe como MEDIA con impacto = diferencia bloque − bolsa F (75.469.677) y pregunta de cuál rige. Se ajustan resumen ejecutivo, XP, checklist e informe. |
| B-09 | MEDIA | `0a1bae6` | Análisis 04: dos falsos positivos de consistencia entre hojas y 16 'duplicados reales' que no lo eran | EJECUTIVO!H56 (59.426.575.199) es el valor actual del contrato, no el total de obras; Presupuesto estimado!A11 (74.667.840.865) excluye por definición la fase de obras iniciales (758.734.334). Los subcapítulos se truncaban a 50 caracteres y '…A CARGO DEL IDU' se confundía con '…A CARGO DE LA ESP'. H02 pasa de ALTA a INFO y H04 de MEDIA a INFO; las diferencias explicadas quedan en observaciones_hojas. |
| B-10 | INFO | `0a1bae6` | Consolidado de hallazgos recontado | Tras B-07 a B-09 y B-12 el consolidado pasó de 44 ALTA / 16 MEDIA / 4 BAJA / 6 INFO a 44 / 15 / 4 / 8 (71); con B-14 queda en 44 / 18 / 4 / 8 (74). Ninguna cifra del waterfall, de la variación por ítem ni del costo por CIV cambia. |
| B-11 | ALTA | `0a1bae6` | El chequeo del tope del 50 % (Ley 80 art. 40) usaba $59.426.575.199 como 'valor inicial' | El valor inicial del contrato es $50.793.789.333 (hoja PRESUPUESTO CONTRACTUAL MAYO 25 fila 279 = boletín IDU 2021); el 'valor actual' ya incluye $8.632.785.866 de incremento. normCheck() pasa a usar la base original y a acumular el incremento previo: 48,5 % nominal (antes se mostraba 26,9 %) y ~54 % del tope en SMMLV si el incremento previo se cuenta a SMMLV 2025. Tarjeta, ficha legal, XP y lista de chequeo actualizados; la duda queda como C-01. |
| B-12 | ALTA | `0a1bae6` | El análisis 04 llamaba 'VU contractual' a la columna Q (APU actualizado 13-09-2024) y truncaba la lista a 200 renglones | El VU pactado en el contrato es la columna M (propuesta VICON). Se agrega la comparación contra M (H04 nuevo: mediana +49,0 %, $15.086M con AIU), se retitula H03 y se guardan las listas completas (367 renglones vs referencia 2024; la sección H de la app mostraba 200 y un total de $3.259M que ahora es el total real). |
| B-13 | MEDIA | `0a1bae6` | 'Trasladado' de las reubicaciones (sección I e informe 8C) usaba el valor completo de los renglones | Se computaba min(Σ N de las filas que bajan, Σ M de las filas que suben), lo que contaba renglones que solo disminuyen o solo aumentan como si se movieran enteros ($6.462.266.802). Ahora trasladado = min(valor que sale, valor que entra), calculado en analisis_01 (campos valor_disminuido / valor_aumentado / trasladado): $5.807.343.956 en 32 códigos. Cambian 'eliminación real' y 'alcance nuevo real' del informe 8C. |
| B-14 | MEDIA | `git log --grep=B-14` | Análisis 02: las métricas de intensidad de obra por m² (rajón, andén, MD12, BG_A) daban 0 en los 27 CIV | El script buscaba "1005", "3039", "2002" y "1012" como código IDU, pero son números de ítem sin punto (y 1.005 no es el rajón). Solo la métrica MD19 (buscada por NP-123) tenía datos, por eso la tabla "Intensidad de obra por m²" de cada ficha de CIV mostraba 0,000. Ahora se buscan por código IDU verificado: rajón 6016, andén 3425, mezcla asfáltica MD12 6313 + NP-123 8618 y base granular BG_A 4158 + NP-124 4744 (los contractuales fueron reemplazados por los NP). Los atípicos pasan de 2 a 5 hallazgos MEDIA (H02-200 a H02-204); el más alto es el andén del CIV 16000013 (5,5× la mediana). Ninguna cifra monetaria cambia. |

## C · Dudas abiertas para el contratista / IDU

| ID | Sev. | Para | Pregunta | Por qué importa | Soporte a pedir |
|---|---|---|---|---|---|
| C-01 | ALTA | IDU | ¿Cuáles otrosíes llevaron el contrato de $50.793.789.333 (propuesta 2021) a $59.426.575.199 y qué parte de esos $8.632.785.866 es adición (cuenta para el tope del 50 %) y qué parte reajuste o actualización de precios? | A-25: con la solicitud el acumulado nominal es 48,5 % del valor inicial; en SMMLV depende de la fecha de cada adición previa. | Historial de otrosíes y adiciones del contrato 1752-2021 con valores, fechas y naturaleza; CDP/RP. |
| C-02 | ALTA | Contratista | ¿Qué APU y qué fecha de insumos (VISOR) sustentan los VU de V4? ¿Están aprobados? | A-01, A-03 y A-24: el efecto precio es +$3.259M en 200 ítems. | Libro APU 28-07-2025; FO-GI-19 por ítem; acta de aprobación de VU. |
| C-03 | ALTA | Contratista | ¿Qué obra es el código 8643 (5.037) por $2.718M con descripción de 'factibilidad, estudios y diseños'? | A-06. | Especificación, APU y memoria por CIV. |
| C-04 | ALTA | Contratista | ¿Cuál es la fecha de terminación vigente y el plazo ejecutado? Sin ella no se puede juzgar si 8 meses son suficientes para $16.000M (ritmo de $2.000M/mes, 3,3 veces el histórico). | H06-03. | Cronograma vigente, curva S y facturación mensual certificada de los últimos 24 meses. |
| C-05 | ALTA | Contratista | ¿La adición incluye ajustes por cambio de vigencia 2027? ¿Con qué fórmula? | A-07. | Cálculo GUDP017 / ICCP por vigencia. |
| C-06 | MEDIA | Contratista | ¿Cuál es el total oficial del subgrupo 5: BY688 (…071,5) o la suma de CIVs (…244.367)? | A-04. | Libro con totales por CIV recalculados. |
| C-07 | MEDIA | Contratista | ¿El bloque ACEROS es la memoria de la bolsa F o alcance adicional? ¿Cuál rige para pagar? | A-05 / H06-01. | Memoria de acero conciliada y constancia en el otrosí. |
| C-08 | MEDIA | Contratista | ¿Cuáles de los 84 NP siguen objetados por la interventoría? La hoja 'NPs Objetados' se cruza por descripción, no por código. | Limitación D-05. | Lista de NP objetados con código, estado y fecha. |
| C-09 | MEDIA | Contratista | ¿Cuál es la cantidad contractual por CIV (columna H desagregada)? El libro solo trae el total. | Limitación D-01: la línea base por CIV es reconstruida. | Presupuesto contractual por CIV (matriz ítem × CIV de la firma). |
| C-10 | MEDIA | Contratista | ¿Qué compensaciones financiaba el fondo de V2 ($5.943M) y dónde quedaron? | A-09. | Trazabilidad V2→V3→V4 del componente K. |
| C-11 | MEDIA | Contratista | ¿Qué es el libro 'PRESUPUESTO TOTAL $80 MIL.xlsx' al que están vinculadas las cantidades del NP-101? | A-02. | Copia del libro y explicación de la versión. |
| C-12 | MEDIA | Contratista | ¿Los 68 renglones NP en cero y los 3 NP sin cantidad se retiran del anexo? | A-15. | Anexo depurado. |
| C-13 | BAJA | Contratista | ¿El contratista renuncia a pedir bioseguridad por los 8 meses o se incorpora? | A-08. | Comunicación expresa. |
| C-14 | BAJA | Contratista | Corregir O690, rótulos con fecha de mayo, 'SISETE' y decimales en totales antes de anexar el libro al otrosí. | A-10, A-13, A-14, A-20. | Libro corregido. |
| C-15 | BAJA | Interventoría | ¿Los 9 CIV 'no alcanza' de la Alternativa 2 siguen fuera del alcance con la adición o vuelven a entrar? | El simulador (sección J) los excluye por −$19.511M de obras. | Acta de alcance por CIV firmada. |
| C-16 | BAJA | IDU | ¿Rige el SMMLV 2026 del Decreto 1469/2025 o el transitorio, para convertir el tope del 50 %? | El decreto está suspendido provisionalmente (12-02-2026). | Concepto jurídico del IDU. |

## D · Limitaciones del análisis

| ID | Sev. | Limitación | Detalle |
|---|---|---|---|
| D-01 | ALTA | La línea base (cantidad contractual) por CIV es reconstruida, no radicada | El Excel trae la cantidad contractual solo como total del renglón (columna H). El análisis 02 la reparte por CIV con la participación de cada CIV en el VISOR de mayo de 2025 (data.json). 40 renglones no tienen participación (código nuevo o sin CIV en el VISOR) y suman 2.460.223.472 que quedan sin repartir y se muestran aparte. Toda cifra 'Δ por CIV' hereda este supuesto; el Δ total por renglón no. |
| D-02 | ALTA | Los valores del Excel son los guardados; el libro no se recalculó | Se lee con openpyxl (data_only). Los VU y algunas cantidades dependen de libros externos ausentes (A-01, A-02), así que ni el analista ni el revisor pueden recalcular el libro completo. Si Excel actualiza vínculos sin los archivos, mostrará #REF!. |
| D-03 | MEDIA | El cruce con V1 (IDU 25-02-2026) y V2 (VICON 21-04-2026) se hace por código IDU agregado y en costo directo | comparativa.json no tiene renglones por subcapítulo ni por CIV. Un código que en V4 está en varias filas se compara con su suma. Las cifras V1/V2 se llevan a AIU con 1,31849 (V4) aunque V1 y V2 tenían su propio AIU (34,01 % en el VISOR de mayo). |
| D-04 | MEDIA | La comparación de precios (sección H) cubre 200 de 649 renglones | Solo los códigos con VU en la hoja PRESUPUESTO CONTRACTUAL MAYO 25 (columna 'actualización APU 13-09-2024') o en el VISOR 07-05-25. Los NP no tienen referencia contractual: su VU se compara solo con V2. |
| D-05 | MEDIA | La hoja 'NPs Objetados' se cruza por descripción normalizada, no por código | El estado 'objetado' de un NP en la app es indicativo. Confirmar con la lista oficial (C-08). |
| D-06 | MEDIA | Los componentes (SST, diálogo, PMT, etc.) se reparten por CIV en proporción al costo directo de obras | Es una convención del análisis para llegar a un 'costo total por CIV'; el contratista no reparte componentes por CIV. Usar solo para comparar CIVs entre sí. |
| D-07 | MEDIA | Las áreas por CIV para el $/m² provienen del dashboard (data.json: longitud × ancho) | Son las áreas del VISOR de mayo de 2025, no las de diseño detallado. El $/m² sirve para detectar atípicos, no para tarifar. |
| D-08 | MEDIA | Los índices 'atención' y 'prioridad' y el simulador son heurísticos del analista | Pesos declarados en la app (ATT_W, itemPriority, SIM). Cambiarlos cambia el orden, no las cifras de origen. El simulador es ilustrativo: no sustituye el recálculo del contratista. |
| D-09 | MEDIA | El marco normativo se consultó el 27-09-2026 y puede cambiar | Fuentes públicas (Ley 80/1993, Ley 1474/2011, CCE C-466/2024, Consejo de Estado exp. 67.508, manuales IDU MG-GC-06 v19, GUDP017, PR-IC-01). El MG-GC-01 no pudo leerse. El SMMLV 2026 (Decreto 1469/2025) está suspendido provisionalmente: el tope del 50 % se muestra con ambos escenarios. |
| D-10 | BAJA | El análisis 05 (NPs) y el 06 (versiones) usan datos de V2 que ya fueron objeto de conciliación en abril | Las cifras de V2 vienen de comparativa.json (trabajo de abril de 2026); si ese archivo se corrige, deben regenerarse 05 y 06. |
| D-11 | BAJA | El repositorio y la página son públicos; la clave de acceso de la app es solo de interfaz | Los JSON y el informe pueden descargarse sin autenticación desde GitHub Pages. No publicar aquí datos que el contrato o la ley protejan; el Excel fuente no está en el repositorio (está en .gitignore) y se identifica solo por su SHA-256. |
| D-12 | BAJA | Redondeos | Las verificaciones aceptan Δ ≤ $100 (redondeo por CIV) y $86.217 (fila 34). Ninguna cifra del informe se redondea salvo donde se indica 'M' (millones). |

## Paquete de auditoría

- Fuente: `4. PRESUPUESTO 01-09-2026 75MM (8 MESES).xlsx` · 7,260,184 bytes · SHA-256 `e17f0f39efe2288d4fb56f340b5e95a4445b0b9cc3ee9b7b170fc885514f570a` · 18 hojas (15 ocultas) · 190 vínculos externos.
- Salidas (SHA-256):

| Archivo | SHA-256 | Bytes |
|---|---|---:|
| `analisis_2026_09.json` | `0b7894909eafa31cbc4a87b00582755b9198f1c702bcafea01ea50a43a6573b2` | 1,951,648 |
| `presupuesto_2026_09.json` | `2bf751263eeb5c3c36a61096a6af52102d97dd3aef686077b1d48b144086e41a` | 862,572 |
| `comparativa.json` | `e35372944224d32737df991b6b319604716d775dbc998102a20214a4125706af` | 1,428,481 |
| `data.json` | `80279d1a8a41039f20ef9cc40e48d0425fe55a285940c2062a4a5bf91abe31b7` | 161,267 |
| `analisis/Analisis_Presupuesto_2026-09.xlsx` | `66c26c6fd23fd307a81250f5a8abbeb3ab92f54a42523862483310b69accc73c` | 94,208 |
| `analisis/INFORME_PRESUPUESTO_2026-09.md` | `c9a5c86c0ee31e15cb89ad935d1a8ea38970e13ef8ca6a25691155fe43164a51` | 36,907 |
| `analisis/hallazgos/01_variacion_items.json` | `7c30fab4d00c7143cceea60c08b72695b69631139a009cc3e3cf78af9c586850` | 781,490 |
| `analisis/hallazgos/02_variacion_civ.json` | `f00863768213976eaaeee1f580f86a2734ea25c2df610c3304f4be6344f98378` | 1,293,368 |
| `analisis/hallazgos/03_costo_civ.json` | `3d6b9de83e041e8db5f127a0aee71883e8847b281604352902b878f951d5ade3` | 76,227 |
| `analisis/hallazgos/04_aritmetica.json` | `ffc6f3f04def42aba9faf9d037fb056fe31198f25c66693387b42722b19cbefc` | 236,439 |
| `analisis/hallazgos/05_nps.json` | `72e6b7fe22254a866be3c1ee91eaab5cd4c6d0f70c637e03aa9535c426951bbd` | 98,516 |
| `analisis/hallazgos/06_versiones_plazo.json` | `82cf990357769c5fe09f00d936eee5d50f2da58815621e616543a15520325b6c` | 25,437 |

- Entorno: Python 3.11.15 · openpyxl 3.1.5 · Linux-6.18.44-fc-v42-x86_64-with-glibc2.39 · commit base `7f1709e` (main).
- Tolerancias aceptadas: Σ CIV vs M688 ≤ $100 (real +69); fila 34 $86.217; waterfall y NP al peso.
- Reproducir todo:

```bash
pip install openpyxl num2words   # (pandas y xlsxwriter para generar_excel.py)
python analisis/scripts/extraer_presupuesto.py      # Excel -> analisis/datos/hojas/*.csv + presupuesto_2026_09.json
python analisis/scripts/analisis_01_variacion_items.py
python analisis/scripts/analisis_02_variacion_civ.py
python analisis/scripts/analisis_03_costo_civ.py
python analisis/scripts/analisis_04.py
python analisis/scripts/analisis_05_nps.py
python analisis/scripts/corregir_06.py               # corrige filas y H06-01 del análisis 06 (idempotente)
python analisis/scripts/consolidar.py
python analisis/scripts/generar_excel.py
python analisis/scripts/verificacion.py   # debe terminar en 'VERIFICACION COMPLETA' con todos [OK ]
python analisis/scripts/auditoria.py                 # este registro
```

*Cada asiento B indica el commit de git que introdujo la corrección; `git show <commit>` muestra el cambio exacto.*
