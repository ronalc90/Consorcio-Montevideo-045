# 03 · Costo por CIV — Obras + componentes → $75.426.575.199

**Fuente principal**: `PRESUPUESTO TODOS LOS CIV 84 NP` (V4 01-09-2026) vía `analisis/datos/presupuesto_2026_09.json`.
**AIU**: 31,849%. **Componentes no-obra**: $17.229.641.399. **Total esperado**: $75.426.575.199.

## Verificaciones globales

| Concepto | Calculado | Esperado | Δ |
|---|---:|---:|---:|
| Obras con AIU (fila 688) | $58.196.933.869 | $58.196.933.800 | $69 |
| Total obras+componentes (fila 703) | $75.426.575.268 | $75.426.575.199 | $69 |
| Suma de los 10 componentes | $17.229.641.399 | $17.229.641.399 | $0 |

## Criterio de reparto de componentes

- **Base**: proporcional al costo directo de obras (V4) por CIV. Σ CD obras = $44.139.078.695.
- **Fórmula**: `componentes_civ = 17.229.641.399 × (obras_cd_civ / Σ obras_cd_civ)`.
- **Razón**: el CD refleja intensidad de obra real (redes, señalización, cantidades). El AIU es proporcional (mismo factor 31,849%) y no aporta información al reparto. El área lineal no representa peso de las 30 partidas contractuales ni de los NPs, por lo cual se descarta.

## Distribución por subgrupo

| Subgrupo | # CIVs | Obras con AIU | Total (con componentes) |
|---|---:|---:|---:|
| SG2 (Puente Aranda) | 7 | $14.938.689.502 | $19.361.401.249 |
| SG5 (Montevideo) | 20 | $43.258.244.367 | $56.065.174.019 |
| **Total** | **27** | **$58.196.933.869** | **$75.426.575.268** |

## Costo por CIV

