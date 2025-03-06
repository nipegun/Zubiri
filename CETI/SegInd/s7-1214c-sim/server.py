#!/usr/bin/env python3

# Pongo a disposición pública este script bajo el término de "software de dominio público".
# Puedes hacer lo que quieras con él porque es libre de verdad; no libre con condiciones como las licencias GNU y otras patrañas similares.
# Si se te llena la boca hablando de libertad entonces hazlo realmente libre.
# No tienes que aceptar ningún tipo de términos de uso o licencia para utilizarlo o modificarlo porque va sin CopyLeft.

import socket
import http.server
import threading
import json

STATES_FILE = "states.json"

# Estado inicial de todas las conexiones
states = {
  "outputs": {
    "%Q0.0": "unknown",
    "%Q0.1": "unknown",
    "%Q0.2": "unknown",
    "%Q0.3": "unknown",
    "%Q0.4": "unknown",
    "%Q0.5": "unknown",
    "%Q0.6": "unknown",
    "%Q0.7": "unknown",
    "%Q0.8": "unknown",
    "%Q0.9": "unknown"
  },
  "inputs": {
    "%I0.0": "unknown",
    "%I0.1": "unknown",
    "%I0.2": "unknown",
    "%I0.3": "unknown",
    "%I0.4": "unknown",
    "%I0.5": "unknown",
    "%I0.6": "unknown",
    "%I0.7": "unknown",
    "%I0.8": "unknown",
    "%I0.9": "unknown",
    "%I1.0": "unknown",
    "%I1.1": "unknown",
    "%I1.2": "unknown",
    "%I1.3": "unknown"
  },
  "analog_inputs": {
    "%AI0": "unknown",
    "%AI1": "unknown"
  }
}

# Guardar el estado inicial en el JSON
with open(STATES_FILE, "w") as f:
  json.dump(states, f, indent=2)

# Mapeo de payloads a estados SOLO para outputs
payload_mapping = {
  '0300002502f08032010000001f000e00060501120a10010001000082000000000300010100': ("outputs", "%Q0.0", "on"),
  '0300002502f08032010000001f000e00060501120a10010001000082000001000300010100': ("outputs", "%Q0.1", "on"),
  '0300002502f08032010000001f000e00060501120a10010001000082000002000300010100': ("outputs", "%Q0.2", "on"),
  '0300002502f08032010000001f000e00060501120a10010001000082000003000300010100': ("outputs", "%Q0.3", "on"),
  '0300002502f08032010000001f000e00060501120a10010001000082000004000300010100': ("outputs", "%Q0.4", "on"),
  '0300002502f08032010000001f000e00060501120a10010001000082000005000300010100': ("outputs", "%Q0.5", "on"),
  '0300002502f08032010000001f000e00060501120a10010001000082000006000300010100': ("outputs", "%Q0.6", "on"),
  '0300002502f08032010000001f000e00060501120a10010001000082000007000300010100': ("outputs", "%Q0.7", "on"),
  '0300002502f08032010000001f000e00060501120a10010001000082000008000300010100': ("outputs", "%Q0.8", "on"),
  '0300002502f08032010000001f000e00060501120a10010001000082000009000300010100': ("outputs", "%Q0.9", "on"),

  '0300002502f08032010000001f000e00060501120a10010001000082000000000300010000': ("outputs", "%Q0.0", "off"),
  '0300002502f08032010000001f000e00060501120a10010001000082000001000300010000': ("outputs", "%Q0.1", "off"),
  '0300002502f08032010000001f000e00060501120a10010001000082000002000300010000': ("outputs", "%Q0.2", "off"),
  '0300002502f08032010000001f000e00060501120a10010001000082000003000300010000': ("outputs", "%Q0.3", "off"),
  '0300002502f08032010000001f000e00060501120a10010001000082000004000300010000': ("outputs", "%Q0.4", "off"),
  '0300002502f08032010000001f000e00060501120a10010001000082000005000300010000': ("outputs", "%Q0.5", "off"),
  '0300002502f08032010000001f000e00060501120a10010001000082000006000300010000': ("outputs", "%Q0.6", "off"),
  '0300002502f08032010000001f000e00060501120a10010001000082000007000300010000': ("outputs", "%Q0.7", "off"),
  '0300002502f08032010000001f000e00060501120a10010001000082000008000300010000': ("outputs", "%Q0.8", "off"),
  '0300002502f08032010000001f000e00060501120a10010001000082000009000300010000': ("outputs", "%Q0.9", "off")
}

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
      category, key, state = payload_mapping[data]
      states[category][key] = state

      with open(STATES_FILE, "w") as f:
        json.dump(states, f, indent=2)

    conn.close()

# Servidor HTTP para servir el JSON
class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
  def do_GET(self):
    if self.path == "/states":
      with open(STATES_FILE, "r") as f:
        content = f.read()
      self.send_response(200)
      self.send_header("Content-type", "application/json")
      self.end_headers()
      self.wfile.write(content.encode())
    else:
      super().do_GET()

# Iniciar servidores
if __name__ == "__main__":
  threading.Thread(target=socket_server, daemon=True).start()
  
  httpd = http.server.ThreadingHTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
  print("Servidor web en http://localhost:8000")
  httpd.serve_forever()
