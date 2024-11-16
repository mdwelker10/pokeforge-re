from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE"]) # change origins for production

@app.route('/api/test', methods=['GET'])
def hello_world():
    return "Hello, World!"