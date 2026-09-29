# Plano 3D · antes vs. ahora

Plano 3D interactivo de los **27 CIV del Grupo 2** (contrato IDU 1752-2021, Consorcio VICON 024, interventoría Consorcio Montevideo 045). Compara el presupuesto contractual (**V0**) con el presupuesto radicado el 01-09-2026 (**V4**, 75MM · 8 meses) sobre la geometría real de las calles.

Se abre desde la pestaña **Presupuesto 01-09-2026 · 75MM · 8 meses → Resumen → «Plano 3D · antes vs. ahora»**. Usa la misma sesión que la aplicación: si se abre sin sesión, muestra el acceso y, después de ingresar, vuelve al plano.

## Qué muestra

| Tipo de mapa | Altura | Color | «Ambos» (V0 vs V4) |
|---|---|---|---|
| **Costos** | valor de obra del CIV (con AIU) | costo por m² (rampa de un solo tono) | sólido = V4, contorno de vidrio = V0 |
| **Variación** | tamaño de Δ V4 − V0 en pesos | divergente: rojo sube, azul baja, gris sin cambio | ya es la diferencia |
| **Estructural** | espesor equivalente de cada capa (m³ ÷ área), exagerado | capa: estabilización, subbase, base, losa, asfalto | franja de alambre = V0, sólida = V4 |
| **Materiales** | columna apilada por material | 8 materiales + «otros» | franja de alambre = V0, sólida = V4 |
| **Redes** | subsuelo: un tubo por red (grosor ∝ valor) | hidrosanitarias / redes secas | tubo de vidrio = V0 |
| **No previstos** | valor NP del CIV en V4 (contorno = total V4) | % del CIV que es NP | solo existe en V4 |
| **Alcance** | valor del CIV | grupo de la Hoja1: ya iniciados, por iniciar, no alcanza | sólido = V4, vidrio = V0 |
| **Simulación** | fases que se construyen mes a mes | fase de obra | — |

- **Etiquetas flotantes** sobre cada calle con el valor, el cambio y mini-barras de materiales o capas. Se ocultan solas para no taparse, con prioridad para el CIV seleccionado y los que tienen hallazgos de severidad alta (▲). El nivel de detalle cambia con el zoom.
- **Detalle del CIV** (clic sobre la calle, su etiqueta o el ranking):
  - V0, V4, Δ y NP.
  - Barras de materiales antes/ahora con tabla.
  - Corte de la estructura de pavimento.
  - Redes y andenes.
  - Renglones que más cambian.
  - Hallazgos enlazados a su ficha en el análisis.
  - Botón «Abrir ficha en el análisis» (`../index.html#p75/civ/<id>`).
- **Cinco paletas**:
  - Noche, Claro y Plano azul usan la paleta categórica de referencia en su orden fijo.
  - Alto contraste usa Okabe-Ito re-escalonado sobre blanco.
  - Realista usa colores figurativos de obra: asfalto, concreto, granular, ladrillo.

  Las cuatro primeras se validaron con el verificador de paletas (separación para daltonismo ΔE ≥ 8 entre capas vecinas y banda de luminosidad). La realista es figurativa y se apoya en leyenda y etiquetas.
- **Vistas** General, SG2 · Montevideo, SG5 · Puente Aranda y Planta; brújula, escala, exageración vertical, capas (edificios, nombres de vías, sombras, alertas de hallazgos).
- **Ranking** de los 27 CIV según el mapa activo y **descarga CSV** (27 filas × 50 columnas).
- **Enlace compartible**: el estado (mapa, comparación, paleta, CIV, simulación) queda en la URL (`#m=materiales&c=ambos&p=noche&civ=16000024`).
- Responsivo:
  - En el teléfono los paneles son hojas inferiores con botón **✕ Cerrar** siempre visible.
  - Una barra inferior da acceso a Mapa, Leyenda, Simular y Detalle.
  - Un mini-reproductor queda visible mientras corre la simulación.

## Simulación por plazos (4D tiempo + 5D costo)

Ilustrativa: el contratista no entregó cronograma (registro de auditoría C-04). Es un modelo por eventos:

1. Los frentes se movilizan escalonados (un frente cada *n* meses) y toman el siguiente CIV de la cola cuando quedan libres. El orden de la cola se elige: mayor valor primero, por grupo de la Hoja1, SG2 → SG5, o de norte a sur.
2. Cada CIV ejecuta sus fases en secuencia: tierras → redes → estructura → carpeta → andenes → acabados.
3. Cada frente produce hasta la **producción máxima por frente** (supuesto, $500M/mes por defecto).
4. El **ritmo mensual** es un tope que se reparte entre los frentes activos: tasa por frente = mín(producción máxima, ritmo ÷ frentes activos).

