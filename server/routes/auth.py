import os
import pathlib
from functools import wraps

from flask import Blueprint, jsonify, session
from google_auth_oauthlib.flow import Flow

auth_bp = Blueprint('auth_bp', __name__)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # Remove this line in production - allows for testing on http
client_secrets_file = os.path.abspath(os.path.join(pathlib.Path(__file__).parent, '../', 'google_secret.json'))

flow = Flow.from_client_secrets_file(
  client_secrets_file=client_secrets_file,
  scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'openid'],
  redirect_uri='http://localhost:8000/callback'
)

def login_required(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    # TODO Check if NOT logged in using a more secure method, also implement tracking for custom login
    # Right now only checks if google is in the session - vulnerable to attack
    if "google" not in session:  
      return jsonify({'message': 'You are not logged in'}), 401
    else:
      return f(*args, **kwargs)
  return wrapper

# @auth_bp.route('/login/google')
# def login():
#   authorization_url, state = flow.authorization_url()
#   session["state"] = state
#   return redirect(authorization_url)

# @auth_bp.route('/callback')
# def callback():
#   flow.fetch_token(authorization_response=request.url)

#   if not session["state"] == request.args["state"]:
#     return jsonify({'error': 'State does not match'})
  
#   credentials = flow.credentials
#   request_session = requests.session()
#   cached_session = cachecontrol.CacheControl(request_session)
#   token_request = google.auth.transport.requests.Request(session=cached_session)

#   id_info = id_token.verify_oauth2_token(id_token=credentials._id_token, request=token_request, audience=current_app.config['GOOGLE_CLIENT_ID'])
#   session["google_id"] = id_info.get('sub') # Sets session variable
#   return jsonify({'message': 'User logged in'}) # TODO: Redirect to home page or page where user logged in

# @auth_bp.route('/logout')
# def logout():
#   session.clear()
#   return jsonify({'message': 'You have logged out'}) # TODO: redirect to home page or page where user logged out