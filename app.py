from flask import Flask
import db

app = Flask(__name__)
app.secret_key = 'DEV'
database, migrate = db.init_app(app)

@app.route("/")
def index():
    return "index"