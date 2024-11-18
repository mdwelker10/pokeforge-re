import os
from functools import wraps

from authlib.integrations.flask_client import OAuth
from flask import Blueprint, jsonify, redirect, session, url_for

# Blueprint for authentication routes
auth_bp = Blueprint('auth_bp', __name__)

oauth = OAuth()
google = oauth.register(
  name="google",
  client_kwargs={"scope": "openid email profile"}
)

def init_oauth(app):
  """Initializes OAuth object for Google authentication"""
  oauth.init_app(app)
  google.client_id = app.config['GOOGLE_CLIENT_ID']
  google.client_secret = app.config['GOOGLE_SECRET']
  google.server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"

@auth_bp.route('/login')
def login(): #TODO: Add logic for differentiating between custom login and google login
  redirect_uri = url_for('callback', _external=True)
  # Generate nonce for one time validation
  nonce = os.urandom(16).hex()
  session["nonce"] = nonce  # Store nonce in session
  return google.authorize_redirect(redirect_uri, nonce=nonce)


@auth_bp.route('/callback')
def callback():
  """Callback route for Google OAuth to use when the user has been authenticated"""
  token = google.authorize_access_token()
  nonce = session.pop("nonce", None) # retrieve nonce
  if not nonce:
    return jsonify({'error': 'Invalid login attempt'}), 401
  
  # Get user information from Google
  user_info = google.parse_id_token(token, nonce=nonce)
  
  # other fields include name, given_name, family_name, picture, email, and ID
  # given is first name, family is last name
  session['google'] = user_info.email # TODO: generate jwt for session management
  return redirect('http://localhost:3000')


# Method used to validate login
def login_required(f):
  """Decorator used to check if user is logged in, place on all protected routes"""
  @wraps(f)
  def wrapper(*args, **kwargs):
    # TODO Check if NOT logged in using a more secure method, also implement tracking for custom login
    # Right now only checks if google is in the session - vulnerable to attack
    if "google" not in session:  
      return jsonify({'message': 'You are not logged in'}), 401
    else:
      return f(*args, **kwargs)
  return wrapper

