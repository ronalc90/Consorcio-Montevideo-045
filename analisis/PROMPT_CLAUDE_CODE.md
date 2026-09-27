# Revisión de interventoría — Presupuesto 01-09-2026 (75MM, 8 meses) · Contrato IDU 1752 de 2021

Trabaja en español. Estás en la raíz del repo `Consorcio-Montevideo-045`. Es la web estática de la interventoría (Consorcio Montevideo 045) del Contrato IDU 1752/2021, cuyo contratista es el Consorcio VICON 024. La app son `index.html`, `data.json` y `comparativa.json`, y usa Chart.js. Primero lee el código y los JSON para entender cómo está construida.

## Objetivo
El contratista presentó un presupuesto nuevo: `fuentes/4. PRESUPUESTO 01-09-2026 75MM (8 MESES).xlsx`. Pide una adición de **$16.000.000.000** y **8 meses** de plazo. El total pasa de $59.426.575.199 a **$75.426.575.199**.

Necesito un análisis detallado, verificado al peso, con dos focos principales:
1. **Variación entre cantidades INICIALES y FINALES**, por ítem y por CIV (frente).
2. **Costo por CIV** para los 27 CIVs.

Usa **múltiples subagentes en paralelo** para revisar todo, y un agente independiente para verificar al final. Después integra el resultado al proyecto: datos nuevos, una pestaña nueva en la app, un informe y un Excel.

## Paso 0 — Preparación
1. Verifica que haya Python con `openpyxl` y `pandas`; instálalos si faltan.
2. Corre `python analisis/scripts/extraer_presupuesto.py`. Genera `analisis/datos/presupuesto_2026_09.json` (hoja principal ítem × CIV) y `analisis/datos/hojas/*.csv` (todas las hojas, incluidas las ocultas). En esos CSV la columna 0 es la A y la fila n es la fila n de Excel. Debe imprimir `obras con AIU = 58,196,933,800`; si no, detente y revisa.
3. Crea la rama `presupuesto-2026-09`. **No hagas push ni publiques nada** sin preguntarme. El repo es público y el login de la app es solo de cliente, así que los JSON quedan expuestos.
4. Si existe una carpeta `_to_delete` fuera del repo, ignórala.

## Estructura del Excel
- Tiene 18 hojas. Las visibles son `PRESUPUESTO TODOS LOS CIV 84 NP` (la principal), `resumen` y `Presupuesto estimado`.
- Hojas ocultas útiles:
  - `MEMORIA CANTIDADES` y `FASE 1 (2)`: cantidades por CIV con numeración vieja 1.1, 1.1001… Probablemente son la **línea base inicial por CIV**.
  - `PRESUPUESTO CONTRACTUAL MAYO 25` y `CONSOLIDADO CTO 1752 AJUSTADO`: presupuesto oficial vs propuesta VICON vs APU actualizados.
  - `VISOR 07-05-25`: precios oficiales del IDU.
  - `NPs Objetados`.
  - `EJECUTIVO`: resumen por CIV del 11/05/2026.
  - `Hoja1`: alcance de la Alt 2, es decir, CIVs ya iniciados, por iniciar y que no alcanzan.
  - `PRESUPUESTO 63 mm`: versión intermedia de ~$63.749M.
  - `Aceros`, `CALCULO DE ANDENES`, `CALCULO ESTRUCTURA`, `MEMORIA ETB` y `MOBILIARIOS`.
- Columnas de la hoja principal:
  - B código IDU · C ítem de pago · F descripción · G unidad
  - **H cantidad contractual (inicial)** · **I cantidad actualizada (final)** · J = I − H
  - K VU costo directo · L VU CD+AIU (AIU 31,849%)
  - M valor final con AIU · N valor inicial con AIU · O balance de mayores/menores cantidades · P incorporación de NP · Q adición
  - Fila 3: IDs de CIV. Subgrupo 2 (7 CIVs) en las columnas S..AF, en pares cantidad/valor, con total en AG/AH. Subgrupo 5 (20 CIVs) en AJ..BW, con total en BX/BY. Total general en CA/CB. Chequeo en CC.
