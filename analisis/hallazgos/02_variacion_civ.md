# 02 - Variacion de cantidades por CIV

## Resumen ejecutivo

- 27 CIVs analizados (mapeo especial 500002375 -> 50002375 en data.json).
- Obras iniciales globales (col N Excel): $44.303.294.799
- Contrato firmado (obras+AIU V0): $44.303.294.799
- Reconstruccion por CIV (cant_data * L_v4): $41.842.985.108
- Delta reconstruccion vs col N: $-2.460.309.691
- Obras finales V4 (col M): $58.196.933.869

## Mapeo de CIVs
| id_v4 | id_data | id_cont | id_memoria | nomenclatura | desde_hasta | area_m2 | notas |
|---|---|---|---|---|---|---:|---|
| 9004002 | 9004002 | 9004002 | 9004002 | CL20 | KR68A - KR68B | 2.710 | - |
| 9003990 | 9003990 | 9003990 | 9003990 | CL20 | KR68B - KR68C | 2.979 | - |
| 9003980 | 9003980 | 9003980 | 9003980 | CL20 | KR68C - AK68D | 2.373 | - |
| 9003989 | 9003989 | 9003989 | 9003989 | KR 68B | CL20 - CL21 | 1.404 | - |
| 9003981 | 9003981 | 9003981 | 9003981 | KR 68B | CL21 - CL22 | 1.985 | - |
| 9003967 | 9003967 | 9003967 | 9003967 | KR 68C | CL21 - CL22 | 2.419 | - |
| 9003968 | 9003968 | 9003968 | 9003968 | CL21 | KR 68C - KR 68D | 1.537 | - |
| 16000016 | 16000016 | 16000016 | 16000016 | KR 66 | CL17A - CL18 | 1.608 | - |
| 16000007 | 16000007 | 16000007 | 16000007 | KR66 | CL18A - CL18B | 1.045 | - |
| 16000023 | 16000023 | 16000023 | 16000023 | CL17A | KR65B - KR66 | 2.852 | - |
| 16000012 | 16000012 | 16000012 | 16000012 | CL18A | KR65B - KR66 | 2.544 | - |
| 16000010 | 16000010 | 16000010 | 16000010 | CL18B | KR65B - KR66 | 1.704 | - |
| 16000013 | 16000013 | 16000013 | 16000013 | CL18B | KR65A - KR65B | 1.541 | - |
| 16000024 | 16000024 | 16000024 | 16000024 | KR 65A | CL18 - CL18A | 2.402 | - |
| 16000017 | 16000017 | 16000017 | 16000017 | KR 65A | CL18A - CL18B | 1.361 | - |
| 16000029 | 16000029 | 16000029 | 16000029 | CL18 | KR65 - KR65A | 939 | - |
| 16000028 | 16000028 | 16000028 | 16000028 | CL18A | KR63 - KR65A | 2.749 | - |
| 16000060 | 16000060 | 16000060 | 16000060 | KR63 | ACCESO VIA 17 - CL17 | 1.593 | - |
| 16000052 | 16000052 | 16000052 | 16000052 | KR63 | ACCESO VIA 17B - CL17B | 1.791 | - |
| 16000043 | 16000043 | 16000043 | 16000043 | KR 63 | CL17B - CL18 | 1.519 | - |
| 16000032 | 16000032 | 16000032 | 16000032 | KR 63 | CL18 - CL18A | 1.835 | - |
| 16000027 | 16000027 | 16000027 | 16000027 | KR 63 | CL18A - CL19 | 1.958 | - |
| 16000038 | 16000038 | 16000038 | 16000038 | CL18A | KR62 - KR63 | 2.644 | - |
| 16000057 | 16000057 | 16000057 | 16000057 | CL17B | KR63 - KR62 | 1.996 | - |
| 500002375 | 50002375 | 16004876 (50002375) | 50002375 | KR65 | CL17 - CL18 | 1.159 | Tramo compartido con 16000047 (segmento 91029906) |
| 16000047 | 16000047 | 16000047 | 16000047 | KR65 | CL17 - CL18 | 2.387 | - |
| 16000077 | 16000077 | 16000077 | 16000077 | CL14 | KR65 - CL CIEGA | 1.237 | - |

