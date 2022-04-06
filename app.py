from flask import Flask
import sys
import db
from classes import SpotifyApi

app = Flask(__name__)
app.secret_key = 'DEV'
# TODO: Better configs

# add modules to path for easy access
module_path = [
  'db',
]

for path in module_path:
  sys.path.append(path)


# Setup SQLAlchemy
database, migrate = db.init_app(app)


@app.route("/")
def index():
    return "index"