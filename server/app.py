from config.config import Config
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins='*', methods=["GET", "POST", "PUT", "DELETE"]) # TODO change origins for production

app.config.from_object(Config)

app.secret_key = app.config['SECRET_KEY'] # For session management

# Import and register blueprints
from routes.auth import auth_bp, init_oauth
from routes.test import test_bp

init_oauth(app) # Initialize OAuth object for Google authentication
app.register_blueprint(auth_bp)
app.register_blueprint(test_bp, url_prefix='/test')


if __name__ == '__main__':
    app.run(debug=True, port=8000)

