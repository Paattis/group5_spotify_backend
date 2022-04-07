from flask import Flask
import sys
import db
from classes import DatabaseTokenCacheHandler
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os
import json

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


@app.route('/songs/search/<searchTerm>')
def search_song(searchTerm: str):
    """Searches for songs with the search term from the Spotify API and returns them
    
    Args:
        searchTerm (str): the search term
    
    Returns:
        dict: the search results 
    """

    auth_manager = DatabaseTokenCacheHandler()

    sp = spotipy.Spotify(auth_manager=auth_manager)
    dat = sp.search(q=searchTerm, limit=50, type=['track'],market='FI')

    return dat.get('tracks')