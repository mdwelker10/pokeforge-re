from flask import Blueprint, jsonify
from routes.auth import login_required

test_bp = Blueprint('test_bp', __name__)

@test_bp.route('/', methods=['GET'])
def hello_world():
    return "Hello, World!"


@test_bp.route('/auth', methods=['GET'])
@login_required
def auth():
    return jsonify({'message': 'You are authenticated! yay!'})