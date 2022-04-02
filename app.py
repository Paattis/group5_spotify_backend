from flask import Flask
import db


app = Flask(__name__)
app.secret_key = 'DEV'
# TODO: Better configs

# Setup SQLAlchemy
database, migrate = db.init_app(app)

@app.route("/")
def index():
    return "index"