## Resumen por CIV (obras con AIU)
| CIV | Nomenclatura | Area m2 | Iniciales | Finales V4 | Delta | Delta % |
|---|---|---:|---:|---:|---:|---:|
| 9004002 | CL20 | 2.710 | $1.919.271.224 | $2.124.569.020 | $205.297.796 | 10.7% |
| 9003990 | CL20 | 2.979 | $2.306.495.798 | $2.711.308.173 | $404.812.375 | 17.6% |
| 9003980 | CL20 | 2.373 | $1.773.268.906 | $2.574.430.351 | $801.161.445 | 45.2% |
| 9003989 | KR 68B | 1.404 | $1.050.018.340 | $1.632.946.727 | $582.928.387 | 55.5% |
| 9003981 | KR 68B | 1.985 | $1.390.366.740 | $2.038.357.883 | $647.991.143 | 46.6% |
| 9003967 | KR 68C | 2.419 | $1.756.193.191 | $2.226.451.976 | $470.258.785 | 26.8% |
| 9003968 | CL21 | 1.537 | $1.104.610.337 | $1.630.625.372 | $526.015.035 | 47.6% |
| 16000016 | KR 66 | 1.608 | $1.301.940.735 | $1.745.875.067 | $443.934.332 | 34.1% |
| 16000007 | KR66 | 1.045 | $638.820.344 | $721.728.089 | $82.907.745 | 13.0% |
| 16000023 | CL17A | 2.852 | $2.231.841.440 | $2.572.153.672 | $340.312.232 | 15.2% |
| 16000012 | CL18A | 2.544 | $2.073.695.190 | $2.347.962.590 | $274.267.400 | 13.2% |
| 16000010 | CL18B | 1.704 | $2.291.612.786 | $3.950.103.092 | $1.658.490.306 | 72.4% |
| 16000013 | CL18B | 1.541 | $828.228.169 | $2.149.935.500 | $1.321.707.331 | 159.6% |
| 16000024 | KR 65A | 2.402 | $2.226.670.707 | $5.899.197.969 | $3.672.527.262 | 164.9% |
| 16000017 | KR 65A | 1.361 | $1.441.265.454 | $2.767.058.972 | $1.325.793.518 | 92.0% |
| 16000029 | CL18 | 939 | $404.749.337 | $812.448.409 | $407.699.072 | 100.7% |
| 16000028 | CL18A | 2.749 | $2.172.680.596 | $2.407.629.903 | $234.949.307 | 10.8% |
| 16000060 | KR63 | 1.593 | $1.711.978.189 | $1.624.271.261 | $-87.706.928 | -5.1% |
| 16000052 | KR63 | 1.791 | $1.504.006.937 | $2.190.004.906 | $685.997.969 | 45.6% |
| 16000043 | KR 63 | 1.519 | $1.236.586.250 | $1.790.457.295 | $553.871.045 | 44.8% |
| 16000032 | KR 63 | 1.835 | $1.632.752.426 | $1.875.405.919 | $242.653.493 | 14.9% |
| 16000027 | KR 63 | 1.958 | $1.783.508.233 | $1.767.518.686 | $-15.989.547 | -0.9% |
| 16000038 | CL18A | 2.644 | $2.230.093.561 | $2.560.234.587 | $330.141.026 | 14.8% |
| 16000057 | CL17B | 1.996 | $1.289.824.581 | $1.789.265.635 | $499.441.054 | 38.7% |
| 500002375 | KR65 | 1.159 | $923.268.542 | $1.486.799.059 | $563.530.517 | 61.0% |
| 16000047 | KR65 | 2.387 | $1.665.738.688 | $1.701.875.688 | $36.137.000 | 2.2% |
| 16000077 | CL14 | 1.237 | $953.498.407 | $1.098.318.068 | $144.819.661 | 15.2% |

