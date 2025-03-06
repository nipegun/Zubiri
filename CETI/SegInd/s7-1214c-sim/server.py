#!/usr/bin/env python3

# Pongo a disposición pública este script bajo el término de "software de dominio público".
# Puedes hacer lo que quieras con él porque es libre de verdad; no libre con condiciones como las licencias GNU y otras patrañas similares.
# Si se te llena la boca hablando de libertad entonces hazlo realmente libre.
# No tienes que aceptar ningún tipo de términos de uso o licencia para utilizarlo o modificarlo porque va sin CopyLeft.

import socket
import http.server
import threading
import json
import os
import asyncio
import websockets

STATES_FILE = "states.json"

# Cargar estados desde el archivo si existe, si no, crearlo
if os.path.exists(STATES_FILE):
  with open(STATES_FILE, "r") as f:
    try:
      states = json.load(f)
    except json.JSONDecodeError:
      print("Error: El archivo states.json no es un JSON válido. Se creará de nuevo.")
      states = {
        "outputs": {f"%Q0.{i}": "unknown" for i in range(10)}
      }
      with open(STATES_FILE, "w") as f:
        json.dump(states, f, indent=2)
else:
  states = {
    "outputs": {f"%Q0.{i}": "unknown" for i in range(10)}
  }
  with open(STATES_FILE, "w") as f:
    json.dump(states, f, indent=2)

# Mapeo de payloads a estados SOLO para outputs
payload_mapping = {
  '0300002502f08032010000001f000e00060501120a10010001000082000000000300010100': ("%Q0.0", "on"),
  '0300002502f08032010000001f000e00060501120a10010001000082000001000300010100': ("%Q0.1", "on"),
  '0300002502f08032010000001f000e00060501120a10010001000082000002000300010100': ("%Q0.2", "on"),
  '0300002502f08032010000001f000e00060501120a10010001000082000003000300010100': ("%Q0.3", "on"),
  '0300002502f08032010000001f000e00060501120a10010001000082000004000300010100': ("%Q0.4", "on"),
  '0300002502f08032010000001f000e00060501120a10010001000082000005000300010100': ("%Q0.5", "on"),
  '0300002502f08032010000001f000e00060501120a10010001000082000006000300010100': ("%Q0.6", "on"),
  '0300002502f08032010000001f000e00060501120a10010001000082000007000300010100': ("%Q0.7", "on"),
  '0300002502f08032010000001f000e00060501120a10010001000082000008000300010100': ("%Q0.8", "on"),
  '0300002502f08032010000001f000e00060501120a10010001000082000009000300010100': ("%Q0.9", "on"),

  '0300002502f08032010000001f000e00060501120a10010001000082000000000300010000': ("%Q0.0", "off"),
  '0300002502f08032010000001f000e00060501120a10010001000082000001000300010000': ("%Q0.1", "off"),
  '0300002502f08032010000001f000e00060501120a10010001000082000002000300010000': ("%Q0.2", "off"),
  '0300002502f08032010000001f000e00060501120a10010001000082000003000300010000': ("%Q0.3", "off"),
  '0300002502f08032010000001f000e00060501120a10010001000082000004000300010000': ("%Q0.4", "off"),
  '0300002502f08032010000001f000e00060501120a10010001000082000005000300010000': ("%Q0.5", "off"),
  '0300002502f08032010000001f000e00060501120a10010001000082000006000300010000': ("%Q0.6", "off"),
  '0300002502f08032010000001f000e00060501120a10010001000082000007000300010000': ("%Q0.7", "off"),
  '0300002502f08032010000001f000e00060501120a10010001000082000008000300010000': ("%Q0.8", "off"),
  '0300002502f08032010000001f000e00060501120a10010001000082000009000300010000': ("%Q0.9", "off")
}

# Lista de clientes WebSocket
clients = set()

async def websocket_handler(websocket, path):
  clients.add(websocket)
  try:
    async for message in websocket:
      pass  # No necesitamos recibir mensajes del cliente
  finally:
    clients.remove(websocket)

# Servidor de sockets
def socket_server():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(("0.0.0.0", 12345))
  s.listen(5)
  print("Servidor de sockets esperando conexiones en el puerto 12345...")

  while True:
    conn, addr = s.accept()
    data = conn.recv(1024).decode().strip()
    print(f"Datos recibidos: {data}")

    if data in payload_mapping:
      key, state = payload_mapping[data]
      states["outputs"][key] = state

      with open(STATES_FILE, "w") as f:
        json.dump(states, f, indent=2)

      # Enviar actualización a todos los clientes WebSocket
      asyncio.run(broadcast(data))

    conn.close()

async def broadcast(message):
  if clients:
    await asyncio.gather(*(client.send(message) for client in clients))

# Iniciar servidores
if __name__ == "__main__":
  threading.Thread(target=socket_server, daemon=True).start()

  start_server = websockets.serve(websocket_handler, "0.0.0.0", 8001)
  asyncio.get_event_loop().run_until_complete(start_server)
  asyncio.get_event_loop().run_forever()
