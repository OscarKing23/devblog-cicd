from flask import Flask
from config import Config


def create_app():
    # Crear la instancia de Flask
    app = Flask(__name__, static_folder="../static", static_url_path="/static")

    # Cargar configuracion desde config.py
    app.config.from_object(Config)

    # Registrar las rutas
    from app.routes import main
    app.register_blueprint(main)

    return app