- Filas de la hoja principal:
  - 7-679: ítems en los capítulos 1 Preliminares, 2 Pavimentos, 3 Espacio público, 4 Señalización, 5 Redes hidrosanitarias, 6 Redes secas y 7 Desvíos.
  - 680-687: bloque ACEROS, que **no** suma en obras.
  - 688: total obras + AIU = 58.196.933.800.
  - 692-701: componentes no-obra.
  - 703: total 75.426.575.199.
  - 729-738: detalle del componente ambiental/SST para 8 meses (AIU 20,006%).

## Versiones a comparar
| Versión | Total | Fuente |
|---|---|---|
| V0 Contrato firmado | 59.426.575.199 (obras+AIU 44.303.294.799) | `comparativa.json` → `globales.contrato_original_firma`; col N |
| V1 IDU oficial 25-02-2026 | 61.411.887.929 | `comparativa.json` → `globales.iniciales`, `civs_idu`, ítems `cant_idu`/`valor_idu_cd` |
| V2 VICON 21-04-2026 (Alt 1) | 77.944.220.992 | `comparativa.json` → `globales.actualizadas_alt1`, `civs_cont`, `civ_items_cont`, ítems `cant_cont`/`valor_cont_cd` |
| V3 intermedia "63MM" | ~63.749M | hoja oculta `PRESUPUESTO 63 mm` |
| **V4 nueva 01-09-2026** | **75.426.575.199** | hoja principal |

Los ítems de `comparativa.json` están en **costo directo (sin AIU)**; V4 viene con AIU.

## Lo que ya está verificado (úsalo como punto de partida y profundiza)
- **Obras con AIU:** 44.303.294.799 → 58.196.933.800 (+13.893.639.001). La hoja lo explica como −257.285.548 de balance de mayores/menores cantidades más 14.150.924.549 de NPs.
- **Componentes no-obra:**
  - PMA-SST +1.167.161.690
  - Diálogo ciudadano +555.057.738
  - PMT +384.141.571
  - Fondo de compensaciones en 0 (en V2 era 5.942.657.520)
  - Ajustes, acero, laboratorio, SDA, bioseguridad y fase inicial sin cambio
- **Variación por renglón:**

| Estado | Renglones | Δ valor |
|---|---|---|
| Eliminado | 118 | −19.443.722.236 |
| Contractual con cantidad inicial 0 que ahora tiene cantidad | 93 | +15.200.542.240 |
| NP nuevo (81 códigos únicos) | 105 | +14.150.924.549 |
| Aumentó | 27 | +8.809.106.675 |
| Disminuyó | 39 | −4.823.212.227 |
| Sin cambio | 25 | 0 |

- **Δ por capítulo:**
  - Redes hidrosanitarias +6.777.852.537
  - Pavimentos +3.556.107.781
  - Preliminares +2.787.734.305
  - Redes secas +1.613.831.550
  - Espacio público −515.309.947
  - Desvíos −326.577.225
  - Señalización 0
- **Patrones que hay que validar:**
  - **Reubicaciones:** el mismo ítem aparece eliminado en un subcapítulo y nuevo en otro, por ejemplo al pasar de "a cargo del IDU" a "a cargo de la ESP". Casos: 6.007 en las filas 490 → 531 y 5.067 en las filas 295 → 399. Hay que calcular la **variación neta por código** para no sobreleer eliminados y nuevos.
  - **Posibles reemplazos de ítem contractual por NP más caro:** fila 33 (2.002 MD12, −2.585M) → fila 39 (NP-123 MD19, +3.270M); fila 24 (1.012 BG_A, −1.811M) → fila 30 (NP-124 BG_A reciclado, +2.519M).
  - **Saltos extremos de cantidad:** fila 20 (1.008 rajón, de 965 a 14.163 m³) y fila 85 (3.039 andén, de 114 a 15.469 m²).
  - **Descripción rara:** la fila 317 (5.037, "estudios y diseños de aceras" en M2, dentro de redes).
