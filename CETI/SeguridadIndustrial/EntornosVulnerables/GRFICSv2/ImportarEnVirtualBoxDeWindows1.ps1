# Pongo a disposición pública este script bajo el término de "software de dominio público".
# Puedes hacer lo que quieras con él porque es libre de verdad; no libre con condiciones como las licencias GNU y otras patrañas similares.
# Si se te llena la boca hablando de libertad entonces hazlo realmente libre.
# No tienes que aceptar ningún tipo de términos de uso o licencia para utilizarlo o modificarlo porque va sin CopyLeft.

# ----------
# Script de NiPeGun para descargar e importar el entorno virtual GRFICSv2 para VirtualBox en Windows
#
# Ejecución remota:
#   iwr 'https://raw.githubusercontent.com/nipegun/Zubiri/refs/heads/main/CETI/SeguridadIndustrial/EntornosVulnerables/GRFICSv2/ImportarEnVirtualBoxDeWindows.ps1' | iex
# ----------

#
#  Referencia: https://github.com/Fortiphyd/GRFICSv2
#

$vURLBaseVMDKs = "http://hacks4geeks.com/_/descargas/MVs/Discos/Packs/GRFICSv2"

$VBoxManage = "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
$7zip       = "C:\Program Files\7-Zip\7z.exe"

$tmpDir = "$env:TEMP"

Write-Host ""
Write-Host "  Importador del entorno vulnerable GRFICSv2 para VirtualBox en Windows"
Write-Host ""

Write-Host "    Selecciona las acciones que quieras ejecutar (ej. 1 3 5 7 9 11):"
Write-Host ""
Write-Host "      1) Crear la máquina virtual pfSense"
Write-Host "      2)   Descargar, descomprimir e importar VHD para la MV pfSense"
Write-Host "      3) Crear la máquina virtual 3DChemicalPlant"
Write-Host "      4)   Descargar, descomprimir e importar VHD para la MV 3DChemicalPlant"
Write-Host "      5) Crear la máquina virtual PLC"
Write-Host "      6)   Descargar, descomprimir e importar VHD para la MV PLC"
Write-Host "      7) Crear la máquina virtual WorkStation"
Write-Host "      8)   Descargar, descomprimir e importar VHD para la MV WorkStation"
Write-Host "      9) Crear la máquina virtual HMIScadaBR"
Write-Host "     10)   Descargar, descomprimir e importar MV HMIScadaBR"
Write-Host "     11) Crear la máquina virtual Kali"
Write-Host "     12)   Descargar, descomprimir e importar VHD para la MV Kali"
Write-Host "     13) Agrupar MVs"
Write-Host "     14) Iniciar MVs en orden"
Write-Host ""
$choices = Read-Host "Opciones seleccionadas (Separadas por espacio)"

if ($choices -match '\b1\b') {
  Write-Host ""
  Write-Host "  Creando la máquina virtual pfSense..."
  Write-Host ""
  & $VBoxManage createvm --name "GRFICSv2-pfSense" --ostype "Linux_64" --register
  & $VBoxManage modifyvm        "GRFICSv2-pfSense" --cpus 2
  & $VBoxManage modifyvm        "GRFICSv2-pfSense" --memory 2048
  & $VBoxManage modifyvm        "GRFICSv2-pfSense" --graphicscontroller vmsvga --vram 128 --accelerate3d on
  & $VBoxManage modifyvm        "GRFICSv2-pfSense" --audio-driver none
  & $VBoxManage modifyvm        "GRFICSv2-pfSense" --nictype1 82540EM --nic1 intnet --intnet1 "RedIntOper" --nicpromisc1 allow-all
  & $VBoxManage modifyvm        "GRFICSv2-pfSense" --nictype2 82540EM --nic2 intnet --intnet2 "RedIntInd" --nicpromisc2 allow-all
  & $VBoxManage storagectl      "GRFICSv2-pfSense" --name "SATA Controller" --add sata --controller IntelAhci --portcount 2
  & $VBoxManage storageattach   "GRFICSv2-pfSense" --storagectl "SATA Controller" --port 0 --device 0 --type dvddrive --medium emptydrive
}

if ($choices -match '\b2\b') {
  Write-Host ""
  Write-Host "  Descargando, descomprimiendo e importando el VMDK para la MV pfSense..."
  Write-Host ""
  $disk = "GRFICSv2-pfSense.vmdk.xz"
  Invoke-WebRequest -Uri "$vURLBaseVMDKs/$disk" -OutFile "$tmpDir\$disk"
  & $7zip e "$tmpDir\$disk" -o"$tmpDir" -y
  Remove-Item "$tmpDir\$disk"
  $vmdk = "$tmpDir\\$($disk -replace '\.xz$', '')"
  $vmDir = (& $VBoxManage showvminfo "GRFICSv2-pfSense" --machinereadable | Select-String '^CfgFile=').ToString().Split('=')[1].Trim('"') | Split-Path
  Move-Item -Path $vmdk -Destination $vmDir -Force
  & $VBoxManage storageattach "GRFICSv2-pfSense" --storagectl "SATA Controller" --port 1 --device 0 --type hdd --medium (Join-Path $vmDir (Split-Path $vmdk -Leaf))
}