## Descomposicion del Δ por CIV
| CIV | Δ Aumentos | Δ Disminuciones | Δ NP | Δ Contractual nuevo | Δ Eliminado | Δ Neto |
|---|---:|---:|---:|---:|---:|---:|
| 9004002 | $182.289.767 | $-222.416.600 | $413.561.201 | $627.421.749 | $-795.558.323 | $205.297.794 |
| 9003990 | $285.378.781 | $-123.491.728 | $557.275.092 | $743.291.573 | $-1.057.641.346 | $404.812.372 |
| 9003980 | $373.301.602 | $-91.672.565 | $495.791.541 | $805.675.799 | $-781.934.933 | $801.161.444 |
| 9003989 | $142.657.619 | $-53.109.380 | $353.627.844 | $606.506.584 | $-466.754.282 | $582.928.385 |
| 9003981 | $211.844.855 | $-68.113.113 | $460.822.231 | $720.381.837 | $-676.944.668 | $647.991.142 |
| 9003967 | $247.663.809 | $-101.923.727 | $484.284.632 | $607.801.137 | $-767.567.066 | $470.258.785 |
| 9003968 | $114.389.159 | $-56.363.007 | $385.295.483 | $667.711.315 | $-585.017.918 | $526.015.032 |
| 16000016 | $399.145.087 | $-56.982.908 | $370.902.099 | $329.611.085 | $-598.741.031 | $443.934.332 |
| 16000007 | $37.365.767 | $-13.415.779 | $170.207.808 | $264.353.875 | $-375.603.926 | $82.907.745 |
| 16000023 | $227.331.221 | $-317.302.857 | $762.715.918 | $587.997.617 | $-920.429.664 | $340.312.235 |
| 16000012 | $304.226.839 | $-169.880.963 | $491.988.701 | $529.038.504 | $-881.105.685 | $274.267.396 |
| 16000010 | $224.247.396 | $-111.578.051 | $2.308.849.811 | $665.403.854 | $-1.428.432.706 | $1.658.490.304 |
| 16000013 | $861.412.774 | $-44.560.484 | $457.445.474 | $429.247.240 | $-381.837.675 | $1.321.707.329 |
| 16000024 | $1.670.481.233 | $-97.572.926 | $1.016.703.547 | $2.154.675.038 | $-1.071.759.634 | $3.672.527.258 |
| 16000017 | $1.062.929.957 | $-48.577.593 | $539.293.095 | $639.108.067 | $-866.960.011 | $1.325.793.515 |
| 16000029 | $240.435.035 | $-18.585.650 | $140.048.966 | $218.290.421 | $-172.489.705 | $407.699.067 |
| 16000028 | $231.309.119 | $-95.922.976 | $539.949.332 | $603.647.788 | $-1.044.033.960 | $234.949.303 |
| 16000060 | $139.062.675 | $-49.696.086 | $364.120.870 | $483.716.766 | $-1.024.911.155 | $-87.706.930 |
| 16000052 | $172.534.203 | $-49.812.815 | $565.653.522 | $739.488.299 | $-741.865.242 | $685.997.967 |
| 16000043 | $80.214.102 | $-33.865.848 | $536.032.431 | $622.362.254 | $-650.871.898 | $553.871.041 |
| 16000032 | $109.958.653 | $-87.754.333 | $393.808.491 | $649.995.927 | $-823.355.245 | $242.653.493 |
| 16000027 | $218.285.917 | $-38.185.778 | $378.061.014 | $459.268.542 | $-1.033.419.244 | $-15.989.549 |
| 16000038 | $321.723.334 | $-127.745.345 | $658.093.228 | $612.681.062 | $-1.134.611.255 | $330.141.024 |
| 16000057 | $221.529.676 | $-44.765.975 | $361.958.674 | $576.800.242 | $-616.081.563 | $499.441.054 |
| 500002375 | $280.116.868 | $-44.777.939 | $307.803.002 | $420.882.047 | $-400.493.465 | $563.530.513 |
| 16000047 | $177.888.720 | $-181.783.221 | $351.895.379 | $497.322.644 | $-809.186.522 | $36.137.000 |
| 16000077 | $140.554.724 | $-156.424.699 | $284.735.171 | $301.003.547 | $-425.049.082 | $144.819.661 |

