# app/app.py

from flask import Blueprint, render_template, request, jsonify
from app.storage import save_players_to_json
from app.players import get_player, update_player, reset_player
from app.levels import TOTAL_LEVELS, get_expected_output, get_hint, get_challenge
from app.validator import validate_answer

main_bp = Blueprint('main', __name__)

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

@main_bp.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json()
    name = data.get("name")
    user_answer = data.get("answer")

    player = get_player(name)
    level = player.current_level

    correct_output = get_expected_output(level)
    is_correct = validate_answer(user_answer, correct_output)

    update_player(player, is_correct, points=10 if is_correct else 5)

    if player.current_level > TOTAL_LEVELS:
        save_players_to_json()
        return jsonify({
            "finished": True,
            "redirect_url": "/game_over"
        })
    # Si no terminó, enviar siguiente reto y pista
    return jsonify({
        "finished": False,
        "is_correct": is_correct,
        "next_level": player.current_level,
        "challenge": get_challenge(player.current_level),
        "hint": get_hint(player.current_level)
    })


@main_bp.route('/get_challenge', methods=['POST'])
def get_challenge_data():
    data = request.get_json()
    name = data.get("name")

    player = get_player(name)
    level = player.current_level

    return jsonify({
        "level": level,
        "challenge": get_challenge(level),
        "hint": get_hint(level)
    })

@main_bp.route('/reset', methods=['POST'])
def reset():
    data = request.get_json()
    name = data.get("name")

    player = get_player(name)
    if player:
        reset_player(player)
        return jsonify({
            "success": True,
            "message": f"🔁 El jugador {name} ha sido reiniciado.",
            "challenge": get_challenge(1),
            "hint": get_hint(1),
            "level": 1
        })
    else:
        return jsonify({
            "success": False,
            "message": "❌ Jugador no encontrado."
        }), 404

@main_bp.route('/game_over')
def game_over():
    return render_template('game_over.html')
