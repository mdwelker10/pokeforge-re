import traceback
from functools import wraps
from urllib.parse import unquote

from flask import current_app, jsonify, request
from server.routes.authentication.jwt import verify_jwt
from server.utils.api_exception import APIException


def handle_api_errors(f):
  """Decorator used to catch exceptions in API routes and return a JSON response"""
  @wraps(f)
  def wrapper(*args, **kwargs):
      try:
          return f(*args, **kwargs)
      except APIException as e:
          # traceback.print_exc() # remove for production
          return jsonify({'error': e.message}), e.code
      except Exception as e:
          traceback.print_exc()
          current_app.logger.error(str(e))
          return jsonify({'error': 'An unexpected error occurred'}), 500
  return wrapper


# Method used to validate login on protected routes
def login_required(f):
  """Decorator used to check if user is logged in. Place on all protected routes"""
  @wraps(f)
  def wrapper(*args, **kwargs):
    token = request.cookies.get(current_app.config['JWT_COOKIE_NAME'])
    token = unquote(token) if token else None
    # If token not in cookie check if it is in the Authorization header
    if not token:
      header = request.headers.get('Authorization')
      if header and header.startswith('Bearer '):
        token = header.split('Bearer ')[1]
      else:
        # No token provided
        return jsonify({'error': 'Unauthorized'}), 401
    try:
      payload = verify_jwt(token)
      request.user = payload['sub']
    except APIException as e:
      # In case token verification fails
      return jsonify({'error': e.message}), e.code
    return f(*args, **kwargs)
  return wrapper
    
