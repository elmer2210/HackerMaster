// Nivel actual (esto se puede cargar dinámicamente desde el backend)
let nivelActual = 1;

document.addEventListener("DOMContentLoaded", () => {
  cargarEnunciado(nivelActual);
});

function cargarEnunciado(nivel) {
  const enunciados = {
    1: "Has interceptado un mensaje cifrado. Las letras en mayúscula forman una clave secreta.\nEntrada: \"aBcdEfgHijK\"",
    2: "Completa la secuencia: 2, 4, 8, __, 32",
    3: "¿Es 'reconocer' un palíndromo?",
    4: "Cifra César: Descifra 'Krod' si el desplazamiento fue de 3 letras",
    5: "Suma los dígitos pares del número: 482713",
    6: "Imprime los primeros 6 números de Fibonacci usando recursividad"
  };

  document.getElementById("enunciado").textContent = enunciados[nivel] || "No hay más retos.";
}

function enviarRespuesta() {
  const nombre = document.getElementById("playerName").value.trim();
  const respuesta = document.getElementById("respuesta").value.trim();

  if (!nombre || !respuesta) {
    document.getElementById("salida").textContent = "⚠️ Debes ingresar tu nombre y una respuesta.";
    return;
  }

  fetch("/evaluar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nombre: nombre,
      nivel: nivelActual,
      respuesta: respuesta
    })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("salida").textContent = data.mensaje;

    if (data.correcto) {
      nivelActual += 1;
      cargarEnunciado(nivelActual);
      document.getElementById("respuesta").value = "";
    }
  })
  .catch(() => {
    document.getElementById("salida").textContent = "❌ Error de conexión con el servidor.";
  });
}
