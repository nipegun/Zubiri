#!/bin/bash

# Pongo a disposición pública este script bajo el término de "software de dominio público".
# Puedes hacer lo que quieras con él porque es libre de verdad; no libre con condiciones como las licencias GNU y otras patrañas similares.
# Si se te llena la boca hablando de libertad entonces hazlo realmente libre.
# No tienes que aceptar ningún tipo de términos de uso o licencia para utilizarlo o modificarlo porque va sin CopyLeft.

# ----------
# Script de NiPeGun para descargar e importar el pack PlantaQuimica para VirtualBox en Debian
#
# Ejecución remota (puede requerir permisos sudo):
#   curl -sL https://raw.githubusercontent.com/nipegun/zubiri/refs/heads/main/CETI/SegInd/PlantaQuimica-Crear.sh | bash
#
# Ejecución remota como root:
#   curl -sL https://raw.githubusercontent.com/nipegun/zubiri/refs/heads/main/CETI/SegInd/PlantaQuimica-Crear.sh | sed 's-sudo--g' | bash
#
# Bajar y editar directamente el archivo en nano
#   curl -sL https://raw.githubusercontent.com/nipegun/zubiri/refs/heads/main/CETI/SegInd/PlantaQuimica-Crear.sh | nano -
# ----------

#
#  Referencia: https://github.com/Fortiphyd/GRFICSv2
#

# Definir constantes de color
  cColorAzul="\033[0;34m"
  cColorAzulClaro="\033[1;34m"
  cColorVerde='\033[1;32m'
  cColorRojo='\033[1;31m'
  # Para el color rojo también:
    #echo "$(tput setaf 1)Mensaje en color rojo. $(tput sgr 0)"
  cFinColor='\033[0m'

# Determinar la versión de Debian
  if [ -f /etc/os-release ]; then             # Para systemd y freedesktop.org.
    . /etc/os-release
    cNomSO=$NAME
    cVerSO=$VERSION_ID
  elif type lsb_release >/dev/null 2>&1; then # Para linuxbase.org.
    cNomSO=$(lsb_release -si)
    cVerSO=$(lsb_release -sr)
  elif [ -f /etc/lsb-release ]; then          # Para algunas versiones de Debian sin el comando lsb_release.
    . /etc/lsb-release
    cNomSO=$DISTRIB_ID
    cVerSO=$DISTRIB_RELEASE
  elif [ -f /etc/debian_version ]; then       # Para versiones viejas de Debian.
    cNomSO=Debian
    cVerSO=$(cat /etc/debian_version)
  else                                        # Para el viejo uname (También funciona para BSD).
    cNomSO=$(uname -s)
    cVerSO=$(uname -r)
  fi