## Outliers de cantidad por m2
| CIV | Metrica | Valor | Veces sobre mediana |
|---|---|---:|---:|
| 16000013 | anden_m2_por_m2 | 1.2087 | 5.49x |
| 16000017 | anden_m2_por_m2 | 0.8416 | 3.82x |
| 16000024 | anden_m2_por_m2 | 0.7324 | 3.33x |
| 16000017 | rajon_m3_por_m2 | 0.7208 | 2.79x |
| 16000017 | mezcla_asfaltica_md12_md19_m3_por_m2 | 0.103 | 2.79x |
| 16000017 | base_granular_bga_m3_por_m2 | 0.5148 | 2.79x |
| 16000024 | rajon_m3_por_m2 | 0.6846 | 2.65x |
| 16000024 | mezcla_asfaltica_md12_md19_m3_por_m2 | 0.0978 | 2.65x |
| 16000024 | base_granular_bga_m3_por_m2 | 0.489 | 2.65x |

## Top 30 celdas (item x CIV) con mayor Δ absoluto
| Row | Codigo | Item | CIV | Cant ini | Cant fin | Δ Cant | Δ Valor AIU |
|---:|---|---|---|---:|---:|---:|---:|
| 479 | N/A | NP-133 | 16000010 | 0.00 | 110.00 | 110.00 | $1.879.745.340 |
| 34 | 7785 | 2.003 | 16000024 | 449.82 | 1022.73 | 572.91 | $855.443.166 |
| 369 | 8643 | 5.037 | 16000024 | 0.00 | 10554.85 | 10554.85 | $701.876.415 |
| 34 | 7785 | 2.003 | 16000017 | 219.62 | 672.84 | 453.22 | $676.723.124 |
| 405 | 4754 | 3.012 | 16000024 | 0.00 | 2916.97 | 2916.97 | $595.505.259 |
| 280 | 7447 | 5.052 | 16000010 | 120.00 | 0.00 | -120.00 | $-557.919.840 |
| 34 | 7785 | 2.003 | 16000013 | 141.00 | 433.17 | 292.17 | $436.249.385 |
| 39 | 8618 | NP-123 | 16000024 | 0.00 | 235.02 | 235.02 | $367.762.586 |
| 30 | 4744 | NP-124 | 16000024 | 0.00 | 1175.16 | 1175.16 | $282.503.763 |
| 20 | 6016 | 1.008 | 16000024 | 64.78 | 1645.20 | 1580.42 | $281.276.347 |
| 370 | 3017 | 5.038 | 16000024 | 0.00 | 4373.82 | 4373.82 | $241.198.678 |
| 39 | 8618 | NP-123 | 16000017 | 0.00 | 140.19 | 140.19 | $219.371.275 |
| 271 | 3923 | 5.043 | 16000027 | 90.86 | 0.00 | -90.86 | $-214.083.059 |
| 271 | 3923 | 5.043 | 16000043 | 89.07 | 0.00 | -89.07 | $-209.865.487 |
| 14 | 3017 | 1.006 | 16000024 | 2367.61 | 6049.64 | 3682.03 | $203.049.492 |
| 290 | 4299 | 5.062 | 16000060 | 98.00 | 0.00 | -98.00 | $-200.938.220 |
| 85 | 3425 | 3.039 | 16000013 | 6.29 | 1863.36 | 1857.07 | $186.562.808 |
| 271 | 3923 | 5.043 | 16000032 | 77.07 | 0.00 | -77.07 | $-181.591.255 |
| 85 | 3425 | 3.039 | 16000024 | 2.05 | 1760.01 | 1757.96 | $176.606.170 |
| 270 | 3922 | 5.042 | 16000060 | 97.85 | 0.00 | -97.85 | $-172.908.581 |
| 531 | 5182 | 6.007 | 9003990 | 0.00 | 304.98 | 304.98 | $169.366.068 |
| 20 | 6016 | 1.008 | 16000017 | 31.76 | 981.24 | 949.48 | $168.984.443 |
| 30 | 4744 | NP-124 | 16000017 | 0.00 | 700.89 | 700.89 | $168.491.152 |
| 39 | 8618 | NP-123 | 9003990 | 0.00 | 105.00 | 105.00 | $164.305.470 |
| 285 | 7876 | 5.057 | 16000032 | 92.20 | 0.00 | -92.20 | $-164.108.626 |
| 268 | 3919 | 5.040 | 16000017 | 181.55 | 0.00 | -181.55 | $-160.357.023 |
| 490 | 5182 | 6.007 | 16000024 | 285.82 | 0.00 | -285.82 | $-158.723.673 |
| 490 | 5182 | 6.007 | 16000060 | 285.82 | 0.00 | -285.82 | $-158.723.673 |
| 33 | 6313 | 2.002 | 16000023 | 104.64 | 0.00 | -104.64 | $-157.164.730 |
| 465 | 7435 | NP-19 | 16000043 | 0.00 | 62.35 | 62.35 | $154.807.755 |

