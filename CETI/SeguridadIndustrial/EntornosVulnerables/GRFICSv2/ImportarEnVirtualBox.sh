#!/bin/bash

# Pongo a disposición pública este script bajo el término de "software de dominio público".
# Puedes hacer lo que quieras con él porque es libre de verdad; no libre con condiciones como las licencias GNU y otras patrañas similares.
# Si se te llena la boca hablando de libertad entonces hazlo realmente libre.
# No tienes que aceptar ningún tipo de términos de uso o licencia para utilizarlo o modificarlo porque va sin CopyLeft.

# ----------
# Script de NiPeGun para descargar e importar el entorno virtual GRFICSv2 para VirtualBox en Debian
#
# Ejecución remota (puede requerir permisos sudo):
#   curl -sL https://raw.githubusercontent.com/nipegun/Zubiri/refs/heads/main/CETI/SeguridadIndustrial/EntornosVulnerables/GRFICSv2/ImportarEnVirtualBox.sh | bash
#
# Ejecución remota como root:
#   curl -sL https://raw.githubusercontent.com/nipegun/Zubiri/refs/heads/main/CETI/SeguridadIndustrial/EntornosVulnerables/GRFICSv2/ImportarEnVirtualBox.sh | sed 's-sudo--g' | bash
#
# Bajar y editar directamente el archivo en nano
#   curl -sL https://raw.githubusercontent.com/nipegun/Zubiri/refs/heads/main/CETI/SeguridadIndustrial/EntornosVulnerables/GRFICSv2/ImportarEnVirtualBox.sh | nano -
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
    echo -e "${cColorAzulClaro}  Iniciando el script de importación del entorno OT vulnerable GRFICSv2 para VirtualBox en Debian 13 (x)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 13 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  elif [ $cVerSO == "12" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de importación del entorno OT vulnerable GRFICSv2 para VirtualBox en Debian 12 (Bookworm)...${cFinColor}"
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

                    1 "Descargar y descomprimir todos los discos duros virtuales" off

                    2 "  Importar máquina virtual de pfSense"         off
                    3 "  Importar máquina virtual de 3DChemicalPlant" off
                    4 "  Importar máquina virtual de PLC"             off
                    5 "  Importar máquina virtual de Workstation"     off
                    6 "  Importar máquina virtual de HMIScadaBR"      off
                    7 "  Importar máquina virtual de Kali"            off

                    8 "    Agrupar máquinas virtuales"              off
                    9 "    Iniciar las máquinas virtuales en orden" off

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
                          curl -L http://hacks4geeks.com/_/zubiri/DiscosPlantaQuim.tar.xz -o /tmp/DiscosPlantaQuim.tar.xz
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
                          echo "    Importando máquina virtual de pfSense..."
                          echo ""
                          VBoxManage createvm --name "GRFICSv2-pfSense" --ostype "Linux_64" --register
                          # Procesador
                            VBoxManage modifyvm "GRFICSv2-pfSense" --cpus 2
                          # RAM
                            VBoxManage modifyvm "GRFICSv2-pfSense" --memory 2048
                          # Gráfica
                            VBoxManage modifyvm "GRFICSv2-pfSense" --graphicscontroller vmsvga --vram 128 --accelerate3d on
                          # Audio
                            VBoxManage modifyvm "GRFICSv2-pfSense" --audio-driver none
                          # Red
                            VBoxManage modifyvm "GRFICSv2-pfSense" --nictype1 82540EM
                              VBoxManage modifyvm "GRFICSv2-pfSense" --nic1 intnet --intnet1 "RedIntOper"
                            # Poner en modo promiscuo
                              VBoxManage modifyvm "GRFICSv2-pfSense" --nicpromisc1 allow-all
                            VBoxManage modifyvm "GRFICSv2-pfSense" --nictype2 82540EM
                              VBoxManage modifyvm "GRFICSv2-pfSense" --nic2 intnet --intnet2 "RedIntInd"
                            # Poner en modo promiscuo
                              VBoxManage modifyvm "GRFICSv2-pfSense" --nicpromisc2 allow-all

                          # Almacenamiento
                            # Controlador
                              VBoxManage storagectl "GRFICSv2-pfSense" --name "SATA Controller" --add sata --controller IntelAhci --portcount 1
                            # CD
                              VBoxManage storageattach "GRFICSv2-pfSense" --storagectl "SATA Controller" --port 0 --device 0 --type dvddrive --medium emptydrive

                        # Disco duro
                          mv ~/DiscosPlantaQuim/GRFICSv2-pfSense.vdi ~/"VirtualBox VMs/GRFICSv2-pfSense/"
                            #VBoxManage internalcommands sethduuid ~/"VirtualBox VMs/GRFICSv2-pfSense/GRFICSv2-pfSense.vdi" d2d48e12-6454-41fb-919d-4127f84459e9
                          VBoxManage storageattach "GRFICSv2-pfSense" --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium ~/"VirtualBox VMs/GRFICSv2-pfSense/GRFICSv2-pfSense.vdi"

                      ;;

                      3)

                          echo ""
                          echo "    Importando máquina virtual de 3DChemicalPlant..."
                          echo ""
                          VBoxManage createvm --name "GRFICSv2-3DChemicalPlant" --ostype "Ubuntu_64" --register
                          # Procesador
                            VBoxManage modifyvm "GRFICSv2-3DChemicalPlant" --cpus 2
                          # RAM
                            VBoxManage modifyvm "GRFICSv2-3DChemicalPlant" --memory 2048
                          # Gráfica
                            VBoxManage modifyvm "GRFICSv2-3DChemicalPlant" --graphicscontroller vmsvga --vram 128 --accelerate3d on
                          # Audio
                            VBoxManage modifyvm "GRFICSv2-3DChemicalPlant" --audio-driver none
                          # Red
                            VBoxManage modifyvm "GRFICSv2-3DChemicalPlant" --nictype1 virtio
                              VBoxManage modifyvm "GRFICSv2-3DChemicalPlant" --nic1 intnet --intnet1 "RedIntInd"
                            # Poner en modo promiscuo
                              VBoxManage modifyvm "GRFICSv2-3DChemicalPlant" --nicpromisc1 allow-all

                          # Almacenamiento
                            # Controlador
                              VBoxManage storagectl "GRFICSv2-3DChemicalPlant" --name "SATA Controller" --add sata --controller IntelAhci --portcount 1
                            # CD
                              VBoxManage storageattach "GRFICSv2-3DChemicalPlant" --storagectl "SATA Controller" --port 0 --device 0 --type dvddrive --medium emptydrive
                            # Controladora de disco duro
                              VBoxManage storagectl "GRFICSv2-3DChemicalPlant" --name "VirtIO" --add "VirtIO" --bootable on --portcount 1

                        # Disco duro
                          mv ~/DiscosPlantaQuim/GRFICSv2-3DChemicalPlant.vdi ~/"VirtualBox VMs/GRFICSv2-3DChemicalPlant/"
                            #VBoxManage internalcommands sethduuid ~/"VirtualBox VMs/GRFICSv2-3DChemicalPlant/GRFICSv2-3DChemicalPlant.vdi" 9e5809b5-5f31-43e5-93fa-de514622390d
                          VBoxManage storageattach "GRFICSv2-3DChemicalPlant" --storagectl "VirtIO" --port 0 --device 0 --type hdd --medium ~/"VirtualBox VMs/GRFICSv2-3DChemicalPlant/GRFICSv2-3DChemicalPlant.vdi"

                      ;;

                      4)

                          echo ""
                          echo "    Importando máquina virtual de PLC..."
                          echo ""
                          VBoxManage createvm --name "GRFICSv2-PLC" --ostype "Ubuntu" --register
                          # Procesador
                            VBoxManage modifyvm "GRFICSv2-PLC" --cpus 2
                          # RAM
                            VBoxManage modifyvm "GRFICSv2-PLC" --memory 2048
                          # Gráfica
                            VBoxManage modifyvm "GRFICSv2-PLC" --graphicscontroller vmsvga --vram 128 --accelerate3d on
                          # Audio
                            VBoxManage modifyvm "GRFICSv2-PLC" --audio-driver none
                          # Red
                            VBoxManage modifyvm "GRFICSv2-PLC" --nictype1 virtio
                              VBoxManage modifyvm "GRFICSv2-PLC" --nic1 intnet --intnet1 "RedIntInd"
                            # Poner en modo promiscuo
                              VBoxManage modifyvm "GRFICSv2-PLC" --nicpromisc1 allow-all

                          # Almacenamiento
                            # Controlador
                              VBoxManage storagectl "GRFICSv2-PLC" --name "SATA Controller" --add sata --controller IntelAhci --portcount 1
                            # CD
                              VBoxManage storageattach "GRFICSv2-PLC" --storagectl "SATA Controller" --port 0 --device 0 --type dvddrive --medium emptydrive
                            # Controladora de disco duro
                              VBoxManage storagectl "GRFICSv2-PLC" --name "VirtIO" --add "VirtIO" --bootable on --portcount 1

                        # Disco duro
                          mv ~/DiscosPlantaQuim/GRFICSv2-PLC.vdi ~/"VirtualBox VMs/GRFICSv2-PLC/"
                            #VBoxManage internalcommands sethduuid ~/"VirtualBox VMs/GRFICSv2-PLC/GRFICSv2-PLC.vdi" df3195b7-7cb0-4848-be56-1e96ebecbc52
                          VBoxManage storageattach "GRFICSv2-PLC" --storagectl "VirtIO" --port 0 --device 0 --type hdd --medium ~/"VirtualBox VMs/GRFICSv2-PLC/GRFICSv2-PLC.vdi"

                      ;;

                      5)

                          echo ""
                          echo "    Importando máquina virtual de Workstation..."
                          echo ""
                          VBoxManage createvm --name "GRFICSv2-Workstation" --ostype "Ubuntu_64" --register
                          # Procesador
                            VBoxManage modifyvm "GRFICSv2-Workstation" --cpus 2
                          # RAM
                            VBoxManage modifyvm "GRFICSv2-Workstation" --memory 2048
                          # Gráfica
                            VBoxManage modifyvm "GRFICSv2-Workstation" --graphicscontroller vmsvga --vram 128 --accelerate3d on
                          # Audio
                            VBoxManage modifyvm "GRFICSv2-Workstation" --audio-driver none
                          # Red
                            VBoxManage modifyvm "GRFICSv2-Workstation" --nictype1 virtio
                              VBoxManage modifyvm "GRFICSv2-Workstation" --nic1 intnet --intnet1 "RedIntInd"
                            # Poner en modo promiscuo
                              VBoxManage modifyvm "GRFICSv2-Workstation" --nicpromisc1 allow-all

                          # Almacenamiento
                            # Controlador
                              VBoxManage storagectl "GRFICSv2-Workstation" --name "SATA Controller" --add sata --controller IntelAhci --portcount 1
                            # CD
                              VBoxManage storageattach "GRFICSv2-Workstation" --storagectl "SATA Controller" --port 0 --device 0 --type dvddrive --medium emptydrive
                            # Controladora de disco duro
                              VBoxManage storagectl "GRFICSv2-Workstation" --name "VirtIO" --add "VirtIO" --bootable on --portcount 1

                        # Disco duro
                          mv ~/DiscosPlantaQuim/GRFICSv2-Workstation.vdi ~/"VirtualBox VMs/GRFICSv2-Workstation/"
                            #VBoxManage internalcommands sethduuid ~/"VirtualBox VMs/GRFICSv2-Workstation/GRFICSv2-Workstation.vdi" 79e7d4fb-1d24-476b-bc12-e4f31554e3e3
                          VBoxManage storageattach "GRFICSv2-Workstation" --storagectl "VirtIO" --port 0 --device 0 --type hdd --medium ~/"VirtualBox VMs/GRFICSv2-Workstation/GRFICSv2-Workstation.vdi"

                      ;;


                      6)

                          echo ""
                          echo "    Importando máquina virtual de HMIScadaBR..."
                          echo ""
                          VBoxManage createvm --name "GRFICSv2-HMIScadaBR" --ostype "Ubuntu_64" --register
                          # Procesador
                            VBoxManage modifyvm "GRFICSv2-HMIScadaBR" --cpus 2
                          # RAM
                            VBoxManage modifyvm "GRFICSv2-HMIScadaBR" --memory 2048
                          # Gráfica
                            VBoxManage modifyvm "GRFICSv2-HMIScadaBR" --graphicscontroller vmsvga --vram 128 --accelerate3d on
                          # Audio
                            VBoxManage modifyvm "GRFICSv2-HMIScadaBR" --audio-driver none
                          # Red
                            VBoxManage modifyvm "GRFICSv2-HMIScadaBR" --nictype1 virtio
                              VBoxManage modifyvm "GRFICSv2-HMIScadaBR" --nic1 intnet --intnet1 "RedIntOper"
                            # Poner en modo promiscuo
                              VBoxManage modifyvm "GRFICSv2-HMIScadaBR" --nicpromisc1 allow-all

                          # Almacenamiento
                            # Controlador
                              VBoxManage storagectl "GRFICSv2-HMIScadaBR" --name "SATA Controller" --add sata --controller IntelAhci --portcount 1
                            # CD
                              VBoxManage storageattach "GRFICSv2-HMIScadaBR" --storagectl "SATA Controller" --port 0 --device 0 --type dvddrive --medium emptydrive
                            # Controladora de disco duro
                              VBoxManage storagectl "GRFICSv2-HMIScadaBR" --name "VirtIO" --add "VirtIO" --bootable on --portcount 1

                        # Disco duro
                          mv ~/DiscosPlantaQuim/GRFICSv2-HMIScadaBR.vdi ~/"VirtualBox VMs/GRFICSv2-HMIScadaBR/"
                            #VBoxManage internalcommands sethduuid ~/"VirtualBox VMs/GRFICSv2-HMIScadaBR/GRFICSv2-HMIScadaBR.vdi" 43606a85-6b4c-420c-99ee-0567adcb16a3
                          VBoxManage storageattach "GRFICSv2-HMIScadaBR" --storagectl "VirtIO" --port 0 --device 0 --type hdd --medium ~/"VirtualBox VMs/GRFICSv2-HMIScadaBR/GRFICSv2-HMIScadaBR.vdi"

                      ;;

                      7)

                          echo ""
                          echo "    Importando máquina virtual de Kali..."
                          echo ""
                          VBoxManage createvm --name "GRFICSv2-Kali" --ostype "Debian_64" --register
                          # Procesador
                            VBoxManage modifyvm "GRFICSv2-Kali" --cpus 2
                          # RAM
                            VBoxManage modifyvm "GRFICSv2-Kali" --memory 2048
                          # Gráfica
                            VBoxManage modifyvm "GRFICSv2-Kali" --graphicscontroller vmsvga --vram 128 --accelerate3d on
                          # Audio
                            VBoxManage modifyvm "GRFICSv2-Kali" --audio-driver none
                          # Red
                            VBoxManage modifyvm "GRFICSv2-Kali" --nictype1 virtio
                              VBoxManage modifyvm "GRFICSv2-Kali" --nic1 intnet --intnet1 "RedIntOper"
                            # Poner en modo promiscuo
                              VBoxManage modifyvm "GRFICSv2-Kali" --nicpromisc1 allow-all

                          # Almacenamiento
                            # Controlador
                              VBoxManage storagectl "GRFICSv2-Kali" --name "SATA Controller" --add sata --controller IntelAhci --portcount 1
                            # CD
                              VBoxManage storageattach "GRFICSv2-Kali" --storagectl "SATA Controller" --port 0 --device 0 --type dvddrive --medium emptydrive
                            # Controladora de disco duro
                              VBoxManage storagectl "GRFICSv2-Kali" --name "VirtIO" --add "VirtIO" --bootable on --portcount 1

                        # Disco duro
                          mv ~/DiscosPlantaQuim/GRFICSv2-Kali.vdi ~/"VirtualBox VMs/GRFICSv2-Kali/"
                            #VBoxManage internalcommands sethduuid ~/"VirtualBox VMs/GRFICSv2-Kali/GRFICSv2-Kali.vdi" 43333a85-6b4c-420c-99ee-0567adcb16a3
                          VBoxManage storageattach "GRFICSv2-Kali" --storagectl "VirtIO" --port 0 --device 0 --type hdd --medium ~/"VirtualBox VMs/GRFICSv2-Kali/GRFICSv2-Kali.vdi"

                      ;;


                      8)

                        echo ""
                        echo "  Agrupando máquinas virtuales..."
                        echo ""
                        VBoxManage modifyvm "GRFICSv2-HMIScadaBR"      --groups "/GRFICSv2" 2> /dev/null
                        VBoxManage modifyvm "GRFICSv2-Kali"            --groups "/GRFICSv2" 2> /dev/null
                        VBoxManage modifyvm "GRFICSv2-pfSense"         --groups "/GRFICSv2" 2> /dev/null
                        VBoxManage modifyvm "GRFICSv2-3DChemicalPlant" --groups "/GRFICSv2" 2> /dev/null
                        VBoxManage modifyvm "GRFICSv2-PLC"             --groups "/GRFICSv2" 2> /dev/null
                        VBoxManage modifyvm "GRFICSv2-Workstation"     --groups "/GRFICSv2" 2> /dev/null

                      ;;

                      9)

                        echo ""
                        echo "  Iniciando máquinas virtuales en el orden correcto..."
                        echo ""
                        VBoxManage startvm "GRFICSv2-pfSense"
                        sleep 15
                        VBoxManage startvm "GRFICSv2-3DChemicalPlant"
                        sleep 15
                        VBoxManage startvm "GRFICSv2-PLC"
                        sleep 15
                        VBoxManage startvm "GRFICSv2-Workstation"
                        sleep 15
                        VBoxManage startvm "GRFICSv2-HMIScadaBR"
                        sleep 15
                        VBoxManage startvm "GRFICSv2-Kali"

                      ;;

                  esac

              done

            ;;

        esac

    done

  elif [ $cVerSO == "11" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de importación del entorno OT vulnerable GRFICSv2 para VirtualBox en Debian 11 (Bullseye)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 11 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  elif [ $cVerSO == "10" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de importación del entorno OT vulnerable GRFICSv2 para VirtualBox en Debian 10 (Buster)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 10 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  elif [ $cVerSO == "9" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de importación del entorno OT vulnerable GRFICSv2 para VirtualBox en Debian 9 (Stretch)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 9 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  elif [ $cVerSO == "8" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de importación del entorno OT vulnerable GRFICSv2 para VirtualBox en Debian 8 (Jessie)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 8 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  elif [ $cVerSO == "7" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de importación del entorno OT vulnerable GRFICSv2 para VirtualBox en Debian 7 (Wheezy)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 7 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  fi
