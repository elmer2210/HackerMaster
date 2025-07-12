function metrics(){
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
}