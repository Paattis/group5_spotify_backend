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
    import spotipy
    import os
    from spotipy.oauth2 import SpotifyClientCredentials
    print("id", os.getenv("SPOTIPY_CLIENT_ID"))
    print("id", os.getenv("SPOTIPY_CLIENT_SECRET"))
    auth_manager = SpotifyApi()
    #print(SpotifyClientCredentials().get_access_token())
    #auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    dat = sp.search(q='pitbull', market='FI')

    #SpotifyApi().get_cached_token()
    return dat