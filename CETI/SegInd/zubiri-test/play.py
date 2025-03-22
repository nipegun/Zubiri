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
    vResp = vSocketConPLC.recv(1024)
    if not vResp:
      print(f"No se recibió respuesta al enviar {vPayloadSolComCOTP}")
      vSocketConPLC.close()
      return
    data_hex = vResp.hex()
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
