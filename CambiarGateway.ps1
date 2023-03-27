

$vGateway="10.14.7.251"
$vCIDR="8"

$vIPyaAsignada=Get-NetIPAddress -AddressFamily IPV4 -PrefixOrigin Dhcp | Select -ExpandProperty IPAddress
$vIndiceDeLaInterfaz=Get-NetIPAddress -AddressFamily IPV4 -PrefixOrigin Dhcp | Select -ExpandProperty InterfaceIndex

New-NetIPAddress 朓PAddress $vIPyaAsignada -DefaultGateway $vGateway -PrefixLength $vCIDR -InterfaceIndex $vIndiceDeLaInterfaz
New-NetIPAddress 朓PAddress $vIPyaAsignada -DefaultGateway $vGateway -PrefixLength $vCIDR -InterfaceIndex (Get-NetAdapter).$vIndiceDeLaInterfaz

