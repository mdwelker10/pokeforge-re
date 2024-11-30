from flask import Blueprint, current_app, jsonify
from server.utils.utils import login_required

test_bp = Blueprint('test_bp', __name__)

@test_bp.route('/', methods=['GET'])
def hello_world():
    current_app.logger.critical('Hello, World!')
    current_app.logger.error('Hello, World!')
    current_app.logger.warning('Hello, World!')
    current_app.logger.info('Hello, World!')
    current_app.logger.debug('Hello, World!')
    return jsonify({'message': 'Hello, World!'}), 200


@test_bp.route('/auth', methods=['GET'])
@login_required
def auth():
    return jsonify({'message': 'You are authenticated! yay!'})