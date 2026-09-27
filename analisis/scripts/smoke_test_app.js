// Smoke test rápido: valida que los JSON existen, que tienen las claves
// esperadas por index.html, y que las funciones críticas de la app pueden
// procesar los datos sin caerse.
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');

function loadJson(name) {
  return JSON.parse(fs.readFileSync(path.join(ROOT, name), 'utf-8'));
}

let errors = 0;
function check(cond, msg) {
  if (!cond) { console.log('  [FAIL]', msg); errors++; }
  else console.log('  [OK]  ', msg);
}

console.log('=== SMOKE TEST APP ===\n');

// 1. Los 4 JSON existen
const files = ['data.json', 'comparativa.json', 'analisis_2026_09.json', 'presupuesto_2026_09.json'];
files.forEach(f => check(fs.existsSync(path.join(ROOT, f)), `Existe ${f}`));

// 2. analisis_2026_09.json tiene las secciones esperadas
const P75 = loadJson('analisis_2026_09.json');
['meta', 'variacion_items', 'variacion_civ', 'costo_civ', 'aritmetica', 'nps', 'versiones_plazo', 'hallazgos'].forEach(k => {
  check(P75[k], `analisis_2026_09.json.${k} presente`);
});

// 3. Contadores clave
check((P75.variacion_items.items || []).length > 400, `>400 items en variacion_items (actual ${(P75.variacion_items.items||[]).length})`);
check((P75.variacion_civ.resumen_por_civ || []).length === 27, `27 CIVs en variacion_civ (actual ${(P75.variacion_civ.resumen_por_civ||[]).length})`);
check((P75.costo_civ.costo_por_civ || []).length === 27, `27 CIVs en costo_civ (actual ${(P75.costo_civ.costo_por_civ||[]).length})`);
check((P75.hallazgos || []).length >= 50, `>=50 hallazgos (actual ${(P75.hallazgos||[]).length})`);
check((P75.versiones_plazo.waterfall || []).length >= 10, `>=10 filas waterfall`);

// 4. Los totales cuadran
const total = (P75.costo_civ.costo_por_civ || []).reduce((s, c) => s + (c.total || 0), 0);
check(Math.abs(total - 75426575199) < 200, `Suma total 27 CIVs = ${total.toLocaleString('es-CO')} (esperado 75.426.575.199, delta ${(total-75426575199)})`);

const totObras = (P75.costo_civ.costo_por_civ || []).reduce((s, c) => s + (c.obras_total || 0), 0);
check(Math.abs(totObras - 58196933800) < 200, `Suma obras+AIU 27 CIVs = ${totObras.toLocaleString('es-CO')} (esperado 58.196.933.800)`);

// 5. Estados en items (para chip de filtro)
const items = P75.variacion_items.items;
const states = new Set(items.map(i => i.estado).filter(Boolean));
check(states.size >= 5, `>=5 estados posibles: ${[...states].join(', ')}`);

// 6. Detección del bug 16004876
const COMP = loadJson('comparativa.json');
const noAlcanza = COMP.alcance_alt2.no_alcanza;
const civIds = COMP.civs_cont.map(c => c.id);
const shortIds = COMP.civs_cont.map(c => String(c.id).split(' ')[0]);
noAlcanza.forEach(id => {
  const found = civIds.includes(id) || shortIds.includes(id);
  check(found, `Alcance no_alcanza incluye CIV ${id} (short match: ${shortIds.includes(id)})`);
});

// 7. Waterfall totales
const wf = P75.versiones_plazo.waterfall;
const tot = wf.find(w => w.componente && w.componente.toUpperCase().includes('TOTAL'));
if (tot) {
  check(tot.v0 === 59426575199, `Waterfall V0 total = 59.426.575.199 (actual ${tot.v0})`);
  check(tot.v4 === 75426575199, `Waterfall V4 total = 75.426.575.199 (actual ${tot.v4})`);
}

// 8. Capítulos concilian
const caps = P75.variacion_items.capitulos;
const capIni = caps.reduce((s, c) => s + (c.valor_inicial || 0), 0);
const capFin = caps.reduce((s, c) => s + (c.valor_final || 0), 0);
check(Math.abs(capIni - 44303294799) < 100, `Sum capitulos valor_inicial = ${capIni.toLocaleString('es-CO')}`);
check(Math.abs(capFin - 58196933800) < 100, `Sum capitulos valor_final = ${capFin.toLocaleString('es-CO')}`);

console.log('\n=== RESULTADO ===');
console.log(errors === 0 ? 'TODAS LAS PRUEBAS OK' : `${errors} pruebas FALLARON`);
process.exit(errors === 0 ? 0 : 1);
