from flask import Flask, jsonify
from flask_httpauth import HTTPTokenAuth
from db import settings

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

######### Authentication ###########
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

# Authentication example for route
@app.route('/auth/test')
@auth.login_required # <-- Auth decorator for secret routes
def auth():
  return jsonify({'message': 'You may enter'})

@app.route("/")
def index():
  return "index"

