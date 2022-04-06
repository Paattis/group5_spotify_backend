"""Summary

Attributes:
    AUTH_BASE_URL (TYPE): Description
    BASE_URL (TYPE): Description
    CLIENT_ID (TYPE): Description
    CLIENT_SECRET (TYPE): Description
    REDIRECT_URI (TYPE): Description
"""
import requests
import base64
import os
import json
import pprint
from datetime import datetime, timedelta
from db.models import AccessToken
from db import db
from sqlalchemy.orm import Session
from sqlalchemy import desc

from spotipy import CacheHandler

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET= os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SPOTIPY_AUTH_BASE_URL = os.getenv("SPOTIPY_AUTH_BASE_URL")
SPOTIPY_BASE_URL = os.getenv("SPOTIPY_BASE_URL")


class SpotifyApi(CacheHandler):
  """a class for connecting to the Spotify API
  
  Attributes:
      access_token (string): the latest access_token for the API
      lastTokenUpdate (datetime): the datetime when the token was last updated
      tokenExpireTime (datetime): the datetime when the token will/has expire(d)
  """
  def __init__(self):
    self.access_token = None
    self.lastTokenUpdate = None
    self.tokenExpireTime = None
    super().__init__()


  def save_token_to_cache(self, token_info):
    print("TOKEN INFO", token_info)
    pass

  def get_access_token(self, as_dict=True):
    return self.get_cached_token(as_dict)

  def get_cached_token(self, as_dict=True):
    """Checks if the current access token is valid/we have one
       gets a new access token if necessary
    Returns:
        string: the access token for the Spotify API
    """

    token = AccessToken.query.filter(
      AccessToken.expire_time>datetime.now()+timedelta(seconds=60)
    ).order_by(desc(AccessToken.id)).first()
    if token:
      self.access_token = token.access_token
      self.tokenExpireTime = token.expire_time

    print("Tokens found", token)

    if not token or (datetime.now() >= self.tokenExpireTime):
      requestCode = base64.b64encode(f'{SPOTIPY_CLIENT_ID}:{SPOTIPY_CLIENT_SECRET}'.encode("utf-8"))
      print("id %s secret: %s"%(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))
      print(list(SPOTIPY_CLIENT_ID))
      headers = {
        "Authorization": "Basic "+requestCode.decode("utf-8"),
        "Content-Type": "application/x-www-form-urlencoded"
      }
      pp = pprint.PrettyPrinter(indent=4)
      print("HEADERS",headers)

      r = requests.post(os.path.join(SPOTIPY_AUTH_BASE_URL, "api/token"), headers=headers, data={"grant_type": "client_credentials"})
      data = r.json()
      print("data", data)
      self.access_token = data["access_token"]
      self.tokenExpireTime = datetime.now() + timedelta(seconds=data["expires_in"])
      print("Returning data", data)
      newToken = AccessToken(access_token=self.access_token, expire_time=self.tokenExpireTime)
      #db.session.add(newToken)
      #db.session.commit()
      print("Returning token", data)
      return data if as_dict else data["access_token"]

    expire_seconds = (token.expire_time - datetime.now()).total_seconds
    return_dict = {'access_token': self.access_token, 'expires_in': expire_seconds, token_type: 'bearer'}
    print("Returning data from db", return_dict)
    return return_dict if as_dict else self.access_token


  @property
  def accessToken(self):
    """a convenience property
    
    Returns:
        string: the access token
    """
    return self.getAccessToken()

  
  """API endpoints"""
  def searchArtists(self, artistName):
    """Searches the Spotify API for artists with
    the given name
    
    Args:
        artistName (string): Description
    
    Returns:
        List<Dictionary>: the representation of the search results 
    """
    try: 
      resp = requests.get(
        BASE_URL+"search",
        params={
          "q": artistName,
          "type": ["artist"],
        },
        headers={
          "Authorization": "Bearer {}".format(self.accessToken)
        }  
      )
      return resp.json()
    except Exception as e:
      print("API ERROR", e)
      return None

  def getArtistTopTracks(self, artistId):
    """Gets the top tracks for the artist with the corresponding id  
       
    Args:
        artistId (string): the Spotify artist id for the artist
    
    Returns:
        List<Dictionary>: the list of the tracks
    """
    try:
      resp = requests.get(
        BASE_URL+"artists/{}/top-tracks".format(artistId),
        params={
          "market":"FI"
        },
        headers={
          "Authorization": "Bearer {}".format(self.accessToken)
        }  
      )
      print("resp",resp)
      return resp.json()

    except Exception as e:
      print("API ERROR", e)
      return None
