document.addEventListener("DOMContentLoaded", () => {
      fetch('/api/metrics')
        .then(res => res.json())
        .then(data => renderMetrics(data));
        console.log("Metrics script loaded");
});

function renderMetrics(data) {
    let html = `
    <p><b>Promedio de puntaje:</b> <span style="color:lime">${data.average_score}</span></p>
    <p><b>Total de jugadores:</b> <span style="color:cyan">${data.total_players}</span></p>
    <h2 style="color:yellow">🏆 Top 3 jugadores</h2>
    <ol>
        ${data.top_players.map(p =>
        `<li><b>${p.name}</b> | Puntaje: <span style="color:lime">${p.score}</span> | Efectividad: <span style="color:orange">${p.accuracy}%</span></li>`
        ).join('')}
    </ol>
    <h2 style="color:aqua"><i class="fa-solid fa-arrow-trend-up"></i> Estadísticas por nivel</h2>
    <table border="1" cellpadding="4" style="background:black;color:lime">
        <tr><th>Nivel</th><th>Puntaje promedio</th><th>Intentos</th></tr>
        ${data.level_stats.map(l =>
        `<tr>
            <td>${l.level}</td>
            <td>${l.average_score}</td>
            <td>${l.attempts}</td>
        </tr>`
        ).join('')}
    </table>
    `;
    document.getElementById("metrics-content").innerHTML = html;
}

/*function metrics(){
    fetch('/api/metrics')
        .then(res => res.json())
            .then(data => {
                const area = document.getElementById("metrics-output");
                let output = "";

                data.players.forEach((player, i) => {
                output += `#${i + 1} ${player.name}\n`;
                output += `  Levels passed: ${player.levels_passed}\n`;
                output += `  Total points: ${player.total_score}\n`;
                output += `  Accuracy: ${player.accuracy}%\n`;
                output += `\n`;
                });

                area.textContent = output;
            })
        .catch(() => {
            document.getElementById("metrics-output").textContent = "❌ Failed to load metrics.";
        });
}*/