| Escenario | Qué se ejecuta |
|---|---|
| **Δ oficial de obra** (por defecto) | $13.894M = V4 fila 688 − V0 fila 688, repartido entre los CIV en proporción al Δ del plano. Es lo que financian los $1.737M/mes de obra × 8 meses. |
| Δ del plano por CIV | $16.458M: suma de los aumentos por CIV. Incluye $2.460M de V0 sin reparto por CIV. |
| Por iniciar + no alcanza | V4 completo de esos 18 CIV. |
| 27 CIV completos | V4 completo. |

Ritmos:
- **Solicitado**: $1.737M/mes de obra. Es la parte de obra de los $2.000M/mes pedidos; los otros $263M/mes son gestión.
- **Histórico**: ≈ $600M/mes, la cota superior del hallazgo H06-03.
- **Personalizado**.

Salidas de la simulación:
- **Tiempo real**:
  - El frente de obra avanza a lo largo de cada calle con un halo luminoso.
  - Las etiquetas muestran la fase y el %.
  - La línea de tiempo se puede arrastrar.
- **Gráficas**: curva S con la línea del plazo de 8 meses, flujo mensual contra el ritmo elegido, y Gantt por frente.
- **Veredicto**: si cabe en 8 meses, y si no, el ritmo o el número de frentes que haría falta.

Con los valores por defecto (Δ oficial, ritmo solicitado, 4 frentes de $500M/mes, movilización de 0,5 meses) el escenario termina en el **mes 8,7**. El ritmo pedido alcanza justo para 8 meses sin ningún tiempo muerto, así que la movilización de los frentes lo empuja fuera del plazo.

## Datos y método

- `datos/plano3d_datos.json`: los 27 CIV con geometría, V0/V4 por material y por fase, estructura, redes, ítems que más cambian y hallazgos. Lo genera `scripts/generar_plano3d.py` a partir de:
  - `../presupuesto_2026_09.json` (matriz ítem × CIV de V4);
  - `../data.json` (reparto contractual por CIV);
  - `../analisis_2026_09.json` (consolidado del análisis).
- **V0 por CIV** = cantidad contractual del renglón (col. H) × participación contractual del CIV (data.json), valorada con el VU con AIU de V4 (col. L), igual que el análisis 02. Σ V0 = $41.843M y Σ V4 = $58.197M cuadran al peso con el análisis 02. Hay $2.460M de V0 en renglones sin reparto por CIV que no se pueden ubicar en el plano.
- **Geometría**:
  - Eje de cada CIV cortado de OpenStreetMap entre los dos cruces del inventario IDU. La longitud resultante coincide con la del inventario: la mayoría a menos del 5 % y todas a menos del 18 %. Cada detalle trae su nota de geometría.
  - Casos especiales: la «KR65A» del IDU es la «Carrera 64» de OSM, y hay tramos partidos en dos CIV.
- `datos/contexto.json`: manzanas, edificios (altura por niveles × 3,2 m o por uso), zonas verdes, vías y rieles alrededor de los frentes.
- `datos/osm/`: descarga cruda de Overpass usada por el generador.

### Regenerar

```bash
python plano3d/scripts/descargar_osm.py      # opcional: vuelve a descargar OSM (prueba varios espejos de Overpass)
python plano3d/scripts/generar_plano3d.py    # requiere shapely; reescribe datos/plano3d_datos.json y datos/contexto.json
```

Para verlo en local sírvalo con un servidor web desde la raíz del repositorio (`python -m http.server`) y abra `http://localhost:8000/plano3d/`.

## Tecnología

- [three.js](https://threejs.org) r170 (importmap desde jsDelivr):
  - `MapControls` con zoom hacia el cursor.
  - `CSS2DRenderer` para las etiquetas HTML flotantes.
  - `mergeGeometries` para el contexto urbano (pocas llamadas de dibujo).
  - Sombras suaves.
- Cada calle es un prisma extruido a lo largo de su polilínea, con juntas en inglete. Un atributo `aT` (distancia recorrida 0→1) permite al sombreador cortar el volumen en el frente de obra (`discard`) y dibujar el halo de avance: es la técnica de construcción progresiva 4D.
- Sin dependencias de compilación: HTML + un módulo JS.

## Licencias y atribución

Geometría © [colaboradores de OpenStreetMap](https://www.openstreetmap.org/copyright), licencia ODbL, descargada vía Overpass API. three.js bajo licencia MIT.
