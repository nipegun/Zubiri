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
import time
import sys

if os.geteuid() != 0:
  print("Este script necesita privilegios de superusuario (sudo).")
  os.execvp("sudo", ["sudo"] + ["python3"] + sys.argv)

vArchivoDeEstados = "states.json"
vPuertoS7 = 102
vPuertoWeb = 8000

# Cerrar cualquier socket abierto previamente
def fCerrarSocketExistente(port):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as vSocketExistente:
    vSocketExistente.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
      vSocketExistente.bind(("0.0.0.0", port))
    except OSError:
      print(f"Cerrando socket en el puerto {port}...")
      os.system(f"fuser -k {port}/tcp")
      os.system(f"lsof -ti:{port} | xargs kill -9")

# Cerrar sockets abiertos antes de iniciar el servidor
fCerrarSocketExistente(vPuertoS7)
fCerrarSocketExistente(vPuertoWeb)

# Cargar estados desde el archivo si existe, si no, crearlo
if os.path.exists(vArchivoDeEstados):
  with open(vArchivoDeEstados, "r") as f:
    try:
      states = json.load(f)
    except json.JSONDecodeError:
      print(f"\n  Error: El archivo {vArchivoDeEstados} no es un JSON válido. Se creará de nuevo.")
      states = {}
else:
  states = {}

# Inicializar estados si están vacíos o no existen en el JSON
states.setdefault("outputs", {
  **{f"%Q0.{i}": "unknown" for i in range(8)},  # %Q0.0 a %Q0.7
  **{f"%Q1.{i}": "unknown" for i in range(2)}   # %Q1.0 a %Q1.1
})
states.setdefault("inputs", {
  **{f"%I0.{i}": "unknown" for i in range(8)},  # %I0.0 a %I0.7
  **{f"%I1.{i}": "unknown" for i in range(6)}   # %I1.0 a %I1.5
})
states.setdefault("analog_inputs", {f"%A0.{i}": "unknown" for i in range(2)})

# Guardar el JSON actualizado si se crearon valores nuevos
with open(vArchivoDeEstados, "w") as f:
  json.dump(states, f, indent=2)

# Mapeo de payloads finales a estados SOLO para outputs
dPayloadsFinales = {

  bytes.fromhex('0300004302f0807202003431000004f200000010000003ca00b4000034019077000801000004e88969001200000000896a001300896b00040000000000000072020000'): ("plc", "power_status", "off"),
  bytes.fromhex('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'): ("plc", "power_status", "on"),
  # '0300001e02f0807202000f32000004f20000001034000000000072020000' < Respuesta que se debe enviar al encender o apagar correctamente el PLC
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

# Sequencia específica de respuestas
# No se usa un diccionario simple sino que se implementará en la lógica del manejo de conexión

# Diccionario para almacenar estado de la comunicación por cliente
client_sessions = {}

# Depuración de hexadecimal a legible (donde sea posible)
def debug_hex(data):
  try:
    # Intenta decodificar como ASCII filtrando caracteres no imprimibles
    ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data)
    #return f"HEX: {data.hex()} | ASCII: {ascii_str}"
    return f"HEX: {data.hex()}"
  except:
    return f"HEX: {data.hex()}"

# Servidor de sockets mejorado
def fServirS7():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(("0.0.0.0", vPuertoS7))
  s.listen(5)
  print(f"\n  Simulador de PLC esperando conexiones en el puerto {vPuertoS7}...")

  while True:
    conn, addr = s.accept()
    client_id = f"{addr[0]}:{addr[1]}"

    # Inicializar sesión para nuevo cliente
    if client_id not in client_sessions:
      client_sessions[client_id] = {
        "sequence": [],
        "last_activity": time.time()
      }

    # Limpiar sesiones antiguas (más de 5 minutos sin actividad)
    current_time = time.time()
    for cid in list(client_sessions.keys()):
      if current_time - client_sessions[cid]["last_activity"] > 300:  # 5 minutos
        del client_sessions[cid]

    # Manejar la conexión en un hilo separado
    threading.Thread(target=fGestionarCliente, args=(conn, addr)).start()

