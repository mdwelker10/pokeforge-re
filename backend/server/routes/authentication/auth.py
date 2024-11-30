import os
from urllib.parse import quote

from authlib.integrations.flask_client import OAuth
from flask import (Blueprint, current_app, jsonify, make_response, redirect,
                   request, session, url_for)
from server.data.dao.user_dao import create_user, google_login, validate_user
from server.routes.authentication.jwt import create_jwt
from server.utils.utils import handle_api_errors, login_required

# Blueprint for authentication routes
auth_bp = Blueprint('auth_bp', __name__)

# Set up OAuth object for Google authentication
oauth = OAuth()
google = oauth.register(
  name="google",
  client_kwargs={"scope": "openid email profile"}
)
HOMEPAGE = 'http://localhost:3000/about' # TODO replace with homepage

def init_oauth(app):
  """Initializes OAuth object for Google authentication"""
  oauth.init_app(app)
  google.client_id = app.config['GOOGLE_CLIENT_ID']
  google.client_secret = app.config['GOOGLE_SECRET']
  google._server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"

@handle_api_errors
@auth_bp.route('/register', methods=['POST'])
def register():
  """Route for registering a new user with custom authentication. Registering with Google uses /login?method=google"""
  # TODO add confirm password field. Keeping at no confirm for testing
  data = request.get_json()
  if not data or 'username' not in data or 'password' not in data:
    return jsonify({'error': 'Invalid registration attempt'}), 400
  
  create_user(data['username'], data['password'])
  return redirect('http://localhost:3000') # TODO replace with login page

@handle_api_errors
@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
  """Route for logging in. Use ?next=/path to redirect after login, if not set goes to homepage by default. 
     Use ?method=google to login with Google.
     Note that logging in with Google will hit this endpoint even if the user has not logged in before (i.e. new account)"""
  # Set destination after login
  next = request.args.get('next', HOMEPAGE)

  # Google login
  if request.args.get('method') == 'google':
    if request.method != 'GET':
      return jsonify({'error': 'Invalid login attempt'}), 405
    # TODO Make login with google redirect properly
    # redirect_uri = url_for('.callback', _external=True, next=quote(next))
    redirect_uri = url_for('.callback', _external=True)
    # Generate nonce for one time validation
    nonce = os.urandom(16).hex()
    session["nonce"] = nonce  # Store nonce in session
    return google.authorize_redirect(redirect_uri, nonce=nonce)
  
  if request.method != 'POST':
    return jsonify({'error': 'Invalid login attempt'}), 405
  # Custom login - validate user
  data = request.get_json()
  if not data or 'username' not in data or 'password' not in data:
    return jsonify({'error': 'Invalid login attempt'}), 400
  user_dto = validate_user(data['username'], data['password'])
  if not user_dto:
    return jsonify({'error': 'Invalid login attempt'}), 401
  
  session['username'] = user_dto['username']
  # Handle setting cookie and redirecting 
  response = redirect(next)
  response.set_cookie(current_app.config['JWT_COOKIE_NAME'], quote(create_jwt(data['username'])), httponly=True, secure=True)
  return response

@handle_api_errors
@auth_bp.route('/callback')
def callback():
  """Callback route for Google OAuth to use when the user has been authenticated"""
  next = request.args.get('next', HOMEPAGE)
  token = google.authorize_access_token()
  nonce = session.pop("nonce", None) # retrieve nonce
  if not nonce:
    return jsonify({'error': 'Invalid login attempt'}), 401
  
  # Get user information from Google
  user_info = google.parse_id_token(token, nonce=nonce) # fields include name, given_name, family_name, picture, email, and sub (the ID)

  # Create or retrieve user from database
  user_dto = google_login(user_info['email'], user_info['sub'])
  # Store username in session for easy access
  session['username'] = user_dto['username']
  # Generate response for redirect and set JWT / cookie
  response = redirect(next)
  response.set_cookie(current_app.config['JWT_COOKIE_NAME'], quote(create_jwt(user_dto['username'])), httponly=True, secure=True)
  return response

@handle_api_errors
@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
  """Route for logging out. Clears session and JWT cookie. Takes user back to the home page even if on a non-protected page."""
  current_app.logger.info('User %s logged out', request.user)
  response = redirect(HOMEPAGE)
  response.delete_cookie(current_app.config['JWT_COOKIE_NAME'])
  session.clear()
  return response