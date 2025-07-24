#!/usr/bin/env python3

# Pongo a disposición pública este script bajo el término de "software de dominio público".
# Puedes hacer lo que quieras con él porque es libre de verdad; no libre con condiciones como las licencias GNU y otras patrañas similares.
# Si se te llena la boca hablando de libertad entonces hazlo realmente libre.
# No tienes que aceptar ningún tipo de términos de uso o licencia para utilizarlo o modificarlo porque va sin CopyLeft.

import os
import json
import socket
import asyncio
import threading
import time
import sys
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import uvicorn

if os.geteuid() != 0:
  print("Este script necesita privilegios de superusuario (sudo).")
  os.execvp("sudo", ["sudo"] + ["python3"] + sys.argv)

vArchivoDeEstados = "states.json"
vPuertoS7 = 102
vPuertoWeb = 8000
vEstados = {}
aWebSockets = set()
client_sessions = {}

# Inicializar estados
if os.path.exists(vArchivoDeEstados):
  with open(vArchivoDeEstados, "r") as f:
    try:
      vEstados = json.load(f)
    except json.JSONDecodeError:
      vEstados = {}
else:
  vEstados = {}

vEstados.setdefault("plc", {
  "power_status": "unknown",
  "firmware": "3.0"
})

vEstados.setdefault("digital_outputs", {
  "%Q0.0": "unknown",
  "%Q0.1": "unknown",
  "%Q0.2": "unknown",
  "%Q0.3": "unknown",
  "%Q0.4": "unknown",
  "%Q0.5": "unknown",
  "%Q0.6": "unknown",
  "%Q0.7": "unknown",
  "%Q1.0": "unknown",
  "%Q1.1": "unknown"
})

vEstados.setdefault("digital_inputs", {
  "%I0.0": "unknown",
  "%I0.1": "unknown",
  "%I0.2": "unknown",
  "%I0.3": "unknown",
  "%I0.4": "unknown",
  "%I0.5": "unknown",
  "%I0.6": "unknown",
  "%I0.7": "unknown",
  "%I1.0": "unknown",
  "%I1.1": "unknown",
  "%I1.2": "unknown",
  "%I1.3": "unknown",
  "%I1.4": "unknown",
  "%I1.5": "unknown"
})

vEstados.setdefault("analog_inputs", {
  "%A0.0": "unknown",
  "%A0.1": "unknown"
})


with open(vArchivoDeEstados, "w") as f:
  json.dump(vEstados, f, indent=2)

# Payloads finales para encendido o apagado
vPayloadFinalOn  = bytes.fromhex('0300004302f0807202003431000004f200000010000003ca00b4000034019077000803000004e88969001200000000896a001300896b00040000000000000072020000')
vPayloadFinalOff = bytes.fromhex('0300004302f0807202003431000004f200000010000003ca00b4000034019077000801000004e88969001200000000896a001300896b00040000000000000072020000')
# '0300001e02f0807202000f32000004f20000001034000000000072020000' < Respuesta que se debe enviar al encender o apagar correctamente el PLC

dPayloadsFinalesDigitalOutputs = {

  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000000000300010100'): ("digital_outputs", "%Q0.0", "on"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000001000300010100'): ("digital_outputs", "%Q0.1", "on"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000002000300010100'): ("digital_outputs", "%Q0.2", "on"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000003000300010100'): ("digital_outputs", "%Q0.3", "on"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000004000300010100'): ("digital_outputs", "%Q0.4", "on"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000005000300010100'): ("digital_outputs", "%Q0.5", "on"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000006000300010100'): ("digital_outputs", "%Q0.6", "on"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000007000300010100'): ("digital_outputs", "%Q0.7", "on"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000008000300010100'): ("digital_outputs", "%Q1.0", "on"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000009000300010100'): ("digital_outputs", "%Q1.1", "on"),

  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000000000300010000'): ("digital_outputs", "%Q0.0", "off"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000001000300010000'): ("digital_outputs", "%Q0.1", "off"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000002000300010000'): ("digital_outputs", "%Q0.2", "off"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000003000300010000'): ("digital_outputs", "%Q0.3", "off"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000004000300010000'): ("digital_outputs", "%Q0.4", "off"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000005000300010000'): ("digital_outputs", "%Q0.5", "off"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000006000300010000'): ("digital_outputs", "%Q0.6", "off"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000007000300010000'): ("digital_outputs", "%Q0.7", "off"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000008000300010000'): ("digital_outputs", "%Q1.0", "off"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000009000300010000'): ("digital_outputs", "%Q1.1", "off")

}

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def leer_index():
  return FileResponse("static/index.html")

@app.get("/api/states")
def obtener_estados():
  return JSONResponse(content=vEstados)

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

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
  await ws.accept()
  aWebSockets.add(ws)
  try:
    await ws.send_text(json.dumps(vEstados))
    while True:
      await ws.receive_text()
  except:
    pass
  finally:
    aWebSockets.discard(ws)

async def fEnviarEstadoATodos():
  mensaje = json.dumps(vEstados)
  vivos = set()
  for ws in list(aWebSockets):
    try:
      await ws.send_text(mensaje)
      vivos.add(ws)
    except:
      pass
  aWebSockets.clear()
  aWebSockets.update(vivos)

