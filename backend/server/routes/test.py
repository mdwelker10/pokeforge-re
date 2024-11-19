from flask import Blueprint, jsonify
from server.utils.utils import login_required

test_bp = Blueprint('test_bp', __name__)

@test_bp.route('/', methods=['GET'])
def hello_world():
    return jsonify({'message': 'Hello, World!'}), 200


@test_bp.route('/auth', methods=['GET'])
@login_required
def auth():
    return jsonify({'message': 'You are authenticated! yay!'})