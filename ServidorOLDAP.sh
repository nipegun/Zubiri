#!/bin/bash

#echo "servidor" > /etc/hostname
#echo "192.168.100.100 servidor.practica.com" >> /etc/hosts
#apt-get -y update
#apt-get -y install slapd
#apt-get -y install ldap-utils
#dpkg-reconfigure slapd
#slapcat

echo ""
echo "  Agregando unidades organizativas..."
echo ""
mkdir -p /root/OpenLDAP/ 2> /dev/null
echo "dn: ou=profesores,dc=practica,dc=com"   > /root/OpenLDAP/UnidadesOrganizativas.ldif
echo "objectClass: organizationalUnit"       >> /root/OpenLDAP/UnidadesOrganizativas.ldif
echo "ou: profesores"                        >> /root/OpenLDAP/UnidadesOrganizativas.ldif
echo ""                                      >> /root/OpenLDAP/UnidadesOrganizativas.ldif
echo "dn: ou=alumnos,dc=practica,dc=com"     >> /root/OpenLDAP/UnidadesOrganizativas.ldif
echo "objectClass: organizationalUnit"       >> /root/OpenLDAP/UnidadesOrganizativas.ldif
echo "ou: alumnos"                           >> /root/OpenLDAP/UnidadesOrganizativas.ldif
ldapadd -x -D cn=admin,dc=practica,dc=com -W -f /root/OpenLDAP/UnidadesOrganizativas.ldif

echo ""
echo "  Agregando usuarios..."
echo ""
mkdir -p /root/OpenLDAP/ 2> /dev/null
echo "dn: uid=profe1,ou=profesores,dc=practica,dc=com"  > /root/OpenLDAP/Usuarios.ldif
echo "objectClass: inetOrgPerson"                      >> /root/OpenLDAP/Usuarios.ldif
echo "objectClass: posixAccount"                       >> /root/OpenLDAP/Usuarios.ldif
echo "cn: Albert"                                      >> /root/OpenLDAP/Usuarios.ldif # Requerido si hay inetOrgPerson y posixAccount
echo "sn: Einstein"                                    >> /root/OpenLDAP/Usuarios.ldif # Requerido si hay inetOrgPerson
echo "uid: profe1"                                     >> /root/OpenLDAP/Usuarios.ldif # Requerido si hay posixAccount
echo "uidNumber: 2000"                                 >> /root/OpenLDAP/Usuarios.ldif # Requerido si hay posixAccount
echo "gidNumber: 10000"                                >> /root/OpenLDAP/Usuarios.ldif # Requerido si hay posixAccount
echo "homeDirectory: /home/profe1"                     >> /root/OpenLDAP/Usuarios.ldif # Requerido si hay posixAccount
echo ""                                                >> /root/OpenLDAP/Usuarios.ldif # Debe haber una línea vacía entre dn y dn
echo "dn: uid=alumno1,ou=alumnos,dc=practica,dc=com"   >> /root/OpenLDAP/Usuarios.ldif
echo "objectClass: inetOrgPerson"                      >> /root/OpenLDAP/Usuarios.ldif
echo "objectClass: posixAccount"                       >> /root/OpenLDAP/Usuarios.ldif
echo "cn: Pepe"                                        >> /root/OpenLDAP/Usuarios.ldif # Requerido si hay inetOrgPerson y posixAccount
echo "sn: Goteras"                                     >> /root/OpenLDAP/Usuarios.ldif # Requerido si hay inetOrgPerson
echo "uid: alumno1"                                    >> /root/OpenLDAP/Usuarios.ldif # Requerido si hay posixAccount
echo "uidNumber: 2002"                                 >> /root/OpenLDAP/Usuarios.ldif # Requerido si hay posixAccount
echo "gidNumber: 10002"                                >> /root/OpenLDAP/Usuarios.ldif # Requerido si hay posixAccount
echo "homeDirectory: /home/alumno1"                    >> /root/OpenLDAP/Usuarios.ldif # Requerido si hay posixAccount
echo ""                                                >> /root/OpenLDAP/Usuarios.ldif # Debe haber una línea vacía entre dn y dn
echo "dn: uid=alumno2,ou=alumnos,dc=practica,dc=com"   >> /root/OpenLDAP/Usuarios.ldif
echo "objectClass: inetOrgPerson"                      >> /root/OpenLDAP/Usuarios.ldif
echo "objectClass: posixAccount"                       >> /root/OpenLDAP/Usuarios.ldif
echo "cn: Collin"                                      >> /root/OpenLDAP/Usuarios.ldif # Requerido si hay inetOrgPerson y posixAccount
echo "sn: McRae"                                       >> /root/OpenLDAP/Usuarios.ldif # Requerido si hay inetOrgPerson
echo "uid: alumno2"                                    >> /root/OpenLDAP/Usuarios.ldif # Requerido si hay posixAccount
echo "uidNumber: 2003"                                 >> /root/OpenLDAP/Usuarios.ldif # Requerido si hay posixAccount
echo "gidNumber: 10003"                                >> /root/OpenLDAP/Usuarios.ldif # Requerido si hay posixAccount
echo "homeDirectory: /home/alumno2"                    >> /root/OpenLDAP/Usuarios.ldif # Requerido si hay posixAccount
ldapadd -x -D cn=admin,dc=practica,dc=com -W -f           /root/OpenLDAP/Usuarios.ldif

 # echo ""
 # echo "  Mostrando los usuarios creados..."
 # echo ""
 # ldapsearch -xLLL -b "dc=$vDominio,dc=$vExtDominio" uid=nipegun sn givenName cn
