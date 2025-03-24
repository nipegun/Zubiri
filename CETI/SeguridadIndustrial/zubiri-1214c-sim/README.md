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

El simulador está preparado para comunicarse con múltiples clientes, pero sólo responderá a los siguientes primeros payloads:

Payload de solicitud de comunicación COTP para encendido o apagado del PLC:
```
030000231ee00000006400c1020600c20f53494d415449432d524f4f542d4553c0010a
```
Payload de solicitud de comunicación COTP para encendido o apagado de salida:
```
0300001611e00000cfc400c0010ac1020100c2020101
```

Y sólo respondera a los segundos payloads:

Payload de solicitud de comunicación S7CommPlus para encendido o apagado del PLC:
```
030000ee02f080720100df31000004ca0000000100000120360000011d00040000000000a1000000d3821f0000a3816900151553657276657253657373696f6e5f31433943333846a38221001532302e302e302e303a305265616c74656b20555342204762452046616d696c7920436f6e74726f6c6c65722e54435049502e33a38228001500a38229001500a3822a0015194445534b544f502d494e414d4455385f313432323331343036a3822b000401a3822c001201c9c38fa3822d001500a1000000d3817f0000a38169001515537562736372697074696f6e436f6e7461696e6572a2a20000000072010000
```

Payload de solicitud de comunicación S7CommPlus para encendido o apagado de salida:
```
0300001902f08032010000000000080000f0000008000803c0
```

A partir del tercer payload, como el cliente debe responder al challenge con el anti-replay, los payloads pueden cambiar.

## Cliente gráfico

Si ejecutamos el archivo client.py con la IP del servidor como parámetro, podremos dar órdenes al simulador y ver como los cambios se reflejan en la interfaz web. Para lanzar el cliente, ejecutamos:

```
~/zubiri-1214c-sim/client.py 127.0.0.1
```
<p align="center">
  <img src="https://github.com/nipegun/Zubiri/blob/main/CETI/SeguridadIndustrial/zubiri-1214c-sim/images/client.png" />
</p>
