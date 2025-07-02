from flask import Blueprint, render_template

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
