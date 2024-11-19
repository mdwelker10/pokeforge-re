import random
import traceback

from argon2 import PasswordHasher
from server.data.models.user import User
from server.db.db import exec
from server.utils.api_exception import APIException

ph = PasswordHasher()

# TODO: Add logging for new user creation - both methods
def create_user(username, password):
  """Create a new user with the given username and password. Returns new user DTO"""
  # Ensure username is not taken. Check separately to provide better error message
  if exec("SELECT * FROM user WHERE username=?", (username,), 'fetchone') is not None:
    raise APIException(400, 'This username is already taken')
  hashed_password = ph.hash(password)
  id = exec("INSERT INTO user (username, password) VALUES (?, ?)", (username, hashed_password), 'lastrowid')
  return User(id=id, username=username).to_dto()


def google_login(email, google_id):
  """If no user with this email exists, create a new user with the given email and Google ID. Otherwise validate the user. Returns user DTO"""
  
  user = exec("SELECT * FROM user WHERE googleid=?", (google_id,), 'fetchone')
  # Account with Google ID found if true
  if user is not None:
    return User.from_obj(user).to_dto()

  # Account with Google ID not found, check if email is already in use
  user = exec("SELECT * FROM user WHERE email=?", (email,), 'fetchone')
  # Account with email found if true, link Google ID to account
  if user is not None:
    #TODO Handle this later, right now manually setting email is not implemented
    raise APIException(400, 'email already in use, please log in manually')
  
  # No account with Google ID or email found, create a new one
  # Attempt to use just gmail as username (excluding @gmail.com)
  username = email.split('@')[0]
  if exec("SELECT * FROM user WHERE username=?", (username,), 'fetchone') is not None:
    # If gmail username is taken then add random numbers until a non-taken username is found
    # TODO: Just make a separate screen to select a username 
    while True:
      username = email.split('@')[0] + '_' + str(random.randint(1, 9999))
      if exec("SELECT * FROM user WHERE username=?", (username,), 'fetchone') is None:
        break
  id = exec("INSERT INTO user (username, googleid, email) VALUES (?, ?, ?)", (username, google_id, email), 'lastrowid')
  return User(id=id, username=username, googleid=google_id, email=email).to_dto()


def validate_user(username, password):
  """Validate a user given the typed in username and password. Returns user DTO"""
  user = exec("SELECT * FROM user WHERE username=?", (username,), 'fetchone')
  # If username does not exist
  # TODO set up logging - invalid attempts for both username and password
  if user is None:
    raise APIException(400, 'Incorrect username or password')
  try:
    ph.verify(user['password'], password) 
    # Check if the password needs to be rehashed, such as an update to the default parameters
    if ph.check_needs_rehash(user['password']):
      # Update the password hash with the new algorithm
      new_hash = ph.hash(password)
      exec("UPDATE user SET password=? WHERE id=?", (new_hash, user['id']), 'lastrowid')
    return User.from_obj(dict(user)).to_dto()
  except Exception as e:
    traceback.print_exc()
    raise APIException(400, 'Incorrect username or password')