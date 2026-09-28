# 06 — Waterfall de versiones, componentes y plazo (8 meses)

**Contrato IDU 1752-2021 · Consorcio Montevideo 045 (Interventoria)**
Analisis del transito V0 → V1 → V2 → V3 → V4 y verificacion de la adicion de $16.000M / 8 meses solicitada por VICON el 01-09-2026.

> **Corrección 2026-09-28 (registro de auditoría B-07 y B-08).** Las referencias de fila de este documento y de `06_versiones_plazo.json` estaban desplazadas +4 en la hoja principal y +5 en la hoja PRESUPUESTO 63 mm; se corrigieron a las filas reales verificadas con openpyxl (`analisis/scripts/corregir_06.py`). El hallazgo H06-01 afirmaba que el bloque ACEROS estaba "cargado dentro de obras": la fórmula `M688 = SUM(M8:M679)` demuestra que el bloque (filas 680-687) está fuera del total, así que no hay doble conteo en el libro. H06-01 pasa de ALTA a MEDIA y su impacto es la diferencia bloque − bolsa F (75.469.677). El texto original se conserva en el historial de git (commit 5cb90b9 y anteriores).

---

## 1. Waterfall por componente (5 versiones)

Todas las cifras en pesos con AIU incluido, salvo donde se indique CD (costo directo).

| Componente | V0 firma | V1 IDU 25-02-2026 | V2 VICON 21-04-2026 | V3 63MM (3 meses) | V4 75MM (8 meses) | Δ V0→V4 |
|---|---:|---:|---:|---:|---:|---:|
| Obras + redes + acero (AIU) | 44.303.294.799 | 49.473.142.875 | 55.282.021.446 | 47.836.306.969 | **58.196.933.800** | **+13.893.639.001** |
| PMA-SST (AIU 20,006%) | 2.943.115.324 | 2.914.808.177 | 3.672.443.894 | 3.380.795.309 | **4.110.277.014** | **+1.167.161.690** |
| Dialogo ciudadano (PGS) | 1.874.965.632 | 1.801.692.069 | 2.339.597.783 | 2.083.112.282 | **2.430.023.370** | **+555.057.738** |
| Plan Manejo Trafico (PMT) | 1.623.435.591 | 1.570.849.611 | 2.025.736.496 | 1.767.488.681 | **2.007.577.162** | **+384.141.571** |
| Ajustes cambio vigencia (E) | 4.555.525.079 | 4.555.525.079 | 4.555.525.079 | 4.555.525.079 | 4.555.525.079 | 0 |
| Actividades acero (bolsa F) | 2.977.517.840 | 0 | 2.977.517.840 | 2.977.517.840 | 2.977.517.840 | 0 |
| Ensayos laboratorio (G) | 299.267.609 | 299.267.609 | 299.267.609 | 299.267.609 | 299.267.609 | 0 |
| SDA (H) | 31.328.679 | 31.328.679 | 31.328.679 | 31.328.679 | 31.328.679 | 0 |
| Fase obras iniciales (I) | 758.734.334 | 705.883.518 | 758.734.334 | 758.734.334 | 758.734.334 | 0 |
| Bioseguridad (J) | 59.390.312 | 59.390.312 | 59.390.312 | 59.390.312 | 59.390.312 | 0 |
| Fondo compensaciones (K) | 0 | 0 | 5.942.657.520 | 0 | 0 | 0 |
| **TOTAL** | **59.426.575.199** | **61.411.887.929** | **77.944.220.992** | **63.749.467.094** | **75.426.575.199** | **+16.000.000.000** |

Diferencias entre etapas (totales):

| Transicion | Δ absoluto |
|---|---:|
| V0 → V1 | +1.985.312.730 |
| V1 → V2 | +16.532.333.063 |
| V2 → V3 | −14.194.753.898 |
| V3 → V4 | +11.677.108.105 |
| V0 → V4 | +16.000.000.000 |

**Fuentes**: hoja principal filas 688-707 (columnas M y N), hoja PRESUPUESTO 63 mm filas 652-671, `comparativa.json` claves `globales.contrato_original_firma`, `globales.iniciales`, `globales.actualizadas_alt1`.

Verificacion al peso del total V4: 58.196.933.800 + 4.110.277.014 + 2.430.023.370 + 2.007.577.162 + 4.555.525.079 + 2.977.517.840 + 299.267.609 + 31.328.679 + 758.734.334 + 59.390.312 + 0 = **75.426.575.199** ✓

---

## 2. Que paso con el capitulo 7 DESVIOS

| Version | Valor cap 7 (CD) | Valor cap 7 (con AIU) |
|---|---:|---:|
| V0 firma | 247.686.413 | 326.577.225 |
| V1 IDU | 247.686.413 | 326.577.225 |
| V2 VICON Alt 1 | **19.347.297.314** | ≈25.500M |
| V3 63MM | 0 (item unico eliminado) | 0 |
| V4 75MM | 0 (col M) | 0 |