# Ejecutar comandos dependiendo de la versión de Debian detectada

  if [ $cVerSO == "13" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de importación del pack PlantaQuimica para el VirtualBox de Debian 13 (x)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 13 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  elif [ $cVerSO == "12" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de importación del pack PlantaQuimica para el VirtualBox de Debian 12 (Bookworm)...${cFinColor}"
    echo ""

    # Definir fecha de ejecución del script
      cFechaDeEjec=$(date +a%Ym%md%d@%T)

    # Comprobar si el paquete dialog está instalado. Si no lo está, instalarlo.
      if [[ $(dpkg-query -s dialog 2>/dev/null | grep installed) == "" ]]; then
        echo ""
        echo -e "${cColorRojo}    El paquete dialog no está instalado. Iniciando su instalación...${cFinColor}"
        echo ""
        sudo apt-get -y update
        sudo apt-get -y install dialog
        echo ""
      fi

    # Crear el menú
      menu=(dialog --checklist "Marca las tareas que quieras ejecutar:" 22 60 16)
        opciones=(
          1 "Instalar VirtualBox"         off
          2 "Importar máquinas virtuales" on
        )
      choices=$("${menu[@]}" "${opciones[@]}" 2>&1 >/dev/tty)

      for choice in $choices
        do
          case $choice in

            1)

              echo ""
              echo "  Lanzando el script de instalación de VirtualBox..."
              echo ""
              # Comprobar si el paquete curl está instalado. Si no lo está, instalarlo.
                if [[ $(dpkg-query -s curl 2>/dev/null | grep installed) == "" ]]; then
                  echo ""
                  echo -e "${cColorRojo}  El paquete curl no está instalado. Iniciando su instalación...${cFinColor}"
                  echo ""
                  sudo apt-get -y update
                  sudo apt-get -y install curl
                  echo ""
                fi
              curl -sL https://raw.githubusercontent.com/nipegun/d-scripts/refs/heads/master/SoftInst/ParaGUI/VirtualBox-Instalar.sh | sudo bash

            ;;

            2)

              echo ""
              echo "  Creando laboratorio completo de planta química para VirtualBox..."
              echo ""

              # Definir fecha de ejecución del script
                cFechaDeEjec=$(date +a%Ym%md%d@%T)

              # Crear el menú
                # Comprobar si el paquete dialog está instalado. Si no lo está, instalarlo.
                  if [[ $(dpkg-query -s dialog 2>/dev/null | grep installed) == "" ]]; then
                    echo ""
                    echo -e "${cColorRojo}   El paquete dialog no está instalado. Iniciando su instalación...${cFinColor}"
                    echo ""
                    sudo apt-get -y update
                    sudo apt-get -y install dialog
                    echo ""
                  fi
                menu=(dialog --checklist "Marca las opciones que quieras instalar:" 22 70 16)
                  opciones=(

                    1 "Descargar y descomprimir discos duros virtuales"        off

                    2 "Importar máquina virtual de HMI (ScadaBR)"              off
                    3 "Importar máquina virtual de Kali"                       off
                    4 "Importar máquina virtual de pfSense"                    off
                    5 "Importar máquina virtual de Simulation (ChemicalPlant)" off
                    6 "Importar máquina virtual de PLC"                        off
                    7 "Importar máquina virtual de Workstation"                off
                    
                    8 "Agrupar máquinas virtuales"                             off
                    9 "Iniciar las máquinas virtuales en orden"                off

                  )
                choices=$("${menu[@]}" "${opciones[@]}" 2>&1 >/dev/tty)

                for choice in $choices
                  do
                    case $choice in

                      1)

                          echo ""
                          echo "    Descargando y descomprimiendo discos virtuales..."
                          echo ""
                          # Comprobar si el paquete curl está instalado. Si no lo está, instalarlo.
                            if [[ $(dpkg-query -s curl 2>/dev/null | grep installed) == "" ]]; then
                              echo ""
                              echo -e "${cColorRojo}    El paquete curl no está instalado. Iniciando su instalación...${cFinColor}"
                              echo ""
                              sudo apt-get -y update
                              sudo apt-get -y install curl
                              echo ""
                            fi
                          echo ""
                          echo "      Descargando..."
                          echo ""
                          curl -L DiscosPlantaQuim.tar.xz -o /tmp/DiscosPlantaQuim.tar.xz
                          # Comprobar si el paquete tar está instalado. Si no lo está, instalarlo.
                            if [[ $(dpkg-query -s tar 2>/dev/null | grep installed) == "" ]]; then
                              echo ""
                              echo -e "${cColorRojo}    El paquete tar no está instalado. Iniciando su instalación...${cFinColor}"
                              echo ""
                              sudo apt-get -y update
                              sudo apt-get -y install tar
                              echo ""
                            fi
                          echo ""
                          echo "      Descomprimiendo..."
                          echo ""
                          tar -xvJf /tmp/DiscosPlantaQuim.tar.xz -C ~/

                      ;;

                      2)

                          echo ""
                          echo "    Importando máquina virtual de HMIScadaBR..."
                          echo ""
                          VBoxManage createvm --name "pq-HMIScadaBR" --ostype "Ubuntu_64" --register
                          # Procesador
                            VBoxManage modifyvm "pq-HMIScadaBR" --cpus 2
                          # RAM
                            VBoxManage modifyvm "pq-HMIScadaBR" --memory 2048
                          # Gráfica
                            VBoxManage modifyvm "pq-HMIScadaBR" --graphicscontroller vmsvga --vram 128 --accelerate3d on
                          # Audio
                            VBoxManage modifyvm "pq-HMIScadaBR" --audio-driver none
                          # Red
                            VBoxManage modifyvm "pq-HMIScadaBR" --nictype1 virtio
                              VBoxManage modifyvm "pq-HMIScadaBR" --nic1 intnet --intnet1 "RedIntOper"

                          # Almacenamiento
                            # Controlador
                              VBoxManage storagectl "pq-HMIScadaBR" --name "SATA Controller" --add sata --controller IntelAhci --portcount 1
                            # CD
                              VBoxManage storageattach "pq-HMIScadaBR" --storagectl "SATA Controller" --port 0 --device 0 --type dvddrive --medium emptydrive
                            # Controladora de disco duro
                              VBoxManage storagectl "pq-HMIScadaBR" --name "VirtIO" --add "VirtIO" --bootable on --portcount 1

                        # Disco duro
                          mv ~/DiscosPlantaQuim/pq-HMIScadaBR.vdi ~/"VirtualBox VMs/pq-HMIScadaBR/"
                            #VBoxManage internalcommands sethduuid ~/"VirtualBox VMs/pq-HMIScadaBR/pq-HMIScadaBR.vdi" 43606a85-6b4c-420c-99ee-0567adcb16a3
                          VBoxManage storageattach "pq-HMIScadaBR" --storagectl "VirtIO" --port 0 --device 0 --type hdd --medium ~/"VirtualBox VMs/pq-HMIScadaBR/pq-HMIScadaBR.vdi"

                      ;;

                      3)

                          echo ""
                          echo "    Importando máquina virtual de Kali..."
                          echo ""
                          VBoxManage createvm --name "pq-Kali" --ostype "Debian_64" --register
                          # Procesador
                            VBoxManage modifyvm "pq-Kali" --cpus 2
                          # RAM
                            VBoxManage modifyvm "pq-Kali" --memory 2048
                          # Gráfica
                            VBoxManage modifyvm "pq-Kali" --graphicscontroller vmsvga --vram 128 --accelerate3d on
                          # Audio
                            VBoxManage modifyvm "pq-Kali" --audio-driver none
                          # Red
                            VBoxManage modifyvm "pq-Kali" --nictype1 virtio
                              VBoxManage modifyvm "pq-Kali" --nic1 intnet --intnet1 "RedIntOper"

                          # Almacenamiento
                            # Controlador
                              VBoxManage storagectl "pq-Kali" --name "SATA Controller" --add sata --controller IntelAhci --portcount 1
                            # CD
                              VBoxManage storageattach "pq-Kali" --storagectl "SATA Controller" --port 0 --device 0 --type dvddrive --medium emptydrive
                            # Controladora de disco duro
                              VBoxManage storagectl "pq-Kali" --name "VirtIO" --add "VirtIO" --bootable on --portcount 1

                        # Disco duro
                          mv ~/DiscosPlantaQuim/pq-Kali.vdi ~/"VirtualBox VMs/pq-Kali/"
                            #VBoxManage internalcommands sethduuid ~/"VirtualBox VMs/pq-Kali/pq-Kali.vdi" 43333a85-6b4c-420c-99ee-0567adcb16a3
                          VBoxManage storageattach "pq-Kali" --storagectl "VirtIO" --port 0 --device 0 --type hdd --medium ~/"VirtualBox VMs/pq-Kali/pq-Kali.vdi"

                      ;;

                      4)

                          echo ""
                          echo "    Importando máquina virtual de pfSense..."
                          echo ""
                          VBoxManage createvm --name "pq-pfSense" --ostype "Linux_64" --register
                          # Procesador
                            VBoxManage modifyvm "pq-pfSense" --cpus 2
                          # RAM
                            VBoxManage modifyvm "pq-pfSense" --memory 2048
                          # Gráfica
                            VBoxManage modifyvm "pq-pfSense" --graphicscontroller vmsvga --vram 128 --accelerate3d on
                          # Audio
                            VBoxManage modifyvm "pq-pfSense" --audio-driver none
                          # Red
                            VBoxManage modifyvm "pq-pfSense" --nictype1 82540EM
                              VBoxManage modifyvm "pq-pfSense" --nic1 intnet --intnet1 "RedIntOper"
                            VBoxManage modifyvm "pq-pfSense" --nictype2 82540EM
                              VBoxManage modifyvm "pq-pfSense" --nic2 intnet --intnet2 "RedIntInd"

                          # Almacenamiento
                            # Controlador
                              VBoxManage storagectl "pq-pfSense" --name "SATA Controller" --add sata --controller IntelAhci --portcount 1
                            # CD
                              VBoxManage storageattach "pq-pfSense" --storagectl "SATA Controller" --port 0 --device 0 --type dvddrive --medium emptydrive

                        # Disco duro
                          mv ~/DiscosPlantaQuim/pq-pfSense.vdi ~/"VirtualBox VMs/pq-pfSense/"
                            #VBoxManage internalcommands sethduuid ~/"VirtualBox VMs/pq-pfSense/pq-pfSense.vdi" d2d48e12-6454-41fb-919d-4127f84459e9
                          VBoxManage storageattach "pq-pfSense" --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium ~/"VirtualBox VMs/pq-pfSense/pq-pfSense.vdi"

                      ;;

                      5)

                          echo ""
                          echo "    Importando máquina virtual de Simulation..."
                          echo ""
                          VBoxManage createvm --name "pq-Simulation" --ostype "Ubuntu_64" --register
                          # Procesador
                            VBoxManage modifyvm "pq-Simulation" --cpus 2
                          # RAM
                            VBoxManage modifyvm "pq-Simulation" --memory 2048
                          # Gráfica
                            VBoxManage modifyvm "pq-Simulation" --graphicscontroller vmsvga --vram 128 --accelerate3d on
                          # Audio
                            VBoxManage modifyvm "pq-Simulation" --audio-driver none
                          # Red
                            VBoxManage modifyvm "pq-Simulation" --nictype1 virtio
                              VBoxManage modifyvm "pq-Simulation" --nic1 intnet --intnet1 "RedIntInd"

                          # Almacenamiento
                            # Controlador
                              VBoxManage storagectl "pq-Simulation" --name "SATA Controller" --add sata --controller IntelAhci --portcount 1
                            # CD
                              VBoxManage storageattach "pq-Simulation" --storagectl "SATA Controller" --port 0 --device 0 --type dvddrive --medium emptydrive
                            # Controladora de disco duro
                              VBoxManage storagectl "pq-Simulation" --name "VirtIO" --add "VirtIO" --bootable on --portcount 1

                        # Disco duro
                          mv ~/DiscosPlantaQuim/pq-Simulation.vdi ~/"VirtualBox VMs/pq-Simulation/"
                            #VBoxManage internalcommands sethduuid ~/"VirtualBox VMs/pq-Simulation/pq-Simulation.vdi" 9e5809b5-5f31-43e5-93fa-de514622390d
                          VBoxManage storageattach "pq-Simulation" --storagectl "VirtIO" --port 0 --device 0 --type hdd --medium ~/"VirtualBox VMs/pq-Simulation/pq-Simulation.vdi"

                      ;;

                      6)

                          echo ""
                          echo "    Importando máquina virtual de PLC..."
                          echo ""
                          VBoxManage createvm --name "pq-PLC" --ostype "Ubuntu" --register
                          # Procesador
                            VBoxManage modifyvm "pq-PLC" --cpus 2
                          # RAM
                            VBoxManage modifyvm "pq-PLC" --memory 2048
                          # Gráfica
                            VBoxManage modifyvm "pq-PLC" --graphicscontroller vmsvga --vram 128 --accelerate3d on
                          # Audio
                            VBoxManage modifyvm "pq-PLC" --audio-driver none
                          # Red
                            VBoxManage modifyvm "pq-PLC" --nictype1 virtio
                              VBoxManage modifyvm "pq-PLC" --nic1 intnet --intnet1 "RedIntInd"

                          # Almacenamiento
                            # Controlador
                              VBoxManage storagectl "pq-PLC" --name "SATA Controller" --add sata --controller IntelAhci --portcount 1
                            # CD
                              VBoxManage storageattach "pq-PLC" --storagectl "SATA Controller" --port 0 --device 0 --type dvddrive --medium emptydrive
                            # Controladora de disco duro
                              VBoxManage storagectl "pq-PLC" --name "VirtIO" --add "VirtIO" --bootable on --portcount 1

                        # Disco duro
                          mv ~/DiscosPlantaQuim/pq-PLC.vdi ~/"VirtualBox VMs/pq-PLC/"
                            #VBoxManage internalcommands sethduuid ~/"VirtualBox VMs/pq-PLC/pq-PLC.vdi" df3195b7-7cb0-4848-be56-1e96ebecbc52
                          VBoxManage storageattach "pq-PLC" --storagectl "VirtIO" --port 0 --device 0 --type hdd --medium ~/"VirtualBox VMs/pq-PLC/pq-PLC.vdi"

                      ;;

                      7)

                          echo ""
                          echo "    Importando máquina virtual de Workstation..."
                          echo ""
                          VBoxManage createvm --name "pq-Workstation" --ostype "Ubuntu" --register
                          # Procesador
                            VBoxManage modifyvm "pq-Workstation" --cpus 2
                          # RAM
                            VBoxManage modifyvm "pq-Workstation" --memory 2048
                          # Gráfica
                            VBoxManage modifyvm "pq-Workstation" --graphicscontroller vmsvga --vram 128 --accelerate3d on
                          # Audio
                            VBoxManage modifyvm "pq-Workstation" --audio-driver none
                          # Red
                            VBoxManage modifyvm "pq-Workstation" --nictype1 virtio
                              VBoxManage modifyvm "pq-Workstation" --nic1 intnet --intnet1 "RedIntInd"

                          # Almacenamiento
                            # Controlador
                              VBoxManage storagectl "pq-Workstation" --name "SATA Controller" --add sata --controller IntelAhci --portcount 1
                            # CD
                              VBoxManage storageattach "pq-Workstation" --storagectl "SATA Controller" --port 0 --device 0 --type dvddrive --medium emptydrive
                            # Controladora de disco duro
                              VBoxManage storagectl "pq-Workstation" --name "VirtIO" --add "VirtIO" --bootable on --portcount 1

                        # Disco duro
                          mv ~/DiscosPlantaQuim/pq-Workstation.vdi ~/"VirtualBox VMs/pq-Workstation/"
                            #VBoxManage internalcommands sethduuid ~/"VirtualBox VMs/pq-Workstation/pq-Workstation.vdi" 79e7d4fb-1d24-476b-bc12-e4f31554e3e3
                          VBoxManage storageattach "pq-Workstation" --storagectl "VirtIO" --port 0 --device 0 --type hdd --medium ~/"VirtualBox VMs/pq-Workstation/pq-Workstation.vdi"

                      ;;

                      8)

                        echo ""
                        echo "  Agrupando máquinas virtuales..."
                        echo ""
                        VBoxManage modifyvm "pq-HMIScadaBR"  --groups "/PlantaQuímica" 2> /dev/null
                        VBoxManage modifyvm "pq-Kali"        --groups "/PlantaQuímica" 2> /dev/null
                        VBoxManage modifyvm "pq-pfSense"     --groups "/PlantaQuímica" 2> /dev/null
                        VBoxManage modifyvm "pq-Simulation"  --groups "/PlantaQuímica" 2> /dev/null
                        VBoxManage modifyvm "pq-PLC"         --groups "/PlantaQuímica" 2> /dev/null
                        VBoxManage modifyvm "pq-Workstation" --groups "/PlantaQuímica" 2> /dev/null

                      ;;

                      9)

                        echo ""
                        echo "  Iniciando máquinas virtuales en el orden correcto..."
                        echo ""
                        VBoxManage startvm "pq-pfSense"
                        sleep 15
                        VBoxManage startvm "pq-Simulation"
                        sleep 5
                        VBoxManage startvm "pq-PLC"
                        sleep 5
                        VBoxManage startvm "pq-Workstation"
                        sleep 5
                        VBoxManage startvm "pq-HMIScadaBR"
                        sleep 5
                        VBoxManage startvm "pq-Kali"

                      ;;

                  esac

              done

            ;;

        esac

    done

  elif [ $cVerSO == "11" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de importación del pack PlantaQuimica para el VirtualBox de ebian 11 (Bullseye)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 11 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  elif [ $cVerSO == "10" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de importación del pack PlantaQuimica para el VirtualBox de ebian 10 (Buster)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 10 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  elif [ $cVerSO == "9" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de importación del pack PlantaQuimica para el VirtualBox de ebian 9 (Stretch)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 9 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  elif [ $cVerSO == "8" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de importación del pack PlantaQuimica para el VirtualBox de ebian 8 (Jessie)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 8 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  elif [ $cVerSO == "7" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de importación del pack PlantaQuimica para el VirtualBox de ebian 7 (Wheezy)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 7 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  fi
