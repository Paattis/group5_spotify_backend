from flask import Flask, Response
from flask_caching import Cache

import sys
import db
from db.models import Location, LocationSong, Song
from classes import DatabaseTokenCacheHandler
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os
import json
from dotenv import load_dotenv

from classes import Messages

def create_app(test_config=None):
  load_dotenv()

  config = {
      'CACHE_TYPE': 'SimpleCache',  # Flask-Caching related configs
      'CACHE_TRESHOLD': int(os.getenv('FLASK_CACHE_TRESHOLD')),
      'CACHE_DEFAULT_TIMEOUT': int(os.getenv('FLASK_CACHE_TIMEOUT')),
  }

  # if running in production, enable file system cache
  if os.getenv('FLASK_ENV') != 'development':
    config['CACHE_TYPE'] = 'FileSystemCache'
    config['CACHE_DIR'] = os.getenv('FLASK_CACHE_DIR')


  app = Flask(__name__)
  app.secret_key = os.getenv('FLASK_SECRET_KEY')
  # TODO: Better configs

  app.config.from_mapping(config)
  cache = Cache(app)

  # add modules to path for easy access
  module_path = [
    'db',
  ]

  for path in module_path:
    sys.path.append(path)


  # Setup SQLAlchemy
  database, migrate = db.init_app(app)

  @app.route('/favicon.ico')
  def favicon():
    """an empty route for favicon.ico
    returns a 200 to prevent a 404 error from being handled when accessing
    from the browser
    Returns:
        str: an empty string
    """
    return ""

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
        return {'msg': Messages.codes.ERR_LOCATION_SAVE_500, 'verbose': Messages.ERR_LOCATION_SAVE_500}, 500

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
      return {'msg': Messages.codes.ERR_LOCATION_404, 'verbose': Messages.ERR_LOCATION_404}, 404


    # annotate data with local popularity of the songs
    # not a good way to do this, don't do this
    # (were gonna do it anyway)

    # TODO: move to separate function and use caching to prevent constant db hits and speed 
    # response times
    location_songs = LocationSong.query.filter(
      LocationSong.location_id==location.id
    )

    # make song_id: song_local_popularity for easier access
    song_ids = dict([(lso.song_id, lso.weighted_popularity()) for lso in location_songs])

    # convert the location object to a dictionary form that will be returned
    location_dict = location.to_dict()

    # add an extra property "song_local_popularity" to each song
    for song in location_dict.get('songs'):
      local_popularity = song.get('id', 0)
      song['song_local_popularity'] = song_ids.get(local_popularity or 0)


    return {'songs': location_dict}


  @app.route('/location/<location_id>/songs/<spotify_id>', methods=['POST',])
  @app.errorhandler(500)
  @app.errorhandler(404)
  @app.errorhandler(400)
  def add_location_song(location_id: int, spotify_id: str):
      """Adds a song to a location after validating that both
      the location and the song exist.
      
      Args:
          location_id (int): the id of the location in the database
          spotify_id (str): the id of the song in the spotify API
      """

      # check if the location exists in the database

      location = Location.query.filter(
        Location.id==location_id
      ).first()

      if not location:
        return {'msg': Messages.codes.ERR_LOCATION_404, 'verbose': Messages.ERR_LOCATION_404}, 404

      # check if the song exists
      song = Song.query.filter(
        Song.spotifyId==spotify_id
      ).first()

      if not song:
        # song doesn't exist, fetch it from the Spotify API and add
        # it to the db
        auth_manager = DatabaseTokenCacheHandler()
        sp = spotipy.Spotify(auth_manager=auth_manager)
        

        from spotipy.exceptions import SpotifyException
        try:
          song_data = sp.track(spotify_id, market='FI')
        except SpotifyException:
          # song doesn't exist
          return {'msg': Messages.codes.ERR_SONG_SPOTIFY_ID_500, 'verbose': Messages.ERR_SONG_SPOTIFY_ID_500}, 500


        try:
          # add song to database if it exists
          album = song_data.get('album')

          # get the desired thumbnail's url, default to the largest if not found
          desired_thumb_size = 300
          try:
            album_thumb = filter(
              lambda x: x.get('width') == desired_thumb_size,
              album.get('images')
            )
            album_thumb = list(album_thumb)[0]
          except IndexError as e:
            # fall back to the largest
            album_thumb = album.get('images').sort(lambda x:-x['width'])

          song = Song(
            name=song_data.get('name'),
            spotifyId=spotify_id,
            artist=', '.join([a['name'].title() for a in song_data.get('artists')]),
            album_name=album.get('name'),
            album_thumb=album_thumb.get('url')
          )
          db.db.session.add(song)
          db.db.session.commit()
        except Exception as e:
          return {'msg': Messages.codes.ERR_SONG_LOCATION_SAVE_500, 'verbose': Messages.ERR_SONG_LOCATION_SAVE_500}, 500


      if song in location.songs:

        #db.db.session.commit()
        # get the row from the intermediate table
        location_song = LocationSong.query.filter(
          LocationSong.song_id==song.id,
          LocationSong.location_id==location.id
        ).first()

        if not location_song.song_local_popularity:
          location_song.song_local_popularity = 0

        location_song.song_local_popularity += 1
        song.popularity += 1

        db.db.session.commit()
        #import ipdb;ipdb.set_trace()
        #db.db.session.commit()
        return {'msg': Messages.codes.SONG_ALREADY_ADDED, 'verbose': Messages.SONG_ALREADY_ADDED}



      try:
        location_song = LocationSong(song_id=song.id, location_id=location.id)
        s = db.db.session.add(location_song)
        db.db.session.commit()
      except Exception as e:
        return {'msg': Messages.codes.ERR_LOCATION_SAVE_500, 'verbose': Messages.ERR_LOCATION_SAVE_500}, 500

      return {'msg': Messages.codes.SONG_ADD_SUCCESS, 'verbose': Messages.SONG_ADD_SUCCESS}



  @app.route('/songs/search/<searchTerm>')
  @cache.cached()
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

  return app