- **Costo por CIV (obras con AIU):** promedio $1.113.048/m² y mediana $1.019.119/m², sobre 52.286 m² con las áreas de V1.
  - Outliers:
    - 16000024 KR 65A: $2.454.941/m², $5.899M, +$1.661M vs V2.
    - 16000010 CL18B: $2.317.646/m², 58% en NPs.
    - 16000017: $2.032.570/m².
    - 16000013: +$891M vs V2.
  - Grupos de `Hoja1`: ya iniciados $19.652M, por iniciar $19.034M, no alcanza $19.511M.
- **Trampas conocidas:**
  - El CIV `500002375` (V4) es el mismo que `50002375` (MEMORIA), `16004876 (50002375)` (comparativa.json) y `16004876` (Hoja1): KR65 CL17–CL18. Comparte segmento 91029906 con el 16000047.
  - La hoja se llama "84 NP", pero hay 81 códigos NP con cantidad en 105 renglones.
  - El bloque de aceros suma 3.052.987.517; el componente fijo de acero es 2.977.517.840.
  - La fila 703 dice "04-05-2026", pero el archivo es del 01-09-2026.
  - Hay diferencias de pocos pesos: .780 vs .800, .017 vs .014 y .268 vs .199.

## Plan de subagentes (lánzalos EN PARALELO)
Escribe primero un brief común en `analisis/hallazgos/BRIEF.md` con este contexto. Luego lanza 6 subagentes. Cada uno escribe `analisis/hallazgos/NN_tema.md`, con resumen, hallazgos y metodología, y `NN_tema.json`, con tablas para la app.

1. **Variación por ítem (inicial vs final).**
   - Estado de cada renglón y su verificación: J = I − H, O = (I − H) × L y Q = O + P.
   - Vista **neta por código**, separando reubicaciones de variaciones reales.
   - Resúmenes por capítulo y subcapítulo que concilien exacto 44.303.294.799 → 58.196.933.800.
   - Rankings: top 30 aumentos y disminuciones, variación mayor a ±50% con impacto mayor a $50M, y cantidad final mayor a 3× la contractual.
   - Detección sistemática de reemplazos de ítems contractuales por NPs, con su sobrecosto.
   - Cruce con V1 y V2 para ver qué recortó el contratista entre abril y septiembre.
2. **Variación por CIV.**
   - Validar la línea base inicial por CIV (`MEMORIA CANTIDADES`, `FASE 1 (2)`, `data.json` → `items[*].cantidades`) contra la col H y documentar qué tanto concilia.
   - Cruzar la numeración vieja con la nueva.
   - Matriz ítem × CIV con cantidad inicial, cantidad final y Δ, valorada al VU de V4 para aislar el efecto cantidad.
   - Descomposición del Δ de cada CIV.
   - Métricas de cantidad por m² de CIV y anomalías.
3. **Costo por CIV.**
   - Obras con AIU, separando CD y AIU, por capítulo y subcapítulo, NP vs contractual y redes vs sin redes.
   - Verificación contra la fila 688 y la hoja `EJECUTIVO`.
   - Reparto documentado de los componentes no-obra para llegar al **costo total por CIV**, que debe sumar exacto 75.426.575.199.
   - Indicadores $/m² y $/ml, con estadísticas y outliers por subgrupo, explicando ítem por ítem.
   - Comparación V1 / V2 / V4 por CIV.
   - Costo de los grupos de `Hoja1`.
4. **Aritmética y precios unitarios.**
   - Celdas digitadas a mano vs fórmulas (`openpyxl` con `data_only=False`) y rangos incompletos.
   - Recálculo completo, incluyendo que L = redondeo(K × 1,31849).
   - Consistencia entre `resumen`, `Presupuesto estimado` (incluidos los valores en letras), `EJECUTIVO` y las filas 688-707.
   - Duplicados.
   - VU de V4 vs `VISOR 07-05-25`, vs el contractual y vs V2.
   - **Separar el efecto precio del efecto cantidad.**
5. **NPs.**
   - Inventario de NPs únicos vs renglones, y explicación del "84 NP".
   - Cambios frente a los 216 NPs de V2.
   - **NPs objetados** (`comparativa.json` → `nps_objetados` y la hoja `NPs Objetados`) que siguen incluidos, con su valor.
   - Precio de cada NP frente a ítems similares del VISOR o del contrato.
   - NPs GLB/MES y su cálculo para 8 meses.
   - Top 20 con ficha y pregunta para el contratista.
   - Clasificación: aprobado, en revisión, objetado o nuevo.
