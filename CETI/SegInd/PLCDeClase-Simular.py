#!/usr/bin/env python3

# Pongo a disposición pública este script bajo el término de "software de dominio público".
# Puedes hacer lo que quieras con él porque es libre de verdad; no libre con condiciones como las licencias GNU y otras patrañas similares.
# Si se te llena la boca hablando de libertad entonces hazlo realmente libre.
# No tienes que aceptar ningún tipo de términos de uso o licencia para utilizarlo o modificarlo porque va sin CopyLeft.

# ----------
# Script de NiPeGun para interactuar con un PLC Siemens S7-1200, versión 1214c
#
# Ejecución remota (puede requerir permisos sudo):
#   wget -q -N --no-cache https://raw.githubusercontent.com/nipegun/zubiri/refs/heads/main/CETI/SegInd/PLCDeClase-Simular.py && python3 PLCDeClase-Simular.py
#
# Bajar y editar directamente el archivo en nano:
#   curl -sL https://raw.githubusercontent.com/nipegun/zubiri/refs/heads/main/CETI/SegInd/PLCDeClase-Simular.py | nano -
# ----------

import socket
import struct

# Definir constantes para colores
cColorAzul = '\033[0;34m'
cColorAzulClaro = '\033[1;34m'
cColorVerde = '\033[1;32m'
cColorRojo = '\033[1;31m'
cFinColor = '\033[0m'  # Vuelve al color normal

# Definir la memoria del PLC simulado
E = bytearray(2)   # Entradas digitales %I0.0 - %I0.13
A = bytearray(2)   # Salidas digitales %Q0.0 - %Q0.9
DB1 = bytearray(1024)  # Simula una DB interna del PLC

# Configurar el servidor TCP en el puerto 102 (S7comm)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 102))
server_socket.listen(1)

print(cColorAzulClaro + "\n  Simulador de PLC Siemens S7-1200 1214c escuchando en el puerto 102...\n" + cFinColor)

def handle_client(client_socket):
  """ Maneja la comunicación con un cliente S7 (TIA Portal, WinCC, SCADA). """
  try:
    while True:
      data = client_socket.recv(1024)
      if not data:
        break  # Desconexión del cliente

      # Solicitud de comunicación COTP para encendido/apagado del PLC
      # El cliente debe enviar algo como          '0300001611e00000000100c0010ac1020102c2020100c00109'
      # El servidor debe responder con algo como: '0300001611d00001000100c0010ac1020102c2020100c00109

      if data.hex() == '030000231ee00000006400c1020600c20f53494d415449432d524f4f542d4553c0010a':
        vTipoSolicitud = '(Solicitud de comunicación COTP para encendido/apagado del PLC).'
        print(f"      Envió: {data.hex()} " + vTipoSolicitud)
        response = b'\x03\x00\x00\x16\x11\xe0\x00\x00\x00\x01\x00\xc0\x01\x0a\xc1\x02\x01\x00\xc2\x02\x01\x02'
        client_socket.send(response)
        print("        Se le respondió: " + str(response.hex()))

      # Solicitud de comunicación s7comm
      if data.hex() == '030000ee02f080720100df31000004ca0000000100000120360000011d00040000000000a1000000d3821f0000a3816900151553657276657253657373':
        vTipoSolicitud = '(Solicitud de comunicación s7comm para encendido/apagado del PLC).'
        print(f"      Envió: {data.hex()} " + vTipoSolicitud)
        response = b'\x03\x00\x00\x16\x11\xe0\x00\x00\x00\x01\x00\xc0\x01\x0a\xc1\x02\x01\x00\xc2\x02\x01\x02'
        client_socket.send(response)
        print("        Se le respondió: " + str(response))


      # Solicitud de comunicación COTP para encendido/apagado de salida
      if data.hex() == '0300001611e00000cfc400c0010ac1020100c2020101':
        vTipoSolicitud = '(Solicitud de comunicación COTP para encendido/apagado de salida).'
        print(f"      Envió: {data.hex()} " + vTipoSolicitud)
        response = b'\x03\x00\x00\x16\x11\xe0\x00\x00\x00\x01\x00\xc0\x01\x0a\xc1\x02\x01\x00\xc2\x02\x01\x02'
        client_socket.send(response)
        print("        Se le respondió: " + str(response))

      # SETUP COMMUNICATION REQUEST (Configurar conexión S7)
      if data.startswith(b'\x03\x00\x00\x19\x02\xf0\x80\x32'):
        response = b'\x03\x00\x00\x1d\x02\xf0\x80\x32\x03\x00\x00\x01\x00\x01\xe0\x00\x00\x01\x00\x01\xe0\x00'
        client_socket.send(response)
        print("      Respondido: Setup Communication")

      # READ REQUEST - Cliente quiere leer memoria del PLC
      if data.startswith(b'\x03\x00\x00\x21\x02\xf0\x80\x32\x07'):
        address = data[-1]  # Último byte contiene la dirección
        
        if address == 0:
          response_data = E
        elif address == 1:
          response_data = A
        elif address == 2:
          response_data = DB1[:4]
        else:
          response_data = b'\x00'

        response = b'\x03\x00\x00\x25\x02\xf0\x80\x32\x07\x00\x00\x00\x04\xff\x04\x00\x00' + response_data
        client_socket.send(response)
        print(f"      Respondido: Datos de dirección {address}")

      # WRITE REQUEST - Cliente quiere escribir memoria del PLC
      elif data.startswith(b'\x03\x00\x00\x24\x02\xf0\x80\x32\x05'):
        address = data[-5]
        value = data[-1]
        
        if address == 0:
          E[0] = value
        elif address == 1:
          A[0] = value
        elif address == 2:
          DB1[:4] = struct.pack(">I", value)

        response = b'\x03\x00\x00\x1e\x02\xf0\x80\x32\x05\x00\x00\x00\x01\xff\x00'
        client_socket.send(response)
        print(f"      Respondido: Escritura en dirección {address} con valor {value}")
  
  except Exception as e:
    print(f"Error en comunicación: {e}")
  
  finally:
    client_socket.close()
    print(cColorRojo + "\n    Cliente desconectado.\n" + cFinColor)

# Aceptar conexiones de clientes
while True:
  client_socket, addr = server_socket.accept()
  print(cColorVerde + f"\n    Cliente conectado desde {addr}.\n" + cFinColor)
  handle_client(client_socket)

