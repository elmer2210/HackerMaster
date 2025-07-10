let playerName = "";
let nivelActual = 1;

document.addEventListener("DOMContentLoaded", () => {
    // Inicializar elementos del DOM
    // Asignar eventos a botones
  document.getElementById("startBtn").addEventListener("click", starPlay);
  document.getElementById("sendBtn").addEventListener("click", sendResponse);
  document.getElementById("reloadBtn").addEventListener("click", reloadPlay);
});

function starPlay() {
  playerName = document.getElementById("playerName").value.trim();

  if (!playerName) {
    alert("⚠️ Debes ingresar tu nombre para comenzar.");
    return;
  }

  // Oculta pantalla de inicio y muestra consola de juego
  document.getElementById("inicio").style.display = "none";
  document.getElementById("consola").style.display = "block";

  // Cargar primer reto desde el backend
  loadChallengeBackend();
}

function loadChallengeBackend() {
  fetch("/get_challenge", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: playerName })
  })
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        document.getElementById("salida").textContent = data.error;
        return;
      }

      nivelActual = data.level;
      document.getElementById("nivel").textContent = `Nivel ${data.level}`;
      document.getElementById("enunciado").textContent = data.challenge;
      document.getElementById("pista").textContent = `💡 ${data.hint}`;
      document.getElementById("respuesta").value = "";
      document.getElementById("salida").textContent = "";
    })
    .catch(() => {
      document.getElementById("salida").textContent = "❌ Error al obtener el reto.";
    });

}

// Enviar respuesta al servidor
function sendResponse() {
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
        alert(data.message);
        window.location.href = data.redirect_url; // Ir a métricas
        return;
      }

      // Mostrar feedback
      document.getElementById("salida").textContent = data.message;

      // Si es correcta, limpiar y cargar siguiente reto tras una pausa
      if (data.is_correct) {
        setTimeout(() => {
          document.getElementById("respuesta").value = "";
          document.getElementById("salida").textContent = "";
          document.getElementById("pista").textContent = "";
          cargarRetoDesdeBackend(); // ← NUEVO RETO ALEATORIO
        }, 1200);
      }
    })
    .catch(() => {
      document.getElementById("salida").textContent = "❌ Error de conexión con el servidor.";
    });
}

// Reiniciar juego
function reloadPlay() {
  // Restablece variables
  playerName = "";
  nivelActual = 1;

  // Muestra la pantalla de inicio
  document.getElementById("inicio").style.display = "block";
  document.getElementById("consola").style.display = "none";

  // Limpia todos los campos
  document.getElementById("playerName").value = "";
  document.getElementById("nivel").textContent = "";
  document.getElementById("enunciado").textContent = "";
  document.getElementById("pista").textContent = "";
  document.getElementById("salida").textContent = "";
  document.getElementById("respuesta").value = "";
}
