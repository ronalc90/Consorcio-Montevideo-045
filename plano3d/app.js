// Plano 3D · antes (V0) vs. ahora (V4) · Contrato IDU 1752-2021, Grupo 2 (27 CIV)
// three.js r170 + CSS2DRenderer (etiquetas flotantes) + MapControls. Datos: datos/plano3d_datos.json y datos/contexto.json
// (generados por scripts/generar_plano3d.py). Geometría © colaboradores de OpenStreetMap (ODbL).
import * as THREE from 'three';
import { MapControls } from 'three/addons/controls/MapControls.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

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
const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
const easeOut = t => 1 - Math.pow(1 - t, 3);

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
const THEMES = {
  noche: { n: 'Noche', dark: true, fog: '#161615', ground: '#171716', block: '#20201e', park: '#1b271c', road: '#2d2d2a', roadMajor: '#393936', path: '#252523', rail: '#56554f', bldg: '#2b2b29', bldgEdge: '#45443f', bldgOp: 1, bEdges: false, grid: null, foot: '#33332f', footLine: '#7d7c75', ghost: '#f4f3ee', edge: '#ffffff', edgeOp: .16, sky: '#dfe7f2', gnd: '#6b6660', ...roles(REF_D, '#77766f'), seq: ['#184f95', '#3987e5', '#b7d3f6'], div: ['#86b6ef', '#3a3a37', '#f07b79'], np: ['#6b3517', '#d95926', '#f6b48c'], swatch: ['#1a1a19', REF_D.blue, REF_D.orange, REF_D.green, REF_D.red] },
  claro: { n: 'Claro', dark: false, fog: '#efeee9', ground: '#fcfcfb', block: '#efeee9', park: '#dfead6', road: '#e2e1db', roadMajor: '#d3d2cb', path: '#eae9e4', rail: '#9c9a93', bldg: '#e6e5df', bldgEdge: '#c3c2b7', bldgOp: 1, bEdges: false, grid: null, foot: '#d8d7d0', footLine: '#898781', ghost: '#0b0b0b', edge: '#000000', edgeOp: .13, sky: '#ffffff', gnd: '#b9b4a8', ...roles(REF_L, '#898781'), seq: ['#b7d3f6', '#3987e5', '#104281'], div: ['#184f95', '#e9e8e3', '#b32b2a'], np: ['#f6c3a5', '#eb6834', '#8c2f0c'], swatch: ['#fcfcfb', REF_L.blue, REF_L.orange, REF_L.green, REF_L.red] },
  azul: { n: 'Plano azul', dark: true, fog: '#0f2b47', ground: '#0f2740', block: '#12304e', park: '#113a4a', road: '#0b2136', roadMajor: '#091b2e', path: '#11304e', rail: '#7fa7cf', bldg: '#16395c', bldgEdge: '#8cb8e6', bldgOp: .32, bEdges: true, grid: '#23507c', foot: '#18406a', footLine: '#b8d8ff', ghost: '#e2f1ff', edge: '#e2f1ff', edgeOp: .3, sky: '#dcecff', gnd: '#10233a', ...roles(REF_D, '#7f95ad'), seq: ['#1f4f80', '#4f95dd', '#e6f3ff'], div: ['#8cc4ff', '#2a4a6c', '#ff8a80'], np: ['#6a3f25', '#e07a3f', '#ffd2b0'], swatch: ['#0f2740', REF_D.blue, REF_D.orange, REF_D.green, REF_D.red] },
  contraste: { n: 'Alto contraste', dark: false, fog: '#ffffff', ground: '#ffffff', block: '#f1f1f1', park: '#e2efe2', road: '#d4d4d4', roadMajor: '#bcbcbc', path: '#e4e4e4', rail: '#000000', bldg: '#fafafa', bldgEdge: '#000000', bldgOp: 1, bEdges: true, grid: null, foot: '#e0e0e0', footLine: '#000000', ghost: '#000000', edge: '#000000', edgeOp: .8, sky: '#ffffff', gnd: '#a0a0a0',
    mat: { hidro: OKI.blue, secas: OKI.yellow, tierras: OKI.sky, estab: OKI.vermillion, granular: OKI.orange, anden: OKI.green, losa: OKI.violet, asfalto: OKI.purple, otros: '#6b6b6b' },
    fase: { tierras: OKI.sky, redes: OKI.blue, estructura: OKI.vermillion, carpeta: OKI.violet, espacio: OKI.green, acabados: '#6b6b6b' },
    capa: { estab: OKI.vermillion, subbase: OKI.blue, base: OKI.orange, losa: OKI.violet, asfalto: OKI.purple },
    grupo: { ya_iniciados: OKI.vermillion, por_iniciar: OKI.sky, no_alcanza: OKI.violet },
    seq: ['#bcdcf0', '#0072b2', '#002a4a'], div: ['#0072b2', '#eeeeee', '#d55e00'], np: ['#f5cf8a', '#e69f00', '#7a4a00'], swatch: ['#ffffff', OKI.blue, OKI.vermillion, OKI.green, '#000000'] },
  real: { n: 'Realista', dark: false, fog: '#e2ded3', ground: '#d6d2c5', block: '#cbc5b4', park: '#a8be8e', road: '#8e8d88', roadMajor: '#7b7a75', path: '#bdb7a8', rail: '#5b544a', bldg: '#ece6d9', bldgEdge: '#b7ae9c', bldgOp: 1, bEdges: false, grid: null, foot: '#a3a29b', footLine: '#4d4a44', ghost: '#2b2924', edge: '#000000', edgeOp: .12, sky: '#fffaf0', gnd: '#8f877a', figurative: true,
    mat: { hidro: '#2e7dbf', secas: '#e3a21a', tierras: '#8b5e3c', estab: '#6f6258', granular: '#c2a36b', anden: '#c7704f', losa: '#bdbab0', asfalto: '#3a3a3c', otros: '#f1cf3f' },
    fase: { tierras: '#8b5e3c', redes: '#2e7dbf', estructura: '#c2a36b', carpeta: '#3a3a3c', espacio: '#c7704f', acabados: '#f1cf3f' },
    capa: { estab: '#6f6258', subbase: '#dbc9a1', base: '#b08d57', losa: '#c9c7be', asfalto: '#333335' },
    grupo: { ya_iniciados: REF_L.blue, por_iniciar: REF_L.orange, no_alcanza: REF_L.aqua },
    seq: ['#b7d3f6', '#3987e5', '#104281'], div: ['#184f95', '#efece4', '#b32b2a'], np: ['#f6c3a5', '#eb6834', '#8c2f0c'], swatch: ['#d6d2c5', '#3a3a3c', '#bdbab0', '#c2a36b', '#c7704f'] },
};
const PAL_NOTE = {
  noche: 'Fondo oscuro. Colores de datos validados para daltonismo (ΔE ≥ 8 entre vecinos).',
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
  { k: 'costos', n: 'Costos', h: 'Valor de obra por CIV', cmp: true, help: 'Altura = valor de obra del CIV con AIU. Color = costo por m² (más intenso = más caro por m²). En “Ambos” el volumen sólido es V4 y el contorno de vidrio es V0.' },
  { k: 'variacion', n: 'Variación', h: 'Δ V4 − V0', cmp: false, help: 'Altura = tamaño del cambio en pesos. Color divergente: rojo = sube, azul = baja, gris = sin cambio (intensidad = % de cambio).' },
  { k: 'estructural', n: 'Estructural', h: 'Capas del pavimento', cmp: true, help: 'Capas de la estructura con su espesor equivalente (m³ del CIV ÷ área), exagerado en vertical. En “Ambos” la franja de alambre es V0 y la sólida V4.' },
  { k: 'materiales', n: 'Materiales', h: 'Costo por material', cmp: true, help: 'Columna apilada por material; altura total = valor del CIV. En “Ambos” la franja de alambre es V0 y la sólida V4, lado a lado.' },
  { k: 'redes', n: 'Redes', h: 'Subsuelo', cmp: true, help: 'Vista del subsuelo: un tubo por tipo de red (hidrosanitaria y seca). Grosor ∝ valor. En “Ambos” el tubo de vidrio es V0.' },
  { k: 'np', n: 'No previstos', h: 'Ítems NP en V4', cmp: false, help: 'Volumen sólido = valor de los ítems no previstos (NP) del CIV en V4; contorno = total V4. Color = % del CIV que es NP.' },
  { k: 'alcance', n: 'Alcance', h: 'Grupos de la Hoja1', cmp: true, help: 'Color = grupo del CIV en la Hoja1 del contratista: ya iniciados, por iniciar o “no alcanza” (excluidos en la alternativa 2). Altura = valor.' },
  { k: 'sim', n: 'Simulación', h: 'Avance por plazos', cmp: false, help: 'Obra que se construye mes a mes: cada CIV levanta sus fases (tierras → redes → estructura → carpeta → andenes → acabados) al ritmo elegido.' },
];

// ───────────────────────── estado ─────────────────────────
const S = { mode: 'costos', cmp: 'ambos', theme: 'noche', exag: 1, labels: true, bldg: true, roads: true, hall: true, shadow: !isMobile(), sel: null, hover: null, view: 'general' };
const SIM = { on: false, playing: false, t: 0, speed: .5, scope: 'oficial', pace: 'pedido', ritmo: 0, fr: 4, cap: 500e6, mov: .5, ord: 'valor', chart: 's', res: null };
const T = () => THEMES[S.theme];

// ───────────────────────── acceso (misma sesión que la aplicación principal) ─────────────────────────
let authed = false;
try { authed = sessionStorage.getItem('auth') === 'true'; } catch (_) { authed = false; }
if (!authed) { $('#loading').hidden = true; $('#gate').hidden = false; }
else boot().catch(e => fail('Error inesperado: ' + (e && e.message || e)));

function fail(msg) { $('#loading').hidden = true; $('#err').hidden = false; $('#errMsg').textContent = msg; console.error(msg); }

// ───────────────────────── arranque ─────────────────────────
let D, CTX, byId, CX, CY, renderer, scene, camera, controls, lblR, hemi, sun, CG, CM = {}, civG = null, pick = [], dirty = true, anims = [], bldgMesh, bldgEdges, grid, subGrid, roadLbls = [], edgeMatShared = null;
const ray = new THREE.Raycaster(), ptr = new THREE.Vector2();

