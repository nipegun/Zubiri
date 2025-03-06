// Crear una conexión WebSocket con el servidor
const socket = new WebSocket("ws://localhost:8001"); // Cambia el puerto si es necesario

socket.onmessage = function(event) {
  let payload = event.data.trim();
  console.log("Payload recibido:", payload);

  if (payload in payloadMapping) {
    let { id, color } = payloadMapping[payload];
    let element = document.getElementById(id);

    if (element) {
      element.style.backgroundColor = color;
      console.log(`Cambiando color de ${id} a ${color}`);
    } else {
      console.log(`Elemento ${id} no encontrado en la tabla.`);
    }
  } else {
    console.log("Payload desconocido:", payload);
  }
};

socket.onerror = function(error) {
  console.log("Error en la conexión WebSocket:", error);
};

socket.onclose = function() {
  console.log("Conexión WebSocket cerrada.");
};
