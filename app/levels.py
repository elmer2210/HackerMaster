import json
import random
import ast

# Ruta al archivo JSON con los retos
CHALLENGES_PATH = "data/challenges.json"

# Constantes
TOTAL_LEVELS = 3
CHALLENGES_PER_LEVEL = 2

# Abrir el archivo de retos y cargar los datos
try:
    with open(CHALLENGES_PATH, "r", encoding="utf-8") as file:
        ALL_CHALLENGES = json.load(file)
except FileNotFoundError:
    raise FileNotFoundError(f" No se encontró el archivo de retos en {CHALLENGES_PATH}")

#Funicón que carga los retos por nivel
def get_challenges_by_level(level: int):
    return [c for c in ALL_CHALLENGES if c["level"] == level]

#Pasar al reto siguiente para el jugador
def get_next_challenge_for_player(player):
    current_level = player.current_level
    resolved_ids = getattr(player, "solved_challenges", [])
    disponibles = [c for c in get_challenges_by_level(current_level) if c["id"] not in resolved_ids]
    if not disponibles:
        return None
    return random.choice(disponibles)

#Obtener la salida esperada del reto
def get_expected_output(challenge: dict):
    value = challenge.get("expected_output", "")
    ctype = challenge.get("type", "")
    if ctype in ["list", "palindrome"]:  # Solo evalúa estructuras de datos
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return value.strip()
    else:
        # Para string, number, etc., devuélvelo como texto
        return value.strip()

#obtener un reto por ID
def get_challenge_by_id(challenge_id: int):
    for challenge in ALL_CHALLENGES:
        if challenge["id"] == challenge_id:
            return challenge
    raise ValueError(f" No se encontró el reto con ID {challenge_id}")
