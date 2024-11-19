import os

from dotenv import load_dotenv

load_dotenv()
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # TODO: Remove this line in production - allows for testing on http

# Set env variables to be accessed via the config object
class Config:
    # Non-secret variables
    JWT_ALGO='ES256'
    JSON_SORT_KEYS = False # Speed up jsonify
    JWT_COOKIE_NAME = 'pokeforge_re_login'

    # Secret variables stored in .env
    FLASK_SECRET = os.getenv("FLASK_SECRET")
    GOOGLE_SECRET = os.getenv("GOOGLE_SECRET")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    DATABASE_FILE = os.getenv("DATABASE_FILE")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ES256_KEY = os.getenv("ES256_KEY")
    ES256_KID = os.getenv("ES256_KID") # TODO: Update this stuff bc you used the website to generate it. Use a cmd tool or something