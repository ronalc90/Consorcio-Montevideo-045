// Plano 3D v2 · antes (V0) vs. ahora (V4) · Contrato IDU 1752-2021, Grupo 2 (27 CIV)
// three.js r170: MapControls, CSS2DRenderer (etiquetas flotantes), EffectComposer (GTAO + contorno + bloom + OutputPass),
// entorno PMREM, cúpula de cielo, árboles instanciados y líneas de flujo animadas. Datos: datos/plano3d_datos.json y
// datos/contexto.json (scripts/generar_plano3d.py). Geometría © colaboradores de OpenStreetMap (ODbL).
import * as THREE from 'three';
import { MapControls } from 'three/addons/controls/MapControls.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { GTAOPass } from 'three/addons/postprocessing/GTAOPass.js';
import { OutlinePass } from 'three/addons/postprocessing/OutlinePass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

// ───────────────────────── utilidades ─────────────────────────
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s ?? '').replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));
const nf = (v, d = 0) => (+v || 0).toLocaleString('es-CO', { minimumFractionDigits: d, maximumFractionDigits: d });
const fM = v => (v < 0 ? '−' : '') + '$' + nf(Math.abs(v) / 1e6) + 'M';
const fMs = v => (v > 0 ? '+' : v < 0 ? '−' : '±') + '$' + nf(Math.abs(v) / 1e6) + 'M';
const fm2 = v => '$' + nf(v / 1000) + ' mil/m²';
const fP = (v, d = 1) => (v > 0.05 ? '+' : v < -0.05 ? '−' : '±') + nf(Math.abs(v), d) + '%';
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
const sumv = o => Object.values(o || {}).reduce((a, b) => a + (+b || 0), 0);
const isMobile = () => matchMedia('(max-width: 760px)').matches;
const coarse = () => matchMedia('(pointer: coarse)').matches;
const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
const easeOut = t => 1 - Math.pow(1 - t, 3);
const rng = seed => () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
const lsGet = k => { try { return localStorage.getItem(k); } catch (_) { return null; } };
const lsSet = (k, v) => { try { localStorage.setItem(k, v); } catch (_) {} };

// Mezcla perceptual en OKLab (rampas secuenciales y divergentes de un solo tono)
const h2l = h => { h = h.replace('#', ''); return [0, 2, 4].map(i => { const c = parseInt(h.slice(i, i + 2), 16) / 255; return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; }); };
const l2h = rgb => '#' + rgb.map(c => { c = clamp(c, 0, 1); c = c <= 0.0031308 ? 12.92 * c : 1.055 * c ** (1 / 2.4) - 0.055; return Math.round(c * 255).toString(16).padStart(2, '0'); }).join('');
const toOk = ([r, g, b]) => { const l = Math.cbrt(.4122214708 * r + .5363325363 * g + .0514459929 * b), m = Math.cbrt(.2119034982 * r + .6806995451 * g + .1073969566 * b), s = Math.cbrt(.0883024619 * r + .2817188376 * g + .6299787005 * b); return [.2104542553 * l + .7936177850 * m - .0040720468 * s, 1.9779984951 * l - 2.4285922050 * m + .4505937099 * s, .0259040371 * l + .7827717662 * m - .8086757660 * s]; };
const fromOk = ([L, a, b]) => { const l = (L + .3963377774 * a + .2158037573 * b) ** 3, m = (L - .1055613458 * a - .0638541728 * b) ** 3, s = (L - .0894841775 * a - 1.2914855480 * b) ** 3; return [4.0767416621 * l - 3.3077115913 * m + .2309699292 * s, -1.2684380046 * l + 2.6097574011 * m - .3413193965 * s, -.0041960863 * l - .7034186147 * m + 1.7076147010 * s]; };
const mix = (a, b, t) => { const A = toOk(h2l(a)), B = toOk(h2l(b)); return l2h(fromOk(A.map((x, i) => x + (B[i] - x) * t))); };
const ramp = (st, t) => { t = clamp(t, 0, 1); const n = st.length - 1, i = Math.min(n - 1, Math.floor(t * n)); return mix(st[i], st[i + 1], t * n - i); };
const lum = h => { const [r, g, b] = h2l(h); return .2126 * r + .7152 * g + .0722 * b; };
const inkOn = h => lum(h) > .32 ? '#0b0b0b' : '#ffffff';

// ───────────────────────── paletas (validadas con dataviz/validate_palette.js) ─────────────────────────
// Categórica de referencia en su orden fijo (azul, naranja, aguamarina, amarillo, magenta, verde, violeta, rojo).
// Materiales toman los 8 cupos en ese orden → CVD adyacente ΔE 9,1 (claro) / 8,4 (oscuro y azul marino).
// Fases y capas son subconjuntos validados aparte (ΔE ≥ 13). Alto contraste = Okabe-Ito re-escalonado (ΔE ≥ 11,4 sobre blanco).
const REF_L = { blue: '#2a78d6', orange: '#eb6834', aqua: '#1baf7a', yellow: '#eda100', magenta: '#e87ba4', green: '#008300', violet: '#4a3aa7', red: '#e34948' };
const REF_D = { blue: '#3987e5', orange: '#d95926', aqua: '#199e70', yellow: '#c98500', magenta: '#d55181', green: '#008300', violet: '#9085e9', red: '#e66767' };
const OKI = { blue: '#0072b2', yellow: '#b89c00', sky: '#56b4e9', vermillion: '#d55e00', orange: '#e69f00', green: '#009e73', violet: '#6a3d9a', purple: '#cc79a7' };
const roles = (H, gray) => ({
  mat: { hidro: H.blue, secas: H.orange, tierras: H.aqua, estab: H.yellow, granular: H.magenta, anden: H.green, losa: H.violet, asfalto: H.red, otros: gray },
  fase: { tierras: H.aqua, redes: H.blue, estructura: H.yellow, carpeta: H.violet, espacio: H.green, acabados: gray },
  capa: { estab: H.yellow, subbase: H.blue, base: H.magenta, losa: H.violet, asfalto: H.red },
  grupo: { ya_iniciados: H.blue, por_iniciar: H.orange, no_alcanza: H.aqua },
});
// sky: [cénit, horizonte, suelo lejano]; flow: color de las líneas de flujo; bloom: [intensidad, radio, umbral]
const THEMES = {
  noche: { n: 'Noche', dark: true, sky: ['#05070a', '#1a2230', '#0b0c0d'], ground: '#141516', block: '#1c1d1e', park: '#16231a', road: '#2a2b2c', roadMajor: '#353637', path: '#212223', rail: '#56554f', bldg: '#2a2b2d', bldgEdge: '#45443f', bldgOp: 1, bEdges: false, grid: null, tree: '#2c4a33', foot: '#303133', ghost: '#f4f3ee', edge: '#ffffff', edgeOp: .16, hemi: ['#cfd8e6', '#4a4540'], light: [1.35, 1.55], env: .45, flow: '#6fb0ff', bloom: [.62, .5, .78], ...roles(REF_D, '#77766f'), seq: ['#184f95', '#3987e5', '#b7d3f6'], div: ['#86b6ef', '#3a3a37', '#f07b79'], np: ['#6b3517', '#d95926', '#f6b48c'], swatch: ['#161717', REF_D.blue, REF_D.orange, REF_D.green, REF_D.red] },
  claro: { n: 'Claro', dark: false, sky: ['#bcd0e8', '#f2f1ec', '#e6e5df'], ground: '#f4f4f1', block: '#eaeae5', park: '#dce8d2', road: '#dcdcd6', roadMajor: '#cfcfc8', path: '#e5e5df', rail: '#9c9a93', bldg: '#ecebe6', bldgEdge: '#c3c2b7', bldgOp: 1, bEdges: false, grid: null, tree: '#8fbf86', foot: '#d6d6cf', ghost: '#0b0b0b', edge: '#000000', edgeOp: .13, hemi: ['#ffffff', '#b9b4a8'], light: [1.35, 1.7], env: .55, flow: '#2a78d6', bloom: [.22, .4, 1.25], ...roles(REF_L, '#898781'), seq: ['#b7d3f6', '#3987e5', '#104281'], div: ['#184f95', '#e9e8e3', '#b32b2a'], np: ['#f6c3a5', '#eb6834', '#8c2f0c'], swatch: ['#fcfcfb', REF_L.blue, REF_L.orange, REF_L.green, REF_L.red] },
  azul: { n: 'Plano azul', dark: true, sky: ['#030c18', '#15406a', '#081a2e'], ground: '#0d2540', block: '#112f4e', park: '#10384a', road: '#0a2036', roadMajor: '#091b2e', path: '#102f4e', rail: '#7fa7cf', bldg: '#15395e', bldgEdge: '#8cb8e6', bldgOp: .3, bEdges: true, grid: '#23507c', tree: '#2f6a8f', foot: '#17406a', ghost: '#e2f1ff', edge: '#e2f1ff', edgeOp: .3, hemi: ['#dcecff', '#10233a'], light: [1.4, 1.4], env: .4, flow: '#9fd0ff', bloom: [.7, .55, .72], ...roles(REF_D, '#7f95ad'), seq: ['#1f4f80', '#4f95dd', '#e6f3ff'], div: ['#8cc4ff', '#2a4a6c', '#ff8a80'], np: ['#6a3f25', '#e07a3f', '#ffd2b0'], swatch: ['#0f2740', REF_D.blue, REF_D.orange, REF_D.green, REF_D.red] },
  contraste: { n: 'Alto contraste', dark: false, sky: ['#ffffff', '#ffffff', '#ffffff'], ground: '#ffffff', block: '#f1f1f1', park: '#e2efe2', road: '#d4d4d4', roadMajor: '#bcbcbc', path: '#e4e4e4', rail: '#000000', bldg: '#fafafa', bldgEdge: '#000000', bldgOp: 1, bEdges: true, grid: null, tree: '#9ccf9c', foot: '#e0e0e0', ghost: '#000000', edge: '#000000', edgeOp: .8, hemi: ['#ffffff', '#a0a0a0'], light: [1.5, 1.6], env: .4, flow: '#0072b2', bloom: [0, .2, 2], figHC: true,
    mat: { hidro: OKI.blue, secas: OKI.yellow, tierras: OKI.sky, estab: OKI.vermillion, granular: OKI.orange, anden: OKI.green, losa: OKI.violet, asfalto: OKI.purple, otros: '#6b6b6b' },
    fase: { tierras: OKI.sky, redes: OKI.blue, estructura: OKI.vermillion, carpeta: OKI.violet, espacio: OKI.green, acabados: '#6b6b6b' },
    capa: { estab: OKI.vermillion, subbase: OKI.blue, base: OKI.orange, losa: OKI.violet, asfalto: OKI.purple },
    grupo: { ya_iniciados: OKI.vermillion, por_iniciar: OKI.sky, no_alcanza: OKI.violet },
    seq: ['#bcdcf0', '#0072b2', '#002a4a'], div: ['#0072b2', '#eeeeee', '#d55e00'], np: ['#f5cf8a', '#e69f00', '#7a4a00'], swatch: ['#ffffff', OKI.blue, OKI.vermillion, OKI.green, '#000000'] },
  real: { n: 'Realista', dark: false, sky: ['#9dbfe2', '#ede6d7', '#d6d2c5'], ground: '#d3cfc2', block: '#c9c3b2', park: '#a8be8e', road: '#8a8984', roadMajor: '#77766f', path: '#bab4a5', rail: '#5b544a', bldg: '#eee8dc', bldgEdge: '#b7ae9c', bldgOp: 1, bEdges: false, grid: null, tree: '#6d9a50', foot: '#a3a29b', ghost: '#2b2924', edge: '#000000', edgeOp: .12, hemi: ['#fff7e8', '#8f877a'], light: [1.3, 1.85], env: .5, flow: '#b0582f', bloom: [.2, .4, 1.25], figurative: true,
    mat: { hidro: '#2e7dbf', secas: '#e3a21a', tierras: '#8b5e3c', estab: '#6f6258', granular: '#c2a36b', anden: '#c7704f', losa: '#bdbab0', asfalto: '#3a3a3c', otros: '#f1cf3f' },
    fase: { tierras: '#8b5e3c', redes: '#2e7dbf', estructura: '#c2a36b', carpeta: '#3a3a3c', espacio: '#c7704f', acabados: '#f1cf3f' },
    capa: { estab: '#6f6258', subbase: '#dbc9a1', base: '#b08d57', losa: '#c9c7be', asfalto: '#333335' },
    grupo: { ya_iniciados: REF_L.blue, por_iniciar: REF_L.orange, no_alcanza: REF_L.aqua },
    seq: ['#b7d3f6', '#3987e5', '#104281'], div: ['#184f95', '#efece4', '#b32b2a'], np: ['#f6c3a5', '#eb6834', '#8c2f0c'], swatch: ['#d6d2c5', '#3a3a3c', '#bdbab0', '#c2a36b', '#c7704f'] },
};
const PAL_NOTE = {
  noche: 'Modo nocturno inmersivo. Colores de datos validados para daltonismo (ΔE ≥ 8 entre capas vecinas).',
  claro: 'Fondo claro para imprimir o proyectar. Mismos 8 tonos, escalonados para superficie clara.',
  azul: 'Estilo plano de ingeniería: edificios en alambre y cuadrícula. Paleta validada sobre azul marino.',
  contraste: 'Okabe-Ito re-escalonado sobre blanco con bordes negros (ΔE ≥ 11 entre vecinos).',
  real: 'Colores figurativos de obra (asfalto, concreto, granular, ladrillo). No es apta para distinguir por color con daltonismo: use etiquetas y leyenda.',
};

// ───────────────────────── catálogos ─────────────────────────
const MATK = ['hidro', 'secas', 'tierras', 'estab', 'granular', 'anden', 'losa', 'asfalto', 'otros'];
const MATN = { hidro: 'Redes hidrosanitarias', secas: 'Redes secas (energía, telecom., gas)', tierras: 'Demoliciones y movimiento de tierras', estab: 'Estabilización de subrasante', granular: 'Subbase y base granular', anden: 'Andenes, espacio público y paisajismo', losa: 'Losa de concreto', asfalto: 'Carpeta asfáltica', otros: 'Señalización y otros' };
const MATS = { hidro: 'Hidrosanitarias', secas: 'Redes secas', tierras: 'Tierras', estab: 'Estabilización', granular: 'Granulares', anden: 'Andenes', losa: 'Losa', asfalto: 'Asfalto', otros: 'Otros' };
const CAPK = ['estab', 'subbase', 'base', 'losa', 'asfalto'];
const CAPN = { estab: 'Estabilización de subrasante', subbase: 'Subbase granular', base: 'Base granular', losa: 'Losa de concreto', asfalto: 'Carpeta asfáltica' };
const FASEK = ['tierras', 'redes', 'estructura', 'carpeta', 'espacio', 'acabados'];
const FASEN = { tierras: 'Demoliciones y tierras', redes: 'Redes subterráneas', estructura: 'Estructura de pavimento', carpeta: 'Carpeta (asfalto / losa)', espacio: 'Andenes y espacio público', acabados: 'Señalización y acabados' };
const GRUPON = { ya_iniciados: 'Ya iniciados', por_iniciar: 'Por iniciar', no_alcanza: 'No alcanza (excluidos Alt. 2)' };
const SEVR = { ALTA: 3, MEDIA: 2, BAJA: 1, INFO: 0 };
const SEVI = { ALTA: '▲', MEDIA: '●', BAJA: '■', INFO: 'ℹ' };
const ICON = {
  costos: '<path d="M4 20V11M10 20V4M16 20v-8M21 20H3"/>',
  variacion: '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
  estructural: '<path d="M3 6h18M3 10h18M3 14h18M3 18h18"/>',
  materiales: '<rect x="5" y="3" width="14" height="5" rx="1"/><rect x="5" y="10" width="14" height="4" rx="1"/><rect x="5" y="16" width="14" height="5" rx="1"/>',
  redes: '<path d="M2 8h20M2 15h20"/><circle cx="7" cy="8" r="1.6"/><circle cx="16" cy="15" r="1.6"/><path d="M2 20h20" stroke-dasharray="2 3"/>',
  np: '<circle cx="12" cy="12" r="9"/><path d="M12 7v6M12 16.5v.5"/>',
  alcance: '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
  sim: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
};
const MODES = [
  { k: 'costos', n: 'Costos', q: '¿Cuánto cuesta cada calle?', cmp: true, help: 'Altura = valor de obra del CIV con AIU. Color = costo por m² (más intenso = más caro por m²). En “Ambos” el volumen sólido es V4 y el contorno de vidrio es V0.' },
  { k: 'variacion', n: 'Variación', q: '¿Dónde sube y dónde baja?', cmp: false, help: 'Altura = tamaño del cambio en pesos. Color divergente: rojo = sube, azul = baja, gris = sin cambio (intensidad = % de cambio).' },
  { k: 'estructural', n: 'Estructura', q: '¿Cómo cambia el pavimento?', cmp: true, help: 'Capas de la estructura con su espesor equivalente (m³ del CIV ÷ área), exagerado en vertical. En “Ambos” la franja de alambre es V0 y la sólida V4.' },
  { k: 'materiales', n: 'Materiales', q: '¿Qué materiales explican el aumento?', cmp: true, help: 'Columna apilada por material; altura total = valor del CIV. En “Ambos” la franja de alambre es V0 y la sólida V4, lado a lado.' },
  { k: 'redes', n: 'Redes', q: '¿Qué pasa bajo tierra?', cmp: true, help: 'Vista del subsuelo: un tubo por tipo de red (hidrosanitaria y seca). Grosor ∝ valor. En “Ambos” el tubo de vidrio es V0.' },
  { k: 'np', n: 'No previstos', q: '¿Cuánto es obra no prevista?', cmp: false, help: 'Volumen sólido = valor de los ítems no previstos (NP) del CIV en V4; contorno = total V4. Color = % del CIV que es NP.' },
  { k: 'alcance', n: 'Alcance', q: '¿Qué calles están en juego?', cmp: true, help: 'Color = grupo del CIV en la Hoja1 del contratista: ya iniciados, por iniciar o “no alcanza” (excluidos en la alternativa 2). Altura = valor.' },
  { k: 'sim', n: 'Simulación', q: '¿Cabe la obra en 8 meses?', cmp: false, help: 'Obra que se construye mes a mes: cada CIV levanta sus fases (tierras → redes → estructura → carpeta → andenes → acabados) al ritmo elegido.' },
];

// ───────────────────────── estado ─────────────────────────
const S = { mode: 'costos', cmp: 'ambos', theme: 'noche', exag: 1, labels: true, bldg: true, trees: true, roads: true, hall: true, motion: true, shadow: !coarse(), sel: null, hover: null, view: 'general', rankAll: false, dtab: 'res', q: null, qManual: false };
const SIM = { on: false, playing: false, t: 0, speed: .5, scope: 'oficial', pace: 'pedido', ritmo: 0, fr: 4, cap: 500e6, mov: .5, ord: 'valor', chart: 's', res: null };
const T = () => THEMES[S.theme];

// ───────────────────────── acceso (misma sesión que la aplicación principal) ─────────────────────────
let authed = false;
try { authed = sessionStorage.getItem('auth') === 'true'; } catch (_) { authed = false; }
if (!authed) { $('#loading').hidden = true; $('#gate').hidden = false; }
else boot().catch(e => fail('Error inesperado: ' + (e && e.message || e)));
function fail(msg) { $('#loading').hidden = true; $('#err').hidden = false; $('#errMsg').textContent = msg; console.error(msg); }

// ───────────────────────── arranque ─────────────────────────
let D, CTX, byId, CX, CY, renderer, scene, camera, controls, lblR, hemi, sun, sky, CG, CM = {}, civG = null, pick = [], dirty = true, anims = [];
let bldgMesh, bldgEdges, grid, subGrid, roadLbls = [], edgeMatShared = null, trees = null, composer = null, gtao = null, outline = null, bloom = null, pmrem = null, envRT = null;
const uTime = { value: 0 };
const ray = new THREE.Raycaster(), ptr = new THREE.Vector2();
const setLoad = t => { const e = $('#loadTxt'); if (e) e.textContent = t; };

async function boot() {
  try {
    const get = u => fetch(u, { cache: 'no-cache' }).then(r => { if (!r.ok) throw new Error(u + ' → HTTP ' + r.status); return r.json(); });
    [D, CTX] = await Promise.all([get('datos/plano3d_datos.json'), get('datos/contexto.json')]);
  } catch (e) { fail('No se pudieron leer los datos del plano (' + e.message + '). Si abrió el archivo desde el disco, sírvalo con un servidor web (GitHub Pages o «python -m http.server»).'); return; }
  try { const t = document.createElement('canvas'); if (!t.getContext('webgl2')) throw new Error('sin WebGL2'); }
  catch (_) { fail('Este navegador no tiene WebGL 2 activo, necesario para el plano 3D. Pruebe con Chrome, Edge, Firefox o Safari recientes.'); return; }
  const shared = readHash();
  if (!location.hash.includes('p=')) S.theme = matchMedia('(prefers-color-scheme: light)').matches ? 'claro' : 'noche';
  if (!S.q) S.q = (coarse() || (navigator.deviceMemory && navigator.deviceMemory <= 4)) ? 'media' : 'alta';
  if (navigator.deviceMemory && navigator.deviceMemory <= 2 && !S.qManual) S.q = 'baja';
  SIM.ritmo = SIM.pace === 'historico' ? D.meta.ritmo.historico_mensual_aprox : D.meta.ritmo.obras_mensual;
  setLoad('Proyectando los 27 ejes de obra…'); await frame();
  prepData();
  initScene();
  setLoad('Levantando 413 edificios, manzanas y arbolado…'); await frame();
  buildContext(); buildTrees();
  initUI();
  simRun();
  applyTheme(false);
  setQuality(S.q, false);
  const target = S.sel && byId[S.sel] ? [byId[S.sel]] : D.civs;
  if (shared || S.sel) fitTo(target, S.view === 'planta' ? .001 : 55, S.view === 'planta' ? 0 : -16, 0);
  else { // entrada cinematográfica: de una vista aérea alta al encuadre general
    fitTo(D.civs, 18, -70, 0); camera.position.multiplyScalar(1).add(new THREE.Vector3(0, 600, 0)); controls.update();
    setTimeout(() => fitTo(D.civs, 55, -16, 2600), 250);
  }
  if (S.sel) selectCiv(S.sel, false);
  requestAnimationFrame(loop);
  setTimeout(() => { $('#loading').hidden = true; if (!shared && lsGet('p3d_welcome_off') !== '1') $('#welcome').hidden = false; }, 200);
}
const frame = () => new Promise(r => requestAnimationFrame(() => r()));

