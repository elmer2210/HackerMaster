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
