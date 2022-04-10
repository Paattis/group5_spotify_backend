from flask import Flask, Response
import sys
import db
from db.models import Location, Song
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

@app.route('/location/<name>', methods=['POST',])
@app.errorhandler(500)
def add_location(name: str):
  """Adds a location to the database and returns the id.
  If the location already exists, return it instead

  Args:
      name (str): The name of the location

  Returns:
      dict: the representation of the location object
  """
  import re

  # sanitize the string a bit, remove all non-alphanumeric
  # characters from the beginning and the end of the string
  # and also turn it into title case (e.g. 'helsinki-vAnTaa' -> 'Helsinki-Vantaa')
  name = re.sub(r'(^\W+|\W+$)', '', name.title())

  location = Location.query.filter(
    Location.name==name
  ).first()

  if not location:
    # if the location wasn't found, create a new one
    try:
      location = Location(name=name)
      db.db.session.add(location)
      db.db.session.commit()
    except Exception as e:
      return {'msg': 'Something went wrong when saving location to the database'}, 500

  return location.to_dict()


@app.route('/location/<location_id>/')
@app.errorhandler(404)
def get_location(location_id: int):
  """Returns the location with the corresponding id

  Args:
      location_id (int): the id of the location

  Returns:
      dict: The corresponding location
  """
  location = Location.query.filter(
    Location.id==location_id
  ).first()

  if not location:
    return {'msg': 'Location not found'}, 404


  return {'songs': location.to_dict()}


@app.route('/location/<location_id>/songs/<song_id>', methods=['POST',])
@app.errorhandler(500)
@app.errorhandler(404)
@app.errorhandler(400)
def add_location_song(location_id: int, song_id: int):
    """Adds a song to a location after validating that both
    the location and the song exist.
    
    Args:
        location_id (int): the id of the location in the database
        song_id (int): the id of the song in the database
    """

    # check if the location exists in the database
    location = Location.query.filter(
      Location.id==location_id
    ).first()

    if not location:
      return {'msg': 'Location not found'}, 404

    # check if the song exists
    song = Song.query.filter(
      Song.id==song_id
    ).first()

    if not song:
      return {'msg': 'Song not found'}, 404

    if song in location.songs:
      return {'msg': 'Song already in location\'s songs'}, 400

    try:
      location.songs.append(song)
      db.db.session.commit()
    except Exception as e:
      return {'msg': 'Something went wrong when adding a song to the location'}, 500

    return {'msg': 'Song added successfully'}



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
    data = sp.search(q=searchTerm, limit=50, type=['track'],market='FI')

    return data.get('tracks')

