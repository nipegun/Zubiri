#!/usr/bin/env python3

# Pongo a disposición pública este script bajo el término de "software de dominio público".
# Puedes hacer lo que quieras con él porque es libre de verdad; no libre con condiciones como las licencias GNU y otras patrañas similares.
# Si se te llena la boca hablando de libertad entonces hazlo realmente libre.
# No tienes que aceptar ningún tipo de términos de uso o licencia para utilizarlo o modificarlo porque va sin CopyLeft.

# ----------
# Script de NiPeGun para interactuar con un PLC Siemens S7-1200, versión 1214c
#
# Ejecución remota (puede requerir permisos sudo):
#   wget -O https://raw.githubusercontent.com/nipegun/zubiri/refs/heads/main/CETI/SegInd/PLCDeClase-Interactuar.py && python3 PLCDeClase-Interactuar.py [IPDelPLC]
#
# Bajar y editar directamente el archivo en nano:
#   curl -sL https://raw.githubusercontent.com/nipegun/zubiri/refs/heads/main/CETI/SegInd/PLCDeClase-Interactuar.py | nano -
# ----------

import curses
import time
import socket
import argparse
import sys
import io

# Definir constantes para colores
cColorAzul='\033[0;34m'
cColorAzulClaro='\033[1;34m'
cColorVerde='\033[1;32m'
cColorRojo='\033[1;31m'
cFinColor='\033[0m' # Vuelve al color normal

def fConectar(vHost):
  print(f"\n  Conectando a {vHost} en el puerto 102... \n")
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.settimeout(10)
  try:
    s.connect((vHost, 102))
    print("\n  Conexión establecida. \n")
    return s
  except socket.error as e:
    print(f"\n  Error al conectar con el PLC: {e} \n")
    return None

def fEnviarPayload(payload, con):
  print(f"\n  Enviando: {payload} \n")
  con.send(bytearray.fromhex(payload))
  try:
    data = con.recv(1024)
    if data:
      print(f"\n  Respuesta cruda del PLC: {data.hex()} \n")
    else:
      print("\n  No se recibió respuesta del PLC. \n")
    return data
  except socket.timeout:
    print("\n  Error: El PLC no respondió en el tiempo esperado. \n")
    return None

def print_output(stdscr, message):
  """ Función para imprimir mensajes en una ventana centrada en la pantalla. """
  height, width = stdscr.getmaxyx()
  output_win_height = 10
  output_win_width = width // 2
  start_y = (height // 2) - (output_win_height // 2)
  start_x = (width // 2) - (output_win_width // 2)

  output_win = curses.newwin(output_win_height, output_win_width, start_y, start_x)
  output_win.clear()
  output_win.border()

  output_lines = message.split("\n")[-(output_win_height - 4):]
  for i, line in enumerate(output_lines):
    output_win.addstr(i + 1, 2, line[:output_win_width - 4])

  output_win.addstr(len(output_lines) + 1, 2, " ")
  output_win.addstr(len(output_lines) + 2, 2, "Presiona una tecla para continuar...")
  output_win.addstr(len(output_lines) + 3, 2, " ")

  output_win.refresh()
  output_win.getch()
  output_win.clear()
  output_win.refresh()

def fMenu(stdscr, vHost):
  curses.curs_set(0)
  stdscr.keypad(True)
  curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

  menu = [
    "Encender PLC", "  Apagar PLC",
    "Encender salida 0", "  Apagar salida 0",
    "Encender salida 1", "  Apagar salida 1",
    "Encender salida 2", "  Apagar salida 2",
    "Encender salida 3", "  Apagar salida 3",
    "Encender salida 4", "  Apagar salida 4",
    "Encender salida 5", "  Apagar salida 5",
    "Encender salida 6", "  Apagar salida 6",
    "Encender salida 7", "  Apagar salida 7",
    "Encender salida 8", "  Apagar salida 8",
    "Encender salida 9", "  Apagar salida 9",
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
        elif menu[current_row] == "Encender salida 0":
          fEncenderSalida(vHost, 'Q0.0', 'Salida 0')
        elif menu[current_row] == "  Apagar salida 0":
          fApagarSalida(vHost, 'Q0.0', 'Salida 0')
        elif menu[current_row] == "Encender salida 1":
          fEncenderSalida(vHost, 'Q0.1', 'Salida 1')
        elif menu[current_row] == "  Apagar salida 1":
          fApagarSalida(vHost, 'Q0.1', 'Salida 1')
        elif menu[current_row] == "Encender salida 2":
          fEncenderSalida(vHost, 'Q0.2', 'Salida 2')
        elif menu[current_row] == "  Apagar salida 2":
          fApagarSalida(vHost, 'Q0.2', 'Salida 2')
        elif menu[current_row] == "Encender salida 3":
          fEncenderSalida(vHost, 'Q0.3', 'Salida 3')
        elif menu[current_row] == "  Apagar salida 3":
          fApagarSalida(vHost, 'Q0.3', 'Salida 3')
        elif menu[current_row] == "Encender salida 4":
          fEncenderSalida(vHost, 'Q0.4', 'Salida 4')
        elif menu[current_row] == "  Apagar salida 4":
          fApagarSalida(vHost, 'Q0.4', 'Salida 4')

      except Exception as e:
        print(f"Error: {e}")

      output_message = sys.stdout.getvalue()
      sys.stdout = old_stdout
      print_output(stdscr, output_message)

  stdscr.clear()
  stdscr.addstr(0, 0, "Saliendo del programa...")
  stdscr.refresh()

if __name__ == "__main__":
  if len(sys.argv) > 1:
    vHost = {sys.argv[1]}
    curses.wrapper(lambda stdscr: fMenu(stdscr, vHost))
  else:
    print(cColorRojo + "\n  No has indicado cual es la IP del PLC. \n" + cFinColor)
    print("  Uso correcto: python3 [RutaAlScript.py] [IPDelPLC] \n")
  #parser = argparse.ArgumentParser(description='Control de PLC Siemens S7-1200')
  #parser.add_argument('--host', required=True, help='\n Dirección IP del PLC \n')
  #args = parser.parse_args()
  #vHost = args.host
  #curses.wrapper(lambda stdscr: fMenu(stdscr, vHost))
