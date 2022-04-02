from flask import Flask, jsonify
from authentications import auth
from db import settings

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/auth/test')
@auth.bearer_token
def auth():
    return jsonify({'message': 'You may enter'})

@app.route("/")
def index():
    return "index"