### El "salto" de V2 a 19.347M

En V2 el capitulo 7 acumulo 19.347M **NO** porque hubiese desvios reales de esa magnitud, sino porque el contratista **metio dentro del capitulo 7 los componentes contractuales no-obra**. Segun `comparativa.json → items_alt1.by_chapter."7. DESVÍOS"`, los 14 items del capitulo 7 en V2 eran:

- Ajustes cambio vigencia: 4.555.525.079
- Ambiental-SST bolsa: 3.672.443.894
- Actividades acero bolsa: 2.977.517.840
- Dialogo ciudadano bolsa: 2.339.597.783
- PMT bolsa: 2.025.736.496
- Fase obras iniciales: 758.734.334
- Laboratorio: 299.267.609
- Bioseguridad: 59.390.312
- SDA: 31.328.679
- Acero refuerzo (item 3708 agregado x2): 1.339.886.672 + 292.524.251
- Acero liso (item 4959 agregado): 259.362.735
- Malla electrosoldada (item 8471 agregada): 735.981.630
- Rutinario (item 6184 eliminado): −247.686.413

Total: 19.347.297.314 CD.

### La conciliacion en V4

En V3 y V4 la contabilidad se reordeno: los componentes contractuales volvieron a estar como bolsas independientes fuera del capitulo 7 (filas 692-701 en V4), y del capitulo 7 solo quedo el item 7.001 (mantenimiento rutinario) que se elimino por completo (13.481 m² → 0 m², balance −326.577.225).

**Conclusion**: la caida cap 7 V2→V4 no es "eliminacion de sobreproyeccion" sino **RECLASIFICACION contable**. El unico item realmente removido es el mantenimiento rutinario 6184 por −326.577.225 con AIU.

---

## 3. Detalle A-E del componente SST (8 meses) — filas 729-738

| Componente | Valor CD |
|---|---:|
| A. Personal | 636.053.253 |
| B. Actividades constructivas | 99.385.568 |
| C. Manejo vegetacion y paisaje | 62.056.927,47 |
| D. Gestion SST | 149.578.289,07 |
| E. Plan de senalizacion | 25.512.074,67 |
| **Subtotal A+B+C+D+E (CD)** | **972.586.112,21** |
| AIU 20,006% | 194.575.577,61 |
| **Total mensual x 8 meses (con AIU)** | **1.167.161.689,81** |

Verificacion:
- Subtotal ABCDE = 972.586.112,21 ✓
- 972.586.112,21 × 1,20006 = 1.167.161.689,81 ✓
- 1.167.161.689,81 / 8 = 145.895.211,23 (costo/mes con AIU, fila 737) ✓
- V0 PMA-SST 2.943.115.324 + delta 8 meses 1.167.161.690 = **4.110.277.014** = V4 PMA-SST ✓

### AIU 20,006% vs AIU contractual 31,849% en obras

El AIU aplicado a obras+redes+acero es 31,849% (contractual pleno = Administracion + Imprevistos + Utilidad). Los componentes de acompañamiento tienen AIU diferenciados:

- PMA-SST: **20,006%** (delta 11,843 pp vs obras)
- Dialogo ciudadano: **19,566%**
- PMT: **19,566%**

**Motivo**: en la matriz IDU los componentes de acompañamiento (SST, PGS, PMT) son bolsas de personal e insumos que no llevan el riesgo constructivo pleno. Se les elimina el componente Imprevistos (~5%) y se aplica una utilidad parcial. Esta diferenciacion esta prevista contractualmente y confirmada en la fila 736 del presupuesto (rotulos "AIU 20,006%" para SST y "AIU 19,566%" para PGS/PMT).

---

## 4. Componentes que NO crecen (V0 = V4)

| Componente | V0 | V4 | Δ | Motivo |
|---|---:|---:|---:|---|
| Ensayos laboratorio (G) | 299.267.609 | 299.267.609 | 0 | Bolsa fija con IVA, dimensionada sobre el alcance total, no sobre el plazo. Fila 696. |
| SDA (H) | 31.328.679 | 31.328.679 | 0 | Bolsa fija de tarifas SDA. No cambia con plazo. Fila 698. |
| Fase obras iniciales (I) | 758.734.334 | 758.734.334 | 0 | Bolsa ya causada al inicio del contrato. Fila 701. |
| Bioseguridad (J) | 59.390.312 | 59.390.312 | 0 | El contratista no solicito adicion pese a ser proporcional al plazo. Fila 699. |
| Ajustes cambio vigencia (E) | 4.555.525.079 | 4.555.525.079 | 0 | Indexacion unica pactada desde firma. Fila 695. |
| Actividades acero (F) | 2.977.517.840 | 2.977.517.840 | 0 | Bolsa fija contractual con AIU y cambio de vigencia. Fila 697. El bloque ACEROS (filas 680-687) está fuera del total de obras (M688 = SUM(M8:M679)). |
| Fondo compensaciones (K) | 0 | 0 | 0 | Aparecio en V2 (5.942.657.520) y desaparecio en V3-V4. Fila 700. |

