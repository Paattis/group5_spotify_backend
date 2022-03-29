from flask import Flask

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

from db import settings

@app.route("/")
def index():
  return "index"