// ───────────────────────── datos → coordenadas del mundo ─────────────────────────
const cumLen = P => { const c = [0]; for (let i = 1; i < P.length; i++) c.push(c[i - 1] + Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1])); return c; };
function at(P, cum, s) { s = clamp(s, 0, cum[cum.length - 1]); let i = 1; while (i < cum.length - 1 && cum[i] < s) i++; const t = (s - cum[i - 1]) / ((cum[i] - cum[i - 1]) || 1); return [P[i - 1][0] + (P[i][0] - P[i - 1][0]) * t, P[i - 1][1] + (P[i][1] - P[i - 1][1]) * t]; }
function subLine(P, a, b) { const cum = cumLen(P); const out = [at(P, cum, a)]; for (let i = 1; i < P.length - 1; i++) if (cum[i] > a && cum[i] < b) out.push(P[i]); out.push(at(P, cum, b)); return out; }
function prepData() {
  const xs = [], ys = [];
  D.civs.forEach(c => c.geom.forEach(([x, y]) => { xs.push(x); ys.push(y); }));
  CX = (Math.min(...xs) + Math.max(...xs)) / 2; CY = (Math.min(...ys) + Math.max(...ys)) / 2;
  byId = {};
  for (const c of D.civs) {
    byId[c.id] = c;
    c.P = c.geom.map(([x, y]) => [x - CX, -(y - CY)]);
    const L = cumLen(c.P).at(-1), inset = Math.min(9, L * .12);
    c.tp = subLine(c.P, inset, L - inset); c.tcum = cumLen(c.tp); c.tL = c.tcum.at(-1);
    c.w = clamp(c.ancho || 14, 9, 24);
    c.mid = at(c.tp, c.tcum, c.tL / 2);
    c.dpct = c.tot0 ? c.delta / c.tot0 * 100 : 0;
    c.m2 = [c.tot0 / c.area, c.tot4 / c.area];
    c.pnp = c.tot4 ? c.np4 / c.tot4 * 100 : 0;
    c.est = [CAPK.reduce((a, k) => a + (c.estructura[k]?.cm0 || 0), 0), CAPK.reduce((a, k) => a + (c.estructura[k]?.cm4 || 0), 0)];
    c.red = [(c.v0.hidro || 0) + (c.v0.secas || 0), (c.v4.hidro || 0) + (c.v4.secas || 0)];
    c.sev = (c.hallazgos || []).reduce((a, h) => SEVR[h.s] > SEVR[a] ? h.s : a, (c.hallazgos || []).length ? 'INFO' : null);
    c.mats = []; c.gm = []; c.lk = '';
  }
  const t = { t0: 0, t4: 0, np: 0, a: 0 }; D.civs.forEach(c => { t.t0 += c.tot0; t.t4 += c.tot4; t.np += c.np4; t.a += c.area; }); D.tot = t;
  D.mat = {}; for (const k of MATK) D.mat[k] = D.civs.reduce((a, c) => [a[0] + (c.v0[k] || 0), a[1] + (c.v4[k] || 0)], [0, 0]);
}

// ───────────────────────── escena y canal de render ─────────────────────────
function initScene() {
  const canvas = $('#gl');
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.NeutralToneMapping; renderer.toneMappingExposure = 1;
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(38, 1, 5, 12000);
  controls = new MapControls(camera, canvas);
  Object.assign(controls, { enableDamping: true, dampingFactor: .085, screenSpacePanning: false, minDistance: 60, maxDistance: 4600, zoomToCursor: true, maxPolarAngle: THREE.MathUtils.degToRad(84), autoRotateSpeed: .35 });
  controls.addEventListener('change', () => { dirty = true; });
  controls.addEventListener('start', () => { if (tour.on) tourPause(true); });
  pmrem = new THREE.PMREMGenerator(renderer);
  hemi = new THREE.HemisphereLight(0xffffff, 0x444444, 1.3);
  sun = new THREE.DirectionalLight(0xffffff, 1.6);
  sun.position.set(-620, 1150, 520); sun.target.position.set(0, 0, 0);
  sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -1150, right: 1150, top: 1150, bottom: -1150, near: 200, far: 3200 });
  sun.shadow.bias = -0.0005; sun.shadow.normalBias = .8;
  scene.add(hemi, sun, sun.target);
  // cúpula de cielo con horizonte (la niebla usa el mismo color del horizonte → transición continua)
  sky = new THREE.Mesh(new THREE.SphereGeometry(9000, 48, 24), new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false, fog: false,
    uniforms: { cTop: { value: new THREE.Color() }, cHor: { value: new THREE.Color() }, cBot: { value: new THREE.Color() } },
    vertexShader: 'varying vec3 vW; void main(){ vec4 w = modelMatrix * vec4(position, 1.0); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }',
    fragmentShader: `uniform vec3 cTop; uniform vec3 cHor; uniform vec3 cBot; varying vec3 vW;
      void main(){ float h = normalize(vW - cameraPosition).y; vec3 c = h > 0.0 ? mix(cHor, cTop, pow(clamp(h * 1.6, 0.0, 1.0), 0.55)) : mix(cHor, cBot, pow(clamp(-h * 4.0, 0.0, 1.0), 0.6));
        gl_FragColor = vec4(c, 1.0);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }`,
  }));
  sky.userData.noAO = true; sky.renderOrder = -10; sky.frustumCulled = false; scene.add(sky);
  lblR = new CSS2DRenderer({ element: $('#lbls') });
  const ro = new ResizeObserver(resize); ro.observe($('#stage')); resize();
}
function resize() {
  const st = $('#stage'), w = st.clientWidth, h = st.clientHeight;
  renderer.setSize(w, h, false); lblR.setSize(w, h);
  if (composer) composer.setSize(w, h);
  if (outline) outline.resolution.set(w, h);
  camera.aspect = w / h; camera.updateProjectionMatrix(); dirty = true;
}
// Calidad: alta = oclusión ambiental (GTAO) + contorno + brillo; media = contorno + brillo; baja = render directo sin sombras
function setQuality(q, user = true) {
  S.q = q; if (user) S.qManual = true;
  $$('#qual button').forEach(b => b.setAttribute('aria-pressed', b.dataset.q === q));
  $('#qualNote').textContent = { alta: 'Oclusión ambiental, brillo, contorno de selección, sombras suaves y antialias ×4.', media: 'Brillo, contorno de selección y sombras. Recomendada para portátiles y tabletas.', baja: 'Render directo, sin sombras ni efectos: para equipos lentos.' }[q];
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, q === 'alta' ? 2 : q === 'media' ? 1.5 : 1));
  if (composer) { composer.renderTarget1.dispose(); composer.renderTarget2.dispose(); composer = null; }
  if (gtao) { gtao.dispose(); gtao = null; } if (bloom) { bloom.dispose(); bloom = null; } if (outline) { outline.dispose(); outline = null; }
  const st = $('#stage'), w = st.clientWidth, h = st.clientHeight;
  renderer.setSize(w, h, false);
  if (q !== 'baja') {
    const rt = new THREE.WebGLRenderTarget(w, h, { type: THREE.HalfFloatType, samples: q === 'alta' ? 4 : 2 });
    composer = new EffectComposer(renderer, rt);
    composer.setPixelRatio(renderer.getPixelRatio()); composer.setSize(w, h);
    composer.addPass(new RenderPass(scene, camera));
    if (q === 'alta') {
      gtao = new GTAOPass(scene, camera, w, h);
      gtao.output = GTAOPass.OUTPUT.Default; gtao.blendIntensity = .9;
      gtao.updateGtaoMaterial({ radius: 11, distanceExponent: 1.4, thickness: 9, scale: 1.15, samples: 16 });
      gtao.updatePdMaterial({ lumaPhi: 10, depthPhi: 2, normalPhi: 3, radius: 5, rings: 2, samples: 16 });
      const ov = gtao.overrideVisibility.bind(gtao); // excluir del búfer G lo translúcido, el cielo y lo que se construye por sombreador
      gtao.overrideVisibility = function () { ov(); this.scene.traverse(o => { if (o.userData.noAO) o.visible = false; }); };
      composer.addPass(gtao);
    }
    outline = new OutlinePass(new THREE.Vector2(w, h), scene, camera);
    Object.assign(outline, { edgeStrength: 4.2, edgeGlow: .55, edgeThickness: 1.6, pulsePeriod: 0, enabled: false });
    composer.addPass(outline);
    bloom = new UnrealBloomPass(new THREE.Vector2(w, h), .5, .5, .8);
    composer.addPass(bloom);
    composer.addPass(new OutputPass());
    themePost();
  }
  sun.castShadow = S.shadow && q !== 'baja';
  perf.samples = []; dirty = true;
}
function themePost() {
  const th = T();
  if (bloom) { [bloom.strength, bloom.radius, bloom.threshold] = th.bloom; bloom.enabled = th.bloom[0] > 0; }
  if (outline) { outline.visibleEdgeColor.set(th.dark ? '#9ccaff' : th.flow); outline.hiddenEdgeColor.set(th.dark ? '#2a4a70' : '#9bb8d8'); }
  if (gtao) gtao.blendIntensity = th.dark ? .95 : .8;
}