async function boot() {
  try {
    const get = u => fetch(u, { cache: 'no-cache' }).then(r => { if (!r.ok) throw new Error(u + ' → HTTP ' + r.status); return r.json(); });
    [D, CTX] = await Promise.all([get('datos/plano3d_datos.json'), get('datos/contexto.json')]);
  } catch (e) { fail('No se pudieron leer los datos del plano (' + e.message + '). Si abrió el archivo desde el disco, sírvalo con un servidor web (GitHub Pages o «python -m http.server»).'); return; }
  try {
    const t = document.createElement('canvas'); if (!(t.getContext('webgl2') || t.getContext('webgl'))) throw new Error('sin WebGL');
  } catch (_) { fail('Este navegador no tiene WebGL activo, necesario para el plano 3D. Pruebe con Chrome, Edge, Firefox o Safari recientes.'); return; }
  readHash();
  if (!location.hash.includes('p=')) S.theme = matchMedia('(prefers-color-scheme: light)').matches ? 'claro' : 'noche';
  SIM.ritmo = SIM.pace === 'historico' ? D.meta.ritmo.historico_mensual_aprox : D.meta.ritmo.obras_mensual;
  prepData();
  initScene();
  buildContext();
  initUI();
  simRun();
  applyTheme(false);
  const target = S.sel && byId[S.sel] ? [byId[S.sel]] : D.civs;
  fitTo(target, S.view === 'planta' ? .001 : 55, S.view === 'planta' ? 0 : -16, 0);
  if (S.sel) selectCiv(S.sel, false);
  requestAnimationFrame(loop);
  setTimeout(() => { $('#loading').hidden = true; }, 150);
}

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
    c.mats = []; c.lk = '';
  }
  const t = { t0: 0, t4: 0, np: 0 }; D.civs.forEach(c => { t.t0 += c.tot0; t.t4 += c.tot4; t.np += c.np4; }); D.tot = t;
}

// ───────────────────────── escena ─────────────────────────
function initScene() {
  const canvas = $('#gl');
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, isMobile() ? 1.75 : 2));
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(38, 1, 5, 9000);
  controls = new MapControls(camera, canvas);
  Object.assign(controls, { enableDamping: true, dampingFactor: .09, screenSpacePanning: false, minDistance: 60, maxDistance: 4200, zoomToCursor: true, maxPolarAngle: THREE.MathUtils.degToRad(84) });
  controls.addEventListener('change', () => { dirty = true; });
  hemi = new THREE.HemisphereLight(0xffffff, 0x444444, 1.9);
  sun = new THREE.DirectionalLight(0xffffff, 1.7);
  sun.position.set(-620, 1150, 520); sun.target.position.set(0, 0, 0);
  sun.castShadow = S.shadow; sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -1150, right: 1150, top: 1150, bottom: -1150, near: 200, far: 3200 });
  sun.shadow.bias = -0.0005; sun.shadow.normalBias = .8;
  scene.add(hemi, sun, sun.target);
  lblR = new CSS2DRenderer({ element: $('#lbls') });
  const ro = new ResizeObserver(resize); ro.observe($('#stage')); resize();
}
function resize() {
  const st = $('#stage'), w = st.clientWidth, h = st.clientHeight;
  renderer.setSize(w, h, false); lblR.setSize(w, h);
  camera.aspect = w / h; camera.updateProjectionMatrix(); dirty = true;
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
// Atributo aT = distancia recorrida normalizada (0→1): lo usa el sombreador para "construir" el tramo en la simulación.
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
  const g = new THREE.TubeGeometry(path, Math.max(6, (V.length - 1) * 8), r, 18, false);
  const uv = g.getAttribute('uv'); const a = new Float32Array(uv.count); for (let i = 0; i < uv.count; i++) a[i] = uv.getX(i);
  g.setAttribute('aT', new THREE.BufferAttribute(a, 1));
  return g;
}
function progMat(color, o = {}) {
  const op = o.opacity ?? 1;
  const m = new THREE.MeshStandardMaterial({ color, roughness: .6, metalness: .04, transparent: op < 1, opacity: op, depthWrite: op >= 1, side: o.double ? THREE.DoubleSide : THREE.FrontSide });
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
function disposeTree(o) { o.traverse(x => { if (x.geometry) x.geometry.dispose(); if (x.material) (Array.isArray(x.material) ? x.material : [x.material]).forEach(m => m.dispose()); }); }

// ───────────────────────── contexto urbano (OpenStreetMap) ─────────────────────────
function buildContext() {
  CG = new THREE.Group(); scene.add(CG);
  const th = T();
  const flat = (color, off) => new THREE.MeshLambertMaterial({ color, polygonOffset: true, polygonOffsetFactor: -off, polygonOffsetUnits: -off * 2 });
  const gg = new THREE.PlaneGeometry(7000, 7000); gg.rotateX(-Math.PI / 2);
  CM.ground = new THREE.MeshLambertMaterial({ color: th.ground });
  const ground = new THREE.Mesh(gg, CM.ground); ground.position.y = -.4; ground.receiveShadow = true; ground.renderOrder = -2; CG.add(ground);
  const shapeGeo = (pts, y) => {
    const p = pts.slice(); if (p.length > 2 && p[0][0] === p.at(-1)[0] && p[0][1] === p.at(-1)[1]) p.pop();
    const g = new THREE.ShapeGeometry(new THREE.Shape(p.map(([x, yy]) => new THREE.Vector2(x - CX, yy - CY))));
    g.rotateX(-Math.PI / 2); g.translate(0, y, 0); g.deleteAttribute('uv'); return g;
  };
  const merged = (list, mat, y, name) => { const gs = list.filter(g => g && g.getAttribute('position').count); if (!gs.length) return null; const m = new THREE.Mesh(mergeGeometries(gs, false), mat); m.receiveShadow = true; m.name = name; gs.forEach(g => g.dispose()); CG.add(m); return m; };
  CM.block = flat(th.block, 1); merged(CTX.blocks.map(b => shapeGeo(b.p, 0)), CM.block, 0, 'blocks');
  CM.park = flat(th.park, 2); merged(CTX.parks.map(b => shapeGeo(b.p, .05)), CM.park, 0, 'parks');
  const W = p => p.map(([x, y]) => [x - CX, -(y - CY)]);
  const major = /^(trunk|primary|secondary)/, path = /^(footway|cycleway|steps|path|pedestrian)/;
  const rd = { major: [], minor: [], path: [] };
  for (const r of CTX.roads) { if (r.p.length < 2) continue; const k = major.test(r.c) ? 'major' : path.test(r.c) ? 'path' : 'minor'; const w = r.w || 6; rd[k].push(ribbon(W(r.p), -w / 2, w / 2, .1, .1)); }
  CM.path = flat(th.path, 3); merged(rd.path, CM.path, 0, 'paths');
  CM.road = flat(th.road, 4); merged(rd.minor, CM.road, 0, 'roads');
  CM.roadMajor = flat(th.roadMajor, 5); merged(rd.major, CM.roadMajor, 0, 'major');
  CM.rail = flat(th.rail, 6); merged(CTX.rails.filter(r => r.p.length > 1).map(r => ribbon(W(r.p), -1.2, 1.2, .15, .15)), CM.rail, 0, 'rails');
  // edificios extruidos (altura OSM: niveles × 3,2 m o altura típica por uso)
  const bg = [];
  for (const b of CTX.buildings) {
    const p = b.p.slice(); if (p.length > 2 && p[0][0] === p.at(-1)[0] && p[0][1] === p.at(-1)[1]) p.pop(); if (p.length < 3) continue;
    const g = new THREE.ExtrudeGeometry(new THREE.Shape(p.map(([x, y]) => new THREE.Vector2(x - CX, y - CY))), { depth: b.h || 7, bevelEnabled: false });
    g.rotateX(-Math.PI / 2); g.deleteAttribute('uv'); bg.push(g);
  }
  CM.bldg = new THREE.MeshStandardMaterial({ color: th.bldg, roughness: .9, metalness: 0, transparent: th.bldgOp < 1, opacity: th.bldgOp, depthWrite: th.bldgOp >= 1 });
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
  const main = /Avenida|Calle 1[3-9]|Calle 2[0-4]|Carrera 6[0-9]|TransMilenio/;
  for (const [n, arr] of Object.entries(byName)) {
    const lens = arr.map(p => cumLen(p).at(-1)); const tot = lens.reduce((a, b) => a + b, 0);
    if (tot < 240 && !main.test(n)) continue;
    if (n === 'TransMilenio') continue;
    const i = lens.indexOf(Math.max(...lens)); const P = arr[i]; const cum = cumLen(P); const m = at(P, cum, cum.at(-1) / 2);
    const el = document.createElement('div'); el.className = 'rl'; el.textContent = short(n);
    const o = new CSS2DObject(el); o.position.set(m[0], 2, m[1]); o.center.set(.5, .5); scene.add(o);
    roadLbls.push({ o, el, pri: tot, w: 0, h: 0 });
  }
}
function themeContext() {
  const th = T();
  for (const k of ['ground', 'block', 'park', 'road', 'roadMajor', 'path', 'rail']) CM[k].color.set(th[k]);
  CM.bldg.color.set(th.bldg); CM.bldg.opacity = th.bldgOp; CM.bldg.transparent = th.bldgOp < 1; CM.bldg.depthWrite = th.bldgOp >= 1; CM.bldg.needsUpdate = true;
  CM.bldgEdge.color.set(th.bldgEdge);
  grid.visible = !!th.grid; if (th.grid) { grid.material.color.set(th.grid); }
  subGrid.material.color.set(th.dark ? '#6d8fb3' : '#8a8a8a');
  scene.fog = new THREE.Fog(th.fog, 1700, 4600);
  hemi.color.set(th.sky); hemi.groundColor.set(th.gnd);
  hemi.intensity = th.dark ? 2.35 : 2.2; sun.intensity = th.dark ? 1.3 : 1.45;
  applyVisibility();
}
function applyVisibility() {
  const under = !SIM.on && S.mode === 'redes', th = T();
  bldgMesh.visible = S.bldg && !under; bldgEdges.visible = S.bldg && !under && th.bEdges;
  for (const k of ['ground', 'block', 'park', 'road', 'roadMajor', 'path', 'rail']) { const m = CM[k]; const want = under ? (th.dark ? .14 : .2) : 1; if (m.opacity !== want) { m.opacity = want; m.transparent = want < 1; m.depthWrite = want >= 1; m.needsUpdate = true; } }
  subGrid.visible = under;
  roadLbls.forEach(r => { r.o.visible = S.roads; });
  sun.castShadow = S.shadow;
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
    npmax: Math.max(...c.map(x => x.np4)),
  };
}
const seqC = v => ramp(T().seq, (v - K.m2min) / ((K.m2max - K.m2min) || 1));
const divC = p => ramp(T().div, .5 + .5 * clamp(p / (K.dmax || 1), -1, 1));
const npC = p => ramp(T().np, p / (K.pmax || 1));
function civColor(c) { // color de identidad del CIV en el modo actual (barra de la etiqueta, ranking)
  if (SIM.on) { const j = SIM.res?.byId[c.id]; if (!j) return T().footLine; const ph = curPhase(j, SIM.t); return ph ? T().fase[ph.k] : (SIM.t >= j.e ? T().fase.espacio : T().footLine); }
  switch (S.mode) {
    case 'costos': return seqC(c.m2[S.cmp === 'v0' ? 0 : 1]);
    case 'variacion': return divC(c.dpct);
    case 'np': return npC(c.pnp);
    case 'alcance': return T().grupo[c.grupo] || T().footLine;
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
  g.add(mesh); c.mats.push(m); pick.push(mesh);
  if (o.edges !== false && T().edgeOp > 0) { const e = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 25), edgeMat()); e.raycast = () => {}; g.add(e); }
  return mesh;
}
function addWire(c, g, geo, color) {
  const f = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color, transparent: true, opacity: T().dark ? .2 : .24, depthWrite: false }));
  f.userData.id = c.id; g.add(f); pick.push(f); (c.gm ||= []).push(f.material);
  const e = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 25), new THREE.LineBasicMaterial({ color, transparent: true, opacity: .95 }));
  e.raycast = () => {}; g.add(e); c.gm.push(e.material);
}
function addGhost(c, g, geo) {
  const th = T();
  const f = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: th.ghost, transparent: true, opacity: th.dark ? .07 : .05, depthWrite: false, side: THREE.DoubleSide }));
  f.userData.id = c.id; g.add(f); pick.push(f);
  const e = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 25), new THREE.LineBasicMaterial({ color: th.ghost, transparent: true, opacity: th.dark ? .75 : .7 }));
  e.raycast = () => {}; g.add(e);
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
    const h0 = c.tot0 * K.kv, h4 = c.tot4 * K.kv, w = c.w / 2, col = T().grupo[c.grupo] || T().footLine;
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
      if (vs > 0) addSolid(c, g, tubeGeo(P, y, r(vs)), T().mat[k], { edges: false });
      if (S.cmp === 'ambos' && v0 > 0) {
        const gg = tubeGeo(P, y, r(v0) + .12);
        const f = new THREE.Mesh(gg, new THREE.MeshBasicMaterial({ color: T().ghost, transparent: true, opacity: T().dark ? .16 : .14, depthWrite: false }));
        f.userData.id = c.id; g.add(f); pick.push(f);
        const e = new THREE.LineSegments(new THREE.EdgesGeometry(gg, 50), new THREE.LineBasicMaterial({ color: T().ghost, transparent: true, opacity: .45 })); e.raycast = () => {}; g.add(e);
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
    const bm = new THREE.Mesh(new THREE.CylinderGeometry(.55, .55, 1, 10, 1, true).translate(0, .5, 0), new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: .85, depthWrite: false, blending: T().dark ? THREE.AdditiveBlending : THREE.NormalBlending }));
    bm.visible = false; bm.raycast = () => {}; g.add(bm); c.beam = bm;
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
    const g = new THREE.Group(); g.userData.id = c.id; c.g = g; c.mats = []; c.gm = [];
    const w = c.w / 2;
    const foot = addSolid(c, g, ribbon(c.tp, -w, w, .2, Y0), th.foot, { edges: false, noShadow: true, opacity: mode === 'redes' ? .3 : 1 }); foot.userData.foot = true;
    const fl = new THREE.LineSegments(new THREE.EdgesGeometry(ribbon(c.tp, -w, w, .2, Y0 + .02), 25), new THREE.LineBasicMaterial({ color: th.footLine, transparent: true, opacity: .9 })); fl.raycast = () => {}; g.add(fl);
    c.top = BUILD[mode](c, g);
    civG.add(g);
    if (grow && mode !== 'sim') { g.scale.y = .001; anims.push({ t0: performance.now() + i * 28, dur: 650, f: t => { g.scale.y = Math.max(.001, easeOut(t)); } }); }
  });
  if (SIM.on) simApply();
  refreshLabels(); applySel(); renderLegend(); renderRank(); dirty = true;
}

