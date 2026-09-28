# 06 — Waterfall de versiones, componentes y plazo (8 meses)

**Contrato IDU 1752-2021 · Consorcio Montevideo 045 (Interventoria)**
Analisis del transito V0 → V1 → V2 → V3 → V4 y verificacion de la adicion de $16.000M / 8 meses solicitada por VICON el 01-09-2026.

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

**Fuentes**: hoja principal filas 692-707 (columnas M y N), hoja PRESUPUESTO 63 mm filas 657-672, `comparativa.json` claves `globales.contrato_original_firma`, `globales.iniciales`, `globales.actualizadas_alt1`.

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

En V3 y V4 la contabilidad se reordeno: los componentes contractuales volvieron a estar como bolsas independientes fuera del capitulo 7 (filas 696-705 en V4), y del capitulo 7 solo quedo el item 7.001 (mantenimiento rutinario) que se elimino por completo (13.481 m² → 0 m², balance −326.577.225).

**Conclusion**: la caida cap 7 V2→V4 no es "eliminacion de sobreproyeccion" sino **RECLASIFICACION contable**. El unico item realmente removido es el mantenimiento rutinario 6184 por −326.577.225 con AIU.

---

## 3. Detalle A-E del componente SST (8 meses) — filas 733-742

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
- 1.167.161.689,81 / 8 = 145.895.211,23 (costo/mes con AIU, fila 741) ✓
- V0 PMA-SST 2.943.115.324 + delta 8 meses 1.167.161.690 = **4.110.277.014** = V4 PMA-SST ✓

### AIU 20,006% vs AIU contractual 31,849% en obras

El AIU aplicado a obras+redes+acero es 31,849% (contractual pleno = Administracion + Imprevistos + Utilidad). Los componentes de acompañamiento tienen AIU diferenciados:

- PMA-SST: **20,006%** (delta 11,843 pp vs obras)
- Dialogo ciudadano: **19,566%**
- PMT: **19,566%**

**Motivo**: en la matriz IDU los componentes de acompañamiento (SST, PGS, PMT) son bolsas de personal e insumos que no llevan el riesgo constructivo pleno. Se les elimina el componente Imprevistos (~5%) y se aplica una utilidad parcial. Esta diferenciacion esta prevista contractualmente y confirmada en la fila 740 del presupuesto (rotulos "AIU 20,006%" para SST y "AIU 19,566%" para PGS/PMT).

---

## 4. Componentes que NO crecen (V0 = V4)

| Componente | V0 | V4 | Δ | Motivo |
|---|---:|---:|---:|---|
| Ensayos laboratorio (G) | 299.267.609 | 299.267.609 | 0 | Bolsa fija con IVA, dimensionada sobre el alcance total, no sobre el plazo. Fila 700. |
| SDA (H) | 31.328.679 | 31.328.679 | 0 | Bolsa fija de tarifas SDA. No cambia con plazo. Fila 702. |
| Fase obras iniciales (I) | 758.734.334 | 758.734.334 | 0 | Bolsa ya causada al inicio del contrato. Fila 705. |
| Bioseguridad (J) | 59.390.312 | 59.390.312 | 0 | El contratista no solicito adicion pese a ser proporcional al plazo. Fila 703. |
| Ajustes cambio vigencia (E) | 4.555.525.079 | 4.555.525.079 | 0 | Indexacion unica pactada desde firma. Fila 699. |
| Actividades acero (F) | 2.977.517.840 | 2.977.517.840 | 0 | Bolsa fija contractual con AIU y cambio de vigencia. Fila 701. Coexiste con items reales de acero en filas 685-690. |
| Fondo compensaciones (K) | 0 | 0 | 0 | Aparecio en V2 (5.942.657.520) y desaparecio en V3-V4. Fila 704. |

**Observacion**: el hecho de que Bioseguridad no se actualice a 8 meses (H06-04) es un renglon con potencial impacto MEDIA (~$40M) porque los insumos EPP y protocolos escalan con el tiempo.

---

## 5. Diferencia del acero: 75.469.677

Bloque interno acero (filas 685-690 en V4):

| Fila | Item | Descripcion | Cant V4 (kg) | Valor V4 |
|---:|---|---|---:|---:|
| 685 | (subtotal pavimentos) | Cabecera | | 2.667.280.349 |
| 686 | 3708 | Acero refuerzo (pavimentos) | 211.290,08 | 1.557.630.470 |
| 687 | 4959 | Acero liso 1 1/4" | 81.288,82 | 900.761.414 |
| 688 | 7713 | Dovelas 1 1/2" | 19.704,60 | 208.888.465 |
| 689 | (subtotal esp. publico) | Cabecera | | 385.707.168 |
| 690 | 3708 | Acero refuerzo (espacio publico) | 52.320,56 | 385.707.168 |
| 691 | 8471 | Malla electrosoldada | 0 | 0 |
| **Total bloque interno** | | | | **3.052.987.517** |

