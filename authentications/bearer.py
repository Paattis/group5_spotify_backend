from flask import jsonify
from flask_httpauth import HTTPTokenAuth


auth = HTTPTokenAuth(scheme='Bearer')

# Register authentication callback
@auth.verify_token
def verify_token(token):
    DEV_TOKEN = 'TOKEN'
    return token == DEV_TOKEN
    # TODO Add some real authentication logic.


# Register error callback
@auth.error_handler
def auth_error(status):
    return jsonify({'message': 'gtfo'}), status