// ───────────────────────── etiquetas flotantes ─────────────────────────
function ensureLabels() {
  for (const c of D.civs) {
    if (c.lbl) continue;
    const el = document.createElement('div'); el.className = 'lbl'; el.dataset.id = c.id;
    el.innerHTML = '<div class="card"></div><div class="stem"></div><div class="dot"></div>';
    el.addEventListener('click', e => { e.stopPropagation(); selectCiv(c.id === S.sel ? null : c.id); });
    el.addEventListener('pointerenter', () => { if (!isMobile()) setHover(c.id, null); });
    el.addEventListener('pointerleave', () => { if (!isMobile()) setHover(null, null); });
    c.lbl = new CSS2DObject(el); c.lbl.center.set(.5, 1); scene.add(c.lbl);
  }
}
function badge(c) { return (S.hall && c.sev) ? `<span class="badge ${c.sev}" title="${c.hallazgos.length} hallazgo(s) · severidad máxima ${c.sev}">${SEVI[c.sev]} ${c.hallazgos.length}</span>` : ''; }
function miniBar(vals, tot, max) { return `<div class="mb" style="width:${Math.max(18, 120 * tot / max)}px">${MATK.filter(k => (vals[k] || 0) > 0).map(k => `<i style="flex:${vals[k]};background:${T().mat[k]}"></i>`).join('')}</div>`; }
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
      const bars = S.cmp === 'ambos' ? miniBar(c.v0, c.tot0, mx) + miniBar(c.v4, c.tot4, mx) + `<div class="mbl"><span>▲ antes · ▼ ahora</span></div>` : miniBar(S.cmp === 'v0' ? c.v0 : c.v4, 1, 1);
      return nm + `<div class="vl">${fM(S.cmp === 'v0' ? c.tot0 : c.tot4)}${S.cmp === 'ambos' ? chip : ''}</div>${bars}<div class="sb">Mayor cambio: ${MATS[best]} ${fMs(bd)}</div>`;
    }
    case 'estructural': {
      const [a, b] = c.est; const v = S.cmp === 'v0' ? a : b;
      const lay = key => `<div class="mb" style="width:120px">${CAPK.filter(k => (c.estructura[k]?.[key] || 0) > 0).map(k => `<i style="flex:${c.estructura[k][key]};background:${T().capa[k]}"></i>`).join('')}</div>`;
      return nm + `<div class="vl">${S.cmp === 'ambos' ? `${nf(a)} → ${nf(b)} cm` : `${nf(v)} cm`}${S.cmp === 'ambos' ? `<span class="d ${b >= a ? 'up' : 'down'}">${fP(a ? (b / a - 1) * 100 : 0)}</span>` : ''}</div>${S.cmp === 'ambos' ? lay('cm0') + lay('cm4') : lay(S.cmp === 'v0' ? 'cm0' : 'cm4')}<div class="sb">espesor equivalente total</div>`;
    }
    case 'redes': {
      const r = c.redes;
      const f = k => S.cmp === 'ambos' ? `${fM(c.v0[k] || 0)} → ${fM(c.v4[k] || 0)}` : fM((S.cmp === 'v0' ? c.v0 : c.v4)[k] || 0);
      return nm + `<div class="vl">${S.cmp === 'ambos' ? `${fM(c.red[0])} → ${fM(c.red[1])}` : fM(c.red[S.cmp === 'v0' ? 0 : 1])}</div><div class="sb"><i class="sw" style="display:inline-block;width:8px;height:8px;background:${T().mat.hidro};border-radius:2px"></i> Hidro ${f('hidro')} · ${nf(r.ml.hidro[0])}→${nf(r.ml.hidro[1])} ml</div><div class="sb"><i class="sw" style="display:inline-block;width:8px;height:8px;background:${T().mat.secas};border-radius:2px"></i> Secas ${f('secas')} · ${nf(r.un.secas[0])}→${nf(r.un.secas[1])} un</div>`;
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
let needMeasure = true;
function measureLabels() { for (const c of D.civs) if (c.lbl?.element.isConnected) { c.lw = c.lbl.element.offsetWidth; c.lh = c.lbl.element.offsetHeight; } for (const r of roadLbls) if (r.el.isConnected) { r.w = r.el.offsetWidth; r.h = r.el.offsetHeight; } needMeasure = false; }
const _v = new THREE.Vector3();
function declutter() {
  const st = $('#stage'), W = st.clientWidth, H = st.clientHeight, placed = [];
  const fits = (x0, y0, x1, y1) => { for (const p of placed) if (x0 < p[2] && x1 > p[0] && y0 < p[3] && y1 > p[1]) return false; return true; };
  const simPri = c => { const j = SIM.res?.byId[c.id]; if (!j) return 0; return (SIM.t >= j.s && SIM.t < j.e ? 1e12 : SIM.t >= j.e ? 1e11 : 1e10) + j.tot; };
  const items = D.civs.map(c => ({ c, pri: (c.id === S.sel ? 1e16 : 0) + (c.id === S.hover ? 1e15 : 0) + (S.hall && c.sev === 'ALTA' ? 1e13 : 0) + (SIM.on ? simPri(c) : Math.abs(metric(c))) }));
  items.sort((a, b) => b.pri - a.pri);
  for (const { c } of items) {
    const el = c.lbl.element; const forced = c.id === S.sel || c.id === S.hover;
    if (!S.labels && !forced) { el.classList.add('hid'); continue; }
    _v.copy(c.lbl.position).project(camera);
    if (_v.z > 1) { el.classList.add('hid'); el.classList.remove('dim'); continue; }
    const x = (_v.x + 1) / 2 * W, y = (1 - _v.y) / 2 * H, w = c.lw || 120, h = c.lh || 50;
    const r = [x - w / 2 - 3, y - h - 2, x + w / 2 + 3, y + 2];
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
  for (const c of D.civs) {
    const dim = S.sel && c.id !== S.sel, sel = c.id === S.sel, hov = c.id === S.hover && !sel;
    for (const m of c.mats) {
      m.color.copy(m.userData.base); if (dim) m.color.lerp(_ground, T().dark ? .62 : .55);
      m.emissive.copy(m.userData.base).multiplyScalar(sel ? .2 : hov ? .14 : 0);
    }
    for (const m of c.gm || []) { m.userData.op ??= m.opacity; m.opacity = m.userData.op * (dim ? .35 : 1); }
    c.lbl?.element.classList.toggle('sel', sel);
  }
  $$('#rank li').forEach(li => li.classList.toggle('sel', li.dataset.id === S.sel));
  dirty = true;
}
function selectCiv(id, fly = true) {
  S.sel = id && byId[id] ? id : null;
  document.body.classList.toggle('has-sel', !!S.sel);
  $('#panelR').hidden = !S.sel;
  const det = $('#mnav button[data-sheet="det"]'); if (det) det.disabled = !S.sel;
  renderDetail(); applySel();
  if (S.sel) { if (isMobile()) openSheet('det'); if (fly) fitTo([byId[S.sel]], null, null, 900, true); }
  else if (isMobile() && sheet === 'det') openSheet(null);
  writeHash();
}
function setHover(id, ev) {
  if (S.hover !== id) { S.hover = id; applySel(); }
  const tip = $('#tip');
  if (!id || !ev) { tip.classList.remove('on'); return; }
  const c = byId[id];
  tip.innerHTML = `<b>${esc(c.nom)} · ${esc(c.tramo)}</b><div style="color:var(--muted);font-size:11.5px;margin-bottom:5px">CIV ${c.id} · SG${c.sg} · ${GRUPON[c.grupo] || ''}</div>
    <div class="r"><span>Antes (V0)</span><b>${fM(c.tot0)}</b></div><div class="r"><span>Ahora (V4)</span><b>${fM(c.tot4)}</b></div>
    <div class="r"><span>Diferencia</span><b class="${c.delta >= 0 ? 'up' : 'down'}">${fMs(c.delta)} (${fP(c.dpct)})</b></div><div class="r"><span>No previstos V4</span><b>${fM(c.np4)} · ${nf(c.pnp, 1)}%</b></div>
    <div style="margin-top:5px;font-size:11px;color:var(--muted)">Clic para ver el detalle</div>`;
  placeTip(ev.clientX, ev.clientY);
}
function placeTip(x, y) { const tip = $('#tip'); tip.classList.add('on'); const r = tip.getBoundingClientRect(); let L = x + 16, Tp = y + 14; if (L + r.width > innerWidth - 8) L = x - r.width - 16; if (Tp + r.height > innerHeight - 8) Tp = y - r.height - 14; tip.style.left = Math.max(8, L) + 'px'; tip.style.top = Math.max(8, Tp) + 'px'; }
function fitTo(list, polarDeg = 55, azDeg = null, ms = 900, keepAngle = false) {
  let x0 = 1e9, x1 = -1e9, z0 = 1e9, z1 = -1e9;
  for (const c of list) for (const [x, z] of c.tp) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); z0 = Math.min(z0, z); z1 = Math.max(z1, z); }
  const one = list.length === 1, tp = one ? (list[0].top || 0) : 0;
  const ctr = new THREE.Vector3((x0 + x1) / 2, one ? tp * .4 : 0, (z0 + z1) / 2);
  const rad = Math.max(70, Math.hypot(x1 - x0, z1 - z0) / 2 + (one ? 80 : 40), one ? tp * .75 + 50 : 0);
  const vf = THREE.MathUtils.degToRad(camera.fov), hf = 2 * Math.atan(Math.tan(vf / 2) * camera.aspect);
  const dist = rad / Math.sin(Math.min(vf, hf) / 2) * (list.length > 1 ? .82 : 1);
  const sph = new THREE.Spherical().setFromVector3(camera.position.clone().sub(controls.target));
  const pol = polarDeg == null || keepAngle ? clamp(sph.phi, .2, 1.2) : THREE.MathUtils.degToRad(polarDeg);
  const az = azDeg == null || keepAngle ? sph.theta : THREE.MathUtils.degToRad(azDeg);
  const pos = ctr.clone().add(new THREE.Vector3().setFromSphericalCoords(dist, Math.max(pol, .001), az));
  // desplazar el encuadre para compensar los paneles abiertos (izquierda / detalle)
  {
    const st = $('#stage'), Wd = st.clientWidth, Hd = st.clientHeight, mob = isMobile();
    const left = mob ? 0 : $('#panelL').getBoundingClientRect().right;
    const right = !mob && S.sel ? $('#panelR').getBoundingClientRect().left : Wd;
    const top = $('#top').getBoundingClientRect().bottom;
    const bottom = mob ? (S.sel ? Hd - 64 - Math.min(Hd * .68, Hd - 150) : Hd - 64) : $('#dock').getBoundingClientRect().top;
    const mpp = 2 * dist * Math.tan(vf / 2) / Hd;
    const dx = (left + right) / 2 - Wd / 2, dy = (top + bottom) / 2 - Hd / 2;
    const rightV = new THREE.Vector3(Math.cos(az), 0, -Math.sin(az)), fwd = new THREE.Vector3(-Math.sin(az), 0, -Math.cos(az));
    const d = rightV.multiplyScalar(-dx * mpp).add(fwd.multiplyScalar(clamp(dy * mpp / Math.max(Math.cos(pol), .35), -rad, rad)));
    ctr.add(d); pos.add(d);
  }
  flyTo(pos, ctr, ms);
}
function flyTo(pos, tgt, ms) {
  if (!ms) { camera.position.copy(pos); controls.target.copy(tgt); controls.update(); dirty = true; return; }
  const p0 = camera.position.clone(), q0 = controls.target.clone();
  anims = anims.filter(a => !a.fly);
  controls.enableDamping = false;
  anims.push({ fly: true, t0: performance.now(), dur: ms, f: t => { const e = ease(t); camera.position.lerpVectors(p0, pos, e); controls.target.lerpVectors(q0, tgt, e); controls.update(); if (t >= 1) controls.enableDamping = true; } });
}
function preset(v) {
  S.view = v; $$('#views button').forEach(b => b.setAttribute('aria-pressed', b.dataset.view === v));
  if (v === 'general') fitTo(D.civs, 55, -16);
  if (v === 'sg2') fitTo(D.civs.filter(c => c.sg === '2'), 50, -28);
  if (v === 'sg5') fitTo(D.civs.filter(c => c.sg === '5'), 52, 18);
  if (v === 'planta') fitTo(D.civs, .001, 0);
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
  r.tInf = schedule(1e14).T; // duración con ritmo ilimitado (solo limita la producción por frente)
  if (r.tInf > 8) r.need = null;
  else { let lo = 1e7, hi = 1e14; for (let i = 0; i < 60; i++) { const mid = Math.sqrt(lo * hi); if (schedule(mid).T > 8) lo = mid; else hi = mid; } r.need = hi; }
  r.needF = null; for (let F = 1; F <= 40; F++) if (schedule(SIM.ritmo, F).T <= 8) { r.needF = F; break; }
  r.minT = r.total / SIM.ritmo;
  SIM.res = r; SIM.t = clamp(SIM.t, 0, r.tEnd);
  const sl = $('#simT'); sl.max = r.tEnd.toFixed(2); sl.value = SIM.t;
  $('#m8').style.left = `calc(${8 / r.tEnd * 100}% - 1px)`;
  $('#simTot').textContent = nf(r.T, 1) + ' meses';
  renderSimKpi(); drawChart();
  if (SIM.on) buildCivs(false);
}
function simApply() {
  const r = SIM.res, t = SIM.t;
  for (const c of D.civs) {
    if (!c.simL) continue;
    let active = null;
    for (const L of c.simL) {
      const p = L.ph, pr = p.e > p.s ? clamp((t - p.s) / (p.e - p.s), 0, 1) : (t >= p.s ? 1 : 0);
      L.mat.userData.u.uProg.value = pr; L.mat.userData.u.uGlowAmt.value = pr > 0 && pr < 1 ? 1.1 : 0;
      if (pr > 0 && pr < 1) active = { L, pr };
    }
    if (c.beam) {
      if (active) { const pt = at(c.tp, c.tcum, active.pr * c.tL); c.beam.visible = true; c.beam.position.set(pt[0], active.L.y0, pt[1]); c.beam.scale.y = active.L.y1 - active.L.y0 + 22; c.beam.material.color.set(T().fase[active.L.ph.k]).lerp(new THREE.Color('#ffffff'), .35); }
      else c.beam.visible = false;
    }
  }
  $('#simMes').textContent = nf(t, 1); $('#miniTxt').textContent = `Mes ${nf(t, 1)} · ${nf(r.total ? r.exec(t) / r.total * 100 : 0)}%`;
  $('#simExec').textContent = `${fM(r.exec(t))} · ${nf(r.total ? r.exec(t) / r.total * 100 : 0)}%`;
  if ($('#simT') !== document.activeElement) $('#simT').value = t;
  refreshLabels(false); updateCursor(); renderSimKpi(true);
  dirty = true;
}
function setSimOn(on) {
  if (SIM.on === on) return;
  SIM.on = on; $('#simOn').checked = on;
  $$('#modes .mode').forEach(b => b.setAttribute('aria-pressed', on ? b.dataset.k === 'sim' : b.dataset.k === S.mode));
  updateCmpUI(); applyVisibility(); buildCivs(!on); writeHash(); updateMini();
}
function play(on = !SIM.playing) {
  if (on && !SIM.on) setSimOn(true);
  if (on && SIM.t >= SIM.res.tEnd - .01) SIM.t = 0;
  SIM.playing = on;
  const ic = on ? '<path d="M4 2.5h3v11H4zM9 2.5h3v11H9z"/>' : '<path d="M4 2.5v11l9.5-5.5z"/>';
  $('#simPlay svg').innerHTML = ic; $('#miniPlay svg').innerHTML = ic;
  $('#simPlay').setAttribute('aria-label', on ? 'Pausar' : 'Reproducir');
  if (on && document.body.classList.contains('dock-min') && !isMobile()) toggleDock(false);
  updateMini();
}
function renderSimKpi(light = false) {
  const r = SIM.res; if (!r) return;
  const t = SIM.t, act = r.jobs.filter(j => t >= j.s && t < j.e).length;
  const k = $('#simKpi');
  k.innerHTML = `<div><small>Alcance del escenario</small><b>${fM(r.total)}</b><small>${r.jobs.length} CIV</small></div>
    <div><small>Duración simulada</small><b class="${r.T > 8 ? 'up' : ''}">${nf(r.T, 1)} meses</b><small>plazo pedido: 8</small></div>
    <div><small>Ejecutado al mes 8</small><b>${nf(r.total ? r.exec(8) / r.total * 100 : 0)}%</b><small>${fM(r.exec(8))}</small></div>
    <div><small>Frentes activos ahora</small><b>${act} de ${SIM.fr}</b><small>${fM(act ? Math.min(SIM.ritmo, act * SIM.cap) : 0)}/mes ahora</small></div>`;
  if (light) return;
  const v = $('#simVerdict'), ok = r.T <= 8 + 1e-6;
  v.className = 'verdict ' + (ok ? 'ok' : 'bad');
  const opts = [];
  if (r.needF && r.needF !== SIM.fr) opts.push(`≈ <b>${r.needF} frentes</b> al ritmo elegido`);
  if (r.need && r.need > SIM.ritmo * 1.001) opts.push(`≈ <b>${fM(r.need)}/mes</b> de obra con ${SIM.fr} frentes`);
  const why = r.minT > 8.05 ? ` Aun sin tiempos muertos, ${fM(r.total)} ÷ ${fM(SIM.ritmo)}/mes = ${nf(r.minT, 1)} meses.` : '';
  v.innerHTML = ok
    ? `<span class="ic">✓</span><span><b>Cabe en el plazo.</b> Con ${SIM.fr} frentes y ${fM(SIM.ritmo)}/mes el escenario termina en el mes ${nf(r.T, 1)}.</span>`
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
    let d = ''; const N = 160; for (let i = 0; i <= N; i++) { const t = i / N * tMax; d += (i ? 'L' : 'M') + X(t).toFixed(1) + ',' + Y(r.exec(t)).toFixed(1); }
    h += `<path d="${d}" fill="none" stroke="var(--accent)" stroke-width="2.2" stroke-linejoin="round"/>`;
    h += `<g id="cur"><line id="curL" y1="${m.t}" y2="${m.t + ih}" stroke="var(--ink)" stroke-width="1" opacity=".55"/><circle id="curD" r="4.5" fill="var(--accent)" stroke="var(--panel-solid)" stroke-width="2"/></g>`;
    h += `<g transform="translate(${m.l + iw - 232},${m.t + ih - 30})"><rect x="-8" y="-11" width="236" height="38" rx="7" fill="var(--panel-solid)" opacity=".85"/><line x2="18" stroke="var(--accent)" stroke-width="2.2"/><text x="23" y="3.5">avance simulado</text><line x1="0" x2="18" y1="15" y2="15" stroke="var(--muted)" stroke-width="1.5" stroke-dasharray="5 4"/><text x="23" y="18.5">ritmo tope sin movilización ni pausas</text></g>`;
    CH = { m, iw, ih, X, Y, tMax };
  } else if (SIM.chart === 'm') {
    const K2 = Math.ceil(r.T - 1e-9) || 1, fl = []; for (let k = 1; k <= K2; k++) fl.push(r.exec(k) - r.exec(k - 1));
    const ymax = Math.max(SIM.ritmo, ...fl) * 1.15 || 1, Y = v => m.t + ih - v / ymax * ih, st = niceStep(ymax / 4);
    for (let v = 0; v <= ymax; v += st) h += `<line x1="${m.l}" x2="${m.l + iw}" y1="${Y(v)}" y2="${Y(v)}" stroke="var(--hair)" stroke-width="1" opacity=".7"/><text x="${m.l - 6}" y="${Y(v) + 3.5}" text-anchor="end">${fM(v)}</text>`;
    h += xAxis();
    const bw = Math.max(3, iw / tMax - 3);
    fl.forEach((v, i) => { const x = X(i) + (iw / tMax - bw) / 2; const y = Y(v); h += `<rect class="fbar" data-k="${i + 1}" data-v="${v}" x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${bw.toFixed(1)}" height="${Math.max(0, m.t + ih - y).toFixed(1)}" rx="3" fill="var(--accent)"/>`; });
    h += plazo + `<line x1="${m.l}" x2="${m.l + iw}" y1="${Y(SIM.ritmo)}" y2="${Y(SIM.ritmo)}" stroke="var(--ink)" stroke-width="1.2" stroke-dasharray="5 4" opacity=".7"/><text x="${m.l + iw - 4}" y="${Y(SIM.ritmo) - 5}" text-anchor="end" style="font-weight:700;fill:var(--ink2)">ritmo elegido ${fM(SIM.ritmo)}/mes</text>`;
    h += `<g id="cur"><line id="curL" y1="${m.t}" y2="${m.t + ih}" stroke="var(--ink)" stroke-width="1" opacity=".55"/></g>`;
    CH = { m, iw, ih, X, Y, tMax };
  } else {
    const F = SIM.fr, rh = Math.min(24, ih / F), gap = Math.min(4, rh * .18);
    h += xAxis();
    for (let f = 0; f < F; f++) h += `<text x="${m.l - 6}" y="${m.t + f * rh + rh / 2 + 3.5}" text-anchor="end">Frente ${f + 1}</text>`;
    for (const j of r.jobs) {
      const y = m.t + j.front * rh + gap / 2, hh = rh - gap;
      for (const p of j.ph) { if (p.e - p.s <= 0) continue; h += `<rect class="gseg" data-id="${j.c.id}" data-k="${p.k}" x="${X(p.s).toFixed(1)}" y="${y.toFixed(1)}" width="${Math.max(.8, X(p.e) - X(p.s)).toFixed(1)}" height="${hh.toFixed(1)}" fill="${T().fase[p.k]}"/>`; }
      h += `<rect class="gjob" data-id="${j.c.id}" x="${X(j.s).toFixed(1)}" y="${y.toFixed(1)}" width="${(X(j.e) - X(j.s)).toFixed(1)}" height="${hh.toFixed(1)}" fill="none" stroke="var(--panel-solid)" stroke-width="1.5" rx="2"/>`;
      if (X(j.e) - X(j.s) > 46 && hh > 11) h += `<text x="${X(j.s) + 4}" y="${y + hh / 2 + 3.5}" style="fill:#fff;font-weight:700;pointer-events:none;paint-order:stroke;stroke:rgba(0,0,0,.45);stroke-width:2px">${esc(j.c.nom)}</text>`;
    }
    h += plazo + `<g id="cur"><line id="curL" y1="${m.t}" y2="${m.t + ih}" stroke="var(--ink)" stroke-width="1.2" opacity=".7"/></g>`;
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
  const tip = $('#tip'); let html = '';
  const tg = e.target;
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

// ───────────────────────── interfaz ─────────────────────────
let sheet = null;
function openSheet(name) {
  if (!isMobile()) return;
  const L = $('#panelL'), R = $('#panelR'), Dk = $('#dock');
  [L, R, Dk].forEach(e => e.classList.remove('open'));
  if (name === 'map' || name === 'ley') { L.dataset.show = name; $('#shLTitle').textContent = name === 'map' ? 'Tipo de mapa y paleta' : 'Leyenda y ranking'; L.classList.add('open'); L.querySelector('.pscroll').scrollTop = 0; }
  if (name === 'sim') { Dk.classList.add('open'); setTimeout(drawChart, 300); }
  if (name === 'det' && S.sel) R.classList.add('open');
  sheet = name;
  $$('#mnav button').forEach(b => b.setAttribute('aria-pressed', b.dataset.sheet === name));
  updateMini();
}
function updateMini() { $('#miniSim').classList.toggle('on', isMobile() && SIM.on && sheet !== 'sim'); }
function toggleDock(min = !document.body.classList.contains('dock-min')) {
  document.body.classList.toggle('dock-min', min); $('#dockMin').textContent = min ? '▴' : '▾';
  setTimeout(() => { drawChart(); dirty = true; }, 280);
}
function toast(msg) { const t = $('#toast'); t.textContent = msg; t.classList.add('on'); clearTimeout(toast._t); toast._t = setTimeout(() => t.classList.remove('on'), 2800); }
function updateCmpUI() {
  const md = MODES.find(m => m.k === (SIM.on ? 'sim' : S.mode));
  $('#cmp').classList.toggle('off', !md.cmp);
  $$('#cmp button').forEach(b => b.setAttribute('aria-pressed', b.dataset.v === S.cmp));
  const notes = {
    ambos: { costos: 'Sólido = ahora (V4) · contorno de vidrio = antes (V0). Si el vidrio sobresale, el CIV bajó.', alcance: 'Sólido = ahora (V4) · contorno de vidrio = antes (V0).', materiales: 'Dos franjas por calle: de alambre = antes (V0), sólida = ahora (V4), con el mismo orden de capas.', estructural: 'Dos franjas por calle: de alambre = antes (V0), sólida = ahora (V4), con el mismo orden de capas.', redes: 'Tubo sólido = ahora (V4) · tubo de vidrio = antes (V0).' },
  };
  $('#cmpNote').textContent = !md.cmp ? (SIM.on ? 'La simulación usa el escenario elegido en el panel inferior.' : md.k === 'variacion' ? 'Este mapa ya muestra la diferencia V4 − V0.' : 'Los no previstos solo existen en V4.') : S.cmp === 'ambos' ? notes.ambos[md.k] : S.cmp === 'v0' ? 'Solo el presupuesto contractual (V0), repartido por CIV.' : 'Solo el presupuesto radicado el 01-09-2026 (V4).';
  $('#cmpAux').textContent = md.cmp ? '' : 'no aplica';
}
function renderLegend() {
  const th = T(), el = $('#legend'); const mode = SIM.on ? 'sim' : S.mode; const md = MODES.find(m => m.k === mode);
  const row = (col, txt, v = '', cls = '') => `<div class="lg-row"><i class="sw ${cls}" style="background:${col}"></i><span>${txt}</span><span class="v">${v}</span></div>`;
  const grad = (st, a, b, mid) => `<div class="grad" style="background:linear-gradient(90deg,${[0, .25, .5, .75, 1].map(t => ramp(st, t)).join(',')})"></div><div class="ticks"><span>${a}</span>${mid ? `<span>${mid}</span>` : ''}<span>${b}</span></div>`;
  let h = `<p class="lg-h">${md.help}</p>`;
  const ghost = S.cmp === 'ambos' && md.cmp ? row('transparent', (mode === 'materiales' || mode === 'estructural') ? 'Franja de alambre = antes (V0) · sólida = ahora (V4)' : 'Contorno de vidrio = antes (V0) · sólido = ahora (V4)', '', 'ghost') : '';
  if (mode === 'costos') h += `<div class="lg-h"><b>Color:</b> costo por m² (${S.cmp === 'v0' ? 'V0' : 'V4'})</div>` + grad(th.seq, fm2(K.m2min), fm2(K.m2max)) + `<div style="height:8px"></div>` + ghost;
  if (mode === 'variacion') h += grad(th.div, fP(-K.dmax, 0), fP(K.dmax, 0), '0%') + `<div class="lg-h" style="margin-top:8px">Mayor alza: ${fP(Math.max(...D.civs.map(c => c.dpct)), 0)} · mayor baja: ${fP(Math.min(...D.civs.map(c => c.dpct)), 1)}</div>`;
  if (mode === 'np') h += grad(th.np, '0% NP', nf(K.pmax, 0) + '% NP') + `<div style="height:8px"></div>` + row('transparent', 'Contorno = total del CIV en V4', '', 'ghost');
  if (mode === 'alcance') { const g = {}; D.civs.forEach(c => { (g[c.grupo] ||= [0, 0]); g[c.grupo][0]++; g[c.grupo][1] += c.tot4; }); h += Object.keys(GRUPON).map(k => row(th.grupo[k], GRUPON[k], `${g[k]?.[0] || 0} · ${fM(g[k]?.[1] || 0)}`)).join('') + ghost; }
  if (mode === 'materiales') { const t0 = {}, t4 = {}; D.civs.forEach(c => MATK.forEach(k => { t0[k] = (t0[k] || 0) + (c.v0[k] || 0); t4[k] = (t4[k] || 0) + (c.v4[k] || 0); })); h += `<div class="lg-row" style="font-size:10.5px;color:var(--muted);font-weight:700"><span style="margin-left:22px">DE ARRIBA ABAJO EN LA COLUMNA</span><span class="v">Δ total</span></div>` + MATK.slice().reverse().map(k => row(th.mat[k], MATS[k], fMs(t4[k] - t0[k]))).join('') + ghost; }
  if (mode === 'estructural') h += CAPK.slice().reverse().map(k => row(th.capa[k], CAPN[k])).join('') + `<div class="lg-h" style="margin-top:6px">Escala vertical: 1 cm de espesor = ${nf(K.kcm, 2)} m en el plano.</div>` + ghost;
  if (mode === 'redes') h += row(th.mat.hidro, MATN.hidro, 'tubo profundo') + row(th.mat.secas, MATN.secas, 'tubo somero') + ghost + `<div class="lg-h" style="margin-top:6px">El terreno se vuelve translúcido para ver el subsuelo.</div>`;
  if (mode === 'sim') h += FASEK.map(k => row(th.fase[k], FASEN[k])).join('') + row('transparent', 'Contorno = volumen final planeado', '', 'ghost') + `<div class="lg-h" style="margin-top:6px">El frente de obra avanza a lo largo de la calle con un halo luminoso; altura de cada franja ∝ valor de la fase.</div>`;
  if (S.hall) h += `<div class="lg-row" style="margin-top:6px;align-items:flex-start"><span class="sev ALTA" style="margin-top:1px">▲ n</span><span>Etiqueta con hallazgos del análisis: ▲ severidad alta · ● media · ℹ informativa; n = cantidad.</span></div>`;
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
  $('#rank').innerHTML = list.map((c, i) => {
    const v = metric(c), col = civColor(c);
    let bar;
    if (mode === 'variacion') { const w = Math.abs(v) / mx * 50; bar = `<i style="background:${col};${v >= 0 ? `left:50%;width:${w}%` : `left:${50 - w}%;width:${w}%`}"></i><span class="mid"></span>`; }
    else if (SIM.on) { const j = SIM.res.byId[c.id]; const tm = SIM.res.tEnd; bar = j ? `<i style="background:var(--accent);left:${j.s / tm * 100}%;width:${Math.max(1, (j.e - j.s) / tm * 100)}%"></i>` : ''; }
    else bar = `<i style="background:${col};left:0;width:${Math.abs(v) / mx * 100}%"></i>`;
    return `<li data-id="${c.id}" class="${c.id === S.sel ? 'sel' : ''}" title="${esc(c.nom + ' · ' + c.tramo)} (CIV ${c.id})"><span class="n">${i + 1}</span><span class="t">${esc(c.nom)} <small>${esc(c.tramo)}</small></span><span class="v">${fmt(c)}</span><span></span><span class="bar">${bar}</span></li>`;
  }).join('');
}
function renderKpis() {
  const t = D.tot, d = t.t4 - t.t0;
  $('#kpis').innerHTML = `
    <div class="kpi" data-tip="<b>Antes · V0</b><br>Cantidad contractual de cada renglón repartida entre los 27 CIV con el reparto del contrato, valorada con el precio con AIU de V4. No incluye ${fM(D.meta.totales.v0_sin_reparto)} de renglones sin reparto por CIV (el total V0 del libro es ${fM(D.meta.totales.v0_N688)})."><small>ANTES · V0</small><b>${fM(t.t0)}</b></div>
    <div class="kpi" data-tip="<b>Ahora · V4</b><br>Suma de la matriz ítem × CIV del presupuesto radicado el 01-09-2026 (75MM · 8 meses), obras con AIU 31,849%. Cuadra con la fila 688 col. M."><small>AHORA · V4</small><b>${fM(t.t4)}</b></div>
    <div class="kpi" data-tip="<b>Diferencia en el plano</b><br>V4 − V0 de los 27 CIV. Es solo efecto cantidad: ambos se valoran con el mismo precio unitario."><small>DIFERENCIA</small><b class="up">${fMs(d)}<span class="d">${fP(d / t.t0 * 100)}</span></b></div>
    <div class="kpi" data-tip="<b>No previstos (NP) en V4</b><br>Valor de los ítems NP asignados a los 27 CIV en V4 y su peso sobre el total V4."><small>NO PREVISTOS V4</small><b>${fM(t.np)}<span class="d" style="color:var(--muted)">${nf(t.np / t.t4 * 100, 1)}%</span></b></div>`;
}
function renderDetail() {
  const el = $('#detail'), c = byId[S.sel]; if (!c) { el.innerHTML = ''; return; }
  const th = T(), mx = Math.max(c.tot0, c.tot4);
  const mbar = (vals, tot) => `<div class="mbar" style="width:${tot / mx * 100}%">${MATK.filter(k => (vals[k] || 0) > 0).map(k => `<i style="flex:${vals[k]};background:${th.mat[k]}" title="${MATS[k]}: ${fM(vals[k])}"></i>`).join('')}</div>`;
  const matRows = MATK.filter(k => (c.v0[k] || 0) || (c.v4[k] || 0)).map(k => { const d = (c.v4[k] || 0) - (c.v0[k] || 0); return `<tr><td><i class="sw" style="display:inline-block;width:10px;height:10px;border-radius:3px;background:${th.mat[k]};vertical-align:-1px;margin-right:6px"></i>${MATS[k]}</td><td>${fM(c.v0[k] || 0)}</td><td>${fM(c.v4[k] || 0)}</td><td class="${d >= 0 ? 'up' : 'down'}">${fMs(d)}</td></tr>`; }).join('');
  const r = c.redes;
  const j = SIM.res?.byId[c.id];
  const hall = (c.hallazgos || []).map(h => `<a class="hl" href="../index.html#p75/hall/${encodeURIComponent(h.id)}"><span class="sev ${h.s}">${SEVI[h.s] || ''} ${h.s}</span><span><b>${esc(h.id)}</b> · ${esc(h.t)}</span></a>`).join('');
  const top = (c.topDelta || []).slice(0, 8).map(it => { const d = it.v4 - it.v0; return `<tr><td>${esc(it.i)}${it.np ? ' <span class="np">NP</span>' : ''}</td><td class="desc">${esc(it.d.slice(0, 64))}${it.d.length > 64 ? '…' : ''}</td><td>${nf(it.q0, 1)} → ${nf(it.q4, 1)} ${esc(it.u || '')}</td><td class="${d >= 0 ? 'up' : 'down'}">${fMs(d)}</td></tr>`; }).join('');
  el.innerHTML = `
  <div class="dhead"><div style="min-width:0"><h3>${esc(c.nom)} <span style="font-weight:500;color:var(--muted)">· ${esc(c.tramo)}</span></h3>
    <p>CIV ${c.id} · Subgrupo ${c.sg} · ${nf(c.longitud, 1)} m × ${nf(c.ancho, 1)} m · ${nf(c.area)} m²</p>
    <p style="margin-top:7px;display:flex;gap:6px;flex-wrap:wrap"><span class="chip"><i style="background:${th.grupo[c.grupo] || th.footLine}"></i>${GRUPON[c.grupo] || 'sin grupo'}</span>${c.sev ? `<span class="chip"><span class="sev ${c.sev}" style="padding:0 4px">${SEVI[c.sev]}</span>${c.hallazgos.length} hallazgo(s)</span>` : ''}</p></div>
    <button class="close dclose" data-close="panelR" aria-label="Cerrar detalle">✕ Cerrar</button></div>
  <div class="pscroll" style="flex:1">
    <div class="dkpis">
      <div class="dk"><small>Antes · V0</small><b>${fM(c.tot0)}</b><em>${fm2(c.m2[0])}</em></div>
      <div class="dk"><small>Ahora · V4</small><b>${fM(c.tot4)}</b><em>${fm2(c.m2[1])}</em></div>
      <div class="dk"><small>Diferencia</small><b class="${c.delta >= 0 ? 'up' : 'down'}">${fMs(c.delta)}</b><em>${fP(c.dpct)}</em></div>
      <div class="dk"><small>No previstos en V4</small><b>${fM(c.np4)}</b><em>${nf(c.pnp, 1)}% del CIV</em></div>
    </div>
    ${j ? `<div class="dsec"><h4>En la simulación</h4><div style="font-size:12.5px;margin-bottom:6px">Frente ${j.front + 1} · mes ${nf(j.s, 1)} → ${nf(j.e, 1)} · ${fM(j.tot)}</div><table class="t"><tr><th>Fase</th><th>Valor</th><th>Meses</th></tr>${j.ph.filter(p => p.v > 0).map(p => `<tr><td><i class="sw" style="display:inline-block;width:10px;height:10px;border-radius:3px;background:${th.fase[p.k]};vertical-align:-1px;margin-right:6px"></i>${FASEN[p.k]}</td><td>${fM(p.v)}</td><td>${nf(p.s, 1)}–${nf(p.e, 1)}</td></tr>`).join('')}</table></div>` : ''}
    <div class="dsec"><h4>Materiales · antes vs. ahora</h4>
      <div class="mrow"><small>Antes</small>${mbar(c.v0, c.tot0)}<b style="font-size:12px">${fM(c.tot0)}</b></div>
      <div class="mrow"><small>Ahora</small>${mbar(c.v4, c.tot4)}<b style="font-size:12px">${fM(c.tot4)}</b></div>
      <table class="t" style="margin-top:8px"><tr><th>Material</th><th>Antes</th><th>Ahora</th><th>Δ</th></tr>${matRows}</table>
    </div>
    <div class="dsec"><h4>Estructura de pavimento (espesor equivalente)</h4><div class="xs">${xsSVG(c)}</div>
      <p class="note">m³ del CIV ÷ área del CIV: mide la intensidad de cada capa, no el espesor de diseño.</p></div>
    <div class="dsec"><h4>Redes y andenes</h4><table class="t"><tr><th></th><th>Antes</th><th>Ahora</th></tr>
      <tr><td>Hidrosanitarias (ml)</td><td>${nf(r.ml.hidro[0], 1)}</td><td>${nf(r.ml.hidro[1], 1)}</td></tr>
      <tr><td>Hidrosanitarias (un)</td><td>${nf(r.un.hidro[0], 1)}</td><td>${nf(r.un.hidro[1], 1)}</td></tr>
      <tr><td>Redes secas (ml)</td><td>${nf(r.ml.secas[0], 1)}</td><td>${nf(r.ml.secas[1], 1)}</td></tr>
      <tr><td>Redes secas (un)</td><td>${nf(r.un.secas[0], 1)}</td><td>${nf(r.un.secas[1], 1)}</td></tr>
      <tr><td>Andenes (m²)</td><td>${nf(c.andenM2[0], 1)}</td><td>${nf(c.andenM2[1], 1)}</td></tr></table></div>
    <div class="dsec"><h4>Renglones que más cambian</h4><table class="t"><tr><th>Ítem</th><th style="text-align:left">Descripción</th><th>Cant.</th><th>Δ $</th></tr>${top}</table></div>
    ${hall ? `<div class="dsec"><h4>Hallazgos del análisis</h4>${hall}</div>` : ''}
    <div class="dsec"><h4>Geometría</h4><p class="note" style="margin:0">${esc(c.nota_geom)} Longitud del inventario ${nf(c.longitud, 1)} m · eje OSM ${nf(c.long_osm, 1)} m.</p></div>
  </div>
  <div class="dfoot"><a class="btn pri" href="../index.html#p75/civ/${encodeURIComponent(c.id)}">Abrir ficha en el análisis ↗</a><button class="btn" id="dFit" type="button">⌖ Centrar</button></div>`;
  $('#dFit').onclick = () => fitTo([c], null, null, 800, true);
}
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
  const y0 = H + 8; let yl = 16;
  s += `<text x="0" y="10" font-size="10" fill="var(--muted)">cm</text>`;
  CAPK.slice().reverse().forEach(k => { s += `<rect x="268" y="${yl - 8}" width="9" height="9" rx="2" fill="${th.capa[k]}"/><text x="264" y="${yl}" text-anchor="end" font-size="9.5" fill="var(--ink2)">${{ estab: 'Estab.', subbase: 'Subbase', base: 'Base', losa: 'Losa', asfalto: 'Asfalto' }[k]}</text>`; yl += 15; });
  s += `<line x1="${xa - 6}" x2="${xb + cw + 6}" y1="${y0}" y2="${y0}" stroke="var(--muted)"/></svg>`;
  return s;
}
function renderPals() {
  $('#pals').innerHTML = Object.entries(THEMES).map(([k, t]) => `<button class="pal" data-p="${k}" aria-pressed="${k === S.theme}" title="${esc(PAL_NOTE[k])}"><i style="background:linear-gradient(90deg,${t.swatch.map((c, i) => `${c} ${i * 20}% ${(i + 1) * 20}%`).join(',')})"></i>${t.n}</button>`).join('');
  $('#palNote').textContent = PAL_NOTE[S.theme];
}
function applyTheme(rebuildSim = true) {
  document.documentElement.dataset.theme = S.theme;
  renderPals(); themeContext();
  if (rebuildSim) drawChart();
  buildCivs(true); renderDetail(); writeHash();
}
function initUI() {
  $('#modes').innerHTML = MODES.map((m, i) => `<button class="mode" data-k="${m.k}" aria-pressed="${SIM.on ? m.k === 'sim' : m.k === S.mode}" title="${esc(m.help)} (tecla ${i + 1})"><svg viewBox="0 0 24 24">${ICON[m.k]}</svg><span><b>${m.n}</b><span>${m.h}</span></span></button>`).join('');
  $('#modes').addEventListener('click', e => {
    const b = e.target.closest('.mode'); if (!b) return; const k = b.dataset.k;
    if (k === 'sim') { setSimOn(true); if (isMobile()) openSheet('sim'); else toggleDock(false); return; }
    setMode(k); if (isMobile()) openSheet(null);
  });
  $('#cmp').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; S.cmp = b.dataset.v; updateCmpUI(); buildCivs(true); writeHash(); });
  $('#pals').addEventListener('click', e => { const b = e.target.closest('.pal'); if (!b) return; S.theme = b.dataset.p; applyTheme(); });
  $('#rank').addEventListener('click', e => { const li = e.target.closest('li'); if (!li) return; selectCiv(li.dataset.id); });
  $('#btnCsv').addEventListener('click', exportCsv);
  const tg = (id, key, fn) => { const el = $(id); el.checked = S[key]; el.addEventListener('change', () => { S[key] = el.checked; fn && fn(); dirty = true; }); };
  tg('#tLabels', 'labels'); tg('#tBldg', 'bldg', applyVisibility); tg('#tRoads', 'roads', applyVisibility); tg('#tShadow', 'shadow', applyVisibility);
  tg('#tHall', 'hall', () => { refreshLabels(); renderLegend(); });
  let exT; $('#rExag').addEventListener('input', e => { S.exag = +e.target.value; $('#oExag').textContent = nf(S.exag, 1) + '×'; cancelAnimationFrame(exT); exT = requestAnimationFrame(() => { if (SIM.on) { SIM.res.k = 130 * S.exag / Math.max(1, ...SIM.res.jobs.map(j => j.tot)); } buildCivs(false); }); });
  $$('#views button').forEach(b => b.addEventListener('click', () => preset(b.dataset.view)));
  $('#compass').addEventListener('click', () => { const sph = new THREE.Spherical().setFromVector3(camera.position.clone().sub(controls.target)); sph.theta = 0; flyTo(controls.target.clone().add(new THREE.Vector3().setFromSpherical(sph)), controls.target.clone(), 600); });
  $('#btnHelp').addEventListener('click', () => { $('#help').hidden = false; });
  $('#helpModes').innerHTML = MODES.map(m => `<li><b>${m.n}:</b> ${m.help}</li>`).join('');
  $('#helpNotes').innerHTML = D.meta.notas.map(n => `<li>${esc(n)}</li>`).join('') + `<li>Hay ${fM(D.meta.totales.v0_sin_reparto)} de V0 en renglones sin reparto por CIV que no se pueden ubicar en el plano; por eso el V0 del plano (${fM(D.tot.t0)}) es menor que el V0 del libro (${fM(D.meta.totales.v0_N688)}).</li><li>Escenario «Δ oficial»: el Δ de obra del libro (fila 688: ${fM(DOFI())}) repartido entre los CIV como el Δ del plano (${fM(DPOS())}); la diferencia es el V0 sin reparto por CIV.</li><li>Ritmo solicitado: $2.000M/mes = ${fM(D.meta.ritmo.obras_mensual)} de obra + ${fM(D.meta.ritmo.gestion_mensual)} de gestión (PMA-SST, diálogo, PMT). ${esc(D.meta.ritmo.nota_historico)}</li>`;
  document.addEventListener('click', e => { const b = e.target.closest('[data-close]'); if (!b) return; const w = b.dataset.close;
    if (w === 'help') $('#help').hidden = true;
    else if (w === 'panelR') { if (isMobile()) openSheet(null); else selectCiv(null); }
    else if (w === 'panelL' || w === 'dock') openSheet(null);
  });
  $('#help').addEventListener('click', e => { if (e.target.id === 'help') $('#help').hidden = true; });
  $$('#mnav button').forEach(b => b.addEventListener('click', () => { const s = b.dataset.sheet; openSheet(sheet === s ? null : s); }));
  // simulación
  $('#simPlay').addEventListener('click', () => play()); $('#miniPlay').addEventListener('click', () => play());
  $('#simReset').addEventListener('click', () => { SIM.t = 0; if (!SIM.on) setSimOn(true); simApply(); });
  $('#simOn').addEventListener('change', e => setSimOn(e.target.checked));
  $('#simSpeed').addEventListener('change', e => { SIM.speed = +e.target.value; });
  $('#simT').addEventListener('input', e => { SIM.t = +e.target.value; if (!SIM.on) setSimOn(true); simApply(); });
  $('#dockMin').addEventListener('click', () => toggleDock());
  const rerun = () => { simRun(); if (SIM.on) simApply(); renderRank(); if (S.sel) renderDetail(); writeHash(); };
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
    if (SIM.chart === 's' && CH) { const b = svg.getBoundingClientRect(), sx = svg.viewBox.baseVal.width / b.width; SIM.t = clamp(((e.clientX - b.left) * sx - CH.m.l) / CH.iw * CH.tMax, 0, SIM.res.tEnd); if (!SIM.on) setSimOn(true); simApply(); }
  });
  new ResizeObserver(() => drawChart()).observe(svg);
  // controles de la simulación reflejan el estado leído del enlace
  $('#simScope').value = SIM.scope; $('#simOrd').value = SIM.ord; $('#simFr').value = SIM.fr; $('#oFr').textContent = SIM.fr; $('#simCap').value = SIM.cap / 1e6; $('#oCap').textContent = fM(SIM.cap); $('#simMov').value = SIM.mov; $('#oMov').textContent = nf(SIM.mov, 2).replace(/,?0+$/, '') + ' mes';
  $('#rExag').value = S.exag; $('#oExag').textContent = nf(S.exag, 1) + '×';
  // interacción con el plano
  const cv = $('#gl'); let down = null, rafH = 0, nPtr = 0, multi = false;
  cv.addEventListener('pointerdown', e => { nPtr++; if (nPtr > 1) multi = true; else multi = false; down = { x: e.clientX, y: e.clientY, b: e.button }; });
  cv.addEventListener('pointercancel', () => { nPtr = Math.max(0, nPtr - 1); down = null; });
  cv.addEventListener('pointerup', e => {
    nPtr = Math.max(0, nPtr - 1);
    if (!down) return; const moved = Math.hypot(e.clientX - down.x, e.clientY - down.y) > 6; const b = down.b; down = null;
    if (moved || b !== 0 || multi) return;
    const id = pickAt(e.clientX, e.clientY);
    if (id) selectCiv(id === S.sel ? null : id); else if (S.sel && !isMobile()) selectCiv(null);
  });
  cv.addEventListener('pointermove', e => {
    if (e.pointerType !== 'mouse' || down) return;
    cancelAnimationFrame(rafH); rafH = requestAnimationFrame(() => { const id = pickAt(e.clientX, e.clientY); cv.style.cursor = id ? 'pointer' : ''; setHover(id, e); });
  });
  cv.addEventListener('pointerleave', () => setHover(null, null));
  // tooltips de la interfaz (encabezado)
  document.addEventListener('pointerover', e => { const t = e.target.closest && e.target.closest('[data-tip]'); if (!t) return; $('#tip').innerHTML = t.dataset.tip; const r = t.getBoundingClientRect(); placeTip(r.left, r.bottom + 4); });
  document.addEventListener('pointerout', e => { const t = e.target.closest && e.target.closest('[data-tip]'); if (t && !t.contains(e.relatedTarget)) $('#tip').classList.remove('on'); });
  document.addEventListener('touchstart', e => { if (!(e.target.closest && e.target.closest('[data-tip]'))) $('#tip').classList.remove('on'); }, { passive: true });
  // teclado
  document.addEventListener('keydown', e => {
    if (/INPUT|SELECT|TEXTAREA/.test(document.activeElement?.tagName) && e.key !== 'Escape') return;
    if (e.key === 'Escape') { if (!$('#help').hidden) $('#help').hidden = true; else if (sheet) openSheet(null); else if (S.sel) selectCiv(null); return; }
    if (e.key === ' ') { if (/^(BUTTON|A)$/.test(document.activeElement?.tagName || '')) return; e.preventDefault(); play(); return; }
    const n = +e.key; if (n >= 1 && n <= MODES.length) { const k = MODES[n - 1].k; if (k === 'sim') { setSimOn(true); toggleDock(false); } else setMode(k); }
  });
  addEventListener('resize', () => { updateMini(); if (!isMobile()) { [$('#panelL'), $('#panelR'), $('#dock')].forEach(e => e.classList.remove('open')); sheet = null; } });
  $('#simPace').value = SIM.pace; $('#fldCustom').hidden = SIM.pace !== 'custom';
  renderKpis(); updateCmpUI();
  if (SIM.on) { $('#simOn').checked = true; toggleDock(false); }
}
function setMode(k) {
  S.mode = k; if (SIM.on) { SIM.on = false; SIM.playing = false; play(false); $('#simOn').checked = false; }
  $$('#modes .mode').forEach(b => b.setAttribute('aria-pressed', b.dataset.k === k));
  updateCmpUI(); applyVisibility(); buildCivs(true); writeHash(); updateMini();
  if (k === 'redes') { const sph = new THREE.Spherical().setFromVector3(camera.position.clone().sub(controls.target)); if (sph.phi < 1.05) { sph.phi = 1.12; flyTo(controls.target.clone().add(new THREE.Vector3().setFromSpherical(sph)), controls.target.clone(), 700); } }
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
  const h = new URLSearchParams(location.hash.slice(1));
  const m = h.get('m'); if (m && MODES.some(x => x.k === m && x.k !== 'sim')) S.mode = m;
  const c = h.get('c'); if (['v0', 'v4', 'ambos'].includes(c)) S.cmp = c;
  const p = h.get('p'); if (p && THEMES[p]) S.theme = p;
  const v = h.get('civ'); if (v) S.sel = v;
  if (h.get('sim') === '1') SIM.on = true;
  const t = parseFloat(h.get('t')); if (!isNaN(t)) SIM.t = t;
  const sc = h.get('esc'); if (['oficial', 'delta', 'pend', 'v4'].includes(sc)) SIM.scope = sc;
  const cp = parseInt(h.get('cap')); if (cp >= 100 && cp <= 2000) SIM.cap = cp * 1e6;
  const o = h.get('ord'); if (['grupo', 'valor', 'sg', 'norte'].includes(o)) SIM.ord = o;
  const f = parseInt(h.get('fr')); if (f >= 1 && f <= 10) SIM.fr = f;
  const r = h.get('ritmo'); if (r === 'historico') { SIM.pace = 'historico'; }
  const vw = h.get('vista'); if (vw === 'planta') S.view = 'planta';
}
let hashT;
function writeHash() {
  clearTimeout(hashT); hashT = setTimeout(() => {
    const o = { m: S.mode, c: S.cmp, p: S.theme }; if (S.sel) o.civ = S.sel;
    if (SIM.on) Object.assign(o, { sim: 1, t: SIM.t.toFixed(1), esc: SIM.scope, ord: SIM.ord, fr: SIM.fr, cap: Math.round(SIM.cap / 1e6), ...(SIM.pace === 'historico' ? { ritmo: 'historico' } : {}) });
    try { history.replaceState(null, '', '#' + new URLSearchParams(o).toString()); } catch (_) {}
  }, 250);
}

