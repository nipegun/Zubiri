// 3d.js - Visualización 3D del PLC Siemens S7-1214C usando Three.js

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader }    from 'three/addons/loaders/GLTFLoader.js';

// ── Escena, cámara, renderer ────────────────────────────────────────

const canvas   = document.getElementById('canvas3d');
const scene    = new THREE.Scene();
scene.background = new THREE.Color(0x1a1a2e);
scene.fog = new THREE.Fog(0x1a1a2e, 20, 40);

const camera   = new THREE.PerspectiveCamera(45, innerWidth / innerHeight, 0.1, 100);
camera.position.set(0, 3, 10);

const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setSize(innerWidth, innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type    = THREE.PCFSoftShadowMap;
renderer.toneMapping       = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;

const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.target.set(0, 1.2, 0);
controls.minDistance = 4;
controls.maxDistance = 20;

// ── Luces ───────────────────────────────────────────────────────────

const ambientLight = new THREE.AmbientLight(0x404060, 0.6);
scene.add(ambientLight);

const mainLight = new THREE.DirectionalLight(0xffffff, 1.2);
mainLight.position.set(5, 8, 6);
mainLight.castShadow = true;
mainLight.shadow.mapSize.set(2048, 2048);
mainLight.shadow.camera.near = 0.5;
mainLight.shadow.camera.far  = 25;
mainLight.shadow.camera.left = mainLight.shadow.camera.bottom = -8;
mainLight.shadow.camera.right = mainLight.shadow.camera.top = 8;
scene.add(mainLight);

const fillLight = new THREE.DirectionalLight(0x8888ff, 0.3);
fillLight.position.set(-4, 3, -3);
scene.add(fillLight);

const rimLight = new THREE.DirectionalLight(0xff8844, 0.2);
rimLight.position.set(0, 2, -5);
scene.add(rimLight);

// ── Suelo ───────────────────────────────────────────────────────────

const floorGeo = new THREE.PlaneGeometry(30, 30);
const floorMat = new THREE.MeshStandardMaterial({ color: 0x222233, roughness: 0.8 });
const floor    = new THREE.Mesh(floorGeo, floorMat);
floor.rotation.x = -Math.PI / 2;
floor.receiveShadow = true;
scene.add(floor);

// Grid
const grid = new THREE.GridHelper(30, 30, 0x333355, 0x222244);
grid.position.y = 0.01;
scene.add(grid);

// ── Grupo principal del PLC ─────────────────────────────────────────

const plcGroup = new THREE.Group();
plcGroup.position.y = 0.35;
scene.add(plcGroup);

// ── Dimensiones del modelo (se actualizan al cargar el GLB) ─────────

let W = 4.4;
let H = 6.0;
let D = 3.0;
let vFrontZ = D / 2;

// ── Colores de estado de los LEDs ───────────────────────────────────

const colorOn      = new THREE.Color(0x00ff88);
const colorOff     = new THREE.Color(0xff2222);
const colorApagado = new THREE.Color(0x333333);
const ledRadius    = 0.06;

function crearLedMaterial(color) {
  return new THREE.MeshStandardMaterial({
    color: color,
    emissive: color,
    emissiveIntensity: 0.8,
    roughness: 0.3,
    metalness: 0.1
  });
}

function colorPorEstado(estado) {
  if (estado === 'on')  return colorOn;
  if (estado === 'off') return colorOff;
  return colorApagado;
}

function actualizarLed(led, estado) {
  if (!led) return;
  const color = colorPorEstado(estado);
  led.mat.color.copy(color);
  led.mat.emissive.copy(color);
  if (estado === 'on') {
    led.mat.emissiveIntensity = 1.5;
  } else if (estado === 'off') {
    led.mat.emissiveIntensity = 0.6;
  } else {
    led.mat.emissiveIntensity = 0.0;
  }

  led.glowMat.color.copy(color);
  led.glowMat.opacity = estado === 'on' ? 0.25 : 0;
}

// ── Preparar un LED del modelo CAD para animación ───────────────────

function fPrepararLed(pMesh, pLocalPos) {
  // Reemplazar material original por uno emisivo
  const mat = crearLedMaterial(colorApagado);
  pMesh.material = mat;

  // Crear esfera de glow en la misma posición (en coordenadas de plcGroup)
  const glowGeo = new THREE.SphereGeometry(ledRadius * 2.5, 12, 12);
  const glowMat = new THREE.MeshBasicMaterial({
    color: colorApagado,
    transparent: true,
    opacity: 0.0
  });
  const glow = new THREE.Mesh(glowGeo, glowMat);
  glow.position.copy(pLocalPos);
  plcGroup.add(glow);

  return { mesh: pMesh, mat, glow, glowMat };
}

// ── Etiquetas en el panel frontal ───────────────────────────────────

function crearEtiquetaCanvas(texto, fontSize, width, height) {
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = 'transparent';
  ctx.fillRect(0, 0, width, height);
  ctx.fillStyle = '#ffffff';
  ctx.font = `${fontSize}px monospace`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(texto, width / 2, height / 2);

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  return texture;
}

function crearEtiqueta3D(texto, x, y, z, scaleX, scaleY) {
  const texture = crearEtiquetaCanvas(texto, 48, 512, 64);
  const geo = new THREE.PlaneGeometry(scaleX, scaleY);
  const mat = new THREE.MeshBasicMaterial({ map: texture, transparent: true });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.position.set(x, y, z);
  plcGroup.add(mesh);
  return mesh;
}

// ── Variables de LEDs (se asignan tras cargar el modelo) ────────────

let ledPower = null;
let ledRun   = null;
let ledStop  = null;
const ledsOutputs = [];
const ledsInputs  = [];
let vLedsCreados  = false;

// ── Crear etiquetas posicionadas según los LEDs del modelo ──────────

function crearEtiquetas() {
  const labelZ = vFrontZ + 0.06;

  // Etiquetas de LEDs de estado (posicionadas según los LEDs reales del modelo)
  if (ledPower) {
    crearEtiqueta3D('RUN/STOP', ledPower.glow.position.x, ledPower.glow.position.y - 0.13, labelZ, 0.5, 0.1);
  }
  if (ledRun) {
    crearEtiqueta3D('ERROR',    ledRun.glow.position.x,   ledRun.glow.position.y - 0.13,   labelZ, 0.4, 0.1);
  }
  if (ledStop) {
    crearEtiqueta3D('MAINT',    ledStop.glow.position.x,  ledStop.glow.position.y - 0.13,  labelZ, 0.4, 0.1);
  }

  // Etiquetas de salidas digitales
  if (ledsOutputs.length > 0) {
    const outputY = ledsOutputs[0].glow.position.y;
    crearEtiqueta3D('SALIDAS DIGITALES  %Q0.0 - %Q1.1', 0, outputY + 0.18, labelZ, 3.8, 0.12);

    const outputNames = ['Q0.0','Q0.1','Q0.2','Q0.3','Q0.4','Q0.5','Q0.6','Q0.7','Q1.0','Q1.1'];
    for (let i = 0; i < ledsOutputs.length && i < outputNames.length; i++) {
      crearEtiqueta3D(outputNames[i], ledsOutputs[i].glow.position.x, outputY - 0.14, labelZ, 0.36, 0.08);
    }
  }

  // Etiquetas de entradas digitales
  if (ledsInputs.length > 0) {
    const inputY = ledsInputs[0].glow.position.y;
    crearEtiqueta3D('ENTRADAS DIGITALES  %I0.0 - %I1.5', 0, inputY + 0.18, labelZ, 3.8, 0.12);

    const inputNames = ['I0.0','I0.1','I0.2','I0.3','I0.4','I0.5','I0.6','I0.7','I1.0','I1.1','I1.2','I1.3','I1.4','I1.5'];
    for (let i = 0; i < ledsInputs.length && i < inputNames.length; i++) {
      crearEtiqueta3D(inputNames[i], ledsInputs[i].glow.position.x, inputY - 0.12, labelZ, 0.28, 0.07);
    }
  }
}

// ── Cargar modelo GLB ───────────────────────────────────────────────

const loader = new GLTFLoader();
loader.load('/static/SiemensS7-1214C.glb', (gltf) => {
  const model = gltf.scene;

  // Calcular bounding box del modelo
  const box    = new THREE.Box3().setFromObject(model);
  const size   = box.getSize(new THREE.Vector3());
  const center = box.getCenter(new THREE.Vector3());

  // Escalar para que el ancho sea ~4.4 unidades
  const vTargetWidth = 4.4;
  const vScale = vTargetWidth / size.x;
  model.scale.setScalar(vScale);

  // Actualizar dimensiones globales
  W = size.x * vScale;
  H = size.y * vScale;
  D = size.z * vScale;

  // Centrar el modelo en X y Z, con base en Y=0
  model.position.set(
    -center.x * vScale,
    -box.min.y * vScale,
    -center.z * vScale
  );

  // Cara frontal (Z máximo tras centrar)
  vFrontZ = (box.max.z - center.z) * vScale;

  // Habilitar sombras en todas las mallas del modelo
  model.traverse((child) => {
    if (child.isMesh) {
      child.castShadow = true;
      child.receiveShadow = true;
    }
  });

  plcGroup.add(model);

  // ── Encontrar LEDs del modelo CAD ─────────────────────────────────

  // Convertir punto en espacio del modelo a coordenadas locales del plcGroup
  function fModelToLocal(p) {
    return new THREE.Vector3(
      p.x * vScale + model.position.x,
      p.y * vScale + model.position.y,
      p.z * vScale + model.position.z
    );
  }

  // Buscar mallas pequeñas con material gris claro (LEDs del CAD)
  const aLedCandidates = [];
  model.traverse((child) => {
    if (!child.isMesh) return;

    child.geometry.computeBoundingBox();
    const meshBox    = child.geometry.boundingBox;
    const meshSize   = new THREE.Vector3();
    meshBox.getSize(meshSize);
    const meshCenter = new THREE.Vector3();
    meshBox.getCenter(meshCenter);

    // Criterio LED: cuadrado pequeño (~1.5x1.5mm), material gris claro (~[0.78, 0.78, 0.81])
    if (meshSize.x > 0.5 && meshSize.x < 3.0 && meshSize.y > 0.5 && meshSize.y < 3.0 && meshSize.z < 2.0) {
      const mat = child.material;
      if (mat && mat.color) {
        const r = mat.color.r, g = mat.color.g, b = mat.color.b;
        if (r > 0.7 && r < 0.9 && g > 0.7 && g < 0.9 && b > 0.7 && b < 0.9) {
          aLedCandidates.push({
            mesh: child,
            modelCenter: meshCenter.clone(),
            localPos: fModelToLocal(meshCenter)
          });
        }
      }
    }
  });

  // Agrupar por posición Y en espacio del modelo
  // Fila superior Y≈63 (entradas + estado), Fila inferior Y≈37 (salidas)
  const aTopRow    = aLedCandidates.filter(l => l.modelCenter.y > 60 && l.modelCenter.y < 66);
  const aBottomRow = aLedCandidates.filter(l => l.modelCenter.y > 35 && l.modelCenter.y < 40);

  // Ordenar por X dentro de cada grupo
  aTopRow.sort((a, b) => a.modelCenter.x - b.modelCenter.x);
  aBottomRow.sort((a, b) => a.modelCenter.x - b.modelCenter.x);

  // Fila superior: LEDs de estado (X negativo) + LEDs de entradas (X positivo)
  const aStatusLeds = aTopRow.filter(l => l.modelCenter.x < 0);
  const aInputLeds  = aTopRow.filter(l => l.modelCenter.x > 0);

  // Fila inferior: LEDs de salidas (primeros 10 usables, los 4 restantes no se usan)
  const aOutputLeds = aBottomRow;

  console.log(`LEDs encontrados: ${aStatusLeds.length} estado, ${aOutputLeds.length} salidas, ${aInputLeds.length} entradas`);

  // Mapear LEDs de estado: ordenados por X [0]=RUN/STOP, [1]=ERROR, [2]=MAINT
  if (aStatusLeds.length >= 3) {
    ledPower = fPrepararLed(aStatusLeds[0].mesh, aStatusLeds[0].localPos);
    ledRun   = fPrepararLed(aStatusLeds[1].mesh, aStatusLeds[1].localPos);
    ledStop  = fPrepararLed(aStatusLeds[2].mesh, aStatusLeds[2].localPos);
  }

  // Mapear LEDs de salidas (fila inferior): primeros 8 = Q0.0-Q0.7, tras hueco primeros 2 = Q1.0-Q1.1
  // Los 4 restantes (índices 10-13) no se usan en el 1214C
  for (let i = 0; i < Math.min(aOutputLeds.length, 10); i++) {
    ledsOutputs.push(fPrepararLed(aOutputLeds[i].mesh, aOutputLeds[i].localPos));
  }

  // Mapear LEDs de entradas (fila superior): 14 = I0.0-I0.7 + I1.0-I1.5
  for (let i = 0; i < Math.min(aInputLeds.length, 14); i++) {
    ledsInputs.push(fPrepararLed(aInputLeds[i].mesh, aInputLeds[i].localPos));
  }

  vLedsCreados = true;

  // Crear etiquetas posicionadas según los LEDs reales del modelo
  crearEtiquetas();

  // Aplicar estado pendiente si el WebSocket ya envió datos
  if (vEstadoActual) {
    aplicarEstados(vEstadoActual);
  }

  // Ajustar cámara y controles al tamaño del modelo
  controls.target.set(0, H / 2, 0);
  camera.position.set(0, H / 2, H * 1.8);
  controls.update();

  console.log(`Modelo GLB cargado: ${W.toFixed(2)} x ${H.toFixed(2)} x ${D.toFixed(2)}, frente Z=${vFrontZ.toFixed(2)}`);

}, (xhr) => {
  if (xhr.lengthComputable) {
    console.log(`Cargando modelo: ${(xhr.loaded / xhr.total * 100).toFixed(0)}%`);
  }
}, (error) => {
  console.error('Error cargando modelo GLB:', error);
});

// ── WebSocket ───────────────────────────────────────────────────────

let vEstadoActual = null;

const wsURL = (location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host + '/ws';

function conectarWebSocket() {
  const ws = new WebSocket(wsURL);

  ws.onopen = () => console.log('WebSocket 3D conectado');

  ws.onmessage = (event) => {
    try {
      vEstadoActual = JSON.parse(event.data);
      aplicarEstados(vEstadoActual);
    } catch (e) {
      console.error('Error parseando estado:', e);
    }
  };

  ws.onclose = () => {
    console.warn('WebSocket cerrado. Reconectando en 3s...');
    setTimeout(conectarWebSocket, 3000);
  };

  ws.onerror = () => ws.close();
}

function aplicarEstados(estados) {
  if (!vLedsCreados) return;

  // RUN/STOP (primer LED de estado): verde si encendido, apagado si no
  const power = estados.plc?.power_status || 'unknown';
  actualizarLed(ledPower, power === 'on' ? 'on' : 'apagado');

  // ERROR y MAINT: apagados siempre (se activarían por condiciones específicas)
  actualizarLed(ledRun,  'apagado');
  actualizarLed(ledStop, 'apagado');

  // Salidas digitales: verde=on, rojo=off, apagado=unknown/plc apagado
  const outputs = estados.digital_outputs || {};
  const outputKeys = ['%Q0.0','%Q0.1','%Q0.2','%Q0.3','%Q0.4','%Q0.5','%Q0.6','%Q0.7','%Q1.0','%Q1.1'];
  for (let i = 0; i < outputKeys.length && i < ledsOutputs.length; i++) {
    const vEstado = outputs[outputKeys[i]] || 'unknown';
    actualizarLed(ledsOutputs[i], vEstado === 'unknown' ? 'apagado' : vEstado);
  }

  // Entradas digitales: verde=on, rojo=off, apagado=unknown/plc apagado
  const inputs = estados.digital_inputs || {};
  const inputKeys = ['%I0.0','%I0.1','%I0.2','%I0.3','%I0.4','%I0.5','%I0.6','%I0.7','%I1.0','%I1.1','%I1.2','%I1.3','%I1.4','%I1.5'];
  for (let i = 0; i < inputKeys.length && i < ledsInputs.length; i++) {
    const vEstado = inputs[inputKeys[i]] || 'unknown';
    actualizarLed(ledsInputs[i], vEstado === 'unknown' ? 'apagado' : vEstado);
  }

  // Actualizar HUD
  actualizarHUD(estados);
}

function actualizarHUD(estados) {
  const power = estados.plc?.power_status || 'unknown';
  const hudPower = document.getElementById('hud-power');
  const dotClass = power === 'on' ? 'on' : (power === 'off' ? 'off' : 'unknown');
  hudPower.innerHTML = `<span class="dot ${dotClass}"></span> Corriente: ${power.toUpperCase()}`;

  // Contar salidas activas
  const outputs = estados.digital_outputs || {};
  const onOutputs = Object.values(outputs).filter(v => v === 'on').length;
  const totalOutputs = Object.keys(outputs).length;
  document.getElementById('hud-outputs').textContent = `Salidas: ${onOutputs}/${totalOutputs} activas`;

  // Contar entradas activas
  const inputs = estados.digital_inputs || {};
  const onInputs = Object.values(inputs).filter(v => v === 'on').length;
  const totalInputs = Object.keys(inputs).length;
  document.getElementById('hud-inputs').textContent = `Entradas: ${onInputs}/${totalInputs} activas`;
}

// ── Animación ───────────────────────────────────────────────────────

let time = 0;

function animate() {
  requestAnimationFrame(animate);
  time += 0.016;

  controls.update();

  // Pulso sutil en LEDs encendidos
  if (vEstadoActual && vLedsCreados) {
    const pulse = 0.85 + 0.15 * Math.sin(time * 3);
    ledsOutputs.forEach((led, i) => {
      const keys = ['%Q0.0','%Q0.1','%Q0.2','%Q0.3','%Q0.4','%Q0.5','%Q0.6','%Q0.7','%Q1.0','%Q1.1'];
      const estado = vEstadoActual.digital_outputs?.[keys[i]];
      if (estado === 'on') {
        led.mat.emissiveIntensity = 1.0 + 0.5 * pulse;
        led.glowMat.opacity = 0.15 + 0.1 * pulse;
      }
    });

    // Pulso en LED power si encendido
    const power = vEstadoActual.plc?.power_status;
    if (power === 'on' && ledPower) {
      ledPower.mat.emissiveIntensity = 1.0 + 0.5 * (0.85 + 0.15 * Math.sin(time * 2));
    }
  }

  renderer.render(scene, camera);
}

// ── Resize ──────────────────────────────────────────────────────────

window.addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
});

// ── Iniciar ─────────────────────────────────────────────────────────

conectarWebSocket();
animate();