// ───────────────────────── geometría ─────────────────────────
function normals(P) { // normales laterales con inglete en cada vértice
  const n = P.length, seg = [], N = [];
  for (let i = 0; i < n - 1; i++) { const dx = P[i + 1][0] - P[i][0], dz = P[i + 1][1] - P[i][1], l = Math.hypot(dx, dz) || 1; seg.push([-dz / l, dx / l]); }
  for (let i = 0; i < n; i++) { const a = seg[Math.max(0, i - 1)], b = seg[Math.min(n - 2, i)]; let mx = a[0] + b[0], mz = a[1] + b[1]; const ml = Math.hypot(mx, mz) || 1; mx /= ml; mz /= ml; const s = 1 / Math.max(mx * b[0] + mz * b[1], .45); N.push([mx * s, mz * s]); }
  return N;
}
const offLine = (P, d) => { const N = normals(P); return P.map((p, i) => [p[0] + N[i][0] * d, p[1] + N[i][1] * d]); };
// Prisma a lo largo de una polilínea entre dos desplazamientos laterales (oA < oB) y dos alturas.
// aT = distancia recorrida normalizada (0→1): el sombreador "construye" el tramo en la simulación y anima las líneas de flujo.
function ribbon(P, oA, oB, y0, y1, bottom = false) {
  const N = normals(P), cum = cumLen(P), L = cum.at(-1) || 1, n = P.length;
  const A = P.map((p, i) => [p[0] + N[i][0] * oA, p[1] + N[i][1] * oA]), B = P.map((p, i) => [p[0] + N[i][0] * oB, p[1] + N[i][1] * oB]);
  const pos = [], tt = [];
  const q = (a, b, c, d, ta, tb, tc, td) => { pos.push(...a, ...b, ...c, ...a, ...c, ...d); tt.push(ta, tb, tc, ta, tc, td); };
  const V = (p, y) => [p[0], y, p[1]];
  const solid = y1 - y0 > .01;
  for (let i = 0; i < n - 1; i++) {
    const t0 = cum[i] / L, t1 = cum[i + 1] / L;
    q(V(A[i], y1), V(B[i], y1), V(B[i + 1], y1), V(A[i + 1], y1), t0, t0, t1, t1);
    if (bottom) q(V(A[i], y0), V(A[i + 1], y0), V(B[i + 1], y0), V(B[i], y0), t0, t1, t1, t0);
    if (solid) { q(V(A[i], y0), V(A[i], y1), V(A[i + 1], y1), V(A[i + 1], y0), t0, t0, t1, t1); q(V(B[i], y0), V(B[i + 1], y0), V(B[i + 1], y1), V(B[i], y1), t0, t1, t1, t0); }
  }
  if (solid) { const i = n - 1; q(V(A[0], y0), V(B[0], y0), V(B[0], y1), V(A[0], y1), 0, 0, 0, 0); q(V(A[i], y0), V(A[i], y1), V(B[i], y1), V(B[i], y0), 1, 1, 1, 1); }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute('aT', new THREE.Float32BufferAttribute(tt, 1));
  g.computeVertexNormals();
  return g;
}
function tubeGeo(P, y, r) {
  const path = new THREE.CurvePath(); const V = P.map(([x, z]) => new THREE.Vector3(x, y, z));
  for (let i = 0; i < V.length - 1; i++) path.add(new THREE.LineCurve3(V[i], V[i + 1]));
  const g = new THREE.TubeGeometry(path, Math.max(6, (V.length - 1) * 8), r, 20, false);
  const uv = g.getAttribute('uv'); const a = new Float32Array(uv.count); for (let i = 0; i < uv.count; i++) a[i] = uv.getX(i);
  g.setAttribute('aT', new THREE.BufferAttribute(a, 1));
  return g;
}
function progMat(color, o = {}) {
  const op = o.opacity ?? 1;
  const m = new THREE.MeshStandardMaterial({ color, roughness: o.rough ?? .42, metalness: .02, envMapIntensity: .7, transparent: op < 1, opacity: op, depthWrite: op >= 1, side: o.double ? THREE.DoubleSide : THREE.FrontSide });
  m.userData.base = new THREE.Color(color);
  if (o.prog) {
    m.userData.u = { uProg: { value: 1 }, uGlow: { value: new THREE.Color(color).lerp(new THREE.Color('#ffffff'), .45) }, uGlowAmt: { value: 0 } };
    m.onBeforeCompile = sh => {
      Object.assign(sh.uniforms, m.userData.u);
      sh.vertexShader = 'attribute float aT;\nvarying float vT;\n' + sh.vertexShader.replace('#include <begin_vertex>', '#include <begin_vertex>\n  vT = aT;');
      sh.fragmentShader = 'uniform float uProg;\nuniform vec3 uGlow;\nuniform float uGlowAmt;\nvarying float vT;\n' + sh.fragmentShader
        .replace('#include <clipping_planes_fragment>', '#include <clipping_planes_fragment>\n  if (vT > uProg + 0.0005) discard;')
        .replace('#include <emissivemap_fragment>', '#include <emissivemap_fragment>\n  totalEmissiveRadiance += uGlow * uGlowAmt * (1.0 - smoothstep(0.0, 0.07, uProg - vT));');
    };
    m.customProgramCacheKey = () => 'p3d-prog';
  }
  return m;
}
// Línea de flujo: cinta luminosa con guiones que avanzan a lo largo de la calle (con brillo en temas oscuros)
function flowMat(color, len, amp = 1) {
  const th = T();
  return new THREE.ShaderMaterial({
    transparent: true, depthWrite: false, blending: th.dark ? THREE.AdditiveBlending : THREE.NormalBlending, polygonOffset: true, polygonOffsetFactor: -4, polygonOffsetUnits: -8,
    uniforms: { uTime, uLen: { value: len }, uCol: { value: new THREE.Color(color) }, uAmp: { value: amp }, uDark: { value: th.dark ? 1 : 0 } },
    vertexShader: 'attribute float aT; varying float vT; void main(){ vT = aT; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: `uniform float uTime; uniform float uLen; uniform vec3 uCol; uniform float uAmp; uniform float uDark; varying float vT;
      void main(){ float s = vT * uLen; float d = fract((s - uTime * 14.0) / 22.0); float dash = smoothstep(0.0, 0.12, d) * (1.0 - smoothstep(0.42, 0.62, d));
        float k = mix(0.35, 1.0, dash) * uAmp; vec3 c = uCol * (uDark > 0.5 ? mix(0.8, 3.2, dash) * uAmp : 1.0);
        gl_FragColor = vec4(c, uDark > 0.5 ? k : mix(0.35, 0.95, dash));
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }`,
  });
}
function disposeTree(o) { o.traverse(x => { if (x.geometry) x.geometry.dispose(); if (x.material) (Array.isArray(x.material) ? x.material : [x.material]).forEach(m => m.dispose()); }); }

// ───────────────────────── contexto urbano (OpenStreetMap) ─────────────────────────
function buildContext() {
  CG = new THREE.Group(); scene.add(CG);
  const th = T();
  const flat = (color, off) => new THREE.MeshLambertMaterial({ color, polygonOffset: true, polygonOffsetFactor: -off, polygonOffsetUnits: -off * 2 });
  const gg = new THREE.PlaneGeometry(16000, 16000); gg.rotateX(-Math.PI / 2);
  CM.ground = new THREE.MeshLambertMaterial({ color: th.ground });
  const ground = new THREE.Mesh(gg, CM.ground); ground.position.y = -.4; ground.receiveShadow = true; ground.renderOrder = -2; CG.add(ground);
  const shapeGeo = (pts, y) => {
    const p = pts.slice(); if (p.length > 2 && p[0][0] === p.at(-1)[0] && p[0][1] === p.at(-1)[1]) p.pop();
    const g = new THREE.ShapeGeometry(new THREE.Shape(p.map(([x, yy]) => new THREE.Vector2(x - CX, yy - CY))));
    g.rotateX(-Math.PI / 2); g.translate(0, y, 0); g.deleteAttribute('uv'); return g;
  };
  const merged = (list, mat, name) => { const gs = list.filter(g => g && g.getAttribute('position').count); if (!gs.length) return null; const m = new THREE.Mesh(mergeGeometries(gs, false), mat); m.receiveShadow = true; m.name = name; gs.forEach(g => g.dispose()); CG.add(m); return m; };
  CM.block = flat(th.block, 1); merged(CTX.blocks.map(b => shapeGeo(b.p, 0)), CM.block, 'blocks');
  CM.park = flat(th.park, 2); merged(CTX.parks.map(b => shapeGeo(b.p, .05)), CM.park, 'parks');
  const W = p => p.map(([x, y]) => [x - CX, -(y - CY)]);
  const major = /^(trunk|primary|secondary)/, path = /^(footway|cycleway|steps|path|pedestrian)/;
  const rd = { major: [], minor: [], path: [] }, marks = [];
  for (const r of CTX.roads) {
    if (r.p.length < 2) continue; const k = major.test(r.c) ? 'major' : path.test(r.c) ? 'path' : 'minor'; const w = r.w || 6; const P = W(r.p);
    rd[k].push(ribbon(P, -w / 2, w / 2, .1, .1));
    if (k === 'major' && w >= 12) marks.push(P);
  }
  CM.path = flat(th.path, 3); merged(rd.path, CM.path, 'paths');
  CM.road = flat(th.road, 4); merged(rd.minor, CM.road, 'roads');
  CM.roadMajor = flat(th.roadMajor, 5); merged(rd.major, CM.roadMajor, 'major');
  CM.rail = flat(th.rail, 6); merged(CTX.rails.filter(r => r.p.length > 1).map(r => ribbon(W(r.p), -1.2, 1.2, .15, .15)), CM.rail, 'rails');
  // demarcación: línea central discontinua en avenidas (realismo sutil)
  const mk = []; for (const P of marks) { const cum = cumLen(P), L = cum.at(-1); for (let s = 4; s < L - 6; s += 14) mk.push(ribbon(subLine(P, s, Math.min(L, s + 6)), -.18, .18, .16, .16)); }
  CM.mark = flat('#ffffff', 7); CM.mark.transparent = true; CM.mark.opacity = .22; merged(mk, CM.mark, 'marks');
  // edificios extruidos (altura OSM: niveles × 3,2 m o altura típica por uso)
  const bg = [];
  for (const b of CTX.buildings) {
    const p = b.p.slice(); if (p.length > 2 && p[0][0] === p.at(-1)[0] && p[0][1] === p.at(-1)[1]) p.pop(); if (p.length < 3) continue;
    const g = new THREE.ExtrudeGeometry(new THREE.Shape(p.map(([x, y]) => new THREE.Vector2(x - CX, y - CY))), { depth: b.h || 7, bevelEnabled: false });
    g.rotateX(-Math.PI / 2); g.deleteAttribute('uv'); bg.push(g);
  }
  CM.bldg = new THREE.MeshStandardMaterial({ color: th.bldg, roughness: .88, metalness: 0, envMapIntensity: .35 });
  const bgeo = mergeGeometries(bg, false); bg.forEach(g => g.dispose());
  bldgMesh = new THREE.Mesh(bgeo, CM.bldg); bldgMesh.castShadow = true; bldgMesh.receiveShadow = true; CG.add(bldgMesh);
  CM.bldgEdge = new THREE.LineBasicMaterial({ color: th.bldgEdge, transparent: true, opacity: .8 });
  bldgEdges = new THREE.LineSegments(new THREE.EdgesGeometry(bgeo, 30), CM.bldgEdge); CG.add(bldgEdges);
  grid = new THREE.GridHelper(3600, 72, 0x23507c, 0x23507c); grid.position.y = .02; grid.material.transparent = true; grid.material.opacity = .55; CG.add(grid);
  subGrid = new THREE.GridHelper(2400, 96, 0x888888, 0x888888); subGrid.position.y = -24; subGrid.material.transparent = true; subGrid.material.opacity = .25; subGrid.visible = false; scene.add(subGrid);
  // nombres de vías principales (etiquetas de contexto, prioridad baja)
  const byName = {};
  for (const r of CTX.roads) if (r.n && r.p.length > 1) (byName[r.n] ||= []).push(W(r.p));
  const short = n => n.replace(/^Avenida /, 'Av. ').replace('Carrera', 'Cra.').replace('Diagonal', 'Dg.').replace('Transversal', 'Tv.');
  const main = /Avenida|Calle 1[3-9]|Calle 2[0-4]|Carrera 6[0-9]/;
  for (const [n, arr] of Object.entries(byName)) {
    const lens = arr.map(p => cumLen(p).at(-1)); const tot = lens.reduce((a, b) => a + b, 0);
    if ((tot < 240 && !main.test(n)) || n === 'TransMilenio') continue;
    const i = lens.indexOf(Math.max(...lens)); const P = arr[i]; const cum = cumLen(P); const m = at(P, cum, cum.at(-1) / 2);
    const el = document.createElement('div'); el.className = 'rl'; el.textContent = short(n);
    const o = new CSS2DObject(el); o.position.set(m[0], 2, m[1]); o.center.set(.5, .5); scene.add(o);
    roadLbls.push({ o, el, pri: tot, w: 0, h: 0 });
  }
}
// Arbolado: puntos aleatorios (semilla fija) dentro de parques y zonas verdes, instanciados en dos mallas (tronco y copa)
function buildTrees() {
  const R = rng(1752), pts = [];
  const inPoly = (x, y, p) => { let c = false; for (let i = 0, j = p.length - 1; i < p.length; j = i++) { if (((p[i][1] > y) !== (p[j][1] > y)) && (x < (p[j][0] - p[i][0]) * (y - p[i][1]) / (p[j][1] - p[i][1]) + p[i][0])) c = !c; } return c; };
  const area = p => Math.abs(p.reduce((a, q, i) => { const r = p[(i + 1) % p.length]; return a + q[0] * r[1] - r[0] * q[1]; }, 0)) / 2;
  for (const pk of CTX.parks) {
    if (pk.t === 'pitch') continue;
    const p = pk.p, A = area(p); const cx = p.reduce((a, q) => a + q[0], 0) / p.length - CX, cy = p.reduce((a, q) => a + q[1], 0) / p.length - CY;
    if (Math.hypot(cx, cy) > 1300) continue;
    const n = Math.min(46, Math.floor(A / 380)); if (!n) continue;
    const xs = p.map(q => q[0]), ys = p.map(q => q[1]); const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
    let k = 0, tries = 0; while (k < n && tries++ < n * 8) { const x = x0 + R() * (x1 - x0), y = y0 + R() * (y1 - y0); if (inPoly(x, y, p)) { pts.push([x - CX, -(y - CY), .75 + R() * .6, R() * 6.28, R()]); k++; } }
  }
  pts.splice(1800);
  const trunkG = new THREE.CylinderGeometry(.26, .38, 4.6, 6).translate(0, 2.3, 0);
  const crownG = new THREE.IcosahedronGeometry(3.3, 0).scale(1, 1.15, 1).translate(0, 7.1, 0);
  const trunk = new THREE.InstancedMesh(trunkG, new THREE.MeshStandardMaterial({ color: '#5b4636', roughness: .95 }), pts.length);
  const crown = new THREE.InstancedMesh(crownG, new THREE.MeshStandardMaterial({ color: '#ffffff', roughness: .9, flatShading: true, envMapIntensity: .25 }), pts.length);
  const m = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler(), s = new THREE.Vector3(), v = new THREE.Vector3(), col = new THREE.Color();
  pts.forEach(([x, z, sc, rot], i) => { q.setFromEuler(e.set(0, rot, 0)); m.compose(v.set(x, 0, z), q, s.set(sc, sc, sc)); trunk.setMatrixAt(i, m); crown.setMatrixAt(i, m); crown.setColorAt(i, col.setScalar(1)); });
  trunk.castShadow = crown.castShadow = true; trunk.receiveShadow = crown.receiveShadow = true;
  trees = new THREE.Group(); trees.add(trunk, crown); trees.userData.pts = pts; trees.userData.crown = crown; trees.userData.trunk = trunk; CG.add(trees);
}
function themeTrees() {
  if (!trees) return; const th = T(), crown = trees.userData.crown, col = new THREE.Color(), base = new THREE.Color(th.tree);
  trees.userData.pts.forEach((p, i) => { col.copy(base).offsetHSL((p[4] - .5) * .05, (p[4] - .5) * .12, (p[4] - .5) * .1); crown.setColorAt(i, col); });
  crown.instanceColor.needsUpdate = true;
  crown.material.transparent = S.theme === 'azul'; crown.material.opacity = S.theme === 'azul' ? .55 : 1; crown.material.needsUpdate = true;
  trees.userData.trunk.material.color.set(th.dark ? '#3a2f26' : '#6b5442');
}
// Iluminación ambiental: mapa de entorno equirrectangular diminuto (degradado del cielo del tema + sol) → PMREM de 16 px
function makeEnv() {
  const th = T(), c = document.createElement('canvas'); c.width = 128; c.height = 64; const g = c.getContext('2d');
  const gr = g.createLinearGradient(0, 0, 0, 64);
  gr.addColorStop(0, mix(th.sky[0], '#ffffff', th.dark ? .25 : .1)); gr.addColorStop(.49, mix(th.sky[1], '#ffffff', th.dark ? .45 : .15));
  gr.addColorStop(.51, mix(th.ground, '#808080', .35)); gr.addColorStop(1, mix(th.ground, '#000000', .3));
  g.fillStyle = gr; g.fillRect(0, 0, 128, 64);
  const rg = g.createRadialGradient(36, 16, 0, 36, 16, 16); rg.addColorStop(0, 'rgba(255,248,232,1)'); rg.addColorStop(1, 'rgba(255,248,232,0)'); g.fillStyle = rg; g.fillRect(0, 0, 128, 64);
  const tex = new THREE.CanvasTexture(c); tex.mapping = THREE.EquirectangularReflectionMapping; tex.colorSpace = THREE.SRGBColorSpace;
  const rt = pmrem.fromEquirectangular(tex); tex.dispose(); if (envRT) envRT.dispose(); envRT = rt; scene.environment = rt.texture;
}
function themeContext() {
  const th = T();
  for (const k of ['ground', 'block', 'park', 'road', 'roadMajor', 'path', 'rail']) CM[k].color.set(th[k]);
  CM.mark.opacity = th.dark ? .16 : .5; CM.mark.color.set(th.dark ? '#ffffff' : '#ffffff');
  CM.bldg.color.set(th.bldg); CM.bldg.opacity = th.bldgOp; CM.bldg.transparent = th.bldgOp < 1; CM.bldg.depthWrite = th.bldgOp >= 1; CM.bldg.needsUpdate = true;
  CM.bldgEdge.color.set(th.bldgEdge);
  grid.visible = !!th.grid; if (th.grid) grid.material.color.set(th.grid);
  subGrid.material.color.set(th.dark ? '#6d8fb3' : '#8a8a8a');
  sky.material.uniforms.cTop.value.set(th.sky[0]); sky.material.uniforms.cHor.value.set(th.sky[1]); sky.material.uniforms.cBot.value.set(th.sky[2]);
  scene.fog = new THREE.Fog(th.sky[1], 1700, 4600);
  hemi.color.set(th.hemi[0]); hemi.groundColor.set(th.hemi[1]); [hemi.intensity, sun.intensity] = th.light;
  makeEnv(); scene.environmentIntensity = th.env;
  document.querySelector('meta[name="theme-color"]').content = th.sky[1];
  themeTrees(); themePost(); applyVisibility();
}
function applyVisibility() {
  const under = !SIM.on && S.mode === 'redes', th = T();
  bldgMesh.visible = S.bldg && !under; bldgEdges.visible = S.bldg && !under && th.bEdges;
  if (trees) trees.visible = S.trees && !under;
  for (const k of ['ground', 'block', 'park', 'road', 'roadMajor', 'path', 'rail']) { const m = CM[k]; const want = under ? (th.dark ? .14 : .2) : 1; if (m.opacity !== want) { m.opacity = want; m.transparent = want < 1; m.depthWrite = want >= 1; m.needsUpdate = true; } }
  subGrid.visible = under;
  roadLbls.forEach(r => { r.o.visible = S.roads; });
  sun.castShadow = S.shadow && S.q !== 'baja';
  dirty = true;
}

// ───────────────────────── modos: escalas, colores, métricas ─────────────────────────
const Y0 = .6, GAP = .35;
let K = {};
function computeScales() {
  const c = D.civs, H = 130 * S.exag;
  const m2 = c.flatMap(x => x.m2);
  K = {
    kv: H / Math.max(...c.map(x => Math.max(x.tot0, x.tot4))),
    kd: H / Math.max(...c.map(x => Math.abs(x.delta))),
    kcm: .62 * S.exag,
    m2min: Math.min(...m2), m2max: Math.max(...m2),
    dmax: Math.max(...c.map(x => Math.abs(x.dpct))),
    pmax: Math.max(...c.map(x => x.pnp)),
    vred: Math.max(...c.flatMap(x => [x.v0.hidro || 0, x.v4.hidro || 0, x.v0.secas || 0, x.v4.secas || 0])),
  };
}
const seqC = v => ramp(T().seq, (v - K.m2min) / ((K.m2max - K.m2min) || 1));
const divC = p => ramp(T().div, .5 + .5 * clamp(p / (K.dmax || 1), -1, 1));
const npC = p => ramp(T().np, p / (K.pmax || 1));
function civColor(c) { // color de identidad del CIV en el modo actual (barra de la etiqueta, ranking, minimapa)
  if (SIM.on) { const j = SIM.res?.byId[c.id]; if (!j) return T().foot; const ph = curPhase(j, SIM.t); return ph ? T().fase[ph.k] : (SIM.t >= j.e ? T().fase.espacio : T().foot); }
  switch (S.mode) {
    case 'costos': return seqC(c.m2[S.cmp === 'v0' ? 0 : 1]);
    case 'variacion': return divC(c.dpct);
    case 'np': return npC(c.pnp);
    case 'alcance': return T().grupo[c.grupo] || T().foot;
    case 'redes': return T().mat.hidro;
    case 'estructural': return T().capa.losa;
    default: { const v = S.cmp === 'v0' ? c.v0 : c.v4; let best = 'otros', bv = -1; for (const k of MATK) if ((v[k] || 0) > bv) { bv = v[k] || 0; best = k; } return T().mat[best]; }
  }
}
function metric(c) {
  const v4 = S.cmp !== 'v0';
  if (SIM.on) { const j = SIM.res?.byId[c.id]; return j ? -j.s : -1e9; }
  switch (S.mode) {
    case 'costos': case 'materiales': case 'alcance': return v4 ? c.tot4 : c.tot0;
    case 'variacion': return c.delta;
    case 'estructural': return v4 ? c.est[1] : c.est[0];
    case 'redes': return v4 ? c.red[1] : c.red[0];
    case 'np': return c.np4;
  }
  return 0;
}

// ───────────────────────── construcción de los 27 CIV ─────────────────────────
function edgeMat() { const th = T(); return edgeMatShared ||= new THREE.LineBasicMaterial({ color: th.edge, transparent: true, opacity: th.edgeOp }); }
function addSolid(c, g, geo, color, o = {}) {
  const m = progMat(color, o); const mesh = new THREE.Mesh(geo, m);
  mesh.castShadow = (o.opacity ?? 1) >= 1 && !o.noShadow; mesh.receiveShadow = true; mesh.userData.id = c.id;
  if (o.prog || (o.opacity ?? 1) < 1) mesh.userData.noAO = true;
  if (!o.foot) (c.solids ||= []).push(mesh);
  g.add(mesh); c.mats.push(m); pick.push(mesh);
  if (o.edges !== false && T().edgeOp > 0) { const e = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 25), edgeMat()); e.raycast = () => {}; g.add(e); }
  return mesh;
}
function addWire(c, g, geo, color) {
  const f = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color, transparent: true, opacity: T().dark ? .2 : .24, depthWrite: false }));
  f.userData.id = c.id; f.userData.noAO = true; g.add(f); pick.push(f); c.gm.push(f.material);
  const e = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 25), new THREE.LineBasicMaterial({ color, transparent: true, opacity: .95 }));
  e.raycast = () => {}; g.add(e); c.gm.push(e.material);
}
function addGhost(c, g, geo) {
  const th = T();
  const f = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: th.ghost, transparent: true, opacity: th.dark ? .07 : .05, depthWrite: false, side: THREE.DoubleSide }));
  f.userData.id = c.id; f.userData.noAO = true; g.add(f); pick.push(f); c.gm.push(f.material);
  const e = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 25), new THREE.LineBasicMaterial({ color: th.ghost, transparent: true, opacity: th.dark ? .72 : .66 }));
  e.raycast = () => {}; g.add(e); c.gm.push(e.material);
}
const lanes = (c, both) => { const w = c.w / 2 - .7; return both ? [[-w, -.7, 0], [.7, w, 1]] : [[-w, w, 1]]; };
const BUILD = {
  costos(c, g) {
    const h0 = c.tot0 * K.kv, h4 = c.tot4 * K.kv, w = c.w / 2;
    if (S.cmp === 'v0') addSolid(c, g, ribbon(c.tp, -w + .8, w - .8, Y0, Y0 + h0), seqC(c.m2[0]));
    else addSolid(c, g, ribbon(c.tp, -w + .8, w - .8, Y0, Y0 + h4), seqC(c.m2[1]));
    if (S.cmp === 'ambos') addGhost(c, g, ribbon(c.tp, -w + .25, w - .25, Y0, Y0 + h0));
    return Y0 + (S.cmp === 'v0' ? h0 : S.cmp === 'v4' ? h4 : Math.max(h0, h4));
  },
  alcance(c, g) {
    const h0 = c.tot0 * K.kv, h4 = c.tot4 * K.kv, w = c.w / 2, col = T().grupo[c.grupo] || T().foot;
    addSolid(c, g, ribbon(c.tp, -w + .8, w - .8, Y0, Y0 + (S.cmp === 'v0' ? h0 : h4)), col);
    if (S.cmp === 'ambos') addGhost(c, g, ribbon(c.tp, -w + .25, w - .25, Y0, Y0 + h0));
    return Y0 + (S.cmp === 'v0' ? h0 : S.cmp === 'v4' ? h4 : Math.max(h0, h4));
  },
  variacion(c, g) {
    const h = Math.max(.8, Math.abs(c.delta) * K.kd), w = c.w / 2;
    addSolid(c, g, ribbon(c.tp, -w + .8, w - .8, Y0, Y0 + h), divC(c.dpct));
    return Y0 + h;
  },
  np(c, g) {
    const w = c.w / 2, h = Math.max(.3, c.np4 * K.kv);
    addSolid(c, g, ribbon(c.tp, -w + .8, w - .8, Y0, Y0 + h), npC(c.pnp));
    addGhost(c, g, ribbon(c.tp, -w + .25, w - .25, Y0, Y0 + c.tot4 * K.kv));
    return Y0 + c.tot4 * K.kv;
  },
  materiales(c, g) {
    let top = Y0;
    for (const [a, b, ver] of lanes(c, S.cmp === 'ambos')) {
      const vals = (S.cmp === 'v0' || (S.cmp === 'ambos' && ver === 0)) ? c.v0 : c.v4, ghosty = S.cmp === 'ambos' && ver === 0;
      let y = Y0;
      for (const k of MATK) { const v = vals[k] || 0; const h = v * K.kv; if (h < .06) continue; if (ghosty) addWire(c, g, ribbon(c.tp, a, b, y, y + h), T().mat[k]); else addSolid(c, g, ribbon(c.tp, a, b, y, y + h), T().mat[k], { edges: false }); y += h; }
      top = Math.max(top, y);
    }
    return top;
  },
  estructural(c, g) {
    let top = Y0;
    for (const [a, b, ver] of lanes(c, S.cmp === 'ambos')) {
      const key = (S.cmp === 'v0' || (S.cmp === 'ambos' && ver === 0)) ? 'cm0' : 'cm4', ghosty = S.cmp === 'ambos' && ver === 0;
      let y = Y0;
      for (const k of CAPK) { const cm = c.estructura[k]?.[key] || 0; const h = cm * K.kcm; if (h < .05) continue; if (ghosty) addWire(c, g, ribbon(c.tp, a, b, y, y + h), T().capa[k]); else addSolid(c, g, ribbon(c.tp, a, b, y, y + h), T().capa[k], { edges: false }); y += h; }
      top = Math.max(top, y);
    }
    return top;
  },
  redes(c, g) {
    const r = v => Math.max(.4, 5.2 * Math.sqrt(v / (K.vred || 1))) * clamp(S.exag, .6, 1.6);
    for (const k of ['hidro', 'secas']) {
      const P = offLine(c.tp, k === 'hidro' ? -c.w / 4 : c.w / 4), v0 = c.v0[k] || 0, v4 = c.v4[k] || 0;
      const rm = r(Math.max(v0, v4)), y = k === 'secas' ? -(1.2 + rm) : -(12.5 + rm);
      const vs = S.cmp === 'v0' ? v0 : v4;
      if (vs > 0) { const tm = addSolid(c, g, tubeGeo(P, y, r(vs)), T().mat[k], { edges: false, rough: .3 }); tm.material.emissive.set(T().mat[k]); tm.material.emissiveIntensity = T().dark ? .35 : .05; tm.material.userData.emi = tm.material.emissiveIntensity; }
      if (S.cmp === 'ambos' && v0 > 0) {
        const gg = tubeGeo(P, y, r(v0) + .12);
        const f = new THREE.Mesh(gg, new THREE.MeshBasicMaterial({ color: T().ghost, transparent: true, opacity: T().dark ? .16 : .14, depthWrite: false }));
        f.userData.id = c.id; f.userData.noAO = true; g.add(f); pick.push(f); c.gm.push(f.material);
      }
    }
    return 4;
  },
  sim(c, g) {
    const j = SIM.res.byId[c.id]; c.simL = null; c.beam = null;
    if (!j) return Y0 + .5;
    let y = Y0; c.simL = []; const w = c.w / 2;
    for (const ph of j.ph) {
      const h = ph.v * SIM.res.k; if (h < .06) continue;
      const m = addSolid(c, g, ribbon(c.tp, -w + .8, w - .8, y, y + h), T().fase[ph.k], { prog: true, double: true, edges: false });
      c.simL.push({ ph, mat: m.material, y0: y, y1: y + h }); y += h + GAP;
    }
    addGhost(c, g, ribbon(c.tp, -w + .3, w - .3, Y0, Math.max(y, Y0 + 1)));
    const bm = new THREE.Mesh(new THREE.CylinderGeometry(.55, .55, 1, 12, 1, true).translate(0, .5, 0), new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: .85, depthWrite: false, blending: T().dark ? THREE.AdditiveBlending : THREE.NormalBlending }));
    bm.visible = false; bm.raycast = () => {}; bm.userData.noAO = true; g.add(bm); c.beam = bm;
    return Math.max(y, Y0 + 1);
  },
};
function buildCivs(grow = true) {
  if (civG) { scene.remove(civG); disposeTree(civG); }
  if (edgeMatShared) { edgeMatShared.dispose(); edgeMatShared = null; }
  civG = new THREE.Group(); scene.add(civG); pick = [];
  computeScales(); ensureLabels();
  const th = T(), mode = SIM.on ? 'sim' : S.mode;
  D.civs.forEach((c, i) => {
    const g = new THREE.Group(); g.userData.id = c.id; c.g = g; c.mats = []; c.gm = []; c.solids = [];
    const w = c.w / 2;
    addSolid(c, g, ribbon(c.tp, -w, w, .2, Y0), th.foot, { edges: false, noShadow: true, foot: true, opacity: mode === 'redes' ? .3 : 1 });
    // líneas de flujo a ambos bordes del frente de obra
    c.flows = [];
    for (const [a, b] of [[-w - .15, -w + .55], [w - .55, w + .15]]) { const fm = flowMat(th.flow, c.tL); const f = new THREE.Mesh(ribbon(c.tp, a, b, Y0 + .04, Y0 + .04), fm); f.userData.noAO = true; f.raycast = () => {}; g.add(f); c.flows.push(fm); }
    c.top = BUILD[mode](c, g);
    civG.add(g);
    if (grow && mode !== 'sim') { g.scale.y = .001; anims.push({ t0: performance.now() + i * 26, dur: 700, f: t => { g.scale.y = Math.max(.001, easeOut(t)); } }); }
  });
  if (SIM.on) simApply();
  refreshLabels(); applySel(); renderPanel(); dirty = true;
}

// ───────────────────────── etiquetas flotantes ─────────────────────────
function ensureLabels() {
  for (const c of D.civs) {
    if (c.lbl) continue;
    const el = document.createElement('div'); el.className = 'lbl'; el.dataset.id = c.id;
    el.innerHTML = '<div class="card"></div><div class="stem"></div><div class="dot"></div>';
    el.addEventListener('click', e => { e.stopPropagation(); selectCiv(c.id === S.sel ? null : c.id); });
    el.addEventListener('pointerenter', () => { if (!coarse()) setHover(c.id, null); });
    el.addEventListener('pointerleave', () => { if (!coarse()) setHover(null, null); });
    c.lbl = new CSS2DObject(el); c.lbl.center.set(.5, 1); scene.add(c.lbl);
  }
}
function badge(c) { return (S.hall && c.sev) ? `<span class="badge ${c.sev}" title="${c.hallazgos.length} hallazgo(s) · severidad máxima ${c.sev}">${SEVI[c.sev]} ${c.hallazgos.length}</span>` : ''; }
function miniBar(vals, tot, max) { return `<div class="mb" style="width:${Math.max(18, 124 * tot / max)}px">${MATK.filter(k => (vals[k] || 0) > 0).map(k => `<i style="flex:${vals[k]};background:${T().mat[k]}"></i>`).join('')}</div>`; }
function labelHTML(c) {
  const nm = `<div class="nm">${esc(c.nom)}<small>${esc(c.tramo)}</small>${badge(c)}</div>`;
  const chip = `<span class="d ${c.delta >= 0 ? 'up' : 'down'}">${fP(c.dpct)}</span>`;
  if (SIM.on) {
    const j = SIM.res?.byId[c.id], t = SIM.t;
    if (!j) return nm + `<div class="sb">Fuera de este escenario</div>`;
    if (t < j.s) return nm + `<div class="ph" style="color:var(--muted)">⏳ Inicia en el mes ${nf(j.s, 1)}</div><div class="sb">${fM(j.tot)} por ejecutar · frente ${j.front + 1}</div>`;
    if (t >= j.e) return nm + `<div class="ph" style="color:var(--goodtxt)">✓ Terminado · mes ${nf(j.e, 1)}</div><div class="sb">${fM(j.tot)} ejecutados</div>`;
    const ph = curPhase(j, t), done = execJob(j, t), pc = ph && ph.e > ph.s ? (t - ph.s) / (ph.e - ph.s) * 100 : 100;
    if (!ph) return nm + `<div class="ph" style="color:var(--goodtxt)">✓ Terminado · mes ${nf(j.e, 1)}</div>`;
    return nm + `<div class="ph"><i style="background:${T().fase[ph.k]}"></i>${FASEN[ph.k]} · ${nf(pc)}%</div><div class="pg"><i style="width:${done / j.tot * 100}%"></i></div><div class="sb">${fM(done)} de ${fM(j.tot)} · frente ${j.front + 1}</div>`;
  }
  switch (S.mode) {
    case 'costos': case 'alcance': {
      const v = S.cmp === 'v0' ? c.tot0 : c.tot4;
      const sb = S.mode === 'alcance' ? `<div class="sb">${GRUPON[c.grupo] || 'sin dato'}</div>` : (S.cmp === 'ambos' ? `<div class="sb">antes ${fM(c.tot0)} · ${fm2(c.m2[1])}</div>` : `<div class="sb">${fm2(c.m2[S.cmp === 'v0' ? 0 : 1])}</div>`);
      return nm + `<div class="vl">${fM(v)}${S.cmp === 'ambos' ? chip : ''}</div>` + sb;
    }
    case 'variacion': return nm + `<div class="vl ${c.delta >= 0 ? 'up' : 'down'}">${fMs(c.delta)}<span class="d">${fP(c.dpct)}</span></div><div class="sb">${fM(c.tot0)} → ${fM(c.tot4)}</div>`;
    case 'np': return nm + `<div class="vl">${fM(c.np4)}<span class="d" style="color:var(--muted)">${nf(c.pnp, 1)}% NP</span></div><div class="sb">de ${fM(c.tot4)} en V4</div>`;
    case 'materiales': {
      const mx = Math.max(c.tot0, c.tot4); let best = null, bd = 0;
      for (const k of MATK) { const d = (c.v4[k] || 0) - (c.v0[k] || 0); if (Math.abs(d) > Math.abs(bd)) { bd = d; best = k; } }
      const bars = S.cmp === 'ambos' ? miniBar(c.v0, c.tot0, mx) + miniBar(c.v4, c.tot4, mx) + `<div class="mbl">▲ antes · ▼ ahora</div>` : miniBar(S.cmp === 'v0' ? c.v0 : c.v4, 1, 1);
      return nm + `<div class="vl">${fM(S.cmp === 'v0' ? c.tot0 : c.tot4)}${S.cmp === 'ambos' ? chip : ''}</div>${bars}<div class="sb">Mayor cambio: ${MATS[best]} ${fMs(bd)}</div>`;
    }
    case 'estructural': {
      const [a, b] = c.est; const v = S.cmp === 'v0' ? a : b;
      const lay = key => `<div class="mb">${CAPK.filter(k => (c.estructura[k]?.[key] || 0) > 0).map(k => `<i style="flex:${c.estructura[k][key]};background:${T().capa[k]}"></i>`).join('')}</div>`;
      return nm + `<div class="vl">${S.cmp === 'ambos' ? `${nf(a)} → ${nf(b)} cm` : `${nf(v)} cm`}${S.cmp === 'ambos' ? `<span class="d ${b >= a ? 'up' : 'down'}">${fP(a ? (b / a - 1) * 100 : 0)}</span>` : ''}</div>${S.cmp === 'ambos' ? lay('cm0') + lay('cm4') : lay(S.cmp === 'v0' ? 'cm0' : 'cm4')}<div class="sb">espesor equivalente total</div>`;
    }
    case 'redes': {
      const r = c.redes;
      const f = k => S.cmp === 'ambos' ? `${fM(c.v0[k] || 0)} → ${fM(c.v4[k] || 0)}` : fM((S.cmp === 'v0' ? c.v0 : c.v4)[k] || 0);
      return nm + `<div class="vl">${S.cmp === 'ambos' ? `${fM(c.red[0])} → ${fM(c.red[1])}` : fM(c.red[S.cmp === 'v0' ? 0 : 1])}</div><div class="sb"><i style="display:inline-block;width:8px;height:8px;background:${T().mat.hidro};border-radius:2px"></i> Hidro ${f('hidro')} · ${nf(r.ml.hidro[0])}→${nf(r.ml.hidro[1])} ml</div><div class="sb"><i style="display:inline-block;width:8px;height:8px;background:${T().mat.secas};border-radius:2px"></i> Secas ${f('secas')} · ${nf(r.un.secas[0])}→${nf(r.un.secas[1])} un</div>`;
    }
  }
  return nm;
}
function labelKey(c) {
  if (!SIM.on) return [S.mode, S.cmp, S.theme, S.hall].join('|');
  const j = SIM.res?.byId[c.id]; if (!j) return 'sim-out' + S.theme;
  const t = SIM.t; if (t < j.s) return 'pre' + S.theme + S.hall; if (t >= j.e) return 'done' + S.theme + S.hall;
  const ph = curPhase(j, t); if (!ph) return 'done' + S.theme + S.hall; return ph.k + Math.floor((t - ph.s) / ((ph.e - ph.s) || 1) * 100) + S.theme + S.hall + Math.round(execJob(j, t) / 1e7);
}
let needMeasure = true;
function refreshLabels(force = true) {
  const changed = [];
  for (const c of D.civs) {
    const k = labelKey(c) + '|' + c.id;
    const y = (!SIM.on && S.mode === 'redes') ? 2 : c.top + 1.2;
    c.lbl.position.set(c.mid[0], y, c.mid[1]);
    if (force || k !== c.lk) { c.lk = k; const card = c.lbl.element.firstChild; card.innerHTML = labelHTML(c); card.style.setProperty('--c', civColor(c)); changed.push(c); }
  }
  for (const c of changed) { if (!c.lbl.element.isConnected) { needMeasure = true; continue; } c.lw = c.lbl.element.offsetWidth; c.lh = c.lbl.element.offsetHeight; }
  for (const r of roadLbls) if (!r.w) { if (!r.el.isConnected) { needMeasure = true; continue; } r.w = r.el.offsetWidth; r.h = r.el.offsetHeight; }
  dirty = true;
}
function measureLabels() { for (const c of D.civs) if (c.lbl?.element.isConnected) { c.lw = c.lbl.element.offsetWidth; c.lh = c.lbl.element.offsetHeight; } for (const r of roadLbls) if (r.el.isConnected) { r.w = r.el.offsetWidth; r.h = r.el.offsetHeight; } needMeasure = false; }
const _v = new THREE.Vector3();
function declutter() {
  const st = $('#stage'), W = st.clientWidth, H = st.clientHeight, placed = [], body = document.body;
  // la interfaz (barra, paneles, línea de tiempo) cuenta como ocupada: ninguna etiqueta queda debajo de ella
  const addR = sel => { const e = $(sel); if (!e || e.hidden) return; const r = e.getBoundingClientRect(); if (r.width > 0 && r.height > 0 && r.right > 0 && r.left < W) placed.push([r.left, r.top, r.right, r.bottom]); };
  if (tour.on) addR('#tourCard');
  else { addR('#bar'); if (isMobile()) { addR('#mnav'); if (sheet) addR({ an: '#an', tl: '#tl', det: '#det', set: '#setPop' }[sheet]); } else { if (body.classList.contains('an-open')) addR('#an'); else addR('#anOpen'); if (body.classList.contains('has-sel')) addR('#det'); else addR('#mini'); addR('#tl'); addR('#hud'); } }
  const fits = (x0, y0, x1, y1) => { for (const p of placed) if (x0 < p[2] && x1 > p[0] && y0 < p[3] && y1 > p[1]) return false; return true; };
  const simPri = c => { const j = SIM.res?.byId[c.id]; if (!j) return 0; return (SIM.t >= j.s && SIM.t < j.e ? 1e12 : SIM.t >= j.e ? 1e11 : 1e10) + j.tot; };
  const items = D.civs.map(c => ({ c, pri: (c.id === S.sel ? 1e16 : 0) + (c.id === S.hover ? 1e15 : 0) + (tour.on && tour.focus === c.id ? 1e17 : 0) + (S.hall && c.sev === 'ALTA' ? 1e13 : 0) + (SIM.on ? simPri(c) : Math.abs(metric(c))) }));
  items.sort((a, b) => b.pri - a.pri);
  for (const { c } of items) {
    const el = c.lbl.element; const forced = c.id === S.sel || c.id === S.hover || (tour.on && tour.focus === c.id);
    if (!S.labels && !forced) { el.classList.add('hid'); continue; }
    _v.copy(c.lbl.position).project(camera);
    if (_v.z > 1) { el.classList.add('hid'); el.classList.remove('dim'); continue; }
    const x = (_v.x + 1) / 2 * W, y = (1 - _v.y) / 2 * H, w = c.lw || 120, h = c.lh || 50;
    const r = [x - w / 2 - 4, y - h - 3, x + w / 2 + 4, y + 3];
    const show = forced || fits(...r);
    if (show) { placed.push(r); el.classList.remove('hid'); } else el.classList.add('hid');
    el.classList.toggle('dim', show && !!S.sel && c.id !== S.sel && !forced);
  }
  for (const rl of roadLbls) {
    if (!S.roads) continue;
    _v.copy(rl.o.position).project(camera);
    const x = (_v.x + 1) / 2 * W, y = (1 - _v.y) / 2 * H, w = rl.w || 60, h = rl.h || 14;
    const r = [x - w / 2 - 6, y - h / 2 - 4, x + w / 2 + 6, y + h / 2 + 4];
    if (_v.z <= 1 && x > 0 && x < W && fits(...r)) { placed.push(r); rl.el.classList.remove('hid'); } else rl.el.classList.add('hid');
  }
}

// ───────────────────────── selección, resaltado, cámara ─────────────────────────
const _ground = new THREE.Color();
function applySel() {
  _ground.set(T().ground);
  const focus = S.sel || (tour.on ? tour.focus : null);
  for (const c of D.civs) {
    const dim = focus && c.id !== focus, sel = c.id === focus, hov = c.id === S.hover && !sel;
    for (const m of c.mats) {
      m.color.copy(m.userData.base); if (dim) m.color.lerp(_ground, T().dark ? .62 : .55);
      m.emissive.copy(m.userData.base).multiplyScalar(sel ? .22 : hov ? .14 : 0);
      if (m.userData.emi != null && !sel && !hov) { m.emissive.copy(m.userData.base); m.emissiveIntensity = dim ? m.userData.emi * .3 : m.userData.emi; }
    }
    for (const m of c.gm || []) { m.userData.op ??= m.opacity; m.opacity = m.userData.op * (dim ? .35 : 1); }
    for (const f of c.flows || []) f.uniforms.uAmp.value = sel ? 1.6 : dim ? .35 : 1;
    c.lbl?.element.classList.toggle('sel', sel);
  }
  if (outline) { const t = focus ? byId[focus] : S.hover ? byId[S.hover] : null; outline.selectedObjects = t ? t.solids || [] : []; outline.enabled = !!outline.selectedObjects.length; }
  $$('#rank li').forEach(li => li.classList.toggle('sel', li.dataset.id === S.sel));
  dirty = true;
}
function selectCiv(id, fly = true, panel = true) {
  S.sel = id && byId[id] ? id : null;
  document.body.classList.toggle('has-sel', !!S.sel && panel);
  $('#det').hidden = !(S.sel && panel);
  const det = $('#mnav button[data-sheet="det"]'); if (det) det.disabled = !S.sel;
  if (S.sel && panel) { S.dtab = 'res'; renderDetail(); }
  applySel();
  if (S.sel) { if (panel && isMobile()) openSheet('det'); if (fly) fitTo([byId[S.sel]], null, null, 950, true); }
  else if (isMobile() && sheet === 'det') openSheet(null);
  writeHash(); drawMini();
}
function setHover(id, ev) {
  if (S.hover !== id) { S.hover = id; applySel(); }
  const tip = $('#tip');
  if (!id || !ev) { tip.classList.remove('on'); return; }
  const c = byId[id];
  tip.innerHTML = `<b>${esc(c.nom)} · ${esc(c.tramo)}</b><div style="color:var(--muted);font-size:11.5px;margin-bottom:6px">CIV ${c.id} · SG${c.sg} · ${GRUPON[c.grupo] || ''}</div>
    <div class="r"><span>Antes (V0)</span><b>${fM(c.tot0)}</b></div><div class="r"><span>Ahora (V4)</span><b>${fM(c.tot4)}</b></div>
    <div class="r"><span>Diferencia</span><b class="${c.delta >= 0 ? 'up' : 'down'}">${fMs(c.delta)} (${fP(c.dpct)})</b></div><div class="r"><span>No previstos V4</span><b>${fM(c.np4)} · ${nf(c.pnp, 1)}%</b></div>
    <div style="margin-top:6px;font-size:11px;color:var(--muted)">Clic para ver el detalle</div>`;
  placeTip(ev.clientX, ev.clientY);
}
function placeTip(x, y) { const tip = $('#tip'); tip.classList.add('on'); const r = tip.getBoundingClientRect(); let L = x + 16, Tp = y + 14; if (L + r.width > innerWidth - 8) L = x - r.width - 16; if (Tp + r.height > innerHeight - 8) Tp = y - r.height - 14; tip.style.left = Math.max(8, L) + 'px'; tip.style.top = Math.max(8, Tp) + 'px'; }
// Encuadre: centra la lista de CIV en el área libre de paneles (panel de análisis, detalle, línea de tiempo)
function viewRect() {
  const st = $('#stage'), W = st.clientWidth, H = st.clientHeight, mob = isMobile(), body = document.body;
  if (body.classList.contains('touring')) return { l: 0, r: W, t: H * .07, b: H - H * .07 - ($('#tourCard').offsetHeight || 170) - 24, W, H };
  const l = mob || !body.classList.contains('an-open') ? 0 : $('#an').getBoundingClientRect().right;
  const r = !mob && body.classList.contains('has-sel') ? $('#det').getBoundingClientRect().left : W;
  const t = $('#bar').getBoundingClientRect().bottom;
  const b = mob ? (sheet ? H - 62 - Math.min(H * .7, H - 170) : H - 62) : H - (body.classList.contains('tl-open') ? parseFloat(getComputedStyle(body).getPropertyValue('--tlo')) : 66) - 28;
  return { l, r, t, b, W, H };
}
function fitTo(list, polarDeg = 55, azDeg = null, ms = 900, keepAngle = false) {
  let x0 = 1e9, x1 = -1e9, z0 = 1e9, z1 = -1e9;
  for (const c of list) for (const [x, z] of c.tp) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); z0 = Math.min(z0, z); z1 = Math.max(z1, z); }
  const one = list.length === 1, tp = one ? (list[0].top || 0) : 0;
  const ctr = new THREE.Vector3((x0 + x1) / 2, one ? tp * .4 : 0, (z0 + z1) / 2);
  const rad = Math.max(70, Math.hypot(x1 - x0, z1 - z0) / 2 + (one ? 80 : 40), one ? tp * .75 + 50 : 0);
  const vr = viewRect(), vf = THREE.MathUtils.degToRad(camera.fov);
  const fracH = clamp((vr.b - vr.t) / vr.H, .3, 1), fracW = clamp((vr.r - vr.l) / vr.W, .3, 1);
  const hf = 2 * Math.atan(Math.tan(vf / 2) * camera.aspect * fracW), vfe = 2 * Math.atan(Math.tan(vf / 2) * fracH);
  const dist = rad / Math.sin(Math.min(vfe, hf) / 2) * (list.length > 1 ? .8 : 1);
  const sph = new THREE.Spherical().setFromVector3(camera.position.clone().sub(controls.target));
  const pol = polarDeg == null || keepAngle ? clamp(sph.phi, .2, 1.2) : THREE.MathUtils.degToRad(polarDeg);
  const az = azDeg == null || keepAngle ? sph.theta : THREE.MathUtils.degToRad(azDeg);
  const pos = ctr.clone().add(new THREE.Vector3().setFromSphericalCoords(dist, Math.max(pol, .001), az));
  const mpp = 2 * dist * Math.tan(vf / 2) / vr.H;
  const dx = (vr.l + vr.r) / 2 - vr.W / 2, dy = (vr.t + vr.b) / 2 - vr.H / 2;
  const rightV = new THREE.Vector3(Math.cos(az), 0, -Math.sin(az)), fwd = new THREE.Vector3(-Math.sin(az), 0, -Math.cos(az));
  const d = rightV.multiplyScalar(-dx * mpp).add(fwd.multiplyScalar(clamp(dy * mpp / Math.max(Math.cos(pol), .35), -rad, rad)));
  ctr.add(d); pos.add(d);
  flyTo(pos, ctr, ms);
}
function flyTo(pos, tgt, ms) {
  if (!ms) { camera.position.copy(pos); controls.target.copy(tgt); controls.update(); dirty = true; return; }
  const p0 = camera.position.clone(), q0 = controls.target.clone();
  anims = anims.filter(a => !a.fly);
  controls.enableDamping = false;
  anims.push({ fly: true, t0: performance.now(), dur: ms, f: t => { const e = ease(t); camera.position.lerpVectors(p0, pos, e); controls.target.lerpVectors(q0, tgt, e); controls.update(); if (t >= 1) controls.enableDamping = true; } });
}
function preset(v, ms = 1100) {
  S.view = v; $$('#views button').forEach(b => b.setAttribute('aria-pressed', b.dataset.view === v));
  if (v === 'general') fitTo(D.civs, 55, -16, ms);
  if (v === 'sg2') fitTo(D.civs.filter(c => c.sg === '2'), 50, -28, ms);
  if (v === 'sg5') fitTo(D.civs.filter(c => c.sg === '5'), 52, 18, ms);
  if (v === 'planta') fitTo(D.civs, .001, 0, ms);
}

// ───────────────────────── simulación por plazos (4D + 5D) ─────────────────────────
function scopeVals(c) {
  if (SIM.scope === 'oficial') { const o = scopeDelta(c); if (!o) return null; const f = DOFI() / DPOS(); for (const k in o) o[k] *= f; return o; }
  if (SIM.scope === 'v4') return c.fase4;
  return scopeDelta(c);
}
const DOFI = () => D.meta.totales.v4_M688 - D.meta.totales.v0_N688;
let _dpos = 0; const DPOS = () => _dpos ||= D.civs.reduce((a, c) => a + Math.max(0, c.delta), 0);
function scopeDelta(c) {
  if (SIM.scope === 'pend') return (c.grupo === 'por_iniciar' || c.grupo === 'no_alcanza') ? c.fase4 : null;
  const d = Math.max(0, c.delta); if (!d) return null;
  const w = {}; let s = 0; for (const k of FASEK) { w[k] = Math.max(0, (c.fase4[k] || 0) - (c.fase0[k] || 0)); s += w[k]; }
  if (!s) return null; const o = {}; for (const k of FASEK) o[k] = d * w[k] / s; return o;
}
const GORD = { ya_iniciados: 0, por_iniciar: 1, no_alcanza: 2 };
// Simulación por eventos: los frentes se movilizan escalonados (mov), toman el siguiente CIV de la cola al quedar libres
// y ejecutan sus fases en secuencia. Cada frente produce hasta SIM.cap $/mes y el ritmo mensual (SIM.ritmo) es un tope
// que se reparte por igual entre los frentes activos: tasa = min(cap, ritmo / activos).
function schedule(ritmo, F = SIM.fr, cap = SIM.cap) {
  const jobs = D.civs.map(c => ({ c, v: scopeVals(c) })).filter(j => j.v && sumv(j.v) > 0).map(j => ({ ...j, tot: sumv(j.v) }));
  const ord = { grupo: (a, b) => (GORD[a.c.grupo] ?? 3) - (GORD[b.c.grupo] ?? 3) || b.tot - a.tot, valor: (a, b) => b.tot - a.tot, sg: (a, b) => a.c.sg.localeCompare(b.c.sg) || b.c.mid[1] - a.c.mid[1], norte: (a, b) => a.c.mid[1] - b.c.mid[1] };
  jobs.sort(ord[SIM.ord] || ord.grupo);
  const fr = Array.from({ length: F }, (_, i) => ({ av: i * SIM.mov, job: null, pi: -1, rem: 0, jobs: [] }));
  const queue = jobs.slice(); let t = 0, guard = 0;
  const startPhase = (f, from) => { const j = f.job; for (let i = from; i < FASEK.length; i++) { const p = j.ph[i]; p.s = t; if (p.v > 0) { f.pi = i; f.rem = p.v; return true; } p.e = t; } j.e = t; f.job = null; f.av = t; return false; };
  for (const j of jobs) j.ph = FASEK.map(k => ({ k, v: j.v[k] || 0, s: 0, e: 0 }));
  while (guard++ < 5000) {
    for (const f of fr.slice().sort((a, b) => a.av - b.av)) if (!f.job && f.av <= t + 1e-9 && queue.length) { const j = queue.shift(); f.job = j; j.front = fr.indexOf(f); j.s = t; f.jobs.push(j); startPhase(f, 0); }
    const act = fr.filter(f => f.job);
    const nextAv = queue.length ? Math.min(...fr.filter(f => !f.job && f.av > t + 1e-9).map(f => f.av), Infinity) : Infinity;
    if (!act.length) { if (nextAv < Infinity) { t = nextAv; continue; } break; }
    const rate = Math.min(cap, ritmo / act.length);
    const dt = Math.min(...act.map(f => f.rem / rate), nextAv - t);
    t += dt;
    for (const f of act) { f.rem -= rate * dt; if (f.rem <= 1e-3) { f.job.ph[f.pi].e = t; startPhase(f, f.pi + 1); } }
  }
  return { jobs, fronts: fr, T: jobs.length ? Math.max(...jobs.map(j => j.e)) : 0, total: jobs.reduce((a, j) => a + j.tot, 0) };
}
const execJob = (j, t) => j.ph.reduce((a, p) => a + (p.e > p.s ? p.v * clamp((t - p.s) / (p.e - p.s), 0, 1) : (t >= p.s ? p.v : 0)), 0);
const curPhase = (j, t) => j.ph.find(p => p.v > 0 && t >= p.s && t < p.e) || null;
function simRun() {
  const r = schedule(SIM.ritmo);
  r.byId = Object.fromEntries(r.jobs.map(j => [j.c.id, j]));
  r.k = 130 * S.exag / Math.max(1, ...r.jobs.map(j => j.tot));
  r.tEnd = Math.max(r.T, 8) + .5;
  r.exec = t => r.jobs.reduce((a, j) => a + execJob(j, t), 0);
  r.tInf = schedule(1e14).T;
  if (r.tInf > 8) r.need = null;
  else { let lo = 1e7, hi = 1e14; for (let i = 0; i < 60; i++) { const mid = Math.sqrt(lo * hi); if (schedule(mid).T > 8) lo = mid; else hi = mid; } r.need = hi; }
  r.needF = null; for (let F = 1; F <= 40; F++) if (schedule(SIM.ritmo, F).T <= 8) { r.needF = F; break; }
  r.minT = r.total / SIM.ritmo;
  SIM.res = r; SIM.t = clamp(SIM.t, 0, r.tEnd);
  const sl = $('#simT'); sl.max = r.tEnd.toFixed(2); sl.value = SIM.t;
  $('#m8').style.left = `calc(8px + (100% - 16px) * ${8 / r.tEnd} - 1px)`;
  const stp = r.tEnd > 16 ? 4 : r.tEnd > 10 ? 2 : 1; let tk = ''; for (let k = 0; k <= r.tEnd; k += stp) tk += `<span style="left:${k / r.tEnd * 100}%">${k}</span>`;
  $('#tlTicks').innerHTML = tk;
  $('#simTot').textContent = nf(r.T, 1) + ' meses';
  $('#simExec').textContent = `${fM(r.exec(SIM.t))} · ${nf(r.total ? r.exec(SIM.t) / r.total * 100 : 0)}%`;
  renderSimKpi(); drawChart();
  if (SIM.on) { buildCivs(false); }
  else if (S.mode === 'sim') renderPanel();
}
function simApply() {
  const r = SIM.res, t = SIM.t;
  for (const c of D.civs) {
    if (!c.simL) continue;
    let active = null;
    for (const L of c.simL) {
      const p = L.ph, pr = p.e > p.s ? clamp((t - p.s) / (p.e - p.s), 0, 1) : (t >= p.s ? 1 : 0);
      L.mat.userData.u.uProg.value = pr; L.mat.userData.u.uGlowAmt.value = pr > 0 && pr < 1 ? 1.3 : 0;
      if (pr > 0 && pr < 1) active = { L, pr };
    }
    if (c.beam) {
      if (active) { const pt = at(c.tp, c.tcum, active.pr * c.tL); c.beam.visible = true; c.beam.position.set(pt[0], active.L.y0, pt[1]); c.beam.scale.y = active.L.y1 - active.L.y0 + 26; c.beam.material.color.set(T().fase[active.L.ph.k]).lerp(new THREE.Color('#ffffff'), .35); }
      else c.beam.visible = false;
    }
  }
  const pct = r.total ? r.exec(t) / r.total * 100 : 0;
  $('#simMes').textContent = nf(t, 1); $('#miniTxt').textContent = `Mes ${nf(t, 1)} · ${nf(pct)}%`;
  $('#simExec').textContent = `${fM(r.exec(t))} · ${nf(pct)}%`;
  if ($('#simT') !== document.activeElement) $('#simT').value = t;
  refreshLabels(false); updateCursor(); renderSimKpi(true);
  dirty = true;
}
function setSimOn(on) {
  if (SIM.on === on) return;
  SIM.on = on; $('#simOn').checked = on;
  markModes(); updateCmpUI(); applyVisibility(); buildCivs(!on); writeHash(); updateMini();
}
function markModes() { $$('#modes .tab').forEach(b => b.setAttribute('aria-pressed', SIM.on ? b.dataset.k === 'sim' : b.dataset.k === S.mode)); }
function play(on = !SIM.playing) {
  if (on && !SIM.on) setSimOn(true);
  if (on && SIM.t >= SIM.res.tEnd - .01) SIM.t = 0;
  SIM.playing = on;
  const ic = on ? '<path d="M4 2.5h3v11H4zM9 2.5h3v11H9z"/>' : '<path d="M4 2.5v11l9.5-5.5z"/>';
  $('#simPlay svg').innerHTML = ic; $('#miniPlay svg').innerHTML = ic;
  $('#simPlay').setAttribute('aria-label', on ? 'Pausar' : 'Reproducir');
  updateMini();
}
function renderSimKpi(light = false) {
  const r = SIM.res; if (!r) return;
  const t = SIM.t, act = r.jobs.filter(j => t >= j.s && t < j.e).length;
  $('#simKpi').innerHTML = `<div><small>Alcance del escenario</small><b>${fM(r.total)}</b><small>${r.jobs.length} CIV</small></div>
    <div><small>Duración simulada</small><b class="${r.T > 8 ? 'up' : ''}">${nf(r.T, 1)} meses</b><small>plazo pedido: 8</small></div>
    <div><small>Ejecutado al mes 8</small><b>${nf(r.total ? r.exec(8) / r.total * 100 : 0)}%</b><small>${fM(r.exec(8))}</small></div>
    <div><small>Frentes activos ahora</small><b>${act} de ${SIM.fr}</b><small>${fM(act ? Math.min(SIM.ritmo, act * SIM.cap) : 0)}/mes ahora</small></div>`;
  if (light) return;
  const v = $('#simVerdict'); v.className = 'verdict ' + (r.T <= 8 + 1e-6 ? 'ok' : 'bad'); v.innerHTML = verdictHTML();
}
function verdictHTML() {
  const r = SIM.res, ok = r.T <= 8 + 1e-6, opts = [];
  if (r.needF && r.needF !== SIM.fr) opts.push(`≈ <b>${r.needF} frentes</b> al ritmo elegido`);
  if (r.need && r.need > SIM.ritmo * 1.001) opts.push(`≈ <b>${fM(r.need)}/mes</b> de obra con ${SIM.fr} frentes`);
  const why = r.minT > 8.05 ? ` Aun sin tiempos muertos, ${fM(r.total)} ÷ ${fM(SIM.ritmo)}/mes = ${nf(r.minT, 1)} meses.` : '';
  return ok ? `<span class="ic">✓</span><span><b>Cabe en el plazo.</b> Con ${SIM.fr} frentes y ${fM(SIM.ritmo)}/mes el escenario termina en el mes ${nf(r.T, 1)}.</span>`
    : `<span class="ic">!</span><span><b>No cabe en 8 meses:</b> termina en el mes ${nf(r.T, 1)} (+${nf(r.T - 8, 1)}).${why} ${opts.length ? 'Para cumplir: ' + opts.join(' o ') + '.' : `Ni con ritmo ilimitado alcanza: con ${SIM.fr} frentes de hasta ${fM(SIM.cap)}/mes tarda ${nf(r.tInf, 1)} meses; se necesitan más frentes o más producción por frente.`}</span>`;
}

// Gráficas de la simulación (SVG, con cursor y tooltip)
function niceStep(x) { const p = Math.pow(10, Math.floor(Math.log10(x))); const f = x / p; return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10) * p; }
let CH = null;
function drawChart() {
  const svg = $('#simChart'), r = SIM.res; if (!svg || !r) return;
  const Wd = Math.max(260, svg.clientWidth || 600), Ht = Math.max(140, svg.clientHeight || 170);
  svg.setAttribute('viewBox', `0 0 ${Wd} ${Ht}`);
  const m = { l: 62, r: 14, t: 16, b: 24 }, iw = Wd - m.l - m.r, ih = Ht - m.t - m.b, tMax = r.tEnd;
  const X = t => m.l + t / tMax * iw;
  const xs = tMax > 24 ? 4 : tMax > 12 ? 2 : 1;
  let h = '';
  const xAxis = () => { let s = `<line x1="${m.l}" x2="${m.l + iw}" y1="${m.t + ih}" y2="${m.t + ih}" stroke="var(--hair)" stroke-width="1"/>`; for (let k = 0; k <= tMax + 1e-9; k += xs) if (X(k) < m.l + iw - 50) s += `<text x="${X(k)}" y="${Ht - 6}" text-anchor="middle">${k}</text>`; s += `<text x="${m.l + iw}" y="${Ht - 6}" text-anchor="end" style="font-weight:700">meses</text>`; return s; };
  const nearEnd = X(8) > m.l + iw - 90;
  const plazo = `<line x1="${X(8)}" x2="${X(8)}" y1="${m.t - 4}" y2="${m.t + ih}" stroke="var(--crit)" stroke-width="1.5" stroke-dasharray="4 3"/><text x="${X(8) + (nearEnd ? -4 : 4)}" y="${m.t - 3}" text-anchor="${nearEnd ? 'end' : 'start'}" style="fill:var(--crit);font-weight:700">plazo 8 meses</text>`;
  if (SIM.chart === 's') {
    const ymax = r.total * 1.12 || 1, Y = v => m.t + ih - v / ymax * ih, st = niceStep(ymax / 4);
    for (let v = 0; v <= ymax; v += st) h += `<line x1="${m.l}" x2="${m.l + iw}" y1="${Y(v)}" y2="${Y(v)}" stroke="var(--hair)" stroke-width="1" opacity=".7"/><text x="${m.l - 6}" y="${Y(v) + 3.5}" text-anchor="end">${fM(v)}</text>`;
    h += xAxis() + plazo;
    const tp = Math.min(tMax, r.total / SIM.ritmo);
    h += `<line x1="${X(0)}" y1="${Y(0)}" x2="${X(tp)}" y2="${Y(SIM.ritmo * tp)}" stroke="var(--muted)" stroke-width="1.5" stroke-dasharray="5 4"/>`;
    h += `<line x1="${m.l}" x2="${m.l + iw}" y1="${Y(r.total)}" y2="${Y(r.total)}" stroke="var(--muted)" stroke-width="1" opacity=".6"/><text x="${m.l + 4}" y="${Y(r.total) - 4}" style="font-weight:700">alcance ${fM(r.total)}</text>`;
    let d = '', a = ''; const N = 160; for (let i = 0; i <= N; i++) { const t = i / N * tMax; const p = X(t).toFixed(1) + ',' + Y(r.exec(t)).toFixed(1); d += (i ? 'L' : 'M') + p; }
    a = d + `L${X(tMax).toFixed(1)},${Y(0)}L${X(0)},${Y(0)}Z`;
    h += `<defs><linearGradient id="sg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--accent)" stop-opacity=".28"/><stop offset="1" stop-color="var(--accent)" stop-opacity="0"/></linearGradient></defs><path d="${a}" fill="url(#sg)"/>`;
    h += `<path d="${d}" fill="none" stroke="var(--accent)" stroke-width="2.4" stroke-linejoin="round"/>`;
    h += `<g><line id="curL" y1="${m.t}" y2="${m.t + ih}" stroke="var(--ink)" stroke-width="1" opacity=".55"/><circle id="curD" r="5" fill="var(--accent)" stroke="var(--solid)" stroke-width="2"/></g>`;
    h += `<g transform="translate(${m.l + iw - 232},${m.t + ih - 30})"><rect x="-8" y="-11" width="236" height="38" rx="8" fill="var(--solid)" opacity=".9"/><line x2="18" stroke="var(--accent)" stroke-width="2.4"/><text x="23" y="3.5">avance simulado</text><line x1="0" x2="18" y1="15" y2="15" stroke="var(--muted)" stroke-width="1.5" stroke-dasharray="5 4"/><text x="23" y="18.5">ritmo tope sin movilización ni pausas</text></g>`;
    CH = { m, iw, ih, X, Y, tMax };
  } else if (SIM.chart === 'm') {
    const K2 = Math.ceil(r.T - 1e-9) || 1, fl = []; for (let k = 1; k <= K2; k++) fl.push(r.exec(k) - r.exec(k - 1));
    const ymax = Math.max(SIM.ritmo, ...fl) * 1.15 || 1, Y = v => m.t + ih - v / ymax * ih, st = niceStep(ymax / 4);
    for (let v = 0; v <= ymax; v += st) h += `<line x1="${m.l}" x2="${m.l + iw}" y1="${Y(v)}" y2="${Y(v)}" stroke="var(--hair)" stroke-width="1" opacity=".7"/><text x="${m.l - 6}" y="${Y(v) + 3.5}" text-anchor="end">${fM(v)}</text>`;
    h += xAxis();
    const bw = Math.max(3, iw / tMax - 3);
    fl.forEach((v, i) => { const x = X(i) + (iw / tMax - bw) / 2; const y = Y(v); h += `<rect class="fbar" data-k="${i + 1}" data-v="${v}" x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${bw.toFixed(1)}" height="${Math.max(0, m.t + ih - y).toFixed(1)}" rx="4" fill="var(--accent)"/>`; });
    h += plazo + `<line x1="${m.l}" x2="${m.l + iw}" y1="${Y(SIM.ritmo)}" y2="${Y(SIM.ritmo)}" stroke="var(--ink)" stroke-width="1.2" stroke-dasharray="5 4" opacity=".7"/><text x="${m.l + iw - 4}" y="${Y(SIM.ritmo) - 5}" text-anchor="end" style="font-weight:700;fill:var(--ink2)">ritmo elegido ${fM(SIM.ritmo)}/mes</text>`;
    h += `<g><line id="curL" y1="${m.t}" y2="${m.t + ih}" stroke="var(--ink)" stroke-width="1" opacity=".55"/></g>`;
    CH = { m, iw, ih, X, tMax };
  } else {
    const F = SIM.fr, rh = Math.min(24, ih / F), gap = Math.min(4, rh * .18);
    h += xAxis();
    for (let f = 0; f < F; f++) h += `<text x="${m.l - 6}" y="${m.t + f * rh + rh / 2 + 3.5}" text-anchor="end">Frente ${f + 1}</text>`;
    for (const j of r.jobs) {
      const y = m.t + j.front * rh + gap / 2, hh = rh - gap;
      for (const p of j.ph) { if (p.e - p.s <= 0) continue; h += `<rect class="gseg" data-id="${j.c.id}" data-k="${p.k}" x="${X(p.s).toFixed(1)}" y="${y.toFixed(1)}" width="${Math.max(.8, X(p.e) - X(p.s)).toFixed(1)}" height="${hh.toFixed(1)}" fill="${T().fase[p.k]}"/>`; }
      h += `<rect class="gjob" data-id="${j.c.id}" x="${X(j.s).toFixed(1)}" y="${y.toFixed(1)}" width="${(X(j.e) - X(j.s)).toFixed(1)}" height="${hh.toFixed(1)}" fill="none" stroke="var(--solid)" stroke-width="1.5" rx="2"/>`;
      if (X(j.e) - X(j.s) > 46 && hh > 11) h += `<text x="${X(j.s) + 4}" y="${y + hh / 2 + 3.5}" style="fill:#fff;font-weight:700;pointer-events:none;paint-order:stroke;stroke:rgba(0,0,0,.45);stroke-width:2px">${esc(j.c.nom)}</text>`;
    }
    h += plazo + `<g><line id="curL" y1="${m.t}" y2="${m.t + ih}" stroke="var(--ink)" stroke-width="1.2" opacity=".7"/></g>`;
    CH = { m, iw, ih, X, tMax };
  }
  svg.innerHTML = h; updateCursor();
}
function updateCursor() {
  if (!CH) return; const x = CH.X(SIM.t); const l = $('#curL'); if (l) { l.setAttribute('x1', x); l.setAttribute('x2', x); }
  const d = $('#curD'); if (d && CH.Y) { d.setAttribute('cx', x); d.setAttribute('cy', CH.Y(SIM.res.exec(SIM.t))); }
  $$('#simChart .fbar').forEach(b => b.setAttribute('opacity', +b.dataset.k === Math.ceil(SIM.t || 1e-9) ? 1 : .55));
}
function chartHover(e) {
  const svg = $('#simChart'), r = SIM.res; if (!CH || !r) return;
  const b = svg.getBoundingClientRect(), vb = svg.viewBox.baseVal, sx = vb.width / b.width;
  const x = (e.clientX - b.left) * sx, t = clamp((x - CH.m.l) / CH.iw * CH.tMax, 0, CH.tMax);
  const tip = $('#tip'); let html = ''; const tg = e.target;
  if (SIM.chart === 'g' && tg.classList && (tg.classList.contains('gseg') || tg.classList.contains('gjob'))) {
    const j = r.byId[tg.dataset.id], p = tg.dataset.k ? j.ph.find(q => q.k === tg.dataset.k) : null;
    html = `<b>${esc(j.c.nom)} · ${esc(j.c.tramo)}</b><div class="r"><span>Frente</span><b>${j.front + 1}</b></div><div class="r"><span>Inicio → fin</span><b>mes ${nf(j.s, 1)} → ${nf(j.e, 1)}</b></div>` + (p ? `<div class="r"><span>${FASEN[p.k]}</span><b>${fM(p.v)}</b></div><div class="r"><span>Fase</span><b>mes ${nf(p.s, 1)} → ${nf(p.e, 1)}</b></div>` : '') + `<div style="font-size:11px;color:var(--muted);margin-top:4px">Clic para ver el CIV</div>`;
  } else if (SIM.chart === 'm' && tg.classList && tg.classList.contains('fbar')) {
    html = `<b>Mes ${tg.dataset.k}</b><div class="r"><span>Obra ejecutada</span><b>${fM(+tg.dataset.v)}</b></div><div class="r"><span>Ritmo elegido</span><b>${fM(SIM.ritmo)}</b></div>`;
  } else if (SIM.chart === 's') {
    const v = r.exec(t);
    html = `<b>Mes ${nf(t, 1)}</b><div class="r"><span>Avance simulado</span><b>${fM(v)} · ${nf(r.total ? v / r.total * 100 : 0)}%</b></div><div class="r"><span>Frentes activos</span><b>${r.jobs.filter(j => t >= j.s && t < j.e).length}</b></div>`;
    let hl = $('#hovL'); if (!hl) { svg.insertAdjacentHTML('beforeend', `<line id="hovL" y1="${CH.m.t}" y2="${CH.m.t + CH.ih}" stroke="var(--muted)" stroke-width="1" stroke-dasharray="2 3"/>`); hl = $('#hovL'); }
    hl.setAttribute('x1', CH.X(t)); hl.setAttribute('x2', CH.X(t));
  }
  if (html) { tip.innerHTML = html; placeTip(e.clientX, e.clientY); } else tip.classList.remove('on');
}

// ───────────────────────── panel de análisis: pregunta, cifras, lo que hay que ver ─────────────────────────
const kpiPair = (a, b, la = 'Antes · V0', lb = 'Ahora · V4', fmt = fM, dfmt = null) => {
  const mx = Math.max(Math.abs(a), Math.abs(b)) || 1, d = b - a, pc = a ? d / a * 100 : 0;
  return `<div class="kpi2"><div><small>${la}</small><b>${fmt(a)}</b></div><span class="ar">→</span><div class="r"><small>${lb}</small><b>${fmt(b)}</b></div>
    <div class="kbar"><i style="width:${Math.abs(a) / mx * 100}%;background:var(--muted);opacity:.55"></i><i style="width:${Math.abs(b) / mx * 100}%;background:var(--accent)"></i></div>
    <div class="kd"><span class="badge ${d >= 0 ? 'up' : 'down'}">${dfmt ? dfmt(d) : fMs(d)}</span><span class="${d >= 0 ? 'up' : 'down'}">${fP(pc)}</span></div></div>`;
};
function insight() {
  const mode = SIM.on ? 'sim' : S.mode, C = D.civs, t = D.tot, dT = t.t4 - t.t0;
  const top = (f, n = 1) => C.slice().sort((a, b) => f(b) - f(a)).slice(0, n);
  const civTxt = c => `<b>${esc(c.nom)}</b> · ${esc(c.tramo)}`;
  switch (mode) {
    case 'costos': {
      const [a] = top(c => c.tot4), [hm2] = top(c => c.m2[1]), [lm2] = top(c => -c.m2[1]);
      return { kpi: kpiPair(t.t0, t.t4), items: [
        { id: a.id, html: `${civTxt(a)} es la calle más costosa: <b>${fM(a.tot4)}</b>, el ${nf(a.tot4 / t.t4 * 100, 1)}% del total.` },
        { id: hm2.id, html: `El mayor costo por m² está en ${civTxt(hm2)}: <b>${fm2(hm2.m2[1])}</b> (antes ${fm2(hm2.m2[0])}).` },
        { id: lm2.id, html: `El menor, en ${civTxt(lm2)}: ${fm2(lm2.m2[1])}. Promedio del grupo: <b>${fm2(t.t4 / t.a)}</b>.` }] };
    }
    case 'variacion': {
      const [a] = top(c => c.delta), [p] = top(c => c.dpct), dn = C.filter(c => c.delta < 0);
      return { kpi: kpiPair(t.t0, t.t4), items: [
        { id: a.id, html: `La mayor alza: ${civTxt(a)}, <b>${fMs(a.delta)}</b> (${fP(a.dpct)}).` },
        ...(p.id !== a.id ? [{ id: p.id, html: `La mayor alza relativa: ${civTxt(p)}, <b>${fP(p.dpct)}</b>.` }] : []),
        { id: dn[0]?.id, html: `<b>${C.length - dn.length} de ${C.length}</b> calles suben; ${dn.length ? `solo ${dn.length} bajan: ${dn.map(c => `${esc(c.nom)} (${fMs(c.delta)})`).join(' y ')}.` : 'ninguna baja.'}` }] };
    }
    case 'materiales': {
      const ds = MATK.map(k => [k, D.mat[k][1] - D.mat[k][0]]).sort((a, b) => b[1] - a[1]);
      return { kpi: kpiPair(t.t0, t.t4), items: ds.slice(0, 3).map(([k, d]) => ({ mode: 'materiales', html: `<i style="display:inline-block;width:10px;height:10px;border-radius:3px;background:${T().mat[k]};margin-right:6px;vertical-align:-1px"></i><b>${MATS[k]}</b>: ${fMs(d)}, el <b>${nf(d / dT * 100, 1)}%</b> del aumento (${fM(D.mat[k][0])} → ${fM(D.mat[k][1])}).` })) };
    }
    case 'estructural': {
      const avg = k => C.reduce((a, c) => a + c.est[k] * c.area, 0) / t.a, [e] = top(c => c.est[1] - c.est[0]);
      const withLosa = C.filter(c => (c.estructura.losa?.cm4 || 0) > 0).length;
      return { kpi: kpiPair(avg(0), avg(1), 'Antes · V0', 'Ahora · V4', v => nf(v, 1) + ' cm', d => (d >= 0 ? '+' : '−') + nf(Math.abs(d), 1) + ' cm'), items: [
        { id: e.id, html: `El mayor engrosamiento: ${civTxt(e)}, de <b>${nf(e.est[0])}</b> a <b>${nf(e.est[1])} cm</b> equivalentes.` },
        { html: `Espesor equivalente promedio (ponderado por área): <b>${nf(avg(0), 1)} → ${nf(avg(1), 1)} cm</b>.` },
        { html: `${withLosa} de ${C.length} CIV llevan losa de concreto en V4. El espesor equivalente es m³ ÷ área: mide intensidad, no el diseño.` }] };
    }
    case 'redes': {
      const r0 = C.reduce((a, c) => a + c.red[0], 0), r4 = C.reduce((a, c) => a + c.red[1], 0), [a] = top(c => c.red[1] - c.red[0]);
      const u0 = C.reduce((a, c) => a + c.redes.un.secas[0], 0), u4 = C.reduce((a, c) => a + c.redes.un.secas[1], 0);
      const m0 = C.reduce((a, c) => a + c.redes.ml.hidro[0], 0), m4 = C.reduce((a, c) => a + c.redes.ml.hidro[1], 0);
      return { kpi: kpiPair(r0, r4), items: [
        { html: `Las redes explican <b>${nf((r4 - r0) / dT * 100)}%</b> del aumento total del plano (${fMs(r4 - r0)} de ${fMs(dT)}).` },
        { html: `Hidrosanitarias: ${nf(m0)} → <b>${nf(m4)} ml</b>; redes secas: ${nf(u0)} → <b>${nf(u4)} unidades</b>.` },
        { id: a.id, html: `Donde más crecen: ${civTxt(a)}, <b>${fMs(a.red[1] - a.red[0])}</b>.` }] };
    }
    case 'np': {
      const [p] = top(c => c.pnp), [v] = top(c => c.np4), n25 = C.filter(c => c.pnp > 25).length;
      return { kpi: `<div class="kpi2"><div style="grid-column:1/4"><small>No previstos en V4 · 27 CIV</small><b>${fM(t.np)}</b></div>
        <div class="kbar"><div style="display:flex;height:8px;border-radius:4px;overflow:hidden;background:var(--chip2)"><i style="width:${t.np / t.t4 * 100}%;height:8px;border-radius:0;background:${ramp(T().np, .75)}"></i></div></div>
        <div class="kd"><span class="badge up">${nf(t.np / t.t4 * 100, 1)}% de V4</span><span style="color:var(--muted);font-weight:600">equivale al ${nf(t.np / dT * 100)}% del aumento</span></div></div>`, items: [
        { id: p.id, html: `En ${civTxt(p)} el <b>${nf(p.pnp, 1)}%</b> del valor son ítems no previstos (${fM(p.np4)}).` },
        { id: v.id, html: `El mayor valor NP: ${civTxt(v)}, <b>${fM(v.np4)}</b>.` },
        { html: `<b>${n25} CIV</b> superan el 25% de su valor en no previstos.` }] };
    }
    case 'alcance': {
      const g = {}; C.forEach(c => { (g[c.grupo] ||= { n: 0, v: 0, d: 0 }); g[c.grupo].n++; g[c.grupo].v += c.tot4; g[c.grupo].d += c.delta; });
      return { kpi: kpiPair(t.t0, t.t4), items: Object.keys(GRUPON).filter(k => g[k]).map(k => ({ group: k, html: `<i style="display:inline-block;width:10px;height:10px;border-radius:50%;background:${T().grupo[k]};margin-right:6px"></i><b>${GRUPON[k]}</b>: ${g[k].n} CIV · ${fM(g[k].v)} en V4 (${fMs(g[k].d)}).` })) };
    }
    case 'sim': {
      const r = SIM.res, ok = r.T <= 8 + 1e-6;
      return { kpi: `<div class="kpi2"><div><small>Plazo pedido</small><b>8,0 meses</b></div><span class="ar">→</span><div class="r"><small>Simulado</small><b class="${ok ? '' : 'up'}">${nf(r.T, 1)} meses</b></div>
        <div class="kbar"><i style="width:${8 / Math.max(8, r.T) * 100}%;background:var(--muted);opacity:.55"></i><i style="width:${r.T / Math.max(8, r.T) * 100}%;background:${ok ? 'var(--good)' : 'var(--crit)'}"></i></div>
        <div class="kd"><span class="badge ${ok ? 'down' : 'up'}">${ok ? 'Cabe' : '+' + nf(r.T - 8, 1) + ' meses'}</span><span style="color:var(--muted);font-weight:600">${fM(r.total)} · ${r.jobs.length} CIV</span></div></div>`,
        items: [{ html: verdictHTML().replace(/<span class="ic">.<\/span>/, '') }, { html: `Al mes 8 se habría ejecutado el <b>${nf(r.total ? r.exec(8) / r.total * 100 : 0)}%</b> (${fM(r.exec(8))}).` }, { html: `Ajuste frentes, ritmo y producción en <b>Analítica</b> (línea de tiempo) y pulse ▶ para verlo construirse.`, tl: true }] };
    }
  }
  return { kpi: '', items: [] };
}
function renderPanel() {
  const mode = SIM.on ? 'sim' : S.mode, md = MODES.find(m => m.k === mode);
  $('#anKicker').innerHTML = `<svg class="i" viewBox="0 0 24 24">${ICON[mode]}</svg>${md.n}`;
  $('#anQ').textContent = md.q;
  const ins = insight();
  $('#anKpi').innerHTML = ins.kpi;
  $('#anIns').innerHTML = ins.items.map((it, i) => `<li data-i="${i}"><span class="n">${i + 1}</span><span>${it.html}</span>${it.id || it.group || it.tl ? '<span class="go">›</span>' : ''}</li>`).join('');
  $('#anIns').onclick = e => { const li = e.target.closest('li'); if (!li) return; const it = ins.items[+li.dataset.i]; if (!it) return;
    if (it.id) selectCiv(it.id); else if (it.group) fitTo(D.civs.filter(c => c.grupo === it.group), 52, null, 1100); else if (it.tl) toggleTl(true); };
  updateCmpUI(); renderLegend(); renderRank(); drawMini();
}
function updateCmpUI() {
  const md = MODES.find(m => m.k === (SIM.on ? 'sim' : S.mode));
  $('#cmpSec').hidden = !md.cmp;
  $$('#cmp button').forEach(b => b.setAttribute('aria-pressed', b.dataset.v === S.cmp));
  const notes = { costos: 'Sólido = ahora (V4) · contorno de vidrio = antes (V0). Si el vidrio sobresale, el CIV bajó.', alcance: 'Sólido = ahora (V4) · contorno de vidrio = antes (V0).', materiales: 'Dos franjas por calle: de alambre = antes (V0), sólida = ahora (V4), con el mismo orden de capas.', estructural: 'Dos franjas por calle: de alambre = antes (V0), sólida = ahora (V4), con el mismo orden de capas.', redes: 'Tubo sólido = ahora (V4) · tubo de vidrio = antes (V0).' };
  $('#cmpNote').textContent = S.cmp === 'ambos' ? (notes[md.k] || '') : S.cmp === 'v0' ? 'Solo el presupuesto contractual (V0), repartido por CIV.' : 'Solo el presupuesto radicado el 01-09-2026 (V4).';
}
function renderLegend() {
  const th = T(), el = $('#legend'); const mode = SIM.on ? 'sim' : S.mode; const md = MODES.find(m => m.k === mode);
  const row = (col, txt, v = '', cls = '') => `<div class="lg-row"><i class="sw ${cls}" style="background:${col}"></i><span>${txt}</span><span class="v">${v}</span></div>`;
  const grad = (st, a, b, mid) => `<div class="grad" style="background:linear-gradient(90deg,${[0, .25, .5, .75, 1].map(t => ramp(st, t)).join(',')})"></div><div class="ticks"><span>${a}</span>${mid ? `<span>${mid}</span>` : ''}<span>${b}</span></div>`;
  let h = `<p class="lg-h">${md.help}</p>`;
  const ghost = S.cmp === 'ambos' && md.cmp ? row('transparent', (mode === 'materiales' || mode === 'estructural') ? 'Franja de alambre = antes (V0)' : 'Contorno de vidrio = antes (V0)', '', 'ghost') : '';
  if (mode === 'costos') h += `<div class="lg-h" style="margin:0"><b>Color:</b> costo por m² (${S.cmp === 'v0' ? 'V0' : 'V4'})</div>` + grad(th.seq, fm2(K.m2min), fm2(K.m2max)) + `<div style="height:8px"></div>` + ghost;
  if (mode === 'variacion') h += grad(th.div, fP(-K.dmax, 0), fP(K.dmax, 0), '0%');
  if (mode === 'np') h += grad(th.np, '0% NP', nf(K.pmax, 0) + '% NP') + `<div style="height:8px"></div>` + row('transparent', 'Contorno = total del CIV en V4', '', 'ghost');
  if (mode === 'alcance') h += Object.keys(GRUPON).map(k => row(th.grupo[k], GRUPON[k])).join('') + ghost;
  if (mode === 'materiales') h += `<div class="lg-row" style="font-size:10.5px;color:var(--muted);font-weight:700"><span style="margin-left:22px">DE ARRIBA ABAJO EN LA COLUMNA</span><span class="v">Δ total</span></div>` + MATK.slice().reverse().map(k => row(th.mat[k], MATS[k], fMs(D.mat[k][1] - D.mat[k][0]))).join('') + ghost;
  if (mode === 'estructural') h += CAPK.slice().reverse().map(k => row(th.capa[k], CAPN[k])).join('') + `<div class="lg-h" style="margin-top:6px">Escala vertical: 1 cm de espesor = ${nf(K.kcm, 2)} m en el plano.</div>` + ghost;
  if (mode === 'redes') h += row(th.mat.hidro, MATN.hidro, 'tubo profundo') + row(th.mat.secas, MATN.secas, 'tubo somero') + ghost + `<div class="lg-h" style="margin-top:6px">El terreno se vuelve translúcido para ver el subsuelo.</div>`;
  if (mode === 'sim') h += FASEK.map(k => row(th.fase[k], FASEN[k])).join('') + row('transparent', 'Contorno = volumen final planeado', '', 'ghost');
  if (S.hall) h += `<div class="lg-row" style="margin-top:6px;align-items:flex-start"><span class="sev ALTA" style="margin-top:1px">▲ n</span><span>Hallazgos del análisis: ▲ alta · ● media · ℹ informativa; n = cantidad.</span></div>`;
  if (th.figurative) h += `<p class="note">Paleta figurativa: identifique cada franja por la leyenda y las etiquetas, no solo por el color.</p>`;
  el.innerHTML = h;
}
function renderRank() {
  const list = D.civs.slice(); const mode = SIM.on ? 'sim' : S.mode;
  list.sort((a, b) => metric(b) - metric(a));
  const vals = list.map(metric), mx = Math.max(...vals.map(Math.abs)) || 1;
  const fmt = c => {
    if (SIM.on) { const j = SIM.res.byId[c.id]; return j ? `m ${nf(j.s, 1)}→${nf(j.e, 1)}` : '—'; }
    switch (mode) { case 'variacion': return fMs(c.delta); case 'estructural': return nf(metric(c)) + ' cm'; case 'np': return fM(c.np4) + ` · ${nf(c.pnp)}%`; default: return fM(metric(c)); }
  };
  $('#rankNote').textContent = SIM.on ? 'Orden de inicio en la simulación (meses de inicio → fin).' : mode === 'variacion' ? 'Barra centrada: derecha sube, izquierda baja.' : 'Ordenado por la métrica del mapa. Clic para ubicar el CIV.';
  const shown = S.rankAll ? list : list.slice(0, 8);
  $('#rank').innerHTML = shown.map((c, i) => {
    const v = metric(c), col = civColor(c); let bar;
    if (mode === 'variacion') { const w = Math.abs(v) / mx * 50; bar = `<i style="background:${col};${v >= 0 ? `left:50%;width:${w}%` : `left:${50 - w}%;width:${w}%`}"></i><span class="mid"></span>`; }
    else if (SIM.on) { const j = SIM.res.byId[c.id]; const tm = SIM.res.tEnd; bar = j ? `<i style="background:var(--accent);left:${j.s / tm * 100}%;width:${Math.max(1, (j.e - j.s) / tm * 100)}%"></i>` : ''; }
    else bar = `<i style="background:${col};left:0;width:${Math.abs(v) / mx * 100}%"></i>`;
    return `<li data-id="${c.id}" class="${c.id === S.sel ? 'sel' : ''}" title="${esc(c.nom + ' · ' + c.tramo)} (CIV ${c.id})"><span class="n">${i + 1}</span><span class="t">${esc(c.nom)} <small>${esc(c.tramo)}</small></span><span class="v">${fmt(c)}</span><span></span><span class="bar">${bar}</span></li>`;
  }).join('');
  $('#rankMore').textContent = S.rankAll ? 'Ver solo los 8 primeros' : `Ver los ${list.length} CIV`;
}

// ───────────────────────── detalle del CIV (pestañas) ─────────────────────────
function renderDetail() {
  const el = $('#detail'), c = byId[S.sel]; if (!c) { el.innerHTML = ''; return; }
  const th = T(), mx = Math.max(c.tot0, c.tot4), j = SIM.res?.byId[c.id];
  const tabs = [['res', 'Resumen'], ['mat', 'Materiales'], ['est', 'Estructura'], ['red', 'Redes'], ['ren', 'Ítems'], ...(c.hallazgos?.length ? [['hal', `Hallazgos ${c.hallazgos.length}`]] : [])];
  if (!tabs.some(t => t[0] === S.dtab)) S.dtab = 'res';
  el.style.setProperty('--dc', civColor(c));
  el.innerHTML = `
  <div class="dh"><div class="dh-top"><span class="kicker">CIV ${c.id} · Subgrupo ${c.sg}</span><button class="close dclose" data-close="det" aria-label="Cerrar detalle">✕ Cerrar</button></div>
    <h2>${esc(c.nom)}</h2><div class="tr">${esc(c.tramo)} · ${nf(c.longitud, 1)} m × ${nf(c.ancho, 1)} m · ${nf(c.area)} m²</div>
    <div class="chips"><span class="chip"><i style="background:${th.grupo[c.grupo] || th.foot}"></i>${GRUPON[c.grupo] || 'sin grupo'}</span>${c.sev ? `<span class="chip"><span class="sev ${c.sev}" style="padding:0 5px">${SEVI[c.sev]}</span>${c.hallazgos.length} hallazgo(s)</span>` : ''}<span class="chip ${c.delta >= 0 ? 'up' : 'down'}" style="font-weight:750">${fMs(c.delta)} · ${fP(c.dpct)}</span></div>
    <div class="dcmp"><small>Antes</small><div class="b" style="width:${c.tot0 / mx * 100}%;background:var(--muted);opacity:.6"></div><b>${fM(c.tot0)}</b><small>Ahora</small><div class="b" style="width:${c.tot4 / mx * 100}%;background:var(--accent)"></div><b>${fM(c.tot4)}</b></div>
  </div>
  <div class="dtabs" role="tablist">${tabs.map(([k, n]) => `<button data-t="${k}" aria-pressed="${k === S.dtab}">${n}</button>`).join('')}</div>
  <div class="dbody">${DTAB[S.dtab](c, th, mx, j)}</div>
  <div class="dfoot"><a class="btn pri" href="../index.html#p75/civ/${encodeURIComponent(c.id)}">Abrir ficha en el análisis ↗</a><button class="btn" id="dFit" type="button">⌖ Centrar</button></div>`;
  $('#dFit').onclick = () => fitTo([c], null, null, 800, true);
  $$('.dtabs button', el).forEach(b => b.onclick = () => { S.dtab = b.dataset.t; renderDetail(); });
}
const sw = col => `<i style="display:inline-block;width:10px;height:10px;border-radius:3px;background:${col};vertical-align:-1px;margin-right:7px"></i>`;
const DTAB = {
  res: (c, th, mx, j) => `<div class="dkpis">
      <div class="dk"><small>Antes · V0</small><b>${fM(c.tot0)}</b><em>${fm2(c.m2[0])}</em></div>
      <div class="dk"><small>Ahora · V4</small><b>${fM(c.tot4)}</b><em>${fm2(c.m2[1])}</em></div>
      <div class="dk"><small>Diferencia</small><b class="${c.delta >= 0 ? 'up' : 'down'}">${fMs(c.delta)}</b><em>${fP(c.dpct)}</em></div>
      <div class="dk"><small>No previstos en V4</small><b>${fM(c.np4)}</b><em>${nf(c.pnp, 1)}% del CIV</em></div></div>
    <div class="dsec"><h4>De dónde sale el cambio</h4><table class="t"><tr><th>Componente</th><th>Δ</th></tr>
      ${[['Aumentos de cantidad', c.desc?.delta_por_aumentos], ['Disminuciones', c.desc?.delta_por_disminuciones], ['No previstos (NP)', c.desc?.delta_por_np], ['Contractual nuevo', c.desc?.delta_por_contractual_nuevo], ['Eliminado', c.desc?.delta_por_eliminado]].filter(r => r[1]).map(([n, v]) => `<tr><td>${n}</td><td class="${v >= 0 ? 'up' : 'down'}">${fMs(v)}</td></tr>`).join('')}</table>
      <p class="note">Descomposición del análisis 02 (obras con AIU).</p></div>
    ${j ? `<div class="dsec"><h4>En la simulación</h4><div style="font-size:12.5px;margin-bottom:6px">Frente ${j.front + 1} · mes ${nf(j.s, 1)} → ${nf(j.e, 1)} · ${fM(j.tot)}</div><table class="t"><tr><th>Fase</th><th>Valor</th><th>Meses</th></tr>${j.ph.filter(p => p.v > 0).map(p => `<tr><td>${sw(th.fase[p.k])}${FASEN[p.k]}</td><td>${fM(p.v)}</td><td>${nf(p.s, 1)}–${nf(p.e, 1)}</td></tr>`).join('')}</table></div>` : ''}
    <div class="dsec"><h4>Geometría</h4><p class="note" style="margin:0">${esc(c.nota_geom)} Longitud del inventario ${nf(c.longitud, 1)} m · eje OSM ${nf(c.long_osm, 1)} m.</p></div>`,
  mat: (c, th, mx) => {
    const mbar = (vals, tot) => `<div class="mbar" style="width:${tot / mx * 100}%">${MATK.filter(k => (vals[k] || 0) > 0).map(k => `<i style="flex:${vals[k]};background:${th.mat[k]}" title="${MATS[k]}: ${fM(vals[k])}"></i>`).join('')}</div>`;
    const rows = MATK.filter(k => (c.v0[k] || 0) || (c.v4[k] || 0)).map(k => { const d = (c.v4[k] || 0) - (c.v0[k] || 0); return `<tr><td>${sw(th.mat[k])}${MATS[k]}</td><td>${fM(c.v0[k] || 0)}</td><td>${fM(c.v4[k] || 0)}</td><td class="${d >= 0 ? 'up' : 'down'}">${fMs(d)}</td></tr>`; }).join('');
    return `<div class="mrow"><small>Antes</small>${mbar(c.v0, c.tot0)}<b style="font-size:12px">${fM(c.tot0)}</b></div><div class="mrow"><small>Ahora</small>${mbar(c.v4, c.tot4)}<b style="font-size:12px">${fM(c.tot4)}</b></div>
      <table class="t" style="margin-top:12px"><tr><th>Material</th><th>Antes</th><th>Ahora</th><th>Δ</th></tr>${rows}</table>`;
  },
  est: c => `<div class="xs">${xsSVG(c)}</div><p class="note">Espesor equivalente = m³ del CIV ÷ área del CIV: mide la intensidad de cada capa, no el espesor de diseño.</p>
    <table class="t" style="margin-top:8px"><tr><th>Capa</th><th>Antes</th><th>Ahora</th></tr>${CAPK.slice().reverse().filter(k => (c.estructura[k]?.cm0 || 0) || (c.estructura[k]?.cm4 || 0)).map(k => `<tr><td>${sw(T().capa[k])}${CAPN[k]}</td><td>${nf(c.estructura[k].cm0, 1)} cm</td><td>${nf(c.estructura[k].cm4, 1)} cm</td></tr>`).join('')}</table>`,
  red: c => { const r = c.redes; return `<div class="dkpis"><div class="dk"><small>Redes · antes</small><b>${fM(c.red[0])}</b></div><div class="dk"><small>Redes · ahora</small><b>${fM(c.red[1])}</b><em class="${c.red[1] >= c.red[0] ? 'up' : 'down'}">${fMs(c.red[1] - c.red[0])}</em></div></div>
    <table class="t" style="margin-top:12px"><tr><th></th><th>Antes</th><th>Ahora</th></tr>
      <tr><td>${sw(T().mat.hidro)}Hidrosanitarias ($)</td><td>${fM(c.v0.hidro || 0)}</td><td>${fM(c.v4.hidro || 0)}</td></tr>
      <tr><td>Hidrosanitarias (ml)</td><td>${nf(r.ml.hidro[0], 1)}</td><td>${nf(r.ml.hidro[1], 1)}</td></tr>
      <tr><td>Hidrosanitarias (un)</td><td>${nf(r.un.hidro[0], 1)}</td><td>${nf(r.un.hidro[1], 1)}</td></tr>
      <tr><td>${sw(T().mat.secas)}Redes secas ($)</td><td>${fM(c.v0.secas || 0)}</td><td>${fM(c.v4.secas || 0)}</td></tr>
      <tr><td>Redes secas (ml)</td><td>${nf(r.ml.secas[0], 1)}</td><td>${nf(r.ml.secas[1], 1)}</td></tr>
      <tr><td>Redes secas (un)</td><td>${nf(r.un.secas[0], 1)}</td><td>${nf(r.un.secas[1], 1)}</td></tr>
      <tr><td>${sw(T().mat.anden)}Andenes (m²)</td><td>${nf(c.andenM2[0], 1)}</td><td>${nf(c.andenM2[1], 1)}</td></tr></table>`; },
  ren: c => `<table class="t"><tr><th>Ítem</th><th style="text-align:left">Descripción</th><th>Cant.</th><th>Δ $</th></tr>${(c.topDelta || []).slice(0, 10).map(it => { const d = it.v4 - it.v0; return `<tr><td>${esc(it.i)}${it.np ? ' <span class="npb">NP</span>' : ''}</td><td class="desc">${esc(it.d.slice(0, 70))}${it.d.length > 70 ? '…' : ''}</td><td>${nf(it.q0, 1)} → ${nf(it.q4, 1)} ${esc(it.u || '')}</td><td class="${d >= 0 ? 'up' : 'down'}">${fMs(d)}</td></tr>`; }).join('')}</table><p class="note">Los 10 renglones con mayor cambio en pesos en este CIV. NP = ítem no previsto.</p>`,
  hal: c => (c.hallazgos || []).map(h => `<a class="hl" href="../index.html#p75/hall/${encodeURIComponent(h.id)}"><span class="sev ${h.s}">${SEVI[h.s] || ''} ${h.s}</span><span><b>${esc(h.id)}</b> · ${esc(h.t)}</span></a>`).join('') + `<p class="note">Clic abre la ficha del hallazgo en el análisis.</p>`,
};
function xsSVG(c) {
  const th = T(), H = 150, cw = 74, xa = 58, xb = 188, tot = [c.est[0], c.est[1]], mx = Math.max(...tot) || 1;
  let s = `<svg viewBox="0 0 300 ${H + 40}" role="img" aria-label="Corte de la estructura antes y ahora">`;
  [['cm0', xa, 'Antes'], ['cm4', xb, 'Ahora']].forEach(([key, x, lab], vi) => {
    let y = H + 8;
    for (const k of CAPK) {
      const cm = c.estructura[k]?.[key] || 0; if (cm <= 0) continue;
      const h = cm / mx * H; y -= h;
      s += `<rect x="${x}" y="${y.toFixed(1)}" width="${cw}" height="${Math.max(1, h - 1.5).toFixed(1)}" rx="2" fill="${th.capa[k]}"><title>${CAPN[k]}: ${nf(cm, 1)} cm</title></rect>`;
      if (h > 12) s += `<text x="${x + cw / 2}" y="${(y + h / 2 + 4).toFixed(1)}" text-anchor="middle" font-size="10.5" font-weight="700" fill="${inkOn(th.capa[k])}">${nf(cm, 1)}</text>`;
    }
    s += `<text x="${x + cw / 2}" y="${H + 24}" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--ink)">${lab}</text><text x="${x + cw / 2}" y="${H + 37}" text-anchor="middle" font-size="10.5" fill="var(--muted)">${nf(tot[vi], 1)} cm</text>`;
  });
  s += `<line x1="${xa - 6}" x2="${xb + cw + 6}" y1="${H + 8}" y2="${H + 8}" stroke="var(--muted)"/></svg>`;
  return s;
}

// ───────────────────────── minimapa ─────────────────────────
let MM = null;
function initMini() {
  const cv = $('#miniC'); const xs = [], zs = []; D.civs.forEach(c => c.tp.forEach(([x, z]) => { xs.push(x); zs.push(z); }));
  const pad = 140, x0 = Math.min(...xs) - pad, x1 = Math.max(...xs) + pad, z0 = Math.min(...zs) - pad, z1 = Math.max(...zs) + pad;
  const s = Math.min(cv.width / (x1 - x0), cv.height / (z1 - z0)), ox = (cv.width - (x1 - x0) * s) / 2, oz = (cv.height - (z1 - z0) * s) / 2;
  const W = p => p.map(([x, y]) => [x - CX, -(y - CY)]);
  const roads = CTX.roads.filter(r => /^(trunk|primary|secondary|tertiary)/.test(r.c)).map(r => W(r.p));
  MM = { x0, z0, s, ox, oz, roads, toC: (x, z) => [ox + (x - x0) * s, oz + (z - z0) * s], toW: (u, v) => [(u - ox) / s + x0, (v - oz) / s + z0] };
  cv.addEventListener('click', e => {
    const b = cv.getBoundingClientRect(); const [x, z] = MM.toW((e.clientX - b.left) * cv.width / b.width, (e.clientY - b.top) * cv.height / b.height);
    const off = camera.position.clone().sub(controls.target); const tgt = new THREE.Vector3(x, 0, z); flyTo(tgt.clone().add(off), tgt, 800);
  });
}
const _ray = new THREE.Raycaster(), _pl = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0), _hit = new THREE.Vector3();
function drawMini() {
  if (!MM || isMobile() || document.body.classList.contains('has-sel')) return;
  const cv = $('#miniC'), g = cv.getContext('2d'), cs = getComputedStyle(document.documentElement);
  g.clearRect(0, 0, cv.width, cv.height);
  g.lineCap = 'round'; g.lineJoin = 'round';
  g.strokeStyle = cs.getPropertyValue('--muted').trim() || '#888'; g.globalAlpha = .35; g.lineWidth = 2.2;
  for (const P of MM.roads) { g.beginPath(); P.forEach(([x, z], i) => { const [u, v] = MM.toC(x, z); i ? g.lineTo(u, v) : g.moveTo(u, v); }); g.stroke(); }
  g.globalAlpha = 1;
  for (const c of D.civs) {
    g.strokeStyle = civColor(c); g.lineWidth = c.id === S.sel ? 11 : 7;
    g.beginPath(); c.tp.forEach(([x, z], i) => { const [u, v] = MM.toC(x, z); i ? g.lineTo(u, v) : g.moveTo(u, v); }); g.stroke();
  }
  // huella de la cámara sobre el terreno
  const pts = [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([x, y]) => { _ray.setFromCamera(new THREE.Vector2(x, y), camera); const h = _ray.ray.intersectPlane(_pl, _hit); if (!h) { const d = _ray.ray.direction.clone().setY(0).normalize().multiplyScalar(4000); return [camera.position.x + d.x, camera.position.z + d.z]; } return [h.x, h.z]; });
  g.fillStyle = cs.getPropertyValue('--accent-soft').trim(); g.strokeStyle = cs.getPropertyValue('--accent').trim(); g.lineWidth = 2.5;
  g.beginPath(); pts.forEach(([x, z], i) => { const [u, v] = MM.toC(x, z); i ? g.lineTo(u, v) : g.moveTo(u, v); }); g.closePath(); g.fill(); g.stroke();
  const [tu, tv] = MM.toC(controls.target.x, controls.target.z); g.fillStyle = cs.getPropertyValue('--accent').trim(); g.beginPath(); g.arc(tu, tv, 5, 0, 7); g.fill();
}

