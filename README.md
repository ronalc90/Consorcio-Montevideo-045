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
| **Usuario** | `johan` |
| **Contrasena** | `1234` |

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
  index.html          # Aplicacion web completa (login + dashboard + graficas)
  data.json           # Base de datos del presupuesto (206 items x 27 CIVs)
  .github/
    workflows/
      pages.yml       # Deploy automatico a GitHub Pages
```

## Tecnologias

- **HTML5 + CSS3 + JavaScript** - Aplicacion 100% estatica, sin backend
- **Chart.js 4.x** - Graficas interactivas
- **GitHub Pages** - Hosting gratuito con deploy automatico

---

<div align="center">

**Instituto de Desarrollo Urbano - IDU | Bogota D.C., Colombia**

*Subdireccion General de Desarrollo Urbano | Direccion Tecnica de Construcciones*

</div>
