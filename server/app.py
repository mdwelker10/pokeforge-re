import os

from authlib.integrations.flask_client import OAuth
from config.config import Config
from flask import Flask, jsonify, redirect, session, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins='*', methods=["GET", "POST", "PUT", "DELETE"]) # change origins for production

app.config.from_object(Config)

app.secret_key = app.config['SECRET_KEY'] # For session management

# from routes.auth import auth_bp
from routes.test import test_bp

# app.register_blueprint(auth_bp)
app.register_blueprint(test_bp, url_prefix='/test')

# Authentication
oauth = OAuth(app)
google = oauth.register(
  name="google",
  client_id=app.config['GOOGLE_CLIENT_ID'],
  client_secret=app.config['GOOGLE_SECRET'],
  server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
  client_kwargs={"scope": "openid email profile"},
)

@app.route('/login')
def login():
  redirect_uri = url_for('callback', _external=True)
  # Generate nonce for one time validation
  nonce = os.urandom(16).hex()
  session["nonce"] = nonce  # Store nonce in session
  return google.authorize_redirect(redirect_uri, nonce=nonce)

@app.route('/callback')
def callback():
  token = google.authorize_access_token()
  nonce = session.pop("nonce", None) # retrieve nonce
  if not nonce:
    return jsonify({'error': 'Invalid login attempt'}), 401
  
  # Get user information from Google
  user_info = google.parse_id_token(token, nonce=nonce)
  
  # other fields include name, given_name, family_name, picture, email 
  # given is first name, family is last name
  session['google'] = user_info.email # TODO: generate a token of sorts for session management
  return redirect('http://localhost:3000')