// ───────────────────────── recorrido guiado (8 paradas calculadas desde los datos) ─────────────────────────
const tour = { on: false, i: 0, paused: false, t0: 0, dur: 14000, steps: [], focus: null, prev: null };
function tourSteps() {
  const C = D.civs, t = D.tot, dT = t.t4 - t.t0, top = f => C.slice().sort((a, b) => f(b) - f(a))[0];
  const a = top(c => c.delta), e = top(c => c.est[1] - c.est[0]), p = top(c => c.pnp), dn = C.filter(c => c.delta < 0);
  const ms = MATK.map(k => [k, D.mat[k][1] - D.mat[k][0]]).sort((x, y) => y[1] - x[1]);
  const r0 = C.reduce((s, c) => s + c.red[0], 0), r4 = C.reduce((s, c) => s + c.red[1], 0);
  const u0 = C.reduce((s, c) => s + c.redes.un.secas[0], 0), u4 = C.reduce((s, c) => s + c.redes.un.secas[1], 0);
  const avg = k => C.reduce((s, c) => s + c.est[k] * c.area, 0) / t.a;
  const g = {}; C.forEach(c => { (g[c.grupo] ||= { n: 0, v: 0 }); g[c.grupo].n++; g[c.grupo].v += c.tot4; });
  const n25 = C.filter(c => c.pnp > 25).length;
  return [
    { mode: 'costos', cmp: 'ambos', view: ['general', 52, -24], kick: 'El panorama', title: `27 frentes de obra: ${fMs(dT)} más`, text: `El presupuesto de obra de los 27 CIV pasa de <b>${fM(t.t0)}</b> (contrato) a <b>${fM(t.t4)}</b> (radicado el 01-09-2026): un alza de <b>${fP(dT / t.t0 * 100)}</b>. Cada volumen sólido es el valor actual; el contorno de vidrio, el del contrato.` },
    { mode: 'variacion', civ: a.id, kick: 'Dónde sube', title: `La mayor alza: ${a.nom} · ${a.tramo}`, text: `Sube <b>${fMs(a.delta)}</b> (${fP(a.dpct)}) y concentra el ${nf(a.delta / dT * 100)}% del aumento. <b>${C.length - dn.length} de ${C.length}</b> calles suben; solo ${dn.length} bajan${dn.length ? ` (${dn.map(c => esc(c.nom)).join(' y ')})` : ''}.` },
    { mode: 'materiales', cmp: 'ambos', view: ['sg5', 50, 28], kick: 'Por qué sube', title: '¿Qué materiales explican el aumento?', text: `Las <b>redes hidrosanitarias</b> suman ${fMs(ms[0][1])} (<b>${nf(ms[0][1] / dT * 100)}%</b> del aumento), seguidas por <b>${MATS[ms[1][0]].toLowerCase()}</b> (${fMs(ms[1][1])}) y <b>${MATS[ms[2][0]].toLowerCase()}</b> (${fMs(ms[2][1])}). En cada calle, la franja de alambre es el contrato y la sólida el presupuesto nuevo.` },
    { mode: 'redes', cmp: 'ambos', view: ['sg5', 66, 40], kick: 'Bajo tierra', title: 'Las redes casi se duplican', text: `El subsuelo pasa de <b>${fM(r0)}</b> a <b>${fM(r4)}</b> (${fMs(r4 - r0)}), el ${nf((r4 - r0) / dT * 100)}% del aumento. Las unidades de redes secas pasan de ${nf(u0)} a <b>${nf(u4)}</b>. El tubo de vidrio es lo contratado; el sólido, lo pedido ahora.` },
    { mode: 'estructural', cmp: 'ambos', civ: e.id, kick: 'El pavimento', title: `Estructura más gruesa en ${e.nom}`, text: `El espesor equivalente de ${esc(e.nom)} · ${esc(e.tramo)} pasa de <b>${nf(e.est[0])} a ${nf(e.est[1])} cm</b>. En promedio, ponderado por área, los 27 CIV van de ${nf(avg(0), 1)} a <b>${nf(avg(1), 1)} cm</b>.` },
    { mode: 'np', civ: p.id, kick: 'No previstos', title: `${fM(t.np)} en ítems no previstos`, text: `Son el <b>${nf(t.np / t.t4 * 100, 1)}%</b> del valor de obra en V4. En ${esc(p.nom)} · ${esc(p.tramo)} llegan al <b>${nf(p.pnp, 1)}%</b> del CIV, y ${n25} CIV superan el 25%.` },
    { mode: 'alcance', cmp: 'v4', view: ['general', 58, -8], kick: 'Qué está en juego', title: 'Tres grupos de calles', text: `<b>${g.ya_iniciados?.n || 0} ya iniciados</b> (${fM(g.ya_iniciados?.v || 0)}), <b>${g.por_iniciar?.n || 0} por iniciar</b> (${fM(g.por_iniciar?.v || 0)}) y <b>${g.no_alcanza?.n || 0} que “no alcanzan”</b> (${fM(g.no_alcanza?.v || 0)}), excluidos en la alternativa 2 del contratista.` },
    { sim: true, view: ['general', 54, -20], kick: 'El plazo', title: '¿Cabe la obra en 8 meses?', text: '' },
  ];
}
function tourStart() {
  $('#welcome').hidden = true; closePop(); openSheet(null);
  if (S.sel) selectCiv(null, false);
  tour.prev = { mode: S.mode, cmp: S.cmp, sim: SIM.on };
  tour.steps = tourSteps(); tour.on = true; tour.i = 0; tour.paused = false;
  document.body.classList.add('touring'); $('#tour').hidden = false;
  $('#tourDots').innerHTML = tour.steps.map((_, i) => `<i data-i="${i}" title="Parada ${i + 1}"></i>`).join('');
  controls.autoRotate = true; controls.autoRotateSpeed = -.3;
  tourGo(0);
}
function tourGo(i) {
  tour.i = clamp(i, 0, tour.steps.length - 1); const st = tour.steps[tour.i];
  tour.t0 = performance.now(); tour.elapsed = 0; tour.paused = false; tour.focus = null;
  SIM.playing && play(false);
  if (st.sim) {
    SIM.scope = 'oficial'; $('#simScope').value = 'oficial'; SIM.t = 0; simRun(); setSimOn(true); SIM.speed = 1.1; $('#simSpeed').value = '1';
    const r = SIM.res; st.text = `Con el Δ oficial de obra (${fM(r.total)}), el ritmo pedido (${fM(SIM.ritmo)}/mes) y ${SIM.fr} frentes, la simulación termina en el <b>mes ${nf(r.T, 1)}</b>${r.T > 8 ? ` (+${nf(r.T - 8, 1)})` : ''}. ${r.need && r.T > 8 ? `Para cumplir los 8 meses harían falta ≈ <b>${fM(r.need)}/mes</b>.` : ''} Mírela construirse, fase por fase.`;
    tour.dur = Math.max(14000, (r.tEnd / SIM.speed) * 1000 + 3000);
    setTimeout(() => { if (tour.on && tour.i === tour.steps.length - 1) play(true); }, 1400);
  } else {
    if (SIM.on) setSimOn(false);
    S.cmp = st.cmp || S.cmp; S.mode = st.mode; markModes(); applyVisibility(); buildCivs(true); tour.dur = 14000;
  }
  if (st.civ) { tour.focus = st.civ; applySel(); const c = byId[st.civ]; setTimeout(() => fitTo([c], 50, THREE.MathUtils.radToDeg(new THREE.Spherical().setFromVector3(camera.position.clone().sub(controls.target)).theta) + 25, 2200), 60); }
  else if (st.view) { applySel(); const [v, pol, az] = st.view; const list = v === 'sg5' ? D.civs.filter(c => c.sg === '5') : v === 'sg2' ? D.civs.filter(c => c.sg === '2') : D.civs; setTimeout(() => fitTo(list, pol, az, 2200), 60); }
  $('#tourStep').textContent = `${tour.i + 1} de ${tour.steps.length} · ${st.kick}`;
  $('#tourTitle').textContent = st.title; $('#tourText').innerHTML = st.text;
  $$('#tourDots i').forEach((d, k) => d.classList.toggle('on', k === tour.i));
  $('#tourNext').innerHTML = tour.i === tour.steps.length - 1 ? 'Terminar' : 'Siguiente<svg class="i" viewBox="0 0 24 24"><path d="M9 18l6-6-6-6"/></svg>';
  tourPause(false);
  const card = $('#tourCard'); card.style.animation = 'none'; card.offsetHeight; card.style.animation = '';
}
function tourPause(p) { const now = performance.now(); if (p && !tour.paused) tour.elapsed = now - tour.t0; if (!p && tour.paused) tour.t0 = now - (tour.elapsed || 0); tour.paused = p; $('#tourPlayIc').innerHTML = p ? '<path d="M8 5l11 7-11 7z" style="fill:currentColor;stroke:none"/>' : '<path d="M8 5v14M16 5v14"/>'; controls.autoRotate = tour.on && !p; }
function tourEnd() {
  if (!tour.on) return;
  tour.on = false; tour.focus = null; document.body.classList.remove('touring'); $('#tour').hidden = true; controls.autoRotate = false;
  if (SIM.playing) play(false);
  if (SIM.on) setSimOn(false);
  S.mode = tour.prev?.mode || 'costos'; S.cmp = 'ambos'; markModes(); applyVisibility(); buildCivs(true); applySel();
  setTimeout(() => preset('general', 1400), 50);
}
function tourTick(now) {
  if (!tour.on || tour.paused) return;
  const k = (now - tour.t0) / tour.dur; $('#tourBar').style.width = clamp(k, 0, 1) * 100 + '%';
  if (k >= 1) { if (tour.i < tour.steps.length - 1) tourGo(tour.i + 1); else { tourPause(true); $('#tourBar').style.width = '100%'; } }
}

