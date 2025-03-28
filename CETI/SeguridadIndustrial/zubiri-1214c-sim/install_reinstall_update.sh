#!/bin/bash

# Pongo a disposición pública este script bajo el término de "software de dominio público".
# Puedes hacer lo que quieras con él porque es libre de verdad; no libre con condiciones como las licencias GNU y otras patrañas similares.
# Si se te llena la boca hablando de libertad entonces hazlo realmente libre.
# No tienes que aceptar ningún tipo de términos de uso o licencia para utilizarlo o modificarlo porque va sin CopyLeft.

# ----------
# Script de NiPeGun para instalar el simulador del PLC 1214c de clase de Zubiri
#
# Ejecución remota (puede requerir permisos sudo):
#   curl -sL https://raw.githubusercontent.com/nipegun/Zubiri/refs/heads/main/CETI/SeguridadIndustrial/zubiri-1214c-sim/install_reinstall_update.sh | bash
#
# Ejecución remota como root (para sistemas sin sudo):
#   curl -sL https://raw.githubusercontent.com/nipegun/Zubiri/refs/heads/main/CETI/SeguridadIndustrial/zubiri-1214c-sim/install_reinstall_update.sh | sed 's-sudo--g' | bash
#
# Bajar y editar directamente el archivo en nano
#   curl -sL https://raw.githubusercontent.com/nipegun/Zubiri/refs/heads/main/CETI/SeguridadIndustrial/zubiri-1214c-sim/install_reinstall_update.sh | nano -
# ----------

# Definir constantes de color
  cColorAzul='\033[0;34m'
  cColorAzulClaro='\033[1;34m'
  cColorVerde='\033[1;32m'
  cColorRojo='\033[1;31m'
  # Para el color rojo también:
    #echo "$(tput setaf 1)Mensaje en color rojo. $(tput sgr 0)"
  cFinColor='\033[0m'

# Notificar inicio de ejecución del script
  echo ""
  echo -e "${cColorAzulClaro}  Iniciando el script de instalación/reinstalación/actualización del simulador del PLC 1214c de Zubiri...${cFinColor}"

# Borrar posible carpeta previa
  cd ~/
  rm -rf ~/zubiri-1214c-sim 2>/dev/null

# Clonar el repositorio
  echo ""
  echo "    Clonando el repositorio..."
  echo ""
  # Comprobar si el paquete git está instalado. Si no lo está, instalarlo.
    if [[ $(dpkg-query -s git 2>/dev/null | grep installed) == "" ]]; then
      echo ""
      echo -e "${cColorRojo}      El paquete git no está instalado. Iniciando su instalación...${cFinColor}"
      echo ""
      sudo apt-get -y update
      sudo apt-get -y install git
      echo ""
    fi
  git clone https://github.com/nipegun/Zubiri.git

# Renombar y mover carpetas
  mv ~/Zubiri/CETI/SeguridadIndustrial/zubiri-1214c-sim/ ~/
  rm -rf ~/Zubiri/

# Asignar permisos de ejecución a los scripts
  chmod +x ~/zubiri-1214c-sim/*.sh
  chmod +x ~/zubiri-1214c-sim/*.py

# Notificar fin de ejecución del script
  echo ""
  echo "    El script ha finalizado."
  echo ""
  echo "      Para ejecutar el servidor:"
  echo ""
  echo "        cd ~/zubiri-1214c-sim/ && ./server.py && cd ~/"
  echo ""
  echo "      Para reinstalarlo o actualizarlo:"
  echo ""
  echo "        ~/zubiri-1214c-sim/install_reinstall_update.sh"
  echo ""
  echo "      Para enviar datos:"
  echo ""
  vIPServ=$(hostname -I | sed 's- --g')
  echo '        printf "\x03\x00\x00\x25\x02\xf0\x80\x32\x01\x00\x00\x00\x1f\x00\x0e\x00\x06\x05\x01\x12\x0a\x10\x01\x00\x01\x00\x00\x82\x00\x00\x04\x00\x03\x00\x01\x00\x00" | nc '"$vIPServ"' 102'
  echo ""
