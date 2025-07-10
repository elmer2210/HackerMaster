import json
import random

# Ruta al archivo JSON con los retos
CHALLENGES_PATH = "data/challenges.json"

# Constantes
TOTAL_LEVELS = 3           # Niveles: 1 = fácil, 2 = medio, 3 = difícil
CHALLENGES_PER_LEVEL = 2   # Se deben resolver 2 retos por nivel

# Cargar todos los retos desde el archivo
with open(CHALLENGES_PATH, "r", encoding="utf-8") as file:
    ALL_CHALLENGES = json.load(file)


# Devuelve todos los retos disponibles para un nivel específico
def get_challenges_by_level(level: int):
    return [c for c in ALL_CHALLENGES if c["level"] == level]


# Devuelve un reto aleatorio que el jugador no haya resuelto aún en el nivel actual
def get_next_challenge_for_player(player):
    current_level = player.current_level
    resolved_ids = getattr(player, "solved_challenges", [])

    disponibles = [
        c for c in get_challenges_by_level(current_level)
        if c["id"] not in resolved_ids
    ]

    if not disponibles:
        return None  # Ya resolvió todos los retos del nivel

    return random.choice(disponibles)


# Devuelve la salida esperada de un reto (como texto limpio)
def get_expected_output(challenge: dict) -> str:
    return challenge.get("expected_output", "").strip()

# Busca un reto por su ID único
def get_challenge_by_id(challenge_id: int) -> dict:
    for challenge in ALL_CHALLENGES:
        if challenge["id"] == challenge_id:
            return challenge
    raise ValueError(f"❌ No se encontró el reto con ID {challenge_id}")
