from flask import Flask
import os

def create_app():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, 'templates'),
        static_folder=os.path.join(BASE_DIR, 'static')
    )

    from .app import main_bp
    app.register_blueprint(main_bp)

    return app

# ============================================
# Archivo: __init__.py
# Propósito: Crear y configurar la aplicación Flask.
# Este archivo expone una función `create_app()` que:
#   - Instancia la aplicación Flask
#   - Configura la carpeta de templates y archivos estáticos
#   - Registra los blueprints (rutas) definidos en otros módulos
# Este archivo es llamado desde run.py para lanzar el servidor.
# ============================================
