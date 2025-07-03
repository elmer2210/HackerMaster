from flask import Blueprint, render_template
from app.storage import save_players_to_json
from app.players import get_player, update_player
from app.levels import TOTAL_LEVELS  # o define tú el número total (ej: 6)


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

    # Aquí llamas a tu lógica para obtener el reto correcto
    correct_output = get_expected_output(level)
    is_correct = validate_answer(user_answer, correct_output)

    # Actualizar jugador
    update_player(player, is_correct, points=10 if is_correct else 5)

    # Verificar si terminó todos los niveles
    if player.current_level > TOTAL_LEVELS:
        save_players_to_json()  # ← ¡GUARDAMOS LOS DATOS!

        return jsonify({
            "finished": True,
            "message": "🎉 ¡Has completado todos los retos! Tus datos han sido guardados.",
            "is_correct": is_correct
        })

    # Si no terminó, seguir jugando
    return jsonify({
        "finished": False,
        "is_correct": is_correct,
        "next_level": player.current_level
    })



# ============================================
# Archivo: app.py
# Propósito: Definir las rutas principales del sistema.
# Este archivo contiene:
#   - Rutas para las vistas HTML (index, play, metrics, etc.)
#   - Ruta '/evaluar' que recibe los datos del jugador y su respuesta
#   - Llama a:
#       - players.py para gestionar al jugador
#       - validator.py para validar la respuesta
#       - storage.py para actualizar los datos en el archivo JSON
# Este módulo funciona como el "cerebro" que orquesta los demás módulos.
# ============================================
