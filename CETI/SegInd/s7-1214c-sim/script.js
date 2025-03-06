async function actualizarColores() {
  try {
    const response = await fetch('states.json');
    if (!response.ok) {
      throw new Error("No se pudo cargar el archivo JSON");
    }
    const data = await response.json();
    console.log("Datos JSON cargados:", data);

    const colores = {
      "on": "green",
      "off": "red",
      "unknown": "white"
    };

    for (let id in data.outputs) {
      let estado = data.outputs[id];
      console.log("Actualizando", id, "con estado:", estado);
      let td = document.getElementById(id);
      if (td) {
        td.style.backgroundColor = colores[estado] || "gray";
      } else {
        console.warn("No se encontró elemento con id:", id);
      }
    }
  } catch (error) {
    console.error("Error al cargar el JSON:", error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  actualizarColores();
  setInterval(actualizarColores, 1000);
});
