from config.config import Config
from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app, origins=['http://localhost:3000'], methods=["GET", "POST", "PUT", "DELETE"], supports_credentials=True)

    app.config.from_object(Config)

    app.secret_key = app.config['FLASK_SECRET'] # For session management

    # Import and register blueprints
    from server.routes.authentication.auth import auth_bp, init_oauth
    from server.routes.test import test_bp

    init_oauth(app) # Initialize OAuth object for Google authentication
    app.register_blueprint(auth_bp)
    app.register_blueprint(test_bp, url_prefix='/test')

    return app