## Hallazgos
### H02-001 - [MEDIA] Reparto de la linea base por CIV no publicado por el contratista
- **Fuente**: PRESUPUESTO TODOS LOS CIV 84 NP · col H (linea base) vs bloque S:BW (matriz por CIV)
- **Impacto**: $2.460.309.691
- **Descripcion**: La col N del Excel suma $44,303,294,799 de valor inicial con AIU global. La reconstruccion por CIV (multiplicando cantidad_inicial_data_json * VU actualizado L) suma $41,842,985,108 (delta $-2,460,309,691). El Excel no reparte la cantidad contractual (col H) por CIV, por lo que la linea base por CIV se estima con data.json (contrato firmado); es un pixel-perfect solo para los ítems que mantuvieron el codigo_idu.
- **Recomendacion**: Pedir al contratista el reparto oficial de la cantidad contractual por CIV (col H desagregada) para auditar al peso el Delta por CIV.

### H02-101 - [ALTA] CIV 16000024 (KR 65A) con Δ obras $3,672,527,262
- **Fuente**: PRESUPUESTO TODOS LOS CIV 84 NP · columnas del CIV
- **Impacto**: $3.672.527.262
- **Descripcion**: Obras iniciales $2,226,670,707 -> finales $5,899,197,969. Delta = $3,672,527,262 (164.9%).
- **Recomendacion**: Solicitar justificacion tecnica del Δ por CIV con documentacion de campo y tramites IDU.

### H02-102 - [ALTA] CIV 16000010 (CL18B) con Δ obras $1,658,490,306
- **Fuente**: PRESUPUESTO TODOS LOS CIV 84 NP · columnas del CIV
- **Impacto**: $1.658.490.306
- **Descripcion**: Obras iniciales $2,291,612,786 -> finales $3,950,103,092. Delta = $1,658,490,306 (72.4%).
- **Recomendacion**: Solicitar justificacion tecnica del Δ por CIV con documentacion de campo y tramites IDU.

### H02-103 - [ALTA] CIV 16000017 (KR 65A) con Δ obras $1,325,793,518
- **Fuente**: PRESUPUESTO TODOS LOS CIV 84 NP · columnas del CIV
- **Impacto**: $1.325.793.518
- **Descripcion**: Obras iniciales $1,441,265,454 -> finales $2,767,058,972. Delta = $1,325,793,518 (92.0%).
- **Recomendacion**: Solicitar justificacion tecnica del Δ por CIV con documentacion de campo y tramites IDU.

### H02-104 - [ALTA] CIV 16000013 (CL18B) con Δ obras $1,321,707,331
- **Fuente**: PRESUPUESTO TODOS LOS CIV 84 NP · columnas del CIV
- **Impacto**: $1.321.707.331
- **Descripcion**: Obras iniciales $828,228,169 -> finales $2,149,935,500. Delta = $1,321,707,331 (159.6%).
- **Recomendacion**: Solicitar justificacion tecnica del Δ por CIV con documentacion de campo y tramites IDU.