if ($choices -match '\b3\b') {
  Write-Host ""
  Write-Host "  Creando la máquina virtual 3DChemicalPlant..."
  Write-Host ""
  & $VBoxManage createvm --name "GRFICSv2-3DChemicalPlant" --ostype "Ubuntu_64" --register
  & $VBoxManage modifyvm        "GRFICSv2-3DChemicalPlant" --cpus 2
  & $VBoxManage modifyvm        "GRFICSv2-3DChemicalPlant" --memory 2048
  & $VBoxManage modifyvm        "GRFICSv2-3DChemicalPlant" --graphicscontroller vmsvga --vram 128 --accelerate3d on
  & $VBoxManage modifyvm        "GRFICSv2-3DChemicalPlant" --audio-driver none
  & $VBoxManage modifyvm        "GRFICSv2-3DChemicalPlant" --nictype1 virtio --nic1 intnet --intnet1 "RedIntInd" --nicpromisc1 allow-all
  & $VBoxManage storagectl      "GRFICSv2-3DChemicalPlant" --name "SATA Controller" --add sata --controller IntelAhci --portcount 1
  & $VBoxManage storageattach   "GRFICSv2-3DChemicalPlant" --storagectl "SATA Controller" --port 0 --device 0 --type dvddrive --medium emptydrive
  & $VBoxManage storagectl      "GRFICSv2-3DChemicalPlant" --name "VirtIO" --add "VirtIO" --bootable on --portcount 1
}

if ($choices -match '\b4\b') {
  Write-Host ""
  Write-Host "  Descargando, descomprimiendo e importando el VMDK para la MV 3DChemicalPlant..."
  Write-Host ""
  $disk = "GRFICSv2-3DChemicalPlant.vmdk.xz"
  Invoke-WebRequest -Uri "$vURLBaseVMDKs/$disk" -OutFile "$tmpDir\$disk"
  & $7zip e "$tmpDir\$disk" -o"$tmpDir" -y
  Remove-Item "$tmpDir\$disk"
  $vmdk = "$tmpDir\\$($disk -replace '\.xz$', '')"
  $vmDir = (& $VBoxManage showvminfo "GRFICSv2-3DChemicalPlant" --machinereadable | Select-String '^CfgFile=').ToString().Split('=')[1].Trim('"') | Split-Path
  Move-Item -Path $vmdk -Destination $vmDir -Force
  & $VBoxManage storageattach "GRFICSv2-3DChemicalPlant" --storagectl "SATA Controller" --port 1 --device 0 --type hdd --medium (Join-Path $vmDir (Split-Path $vmdk -Leaf))
}

if ($choices -match '\b5\b') {
  Write-Host ""
  Write-Host "  Creando la máquina virtual PLC..."
  Write-Host ""
  & $VBoxManage createvm --name "GRFICSv2-PLC" --ostype "Ubuntu" --register
  & $VBoxManage modifyvm        "GRFICSv2-PLC" --cpus 2
  & $VBoxManage modifyvm        "GRFICSv2-PLC" --memory 2048
  & $VBoxManage modifyvm        "GRFICSv2-PLC" --graphicscontroller vmsvga --vram 128 --accelerate3d on
  & $VBoxManage modifyvm        "GRFICSv2-PLC" --audio-driver none
  & $VBoxManage modifyvm        "GRFICSv2-PLC" --nictype1 virtio --nic1 intnet --intnet1 "RedIntInd" --nicpromisc1 allow-all
  & $VBoxManage storagectl      "GRFICSv2-PLC" --name "SATA Controller" --add sata --controller IntelAhci --portcount 1
  & $VBoxManage storageattach   "GRFICSv2-PLC" --storagectl "SATA Controller" --port 0 --device 0 --type dvddrive --medium emptydrive
  & $VBoxManage storagectl      "GRFICSv2-PLC" --name "VirtIO" --add "VirtIO" --bootable on --portcount 1
}