// ───────────────────────── bucle de render ─────────────────────────
let last = performance.now(), lastDecl = 0;
function loop(now) {
  requestAnimationFrame(loop);
  const dt = Math.min(.1, (now - last) / 1000); last = now;
  if (anims.length) {
    anims = anims.filter(a => { const t = clamp((now - a.t0) / a.dur, 0, 1); if (now >= a.t0) a.f(t); return t < 1; });
    dirty = true;
  }
  if (SIM.playing && SIM.res) {
    SIM.t = Math.min(SIM.res.tEnd, SIM.t + dt * SIM.speed);
    simApply();
    if (SIM.t >= SIM.res.tEnd) { play(false); toast(SIM.res.T <= 8 ? `Escenario completo en el mes ${nf(SIM.res.T, 1)}: cabe en los 8 meses.` : `Escenario completo en el mes ${nf(SIM.res.T, 1)}: ${nf(SIM.res.T - 8, 1)} meses después del plazo.`); writeHash(); }
  }
  if (SIM.on) { const k = .55 + .45 * Math.sin(now / 180); for (const c of D.civs) if (c.beam?.visible) c.beam.material.opacity = .45 + .45 * k; if (D.civs.some(c => c.beam?.visible)) dirty = true; }
  if (controls.update()) dirty = true;
  if (!dirty) return;
  dirty = false;
  renderer.render(scene, camera); lblR.render(scene, camera);
  if (needMeasure) measureLabels();
  if (now - lastDecl > 60 || !SIM.playing) { declutter(); lastDecl = now; }
  hud();
}
function hud() {
  const az = controls.getAzimuthalAngle();
  $('#compass svg').style.transform = `rotate(${az}rad)`;
  const st = $('#stage'), d = camera.position.distanceTo(controls.target), mpp = 2 * d * Math.tan(THREE.MathUtils.degToRad(camera.fov) / 2) / st.clientHeight;
  const L = [10, 20, 50, 100, 200, 500, 1000].find(l => l / mpp >= 60) || 1000;
  $('#scaleTxt').textContent = (L >= 1000 ? nf(L / 1000) + ' km' : L + ' m') ; $('#scaleBar').style.width = Math.round(L / mpp) + 'px';
  if (scene.fog) { scene.fog.near = d * .95 + 500; scene.fog.far = d * 2.4 + 1800; }
  const lod = d > (isMobile() ? 1200 : 1750) ? 'min' : d > (isMobile() ? 600 : 800) ? 'mid' : 'full';
  const lb = $('#lbls'); if (lb.dataset.lod !== lod) { lb.dataset.lod = lod; D.civs.forEach(c => { c.lw = c.lbl.element.offsetWidth; c.lh = c.lbl.element.offsetHeight; }); }
}
