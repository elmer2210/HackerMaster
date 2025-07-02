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