if ($choices -match '\b6\b') {
  Write-Host ""
  Write-Host "  Descargando, descomprimiendo e importando el VMDK para la MV PLC..."
  Write-Host ""
  $disk = "GRFICSv2-PLC.vmdk.xz"
  Invoke-WebRequest -Uri "$vURLBaseVMDKs/$disk" -OutFile "$tmpDir\$disk"
  & $7zip e "$tmpDir\$disk" -o"$tmpDir" -y
  Remove-Item "$tmpDir\$disk"
  $vmdk = "$tmpDir\\$($disk -replace '\.xz$', '')"
  $vmDir = (& $VBoxManage showvminfo "GRFICSv2-PLC" --machinereadable | Select-String '^CfgFile=').ToString().Split('=')[1].Trim('"') | Split-Path
  Move-Item -Path $vmdk -Destination $vmDir -Force
  & $VBoxManage storageattach "GRFICSv2-PLC" --storagectl "SATA Controller" --port 1 --device 0 --type hdd --medium (Join-Path $vmDir (Split-Path $vmdk -Leaf))
}


if ($choices -match '\b7\b') {
  Write-Host ""
  Write-Host "  Creando la máquina virtual WorkStation..."
  Write-Host ""
  & $VBoxManage createvm --name "GRFICSv2-WorkStation" --ostype "Ubuntu_64" --register
  & $VBoxManage modifyvm        "GRFICSv2-WorkStation" --cpus 2
  & $VBoxManage modifyvm        "GRFICSv2-WorkStation" --memory 2048
  & $VBoxManage modifyvm        "GRFICSv2-WorkStation" --graphicscontroller vmsvga --vram 128 --accelerate3d on
  & $VBoxManage modifyvm        "GRFICSv2-WorkStation" --audio-driver none
  & $VBoxManage modifyvm        "GRFICSv2-WorkStation" --nictype1 virtio --nic1 intnet --intnet1 "RedIntInd" --nicpromisc1 allow-all --macaddress1 080027383548
  & $VBoxManage storagectl      "GRFICSv2-WorkStation" --name "SATA Controller" --add sata --controller IntelAhci --portcount 1
  & $VBoxManage storageattach   "GRFICSv2-WorkStation" --storagectl "SATA Controller" --port 0 --device 0 --type dvddrive --medium emptydrive
  & $VBoxManage storagectl      "GRFICSv2-WorkStation" --name "VirtIO" --add "VirtIO" --bootable on --portcount 1
}

if ($choices -match '\b8\b') {
  Write-Host ""
  Write-Host "  Descargando, descomprimiendo e importando el VMDK para la MV WorkStation..."
  Write-Host ""
  $disk = "GRFICSv2-WorkStation.vmdk.xz"
  Invoke-WebRequest -Uri "$vURLBaseVMDKs/$disk" -OutFile "$tmpDir\$disk"
  & $7zip e "$tmpDir\$disk" -o"$tmpDir" -y
  Remove-Item "$tmpDir\$disk"
  $vmdk = "$tmpDir\\$($disk -replace '\.xz$', '')"
  $vmDir = (& $VBoxManage showvminfo "GRFICSv2-WorkStation" --machinereadable | Select-String '^CfgFile=').ToString().Split('=')[1].Trim('"') | Split-Path
  Move-Item -Path $vmdk -Destination $vmDir -Force
  & $VBoxManage storageattach "GRFICSv2-WorkStation" --storagectl "SATA Controller" --port 1 --device 0 --type hdd --medium (Join-Path $vmDir (Split-Path $vmdk -Leaf))
}

if ($choices -match '\b9\b') {
  Write-Host ""
  Write-Host "  Creando la máquina virtual HMIScadaBR..."
  Write-Host ""
  & $VBoxManage createvm --name "GRFICSv2-HMIScadaBR" --ostype "Ubuntu_64" --register
  & $VBoxManage modifyvm        "GRFICSv2-HMIScadaBR" --cpus 2
  & $VBoxManage modifyvm        "GRFICSv2-HMIScadaBR" --memory 2048
  & $VBoxManage modifyvm        "GRFICSv2-HMIScadaBR" --graphicscontroller vmsvga --vram 128 --accelerate3d on
  & $VBoxManage modifyvm        "GRFICSv2-HMIScadaBR" --audio-driver none
  & $VBoxManage modifyvm        "GRFICSv2-HMIScadaBR" --nictype1 virtio --nic1 intnet --intnet1 "RedIntOper" --nicpromisc1 allow-all
  & $VBoxManage storagectl      "GRFICSv2-HMIScadaBR" --name "SATA Controller" --add sata --controller IntelAhci --portcount 1
  & $VBoxManage storageattach   "GRFICSv2-HMIScadaBR" --storagectl "SATA Controller" --port 0 --device 0 --type dvddrive --medium emptydrive
  & $VBoxManage storagectl      "GRFICSv2-HMIScadaBR" --name "VirtIO" --add "VirtIO" --bootable on --portcount 1
}

