let playerName = "";
let nivelActual = 1;

const terminal = document.querySelector(".terminal");

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
      console.log(data);
      document.getElementById("playerNameDisplay").textContent = playerName;
      document.getElementById("attempts").innerHTML= `<i class="fa-solid fa-heart"></i> ${data.attempts}`;
      document.getElementById("correct_attempts").innerHTML = `<i class="fa-solid fa-web-awesome"></i> ${data.corret_attempts}`;
      document.getElementById("failed_attempts").innerHTML = `<i class="fa-solid fa-skull"></i> ${data.failed_attempts}`;
      document.getElementById("nivel").textContent = `Nivel ${data.level}`;
      document.getElementById("reto").innerHTML = `<i class="fa-solid fa-chevron-right"></i> ${data.challenge}`;
      document.getElementById("pista").innerHTML = `<i class="fa-solid fa-lightbulb"></i> ${data.hint}`;
      document.getElementById("respuesta").value = "";
      document.getElementById("salida").textContent = "";
    })
    .catch(() => {
      document.getElementById("salida").innerHTML = `<i class="fa-solid fa-circle-xmark"></i> Error al obtener el reto.`;
    });

}

function sendResponse() {
  const respuesta = document.getElementById("respuesta").value.trim();
  if (!respuesta) {
    document.getElementById("salida").innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> Ingresa una respuesta.`;
     // Animación simple de parpadeo rojo en consola
    terminal.classList.add("error-blink");
    setTimeout(() => terminal.classList.remove("error-blink"), 400);
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
    // Mostrar feedback
    document.getElementById("salida").textContent = data.message;
    document.getElementById("attempts").innerHTML= `<i class="fa-solid fa-heart"></i> ${data.attempts}`;
    document.getElementById("correct_attempts").innerHTML = `<i class="fa-solid fa-web-awesome"></i> ${data.corret_attempts}`;
    document.getElementById("failed_attempts").innerHTML = `<i class="fa-solid fa-skull"></i> ${data.failed_attempts}`;

    if (data.finished) {
      showVictory(data.message);
      return;
    }
    if (data.game_over) {
      showGameOver(data.message);
      return; // Ya terminó, no sigas mostrando el juego
    }

    if (data.is_correct) {
      
      console.log("Respuesta correcta:", data);
      // Detectar si subió de nivel
      if (data.level_completed) {
        pass_nivel(data.level_completed);
        // Esperar un poco antes de mostrar el siguiente reto
        setTimeout(() => {
          document.getElementById("respuesta").value = "";
          document.getElementById("salida").textContent = "";
          document.getElementById("pista").textContent = data.hint ? `${data.hint}` : "";
          document.getElementById("nivel").innerText = data.next_level ? `Nivel ${data.next_level}` : "";
          document.getElementById("reto").innerText = data.challenge ? data.challenge : "";
        }, 2300); // Espera a que desaparezca el overlay
        return;
      }

      showLevelTransition();
      setTimeout(() => {
        document.getElementById("respuesta").value = "";
        document.getElementById("salida").textContent = "";
        document.getElementById("pista").textContent = data.hint ? `💡 ${data.hint}` : "";
        document.getElementById("nivel").innerText = data.next_level ? `Nivel ${data.next_level}` : "";
        document.getElementById("reto").innerText = data.challenge ? data.challenge : "";
        hideLevelTransition();
      }, 3000);
    }
    
    // Si no es correcto, solo se actualiza el mensaje, no el reto/pista/nivel
    // Animación simple de parpadeo rojo en consola
    terminal.classList.add("error-blink");
    setTimeout(() => terminal.classList.remove("error-blink"), 400);
  })
  .catch(() => {
    document.getElementById("salida").innerHTML = `<i class="fa-solid fa-circle-xmark"></i> Error al enviar la respuesta.`;
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

let spinnerInterval;
const spinnerFrames = [
  "[|] Hackeando acceso...",
  "[/] Hackeando acceso...",
  "[-] Hackeando acceso...",
  "[\\] Hackeando acceso..."
];

function showLevelTransition(message = "Hackeando acceso...") {
  const overlay = document.getElementById("level-transition");
  const anim = document.getElementById("loading-animation");
  overlay.style.display = "flex";
  overlay.classList.remove("hide");
  let frame = 0;
  spinnerInterval = setInterval(() => {
    anim.textContent = spinnerFrames[frame % spinnerFrames.length];
    frame++;
  }, 120);
}

function hideLevelTransition() {
  clearInterval(spinnerInterval);
  const overlay = document.getElementById("level-transition");
  overlay.classList.add("hide");
  setTimeout(() => overlay.style.display = "none", 500);
}

//Paso de nivel
function pass_nivel(nivel) {
  const overlay = document.createElement("div");
  overlay.className = "terminal";
  overlay.style = "position:fixed;top:0;left:0;width:100vw;height:100vh;background:rgba(0,255,0,0.1);color:lime;font-size:2.5em;z-index:9999;display:flex;align-items:center;justify-content:center;flex-direction:column;";
  overlay.innerHTML = `
    <h1><i class="fa-solid fa-champagne-glasses"></i></h1>
    <p>¡Felicidades, Agente !</p>
    <h1> ¡Nivel ${nivel} completado!</h1>
    <p>Prepárate para el siguiente desafío...</p>
  `;
  document.body.appendChild(overlay);
  setTimeout(() => overlay.remove(), 2000); // Desaparece tras 2s
}

function showGameOver(msg) {
  // Oculta la consola del juego
  document.getElementById("consola").style.display = "none";
  // Crea overlay de Game Over
  const overlay = document.createElement("div");
  overlay.className = "terminal";
  overlay.style = `
    position:fixed;top:0;left:0;width:100vw;height:100vh;
    background:rgba(0,0,0,0.95);color:red;font-size:2.5em;z-index:9999;
    display:flex;align-items:center;justify-content:center;flex-direction:column;
  `;
  overlay.innerHTML = `
    <h1><i class="fa-solid fa-skull"></i> GAME OVER</h1>
    <p style="color:white;font-size:1.2em;white-space:pre-line;">${msg}</p>
    <button style="font-size:1em;padding:0.5em 2em;border-radius:0.5em;margin-top:1em" onclick="location.reload()">Reintentar</button>
  `;
  document.body.appendChild(overlay);
}

function showVictory(msg) {
  document.getElementById("consola").style.display = "none";
  const overlay = document.createElement("div");
  overlay.className = "terminal";
  overlay.style = `
    position:fixed;top:0;left:0;width:100vw;height:100vh;
    background:rgba(0,0,0,0.95);color:lime;font-size:2.5em;z-index:9999;
    display:flex;align-items:center;justify-content:center;flex-direction:column;
  `;
  overlay.innerHTML = `
    <h1><i class="fa-solid fa-trophy"></i> ¡MISIÓN COMPLETADA!</h1>
    <p style="color:white;font-size:1.2em;white-space:pre-line;">${msg}</p>
    <button style="font-size:1em;padding:0.5em 2em;border-radius:0.5em;margin-top:1em" onclick="window.location.href='/metrics'">Ver métricas</button>
    <button style="font-size:1em;padding:0.5em 2em;border-radius:0.5em;margin-top:1em" onclick="location.reload()">Jugar de nuevo</button>
  `;
  document.body.appendChild(overlay);
}