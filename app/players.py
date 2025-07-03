from dataclasses import dataclass, asdict
from typing import List, Optional

# Lista en memoria que mantiene todos los jugadores activos
players_list: List['Player'] = []

# Estructura de datos que representa a un jugador
@dataclass
class Player:
    name: str                            # Nombre del jugador
    current_level: int = 1               # Nivel actual del juego
    score_per_level: List[int] = None   # Puntajes por nivel
    attempts: int = 0                    # Número de intentos realizados
    correct_attempts: int = 0           # Número de intentos correctos
    incorrect_attempts: int = 0         # Número de intentos incorrectos

    def __post_init__(self):
        if self.score_per_level is None:
            self.score_per_level = []

# Crea un nuevo jugador y lo añade a la lista en memoria
def create_player(name: str) -> Player:
    name = name.strip()
    new_player = Player(name=name)
    players_list.append(new_player)
    return new_player

# Busca un jugador por nombre (case-insensitive)
def get_player(name: str) -> Optional[Player]:
    name = name.strip().lower()
    for player in players_list:
        if player.name.lower() == name:
            return player
    return None

# Actualiza los datos del jugador tras un intento
def update_player(player: Player, is_correct: bool, points: int):
    player.attempts += 1

    if is_correct:
        player.correct_attempts += 1
        player.score_per_level.append(points)
        player.current_level += 1
    else:
        player.incorrect_attempts += 1
        player.score_per_level.append(-abs(points))

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