| CIV | Nom. | SG | Área m² | Obras CD | AIU | Obras total | Componentes | Total | $/m² obras | $/m² total | %NP |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 16000024 | KR 65A | 5 | 2402.99 | $4.474.207.593 | $1.424.990.376 | $5.899.197.969 | $1.746.502.071 | $7.645.700.040 | $2.454.941 | $3.181.744 | 17.23% |
| 16000010 | CL18B | 5 | 1704.36 | $2.995.929.504 | $954.173.588 | $3.950.103.092 | $1.169.457.826 | $5.119.560.918 | $2.317.646 | $3.003.803 | 58.45% |
| 16000017 | KR 65A | 5 | 1361.36 | $2.098.657.534 | $668.401.438 | $2.767.058.972 | $819.208.688 | $3.586.267.660 | $2.032.570 | $2.634.327 | 19.49% |
| 9003990 | CL20 | 2 | 2979.83 | $2.056.373.710 | $654.934.463 | $2.711.308.173 | $802.703.243 | $3.514.011.416 | $909.887 | $1.179.266 | 20.55% |
| 9003980 | CL20 | 2 | 2373.61 | $1.952.559.633 | $621.870.718 | $2.574.430.351 | $762.179.531 | $3.336.609.882 | $1.084.605 | $1.405.711 | 19.26% |
| 16000023 | CL17A | 5 | 2852.0 | $1.950.832.901 | $621.320.771 | $2.572.153.672 | $761.505.503 | $3.333.659.175 | $901.877 | $1.168.885 | 29.65% |
| 16000038 | CL18A | 5 | 2644.76 | $1.941.792.950 | $618.441.637 | $2.560.234.587 | $757.976.768 | $3.318.211.355 | $968.040 | $1.254.636 | 25.7% |
| 16000028 | CL18A | 5 | 2749.3 | $1.826.050.939 | $581.578.964 | $2.407.629.903 | $712.797.000 | $3.120.426.903 | $875.725 | $1.134.990 | 22.43% |
| 16000012 | CL18A | 5 | 2544.68 | $1.780.796.661 | $567.165.929 | $2.347.962.590 | $695.132.041 | $3.043.094.631 | $922.695 | $1.195.865 | 20.95% |
| 9003967 | KR 68C | 2 | 2419.5 | $1.688.637.742 | $537.814.234 | $2.226.451.976 | $659.157.907 | $2.885.609.883 | $920.212 | $1.192.647 | 21.75% |
| 16000052 | KR63 | 5 | 1791.31 | $1.660.994.703 | $529.010.203 | $2.190.004.906 | $648.367.477 | $2.838.372.383 | $1.222.572 | $1.584.523 | 25.83% |
| 16000013 | CL18B | 5 | 1541.61 | $1.630.604.328 | $519.331.172 | $2.149.935.500 | $636.504.627 | $2.786.440.127 | $1.394.604 | $1.807.487 | 21.28% |
| 9004002 | CL20 | 2 | 2710.31 | $1.611.365.289 | $513.203.731 | $2.124.569.020 | $628.994.689 | $2.753.563.709 | $783.884 | $1.015.959 | 19.47% |
| 9003981 | KR 68B | 2 | 1985.23 | $1.545.979.024 | $492.378.859 | $2.038.357.883 | $603.471.232 | $2.641.829.115 | $1.026.762 | $1.330.742 | 22.61% |
| 16000032 | KR 63 | 5 | 1835.68 | $1.422.389.187 | $453.016.732 | $1.875.405.919 | $555.228.073 | $2.430.633.992 | $1.021.641 | $1.324.106 | 21.0% |
| 16000043 | KR 63 | 5 | 1519.4 | $1.357.960.466 | $432.496.829 | $1.790.457.295 | $530.078.392 | $2.320.535.687 | $1.178.398 | $1.527.271 | 29.94% |
| 16000057 | CL17B | 5 | 1996.95 | $1.357.056.660 | $432.208.975 | $1.789.265.635 | $529.725.592 | $2.318.991.227 | $895.999 | $1.161.267 | 20.23% |
| 16000027 | KR 63 | 5 | 1958.61 | $1.340.562.830 | $426.955.856 | $1.767.518.686 | $523.287.244 | $2.290.805.930 | $902.435 | $1.169.608 | 21.39% |
| 16000016 | KR 66 | 5 | 1608.57 | $1.324.147.371 | $421.727.696 | $1.745.875.067 | $516.879.487 | $2.262.754.554 | $1.085.358 | $1.406.687 | 21.24% |
| 16000047 | KR65 | 5 | 2387.64 | $1.290.776.334 | $411.099.354 | $1.701.875.688 | $503.853.139 | $2.205.728.827 | $712.786 | $923.811 | 20.68% |
| 9003989 | KR 68B | 2 | 1404.75 | $1.238.497.620 | $394.449.107 | $1.632.946.727 | $483.446.200 | $2.116.392.927 | $1.162.447 | $1.506.598 | 21.66% |
| 9003968 | CL21 | 2 | 1537.22 | $1.236.737.004 | $393.888.368 | $1.630.625.372 | $482.758.945 | $2.113.384.317 | $1.060.763 | $1.374.809 | 23.63% |
| 16000060 | KR63 | 5 | 1593.8 | $1.231.917.770 | $392.353.491 | $1.624.271.261 | $480.877.763 | $2.105.149.024 | $1.019.119 | $1.320.836 | 22.42% |
| 500002375 | KR65 | 5 | 1159.92 | $1.127.652.890 | $359.146.169 | $1.486.799.059 | $440.178.080 | $1.926.977.139 | $1.281.812 | $1.661.302 | 20.7% |
| 16000077 | CL14 | 5 | 1237.01 | $833.012.058 | $265.306.010 | $1.098.318.068 | $325.165.351 | $1.423.483.419 | $887.881 | $1.150.745 | 25.92% |
| 16000029 | CL18 | 5 | 939.76 | $616.196.110 | $196.252.299 | $812.448.409 | $240.531.482 | $1.052.979.891 | $864.528 | $1.120.477 | 17.24% |
| 16000007 | KR66 | 5 | 1045.93 | $547.389.885 | $174.338.204 | $721.728.089 | $213.673.047 | $935.401.136 | $690.035 | $894.325 | 23.58% |

## Estadística $/m² (obras con AIU)

