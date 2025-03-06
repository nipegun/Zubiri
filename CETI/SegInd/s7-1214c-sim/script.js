function updateData() {
  fetch("/states")
    .then(response => response.json())
    .then(states => {
      for (let key in states) {
        let element = document.getElementById(key);
        if (element) {
          if (states[key] === "on") {
            element.style.backgroundColor = "green";
          } else if (states[key] === "off") {
            element.style.backgroundColor = "red";
          } else {
            element.style.backgroundColor = "gray"; // Unknown
          }
        }
      }
    })
    .catch(err => console.log("Error:", err));
}

setInterval(updateData, 500); // Actualizar cada 500 ms