**Observacion**: el hecho de que Bioseguridad no se actualice a 8 meses (H06-04) es un renglon con potencial impacto MEDIA (~$40M) porque los insumos EPP y protocolos escalan con el tiempo.

---

## 5. Diferencia del acero: 75.469.677

Bloque interno acero (filas 680-687 en V4):

| Fila | Item | Descripcion | Cant V4 (kg) | Valor V4 |
|---:|---|---|---:|---:|
| 681 | (subtotal pavimentos) | Cabecera | | 2.667.280.349 |
| 682 | 3708 | Acero refuerzo (pavimentos) | 211.290,08 | 1.557.630.470 |
| 683 | 4959 | Acero liso 1 1/4" | 81.288,82 | 900.761.414 |
| 684 | 7713 | Dovelas 1 1/2" | 19.704,60 | 208.888.465 |
| 685 | (subtotal esp. publico) | Cabecera | | 385.707.168 |
| 686 | 3708 | Acero refuerzo (espacio publico) | 52.320,56 | 385.707.168 |
| 687 | 8471 | Malla electrosoldada | 0 | 0 |
| **Total bloque interno** | | | | **3.052.987.517** |

Componente fijo F (fila 697): **2.977.517.840**
Diferencia: **3.052.987.517 − 2.977.517.840 = 75.469.677**

### Explicacion de los 75.469.677

Los 75M no son un error aritmetico. Reflejan que **hay dos representaciones del acero en el mismo presupuesto**:

1. **Bloque ACEROS fuera del total de obras** (filas 680-687, con AIU 31,849%): detalle por CIV con las cantidades actualizadas y los VU vigentes al 01-09-2026. La fórmula `M688 = SUM(M8:M679)` no lo incluye, así que no está dentro de los 58.196.933.800.
2. **Bolsa fija F "Actividades acero"** (fila 697, 2.977.517.840): valor global pactado en el contrato original, incluye AIU y ajuste por cambio de vigencia.

La diferencia de 75.469.677 (2,5% de la bolsa) se explica porque las dos aproximaciones usan bases distintas: la bolsa F trae indexacion mientras el bloque interno usa VU actuales sin banda de vigencia.

### Bloque vs bolsa: qué rige (hallazgo H06-01, corregido)

Con las fórmulas actuales del libro no hay doble conteo: el bloque no está sumado en obras y la bolsa F es la única partida de acero dentro de los 75.426.575.199. El riesgo aparecería únicamente si el otrosí o las actas pagaran el acero por ítems y además la bolsa. La interventoría debe pedir por escrito cuál de las dos representaciones rige, justificar la diferencia de 75.469.677 y dejar constancia de que la otra no se factura.

---

## 6. Ritmo de ~$2.000M/mes

Adicion neta = $16.000.000.000 en 8 meses.

| Componente | Δ V0→V4 | % del delta |
|---|---:|---:|
| Obras | 13.893.639.001 | 86,84% |
| PMA-SST | 1.167.161.690 | 7,29% |
| Dialogo | 555.057.738 | 3,47% |
| PMT | 384.141.571 | 2,40% |
| **Suma** | **15.999.999.999** | 100,00% |

Verificacion al peso: **15.999.999.999** (diferencia de $1 con $16.000.000.000 por redondeo en el calculo de AIU sobre los CD).

Mensualidad implicita: 15.999.999.999 / 8 = **1.999.999.999**/mes = **$2.000M/mes**.

Mensualidad por componente:
- Obras: $1.736.704.875/mes
- PMA-SST: $145.895.211/mes
- Dialogo: $69.382.217/mes
- PMT: $48.017.696/mes
- Total: $1.999.999.999/mes

### ¿Puede el contratista sostener $2.000M/mes?

Segun `Hoja1` del propio archivo:
- Obra ya iniciada: $19.652M
- Obra por iniciar: $19.034M
- Obra "no alcanza": $19.511M

Si $19.652M se ejecutaron en aproximadamente 30 meses de contrato hasta hoy, el ritmo real historico es **~$650M/mes**. El ritmo propuesto de $2.000M/mes es **3,1x** el ritmo real historico.

**No hay evidencia en la hoja EJECUTIVO** de ejecucion mes a mes; solo un resumen por CIV. La Interventoria debe pedir cronograma detallado.

---

## 7. Que cambio de V3 a V4 (63MM → 75MM)

Delta total: **75.426.575.199 − 63.749.467.094 = 11.677.108.105**

