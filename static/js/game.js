let playerName = "";
let nivelActual = 1;
let matrixOverlayAnimation;

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
      document.getElementById("correct_attempts").innerHTML = `<i class="fa-solid fa-web-awesome"></i> ${data.correct_attempts}`;
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
    document.getElementById("correct_attempts").innerHTML = `<i class="fa-solid fa-web-awesome"></i> ${data.correct_attempts}`;
    document.getElementById("failed_attempts").innerHTML = `<i class="fa-solid fa-skull"></i> ${data.failed_attempts}`;

    if (data.finished) {
      showVictory(data.message);
      return;
    }
    if (data.game_over) {
      showGameOver();
      return; // Ya terminó, no sigas mostrando el juego
    }

    if (data.is_correct) {
      
      console.log("Respuesta correcta:", data);
      // Detectar si subió de nivel
      if (data.level_completed) {
        console.log("Nivel completado:", data.level_completed);
        pass_nivel(nivelActual);
        nivelActual = data.next_level; // Actualizar nivel actual

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
      // Si no subió de nivel, solo actualizar reto/pista/nivel
      console.log("Respuesta correcta, cargando siguiente reto..."); 
      showLevelTransition();
      console.log("Respuesta correcta, cargando siguiente reto...");
      setTimeout(() => {
        console.log("Cargando siguiente reto...");
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
  document.getElementById("reto").textContent = "";
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
   // Elimina si ya hay uno viejo (por si acaso)
  let oldOverlay = document.getElementById('overlay-nivel');
  if (oldOverlay) oldOverlay.remove();

  // Crea un nuevo overlay de nivel
  const overlay = document.createElement("div");
  overlay.id = "overlay-nivel";
  overlay.className = "overlay-nivel";

  // Matrix canvas
  overlay.innerHTML = `
    <canvas id="matrix-nivel"></canvas>
    <div >
       <h1><i class="fa-solid fa-champagne-glasses"></i></h1>
      <p>¡Felicidades, Agente !</p>
      <h1> ¡Nivel ${nivel} completado!</h1>
      <h2>Bievenido al siguiente nivel</h2>
      <p>Prepárate para el siguiente desafío...</p>
    </div>
  `;
  
  document.body.appendChild(overlay);

  // Iniciar matrix solo en ese canvas
  startMatrixOverlay("matrix-nivel", "#00FF41");

  setTimeout(() => {
    // Remover overlay y detener animación
    overlay.remove();
    stopMatrixOverlay();
  }, 3000);
}

function showGameOver() {
   // Elimina si ya hay uno viejo (por si acaso)
  let oldOverlay = document.getElementById('overlay-gameover');
  if (oldOverlay) oldOverlay.remove();

  // Crea un nuevo overlay de nivel
  const overlay = document.createElement("div");
  overlay.id = "overlay-gameover";


  overlay.innerHTML = `
    <canvas id="matrix-gameover"></canvas>
    <div id="gameover-mensaje"
      <h1><i class="fa-solid fa-skull"></i> GAME OVER</h1>
      <p>"No has podido desincriptar la computadora"</p>
    </div>
  `;
  document.body.appendChild(overlay);

  // Iniciar matrix solo en ese canvas
  startMatrixOverlay("matrix-gameover", "#e53935");

  setTimeout(() => {
    // Remover overlay y detener animación
    overlay.remove();
    stopMatrixOverlay();
  }, 3000);
  // Llama animación de matrix rojo
  
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

function startMatrixOverlay(canvasId, color = "#0f0") {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  // Tamaño pantalla completa del overlay
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const ctx = canvas.getContext("2d");
  const letters = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*アカサタナハマヤラワ".split("");
  const fontSize = 18;
  const columns = Math.floor(canvas.width / fontSize);

  let drops = Array.from({ length: columns }, () => Math.random() * canvas.height / fontSize);

  function draw() {
    ctx.fillStyle = "rgba(0, 0, 0, 0.25)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.font = fontSize + "px monospace";
    ctx.fillStyle = color;

    for (let i = 0; i < drops.length; i++) {
      const text = letters[Math.floor(Math.random() * letters.length)];
      ctx.fillText(text, i * fontSize, drops[i] * fontSize);

      if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
        drops[i] = 0;
      }
      drops[i]++;
    }
    matrixOverlayAnimation = requestAnimationFrame(draw);
  }
  // Limpia animaciones previas
  if (canvas.matrixInterval) clearInterval(canvas.matrixInterval);
  canvas.matrixInterval = setInterval(draw, 33);
}

function stopMatrixOverlay() {
  cancelAnimationFrame(matrixOverlayAnimation);
}