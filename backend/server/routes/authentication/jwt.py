import base64
import json
import time

import jwt
from flask import current_app
from jwt.algorithms import ECAlgorithm
from server.utils.api_exception import APIException


def load_ES256_key():
  """Loads the ES256 private key from the environment"""
  algo = ECAlgorithm(current_app.config['JWT_ALGO'])
  key = current_app.config['ES256_KEY']
  encoded_key = base64.b64decode(key)
  json_key = json.loads(encoded_key)
  ES256_key = algo.from_jwk(json_key.get("keys")[0])
  return ES256_key

def create_jwt(sub):
  """Create a new JWT token with the given sub. sub is username"""

  payload = {
    'exp': int(time.time()) + (60 * 60 * 3), # 3 hours
    'iat': int(time.time()),
    'scope': 'access_token',
    'sub': sub
  }
  signing_key = load_ES256_key()
  return jwt.encode(payload, signing_key, algorithm=current_app.config['JWT_ALGO'], headers={'kid': current_app.config['ES256_KID']})

def verify_jwt(token):
  """Verify that a JWT token is legitimate and return the decoded payload"""
  try:
    pub_key = load_ES256_key().public_key() # Get the public key for decoding
    decoded = jwt.decode(token, pub_key, algorithms=[current_app.config['JWT_ALGO']])
    return decoded
  except jwt.ExpiredSignatureError:
    raise APIException(401, 'Token has expired')
  except jwt.InvalidTokenError:
    raise APIException(401, 'Invalid token')

# TODO idk how to implement refresh tokens properly and securely lol
# def create_refresh_token(sub):
#   """Create a refresh token that can be used to get a new access token without logging in again."""
#   payload = {
#     'exp': datetime.now() + timedelta(hours=24),
#     'iat': datetime.now(),
#     'scope': 'refresh_token',
#     'sub': sub
#   }
#   signing_key = load_ES256_key()
#   return jwt.encode(payload, signing_key, algorithm=current_app.config['JWT_ALGO'], headers={'kid': current_app.config['ES256_KID']})

# def refresh_token(refresh_token):
#   """Refresh an expired access token with a valid refresh token"""
#   try:
#     pub_key = load_ES256_key().public_key() # Get the public key for decoding
#     payload = jwt.decode(refresh_token, pub_key, algorithms=[current_app.config['JWT_ALGO']])
#     if payload['scope'] == 'refresh_token':
#       return create_jwt(payload['sub'])
#     raise APIException(401, 'Invalid scope for token')
#   except jwt.ExpiredSignatureError:
#     raise APIException(401, 'Token has expired')
#   except jwt.InvalidTokenError:
#     raise APIException(401, 'Invalid token')
  