| Segmento | Media | Mediana | P25 | P75 | Min | Max | Std |
|---|---:|---:|---:|---:|---:|---:|---:|
| Global | $1.132.564 | $1.019.119 | $898.938 | $1.170.422 | $690.035 | $2.454.941 | $444.212 |
| Subgrupo 2 | $992.651 | $1.026.762 | $915.049 | $1.072.684 | $783.884 | $1.162.447 | $128.303 |
| Subgrupo 5 | $1.181.533 | $993.580 | $893.970 | $1.237.382 | $690.035 | $2.454.941 | $505.062 |

**Límites outlier**: superior $1.426.345, inferior $611.893 (mediana ± 1,5·IQR = ±$407.226).

## Outliers

### CIV 16000024 (KR 65A) — $2.454.941/m² (2.41× mediana)
- Subgrupo 5 · Área 2402.99 m² · Obras con AIU $5.899.197.969
- Top 5 renglones que inflan el $/m²:
  - Fila 34 · ítem 2.003 · 2. PAVIMENTOS · LOSA DE CONCRETO MR45 (SUMINISTRO, FORMALETEADO, COLOCACIÓN, CURADO, JUNTAS Y ACABADO. INCLUYE CANASTILLA PASA JUNTA. · cant 1022.734192 M3 · **$1.527.099.650**
  - Fila 369 · ítem 5.037 · 5. REDES HIDROSANITARIAS · Proyecto: factibilidad, estudios y diseños de aceras, ciclorutas y conexiones peatonales en la ciudad de Bogotá D.C. Pro · cant 10554.85 M2 · **$701.876.415**
  - Fila 405 · ítem 3.012 · 5. REDES HIDROSANITARIAS · SUBBASE GRANULAR CLASE B (SBG_B) CON RECICLADO DE CONCRETO HIDRAULICO (SUMINISTRO, EXTENDIDO MANUAL, HUMEDECIMIENTO Y CO · cant 2916.97 M3 · **$595.505.259**
  - Fila 39 · ítem NP-123 [NP] · 2. PAVIMENTOS · MEZCLA ASFÁLTICA EN CALIENTE DENSA MD19 CON CEMENTO ASFÁLTICO CA 14 (Suministro, Extendido, Nivelación y Compactación
me · cant 235.02 M3 · **$367.762.586**
  - Fila 14 · ítem 1.006 · 1. PRELIMINARES · TRANSPORTE Y DISPOSICIÓN FINAL DE ESCOMBROS EN SITIO AUTORIZADO (DISTANCIA DE TRANSPORTE 21 KM). A DISTANCIA MAYOR DEL A · cant 6049.64 M3 · **$333.613.447**

### CIV 16000010 (CL18B) — $2.317.646/m² (2.27× mediana)
- Subgrupo 5 · Área 1704.36 m² · Obras con AIU $3.950.103.092
- Top 5 renglones que inflan el $/m²:
  - Fila 479 · ítem NP-133 [NP] · 5. REDES HIDROSANITARIAS · CONTRATO 1752-2021 - BOX CULVERT PREFABRICADO TIPO 1, Ancho Int: 1.875 m, Alto Int: 1.80m, Longitud: 1.00m, Espesores de · cant 110 UN · **$1.879.745.340**
  - Fila 34 · ítem 2.003 · 2. PAVIMENTOS · LOSA DE CONCRETO MR45 (SUMINISTRO, FORMALETEADO, COLOCACIÓN, CURADO, JUNTAS Y ACABADO. INCLUYE CANASTILLA PASA JUNTA. · cant 372.46 M3 · **$556.140.139**
  - Fila 39 · ítem NP-123 [NP] · 2. PAVIMENTOS · MEZCLA ASFÁLTICA EN CALIENTE DENSA MD19 CON CEMENTO ASFÁLTICO CA 14 (Suministro, Extendido, Nivelación y Compactación
me · cant 77.6 M3 · **$121.429.566**
  - Fila 14 · ítem 1.006 · 1. PRELIMINARES · TRANSPORTE Y DISPOSICIÓN FINAL DE ESCOMBROS EN SITIO AUTORIZADO (DISTANCIA DE TRANSPORTE 21 KM). A DISTANCIA MAYOR DEL A · cant 2002.3 M3 · **$110.418.836**
  - Fila 531 · ítem 6.007 · 6. REDES SECAS · 6 DUCTOS D=6" + 2 DUCTOS D=3" PVC TDP. SUMINISTRO E INSTALACION. (NO INCLUYE RELLENOS). · cant 187.98 ML · **$104.391.873**

### CIV 16000017 (KR 65A) — $2.032.570/m² (1.99× mediana)
- Subgrupo 5 · Área 1361.36 m² · Obras con AIU $2.767.058.972
- Top 5 renglones que inflan el $/m²:
  - Fila 34 · ítem 2.003 · 2. PAVIMENTOS · LOSA DE CONCRETO MR45 (SUMINISTRO, FORMALETEADO, COLOCACIÓN, CURADO, JUNTAS Y ACABADO. INCLUYE CANASTILLA PASA JUNTA. · cant 672.84 M3 · **$1.004.653.737**
  - Fila 39 · ítem NP-123 [NP] · 2. PAVIMENTOS · MEZCLA ASFÁLTICA EN CALIENTE DENSA MD19 CON CEMENTO ASFÁLTICO CA 14 (Suministro, Extendido, Nivelación y Compactación
me · cant 140.19 M3 · **$219.371.275**
  - Fila 14 · ítem 1.006 · 1. PRELIMINARES · TRANSPORTE Y DISPOSICIÓN FINAL DE ESCOMBROS EN SITIO AUTORIZADO (DISTANCIA DE TRANSPORTE 21 KM). A DISTANCIA MAYOR DEL A · cant 3608.12 M3 · **$198.973.386**
  - Fila 20 · ítem 1.008 · 1. PRELIMINARES · ESTABILIZACIÓN DE SUBRASANTE CON RAJÓN, INCLUYE EQUIPO DE COMPACTACIÓN (SUMINISTRO, EXTENDIDO, NIVELACIÓN Y COMPACTACIÓN · cant 981.24 M3 · **$174.637.170**
  - Fila 30 · ítem NP-124 [NP] · 1. PRELIMINARES · BASE GRANULAR CLASE A (BG_A) CON RECICLADO DE CONCRETO HIDRAULICO (SUMINISTRO, EXTENDIDO, NIVELACIÓN, HUMEDECIMIENTO Y C · cant 700.89 M3 · **$168.491.152**

## Comparativa V1 (IDU 25-02-2026) vs V2 (VICON 21-04-2026) vs V4 (01-09-2026)

| CIV | V1 total | V2 total | V4 obras AIU | Δ V4−V1 | %V4/V1 | Δ V4−V2 | %V4/V2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 9004002 | $2.679.612.302 | $2.340.063.114 | $2.124.569.020 | $-555.043.282 | -20.71% | $-215.494.094 | -9.21% |
| 9003990 | $2.537.825.825 | $2.667.336.411 | $2.711.308.173 | $173.482.348 | 6.84% | $43.971.762 | 1.65% |
| 9003980 | $2.312.874.652 | $2.444.643.007 | $2.574.430.351 | $261.555.699 | 11.31% | $129.787.344 | 5.31% |
| 9003989 | $1.424.778.297 | $1.538.753.791 | $1.632.946.727 | $208.168.430 | 14.61% | $94.192.936 | 6.12% |
| 9003981 | $1.972.706.135 | $2.041.220.357 | $2.038.357.883 | $65.651.748 | 3.33% | $-2.862.474 | -0.14% |
| 9003967 | $1.850.363.381 | $2.075.372.979 | $2.226.451.976 | $376.088.595 | 20.33% | $151.078.997 | 7.28% |
| 9003968 | $1.767.059.390 | $1.856.888.679 | $1.630.625.372 | $-136.434.018 | -7.72% | $-226.263.307 | -12.19% |
| 16000016 | $1.157.651.934 | $1.299.966.980 | $1.745.875.067 | $588.223.133 | 50.81% | $445.908.087 | 34.30% |
| 16000007 | $696.444.456 | $815.380.689 | $721.728.089 | $25.283.633 | 3.63% | $-93.652.600 | -11.49% |
| 16000023 | $2.751.554.997 | $2.880.817.470 | $2.572.153.672 | $-179.401.325 | -6.52% | $-308.663.798 | -10.71% |
| 16000012 | $2.226.684.665 | $2.358.154.014 | $2.347.962.590 | $121.277.925 | 5.45% | $-10.191.424 | -0.43% |
| 16000010 | $1.704.354.625 | $3.827.888.648 | $3.950.103.092 | $2.245.748.467 | 131.77% | $122.214.444 | 3.19% |
| 16000013 | $1.893.852.881 | $1.258.518.912 | $2.149.935.500 | $256.082.619 | 13.52% | $891.416.588 | 70.83% |
| 16000024 | $3.752.120.822 | $4.238.174.174 | $5.899.197.969 | $2.147.077.147 | 57.22% | $1.661.023.795 | 39.19% |
| 16000017 | $1.533.890.165 | $1.888.172.582 | $2.767.058.972 | $1.233.168.807 | 80.39% | $878.886.390 | 46.55% |
| 16000029 | $585.887.485 | $785.835.853 | $812.448.409 | $226.560.924 | 38.67% | $26.612.556 | 3.39% |
| 16000028 | $2.048.902.433 | $2.205.169.960 | $2.407.629.903 | $358.727.470 | 17.51% | $202.459.943 | 9.18% |
| 16000060 | $1.512.963.553 | $1.822.060.696 | $1.624.271.261 | $111.307.708 | 7.36% | $-197.789.435 | -10.86% |
| 16000052 | $2.087.411.444 | $2.168.192.162 | $2.190.004.906 | $102.593.462 | 4.91% | $21.812.744 | 1.01% |
| 16000043 | $1.815.561.841 | $1.928.040.404 | $1.790.457.295 | $-25.104.546 | -1.38% | $-137.583.109 | -7.14% |
| 16000032 | $1.643.316.068 | $2.104.600.859 | $1.875.405.919 | $232.089.851 | 14.12% | $-229.194.940 | -10.89% |
| 16000027 | $1.639.392.473 | $2.096.946.548 | $1.767.518.686 | $128.126.213 | 7.82% | $-329.427.862 | -15.71% |
| 16000038 | $1.939.975.267 | $2.167.849.792 | $2.560.234.587 | $620.259.320 | 31.97% | $392.384.795 | 18.10% |
| 16000057 | $1.682.838.531 | $1.796.568.803 | $1.789.265.635 | $106.427.104 | 6.32% | $-7.303.168 | -0.41% |
| 500002375 | $1.414.104.748 | $1.565.392.676 | $1.486.799.059 | $72.694.311 | 5.14% | $-78.593.617 | -5.02% |
| 16000047 | $1.743.449.483 | $1.950.567.933 | $1.701.875.688 | $-41.573.795 | -2.38% | $-248.692.245 | -12.75% |
| 16000077 | $1.097.565.022 | $1.159.443.953 | $1.098.318.068 | $753.046 | 0.07% | $-61.125.885 | -5.27% |

Nota: en `civs_cont` el CIV `16004876 (50002375)` se normaliza a `500002375` en V4 (mismo segmento 91029906).

## Grupos alcance (Hoja1 / alcance_alt2)

| Grupo | # CIVs | Obras con AIU | Componentes | Total | Referencia BRIEF |
|---|---:|---:|---:|---:|---:|
| ya_iniciados | 9 | $19.651.807.277 | $5.818.065.828 | $25.469.873.105 | ~$19.652.000.000 |
| por_iniciar | 9 | $19.033.849.055 | $5.635.114.633 | $24.668.963.688 | ~$19.034.000.000 |
| no_alcanza | 9 | $19.511.277.537 | $5.776.460.938 | $25.287.738.475 | ~$19.511.000.000 |

## Redes vs sin redes por CIV

| CIV | Redes (cap 5+6) | Sin redes (1-4+7) | %redes |
|---|---:|---:|---:|
| 16000010 | $2.545.642.843 | $1.404.460.249 | 64.44% |
| 16000052 | $1.026.428.609 | $1.163.576.297 | 46.87% |
| 9003989 | $748.630.721 | $884.316.006 | 45.85% |
| 16000043 | $820.086.334 | $970.370.961 | 45.8% |
| 9003981 | $926.684.455 | $1.111.673.428 | 45.46% |
| 9003968 | $739.353.959 | $891.271.413 | 45.34% |
| 16000024 | $2.441.374.706 | $3.457.823.263 | 41.38% |
| 16000023 | $1.062.245.710 | $1.509.907.962 | 41.3% |
| 16000077 | $440.700.013 | $657.618.055 | 40.12% |
| 16000038 | $962.795.485 | $1.597.439.102 | 37.61% |
| 16000047 | $638.280.133 | $1.063.595.555 | 37.5% |
| 16000057 | $670.237.683 | $1.119.027.952 | 37.46% |
| 16000060 | $608.045.423 | $1.016.225.838 | 37.43% |
| 9003980 | $959.707.179 | $1.614.723.172 | 37.28% |
| 16000007 | $268.699.995 | $453.028.094 | 37.23% |
| 9004002 | $761.617.958 | $1.362.951.062 | 35.85% |
| 9003990 | $935.019.206 | $1.776.288.967 | 34.49% |
| 9003967 | $765.027.342 | $1.461.424.634 | 34.36% |
| 500002375 | $500.266.561 | $986.532.498 | 33.65% |
| 16000032 | $614.214.506 | $1.261.191.413 | 32.75% |
| 16000027 | $562.008.303 | $1.205.510.383 | 31.8% |
| 16000028 | $743.524.891 | $1.664.105.012 | 30.88% |
| 16000012 | $696.553.021 | $1.651.409.569 | 29.67% |
| 16000029 | $214.637.920 | $597.810.489 | 26.42% |
| 16000013 | $503.142.301 | $1.646.793.199 | 23.4% |
| 16000017 | $576.861.638 | $2.190.197.334 | 20.85% |
| 16000016 | $348.110.105 | $1.397.764.962 | 19.94% |

## NP vs Contractual por CIV

| CIV | Contractual | NP | %NP |
|---|---:|---:|---:|
| 16000010 | $1.641.253.281 | $2.308.849.811 | 58.45% |
| 16000043 | $1.254.424.864 | $536.032.431 | 29.94% |
| 16000023 | $1.809.437.754 | $762.715.918 | 29.65% |
| 16000077 | $813.582.897 | $284.735.171 | 25.92% |
| 16000052 | $1.624.351.384 | $565.653.522 | 25.83% |
| 16000038 | $1.902.141.359 | $658.093.228 | 25.7% |
| 9003968 | $1.245.329.889 | $385.295.483 | 23.63% |
| 16000007 | $551.520.281 | $170.207.808 | 23.58% |
| 9003981 | $1.577.535.652 | $460.822.231 | 22.61% |
| 16000028 | $1.867.680.571 | $539.949.332 | 22.43% |
| 16000060 | $1.260.150.391 | $364.120.870 | 22.42% |
| 9003967 | $1.742.167.344 | $484.284.632 | 21.75% |
| 9003989 | $1.279.318.883 | $353.627.844 | 21.66% |
| 16000027 | $1.389.457.672 | $378.061.014 | 21.39% |
| 16000013 | $1.692.490.026 | $457.445.474 | 21.28% |
| 16000016 | $1.374.972.968 | $370.902.099 | 21.24% |
| 16000032 | $1.481.597.428 | $393.808.491 | 21.0% |
| 16000012 | $1.855.973.889 | $491.988.701 | 20.95% |
| 500002375 | $1.178.996.057 | $307.803.002 | 20.7% |
| 16000047 | $1.349.980.309 | $351.895.379 | 20.68% |
| 9003990 | $2.154.033.081 | $557.275.092 | 20.55% |
| 16000057 | $1.427.306.961 | $361.958.674 | 20.23% |
| 16000017 | $2.227.765.877 | $539.293.095 | 19.49% |
| 9004002 | $1.711.007.819 | $413.561.201 | 19.47% |
| 9003980 | $2.078.638.810 | $495.791.541 | 19.26% |
| 16000029 | $672.399.443 | $140.048.966 | 17.24% |
| 16000024 | $4.882.494.422 | $1.016.703.547 | 17.23% |

## Hallazgos y recomendaciones

### H03-01 · [INFO] Suma de obras con AIU por CIV cuadra a fila 688
- Descripción: Suma de it.civ[cid].valor (excluye ACEROS) = $58,196,933,869. Esperado (fila 688 col M) = $58,196,933,800. Δ = $69
- Fuente: PRESUPUESTO TODOS LOS CIV 84 NP fila 688
- Impacto: $69
- Recomendación: Cuadre verificado; no requiere acción si Δ es residual (<$1.000). Si es mayor, revisar redondeos por CIV.

### H03-02 · [INFO] Suma total con componentes cuadra a fila 703
- Descripción: Obras+componentes por CIV = $75,426,575,268. Esperado = $75,426,575,199. Δ = $69
- Fuente: PRESUPUESTO TODOS LOS CIV 84 NP fila 703
- Impacto: $69
- Recomendación: Cuadre verificado si Δ residual. En caso contrario, revisar reparto de componentes.

### H03-OUT-16000024 · [ALTA] CIV 16000024 (KR 65A) es outlier de $/m² con $2,454,941/m²
- Descripción: $/m² = $2,454,941 (2.41× mediana $1,019,119/m²). Obras con AIU = $5,899,197,969. Top 3 renglones: [2] LOSA DE CONCRETO MR45 (SUMINISTRO, FORMALETEADO, COLOCACIÓN, $1,527,099,650; [5] Proyecto: factibilidad, estudios y diseños de aceras, ciclor $701,876,415; [5] SUBBASE GRANULAR CLASE B (SBG_B) CON RECICLADO DE CONCRETO H $595,505,259
- Fuente: PRESUPUESTO TODOS LOS CIV 84 NP fila múltiples
- Impacto: $5.899.197.969
- Recomendación: Solicitar al contratista soporte técnico y de cantidades para renglones dominantes. Comparar con V1/V2 y verificar consistencia con memorias de cantidades.

### H03-OUT-16000010 · [ALTA] CIV 16000010 (CL18B) es outlier de $/m² con $2,317,646/m²
- Descripción: $/m² = $2,317,646 (2.27× mediana $1,019,119/m²). Obras con AIU = $3,950,103,092. Top 3 renglones: [5] CONTRATO 1752-2021 - BOX CULVERT PREFABRICADO TIPO 1, Ancho  $1,879,745,340; [2] LOSA DE CONCRETO MR45 (SUMINISTRO, FORMALETEADO, COLOCACIÓN, $556,140,139; [2] MEZCLA ASFÁLTICA EN CALIENTE DENSA MD19 CON CEMENTO ASFÁLTIC $121,429,566
- Fuente: PRESUPUESTO TODOS LOS CIV 84 NP fila múltiples
- Impacto: $3.950.103.092
- Recomendación: Solicitar al contratista soporte técnico y de cantidades para renglones dominantes. Comparar con V1/V2 y verificar consistencia con memorias de cantidades.

### H03-OUT-16000017 · [ALTA] CIV 16000017 (KR 65A) es outlier de $/m² con $2,032,570/m²
- Descripción: $/m² = $2,032,570 (1.99× mediana $1,019,119/m²). Obras con AIU = $2,767,058,972. Top 3 renglones: [2] LOSA DE CONCRETO MR45 (SUMINISTRO, FORMALETEADO, COLOCACIÓN, $1,004,653,737; [2] MEZCLA ASFÁLTICA EN CALIENTE DENSA MD19 CON CEMENTO ASFÁLTIC $219,371,275; [1] TRANSPORTE Y DISPOSICIÓN FINAL DE ESCOMBROS EN SITIO AUTORIZ $198,973,386
- Fuente: PRESUPUESTO TODOS LOS CIV 84 NP fila múltiples
- Impacto: $2.767.058.972
- Recomendación: Solicitar al contratista soporte técnico y de cantidades para renglones dominantes. Comparar con V1/V2 y verificar consistencia con memorias de cantidades.

### H03-NP-16000010 · [MEDIA] CIV 16000010: 58.45% del valor viene de NPs
- Descripción: Contractual $1,641,253,281 + NP $2,308,849,811 = obras totales. Alta dependencia de precios no pactados.
- Fuente: PRESUPUESTO TODOS LOS CIV 84 NP fila múltiples
- Impacto: $2.308.849.811
- Recomendación: Auditar NPs asignados a este CIV, verificar códigos IDU, análisis de precios unitarios y actas de fijación.