6. **Versiones, componentes y plazo.**
   - Waterfall V0→V1→V2→V3→V4 por componente.
   - Qué pasó con **Desvíos**: en V2 subió a 19.347M en CD y en V4 está casi en 0.
   - Detalle A-E del componente SST para 8 meses (filas 718-739), comparando incremento vs 8 × costo mensual y el AIU de 20,006%.
   - Explicar por qué laboratorio, acero, ajustes y los demás componentes no crecen.
   - Diferencia del acero.
   - Ritmo de ~$2.000M/mes.
   - Qué cambió de V3 a V4.

Reglas para todos los agentes:
- Todo número sale de código; nada estimado.
- Citar la **hoja y la fila de Excel** de cada hallazgo.
- Severidad ALTA, MEDIA, BAJA o INFO.
- Una recomendación concreta para la interventoría en cada hallazgo, es decir, qué pedirle al contratista.
- Pesos con punto de miles.
- No modificar los archivos fuente.

## Integración (cuando terminen los 6)
1. Consolida en `analisis/analisis_2026_09.json`, sin duplicar datos innecesarios, y copia `presupuesto_2026_09.json` a la raíz si la app lo va a cargar.
2. **Pestaña nueva en `index.html`**: "Presupuesto 01-09-2026 · 75MM · 8 meses". Respeta el estilo, los helpers (`fmt`, modales, chips de filtro, Chart.js) y el patrón de exportación que ya existen. Debe tener estas subsecciones:
   - Resumen y puente: KPIs, waterfall V0→V4 y componentes.
   - **Variación de cantidades**: tabla por ítem con filtros por estado, capítulo y búsqueda; alterna entre vista por renglón y vista neta por código; top de movimientos; reemplazos por NP.
   - **Variación por CIV**: selector de CIV con su tabla inicial/final/Δ y un gráfico de descomposición.
   - **Costo por CIV**: tabla de los 27 con obras, componentes, total, $/m² y V1/V2/V4; gráfica de $/m² con outliers resaltados; clic para ver el detalle por capítulo.
   - NPs, con los objetados incluidos resaltados.
   - Hallazgos para la interventoría, ordenados por severidad, con la fila de Excel.
   - Exportar a Excel y CSV.
3. Corrige de paso el bug conocido de la sección 4 de la pestaña comparativa: el CIV `16004876 (50002375)` no se dibuja en "No alcanza" porque la búsqueda no normaliza el ID con `split(' ')[0]`, y el subtotal queda corto en $1.792.994.322.
4. Informe escrito `analisis/INFORME_PRESUPUESTO_2026-09.md`, pensado para gerencia y para la interventoría, con este orden: resumen ejecutivo, variación de cantidades, costo por CIV, NPs, componentes y plazo, hallazgos por severidad, preguntas para el contratista y anexos.
5. Excel `analisis/Analisis_Presupuesto_2026-09.xlsx` con las hojas: Resumen, Variación ítems, Variación neta por código, Variación por CIV (matriz), Costo por CIV, NPs, Hallazgos. Debe tener formato profesional y filtros.
6. Actualiza el README: la pestaña nueva, los archivos nuevos y la estructura.

## Verificación (obligatoria, con un subagente independiente que NO haya participado)
- Recalcular desde el Excel fuente las cifras clave del informe, la app y el Excel de salida: totales, variación por estado y capítulo, costo por CIV y la suma de 75.426.575.199. Reportar cualquier diferencia.
- Levantar la app con `python -m http.server` y revisar que la pestaña nueva cargue sin errores de consola, que los filtros funcionen y que las pestañas existentes no se hayan dañado.
- Corrige lo que salga y vuelve a verificar.

## Cierre
- Haz commit en la rama `presupuesto-2026-09` con mensajes claros. **No hagas push.**
- Al final dame:
  - un resumen corto con los 10 hallazgos más importantes y su impacto en pesos;
  - la tabla resumen de costo por CIV;
  - la lista de archivos creados o modificados;
  - lo que no se pudo conciliar.