if ($choices -match '\b10\b') {
  Write-Host ""
  Write-Host "  Descargando, descomprimiendo e importando el VMDK para la MV HMIScadaBR..."
  Write-Host ""
  $disk = "GRFICSv2-HMIScadaBR.vmdk.xz"
  Invoke-WebRequest -Uri "$vURLBaseVMDKs/$disk" -OutFile "$tmpDir\$disk"
  & $7zip e "$tmpDir\$disk" -o"$tmpDir" -y
  Remove-Item "$tmpDir\$disk"
  $vmdk = "$tmpDir\\$($disk -replace '\.xz$', '')"
  $vmDir = (& $VBoxManage showvminfo "GRFICSv2-HMIScadaBR" --machinereadable | Select-String '^CfgFile=').ToString().Split('=')[1].Trim('"') | Split-Path
  Move-Item -Path $vmdk -Destination $vmDir -Force
  & $VBoxManage storageattach "GRFICSv2-HMIScadaBR" --storagectl "SATA Controller" --port 1 --device 0 --type hdd --medium (Join-Path $vmDir (Split-Path $vmdk -Leaf))
}

if ($choices -match '\b11\b') {
  Write-Host ""
  Write-Host "  Creando la máquina virtual Kali..."
  Write-Host ""
  & $VBoxManage createvm --name "GRFICSv2-Kali" --ostype "Debian_64" --register
  & $VBoxManage modifyvm        "GRFICSv2-Kali" --cpus 2
  & $VBoxManage modifyvm        "GRFICSv2-Kali" --memory 2048
  & $VBoxManage modifyvm        "GRFICSv2-Kali" --graphicscontroller vmsvga --vram 128 --accelerate3d on
  & $VBoxManage modifyvm        "GRFICSv2-Kali" --audio-driver none
  & $VBoxManage modifyvm        "GRFICSv2-Kali" --nictype1 virtio --nic1 intnet --intnet1 "RedIntOper" --nicpromisc1 allow-all
  & $VBoxManage storagectl      "GRFICSv2-Kali" --name "SATA Controller" --add sata --controller IntelAhci --portcount 1
  & $VBoxManage storageattach   "GRFICSv2-Kali" --storagectl "SATA Controller" --port 0 --device 0 --type dvddrive --medium emptydrive
  & $VBoxManage storagectl      "GRFICSv2-Kali" --name "VirtIO" --add "VirtIO" --bootable on --portcount 1
}

if ($choices -match '\b12\b') {
  Write-Host ""
  Write-Host "  Descargando, descomprimiendo e importando el VMDK para la MV Kali..."
  Write-Host ""
  $disk = "GRFICSv2-Kali.vmdk.xz"
  Invoke-WebRequest -Uri "$vURLBaseVMDKs/$disk" -OutFile "$tmpDir\$disk"
  & $7zip e "$tmpDir\$disk" -o"$tmpDir" -y
  Remove-Item "$tmpDir\$disk"
  $vmdk = "$tmpDir\\$($disk -replace '\.xz$', '')"
  $vmDir = (& $VBoxManage showvminfo "GRFICSv2-Kali" --machinereadable | Select-String '^CfgFile=').ToString().Split('=')[1].Trim('"') | Split-Path
  Move-Item -Path $vmdk -Destination $vmDir -Force
  & $VBoxManage storageattach "GRFICSv2-Kali" --storagectl "SATA Controller" --port 1 --device 0 --type hdd --medium (Join-Path $vmDir (Split-Path $vmdk -Leaf))
}

if ($choices -match '\b13\b') {
  Write-Host ""
  Write-Host "  Agrupando máquinas virtuales..."
  Write-Host ""
  & $VBoxManage modifyvm "GRFICSv2-pfSense"         --groups "/GRFICSv2"
  & $VBoxManage modifyvm "GRFICSv2-3DChemicalPlant" --groups "/GRFICSv2" 2> $null
  & $VBoxManage modifyvm "GRFICSv2-PLC"             --groups "/GRFICSv2" 2> $null
  & $VBoxManage modifyvm "GRFICSv2-WorkStation"     --groups "/GRFICSv2" 2> $null
  & $VBoxManage modifyvm "GRFICSv2-HMIScadaBR"      --groups "/GRFICSv2" 2> $null
  & $VBoxManage modifyvm "GRFICSv2-Kali"            --groups "/GRFICSv2" 2> $null
}

if ($choices -match '\b14\b') {
  Write-Host ""
  Write-Host "  Iniciando máquinas virtuales en orden..."
  Write-Host ""
  & $VBoxManage startvm "GRFICSv2-pfSense"
  Start-Sleep -Seconds 15
  & $VBoxManage startvm "GRFICSv2-3DChemicalPlant"
  Start-Sleep -Seconds 15
  & $VBoxManage startvm "GRFICSv2-PLC"
  Start-Sleep -Seconds 15
  & $VBoxManage startvm "GRFICSv2-WorkStation"
  Start-Sleep -Seconds 15
  & $VBoxManage startvm "GRFICSv2-HMIScadaBR"
  Start-Sleep -Seconds 15
  & $VBoxManage startvm "GRFICSv2-Kali"
}
