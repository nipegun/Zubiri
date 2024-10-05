#!/bin/bash

# Pongo a disposición pública este script bajo el término de "software de dominio público".
# Puedes hacer lo que quieras con él porque es libre de verdad; no libre con condiciones como las licencias GNU y otras patrañas similares.
# Si se te llena la boca hablando de libertad entonces hazlo realmente libre.
# No tienes que aceptar ningún tipo de términos de uso o licencia para utilizarlo o modificarlo porque va sin CopyLeft.

# ----------
# Script de NiPeGun para buscar posibles proxmox corriendo en la IP pública de Zubiri Manteo
#
# Ejecución remota:
#   curl -sL https://raw.githubusercontent.com/nipegun/asir/main/zubiri/RDPs-BuscarEnSubred.sh | bash
# ----------

# Definir variables de color
  vColorAzul="\033[0;34m"
  vColorAzulClaro="\033[1;34m"
  vColorVerde='\033[1;32m'
  vColorRojo='\033[1;31m'
  vFinColor='\033[0m'

# Notificar inicio de ejecución del script
  echo ""
  echo -e "${vColorAzulClaro}  Iniciando el script de búsqueda de posibles RDPs corriendo en la subred de cyber...${vFinColor}"
  echo ""

# Comprobar si el paquete curl está instalado. Si no lo está, instalarlo.
  if [[ $(dpkg-query -s curl 2>/dev/null | grep installed) == "" ]]; then
    echo ""
    echo -e "${vColorRojo}    El paquete curl no está instalado. Iniciando su instalación...${vFinColor}"
    echo ""
    apt-get -y update && apt-get -y install curl
    echo ""
  fi

# Determinar la IP WAN
  vSubRed="172.16.2.0/24"
  #vIPWAN=$(curl --silent ipinfo.io/ip)
  
# Escanear puertos y salvar a un archivo
  echo "    Escaneando IPs..."
  echo ""
  # Comprobar si el paquete nmap está instalado. Si no lo está, instalarlo.
    if [[ $(dpkg-query -s nmap 2>/dev/null | grep installed) == "" ]]; then
      echo ""
      echo -e "${vColorRojo}    El paquete nmap no está instalado. Iniciando su instalación...${vFinColor}"
      echo ""
      apt-get -y update && apt-get -y install nmap
      echo ""
    fi
  nmap $vSubRed -p 3389 | grep 172 | sed 's/^[^0-9]*//' > /tmp/IPsConRDPActivo.txt

#
  for vLinea in $(cat /tmp/IPsConRDPActivo.txt)
    do
      echo "$vLinea:" $(nmap -sV $vLinea -p 3389 | grep -v ^MAC | grep -v atency | grep -v scan | grep -v ^PORT | grep -v map)
    done
