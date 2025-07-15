# app/app.py

from flask import Blueprint, render_template, request, jsonify
from .storage import save_players_to_json
from .players import get_player, update_player, reset_player, create_player, get_all_players
from .levels import get_next_challenge_for_player, get_challenge_by_id, get_expected_output, TOTAL_LEVELS
from .validator import validate_answer
from .metrics import load_players, format_metrics_output
import ast 

main_bp = Blueprint('main', __name__)
metrics_bp = Blueprint('metrics_bp', __name__)

@main_bp.route('/')
def menu():
    return render_template('index.html')

@main_bp.route('/play')
def play():
    return render_template('play.html')

@main_bp.route('/metrics')
def metrics():
    return render_template('metrics.html')

@main_bp.route('/instructions')
def instructions():
    return render_template('instructions.html')

@main_bp.route('/credits')
def credits():
    return render_template('credits.html')

@main_bp.route('/game_over')
def game_over():
    return render_template('game_over.html')

@main_bp.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()
    name = data.get("name")
    user_answer = data.get("answer")

    player = get_player(name)

    if not player or not player.current_challenge:
        return jsonify({"error": "Jugador no válido o sin reto asignado"}), 400

    # Obtener el reto actual del jugador por ID
    challenge = player.current_challenge
    

    # Validar la respuesta del jugador
    expected_output = get_expected_output(challenge)
    challenge_type = challenge.get("type")
    result = validate_answer(user_answer, expected_output, challenge_type)

    # Actualizar jugador
    player_response=update_player(player, is_correct=result["success"], points=10, challenge_id=challenge["id"])
    print(player_response)
    response = {
        "is_correct": result["success"],
        "output": result["output"],
        "attempts": player.attempts,
        "correct_attempts":player.correct_attempts,
        "failed_attempts": player.incorrect_attempts,
    }

    # Si fue correcto, pasar al siguiente reto
    if result["success"]:
    # === RESPUESTA CORRECTA ===
        next_challenge = get_next_challenge_for_player(player)
        if player_response["level_up"]:
            # Ha resuelto todos los retos de este nivel, sube de nivel o termina juego
            if player.current_level > TOTAL_LEVELS:
                # Juego completado
                save_players_to_json()
                player.current_challenge = None
                response.update({
                    "finished": True,
                    "message": f"¡Misión completada con éxito! Resolviste {len(player.solved_challenges)} retos.",
                })
                return jsonify(response)
            else:
                # Nuevo nivel desbloqueado, asignar primer reto del siguiente nivel
                player.current_challenge = next_challenge
                response.update({
                    "finished": False,
                    "level_completed": True,
                    "next_level": player.current_level,
                    "challenge": next_challenge["challenge"],
                    "hint": next_challenge["hint"],
                    "message": f"¡Nivel {player.current_level} desbloqueado!"
                })
                return jsonify(response)
        else:
            # Aún quedan retos en este nivel, avanza al siguiente reto
            player.current_challenge = next_challenge
            response.update({
                "finished": False,
                "next_level": player.current_level,
                "challenge": next_challenge["challenge"],
                "hint": next_challenge["hint"],
                "message": challenge["success_message"],  # mensaje del reto resuelto
                "attempts": player.attempts,
                "retos_resueltos": len(player.solved_challenges),
            })
    else:
        # === RESPUESTA INCORRECTA ===
        if player.attempts <= 0:
            save_players_to_json()
            reset_player(player)  # Reiniciar jugador si se acabaron los intentos
            response.update({
                "game_over": True,
                "message": "GAME OVER"
            })
        else:
            response["message"] = challenge["error_message"]

    return jsonify(response)

    return jsonify(response)


@main_bp.route('/get_challenge', methods=['POST'])
def get_challenge():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"error": "Nombre no proporcionado"}), 400

    player = get_player(name)
    if not player:
        player = create_player(name)

    challenge = get_next_challenge_for_player(player)

    player.current_challenge = challenge

    if not challenge:
        return jsonify({
            "error": "No hay más retos disponibles en este nivel.",
            "level": player.current_level
        }), 404

    return jsonify({
        "level": player.current_level,
        "attempts": player.attempts,
        "challenge": challenge["challenge"] if challenge else "",
        "correct_attempts": player.correct_attempts,
        "failed_attempts": player.incorrect_attempts,
        "hint": challenge["hint"]
    })



@main_bp.route('/reset', methods=['POST'])
def reset():
    data = request.get_json()
    name = data.get("name")

    player = get_player(name)
    if player:
        reset_player(player)
        # Consigue un reto inicial directamente (no usando get_challenge view!)
        challenge = get_next_challenge_for_player(player)
        player.current_challenge = challenge  # asegúrate que esto se asigne
        return jsonify({
            "success": True,
            "message": f" El jugador {name} ha sido reiniciado.",
            "challenge": challenge["challenge"] if challenge else "",
            "hint": challenge["hint"] if challenge else "",
            "level": 1
        })
    else:
        return jsonify({
            "success": False,
            "message": "❌ Jugador no encontrado."
        }), 404

#Carga de métricas
@main_bp.route('/api/metrics')
def api_metrics():
    from .metrics import load_players, format_metrics_output
    jugadores = load_players()
    metrics = format_metrics_output(jugadores)
    return jsonify(metrics)