### H02-105 - [ALTA] CIV 9003980 (CL20) con Δ obras $801,161,445
- **Fuente**: PRESUPUESTO TODOS LOS CIV 84 NP · columnas del CIV
- **Impacto**: $801.161.445
- **Descripcion**: Obras iniciales $1,773,268,906 -> finales $2,574,430,351. Delta = $801,161,445 (45.2%).
- **Recomendacion**: Solicitar justificacion tecnica del Δ por CIV con documentacion de campo y tramites IDU.

### H02-200 - [MEDIA] CIV 16000013: intensidad de andén (m²/m²) 5,49× la mediana
- **Fuente**: PRESUPUESTO TODOS LOS CIV 84 NP · columnas del CIV
- **Impacto**: $0
- **Descripcion**: Ratio anden_m2_por_m2 = 1.2087, 5.49x sobre la mediana de los 27 CIVs.
- **Recomendacion**: Verificar en campo si la cantidad final del renglon corresponde al tramo real.

### H02-201 - [MEDIA] CIV 16000017: intensidad de andén (m²/m²) 3,82× la mediana
- **Fuente**: PRESUPUESTO TODOS LOS CIV 84 NP · columnas del CIV
- **Impacto**: $0
- **Descripcion**: Ratio anden_m2_por_m2 = 0.8416, 3.82x sobre la mediana de los 27 CIVs.
- **Recomendacion**: Verificar en campo si la cantidad final del renglon corresponde al tramo real.

### H02-202 - [MEDIA] CIV 16000024: intensidad de andén (m²/m²) 3,33× la mediana
- **Fuente**: PRESUPUESTO TODOS LOS CIV 84 NP · columnas del CIV
- **Impacto**: $0
- **Descripcion**: Ratio anden_m2_por_m2 = 0.7324, 3.33x sobre la mediana de los 27 CIVs.
- **Recomendacion**: Verificar en campo si la cantidad final del renglon corresponde al tramo real.

### H02-203 - [MEDIA] CIV 16000017: intensidad de rajón (m³/m²) 2,79× la mediana
- **Fuente**: PRESUPUESTO TODOS LOS CIV 84 NP · columnas del CIV
- **Impacto**: $0
- **Descripcion**: Ratio rajon_m3_por_m2 = 0.7208, 2.79x sobre la mediana de los 27 CIVs.
- **Recomendacion**: Verificar en campo si la cantidad final del renglon corresponde al tramo real.

### H02-204 - [MEDIA] CIV 16000017: intensidad de mezcla asfáltica MD12+MD19 (m³/m²) 2,79× la mediana
- **Fuente**: PRESUPUESTO TODOS LOS CIV 84 NP · columnas del CIV
- **Impacto**: $0
- **Descripcion**: Ratio mezcla_asfaltica_md12_md19_m3_por_m2 = 0.1030, 2.79x sobre la mediana de los 27 CIVs.
- **Recomendacion**: Verificar en campo si la cantidad final del renglon corresponde al tramo real.

### H02-300 - [INFO] Mapeo especial CIV 500002375 = 16004876 = 50002375
- **Fuente**: hoja principal + MEMORIA CANTIDADES + Hoja1 · fila 3 IDs
- **Impacto**: $0
- **Descripcion**: El CIV V4 500002375 corresponde al tramo KR65 CL17-CL18 y se llama 16004876 en data.json, 16004876 en Hoja1 y 50002375 en MEMORIA CANTIDADES. Comparte segmento 91029906 con el CIV 16000047.
- **Recomendacion**: Unificar la nomenclatura en documentos futuros (usar siempre el 500002375 IDU actual).

## Metodologia
- Fuente V4: analisis/datos/presupuesto_2026_09.json (matriz ítem x CIV con AIU).
- Fuente V0 (linea base): data.json → items[*].cantidades. Los NPs no tienen linea base.
- El mapeo CIV 500002375 <-> 16004876 <-> 50002375 (KR65 CL17-CL18) se aplica en todas las tablas.
- AIU contractual = 1,31849. Los valores por celda del JSON estan con AIU; el CD se obtiene dividiendo.
- Los ratios por m2 usan el area de data.json[civs].