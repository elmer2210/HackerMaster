# ============================================
# Archivo: metrics.py
# Propósito: Analizar el rendimiento de los jugadores.
# Contiene funciones de análisis y formateo para la vista de métricas.
# ============================================

import json
import os

# Ruta al archivo de jugadores (ajusta si es necesario)
PLAYERS_PATH = os.path.join("data", "players.json")

def load_players():
    """Carga y devuelve la lista de jugadores desde el archivo JSON."""
    with open(PLAYERS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# --- Aquí tus funciones de métricas ---

def calculate_average_score(jugadores):
    if not jugadores:
        return 0.0
    total_score = sum(sum(j["score_per_level"]) for j in jugadores)
    return round(total_score / len(jugadores), 2)

def calculate_accuracy(jugador):
    if jugador["attempts"] == 0:
        return 0.0
    return round((jugador["correct_attempts"] / jugador["attempts"]) * 100, 2)

def get_top_players(jugadores, top=3):
    return sorted(
        jugadores,
        key=lambda j: sum(j["score_per_level"]),
        reverse=True
    )[:top]

def generate_level_stats(jugadores, total_levels=3):
    stats = []
    for level in range(1, total_levels+1):
        level_scores = []
        for j in jugadores:
            # Supón que score_per_level está alineado con niveles
            if len(j["score_per_level"]) >= level:
                level_scores.append(j["score_per_level"][level-1])
        promedio = round(sum(level_scores)/len(level_scores), 2) if level_scores else 0
        stats.append({
            "level": level,
            "average_score": promedio,
            "attempts": len(level_scores)
        })
    return stats

def format_metrics_output(jugadores):
    return {
        "average_score": calculate_average_score(jugadores),
        "top_players": [
            {
                "name": p["name"],
                "score": sum(p["score_per_level"]),
                "accuracy": calculate_accuracy(p)
            }
            for p in get_top_players(jugadores)
        ],
        "level_stats": generate_level_stats(jugadores),
        "total_players": len(jugadores)
    }