// ───────────────────────── captura de imagen (PNG con etiquetas, título y leyenda) ─────────────────────────
async function capture() {
  renderFrame();
  const src = renderer.domElement, W = src.width, H = src.height, st = $('#stage'), sc = W / st.clientWidth;
  const cv = document.createElement('canvas'); cv.width = W; cv.height = H; const g = cv.getContext('2d');
  g.drawImage(src, 0, 0);
  const cs = getComputedStyle(document.documentElement), font = '"Inter", system-ui, sans-serif';
  const rr = (x, y, w, h, r) => { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); };
  const sr = st.getBoundingClientRect();
  // etiquetas visibles
  for (const c of D.civs) {
    const el = c.lbl.element; if (el.classList.contains('hid') || !el.isConnected) continue;
    const card = el.firstChild, b = card.getBoundingClientRect(), dot = el.lastChild.getBoundingClientRect();
    const x = (b.left - sr.left) * sc, y = (b.top - sr.top) * sc, w = b.width * sc, h = b.height * sc;
    g.globalAlpha = el.classList.contains('dim') ? .4 : 1;
    g.strokeStyle = cs.getPropertyValue('--ink2'); g.lineWidth = 1.5 * sc; g.beginPath(); g.moveTo(x + w / 2, y + h); g.lineTo((dot.left + dot.width / 2 - sr.left) * sc, (dot.top + dot.height / 2 - sr.top) * sc); g.stroke();
    g.fillStyle = getComputedStyle(card).backgroundColor; rr(x, y, w, h, 10 * sc); g.fill();
    g.fillStyle = getComputedStyle(card).getPropertyValue('--c') || cs.getPropertyValue('--accent'); g.fillRect(x, y + 4 * sc, 4 * sc, h - 8 * sc);
    const nmEl = card.querySelector('.nm'), vlEl = card.querySelector('.vl, .ph');
    g.fillStyle = cs.getPropertyValue('--ink'); g.font = `700 ${12 * sc}px ${font}`; g.fillText((nmEl?.firstChild?.textContent || c.nom).trim(), x + 12 * sc, y + 17 * sc);
    if (vlEl) { g.font = `800 ${13.5 * sc}px ${font}`; g.fillText([...vlEl.childNodes].map(n => n.textContent.trim()).filter(Boolean).join('  ').slice(0, 36), x + 12 * sc, y + 35 * sc); }
    g.globalAlpha = 1;
  }
  // banda de título
  const md = MODES.find(m => m.k === (SIM.on ? 'sim' : S.mode));
  const title = `Plano 3D · ${md.n}${md.cmp ? ' · ' + { v0: 'antes (V0)', v4: 'ahora (V4)', ambos: 'antes vs. ahora' }[S.cmp] : ''}${SIM.on ? ` · mes ${nf(SIM.t, 1)}` : ''}`;
  g.fillStyle = cs.getPropertyValue('--solid'); g.globalAlpha = .9; rr(16 * sc, 16 * sc, 560 * sc, 62 * sc, 14 * sc); g.fill(); g.globalAlpha = 1;
  g.fillStyle = cs.getPropertyValue('--ink'); g.font = `800 ${20 * sc}px ${font}`; g.fillText(title, 32 * sc, 44 * sc);
  g.fillStyle = cs.getPropertyValue('--muted'); g.font = `500 ${12 * sc}px ${font}`; g.fillText(`Contrato IDU 1752-2021 · Grupo 2 · 27 CIV · V0 ${fM(D.tot.t0)} → V4 ${fM(D.tot.t4)} · ${new Date().toLocaleDateString('es-CO')}`, 32 * sc, 64 * sc);
  // leyenda
  const rows = $$('#legend .lg-row').filter(r => r.querySelector('.sw')).slice(0, 10).map(r => [getComputedStyle(r.querySelector('.sw')).backgroundColor, r.querySelector('span:not(.v)')?.textContent || '']);
  if (rows.length) { const lh = 20 * sc, bw = 300 * sc, bh = (rows.length * 20 + 20) * sc, lx = 16 * sc, ly = H - bh - 16 * sc;
    g.fillStyle = cs.getPropertyValue('--solid'); g.globalAlpha = .9; rr(lx, ly, bw, bh, 12 * sc); g.fill(); g.globalAlpha = 1;
    rows.forEach(([col, txt], i) => { g.fillStyle = col === 'rgba(0, 0, 0, 0)' ? 'transparent' : col; g.fillRect(lx + 12 * sc, ly + 12 * sc + i * lh, 12 * sc, 12 * sc); if (col === 'rgba(0, 0, 0, 0)') { g.strokeStyle = cs.getPropertyValue('--ink2'); g.setLineDash([3 * sc, 2 * sc]); g.strokeRect(lx + 12 * sc, ly + 12 * sc + i * lh, 12 * sc, 12 * sc); g.setLineDash([]); } g.fillStyle = cs.getPropertyValue('--ink'); g.font = `500 ${12 * sc}px ${font}`; g.fillText(txt.slice(0, 44), lx + 32 * sc, ly + 22 * sc + i * lh); }); }
  g.fillStyle = cs.getPropertyValue('--muted'); g.font = `500 ${11 * sc}px ${font}`; g.textAlign = 'right'; g.fillText('Geometría © colaboradores de OpenStreetMap (ODbL) · three.js', W - 16 * sc, H - 16 * sc);
  cv.toBlob(b => { const a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = `plano3d_${SIM.on ? 'simulacion' : S.mode}_${new Date().toISOString().slice(0, 10)}.png`; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 800); toast('Imagen descargada: ' + a.download); }, 'image/png');
}

