#!/bin/bash

echo ""
echo "  Agregando usuarios..."
echo ""
mkdir -p /root/OpenLDAP/ 2> /dev/null
echo "dn: uid=profe2,ou=profesores,dc=practica,dc=com"  > /root/OpenLDAP/Usuarios2.ldif
echo "objectClass: inetOrgPerson"                      >> /root/OpenLDAP/Usuarios2.ldif
echo "objectClass: posixAccount"                       >> /root/OpenLDAP/Usuarios2.ldif
echo "cn: Nahikari"                                    >> /root/OpenLDAP/Usuarios2.ldif # Requerido si hay inetOrgPerson y posixAccount
echo "sn: Iturralde"                                   >> /root/OpenLDAP/Usuarios2.ldif # Requerido si hay inetOrgPerson
echo "uid: profe2"                                     >> /root/OpenLDAP/Usuarios2.ldif # Requerido si hay posixAccount
echo "uidNumber: 2004"                                 >> /root/OpenLDAP/Usuarios2.ldif # Requerido si hay posixAccount
echo "gidNumber: 10004"                                >> /root/OpenLDAP/Usuarios2.ldif # Requerido si hay posixAccount
echo "homeDirectory: /home/profe2"                     >> /root/OpenLDAP/Usuarios2.ldif # Requerido si hay posixAccount
echo ""                                                >> /root/OpenLDAP/Usuarios2.ldif # Debe haber una línea vacía entre dn y dn
echo "dn: uid=alumno3,ou=alumnos,dc=practica,dc=com"   >> /root/OpenLDAP/Usuarios2.ldif
echo "objectClass: inetOrgPerson"                      >> /root/OpenLDAP/Usuarios2.ldif
echo "objectClass: posixAccount"                       >> /root/OpenLDAP/Usuarios2.ldif
echo "cn: Ana"                                         >> /root/OpenLDAP/Usuarios2.ldif # Requerido si hay inetOrgPerson y posixAccount
echo "sn: Urroz"                                       >> /root/OpenLDAP/Usuarios2.ldif # Requerido si hay inetOrgPerson
echo "uid: alumno3"                                    >> /root/OpenLDAP/Usuarios2.ldif # Requerido si hay posixAccount
echo "uidNumber: 2005"                                 >> /root/OpenLDAP/Usuarios2.ldif # Requerido si hay posixAccount
echo "gidNumber: 10005"                                >> /root/OpenLDAP/Usuarios2.ldif # Requerido si hay posixAccount
echo "homeDirectory: /home/alumno3"                    >> /root/OpenLDAP/Usuarios2.ldif # Requerido si hay posixAccount
ldapadd -x -D cn=admin,dc=practica,dc=com -W -f           /root/OpenLDAP/Usuarios2.ldif