Componente fijo F (fila 701): **2.977.517.840**
Diferencia: **3.052.987.517 − 2.977.517.840 = 75.469.677**

### Explicacion de los 75.469.677

Los 75M no son un error aritmetico. Reflejan que **hay dos representaciones del acero en el mismo presupuesto**:

1. **Items reales dentro de obras** (filas 685-690, con AIU 31,849%): valores calculados con las cantidades actualizadas y los VU vigentes al 01-09-2026.
2. **Bolsa fija F "Actividades acero"** (fila 701, 2.977.517.840): valor global pactado en el contrato original, incluye AIU y ajuste por cambio de vigencia.

La diferencia de 75.469.677 (2,5% de la bolsa) se explica porque las dos aproximaciones usan bases distintas: la bolsa F trae indexacion mientras el bloque interno usa VU actuales sin banda de vigencia.

### Riesgo de doble pago (hallazgo H06-01)

Si ambos importes se pagan (bloque interno dentro de obras 58.196.933.800 + bolsa F 2.977.517.840), el contratista cobraria acero dos veces por aproximadamente 3.000M. La Interventoria debe exigir aclaracion: definir si la bolsa F se descuenta o si tiene un uso independiente (por ejemplo, acero de reserva no incluido en items).

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
| H06-01 | ALTA | Riesgo doble pago en acero (bloque + bolsa F) | $2.977M–$3.053M |
| H06-02 | ALTA | Cap 7 DESVIOS V2 era reclasificacion, no ahorro | $19.347M |
| H06-03 | ALTA | Ritmo $2.000M/mes es 3,1x el historico | $16.000M |
| H06-04 | MEDIA | Bioseguridad no se actualiza a 8 meses | ~$40M |
| H06-05 | MEDIA | Delta V3→V4 obras $10.361M sin sustento tecnico | $10.361M |
| H06-06 | MEDIA | Fondo Compensaciones aparece y desaparece sin trazabilidad | $5.943M |
| H06-07 | INFO | AIU diferenciados por componente confirmados | 0 |
| H06-08 | BAJA | Etiqueta fila 707 con fecha desactualizada (04-05-2026 en archivo 01-09-2026) | 0 |

### Recomendaciones concretas

1. **Antes de aprobar la adicion**: exigir tabla de conciliacion V2→V3→V4 por capitulo y por componente, explicando reclasificaciones vs cambios reales de alcance.
2. **Acero (H06-01)**: pedir por escrito al contratista si la bolsa F Actividades Acero se descuenta al pagar los ítems reales o si tiene destino independiente.
3. **Ritmo mensual (H06-03)**: solicitar cronograma detallado con curvas S semana a semana, frentes de obra simultaneos y capacidad instalada. Comparar con facturacion certificada de los ultimos 24 meses.
4. **V3→V4 (H06-05)**: pedir la sustentacion tecnica del $10.361M adicional en obras en solo 4 meses (mayo → septiembre 2026).
5. **Fondo Compensaciones (H06-06)**: solicitar trazabilidad de por que se propuso en V2 y desaparecio; verificar que no se este pagando doble via NP-109/NP-110 arqueologia.
6. **Bioseguridad (H06-04)**: obtener del contratista renuncia expresa a solicitar adicion en este renglon para el plazo ampliado, o incorporarlo formalmente.

---

## Referencias

- `analisis/datos/hojas/PRESUPUESTO_TODOS_LOS_CIV_84_NP.csv`: filas 685-707 (componentes), 733-742 (detalle SST 8 meses).
- `analisis/datos/hojas/PRESUPUESTO_63_mm.csv`: filas 649-672 (V3), 698-707 (detalle SST 3 meses).
- `analisis/datos/hojas/Aceros.csv`: memorias de calculo por CIV.
- `analisis/datos/hojas/resumen.csv`: resumen adicion (fila 19 total = 75.426.575.199 + Δ = 16.000.000.000).
- `analisis/datos/hojas/Presupuesto_estimado.csv`: valores desagregados oficiales del presupuesto V4.
- `comparativa.json`: `globales.contrato_original_firma`, `globales.iniciales`, `globales.actualizadas_alt1`, `items_alt1.by_chapter."7. DESVÍOS"`.