async def fActualizarEstado(tipo, clave, valor):
  vEstados[tipo][clave] = valor
  with open(vArchivoDeEstados, "w") as f:
    json.dump(vEstados, f, indent=2)
  await fEnviarEstadoATodos()

def debug_hex(data):
  try:
    return f"HEX: {data.hex()}"
  except:
    return str(data)

def fServirS7():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(("0.0.0.0", vPuertoS7))
  s.listen(5)
  print(f"\n  Simulador de PLC esperando conexiones en el puerto {vPuertoS7}...")

  while True:
    conn, addr = s.accept()
    client_id = f"{addr[0]}:{addr[1]}"
    if client_id not in client_sessions:
      client_sessions[client_id] = {"sequence": [], "last_activity": time.time()}

    threading.Thread(target=fGestionarCliente, args=(conn, addr), daemon=True).start()

def fGestionarCliente(conn, addr):
  client_id = f"{addr[0]}:{addr[1]}"
  client_sessions[client_id]["sequence"] = []
  try:
    while True:
      data = conn.recv(1024)
      print(f"---------------------------------------------")
      print(f"\n  Conexión abierta con {client_id}")
      if not data:
        break

      client_sessions[client_id]["last_activity"] = time.time()
      client_sessions[client_id]["sequence"].append(data)
      print(f"\n  [FROM {client_id}] {debug_hex(data)}")

      response = None
      if data in dPayloadsFinalesDigitalOutputs:
        tipo, clave, valor = dPayloadsFinalesDigitalOutputs[data]
        asyncio.run(fActualizarEstado(tipo, clave, valor))
        response = data
      elif data in [vPayloadFinalOff]:
        asyncio.run(fActualizarEstado("plc", "power_status", "off"))
        asyncio.run(fActualizarEstado("digital_outputs", "%Q0.0", "unknown"))
        asyncio.run(fActualizarEstado("digital_outputs", "%Q0.1", "unknown"))
        asyncio.run(fActualizarEstado("digital_outputs", "%Q0.2", "unknown"))
        asyncio.run(fActualizarEstado("digital_outputs", "%Q0.3", "unknown"))
        asyncio.run(fActualizarEstado("digital_outputs", "%Q0.4", "unknown"))
        asyncio.run(fActualizarEstado("digital_outputs", "%Q0.5", "unknown"))
        asyncio.run(fActualizarEstado("digital_outputs", "%Q0.6", "unknown"))
        asyncio.run(fActualizarEstado("digital_outputs", "%Q0.7", "unknown"))
        asyncio.run(fActualizarEstado("digital_outputs", "%Q1.0", "unknown"))
        asyncio.run(fActualizarEstado("digital_outputs", "%Q1.1", "unknown"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I0.0", "unknown"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I0.1", "unknown"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I0.2", "unknown"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I0.3", "unknown"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I0.4", "unknown"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I0.5", "unknown"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I0.6", "unknown"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I0.7", "unknown"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I1.0", "unknown"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I1.1", "unknown"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I1.2", "unknown"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I1.3", "unknown"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I1.4", "unknown"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I1.5", "unknown"))
        asyncio.run(fActualizarEstado("analog_inputs", "%A0.0", "unknown"))
        asyncio.run(fActualizarEstado("analog_inputs", "%A0.1", "unknown"))
        response = data
      elif data in [vPayloadFinalOn]:
        asyncio.run(fActualizarEstado("plc", "power_status", "on"))
        asyncio.run(fActualizarEstado("digital_outputs", "%Q0.0", "off"))
        asyncio.run(fActualizarEstado("digital_outputs", "%Q0.1", "off"))
        asyncio.run(fActualizarEstado("digital_outputs", "%Q0.2", "off"))
        asyncio.run(fActualizarEstado("digital_outputs", "%Q0.3", "off"))
        asyncio.run(fActualizarEstado("digital_outputs", "%Q0.4", "off"))
        asyncio.run(fActualizarEstado("digital_outputs", "%Q0.5", "off"))
        asyncio.run(fActualizarEstado("digital_outputs", "%Q0.6", "off"))
        asyncio.run(fActualizarEstado("digital_outputs", "%Q0.7", "off"))
        asyncio.run(fActualizarEstado("digital_outputs", "%Q1.0", "off"))
        asyncio.run(fActualizarEstado("digital_outputs", "%Q1.1", "off"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I0.0", "off"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I0.1", "off"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I0.2", "off"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I0.3", "off"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I0.4", "off"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I0.5", "off"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I0.6", "off"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I0.7", "off"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I1.0", "off"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I1.1", "off"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I1.2", "off"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I1.3", "off"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I1.4", "off"))
        asyncio.run(fActualizarEstado("digital_inputs", "%I1.5", "off"))
        asyncio.run(fActualizarEstado("analog_inputs", "%A0.0", "off"))
        asyncio.run(fActualizarEstado("analog_inputs", "%A0.1", "off"))
        response = data
      else:
        response = data

      conn.sendall(response)
  except Exception as e:
    print(f"  [ERROR] Error en la conexión con {client_id}: {str(e)}")
  finally:
    conn.close()
    print(f"\n  Conexión cerrada con {client_id}")
    print(f"---------------------------------------------")

if __name__ == "__main__":
  threading.Thread(target=fServirS7, daemon=True).start()
  uvicorn.run(app, host="0.0.0.0", port=vPuertoWeb)