// ───────────────────────── interfaz ─────────────────────────
let sheet = null;
function openSheet(name) {
  if (!isMobile()) return;
  const map = { an: '#an', tl: '#tl', det: '#det', set: '#setPop' };
  if (sheet === 'set' && name !== 'set') setTimeout(() => { if (sheet !== 'set') $('#setPop').hidden = true; }, 360);
  Object.values(map).forEach(s => $(s).classList.remove('open'));
  if (name === 'set') $('#setPop').hidden = false;
  if (name && map[name] && !(name === 'det' && !S.sel)) { $(map[name]).classList.add('open'); if (name === 'tl') setTimeout(drawChart, 320); }
  sheet = name;
  $$('#mnav button').forEach(b => b.setAttribute('aria-pressed', b.dataset.sheet === name));
  updateMini();
}
function updateMini() { $('#miniSim').classList.toggle('on', isMobile() && SIM.on && sheet !== 'tl' && !tour.on); }
function toggleTl(open = !document.body.classList.contains('tl-open')) {
  if (isMobile()) { openSheet(open ? 'tl' : null); return; }
  document.body.classList.toggle('tl-open', open); $('#tlMore').setAttribute('aria-expanded', open); $('#tlChev').style.transform = open ? 'rotate(180deg)' : '';
  setTimeout(() => { drawChart(); dirty = true; }, 380);
}
function closePop() { $('#setPop').hidden = true; $('#btnSet').setAttribute('aria-pressed', 'false'); }
function toast(msg) { const t = $('#toast'); t.textContent = msg; t.classList.add('on'); clearTimeout(toast._t); toast._t = setTimeout(() => t.classList.remove('on'), 3000); }
function renderPals() {
  $('#pals').innerHTML = Object.entries(THEMES).map(([k, t]) => `<button class="pal" data-p="${k}" aria-pressed="${k === S.theme}" title="${esc(PAL_NOTE[k])}"><i style="background:linear-gradient(90deg,${t.swatch.map((c, i) => `${c} ${i * 20}% ${(i + 1) * 20}%`).join(',')})"></i>${t.n}</button>`).join('');
  $('#palNote').textContent = PAL_NOTE[S.theme];
}
function applyTheme(redraw = true) {
  document.documentElement.dataset.theme = S.theme;
  renderPals(); themeContext();
  if (redraw) drawChart();
  buildCivs(true); if (S.sel) renderDetail(); writeHash();
}
function setMode(k) {
  if (k === 'sim') { setSimOn(true); renderPanel(); if (isMobile()) openSheet('tl'); else toggleTl(true); return; }
  S.mode = k; if (SIM.on) { SIM.playing && play(false); SIM.on = false; $('#simOn').checked = false; }
  markModes(); applyVisibility(); buildCivs(true); writeHash(); updateMini();
  if (k === 'redes') { const sph = new THREE.Spherical().setFromVector3(camera.position.clone().sub(controls.target)); if (sph.phi < 1.05) { sph.phi = 1.12; flyTo(controls.target.clone().add(new THREE.Vector3().setFromSpherical(sph)), controls.target.clone(), 800); } }
}
function initUI() {
  $('#modes').innerHTML = MODES.map((m, i) => `<button class="tab" data-k="${m.k}" aria-pressed="false" title="${esc(m.n + ': ' + m.help)} (tecla ${i + 1})"><svg class="i" viewBox="0 0 24 24">${ICON[m.k]}</svg><span>${m.n}</span></button>`).join('');
  markModes();
  $('#modes').addEventListener('click', e => { const b = e.target.closest('.tab'); if (!b) return; setMode(b.dataset.k); b.scrollIntoView({ inline: 'nearest', block: 'nearest' }); });
  $('#cmp').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; S.cmp = b.dataset.v; buildCivs(true); writeHash(); });
  $('#pals').addEventListener('click', e => { const b = e.target.closest('.pal'); if (!b) return; S.theme = b.dataset.p; applyTheme(); });
  $('#qual').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; setQuality(b.dataset.q); writeHash(); });
  $('#rank').addEventListener('click', e => { const li = e.target.closest('li'); if (!li) return; selectCiv(li.dataset.id); });
  $('#rankMore').addEventListener('click', () => { S.rankAll = !S.rankAll; renderRank(); });
  $('#btnCsv').addEventListener('click', exportCsv);
  const tg = (id, key, fn) => { const el = $(id); el.checked = S[key]; el.addEventListener('change', () => { S[key] = el.checked; fn && fn(); dirty = true; }); };
  tg('#tLabels', 'labels'); tg('#tBldg', 'bldg', applyVisibility); tg('#tTrees', 'trees', applyVisibility); tg('#tRoads', 'roads', applyVisibility);
  tg('#tHall', 'hall', () => { refreshLabels(); renderLegend(); }); tg('#tMotion', 'motion');
  let exT; $('#rExag').addEventListener('input', e => { S.exag = +e.target.value; $('#oExag').textContent = nf(S.exag, 1) + '×'; cancelAnimationFrame(exT); exT = requestAnimationFrame(() => { if (SIM.on) SIM.res.k = 130 * S.exag / Math.max(1, ...SIM.res.jobs.map(j => j.tot)); buildCivs(false); }); });
  $$('#views button').forEach(b => b.addEventListener('click', () => preset(b.dataset.view)));
  $('#compass').addEventListener('click', () => { const sph = new THREE.Spherical().setFromVector3(camera.position.clone().sub(controls.target)); sph.theta = 0; flyTo(controls.target.clone().add(new THREE.Vector3().setFromSpherical(sph)), controls.target.clone(), 700); });
  $('#btnHelp').addEventListener('click', () => { $('#help').hidden = false; });
  $('#btnSet').addEventListener('click', e => { e.stopPropagation(); if (isMobile()) { openSheet(sheet === 'set' ? null : 'set'); return; } const open = $('#setPop').hidden; $('#setPop').hidden = !open; $('#btnSet').setAttribute('aria-pressed', open); });
  document.addEventListener('pointerdown', e => { if (!isMobile() && !$('#setPop').hidden && !e.target.closest('#setPop,#btnSet')) closePop(); });
  $('#btnFull').addEventListener('click', () => { if (document.fullscreenElement) document.exitFullscreen(); else document.documentElement.requestFullscreen?.().catch(() => toast('Pantalla completa no disponible')); });
  $('#btnShot').addEventListener('click', () => capture().catch(err => toast('No se pudo capturar: ' + err.message)));
  $('#btnTour').addEventListener('click', tourStart);
  $('#anToggle').addEventListener('click', () => { document.body.classList.remove('an-open'); setTimeout(() => dirty = true, 400); });
  $('#anOpen').addEventListener('click', () => { document.body.classList.add('an-open'); });
  $('#helpModes').innerHTML = MODES.map(m => `<li><b>${m.n}:</b> ${m.help}</li>`).join('');
  $('#helpNotes').innerHTML = D.meta.notas.map(n => `<li>${esc(n)}</li>`).join('') + `<li>Hay ${fM(D.meta.totales.v0_sin_reparto)} de V0 en renglones sin reparto por CIV que no se pueden ubicar en el plano; por eso el V0 del plano (${fM(D.tot.t0)}) es menor que el V0 del libro (${fM(D.meta.totales.v0_N688)}).</li><li>Escenario «Δ oficial»: el Δ de obra del libro (fila 688: ${fM(DOFI())}) repartido entre los CIV como el Δ del plano (${fM(DPOS())}).</li><li>Ritmo solicitado: $2.000M/mes = ${fM(D.meta.ritmo.obras_mensual)} de obra + ${fM(D.meta.ritmo.gestion_mensual)} de gestión (PMA-SST, diálogo, PMT). ${esc(D.meta.ritmo.nota_historico)}</li>`;
  document.addEventListener('click', e => { const b = e.target.closest('[data-close]'); if (!b) return; const w = b.dataset.close;
    if (w === 'help') $('#help').hidden = true;
    else if (w === 'det') { if (isMobile()) openSheet(null); else selectCiv(null); }
    else if (w === 'set') { closePop(); openSheet(null); }
    else openSheet(null);
  });
  $('#help').addEventListener('click', e => { if (e.target.id === 'help') $('#help').hidden = true; });
  $$('#mnav button').forEach(b => b.addEventListener('click', () => { const s = b.dataset.sheet; openSheet(sheet === s ? null : s); }));
  // bienvenida
  $('#wTour').addEventListener('click', () => { if ($('#wNoShow').checked) lsSet('p3d_welcome_off', '1'); tourStart(); });
  $('#wExplore').addEventListener('click', () => { if ($('#wNoShow').checked) lsSet('p3d_welcome_off', '1'); $('#welcome').hidden = true; });
  // recorrido
  $('#tourNext').addEventListener('click', () => { if (tour.i >= tour.steps.length - 1) tourEnd(); else tourGo(tour.i + 1); });
  $('#tourPrev').addEventListener('click', () => tourGo(tour.i - 1));
  $('#tourPlay').addEventListener('click', () => tourPause(!tour.paused));
  $('#tourExit').addEventListener('click', tourEnd);
  $('#tourDots').addEventListener('click', e => { const d = e.target.closest('i'); if (d) tourGo(+d.dataset.i); });
  // simulación
  $('#simPlay').addEventListener('click', () => play()); $('#miniPlay').addEventListener('click', () => play());
  $('#simReset').addEventListener('click', () => { SIM.t = 0; if (!SIM.on) setSimOn(true); simApply(); });
  $('#simOn').addEventListener('change', e => { setSimOn(e.target.checked); renderPanel(); });
  $('#simSpeed').addEventListener('change', e => { SIM.speed = +e.target.value; });
  $('#simT').addEventListener('input', e => { SIM.t = +e.target.value; if (!SIM.on) { setSimOn(true); renderPanel(); } simApply(); });
  $('#tlMore').addEventListener('click', () => toggleTl());
  const rerun = () => { simRun(); if (SIM.on) simApply(); renderPanel(); if (S.sel) renderDetail(); writeHash(); };
  $('#simScope').addEventListener('change', e => { SIM.scope = e.target.value; rerun(); });
  $('#simOrd').addEventListener('change', e => { SIM.ord = e.target.value; rerun(); });
  $('#simPace').addEventListener('change', e => { SIM.pace = e.target.value; $('#fldCustom').hidden = SIM.pace !== 'custom'; if (SIM.pace === 'pedido') SIM.ritmo = D.meta.ritmo.obras_mensual; if (SIM.pace === 'historico') SIM.ritmo = D.meta.ritmo.historico_mensual_aprox; if (SIM.pace === 'custom') SIM.ritmo = +$('#simRitmo').value * 1e6; $('#oRitmo').textContent = fM(SIM.ritmo); rerun(); });
  $('#simRitmo').addEventListener('input', e => { SIM.ritmo = +e.target.value * 1e6; $('#oRitmo').textContent = fM(SIM.ritmo); rerun(); });
  $('#simFr').addEventListener('input', e => { SIM.fr = +e.target.value; $('#oFr').textContent = SIM.fr; rerun(); });
  $('#simCap').addEventListener('input', e => { SIM.cap = +e.target.value * 1e6; $('#oCap').textContent = fM(SIM.cap); rerun(); });
  $('#simMov').addEventListener('input', e => { SIM.mov = +e.target.value; $('#oMov').textContent = nf(SIM.mov, 2).replace(/,?0+$/, '') + ' mes'; rerun(); });
  $$('.ctabs button').forEach(b => b.addEventListener('click', () => { SIM.chart = b.dataset.ch; $$('.ctabs button').forEach(x => x.setAttribute('aria-pressed', x === b)); drawChart(); }));
  const svg = $('#simChart');
  svg.addEventListener('pointermove', chartHover);
  svg.addEventListener('pointerleave', () => { $('#tip').classList.remove('on'); const hl = $('#hovL'); if (hl) hl.remove(); });
  svg.addEventListener('click', e => {
    const id = e.target.dataset && e.target.dataset.id; if (id) { selectCiv(id); return; }
    if (SIM.chart === 's' && CH) { const b = svg.getBoundingClientRect(), sx = svg.viewBox.baseVal.width / b.width; SIM.t = clamp(((e.clientX - b.left) * sx - CH.m.l) / CH.iw * CH.tMax, 0, SIM.res.tEnd); if (!SIM.on) { setSimOn(true); renderPanel(); } simApply(); }
  });
  new ResizeObserver(() => drawChart()).observe(svg);
  $('#simScope').value = SIM.scope; $('#simOrd').value = SIM.ord; $('#simFr').value = SIM.fr; $('#oFr').textContent = SIM.fr; $('#simCap').value = SIM.cap / 1e6; $('#oCap').textContent = fM(SIM.cap);
  $('#simMov').value = SIM.mov; $('#oMov').textContent = nf(SIM.mov, 2).replace(/,?0+$/, '') + ' mes';
  $('#rExag').value = S.exag; $('#oExag').textContent = nf(S.exag, 1) + '×';
  $('#simPace').value = SIM.pace; $('#fldCustom').hidden = SIM.pace !== 'custom';
  // interacción con el plano
  const cv = $('#gl'); let down = null, rafH = 0, nPtr = 0, multi = false;
  cv.addEventListener('pointerdown', e => { nPtr++; multi = nPtr > 1; down = { x: e.clientX, y: e.clientY, b: e.button }; });
  cv.addEventListener('pointercancel', () => { nPtr = Math.max(0, nPtr - 1); down = null; });
  cv.addEventListener('pointerup', e => {
    nPtr = Math.max(0, nPtr - 1);
    if (!down) return; const moved = Math.hypot(e.clientX - down.x, e.clientY - down.y) > 6; const b = down.b; down = null;
    if (moved || b !== 0 || multi || tour.on) return;
    const id = pickAt(e.clientX, e.clientY);
    if (id) selectCiv(id === S.sel ? null : id); else if (S.sel && !isMobile()) selectCiv(null);
  });
  cv.addEventListener('pointermove', e => {
    if (e.pointerType !== 'mouse' || down) return;
    cancelAnimationFrame(rafH); rafH = requestAnimationFrame(() => { const id = pickAt(e.clientX, e.clientY); cv.style.cursor = id ? 'pointer' : ''; setHover(id, e); });
  });
  cv.addEventListener('pointerleave', () => setHover(null, null));
  document.addEventListener('pointerover', e => { const t = e.target.closest && e.target.closest('[data-tip]'); if (!t) return; $('#tip').innerHTML = t.dataset.tip; const r = t.getBoundingClientRect(); placeTip(r.left, r.bottom + 4); });
  document.addEventListener('pointerout', e => { const t = e.target.closest && e.target.closest('[data-tip]'); if (t && !t.contains(e.relatedTarget)) $('#tip').classList.remove('on'); });
  document.addEventListener('touchstart', e => { if (!(e.target.closest && e.target.closest('[data-tip]'))) $('#tip').classList.remove('on'); }, { passive: true });
  document.addEventListener('keydown', e => {
    if (/INPUT|SELECT|TEXTAREA/.test(document.activeElement?.tagName) && e.key !== 'Escape') return;
    if (tour.on) { if (e.key === 'Escape') tourEnd(); else if (e.key === 'ArrowRight') tourGo(tour.i + 1); else if (e.key === 'ArrowLeft') tourGo(tour.i - 1); else if (e.key === ' ') { e.preventDefault(); $('#tourPlay').click(); } return; }
    if (e.key === 'Escape') { if (!$('#help').hidden) $('#help').hidden = true; else if (!$('#welcome').hidden) $('#welcome').hidden = true; else if (!$('#setPop').hidden) closePop(); else if (sheet) openSheet(null); else if (S.sel) selectCiv(null); return; }
    if (e.key === ' ') { if (/^(BUTTON|A)$/.test(document.activeElement?.tagName || '')) return; e.preventDefault(); play(); return; }
    if (e.key === 't' || e.key === 'T') { tourStart(); return; }
    const n = +e.key; if (n >= 1 && n <= MODES.length) setMode(MODES[n - 1].k);
  });
  addEventListener('resize', () => { updateMini(); if (!isMobile()) { ['#an', '#tl', '#det', '#setPop'].forEach(s => $(s).classList.remove('open')); sheet = null; } drawMini(); });
  initMini();
  if (SIM.on) { $('#simOn').checked = true; if (!isMobile()) toggleTl(true); }
}
function pickAt(x, y) {
  const b = $('#gl').getBoundingClientRect(); ptr.set((x - b.left) / b.width * 2 - 1, -(y - b.top) / b.height * 2 + 1);
  ray.setFromCamera(ptr, camera); const hit = ray.intersectObjects(pick, false)[0];
  return hit ? hit.object.userData.id : null;
}
function exportCsv() {
  const head = ['CIV', 'Subgrupo', 'Nomenclatura', 'Tramo', 'Grupo_Hoja1', 'Longitud_m', 'Ancho_m', 'Area_m2', 'V0', 'V4', 'Delta', 'Delta_pct', 'NP_V4', 'NP_pct', 'V4_por_m2', ...MATK.flatMap(k => [`${k}_V0`, `${k}_V4`]), ...CAPK.flatMap(k => [`${k}_cm_V0`, `${k}_cm_V4`]), 'hidro_ml_V0', 'hidro_ml_V4', 'secas_un_V0', 'secas_un_V4', 'andenes_m2_V0', 'andenes_m2_V4', 'Hallazgos'];
  const num = (v, d = 0) => (+v || 0).toFixed(d).replace('.', ',');
  const rows = D.civs.map(c => [c.id, c.sg, c.nom, c.tramo, GRUPON[c.grupo] || '', num(c.longitud, 2), num(c.ancho, 2), num(c.area, 2), c.tot0, c.tot4, c.delta, num(c.dpct, 2), c.np4, num(c.pnp, 2), Math.round(c.m2[1]), ...MATK.flatMap(k => [c.v0[k] || 0, c.v4[k] || 0]), ...CAPK.flatMap(k => [num(c.estructura[k]?.cm0, 1), num(c.estructura[k]?.cm4, 1)]), num(c.redes.ml.hidro[0], 1), num(c.redes.ml.hidro[1], 1), num(c.redes.un.secas[0], 1), num(c.redes.un.secas[1], 1), num(c.andenM2[0], 1), num(c.andenM2[1], 1), (c.hallazgos || []).map(h => h.id).join(' ')]);
  const csv = '﻿' + [head, ...rows].map(r => r.map(v => /[;"\n]/.test(String(v)) ? `"${String(v).replace(/"/g, '""')}"` : v).join(';')).join('\r\n');
  const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' })); a.download = 'plano3d_27_civ_v0_v4.csv'; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  toast('CSV descargado: 27 CIV × ' + head.length + ' columnas');
}

// ───────────────────────── enlace compartible (estado en el #hash) ─────────────────────────
function readHash() {
  const h = new URLSearchParams(location.hash.slice(1)); let any = false;
  const m = h.get('m'); if (m && MODES.some(x => x.k === m && x.k !== 'sim')) { S.mode = m; any = true; }
  const c = h.get('c'); if (['v0', 'v4', 'ambos'].includes(c)) S.cmp = c;
  const p = h.get('p'); if (p && THEMES[p]) S.theme = p;
  const v = h.get('civ'); if (v) { S.sel = v; any = true; }
  if (h.get('sim') === '1') { SIM.on = true; any = true; }
  const t = parseFloat(h.get('t')); if (!isNaN(t)) SIM.t = t;
  const sc = h.get('esc'); if (['oficial', 'delta', 'pend', 'v4'].includes(sc)) SIM.scope = sc;
  const cp = parseInt(h.get('cap')); if (cp >= 100 && cp <= 2000) SIM.cap = cp * 1e6;
  const o = h.get('ord'); if (['grupo', 'valor', 'sg', 'norte'].includes(o)) SIM.ord = o;
  const f = parseInt(h.get('fr')); if (f >= 1 && f <= 10) SIM.fr = f;
  if (h.get('ritmo') === 'historico') SIM.pace = 'historico';
  if (h.get('vista') === 'planta') S.view = 'planta';
  const q = h.get('q'); if (['alta', 'media', 'baja'].includes(q)) { S.q = q; S.qManual = true; }
  if (h.get('mo') === '0') S.motion = false;
  return any;
}
let hashT;
function writeHash() {
  clearTimeout(hashT); hashT = setTimeout(() => {
    const o = { m: S.mode, c: S.cmp, p: S.theme }; if (S.sel) o.civ = S.sel;
    if (SIM.on) Object.assign(o, { sim: 1, t: SIM.t.toFixed(1), esc: SIM.scope, ord: SIM.ord, fr: SIM.fr, cap: Math.round(SIM.cap / 1e6), ...(SIM.pace === 'historico' ? { ritmo: 'historico' } : {}) });
    if (S.qManual) o.q = S.q;
    try { history.replaceState(null, '', '#' + new URLSearchParams(o).toString()); } catch (_) {}
  }, 250);
}

// ───────────────────────── bucle de render ─────────────────────────
let last = performance.now(), lastDecl = 0, lastAmb = 0, lastMini = 0;
const perf = { samples: [], downgraded: 0 };
function renderFrame() {
  sky.position.copy(camera.position);
  if (composer) composer.render(); else renderer.render(scene, camera);
}
function loop(now) {
  requestAnimationFrame(loop);
  const dt = Math.min(.1, (now - last) / 1000); last = now;
  if (anims.length) { anims = anims.filter(a => { const t = clamp((now - a.t0) / a.dur, 0, 1); if (now >= a.t0) a.f(t); return t < 1; }); dirty = true; }
  if (SIM.playing && SIM.res) {
    SIM.t = Math.min(SIM.res.tEnd, SIM.t + dt * SIM.speed);
    simApply();
    if (SIM.t >= SIM.res.tEnd) { play(false); if (!tour.on) toast(SIM.res.T <= 8 ? `Escenario completo en el mes ${nf(SIM.res.T, 1)}: cabe en los 8 meses.` : `Escenario completo en el mes ${nf(SIM.res.T, 1)}: ${nf(SIM.res.T - 8, 1)} meses después del plazo.`); writeHash(); }
  }
  tourTick(now);
  if (SIM.on) { const k = .55 + .45 * Math.sin(now / 180); let any = false; for (const c of D.civs) if (c.beam?.visible) { c.beam.material.opacity = .45 + .45 * k; any = true; } if (any) dirty = true; }
  const ambient = S.motion && S.q !== 'baja' && !document.hidden && !matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (ambient) { uTime.value = now / 1000; if (now - lastAmb > 40) { dirty = true; lastAmb = now; } }
  if (controls.update()) dirty = true;
  if (!dirty) return;
  dirty = false;
  if (perf.lastR && now - perf.lastR < 400) autoQuality(now - perf.lastR); perf.lastR = now;
  renderFrame(); lblR.render(scene, camera);
  if (needMeasure) measureLabels();
  if (now - lastDecl > 60 || !SIM.playing) { declutter(); lastDecl = now; }
  if (now - lastMini > 120) { drawMini(); lastMini = now; }
  hud();
}
// Si el equipo no alcanza a dibujar con fluidez, se baja un nivel de calidad (solo si el usuario no la eligió)
function autoQuality(ms) {
  if (S.qManual || perf.downgraded >= 2) return;
  perf.samples.push(ms); if (perf.samples.length < 40) return;
  const avg = perf.samples.reduce((a, b) => a + b, 0) / perf.samples.length; perf.samples = [];
  if (avg > 55 && S.q !== 'baja') { perf.downgraded++; setQuality(S.q === 'alta' ? 'media' : 'baja', false); toast(`Calidad ajustada a «${S.q === 'media' ? 'Media' : 'Básica'}» para mantener la fluidez (Ajustes → Calidad).`); }
}
function hud() {
  const az = controls.getAzimuthalAngle();
  $('#compass svg').style.transform = `rotate(${az}rad)`;
  const st = $('#stage'), d = camera.position.distanceTo(controls.target), mpp = 2 * d * Math.tan(THREE.MathUtils.degToRad(camera.fov) / 2) / st.clientHeight;
  const L = [10, 20, 50, 100, 200, 500, 1000].find(l => l / mpp >= 60) || 1000;
  $('#scaleTxt').textContent = L >= 1000 ? nf(L / 1000) + ' km' : L + ' m'; $('#scaleBar').style.width = Math.round(L / mpp) + 'px';
  if (scene.fog) { scene.fog.near = d * .95 + 500; scene.fog.far = d * 2.6 + 2200; }
  const lod = d > (isMobile() ? 1200 : 1750) ? 'min' : d > (isMobile() ? 600 : 800) ? 'mid' : 'full';
  const lb = $('#lbls'); if (lb.dataset.lod !== lod) { lb.dataset.lod = lod; D.civs.forEach(c => { c.lw = c.lbl.element.offsetWidth; c.lh = c.lbl.element.offsetHeight; }); }
}