def fGestionarCliente(conn, addr):
  client_id = f"{addr[0]}:{addr[1]}"
  print(f"\n  Nueva conexión desde {client_id}")

  # Inicializar o reiniciar la secuencia del cliente
  client_sessions[client_id]["sequence"] = []
  try:
    while True:
      data = conn.recv(1024)
      if not data:
        break

      # Actualizar tiempo de actividad
      client_sessions[client_id]["last_activity"] = time.time()

      # Registrar payload recibido en la secuencia del cliente
      client_sessions[client_id]["sequence"].append(data)

      # Depurar datos recibidos
      print(f"\n  [FROM {client_id}] {debug_hex(data)}")

      # Determinar respuesta según la secuencia exacta
      response = None
      sequence_position = len(client_sessions[client_id]["sequence"])

      # Primera posición en la secuencia
      if sequence_position == 1:
        if data   == bytes.fromhex('030000231ee00000006400c1020600c20f53494d415449432d524f4f542d4553c0010a'):
          response = bytes.fromhex('030000231ed00064000b00c0010ac1020600c20f53494d415449432d524f4f542d4553')
        else:
          print(f"  [TO {client_id}] Payload 1 no reconocido!")
          response = data  # Echo si no coincide

      # Segunda posición en la secuencia
      elif sequence_position == 2:
        if data   == bytes.fromhex('030000ee02f080720100df31000004ca0000000100000120360000011d00040000000000a1000000d3821f0000a3816900151553657276657253657373696f6e5f31433943333846a38221001532302e302e302e303a305265616c74656b20555342204762452046616d696c7920436f6e74726f6c6c65722e54435049502e33a38228001500a38229001500a3822a0015194445534b544f502d494e414d4455385f313432323331343036a3822b000401a3822c001201c9c38fa3822d001500a1000000d3817f0000a38169001515537562736372697074696f6e436f6e7461696e6572a2a20000000072010000'):
          response = bytes.fromhex('0300008902f0807201007a32000004ca0000000136110287248711a100000120821f0000a38169001500a3823200170000013a823b00048200823c00048140823d00048480c040823e00048480c040823f00151b313b36455337203231342d31414533302d30584230203b56322e328240001505323b37393482410003000300a20000000072010000')
        else:
          print(f"  [TO {client_id}] Payload 2 no reconocido!")
          response = data  # Echo si no coincide

      # Tercera posición en la secuencia
      elif sequence_position == 3:
        if data in dPayloadsFinales:
          category, key, state = dPayloadsFinales[data]
          states[category][key] = state
          # Guardar el cambio de estado en el archivo JSON
          with open(vArchivoDeEstados, "w") as f:
            json.dump(states, f, indent=2)
          print(f"  [STATE CHANGE] {category} {key} -> {state}")
          response = data  # Responder con eco para payloads finales
        else:
          response = bytes.fromhex('0300008f02f08072020080310000054200000002000003b834000003b8010182320100170000013a823b00048200823c00048140823d00048480c040823e00048480c040823f001500824000151a313b36455337203231342d31414533302d305842303b56322e328241000300030000000004e88969001200000000896a001300896b000400000000000072020000')

      # Cuarta posición en la secuencia
      elif sequence_position == 4:
        if data in dPayloadsFinales: # También verificar si es un payload que cambia estados
          category, key, state = dPayloadsFinales[data]
          states[category][key] = state

          # Guardar el cambio de estado en el archivo JSON
          with open(vArchivoDeEstados, "w") as f:
            json.dump(states, f, indent=2)

          print(f"  [STATE CHANGE] {category} {key} -> {state}")
          response = data  # Responder con eco para payloads finales
        else:
          print(f"  [TO {client_id}] Payload 4 no reconocido.")
          response = data  # Echo si no coincide

      # Verificar si es un payload final después de la secuencia
      elif data in dPayloadsFinales:
        category, key, state = dPayloadsFinales[data]
        states[category][key] = state

        # Guardar el cambio de estado en el archivo JSON
        with open(vArchivoDeEstados, "w") as f:
          json.dump(states, f, indent=2)

        print(f"  [STATE CHANGE] {category} {key} -> {state}")
        response = data  # Responder con eco para payloads finales

      # Si no es reconocido, responder con eco
      else:
        print(f"  [TO {client_id}] Payload no reconocido, respondiendo con eco")
        response = data

      # Enviar respuesta
      if response:
        print(f"  [TO {client_id}] {debug_hex(response)}")
        conn.sendall(response)

  except Exception as e:
    print(f"  [ERROR] Error en la conexión con {client_id}: {str(e)}")

  finally:
    conn.close()
    print(f"  Conexión cerrada con {client_id}")

# Servidor HTTP para servir el JSON correctamente
class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
  def do_GET(self):
    if self.path == "/states" or self.path == "/api/json":
      try:
        with open(vArchivoDeEstados, "r") as f:
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
    elif self.path == "/sessions":
      # Endpoint para mostrar las sesiones activas
      self.send_response(200)
      self.send_header("Content-type", "application/json")
      self.end_headers()

      # Preparar datos de sesiones para JSON
      session_data = {}
      for client_id, session in client_sessions.items():
        session_data[client_id] = {
          "last_activity": session["last_activity"],
          "sequence_count": len(session["sequence"]),
          "last_sequences": [seq.hex() for seq in session["sequence"][-5:]]  # Últimas 5 secuencias
        }

      self.wfile.write(json.dumps(session_data, indent=2).encode())
    else:
      super().do_GET()

# Iniciar servidores
if __name__ == "__main__":
  threading.Thread(target=fServirS7, daemon=True).start()
  httpd = http.server.ThreadingHTTPServer(("0.0.0.0", vPuertoWeb), SimpleHTTPRequestHandler)
  print(f"\n  Servidor web en http://localhost:{vPuertoWeb}")
  print(f"  Para ver estados: http://localhost:{vPuertoWeb}/states")
  print(f"  Para ver sesiones activas: http://localhost:{vPuertoWeb}/sessions\n")
  httpd.serve_forever()