| Componente | V3 | V4 | Δ | % del delta |
|---|---:|---:|---:|---:|
| Obras + AIU | 47.836.306.969 | 58.196.933.800 | +10.360.626.831 | 88,73% |
| PMA-SST (3→8 meses) | 3.380.795.309 | 4.110.277.014 | +729.481.705 | 6,25% |
| Dialogo (3→8 meses) | 2.083.112.282 | 2.430.023.370 | +346.911.088 | 2,97% |
| PMT (3→8 meses) | 1.767.488.681 | 2.007.577.162 | +240.088.481 | 2,06% |
| Otros | iguales | iguales | 0 | 0% |

### Efecto precio vs. efecto cantidad

Comparacion de VU (columnas K y L) en V3 vs V4 muestra que **los VU son practicamente identicos**:
- Item 1.001 replanteo: VU 833 CD / 1.098 CD+AIU en ambas versiones
- Item 1.002 demolicion pavimento: VU 35.570 / 46.899 en ambas
- Item 1.006 transporte escombros: VU 41.825 / 55.146 en ambas

**Conclusion**: el delta V3→V4 en obras (+$10.361M) no es efecto precio (reindexacion). Es **efecto CANTIDAD y agregacion de NPs**:
- Se incorporaron nuevos ítems y NPs que en V3 no estaban.
- Aumentaron cantidades en items existentes.
- La escalada V3 (3 meses) → V4 (8 meses) explica $1.316M de los bolsones SST/PGS/PMT, no obras.

---

## 8. Hallazgos y recomendaciones para Interventoria

Ver detalle completo en `06_versiones_plazo.json` clave `hallazgos`. Resumen:

| ID | Severidad | Titulo | Impacto |
|---|---|---|---:|
| H06-01 | MEDIA | Bloque ACEROS (fuera del total de obras) vs bolsa fija F: aclarar cuál rige y justificar 75.469.677 | $75,5M |
| H06-02 | ALTA | Cap 7 DESVIOS V2 era reclasificacion, no ahorro | $19.347M |
| H06-03 | ALTA | Ritmo $2.000M/mes es 3,1x el historico | $16.000M |
| H06-04 | MEDIA | Bioseguridad no se actualiza a 8 meses | ~$40M |
| H06-05 | MEDIA | Delta V3→V4 obras $10.361M sin sustento tecnico | $10.361M |
| H06-06 | MEDIA | Fondo Compensaciones aparece y desaparece sin trazabilidad | $5.943M |
| H06-07 | INFO | AIU diferenciados por componente confirmados | 0 |
| H06-08 | BAJA | Etiqueta fila 703 con fecha desactualizada (04-05-2026 en archivo 01-09-2026) | 0 |

### Recomendaciones concretas

1. **Antes de aprobar la adicion**: exigir tabla de conciliacion V2→V3→V4 por capitulo y por componente, explicando reclasificaciones vs cambios reales de alcance.
2. **Acero (H06-01)**: pedir por escrito al contratista si el bloque ACEROS es la memoria de la bolsa F o alcance adicional; dejar en el otrosí que el acero se paga por una sola vía.
3. **Ritmo mensual (H06-03)**: solicitar cronograma detallado con curvas S semana a semana, frentes de obra simultaneos y capacidad instalada. Comparar con facturacion certificada de los ultimos 24 meses.
4. **V3→V4 (H06-05)**: pedir la sustentacion tecnica del $10.361M adicional en obras en solo 4 meses (mayo → septiembre 2026).
5. **Fondo Compensaciones (H06-06)**: solicitar trazabilidad de por que se propuso en V2 y desaparecio; verificar que no se este pagando doble via NP-109/NP-110 arqueologia.
6. **Bioseguridad (H06-04)**: obtener del contratista renuncia expresa a solicitar adicion en este renglon para el plazo ampliado, o incorporarlo formalmente.

---

## Referencias

- `analisis/datos/hojas/PRESUPUESTO_TODOS_LOS_CIV_84_NP.csv`: filas 680-707 (bloque ACEROS, totales y componentes), 729-738 (detalle SST 8 meses).
- `analisis/datos/hojas/PRESUPUESTO_63_mm.csv`: filas 650-671 (V3), 693-702 (detalle SST 3 meses).
- `analisis/datos/hojas/Aceros.csv`: memorias de calculo por CIV.
- `analisis/datos/hojas/resumen.csv`: resumen adicion (fila 19 total = 75.426.575.199 + Δ = 16.000.000.000).
- `analisis/datos/hojas/Presupuesto_estimado.csv`: valores desagregados oficiales del presupuesto V4.
- `comparativa.json`: `globales.contrato_original_firma`, `globales.iniciales`, `globales.actualizadas_alt1`, `items_alt1.by_chapter."7. DESVÍOS"`.
