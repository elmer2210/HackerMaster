
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
