from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict
from .levels import get_next_challenge_for_player, get_challenge_by_id

# Lista en memoria que mantiene todos los jugadores activos
players_list: List['Player'] = []
CHALLENGES_PER_LEVEL = 2

# Estructura de datos que representa a un jugador
@dataclass
class Player:
    name: str                            # Nombre del jugador
    current_level: int = 1               # Nivel actual del juego
    score_per_level: List[int] = field(default_factory=list)   # Puntajes por nivel
    attempts: int = 3                    # Número de intentos realizados
    correct_attempts: int = 0           # Número de intentos correctos
    incorrect_attempts: int = 0         # Número de intentos incorrectos
    solved_challenges: List[int] = field(default_factory=list) # ← Lista de retos resueltos por el jugador
    current_challenge: Optional[Dict] = None

    def __post_init__(self):
        if self.score_per_level is None:
            self.score_per_level = []
        if self.solved_challenges is None:
            self.solved_challenges = []

# Crea un nuevo jugador y lo añade a la lista en memoria
def create_player(name: str) -> Player:
    name = name.strip()

    new_player = Player(name=name)

    # Obtener primer reto automáticamente
    first_challenge = get_next_challenge_for_player(new_player)
    new_player.current_challenge = first_challenge
    new_player.current_level = 1
    new_player.solved_challenges = []

    players_list.append(new_player)
    return new_player

# Busca un jugador por nombre (case-insensitive)
def get_player(name: str) -> Optional[Player]:
    name = name.strip().lower()
    for player in players_list:
        if player.name.lower()== name and player.attempts > 0:
            return player
    return None

def update_player(player: Player, is_correct: bool, challenge_id: int, points: int = 10) -> dict:
    """
    Actualiza el estado del jugador según el resultado del reto.
    Retorna un diccionario indicando si subió de nivel y el nivel actual.
    """
    level_up = False
    prev_level = player.current_level

    if is_correct:
        player.correct_attempts += 1

        if challenge_id not in player.solved_challenges:
            player.solved_challenges.append(challenge_id)
            player.score_per_level.append(points)

        # Verificar si resolvió 2 retos del nivel actual
        retos_resueltos_en_nivel = [
            cid for cid in player.solved_challenges
            if get_challenge_by_id(cid)["level"] == player.current_level
        ]

        if len(retos_resueltos_en_nivel) >= CHALLENGES_PER_LEVEL:
            player.current_level += 1
            player.current_challenge = None  # Se asignará nuevo en el siguiente reto
            level_up = True

    else:
        player.attempts -= 1
        player.incorrect_attempts += 1
        player.score_per_level.append(-abs(points))

    return {
        "level_up": level_up,
        "prev_level": prev_level,
        "current_level": player.current_level,
        "attempts": player.attempts,
        "retos_resueltos": len(player.solved_challenges)
    }

# Devuelve todos los jugadores activos
def get_all_players() -> List[Player]:
    return players_list

# Serializa jugadores para guardar en JSON
def serialize_players() -> List[dict]:
    return [asdict(player) for player in players_list]

# Carga jugadores desde JSON
def load_players_from_data(data: List[dict]):
    players_list.clear()
    for d in data:
        player = Player(**d)
        players_list.append(player)

def reset_player(player):
    """Reinicia los datos del jugador sin cambiar su nombre."""
    player.current_level = 1
    player.attempts = 3
    player.correct_attempts = 0
    player.incorrect_attempts = 0
    player.score_per_level = []