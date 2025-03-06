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

STATES_FILE = "states.json"
PORT_SOCKET = 102
PORT_HTTP = 8000

# Mapeo de payloads a estados SOLO para outputs
payload_mapping = {
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000000000300010100'): ("outputs", "%Q0.0", "on"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000001000300010100'): ("outputs", "%Q0.1", "on"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000002000300010100'): ("outputs", "%Q0.2", "on"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000003000300010100'): ("outputs", "%Q0.3", "on"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000004000300010100'): ("outputs", "%Q0.4", "on"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000005000300010100'): ("outputs", "%Q0.5", "on"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000006000300010100'): ("outputs", "%Q0.6", "on"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000007000300010100'): ("outputs", "%Q0.7", "on"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000008000300010100'): ("outputs", "%Q1.0", "on"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000009000300010100'): ("outputs", "%Q1.1", "on"),

  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000000000300010000'): ("outputs", "%Q0.0", "off"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000001000300010000'): ("outputs", "%Q0.1", "off"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000002000300010000'): ("outputs", "%Q0.2", "off"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000003000300010000'): ("outputs", "%Q0.3", "off"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000004000300010000'): ("outputs", "%Q0.4", "off"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000005000300010000'): ("outputs", "%Q0.5", "off"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000006000300010000'): ("outputs", "%Q0.6", "off"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000007000300010000'): ("outputs", "%Q0.7", "off"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000008000300010000'): ("outputs", "%Q1.0", "off"),
  bytes.fromhex('0300002502f08032010000001f000e00060501120a10010001000082000009000300010000'): ("outputs", "%Q1.1", "off")
}

# Cerrar cualquier socket abierto previamente
def close_existing_socket(port):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
      s.bind(("0.0.0.0", port))
    except OSError:
      print(f"Cerrando socket en el puerto {port}...")
      os.system(f"fuser -k {port}/tcp")

# Cerrar sockets abiertos antes de iniciar el servidor
close_existing_socket(PORT_SOCKET)
close_existing_socket(PORT_HTTP)

# Cargar estados desde el archivo si existe, si no, crearlo
if os.path.exists(STATES_FILE):
  with open(STATES_FILE, "r") as f:
    try:
      states = json.load(f)
    except json.JSONDecodeError:
      print("\n  Error: El archivo states.json no es un JSON válido. Se creará de nuevo.")
      states = {}
else:
  states = {}

# Inicializar estados si están vacíos o no existen en el JSON
states.setdefault("outputs", {
  **{f"%Q0.{i}": "unknown" for i in range(8)},  # %Q0.0 a %Q0.7
  **{f"%Q1.{i}": "unknown" for i in range(2)}   # %Q1.0 a %Q1.1
})
states.setdefault("outputs", {
  **{f"%I0.{i}": "unknown" for i in range(8)},  # %I0.0 a %I0.7
  **{f"%I1.{i}": "unknown" for i in range(6)}   # %I1.0 a %I1.1
})
states.setdefault("analog_inputs", {f"%A0.{i}": "unknown" for i in range(2)})

# Guardar el JSON actualizado si se crearon valores nuevos
with open(STATES_FILE, "w") as f:
  json.dump(states, f, indent=2)

# Servidor de sockets
def socket_server():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(("0.0.0.0", PORT_SOCKET))
  s.listen(5)
  print("\n  Servidor de sockets esperando conexiones en el puerto 102...")

  while True:
    conn, addr = s.accept()
    data = conn.recv(1024)

    try:
      decoded_data = data.decode("utf-8").strip()
      print(f"Datos recibidos en texto: {decoded_data}")
    except UnicodeDecodeError:
      decoded_data = data.hex()
      print(f"Datos recibidos en binario (hex): {decoded_data}")
    
    binary_data = bytes.fromhex(decoded_data) if isinstance(decoded_data, str) else data

    if binary_data in payload_mapping:
      category, key, state = payload_mapping[binary_data]
      states[category][key] = state

      with open(STATES_FILE, "w") as f:
        json.dump(states, f, indent=2)
    
    conn.sendall(binary_data)  # Responder siempre en binario
    conn.close()

# Servidor HTTP para servir el JSON correctamente
class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
  def do_GET(self):
    if self.path == "/states" or self.path == "/api/json":
      try:
        with open(STATES_FILE, "r") as f:
          content = f.read()
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(content.encode())
      except Exception as e:
        self.send_response(500)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(f"\n  Error al leer states.json: {str(e)}".encode())
    else:
      super().do_GET()

# Iniciar servidores
if __name__ == "__main__":
  threading.Thread(target=socket_server, daemon=True).start()
  httpd = http.server.ThreadingHTTPServer(("0.0.0.0", PORT_HTTP), SimpleHTTPRequestHandler)
  print("\n  Servidor web en http://localhost:8000")
  httpd.serve_forever()
