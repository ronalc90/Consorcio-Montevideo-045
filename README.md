<div align="center">

# Consorcio Montevideo 045

### Sistema de Presupuesto Real - Contrato IDU 1752 de 2021

**Construccion de Vias y Espacio Publico | Zonas Industriales Montevideo y Puente Aranda | Bogota D.C.**

[![GitHub Pages](https://img.shields.io/badge/DEMO-En%20Vivo-brightgreen?style=for-the-badge&logo=github)](https://ronalc90.github.io/Consorcio-Montevideo-045/)
[![IDU](https://img.shields.io/badge/Entidad-IDU%20Bogot%C3%A1-blue?style=for-the-badge)](https://www.idu.gov.co/)
[![Contrato](https://img.shields.io/badge/Contrato-1752%20de%202021-orange?style=for-the-badge)]()

---

<img src="https://img.shields.io/badge/Frentes-27%20CIVs-1a365d?style=flat-square&labelColor=2c5282&color=1a365d" />
<img src="https://img.shields.io/badge/Items-206-ed8936?style=flat-square&labelColor=dd6b20&color=ed8936" />
<img src="https://img.shields.io/badge/APU-VISOR%20Mayo%202025-48bb78?style=flat-square&labelColor=38a169&color=48bb78" />
<img src="https://img.shields.io/badge/AIU-34.01%25-e53e3e?style=flat-square&labelColor=c53030&color=e53e3e" />

</div>

---

## Descripcion

Plataforma web para la gestion y analisis del presupuesto real del **Contrato IDU 1752 de 2021 - Grupo 2**, que comprende la construccion de vias y espacio publico en las zonas industriales de **Montevideo** y **Puente Aranda** en Bogota D.C.

El sistema calcula el presupuesto actualizado con base en los **Analisis de Precios Unitarios (APU)** del VISOR IDU (Mayo 2025) y permite compararlo con el presupuesto presentado por el contratista para cada uno de los 27 frentes de obra.

## Acceso

| | |
|---|---|
| **URL** | [ronalc90.github.io/Consorcio-Montevideo-045](https://ronalc90.github.io/Consorcio-Montevideo-045/) |

> Acceso restringido. Credenciales proporcionadas al personal autorizado.

## Funcionalidades

### Resumen General
- Dashboard ejecutivo con KPIs principales (valor total, costo/m2, distribucion por subgrupo)
- Tabla resumen por frente con costo directo, AIU, total, $/m2 e incidencia porcentual
- Resumen por capitulo de obra

### Reportes para Alta Gerencia
5 graficas interactivas para presentaciones ejecutivas:

| Grafica | Tipo | Descripcion |
|---------|------|-------------|
| Presupuesto por Frente | Barras horizontales | Comparativo visual de los 27 frentes ordenados por valor |
| Distribucion por Subgrupo | Dona | Peso porcentual Montevideo vs Puente Aranda |
| Composicion por Capitulo | Torta | Incidencia de cada capitulo en el presupuesto total |
| Curva S Acumulada | Linea + Barras | Presupuesto acumulado con % progresivo |
| Top 15 Items | Barras | Los items con mayor impacto economico |

- Exportar cada grafica como **PNG**
- **Imprimir** reporte completo

### Frentes (27 CIVs)
- Tarjetas visuales con resumen por frente
- Detalle completo al hacer clic: todos los items con cantidades y precios
- Filtros por subgrupo y busqueda

### Presupuesto Detallado
- 206 items con precios originales vs precios VISOR actualizados
- Diferencia de valor unitario por item
- Filtro por capitulo y busqueda libre

### Comparativo Contratista
- Seleccion por frente o vista consolidada
- Ingreso de valores unitarios del contratista por item
- Calculo automatico de diferencia y porcentaje
- Totales en tiempo real

### Exportacion
- Todas las tablas exportables a **CSV**
- Compatible con Excel para analisis adicional

## Datos Tecnicos

| Concepto | Valor |
|----------|-------|
| Valor total del proyecto | $53.691 millones (con AIU) |
| Subgrupo 2 - Montevideo | 7 CIVs - $15.046 millones (28%) |
| Subgrupo 5 - Puente Aranda | 20 CIVs - $38.644 millones (72%) |
| Area total de intervencion | 52.286 m2 |
| Costo promedio por m2 | $1.026.885 |
| Factor AIU | 34.01% |
| Fuente de precios | VISOR IDU - Mayo 7 de 2025 |

## Estructura del Proyecto

```
Consorcio-Montevideo-045/
  index.html                            # Aplicacion web completa (login + dashboard + graficas)
  data.json                             # Base de datos del presupuesto (206 items x 27 CIVs)
  comparativa.json                      # Comparativa IDU oficial vs propuesta contratista (V1 y V2)
  analisis_2026_09.json                 # Consolidado del analisis del presupuesto 01-09-2026 (V4)
  presupuesto_2026_09.json              # Matriz item x CIV V4 (obras con AIU)
  analisis/
    INFORME_PRESUPUESTO_2026-09.md      # Informe ejecutivo para gerencia e interventoria
    REGISTRO_AUDITORIA.md               # Registro de auditoria (errores de la fuente, correcciones, dudas, limitaciones)
    Analisis_Presupuesto_2026-09.xlsx   # Excel con 7 hojas (formato profesional)
    analisis_2026_09.json               # Consolidado (copia canonica)
    auditoria/
      registro_auditoria.{json,csv}     # Registro de auditoria generado por auditoria.py (insumo de la seccion N)
    hallazgos/
      BRIEF.md                          # Brief comun de los 6 analisis
      01_variacion_items.{md,json}      # Analisis 01: variacion de cantidades por item
      02_variacion_civ.{md,json}        # Analisis 02: variacion por CIV
      03_costo_civ.{md,json}            # Analisis 03: costo por CIV (27 CIVs)
      04_aritmetica.{md,json}           # Analisis 04: aritmetica, formulas, precios
      05_nps.{md,json}                  # Analisis 05: items no previstos
      06_versiones_plazo.{md,json}      # Analisis 06: waterfall V0-V4 y plazo 8 meses
    scripts/
      extraer_presupuesto.py            # Extrae la hoja principal a JSON + CSVs
      analisis_01_variacion_items.py    # Genera 01_variacion_items.{md,json}
      analisis_02_variacion_civ.py      # Genera 02_variacion_civ.{md,json}
      analisis_03_costo_civ.py          # Genera 03_costo_civ.{md,json}
      analisis_04.py                    # Genera 04_aritmetica.{md,json}
      analisis_05_nps.py                # Genera 05_nps.{md,json}
      corregir_06.py                    # Corrige filas y H06-01 del analisis 06 (idempotente, documentado en el registro B-07/B-08)
      consolidar.py                     # Consolida los 6 en analisis_2026_09.json
      generar_excel.py                  # Genera Analisis_Presupuesto_2026-09.xlsx
      verificacion.py                   # Verifica al peso los totales contra el Excel
      auditoria.py                      # Genera el registro de auditoria (JSON, CSV y Markdown)
    datos/
      presupuesto_2026_09.json          # Extraccion cruda de la hoja principal V4
      hojas/                            # Las 18 hojas del Excel exportadas como CSV
  fuentes/
    4. PRESUPUESTO 01-09-2026 75MM (8 MESES).xlsx   # Excel fuente del contratista
  .github/
    workflows/
      pages.yml                         # Deploy automatico a GitHub Pages
```

## Pestanas de la aplicacion

1. **Resumen General** — dashboard ejecutivo con KPIs y tabla resumen por frente.
2. **Reportes Gerencia** — graficas para presentaciones.
3. **Frentes (27 CIVs)** — tarjetas visuales con detalle por CIV.
4. **Presupuesto Detallado** — 206 items con precios VISOR vs originales.
5. **IDU Oficial vs Propuesta Contratista** — comparativa V1 (25-02-2026) vs V2 (21-04-2026).
6. **Presupuesto 01-09-2026 · 75MM · 8 meses** — analisis del nuevo presupuesto:
   - KPIs, puente de versiones V0→V4 por componente y tabla por capitulo.
   - **Explorador visual** con 11 graficas conmutables (puente, evolucion por version, Δ por capitulo y estado, Δ por CIV descompuesto, $/m² vs mediana, costo por CIV × capitulo, mapa de calor, area vs costo, top NP, Pareto, composicion). Cada grafica trae su panel *que muestra / fuente y calculo / lectura del analista*; clic en una barra o punto abre la ficha correspondiente.
   - Variacion de cantidades por item (renglon o neta por codigo), con modo de contraste V2 (abril) y valores con AIU o costo directo.
   - Variacion por CIV con descomposicion del delta (aumentos, disminuciones, NP, contractual nuevo, eliminado).
   - Costo por CIV (obras + componentes + $/m2) para los 27 CIVs, con grupos de alcance de Hoja1.
   - NPs top 20 con contraste frente a abril y clasificacion.
   - 71 hallazgos por severidad (ALTA / MEDIA / BAJA / INFO) con recomendacion, filtrables por analisis de origen.
   - Metodologia, fuentes y verificacion al peso.
   - Exportacion a Excel (8 hojas) y CSV por seccion.

### Capa de revisión profesional (v3 · 27-09-2026)

- **Ficha del contrato y resumen ejecutivo** para revisores (8 conclusiones con cifras) y **chequeo normativo** (tope del 50% en SMMLV, naturaleza jurídica de lo pedido, soportes faltantes, deber de informar).
- **Marco normativo con fuentes** (Ley 80 art. 40, CCE C-466/2024, Consejo de Estado exp. 67.508, Ley 1474 arts. 83-84, manuales y guias IDU MG-GC-06, GUDP017, PR-IC-01, actas FOEO24, SMMLV 2021/2026) con "que dice" y "como aplica aqui".
- **Indice de atencion por CIV** (0-100, seis factores ponderados) y **prioridad de revision por renglon**, con sus factores explicados en cada ficha.
- **Precios unitarios**: VU de V4 frente a tres referencias: el VU pactado en la propuesta 2021 (mediana +49%, Δ $15.086M), el APU actualizado 13-09-2024 (367 renglones con Δ > 2%, +$3.639M) y el VISOR de mayo-2025.
- **Reubicaciones**: $5.807M de lo "eliminado" reaparece bajo el mismo codigo IDU en otro renglon o subcapitulo (solo la parte que cambia).
- **Simulador de escenarios**: plazo, % de NP aceptados, rechazo de reemplazos, VU de referencia, exclusion de los 9 CIVs "no alcanza", recalculo ilustrativo de vigencia.
- **Lista de chequeo del revisor** (23 items con notas, estado guardado en el navegador y exportable a CSV), **glosario** buscable, **busqueda global**, **enlaces directos a cada ficha** (`#p75/civ/16000024`, `#p75/item/34`, `#p75/hall/H06-02`), impresion de pestaña y de fichas, navegacion por teclado.

### Registro de auditoría (v4 · 28-09-2026)

- **Seccion N de la pestaña 75MM** y `analisis/REGISTRO_AUDITORIA.md`: 66 asientos generados por `analisis/scripts/auditoria.py` leyendo el Excel con openpyxl — **A** errores e inconsistencias de la fuente (25, con hoja, celda y formula), **B** correcciones que el propio analisis tuvo que hacerse (13, con el commit), **C** dudas abiertas para el contratista o el IDU (16) y **D** limitaciones del analisis (12). Filtros por tipo, severidad y estado, ficha por asiento con evidencia y "como verificarlo usted mismo", exportacion CSV y enlaces directos (`#p75/aud/A-25`).
- **Paquete de auditoria**: SHA-256 del Excel fuente y de cada salida, versiones del entorno, tolerancias aceptadas y comandos para reproducir todo el analisis.
- Hallazgos que salieron del registro y cambian la lectura: el valor inicial del contrato fue **$50.793.789.333** (no $59.426M), asi que el acumulado de adiciones llega al **48,5% nominal** del tope del 50% (A-25, B-11); los VU vigentes estan **+49%** sobre los pactados en la propuesta (A-24); la base de precios y 81 cantidades por CIV dependen de **libros externos no entregados** (A-01, A-02); el codigo 8643 ($2.718M) tiene descripcion de consultoria y cambio de unidad (A-06). Correcciones del analisis: filas del analisis 06 desplazadas (B-07), "doble pago de acero" retirado (B-08), falsos positivos del analisis 04 (B-09), "trasladado" de reubicaciones (B-13).

### Capa explicativa ("explica TODO")

- **Tooltips ricos en toda la app**: cada encabezado de columna, KPI y chip muestra al pasar el mouse que es, de donde sale (hoja · fila · columna del Excel) y como se calcula.
- **Fichas al hacer clic**: cualquier fila (item, codigo, CIV, capitulo, componente, NP, hallazgo), tarjeta KPI o barra de grafica abre una ficha con la formula aplicada a sus numeros reales, la verificacion contra el Excel (✓/✗), la distribucion por CIV, el contraste V1/V2/V4, los hallazgos relacionados y las preguntas sugeridas para el contratista.
- **Colores validados para daltonismo**: estados calidos suman dinero (aumento, nuevo contractual, NP) y frios restan (disminucion, eliminado); en tablas rojo = suma a la adicion y verde = resta.

## Tecnologias

- **HTML5 + CSS3 + JavaScript** - Aplicacion 100% estatica, sin backend
- **Chart.js 4.x** - Graficas interactivas
- **GitHub Pages** - Hosting gratuito con deploy automatico

---

<div align="center">

**Instituto de Desarrollo Urbano - IDU | Bogota D.C., Colombia**

*Subdireccion General de Desarrollo Urbano | Direccion Tecnica de Construcciones*

</div>
