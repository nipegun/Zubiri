// Mapeo de payloads a IDs de salida y colores
const payloadMapping = {
  '0300002502f08032010000001f000e00060501120a10010001000082000000000300010100': { id: '%Q0.0', color: 'green' },
  '0300002502f08032010000001f000e00060501120a10010001000082000001000300010100': { id: '%Q0.1', color: 'green' },
  '0300002502f08032010000001f000e00060501120a10010001000082000002000300010100': { id: '%Q0.2', color: 'green' },
  '0300002502f08032010000001f000e00060501120a10010001000082000003000300010100': { id: '%Q0.3', color: 'green' },
  '0300002502f08032010000001f000e00060501120a10010001000082000004000300010100': { id: '%Q0.4', color: 'green' },
  '0300002502f08032010000001f000e00060501120a10010001000082000005000300010100': { id: '%Q0.5', color: 'green' },
  '0300002502f08032010000001f000e00060501120a10010001000082000006000300010100': { id: '%Q0.6', color: 'green' },
  '0300002502f08032010000001f000e00060501120a10010001000082000007000300010100': { id: '%Q0.7', color: 'green' },
  '0300002502f08032010000001f000e00060501120a10010001000082000008000300010100': { id: '%Q0.8', color: 'green' },
  '0300002502f08032010000001f000e00060501120a10010001000082000009000300010100': { id: '%Q0.9', color: 'green' },

  '0300002502f08032010000001f000e00060501120a10010001000082000000000300010000': { id: '%Q0.0', color: 'red' },
  '0300002502f08032010000001f000e00060501120a10010001000082000001000300010000': { id: '%Q0.1', color: 'red' },
  '0300002502f08032010000001f000e00060501120a10010001000082000002000300010000': { id: '%Q0.2', color: 'red' },
  '0300002502f08032010000001f000e00060501120a10010001000082000003000300010000': { id: '%Q0.3', color: 'red' },
  '0300002502f08032010000001f000e00060501120a10010001000082000004000300010000': { id: '%Q0.4', color: 'red' },
  '0300002502f08032010000001f000e00060501120a10010001000082000005000300010000': { id: '%Q0.5', color: 'red' },
  '0300002502f08032010000001f000e00060501120a10010001000082000006000300010000': { id: '%Q0.6', color: 'red' },
  '0300002502f08032010000001f000e00060501120a10010001000082000007000300010000': { id: '%Q0.7', color: 'red' },
  '0300002502f08032010000001f000e00060501120a10010001000082000008000300010000': { id: '%Q0.8', color: 'red' },
  '0300002502f08032010000001f000e00060501120a10010001000082000009000300010000': { id: '%Q0.9', color: 'red' }
};

function updateData() {
  // Agregar timestamp para evitar la caché del navegador
  let url = "/states?t=" + new Date().getTime();

  fetch(url)
    .then(response => response.json()) // Obtener los datos de states.json
    .then(states => {
      console.log("Estados recibidos:", states); // DEBUG: Verifica en consola

      // Actualizar los colores de los outputs
      for (let key in states.outputs) {
        let element = document.getElementById(key);
        if (element) {
          if (states.outputs[key] === "on") {
            element.style.backgroundColor = "green";
          } else if (states.outputs[key] === "off") {
            element.style.backgroundColor = "red";
          } else {
            element.style.backgroundColor = "gray"; // Unknown
          }
        } else {
          console.log("Elemento no encontrado en la tabla:", key); // DEBUG
        }
      }
    })
    .catch(err => console.log("Error en la actualización:", err));
}

// Ejecutar updateData() cada 500 ms
setInterval(updateData, 500);
