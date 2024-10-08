#!/bin/bash

# Pongo a disposición pública este script bajo el término de "software de dominio público".
# Puedes hacer lo que quieras con él porque es libre de verdad; no libre con condiciones como las licencias GNU y otras patrañas similares.
# Si se te llena la boca hablando de libertad entonces hazlo realmente libre.
# No tienes que aceptar ningún tipo de términos de uso o licencia para utilizarlo o modificarlo porque va sin CopyLeft.

# ----------
# Script de NiPeGun para preparar en el escritorio una carpeta con los archivos para un nuevo examen de Python
#
# Ejecución remota:
#   curl -sL https://raw.githubusercontent.com/nipegun/asir/refs/heads/main/zubiri/Python-NuevoExamen.sh | bash
# ----------

# Definir constantes de color
  cColorAzul="\033[0;34m"
  cColorAzulClaro="\033[1;34m"
  cColorVerde='\033[1;32m'
  cColorRojo='\033[1;31m'
  # Para el color rojo también:
    #echo "$(tput setaf 1)Mensaje en color rojo. $(tput sgr 0)"
  cFinColor='\033[0m'

# Notificar inicio del script
  echo ""
  echo -e "${cColorAzulClaro}  Iniciando el script para preparar en el escritorio una carpeta con los archivos para un nuevo examen de Python...${cFinColor}"
  echo ""

# Crear la carpeta
  # Definir fecha de ejecución del script
    cFechaDeEjec=$(date +a%Ym%md%d)
  # Crear la carpeta en con la fecha
    mkdir ~/Escritorio/$cFechaDeEjec/
  # Crear los archivos
    # main.py
      echo "from functions import *"     > ~/Escritorio/Ex"$cFechaDeEjec"/main.py
      echo ""                           >> ~/Escritorio/Ex"$cFechaDeEjec"/main.py
    # functions.py
      echo 'import csv'                  > ~/Escritorio/Ex"$cFechaDeEjec"/functions.py
      echo ''                           >> ~/Escritorio/Ex"$cFechaDeEjec"/functions.py
      echo 'def x():'                   >> ~/Escritorio/Ex"$cFechaDeEjec"/functions.py
      echo -e "\tpass"                  >> ~/Escritorio/Ex"$cFechaDeEjec"/functions.py
      echo ''                           >> ~/Escritorio/Ex"$cFechaDeEjec"/functions.py
      echo 'if __name__ == "__main__":' >> ~/Escritorio/Ex"$cFechaDeEjec"/functions.py
      echo -e "\tprint('')"             >> ~/Escritorio/Ex"$cFechaDeEjec"/functions.py
