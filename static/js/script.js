
let playerName = "";
let nivelActual = 1;

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("startBtn").addEventListener("click", iniciarJuego);
  document.getElementById("sendBtn").addEventListener("click", enviarRespuesta);
});

function iniciarJuego() {
  playerName = document.getElementById("playerName").value.trim();

  if (!playerName) {
    alert("⚠️ Debes ingresar tu nombre para comenzar.");
    return;
  }

  // Oculta formulario de inicio y muestra el juego
  document.getElementById("inicio").style.display = "none";
  document.getElementById("consola").style.display = "block";

  cargarRetoDesdeBackend();
}

function cargarRetoDesdeBackend() {
  fetch("/get_challenge", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: playerName })
  })
  .then(res => res.json())
  .then(data => {
    nivelActual = data.level;
    document.getElementById("nivel").textContent = `Nivel ${data.level}`;
    document.getElementById("enunciado").textContent = data.challenge;
    document.getElementById("pista").textContent = `💡 ${data.hint}`;
    document.getElementById("salida").textContent = "";
    document.getElementById("respuesta").value = "";
  });
}

function enviarRespuesta() {
  const respuesta = document.getElementById("respuesta").value.trim();

  if (!respuesta) {
    document.getElementById("salida").textContent = "⚠️ Ingresa una respuesta.";
    return;
  }

  fetch("/evaluate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: playerName,
      answer: respuesta
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.finished) {
      window.location.href = data.redirect_url;
      return;
    }

    document.getElementById("salida").textContent = data.is_correct
      ? "✅ Correcto. Cargando siguiente nivel..."
      : "❌ Incorrecto. Intenta otra vez.";

    if (data.is_correct) {
      // Cargar el siguiente reto desde el backend
      document.getElementById("respuesta").value = "";
      setTimeout(() => {
        document.getElementById("salida").textContent = "";
        document.getElementById("pista").textContent = "";
        document.getElementById("nivel").textContent = `Nivel ${data.next_level}`;
        document.getElementById("enunciado").textContent = data.challenge;
        document.getElementById("pista").textContent = `💡 ${data.hint}`;
      }, 1200);
    }
  })
  .catch(() => {
    document.getElementById("salida").textContent = "❌ Error de conexión con el servidor.";
  });
}
