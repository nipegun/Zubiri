// script.js

function fColorPorEstado(pValor) {
  if (pValor === "on")      return "background-color: green;";
  if (pValor === "off")     return "background-color: red;";
  if (pValor === "unknown") return "background-color: white;";
  return "";
}

function fActualizarEstados(pEstados) {
  // Estado PLC (asumimos power_status puede ser "on", "off", "unknown")
  const plcStatus = pEstados.plc?.power_status || "unknown";
  const plcCell = document.getElementById('Corriente');
  plcCell.innerText = "CORRIENTE"; // No texto, solo color
  plcCell.setAttribute("style", fColorPorEstado(plcStatus));

  // Salidas digitales
  for (const salida in pEstados.digital_outputs) {
    const el = document.getElementById(salida);
    if (el) {
      el.innerText = salida; // Solo el nombre, sin estado
      el.setAttribute("style", fColorPorEstado(pEstados.digital_outputs[salida]));
    }
  }

  // Entradas digitales
  for (const entrada in pEstados.digital_inputs) {
    const el = document.getElementById(entrada);
    if (el) {
      el.innerText = entrada; // Solo el nombre, sin estado
      el.setAttribute("style", fColorPorEstado(pEstados.digital_inputs[entrada]));
    }
  }

  // Entradas analógicas
  for (const anal in pEstados.analog_inputs) {
    const el = document.getElementById(anal);
    if (el) {
      el.innerText = anal; // Solo el nombre, sin estado
      el.setAttribute("style", fColorPorEstado(pEstados.analog_inputs[anal]));
    }
  }
}

// --- WebSocket ---

let vWebSocket = null;
let vURLDelWebSocket = (window.location.protocol === "https:" ? "wss://" : "ws://") + window.location.host + "/ws";

function fConectarWebSocket() {
  vWebSocket = new WebSocket(vURLDelWebSocket);

  vWebSocket.onopen = () => {
    console.log("WebSocket conectado");
  };

  vWebSocket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      fActualizarEstados(data);
    } catch (e) {
      console.error("Error parseando estado recibido:", e);
    }
  };

  vWebSocket.onclose = () => {
    console.warn("WebSocket cerrado. Intentando reconectar en 3 segundos...");
    setTimeout(() => fConectarWebSocket(), 3000);
  };

  vWebSocket.onerror = (e) => {
    console.error("WebSocket error:", e);
    vWebSocket.close();
  };
}

window.addEventListener('DOMContentLoaded', fConectarWebSocket);

