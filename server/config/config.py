import os

from dotenv import load_dotenv

load_dotenv()
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # Remove this line in production - allows for testing on http

# Set env variables to be accessed via the config object
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    GOOGLE_SECRET = os.getenv("GOOGLE_SECRET")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    JSON_SORT_KEYS = False # Speed up jsonify
    DATABASE_FILE = os.getenv("DATABASE_FILE")