# zubiri-1214c-sim

Simulador del PLC Siemens S7-1200 1214c de la clase Cyber Range del instituto de formación profesional Zubiri Manteo.

## Instalación

Para instalarlo, ejecutamos:

**En Linux (distros basadas en Debian):**

```
curl -sL https://raw.githubusercontent.com/nipegun/Zubiri/refs/heads/main/CETI/SeguridadIndustrial/zubiri-1214c-sim/install_reinstall_update.sh | bash
```

**En Windows:**

(TODAVÍA NO DISPNIBLE)

## Ejecución

Las instrucciones de ejecución aparecerán en la misma terminal una vez finalizada la instalación. Pero, para futuras consultas, la forma correcta de ejecutar el simulador es:

```
cd ~/zubiri-1214c-sim/ && ./server.py
```

Es importante que se ejecute desde la misma carpeta donde están el resto de los archivos que conforman el paquete. En el caso de no haberlo ejecutado como root, se solicitarán permisos sudo.

## Web

Una vez iniciado, podremos acceder a la web del servidor desde el ordenador donde se ejecuta (con IP http://127.0.0.1:8000), desde la IP del servidor en la subred (por ejemplo: http://172.16.4.200:8000) o desde una IP pública (si tenemos configurado el reenvío de puertos).

<p align="center">
  <img src="https://github.com/nipegun/Zubiri/blob/main/CETI/SeguridadIndustrial/zubiri-1214c-sim/images/web.png" />
</p>

## Re-instalación o actualización

Para reinstalarlo o actualizarlo a la última versión, ejecutamos:

```
~/zubiri-1214c-sim/install_reinstall_update.sh
```

## APIs

El servidor pone a disposición de los usuarios dos APIs JSON diferentes:

/api/states

...donde se pueden consultar el estado de las salidas y entradas del PLC simulado y

/api/sessions

...donde se pueden consultar las sesiones activas que mantiene con los clientes y los payloads que estos han enviado. De esta forma es posible diagnosticar los motivos por los cuales un payload pueda no estar provocando los cambios deseados en el simulador.

## Interacción con los clientes

El simulador está preparado para comunicarse con múltimples clientes pero sólo responderá a los siguientes primeros payloads:

Payload de solicitud de comuniocación COTP para encendido o apagado del PLC:
```
.
```
Payload de solicitud de comuniocación COTP para modificaciencendido o apagado del PLC:
```
.
```

Payload de solicitud de comunicación S7CommPlus:

servidor está preparado para recibir los payload típicos de solicitud de comunicacionSi ejecutamos el archivo client.py con la IP del servidor como parámetro, podremos dar órdenes al simulador y ver como los cambios se reflejan en la interfaz web. Para lanzar el cliente, ejecutamos:

```
~/zubiri-1214c-sim/client.py 127.0.0.1
```
<p align="center">
  <img src="https://github.com/nipegun/Zubiri/blob/main/CETI/SeguridadIndustrial/zubiri-1214c-sim/images/client.png" />
</p>
