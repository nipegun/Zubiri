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

Las instrucciones de ejecución aparecerán en la misma terminal una vez finalizada la instalación. Se solicitarán permisos sudo, en el caso de no haberlo ejecutado como root. Una vez instalado, podremos acceder a la web del servidor desde el ordenador donde se ejecuta (con IP http://127.0.0.1:8000), desde la IP del servidor en la subred (por ejemplo: http://172.16.4.200:8000) o desde una IP pública (si tenemos configurado el reenvío de puertos).

<p align="center">
  <img src="https://github.com/nipegun/Zubiri/blob/main/CETI/SeguridadIndustrial/zubiri-1214c-sim/images/web.png" />
</p>

## Re-instalación o actualización

Para reinstalarlo o actualizarlo a la última versión, ejecutamos:

```
~/zubiri-1214c-sim/install_reinstall_update.sh
```

## Interacción del cliente

Si ejecutamos el archivo client.py con la IP del servidor como parámetro, podremos dar órdenes al simulador y ver como los cambios se reflejan en la interfaz web. Para lanzar el cliente, ejecutamos:

```
~/zubiri-1214c-sim/client.py
```
<p align="center">
  <img src="https://github.com/nipegun/Zubiri/blob/main/CETI/SeguridadIndustrial/zubiri-1214c-sim/images/client.png" />
</p>

## APIs

El servidor pone a disposición de los usuarios dos APIs JSON diferentes:

/api/states

...donde se pueden consultar el estado de las salidas y entradas del PLC simulado y

/api/sessions

...donde se pueden consultar las sesiones activas que mantiene con los clientes y los payloads que estos han enviado. De esta forma es posible diagnosticar los motivos por los cuales un payload pueda no estar provocando los cambios deseados en el simulador.
